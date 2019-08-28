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

import itertools
import logging
import time
import unittest
import warnings

import mock
import pytest
import six

import google.api_core.exceptions

try:
    from google.cloud import bigquery_storage_v1beta1
except ImportError:  # pragma: NO COVER
    bigquery_storage_v1beta1 = None

try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None

try:
    import pyarrow
    import pyarrow.types
except ImportError:  # pragma: NO COVER
    pyarrow = None

try:
    from tqdm import tqdm
except (ImportError, AttributeError):  # pragma: NO COVER
    tqdm = None

from google.cloud.bigquery.dataset import DatasetReference


def _mock_client():
    from google.cloud.bigquery import client

    mock_client = mock.create_autospec(client.Client)
    mock_client.project = "my-project"
    return mock_client


class _SchemaBase(object):
    def _verify_field(self, field, r_field):
        self.assertEqual(field.name, r_field["name"])
        self.assertEqual(field.field_type, r_field["type"])
        self.assertEqual(field.mode, r_field.get("mode", "NULLABLE"))

    def _verifySchema(self, schema, resource):
        r_fields = resource["schema"]["fields"]
        self.assertEqual(len(schema), len(r_fields))

        for field, r_field in zip(schema, r_fields):
            self._verify_field(field, r_field)


class TestEncryptionConfiguration(unittest.TestCase):
    KMS_KEY_NAME = "projects/1/locations/global/keyRings/1/cryptoKeys/1"

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
        RESOURCE = {"kmsKeyName": self.KMS_KEY_NAME}
        klass = self._get_target_class()
        encryption_config = klass.from_api_repr(RESOURCE)
        self.assertEqual(encryption_config.kms_key_name, self.KMS_KEY_NAME)

    def test_to_api_repr(self):
        encryption_config = self._make_one(kms_key_name=self.KMS_KEY_NAME)
        resource = encryption_config.to_api_repr()
        self.assertEqual(resource, {"kmsKeyName": self.KMS_KEY_NAME})

    def test___eq___wrong_type(self):
        encryption_config = self._make_one()
        other = object()
        self.assertNotEqual(encryption_config, other)
        self.assertEqual(encryption_config, mock.ANY)

    def test___eq___kms_key_name_mismatch(self):
        encryption_config = self._make_one()
        other = self._make_one(self.KMS_KEY_NAME)
        self.assertNotEqual(encryption_config, other)

    def test___eq___hit(self):
        encryption_config = self._make_one(self.KMS_KEY_NAME)
        other = self._make_one(self.KMS_KEY_NAME)
        self.assertEqual(encryption_config, other)

    def test___ne___wrong_type(self):
        encryption_config = self._make_one()
        other = object()
        self.assertNotEqual(encryption_config, other)
        self.assertEqual(encryption_config, mock.ANY)

    def test___ne___same_value(self):
        encryption_config1 = self._make_one(self.KMS_KEY_NAME)
        encryption_config2 = self._make_one(self.KMS_KEY_NAME)
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = encryption_config1 != encryption_config2
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        encryption_config1 = self._make_one()
        encryption_config2 = self._make_one(self.KMS_KEY_NAME)
        self.assertNotEqual(encryption_config1, encryption_config2)

    def test___hash__set_equality(self):
        encryption_config1 = self._make_one(self.KMS_KEY_NAME)
        encryption_config2 = self._make_one(self.KMS_KEY_NAME)
        set_one = {encryption_config1, encryption_config2}
        set_two = {encryption_config1, encryption_config2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        encryption_config1 = self._make_one()
        encryption_config2 = self._make_one(self.KMS_KEY_NAME)
        set_one = {encryption_config1}
        set_two = {encryption_config2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        encryption_config = self._make_one(self.KMS_KEY_NAME)
        expected = "EncryptionConfiguration({})".format(self.KMS_KEY_NAME)
        self.assertEqual(repr(encryption_config), expected)


class TestTableReference(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import TableReference

        return TableReference

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset_ref = DatasetReference("project_1", "dataset_1")

        table_ref = self._make_one(dataset_ref, "table_1")
        self.assertEqual(table_ref.dataset_id, dataset_ref.dataset_id)
        self.assertEqual(table_ref.table_id, "table_1")

    def test_to_api_repr(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset_ref = DatasetReference("project_1", "dataset_1")
        table_ref = self._make_one(dataset_ref, "table_1")

        resource = table_ref.to_api_repr()

        self.assertEqual(
            resource,
            {"projectId": "project_1", "datasetId": "dataset_1", "tableId": "table_1"},
        )

    def test_from_api_repr(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import TableReference

        dataset_ref = DatasetReference("project_1", "dataset_1")
        expected = self._make_one(dataset_ref, "table_1")

        got = TableReference.from_api_repr(
            {"projectId": "project_1", "datasetId": "dataset_1", "tableId": "table_1"}
        )

        self.assertEqual(expected, got)

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string("string-project.string_dataset.string_table")
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string-project:string_dataset.string_table")

    def test_from_string_not_fully_qualified(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string_table")

        with self.assertRaises(ValueError):
            cls.from_string("string_dataset.string_table")

        with self.assertRaises(ValueError):
            cls.from_string("a.b.c.d")

    def test_from_string_with_default_project(self):
        cls = self._get_target_class()
        got = cls.from_string(
            "string_dataset.string_table", default_project="default-project"
        )
        self.assertEqual(got.project, "default-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")

    def test_from_string_ignores_default_project(self):
        cls = self._get_target_class()
        got = cls.from_string(
            "string-project.string_dataset.string_table",
            default_project="default-project",
        )
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")

    def test___eq___wrong_type(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset_ref = DatasetReference("project_1", "dataset_1")
        table = self._make_one(dataset_ref, "table_1")
        other = object()
        self.assertNotEqual(table, other)
        self.assertEqual(table, mock.ANY)

    def test___eq___project_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        other_dataset = DatasetReference("project_2", "dataset_1")
        table = self._make_one(dataset, "table_1")
        other = self._make_one(other_dataset, "table_1")
        self.assertNotEqual(table, other)

    def test___eq___dataset_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        other_dataset = DatasetReference("project_1", "dataset_2")
        table = self._make_one(dataset, "table_1")
        other = self._make_one(other_dataset, "table_1")
        self.assertNotEqual(table, other)

    def test___eq___table_mismatch(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        table = self._make_one(dataset, "table_1")
        other = self._make_one(dataset, "table_2")
        self.assertNotEqual(table, other)

    def test___eq___equality(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        table = self._make_one(dataset, "table_1")
        other = self._make_one(dataset, "table_1")
        self.assertEqual(table, other)

    def test___hash__set_equality(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        table1 = self._make_one(dataset, "table1")
        table2 = self._make_one(dataset, "table2")
        set_one = {table1, table2}
        set_two = {table1, table2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = DatasetReference("project_1", "dataset_1")
        table1 = self._make_one(dataset, "table1")
        table2 = self._make_one(dataset, "table2")
        set_one = {table1}
        set_two = {table2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        dataset = DatasetReference("project1", "dataset1")
        table1 = self._make_one(dataset, "table1")
        expected = (
            "TableReference(DatasetReference('project1', 'dataset1'), " "'table1')"
        )
        self.assertEqual(repr(table1), expected)


class TestTable(unittest.TestCase, _SchemaBase):

    PROJECT = "prahj-ekt"
    DS_ID = "dataset-name"
    TABLE_NAME = "table-name"
    KMS_KEY_NAME = "projects/1/locations/global/keyRings/1/cryptoKeys/1"

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
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(tzinfo=UTC)
        self.ETAG = "ETAG"
        self.TABLE_FULL_ID = "%s:%s.%s" % (self.PROJECT, self.DS_ID, self.TABLE_NAME)
        self.RESOURCE_URL = "http://example.com/path/to/resource"
        self.NUM_BYTES = 12345
        self.NUM_ROWS = 67
        self.NUM_EST_BYTES = 1234
        self.NUM_EST_ROWS = 23

    def _make_resource(self):
        self._setUpConstants()
        return {
            "creationTime": self.WHEN_TS * 1000,
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_NAME,
            },
            "schema": {
                "fields": [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
                ]
            },
            "etag": "ETAG",
            "id": self.TABLE_FULL_ID,
            "lastModifiedTime": self.WHEN_TS * 1000,
            "location": "US",
            "selfLink": self.RESOURCE_URL,
            "numRows": self.NUM_ROWS,
            "numBytes": self.NUM_BYTES,
            "type": "TABLE",
            "streamingBuffer": {
                "estimatedRows": str(self.NUM_EST_ROWS),
                "estimatedBytes": str(self.NUM_EST_BYTES),
                "oldestEntryTime": self.WHEN_TS * 1000,
            },
            "externalDataConfiguration": {
                "sourceFormat": "CSV",
                "csvOptions": {"allowJaggedRows": True, "encoding": "encoding"},
            },
            "labels": {"x": "y"},
        }

    def _verifyReadonlyResourceProperties(self, table, resource):
        if "creationTime" in resource:
            self.assertEqual(table.created, self.WHEN)
        else:
            self.assertIsNone(table.created)

        if "etag" in resource:
            self.assertEqual(table.etag, self.ETAG)
        else:
            self.assertIsNone(table.etag)

        if "numRows" in resource:
            self.assertEqual(table.num_rows, self.NUM_ROWS)
        else:
            self.assertIsNone(table.num_rows)

        if "numBytes" in resource:
            self.assertEqual(table.num_bytes, self.NUM_BYTES)
        else:
            self.assertIsNone(table.num_bytes)

        if "selfLink" in resource:
            self.assertEqual(table.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(table.self_link)

        if "streamingBuffer" in resource:
            self.assertEqual(table.streaming_buffer.estimated_rows, self.NUM_EST_ROWS)
            self.assertEqual(table.streaming_buffer.estimated_bytes, self.NUM_EST_BYTES)
            self.assertEqual(table.streaming_buffer.oldest_entry_time, self.WHEN)
        else:
            self.assertIsNone(table.streaming_buffer)

        self.assertEqual(table.full_table_id, self.TABLE_FULL_ID)
        self.assertEqual(
            table.table_type, "TABLE" if "view" not in resource else "VIEW"
        )

    def _verifyResourceProperties(self, table, resource):

        self._verifyReadonlyResourceProperties(table, resource)

        if "expirationTime" in resource:
            self.assertEqual(table.expires, self.EXP_TIME)
        else:
            self.assertIsNone(table.expires)

        self.assertEqual(table.description, resource.get("description"))
        self.assertEqual(table.friendly_name, resource.get("friendlyName"))
        self.assertEqual(table.location, resource.get("location"))

        if "view" in resource:
            self.assertEqual(table.view_query, resource["view"]["query"])
            self.assertEqual(
                table.view_use_legacy_sql, resource["view"].get("useLegacySql", True)
            )
        else:
            self.assertIsNone(table.view_query)
            self.assertIsNone(table.view_use_legacy_sql)

        if "schema" in resource:
            self._verifySchema(table.schema, resource)
        else:
            self.assertEqual(table.schema, [])

        if "externalDataConfiguration" in resource:
            edc = table.external_data_configuration
            self.assertEqual(edc.source_format, "CSV")
            self.assertEqual(edc.options.allow_jagged_rows, True)

        if "labels" in resource:
            self.assertEqual(table.labels, {"x": "y"})
        else:
            self.assertEqual(table.labels, {})

        if "encryptionConfiguration" in resource:
            self.assertIsNotNone(table.encryption_configuration)
            self.assertEqual(
                table.encryption_configuration.kms_key_name,
                resource["encryptionConfiguration"]["kmsKeyName"],
            )
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
            "/projects/%s/datasets/%s/tables/%s"
            % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
        )
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
        self.assertEqual(table.labels, {})
        self.assertIsNone(table.encryption_configuration)
        self.assertIsNone(table.time_partitioning)
        self.assertIsNone(table.clustering_fields)

    def test_ctor_w_schema(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        table = self._make_one(table_ref, schema=[full_name, age])

        self.assertEqual(table.schema, [full_name, age])

    def test_ctor_string(self):
        table = self._make_one("some-project.some_dset.some_tbl")
        self.assertEqual(table.project, "some-project")
        self.assertEqual(table.dataset_id, "some_dset")
        self.assertEqual(table.table_id, "some_tbl")

    def test_ctor_tablelistitem(self):
        from google.cloud.bigquery.table import Table, TableListItem

        import datetime
        from google.cloud._helpers import _millis, UTC

        self.WHEN_TS = 1437767599.125
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)

        project = "test-project"
        dataset_id = "test_dataset"
        table_id = "coffee_table"
        resource = {
            "creationTime": self.WHEN_TS * 1000,
            "expirationTime": _millis(self.EXP_TIME),
            "kind": "bigquery#table",
            "id": "{}:{}.{}".format(project, dataset_id, table_id),
            "tableReference": {
                "projectId": project,
                "datasetId": dataset_id,
                "tableId": table_id,
            },
            "friendlyName": "Mahogany Coffee Table",
            "type": "TABLE",
            "timePartitioning": {
                "type": "DAY",
                "field": "mycolumn",
                "expirationMs": "10000",
            },
            "labels": {"some-stuff": "this-is-a-label"},
            "clustering": {"fields": ["string"]},
        }

        table_list_item = TableListItem(resource)
        table = Table(table_list_item)

        self.assertIsNone(table.created)
        self.assertEqual(table.reference.project, project)
        self.assertEqual(table.reference.dataset_id, dataset_id)
        self.assertEqual(table.reference.table_id, table_id)

    def test_ctor_string_wo_project_id(self):
        with pytest.raises(ValueError):
            # Project ID is missing.
            self._make_one("some_dset.some_tbl")

    def test_num_bytes_getter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        # Check with no value set.
        self.assertIsNone(table.num_bytes)

        num_bytes = 1337
        # Check with integer value set.
        table._properties = {"numBytes": num_bytes}
        self.assertEqual(table.num_bytes, num_bytes)

        # Check with a string value set.
        table._properties = {"numBytes": str(num_bytes)}
        self.assertEqual(table.num_bytes, num_bytes)

        # Check with invalid int value.
        table._properties = {"numBytes": "x"}
        with self.assertRaises(ValueError):
            getattr(table, "num_bytes")

    def test_num_rows_getter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        # Check with no value set.
        self.assertIsNone(table.num_rows)

        num_rows = 42
        # Check with integer value set.
        table._properties = {"numRows": num_rows}
        self.assertEqual(table.num_rows, num_rows)

        # Check with a string value set.
        table._properties = {"numRows": str(num_rows)}
        self.assertEqual(table.num_rows, num_rows)

        # Check with invalid int value.
        table._properties = {"numRows": "x"}
        with self.assertRaises(ValueError):
            getattr(table, "num_rows")

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
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        with self.assertRaises(ValueError):
            table.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.table import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        table.schema = [full_name, age]
        self.assertEqual(table.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        CREATED = datetime.datetime(2015, 7, 29, 12, 13, 22, tzinfo=UTC)
        MODIFIED = datetime.datetime(2015, 7, 29, 14, 47, 15, tzinfo=UTC)
        TABLE_FULL_ID = "%s:%s.%s" % (self.PROJECT, self.DS_ID, self.TABLE_NAME)
        URL = "http://example.com/projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_NAME,
        )
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties["creationTime"] = _millis(CREATED)
        table._properties["etag"] = "ETAG"
        table._properties["lastModifiedTime"] = _millis(MODIFIED)
        table._properties["numBytes"] = 12345
        table._properties["numRows"] = 66
        table._properties["selfLink"] = URL
        table._properties["id"] = TABLE_FULL_ID
        table._properties["type"] = "TABLE"

        self.assertEqual(table.created, CREATED)
        self.assertEqual(table.etag, "ETAG")
        self.assertEqual(table.modified, MODIFIED)
        self.assertEqual(table.num_bytes, 12345)
        self.assertEqual(table.num_rows, 66)
        self.assertEqual(table.self_link, URL)
        self.assertEqual(table.full_table_id, TABLE_FULL_ID)
        self.assertEqual(table.table_type, "TABLE")

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
        table.description = "DESCRIPTION"
        self.assertEqual(table.description, "DESCRIPTION")

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
        table.friendly_name = "FRIENDLY"
        self.assertEqual(table.friendly_name, "FRIENDLY")

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
        table.view_query = "select * from foo"
        self.assertEqual(table.view_query, "select * from foo")
        self.assertEqual(table.view_use_legacy_sql, False)

        table.view_use_legacy_sql = True
        self.assertEqual(table.view_use_legacy_sql, True)

    def test_view_query_deleter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.view_query = "select * from foo"
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
        table.view_query = "select * from foo"
        self.assertEqual(table.view_use_legacy_sql, True)
        self.assertEqual(table.view_query, "select * from foo")

    def test_external_data_configuration_setter(self):
        from google.cloud.bigquery.external_config import ExternalConfig

        external_config = ExternalConfig("CSV")
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.external_data_configuration = external_config

        self.assertEqual(
            table.external_data_configuration.source_format,
            external_config.source_format,
        )

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
        del table._properties["labels"]  # don't start w/ existing dict
        labels = table.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(table.labels, {"foo": "bar"})

    def test_labels_setter_bad_value(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(ValueError):
            table.labels = 12345

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string("string-project.string_dataset.string_table")
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string-project:string_dataset.string_table")

    def test_from_string_not_fully_qualified(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string_dataset.string_table")

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        RESOURCE = {
            "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_NAME,
            },
            "type": "TABLE",
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
        RESOURCE["view"] = {"query": "select fullname, age from person_ages"}
        RESOURCE["type"] = "VIEW"
        RESOURCE["location"] = "EU"
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        RESOURCE["expirationTime"] = _millis(self.EXP_TIME)
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self._verifyResourceProperties(table, RESOURCE)

    def test_from_api_with_encryption(self):
        self._setUpConstants()
        RESOURCE = {
            "id": "%s:%s.%s" % (self.PROJECT, self.DS_ID, self.TABLE_NAME),
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_NAME,
            },
            "encryptionConfiguration": {"kmsKeyName": self.KMS_KEY_NAME},
            "type": "TABLE",
        }
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self._verifyResourceProperties(table, RESOURCE)

    def test_to_api_repr_w_custom_field(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties["newAlphaProperty"] = "unreleased property"
        resource = table.to_api_repr()

        exp_resource = {
            "tableReference": table_ref.to_api_repr(),
            "labels": {},
            "newAlphaProperty": "unreleased property",
        }
        self.assertEqual(resource, exp_resource)

    def test__build_resource_w_custom_field(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table._properties["newAlphaProperty"] = "unreleased property"
        resource = table._build_resource(["newAlphaProperty"])

        exp_resource = {"newAlphaProperty": "unreleased property"}
        self.assertEqual(resource, exp_resource)

    def test__build_resource_w_custom_field_not_in__properties(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table = self._make_one(dataset.table(self.TABLE_NAME))
        table.bad = "value"
        with self.assertRaises(ValueError):
            table._build_resource(["bad"])

    def test_time_partitioning_getter(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table._properties["timePartitioning"] = {
            "type": "DAY",
            "field": "col1",
            "expirationMs": "123456",
            "requirePartitionFilter": False,
        }
        self.assertIsInstance(table.time_partitioning, TimePartitioning)
        self.assertEqual(table.time_partitioning.type_, TimePartitioningType.DAY)
        self.assertEqual(table.time_partitioning.field, "col1")
        self.assertEqual(table.time_partitioning.expiration_ms, 123456)
        self.assertFalse(table.time_partitioning.require_partition_filter)

    def test_time_partitioning_getter_w_none(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table._properties["timePartitioning"] = None
        self.assertIsNone(table.time_partitioning)

        del table._properties["timePartitioning"]
        self.assertIsNone(table.time_partitioning)

    def test_time_partitioning_getter_w_empty(self):
        from google.cloud.bigquery.table import TimePartitioning

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        # Even though there are required properties according to the API
        # specification, sometimes time partitioning is populated as an empty
        # object. See internal bug 131167013.
        table._properties["timePartitioning"] = {}
        self.assertIsInstance(table.time_partitioning, TimePartitioning)
        self.assertIsNone(table.time_partitioning.type_)
        self.assertIsNone(table.time_partitioning.field)
        self.assertIsNone(table.time_partitioning.expiration_ms)
        self.assertIsNone(table.time_partitioning.require_partition_filter)

    def test_time_partitioning_setter(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY)

        table.time_partitioning = time_partitioning

        self.assertEqual(table.time_partitioning.type_, TimePartitioningType.DAY)
        # Both objects point to the same properties dict
        self.assertIs(
            table._properties["timePartitioning"], time_partitioning._properties
        )

        time_partitioning.expiration_ms = 10000

        # Changes to TimePartitioning object are reflected in Table properties
        self.assertEqual(
            table.time_partitioning.expiration_ms, time_partitioning.expiration_ms
        )

    def test_time_partitioning_setter_bad_type(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        with self.assertRaises(ValueError):
            table.time_partitioning = {"timePartitioning": {"type": "DAY"}}

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

        with warnings.catch_warnings(record=True) as warned:
            self.assertIsNone(table.partitioning_type)

            table.partitioning_type = TimePartitioningType.DAY

            self.assertEqual(table.partitioning_type, "DAY")

        self.assertEqual(len(warned), 3)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_partitioning_type_setter_w_time_partitioning_set(self):
        from google.cloud.bigquery.table import TimePartitioning

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.time_partitioning = TimePartitioning()

        with warnings.catch_warnings(record=True) as warned:
            table.partitioning_type = "NEW_FAKE_TYPE"

            self.assertEqual(table.partitioning_type, "NEW_FAKE_TYPE")

        self.assertEqual(len(warned), 2)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_partitioning_expiration_setter_w_time_partitioning_set(self):
        from google.cloud.bigquery.table import TimePartitioning

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        table.time_partitioning = TimePartitioning()

        with warnings.catch_warnings(record=True) as warned:
            table.partition_expiration = 100000

            self.assertEqual(table.partition_expiration, 100000)

        self.assertEqual(len(warned), 2)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_partition_expiration_setter(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        with warnings.catch_warnings(record=True) as warned:
            self.assertIsNone(table.partition_expiration)

            table.partition_expiration = 100

            self.assertEqual(table.partition_expiration, 100)
            # defaults to 'DAY' when expiration is set and type is not set
            self.assertEqual(table.partitioning_type, "DAY")

        self.assertEqual(len(warned), 4)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_clustering_fields_setter_w_fields(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        fields = ["email", "phone"]

        table.clustering_fields = fields
        self.assertEqual(table.clustering_fields, fields)
        self.assertEqual(table._properties["clustering"], {"fields": fields})

    def test_clustering_fields_setter_w_none(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        fields = ["email", "phone"]

        table._properties["clustering"] = {"fields": fields}
        table.clustering_fields = None
        self.assertEqual(table.clustering_fields, None)
        self.assertFalse("clustering" in table._properties)

    def test_clustering_fields_setter_w_none_noop(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.clustering_fields = None
        self.assertEqual(table.clustering_fields, None)
        self.assertFalse("clustering" in table._properties)

    def test_encryption_configuration_setter(self):
        from google.cloud.bigquery.table import EncryptionConfiguration

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME
        )
        table.encryption_configuration = encryption_configuration
        self.assertEqual(table.encryption_configuration.kms_key_name, self.KMS_KEY_NAME)
        table.encryption_configuration = None
        self.assertIsNone(table.encryption_configuration)

    def test___repr__(self):
        from google.cloud.bigquery.table import TableReference

        dataset = DatasetReference("project1", "dataset1")
        table1 = self._make_one(TableReference(dataset, "table1"))
        expected = (
            "Table(TableReference("
            "DatasetReference('project1', 'dataset1'), "
            "'table1'))"
        )
        self.assertEqual(repr(table1), expected)


class Test_row_from_mapping(unittest.TestCase, _SchemaBase):

    PROJECT = "prahj-ekt"
    DS_ID = "dataset-name"
    TABLE_NAME = "table-name"

    def _call_fut(self, mapping, schema):
        from google.cloud.bigquery.table import _row_from_mapping

        return _row_from_mapping(mapping, schema)

    def test__row_from_mapping_wo_schema(self):
        from google.cloud.bigquery.table import Table, _TABLE_HAS_NO_SCHEMA

        MAPPING = {"full_name": "Phred Phlyntstone", "age": 32}
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = Table(table_ref)

        with self.assertRaises(ValueError) as exc:
            self._call_fut(MAPPING, table.schema)

        self.assertEqual(exc.exception.args, (_TABLE_HAS_NO_SCHEMA,))

    def test__row_from_mapping_w_invalid_schema(self):
        from google.cloud.bigquery.table import Table, SchemaField

        MAPPING = {
            "full_name": "Phred Phlyntstone",
            "age": 32,
            "colors": ["red", "green"],
            "bogus": "WHATEVER",
        }
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        colors = SchemaField("colors", "DATETIME", mode="REPEATED")
        bogus = SchemaField("joined", "STRING", mode="BOGUS")
        table = Table(table_ref, schema=[full_name, age, colors, bogus])

        with self.assertRaises(ValueError) as exc:
            self._call_fut(MAPPING, table.schema)

        self.assertIn("Unknown field mode: BOGUS", str(exc.exception))

    def test__row_from_mapping_w_schema(self):
        from google.cloud.bigquery.table import Table, SchemaField

        MAPPING = {
            "full_name": "Phred Phlyntstone",
            "age": 32,
            "colors": ["red", "green"],
            "extra": "IGNORED",
        }
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        colors = SchemaField("colors", "DATETIME", mode="REPEATED")
        joined = SchemaField("joined", "STRING", mode="NULLABLE")
        table = Table(table_ref, schema=[full_name, age, colors, joined])

        self.assertEqual(
            self._call_fut(MAPPING, table.schema),
            ("Phred Phlyntstone", 32, ["red", "green"], None),
        )


class TestTableListItem(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import TableListItem

        return TableListItem

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.125
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(tzinfo=UTC)
        self.EXP_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)

    def test_ctor(self):
        from google.cloud._helpers import _millis

        self._setUpConstants()
        project = "test-project"
        dataset_id = "test_dataset"
        table_id = "coffee_table"
        resource = {
            "creationTime": self.WHEN_TS * 1000,
            "expirationTime": _millis(self.EXP_TIME),
            "kind": "bigquery#table",
            "id": "{}:{}.{}".format(project, dataset_id, table_id),
            "tableReference": {
                "projectId": project,
                "datasetId": dataset_id,
                "tableId": table_id,
            },
            "friendlyName": "Mahogany Coffee Table",
            "type": "TABLE",
            "timePartitioning": {
                "type": "DAY",
                "field": "mycolumn",
                "expirationMs": "10000",
            },
            "labels": {"some-stuff": "this-is-a-label"},
            "clustering": {"fields": ["string"]},
        }

        table = self._make_one(resource)

        self.assertEqual(table.created, self.WHEN)
        self.assertEqual(table.expires, self.EXP_TIME)
        self.assertEqual(table.project, project)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(
            table.full_table_id, "{}:{}.{}".format(project, dataset_id, table_id)
        )
        self.assertEqual(table.reference.project, project)
        self.assertEqual(table.reference.dataset_id, dataset_id)
        self.assertEqual(table.reference.table_id, table_id)
        self.assertEqual(table.friendly_name, "Mahogany Coffee Table")
        self.assertEqual(table.table_type, "TABLE")
        self.assertEqual(table.time_partitioning.type_, "DAY")
        self.assertEqual(table.time_partitioning.expiration_ms, 10000)
        self.assertEqual(table.time_partitioning.field, "mycolumn")
        self.assertEqual(table.labels["some-stuff"], "this-is-a-label")
        self.assertIsNone(table.view_use_legacy_sql)
        self.assertEqual(table.clustering_fields, ["string"])

        with warnings.catch_warnings(record=True) as warned:
            self.assertEqual(table.partitioning_type, "DAY")
            self.assertEqual(table.partition_expiration, 10000)

        self.assertEqual(len(warned), 2)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_ctor_view(self):
        project = "test-project"
        dataset_id = "test_dataset"
        table_id = "just_looking"
        resource = {
            "kind": "bigquery#table",
            "id": "{}:{}.{}".format(project, dataset_id, table_id),
            "tableReference": {
                "projectId": project,
                "datasetId": dataset_id,
                "tableId": table_id,
            },
            "type": "VIEW",
        }

        table = self._make_one(resource)
        self.assertEqual(table.project, project)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(
            table.full_table_id, "{}:{}.{}".format(project, dataset_id, table_id)
        )
        self.assertEqual(table.reference.project, project)
        self.assertEqual(table.reference.dataset_id, dataset_id)
        self.assertEqual(table.reference.table_id, table_id)
        self.assertEqual(table.table_type, "VIEW")
        # Server default for useLegacySql is True.
        self.assertTrue(table.view_use_legacy_sql)

    def test_ctor_missing_properties(self):
        resource = {
            "tableReference": {
                "projectId": "testproject",
                "datasetId": "testdataset",
                "tableId": "testtable",
            }
        }
        table = self._make_one(resource)
        self.assertEqual(table.project, "testproject")
        self.assertEqual(table.dataset_id, "testdataset")
        self.assertEqual(table.table_id, "testtable")
        self.assertIsNone(table.created)
        self.assertIsNone(table.expires)
        self.assertIsNone(table.clustering_fields)
        self.assertIsNone(table.full_table_id)
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.table_type)
        self.assertIsNone(table.time_partitioning)
        self.assertEqual(table.labels, {})
        self.assertIsNone(table.view_use_legacy_sql)

        with warnings.catch_warnings(record=True) as warned:
            self.assertIsNone(table.partitioning_type)
            self.assertIsNone(table.partition_expiration)

        self.assertEqual(len(warned), 2)
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_ctor_wo_project(self):
        resource = {
            "tableReference": {"datasetId": "testdataset", "tableId": "testtable"}
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_dataset(self):
        resource = {
            "tableReference": {"projectId": "testproject", "tableId": "testtable"}
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_table(self):
        resource = {
            "tableReference": {"projectId": "testproject", "datasetId": "testdataset"}
        }
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_reference(self):
        with self.assertRaises(ValueError):
            self._make_one({})

    def test_labels_update_in_place(self):
        resource = {
            "tableReference": {
                "projectId": "testproject",
                "datasetId": "testdataset",
                "tableId": "testtable",
            }
        }
        table = self._make_one(resource)
        labels = table.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(table.labels, {"foo": "bar"})


class TestRow(unittest.TestCase):
    def test_row(self):
        from google.cloud.bigquery.table import Row

        VALUES = (1, 2, 3)
        row = Row(VALUES, {"a": 0, "b": 1, "c": 2})
        self.assertEqual(row.a, 1)
        self.assertEqual(row[1], 2)
        self.assertEqual(row["c"], 3)
        self.assertEqual(len(row), 3)
        self.assertEqual(row.values(), VALUES)
        self.assertEqual(set(row.keys()), set({"a": 1, "b": 2, "c": 3}.keys()))
        self.assertEqual(set(row.items()), set({"a": 1, "b": 2, "c": 3}.items()))
        self.assertEqual(row.get("a"), 1)
        self.assertEqual(row.get("d"), None)
        self.assertEqual(row.get("d", ""), "")
        self.assertEqual(row.get("d", default=""), "")
        self.assertEqual(repr(row), "Row((1, 2, 3), {'a': 0, 'b': 1, 'c': 2})")
        self.assertFalse(row != row)
        self.assertFalse(row == 3)
        with self.assertRaises(AttributeError):
            row.z
        with self.assertRaises(KeyError):
            row["z"]


class Test_EmptyRowIterator(unittest.TestCase):
    def _make_one(self):
        from google.cloud.bigquery.table import _EmptyRowIterator

        return _EmptyRowIterator()

    def test_total_rows_eq_zero(self):
        row_iterator = self._make_one()
        self.assertEqual(row_iterator.total_rows, 0)

    @mock.patch("google.cloud.bigquery.table.pyarrow", new=None)
    def test_to_arrow_error_if_pyarrow_is_none(self):
        row_iterator = self._make_one()
        with self.assertRaises(ValueError):
            row_iterator.to_arrow()

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_arrow(self):
        row_iterator = self._make_one()
        tbl = row_iterator.to_arrow()
        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 0)

    @mock.patch("google.cloud.bigquery.table.pandas", new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        row_iterator = self._make_one()
        with self.assertRaises(ValueError):
            row_iterator.to_dataframe()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe(self):
        row_iterator = self._make_one()
        df = row_iterator.to_dataframe()
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows


class TestRowIterator(unittest.TestCase):
    def _class_under_test(self):
        from google.cloud.bigquery.table import RowIterator

        return RowIterator

    def _make_one(
        self,
        client=None,
        api_request=None,
        path=None,
        schema=None,
        table=None,
        **kwargs
    ):
        from google.cloud.bigquery.table import TableReference

        if client is None:
            client = _mock_client()

        if api_request is None:
            api_request = mock.sentinel.api_request

        if path is None:
            path = "/foo"

        if schema is None:
            schema = []

        if table is None:
            table = TableReference.from_string("my-project.my_dataset.my_table")

        return self._class_under_test()(
            client, api_request, path, schema, table=table, **kwargs
        )

    def test_constructor(self):
        from google.cloud.bigquery.table import _item_to_row
        from google.cloud.bigquery.table import _rows_page_start

        client = _mock_client()
        path = "/some/path"
        iterator = self._make_one(client=client, path=path)

        # Objects are set without copying.
        self.assertIs(iterator.client, client)
        self.assertIs(iterator.item_to_value, _item_to_row)
        self.assertIs(iterator._page_start, _rows_page_start)
        # Properties have the expect value.
        self.assertEqual(iterator.extra_params, {})
        self.assertEqual(iterator._items_key, "rows")
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator.path, path)
        self.assertFalse(iterator._started)
        self.assertIsNone(iterator.total_rows)
        # Changing attributes.
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.num_results, 0)

    def test_constructor_with_table(self):
        from google.cloud.bigquery.table import Table

        table = Table("proj.dset.tbl")
        table._properties["numRows"] = 100

        iterator = self._make_one(table=table)

        self.assertIs(iterator._table, table)
        self.assertEqual(iterator.total_rows, 100)

    def test_iterate(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)
        self.assertEqual(row_iterator.num_results, 0)

        rows_iter = iter(row_iterator)

        val1 = six.next(rows_iter)
        self.assertEqual(val1.name, "Phred Phlyntstone")
        self.assertEqual(row_iterator.num_results, 1)

        val2 = six.next(rows_iter)
        self.assertEqual(val2.name, "Bharney Rhubble")
        self.assertEqual(row_iterator.num_results, 2)

        with self.assertRaises(StopIteration):
            six.next(rows_iter)

        api_request.assert_called_once_with(method="GET", path=path, query_params={})

    def test_page_size(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})

        row_iterator = self._make_one(
            _mock_client(), api_request, path, schema, page_size=4
        )
        row_iterator._get_next_page_response()

        api_request.assert_called_once_with(
            method="GET",
            path=path,
            query_params={"maxResults": row_iterator._page_size},
        )

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_arrow(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField(
                "child",
                "RECORD",
                mode="REPEATED",
                fields=[
                    SchemaField("name", "STRING", mode="REQUIRED"),
                    SchemaField("age", "INTEGER", mode="REQUIRED"),
                ],
            ),
        ]
        rows = [
            {
                "f": [
                    {"v": "Bharney Rhubble"},
                    {"v": "33"},
                    {
                        "v": [
                            {"v": {"f": [{"v": "Whamm-Whamm Rhubble"}, {"v": "3"}]}},
                            {"v": {"f": [{"v": "Hoppy"}, {"v": "1"}]}},
                        ]
                    },
                ]
            },
            {
                "f": [
                    {"v": "Wylma Phlyntstone"},
                    {"v": "29"},
                    {
                        "v": [
                            {"v": {"f": [{"v": "Bepples Phlyntstone"}, {"v": "0"}]}},
                            {"v": {"f": [{"v": "Dino"}, {"v": "4"}]}},
                        ]
                    },
                ]
            },
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        tbl = row_iterator.to_arrow()

        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 2)

        # Check the schema.
        self.assertEqual(tbl.schema[0].name, "name")
        self.assertTrue(pyarrow.types.is_string(tbl.schema[0].type))
        self.assertEqual(tbl.schema[1].name, "age")
        self.assertTrue(pyarrow.types.is_int64(tbl.schema[1].type))
        child_field = tbl.schema[2]
        self.assertEqual(child_field.name, "child")
        self.assertTrue(pyarrow.types.is_list(child_field.type))
        self.assertTrue(pyarrow.types.is_struct(child_field.type.value_type))
        self.assertEqual(child_field.type.value_type[0].name, "name")
        self.assertEqual(child_field.type.value_type[1].name, "age")

        # Check the data.
        tbl_data = tbl.to_pydict()
        names = tbl_data["name"]
        ages = tbl_data["age"]
        children = tbl_data["child"]
        self.assertEqual(names, ["Bharney Rhubble", "Wylma Phlyntstone"])
        self.assertEqual(ages, [33, 29])
        self.assertEqual(
            children,
            [
                [
                    {"name": "Whamm-Whamm Rhubble", "age": 3},
                    {"name": "Hoppy", "age": 1},
                ],
                [{"name": "Bepples Phlyntstone", "age": 0}, {"name": "Dino", "age": 4}],
            ],
        )

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_arrow_w_nulls(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [SchemaField("name", "STRING"), SchemaField("age", "INTEGER")]
        rows = [
            {"f": [{"v": "Donkey"}, {"v": 32}]},
            {"f": [{"v": "Diddy"}, {"v": 29}]},
            {"f": [{"v": "Dixie"}, {"v": None}]},
            {"f": [{"v": None}, {"v": 111}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        tbl = row_iterator.to_arrow()

        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 4)

        # Check the schema.
        self.assertEqual(tbl.schema[0].name, "name")
        self.assertTrue(pyarrow.types.is_string(tbl.schema[0].type))
        self.assertEqual(tbl.schema[1].name, "age")
        self.assertTrue(pyarrow.types.is_int64(tbl.schema[1].type))

        # Check the data.
        tbl_data = tbl.to_pydict()
        names = tbl_data["name"]
        ages = tbl_data["age"]
        self.assertEqual(names, ["Donkey", "Diddy", "Dixie", None])
        self.assertEqual(ages, [32, 29, None, 111])

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_arrow_w_unknown_type(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField("sport", "UNKNOWN_TYPE", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}, {"v": "volleyball"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}, {"v": "basketball"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        tbl = row_iterator.to_arrow()

        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 2)

        # Check the schema.
        self.assertEqual(tbl.schema[0].name, "name")
        self.assertTrue(pyarrow.types.is_string(tbl.schema[0].type))
        self.assertEqual(tbl.schema[1].name, "age")
        self.assertTrue(pyarrow.types.is_int64(tbl.schema[1].type))
        self.assertEqual(tbl.schema[2].name, "sport")

        # Check the data.
        tbl_data = tbl.to_pydict()
        names = tbl_data["name"]
        ages = tbl_data["age"]
        sports = tbl_data["sport"]
        self.assertEqual(names, ["Bharney Rhubble", "Wylma Phlyntstone"])
        self.assertEqual(ages, [33, 29])
        self.assertEqual(sports, ["volleyball", "basketball"])

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_arrow_w_empty_table(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
            SchemaField(
                "child",
                "RECORD",
                mode="REPEATED",
                fields=[
                    SchemaField("name", "STRING", mode="REQUIRED"),
                    SchemaField("age", "INTEGER", mode="REQUIRED"),
                ],
            ),
        ]
        rows = []
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        tbl = row_iterator.to_arrow()

        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 0)

        # Check the schema.
        self.assertEqual(tbl.schema[0].name, "name")
        self.assertTrue(pyarrow.types.is_string(tbl.schema[0].type))
        self.assertEqual(tbl.schema[1].name, "age")
        self.assertTrue(pyarrow.types.is_int64(tbl.schema[1].type))
        child_field = tbl.schema[2]
        self.assertEqual(child_field.name, "child")
        self.assertTrue(pyarrow.types.is_list(child_field.type))
        self.assertTrue(pyarrow.types.is_struct(child_field.type.value_type))
        self.assertEqual(child_field.type.value_type[0].name, "name")
        self.assertEqual(child_field.type.value_type[1].name, "age")

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_arrow_w_bqstorage(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage_v1beta1.types.ReadSession(streams=streams)
        arrow_schema = pyarrow.schema(
            [
                pyarrow.field("colA", pyarrow.int64()),
                # Not alphabetical to test column order.
                pyarrow.field("colC", pyarrow.float64()),
                pyarrow.field("colB", pyarrow.string()),
            ]
        )
        session.arrow_schema.serialized_schema = arrow_schema.serialize().to_pybytes()
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        expected_num_rows = 2
        expected_num_columns = 3
        page_items = [
            pyarrow.array([1, -1]),
            pyarrow.array([2.0, 4.0]),
            pyarrow.array(["abc", "def"]),
        ]

        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_arrow.return_value = pyarrow.RecordBatch.from_arrays(
            page_items, arrow_schema
        )
        mock_pages = (mock_page, mock_page, mock_page)
        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        schema = [
            schema.SchemaField("colA", "INTEGER"),
            schema.SchemaField("colC", "FLOAT"),
            schema.SchemaField("colB", "STRING"),
        ]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        actual_tbl = row_iterator.to_arrow(bqstorage_client=bqstorage_client)

        # Are the columns in the expected order?
        self.assertEqual(actual_tbl.num_columns, expected_num_columns)
        self.assertEqual(actual_tbl.schema[0].name, "colA")
        self.assertEqual(actual_tbl.schema[1].name, "colC")
        self.assertEqual(actual_tbl.schema[2].name, "colB")

        # Have expected number of rows?
        total_pages = len(streams) * len(mock_pages)
        total_rows = expected_num_rows * total_pages
        self.assertEqual(actual_tbl.num_rows, total_rows)

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_arrow_w_bqstorage_no_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        session = bigquery_storage_v1beta1.types.ReadSession()
        arrow_schema = pyarrow.schema(
            [
                pyarrow.field("colA", pyarrow.string()),
                # Not alphabetical to test column order.
                pyarrow.field("colC", pyarrow.string()),
                pyarrow.field("colB", pyarrow.string()),
            ]
        )
        session.arrow_schema.serialized_schema = arrow_schema.serialize().to_pybytes()
        bqstorage_client.create_read_session.return_value = session

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            [
                schema.SchemaField("colA", "STRING"),
                schema.SchemaField("colC", "STRING"),
                schema.SchemaField("colB", "STRING"),
            ],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )

        actual_table = row_iterator.to_arrow(bqstorage_client=bqstorage_client)
        self.assertEqual(actual_table.num_columns, 3)
        self.assertEqual(actual_table.num_rows, 0)
        self.assertEqual(actual_table.schema[0].name, "colA")
        self.assertEqual(actual_table.schema[1].name, "colC")
        self.assertEqual(actual_table.schema[2].name, "colB")

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui")
    @mock.patch("tqdm.tqdm_notebook")
    @mock.patch("tqdm.tqdm")
    def test_to_arrow_progress_bar(self, tqdm_mock, tqdm_notebook_mock, tqdm_gui_mock):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})

        progress_bars = (
            ("tqdm", tqdm_mock),
            ("tqdm_notebook", tqdm_notebook_mock),
            ("tqdm_gui", tqdm_gui_mock),
        )

        for progress_bar_type, progress_bar_mock in progress_bars:
            row_iterator = self._make_one(_mock_client(), api_request, path, schema)
            tbl = row_iterator.to_arrow(progress_bar_type=progress_bar_type)

            progress_bar_mock.assert_called()
            progress_bar_mock().update.assert_called()
            progress_bar_mock().close.assert_called_once()
            self.assertEqual(tbl.num_rows, 4)

    @mock.patch("google.cloud.bigquery.table.pyarrow", new=None)
    def test_to_arrow_w_pyarrow_none(self):
        schema = []
        rows = []
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        with self.assertRaises(ValueError):
            row_iterator.to_arrow()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        self.assertEqual(list(df), ["name", "age"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.age.dtype.name, "int64")

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui")
    @mock.patch("tqdm.tqdm_notebook")
    @mock.patch("tqdm.tqdm")
    def test_to_dataframe_progress_bar(
        self, tqdm_mock, tqdm_notebook_mock, tqdm_gui_mock
    ):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})

        progress_bars = (
            ("tqdm", tqdm_mock),
            ("tqdm_notebook", tqdm_notebook_mock),
            ("tqdm_gui", tqdm_gui_mock),
        )

        for progress_bar_type, progress_bar_mock in progress_bars:
            row_iterator = self._make_one(_mock_client(), api_request, path, schema)
            df = row_iterator.to_dataframe(progress_bar_type=progress_bar_type)

            progress_bar_mock.assert_called()
            progress_bar_mock().update.assert_called()
            progress_bar_mock().close.assert_called_once()
            self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @mock.patch("google.cloud.bigquery.table.tqdm", new=None)
    def test_to_dataframe_no_tqdm_no_progress_bar(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        with warnings.catch_warnings(record=True) as warned:
            df = row_iterator.to_dataframe()

        self.assertEqual(len(warned), 0)
        self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @mock.patch("google.cloud.bigquery.table.tqdm", new=None)
    def test_to_dataframe_no_tqdm(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        with warnings.catch_warnings(record=True) as warned:
            df = row_iterator.to_dataframe(progress_bar_type="tqdm")

        self.assertEqual(len(warned), 1)
        for warning in warned:
            self.assertIs(warning.category, UserWarning)

        # Even though the progress bar won't show, downloading the dataframe
        # should still work.
        self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui", new=None)  # will raise TypeError on call
    @mock.patch("tqdm.tqdm_notebook", new=None)  # will raise TypeError on call
    @mock.patch("tqdm.tqdm", new=None)  # will raise TypeError on call
    def test_to_dataframe_tqdm_error(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"

        for progress_bar_type in ("tqdm", "tqdm_notebook", "tqdm_gui"):
            api_request = mock.Mock(return_value={"rows": rows})
            row_iterator = self._make_one(_mock_client(), api_request, path, schema)

            with warnings.catch_warnings(record=True) as warned:
                df = row_iterator.to_dataframe(progress_bar_type=progress_bar_type)

            self.assertEqual(len(df), 4)  # all should be well

            # Warn that a progress bar was requested, but creating the tqdm
            # progress bar failed.
            for warning in warned:
                self.assertIs(warning.category, UserWarning)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_empty_results(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = self._make_one(_mock_client(), api_request, schema=schema)

        df = row_iterator.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows
        self.assertEqual(list(df), ["name", "age"])  # verify the column names

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_logs_tabledata_list(self):
        from google.cloud.bigquery.table import Table

        mock_logger = mock.create_autospec(logging.Logger)
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = self._make_one(
            _mock_client(), api_request, table=Table("debug-proj.debug_dset.debug_tbl")
        )

        with mock.patch("google.cloud.bigquery.table._LOGGER", mock_logger):
            row_iterator.to_dataframe()

        mock_logger.debug.assert_any_call(
            "Started reading table 'debug-proj.debug_dset.debug_tbl' with tabledata.list."
        )

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_various_types_nullable(self):
        import datetime
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("start_timestamp", "TIMESTAMP"),
            SchemaField("seconds", "INT64"),
            SchemaField("miles", "FLOAT64"),
            SchemaField("payment_type", "STRING"),
            SchemaField("complete", "BOOL"),
            SchemaField("date", "DATE"),
        ]
        row_data = [
            [None, None, None, None, None, None],
            ["1.4338368E9", "420", "1.1", "Cash", "true", "1999-12-01"],
            ["1.3878117E9", "2580", "17.7", "Cash", "false", "1953-06-14"],
            ["1.3855653E9", "2280", "4.4", "Credit", "true", "1981-11-04"],
        ]
        rows = [{"f": [{"v": field} for field in row]} for row in row_data]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

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

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_column_dtypes(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("start_timestamp", "TIMESTAMP"),
            SchemaField("seconds", "INT64"),
            SchemaField("miles", "FLOAT64"),
            SchemaField("km", "FLOAT64"),
            SchemaField("payment_type", "STRING"),
            SchemaField("complete", "BOOL"),
            SchemaField("date", "DATE"),
        ]
        row_data = [
            ["1.4338368E9", "420", "1.1", "1.77", "Cash", "true", "1999-12-01"],
            ["1.3878117E9", "2580", "17.7", "28.5", "Cash", "false", "1953-06-14"],
            ["1.3855653E9", "2280", "4.4", "7.1", "Credit", "true", "1981-11-04"],
        ]
        rows = [{"f": [{"v": field} for field in row]} for row in row_data]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(dtypes={"km": "float16"})

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        exp_columns = [field.name for field in schema]
        self.assertEqual(list(df), exp_columns)  # verify the column names

        self.assertEqual(df.start_timestamp.dtype.name, "datetime64[ns, UTC]")
        self.assertEqual(df.seconds.dtype.name, "int64")
        self.assertEqual(df.miles.dtype.name, "float64")
        self.assertEqual(df.km.dtype.name, "float16")
        self.assertEqual(df.payment_type.dtype.name, "object")
        self.assertEqual(df.complete.dtype.name, "bool")
        self.assertEqual(df.date.dtype.name, "object")

    @mock.patch("google.cloud.bigquery.table.pandas", new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        from google.cloud.bigquery.table import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        with self.assertRaises(ValueError):
            row_iterator.to_dataframe()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_no_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        session = bigquery_storage_v1beta1.types.ReadSession()
        bqstorage_client.create_read_session.return_value = session

        row_iterator = mut.RowIterator(
            _mock_client(),
            api_request=None,
            path=None,
            schema=[
                schema.SchemaField("colA", "IGNORED"),
                schema.SchemaField("colC", "IGNORED"),
                schema.SchemaField("colB", "IGNORED"),
            ],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )

        got = row_iterator.to_dataframe(bqstorage_client)
        column_names = ["colA", "colC", "colB"]
        self.assertEqual(list(got), column_names)
        self.assertTrue(got.empty)

    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_dataframe_w_bqstorage_logs_session(self):
        from google.cloud.bigquery.table import Table

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        session = bigquery_storage_v1beta1.types.ReadSession()
        session.name = "projects/test-proj/locations/us/sessions/SOMESESSION"
        bqstorage_client.create_read_session.return_value = session
        mock_logger = mock.create_autospec(logging.Logger)
        row_iterator = self._make_one(
            _mock_client(), table=Table("debug-proj.debug_dset.debug_tbl")
        )

        with mock.patch("google.cloud.bigquery._pandas_helpers._LOGGER", mock_logger):
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        mock_logger.debug.assert_any_call(
            "Started reading table 'debug-proj.debug_dset.debug_tbl' "
            "with BQ Storage API session 'projects/test-proj/locations/us/sessions/SOMESESSION'."
        )

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_dataframe_w_bqstorage_empty_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        session = bigquery_storage_v1beta1.types.ReadSession(
            streams=[{"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"}],
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        mock_pages = mock.PropertyMock(return_value=())
        type(mock_rows).pages = mock_pages

        schema = [
            schema.SchemaField("colA", "IGNORED"),
            schema.SchemaField("colC", "IGNORED"),
            schema.SchemaField("colB", "IGNORED"),
        ]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        got = row_iterator.to_dataframe(bqstorage_client)

        column_names = ["colA", "colC", "colB"]
        self.assertEqual(list(got), column_names)
        self.assertTrue(got.empty)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_dataframe_w_bqstorage_nonempty(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage_v1beta1.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        page_items = [
            {"colA": 1, "colB": "abc", "colC": 2.0},
            {"colA": -1, "colB": "def", "colC": 4.0},
        ]

        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_dataframe.return_value = pandas.DataFrame(
            page_items, columns=["colA", "colB", "colC"]
        )
        mock_pages = (mock_page, mock_page, mock_page)
        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        schema = [
            schema.SchemaField("colA", "IGNORED"),
            schema.SchemaField("colC", "IGNORED"),
            schema.SchemaField("colB", "IGNORED"),
        ]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        got = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        # Are the columns in the expected order?
        column_names = ["colA", "colC", "colB"]
        self.assertEqual(list(got), column_names)

        # Have expected number of rows?
        total_pages = len(streams) * len(mock_pages)
        total_rows = len(page_items) * total_pages
        self.assertEqual(len(got.index), total_rows)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_dataframe_w_bqstorage_multiple_streams_return_unique_index(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        arrow_fields = [pyarrow.field("colA", pyarrow.int64())]
        arrow_schema = pyarrow.schema(arrow_fields)

        streams = [
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage_v1beta1.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows

        page_data_frame = pandas.DataFrame(
            [{"colA": 1}, {"colA": -1}], columns=["colA"]
        )
        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_dataframe.return_value = page_data_frame
        mock_pages = (mock_page, mock_page, mock_page)
        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        row_iterator = self._make_one(
            schema=[schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )
        got = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        self.assertEqual(list(got), ["colA"])
        total_pages = len(streams) * len(mock_pages)
        total_rows = len(page_data_frame) * total_pages
        self.assertEqual(len(got.index), total_rows)
        self.assertTrue(got.index.is_unique)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    @mock.patch("tqdm.tqdm")
    def test_to_dataframe_w_bqstorage_updates_progress_bar(self, tqdm_mock):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        # Speed up testing.
        mut._PROGRESS_INTERVAL = 0.01

        arrow_fields = [pyarrow.field("testcol", pyarrow.int64())]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        streams = [
            # Use two streams we want to check that progress bar updates are
            # sent from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage_v1beta1.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        mock_page = mock.create_autospec(reader.ReadRowsPage)
        page_items = [-1, 0, 1]
        type(mock_page).num_items = mock.PropertyMock(return_value=len(page_items))

        def blocking_to_dataframe(*args, **kwargs):
            # Sleep for longer than the waiting interval. This ensures the
            # progress_queue gets written to more than once because it gives
            # the worker->progress updater time to sum intermediate updates.
            time.sleep(2 * mut._PROGRESS_INTERVAL)
            return pandas.DataFrame({"testcol": page_items})

        mock_page.to_dataframe.side_effect = blocking_to_dataframe
        mock_pages = (mock_page, mock_page, mock_page, mock_page, mock_page)
        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        schema = [schema.SchemaField("testcol", "IGNORED")]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        row_iterator.to_dataframe(
            bqstorage_client=bqstorage_client, progress_bar_type="tqdm"
        )

        # Make sure that this test updated the progress bar once per page from
        # each stream.
        total_pages = len(streams) * len(mock_pages)
        expected_total_rows = total_pages * len(page_items)
        progress_updates = [
            args[0] for args, kwargs in tqdm_mock().update.call_args_list
        ]
        # Should have sent >1 update due to delay in blocking_to_dataframe.
        self.assertGreater(len(progress_updates), 1)
        self.assertEqual(sum(progress_updates), expected_total_rows)
        tqdm_mock().close.assert_called_once()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_to_dataframe_w_bqstorage_exits_on_keyboardinterrupt(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1beta1 import reader

        # Speed up testing.
        mut._PROGRESS_INTERVAL = 0.01

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        session = bigquery_storage_v1beta1.types.ReadSession(
            streams=[
                # Use two streams because one will fail with a
                # KeyboardInterrupt, and we want to check that the other stream
                # ends early.
                {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
                {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
            ],
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        def blocking_to_dataframe(*args, **kwargs):
            # Sleep for longer than the waiting interval so that we know we're
            # only reading one page per loop at most.
            time.sleep(2 * mut._PROGRESS_INTERVAL)
            return pandas.DataFrame(
                {"colA": [1, -1], "colB": ["abc", "def"], "colC": [2.0, 4.0]},
                columns=["colA", "colB", "colC"],
            )

        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_dataframe.side_effect = blocking_to_dataframe
        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_pages = mock.PropertyMock(return_value=(mock_page, mock_page, mock_page))
        type(mock_rows).pages = mock_pages
        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        mock_rowstream.rows.return_value = mock_rows

        mock_cancelled_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_cancelled_pages = mock.PropertyMock(side_effect=KeyboardInterrupt)
        type(mock_cancelled_rows).pages = mock_cancelled_pages
        mock_cancelled_rowstream = mock.create_autospec(reader.ReadRowsStream)
        mock_cancelled_rowstream.rows.return_value = mock_cancelled_rows

        bqstorage_client.read_rows.side_effect = (
            mock_cancelled_rowstream,
            mock_rowstream,
        )

        schema = [
            schema.SchemaField("colA", "IGNORED"),
            schema.SchemaField("colB", "IGNORED"),
            schema.SchemaField("colC", "IGNORED"),
        ]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        with pytest.raises(KeyboardInterrupt):
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        # Should not have fetched the third page of results because exit_early
        # should have been set.
        self.assertLessEqual(mock_page.to_dataframe.call_count, 2)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_fallback_to_tabledata_list(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        bqstorage_client.create_read_session.side_effect = google.api_core.exceptions.InternalServerError(
            "can't read with bqstorage_client"
        )
        iterator_schema = [
            schema.SchemaField("name", "STRING", mode="REQUIRED"),
            schema.SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
            {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            {"f": [{"v": "Wylma Phlyntstone"}, {"v": "29"}]},
            {"f": [{"v": "Bhettye Rhubble"}, {"v": "27"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = mut.RowIterator(
            _mock_client(),
            api_request,
            path,
            iterator_schema,
            table=mut.Table("proj.dset.tbl"),
        )

        df = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        self.assertEqual(list(df), ["name", "age"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.age.dtype.name, "int64")

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_tabledata_list_w_multiple_pages_return_unique_index(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        iterator_schema = [schema.SchemaField("name", "STRING", mode="REQUIRED")]
        path = "/foo"
        api_request = mock.Mock(
            side_effect=[
                {"rows": [{"f": [{"v": "Bengt"}]}], "pageToken": "NEXTPAGE"},
                {"rows": [{"f": [{"v": "Sven"}]}]},
            ]
        )
        row_iterator = mut.RowIterator(
            _mock_client(),
            api_request,
            path,
            iterator_schema,
            table=mut.Table("proj.dset.tbl"),
        )

        df = row_iterator.to_dataframe(bqstorage_client=None)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df), ["name"])
        self.assertEqual(df.name.dtype.name, "object")
        self.assertTrue(df.index.is_unique)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_raises_auth_error(self):
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        bqstorage_client.create_read_session.side_effect = google.api_core.exceptions.Forbidden(
            "TEST BigQuery Storage API not enabled. TEST"
        )
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = mut.RowIterator(
            _mock_client(), api_request, path, [], table=mut.Table("proj.dset.tbl")
        )

        with pytest.raises(google.api_core.exceptions.Forbidden):
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_raises_import_error(self):
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = mut.RowIterator(
            _mock_client(), api_request, path, [], table=mut.Table("proj.dset.tbl")
        )

        with mock.patch.object(mut, "bigquery_storage_v1beta1", None), pytest.raises(
            ValueError
        ) as exc_context:
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)
        assert mut._NO_BQSTORAGE_ERROR in str(exc_context.value)

    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_partition(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            [schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl$20181225"),
        )

        with pytest.raises(ValueError):
            row_iterator.to_dataframe(bqstorage_client)

    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_to_dataframe_w_bqstorage_snapshot(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(
            bigquery_storage_v1beta1.BigQueryStorageClient
        )

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            [schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl@1234567890000"),
        )

        with pytest.raises(ValueError):
            row_iterator.to_dataframe(bqstorage_client)


class TestTimePartitioning(unittest.TestCase):
    def _get_target_class(self):
        from google.cloud.bigquery.table import TimePartitioning

        return TimePartitioning

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        time_partitioning = self._make_one()

        self.assertEqual(time_partitioning.type_, "DAY")
        self.assertIsNone(time_partitioning.field)
        self.assertIsNone(time_partitioning.expiration_ms)
        self.assertIsNone(time_partitioning.require_partition_filter)

    def test_constructor_explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY,
            field="name",
            expiration_ms=10000,
            require_partition_filter=True,
        )

        self.assertEqual(time_partitioning.type_, "DAY")
        self.assertEqual(time_partitioning.field, "name")
        self.assertEqual(time_partitioning.expiration_ms, 10000)
        self.assertTrue(time_partitioning.require_partition_filter)

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()

        # Even though there are required properties according to the API
        # specification, sometimes time partitioning is populated as an empty
        # object. See internal bug 131167013.
        api_repr = {}
        time_partitioning = klass.from_api_repr(api_repr)

        self.assertIsNone(time_partitioning.type_)
        self.assertIsNone(time_partitioning.field)
        self.assertIsNone(time_partitioning.expiration_ms)
        self.assertIsNone(time_partitioning.require_partition_filter)

    def test_from_api_repr_minimal(self):
        from google.cloud.bigquery.table import TimePartitioningType

        klass = self._get_target_class()
        api_repr = {"type": "DAY"}
        time_partitioning = klass.from_api_repr(api_repr)

        self.assertEqual(time_partitioning.type_, TimePartitioningType.DAY)
        self.assertIsNone(time_partitioning.field)
        self.assertIsNone(time_partitioning.expiration_ms)
        self.assertIsNone(time_partitioning.require_partition_filter)

    def test_from_api_repr_doesnt_override_type(self):
        klass = self._get_target_class()
        api_repr = {"type": "HOUR"}
        time_partitioning = klass.from_api_repr(api_repr)
        self.assertEqual(time_partitioning.type_, "HOUR")

    def test_from_api_repr_explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        klass = self._get_target_class()
        api_repr = {
            "type": "DAY",
            "field": "name",
            "expirationMs": "10000",
            "requirePartitionFilter": True,
        }
        time_partitioning = klass.from_api_repr(api_repr)

        self.assertEqual(time_partitioning.type_, TimePartitioningType.DAY)
        self.assertEqual(time_partitioning.field, "name")
        self.assertEqual(time_partitioning.expiration_ms, 10000)
        self.assertTrue(time_partitioning.require_partition_filter)

    def test_to_api_repr_defaults(self):
        time_partitioning = self._make_one()
        expected = {"type": "DAY"}
        self.assertEqual(time_partitioning.to_api_repr(), expected)

    def test_to_api_repr_explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY,
            field="name",
            expiration_ms=10000,
            require_partition_filter=True,
        )

        expected = {
            "type": "DAY",
            "field": "name",
            "expirationMs": "10000",
            "requirePartitionFilter": True,
        }
        self.assertEqual(time_partitioning.to_api_repr(), expected)

    def test___eq___wrong_type(self):
        time_partitioning = self._make_one()
        other = object()
        self.assertNotEqual(time_partitioning, other)
        self.assertEqual(time_partitioning, mock.ANY)

    def test___eq___type__mismatch(self):
        time_partitioning = self._make_one()
        other = self._make_one(type_="HOUR")
        self.assertNotEqual(time_partitioning, other)

    def test___eq___field_mismatch(self):
        time_partitioning = self._make_one(field="foo")
        other = self._make_one(field="bar")
        self.assertNotEqual(time_partitioning, other)

    def test___eq___expiration_ms_mismatch(self):
        time_partitioning = self._make_one(field="foo", expiration_ms=100000)
        other = self._make_one(field="foo", expiration_ms=200000)
        self.assertNotEqual(time_partitioning, other)

    def test___eq___require_partition_filter_mismatch(self):
        time_partitioning = self._make_one(
            field="foo", expiration_ms=100000, require_partition_filter=True
        )
        other = self._make_one(
            field="foo", expiration_ms=100000, require_partition_filter=False
        )
        self.assertNotEqual(time_partitioning, other)

    def test___eq___hit(self):
        time_partitioning = self._make_one(
            field="foo", expiration_ms=100000, require_partition_filter=True
        )
        other = self._make_one(
            field="foo", expiration_ms=100000, require_partition_filter=True
        )
        self.assertEqual(time_partitioning, other)

    def test___ne___wrong_type(self):
        time_partitioning = self._make_one()
        other = object()
        self.assertNotEqual(time_partitioning, other)
        self.assertEqual(time_partitioning, mock.ANY)

    def test___ne___same_value(self):
        time_partitioning1 = self._make_one()
        time_partitioning2 = self._make_one()
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = time_partitioning1 != time_partitioning2
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        time_partitioning1 = self._make_one()
        time_partitioning2 = self._make_one(type_="HOUR")
        self.assertNotEqual(time_partitioning1, time_partitioning2)

    def test___hash__set_equality(self):
        time_partitioning1 = self._make_one(field="foo")
        time_partitioning2 = self._make_one(field="foo")
        set_one = {time_partitioning1, time_partitioning2}
        set_two = {time_partitioning1, time_partitioning2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        time_partitioning1 = self._make_one(field="foo")
        time_partitioning2 = self._make_one(field="bar")
        set_one = {time_partitioning1}
        set_two = {time_partitioning2}
        self.assertNotEqual(set_one, set_two)

    def test___repr___minimal(self):
        time_partitioning = self._make_one()
        expected = "TimePartitioning(type=DAY)"
        self.assertEqual(repr(time_partitioning), expected)

    def test___repr___explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY,
            field="name",
            expiration_ms=10000,
            require_partition_filter=True,
        )
        expected = (
            "TimePartitioning("
            "expirationMs=10000,"
            "field=name,"
            "requirePartitionFilter=True,"
            "type=DAY)"
        )
        self.assertEqual(repr(time_partitioning), expected)

    def test_set_expiration_w_none(self):
        time_partitioning = self._make_one()
        time_partitioning.expiration_ms = None
        assert time_partitioning._properties["expirationMs"] is None


@pytest.mark.skipif(
    bigquery_storage_v1beta1 is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_table_reference_to_bqstorage():
    from google.cloud.bigquery import table as mut

    # Can't use parametrized pytest because bigquery_storage_v1beta1 may not be
    # available.
    expected = bigquery_storage_v1beta1.types.TableReference(
        project_id="my-project", dataset_id="my_dataset", table_id="my_table"
    )
    cases = (
        "my-project.my_dataset.my_table",
        "my-project.my_dataset.my_table$20181225",
        "my-project.my_dataset.my_table@1234567890",
        "my-project.my_dataset.my_table$20181225@1234567890",
    )

    classes = (mut.TableReference, mut.Table, mut.TableListItem)

    for case, cls in itertools.product(cases, classes):
        got = cls.from_string(case).to_bqstorage()
        assert got == expected


@unittest.skipIf(
    bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
)
def test_table_reference_to_bqstorage_raises_import_error():
    from google.cloud.bigquery import table as mut

    classes = (mut.TableReference, mut.Table, mut.TableListItem)
    for cls in classes:
        with mock.patch.object(mut, "bigquery_storage_v1beta1", None), pytest.raises(
            ValueError
        ) as exc_context:
            cls.from_string("my-project.my_dataset.my_table").to_bqstorage()
        assert mut._NO_BQSTORAGE_ERROR in str(exc_context.value)
