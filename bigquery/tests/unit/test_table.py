# Copyright 2015 Google LLC
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
import six
try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None

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


class TestEncryptionConfiguration(unittest.TestCase):
    KMS_KEY_NAME = 'projects/1/locations/global/keyRings/1/cryptoKeys/1'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import EncryptionConfiguration

        return EncryptionConfiguration

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        encryption_config = self._make_one()
        self.assertIsNone(encryption_config.kms_key_name)

    def test_ctor_with_key(self):
        encryption_config = self._make_one(kms_key_name=self.KMS_KEY_NAME)
        self.assertEqual(encryption_config.kms_key_name, self.KMS_KEY_NAME)

    def test_kms_key_name_setter(self):
        encryption_config = self._make_one()
        self.assertIsNone(encryption_config.kms_key_name)
        encryption_config.kms_key_name = self.KMS_KEY_NAME
        self.assertEqual(encryption_config.kms_key_name, self.KMS_KEY_NAME)
        encryption_config.kms_key_name = None
        self.assertIsNone(encryption_config.kms_key_name)

    def test_from_api_repr(self):
        RESOURCE = {
            'kmsKeyName': self.KMS_KEY_NAME,
        }
        klass = self._get_target_class()
        encryption_config = klass.from_api_repr(RESOURCE)
        self.assertEqual(encryption_config.kms_key_name, self.KMS_KEY_NAME)

    def test_to_api_repr(self):
        encryption_config = self._make_one(kms_key_name=self.KMS_KEY_NAME)
        resource = encryption_config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'kmsKeyName': self.KMS_KEY_NAME,
            })


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

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string('string-project.string_dataset.string_table')
        self.assertEqual(got.project, 'string-project')
        self.assertEqual(got.dataset_id, 'string_dataset')
        self.assertEqual(got.table_id, 'string_table')

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string('string-project:string_dataset.string_table')

    def test_from_string_not_fully_qualified(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string('string_dataset.string_table')

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
        expected = (
            "TableReference(DatasetReference('project1', 'dataset1'), "
            "'table1')"
        )
        self.assertEqual(repr(table1), expected)


class TestTable(unittest.TestCase, _SchemaBase):

    PROJECT = 'prahj-ekt'
    DS_ID = 'dataset-name'
    TABLE_NAME = 'table-name'
    KMS_KEY_NAME = 'projects/1/locations/global/keyRings/1/cryptoKeys/1'

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
        self.TABLE_FULL_ID = '%s:%s.%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.NUM_BYTES = 12345
        self.NUM_ROWS = 67
        self.NUM_EST_BYTES = 1234
        self.NUM_EST_ROWS = 23

    def _make_resource(self):
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

        if 'encryptionConfiguration' in resource:
            self.assertIsNotNone(table.encryption_configuration)
            self.assertEqual(table.encryption_configuration.kms_key_name,
                             resource['encryptionConfiguration']['kmsKeyName'])
        else:
            self.assertIsNone(table.encryption_configuration)

    def test_ctor(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        self.assertEqual(table.table_id, self.TABLE_NAME)
        self.assertEqual(table.project, self.PROJECT)
        self.assertEqual(table.dataset_id, self.DS_ID)
        self.assertEqual(table.reference.table_id, self.TABLE_NAME)
        self.assertEqual(table.reference.project, self.PROJECT)
        self.assertEqual(table.reference.dataset_id, self.DS_ID)
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
        self.assertIsNone(table.encryption_configuration)
        self.assertIsNone(table.time_partitioning)
        self.assertIsNone(table.clustering_fields)

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
        TABLE_FULL_ID = '%s:%s.%s' % (
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

    def test_external_data_configuration_setter(self):
        from google.cloud.bigquery.external_config import ExternalConfig

        external_config = ExternalConfig('CSV')
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.external_data_configuration = external_config

        self.assertEqual(
            table.external_data_configuration.source_format,
            external_config.source_format)

    def test_external_data_configuration_setter_none(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.external_data_configuration = None

        self.assertIsNone(table.external_data_configuration)

    def test_external_data_configuration_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.external_data_configuration = 12345

    def test_labels_update_in_place(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        del table._properties['labels']  # don't start w/ existing dict
        labels = table.labels
        labels['foo'] = 'bar'  # update in place
        self.assertEqual(table.labels, {'foo': 'bar'})

    def test_labels_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.labels = 12345

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string('string-project.string_dataset.string_table')
        self.assertEqual(got.project, 'string-project')
        self.assertEqual(got.dataset_id, 'string_dataset')
        self.assertEqual(got.table_id, 'string_table')

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string('string-project:string_dataset.string_table')

    def test_from_string_not_fully_qualified(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string('string_dataset.string_table')

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        RESOURCE = {
            'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
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

        RESOURCE = self._make_resource()
        RESOURCE['view'] = {'query': 'select fullname, age from person_ages'}
        RESOURCE['type'] = 'VIEW'
        RESOURCE['location'] = 'EU'
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        RESOURCE['expirationTime'] = _millis(self.EXP_TIME)
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self._verifyResourceProperties(table, RESOURCE)

    def test_from_api_with_encryption(self):
        self._setUpConstants()
        RESOURCE = {
            'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_NAME,
            },
            'encryptionConfiguration': {
                'kmsKeyName': self.KMS_KEY_NAME
            },
            'type': 'TABLE',
        }
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self._verifyResourceProperties(table, RESOURCE)

    def test_to_api_repr_w_custom_field(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties['newAlphaProperty'] = 'unreleased property'
        resource = table.to_api_repr()

        exp_resource = {
            'tableReference': table_ref.to_api_repr(),
            'labels': {},
            'newAlphaProperty': 'unreleased property'
        }
        self.assertEqual(resource, exp_resource)

    def test__build_resource_w_custom_field(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties['newAlphaProperty'] = 'unreleased property'
        resource = table._build_resource(['newAlphaProperty'])

        exp_resource = {
            'newAlphaProperty': 'unreleased property'
        }
        self.assertEqual(resource, exp_resource)

    def test__build_resource_w_custom_field_not_in__properties(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table = self._make_one(dataset.table(self.TABLE_NAME))
        table.bad = 'value'
        with self.assertRaises(ValueError):
            table._build_resource(['bad'])

    def test_time_partitioning_setter(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY)

        table.time_partitioning = time_partitioning

        self.assertEqual(
            table.time_partitioning.type_, TimePartitioningType.DAY)
        # Both objects point to the same properties dict
        self.assertIs(
            table._properties['timePartitioning'],
            time_partitioning._properties)

        time_partitioning.expiration_ms = 10000

        # Changes to TimePartitioning object are reflected in Table properties
        self.assertEqual(
            table.time_partitioning.expiration_ms,
            time_partitioning.expiration_ms)

    def test_time_partitioning_setter_bad_type(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        with self.assertRaises(ValueError):
            table.time_partitioning = {'timePartitioning': {'type': 'DAY'}}

    def test_time_partitioning_setter_none(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.time_partitioning = None

        self.assertIsNone(table.time_partitioning)

    def test_partitioning_type_setter(self):
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        with mock.patch('warnings.warn') as warn_patch:
            self.assertIsNone(table.partitioning_type)

            table.partitioning_type = TimePartitioningType.DAY

            self.assertEqual(table.partitioning_type, 'DAY')

        assert warn_patch.called

    def test_partitioning_type_setter_w_time_partitioning_set(self):
        from google.cloud.bigquery.table import TimePartitioning

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.time_partitioning = TimePartitioning()

        with mock.patch('warnings.warn') as warn_patch:
            table.partitioning_type = 'NEW_FAKE_TYPE'

            self.assertEqual(table.partitioning_type, 'NEW_FAKE_TYPE')

        assert warn_patch.called

    def test_partitioning_expiration_setter_w_time_partitioning_set(self):
        from google.cloud.bigquery.table import TimePartitioning

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.time_partitioning = TimePartitioning()

        with mock.patch('warnings.warn') as warn_patch:
            table.partition_expiration = 100000

            self.assertEqual(table.partition_expiration, 100000)

        assert warn_patch.called

    def test_partition_expiration_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        with mock.patch('warnings.warn') as warn_patch:
            self.assertIsNone(table.partition_expiration)

            table.partition_expiration = 100

            self.assertEqual(table.partition_expiration, 100)
            # defaults to 'DAY' when expiration is set and type is not set
            self.assertEqual(table.partitioning_type, 'DAY')

        assert warn_patch.called

    def test_clustering_fields_setter_w_fields(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        fields = ['email', 'phone']

        table.clustering_fields = fields
        self.assertEqual(table.clustering_fields, fields)
        self.assertEqual(table._properties['clustering'], {'fields': fields})

    def test_clustering_fields_setter_w_none(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        fields = ['email', 'phone']

        table._properties['clustering'] = {'fields': fields}
        table.clustering_fields = None
        self.assertEqual(table.clustering_fields, None)
        self.assertFalse('clustering' in table._properties)

    def test_clustering_fields_setter_w_none_noop(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.clustering_fields = None
        self.assertEqual(table.clustering_fields, None)
        self.assertFalse('clustering' in table._properties)

    def test_encryption_configuration_setter(self):
        from google.cloud.bigquery.table import EncryptionConfiguration
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME)
        table.encryption_configuration = encryption_configuration
        self.assertEqual(table.encryption_configuration.kms_key_name,
                         self.KMS_KEY_NAME)
        table.encryption_configuration = None
        self.assertIsNone(table.encryption_configuration)

    def test___repr__(self):
        from google.cloud.bigquery.table import TableReference
        dataset = DatasetReference('project1', 'dataset1')
        table1 = self._make_one(TableReference(dataset, 'table1'))
        expected = (
            "Table(TableReference("
            "DatasetReference('project1', 'dataset1'), "
            "'table1'))"
        )
        self.assertEqual(repr(table1), expected)


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


class TestTableListItem(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import TableListItem

        return TableListItem

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        project = 'test-project'
        dataset_id = 'test_dataset'
        table_id = 'coffee_table'
        resource = {
            'kind': 'bigquery#table',
            'id': '{}:{}.{}'.format(project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id,
            },
            'friendlyName': 'Mahogany Coffee Table',
            'type': 'TABLE',
            'timePartitioning': {
                'type': 'DAY',
                'field': 'mycolumn',
                'expirationMs': '10000',
            },
            'labels': {
                'some-stuff': 'this-is-a-label',
            },
        }

        table = self._make_one(resource)
        self.assertEqual(table.project, project)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(
            table.full_table_id,
            '{}:{}.{}'.format(project, dataset_id, table_id))
        self.assertEqual(table.reference.project, project)
        self.assertEqual(table.reference.dataset_id, dataset_id)
        self.assertEqual(table.reference.table_id, table_id)
        self.assertEqual(table.friendly_name, 'Mahogany Coffee Table')
        self.assertEqual(table.table_type, 'TABLE')
        self.assertEqual(table.time_partitioning.type_, 'DAY')
        self.assertEqual(table.time_partitioning.expiration_ms, 10000)
        self.assertEqual(table.time_partitioning.field, 'mycolumn')
        self.assertEqual(table.partitioning_type, 'DAY')
        self.assertEqual(table.partition_expiration, 10000)
        self.assertEqual(table.labels['some-stuff'], 'this-is-a-label')
        self.assertIsNone(table.view_use_legacy_sql)

    def test_ctor_view(self):
        project = 'test-project'
        dataset_id = 'test_dataset'
        table_id = 'just_looking'
        resource = {
            'kind': 'bigquery#table',
            'id': '{}:{}.{}'.format(project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id,
            },
            'type': 'VIEW',
        }

        table = self._make_one(resource)
        self.assertEqual(table.project, project)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(
            table.full_table_id,
            '{}:{}.{}'.format(project, dataset_id, table_id))
        self.assertEqual(table.reference.project, project)
        self.assertEqual(table.reference.dataset_id, dataset_id)
        self.assertEqual(table.reference.table_id, table_id)
        self.assertEqual(table.table_type, 'VIEW')
        # Server default for useLegacySql is True.
        self.assertTrue(table.view_use_legacy_sql)

    def test_ctor_missing_properties(self):
        resource = {
            'tableReference': {
                'projectId': 'testproject',
                'datasetId': 'testdataset',
                'tableId': 'testtable',
            },
        }
        table = self._make_one(resource)
        self.assertEqual(table.project, 'testproject')
        self.assertEqual(table.dataset_id, 'testdataset')
        self.assertEqual(table.table_id, 'testtable')
        self.assertIsNone(table.full_table_id)
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.table_type)
        self.assertIsNone(table.time_partitioning)
        self.assertIsNone(table.partitioning_type)
        self.assertIsNone(table.partition_expiration)
        self.assertEqual(table.labels, {})
        self.assertIsNone(table.view_use_legacy_sql)

    def test_ctor_wo_project(self):
        resource = {
            'tableReference': {
                'datasetId': 'testdataset',
                'tableId': 'testtable',
            },
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_dataset(self):
        resource = {
            'tableReference': {
                'projectId': 'testproject',
                'tableId': 'testtable',
            },
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_table(self):
        resource = {
            'tableReference': {
                'projectId': 'testproject',
                'datasetId': 'testdataset',
            },
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_reference(self):
        with self.assertRaises(ValueError):
            self._make_one({})

    def test_labels_update_in_place(self):
        resource = {
            'tableReference': {
                'projectId': 'testproject',
                'datasetId': 'testdataset',
                'tableId': 'testtable',
            },
        }
        table = self._make_one(resource)
        labels = table.labels
        labels['foo'] = 'bar'  # update in place
        self.assertEqual(table.labels, {'foo': 'bar'})


class TestRow(unittest.TestCase):

    def test_row(self):
        from google.cloud.bigquery.table import Row

        VALUES = (1, 2, 3)
        row = Row(VALUES, {'a': 0, 'b': 1, 'c': 2})
        self.assertEqual(row.a, 1)
        self.assertEqual(row[1], 2)
        self.assertEqual(row['c'], 3)
        self.assertEqual(len(row), 3)
        self.assertEqual(row.values(), VALUES)
        self.assertEqual(set(row.keys()), set({'a': 1, 'b': 2, 'c': 3}.keys()))
        self.assertEqual(set(row.items()),
                         set({'a': 1, 'b': 2, 'c': 3}.items()))
        self.assertEqual(row.get('a'), 1)
        self.assertEqual(row.get('d'), None)
        self.assertEqual(row.get('d', ''), '')
        self.assertEqual(row.get('d', default=''), '')
        self.assertEqual(repr(row),
                         "Row((1, 2, 3), {'a': 0, 'b': 1, 'c': 2})")
        self.assertFalse(row != row)
        self.assertFalse(row == 3)
        with self.assertRaises(AttributeError):
            row.z
        with self.assertRaises(KeyError):
            row['z']


class Test_EmptyRowIterator(unittest.TestCase):

    @mock.patch('google.cloud.bigquery.table.pandas', new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        from google.cloud.bigquery.table import _EmptyRowIterator
        row_iterator = _EmptyRowIterator()
        with self.assertRaises(ValueError):
            row_iterator.to_dataframe()

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe(self):
        from google.cloud.bigquery.table import _EmptyRowIterator
        row_iterator = _EmptyRowIterator()
        df = row_iterator.to_dataframe()
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows


class TestRowIterator(unittest.TestCase):

    def test_constructor(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import _item_to_row
        from google.cloud.bigquery.table import _rows_page_start

        client = mock.sentinel.client
        api_request = mock.sentinel.api_request
        path = '/foo'
        schema = []
        iterator = RowIterator(client, api_request, path, schema)

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertEqual(iterator.path, path)
        self.assertIs(iterator.item_to_value, _item_to_row)
        self.assertEqual(iterator._items_key, 'rows')
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator.extra_params, {})
        self.assertIs(iterator._page_start, _rows_page_start)
        # Changing attributes.
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.num_results, 0)

    def test_iterate(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        rows = [
            {'f': [{'v': 'Phred Phlyntstone'}, {'v': '32'}]},
            {'f': [{'v': 'Bharney Rhubble'}, {'v': '33'}]},
        ]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)
        self.assertEqual(row_iterator.num_results, 0)

        rows_iter = iter(row_iterator)

        val1 = six.next(rows_iter)
        self.assertEqual(val1.name, 'Phred Phlyntstone')
        self.assertEqual(row_iterator.num_results, 1)

        val2 = six.next(rows_iter)
        self.assertEqual(val2.name, 'Bharney Rhubble')
        self.assertEqual(row_iterator.num_results, 2)

        with self.assertRaises(StopIteration):
            six.next(rows_iter)

        api_request.assert_called_once_with(
            method='GET', path=path, query_params={})

    def test_page_size(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        rows = [
            {'f': [{'v': 'Phred Phlyntstone'}, {'v': '32'}]},
            {'f': [{'v': 'Bharney Rhubble'}, {'v': '33'}]},
        ]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})

        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema, page_size=4)
        row_iterator._get_next_page_response()

        api_request.assert_called_once_with(
            method='GET', path=path, query_params={
                'maxResults': row_iterator._page_size})

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        rows = [
            {'f': [{'v': 'Phred Phlyntstone'}, {'v': '32'}]},
            {'f': [{'v': 'Bharney Rhubble'}, {'v': '33'}]},
            {'f': [{'v': 'Wylma Phlyntstone'}, {'v': '29'}]},
            {'f': [{'v': 'Bhettye Rhubble'}, {'v': '27'}]},
        ]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        self.assertEqual(list(df), ['name', 'age'])  # verify the column names
        self.assertEqual(df.name.dtype.name, 'object')
        self.assertEqual(df.age.dtype.name, 'int64')

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe_w_empty_results(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': []})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows
        self.assertEqual(list(df), ['name', 'age'])  # verify the column names

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe_w_various_types_nullable(self):
        import datetime
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('start_timestamp', 'TIMESTAMP'),
            SchemaField('seconds', 'INT64'),
            SchemaField('miles', 'FLOAT64'),
            SchemaField('payment_type', 'STRING'),
            SchemaField('complete', 'BOOL'),
            SchemaField('date', 'DATE'),
        ]
        row_data = [
            [None, None, None, None, None, None],
            ['1.4338368E9', '420', '1.1', 'Cash', 'true', '1999-12-01'],
            ['1.3878117E9', '2580', '17.7', 'Cash', 'false', '1953-06-14'],
            ['1.3855653E9', '2280', '4.4', 'Credit', 'true', '1981-11-04'],
        ]
        rows = [{'f': [{'v': field} for field in row]} for row in row_data]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        exp_columns = [field.name for field in schema]
        self.assertEqual(list(df), exp_columns)  # verify the column names

        for index, row in df.iterrows():
            if index == 0:
                self.assertTrue(row.isnull().all())
            else:
                self.assertIsInstance(row.start_timestamp, pandas.Timestamp)
                self.assertIsInstance(row.seconds, float)
                self.assertIsInstance(row.payment_type, str)
                self.assertIsInstance(row.complete, bool)
                self.assertIsInstance(row.date, datetime.date)

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe_column_dtypes(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('start_timestamp', 'TIMESTAMP'),
            SchemaField('seconds', 'INT64'),
            SchemaField('miles', 'FLOAT64'),
            SchemaField('payment_type', 'STRING'),
            SchemaField('complete', 'BOOL'),
            SchemaField('date', 'DATE'),
        ]
        row_data = [
            ['1.4338368E9', '420', '1.1', 'Cash', 'true', '1999-12-01'],
            ['1.3878117E9', '2580', '17.7', 'Cash', 'false', '1953-06-14'],
            ['1.3855653E9', '2280', '4.4', 'Credit', 'true', '1981-11-04'],
        ]
        rows = [{'f': [{'v': field} for field in row]} for row in row_data]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        exp_columns = [field.name for field in schema]
        self.assertEqual(list(df), exp_columns)  # verify the column names

        self.assertEqual(df.start_timestamp.dtype.name, 'datetime64[ns, UTC]')
        self.assertEqual(df.seconds.dtype.name, 'int64')
        self.assertEqual(df.miles.dtype.name, 'float64')
        self.assertEqual(df.payment_type.dtype.name, 'object')
        self.assertEqual(df.complete.dtype.name, 'bool')
        self.assertEqual(df.date.dtype.name, 'object')

    @mock.patch('google.cloud.bigquery.table.pandas', new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        from google.cloud.bigquery.table import RowIterator
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField('name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        rows = [
            {'f': [{'v': 'Phred Phlyntstone'}, {'v': '32'}]},
            {'f': [{'v': 'Bharney Rhubble'}, {'v': '33'}]},
        ]
        path = '/foo'
        api_request = mock.Mock(return_value={'rows': rows})
        row_iterator = RowIterator(
            mock.sentinel.client, api_request, path, schema)

        with self.assertRaises(ValueError):
            row_iterator.to_dataframe()


class TestTimePartitioning(unittest.TestCase):

    def test_constructor_defaults(self):
        from google.cloud.bigquery.table import TimePartitioning

        time_partitioning = TimePartitioning()

        self.assertEqual(time_partitioning.type_, 'DAY')
        self.assertIsNone(time_partitioning.field)
        self.assertIsNone(time_partitioning.expiration_ms)
        self.assertIsNone(time_partitioning.require_partition_filter)

        api_repr = time_partitioning.to_api_repr()

        exp_api_repr = {'type': 'DAY'}
        self.assertEqual(api_repr, exp_api_repr)

        tp_from_api_repr = TimePartitioning.from_api_repr(api_repr)

        self.assertEqual(tp_from_api_repr.type_, 'DAY')
        self.assertIsNone(tp_from_api_repr.field)
        self.assertIsNone(tp_from_api_repr.expiration_ms)
        self.assertIsNone(tp_from_api_repr.require_partition_filter)

    def test_constructor_properties(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = TimePartitioning(
            type_=TimePartitioningType.DAY,
            field='name',
            expiration_ms=10000,
            require_partition_filter=True
        )

        self.assertEqual(time_partitioning.type_, 'DAY')
        self.assertEqual(time_partitioning.field, 'name')
        self.assertEqual(time_partitioning.expiration_ms, 10000)
        self.assertTrue(time_partitioning.require_partition_filter)

        api_repr = time_partitioning.to_api_repr()

        exp_api_repr = {
            'type': 'DAY',
            'field': 'name',
            'expirationMs': '10000',
            'requirePartitionFilter': True,
        }
        self.assertEqual(api_repr, exp_api_repr)

        tp_from_api_repr = TimePartitioning.from_api_repr(api_repr)

        self.assertEqual(tp_from_api_repr.type_, 'DAY')
        self.assertEqual(tp_from_api_repr.field, 'name')
        self.assertEqual(tp_from_api_repr.expiration_ms, 10000)
        self.assertTrue(time_partitioning.require_partition_filter)
