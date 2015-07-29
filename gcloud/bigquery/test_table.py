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


class TestTable(unittest2.TestCase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'
    TABLE_NAME = 'table-name'

    def _getTargetClass(self):
        from gcloud.bigquery.table import Table
        return Table

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertTrue(table._dataset is dataset)
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
        import pytz
        from gcloud.bigquery._helpers import _millis
        CREATED = datetime.datetime(2015, 7, 29, 12, 13, 22, tzinfo=pytz.utc)
        MODIFIED = datetime.datetime(2015, 7, 29, 14, 47, 15, tzinfo=pytz.utc)
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
        import pytz
        WHEN = datetime.datetime(2015, 7, 28, 16, 39, tzinfo=pytz.utc)
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


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Dataset(object):

    def __init__(self, client, name=TestTable.DS_NAME):
        self._client = client
        self._name = name

    @property
    def path(self):
        return '/projects/%s/datasets/%s' % (
            self._client.project, self._name)
