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

import datetime
import logging
import re
import time
import types
import unittest
import warnings

import mock
import pyarrow
import pyarrow.types
import pytest

import google.api_core.exceptions

from google.cloud.bigquery.table import TableReference

from google.cloud import bigquery_storage
from google.cloud.bigquery_storage_v1.services.big_query_read.transports import (
    grpc as big_query_read_grpc_transport,
)

try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None

try:
    import geopandas
except (ImportError, AttributeError):  # pragma: NO COVER
    geopandas = None

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
    KMS_KEY_NAME = "projects/1/locations/us/keyRings/1/cryptoKeys/1"

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


class TestTableBase:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import _TableBase

        return _TableBase

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        instance = self._make_one()
        assert instance._properties == {}

    def test_project(self):
        instance = self._make_one()
        instance._properties = {"tableReference": {"projectId": "p_1"}}
        assert instance.project == "p_1"

    def test_dataset_id(self):
        instance = self._make_one()
        instance._properties = {"tableReference": {"datasetId": "ds_1"}}
        assert instance.dataset_id == "ds_1"

    def test_table_id(self):
        instance = self._make_one()
        instance._properties = {"tableReference": {"tableId": "tbl_1"}}
        assert instance.table_id == "tbl_1"

    def test_path(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        assert instance.path == "/projects/p_1/datasets/ds_1/tables/tbl_1"

    def test___eq___wrong_type(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }

        class TableWannabe:
            pass

        wannabe_other = TableWannabe()
        wannabe_other._properties = instance._properties
        wannabe_other.project = "p_1"
        wannabe_other.dataset_id = "ds_1"
        wannabe_other.table_id = "tbl_1"

        assert instance != wannabe_other  # Can't fake it.
        assert instance == mock.ANY  # ...but delegation to other object works.

    def test___eq___project_mismatch(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        other = self._make_one()
        other._properties = {
            "projectId": "p_2",
            "datasetId": "ds_1",
            "tableId": "tbl_1",
        }
        assert instance != other

    def test___eq___dataset_mismatch(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        other = self._make_one()
        other._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_2",
                "tableId": "tbl_1",
            }
        }
        assert instance != other

    def test___eq___table_mismatch(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        other = self._make_one()
        other._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_2",
            }
        }
        assert instance != other

    def test___eq___equality(self):
        instance = self._make_one()
        instance._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        other = self._make_one()
        other._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }
        assert instance == other

    def test___hash__set_equality(self):
        instance_1 = self._make_one()
        instance_1._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }

        instance_2 = self._make_one()
        instance_2._properties = {
            "tableReference": {
                "projectId": "p_2",
                "datasetId": "ds_2",
                "tableId": "tbl_2",
            }
        }

        set_one = {instance_1, instance_2}
        set_two = {instance_1, instance_2}
        assert set_one == set_two

    def test___hash__sets_not_equal(self):
        instance_1 = self._make_one()
        instance_1._properties = {
            "tableReference": {
                "projectId": "p_1",
                "datasetId": "ds_1",
                "tableId": "tbl_1",
            }
        }

        instance_2 = self._make_one()
        instance_2._properties = {
            "tableReference": {
                "projectId": "p_2",
                "datasetId": "ds_2",
                "tableId": "tbl_2",
            }
        }

        set_one = {instance_1}
        set_two = {instance_2}
        assert set_one != set_two


class TestTableReference(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import TableReference

        return TableReference

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        dataset_ref = DatasetReference("project_1", "dataset_1")

        table_ref = self._make_one(dataset_ref, "table_1")
        self.assertEqual(table_ref.dataset_id, dataset_ref.dataset_id)
        self.assertEqual(table_ref.table_id, "table_1")

    def test_to_api_repr(self):
        dataset_ref = DatasetReference("project_1", "dataset_1")
        table_ref = self._make_one(dataset_ref, "table_1")

        resource = table_ref.to_api_repr()

        self.assertEqual(
            resource,
            {"projectId": "project_1", "datasetId": "dataset_1", "tableId": "table_1"},
        )

    def test_from_api_repr(self):
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

    def test_from_string_w_prefix(self):
        cls = self._get_target_class()
        got = cls.from_string("google.com:string-project.string_dataset.string_table")
        self.assertEqual(got.project, "google.com:string-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string-project:string_dataset.string_table")

    def test_from_string_w_incorrect_prefix(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("google.com.string-project.string_dataset.string_table")

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

    def test___repr__(self):
        dataset = DatasetReference("project1", "dataset1")
        table1 = self._make_one(dataset, "table1")
        expected = (
            "TableReference(DatasetReference('project1', 'dataset1'), " "'table1')"
        )
        self.assertEqual(repr(table1), expected)

    def test___str__(self):
        dataset = DatasetReference("project1", "dataset1")
        table1 = self._make_one(dataset, "table1")
        self.assertEqual(str(table1), "project1.dataset1.table1")


class TestTable(unittest.TestCase, _SchemaBase):

    PROJECT = "prahj-ekt"
    DS_ID = "dataset-name"
    TABLE_NAME = "table-name"
    KMS_KEY_NAME = "projects/1/locations/us/keyRings/1/cryptoKeys/1"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import Table

        return Table

    def _make_one(self, *args, **kw):
        if len(args) == 0:
            dataset = DatasetReference(self.PROJECT, self.DS_ID)
            table_ref = dataset.table(self.TABLE_NAME)
            args = (table_ref,)

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
        from google.cloud.bigquery.schema import SchemaField

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

    def test__eq__same_table_property_different(self):
        table_1 = self._make_one("project_foo.dataset_bar.table_baz")
        table_1.description = "This is table baz"

        table_2 = self._make_one("project_foo.dataset_bar.table_baz")
        table_2.description = "This is also table baz"

        assert table_1 == table_2  # Still equal, only table reference is important.

    def test_hashable(self):
        table_1 = self._make_one("project_foo.dataset_bar.table_baz")
        table_1.description = "This is a table"

        table_1b = self._make_one("project_foo.dataset_bar.table_baz")
        table_1b.description = "Metadata is irrelevant for hashes"

        assert hash(table_1) == hash(table_1b)

    def test_schema_setter_non_sequence(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        with self.assertRaises(TypeError):
            table.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.schema import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        with self.assertRaises(ValueError):
            table.schema = [full_name, object()]

    def test_schema_setter_valid_fields(self):
        from google.cloud.bigquery.schema import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        table.schema = [full_name, age]
        self.assertEqual(table.schema, [full_name, age])

    def test_schema_setter_invalid_mapping_representation(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = {"name": "full_name", "type": "STRING", "mode": "REQUIRED"}
        invalid_field = {"name": "full_name", "typeooo": "STRING", "mode": "REQUIRED"}
        with self.assertRaises(Exception):
            table.schema = [full_name, invalid_field]

    def test_schema_setter_valid_mapping_representation(self):
        from google.cloud.bigquery.schema import SchemaField

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        full_name = {"name": "full_name", "type": "STRING", "mode": "REQUIRED"}
        job_status = {
            "name": "is_employed",
            "type": "STRUCT",
            "mode": "NULLABLE",
            "fields": [
                {"name": "foo", "type": "DATE", "mode": "NULLABLE"},
                {"name": "bar", "type": "BYTES", "mode": "REQUIRED"},
            ],
        }

        table.schema = [full_name, job_status]

        expected_schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField(
                "is_employed",
                "STRUCT",
                mode="NULLABLE",
                fields=[
                    SchemaField("foo", "DATE", mode="NULLABLE"),
                    SchemaField("bar", "BYTES", mode="REQUIRED"),
                ],
            ),
        ]
        self.assertEqual(table.schema, expected_schema)

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

    def test_snapshot_definition_not_set(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        assert table.snapshot_definition is None

    def test_snapshot_definition_set(self):
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import SnapshotDefinition

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table._properties["snapshotDefinition"] = {
            "baseTableReference": {
                "projectId": "project_x",
                "datasetId": "dataset_y",
                "tableId": "table_z",
            },
            "snapshotTime": "2010-09-28T10:20:30.123Z",
        }

        snapshot = table.snapshot_definition

        assert isinstance(snapshot, SnapshotDefinition)
        assert snapshot.base_table_reference.path == (
            "/projects/project_x/datasets/dataset_y/tables/table_z"
        )
        assert snapshot.snapshot_time == datetime.datetime(
            2010, 9, 28, 10, 20, 30, 123000, tzinfo=UTC
        )

    def test_clone_definition_not_set(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        assert table.clone_definition is None

    def test_clone_definition_set(self):
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import CloneDefinition

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table._properties["cloneDefinition"] = {
            "baseTableReference": {
                "projectId": "project_x",
                "datasetId": "dataset_y",
                "tableId": "table_z",
            },
            "cloneTime": "2010-09-28T10:20:30.123Z",
        }

        clone = table.clone_definition

        assert isinstance(clone, CloneDefinition)
        assert clone.base_table_reference.path == (
            "/projects/project_x/datasets/dataset_y/tables/table_z"
        )
        assert clone.clone_time == datetime.datetime(
            2010, 9, 28, 10, 20, 30, 123000, tzinfo=UTC
        )

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

    def test_mview_query(self):
        table = self._make_one()
        self.assertIsNone(table.mview_query)
        table.mview_query = "SELECT name, SUM(number) FROM dset.tbl GROUP BY 1"
        self.assertEqual(
            table.mview_query, "SELECT name, SUM(number) FROM dset.tbl GROUP BY 1"
        )
        del table.mview_query
        self.assertIsNone(table.mview_query)

    def test_mview_last_refresh_time(self):
        table = self._make_one()
        self.assertIsNone(table.mview_last_refresh_time)
        table._properties["materializedView"] = {
            "lastRefreshTime": "1606751842496",
        }
        self.assertEqual(
            table.mview_last_refresh_time,
            datetime.datetime(
                2020, 11, 30, 15, 57, 22, 496000, tzinfo=datetime.timezone.utc
            ),
        )

    def test_mview_enable_refresh(self):
        table = self._make_one()
        self.assertIsNone(table.mview_enable_refresh)
        table.mview_enable_refresh = True
        self.assertTrue(table.mview_enable_refresh)
        table.mview_enable_refresh = False
        self.assertFalse(table.mview_enable_refresh)
        table.mview_enable_refresh = None
        self.assertIsNone(table.mview_enable_refresh)

    def test_mview_refresh_interval(self):
        table = self._make_one()
        self.assertIsNone(table.mview_refresh_interval)
        table.mview_refresh_interval = datetime.timedelta(minutes=30)
        self.assertEqual(table.mview_refresh_interval, datetime.timedelta(minutes=30))
        self.assertEqual(
            table._properties["materializedView"]["refreshIntervalMs"], "1800000"
        )
        table.mview_refresh_interval = None
        self.assertIsNone(table.mview_refresh_interval)

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string("string-project.string_dataset.string_table")
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")
        self.assertEqual(got.table_id, "string_table")
        self.assertEqual(
            str(got.reference), "string-project.string_dataset.string_table"
        )

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

    def test_from_api_repr_w_partial_streamingbuffer(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        RESOURCE = self._make_resource()
        self.OLDEST_TIME = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        RESOURCE["streamingBuffer"] = {"oldestEntryTime": _millis(self.OLDEST_TIME)}
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self.assertIsNotNone(table.streaming_buffer)
        self.assertIsNone(table.streaming_buffer.estimated_rows)
        self.assertIsNone(table.streaming_buffer.estimated_bytes)
        self.assertEqual(table.streaming_buffer.oldest_entry_time, self.OLDEST_TIME)
        # Another partial construction
        RESOURCE["streamingBuffer"] = {"estimatedRows": 1}
        klass = self._get_target_class()
        table = klass.from_api_repr(RESOURCE)
        self.assertIsNotNone(table.streaming_buffer)
        self.assertEqual(table.streaming_buffer.estimated_rows, 1)
        self.assertIsNone(table.streaming_buffer.estimated_bytes)
        self.assertIsNone(table.streaming_buffer.oldest_entry_time)

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

    def test_range_partitioning(self):
        from google.cloud.bigquery.table import RangePartitioning
        from google.cloud.bigquery.table import PartitionRange

        table = self._make_one("proj.dset.tbl")
        assert table.range_partitioning is None

        table.range_partitioning = RangePartitioning(
            field="col1", range_=PartitionRange(start=-512, end=1024, interval=128)
        )
        assert table.range_partitioning.field == "col1"
        assert table.range_partitioning.range_.start == -512
        assert table.range_partitioning.range_.end == 1024
        assert table.range_partitioning.range_.interval == 128

        table.range_partitioning = None
        assert table.range_partitioning is None

    def test_range_partitioning_w_wrong_type(self):
        object_under_test = self._make_one("proj.dset.tbl")
        with pytest.raises(ValueError, match="RangePartitioning"):
            object_under_test.range_partitioning = object()

    def test_require_partitioning_filter(self):
        table = self._make_one("proj.dset.tbl")
        assert table.require_partition_filter is None
        table.require_partition_filter = True
        assert table.require_partition_filter
        table.require_partition_filter = False
        assert table.require_partition_filter is not None
        assert not table.require_partition_filter
        table.require_partition_filter = None
        assert table.require_partition_filter is None

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

        with warnings.catch_warnings(record=True) as warned:
            self.assertFalse(table.time_partitioning.require_partition_filter)

        assert len(warned) == 1
        self.assertIs(warned[0].category, PendingDeprecationWarning)

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

        with warnings.catch_warnings(record=True) as warned:
            self.assertIsNone(table.time_partitioning.require_partition_filter)

        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

    def test_time_partitioning_setter(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)
        time_partitioning = TimePartitioning(type_=TimePartitioningType.HOUR)

        table.time_partitioning = time_partitioning

        self.assertEqual(table.time_partitioning.type_, TimePartitioningType.HOUR)
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
        self.assertIsNone(table.clustering_fields)
        self.assertTrue("clustering" in table._properties)  # None stored explicitly

    def test_clustering_fields_setter_w_none_noop(self):
        dataset = DatasetReference(self.PROJECT, self.DS_ID)
        table_ref = dataset.table(self.TABLE_NAME)
        table = self._make_one(table_ref)

        table.clustering_fields = None
        self.assertIsNone(table.clustering_fields)
        self.assertTrue("clustering" in table._properties)  # None stored explicitly

    def test_encryption_configuration_setter(self):
        # Previously, the EncryptionConfiguration class was in the table module, not the
        # encryption_configuration module. It was moved to support models encryption.
        # This test import from the table module to ensure that the previous location
        # continues to function as an alias.
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

    def test___str__(self):
        dataset = DatasetReference("project1", "dataset1")
        table1 = self._make_one(TableReference(dataset, "table1"))
        self.assertEqual(str(table1), "project1.dataset1.table1")


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
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery.table import Table

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
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery.table import Table

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

    def test_to_api_repr(self):
        resource = {
            "tableReference": {
                "projectId": "testproject",
                "datasetId": "testdataset",
                "tableId": "testtable",
            }
        }
        table = self._make_one(resource)
        self.assertEqual(table.to_api_repr(), resource)

    def test__eq__same_table_property_different(self):
        table_ref_resource = {
            "projectId": "project_foo",
            "datasetId": "dataset_bar",
            "tableId": "table_baz",
        }

        resource_1 = {"tableReference": table_ref_resource, "friendlyName": "Table One"}
        table_1 = self._make_one(resource_1)

        resource_2 = {"tableReference": table_ref_resource, "friendlyName": "Table Two"}
        table_2 = self._make_one(resource_2)

        assert table_1 == table_2  # Still equal, only table reference is important.


class TestTableClassesInterchangeability:
    @staticmethod
    def _make_table(*args, **kwargs):
        from google.cloud.bigquery.table import Table

        return Table(*args, **kwargs)

    @staticmethod
    def _make_table_ref(*args, **kwargs):
        from google.cloud.bigquery.table import TableReference

        return TableReference(*args, **kwargs)

    @staticmethod
    def _make_table_list_item(*args, **kwargs):
        from google.cloud.bigquery.table import TableListItem

        return TableListItem(*args, **kwargs)

    def test_table_eq_table_ref(self):

        table = self._make_table("project_foo.dataset_bar.table_baz")
        dataset_ref = DatasetReference("project_foo", "dataset_bar")
        table_ref = self._make_table_ref(dataset_ref, "table_baz")

        assert table == table_ref
        assert table_ref == table

    def test_table_eq_table_list_item(self):
        table = self._make_table("project_foo.dataset_bar.table_baz")
        table_list_item = self._make_table_list_item(
            {
                "tableReference": {
                    "projectId": "project_foo",
                    "datasetId": "dataset_bar",
                    "tableId": "table_baz",
                }
            }
        )

        assert table == table_list_item
        assert table_list_item == table

    def test_table_ref_eq_table_list_item(self):

        dataset_ref = DatasetReference("project_foo", "dataset_bar")
        table_ref = self._make_table_ref(dataset_ref, "table_baz")
        table_list_item = self._make_table_list_item(
            {
                "tableReference": {
                    "projectId": "project_foo",
                    "datasetId": "dataset_bar",
                    "tableId": "table_baz",
                }
            }
        )

        assert table_ref == table_list_item
        assert table_list_item == table_ref


class TestSnapshotDefinition:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import SnapshotDefinition

        return SnapshotDefinition

    @classmethod
    def _make_one(cls, *args, **kwargs):
        klass = cls._get_target_class()
        return klass(*args, **kwargs)

    def test_ctor_empty_resource(self):
        instance = self._make_one(resource={})
        assert instance.base_table_reference is None
        assert instance.snapshot_time is None

    def test_ctor_full_resource(self):
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import TableReference

        resource = {
            "baseTableReference": {
                "projectId": "my-project",
                "datasetId": "your-dataset",
                "tableId": "our-table",
            },
            "snapshotTime": "2005-06-07T19:35:02.123Z",
        }
        instance = self._make_one(resource)

        expected_table_ref = TableReference.from_string(
            "my-project.your-dataset.our-table"
        )
        assert instance.base_table_reference == expected_table_ref

        expected_time = datetime.datetime(2005, 6, 7, 19, 35, 2, 123000, tzinfo=UTC)
        assert instance.snapshot_time == expected_time


class TestCloneDefinition:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.table import CloneDefinition

        return CloneDefinition

    @classmethod
    def _make_one(cls, *args, **kwargs):
        klass = cls._get_target_class()
        return klass(*args, **kwargs)

    def test_ctor_empty_resource(self):
        instance = self._make_one(resource={})
        assert instance.base_table_reference is None
        assert instance.clone_time is None

    def test_ctor_full_resource(self):
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.table import TableReference

        resource = {
            "baseTableReference": {
                "projectId": "my-project",
                "datasetId": "your-dataset",
                "tableId": "our-table",
            },
            "cloneTime": "2005-06-07T19:35:02.123Z",
        }
        instance = self._make_one(resource)

        expected_table_ref = TableReference.from_string(
            "my-project.your-dataset.our-table"
        )
        assert instance.base_table_reference == expected_table_ref

        expected_time = datetime.datetime(2005, 6, 7, 19, 35, 2, 123000, tzinfo=UTC)
        assert instance.clone_time == expected_time


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

    def test_to_arrow(self):
        row_iterator = self._make_one()
        tbl = row_iterator.to_arrow()
        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 0)

    def test_to_arrow_iterable(self):
        row_iterator = self._make_one()
        arrow_iter = row_iterator.to_arrow_iterable()

        result = list(arrow_iter)

        self.assertEqual(len(result), 1)
        record_batch = result[0]
        self.assertIsInstance(record_batch, pyarrow.RecordBatch)
        self.assertEqual(record_batch.num_rows, 0)
        self.assertEqual(record_batch.num_columns, 0)

    @mock.patch("google.cloud.bigquery._pandas_helpers.pandas", new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        row_iterator = self._make_one()
        with self.assertRaises(ValueError):
            row_iterator.to_dataframe()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe(self):
        row_iterator = self._make_one()
        df = row_iterator.to_dataframe(create_bqstorage_client=False)
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows

    @mock.patch("google.cloud.bigquery._pandas_helpers.pandas", new=None)
    def test_to_dataframe_iterable_error_if_pandas_is_none(self):
        row_iterator = self._make_one()
        with self.assertRaises(ValueError):
            row_iterator.to_dataframe_iterable()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_iterable(self):
        row_iterator = self._make_one()
        df_iter = row_iterator.to_dataframe_iterable()

        result = list(df_iter)

        self.assertEqual(len(result), 1)
        df = result[0]
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # Verify the number of rows.
        self.assertEqual(len(df.columns), 0)

    @mock.patch("google.cloud.bigquery.table.geopandas", new=None)
    def test_to_geodataframe_if_geopandas_is_none(self):
        row_iterator = self._make_one()
        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "The geopandas library is not installed, please install "
                "geopandas to use the to_geodataframe() function."
            ),
        ):
            row_iterator.to_geodataframe(create_bqstorage_client=False)

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe(self):
        row_iterator = self._make_one()
        df = row_iterator.to_geodataframe(create_bqstorage_client=False)
        self.assertIsInstance(df, geopandas.GeoDataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows
        self.assertIsNone(df.crs)


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

    def _make_one_from_data(self, schema=(), rows=()):
        from google.cloud.bigquery.schema import SchemaField

        schema = [SchemaField(*a) for a in schema]
        rows = [{"f": [{"v": v} for v in row]} for row in rows]

        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        return self._make_one(_mock_client(), api_request, path, schema)

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
        iterator = self._make_one(table=table, total_rows=100)
        self.assertIs(iterator._table, table)
        self.assertEqual(iterator.total_rows, 100)

    def test_constructor_with_dict_schema(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "age", "type": "INT64", "mode": "NULLABLE"},
        ]

        iterator = self._make_one(schema=schema)

        expected_schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INT64", mode="NULLABLE"),
        ]
        self.assertEqual(iterator.schema, expected_schema)

    def test_iterate(self):
        from google.cloud.bigquery.schema import SchemaField

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

        val1 = next(rows_iter)
        self.assertEqual(val1.name, "Phred Phlyntstone")
        self.assertEqual(row_iterator.num_results, 1)

        val2 = next(rows_iter)
        self.assertEqual(val2.name, "Bharney Rhubble")
        self.assertEqual(row_iterator.num_results, 2)

        with self.assertRaises(StopIteration):
            next(rows_iter)

        api_request.assert_called_once_with(method="GET", path=path, query_params={})

    def test_iterate_with_cached_first_page(self):
        from google.cloud.bigquery.schema import SchemaField

        first_page = {
            "rows": [
                {"f": [{"v": "Whillma Phlyntstone"}, {"v": "27"}]},
                {"f": [{"v": "Bhetty Rhubble"}, {"v": "28"}]},
            ],
            "pageToken": "next-page",
        }
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
            _mock_client(), api_request, path, schema, first_page_response=first_page
        )
        rows = list(row_iterator)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0].age, 27)
        self.assertEqual(rows[1].age, 28)
        self.assertEqual(rows[2].age, 32)
        self.assertEqual(rows[3].age, 33)

        api_request.assert_called_once_with(
            method="GET", path=path, query_params={"pageToken": "next-page"}
        )

    def test_page_size(self):
        from google.cloud.bigquery.schema import SchemaField

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

    def test__is_completely_cached_returns_false_without_first_page(self):
        iterator = self._make_one(first_page_response=None)
        self.assertFalse(iterator._is_completely_cached())

    def test__is_completely_cached_returns_false_with_page_token(self):
        first_page = {"pageToken": "next-page"}
        iterator = self._make_one(first_page_response=first_page)
        self.assertFalse(iterator._is_completely_cached())

    def test__is_completely_cached_returns_true(self):
        first_page = {"rows": []}
        iterator = self._make_one(first_page_response=first_page)
        self.assertTrue(iterator._is_completely_cached())

    def test__validate_bqstorage_returns_false_when_completely_cached(self):
        first_page = {"rows": []}
        iterator = self._make_one(first_page_response=first_page)
        self.assertFalse(
            iterator._validate_bqstorage(
                bqstorage_client=None, create_bqstorage_client=True
            )
        )

    def test__validate_bqstorage_returns_false_if_max_results_set(self):
        iterator = self._make_one(
            max_results=10, first_page_response=None  # not cached
        )
        result = iterator._validate_bqstorage(
            bqstorage_client=None, create_bqstorage_client=True
        )
        self.assertFalse(result)

    def test_to_arrow_iterable(self):
        from google.cloud.bigquery.schema import SchemaField

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
        api_request = mock.Mock(
            side_effect=[
                {"rows": [rows[0]], "pageToken": "NEXTPAGE"},
                {"rows": [rows[1]]},
            ]
        )
        row_iterator = self._make_one(
            _mock_client(), api_request, path, schema, page_size=1, max_results=5
        )

        record_batches = row_iterator.to_arrow_iterable()
        self.assertIsInstance(record_batches, types.GeneratorType)
        record_batches = list(record_batches)
        self.assertEqual(len(record_batches), 2)

        # Check the schema.
        for record_batch in record_batches:
            self.assertIsInstance(record_batch, pyarrow.RecordBatch)
            self.assertEqual(record_batch.schema[0].name, "name")
            self.assertTrue(pyarrow.types.is_string(record_batch.schema[0].type))
            self.assertEqual(record_batch.schema[1].name, "age")
            self.assertTrue(pyarrow.types.is_int64(record_batch.schema[1].type))
            child_field = record_batch.schema[2]
            self.assertEqual(child_field.name, "child")
            self.assertTrue(pyarrow.types.is_list(child_field.type))
            self.assertTrue(pyarrow.types.is_struct(child_field.type.value_type))
            self.assertEqual(child_field.type.value_type[0].name, "name")
            self.assertEqual(child_field.type.value_type[1].name, "age")

        # Check the data.
        record_batch_1 = record_batches[0].to_pydict()
        names = record_batch_1["name"]
        ages = record_batch_1["age"]
        children = record_batch_1["child"]
        self.assertEqual(names, ["Bharney Rhubble"])
        self.assertEqual(ages, [33])
        self.assertEqual(
            children,
            [
                [
                    {"name": "Whamm-Whamm Rhubble", "age": 3},
                    {"name": "Hoppy", "age": 1},
                ],
            ],
        )

        record_batch_2 = record_batches[1].to_pydict()
        names = record_batch_2["name"]
        ages = record_batch_2["age"]
        children = record_batch_2["child"]
        self.assertEqual(names, ["Wylma Phlyntstone"])
        self.assertEqual(ages, [29])
        self.assertEqual(
            children,
            [[{"name": "Bepples Phlyntstone", "age": 0}, {"name": "Dino", "age": 4}]],
        )

    def test_to_arrow_iterable_w_bqstorage(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(streams=streams)
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
        page_items = [
            pyarrow.array([1, -1]),
            pyarrow.array([2.0, 4.0]),
            pyarrow.array(["abc", "def"]),
        ]

        expected_record_batch = pyarrow.RecordBatch.from_arrays(
            page_items, schema=arrow_schema
        )
        expected_num_record_batches = 3

        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_arrow.return_value = expected_record_batch
        mock_pages = (mock_page,) * expected_num_record_batches
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

        record_batches = list(
            row_iterator.to_arrow_iterable(bqstorage_client=bqstorage_client)
        )
        total_record_batches = len(streams) * len(mock_pages)
        self.assertEqual(len(record_batches), total_record_batches)

        for record_batch in record_batches:
            # Are the record batches return as expected?
            self.assertEqual(record_batch, expected_record_batch)

        # Don't close the client if it was passed in.
        bqstorage_client._transport.grpc_channel.close.assert_not_called()

    def test_to_arrow(self):
        from google.cloud.bigquery.schema import SchemaField

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

        tbl = row_iterator.to_arrow(create_bqstorage_client=False)

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

    def test_to_arrow_w_nulls(self):
        from google.cloud.bigquery.schema import SchemaField

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

        tbl = row_iterator.to_arrow(create_bqstorage_client=False)

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

    def test_to_arrow_w_unknown_type(self):
        from google.cloud.bigquery.schema import SchemaField

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

        with warnings.catch_warnings(record=True) as warned:
            tbl = row_iterator.to_arrow(create_bqstorage_client=False)

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

        self.assertEqual(len(warned), 1)
        warning = warned[0]
        self.assertTrue("sport" in str(warning))

    def test_to_arrow_w_empty_table(self):
        from google.cloud.bigquery.schema import SchemaField

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

        tbl = row_iterator.to_arrow(create_bqstorage_client=False)

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

    def test_to_arrow_max_results_w_explicit_bqstorage_client_warning(self):
        from google.cloud.bigquery.schema import SchemaField

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
        mock_client = _mock_client()
        mock_bqstorage_client = mock.sentinel.bq_storage_client

        row_iterator = self._make_one(
            client=mock_client,
            api_request=api_request,
            path=path,
            schema=schema,
            max_results=42,
        )

        with warnings.catch_warnings(record=True) as warned:
            row_iterator.to_arrow(bqstorage_client=mock_bqstorage_client)

        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        self.assertEqual(len(matches), 1, msg="User warning was not emitted.")
        self.assertIn(
            __file__, str(matches[0]), msg="Warning emitted with incorrect stacklevel"
        )
        mock_client._ensure_bqstorage_client.assert_not_called()

    def test_to_arrow_max_results_w_create_bqstorage_client_no_warning(self):
        from google.cloud.bigquery.schema import SchemaField

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
        mock_client = _mock_client()

        row_iterator = self._make_one(
            client=mock_client,
            api_request=api_request,
            path=path,
            schema=schema,
            max_results=42,
        )

        with warnings.catch_warnings(record=True) as warned:
            row_iterator.to_arrow(create_bqstorage_client=True)

        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        self.assertFalse(matches)
        mock_client._ensure_bqstorage_client.assert_not_called()

    def test_to_arrow_w_bqstorage(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(streams=streams)
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
            page_items, schema=arrow_schema
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

        # Don't close the client if it was passed in.
        bqstorage_client._transport.grpc_channel.close.assert_not_called()

    def test_to_arrow_w_bqstorage_creates_client(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        mock_client = _mock_client()
        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        mock_client._ensure_bqstorage_client.return_value = bqstorage_client
        session = bigquery_storage.types.ReadSession()
        bqstorage_client.create_read_session.return_value = session
        row_iterator = mut.RowIterator(
            mock_client,
            None,  # api_request: ignored
            None,  # path: ignored
            [
                schema.SchemaField("colA", "STRING"),
                schema.SchemaField("colC", "STRING"),
                schema.SchemaField("colB", "STRING"),
            ],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )
        row_iterator.to_arrow(create_bqstorage_client=True)
        mock_client._ensure_bqstorage_client.assert_called_once()
        bqstorage_client._transport.grpc_channel.close.assert_called_once()

    def test_to_arrow_ensure_bqstorage_client_wo_bqstorage(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        rows = [
            {"f": [{"v": "Alice"}, {"v": "98"}]},
            {"f": [{"v": "Bob"}, {"v": "99"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})

        mock_client = _mock_client()
        mock_client._ensure_bqstorage_client.return_value = None
        row_iterator = self._make_one(mock_client, api_request, path, schema)

        tbl = row_iterator.to_arrow(create_bqstorage_client=True)

        # The client attempted to create a BQ Storage client, and even though
        # that was not possible, results were still returned without errors.
        mock_client._ensure_bqstorage_client.assert_called_once()
        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 2)

    def test_to_arrow_w_bqstorage_no_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        session = bigquery_storage.types.ReadSession()
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

    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui")
    @mock.patch("tqdm.tqdm_notebook")
    @mock.patch("tqdm.tqdm")
    def test_to_arrow_progress_bar(self, tqdm_mock, tqdm_notebook_mock, tqdm_gui_mock):
        from google.cloud.bigquery.schema import SchemaField

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
            tbl = row_iterator.to_arrow(
                progress_bar_type=progress_bar_type,
                create_bqstorage_client=False,
            )

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
    def test_to_dataframe_iterable(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]

        path = "/foo"
        api_request = mock.Mock(
            side_effect=[
                {
                    "rows": [{"f": [{"v": "Bengt"}, {"v": "32"}]}],
                    "pageToken": "NEXTPAGE",
                },
                {"rows": [{"f": [{"v": "Sven"}, {"v": "33"}]}]},
            ]
        )

        row_iterator = self._make_one(
            _mock_client(), api_request, path, schema, page_size=1, max_results=5
        )
        dfs = row_iterator.to_dataframe_iterable()

        self.assertIsInstance(dfs, types.GeneratorType)

        df_1 = next(dfs)
        self.assertIsInstance(df_1, pandas.DataFrame)
        self.assertEqual(df_1.name.dtype.name, "object")
        self.assertEqual(df_1.age.dtype.name, "int64")
        self.assertEqual(len(df_1), 1)  # verify the number of rows
        self.assertEqual(
            df_1["name"][0], "Bengt"
        )  # verify the first value of 'name' column
        self.assertEqual(df_1["age"][0], 32)  # verify the first value of 'age' column

        df_2 = next(dfs)
        self.assertEqual(len(df_2), 1)  # verify the number of rows
        self.assertEqual(df_2["name"][0], "Sven")
        self.assertEqual(df_2["age"][0], 33)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_iterable_with_dtypes(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]

        path = "/foo"
        api_request = mock.Mock(
            side_effect=[
                {
                    "rows": [{"f": [{"v": "Bengt"}, {"v": "32"}]}],
                    "pageToken": "NEXTPAGE",
                },
                {"rows": [{"f": [{"v": "Sven"}, {"v": "33"}]}]},
            ]
        )

        row_iterator = self._make_one(
            _mock_client(), api_request, path, schema, page_size=1, max_results=5
        )
        dfs = row_iterator.to_dataframe_iterable(dtypes={"age": "int32"})

        self.assertIsInstance(dfs, types.GeneratorType)

        df_1 = next(dfs)
        self.assertIsInstance(df_1, pandas.DataFrame)
        self.assertEqual(df_1.name.dtype.name, "object")
        self.assertEqual(df_1.age.dtype.name, "int32")
        self.assertEqual(len(df_1), 1)  # verify the number of rows
        self.assertEqual(
            df_1["name"][0], "Bengt"
        )  # verify the first value of 'name' column
        self.assertEqual(df_1["age"][0], 32)  # verify the first value of 'age' column

        df_2 = next(dfs)
        self.assertEqual(len(df_2), 1)  # verify the number of rows
        self.assertEqual(df_2["name"][0], "Sven")
        self.assertEqual(df_2["age"][0], 33)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_iterable_w_bqstorage(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        page_dataframe = pandas.DataFrame(
            {"colA": [1, -1], "colC": [2.0, 4.0], "colB": ["abc", "def"]},
        )
        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_dataframe.return_value = page_dataframe
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

        got = list(
            row_iterator.to_dataframe_iterable(bqstorage_client=bqstorage_client)
        )

        # Have expected number of rows?
        total_pages = len(streams) * len(mock_pages)
        self.assertEqual(len(got), total_pages)

        # Don't close the client if it was passed in.
        bqstorage_client._transport.grpc_channel.close.assert_not_called()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_iterable_w_bqstorage_max_results_warning(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)

        iterator_schema = [
            schema.SchemaField("name", "STRING", mode="REQUIRED"),
            schema.SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        path = "/foo"
        api_request = mock.Mock(
            side_effect=[
                {
                    "rows": [{"f": [{"v": "Bengt"}, {"v": "32"}]}],
                    "pageToken": "NEXTPAGE",
                },
                {"rows": [{"f": [{"v": "Sven"}, {"v": "33"}]}]},
            ]
        )
        row_iterator = mut.RowIterator(
            _mock_client(),
            api_request,
            path,
            iterator_schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=iterator_schema,
            max_results=25,
        )

        with warnings.catch_warnings(record=True) as warned:
            dfs = row_iterator.to_dataframe_iterable(bqstorage_client=bqstorage_client)

        # Was a warning emitted?
        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        assert len(matches) == 1, "User warning was not emitted."
        assert __file__ in str(matches[0]), "Warning emitted with incorrect stacklevel"

        # Basic check of what we got as a result.
        dataframes = list(dfs)
        assert len(dataframes) == 2
        assert isinstance(dataframes[0], pandas.DataFrame)
        assert isinstance(dataframes[1], pandas.DataFrame)

    @mock.patch("google.cloud.bigquery._pandas_helpers.pandas", new=None)
    def test_to_dataframe_iterable_error_if_pandas_is_none(self):
        from google.cloud.bigquery.schema import SchemaField

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

        with pytest.raises(ValueError, match="pandas"):
            row_iterator.to_dataframe_iterable()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe(self):
        from google.cloud.bigquery.schema import SchemaField

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

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        self.assertEqual(list(df), ["name", "age"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.age.dtype.name, "Int64")

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_timestamp_out_of_pyarrow_bounds(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [SchemaField("some_timestamp", "TIMESTAMP")]
        rows = [
            {"f": [{"v": "81953424000000000"}]},  # 4567-01-01 00:00:00  UTC
            {"f": [{"v": "253402214400000000"}]},  # 9999-12-31 00:00:00  UTC
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        tzinfo = datetime.timezone.utc
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 2)  # verify the number of rows
        self.assertEqual(list(df.columns), ["some_timestamp"])
        self.assertEqual(
            list(df["some_timestamp"]),
            [
                datetime.datetime(4567, 1, 1, tzinfo=tzinfo),
                datetime.datetime(9999, 12, 31, tzinfo=tzinfo),
            ],
        )

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_datetime_out_of_pyarrow_bounds(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [SchemaField("some_datetime", "DATETIME")]
        rows = [
            {"f": [{"v": "4567-01-01T00:00:00"}]},
            {"f": [{"v": "9999-12-31T00:00:00"}]},
        ]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 2)  # verify the number of rows
        self.assertEqual(list(df.columns), ["some_datetime"])
        self.assertEqual(
            list(df["some_datetime"]),
            [datetime.datetime(4567, 1, 1), datetime.datetime(9999, 12, 31)],
        )

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui")
    @mock.patch("tqdm.tqdm_notebook")
    @mock.patch("tqdm.tqdm")
    def test_to_dataframe_progress_bar(
        self, tqdm_mock, tqdm_notebook_mock, tqdm_gui_mock
    ):
        from google.cloud.bigquery.schema import SchemaField

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
            df = row_iterator.to_dataframe(
                progress_bar_type=progress_bar_type,
                create_bqstorage_client=False,
            )

            progress_bar_mock.assert_called()
            progress_bar_mock().update.assert_called()
            progress_bar_mock().close.assert_called_once()
            self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @mock.patch("google.cloud.bigquery._tqdm_helpers.tqdm", new=None)
    def test_to_dataframe_no_tqdm_no_progress_bar(self):
        from google.cloud.bigquery.schema import SchemaField

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
            df = row_iterator.to_dataframe(create_bqstorage_client=False)

        user_warnings = [
            warning for warning in warned if warning.category is UserWarning
        ]
        self.assertEqual(len(user_warnings), 0)
        self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @mock.patch("google.cloud.bigquery._tqdm_helpers.tqdm", new=None)
    def test_to_dataframe_no_tqdm(self):
        from google.cloud.bigquery.schema import SchemaField

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
            df = row_iterator.to_dataframe(
                progress_bar_type="tqdm",
                create_bqstorage_client=False,
            )

        user_warnings = [
            warning for warning in warned if warning.category is UserWarning
        ]
        self.assertEqual(len(user_warnings), 1)

        # Even though the progress bar won't show, downloading the dataframe
        # should still work.
        self.assertEqual(len(df), 4)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm_gui", new=None)  # will raise TypeError on call
    @mock.patch("tqdm.tqdm_notebook", new=None)  # will raise TypeError on call
    @mock.patch("tqdm.tqdm", new=None)  # will raise TypeError on call
    def test_to_dataframe_tqdm_error(self):
        from google.cloud.bigquery.schema import SchemaField

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
                df = row_iterator.to_dataframe(
                    progress_bar_type=progress_bar_type,
                    create_bqstorage_client=False,
                )

            self.assertEqual(len(df), 4)  # all should be well

            # Warn that a progress bar was requested, but creating the tqdm
            # progress bar failed.
            for warning in warned:
                self.assertIs(warning.category, UserWarning)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_empty_results(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = self._make_one(_mock_client(), api_request, schema=schema)

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 0)  # verify the number of rows
        self.assertEqual(list(df), ["name", "age"])  # verify the column names

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_various_types_nullable(self):
        import datetime
        from google.cloud.bigquery.schema import SchemaField

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
            ["1433836800000000", "420", "1.1", "Cash", "true", "1999-12-01"],
            ["1387811700000000", "2580", "17.7", "Cash", "false", "1953-06-14"],
            ["1385565300000000", "2280", "4.4", "Credit", "true", "1981-11-04"],
        ]
        rows = [{"f": [{"v": field} for field in row]} for row in row_data]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        exp_columns = [field.name for field in schema]
        self.assertEqual(list(df), exp_columns)  # verify the column names

        for index, row in df.iterrows():
            if index == 0:
                self.assertTrue(row.isnull().all())
            else:
                self.assertIsInstance(row.start_timestamp, pandas.Timestamp)
                self.assertIsInstance(row.seconds, int)
                self.assertIsInstance(row.payment_type, str)
                self.assertIsInstance(row.complete, bool)
                self.assertIsInstance(row.date, datetime.date)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_column_dtypes(self):
        from google.cloud.bigquery.schema import SchemaField

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
            ["1433836800000000", "420", "1.1", "1.77", "Cash", "true", "1999-12-01"],
            [
                "1387811700000000",
                "2580",
                "17.7",
                "28.5",
                "Cash",
                "false",
                "1953-06-14",
            ],
            ["1385565300000000", "2280", "4.4", "7.1", "Credit", "true", "1981-11-04"],
        ]
        rows = [{"f": [{"v": field} for field in row]} for row in row_data]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(
            dtypes={"km": "float16"},
            create_bqstorage_client=False,
        )

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        exp_columns = [field.name for field in schema]
        self.assertEqual(list(df), exp_columns)  # verify the column names

        self.assertEqual(df.start_timestamp.dtype.name, "datetime64[ns, UTC]")
        self.assertEqual(df.seconds.dtype.name, "Int64")
        self.assertEqual(df.miles.dtype.name, "float64")
        self.assertEqual(df.km.dtype.name, "float16")
        self.assertEqual(df.payment_type.dtype.name, "object")
        self.assertEqual(df.complete.dtype.name, "boolean")
        self.assertEqual(df.date.dtype.name, "dbdate")

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_datetime_objects(self):
        # When converting date or timestamp values to nanosecond
        # precision, the result can be out of pyarrow bounds. To avoid
        # the error when converting to Pandas, we use object type if
        # necessary.

        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("ts", "TIMESTAMP"),
            SchemaField("date", "DATE"),
        ]
        row_data = [
            ["-20000000000000000", "1111-01-01"],
        ]
        rows = [{"f": [{"v": field} for field in row]} for row in row_data]
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": rows})
        row_iterator = self._make_one(_mock_client(), api_request, path, schema)

        df = row_iterator.to_dataframe(create_bqstorage_client=False)

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 1)  # verify the number of rows
        self.assertEqual(df["ts"].dtype.name, "object")
        self.assertEqual(df["date"].dtype.name, "object")
        self.assertEqual(df["ts"][0].date(), datetime.date(1336, 3, 23))
        self.assertEqual(df["date"][0], datetime.date(1111, 1, 1))

    @mock.patch("google.cloud.bigquery._pandas_helpers.pandas", new=None)
    def test_to_dataframe_error_if_pandas_is_none(self):
        from google.cloud.bigquery.schema import SchemaField

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
    @mock.patch("google.cloud.bigquery.table.shapely", new=None)
    def test_to_dataframe_error_if_shapely_is_none(self):
        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "The shapely library is not installed, please install "
                "shapely to use the geography_as_object option."
            ),
        ):
            self._make_one_from_data().to_dataframe(geography_as_object=True)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_max_results_w_bqstorage_warning(self):
        from google.cloud.bigquery.schema import SchemaField

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
        bqstorage_client = mock.Mock()

        row_iterator = self._make_one(
            client=_mock_client(),
            api_request=api_request,
            path=path,
            schema=schema,
            max_results=42,
        )

        with warnings.catch_warnings(record=True) as warned:
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        self.assertEqual(len(matches), 1, msg="User warning was not emitted.")

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_max_results_w_explicit_bqstorage_client_warning(self):
        from google.cloud.bigquery.schema import SchemaField

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
        mock_client = _mock_client()
        mock_bqstorage_client = mock.sentinel.bq_storage_client

        row_iterator = self._make_one(
            client=mock_client,
            api_request=api_request,
            path=path,
            schema=schema,
            max_results=42,
        )

        with warnings.catch_warnings(record=True) as warned:
            row_iterator.to_dataframe(bqstorage_client=mock_bqstorage_client)

        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        self.assertEqual(len(matches), 1, msg="User warning was not emitted.")
        self.assertIn(
            __file__, str(matches[0]), msg="Warning emitted with incorrect stacklevel"
        )
        mock_client._ensure_bqstorage_client.assert_not_called()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_max_results_w_create_bqstorage_client_no_warning(self):
        from google.cloud.bigquery.schema import SchemaField

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
        mock_client = _mock_client()

        row_iterator = self._make_one(
            client=mock_client,
            api_request=api_request,
            path=path,
            schema=schema,
            max_results=42,
        )

        with warnings.catch_warnings(record=True) as warned:
            row_iterator.to_dataframe(create_bqstorage_client=True)

        matches = [
            warning
            for warning in warned
            if warning.category is UserWarning
            and "cannot use bqstorage_client" in str(warning).lower()
            and "REST" in str(warning)
        ]
        self.assertFalse(matches)
        mock_client._ensure_bqstorage_client.assert_not_called()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_creates_client(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        mock_client = _mock_client()
        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        mock_client._ensure_bqstorage_client.return_value = bqstorage_client
        session = bigquery_storage.types.ReadSession()
        bqstorage_client.create_read_session.return_value = session
        row_iterator = mut.RowIterator(
            mock_client,
            None,  # api_request: ignored
            None,  # path: ignored
            [
                schema.SchemaField("colA", "STRING"),
                schema.SchemaField("colC", "STRING"),
                schema.SchemaField("colB", "STRING"),
            ],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )
        row_iterator.to_dataframe(create_bqstorage_client=True)
        mock_client._ensure_bqstorage_client.assert_called_once()
        bqstorage_client._transport.grpc_channel.close.assert_called_once()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_no_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        session = bigquery_storage.types.ReadSession()
        bqstorage_client.create_read_session.return_value = session

        row_iterator = mut.RowIterator(
            _mock_client(),
            api_request=None,
            path=None,
            schema=[
                schema.SchemaField("colA", "INTEGER"),
                schema.SchemaField("colC", "FLOAT"),
                schema.SchemaField("colB", "STRING"),
            ],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )

        got = row_iterator.to_dataframe(bqstorage_client)
        column_names = ["colA", "colC", "colB"]
        self.assertEqual(list(got), column_names)
        self.assertTrue(got.empty)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_logs_session(self):
        from google.cloud.bigquery.table import Table

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        session = bigquery_storage.types.ReadSession()
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
    def test_to_dataframe_w_bqstorage_empty_streams(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        session = bigquery_storage.types.ReadSession(
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

        # Schema is required when there are no record batches in the stream.
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

        got = row_iterator.to_dataframe(bqstorage_client)

        column_names = ["colA", "colC", "colB"]
        self.assertEqual(list(got), column_names)
        self.assertTrue(got.empty)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_nonempty(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        streams = [
            # Use two streams we want to check frames are read from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        page_items = [
            pyarrow.array([1, -1]),
            pyarrow.array([2.0, 4.0]),
            pyarrow.array(["abc", "def"]),
        ]
        page_record_batch = pyarrow.RecordBatch.from_arrays(
            page_items, schema=arrow_schema
        )
        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_arrow.return_value = page_record_batch
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
        total_rows = len(page_items[0]) * total_pages
        self.assertEqual(len(got.index), total_rows)

        # Don't close the client if it was passed in.
        bqstorage_client._transport.grpc_channel.close.assert_not_called()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_multiple_streams_return_unique_index(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        arrow_fields = [pyarrow.field("colA", pyarrow.int64())]
        arrow_schema = pyarrow.schema(arrow_fields)

        streams = [
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(
            streams=streams,
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows

        page_items = [
            pyarrow.array([1, -1]),
        ]
        page_record_batch = pyarrow.RecordBatch.from_arrays(
            page_items, schema=arrow_schema
        )
        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_arrow.return_value = page_record_batch
        mock_pages = (mock_page, mock_page, mock_page)
        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        row_iterator = self._make_one(
            schema=[schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl"),
        )
        got = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

        self.assertEqual(list(got), ["colA"])
        total_pages = len(streams) * len(mock_pages)
        total_rows = len(page_items[0]) * total_pages
        self.assertEqual(len(got.index), total_rows)
        self.assertTrue(got.index.is_unique)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    @unittest.skipIf(tqdm is None, "Requires `tqdm`")
    @mock.patch("tqdm.tqdm")
    def test_to_dataframe_w_bqstorage_updates_progress_bar(self, tqdm_mock):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        # Speed up testing.
        mut._PROGRESS_INTERVAL = 0.01

        arrow_fields = [pyarrow.field("testcol", pyarrow.int64())]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        streams = [
            # Use two streams we want to check that progress bar updates are
            # sent from each stream.
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
            {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
        ]
        session = bigquery_storage.types.ReadSession(
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

        def blocking_to_arrow(*args, **kwargs):
            # Sleep for longer than the waiting interval so that we know we're
            # only reading one page per loop at most.
            time.sleep(2 * mut._PROGRESS_INTERVAL)
            return pyarrow.RecordBatch.from_arrays(
                [pyarrow.array(page_items)], schema=arrow_schema
            )

        mock_page.to_arrow.side_effect = blocking_to_arrow
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
        # Should have sent >1 update due to delay in blocking_to_arrow.
        self.assertGreater(len(progress_updates), 1)
        self.assertEqual(sum(progress_updates), expected_total_rows)
        tqdm_mock().close.assert_called_once()

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_exits_on_keyboardinterrupt(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        # Speed up testing.
        mut._PROGRESS_INTERVAL = 0.01

        arrow_fields = [
            pyarrow.field("colA", pyarrow.int64()),
            # Not alphabetical to test column order.
            pyarrow.field("colC", pyarrow.float64()),
            pyarrow.field("colB", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        session = bigquery_storage.types.ReadSession(
            streams=[
                # Use multiple streams because one will fail with a
                # KeyboardInterrupt, and we want to check that the other streams
                # ends early.
                {"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"},
                {"name": "/projects/proj/dataset/dset/tables/tbl/streams/5678"},
                {"name": "/projects/proj/dataset/dset/tables/tbl/streams/9999"},
            ],
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session
        page_items = [
            pyarrow.array([1, -1]),
            pyarrow.array([2.0, 4.0]),
            pyarrow.array(["abc", "def"]),
        ]

        def blocking_to_arrow(*args, **kwargs):
            # Sleep for longer than the waiting interval so that we know we're
            # only reading one page per loop at most.
            time.sleep(2 * mut._PROGRESS_INTERVAL)
            return pyarrow.RecordBatch.from_arrays(page_items, schema=arrow_schema)

        mock_page = mock.create_autospec(reader.ReadRowsPage)
        mock_page.to_arrow.side_effect = blocking_to_arrow
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
            mock_rowstream,
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

        df = row_iterator.to_dataframe(
            bqstorage_client=None,
            create_bqstorage_client=False,
        )

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df), ["name"])
        self.assertEqual(df.name.dtype.name, "object")
        self.assertTrue(df.index.is_unique)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_w_bqstorage_raises_auth_error(self):
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client.create_read_session.side_effect = (
            google.api_core.exceptions.Forbidden(
                "TEST BigQuery Storage API not enabled. TEST"
            )
        )
        path = "/foo"
        api_request = mock.Mock(return_value={"rows": []})
        row_iterator = mut.RowIterator(
            _mock_client(), api_request, path, [], table=mut.Table("proj.dset.tbl")
        )

        with pytest.raises(google.api_core.exceptions.Forbidden):
            row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

    def test_to_dataframe_w_bqstorage_partition(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            [schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl$20181225"),
        )

        with pytest.raises(ValueError):
            row_iterator.to_dataframe(bqstorage_client)

    def test_to_dataframe_w_bqstorage_snapshot(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut

        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            [schema.SchemaField("colA", "IGNORED")],
            table=mut.TableReference.from_string("proj.dset.tbl@1234567890000"),
        )

        with pytest.raises(ValueError):
            row_iterator.to_dataframe(bqstorage_client)

    @unittest.skipIf(pandas is None, "Requires `pandas`")
    def test_to_dataframe_concat_categorical_dtype_w_pyarrow(self):
        from google.cloud.bigquery import schema
        from google.cloud.bigquery import table as mut
        from google.cloud.bigquery_storage_v1 import reader

        arrow_fields = [
            # Not alphabetical to test column order.
            pyarrow.field("col_str", pyarrow.utf8()),
            # The backend returns strings, and without other info, pyarrow contains
            # string data in categorical columns, too (and not maybe the Dictionary
            # type that corresponds to pandas.Categorical).
            pyarrow.field("col_category", pyarrow.utf8()),
        ]
        arrow_schema = pyarrow.schema(arrow_fields)

        # create a mock BQ storage client
        bqstorage_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        bqstorage_client._transport = mock.create_autospec(
            big_query_read_grpc_transport.BigQueryReadGrpcTransport
        )
        session = bigquery_storage.types.ReadSession(
            streams=[{"name": "/projects/proj/dataset/dset/tables/tbl/streams/1234"}],
            arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()},
        )
        bqstorage_client.create_read_session.return_value = session

        mock_rowstream = mock.create_autospec(reader.ReadRowsStream)
        bqstorage_client.read_rows.return_value = mock_rowstream

        # prepare the iterator over mocked rows
        mock_rows = mock.create_autospec(reader.ReadRowsIterable)
        mock_rowstream.rows.return_value = mock_rows
        page_items = [
            [
                pyarrow.array(["foo", "bar", "baz"]),  # col_str
                pyarrow.array(["low", "medium", "low"]),  # col_category
            ],
            [
                pyarrow.array(["foo_page2", "bar_page2", "baz_page2"]),  # col_str
                pyarrow.array(["medium", "high", "low"]),  # col_category
            ],
        ]

        mock_pages = []

        for record_list in page_items:
            page_record_batch = pyarrow.RecordBatch.from_arrays(
                record_list, schema=arrow_schema
            )
            mock_page = mock.create_autospec(reader.ReadRowsPage)
            mock_page.to_arrow.return_value = page_record_batch
            mock_pages.append(mock_page)

        type(mock_rows).pages = mock.PropertyMock(return_value=mock_pages)

        schema = [
            schema.SchemaField("col_str", "IGNORED"),
            schema.SchemaField("col_category", "IGNORED"),
        ]

        row_iterator = mut.RowIterator(
            _mock_client(),
            None,  # api_request: ignored
            None,  # path: ignored
            schema,
            table=mut.TableReference.from_string("proj.dset.tbl"),
            selected_fields=schema,
        )

        # run the method under test
        got = row_iterator.to_dataframe(
            bqstorage_client=bqstorage_client,
            dtypes={
                "col_category": pandas.core.dtypes.dtypes.CategoricalDtype(
                    categories=["low", "medium", "high"],
                    ordered=False,
                ),
            },
        )

        # Are the columns in the expected order?
        column_names = ["col_str", "col_category"]
        self.assertEqual(list(got), column_names)

        # Have expected number of rows?
        total_pages = len(mock_pages)  # we have a single stream, thus these two equal
        total_rows = len(page_items[0][0]) * total_pages
        self.assertEqual(len(got.index), total_rows)

        # Are column types correct?
        expected_dtypes = [
            pandas.core.dtypes.dtypes.np.dtype("O"),  # the default for string data
            pandas.core.dtypes.dtypes.CategoricalDtype(
                categories=["low", "medium", "high"],
                ordered=False,
            ),
        ]
        self.assertEqual(list(got.dtypes), expected_dtypes)

        # And the data in the categorical column?
        self.assertEqual(
            list(got["col_category"]),
            ["low", "medium", "low", "medium", "high", "low"],
        )

        # Don't close the client if it was passed in.
        bqstorage_client._transport.grpc_channel.close.assert_not_called()

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_dataframe_geography_as_object(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "GEOGRAPHY")),
            (
                ("foo", "Point(0 0)"),
                ("bar", None),
                ("baz", "Polygon((0 0, 0 1, 1 0, 0 0))"),
            ),
        )
        df = row_iterator.to_dataframe(
            create_bqstorage_client=False,
            geography_as_object=True,
        )
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        self.assertEqual(list(df), ["name", "geog"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.geog.dtype.name, "object")
        self.assertIsInstance(df.geog, pandas.Series)
        self.assertEqual(
            [v.__class__.__name__ for v in df.geog], ["Point", "float", "Polygon"]
        )

    @mock.patch("google.cloud.bigquery.table.geopandas", new=None)
    def test_to_geodataframe_error_if_geopandas_is_none(self):
        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "The geopandas library is not installed, please install "
                "geopandas to use the to_geodataframe() function."
            ),
        ):
            self._make_one_from_data().to_geodataframe()

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "GEOGRAPHY")),
            (
                ("foo", "Point(0 0)"),
                ("bar", None),
                ("baz", "Polygon((0 0, 0 1, 1 0, 0 0))"),
            ),
        )
        df = row_iterator.to_geodataframe(create_bqstorage_client=False)
        self.assertIsInstance(df, geopandas.GeoDataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        self.assertEqual(list(df), ["name", "geog"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.geog.dtype.name, "geometry")
        self.assertIsInstance(df.geog, geopandas.GeoSeries)

        with warnings.catch_warnings():
            # Computing the area on a GeoDataFrame that uses a geographic Coordinate
            # Reference System (CRS) produces a warning that we are not interested in.
            warnings.filterwarnings("ignore", category=UserWarning)
            self.assertEqual(list(map(str, df.area)), ["0.0", "nan", "0.5"])
            self.assertEqual(list(map(str, df.geog.area)), ["0.0", "nan", "0.5"])

        self.assertEqual(df.crs.srs, "EPSG:4326")
        self.assertEqual(df.crs.name, "WGS 84")
        self.assertEqual(df.geog.crs.srs, "EPSG:4326")
        self.assertEqual(df.geog.crs.name, "WGS 84")

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe_ambiguous_geog(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "GEOGRAPHY"), ("geog2", "GEOGRAPHY")), ()
        )
        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "There is more than one GEOGRAPHY column in the result. "
                "The geography_column argument must be used to specify which "
                "one to use to create a GeoDataFrame"
            ),
        ):
            row_iterator.to_geodataframe(create_bqstorage_client=False)

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe_bad_geography_column(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "GEOGRAPHY"), ("geog2", "GEOGRAPHY")), ()
        )
        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "The given geography column, xxx, doesn't name"
                " a GEOGRAPHY column in the result."
            ),
        ):
            row_iterator.to_geodataframe(
                create_bqstorage_client=False, geography_column="xxx"
            )

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe_no_geog(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "STRING")), ()
        )
        with self.assertRaisesRegex(
            TypeError,
            re.escape(
                "There must be at least one GEOGRAPHY column"
                " to create a GeoDataFrame"
            ),
        ):
            row_iterator.to_geodataframe(create_bqstorage_client=False)

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    def test_to_geodataframe_w_geography_column(self):
        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("geog", "GEOGRAPHY"), ("geog2", "GEOGRAPHY")),
            (
                ("foo", "Point(0 0)", "Point(1 1)"),
                ("bar", None, "Point(2 2)"),
                ("baz", "Polygon((0 0, 0 1, 1 0, 0 0))", "Point(3 3)"),
            ),
        )
        df = row_iterator.to_geodataframe(
            create_bqstorage_client=False, geography_column="geog"
        )
        self.assertIsInstance(df, geopandas.GeoDataFrame)
        self.assertEqual(len(df), 3)  # verify the number of rows
        self.assertEqual(list(df), ["name", "geog", "geog2"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.geog.dtype.name, "geometry")
        self.assertEqual(df.geog2.dtype.name, "object")
        self.assertIsInstance(df.geog, geopandas.GeoSeries)

        with warnings.catch_warnings():
            # Computing the area on a GeoDataFrame that uses a geographic Coordinate
            # Reference System (CRS) produces a warning that we are not interested in.
            warnings.filterwarnings("ignore", category=UserWarning)
            self.assertEqual(list(map(str, df.area)), ["0.0", "nan", "0.5"])
            self.assertEqual(list(map(str, df.geog.area)), ["0.0", "nan", "0.5"])

        self.assertEqual(
            [v.__class__.__name__ for v in df.geog], ["Point", "NoneType", "Polygon"]
        )

        # Geog2 isn't a GeoSeries, but it contains geomentries:
        self.assertIsInstance(df.geog2, pandas.Series)
        self.assertEqual(
            [v.__class__.__name__ for v in df.geog2], ["Point", "Point", "Point"]
        )

        # and can easily be converted to a GeoSeries
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.assertEqual(
                list(map(str, geopandas.GeoSeries(df.geog2).area)),
                ["0.0", "0.0", "0.0"],
            )

    @unittest.skipIf(geopandas is None, "Requires `geopandas`")
    @mock.patch("google.cloud.bigquery.table.RowIterator.to_dataframe")
    def test_rowiterator_to_geodataframe_delegation(self, to_dataframe):
        """
        RowIterator.to_geodataframe just delegates to RowIterator.to_dataframe.

        This test just demonstrates that. We don't need to test all the
        variations, which are tested for to_dataframe.
        """
        import numpy
        from shapely import wkt

        row_iterator = self._make_one_from_data(
            (("name", "STRING"), ("g", "GEOGRAPHY"))
        )
        bqstorage_client = object()
        dtypes = dict(xxx=numpy.dtype("int64"))
        progress_bar_type = "normal"
        create_bqstorage_client = False
        geography_column = "g"

        to_dataframe.return_value = pandas.DataFrame(
            dict(
                name=["foo"],
                g=[wkt.loads("point(0 0)")],
            )
        )

        df = row_iterator.to_geodataframe(
            bqstorage_client=bqstorage_client,
            dtypes=dtypes,
            progress_bar_type=progress_bar_type,
            create_bqstorage_client=create_bqstorage_client,
            geography_column=geography_column,
        )

        to_dataframe.assert_called_once_with(
            bqstorage_client,
            dtypes,
            progress_bar_type,
            create_bqstorage_client,
            geography_as_object=True,
        )

        self.assertIsInstance(df, geopandas.GeoDataFrame)
        self.assertEqual(len(df), 1)  # verify the number of rows
        self.assertEqual(list(df), ["name", "g"])  # verify the column names
        self.assertEqual(df.name.dtype.name, "object")
        self.assertEqual(df.g.dtype.name, "geometry")
        self.assertIsInstance(df.g, geopandas.GeoSeries)

        with warnings.catch_warnings():
            # Computing the area on a GeoDataFrame that uses a geographic Coordinate
            # Reference System (CRS) produces a warning that we are not interested in.
            warnings.filterwarnings("ignore", category=UserWarning)
            self.assertEqual(list(map(str, df.area)), ["0.0"])
            self.assertEqual(list(map(str, df.g.area)), ["0.0"])

        self.assertEqual([v.__class__.__name__ for v in df.g], ["Point"])


class TestPartitionRange(unittest.TestCase):
    def _get_target_class(self):
        from google.cloud.bigquery.table import PartitionRange

        return PartitionRange

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        object_under_test = self._make_one()
        assert object_under_test.start is None
        assert object_under_test.end is None
        assert object_under_test.interval is None

    def test_constructor_w_properties(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        assert object_under_test.start == 1
        assert object_under_test.end == 10
        assert object_under_test.interval == 2

    def test_constructor_w_resource(self):
        object_under_test = self._make_one(
            _properties={"start": -1234567890, "end": 1234567890, "interval": 1000000}
        )
        assert object_under_test.start == -1234567890
        assert object_under_test.end == 1234567890
        assert object_under_test.interval == 1000000

    def test___eq___start_mismatch(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        other = self._make_one(start=2, end=10, interval=2)
        self.assertNotEqual(object_under_test, other)

    def test___eq___end__mismatch(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        other = self._make_one(start=1, end=11, interval=2)
        self.assertNotEqual(object_under_test, other)

    def test___eq___interval__mismatch(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        other = self._make_one(start=1, end=11, interval=3)
        self.assertNotEqual(object_under_test, other)

    def test___eq___hit(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        other = self._make_one(start=1, end=10, interval=2)
        self.assertEqual(object_under_test, other)

    def test__eq___type_mismatch(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        self.assertNotEqual(object_under_test, object())
        self.assertEqual(object_under_test, mock.ANY)

    def test_unhashable_object(self):
        object_under_test1 = self._make_one(start=1, end=10, interval=2)

        with self.assertRaisesRegex(TypeError, r".*unhashable type.*"):
            hash(object_under_test1)

    def test_repr(self):
        object_under_test = self._make_one(start=1, end=10, interval=2)
        assert repr(object_under_test) == "PartitionRange(end=10, interval=2, start=1)"


class TestRangePartitioning(unittest.TestCase):
    def _get_target_class(self):
        from google.cloud.bigquery.table import RangePartitioning

        return RangePartitioning

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        object_under_test = self._make_one()
        assert object_under_test.field is None
        assert object_under_test.range_.start is None
        assert object_under_test.range_.end is None
        assert object_under_test.range_.interval is None

    def test_constructor_w_properties(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        assert object_under_test.field == "integer_col"
        assert object_under_test.range_.start == 1
        assert object_under_test.range_.end == 10
        assert object_under_test.range_.interval == 2

    def test_constructor_w_resource(self):
        object_under_test = self._make_one(
            _properties={
                "field": "some_column",
                "range": {"start": -1234567890, "end": 1234567890, "interval": 1000000},
            }
        )
        assert object_under_test.field == "some_column"
        assert object_under_test.range_.start == -1234567890
        assert object_under_test.range_.end == 1234567890
        assert object_under_test.range_.interval == 1000000

    def test_range_w_wrong_type(self):
        object_under_test = self._make_one()
        with pytest.raises(ValueError, match="PartitionRange"):
            object_under_test.range_ = object()

    def test___eq___field_mismatch(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        other = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="float_col"
        )
        self.assertNotEqual(object_under_test, other)

    def test___eq___range__mismatch(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        other = self._make_one(
            range_=PartitionRange(start=2, end=20, interval=2), field="float_col"
        )
        self.assertNotEqual(object_under_test, other)

    def test___eq___hit(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        other = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        self.assertEqual(object_under_test, other)

    def test__eq___type_mismatch(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        self.assertNotEqual(object_under_test, object())
        self.assertEqual(object_under_test, mock.ANY)

    def test_unhashable_object(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test1 = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        with self.assertRaisesRegex(TypeError, r".*unhashable type.*"):
            hash(object_under_test1)

    def test_repr(self):
        from google.cloud.bigquery.table import PartitionRange

        object_under_test = self._make_one(
            range_=PartitionRange(start=1, end=10, interval=2), field="integer_col"
        )
        assert (
            repr(object_under_test)
            == "RangePartitioning(field='integer_col', range_=PartitionRange(end=10, interval=2, start=1))"
        )


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

    def test_constructor_explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY, field="name", expiration_ms=10000
        )

        self.assertEqual(time_partitioning.type_, "DAY")
        self.assertEqual(time_partitioning.field, "name")
        self.assertEqual(time_partitioning.expiration_ms, 10000)

    def test_require_partition_filter_warns_deprecation(self):
        object_under_test = self._make_one()

        with warnings.catch_warnings(record=True) as warned:
            assert object_under_test.require_partition_filter is None
            object_under_test.require_partition_filter = True
            assert object_under_test.require_partition_filter

        assert len(warned) == 3
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

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

    def test_from_api_repr_minimal(self):
        from google.cloud.bigquery.table import TimePartitioningType

        klass = self._get_target_class()
        api_repr = {"type": "DAY"}
        time_partitioning = klass.from_api_repr(api_repr)

        self.assertEqual(time_partitioning.type_, TimePartitioningType.DAY)
        self.assertIsNone(time_partitioning.field)
        self.assertIsNone(time_partitioning.expiration_ms)

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

        with warnings.catch_warnings(record=True) as warned:
            self.assertTrue(time_partitioning.require_partition_filter)

        self.assertIs(warned[0].category, PendingDeprecationWarning)

    def test_to_api_repr_defaults(self):
        time_partitioning = self._make_one()
        expected = {"type": "DAY"}
        self.assertEqual(time_partitioning.to_api_repr(), expected)

    def test_to_api_repr_explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY, field="name", expiration_ms=10000
        )

        with warnings.catch_warnings(record=True) as warned:
            time_partitioning.require_partition_filter = True

        self.assertIs(warned[0].category, PendingDeprecationWarning)

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
        time_partitioning = self._make_one(field="foo", expiration_ms=100000)
        other = self._make_one(field="foo", expiration_ms=100000)
        with warnings.catch_warnings(record=True) as warned:
            time_partitioning.require_partition_filter = True
            other.require_partition_filter = False

        assert len(warned) == 2
        for warning in warned:
            self.assertIs(warning.category, PendingDeprecationWarning)

        self.assertNotEqual(time_partitioning, other)

    def test___eq___hit(self):
        time_partitioning = self._make_one(field="foo", expiration_ms=100000)
        other = self._make_one(field="foo", expiration_ms=100000)
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
        expected = "TimePartitioning(type_='DAY')"
        self.assertEqual(repr(time_partitioning), expected)

    def test___repr___explicit(self):
        from google.cloud.bigquery.table import TimePartitioningType

        time_partitioning = self._make_one(
            type_=TimePartitioningType.DAY, field="name", expiration_ms=10000
        )
        expected = "TimePartitioning(expiration_ms=10000,field='name',type_='DAY')"
        self.assertEqual(repr(time_partitioning), expected)

    def test_set_expiration_w_none(self):
        time_partitioning = self._make_one()
        time_partitioning.expiration_ms = None
        assert time_partitioning._properties["expirationMs"] is None


@pytest.mark.parametrize(
    "table_path",
    (
        "my-project.my_dataset.my_table",
        "my-project.my_dataset.my_table$20181225",
        "my-project.my_dataset.my_table@1234567890",
        "my-project.my_dataset.my_table$20181225@1234567890",
    ),
)
def test_table_reference_to_bqstorage_v1_stable(table_path):
    from google.cloud.bigquery import table as mut

    expected = "projects/my-project/datasets/my_dataset/tables/my_table"

    for klass in (mut.TableReference, mut.Table, mut.TableListItem):
        got = klass.from_string(table_path).to_bqstorage()
        assert got == expected
