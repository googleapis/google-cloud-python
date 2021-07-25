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

import base64
import concurrent.futures
import csv
import datetime
import decimal
import io
import json
import operator
import os
import pathlib
import time
import unittest
import uuid
from typing import Optional

import psutil
import pytest

from google.cloud.bigquery._pandas_helpers import _BIGNUMERIC_SUPPORT
from . import helpers

try:
    from google.cloud import bigquery_storage
except ImportError:  # pragma: NO COVER
    bigquery_storage = None

try:
    import fastavro  # to parse BQ storage client results
except ImportError:  # pragma: NO COVER
    fastavro = None

try:
    import pyarrow
    import pyarrow.types
except ImportError:  # pragma: NO COVER
    pyarrow = None

from google.api_core.exceptions import PreconditionFailed
from google.api_core.exceptions import BadRequest
from google.api_core.exceptions import ClientError
from google.api_core.exceptions import Conflict
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import ServiceUnavailable
from google.api_core.exceptions import TooManyRequests
from google.api_core.iam import Policy
from google.cloud import bigquery
from google.cloud import bigquery_v2
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.table import Table
from google.cloud._helpers import UTC
from google.cloud.bigquery import dbapi, enums
from google.cloud import storage
from google.cloud.datacatalog_v1 import types as datacatalog_types
from google.cloud.datacatalog_v1 import PolicyTagManagerClient

from test_utils.retry import RetryErrors
from test_utils.retry import RetryInstanceState
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


JOB_TIMEOUT = 120  # 2 minutes
DATA_PATH = pathlib.Path(__file__).parent.parent / "data"

# Common table data used for many tests.
ROWS = [
    ("Phred Phlyntstone", 32),
    ("Bharney Rhubble", 33),
    ("Wylma Phlyntstone", 29),
    ("Bhettye Rhubble", 27),
]
HEADER_ROW = ("Full Name", "Age")
SCHEMA = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]
CLUSTERING_SCHEMA = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("body_height_cm", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("date_of_birth", "DATE", mode="REQUIRED"),
]
TIME_PARTITIONING_CLUSTERING_FIELDS_SCHEMA = [
    bigquery.SchemaField("transaction_time", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("transaction_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("user_email", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("store_code", "STRING", mode="REQUIRED"),
    bigquery.SchemaField(
        "items",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("item_code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("comments", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("expiration_date", "DATE", mode="REQUIRED"),
        ],
    ),
]

# The VPC-SC team maintains a mirror of the GCS bucket used for code
# samples. The public bucket crosses the configured security boundary.
# See: https://github.com/googleapis/google-cloud-python/issues/8550
SAMPLES_BUCKET = os.environ.get("GCLOUD_TEST_SAMPLES_BUCKET", "cloud-samples-data")

retry_storage_errors = RetryErrors(
    (TooManyRequests, InternalServerError, ServiceUnavailable)
)

MTLS_TESTING = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE") == "true"


def _has_rows(result):
    return len(result) > 0


def _make_dataset_id(prefix):
    return f"python_bigquery_tests_system_{prefix}{unique_resource_id()}"


def _load_json_schema(filename="schema.json"):
    from google.cloud.bigquery.table import _parse_schema_resource

    json_filename = DATA_PATH / filename

    with open(json_filename, "r") as schema_file:
        return _parse_schema_resource(json.load(schema_file))


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT: Optional[bigquery.Client] = None
    CURSOR = None


def setUpModule():
    Config.CLIENT = bigquery.Client()
    Config.CURSOR = dbapi.connect(Config.CLIENT).cursor()


class TestBigQuery(unittest.TestCase):
    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        policy_tag_client = PolicyTagManagerClient()

        def _still_in_use(bad_request):
            return any(
                error["reason"] == "resourceInUse" for error in bad_request._errors
            )

        retry_in_use = RetryErrors(BadRequest, error_predicate=_still_in_use)
        retry_storage_errors_conflict = RetryErrors(
            (Conflict, TooManyRequests, InternalServerError, ServiceUnavailable)
        )
        for doomed in self.to_delete:
            if isinstance(doomed, storage.Bucket):
                retry_storage_errors_conflict(doomed.delete)(force=True)
            elif isinstance(doomed, (Dataset, bigquery.DatasetReference)):
                retry_in_use(Config.CLIENT.delete_dataset)(doomed, delete_contents=True)
            elif isinstance(doomed, (Table, bigquery.TableReference)):
                retry_in_use(Config.CLIENT.delete_table)(doomed)
            elif isinstance(doomed, datacatalog_types.Taxonomy):
                policy_tag_client.delete_taxonomy(name=doomed.name)
            else:
                doomed.delete()

    def test_get_service_account_email(self):
        client = Config.CLIENT

        got = client.get_service_account_email()

        self.assertIsInstance(got, str)
        self.assertIn("@", got)

    def _create_bucket(self, bucket_name, location=None):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        retry_storage_errors(storage_client.create_bucket)(
            bucket_name, location=location
        )
        self.to_delete.append(bucket)

        return bucket

    def test_close_releases_open_sockets(self):
        current_process = psutil.Process()
        conn_count_start = len(current_process.connections())

        client = Config.CLIENT
        client.query(
            """
            SELECT
                source_year AS year, COUNT(is_male) AS birth_count
            FROM `bigquery-public-data.samples.natality`
            GROUP BY year
            ORDER BY year DESC
            LIMIT 15
            """
        )

        client.close()

        conn_count_end = len(current_process.connections())
        self.assertLessEqual(conn_count_end, conn_count_start)

    def test_create_dataset(self):
        DATASET_ID = _make_dataset_id("create_dataset")
        dataset = self.temp_dataset(DATASET_ID)

        self.assertTrue(_dataset_exists(dataset))
        self.assertEqual(dataset.dataset_id, DATASET_ID)
        self.assertEqual(dataset.project, Config.CLIENT.project)

    def test_get_dataset(self):
        dataset_id = _make_dataset_id("get_dataset")
        client = Config.CLIENT
        project = client.project
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        dataset_arg = Dataset(dataset_ref)
        dataset_arg.friendly_name = "Friendly"
        dataset_arg.description = "Description"
        dataset = helpers.retry_403(client.create_dataset)(dataset_arg)
        self.to_delete.append(dataset)
        dataset_ref = bigquery.DatasetReference(project, dataset_id)

        # Get with a reference.
        got = client.get_dataset(dataset_ref)
        self.assertEqual(got.friendly_name, "Friendly")
        self.assertEqual(got.description, "Description")

        # Get with a string.
        got = client.get_dataset(dataset_id)
        self.assertEqual(got.friendly_name, "Friendly")
        self.assertEqual(got.description, "Description")

        # Get with a fully-qualified string.
        got = client.get_dataset("{}.{}".format(client.project, dataset_id))
        self.assertEqual(got.friendly_name, "Friendly")
        self.assertEqual(got.description, "Description")

    def test_update_dataset(self):
        dataset = self.temp_dataset(_make_dataset_id("update_dataset"))
        self.assertTrue(_dataset_exists(dataset))
        self.assertIsNone(dataset.friendly_name)
        self.assertIsNone(dataset.description)
        self.assertEqual(dataset.labels, {})

        dataset.friendly_name = "Friendly"
        dataset.description = "Description"
        dataset.labels = {"priority": "high", "color": "blue"}
        ds2 = Config.CLIENT.update_dataset(
            dataset, ("friendly_name", "description", "labels")
        )
        self.assertEqual(ds2.friendly_name, "Friendly")
        self.assertEqual(ds2.description, "Description")
        self.assertEqual(ds2.labels, {"priority": "high", "color": "blue"})

        ds2.labels = {
            "color": "green",  # change
            "shape": "circle",  # add
            "priority": None,  # delete
        }
        ds3 = Config.CLIENT.update_dataset(ds2, ["labels"])
        self.assertEqual(ds3.labels, {"color": "green", "shape": "circle"})

        # If we try to update using d2 again, it will fail because the
        # previous update changed the ETag.
        ds2.description = "no good"
        with self.assertRaises(PreconditionFailed):
            Config.CLIENT.update_dataset(ds2, ["description"])

    def test_list_datasets(self):
        datasets_to_create = [
            "new" + unique_resource_id(),
            "newer" + unique_resource_id(),
            "newest" + unique_resource_id(),
        ]
        for dataset_id in datasets_to_create:
            self.temp_dataset(dataset_id)

        # Retrieve the datasets.
        iterator = Config.CLIENT.list_datasets()
        all_datasets = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [
            dataset
            for dataset in all_datasets
            if dataset.dataset_id in datasets_to_create
            and dataset.project == Config.CLIENT.project
        ]
        self.assertEqual(len(created), len(datasets_to_create))

    def test_list_datasets_w_project(self):
        # Retrieve datasets from a different project.
        iterator = Config.CLIENT.list_datasets(project="bigquery-public-data")
        all_datasets = frozenset([dataset.dataset_id for dataset in iterator])
        self.assertIn("usa_names", all_datasets)

    def test_create_table(self):
        dataset = self.temp_dataset(_make_dataset_id("create_table"))
        table_id = "test_table"
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_id)

    def test_create_table_with_policy(self):
        from google.cloud.bigquery.schema import PolicyTagList

        dataset = self.temp_dataset(_make_dataset_id("create_table_with_policy"))
        table_id = "test_table"
        policy_1 = PolicyTagList(
            names=[
                "projects/{}/locations/us/taxonomies/1/policyTags/2".format(
                    Config.CLIENT.project
                ),
            ]
        )
        policy_2 = PolicyTagList(
            names=[
                "projects/{}/locations/us/taxonomies/3/policyTags/4".format(
                    Config.CLIENT.project
                ),
            ]
        )

        schema = [
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField(
                "secret_int", "INTEGER", mode="REQUIRED", policy_tags=policy_1
            ),
        ]
        table_arg = Table(dataset.table(table_id), schema=schema)
        self.assertFalse(_table_exists(table_arg))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(policy_1, table.schema[1].policy_tags)

        # Amend the schema to replace the policy tags
        new_schema = table.schema[:]
        old_field = table.schema[1]
        new_schema[1] = bigquery.SchemaField(
            name=old_field.name,
            field_type=old_field.field_type,
            mode=old_field.mode,
            description=old_field.description,
            fields=old_field.fields,
            policy_tags=policy_2,
        )

        table.schema = new_schema
        table2 = Config.CLIENT.update_table(table, ["schema"])
        self.assertEqual(policy_2, table2.schema[1].policy_tags)

    def test_create_table_with_real_custom_policy(self):
        from google.cloud.bigquery.schema import PolicyTagList

        policy_tag_client = PolicyTagManagerClient()
        taxonomy_parent = f"projects/{Config.CLIENT.project}/locations/us"

        new_taxonomy = datacatalog_types.Taxonomy(
            display_name="Custom test taxonomy" + unique_resource_id(),
            description="This taxonomy is ony used for a test.",
            activated_policy_types=[
                datacatalog_types.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
            ],
        )

        taxonomy = policy_tag_client.create_taxonomy(
            parent=taxonomy_parent, taxonomy=new_taxonomy
        )
        self.to_delete.insert(0, taxonomy)

        parent_policy_tag = policy_tag_client.create_policy_tag(
            parent=taxonomy.name,
            policy_tag=datacatalog_types.PolicyTag(
                display_name="Parent policy tag", parent_policy_tag=None
            ),
        )
        child_policy_tag = policy_tag_client.create_policy_tag(
            parent=taxonomy.name,
            policy_tag=datacatalog_types.PolicyTag(
                display_name="Child policy tag",
                parent_policy_tag=parent_policy_tag.name,
            ),
        )

        dataset = self.temp_dataset(
            _make_dataset_id("create_table_with_real_custom_policy")
        )
        table_id = "test_table"
        policy_1 = PolicyTagList(names=[parent_policy_tag.name])
        policy_2 = PolicyTagList(names=[child_policy_tag.name])

        schema = [
            bigquery.SchemaField(
                "first_name", "STRING", mode="REQUIRED", policy_tags=policy_1
            ),
            bigquery.SchemaField(
                "age", "INTEGER", mode="REQUIRED", policy_tags=policy_2
            ),
        ]
        table_arg = Table(dataset.table(table_id), schema=schema)
        self.assertFalse(_table_exists(table_arg))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertCountEqual(
            list(table.schema[0].policy_tags.names), [parent_policy_tag.name]
        )
        self.assertCountEqual(
            list(table.schema[1].policy_tags.names), [child_policy_tag.name]
        )

    def test_create_table_w_time_partitioning_w_clustering_fields(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = self.temp_dataset(_make_dataset_id("create_table_tp_cf"))
        table_id = "test_table"
        table_arg = Table(
            dataset.table(table_id), schema=TIME_PARTITIONING_CLUSTERING_FIELDS_SCHEMA
        )
        self.assertFalse(_table_exists(table_arg))

        table_arg.time_partitioning = TimePartitioning(field="transaction_time")

        table_arg.clustering_fields = ["user_email", "store_code"]
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_id)
        time_partitioning = table.time_partitioning
        self.assertEqual(time_partitioning.type_, TimePartitioningType.DAY)
        self.assertEqual(time_partitioning.field, "transaction_time")
        self.assertEqual(table.clustering_fields, ["user_email", "store_code"])

    def test_delete_dataset_with_string(self):
        dataset_id = _make_dataset_id("delete_table_true_with_string")
        project = Config.CLIENT.project
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        helpers.retry_403(Config.CLIENT.create_dataset)(Dataset(dataset_ref))
        self.assertTrue(_dataset_exists(dataset_ref))
        Config.CLIENT.delete_dataset(dataset_id)
        self.assertFalse(_dataset_exists(dataset_ref))

    def test_delete_dataset_delete_contents_true(self):
        dataset_id = _make_dataset_id("delete_table_true_with_content")
        project = Config.CLIENT.project
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        dataset = helpers.retry_403(Config.CLIENT.create_dataset)(Dataset(dataset_ref))

        table_id = "test_table"
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        Config.CLIENT.delete_dataset(dataset, delete_contents=True)

        self.assertFalse(_table_exists(table))

    def test_delete_dataset_delete_contents_false(self):
        from google.api_core import exceptions

        dataset = self.temp_dataset(_make_dataset_id("delete_table_false"))
        table_id = "test_table"
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)

        helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        with self.assertRaises(exceptions.BadRequest):
            Config.CLIENT.delete_dataset(dataset)

    def test_get_table_w_public_dataset(self):
        public = "bigquery-public-data"
        dataset_id = "samples"
        table_id = "shakespeare"
        table_ref = DatasetReference(public, dataset_id).table(table_id)

        # Get table with reference.
        table = Config.CLIENT.get_table(table_ref)
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.project, public)
        schema_names = [field.name for field in table.schema]
        self.assertEqual(schema_names, ["word", "word_count", "corpus", "corpus_date"])

        # Get table with string.
        table = Config.CLIENT.get_table("{}.{}.{}".format(public, dataset_id, table_id))
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.project, public)

    def test_list_partitions(self):
        table_ref = DatasetReference(
            "bigquery-public-data", "ethereum_blockchain"
        ).table("blocks")
        all_rows = Config.CLIENT.list_partitions(table_ref)
        self.assertIn("20180801", all_rows)
        self.assertGreater(len(all_rows), 1000)

    def test_list_tables(self):
        dataset_id = _make_dataset_id("list_tables")
        dataset = self.temp_dataset(dataset_id)
        # Retrieve tables before any are created for the dataset.
        iterator = Config.CLIENT.list_tables(dataset)
        all_tables = list(iterator)
        self.assertEqual(all_tables, [])
        self.assertIsNone(iterator.next_page_token)

        # Insert some tables to be listed.
        tables_to_create = [
            "new" + unique_resource_id(),
            "newer" + unique_resource_id(),
            "newest" + unique_resource_id(),
        ]
        for table_name in tables_to_create:
            table = Table(dataset.table(table_name), schema=SCHEMA)
            created_table = helpers.retry_403(Config.CLIENT.create_table)(table)
            self.to_delete.insert(0, created_table)

        # Retrieve the tables.
        iterator = Config.CLIENT.list_tables(dataset)
        all_tables = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [
            table
            for table in all_tables
            if (table.table_id in tables_to_create and table.dataset_id == dataset_id)
        ]
        self.assertEqual(len(created), len(tables_to_create))

        # List tables with a string ID.
        iterator = Config.CLIENT.list_tables(dataset_id)
        self.assertGreater(len(list(iterator)), 0)

        # List tables with a fully-qualified string ID.
        iterator = Config.CLIENT.list_tables(
            "{}.{}".format(Config.CLIENT.project, dataset_id)
        )
        self.assertGreater(len(list(iterator)), 0)

    def test_update_table(self):
        dataset = self.temp_dataset(_make_dataset_id("update_table"))

        TABLE_NAME = "test_table"
        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.description)
        self.assertEqual(table.labels, {})
        table.friendly_name = "Friendly"
        table.description = "Description"
        table.labels = {"priority": "high", "color": "blue"}

        table2 = Config.CLIENT.update_table(
            table, ["friendly_name", "description", "labels"]
        )

        self.assertEqual(table2.friendly_name, "Friendly")
        self.assertEqual(table2.description, "Description")
        self.assertEqual(table2.labels, {"priority": "high", "color": "blue"})

        table2.description = None
        table2.labels = {
            "color": "green",  # change
            "shape": "circle",  # add
            "priority": None,  # delete
        }
        table3 = Config.CLIENT.update_table(table2, ["description", "labels"])
        self.assertIsNone(table3.description)
        self.assertEqual(table3.labels, {"color": "green", "shape": "circle"})

        # If we try to update using table2 again, it will fail because the
        # previous update changed the ETag.
        table2.description = "no good"
        with self.assertRaises(PreconditionFailed):
            Config.CLIENT.update_table(table2, ["description"])

    def test_update_table_schema(self):
        dataset = self.temp_dataset(_make_dataset_id("update_table"))

        TABLE_NAME = "test_table"
        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        voter = bigquery.SchemaField("voter", "BOOLEAN", mode="NULLABLE")
        schema = table.schema
        schema.append(voter)
        table.schema = schema

        updated_table = Config.CLIENT.update_table(table, ["schema"])

        self.assertEqual(len(updated_table.schema), len(schema))
        for found, expected in zip(updated_table.schema, schema):
            self.assertEqual(found.name, expected.name)
            self.assertEqual(found.field_type, expected.field_type)
            self.assertEqual(found.mode, expected.mode)

    def test_unset_table_schema_attributes(self):
        from google.cloud.bigquery.schema import PolicyTagList

        dataset = self.temp_dataset(_make_dataset_id("unset_policy_tags"))
        table_id = "test_table"
        policy_tags = PolicyTagList(
            names=[
                "projects/{}/locations/us/taxonomies/1/policyTags/2".format(
                    Config.CLIENT.project
                ),
            ]
        )

        schema = [
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField(
                "secret_int",
                "INTEGER",
                mode="REQUIRED",
                description="This field is numeric",
                policy_tags=policy_tags,
            ),
        ]
        table_arg = Table(dataset.table(table_id), schema=schema)
        self.assertFalse(_table_exists(table_arg))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(policy_tags, table.schema[1].policy_tags)

        # Amend the schema to replace the policy tags
        new_schema = table.schema[:]
        old_field = table.schema[1]
        new_schema[1] = bigquery.SchemaField(
            name=old_field.name,
            field_type=old_field.field_type,
            mode=old_field.mode,
            description=None,
            fields=old_field.fields,
            policy_tags=None,
        )

        table.schema = new_schema
        updated_table = Config.CLIENT.update_table(table, ["schema"])

        self.assertFalse(updated_table.schema[1].description)  # Empty string or None.
        self.assertEqual(updated_table.schema[1].policy_tags.names, ())

    def test_update_table_clustering_configuration(self):
        dataset = self.temp_dataset(_make_dataset_id("update_table"))

        TABLE_NAME = "test_table"
        table_arg = Table(dataset.table(TABLE_NAME), schema=CLUSTERING_SCHEMA)
        self.assertFalse(_table_exists(table_arg))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))

        table.clustering_fields = ["full_name", "date_of_birth"]
        table2 = Config.CLIENT.update_table(table, ["clustering_fields"])
        self.assertEqual(table2.clustering_fields, ["full_name", "date_of_birth"])

        table2.clustering_fields = None
        table3 = Config.CLIENT.update_table(table2, ["clustering_fields"])
        self.assertIsNone(table3.clustering_fields, None)

    @staticmethod
    def _fetch_single_page(table, selected_fields=None):
        iterator = Config.CLIENT.list_rows(table, selected_fields=selected_fields)
        page = next(iterator.pages)
        return list(page)

    def _create_table_many_columns(self, rowcount):
        # Generate a table of maximum width via CREATE TABLE AS SELECT.
        # first column is named 'rowval', and has a value from 1..rowcount
        # Subsequent column is named col_<N> and contains the value N*rowval,
        # where N is between 1 and 9999 inclusive.
        dsname = _make_dataset_id("wide_schema")
        dataset = self.temp_dataset(dsname)
        table_id = "many_columns"
        table_ref = dataset.table(table_id)
        self.to_delete.insert(0, table_ref)
        colprojections = ",".join(
            ["r * {} as col_{}".format(n, n) for n in range(1, 10000)]
        )
        sql = """
            CREATE TABLE {}.{}
            AS
            SELECT
                r as rowval,
                {}
            FROM
              UNNEST(GENERATE_ARRAY(1,{},1)) as r
            """.format(
            dsname, table_id, colprojections, rowcount
        )
        query_job = Config.CLIENT.query(sql)
        query_job.result()
        self.assertEqual(query_job.statement_type, "CREATE_TABLE_AS_SELECT")
        self.assertEqual(query_job.ddl_operation_performed, "CREATE")
        self.assertEqual(query_job.ddl_target_table, table_ref)

        return table_ref

    def test_query_many_columns(self):
        # Test working with the widest schema BigQuery supports, 10k columns.
        row_count = 2
        table_ref = self._create_table_many_columns(row_count)
        rows = list(
            Config.CLIENT.query(
                "SELECT * FROM `{}.{}`".format(table_ref.dataset_id, table_ref.table_id)
            )
        )

        self.assertEqual(len(rows), row_count)

        # check field representations adhere to expected values.
        correctwidth = 0
        badvals = 0
        for r in rows:
            vals = r._xxx_values
            rowval = vals[0]
            if len(vals) == 10000:
                correctwidth = correctwidth + 1
            for n in range(1, 10000):
                if vals[n] != rowval * (n):
                    badvals = badvals + 1
        self.assertEqual(correctwidth, row_count)
        self.assertEqual(badvals, 0)

    def test_insert_rows_then_dump_table(self):
        NOW_SECONDS = 1448911495.484366
        NOW = datetime.datetime.utcfromtimestamp(NOW_SECONDS).replace(tzinfo=UTC)
        ROWS = [
            ("Phred Phlyntstone", 32, NOW),
            ("Bharney Rhubble", 33, NOW + datetime.timedelta(seconds=10)),
            ("Wylma Phlyntstone", 29, NOW + datetime.timedelta(seconds=20)),
            ("Bhettye Rhubble", 27, None),
        ]
        ROW_IDS = range(len(ROWS))

        dataset = self.temp_dataset(_make_dataset_id("insert_rows_then_dump"))
        TABLE_ID = "test_table"
        schema = [
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("now", "TIMESTAMP"),
        ]
        table_arg = Table(dataset.table(TABLE_ID), schema=schema)
        self.assertFalse(_table_exists(table_arg))
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))

        errors = Config.CLIENT.insert_rows(table, ROWS, row_ids=ROW_IDS)
        self.assertEqual(len(errors), 0)

        rows = ()

        # Allow for "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)
        row_tuples = [r.values() for r in rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age), sorted(ROWS, key=by_age))

    def test_load_table_from_local_avro_file_then_dump_table(self):
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        TABLE_NAME = "test_table_avro"
        ROWS = [
            ("violet", 400),
            ("indigo", 445),
            ("blue", 475),
            ("green", 510),
            ("yellow", 570),
            ("orange", 590),
            ("red", 650),
        ]

        dataset = self.temp_dataset(_make_dataset_id("load_local_then_dump"))
        table_ref = dataset.table(TABLE_NAME)
        table = Table(table_ref)
        self.to_delete.insert(0, table)

        with open(DATA_PATH / "colors.avro", "rb") as avrof:
            config = bigquery.LoadJobConfig()
            config.source_format = SourceFormat.AVRO
            config.write_disposition = WriteDisposition.WRITE_TRUNCATE
            job = Config.CLIENT.load_table_from_file(
                avrof, table_ref, job_config=config
            )
        # Retry until done.
        job.result(timeout=JOB_TIMEOUT)

        self.assertEqual(job.output_rows, len(ROWS))

        table = Config.CLIENT.get_table(table)
        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        by_wavelength = operator.itemgetter(1)
        self.assertEqual(
            sorted(row_tuples, key=by_wavelength), sorted(ROWS, key=by_wavelength)
        )

    def test_load_table_from_local_parquet_file_decimal_types(self):
        from google.cloud.bigquery.enums import DecimalTargetType
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        TABLE_NAME = "test_table_parquet"

        expected_rows = [
            (decimal.Decimal("123.999999999999"),),
            (decimal.Decimal("99999999999999999999999999.999999999999"),),
        ]

        dataset = self.temp_dataset(_make_dataset_id("load_local_parquet_then_dump"))
        table_ref = dataset.table(TABLE_NAME)
        table = Table(table_ref)
        self.to_delete.insert(0, table)

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = SourceFormat.PARQUET
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job_config.decimal_target_types = [
            DecimalTargetType.NUMERIC,
            DecimalTargetType.BIGNUMERIC,
            DecimalTargetType.STRING,
        ]

        with open(DATA_PATH / "numeric_38_12.parquet", "rb") as parquet_file:
            job = Config.CLIENT.load_table_from_file(
                parquet_file, table_ref, job_config=job_config
            )

        job.result(timeout=JOB_TIMEOUT)  # Retry until done.

        self.assertEqual(job.output_rows, len(expected_rows))

        table = Config.CLIENT.get_table(table)
        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        self.assertEqual(sorted(row_tuples), sorted(expected_rows))

        # Forcing the NUMERIC type, however, should result in an error.
        job_config.decimal_target_types = [DecimalTargetType.NUMERIC]

        with open(DATA_PATH / "numeric_38_12.parquet", "rb") as parquet_file:
            job = Config.CLIENT.load_table_from_file(
                parquet_file, table_ref, job_config=job_config
            )

        with self.assertRaises(BadRequest) as exc_info:
            job.result(timeout=JOB_TIMEOUT)

        exc_msg = str(exc_info.exception)
        self.assertIn("out of valid NUMERIC range", exc_msg)

    def test_load_table_from_json_basic_use(self):
        table_schema = (
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("birthday", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("is_awesome", "BOOLEAN", mode="REQUIRED"),
        )

        json_rows = [
            {"name": "John", "age": 18, "birthday": "2001-10-15", "is_awesome": False},
            {"name": "Chuck", "age": 79, "birthday": "1940-03-10", "is_awesome": True},
        ]

        dataset_id = _make_dataset_id("bq_system_test")
        self.temp_dataset(dataset_id)
        table_id = "{}.{}.load_table_from_json_basic_use".format(
            Config.CLIENT.project, dataset_id
        )

        # Create the table before loading so that schema mismatch errors are
        # identified.
        table = helpers.retry_403(Config.CLIENT.create_table)(
            Table(table_id, schema=table_schema)
        )
        self.to_delete.insert(0, table)

        job_config = bigquery.LoadJobConfig(schema=table_schema)
        load_job = Config.CLIENT.load_table_from_json(
            json_rows, table_id, job_config=job_config
        )
        load_job.result()

        table = Config.CLIENT.get_table(table)
        self.assertEqual(tuple(table.schema), table_schema)
        self.assertEqual(table.num_rows, 2)

    def test_load_table_from_json_schema_autodetect(self):
        json_rows = [
            {"name": "John", "age": 18, "birthday": "2001-10-15", "is_awesome": False},
            {"name": "Chuck", "age": 79, "birthday": "1940-03-10", "is_awesome": True},
        ]

        dataset_id = _make_dataset_id("bq_system_test")
        self.temp_dataset(dataset_id)
        table_id = "{}.{}.load_table_from_json_basic_use".format(
            Config.CLIENT.project, dataset_id
        )

        # Use schema with NULLABLE fields, because schema autodetection
        # defaults to field mode NULLABLE.
        table_schema = (
            bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("birthday", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("is_awesome", "BOOLEAN", mode="NULLABLE"),
        )
        # create the table before loading so that the column order is predictable
        table = helpers.retry_403(Config.CLIENT.create_table)(
            Table(table_id, schema=table_schema)
        )
        self.to_delete.insert(0, table)

        # do not pass an explicit job config to trigger automatic schema detection
        load_job = Config.CLIENT.load_table_from_json(json_rows, table_id)
        load_job.result()

        table = Config.CLIENT.get_table(table)
        self.assertEqual(tuple(table.schema), table_schema)
        self.assertEqual(table.num_rows, 2)

    def test_load_avro_from_uri_then_dump_table(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        table_name = "test_table"
        rows = [
            ("violet", 400),
            ("indigo", 445),
            ("blue", 475),
            ("green", 510),
            ("yellow", 570),
            ("orange", 590),
            ("red", 650),
        ]
        with open(DATA_PATH / "colors.avro", "rb") as f:
            GS_URL = self._write_avro_to_storage(
                "bq_load_test" + unique_resource_id(), "colors.avro", f
            )

        dataset = self.temp_dataset(_make_dataset_id("bq_load_test"))
        table_arg = dataset.table(table_name)
        table = helpers.retry_403(Config.CLIENT.create_table)(Table(table_arg))
        self.to_delete.insert(0, table)

        config = bigquery.LoadJobConfig()
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.source_format = SourceFormat.AVRO
        config.write_disposition = WriteDisposition.WRITE_EMPTY
        job = Config.CLIENT.load_table_from_uri(GS_URL, table_arg, job_config=config)
        job.result(timeout=JOB_TIMEOUT)
        self.assertEqual(job.output_rows, len(rows))

        table = Config.CLIENT.get_table(table)
        fetched = self._fetch_single_page(table)
        row_tuples = [r.values() for r in fetched]
        self.assertEqual(
            sorted(row_tuples, key=lambda x: x[1]), sorted(rows, key=lambda x: x[1])
        )

    def test_load_table_from_uri_then_dump_table(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        TABLE_ID = "test_table"
        GS_URL = self._write_csv_to_storage(
            "bq_load_test" + unique_resource_id(), "person_ages.csv", HEADER_ROW, ROWS
        )

        dataset = self.temp_dataset(_make_dataset_id("load_gcs_then_dump"))

        table_arg = Table(dataset.table(TABLE_ID), schema=SCHEMA)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        config = bigquery.LoadJobConfig()
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.skip_leading_rows = 1
        config.source_format = SourceFormat.CSV
        config.write_disposition = WriteDisposition.WRITE_EMPTY
        job = Config.CLIENT.load_table_from_uri(
            GS_URL, dataset.table(TABLE_ID), job_config=config
        )

        # Allow for 90 seconds of "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age), sorted(ROWS, key=by_age))

    def test_load_table_from_file_w_explicit_location(self):
        # Create a temporary bucket for extract files.
        bucket_name = "bq_load_table_eu_extract_test" + unique_resource_id()
        self._create_bucket(bucket_name, location="eu")

        # Create a temporary dataset & table in the EU.
        table_bytes = io.BytesIO(b"a,3\nb,2\nc,1\n")
        client = Config.CLIENT
        dataset = self.temp_dataset(_make_dataset_id("eu_load_file"), location="EU")
        table_ref = dataset.table("letters")
        job_config = bigquery.LoadJobConfig()
        job_config.skip_leading_rows = 0
        job_config.schema = [
            bigquery.SchemaField("letter", "STRING"),
            bigquery.SchemaField("value", "INTEGER"),
        ]

        # Load the file to an EU dataset with an EU load job.
        load_job = client.load_table_from_file(
            table_bytes, table_ref, location="EU", job_config=job_config
        )
        load_job.result()
        job_id = load_job.job_id

        # Can get the job from the EU.
        load_job = client.get_job(load_job)
        self.assertEqual(job_id, load_job.job_id)
        self.assertEqual("EU", load_job.location)
        self.assertTrue(load_job.exists())

        # Cannot get the job from the US.
        with self.assertRaises(NotFound):
            client.get_job(job_id, location="US")

        load_job_us = client.get_job(job_id)
        load_job_us._properties["jobReference"]["location"] = "US"
        self.assertFalse(load_job_us.exists())
        with self.assertRaises(NotFound):
            load_job_us.reload()

        # Can cancel the job from the EU.
        self.assertTrue(load_job.cancel())
        load_job = client.cancel_job(load_job)
        self.assertEqual(job_id, load_job.job_id)
        self.assertEqual("EU", load_job.location)

        # Cannot cancel the job from the US.
        with self.assertRaises(ClientError):
            client.cancel_job(job_id, location="US")
        with self.assertRaises(ClientError):
            load_job_us.cancel()

        # Can list the table rows.
        table = client.get_table(table_ref)
        self.assertEqual(table.num_rows, 3)
        rows = [(row.letter, row.value) for row in client.list_rows(table)]
        self.assertEqual(list(sorted(rows)), [("a", 3), ("b", 2), ("c", 1)])

        # Verify location behavior with queries
        query_config = bigquery.QueryJobConfig()
        query_config.dry_run = True

        query_string = "SELECT * FROM `{}.letters` LIMIT 1".format(dataset.dataset_id)

        eu_query = client.query(query_string, location="EU", job_config=query_config)
        self.assertTrue(eu_query.done)

        # Cannot query from US.
        with self.assertRaises(GoogleAPICallError):
            list(client.query(query_string, location="US", job_config=query_config))

        # Cannot copy from US.
        with self.assertRaises(GoogleAPICallError):
            client.copy_table(
                table_ref, dataset.table("letters2_us"), location="US"
            ).result()

        # Cannot extract from US.
        with self.assertRaises(GoogleAPICallError):
            client.extract_table(
                table_ref, "gs://{}/letters-us.csv".format(bucket_name), location="US"
            ).result()

    def _write_csv_to_storage(self, bucket_name, blob_name, header_row, data_rows):
        from google.cloud._testing import _NamedTemporaryFile

        bucket = self._create_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, "w") as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(header_row)
                writer.writerows(data_rows)

            with open(temp.name, "rb") as csv_read:
                retry_storage_errors(blob.upload_from_file)(
                    csv_read, content_type="text/csv"
                )

        self.to_delete.insert(0, blob)
        return "gs://{}/{}".format(bucket_name, blob_name)

    def _write_avro_to_storage(self, bucket_name, blob_name, avro_file):
        bucket = self._create_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        retry_storage_errors(blob.upload_from_file)(
            avro_file, content_type="application/x-avro-binary"
        )
        self.to_delete.insert(0, blob)
        return "gs://{}/{}".format(bucket_name, blob_name)

    def _load_table_for_extract_table(self, bucket, blob_name, table, rows):
        from google.cloud._testing import _NamedTemporaryFile

        blob = bucket.blob(blob_name)
        with _NamedTemporaryFile() as temp:
            with open(temp.name, "w") as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(HEADER_ROW)
                writer.writerows(rows)

            with open(temp.name, "rb") as csv_read:
                retry_storage_errors(blob.upload_from_file)(
                    csv_read, content_type="text/csv"
                )

        self.to_delete.insert(0, blob)

        dataset = self.temp_dataset(table.dataset_id)
        table_ref = dataset.table(table.table_id)
        config = bigquery.LoadJobConfig()
        config.autodetect = True
        gs_url = "gs://{}/{}".format(bucket.name, blob_name)
        job = Config.CLIENT.load_table_from_uri(gs_url, table_ref, job_config=config)
        # TODO(jba): do we need this retry now that we have job.result()?
        # Allow for 90 seconds of "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

    def test_extract_table(self):
        local_id = unique_resource_id()
        bucket_name = "bq_extract_test" + local_id
        source_blob_name = "person_ages.csv"
        dataset_id = _make_dataset_id("load_gcs_then_extract")
        table_id = "test_table"
        project = Config.CLIENT.project
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = Table(table_ref)
        self.to_delete.insert(0, table)
        bucket = self._create_bucket(bucket_name)
        self._load_table_for_extract_table(bucket, source_blob_name, table_ref, ROWS)
        destination_blob_name = "person_ages_out.csv"
        destination = bucket.blob(destination_blob_name)
        destination_uri = "gs://{}/person_ages_out.csv".format(bucket_name)

        job = Config.CLIENT.extract_table(table_ref, destination_uri)
        job.result(timeout=100)

        self.to_delete.insert(0, destination)
        got_bytes = retry_storage_errors(destination.download_as_bytes)()
        got = got_bytes.decode("utf-8")
        self.assertIn("Bharney Rhubble", got)

    def test_copy_table(self):
        # If we create a new table to copy from, the test won't work
        # because the new rows will be stored in the streaming buffer,
        # and copy jobs don't read the streaming buffer.
        # We could wait for the streaming buffer to empty, but that could
        # take minutes. Instead we copy a small public table.
        source_dataset = DatasetReference("bigquery-public-data", "samples")
        source_ref = source_dataset.table("shakespeare")
        dest_dataset = self.temp_dataset(_make_dataset_id("copy_table"))
        dest_ref = dest_dataset.table("destination_table")
        job_config = bigquery.CopyJobConfig()
        job = Config.CLIENT.copy_table(source_ref, dest_ref, job_config=job_config)
        job.result()

        dest_table = Config.CLIENT.get_table(dest_ref)
        self.to_delete.insert(0, dest_table)
        # Just check that we got some rows.
        got_rows = self._fetch_single_page(dest_table)
        self.assertTrue(len(got_rows) > 0)

    def test_get_set_iam_policy(self):
        from google.cloud.bigquery.iam import BIGQUERY_DATA_VIEWER_ROLE

        dataset = self.temp_dataset(_make_dataset_id("create_table"))
        table_id = "test_table"
        table_ref = Table(dataset.table(table_id))
        self.assertFalse(_table_exists(table_ref))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_ref)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))

        member = "serviceAccount:{}".format(Config.CLIENT.get_service_account_email())
        BINDING = {
            "role": BIGQUERY_DATA_VIEWER_ROLE,
            "members": {member},
        }

        policy = Config.CLIENT.get_iam_policy(table)
        self.assertIsInstance(policy, Policy)
        self.assertEqual(policy.bindings, [])

        policy.bindings.append(BINDING)
        returned_policy = Config.CLIENT.set_iam_policy(table, policy)
        self.assertEqual(returned_policy.bindings, policy.bindings)

    def test_test_iam_permissions(self):
        dataset = self.temp_dataset(_make_dataset_id("create_table"))
        table_id = "test_table"
        table_ref = Table(dataset.table(table_id))
        self.assertFalse(_table_exists(table_ref))

        table = helpers.retry_403(Config.CLIENT.create_table)(table_ref)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))

        # Test some default permissions.
        permissions = [
            "bigquery.tables.get",
            "bigquery.tables.getData",
            "bigquery.tables.update",
        ]

        response = Config.CLIENT.test_iam_permissions(table, [permissions])
        self.assertEqual(set(response["permissions"]), set(permissions))

    def test_job_cancel(self):
        DATASET_ID = _make_dataset_id("job_cancel")
        JOB_ID_PREFIX = "fetch_" + DATASET_ID
        TABLE_NAME = "test_table"
        QUERY = "SELECT * FROM %s.%s" % (DATASET_ID, TABLE_NAME)

        dataset = self.temp_dataset(DATASET_ID)

        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        job = Config.CLIENT.query(QUERY, job_id_prefix=JOB_ID_PREFIX)
        job.cancel()

        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        # The `cancel` API doesn't leave any reliable traces on
        # the status of the job resource, so we can't really assert for
        # them here.  The best we can do is not that the API call didn't
        # raise an error, and that the job completed (in the `retry()`
        # above).

    def test_job_labels(self):
        DATASET_ID = _make_dataset_id("job_cancel")
        JOB_ID_PREFIX = "fetch_" + DATASET_ID
        QUERY = "SELECT 1 as one"

        self.temp_dataset(DATASET_ID)

        job_config = bigquery.QueryJobConfig(
            labels={"custom_label": "label_value", "another_label": "foo123"}
        )
        job = Config.CLIENT.query(
            QUERY, job_id_prefix=JOB_ID_PREFIX, job_config=job_config
        )

        expected_labels = {"custom_label": "label_value", "another_label": "foo123"}
        self.assertEqual(job.labels, expected_labels)

    def test_get_failed_job(self):
        # issue 4246
        from google.api_core.exceptions import BadRequest

        JOB_ID = "invalid_{}".format(str(uuid.uuid4()))
        QUERY = "SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);"
        PARAM = bigquery.ScalarQueryParameter("ts_value", "TIMESTAMP", 1.4810976e9)

        job_config = bigquery.QueryJobConfig()
        job_config.query_parameters = [PARAM]

        with self.assertRaises(BadRequest):
            Config.CLIENT.query(QUERY, job_id=JOB_ID, job_config=job_config).result()

        job = Config.CLIENT.get_job(JOB_ID)

        with self.assertRaises(ValueError):
            job.query_parameters

    def test_query_w_legacy_sql_types(self):
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        stamp = "%s %s" % (naive.date().isoformat(), naive.time().isoformat())
        zoned = naive.replace(tzinfo=UTC)
        examples = [
            {"sql": "SELECT 1", "expected": 1},
            {"sql": "SELECT 1.3", "expected": 1.3},
            {"sql": "SELECT TRUE", "expected": True},
            {"sql": 'SELECT "ABC"', "expected": "ABC"},
            {"sql": 'SELECT CAST("foo" AS BYTES)', "expected": b"foo"},
            {"sql": 'SELECT CAST("%s" AS TIMESTAMP)' % (stamp,), "expected": zoned},
        ]
        for example in examples:
            job_config = bigquery.QueryJobConfig()
            job_config.use_legacy_sql = True
            rows = list(Config.CLIENT.query(example["sql"], job_config=job_config))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example["expected"])

    def test_query_w_standard_sql_types(self):
        for sql, expected in helpers.STANDARD_SQL_EXAMPLES:
            rows = list(Config.CLIENT.query(sql))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], expected)

    def test_query_w_failed_query(self):
        from google.api_core.exceptions import BadRequest

        with self.assertRaises(BadRequest):
            Config.CLIENT.query("invalid syntax;").result()

    def test_query_w_wrong_config(self):
        from google.cloud.bigquery.job import LoadJobConfig

        good_query = "SELECT 1;"
        rows = list(Config.CLIENT.query("SELECT 1;").result())
        assert rows[0][0] == 1

        bad_config = LoadJobConfig()
        bad_config.source_format = enums.SourceFormat.CSV
        with self.assertRaises(Exception):
            Config.CLIENT.query(good_query, job_config=bad_config).result()

    def test_query_w_timeout(self):
        job_config = bigquery.QueryJobConfig()
        job_config.use_query_cache = False

        query_job = Config.CLIENT.query(
            "SELECT * FROM `bigquery-public-data.github_repos.commits`;",
            job_id_prefix="test_query_w_timeout_",
            location="US",
            job_config=job_config,
        )

        with self.assertRaises(concurrent.futures.TimeoutError):
            query_job.result(timeout=1)

        # Even though the query takes >1 second, the call to getQueryResults
        # should succeed.
        self.assertFalse(query_job.done(timeout=1))
        self.assertIsNotNone(Config.CLIENT.cancel_job(query_job))

    def test_query_w_page_size(self):
        page_size = 45
        query_job = Config.CLIENT.query(
            "SELECT word FROM `bigquery-public-data.samples.shakespeare`;",
            job_id_prefix="test_query_w_page_size_",
        )
        iterator = query_job.result(page_size=page_size)
        self.assertEqual(next(iterator.pages).num_items, page_size)

    def test_query_w_start_index(self):
        start_index = 164652
        query_job = Config.CLIENT.query(
            "SELECT word FROM `bigquery-public-data.samples.shakespeare`;",
            job_id_prefix="test_query_w_start_index_",
        )
        result1 = query_job.result(start_index=start_index)
        total_rows = result1.total_rows

        self.assertEqual(result1.extra_params["startIndex"], start_index)
        self.assertEqual(len(list(result1)), total_rows - start_index)

    def test_query_statistics(self):
        """
        A system test to exercise some of the extended query statistics.

        Note:  We construct a query that should need at least three stages by
        specifying a JOIN query.  Exact plan and stats are effectively
        non-deterministic, so we're largely interested in confirming values
        are present.
        """

        job_config = bigquery.QueryJobConfig()
        job_config.use_query_cache = False

        query_job = Config.CLIENT.query(
            """
            SELECT
              COUNT(1)
            FROM
            (
              SELECT
                year,
                wban_number
              FROM `bigquery-public-data.samples.gsod`
              LIMIT 1000
            ) lside
            INNER JOIN
            (
              SELECT
                year,
                state
              FROM `bigquery-public-data.samples.natality`
              LIMIT 1000
            ) rside
            ON
            lside.year = rside.year
            """,
            location="US",
            job_config=job_config,
        )

        # run the job to completion
        query_job.result()

        # Assert top-level stats
        self.assertFalse(query_job.cache_hit)
        self.assertIsNotNone(query_job.destination)
        self.assertTrue(query_job.done)
        self.assertFalse(query_job.dry_run)
        self.assertIsNone(query_job.num_dml_affected_rows)
        self.assertEqual(query_job.priority, "INTERACTIVE")
        self.assertGreater(query_job.total_bytes_billed, 1)
        self.assertGreater(query_job.total_bytes_processed, 1)
        self.assertEqual(query_job.statement_type, "SELECT")
        self.assertGreater(query_job.slot_millis, 1)

        # Make assertions on the shape of the query plan.
        plan = query_job.query_plan
        self.assertGreaterEqual(len(plan), 3)
        first_stage = plan[0]
        self.assertIsNotNone(first_stage.start)
        self.assertIsNotNone(first_stage.end)
        self.assertIsNotNone(first_stage.entry_id)
        self.assertIsNotNone(first_stage.name)
        self.assertGreater(first_stage.parallel_inputs, 0)
        self.assertGreater(first_stage.completed_parallel_inputs, 0)
        self.assertGreater(first_stage.shuffle_output_bytes, 0)
        self.assertEqual(first_stage.status, "COMPLETE")

        # Query plan is a digraph.  Ensure it has inter-stage links,
        # but not every stage has inputs.
        stages_with_inputs = 0
        for entry in plan:
            if len(entry.input_stages) > 0:
                stages_with_inputs = stages_with_inputs + 1
        self.assertGreater(stages_with_inputs, 0)
        self.assertGreater(len(plan), stages_with_inputs)

    def test_dml_statistics(self):
        table_schema = (
            bigquery.SchemaField("foo", "STRING"),
            bigquery.SchemaField("bar", "INTEGER"),
        )

        dataset_id = _make_dataset_id("bq_system_test")
        self.temp_dataset(dataset_id)
        table_id = "{}.{}.test_dml_statistics".format(Config.CLIENT.project, dataset_id)

        # Create the table before loading so that the column order is deterministic.
        table = helpers.retry_403(Config.CLIENT.create_table)(
            Table(table_id, schema=table_schema)
        )
        self.to_delete.insert(0, table)

        # Insert a few rows and check the stats.
        sql = f"""
            INSERT INTO `{table_id}`
            VALUES ("one", 1), ("two", 2), ("three", 3), ("four", 4);
        """
        query_job = Config.CLIENT.query(sql)
        query_job.result()

        assert query_job.dml_stats is not None
        assert query_job.dml_stats.inserted_row_count == 4
        assert query_job.dml_stats.updated_row_count == 0
        assert query_job.dml_stats.deleted_row_count == 0

        # Update some of the rows.
        sql = f"""
            UPDATE `{table_id}`
            SET bar = bar + 1
            WHERE bar > 2;
        """
        query_job = Config.CLIENT.query(sql)
        query_job.result()

        assert query_job.dml_stats is not None
        assert query_job.dml_stats.inserted_row_count == 0
        assert query_job.dml_stats.updated_row_count == 2
        assert query_job.dml_stats.deleted_row_count == 0

        # Now delete a few rows and check the stats.
        sql = f"""
            DELETE FROM `{table_id}`
            WHERE foo != "two";
        """
        query_job = Config.CLIENT.query(sql)
        query_job.result()

        assert query_job.dml_stats is not None
        assert query_job.dml_stats.inserted_row_count == 0
        assert query_job.dml_stats.updated_row_count == 0
        assert query_job.dml_stats.deleted_row_count == 3

    def test_dbapi_w_standard_sql_types(self):
        for sql, expected in helpers.STANDARD_SQL_EXAMPLES:
            Config.CURSOR.execute(sql)
            self.assertEqual(Config.CURSOR.rowcount, 1)
            row = Config.CURSOR.fetchone()
            self.assertEqual(len(row), 1)
            self.assertEqual(row[0], expected)
            row = Config.CURSOR.fetchone()
            self.assertIsNone(row)

    def test_dbapi_fetchall(self):
        query = "SELECT * FROM UNNEST([(1, 2), (3, 4), (5, 6)])"

        for arraysize in range(1, 5):
            Config.CURSOR.execute(query)
            self.assertEqual(Config.CURSOR.rowcount, 3, "expected 3 rows")
            Config.CURSOR.arraysize = arraysize
            rows = Config.CURSOR.fetchall()
            row_tuples = [r.values() for r in rows]
            self.assertEqual(row_tuples, [(1, 2), (3, 4), (5, 6)])

    def test_dbapi_fetchall_from_script(self):
        query = """
        CREATE TEMP TABLE Example
        (
          x INT64,
          y STRING
        );

        INSERT INTO Example
        VALUES (5, 'foo'),
        (6, 'bar'),
        (7, 'baz');

        SELECT *
        FROM Example
        ORDER BY x ASC;
        """

        Config.CURSOR.execute(query)
        self.assertEqual(Config.CURSOR.rowcount, 3, "expected 3 rows")
        rows = Config.CURSOR.fetchall()
        row_tuples = [r.values() for r in rows]
        self.assertEqual(row_tuples, [(5, "foo"), (6, "bar"), (7, "baz")])

    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_dbapi_fetch_w_bqstorage_client_large_result_set(self):
        bqstorage_client = bigquery_storage.BigQueryReadClient(
            credentials=Config.CLIENT._credentials
        )
        cursor = dbapi.connect(Config.CLIENT, bqstorage_client).cursor()

        cursor.execute(
            """
            SELECT id, `by`, time_ts
            FROM `bigquery-public-data.hacker_news.comments`
            ORDER BY `id` ASC
            LIMIT 100000
        """
        )

        result_rows = [cursor.fetchone(), cursor.fetchone(), cursor.fetchone()]

        field_name = operator.itemgetter(0)
        fetched_data = [sorted(row.items(), key=field_name) for row in result_rows]

        # Since DB API is not thread safe, only a single result stream should be
        # requested by the BQ storage client, meaning that results should arrive
        # in the sorted order.
        expected_data = [
            [
                ("by", "sama"),
                ("id", 15),
                ("time_ts", datetime.datetime(2006, 10, 9, 19, 51, 1, tzinfo=UTC)),
            ],
            [
                ("by", "pg"),
                ("id", 17),
                ("time_ts", datetime.datetime(2006, 10, 9, 19, 52, 45, tzinfo=UTC)),
            ],
            [
                ("by", "pg"),
                ("id", 22),
                ("time_ts", datetime.datetime(2006, 10, 10, 2, 18, 22, tzinfo=UTC)),
            ],
        ]
        self.assertEqual(fetched_data, expected_data)

    def test_dbapi_dry_run_query(self):
        from google.cloud.bigquery.job import QueryJobConfig

        query = """
            SELECT country_name
            FROM `bigquery-public-data.utility_us.country_code_iso`
            WHERE country_name LIKE 'U%'
        """

        Config.CURSOR.execute(query, job_config=QueryJobConfig(dry_run=True))
        self.assertEqual(Config.CURSOR.rowcount, 0, "expected no rows")

        rows = Config.CURSOR.fetchall()

        self.assertEqual(list(rows), [])

    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_dbapi_connection_does_not_leak_sockets(self):
        current_process = psutil.Process()
        conn_count_start = len(current_process.connections())

        # Provide no explicit clients, so that the connection will create and own them.
        connection = dbapi.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, `by`, time_ts
            FROM `bigquery-public-data.hacker_news.comments`
            ORDER BY `id` ASC
            LIMIT 100000
        """
        )
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 100000)

        connection.close()
        conn_count_end = len(current_process.connections())
        self.assertEqual(conn_count_end, conn_count_start)

    def _load_table_for_dml(self, rows, dataset_id, table_id):
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        dataset = self.temp_dataset(dataset_id)
        greeting = bigquery.SchemaField("greeting", "STRING", mode="NULLABLE")
        table_ref = dataset.table(table_id)
        table_arg = Table(table_ref, schema=[greeting])
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, "w") as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(("Greeting",))
                writer.writerows(rows)

            with open(temp.name, "rb") as csv_read:
                config = bigquery.LoadJobConfig()
                config.source_format = SourceFormat.CSV
                config.skip_leading_rows = 1
                config.create_disposition = CreateDisposition.CREATE_NEVER
                config.write_disposition = WriteDisposition.WRITE_EMPTY
                job = Config.CLIENT.load_table_from_file(
                    csv_read, table_ref, job_config=config
                )

        # Retry until done.
        job.result(timeout=JOB_TIMEOUT)
        self._fetch_single_page(table)

    def test_query_w_dml(self):
        dataset_name = _make_dataset_id("dml_query")
        table_name = "test_table"
        self._load_table_for_dml([("Hello World",)], dataset_name, table_name)
        query_template = """UPDATE {}.{}
            SET greeting = 'Guten Tag'
            WHERE greeting = 'Hello World'
            """

        query_job = Config.CLIENT.query(
            query_template.format(dataset_name, table_name),
            job_id_prefix="test_query_w_dml_",
        )
        query_job.result()

        self.assertEqual(query_job.num_dml_affected_rows, 1)

    def test_dbapi_w_dml(self):
        dataset_name = _make_dataset_id("dml_dbapi")
        table_name = "test_table"
        self._load_table_for_dml(
            [("こんにちは",), ("Hello World",), ("Howdy!",)], dataset_name, table_name
        )
        query_template = """UPDATE {}.{}
            SET greeting = 'Guten Tag'
            WHERE greeting = 'Hello World'
            """

        Config.CURSOR.execute(
            query_template.format(dataset_name, table_name),
            job_id="test_dbapi_w_dml_{}".format(str(uuid.uuid4())),
        )
        self.assertEqual(Config.CURSOR.rowcount, 1)

    def test_query_w_query_params(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ArrayQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameterType
        from google.cloud.bigquery.query import StructQueryParameter
        from google.cloud.bigquery.query import StructQueryParameterType

        question = "What is the answer to life, the universe, and everything?"
        question_param = ScalarQueryParameter(
            name="question", type_="STRING", value=question
        )
        answer = 42
        answer_param = ScalarQueryParameter(name="answer", type_="INT64", value=answer)
        pi = 3.1415926
        pi_param = ScalarQueryParameter(name="pi", type_="FLOAT64", value=pi)
        pi_numeric = decimal.Decimal("3.141592654")
        pi_numeric_param = ScalarQueryParameter(
            name="pi_numeric_param", type_="NUMERIC", value=pi_numeric
        )
        bignum = decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38))
        bignum_param = ScalarQueryParameter(
            name="bignum_param", type_="BIGNUMERIC", value=bignum
        )
        truthy = True
        truthy_param = ScalarQueryParameter(name="truthy", type_="BOOL", value=truthy)
        beef = b"DEADBEEF"
        beef_param = ScalarQueryParameter(name="beef", type_="BYTES", value=beef)
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        naive_param = ScalarQueryParameter(name="naive", type_="DATETIME", value=naive)
        naive_date_param = ScalarQueryParameter(
            name="naive_date", type_="DATE", value=naive.date()
        )
        naive_time_param = ScalarQueryParameter(
            name="naive_time", type_="TIME", value=naive.time()
        )
        zoned = naive.replace(tzinfo=UTC)
        zoned_param = ScalarQueryParameter(name="zoned", type_="TIMESTAMP", value=zoned)
        array_param = ArrayQueryParameter(
            name="array_param", array_type="INT64", values=[1, 2]
        )
        struct_param = StructQueryParameter("hitchhiker", question_param, answer_param)
        phred_name = "Phred Phlyntstone"
        phred_name_param = ScalarQueryParameter(
            name="name", type_="STRING", value=phred_name
        )
        phred_age = 32
        phred_age_param = ScalarQueryParameter(
            name="age", type_="INT64", value=phred_age
        )
        phred_param = StructQueryParameter(None, phred_name_param, phred_age_param)
        bharney_name = "Bharney Rhubbyl"
        bharney_name_param = ScalarQueryParameter(
            name="name", type_="STRING", value=bharney_name
        )
        bharney_age = 31
        bharney_age_param = ScalarQueryParameter(
            name="age", type_="INT64", value=bharney_age
        )
        bharney_param = StructQueryParameter(
            None, bharney_name_param, bharney_age_param
        )
        characters_param = ArrayQueryParameter(
            name=None, array_type="RECORD", values=[phred_param, bharney_param]
        )
        empty_struct_array_param = ArrayQueryParameter(
            name="empty_array_param",
            values=[],
            array_type=StructQueryParameterType(
                ScalarQueryParameterType(name="foo", type_="INT64"),
                ScalarQueryParameterType(name="bar", type_="STRING"),
            ),
        )
        hero_param = StructQueryParameter("hero", phred_name_param, phred_age_param)
        sidekick_param = StructQueryParameter(
            "sidekick", bharney_name_param, bharney_age_param
        )
        roles_param = StructQueryParameter("roles", hero_param, sidekick_param)
        friends_param = ArrayQueryParameter(
            name="friends", array_type="STRING", values=[phred_name, bharney_name]
        )
        with_friends_param = StructQueryParameter(None, friends_param)
        top_left_param = StructQueryParameter(
            "top_left",
            ScalarQueryParameter("x", "INT64", 12),
            ScalarQueryParameter("y", "INT64", 102),
        )
        bottom_right_param = StructQueryParameter(
            "bottom_right",
            ScalarQueryParameter("x", "INT64", 22),
            ScalarQueryParameter("y", "INT64", 92),
        )
        rectangle_param = StructQueryParameter(
            "rectangle", top_left_param, bottom_right_param
        )
        examples = [
            {
                "sql": "SELECT @question",
                "expected": question,
                "query_parameters": [question_param],
            },
            {
                "sql": "SELECT @answer",
                "expected": answer,
                "query_parameters": [answer_param],
            },
            {"sql": "SELECT @pi", "expected": pi, "query_parameters": [pi_param]},
            {
                "sql": "SELECT @pi_numeric_param",
                "expected": pi_numeric,
                "query_parameters": [pi_numeric_param],
            },
            {
                "sql": "SELECT @truthy",
                "expected": truthy,
                "query_parameters": [truthy_param],
            },
            {"sql": "SELECT @beef", "expected": beef, "query_parameters": [beef_param]},
            {
                "sql": "SELECT @naive",
                "expected": naive,
                "query_parameters": [naive_param],
            },
            {
                "sql": "SELECT @naive_date",
                "expected": naive.date(),
                "query_parameters": [naive_date_param],
            },
            {
                "sql": "SELECT @naive_time",
                "expected": naive.time(),
                "query_parameters": [naive_time_param],
            },
            {
                "sql": "SELECT @zoned",
                "expected": zoned,
                "query_parameters": [zoned_param],
            },
            {
                "sql": "SELECT @array_param",
                "expected": [1, 2],
                "query_parameters": [array_param],
            },
            {
                "sql": "SELECT (@hitchhiker.question, @hitchhiker.answer)",
                "expected": ({"_field_1": question, "_field_2": answer}),
                "query_parameters": [struct_param],
            },
            {
                "sql": "SELECT "
                "((@rectangle.bottom_right.x - @rectangle.top_left.x) "
                "* (@rectangle.top_left.y - @rectangle.bottom_right.y))",
                "expected": 100,
                "query_parameters": [rectangle_param],
            },
            {
                "sql": "SELECT ?",
                "expected": [
                    {"name": phred_name, "age": phred_age},
                    {"name": bharney_name, "age": bharney_age},
                ],
                "query_parameters": [characters_param],
            },
            {
                "sql": "SELECT @empty_array_param",
                "expected": [],
                "query_parameters": [empty_struct_array_param],
            },
            {
                "sql": "SELECT @roles",
                "expected": {
                    "hero": {"name": phred_name, "age": phred_age},
                    "sidekick": {"name": bharney_name, "age": bharney_age},
                },
                "query_parameters": [roles_param],
            },
            {
                "sql": "SELECT ?",
                "expected": {"friends": [phred_name, bharney_name]},
                "query_parameters": [with_friends_param],
            },
        ]
        if _BIGNUMERIC_SUPPORT:
            examples.append(
                {
                    "sql": "SELECT @bignum_param",
                    "expected": bignum,
                    "query_parameters": [bignum_param],
                }
            )

        for example in examples:
            jconfig = QueryJobConfig()
            jconfig.query_parameters = example["query_parameters"]
            query_job = Config.CLIENT.query(
                example["sql"],
                job_config=jconfig,
                job_id_prefix="test_query_w_query_params",
            )
            rows = list(query_job.result())
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example["expected"])

    def test_dbapi_w_query_parameters(self):
        examples = [
            {
                "sql": "SELECT %(boolval)s",
                "expected": True,
                "query_parameters": {"boolval": True},
            },
            {
                "sql": 'SELECT %(a "very" weird `name`)s',
                "expected": True,
                "query_parameters": {'a "very" weird `name`': True},
            },
            {
                "sql": "SELECT %(select)s",
                "expected": True,
                "query_parameters": {"select": True},  # this name is a keyword
            },
            {"sql": "SELECT %s", "expected": False, "query_parameters": [False]},
            {
                "sql": "SELECT %(intval)s",
                "expected": 123,
                "query_parameters": {"intval": 123},
            },
            {
                "sql": "SELECT %s",
                "expected": -123456789,
                "query_parameters": [-123456789],
            },
            {
                "sql": "SELECT %(floatval)s",
                "expected": 1.25,
                "query_parameters": {"floatval": 1.25},
            },
            {
                "sql": "SELECT LOWER(%(strval)s)",
                "query_parameters": {"strval": "I Am A String"},
                "expected": "i am a string",
            },
            {
                "sql": "SELECT DATE_SUB(%(dateval)s, INTERVAL 1 DAY)",
                "query_parameters": {"dateval": datetime.date(2017, 4, 2)},
                "expected": datetime.date(2017, 4, 1),
            },
            {
                "sql": "SELECT TIME_ADD(%(timeval)s, INTERVAL 4 SECOND)",
                "query_parameters": {"timeval": datetime.time(12, 34, 56)},
                "expected": datetime.time(12, 35, 0),
            },
            {
                "sql": ("SELECT DATETIME_ADD(%(datetimeval)s, INTERVAL 53 SECOND)"),
                "query_parameters": {
                    "datetimeval": datetime.datetime(2012, 3, 4, 5, 6, 7)
                },
                "expected": datetime.datetime(2012, 3, 4, 5, 7, 0),
            },
            {
                "sql": "SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)",
                "query_parameters": {
                    "zoned": datetime.datetime(2012, 3, 4, 5, 6, 7, tzinfo=UTC)
                },
                "expected": datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            },
            {
                "sql": "SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)",
                "query_parameters": {
                    "zoned": datetime.datetime(2012, 3, 4, 5, 6, 7, 250000, tzinfo=UTC)
                },
                "expected": datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            },
        ]
        for example in examples:
            msg = "sql: {} query_parameters: {}".format(
                example["sql"], example["query_parameters"]
            )

            Config.CURSOR.execute(example["sql"], example["query_parameters"])

            self.assertEqual(Config.CURSOR.rowcount, 1, msg=msg)
            row = Config.CURSOR.fetchone()
            self.assertEqual(len(row), 1, msg=msg)
            self.assertEqual(row[0], example["expected"], msg=msg)
            row = Config.CURSOR.fetchone()
            self.assertIsNone(row, msg=msg)

    def test_large_query_w_public_data(self):
        PUBLIC = "bigquery-public-data"
        DATASET_ID = "samples"
        TABLE_NAME = "natality"
        LIMIT = 1000
        SQL = "SELECT * from `{}.{}.{}` LIMIT {}".format(
            PUBLIC, DATASET_ID, TABLE_NAME, LIMIT
        )

        query_job = Config.CLIENT.query(SQL)

        rows = list(query_job)
        self.assertEqual(len(rows), LIMIT)

    def test_query_future(self):
        query_job = Config.CLIENT.query("SELECT 1")
        iterator = query_job.result(timeout=JOB_TIMEOUT)
        row_tuples = [r.values() for r in iterator]
        self.assertEqual(row_tuples, [(1,)])

    def test_query_iter(self):
        import types

        query_job = Config.CLIENT.query("SELECT 1")
        self.assertIsInstance(iter(query_job), types.GeneratorType)
        row_tuples = [r.values() for r in query_job]
        self.assertEqual(row_tuples, [(1,)])

    def test_insert_rows_nested_nested(self):
        # See #2951
        SF = bigquery.SchemaField
        schema = [
            SF("string_col", "STRING", mode="NULLABLE"),
            SF(
                "record_col",
                "RECORD",
                mode="NULLABLE",
                fields=[
                    SF("nested_string", "STRING", mode="NULLABLE"),
                    SF("nested_repeated", "INTEGER", mode="REPEATED"),
                    SF(
                        "nested_record",
                        "RECORD",
                        mode="NULLABLE",
                        fields=[SF("nested_nested_string", "STRING", mode="NULLABLE")],
                    ),
                ],
            ),
        ]
        record = {
            "nested_string": "another string value",
            "nested_repeated": [0, 1, 2],
            "nested_record": {"nested_nested_string": "some deep insight"},
        }
        to_insert = [("Some value", record)]
        table_id = "test_table"
        dataset = self.temp_dataset(_make_dataset_id("issue_2951"))
        table_arg = Table(dataset.table(table_id), schema=schema)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        Config.CLIENT.insert_rows(table, to_insert)

        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)
        row_tuples = [r.values() for r in rows]
        self.assertEqual(row_tuples, to_insert)

    def test_insert_rows_nested_nested_dictionary(self):
        # See #2951
        SF = bigquery.SchemaField
        schema = [
            SF("string_col", "STRING", mode="NULLABLE"),
            SF(
                "record_col",
                "RECORD",
                mode="NULLABLE",
                fields=[
                    SF("nested_string", "STRING", mode="NULLABLE"),
                    SF("nested_repeated", "INTEGER", mode="REPEATED"),
                    SF(
                        "nested_record",
                        "RECORD",
                        mode="NULLABLE",
                        fields=[SF("nested_nested_string", "STRING", mode="NULLABLE")],
                    ),
                ],
            ),
        ]
        record = {
            "nested_string": "another string value",
            "nested_repeated": [0, 1, 2],
            "nested_record": {"nested_nested_string": "some deep insight"},
        }
        to_insert = [{"string_col": "Some value", "record_col": record}]
        table_id = "test_table"
        dataset = self.temp_dataset(_make_dataset_id("issue_2951"))
        table_arg = Table(dataset.table(table_id), schema=schema)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        Config.CLIENT.insert_rows(table, to_insert)

        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)
        row_tuples = [r.values() for r in rows]
        expected_rows = [("Some value", record)]
        self.assertEqual(row_tuples, expected_rows)

    @pytest.mark.skipif(
        MTLS_TESTING, reason="mTLS testing has no permission to the max-value.js file"
    )
    def test_create_routine(self):
        routine_name = "test_routine"
        dataset = self.temp_dataset(_make_dataset_id("create_routine"))
        float64_type = bigquery_v2.types.StandardSqlDataType(
            type_kind=bigquery_v2.types.StandardSqlDataType.TypeKind.FLOAT64
        )
        routine = bigquery.Routine(
            dataset.routine(routine_name),
            language="JAVASCRIPT",
            type_="SCALAR_FUNCTION",
            return_type=float64_type,
            imported_libraries=[
                "gs://{}/bigquery/udfs/max-value.js".format(SAMPLES_BUCKET)
            ],
        )
        routine.arguments = [
            bigquery.RoutineArgument(
                name="arr",
                data_type=bigquery_v2.types.StandardSqlDataType(
                    type_kind=bigquery_v2.types.StandardSqlDataType.TypeKind.ARRAY,
                    array_element_type=float64_type,
                ),
            )
        ]
        routine.body = "return maxValue(arr)"
        routine.determinism_level = bigquery.DeterminismLevel.DETERMINISTIC
        query_string = "SELECT `{}`([-100.0, 3.14, 100.0, 42.0]) as max_value;".format(
            str(routine.reference)
        )

        routine = helpers.retry_403(Config.CLIENT.create_routine)(routine)
        query_job = helpers.retry_403(Config.CLIENT.query)(query_string)
        rows = list(query_job.result())

        assert len(rows) == 1
        assert rows[0].max_value == 100.0

    def test_create_tvf_routine(self):
        from google.cloud.bigquery import Routine, RoutineArgument, RoutineType

        StandardSqlDataType = bigquery_v2.types.StandardSqlDataType
        StandardSqlField = bigquery_v2.types.StandardSqlField
        StandardSqlTableType = bigquery_v2.types.StandardSqlTableType

        INT64 = StandardSqlDataType.TypeKind.INT64
        STRING = StandardSqlDataType.TypeKind.STRING

        client = Config.CLIENT

        dataset = self.temp_dataset(_make_dataset_id("create_tvf_routine"))
        routine_ref = dataset.routine("test_tvf_routine")

        routine_body = """
            SELECT int_col, str_col
            FROM (
                UNNEST([1, 2, 3]) int_col
                JOIN
                (SELECT str_col FROM UNNEST(["one", "two", "three"]) str_col)
                ON TRUE
            )
            WHERE int_col > threshold
            """

        return_table_type = StandardSqlTableType(
            columns=[
                StandardSqlField(
                    name="int_col", type=StandardSqlDataType(type_kind=INT64),
                ),
                StandardSqlField(
                    name="str_col", type=StandardSqlDataType(type_kind=STRING),
                ),
            ]
        )

        routine_args = [
            RoutineArgument(
                name="threshold", data_type=StandardSqlDataType(type_kind=INT64),
            )
        ]

        routine_def = Routine(
            routine_ref,
            type_=RoutineType.TABLE_VALUED_FUNCTION,
            arguments=routine_args,
            return_table_type=return_table_type,
            body=routine_body,
        )

        # Create TVF routine.
        client.delete_routine(routine_ref, not_found_ok=True)
        routine = client.create_routine(routine_def)

        assert routine.body == routine_body
        assert routine.return_table_type == return_table_type
        assert routine.arguments == routine_args

        # Execute the routine to see if it's working as expected.
        query_job = client.query(
            f"""
            SELECT int_col, str_col
            FROM `{routine.reference}`(1)
            ORDER BY int_col, str_col ASC
            """
        )

        result_rows = [tuple(row) for row in query_job.result()]
        expected = [
            (2, "one"),
            (2, "three"),
            (2, "two"),
            (3, "one"),
            (3, "three"),
            (3, "two"),
        ]
        assert result_rows == expected

    def test_create_table_rows_fetch_nested_schema(self):
        table_name = "test_table"
        dataset = self.temp_dataset(_make_dataset_id("create_table_nested_schema"))
        schema = _load_json_schema()
        table_arg = Table(dataset.table(table_name), schema=schema)
        table = helpers.retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_name)

        to_insert = []
        # Data is in "JSON Lines" format, see http://jsonlines.org/
        json_filename = DATA_PATH / "characters.jsonl"
        with open(json_filename) as rows_file:
            for line in rows_file:
                to_insert.append(json.loads(line))

        errors = Config.CLIENT.insert_rows_json(table, to_insert)
        self.assertEqual(len(errors), 0)

        retry = RetryResult(_has_rows, max_tries=8)
        fetched = retry(self._fetch_single_page)(table)
        fetched_tuples = [f.values() for f in fetched]

        self.assertEqual(len(fetched), len(to_insert))

        for found, expected in zip(sorted(fetched_tuples), to_insert):
            self.assertEqual(found[0], expected["Name"])
            self.assertEqual(found[1], int(expected["Age"]))
            self.assertEqual(found[2], expected["Weight"])
            self.assertEqual(found[3], expected["IsMagic"])

            self.assertEqual(len(found[4]), len(expected["Spells"]))
            for f_spell, e_spell in zip(found[4], expected["Spells"]):
                self.assertEqual(f_spell["Name"], e_spell["Name"])
                parts = time.strptime(e_spell["LastUsed"], "%Y-%m-%d %H:%M:%S UTC")
                e_used = datetime.datetime(*parts[0:6], tzinfo=UTC)
                self.assertEqual(f_spell["LastUsed"], e_used)
                self.assertEqual(f_spell["DiscoveredBy"], e_spell["DiscoveredBy"])
                self.assertEqual(f_spell["Properties"], e_spell["Properties"])

                e_icon = base64.standard_b64decode(e_spell["Icon"].encode("ascii"))
                self.assertEqual(f_spell["Icon"], e_icon)

            parts = time.strptime(expected["TeaTime"], "%H:%M:%S")
            e_teatime = datetime.time(*parts[3:6])
            self.assertEqual(found[5], e_teatime)

            parts = time.strptime(expected["NextVacation"], "%Y-%m-%d")
            e_nextvac = datetime.date(*parts[0:3])
            self.assertEqual(found[6], e_nextvac)

            parts = time.strptime(expected["FavoriteTime"], "%Y-%m-%dT%H:%M:%S")
            e_favtime = datetime.datetime(*parts[0:6])
            self.assertEqual(found[7], e_favtime)
            self.assertEqual(found[8], decimal.Decimal(expected["FavoriteNumber"]))

    def _fetch_dataframe(self, query):
        return Config.CLIENT.query(query).result().to_dataframe()

    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_nested_table_to_arrow(self):
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        SF = bigquery.SchemaField
        schema = [
            SF("string_col", "STRING", mode="NULLABLE"),
            SF(
                "record_col",
                "RECORD",
                mode="NULLABLE",
                fields=[
                    SF("nested_string", "STRING", mode="NULLABLE"),
                    SF("nested_repeated", "INTEGER", mode="REPEATED"),
                ],
            ),
            SF("float_col", "FLOAT", mode="NULLABLE"),
        ]
        record = {"nested_string": "another string value", "nested_repeated": [0, 1, 2]}
        to_insert = [
            {"string_col": "Some value", "record_col": record, "float_col": 3.14}
        ]
        rows = [json.dumps(row) for row in to_insert]
        body = io.BytesIO("{}\n".format("\n".join(rows)).encode("ascii"))
        table_id = "test_table"
        dataset = self.temp_dataset(_make_dataset_id("nested_df"))
        table = dataset.table(table_id)
        self.to_delete.insert(0, table)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = schema
        # Load a table using a local JSON file from memory.
        Config.CLIENT.load_table_from_file(body, table, job_config=job_config).result()
        bqstorage_client = bigquery_storage.BigQueryReadClient(
            credentials=Config.CLIENT._credentials
        )

        tbl = Config.CLIENT.list_rows(table, selected_fields=schema).to_arrow(
            bqstorage_client=bqstorage_client
        )

        self.assertIsInstance(tbl, pyarrow.Table)
        self.assertEqual(tbl.num_rows, 1)
        self.assertEqual(tbl.num_columns, 3)
        # Columns may not appear in the requested order.
        self.assertTrue(pyarrow.types.is_float64(tbl.schema.field("float_col").type))
        self.assertTrue(pyarrow.types.is_string(tbl.schema.field("string_col").type))
        record_col = tbl.schema.field("record_col").type
        self.assertTrue(pyarrow.types.is_struct(record_col))
        self.assertEqual(record_col.num_fields, 2)
        self.assertEqual(record_col[0].name, "nested_string")
        self.assertTrue(pyarrow.types.is_string(record_col[0].type))
        self.assertEqual(record_col[1].name, "nested_repeated")
        self.assertTrue(pyarrow.types.is_list(record_col[1].type))
        self.assertTrue(pyarrow.types.is_int64(record_col[1].type.value_type))

    def test_list_rows_empty_table(self):
        from google.cloud.bigquery.table import RowIterator

        dataset_id = _make_dataset_id("empty_table")
        dataset = self.temp_dataset(dataset_id)
        table_ref = dataset.table("empty_table")
        table = Config.CLIENT.create_table(bigquery.Table(table_ref))

        # It's a bit silly to list rows for an empty table, but this does
        # happen as the result of a DDL query from an IPython magic command.
        rows = Config.CLIENT.list_rows(table)
        self.assertIsInstance(rows, RowIterator)
        self.assertEqual(tuple(rows), ())

    def test_list_rows_page_size(self):
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        num_items = 7
        page_size = 3
        num_pages, num_last_page = divmod(num_items, page_size)

        SF = bigquery.SchemaField
        schema = [SF("string_col", "STRING", mode="NULLABLE")]
        to_insert = [{"string_col": "item%d" % i} for i in range(num_items)]
        rows = [json.dumps(row) for row in to_insert]
        body = io.BytesIO("{}\n".format("\n".join(rows)).encode("ascii"))

        table_id = "test_table"
        dataset = self.temp_dataset(_make_dataset_id("nested_df"))
        table = dataset.table(table_id)
        self.to_delete.insert(0, table)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = schema
        # Load a table using a local JSON file from memory.
        Config.CLIENT.load_table_from_file(body, table, job_config=job_config).result()

        df = Config.CLIENT.list_rows(table, selected_fields=schema, page_size=page_size)
        pages = df.pages

        for i in range(num_pages):
            page = next(pages)
            self.assertEqual(page.num_items, page_size)
        page = next(pages)
        self.assertEqual(page.num_items, num_last_page)

    def temp_dataset(self, dataset_id, location=None):
        project = Config.CLIENT.project
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        dataset = Dataset(dataset_ref)
        if location:
            dataset.location = location
        dataset = helpers.retry_403(Config.CLIENT.create_dataset)(dataset)
        self.to_delete.append(dataset)
        return dataset


def _job_done(instance):
    return instance.state.lower() == "done"


def _dataset_exists(ds):
    try:
        Config.CLIENT.get_dataset(DatasetReference(ds.project, ds.dataset_id))
        return True
    except NotFound:
        return False


def _table_exists(t):
    try:
        tr = DatasetReference(t.project, t.dataset_id).table(t.table_id)
        Config.CLIENT.get_table(tr)
        return True
    except NotFound:
        return False


def test_dbapi_create_view(dataset_id):

    query = f"""
    CREATE VIEW {dataset_id}.dbapi_create_view
    AS SELECT name, SUM(number) AS total
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    GROUP BY name;
    """

    Config.CURSOR.execute(query)
    assert Config.CURSOR.rowcount == 0, "expected 0 rows"


def test_parameterized_types_round_trip(dataset_id):
    client = Config.CLIENT
    table_id = f"{dataset_id}.test_parameterized_types_round_trip"
    fields = (
        ("n", "NUMERIC"),
        ("n9", "NUMERIC(9)"),
        ("n92", "NUMERIC(9, 2)"),
        ("bn", "BIGNUMERIC"),
        ("bn9", "BIGNUMERIC(38)"),
        ("bn92", "BIGNUMERIC(38, 22)"),
        ("s", "STRING"),
        ("s9", "STRING(9)"),
        ("b", "BYTES"),
        ("b9", "BYTES(9)"),
    )
    client.query(
        "create table {} ({})".format(table_id, ", ".join(" ".join(f) for f in fields))
    ).result()
    table = client.get_table(table_id)
    table_id2 = table_id + "2"
    client.create_table(Table(f"{client.project}.{table_id2}", table.schema))
    table2 = client.get_table(table_id2)

    assert tuple(s._key()[:2] for s in table2.schema) == fields


def test_table_snapshots(dataset_id):
    from google.cloud.bigquery import CopyJobConfig
    from google.cloud.bigquery import OperationType

    client = Config.CLIENT

    source_table_path = f"{client.project}.{dataset_id}.test_table"
    snapshot_table_path = f"{source_table_path}_snapshot"

    # Create the table before loading so that the column order is predictable.
    schema = [
        bigquery.SchemaField("foo", "INTEGER"),
        bigquery.SchemaField("bar", "STRING"),
    ]
    source_table = helpers.retry_403(Config.CLIENT.create_table)(
        Table(source_table_path, schema=schema)
    )

    # Populate the table with initial data.
    rows = [{"foo": 1, "bar": "one"}, {"foo": 2, "bar": "two"}]
    load_job = Config.CLIENT.load_table_from_json(rows, source_table)
    load_job.result()

    # Now create a snapshot before modifying the original table data.
    copy_config = CopyJobConfig()
    copy_config.operation_type = OperationType.SNAPSHOT

    copy_job = client.copy_table(
        sources=source_table_path,
        destination=snapshot_table_path,
        job_config=copy_config,
    )
    copy_job.result()

    # Modify data in original table.
    sql = f'INSERT INTO `{source_table_path}`(foo, bar) VALUES (3, "three")'
    query_job = client.query(sql)
    query_job.result()

    # List rows from the source table and compare them to rows from the snapshot.
    rows_iter = client.list_rows(source_table_path)
    rows = sorted(row.values() for row in rows_iter)
    assert rows == [(1, "one"), (2, "two"), (3, "three")]

    rows_iter = client.list_rows(snapshot_table_path)
    rows = sorted(row.values() for row in rows_iter)
    assert rows == [(1, "one"), (2, "two")]

    # Now restore the table from the snapshot and it should again contain the old
    # set of rows.
    copy_config = CopyJobConfig()
    copy_config.operation_type = OperationType.RESTORE
    copy_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    copy_job = client.copy_table(
        sources=snapshot_table_path,
        destination=source_table_path,
        job_config=copy_config,
    )
    copy_job.result()

    rows_iter = client.list_rows(source_table_path)
    rows = sorted(row.values() for row in rows_iter)
    assert rows == [(1, "one"), (2, "two")]
