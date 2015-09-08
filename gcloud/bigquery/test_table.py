# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestSchemaField(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.table import SchemaField
        return SchemaField

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        field = self._makeOne('test', 'STRING')
        self.assertEqual(field.name, 'test')
        self.assertEqual(field.field_type, 'STRING')
        self.assertEqual(field.mode, 'NULLABLE')
        self.assertEqual(field.description, None)
        self.assertEqual(field.fields, None)

    def test_ctor_explicit(self):
        field = self._makeOne('test', 'STRING', mode='REQUIRED',
                              description='Testing')
        self.assertEqual(field.name, 'test')
        self.assertEqual(field.field_type, 'STRING')
        self.assertEqual(field.mode, 'REQUIRED')
        self.assertEqual(field.description, 'Testing')
        self.assertEqual(field.fields, None)

    def test_ctor_subfields(self):
        field = self._makeOne('phone_number', 'RECORD',
                              fields=[self._makeOne('area_code', 'STRING'),
                                      self._makeOne('local_number', 'STRING')])
        self.assertEqual(field.name, 'phone_number')
        self.assertEqual(field.field_type, 'RECORD')
        self.assertEqual(field.mode, 'NULLABLE')
        self.assertEqual(field.description, None)
        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0].name, 'area_code')
        self.assertEqual(field.fields[0].field_type, 'STRING')
        self.assertEqual(field.fields[0].mode, 'NULLABLE')
        self.assertEqual(field.fields[0].description, None)
        self.assertEqual(field.fields[0].fields, None)
        self.assertEqual(field.fields[1].name, 'local_number')
        self.assertEqual(field.fields[1].field_type, 'STRING')
        self.assertEqual(field.fields[1].mode, 'NULLABLE')
        self.assertEqual(field.fields[1].description, None)
        self.assertEqual(field.fields[1].fields, None)


class _SchemaBase(object):

    def _verify_field(self, field, r_field):
        self.assertEqual(field.name, r_field['name'])
        self.assertEqual(field.field_type, r_field['type'])
        self.assertEqual(field.mode, r_field['mode'])

    def _verifySchema(self, schema, resource):
        r_fields = resource['schema']['fields']
        self.assertEqual(len(schema), len(r_fields))

        for field, r_field in zip(schema, r_fields):
            self._verify_field(field, r_field)


class TestTable(unittest2.TestCase, _SchemaBase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'
    TABLE_NAME = 'table-name'

    def _getTargetClass(self):
        from gcloud.bigquery.table import Table
        return Table

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from gcloud._helpers import UTC

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
            self.assertEqual(table.created, None)

        if 'etag' in resource:
            self.assertEqual(table.etag, self.ETAG)
        else:
            self.assertEqual(table.etag, None)

        if 'numRows' in resource:
            self.assertEqual(table.num_rows, self.NUM_ROWS)
        else:
            self.assertEqual(table.num_rows, None)

        if 'numBytes' in resource:
            self.assertEqual(table.num_bytes, self.NUM_BYTES)
        else:
            self.assertEqual(table.num_bytes, None)

        if 'selfLink' in resource:
            self.assertEqual(table.self_link, self.RESOURCE_URL)
        else:
            self.assertEqual(table.self_link, None)

        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table.table_type,
                         'TABLE' if 'view' not in resource else 'VIEW')

    def _verifyResourceProperties(self, table, resource):

        self._verifyReadonlyResourceProperties(table, resource)

        if 'expirationTime' in resource:
            self.assertEqual(table.expires, self.EXP_TIME)
        else:
            self.assertEqual(table.expires, None)

        self.assertEqual(table.description, resource.get('description'))
        self.assertEqual(table.friendly_name, resource.get('friendlyName'))
        self.assertEqual(table.location, resource.get('location'))

        if 'view' in resource:
            self.assertEqual(table.view_query, resource['view']['query'])
        else:
            self.assertEqual(table.view_query, None)

        if 'schema' in resource:
            self._verifySchema(table.schema, resource)
        else:
            self.assertEqual(table.schema, [])

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertTrue(table._dataset is dataset)
        self.assertEqual(table.project, self.PROJECT)
        self.assertEqual(table.dataset_name, self.DS_NAME)
        self.assertEqual(
            table.path,
            '/projects/%s/datasets/%s/tables/%s' % (
                self.PROJECT, self.DS_NAME, self.TABLE_NAME))
        self.assertEqual(table.schema, [])

        self.assertEqual(table.created, None)
        self.assertEqual(table.etag, None)
        self.assertEqual(table.modified, None)
        self.assertEqual(table.num_bytes, None)
        self.assertEqual(table.num_rows, None)
        self.assertEqual(table.self_link, None)
        self.assertEqual(table.table_id, None)
        self.assertEqual(table.table_type, None)

        self.assertEqual(table.description, None)
        self.assertEqual(table.expires, None)
        self.assertEqual(table.friendly_name, None)
        self.assertEqual(table.location, None)
        self.assertEqual(table.view_query, None)

    def test_ctor_w_schema(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._makeOne(self.TABLE_NAME, dataset,
                              schema=[full_name, age])
        self.assertEqual(table.schema, [full_name, age])

    def test_schema_setter_non_list(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(TypeError):
            table.schema = object()

    def test_schema_setter_invalid_field(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            table.schema = [full_name, object()]

    def test_schema_setter(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table.schema = [full_name, age]
        self.assertEqual(table.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud._helpers import _millis

        CREATED = datetime.datetime(2015, 7, 29, 12, 13, 22, tzinfo=UTC)
        MODIFIED = datetime.datetime(2015, 7, 29, 14, 47, 15, tzinfo=UTC)
        TABLE_ID = '%s:%s:%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        URL = 'http://example.com/projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
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
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.description = 12345

    def test_description_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.description = 'DESCRIPTION'
        self.assertEqual(table.description, 'DESCRIPTION')

    def test_expires_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.expires = object()

    def test_expires_setter(self):
        import datetime
        from gcloud._helpers import UTC

        WHEN = datetime.datetime(2015, 7, 28, 16, 39, tzinfo=UTC)
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.expires = WHEN
        self.assertEqual(table.expires, WHEN)

    def test_friendly_name_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.friendly_name = 12345

    def test_friendly_name_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.friendly_name = 'FRIENDLY'
        self.assertEqual(table.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.location = 12345

    def test_location_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.location = 'LOCATION'
        self.assertEqual(table.location, 'LOCATION')

    def test_view_query_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.view_query = 12345

    def test_view_query_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.view_query = 'select * from foo'
        self.assertEqual(table.view_query, 'select * from foo')

    def test_view_query_deleter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.view_query = 'select * from foo'
        del table.view_query
        self.assertEqual(table.view_query, None)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        RESOURCE = {}
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
        table = klass.from_api_repr(RESOURCE, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertTrue(table._dataset is dataset)
        self._verifyResourceProperties(table, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        table = klass.from_api_repr(RESOURCE, dataset)
        self.assertTrue(table._dataset._client is client)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_w_bound_client(self):
        from gcloud.bigquery.table import SchemaField
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._makeOne(self.TABLE_NAME, dataset,
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

    def test_create_w_alternate_client(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud._helpers import _millis
        from gcloud.bigquery.table import SchemaField

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
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
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'description': DESCRIPTION,
            'friendlyName': TITLE,
            'view': {'query': QUERY},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(table, RESOURCE)

    def test_create_w_missing_output_properties(self):
        # In the wild, the resource returned from 'dataset.create' sometimes
        # lacks 'creationTime' / 'lastModifiedTime'
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset,
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        from gcloud._helpers import UTC
        from gcloud._helpers import _millis
        from gcloud.bigquery.table import SchemaField

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

        table.patch(schema=None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {'schema': None}
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(table, RESOURCE)

    def test_update_w_bound_client(self):
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
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
        from gcloud._helpers import UTC
        from gcloud._helpers import _millis
        from gcloud.bigquery.table import SchemaField

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
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, age])
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
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset)

        table.delete(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_bound_client(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud.bigquery.table import SchemaField

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
            'totalRows': ROWS,
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, age, joined])

        rows, total_rows, page_token = table.fetch_data()

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
        from gcloud.bigquery.table import SchemaField
        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        MAX = 10
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, age, voter, score])

        rows, total_rows, page_token = table.fetch_data(client=client2,
                                                        max_results=MAX,
                                                        page_token=TOKEN)

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32, True, 3.1415926))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33, False, 1.414))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29, True, 2.71828))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27, None, None))
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, None)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': MAX, 'pageToken': TOKEN})

    def test_fetch_data_w_repeated_fields(self):
        from gcloud.bigquery.table import SchemaField
        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_NAME, self.TABLE_NAME)
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': ['red', 'green']},
                    {'v': [{'f': [{'v': ['1', '2']},
                                  {'v': ['3.1415', '1.414']}]}]},
                ]},
            ]
        }
        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = _Dataset(client)
        full_name = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, struct])

        rows, total_rows, page_token = table.fetch_data()

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
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, phone])

        rows, total_rows, page_token = table.fetch_data()

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
        self.assertEqual(rows[2][1], None)
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_insert_data_w_bound_client(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud._helpers import _millis_from_datetime
        from gcloud.bigquery.table import SchemaField

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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
                              schema=[full_name, age, joined])
        ROWS = [
            ('Phred Phlyntstone', 32, WHEN),
            ('Bharney Rhubble', 33, WHEN + datetime.timedelta(seconds=1)),
            ('Wylma Phlyntstone', 29, WHEN + datetime.timedelta(seconds=2)),
            ('Bhettye Rhubble', 27, None),
        ]

        def _row_data(row):
            return {'full_name': row[0],
                    'age': row[1],
                    'joined': _millis_from_datetime(row[2])}

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
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
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
            'rows': [{'insertId': index, 'json': _row_data(row)}
                     for index, row in enumerate(ROWS)],
        }

        errors = table.insert_data(
            client=client2,
            rows=ROWS,
            row_ids=[index for index, _ in enumerate(ROWS)],
            skip_invalid_rows=True,
            ignore_unknown_values=True)

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
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
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
        from gcloud.bigquery.table import SchemaField
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
        table = self._makeOne(self.TABLE_NAME, dataset=dataset,
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


class Test_parse_schema_resource(unittest2.TestCase, _SchemaBase):

    def _callFUT(self, resource):
        from gcloud.bigquery.table import _parse_schema_resource
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
        schema = self._callFUT(RESOURCE['schema'])
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
        schema = self._callFUT(RESOURCE['schema'])
        self._verifySchema(schema, RESOURCE)


class Test_build_schema_resource(unittest2.TestCase, _SchemaBase):

    def _callFUT(self, resource):
        from gcloud.bigquery.table import _build_schema_resource
        return _build_schema_resource(resource)

    def test_defaults(self):
        from gcloud.bigquery.table import SchemaField
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        resource = self._callFUT([full_name, age])
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
        from gcloud.bigquery.table import SchemaField
        DESCRIPTION = 'DESCRIPTION'
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED',
                                description=DESCRIPTION)
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        resource = self._callFUT([full_name, age])
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
        from gcloud.bigquery.table import SchemaField
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        ph_type = SchemaField('type', 'STRING', 'REQUIRED')
        ph_num = SchemaField('number', 'STRING', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='REPEATABLE',
                            fields=[ph_type, ph_num])
        resource = self._callFUT([full_name, phone])
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

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


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


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response
