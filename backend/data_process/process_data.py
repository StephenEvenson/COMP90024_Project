#
# Part of Assignment 2 - COMP90024
#
# Cluster and Cloud Computing - Team 72
#
# Authors:
#
#  - Juntao Lu (Student ID: 1290513)
#  - Runtian Zhang (Student ID: 1290379)
#  - Jiahao Shen (Student ID: 1381187)
#  - Yuchen Liu (Student ID: 1313394)
#  - Jie Shen (Student ID: 1378708)
#
# Location: Melbourne
#
import json
import os
import mmap
import time
import argparse
import couchdb
import requests

from tqdm import tqdm
from mpi4py import MPI
import pandas as pd
from profanity_check import predict

from backend.data_process.sal_api import SALAPI
from backend.database.couch_api import CouchAPI
from backend.data_process.phn_api import PHNAPI

from backend.data_process.label import get_label_sim

nlp_port = os.environ.get('NLP_PORT')
nlp_host = os.environ.get('NLP_HOST')
json_path = os.environ.get('JSON_PATH')
write_db_host = os.environ.get('WRITE_DB_HOST')
write_db_port = os.environ.get('WRITE_DB_PORT')

# from backend.nlp.search_interface import compute_embedding
# from backend.nlp.abusive_interface import get_abusive_score

# MPI settings
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = comm.Get_size()

argparser = argparse.ArgumentParser()
argparser.add_argument('--json_path', type=str, default=json_path)
argparser.add_argument('--db_name', type=str, default='twitter')
argparser.add_argument('--sa4_file', type=str, default='backend/data/sa4.csv')
argparser.add_argument('--sal_json_file', type=str, default='backend/data/sal.json')
argparser.add_argument('--server_url', type=str, default=f'http://{write_db_host}:{write_db_port}/')
argparser.add_argument('--phn_memory_file', type=str, default='backend/data_process/phn_memory.json')
argparser.add_argument('--batch_size', type=int, default=1000)
args = argparser.parse_args()

phn_memory_file = args.phn_memory_file
sal_json_file = args.sal_json_file
sa4_file = args.sa4_file
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


# def merge_text_files(input_files, output_file):
#     with open(output_file, 'w') as output:
#         for file in input_files:
#             with open(file, 'r') as input_file:
#                 output.write(input_file.read())



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


phn_api = PHNAPI(phn_memory_file)
sal_api = SALAPI(sal_json_file)
df = pd.read_csv(sa4_file)


def handle_tweet(item):
    try:
        text = item['doc']['data']['text']
        # emb = compute_embedding(text)
        # abusive_score = get_abusive_score(text)

        # bbox = item['doc']['includes']['places'][0]['geo']['bbox']
        # phn = phn_api.get_phn_by_bbox(bbox)
        # if phn is None:
        #     return None

        full_name = item['doc']['includes']['places'][0]['full_name']
        name = full_name.split(',')[0].strip().lower()
        gcc = sal_api.get_gcc_by_name(name)
        # if gcc is None:
        #     return None

        df['SA4_NAME_2016'] = df['SA4_NAME_2016'].str.lower()
        df_filtered = df[df['SA4_NAME_2016'] == name]['SA4_CODE_2016']
        sa4_code = df_filtered.values[0] if not df_filtered.empty else None
        # if sa4_code is None:
        #     return None

        abusive_score = predict([text])[0].item()
        # assert type(abusive_score) == type(1)
        # print(type(abusive_score).item())

        tweet = {
            '_id': item['id'],
            'author_id': item['doc']['data']['author_id'],
            'created_at': item['doc']['data']['created_at'],
            'geo': item['doc']['data'].get('geo', {}),
            'lang': item['doc']['data']['lang'],
            'geo_gcc': str(gcc),
            'geo_sa4': str(sa4_code),
            # 'geo_phn': str(phn),
            'sentiment': item['doc']['data']['sentiment'],
            'tokens': item['value']['tokens'],
            'text': item['doc']['data']['text'],
            'public_metrics': item['doc']['data']['public_metrics'],
            # 'embedding': emb.tolist(),
            'abusive_score': abusive_score
        }
        return tweet
    except (AttributeError, KeyError, TypeError):
        return None


def process_batch(batch_data):
    sims = [get_label_sim(item['text']) for item in batch_data]
    precessed = []
    for i, item in enumerate(batch_data):
        sim = sims[i]
        for score_item in sim:
            item[score_item['label']] = score_item['score']
        precessed.append(item)
    return precessed


def attach_jsonl_file(jsonl_path, jsons):
    with open(jsonl_path, 'a') as f:
        for j in jsons:
            f.writelines(json.dumps(j) + '\n')


# def creat_jsonl_file():
#     for i in range(world_size):
#         path = f'data/{db_name}_{i}.jsonl'
#         if os.path.exists(path):
#             print(f'Delete exist file: {path}')
#             os.remove(path)
#         with open(f'data/{db_name}_{i}.jsonl', 'w') as f:
#             pass
#         print(f'Create file: {path}')
#     with open(f'data/{db_name}_merged.jsonl', 'w') as f:
#         pass
#     print(f'Create file: data/{db_name}_merged.jsonl')


def process(json_path='/data/twitter-huge.json', batch_size=1_000):
    # if rank == 0:
    #     creat_jsonl_file()

    comm.Barrier()

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

        if new_tweet is not None:
            jsons.append(new_tweet)
            if len(jsons) >= batch_size:
                handeled = process_batch(jsons)
                # attach_jsonl_file(f'data/{db_name}_{rank}.jsonl', handeled)
                db.save_batch(handeled)
                jsons = []

        if rank == pbar_rank:
            pbar.update((new_tell - tell) / total_bytes * 100)

        tell = new_tell
        line_count += 1

    handeled = process_batch(jsons)
    # attach_jsonl_file(f'data/{db_name}_{rank}.jsonl', handeled)
    db.save_batch(handeled)

    if rank == pbar_rank:
        pbar.close()

    end_time = time.time()
    total_time = end_time - start_time
    # print(f'Rank: {rank}, per_time: {total_time / line_count}, line_count: {line_count}')

    mmap_obj.close()
    f.close()

    comm.Barrier()

    all_line_count = comm.reduce(line_count, op=MPI.SUM, root=0)
    all_time = comm.reduce(total_time, op=MPI.SUM, root=0)

    # if rank == 0:
    #     input_files = [f'data/{db_name}_{i}.jsonl' for i in range(world_size)]
    #     output_file = f'data/{db_name}_merged.jsonl'
    #     merge_text_files(input_files, output_file)

    if rank == 0:
        print(f'All_line_count: {all_line_count}')
        print(f'All_time: {all_time}')
        # print(f'Per_time: {all_time / all_line_count}')


def main():
    process(args.json_path, args.batch_size)


if __name__ == '__main__':
    main()
