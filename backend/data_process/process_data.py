import json
import os
import mmap
import time
import argparse
import couchdb
import requests

from tqdm import tqdm
from mpi4py import MPI

from backend.database.couch_api import CouchAPI
from backend.data_process.phn_api import PHNAPI

# from backend.nlp import get_abusive_scores, compute_cross_scores, get_sentiment_scores

# MPI settings
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = comm.Get_size()

argparser = argparse.ArgumentParser()
argparser.add_argument('--twitter_json_path', type=str,
                       default='backend/twitter-huge.json/mnt/ext100/twitter-huge.json')
argparser.add_argument('--phn_memory_file', type=str, default='backend/data_process/phn_memory.json')
argparser.add_argument('--db_name', type=str, default='raw_tweets_processed_3')
argparser.add_argument('--server_url', type=str, default='http://192.168.0.80:5984/')
argparser.add_argument('--batch_size', type=int, default=1_000)
args = argparser.parse_args()

phn_memory_file = args.phn_memory_file
db_name = args.db_name
server_url = args.server_url
couch_api = CouchAPI(server_url, username='admin', password='admin')

nlp_host = '127.0.0.1'
nlp_port = 8000

if rank == 0:
    try:
        db = couch_api.create(db_name)
    except couchdb.http.PreconditionFailed:
        pass
    print(f'Rank: {rank} Create database, db_name: {db_name}')

time.sleep(1)
print(f'Rank: {rank} Waiting for database to be created')
comm.Barrier()
db = couch_api[db_name]


def seek_end_of_line(mmap_obj: mmap.mmap, start_offset: int, end_offset: int):
    return mmap_obj.find(b'\r\n', start_offset, end_offset) + 2


def get_file_size(twitter_json_path: str):
    return os.stat(twitter_json_path).st_size


def get_json_line(byte_text: bytes):
    return byte_text.decode('utf8').rstrip(',\r\n')


phn_api = PHNAPI(phn_memory_file)


def handle_tweet(item):
    try:
        if item['doc']['data']['sentiment'] == 0:
            return None

        bbox = item['doc']['includes']['places'][0]['geo']['bbox']
        phn = phn_api.get_phn_by_bbox(bbox)
        if phn is None:
            return None

        tweet = {
            '_id': item['id'],
            'author_id': item['doc']['data']['author_id'],
            'created_at': item['doc']['data']['created_at'],
            'geo': phn,
            'lang': item['doc']['data']['lang'],
            'sentiment': item['doc']['data']['sentiment'],
            'tokens': item['value']['tokens'],
            'text': item['doc']['data']['text'],
        }
        return tweet
    except (AttributeError, KeyError, TypeError):
        return None


def nlp_req(query, doc=None, path='/get_abusive_scores'):
    req_data = {'query': query}
    if doc is not None:
        req_data = {'query': query, 'doc': doc}
    req_url = f'http://{nlp_host}:{nlp_port}' + path
    response = requests.post(req_url, json=req_data, headers={
        'Content-Type': 'application/json'
    })
    if response.status_code != 200:
        raise Exception(f'NLP request failed, status_code: {response.status_code}, text: {response.text}')

    return json.loads(response.text).get('score')


def process_scores(items):
    texts = [item['text'] for item in items]
    abusive_scores = nlp_req(texts, path='/get_abusive_score')
    sentiment_scores = nlp_req(texts, path='/get_sentiment_score')
    cross_scores = nlp_req('homeless', texts, path='/get_score')
    for i, item in enumerate(items):
        item['abusive_score'] = float(abusive_scores[i])
        item['sentiment_score'] = float(sentiment_scores[i])
        item['cross_score'] = float(cross_scores[i])
    return items


def process(twitter_json_path='data/twitter-huge.json', batch_size=1_000):
    start_time = time.time()
    file_size = get_file_size(twitter_json_path)
    block_size = int(file_size / world_size)
    start_offset = rank * block_size if rank != 0 else 0
    end_offset = (rank + 1) * block_size if rank != world_size - 1 else file_size

    f = open(twitter_json_path, 'rb')
    mmap_obj = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)

    real_start_offset = seek_end_of_line(mmap_obj, start_offset, start_offset + 5000)
    search_start = end_offset if rank != world_size - 1 else file_size - 100
    search_end = min(end_offset + 5000, file_size)
    real_end_offset = seek_end_of_line(mmap_obj, search_start, search_end)

    line_count = 0
    pbar_rank = 0
    jsons = []
    total_bytes = real_end_offset - real_start_offset

    if rank == pbar_rank:
        pbar = tqdm(
            total=100, unit='%', smoothing=0.3,
            bar_format='{percentage:.0f}%|{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
        )

    mmap_obj.seek(real_start_offset)
    tell = mmap_obj.tell()
    while tell < real_end_offset:
        byte_text = mmap_obj.readline()
        new_tell = mmap_obj.tell()

        byte_text = byte_text.rstrip(b',\r\n')
        item = json.loads(byte_text)

        new_tweet = handle_tweet(item)

        if new_tweet is not None:
            jsons.append(new_tweet)
            if len(jsons) >= batch_size:
                processed = process_scores(jsons)
                db.save_batch(processed)
                jsons = []

        if rank == pbar_rank:
            pbar.update((new_tell - tell) / total_bytes * 100)

        tell = new_tell
        line_count += 1
    processed = process_scores(jsons)
    db.save_batch(processed)

    if rank == pbar_rank:
        pbar.close()

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Rank: {rank}, per_time: {total_time / line_count}, line_count: {line_count}')

    mmap_obj.close()
    f.close()

    comm.Barrier()

    all_line_count = comm.reduce(line_count, op=MPI.SUM, root=0)
    all_time = comm.reduce(total_time, op=MPI.SUM, root=0)

    if rank == 0:
        print(f'All_line_count: {all_line_count}')
        print(f'All_time: {all_time}')
        print(f'Per_time: {all_time / all_line_count}')


def main():
    process(args.twitter_json_path, args.batch_size)


if __name__ == '__main__':
    main()
