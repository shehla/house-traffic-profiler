import boto.dynamodb2
from boto.dynamodb2.table import Table
from decimal import Decimal
from operator import itemgetter
import json

import time


class RouteStore(object):
    """Class to handle all file changes related to a SHA."""
    def __init__(
            self,
            connection=None,
            dynamodb_region='us-west-1'):
        self.AWS_creds = self.get_AWS_creds()
        print('AWS creds:{0}'.format(self.AWS_creds))
        self.table_handles = dict()
        self.connection = None
        self.dynamodb_region = dynamodb_region
        self.connection = self.get_connection()

    def get_AWS_creds(self):
        with open('AWS_creds.json') as fd:
            return json.load(fd)

    def sort_list(self, stock_list, key_to_sort, s_order=False):
        return sorted(stock_list, key=itemgetter(key_to_sort), reverse=s_order)

    def get_routes(self):
        now = time.time()
        routes_table = self.get_table('routes')
        recs = routes_table.scan()
        results = []
        for r in recs:
            results.append(dict(r))
        return results

    def get_time_profile(self, route, end_time=time.time(), duration=12*60.0*60.0):
        prof_table = self.get_table('travel_time_profiles')
        print('route:{0} start:{1} end:{2}'.format(
            route['route_id'],
            end_time - duration,
            end_time,
        ))
        recs = prof_table.query_2(
            route_id__eq=route['route_id'],
            time__gte=end_time - duration,
        )
        results = []
        for r in recs:
            try:
                times = json.loads(r['info'])
                info = {}
                for t in times:
                    info[t.keys()[0]] = t.values()[0]
                rec = {
                    'epoch': float(r['time']) - 7 * 60 * 60.0,
                    'info': info,
                    'current_delay': r['current_delay'],
                }
                results.append(rec)
            except TypeError:
                print(json.loads(r))
        return results

    # TODO: Delete this and use DynamoStore object.
    def get_connection(self):
        if self.connection is None:
            self.connection = boto.dynamodb2.connect_to_region(
                self.dynamodb_region,
                aws_access_key_id=self.AWS_creds['AWSAccessKeyId'],
                aws_secret_access_key=self.AWS_creds['AWSSecretKey']
            )
        return self.connection

    # TODO: Delete this and use DynamoStore object.
    def get_table(self, table_name):
        if table_name not in self.table_handles:
            self.table_handles[table_name] = Table(
                table_name, connection=self.get_connection())
        return self.table_handles[table_name]

    def report(self, table_name, record):
        summary_table = self.get_table(table_name)
        summary_table.put_item(data=record, overwrite=True)
