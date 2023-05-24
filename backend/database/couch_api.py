import csv
import math
import os

import couchdb
import json
import decimal

import numpy as np
import pandas as pd
import pytz
import requests

from datetime import datetime, timedelta


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        print("Encoding:", obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (np.float, float)):
            if np.isnan(obj) or np.isinf(obj):
                return None
        return super(CustomEncoder, self).default(obj)


class Mydb(couchdb.Database):
    def __init__(self, url, name=None, session=None, map_reduce_functions=None):
        super().__init__(url, name, session)
        self.map_reduce_functions = map_reduce_functions

    def save_doc(self, doc):
        try:
            json_doc = json.dumps(doc, cls=CustomEncoder)
            self.save(json.loads(json_doc))
        except ValueError as e:
            print(f"Problematic document: {doc}")
            print(e)
            raise e

    def save_batch(self, data):
        """Save a batch of documents to the database."""
        json_body = json.dumps({'docs': data}, cls=CustomEncoder)
        url = f'{self.resource.url}/_bulk_docs'
        requests.post(
            url=url,
            data=json_body,
            headers={'Content-type': 'application/json'},
            auth=self.resource.credentials
        )

    def create_views(self, db_name):
        """Create all views in the database."""
        # Load the MapReduce functions from the JSON file
        with open('data/map_reduce_functions.json', 'r', encoding='utf-8') as file:
            map_reduce_functions = json.load(file)

        db_views = map_reduce_functions[db_name]
        for view_name, map_reduce in db_views.items():
            map_func = map_reduce['map']
            reduce_func = map_reduce.get('reduce', None)

            design_doc_id = "_design/" + view_name

            design_doc = {
                "_id": design_doc_id,
                'views': {
                    view_name: {
                        'map': map_func,
                    }
                }
            }

            # Include the reduce function if it exists
            if reduce_func:
                design_doc['views'][view_name]['reduce'] = reduce_func

            # Save the design document
            url = f'{self.resource.url}/{design_doc_id}'
            response = requests.put(
                url=url,
                data=json.dumps(design_doc),
                headers={'Content-type': 'application/json'},
                auth=self.resource.credentials
            )

            response.raise_for_status()


class CouchAPI(couchdb.Server):
    def __init__(self, server_url='http://localhost:5984/', username='admin', password='admin'):
        super().__init__(server_url)
        self.resource.credentials = (username, password)

    def __getitem__(self, name):
        """Return a `Database` object representing the database with the
        specified name.

        :param name: the name of the database
        :return: a `Database` object representing the database
        :rtype: `Database`
        :raise ResourceNotFound: if no database with that name exists
        """
        db = Mydb(self.resource(name), name)
        db.resource.head()  # actually make a request to the database
        return db


class DatabaseService:
    def __init__(self, server_url, username, password):
        self.couch_api = CouchAPI(server_url=server_url, username=username, password=password)

    def create_views(self, db_name):
        db = self.couch_api[db_name]
        db.create_views(db_name)

    def get_mastodon_new(self, db_name, source, seconds):
        now = datetime.now(pytz.utc)
        cutoff = now - timedelta(seconds=seconds)

        db = self.couch_api[db_name]

        # source = https://aus.social | https://mastodon.au | https://tictoc.social
        rows = db.view('_design/by_created_at/_view/by_created_at',
                       startkey=cutoff.isoformat(),
                       endkey=now.isoformat(),
                       include_docs=True)

        docs = []
        docs_aus_social = []
        docs_mastodon_au = []
        docs_tictoc_social = []

        for row in rows:
            if row.doc['source'] == 'https://aus.social':
                docs_aus_social.append(row.doc)
            elif row.doc['source'] == 'https://mastodon.au':
                docs_mastodon_au.append(row.doc)
            elif row.doc['source'] == 'https://tictoc.social':
                docs_tictoc_social.append(row.doc)
            docs.append(row.doc)

        if source == '.social':
            return docs_aus_social
        elif source == '.au':
            return docs_mastodon_au
        elif source == '.tictoc':
            return docs_tictoc_social
        else:
            return docs

    def get_mastodon_sentiment(self, db_name, seconds):
        now = datetime.now(pytz.utc)
        start_time = now - timedelta(seconds=seconds)

        db = self.couch_api[db_name]

        # Query the view with the group=true option to get counts by date and sentiment bucket
        rows = db.view('_design/by_created_at_and_sentiment_score/_view/by_created_at_and_sentiment_score',
                       startkey=[start_time.isoformat()],
                       endkey=[now.isoformat(), {}],
                       group=True)

        data = []
        for row in rows:
            # Each row will have a key of [date, sentiment_bucket] and a value of the count
            date, sentiment_bucket = row.key
            count = row.value
            data.append({
                'date': date,
                'sentiment_bucket': sentiment_bucket,
                'count': count
            })

        return data

    def init_sudo(self):
        path_to_csvs = 'data/sudo/'
        for filename in os.listdir(path_to_csvs):
            if filename.endswith('.csv'):
                db_name = filename[:-4]  # Remove the '.csv' from the filename to use it as the db name

                # Create a new database for each CSV file
                self.couch_api.create(db_name)
                db = self.couch_api[db_name]
                # Create the views for the database
                try:
                    db.create_views(db_name)
                except KeyError:
                    # If the design document already exists, ignore the error
                    pass

                # Use pandas to read the CSV file and convert it to a list of dictionaries
                csv_data = pd.read_csv(f'{path_to_csvs}/{filename}')
                data_dict = csv_data.to_dict('records')

                # Extract column names using the csv library
                with open(f'{path_to_csvs}/{filename}', newline='') as f:
                    reader = csv.reader(f)
                    column_names = next(reader)  # gets the first line

                for row in data_dict:
                    doc = {column_names[i]: value for i, value in enumerate(row.values())}
                    db.save_doc(doc)

    def get_sudo_regional_language(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_all_docs', include_docs=True)

        docs = []
        for row in rows:
            doc = row.doc
            docs.append(doc)

        return docs

    def get_sudo_regional_population(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_all_docs', include_docs=True)

        docs = []
        for row in rows:
            doc = row.doc
            docs.append(doc)

        return docs

    def get_sudo_gcc_homeless(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_design/by_gccsa_and_homeless_counts/_view/by_gccsa_and_homeless_counts')

        docs = []
        for row in rows:
            gccsa_code, gccsa_name, homeless_m_tot, homeless_f_total, homeless_total = row.key
            doc = {
                'gccsa_code': gccsa_code,
                'gccsa_name': gccsa_name,
                'homeless_m_tot': homeless_m_tot,
                'homeless_f_total': homeless_f_total,
                'homeless_total': homeless_total
            }
            docs.append(doc)

        return docs

    def get_sudo_sa4_homeless(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_design/by_sa4_and_homeless_counts/_view/by_sa4_and_homeless_counts')

        docs = []
        for row in rows:
            sa4_code16, sa4_name_2016, homeless_total = row.key
            doc = {
                'sa4_code16': sa4_code16,
                'sa4_name_2016': sa4_name_2016,
                'homeless_total': homeless_total
            }
            docs.append(doc)

        return docs

    def get_sudo_sa4_income(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_design/by_sa4_and_weekly_income/_view/by_sa4_and_weekly_income')

        docs = []
        for row in rows:
            sa4_code_2021, median_tot_fam_inc_weekly, median_tot_prsnl_inc_weekly = row.key
            doc = {
                'sa4_code_2021': sa4_code_2021,
                'median_tot_fam_inc_weekly': median_tot_fam_inc_weekly,
                'median_tot_prsnl_inc_weekly': median_tot_prsnl_inc_weekly
            }
            docs.append(doc)

        return docs
