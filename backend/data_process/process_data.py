import json
import os
import mmap
import time
import argparse
import couchdb

from tqdm import tqdm
from mpi4py import MPI
from CouchAPI import CouchAPI

# Constants
BATCH_SIZE = 1_000
TWITTER_HUGE_JSON_PATH = '../twitter-huge.json/mnt/ext100/twitter-huge.json'
DB_NAME = 'raw_tweets_geo_2'
SERVER_URL = 'http://localhost:5984/'

# MPI settings
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = comm.Get_size()

argparser = argparse.ArgumentParser()
argparser.add_argument('--json_path', type=str, default=TWITTER_HUGE_JSON_PATH)
argparser.add_argument('--db_name', type=str, default=DB_NAME)
argparser.add_argument('--server_url', type=str, default=SERVER_URL)
argparser.add_argument('--batch_size', type=int, default=BATCH_SIZE)
args = argparser.parse_args()

db_name = args.db_name
server_url = args.server_url
couch = CouchAPI(server_url, username='admin', password='admin')

if rank == 0:
    try:
        db = couch.create(db_name)
    except couchdb.http.PreconditionFailed:
        pass
    print(f'Rank: {rank} Create database, db_name: {db_name}')

time.sleep(1)
print(f'Rank: {rank} Waiting for database to be created')
comm.Barrier()
db = couch[db_name]


def seek_end_of_line(mmap_obj: mmap.mmap, start_offset: int, end_offset: int):
    return mmap_obj.find(b'\r\n', start_offset, end_offset) + 2


def get_file_size(json_path: str):
    return os.stat(json_path).st_size


def get_json_line(byte_text: bytes):
    return byte_text.decode('utf8').rstrip(',\r\n')


def handle_tweet(item):
    tweet = {
        '_id': item['id'],
        'author_id': item['doc']['data']['author_id'],
        'created_at': item['doc']['data']['created_at'],
        'geo': item['doc']['data'].get('geo', {}),
        'lang': item['doc']['data']['lang'],
        'sentiment': item['doc']['data']['sentiment'],
        'tokens': item['value']['tokens'],
        'text': item['doc']['data']['text'],
    }
    return tweet


def process(json_path='data/twitter-huge.json', batch_size=1_000):
    start_time = time.time()
    file_size = get_file_size(json_path)
    block_size = int(file_size / world_size)
    start_offset = rank * block_size if rank != 0 else 0
    end_offset = (rank + 1) * block_size if rank != world_size - 1 else file_size

    f = open(json_path, 'rb')
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

        if new_tweet['geo'] != {}:
            jsons.append(new_tweet)
            if len(jsons) >= batch_size:
                db.save_batch(jsons)
                jsons = []

        # jsons.append(new_tweet)
        # if len(jsons) >= batch_size:
        #     db.save_batch(jsons)
        #     jsons = []

        if rank == pbar_rank:
            pbar.update((new_tell - tell) / total_bytes * 100)

        tell = new_tell
        line_count += 1

    db.save_batch(jsons)

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
    db.create_view('by_geo')

    process(args.json_path, args.batch_size)

    def query_all_data(db, view_name):
        page_number = 0
        while True:
            skip = page_number * 5
            page_results = db.query_data_from_view(view_name, limit=50, skip=skip)
            if not page_results:
                break
            for key, value in page_results:
                print(f'Key: {key}, Value: {value}')
            page_number += 1

    # Query all data
    query_all_data(db, 'by_geo')


if __name__ == '__main__':
    main()
