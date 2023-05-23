import json
import os
import re

import couchdb
from mastodon import Mastodon, StreamListener

from backend.nlp import compute_cross_score, get_abusive_score

# db_host = os.environ.get('READ_DB_HOST')
# db_port = os.environ.get('READ_DB_PORT')
#
# # couchdb login data
# admin = 'admin'
# password = 'admin'
#
# # connect to couchdb
# url = f'http://{admin}:{password}@{db_host}:{db_port}/'
# couch = couchdb.Server(url)
#
# db_name = 'mastodon'
# if db_name not in couch:
#     db = couch.create(db_name)
# else:
#     db = couch[db_name]
#
# mastodon message (with url and private token)
m = Mastodon(
    api_base_url='https://aus.social',
    access_token='x8UJOO1_G6AiB_dJ29GixEidEfianC5NjLHcAMoaPzc'
)


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

            abusive_score = get_abusive_score(readable_string)
            homeless_relative_score = compute_cross_score('homeless', readable_string)

            # create a new dictionary to store the capture data
            new_store = {
                'id': json_single['id'],
                'content': readable_string,
                'abusive_score': abusive_score,
                'homeless_relative_score': homeless_relative_score,
                'created_at': json_single['created_at'],
                'language': json_single['language']
            }
            print(new_store)
            # db.save(new_store)

        except:
            print("error")


# open the harvest
m.stream_public(Listener())
