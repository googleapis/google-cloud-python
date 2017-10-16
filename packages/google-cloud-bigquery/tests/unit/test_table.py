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

import mock

from google.cloud.bigquery.dataset import DatasetReference


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


class TestTableReference(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import TableReference

        return TableReference

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset_ref = DatasetReference('project_1', 'dataset_1')

        table_ref = self._make_one(dataset_ref, 'table_1')
        self.assertEqual(table_ref.dataset_id, dataset_ref.dataset_id)
        self.assertEqual(table_ref.table_id, 'table_1')

    def test_to_api_repr(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset_ref = DatasetReference('project_1', 'dataset_1')
        table_ref = self._make_one(dataset_ref, 'table_1')

        resource = table_ref.to_api_repr()

        self.assertEqual(
            resource,
            {
                'projectId': 'project_1',
                'datasetId': 'dataset_1',
                'tableId': 'table_1',
            })

    def test_from_api_repr(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import TableReference
        dataset_ref = DatasetReference('project_1', 'dataset_1')
        expected = self._make_one(dataset_ref, 'table_1')

        got = TableReference.from_api_repr(
            {
                'projectId': 'project_1',
                'datasetId': 'dataset_1',
                'tableId': 'table_1',
            })

        self.assertEqual(expected, got)

    def test___eq___wrong_type(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset_ref = DatasetReference('project_1', 'dataset_1')
        table = self._make_one(dataset_ref, 'table_1')
        other = object()
        self.assertNotEqual(table, other)
        self.assertEqual(table, mock.ANY)

    def test___eq___project_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        other_dataset = DatasetReference('project_2', 'dataset_1')
        table = self._make_one(dataset, 'table_1')
        other = self._make_one(other_dataset, 'table_1')
        self.assertNotEqual(table, other)

    def test___eq___dataset_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        other_dataset = DatasetReference('project_1', 'dataset_2')
        table = self._make_one(dataset, 'table_1')
        other = self._make_one(other_dataset, 'table_1')
        self.assertNotEqual(table, other)

    def test___eq___table_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        table = self._make_one(dataset, 'table_1')
        other = self._make_one(dataset, 'table_2')
        self.assertNotEqual(table, other)

    def test___eq___equality(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        table = self._make_one(dataset, 'table_1')
        other = self._make_one(dataset, 'table_1')
        self.assertEqual(table, other)

    def test___hash__set_equality(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        table1 = self._make_one(dataset, 'table1')
        table2 = self._make_one(dataset, 'table2')
        set_one = {table1, table2}
        set_two = {table1, table2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        from google.cloud.bigquery.dataset import DatasetReference
        dataset = DatasetReference('project_1', 'dataset_1')
        table1 = self._make_one(dataset, 'table1')
        table2 = self._make_one(dataset, 'table2')
        set_one = {table1}
        set_two = {table2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        dataset = DatasetReference('project1', 'dataset1')
        table1 = self._make_one(dataset, 'table1')
        expected = "TableReference('project1', 'dataset1', 'table1')"
        self.assertEqual(repr(table1), expected)


class TestTable(unittest.TestCase, _SchemaBase):

    PROJECT = 'prahj-ekt'
    DS_ID = 'dataset-name'
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
        self.TABLE_FULL_ID = '%s:%s:%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.NUM_BYTES = 12345
        self.NUM_ROWS = 67
        self.NUM_EST_BYTES = 1234
        self.NUM_EST_ROWS = 23

    def _makeResource(self):
        self._setUpConstants()
        return {
            'creationTime': self.WHEN_TS * 1000,
            'tableReference':
                {'projectId': self.PROJECT,
                 'datasetId': self.DS_ID,
                 'tableId': self.TABLE_NAME},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'etag': 'ETAG',
            'id': self.TABLE_FULL_ID,
            'lastModifiedTime': self.WHEN_TS * 1000,
            'location': 'US',
            'selfLink': self.RESOURCE_URL,
            'numRows': self.NUM_ROWS,
            'numBytes': self.NUM_BYTES,
            'type': 'TABLE',
            'streamingBuffer': {
                'estimatedRows': str(self.NUM_EST_ROWS),
                'estimatedBytes': str(self.NUM_EST_BYTES),
                'oldestEntryTime': self.WHEN_TS * 1000},
            'externalDataConfiguration': {
                'sourceFormat': 'CSV',
                'csvOptions': {
                    'allowJaggedRows': True,
                    'encoding': 'encoding'}},
            'labels': {'x': 'y'},
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

        if 'streamingBuffer' in resource:
            self.assertEqual(table.streaming_buffer.estimated_rows,
                             self.NUM_EST_ROWS)
            self.assertEqual(table.streaming_buffer.estimated_bytes,
                             self.NUM_EST_BYTES)
            self.assertEqual(table.streaming_buffer.oldest_entry_time,
                             self.WHEN)
        else:
            self.assertIsNone(table.streaming_buffer)

        self.assertEqual(table.full_table_id, self.TABLE_FULL_ID)
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
            self.assertEqual(
                table.view_use_legacy_sql,
                resource['view'].get('useLegacySql', True))
        else:
            self.assertIsNone(table.view_query)
            self.assertIsNone(table.view_use_legacy_sql)

        if 'schema' in resource:
            self._verifySchema(table.schema, resource)
        else:
            self.assertEqual(table.schema, [])

        if 'externalDataConfiguration' in resource:
            edc = table.external_data_configuration
            self.assertEqual(edc.source_format, 'CSV')
            self.assertEqual(edc.options.allow_jagged_rows, True)

        if 'labels' in resource:
            self.assertEqual(table.labels, {'x': 'y'})
        else:
            self.assertEqual(table.labels, {})

    def test_ctor(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        self.assertEqual(table.table_id, self.TABLE_NAME)
        self.assertEqual(table.project, self.PROJECT)
        self.assertEqual(table.dataset_id, self.DS_ID)
        self.assertEqual(
            table.path,
            '/projects/%s/datasets/%s/tables/%s' % (
                self.PROJECT, self.DS_ID, self.TABLE_NAME))
        self.assertEqual(table.schema, [])

        self.assertIsNone(table.created)
        self.assertIsNone(table.etag)
        self.assertIsNone(table.modified)
        self.assertIsNone(table.num_bytes)
        self.assertIsNone(table.num_rows)
        self.assertIsNone(table.self_link)
        self.assertIsNone(table.full_table_id)
        self.assertIsNone(table.table_type)
        self.assertIsNone(table.description)
        self.assertIsNone(table.expires)
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.location)
        self.assertIsNone(table.view_query)
        self.assertIsNone(table.view_use_legacy_sql)
        self.assertIsNone(table.external_data_configuration)
        self.assertEquals(table.labels, {})

    def test_ctor_w_schema(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])

        self.assertEqual(table.schema, [full_name, age])

    def test_num_bytes_getter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

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
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

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
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(TypeError):
            table.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            table.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
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
        TABLE_FULL_ID = '%s:%s:%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_NAME)
        URL = 'http://example.com/projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_NAME)
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties['creationTime'] = _millis(CREATED)
        table._properties['etag'] = 'ETAG'
        table._properties['lastModifiedTime'] = _millis(MODIFIED)
        table._properties['numBytes'] = 12345
        table._properties['numRows'] = 66
        table._properties['selfLink'] = URL
        table._properties['id'] = TABLE_FULL_ID
        table._properties['type'] = 'TABLE'

        self.assertEqual(table.created, CREATED)
        self.assertEqual(table.etag, 'ETAG')
        self.assertEqual(table.modified, MODIFIED)
        self.assertEqual(table.num_bytes, 12345)
        self.assertEqual(table.num_rows, 66)
        self.assertEqual(table.self_link, URL)
        self.assertEqual(table.full_table_id, TABLE_FULL_ID)
        self.assertEqual(table.table_type, 'TABLE')

    def test_description_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.description = 12345

    def test_description_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.description = 'DESCRIPTION'
        self.assertEqual(table.description, 'DESCRIPTION')

    def test_expires_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.expires = object()

    def test_expires_setter(self):
        import datetime
        from google.cloud._helpers import UTC

        WHEN = datetime.datetime(2015, 7, 28, 16, 39, tzinfo=UTC)
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.expires = WHEN
        self.assertEqual(table.expires, WHEN)

    def test_friendly_name_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.friendly_name = 12345

    def test_friendly_name_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.friendly_name = 'FRIENDLY'
        self.assertEqual(table.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.location = 12345

    def test_location_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.location = 'LOCATION'
        self.assertEqual(table.location, 'LOCATION')

    def test_view_query_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.view_query = 12345

    def test_view_query_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.view_query = 'select * from foo'
        self.assertEqual(table.view_query, 'select * from foo')
        self.assertEqual(table.view_use_legacy_sql, False)

        table.view_use_legacy_sql = True
        self.assertEqual(table.view_use_legacy_sql, True)

    def test_view_query_deleter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.view_query = 'select * from foo'
        del table.view_query
        self.assertIsNone(table.view_query)
        self.assertIsNone(table.view_use_legacy_sql)

    def test_view_use_legacy_sql_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.view_use_legacy_sql = 12345

    def test_view_use_legacy_sql_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.view_use_legacy_sql = True
        table.view_query = 'select * from foo'
        self.assertEqual(table.view_use_legacy_sql, True)
        self.assertEqual(table.view_query, 'select * from foo')

    def test_external_data_configuration_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.external_data_configuration = 12345

    def test_labels_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.labels = 12345

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        RESOURCE = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_NAME,
            },
            'type': 'TABLE',
        }
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self.assertEqual(table.table_id, self.TABLE_NAME)
        self._verifyResourceProperties(table, RESOURCE)

    def test_from_api_repr_w_properties(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        RESOURCE = self._makeResource()
        RESOURCE['view'] = {'query': 'select fullname, age from person_ages'}
        RESOURCE['type'] = 'VIEW'
        RESOURCE['location'] = 'EU'
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        RESOURCE['expirationTime'] = _millis(self.EXP_TIME)
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self._verifyResourceProperties(table, RESOURCE)

    def test_partition_type_setter_bad_type(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partitioning_type = 123

    def test_partition_type_setter_unknown_value(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partitioning_type = "HASH"

    def test_partition_type_setter_w_known_value(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        self.assertIsNone(table.partitioning_type)
        table.partitioning_type = 'DAY'
        self.assertEqual(table.partitioning_type, 'DAY')

    def test_partition_type_setter_w_none(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        table._properties['timePartitioning'] = {'type': 'DAY'}
        table.partitioning_type = None
        self.assertIsNone(table.partitioning_type)
        self.assertFalse('timePartitioning' in table._properties)

    def test_partition_experation_bad_type(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        with self.assertRaises(ValueError):
            table.partition_expiration = "NEVER"

    def test_partition_expiration_w_integer(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table.partition_expiration = 100
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(table.partition_expiration, 100)

    def test_partition_expiration_w_none(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
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

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = self._make_one(table_ref, schema=[full_name, age])
        self.assertIsNone(table.partition_expiration)
        table.partition_expiration = None
        self.assertIsNone(table.partitioning_type)
        self.assertIsNone(table.partition_expiration)


class Test_row_from_mapping(unittest.TestCase, _SchemaBase):

    PROJECT = 'prahj-ekt'
    DS_ID = 'dataset-name'
    TABLE_NAME = 'table-name'

    def _call_fut(self, mapping, schema):
        from google.cloud.bigquery.table import _row_from_mapping

        return _row_from_mapping(mapping, schema)

    def test__row_from_mapping_wo_schema(self):
        from google.cloud.bigquery.table import Table, _TABLE_HAS_NO_SCHEMA
        MAPPING = {'full_name': 'Phred Phlyntstone', 'age': 32}
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = Table(table_ref)

        with self.assertRaises(ValueError) as exc:
            self._call_fut(MAPPING, table.schema)

        self.assertEqual(exc.exception.args, (_TABLE_HAS_NO_SCHEMA,))

    def test__row_from_mapping_w_invalid_schema(self):
        from google.cloud.bigquery.table import Table, SchemaField
        MAPPING = {
            'full_name': 'Phred Phlyntstone',
            'age': 32,
            'colors': ['red', 'green'],
            'bogus': 'WHATEVER',
        }
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        colors = SchemaField('colors', 'DATETIME', mode='REPEATED')
        bogus = SchemaField('joined', 'STRING', mode='BOGUS')
        table = Table(table_ref, schema=[full_name, age, colors, bogus])

        with self.assertRaises(ValueError) as exc:
            self._call_fut(MAPPING, table.schema)

        self.assertIn('Unknown field mode: BOGUS', str(exc.exception))

    def test__row_from_mapping_w_schema(self):
        from google.cloud.bigquery.table import Table, SchemaField
        MAPPING = {
            'full_name': 'Phred Phlyntstone',
            'age': 32,
            'colors': ['red', 'green'],
            'extra': 'IGNORED',
        }
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        colors = SchemaField('colors', 'DATETIME', mode='REPEATED')
        joined = SchemaField('joined', 'STRING', mode='NULLABLE')
        table = Table(table_ref, schema=[full_name, age, colors, joined])

        self.assertEqual(
            self._call_fut(MAPPING, table.schema),
            ('Phred Phlyntstone', 32, ['red', 'green'], None))
