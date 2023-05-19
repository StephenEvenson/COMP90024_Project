import couchdb
import json
import decimal
import requests


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class myDB(couchdb.Database):
    def __int__(self, url, name=None, session=None):
        super().__init__(url, name, session)

    def save_batch(self, data):
        json_body = json.dumps({'docs': data}, cls=DecimalEncoder)
        url = f'{self.resource.url}/_bulk_docs'
        requests.post(
            url=url,
            data=json_body,
            headers={'Content-type': 'application/json'},
            auth=self.resource.credentials
        )


class CouchApi(couchdb.Server):
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
        db = myDB(self.resource(name), name)
        db.resource.head()  # actually make a request to the database
        return db
