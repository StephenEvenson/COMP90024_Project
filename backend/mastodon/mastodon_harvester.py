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
import re
import requests

import couchdb
from mastodon import Mastodon, StreamListener

db_host = os.environ.get('WRITE_DB_HOST')
db_port = os.environ.get('WRITE_DB_PORT')
nlp_host = os.environ.get('NLP_HOST')
nlp_port = os.environ.get('NLP_PORT')
api_url = os.environ.get('API_URL')
access_token = os.environ.get('ACCESS_TOKEN')

# couchdb login data
admin = 'admin'
password = 'admin'

# connect to couchdb
url = f'http://{admin}:{password}@{db_host}:{db_port}/'
couch = couchdb.Server(url)

db_name = 'mastodon'
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# mastodon message (with url and private token)
m = Mastodon(
    api_base_url=api_url,
    access_token=access_token
)
# m = Mastodon(
#     api_base_url=api_url,
#     access_token='x8UJOO1_G6AiB_dJ29GixEidEfianC5NjLHcAMoaPzc'
# )


def nlp_req(query, doc=None, path='/get_abusive_score'):
    req_data = {'query': query}
    if doc is not None:
        req_data = {'query': query, 'doc': doc}
    req_url = f'http://{nlp_host}:{nlp_port}' + path
    response = requests.post(req_url, json=req_data, headers={
        'Content-Type': 'application/json'
    })
    return float(json.loads(response.text).get('score'))


# create listener to load the data
class Listener(StreamListener):
    def on_update(self, status):
        # if some message have some error, just print error to let the script run
        try:
            # load json element
            json_element = json.dumps(status, indent=2, sort_keys=True, default=str)
            json_single = json.loads(json_element)

            # ignore the http tag in the sentence, to extract the real words in the note.
            no_tags_string = re.sub('<.*?>', '', json_single['content'])

            # Replace Unicode line separator and paragraph separator characters
            no_special_chars_string = no_tags_string.replace(u'\u2028', ' ').replace(u'\u2029', ' ')

            # Replace HTML entities
            readable_string = no_special_chars_string.replace('&gt;', '>')

            abusive_score = nlp_req(readable_string)
            homeless_relative_score = nlp_req('homeless', readable_string, path='/get_score')
            sentiment_score = nlp_req(readable_string, path='/get_sentiment_score')

            # create a new dictionary to store the capture data
            new_store = {
                'id': json_single['id'],
                'content': readable_string,
                'abusive_score': abusive_score,
                'homeless_relative_score': homeless_relative_score,
                'sentiment_score': sentiment_score,
                'created_at': json_single['created_at'],
                'language': json_single['language'],
                'source': api_url
            }
            db.save(new_store)

        except:
            print("Wait for next message")


# open the harvest
m.stream_public(Listener())
