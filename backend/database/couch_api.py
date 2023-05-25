import csv
import os
from collections import defaultdict

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

    def init_mastodon(self):
        self.create_views('mastodon')

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

    def get_mastodon_scenario_count(self, db_name, scenario):
        db = self.couch_api[db_name]
        scenario_view_map = {
            'all': [
                '_design/total_docs/_view/total_docs',
                '_design/positive_homeless_scores/_view/positive_homeless_scores',
                '_design/high_abusive_scores/_view/high_abusive_scores',
            ],
            'homeless': ['_design/positive_homeless_scores/_view/positive_homeless_scores'],
            'abuse': ['_design/high_abusive_scores/_view/high_abusive_scores'],
        }

        if scenario not in scenario_view_map:
            raise ValueError("Scenario must be 'all', 'homeless', or 'abuse'")

        # prepare counts dictionary
        counts = {
            'total': 0,
            'positive_homeless_scores': 0,
            'high_abusive_scores': 0,
        }

        for view_name in scenario_view_map[scenario]:
            # Query the appropriate view based on the scenario
            rows = db.view(view_name)
            count = 0
            for row in rows:
                # The value of each row is the count from the reduce function
                count += row.value

            # assign count to the appropriate key in the counts dictionary
            if view_name == '_design/total_docs/_view/total_docs':
                counts['total'] = count
            elif view_name == '_design/positive_homeless_scores/_view/positive_homeless_scores':
                counts['positive_homeless_scores'] = count
            elif view_name == '_design/high_abusive_scores/_view/high_abusive_scores':
                counts['high_abusive_scores'] = count

        return counts

    def get_mastodon_lang_count(self, db_name, seconds):
        now = datetime.now(pytz.utc)
        cutoff = now - timedelta(seconds=seconds)

        db = self.couch_api[db_name]

        rows = db.view('_design/by_created_at/_view/by_created_at',
                       startkey=cutoff.isoformat(),
                       endkey=now.isoformat(),
                       include_docs=True)

        langs = {}
        for row in rows:
            lang = row.doc['language']
            if not lang:
                continue
            lang = lang.split('-')[0]
            if lang not in langs:
                langs[lang] = 0
            langs[lang] += 1

        return langs

    def get_mastodon_abuse_lang_percent(self, db_name):
        db = self.couch_api[db_name]
        rows = db.view('_design/by_lang/_view/by_lang')
        # get percentage of abusive tweets per language
        lang_count = defaultdict(int)
        lang_abuse_count = defaultdict(int)
        print(len(rows))
        for row in rows:
            lang = row.key
            abusive_score = row.value
            lang_count[lang] += 1
            if abusive_score > 0.5:
                lang_abuse_count[lang] += 1
        lang_percent = {}
        for lang in lang_count:
            lang_percent[lang] = lang_abuse_count[lang] / lang_count[lang]

        # sort by percentage, and return top 3
        lang_percent = dict(sorted(lang_percent.items(), key=lambda item: item[1], reverse=True)[:20])
        return lang_percent

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

        with open('data/2011sa4.geojson') as f:
            geojson = json.load(f)

        code_total_dict = {}
        for row in rows:
            sa4_code16, homeless_total = row.key
            code_total_dict[str(sa4_code16)] = homeless_total

        for feature in geojson['features']:
            sa4_code = feature['properties']['SA4_CODE']
            if str(sa4_code) in code_total_dict:
                feature['properties']['homeless_total'] = code_total_dict[sa4_code]
            else:
                feature['properties']['homeless_total'] = 0

        return geojson

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

    def init_twitter(self):
        self.create_views('twitter')

    def get_twitter_scenario_count(self, db_name, scenario):
        db = self.couch_api[db_name]
        scenario_view_map = {
            'all': [
                '_design/total_docs/_view/total_docs',
                '_design/by_homeless_related/_view/by_homeless_related',
                '_design/by_high_abusive_score/_view/by_high_abusive_score',
            ],
            'homeless': ['_design/by_homeless_related/_view/by_homeless_related'],
        }

        if scenario not in scenario_view_map:
            raise ValueError("Scenario must be 'all' or 'homeless'")

        # prepare counts dictionary
        counts = {
            'all': 0,
            'homeless': 0,
            'high_abusive_scores': 0,
        }

        for view_name in scenario_view_map[scenario]:
            # Query the appropriate view based on the scenario
            rows = db.view(view_name)
            count = 0
            for row in rows:
                # The value of each row is the count from the reduce function
                count += row.value

            # assign count to the appropriate key in the counts dictionary
            if view_name == '_design/total_docs/_view/total_docs':
                counts['all'] = count
            elif view_name == '_design/by_homeless_related/_view/by_homeless_related':
                counts['homeless'] = count
            elif view_name == '_design/by_high_abusive_score/_view/by_high_abusive_score':
                counts['high_abusive_scores'] = count

        return counts

    def get_twitter_homeless_related_distribution(self, db_name, gcc):
        db = self.couch_api[db_name]

        views = [
            '_design/by_homeless_job_city/_view/by_homeless_job_city',
            '_design/by_homeless_eco_city/_view/by_homeless_eco_city',
            '_design/by_homeless_men_city/_view/by_homeless_men_city',
            '_design/by_homeless_soc_city/_view/by_homeless_soc_city',
            '_design/by_homeless_edu_city/_view/by_homeless_edu_city',
        ]

        counts = {}

        for view_name in views:
            if gcc == 'all':
                rows = db.view(view_name)
            else:
                rows = db.view(view_name, key=gcc)
            rows = list(rows)
            if rows:  # Check if the list is not empty
                if view_name == '_design/by_homeless_job_city/_view/by_homeless_job_city':
                    counts['job'] = rows[0].value
                elif view_name == '_design/by_homeless_eco_city/_view/by_homeless_eco_city':
                    counts['eco'] = rows[0].value
                elif view_name == '_design/by_homeless_men_city/_view/by_homeless_men_city':
                    counts['men'] = rows[0].value
                elif view_name == '_design/by_homeless_soc_city/_view/by_homeless_soc_city':
                    counts['soc'] = rows[0].value
                elif view_name == '_design/by_homeless_edu_city/_view/by_homeless_edu_city':
                    counts['edu'] = rows[0].value

        return counts

    def get_twitter_geo_combine(self):
        db_sudo = self.couch_api['sudo_sa4_homeless']

        rows_sudo = db_sudo.view('_design/by_sa4_and_homeless_counts/_view/by_sa4_and_homeless_counts')

        db_twitter = self.couch_api['twitter']

        rows_twitter_heat = db_twitter.view('_design/by_homeless_tweet_heat/_view/by_homeless_tweet_heat')

        rows_twitter_lang = db_twitter.view('_design/by_lang/_view/by_lang')

        with open('data/2011sa4.geojson') as f:
            geojson = json.load(f)

        code_total_dict = {}
        for row in rows_sudo:
            sa4_code16, homeless_total = row.key
            code_total_dict[str(sa4_code16)] = homeless_total

        code_heat_dict = {}
        for row in rows_twitter_heat:
            geo_sa4 = str(row.key)
            combine = row.value
            if geo_sa4 not in code_heat_dict:
                code_heat_dict[geo_sa4] = 0
            code_heat_dict[geo_sa4] += combine['like_count'] * 0.1 + combine['retweet_count'] * 0.2 + combine[
                'reply_count'] * 0.3 + combine['quote_count'] * 0.3

        code_lang_dict = {}
        for row in rows_twitter_lang:
            geo_sa4 = str(row.key)
            lang = row.value
            if geo_sa4 not in code_lang_dict:
                code_lang_dict[geo_sa4] = {}
            code_lang_dict[geo_sa4][lang] = code_lang_dict[geo_sa4].get(lang, 0) + 1

        for feature in geojson['features']:
            sa4_code = feature['properties']['SA4_CODE']
            if str(sa4_code) in code_heat_dict:
                feature['properties']['homeless_heat'] = code_heat_dict[sa4_code]
            else:
                feature['properties']['homeless_heat'] = 0
            if str(sa4_code) in code_total_dict:
                feature['properties']['homeless_total'] = code_total_dict[sa4_code]
            else:
                feature['properties']['homeless_total'] = 0
            if str(sa4_code) in code_lang_dict:
                feature['properties']['lang'] = code_lang_dict[sa4_code]
            else:
                feature['properties']['lang'] = {}

        return geojson

    def get_twitter_sentiment_gcc(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_design/by_sentiment_gcc/_view/by_sentiment_gcc')
        docs = {}
        for row in rows:
            geo_gcc = row.key
            sentiment = row.value
            if geo_gcc not in docs:
                docs[geo_gcc] = 0
            else:
                docs[geo_gcc] += sentiment
        return docs

    def get_sudo_abs_regional_population_sentiment_weighted(self, db_name):
        db = self.couch_api[db_name]

        rows = db.view('_design/by_abs_regional_population/_view/by_abs_regional_population')

        persons_total = 0
        for row in rows:
            state_name, state_persons_total = row.key
            persons_total += state_persons_total

        # '1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte', '9oter'
        gcc_state_map = {
            '8acte': 'Australian Capital Territory',
            '1gsyd': 'New South Wales',
            '7gdar': 'Northern Territory',
            '3gbri': 'Queensland',
            '4gade': 'South Australia',
            '9oter': 'Tasmania',
            '2gmel': 'Victoria',
            '5gper': 'Western Australia',
        }
        gcc_weighted_dict = {}
        for row in rows:
            state_name, state_persons_total = row.key
            gcc_weighted_dict[state_name] = state_persons_total / persons_total

        gcc_sentiment = self.get_twitter_sentiment_gcc('twitter')

        gcc_sentiment_weighted = {
            'Australian Capital Territory': 0,
            'New South Wales': 0,
            'Northern Territory': 0,
            'Queensland': 0,
            'South Australia': 0,
            'Tasmania': 0,
            'Victoria': 0,
            'Western Australia': 0,
        }
        for gcc, sentiment in gcc_sentiment.items():
            if gcc in gcc_state_map:
                state = gcc_state_map[gcc]
                gcc_sentiment_weighted[state] = sentiment * gcc_weighted_dict[state]
        return gcc_sentiment_weighted

    def get_twitter_sentiment_period(self, db_name, kind):
        db = self.couch_api[db_name]
        rows = db.view('_design/by_sentiment_time/_view/by_sentiment_time')

        sentiment_counts = defaultdict(lambda: defaultdict(int))

        start_date = datetime.now()
        end_date = datetime(1970, 1, 1)
        for row in rows:
            dt = datetime.strptime(row.key[:19], "%Y-%m-%dT%H:%M:%S")  # Convert timestamp string to datetime

            if dt < start_date:
                start_date = dt
            if dt > end_date:
                end_date = dt

            sentiment = row.value

            if kind == "year":
                key = str(dt.month)  # for each month
            elif kind == "month":
                # quartile = dt.day // 8  # Divide the month into roughly 4 parts
                # key = f"{quartile * 8 + 1}-{min((quartile + 1) * 8, 31)}"
                key = str(dt.day)
            elif kind == "week":
                key = str(dt.weekday())  # 0 for Monday, 6 for Sunday
            elif kind == "day":
                segment = dt.hour // 2  # Divide the day into 12 parts
                key = f"{segment * 2}-{min((segment + 1) * 2, 23)}"
            else:
                raise ValueError("Invalid 'kind' value. It should be one of ['year', 'month', 'week', 'day']")

            if -1 <= sentiment < -0.25:
                sentiment_counts[key]['negative'] += 1
            elif -0.25 <= sentiment <= 0.25:
                sentiment_counts[key]['neutral'] += 1
            elif 0.25 < sentiment <= 1:
                sentiment_counts[key]['positive'] += 1

        return {
            'start_date': start_date,
            'end_date': end_date,
            'sentiment_counts': sentiment_counts
        }
