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
            headers={
                'Content-type': 'application/json'
            },
            auth=self.resource.credentials
        )

    def create_view(self, view_name):
        """Create a view in the database."""
        # Load the MapReduce functions from the JSON file
        with open('map_reduce_functions.json', 'r') as file:
            map_reduce_functions = json.load(file)

        # Get the specified view's map and reduce functions
        map_func = map_reduce_functions[view_name]['map']
        reduce_func = map_reduce_functions[view_name]['reduce']

        design_doc_id = "_design/" + view_name

        # If the design document already exists, get it
        if design_doc_id in self:
            design_doc = self[design_doc_id]
        else:
            # Otherwise, create a new design document
            design_doc = {'views': {}}

        # Update the design document with the new view
        design_doc['views'][view_name] = {
            'map': map_func,
            'reduce': reduce_func
        }

        # Save the design document
        self[design_doc_id] = design_doc

    def query_data_from_view(self, view_name, limit=None, skip=None):
        """Query the database with the specified view."""
        # Query the view and return the results
        rows = self.view(view_name + '/' + view_name, group=True, limit=limit, skip=skip)
        return [(row.key, row.value) for row in rows]


class CouchAPI(couchdb.Server):
    def __init__(self, server_url='http://localhost:5984/', username='admin', password='admin',
                 map_reduce_file='map_reduce_functions.json'):
        super().__init__(server_url)
        self.resource.credentials = (username, password)

        # Load the MapReduce functions from the JSON file
        with open(map_reduce_file, 'r') as file:
            self.map_reduce_functions = json.load(file)

    def __getitem__(self, name):
        """Return a `Database` object representing the database with the
        specified name.

        :param name: the name of the database
        :return: a `Database` object representing the database
        :rtype: `Database`
        :raise ResourceNotFound: if no database with that name exists
        """
        db = Mydb(self.resource(name), name, map_reduce_functions=self.map_reduce_functions)
        db.resource.head()  # actually make a request to the database
        return db
