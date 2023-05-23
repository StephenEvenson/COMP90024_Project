from couch_api import CouchAPI

couch_api = CouchAPI('http://192.168.0.80:5984/', username='admin', password='admin')
db = couch_api['raw_tweets_processed_2']

if __name__ == '__main__':
    db.create_views()
    results = db.query_data_from_view('by_geo', limit=10, skip=0)
    print(results)
