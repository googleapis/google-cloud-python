# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest


class _SchemaBase(object):

    def _verify_field(self, field, r_field):
        self.assertEqual(field.name, r_field['name'])
        self.assertEqual(field.field_type, r_field['type'])
        self.assertEqual(field.mode, r_field.get('mode', 'NULLABLE'))

    def _verifySchema(self, schema, resource):
        r_fields = resource['schema']['fields']
        self.assertEqual(len(schema), len(r_fields))

        for field, r_field in zip(schema, r_fields):
            self._verify_field(field, r_field)


class TestTable(unittest.TestCase, _SchemaBase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'
    TABLE_NAME = 'table-name'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import Table

        return Table

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.TABLE_ID = '%s:%s:%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.NUM_BYTES = 12345
        self.NUM_ROWS = 67

    def _makeResource(self):
        self._setUpConstants()
        return {
            'creationTime': self.WHEN_TS * 1000,
            'tableReference':
                {'projectId': self.PROJECT,
                 'datasetId': self.DS_NAME,
                 'tableId': self.TABLE_NAME},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'etag': 'ETAG',
            'id': self.TABLE_ID,
            'lastModifiedTime': self.WHEN_TS * 1000,
            'location': 'US',
            'selfLink': self.RESOURCE_URL,
            'numRows': self.NUM_ROWS,
            'numBytes': self.NUM_BYTES,
            'type': 'TABLE',
        }

    def _verifyReadonlyResourceProperties(self, table, resource):
        if 'creationTime' in resource:
            self.assertEqual(table.created, self.WHEN)
        else:
            self.assertIsNone(table.created)

        if 'etag' in resource:
            self.assertEqual(table.etag, self.ETAG)
        else:
            self.assertIsNone(table.etag)

        if 'numRows' in resource:
            self.assertEqual(table.num_rows, self.NUM_ROWS)
        else:
            self.assertIsNone(table.num_rows)

        if 'numBytes' in resource:
            self.assertEqual(table.num_bytes, self.NUM_BYTES)
        else:
            self.assertIsNone(table.num_bytes)

        if 'selfLink' in resource:
            self.assertEqual(table.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(table.self_link)

        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table.table_type,
                         'TABLE' if 'view' not in resource else 'VIEW')

    def _verifyResourceProperties(self, table, resource):

        self._verifyReadonlyResourceProperties(table, resource)

        if 'expirationTime' in resource:
            self.assertEqual(table.expires, self.EXP_TIME)
        else:
            self.assertIsNone(table.expires)

        self.assertEqual(table.description, resource.get('description'))
        self.assertEqual(table.friendly_name, resource.get('friendlyName'))
        self.assertEqual(table.location, resource.get('location'))

        if 'view' in resource:
            self.assertEqual(table.view_query, resource['view']['query'])
        else:
            self.assertIsNone(table.view_query)

        if 'schema' in resource:
            self._verifySchema(table.schema, resource)
        else:
            self.assertEqual(table.schema, [])

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertIs(table._dataset, dataset)
        self.assertEqual(table.project, self.PROJECT)
        self.assertEqual(table.dataset_name, self.DS_NAME)
        self.assertEqual(
            table.path,
            '/projects/%s/datasets/%s/tables/%s' % (
                self.PROJECT, self.DS_NAME, self.TABLE_NAME))
        self.assertEqual(table.schema, [])

        self.assertIsNone(table.created)
        self.assertIsNone(table.etag)
        self.assertIsNone(table.modified)
        self.assertIsNone(table.num_bytes)
        self.assertIsNone(table.num_rows)
        self.assertIsNone(table.self_link)
        self.assertIsNone(table.table_id)
        self.assertIsNone(table.table_type)

        self.assertIsNone(table.description)
        self.assertIsNone(table.expires)
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.location)
        self.assertIsNone(table.view_query)

    def test_ctor_w_schema(self):
        from google.cloud.bigquery.table import SchemaField

        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertEqual(table.schema, [full_name, age])

    def test_num_bytes_getter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)

        # Check with no value set.
        self.assertIsNone(table.num_bytes)

        num_bytes = 1337
        # Check with integer value set.
        table._properties = {'numBytes': num_bytes}
        self.assertEqual(table.num_bytes, num_bytes)

        # Check with a string value set.
        table._properties = {'numBytes': str(num_bytes)}
        self.assertEqual(table.num_bytes, num_bytes)

        # Check with invalid int value.
        table._properties = {'numBytes': 'x'}
        with self.assertRaises(ValueError):
            getattr(table, 'num_bytes')

    def test_num_rows_getter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)

        # Check with no value set.
        self.assertIsNone(table.num_rows)

        num_rows = 42
        # Check with integer value set.
        table._properties = {'numRows': num_rows}
        self.assertEqual(table.num_rows, num_rows)

        # Check with a string value set.
        table._properties = {'numRows': str(num_rows)}
        self.assertEqual(table.num_rows, num_rows)

        # Check with invalid int value.
        table._properties = {'numRows': 'x'}
        with self.assertRaises(ValueError):
            getattr(table, 'num_rows')

    def test_schema_setter_non_list(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(TypeError):
            table.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.table import SchemaField

        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            table.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.table import SchemaField

        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table.schema = [full_name, age]
        self.assertEqual(table.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        CREATED = datetime.datetime(2015, 7, 29, 12, 13, 22, tzinfo=UTC)
        MODIFIED = datetime.datetime(2015, 7, 29, 14, 47, 15, tzinfo=UTC)
        TABLE_ID = '%s:%s:%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        URL = 'http://example.com/projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table._properties['creationTime'] = _millis(CREATED)
        table._properties['etag'] = 'ETAG'
        table._properties['lastModifiedTime'] = _millis(MODIFIED)
        table._properties['numBytes'] = 12345
        table._properties['numRows'] = 66
        table._properties['selfLink'] = URL
        table._properties['id'] = TABLE_ID
        table._properties['type'] = 'TABLE'

        self.assertEqual(table.created, CREATED)
        self.assertEqual(table.etag, 'ETAG')
        self.assertEqual(table.modified, MODIFIED)
        self.assertEqual(table.num_bytes, 12345)
        self.assertEqual(table.num_rows, 66)
        self.assertEqual(table.self_link, URL)
        self.assertEqual(table.table_id, TABLE_ID)
        self.assertEqual(table.table_type, 'TABLE')

    def test_description_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.description = 12345

    def test_description_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.description = 'DESCRIPTION'
        self.assertEqual(table.description, 'DESCRIPTION')

    def test_expires_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.expires = object()

    def test_expires_setter(self):
        import datetime
        from google.cloud._helpers import UTC

        WHEN = datetime.datetime(2015, 7, 28, 16, 39, tzinfo=UTC)
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.expires = WHEN
        self.assertEqual(table.expires, WHEN)

    def test_friendly_name_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.friendly_name = 12345

    def test_friendly_name_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.friendly_name = 'FRIENDLY'
        self.assertEqual(table.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.location = 12345

    def test_location_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.location = 'LOCATION'
        self.assertEqual(table.location, 'LOCATION')

    def test_view_query_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.view_query = 12345

    def test_view_query_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.view_query = 'select * from foo'
        self.assertEqual(table.view_query, 'select * from foo')

    def test_view_query_deleter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)
        table.view_query = 'select * from foo'
        del table.view_query
        self.assertIsNone(table.view_query)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, dataset)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        RESOURCE = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_NAME, self.TABLE_NAME),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME,
            },
            'type': 'TABLE',
        }
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertIs(table._dataset, dataset)
        self._verifyResourceProperties(table, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        RESOURCE = self._makeResource()
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE, dataset)
        self.assertIs(table._dataset._client, client)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_no_view_query_no_schema(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset)

        with self.assertRaises(ValueError):
            table.create()

    def test_create_w_bound_client(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])

        table.create()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_w_partition_no_expire(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])

        self.assertIsNone(table.partitioning_type)
        table.partitioning_type = "DAY"
        self.assertEqual(table.partitioning_type, "DAY")
        table.create()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME},
            'timePartitioning': {'type': 'DAY'},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_w_partition_and_expire(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table.partition_expiration = 100
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(table.partition_expiration, 100)
        table.create()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME},
            'timePartitioning': {'type': 'DAY', 'expirationMs': 100},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_partition_type_setter_bad_type(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partitioning_type = 123

    def test_partition_type_setter_unknown_value(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partitioning_type = "HASH"

    def test_partition_type_setter_w_known_value(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertIsNone(table.partitioning_type)
        table.partitioning_type = 'DAY'
        self.assertEqual(table.partitioning_type, 'DAY')

    def test_partition_type_setter_w_none(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        table._properties['timePartitioning'] = {'type': 'DAY'}
        table.partitioning_type = None
        self.assertIsNone(table.partitioning_type)
        self.assertFalse('timePartitioning' in table._properties)

    def test_partition_experation_bad_type(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partition_expiration = "NEVER"

    def test_partition_expiration_w_integer(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table.partition_expiration = 100
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(table.partition_expiration, 100)

    def test_partition_expiration_w_none(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table._properties['timePartitioning'] = {
            'type': 'DAY',
            'expirationMs': 100,
        }
        table.partition_expiration = None
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertIsNone(table.partition_expiration)

    def test_partition_expiration_w_none_no_partition_set(self):
        from google.cloud.bigquery.table import SchemaField

        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table.partition_expiration = None
        self.assertIsNone(table.partitioning_type)
        self.assertIsNone(table.partition_expiration)

    def test_list_partitions(self):
        from google.cloud.bigquery.table import SchemaField

        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        client._query_results = [(20160804, None), (20160805, None)]
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])
        self.assertEqual(table.list_partitions(), [20160804, 20160805])

    def test_create_w_alternate_client(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        QUERY = 'select fullname, age from person_ages'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59,
                                          tzinfo=UTC)
        RESOURCE['expirationTime'] = _millis(self.EXP_TIME)
        RESOURCE['view'] = {}
        RESOURCE['view']['query'] = QUERY
        RESOURCE['type'] = 'VIEW'
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client=client1)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age])
        table.friendly_name = TITLE
        table.description = DESCRIPTION
        table.view_query = QUERY

        table.create(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME},
            'description': DESCRIPTION,
            'friendlyName': TITLE,
            'view': {'query': QUERY},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_w_missing_output_properties(self):
        # In the wild, the resource returned from 'dataset.create' sometimes
        # lacks 'creationTime' / 'lastModifiedTime'
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        del RESOURCE['creationTime']
        del RESOURCE['lastModifiedTime']
        self.WHEN = None
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset,
                               schema=[full_name, age])

        table.create()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        self.assertFalse(table.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        self.assertTrue(table.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_patch_w_invalid_expiration(self):
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        with self.assertRaises(ValueError):
            table.patch(expires='BOGUS')

    def test_patch_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.patch(description=DESCRIPTION,
                    friendly_name=TITLE,
                    view_query=None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {
            'description': DESCRIPTION,
            'friendlyName': TITLE,
            'view': None,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_patch_w_alternate_client(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        QUERY = 'select fullname, age from person_ages'
        LOCATION = 'EU'
        RESOURCE = self._makeResource()
        RESOURCE['view'] = {'query': QUERY}
        RESOURCE['type'] = 'VIEW'
        RESOURCE['location'] = LOCATION
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59,
                                          tzinfo=UTC)
        RESOURCE['expirationTime'] = _millis(self.EXP_TIME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='NULLABLE')

        table.patch(client=client2, view_query=QUERY, location=LOCATION,
                    expires=self.EXP_TIME, schema=[full_name, age])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'view': {'query': QUERY},
            'location': LOCATION,
            'expirationTime': _millis(self.EXP_TIME),
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'NULLABLE'}]},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_patch_w_schema_None(self):
        # Simulate deleting schema:  not sure if back-end will actually
        # allow this operation, but the spec says it is optional.
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.patch(schema=None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {'schema': None}
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_update_w_bound_client(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age])
        table.description = DESCRIPTION
        table.friendly_name = TITLE

        table.update()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        SENT = {
            'tableReference':
                {'projectId': self.PROJECT,
                 'datasetId': self.DS_NAME,
                 'tableId': self.TABLE_NAME},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'description': DESCRIPTION,
            'friendlyName': TITLE,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_update_w_alternate_client(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        DEF_TABLE_EXP = 12345
        LOCATION = 'EU'
        QUERY = 'select fullname, age from person_ages'
        RESOURCE = self._makeResource()
        RESOURCE['defaultTableExpirationMs'] = 12345
        RESOURCE['location'] = LOCATION
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59,
                                          tzinfo=UTC)
        RESOURCE['expirationTime'] = _millis(self.EXP_TIME)
        RESOURCE['view'] = {'query': QUERY}
        RESOURCE['type'] = 'VIEW'
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)
        table.default_table_expiration_ms = DEF_TABLE_EXP
        table.location = LOCATION
        table.expires = self.EXP_TIME
        table.view_query = QUERY

        table.update(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'tableReference':
                {'projectId': self.PROJECT,
                 'datasetId': self.DS_NAME,
                 'tableId': self.TABLE_NAME},
            'expirationTime': _millis(self.EXP_TIME),
            'location': 'EU',
            'view': {'query': QUERY},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_delete_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.delete()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        table.delete(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_bound_client(self):
        import datetime
        import six
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        WHEN_1 = WHEN + datetime.timedelta(seconds=1)
        WHEN_2 = WHEN + datetime.timedelta(seconds=2)
        ROWS = 1234
        TOKEN = 'TOKEN'

        def _bigquery_timestamp_float_repr(ts_float):
            # Preserve microsecond precision for E+09 timestamps
            return '%0.15E' % (ts_float,)

        DATA = {
            'totalRows': str(ROWS),
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': 'Phred Phlyntstone'},
                    {'v': '32'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS)},
                ]},
                {'f': [
                    {'v': 'Bharney Rhubble'},
                    {'v': '33'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS + 1)},
                ]},
                {'f': [
                    {'v': 'Wylma Phlyntstone'},
                    {'v': '29'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS + 2)},
                ]},
                {'f': [
                    {'v': 'Bhettye Rhubble'},
                    {'v': None},
                    {'v': None},
                ]},
            ]
        }

        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='NULLABLE')
        joined = SchemaField('joined', 'TIMESTAMP', mode='NULLABLE')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age, joined])

        iterator = table.fetch_data()
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32, WHEN))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33, WHEN_1))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29, WHEN_2))
        self.assertEqual(rows[3], ('Bhettye Rhubble', None, None))
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_alternate_client(self):
        import six
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        MAX = 10
        TOKEN = 'TOKEN'
        DATA = {
            'rows': [
                {'f': [
                    {'v': 'Phred Phlyntstone'},
                    {'v': '32'},
                    {'v': 'true'},
                    {'v': '3.1415926'},
                ]},
                {'f': [
                    {'v': 'Bharney Rhubble'},
                    {'v': '33'},
                    {'v': 'false'},
                    {'v': '1.414'},
                ]},
                {'f': [
                    {'v': 'Wylma Phlyntstone'},
                    {'v': '29'},
                    {'v': 'true'},
                    {'v': '2.71828'},
                ]},
                {'f': [
                    {'v': 'Bhettye Rhubble'},
                    {'v': '27'},
                    {'v': None},
                    {'v': None},
                ]},
            ]
        }
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(DATA)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        voter = SchemaField('voter', 'BOOLEAN', mode='NULLABLE')
        score = SchemaField('score', 'FLOAT', mode='NULLABLE')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age, voter, score])

        iterator = table.fetch_data(
            client=client2, max_results=MAX, page_token=TOKEN)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32, True, 3.1415926))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33, False, 1.414))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29, True, 2.71828))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27, None, None))
        self.assertIsNone(total_rows)
        self.assertIsNone(page_token)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': MAX, 'pageToken': TOKEN})

    def test_fetch_data_w_repeated_fields(self):
        import six
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': [{'v': 'red'}, {'v': 'green'}]},
                    {'v': [{
                        'v': {
                            'f': [
                                {'v': [{'v': '1'}, {'v': '2'}]},
                                {'v': [{'v': '3.1415'}, {'v': '1.414'}]},
                            ]}
                    }]},
                ]},
            ]
        }
        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        color = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[color, struct])

        iterator = table.fetch_data()
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], ['red', 'green'])
        self.assertEqual(rows[0][1], [{'index': [1, 2],
                                       'score': [3.1415, 1.414]}])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_record_schema(self):
        import six
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': 'Phred Phlyntstone'},
                    {'v': {'f': [{'v': '800'}, {'v': '555-1212'}, {'v': 1}]}},
                ]},
                {'f': [
                    {'v': 'Bharney Rhubble'},
                    {'v': {'f': [{'v': '877'}, {'v': '768-5309'}, {'v': 2}]}},
                ]},
                {'f': [
                    {'v': 'Wylma Phlyntstone'},
                    {'v': None},
                ]},
            ]
        }
        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        area_code = SchemaField('area_code', 'STRING', 'REQUIRED')
        local_number = SchemaField('local_number', 'STRING', 'REQUIRED')
        rank = SchemaField('rank', 'INTEGER', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='NULLABLE',
                            fields=[area_code, local_number, rank])
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, phone])

        iterator = table.fetch_data()
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][0], 'Phred Phlyntstone')
        self.assertEqual(rows[0][1], {'area_code': '800',
                                      'local_number': '555-1212',
                                      'rank': 1})
        self.assertEqual(rows[1][0], 'Bharney Rhubble')
        self.assertEqual(rows[1][1], {'area_code': '877',
                                      'local_number': '768-5309',
                                      'rank': 2})
        self.assertEqual(rows[2][0], 'Wylma Phlyntstone')
        self.assertIsNone(rows[2][1])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_insert_data_wo_schema(self):
        from google.cloud.bigquery.table import _TABLE_HAS_NO_SCHEMA

        client = _Client(project=self.PROJECT)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)
        ROWS = [
            ('Phred Phlyntstone', 32),
            ('Bharney Rhubble', 33),
            ('Wylma Phlyntstone', 29),
            ('Bhettye Rhubble', 27),
        ]

        with self.assertRaises(ValueError) as exc:
            table.insert_data(ROWS)

        self.assertEqual(exc.exception.args, (_TABLE_HAS_NO_SCHEMA,))

    def test_insert_data_w_bound_client(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import _microseconds_from_datetime
        from google.cloud.bigquery.table import SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        joined = SchemaField('joined', 'TIMESTAMP', mode='NULLABLE')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age, joined])
        ROWS = [
            ('Phred Phlyntstone', 32, _datetime_to_rfc3339(WHEN)),
            ('Bharney Rhubble', 33, WHEN + datetime.timedelta(seconds=1)),
            ('Wylma Phlyntstone', 29, WHEN + datetime.timedelta(seconds=2)),
            ('Bhettye Rhubble', 27, None),
        ]

        def _row_data(row):
            joined = row[2]
            if isinstance(row[2], datetime.datetime):
                joined = _microseconds_from_datetime(joined) * 1e-6
            return {'full_name': row[0],
                    'age': row[1],
                    'joined': joined}

        SENT = {
            'rows': [{'json': _row_data(row)} for row in ROWS],
        }

        errors = table.insert_data(ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_insert_data_w_alternate_client(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        RESPONSE = {
            'insertErrors': [
                {'index': 1,
                 'errors': [
                     {'reason': 'REASON',
                      'location': 'LOCATION',
                      'debugInfo': 'INFO',
                      'message': 'MESSAGE'}
                 ]},
            ]}
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESPONSE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = _Dataset(client1)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        voter = SchemaField('voter', 'BOOLEAN', mode='NULLABLE')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age, voter])
        ROWS = [
            ('Phred Phlyntstone', 32, True),
            ('Bharney Rhubble', 33, False),
            ('Wylma Phlyntstone', 29, True),
            ('Bhettye Rhubble', 27, True),
        ]

        def _row_data(row):
            return {'full_name': row[0], 'age': row[1], 'voter': row[2]}

        SENT = {
            'skipInvalidRows': True,
            'ignoreUnknownValues': True,
            'templateSuffix': '20160303',
            'rows': [{'insertId': index, 'json': _row_data(row)}
                     for index, row in enumerate(ROWS)],
        }

        errors = table.insert_data(
            client=client2,
            rows=ROWS,
            row_ids=[index for index, _ in enumerate(ROWS)],
            skip_invalid_rows=True,
            ignore_unknown_values=True,
            template_suffix='20160303',
        )

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['index'], 1)
        self.assertEqual(len(errors[0]['errors']), 1)
        self.assertEqual(errors[0]['errors'][0],
                         RESPONSE['insertErrors'][0]['errors'][0])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_insert_data_w_repeated_fields(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, struct])
        ROWS = [
            (['red', 'green'], [{'index': [1, 2], 'score': [3.1415, 1.414]}]),
        ]

        def _row_data(row):
            return {'color': row[0],
                    'struct': row[1]}

        SENT = {
            'rows': [{'json': _row_data(row)} for row in ROWS],
        }

        errors = table.insert_data(ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_insert_data_w_record_schema(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        area_code = SchemaField('area_code', 'STRING', 'REQUIRED')
        local_number = SchemaField('local_number', 'STRING', 'REQUIRED')
        rank = SchemaField('rank', 'INTEGER', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='NULLABLE',
                            fields=[area_code, local_number, rank])
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, phone])
        ROWS = [
            ('Phred Phlyntstone', {'area_code': '800',
                                   'local_number': '555-1212',
                                   'rank': 1}),
            ('Bharney Rhubble', {'area_code': '877',
                                 'local_number': '768-5309',
                                 'rank': 2}),
            ('Wylma Phlyntstone', None),
        ]

        def _row_data(row):
            return {'full_name': row[0],
                    'phone': row[1]}

        SENT = {
            'rows': [{'json': _row_data(row)} for row in ROWS],
        }

        errors = table.insert_data(ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_upload_from_file_text_mode_file_failure(self):

        class TextModeFile(object):
            mode = 'r'

        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        file_obj = TextModeFile()
        table = self._make_one(self.TABLE_NAME, dataset=dataset)
        with self.assertRaises(ValueError):
            table.upload_from_file(file_obj, 'CSV', size=1234)

    def test_upload_from_file_binary_mode_no_failure(self):
        self._upload_from_file_helper(input_file_mode='r+b')

    def test_upload_from_file_size_failure(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        file_obj = object()
        table = self._make_one(self.TABLE_NAME, dataset=dataset)
        with self.assertRaises(ValueError):
            table.upload_from_file(file_obj, 'CSV', size=None)

    def test_upload_from_file_multipart_w_400(self):
        import csv
        import datetime
        from six.moves.http_client import BAD_REQUEST
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud._helpers import UTC
        from google.cloud.exceptions import BadRequest

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        response = {'status': BAD_REQUEST}
        conn = _Connection(
            (response, b'{}'),
        )
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as file_obj:
                writer = csv.writer(file_obj)
                writer.writerow(('full_name', 'age', 'joined'))
                writer.writerow(('Phred Phlyntstone', 32, WHEN))

            with open(temp.name, 'rb') as file_obj:
                with self.assertRaises(BadRequest):
                    table.upload_from_file(
                        file_obj, 'CSV', rewind=True)

    def _upload_from_file_helper(self, **kw):
        import csv
        import datetime
        from six.moves.http_client import OK
        from google.cloud._helpers import UTC
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.bigquery.table import SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        PATH = 'projects/%s/jobs' % (self.PROJECT,)
        response = {'status': OK}
        conn = _Connection(
            (response, b'{}'),
        )
        client = _Client(project=self.PROJECT, connection=conn)
        expected_job = object()
        if 'client' in kw:
            kw['client']._job = expected_job
        else:
            client._job = expected_job
        input_file_mode = kw.pop('input_file_mode', 'rb')
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        joined = SchemaField('joined', 'TIMESTAMP', mode='NULLABLE')
        table = self._make_one(self.TABLE_NAME, dataset=dataset,
                               schema=[full_name, age, joined])
        ROWS = [
            ('Phred Phlyntstone', 32, WHEN),
            ('Bharney Rhubble', 33, WHEN + datetime.timedelta(seconds=1)),
            ('Wylma Phlyntstone', 29, WHEN + datetime.timedelta(seconds=2)),
            ('Bhettye Rhubble', 27, None),
        ]

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as file_obj:
                writer = csv.writer(file_obj)
                writer.writerow(('full_name', 'age', 'joined'))
                writer.writerows(ROWS)

            with open(temp.name, input_file_mode) as file_obj:
                BODY = file_obj.read()
                explicit_size = kw.pop('_explicit_size', False)
                if explicit_size:
                    kw['size'] = len(BODY)
                job = table.upload_from_file(
                    file_obj, 'CSV', rewind=True, **kw)

        self.assertIs(job, expected_job)
        return conn.http._requested, PATH, BODY

    def test_upload_from_file_w_bound_client_multipart(self):
        import json
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._helpers import _to_bytes

        requested, PATH, BODY = self._upload_from_file_helper()
        parse_chunk = _email_chunk_parser()

        self.assertEqual(len(requested), 1)
        req = requested[0]
        self.assertEqual(req['method'], 'POST')
        uri = req['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/%s' % PATH)
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'multipart'})

        ctype, boundary = [x.strip()
                           for x in req['headers']['content-type'].split(';')]
        self.assertEqual(ctype, 'multipart/related')
        self.assertTrue(boundary.startswith('boundary="=='))
        self.assertTrue(boundary.endswith('=="'))

        divider = b'--' + _to_bytes(boundary[len('boundary="'):-1])
        chunks = req['body'].split(divider)[1:-1]  # discard prolog / epilog
        self.assertEqual(len(chunks), 2)

        text_msg = parse_chunk(chunks[0].strip())
        self.assertEqual(dict(text_msg._headers),
                         {'Content-Type': 'application/json',
                          'MIME-Version': '1.0'})
        metadata = json.loads(text_msg._payload)
        load_config = metadata['configuration']['load']
        DESTINATION_TABLE = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.TABLE_NAME,
        }
        self.assertEqual(load_config['destinationTable'], DESTINATION_TABLE)
        self.assertEqual(load_config['sourceFormat'], 'CSV')

        app_msg = parse_chunk(chunks[1].strip())
        self.assertEqual(dict(app_msg._headers),
                         {'Content-Type': 'application/octet-stream',
                          'Content-Transfer-Encoding': 'binary',
                          'MIME-Version': '1.0'})
        body = BODY.decode('ascii').rstrip()
        body_lines = [line.strip() for line in body.splitlines()]
        payload_lines = app_msg._payload.rstrip().splitlines()
        self.assertEqual(payload_lines, body_lines)

    def test_upload_from_file_resumable_with_400(self):
        import csv
        import datetime
        import mock
        from six.moves.http_client import BAD_REQUEST
        from google.cloud.exceptions import BadRequest
        from google.cloud._helpers import UTC
        from google.cloud._testing import _NamedTemporaryFile

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        initial_response = {'status': BAD_REQUEST}
        conn = _Connection(
            (initial_response, b'{}'),
        )
        client = _Client(project=self.PROJECT, connection=conn)

        class _UploadConfig(object):
            accept = ['*/*']
            max_size = None
            resumable_multipart = True
            resumable_path = u'/upload/bigquery/v2/projects/{project}/jobs'
            simple_multipart = True
            simple_path = u''  # force resumable
        dataset = _Dataset(client)
        table = self._make_one(self.TABLE_NAME, dataset=dataset)

        with mock.patch('google.cloud.bigquery.table._UploadConfig',
                        new=_UploadConfig):
            with _NamedTemporaryFile() as temp:
                with open(temp.name, 'w') as file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(('full_name', 'age', 'joined'))
                    writer.writerow(('Phred Phlyntstone', 32, WHEN))

                with open(temp.name, 'rb') as file_obj:
                    with self.assertRaises(BadRequest):
                        table.upload_from_file(
                            file_obj, 'CSV', rewind=True)

    # pylint: disable=too-many-statements
    def test_upload_from_file_w_explicit_client_resumable(self):
        import json
        import mock
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        UPLOAD_PATH = 'https://example.com/upload/test'
        initial_response = {'status': OK, 'location': UPLOAD_PATH}
        upload_response = {'status': OK}
        conn = _Connection(
            (initial_response, b'{}'),
            (upload_response, b'{}'),
        )
        client = _Client(project=self.PROJECT, connection=conn)

        class _UploadConfig(object):
            accept = ['*/*']
            max_size = None
            resumable_multipart = True
            resumable_path = u'/upload/bigquery/v2/projects/{project}/jobs'
            simple_multipart = True
            simple_path = u''  # force resumable

        with mock.patch('google.cloud.bigquery.table._UploadConfig',
                        new=_UploadConfig):
            orig_requested, PATH, BODY = self._upload_from_file_helper(
                allow_jagged_rows=False,
                allow_quoted_newlines=False,
                create_disposition='CREATE_IF_NEEDED',
                encoding='utf8',
                field_delimiter=',',
                ignore_unknown_values=False,
                max_bad_records=0,
                quote_character='"',
                skip_leading_rows=1,
                write_disposition='WRITE_APPEND',
                client=client,
                _explicit_size=True)

        self.assertEqual(len(orig_requested), 0)

        requested = conn.http._requested
        self.assertEqual(len(requested), 2)
        req = requested[0]
        self.assertEqual(req['method'], 'POST')
        uri = req['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/%s' % PATH)
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable'})

        self.assertEqual(req['headers']['content-type'], 'application/json')
        metadata = json.loads(req['body'])
        load_config = metadata['configuration']['load']
        DESTINATION_TABLE = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.TABLE_NAME,
        }
        self.assertEqual(load_config['destinationTable'], DESTINATION_TABLE)
        self.assertEqual(load_config['sourceFormat'], 'CSV')
        self.assertEqual(load_config['allowJaggedRows'], False)
        self.assertEqual(load_config['allowQuotedNewlines'], False)
        self.assertEqual(load_config['createDisposition'], 'CREATE_IF_NEEDED')
        self.assertEqual(load_config['encoding'], 'utf8')
        self.assertEqual(load_config['fieldDelimiter'], ',')
        self.assertEqual(load_config['ignoreUnknownValues'], False)
        self.assertEqual(load_config['maxBadRecords'], 0)
        self.assertEqual(load_config['quote'], '"')
        self.assertEqual(load_config['skipLeadingRows'], 1)
        self.assertEqual(load_config['writeDisposition'], 'WRITE_APPEND')

        req = requested[1]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['uri'], UPLOAD_PATH)
        headers = req['headers']
        length = len(BODY)
        self.assertEqual(headers['Content-Type'], 'application/octet-stream')
        self.assertEqual(headers['Content-Range'],
                         'bytes 0-%d/%d' % (length - 1, length))
        self.assertEqual(headers['content-length'], '%d' % (length,))
        self.assertEqual(req['body'], BODY)
    # pylint: enable=too-many-statements


class Test_parse_schema_resource(unittest.TestCase, _SchemaBase):

    def _call_fut(self, resource):
        from google.cloud.bigquery.table import _parse_schema_resource

        return _parse_schema_resource(resource)

    def _makeResource(self):
        return {
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            ]},
        }

    def test__parse_schema_resource_defaults(self):
        RESOURCE = self._makeResource()
        schema = self._call_fut(RESOURCE['schema'])
        self._verifySchema(schema, RESOURCE)

    def test__parse_schema_resource_subfields(self):
        RESOURCE = self._makeResource()
        RESOURCE['schema']['fields'].append(
            {'name': 'phone',
             'type': 'RECORD',
             'mode': 'REPEATABLE',
             'fields': [{'name': 'type',
                         'type': 'STRING',
                         'mode': 'REQUIRED'},
                        {'name': 'number',
                         'type': 'STRING',
                         'mode': 'REQUIRED'}]})
        schema = self._call_fut(RESOURCE['schema'])
        self._verifySchema(schema, RESOURCE)

    def test__parse_schema_resource_fields_without_mode(self):
        RESOURCE = self._makeResource()
        RESOURCE['schema']['fields'].append(
            {'name': 'phone',
             'type': 'STRING'})

        schema = self._call_fut(RESOURCE['schema'])
        self._verifySchema(schema, RESOURCE)


class Test_build_schema_resource(unittest.TestCase, _SchemaBase):

    def _call_fut(self, resource):
        from google.cloud.bigquery.table import _build_schema_resource

        return _build_schema_resource(resource)

    def test_defaults(self):
        from google.cloud.bigquery.table import SchemaField

        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        resource = self._call_fut([full_name, age])
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0],
                         {'name': 'full_name',
                          'type': 'STRING',
                          'mode': 'REQUIRED'})
        self.assertEqual(resource[1],
                         {'name': 'age',
                          'type': 'INTEGER',
                          'mode': 'REQUIRED'})

    def test_w_description(self):
        from google.cloud.bigquery.table import SchemaField

        DESCRIPTION = 'DESCRIPTION'
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED',
                                description=DESCRIPTION)
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        resource = self._call_fut([full_name, age])
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0],
                         {'name': 'full_name',
                          'type': 'STRING',
                          'mode': 'REQUIRED',
                          'description': DESCRIPTION})
        self.assertEqual(resource[1],
                         {'name': 'age',
                          'type': 'INTEGER',
                          'mode': 'REQUIRED'})

    def test_w_subfields(self):
        from google.cloud.bigquery.table import SchemaField

        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        ph_type = SchemaField('type', 'STRING', 'REQUIRED')
        ph_num = SchemaField('number', 'STRING', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='REPEATABLE',
                            fields=[ph_type, ph_num])
        resource = self._call_fut([full_name, phone])
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0],
                         {'name': 'full_name',
                          'type': 'STRING',
                          'mode': 'REQUIRED'})
        self.assertEqual(resource[1],
                         {'name': 'phone',
                          'type': 'RECORD',
                          'mode': 'REPEATABLE',
                          'fields': [{'name': 'type',
                                      'type': 'STRING',
                                      'mode': 'REQUIRED'},
                                     {'name': 'number',
                                      'type': 'STRING',
                                      'mode': 'REQUIRED'}]})


class _Client(object):

    _query_results = ()

    def __init__(self, project='project', connection=None):
        self.project = project
        self._connection = connection

    def job_from_resource(self, resource):  # pylint: disable=unused-argument
        return self._job

    def run_sync_query(self, query):
        return _Query(query, self)


class _Query(object):

    def __init__(self, query, client):
        self.query = query
        self.rows = []
        self.client = client

    def run(self):
        self.rows = self.client._query_results


class _Dataset(object):

    def __init__(self, client, name=TestTable.DS_NAME):
        self._client = client
        self.name = name

    @property
    def path(self):
        return '/projects/%s/datasets/%s' % (
            self._client.project, self.name)

    @property
    def project(self):
        return self._client.project


class _Responder(object):

    def __init__(self, *responses):
        self._responses = responses[:]
        self._requested = []

    def _respond(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _HTTP(_Responder):

    connections = {}  # For google-apitools debugging.

    def request(self, uri, method, headers, body, **kw):
        if hasattr(body, 'read'):
            body = body.read()
        return self._respond(uri=uri, method=method, headers=headers,
                             body=body, **kw)


class _Connection(_Responder):

    API_BASE_URL = 'http://example.com'
    USER_AGENT = 'testing 1.2.3'

    def __init__(self, *responses):
        super(_Connection, self).__init__(*responses)
        self.http = _HTTP(*responses)

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound

        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except IndexError:
            raise NotFound('miss')
        else:
            return response

    def build_api_url(self, path, query_params=None,
                      api_base_url=API_BASE_URL):
        from six.moves.urllib.parse import urlencode
        from six.moves.urllib.parse import urlsplit
        from six.moves.urllib.parse import urlunsplit

        # Mimic the build_api_url interface.
        qs = urlencode(query_params or {})
        scheme, netloc, _, _, _ = urlsplit(api_base_url)
        return urlunsplit((scheme, netloc, path, qs, ''))


def _email_chunk_parser():
    import six

    if six.PY3:  # pragma: NO COVER  Python3
        from email.parser import BytesParser

        parser = BytesParser()
        return parser.parsebytes
    else:
        from email.parser import Parser

        parser = Parser()
        return parser.parsestr
