import couchdb
import json
import decimal
import requests


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class Mydb(couchdb.Database):
    def __init__(self, url, name=None, session=None, map_reduce_functions=None):
        super().__init__(url, name, session)
        self.map_reduce_functions = map_reduce_functions

    def save_batch(self, data):
        """Save a batch of documents to the database."""
        json_body = json.dumps({'docs': data}, cls=DecimalEncoder)
        url = f'{self.resource.url}/_bulk_docs'
        requests.post(
            url=url,
            data=json_body,
            headers={'Content-type': 'application/json'},
            auth=self.resource.credentials
        )

    def create_views(self):
        """Create all views in the database."""
        # Load the MapReduce functions from the JSON file
        with open('map_reduce_functions.json', 'r') as file:
            map_reduce_functions = json.load(file)

        for view_name in map_reduce_functions:
            # Get the specified view's map and reduce functions
            map_func = map_reduce_functions[view_name]['map']
            reduce_func = map_reduce_functions[view_name]['reduce']

            design_doc_id = "_design/" + view_name

            design_doc = {
                "_id": design_doc_id,
                'views': {
                    view_name: {
                        'map': map_func,
                        'reduce': reduce_func
                    }
                }
            }

            # Save the design document
            url = f'{self.resource.url}/{design_doc_id}'
            response = requests.put(
                url=url,
                data=json.dumps(design_doc),
                headers={'Content-type': 'application/json'},
                auth=self.resource.credentials
            )

            response.raise_for_status()

    def query_data_from_view(self, view_name, limit=0, skip=0):
        """Query the database with the specified view."""
        url = f'{self.resource.url}/_design/{view_name}/_view/{view_name}'
        print(url)
        params = {'limit': limit, 'skip': skip, 'group': 'true'}

        response = requests.get(url=url, params=params, auth=self.resource.credentials)
        response.raise_for_status()

        data = response.json()

        return [(row['key'], row['value']) for row in data['rows']]


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
