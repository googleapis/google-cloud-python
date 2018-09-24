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
import json
import operator
import os
import time
import unittest
import uuid
import re

import six
import pytest
try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import IPython
    from IPython.utils import io
    from IPython.testing import tools
    from IPython.terminal import interactiveshell
except ImportError:  # pragma: NO COVER
    IPython = None

from google.api_core.exceptions import PreconditionFailed
from google.cloud import bigquery
from google.cloud.bigquery.dataset import Dataset, DatasetReference
from google.cloud.bigquery.table import Table
from google.cloud._helpers import UTC
from google.cloud.bigquery import dbapi
from google.cloud.exceptions import BadRequest, Forbidden, NotFound
from google.cloud import storage

from test_utils.retry import RetryErrors
from test_utils.retry import RetryInstanceState
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


JOB_TIMEOUT = 120  # 2 minutes
WHERE = os.path.abspath(os.path.dirname(__file__))

# Common table data used for many tests.
ROWS = [
    ('Phred Phlyntstone', 32),
    ('Bharney Rhubble', 33),
    ('Wylma Phlyntstone', 29),
    ('Bhettye Rhubble', 27),
]
HEADER_ROW = ('Full Name', 'Age')
SCHEMA = [
    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
]
TIME_PARTITIONING_CLUSTERING_FIELDS_SCHEMA = [
    bigquery.SchemaField('transaction_time', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('transaction_id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('user_email', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('store_code', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField(
        'items', 'RECORD', mode='REPEATED', fields=[
            bigquery.SchemaField('item_code', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('quantity', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('comments', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('expiration_date', 'DATE', mode='REQUIRED'),
        ]),
]


def _has_rows(result):
    return len(result) > 0


def _make_dataset_id(prefix):
    return '%s%s' % (prefix, unique_resource_id())


def _load_json_schema(filename='data/schema.json'):
    from google.cloud.bigquery.table import _parse_schema_resource

    json_filename = os.path.join(WHERE, filename)

    with open(json_filename, 'r') as schema_file:
        return _parse_schema_resource(json.load(schema_file))


def _rate_limit_exceeded(forbidden):
    """Predicate: pass only exceptions with 'rateLimitExceeded' as reason."""
    return any(error['reason'] == 'rateLimitExceeded'
               for error in forbidden._errors)


# We need to wait to stay within the rate limits.
# The alternative outcome is a 403 Forbidden response from upstream, which
# they return instead of the more appropriate 429.
# See https://cloud.google.com/bigquery/quota-policy
retry_403 = RetryErrors(Forbidden, error_predicate=_rate_limit_exceeded)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    CURSOR = None


def setUpModule():
    Config.CLIENT = bigquery.Client()
    Config.CURSOR = dbapi.connect(Config.CLIENT).cursor()


class TestBigQuery(unittest.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        from google.cloud.storage import Bucket
        from google.cloud.exceptions import BadRequest
        from google.cloud.exceptions import Conflict

        def _still_in_use(bad_request):
            return any(error['reason'] == 'resourceInUse'
                       for error in bad_request._errors)

        retry_in_use = RetryErrors(BadRequest, error_predicate=_still_in_use)
        retry_409 = RetryErrors(Conflict)
        for doomed in self.to_delete:
            if isinstance(doomed, Bucket):
                retry_409(doomed.delete)(force=True)
            elif isinstance(doomed, (Dataset, bigquery.DatasetReference)):
                retry_in_use(Config.CLIENT.delete_dataset)(
                    doomed, delete_contents=True)
            elif isinstance(doomed, (Table, bigquery.TableReference)):
                retry_in_use(Config.CLIENT.delete_table)(doomed)
            else:
                doomed.delete()

    def test_get_service_account_email(self):
        client = Config.CLIENT

        got = client.get_service_account_email()

        self.assertIsInstance(got, six.text_type)
        self.assertIn('@', got)

    def test_create_dataset(self):
        DATASET_ID = _make_dataset_id('create_dataset')
        dataset = self.temp_dataset(DATASET_ID)

        self.assertTrue(_dataset_exists(dataset))
        self.assertEqual(dataset.dataset_id, DATASET_ID)
        self.assertEqual(dataset.project, Config.CLIENT.project)

    def test_get_dataset(self):
        DATASET_ID = _make_dataset_id('get_dataset')
        client = Config.CLIENT
        dataset_arg = Dataset(client.dataset(DATASET_ID))
        dataset_arg.friendly_name = 'Friendly'
        dataset_arg.description = 'Description'
        dataset = retry_403(client.create_dataset)(dataset_arg)
        self.to_delete.append(dataset)
        dataset_ref = client.dataset(DATASET_ID)

        got = client.get_dataset(dataset_ref)

        self.assertEqual(got.friendly_name, 'Friendly')
        self.assertEqual(got.description, 'Description')

    def test_update_dataset(self):
        dataset = self.temp_dataset(_make_dataset_id('update_dataset'))
        self.assertTrue(_dataset_exists(dataset))
        self.assertIsNone(dataset.friendly_name)
        self.assertIsNone(dataset.description)
        self.assertEquals(dataset.labels, {})

        dataset.friendly_name = 'Friendly'
        dataset.description = 'Description'
        dataset.labels = {'priority': 'high', 'color': 'blue'}
        ds2 = Config.CLIENT.update_dataset(
            dataset,
            ('friendly_name', 'description', 'labels'))
        self.assertEqual(ds2.friendly_name, 'Friendly')
        self.assertEqual(ds2.description, 'Description')
        self.assertEqual(ds2.labels, {'priority': 'high', 'color': 'blue'})

        ds2.labels = {
            'color': 'green',   # change
            'shape': 'circle',  # add
            'priority': None,   # delete
        }
        ds3 = Config.CLIENT.update_dataset(ds2, ['labels'])
        self.assertEqual(ds3.labels, {'color': 'green', 'shape': 'circle'})

        # If we try to update using d2 again, it will fail because the
        # previous update changed the ETag.
        ds2.description = 'no good'
        with self.assertRaises(PreconditionFailed):
            Config.CLIENT.update_dataset(ds2, ['description'])

    def test_list_datasets(self):
        datasets_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        for dataset_id in datasets_to_create:
            self.temp_dataset(dataset_id)

        # Retrieve the datasets.
        iterator = Config.CLIENT.list_datasets()
        all_datasets = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [dataset for dataset in all_datasets
                   if dataset.dataset_id in datasets_to_create and
                   dataset.project == Config.CLIENT.project]
        self.assertEqual(len(created), len(datasets_to_create))

    def test_list_datasets_w_project(self):
        # Retrieve datasets from a different project.
        iterator = Config.CLIENT.list_datasets(project='bigquery-public-data')
        all_datasets = frozenset([dataset.dataset_id for dataset in iterator])
        self.assertIn('usa_names', all_datasets)

    def test_create_table(self):
        dataset = self.temp_dataset(_make_dataset_id('create_table'))
        table_id = 'test_table'
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))

        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_id)

    def test_create_table_w_time_partitioning_w_clustering_fields(self):
        from google.cloud.bigquery.table import TimePartitioning
        from google.cloud.bigquery.table import TimePartitioningType

        dataset = self.temp_dataset(_make_dataset_id('create_table_tp_cf'))
        table_id = 'test_table'
        table_arg = Table(
            dataset.table(table_id),
            schema=TIME_PARTITIONING_CLUSTERING_FIELDS_SCHEMA)
        self.assertFalse(_table_exists(table_arg))

        table_arg.time_partitioning = TimePartitioning(
            field='transaction_time')

        table_arg.clustering_fields = ['user_email', 'store_code']
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_id)
        time_partitioning = table.time_partitioning
        self.assertEqual(time_partitioning.type_, TimePartitioningType.DAY)
        self.assertEqual(time_partitioning.field, 'transaction_time')
        self.assertEqual(table.clustering_fields, ['user_email', 'store_code'])

    def test_delete_dataset_delete_contents_true(self):
        dataset_id = _make_dataset_id('delete_table_true')
        dataset = retry_403(Config.CLIENT.create_dataset)(
            Dataset(Config.CLIENT.dataset(dataset_id)))

        table_id = 'test_table'
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        Config.CLIENT.delete_dataset(dataset, delete_contents=True)

        self.assertFalse(_table_exists(table))

    def test_delete_dataset_delete_contents_false(self):
        from google.api_core import exceptions
        dataset_id = _make_dataset_id('delete_table_false')
        dataset = retry_403(Config.CLIENT.create_dataset)(
            Dataset(Config.CLIENT.dataset(dataset_id)))

        table_id = 'test_table'
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)

        retry_403(Config.CLIENT.create_table)(table_arg)
        with self.assertRaises(exceptions.BadRequest):
            Config.CLIENT.delete_dataset(dataset)

    def test_get_table_w_public_dataset(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_ID = 'samples'
        TABLE_ID = 'shakespeare'
        table_ref = DatasetReference(PUBLIC, DATASET_ID).table(TABLE_ID)

        table = Config.CLIENT.get_table(table_ref)

        self.assertEqual(table.table_id, TABLE_ID)
        self.assertEqual(table.dataset_id, DATASET_ID)
        self.assertEqual(table.project, PUBLIC)
        schema_names = [field.name for field in table.schema]
        self.assertEqual(
            schema_names, ['word', 'word_count', 'corpus', 'corpus_date'])

    def test_list_partitions(self):
        table_ref = DatasetReference(
            'bigquery-public-data',
            'ethereum_blockchain').table('blocks')
        all_rows = Config.CLIENT.list_partitions(table_ref)
        self.assertIn('20180801', all_rows)
        self.assertGreater(len(all_rows), 1000)

    def test_list_tables(self):
        DATASET_ID = _make_dataset_id('list_tables')
        dataset = self.temp_dataset(DATASET_ID)
        # Retrieve tables before any are created for the dataset.
        iterator = Config.CLIENT.list_tables(dataset)
        all_tables = list(iterator)
        self.assertEqual(all_tables, [])
        self.assertIsNone(iterator.next_page_token)

        # Insert some tables to be listed.
        tables_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        for table_name in tables_to_create:
            table = Table(dataset.table(table_name), schema=SCHEMA)
            created_table = retry_403(Config.CLIENT.create_table)(table)
            self.to_delete.insert(0, created_table)

        # Retrieve the tables.
        iterator = Config.CLIENT.list_tables(dataset)
        all_tables = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [table for table in all_tables
                   if (table.table_id in tables_to_create and
                       table.dataset_id == DATASET_ID)]
        self.assertEqual(len(created), len(tables_to_create))

    def test_update_table(self):
        dataset = self.temp_dataset(_make_dataset_id('update_table'))

        TABLE_NAME = 'test_table'
        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.description)
        self.assertEquals(table.labels, {})
        table.friendly_name = 'Friendly'
        table.description = 'Description'
        table.labels = {'priority': 'high', 'color': 'blue'}

        table2 = Config.CLIENT.update_table(
            table, ['friendly_name', 'description', 'labels'])

        self.assertEqual(table2.friendly_name, 'Friendly')
        self.assertEqual(table2.description, 'Description')
        self.assertEqual(table2.labels, {'priority': 'high', 'color': 'blue'})

        table2.description = None
        table2.labels = {
            'color': 'green',   # change
            'shape': 'circle',  # add
            'priority': None,   # delete
        }
        table3 = Config.CLIENT.update_table(table2, ['description', 'labels'])
        self.assertIsNone(table3.description)
        self.assertEqual(table3.labels, {'color': 'green', 'shape': 'circle'})

        # If we try to update using table2 again, it will fail because the
        # previous update changed the ETag.
        table2.description = 'no good'
        with self.assertRaises(PreconditionFailed):
            Config.CLIENT.update_table(table2, ['description'])

    def test_update_table_schema(self):
        dataset = self.temp_dataset(_make_dataset_id('update_table'))

        TABLE_NAME = 'test_table'
        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        voter = bigquery.SchemaField('voter', 'BOOLEAN', mode='NULLABLE')
        schema = table.schema
        schema.append(voter)
        table.schema = schema

        updated_table = Config.CLIENT.update_table(table, ['schema'])

        self.assertEqual(len(updated_table.schema), len(schema))
        for found, expected in zip(updated_table.schema, schema):
            self.assertEqual(found.name, expected.name)
            self.assertEqual(found.field_type, expected.field_type)
            self.assertEqual(found.mode, expected.mode)

    @staticmethod
    def _fetch_single_page(table, selected_fields=None):
        iterator = Config.CLIENT.list_rows(
            table, selected_fields=selected_fields)
        page = six.next(iterator.pages)
        return list(page)

    def _create_table_many_columns(self, rowcount):
        # Generate a table of maximum width via CREATE TABLE AS SELECT.
        # first column is named 'rowval', and has a value from 1..rowcount
        # Subsequent column is named col_<N> and contains the value N*rowval,
        # where N is between 1 and 9999 inclusive.
        dsname = _make_dataset_id('wide_schema')
        dataset = self.temp_dataset(dsname)
        table_id = 'many_columns'
        table_ref = dataset.table(table_id)
        self.to_delete.insert(0, table_ref)
        colprojections = ','.join(
                ['r * {} as col_{}'.format(n, n) for n in range(1, 10000)])
        sql = """
            CREATE TABLE {}.{}
            AS
            SELECT
                r as rowval,
                {}
            FROM
              UNNEST(GENERATE_ARRAY(1,{},1)) as r
            """.format(dsname, table_id, colprojections, rowcount)
        query_job = Config.CLIENT.query(sql)
        query_job.result()
        self.assertEqual(query_job.statement_type, 'CREATE_TABLE_AS_SELECT')
        self.assertEqual(query_job.ddl_operation_performed, 'CREATE')
        self.assertEqual(query_job.ddl_target_table, table_ref)

        return table_ref

    def test_query_many_columns(self):
        # Test working with the widest schema BigQuery supports, 10k columns.
        row_count = 2
        table_ref = self._create_table_many_columns(row_count)
        rows = list(Config.CLIENT.query(
            'SELECT * FROM `{}.{}`'.format(
                table_ref.dataset_id, table_ref.table_id)))

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
        NOW = datetime.datetime.utcfromtimestamp(
            NOW_SECONDS).replace(tzinfo=UTC)
        ROWS = [
            ('Phred Phlyntstone', 32, NOW),
            ('Bharney Rhubble', 33, NOW + datetime.timedelta(seconds=10)),
            ('Wylma Phlyntstone', 29, NOW + datetime.timedelta(seconds=20)),
            ('Bhettye Rhubble', 27, None),
        ]
        ROW_IDS = range(len(ROWS))

        dataset = self.temp_dataset(_make_dataset_id('insert_rows_then_dump'))
        TABLE_ID = 'test_table'
        schema = [
            bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('now', 'TIMESTAMP'),
        ]
        table_arg = Table(dataset.table(TABLE_ID), schema=schema)
        self.assertFalse(_table_exists(table_arg))
        table = retry_403(Config.CLIENT.create_table)(table_arg)
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
        self.assertEqual(sorted(row_tuples, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_local_avro_file_then_dump_table(self):
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition
        TABLE_NAME = 'test_table_avro'
        ROWS = [
            ("violet", 400),
            ("indigo", 445),
            ("blue", 475),
            ("green", 510),
            ("yellow", 570),
            ("orange", 590),
            ("red", 650)]

        dataset = self.temp_dataset(_make_dataset_id('load_local_then_dump'))
        table_ref = dataset.table(TABLE_NAME)
        table = Table(table_ref)
        self.to_delete.insert(0, table)

        with open(os.path.join(WHERE, 'data', 'colors.avro'), 'rb') as avrof:
            config = bigquery.LoadJobConfig()
            config.source_format = SourceFormat.AVRO
            config.write_disposition = WriteDisposition.WRITE_TRUNCATE
            job = Config.CLIENT.load_table_from_file(
                avrof, table_ref, job_config=config)
        # Retry until done.
        job.result(timeout=JOB_TIMEOUT)

        self.assertEqual(job.output_rows, len(ROWS))

        table = Config.CLIENT.get_table(table)
        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        by_wavelength = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_wavelength),
                         sorted(ROWS, key=by_wavelength))

    def test_load_avro_from_uri_then_dump_table(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition
        table_name = 'test_table'
        rows = [
            ("violet", 400),
            ("indigo", 445),
            ("blue", 475),
            ("green", 510),
            ("yellow", 570),
            ("orange", 590),
            ("red", 650)
        ]
        with open(os.path.join(WHERE, 'data', 'colors.avro'), 'rb') as f:
            GS_URL = self._write_avro_to_storage(
                'bq_load_test' + unique_resource_id(), 'colors.avro', f)

        dataset = self.temp_dataset(_make_dataset_id('bq_load_test'))
        table_arg = dataset.table(table_name)
        table = retry_403(Config.CLIENT.create_table)(Table(table_arg))
        self.to_delete.insert(0, table)

        config = bigquery.LoadJobConfig()
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.source_format = SourceFormat.AVRO
        config.write_disposition = WriteDisposition.WRITE_EMPTY
        job = Config.CLIENT.load_table_from_uri(
            GS_URL, table_arg, job_config=config)
        job.result(timeout=JOB_TIMEOUT)
        self.assertEqual(job.output_rows, len(rows))

        table = Config.CLIENT.get_table(table)
        fetched = self._fetch_single_page(table)
        row_tuples = [r.values() for r in fetched]
        self.assertEqual(sorted(row_tuples, key=lambda x: x[1]),
                         sorted(rows, key=lambda x: x[1]))

    def test_load_table_from_uri_then_dump_table(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        TABLE_ID = 'test_table'
        GS_URL = self._write_csv_to_storage(
            'bq_load_test' + unique_resource_id(), 'person_ages.csv',
            HEADER_ROW, ROWS)

        dataset = self.temp_dataset(_make_dataset_id('load_gcs_then_dump'))

        table_arg = Table(dataset.table(TABLE_ID), schema=SCHEMA)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        config = bigquery.LoadJobConfig()
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.skip_leading_rows = 1
        config.source_format = SourceFormat.CSV
        config.write_disposition = WriteDisposition.WRITE_EMPTY
        job = Config.CLIENT.load_table_from_uri(
            GS_URL, dataset.table(TABLE_ID), job_config=config)

        # Allow for 90 seconds of "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_file_w_explicit_location(self):
        # Create a temporary bucket for extract files.
        storage_client = storage.Client()
        bucket_name = 'bq_load_table_eu_extract_test' + unique_resource_id()
        bucket = storage_client.bucket(bucket_name)
        bucket.location = 'eu'
        self.to_delete.append(bucket)
        bucket.create()

        # Create a temporary dataset & table in the EU.
        table_bytes = six.BytesIO(b'a,3\nb,2\nc,1\n')
        client = Config.CLIENT
        dataset = self.temp_dataset(
            _make_dataset_id('eu_load_file'), location='EU')
        table_ref = dataset.table('letters')
        job_config = bigquery.LoadJobConfig()
        job_config.skip_leading_rows = 0
        job_config.schema = [
            bigquery.SchemaField('letter', 'STRING'),
            bigquery.SchemaField('value', 'INTEGER'),
        ]

        # Load the file to an EU dataset with an EU load job.
        load_job = client.load_table_from_file(
            table_bytes, table_ref, location='EU', job_config=job_config)
        load_job.result()
        job_id = load_job.job_id

        # Can get the job from the EU.
        load_job = client.get_job(job_id, location='EU')
        self.assertEqual(job_id, load_job.job_id)
        self.assertEqual('EU', load_job.location)
        self.assertTrue(load_job.exists())

        # Cannot get the job from the US.
        with self.assertRaises(NotFound):
            client.get_job(job_id, location='US')

        load_job_us = client.get_job(job_id)
        load_job_us._properties['jobReference']['location'] = 'US'
        self.assertFalse(load_job_us.exists())
        with self.assertRaises(NotFound):
            load_job_us.reload()

        # Can cancel the job from the EU.
        self.assertTrue(load_job.cancel())
        load_job = client.cancel_job(job_id, location='EU')
        self.assertEqual(job_id, load_job.job_id)
        self.assertEqual('EU', load_job.location)

        # Cannot cancel the job from the US.
        with self.assertRaises(NotFound):
            client.cancel_job(job_id, location='US')
        with self.assertRaises(NotFound):
            load_job_us.cancel()

        # Can list the table rows.
        table = client.get_table(table_ref)
        self.assertEqual(table.num_rows, 3)
        rows = [(row.letter, row.value) for row in client.list_rows(table)]
        self.assertEqual(
            list(sorted(rows)), [('a', 3), ('b', 2), ('c', 1)])

        # Verify location behavior with queries
        query_config = bigquery.QueryJobConfig()
        query_config.dry_run = True

        query_string = 'SELECT * FROM `{}.letters` LIMIT 1'.format(
            dataset.dataset_id)

        eu_query = client.query(
            query_string,
            location='EU',
            job_config=query_config)
        self.assertTrue(eu_query.done)

        # Cannot query from US.
        with self.assertRaises(BadRequest):
            list(client.query(
                    query_string,
                    location='US',
                    job_config=query_config))

        # Cannot copy from US.
        with self.assertRaises(BadRequest):
            client.copy_table(
                table_ref, dataset.table('letters2_us'),
                location='US').result()

        # Cannot extract from US.
        with self.assertRaises(BadRequest):
            client.extract_table(
                table_ref,
                'gs://{}/letters-us.csv'.format(bucket_name),
                location='US').result()

    def _create_storage(self, bucket_name, blob_name):
        storage_client = storage.Client()

        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        bucket = storage_client.create_bucket(bucket_name)
        self.to_delete.append(bucket)

        return bucket.blob(blob_name)

    def _write_csv_to_storage(self, bucket_name, blob_name, header_row,
                              data_rows):
        from google.cloud._testing import _NamedTemporaryFile

        blob = self._create_storage(bucket_name, blob_name)
        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(header_row)
                writer.writerows(data_rows)

            with open(temp.name, 'rb') as csv_read:
                blob.upload_from_file(csv_read, content_type='text/csv')

        self.to_delete.insert(0, blob)
        return 'gs://{}/{}'.format(bucket_name, blob_name)

    def _write_avro_to_storage(self, bucket_name, blob_name, avro_file):
        blob = self._create_storage(bucket_name, blob_name)
        blob.upload_from_file(avro_file,
                              content_type='application/x-avro-binary')
        self.to_delete.insert(0, blob)
        return 'gs://{}/{}'.format(bucket_name, blob_name)

    def _load_table_for_extract_table(
            self, storage_client, rows, bucket_name, blob_name, table):
        from google.cloud._testing import _NamedTemporaryFile

        gs_url = 'gs://{}/{}'.format(bucket_name, blob_name)

        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        bucket = storage_client.create_bucket(bucket_name)
        self.to_delete.append(bucket)
        blob = bucket.blob(blob_name)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(HEADER_ROW)
                writer.writerows(rows)

            with open(temp.name, 'rb') as csv_read:
                blob.upload_from_file(csv_read, content_type='text/csv')
        self.to_delete.insert(0, blob)

        dataset = self.temp_dataset(table.dataset_id)
        table_ref = dataset.table(table.table_id)
        config = bigquery.LoadJobConfig()
        config.autodetect = True
        job = Config.CLIENT.load_table_from_uri(gs_url, table_ref,
                                                job_config=config)
        # TODO(jba): do we need this retry now that we have job.result()?
        # Allow for 90 seconds of "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

    def test_extract_table(self):
        from google.cloud.storage import Client as StorageClient

        storage_client = StorageClient()
        local_id = unique_resource_id()
        bucket_name = 'bq_extract_test' + local_id
        blob_name = 'person_ages.csv'
        dataset_id = _make_dataset_id('load_gcs_then_extract')
        table_id = 'test_table'
        table_ref = Config.CLIENT.dataset(dataset_id).table(table_id)
        table = Table(table_ref)
        self.to_delete.insert(0, table)
        self._load_table_for_extract_table(
            storage_client, ROWS, bucket_name, blob_name, table_ref)
        bucket = storage_client.bucket(bucket_name)
        destination_blob_name = 'person_ages_out.csv'
        destination = bucket.blob(destination_blob_name)
        destination_uri = 'gs://{}/person_ages_out.csv'.format(bucket_name)

        job = Config.CLIENT.extract_table(table_ref, destination_uri)
        job.result(timeout=100)

        self.to_delete.insert(0, destination)
        got = destination.download_as_string().decode('utf-8')
        self.assertIn('Bharney Rhubble', got)

    def test_copy_table(self):
        # If we create a new table to copy from, the test won't work
        # because the new rows will be stored in the streaming buffer,
        # and copy jobs don't read the streaming buffer.
        # We could wait for the streaming buffer to empty, but that could
        # take minutes. Instead we copy a small public table.
        source_dataset = DatasetReference('bigquery-public-data', 'samples')
        source_ref = source_dataset.table('shakespeare')
        dest_dataset = self.temp_dataset(_make_dataset_id('copy_table'))
        dest_ref = dest_dataset.table('destination_table')
        job_config = bigquery.CopyJobConfig()
        job = Config.CLIENT.copy_table(
            source_ref, dest_ref, job_config=job_config)
        job.result()

        dest_table = Config.CLIENT.get_table(dest_ref)
        self.to_delete.insert(0, dest_table)
        # Just check that we got some rows.
        got_rows = self._fetch_single_page(dest_table)
        self.assertTrue(len(got_rows) > 0)

    def test_job_cancel(self):
        DATASET_ID = _make_dataset_id('job_cancel')
        JOB_ID_PREFIX = 'fetch_' + DATASET_ID
        TABLE_NAME = 'test_table'
        QUERY = 'SELECT * FROM %s.%s' % (DATASET_ID, TABLE_NAME)

        dataset = self.temp_dataset(DATASET_ID)

        table_arg = Table(dataset.table(TABLE_NAME), schema=SCHEMA)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
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

    def test_get_failed_job(self):
        # issue 4246
        from google.api_core.exceptions import BadRequest

        JOB_ID = 'invalid_{}'.format(str(uuid.uuid4()))
        QUERY = 'SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);'
        PARAM = bigquery.ScalarQueryParameter(
            'ts_value', 'TIMESTAMP', 1.4810976E9)

        job_config = bigquery.QueryJobConfig()
        job_config.query_parameters = [PARAM]

        with self.assertRaises(BadRequest):
            Config.CLIENT.query(
                QUERY, job_id=JOB_ID, job_config=job_config).result()

        job = Config.CLIENT.get_job(JOB_ID)

        with self.assertRaises(ValueError):
            job.query_parameters

    def test_query_w_legacy_sql_types(self):
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        stamp = '%s %s' % (naive.date().isoformat(), naive.time().isoformat())
        zoned = naive.replace(tzinfo=UTC)
        examples = [
            {
                'sql': 'SELECT 1',
                'expected': 1,
            },
            {
                'sql': 'SELECT 1.3',
                'expected': 1.3,
            },
            {
                'sql': 'SELECT TRUE',
                'expected': True,
            },
            {
                'sql': 'SELECT "ABC"',
                'expected': 'ABC',
            },
            {
                'sql': 'SELECT CAST("foo" AS BYTES)',
                'expected': b'foo',
            },
            {
                'sql': 'SELECT CAST("%s" AS TIMESTAMP)' % (stamp,),
                'expected': zoned,
            },
        ]
        for example in examples:
            job_config = bigquery.QueryJobConfig()
            job_config.use_legacy_sql = True
            rows = list(Config.CLIENT.query(
                example['sql'], job_config=job_config))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example['expected'])

    def _generate_standard_sql_types_examples(self):
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        naive_microseconds = datetime.datetime(2016, 12, 5, 12, 41, 9, 250000)
        stamp = '%s %s' % (naive.date().isoformat(), naive.time().isoformat())
        stamp_microseconds = stamp + '.250000'
        zoned = naive.replace(tzinfo=UTC)
        zoned_microseconds = naive_microseconds.replace(tzinfo=UTC)
        numeric = decimal.Decimal('123456789.123456789')
        return [
            {
                'sql': 'SELECT 1',
                'expected': 1,
            },
            {
                'sql': 'SELECT 1.3',
                'expected': 1.3,
            },
            {
                'sql': 'SELECT TRUE',
                'expected': True,
            },
            {
                'sql': 'SELECT "ABC"',
                'expected': 'ABC',
            },
            {
                'sql': 'SELECT CAST("foo" AS BYTES)',
                'expected': b'foo',
            },
            {
                'sql': 'SELECT TIMESTAMP "%s"' % (stamp,),
                'expected': zoned,
            },
            {
                'sql': 'SELECT TIMESTAMP "%s"' % (stamp_microseconds,),
                'expected': zoned_microseconds,
            },
            {
                'sql': 'SELECT DATETIME(TIMESTAMP "%s")' % (stamp,),
                'expected': naive,
            },
            {
                'sql': 'SELECT DATETIME(TIMESTAMP "%s")' % (
                    stamp_microseconds,),
                'expected': naive_microseconds,
            },
            {
                'sql': 'SELECT DATE(TIMESTAMP "%s")' % (stamp,),
                'expected': naive.date(),
            },
            {
                'sql': 'SELECT TIME(TIMESTAMP "%s")' % (stamp,),
                'expected': naive.time(),
            },
            {
                'sql': 'SELECT NUMERIC "%s"' % (numeric,),
                'expected': numeric,
            },
            {
                'sql': 'SELECT (1, 2)',
                'expected': {'_field_1': 1, '_field_2': 2},
            },
            {
                'sql': 'SELECT ((1, 2), (3, 4), 5)',
                'expected': {
                    '_field_1': {'_field_1': 1, '_field_2': 2},
                    '_field_2': {'_field_1': 3, '_field_2': 4},
                    '_field_3': 5,
                },
            },
            {
                'sql': 'SELECT [1, 2, 3]',
                'expected': [1, 2, 3],
            },
            {
                'sql': 'SELECT ([1, 2], 3, [4, 5])',
                'expected':
                    {'_field_1': [1, 2], '_field_2': 3, '_field_3': [4, 5]},
            },
            {
                'sql': 'SELECT [(1, 2, 3), (4, 5, 6)]',
                'expected': [
                    {'_field_1': 1, '_field_2': 2, '_field_3': 3},
                    {'_field_1': 4, '_field_2': 5, '_field_3': 6},
                ],
            },
            {
                'sql': 'SELECT [([1, 2, 3], 4), ([5, 6], 7)]',
                'expected': [
                    {u'_field_1': [1, 2, 3], u'_field_2': 4},
                    {u'_field_1': [5, 6], u'_field_2': 7},
                ],
            },
            {
                'sql': 'SELECT ARRAY(SELECT STRUCT([1, 2]))',
                'expected': [{u'_field_1': [1, 2]}],
            },
        ]

    def test_query_w_standard_sql_types(self):
        examples = self._generate_standard_sql_types_examples()
        for example in examples:
            rows = list(Config.CLIENT.query(example['sql']))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example['expected'])

    def test_query_w_failed_query(self):
        from google.api_core.exceptions import BadRequest

        with self.assertRaises(BadRequest):
            Config.CLIENT.query('invalid syntax;').result()

    def test_query_w_wrong_config(self):
        from google.cloud.bigquery.job import LoadJobConfig

        good_query = 'SELECT 1;'
        rows = list(Config.CLIENT.query('SELECT 1;').result())
        assert rows[0][0] == 1

        bad_config = LoadJobConfig()
        bad_config.destination = Config.CLIENT.dataset('dset').table('tbl')
        with self.assertRaises(Exception):
            Config.CLIENT.query(good_query, job_config=bad_config).result()

    def test_query_w_timeout(self):
        query_job = Config.CLIENT.query(
            'SELECT * FROM `bigquery-public-data.github_repos.commits`;',
            job_id_prefix='test_query_w_timeout_')

        with self.assertRaises(concurrent.futures.TimeoutError):
            # 1 second is much too short for this query.
            query_job.result(timeout=1)

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
            location='US',
            job_config=job_config)

        # run the job to completion
        query_job.result()

        # Assert top-level stats
        self.assertFalse(query_job.cache_hit)
        self.assertIsNotNone(query_job.destination)
        self.assertTrue(query_job.done)
        self.assertFalse(query_job.dry_run)
        self.assertIsNone(query_job.num_dml_affected_rows)
        self.assertEqual(query_job.priority, 'INTERACTIVE')
        self.assertGreater(query_job.total_bytes_billed, 1)
        self.assertGreater(query_job.total_bytes_processed, 1)
        self.assertEqual(query_job.statement_type, 'SELECT')
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
        self.assertEqual(first_stage.status, 'COMPLETE')

        # Query plan is a digraph.  Ensure it has inter-stage links,
        # but not every stage has inputs.
        stages_with_inputs = 0
        for entry in plan:
            if len(entry.input_stages) > 0:
                stages_with_inputs = stages_with_inputs + 1
        self.assertGreater(stages_with_inputs, 0)
        self.assertGreater(len(plan), stages_with_inputs)

    def test_dbapi_w_standard_sql_types(self):
        examples = self._generate_standard_sql_types_examples()
        for example in examples:
            Config.CURSOR.execute(example['sql'])
            self.assertEqual(Config.CURSOR.rowcount, 1)
            row = Config.CURSOR.fetchone()
            self.assertEqual(len(row), 1)
            self.assertEqual(row[0], example['expected'])
            row = Config.CURSOR.fetchone()
            self.assertIsNone(row)

    def test_dbapi_fetchall(self):
        query = 'SELECT * FROM UNNEST([(1, 2), (3, 4), (5, 6)])'

        for arraysize in range(1, 5):
            Config.CURSOR.execute(query)
            self.assertEqual(Config.CURSOR.rowcount, 3, "expected 3 rows")
            Config.CURSOR.arraysize = arraysize
            rows = Config.CURSOR.fetchall()
            row_tuples = [r.values() for r in rows]
            self.assertEqual(row_tuples, [(1, 2), (3, 4), (5, 6)])

    def _load_table_for_dml(self, rows, dataset_id, table_id):
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        dataset = self.temp_dataset(dataset_id)
        greeting = bigquery.SchemaField(
            'greeting', 'STRING', mode='NULLABLE')
        table_ref = dataset.table(table_id)
        table_arg = Table(table_ref, schema=[greeting])
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(('Greeting',))
                writer.writerows(rows)

            with open(temp.name, 'rb') as csv_read:
                config = bigquery.LoadJobConfig()
                config.source_format = SourceFormat.CSV
                config.skip_leading_rows = 1
                config.create_disposition = CreateDisposition.CREATE_NEVER
                config.write_disposition = WriteDisposition.WRITE_EMPTY
                job = Config.CLIENT.load_table_from_file(
                    csv_read, table_ref, job_config=config)

        # Retry until done.
        job.result(timeout=JOB_TIMEOUT)
        self._fetch_single_page(table)

    def test_query_w_dml(self):
        dataset_name = _make_dataset_id('dml_tests')
        table_name = 'test_table'
        self._load_table_for_dml([('Hello World',)], dataset_name, table_name)
        query_template = """UPDATE {}.{}
            SET greeting = 'Guten Tag'
            WHERE greeting = 'Hello World'
            """

        query_job = Config.CLIENT.query(
            query_template.format(dataset_name, table_name),
            job_id_prefix='test_query_w_dml_')
        query_job.result()

        self.assertEqual(query_job.num_dml_affected_rows, 1)

    def test_dbapi_w_dml(self):
        dataset_name = _make_dataset_id('dml_tests')
        table_name = 'test_table'
        self._load_table_for_dml([('Hello World',)], dataset_name, table_name)
        query_template = """UPDATE {}.{}
            SET greeting = 'Guten Tag'
            WHERE greeting = 'Hello World'
            """

        Config.CURSOR.execute(
            query_template.format(dataset_name, table_name),
            job_id='test_dbapi_w_dml_{}'.format(str(uuid.uuid4())))
        self.assertEqual(Config.CURSOR.rowcount, 1)
        self.assertIsNone(Config.CURSOR.fetchone())

    def test_query_w_query_params(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ArrayQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameter
        from google.cloud.bigquery.query import StructQueryParameter
        question = 'What is the answer to life, the universe, and everything?'
        question_param = ScalarQueryParameter(
            name='question', type_='STRING', value=question)
        answer = 42
        answer_param = ScalarQueryParameter(
            name='answer', type_='INT64', value=answer)
        pi = 3.1415926
        pi_param = ScalarQueryParameter(
            name='pi', type_='FLOAT64', value=pi)
        pi_numeric = decimal.Decimal('3.141592654')
        pi_numeric_param = ScalarQueryParameter(
            name='pi_numeric_param', type_='NUMERIC',
            value=pi_numeric)
        truthy = True
        truthy_param = ScalarQueryParameter(
            name='truthy', type_='BOOL', value=truthy)
        beef = b'DEADBEEF'
        beef_param = ScalarQueryParameter(
            name='beef', type_='BYTES', value=beef)
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        naive_param = ScalarQueryParameter(
            name='naive', type_='DATETIME', value=naive)
        naive_date_param = ScalarQueryParameter(
            name='naive_date', type_='DATE', value=naive.date())
        naive_time_param = ScalarQueryParameter(
            name='naive_time', type_='TIME', value=naive.time())
        zoned = naive.replace(tzinfo=UTC)
        zoned_param = ScalarQueryParameter(
            name='zoned', type_='TIMESTAMP', value=zoned)
        array_param = ArrayQueryParameter(
            name='array_param', array_type='INT64', values=[1, 2])
        struct_param = StructQueryParameter(
            'hitchhiker', question_param, answer_param)
        phred_name = 'Phred Phlyntstone'
        phred_name_param = ScalarQueryParameter(
            name='name', type_='STRING', value=phred_name)
        phred_age = 32
        phred_age_param = ScalarQueryParameter(
            name='age', type_='INT64', value=phred_age)
        phred_param = StructQueryParameter(
            None, phred_name_param, phred_age_param)
        bharney_name = 'Bharney Rhubbyl'
        bharney_name_param = ScalarQueryParameter(
            name='name', type_='STRING', value=bharney_name)
        bharney_age = 31
        bharney_age_param = ScalarQueryParameter(
            name='age', type_='INT64', value=bharney_age)
        bharney_param = StructQueryParameter(
            None, bharney_name_param, bharney_age_param)
        characters_param = ArrayQueryParameter(
            name=None, array_type='RECORD',
            values=[phred_param, bharney_param])
        hero_param = StructQueryParameter(
            'hero', phred_name_param, phred_age_param)
        sidekick_param = StructQueryParameter(
            'sidekick', bharney_name_param, bharney_age_param)
        roles_param = StructQueryParameter(
            'roles', hero_param, sidekick_param)
        friends_param = ArrayQueryParameter(
            name='friends', array_type='STRING',
            values=[phred_name, bharney_name])
        with_friends_param = StructQueryParameter(None, friends_param)
        top_left_param = StructQueryParameter(
            'top_left',
            ScalarQueryParameter('x', 'INT64', 12),
            ScalarQueryParameter('y', 'INT64', 102))
        bottom_right_param = StructQueryParameter(
            'bottom_right',
            ScalarQueryParameter('x', 'INT64', 22),
            ScalarQueryParameter('y', 'INT64', 92))
        rectangle_param = StructQueryParameter(
            'rectangle', top_left_param, bottom_right_param)
        examples = [
            {
                'sql': 'SELECT @question',
                'expected': question,
                'query_parameters': [question_param],
            },
            {
                'sql': 'SELECT @answer',
                'expected': answer,
                'query_parameters': [answer_param],
            },
            {
                'sql': 'SELECT @pi',
                'expected': pi,
                'query_parameters': [pi_param],
            },
            {
                'sql': 'SELECT @pi_numeric_param',
                'expected': pi_numeric,
                'query_parameters': [pi_numeric_param],
            },
            {
                'sql': 'SELECT @truthy',
                'expected': truthy,
                'query_parameters': [truthy_param],
            },
            {
                'sql': 'SELECT @beef',
                'expected': beef,
                'query_parameters': [beef_param],
            },
            {
                'sql': 'SELECT @naive',
                'expected': naive,
                'query_parameters': [naive_param],
            },
            {
                'sql': 'SELECT @naive_date',
                'expected': naive.date(),
                'query_parameters': [naive_date_param],
            },
            {
                'sql': 'SELECT @naive_time',
                'expected': naive.time(),
                'query_parameters': [naive_time_param],
            },
            {
                'sql': 'SELECT @zoned',
                'expected': zoned,
                'query_parameters': [zoned_param],
            },
            {
                'sql': 'SELECT @array_param',
                'expected': [1, 2],
                'query_parameters': [array_param],
            },
            {
                'sql': 'SELECT (@hitchhiker.question, @hitchhiker.answer)',
                'expected': ({'_field_1': question, '_field_2': answer}),
                'query_parameters': [struct_param],
            },
            {
                'sql':
                    'SELECT '
                    '((@rectangle.bottom_right.x - @rectangle.top_left.x) '
                    '* (@rectangle.top_left.y - @rectangle.bottom_right.y))',
                'expected': 100,
                'query_parameters': [rectangle_param],
            },
            {
                'sql': 'SELECT ?',
                'expected': [
                    {'name': phred_name, 'age': phred_age},
                    {'name': bharney_name, 'age': bharney_age},
                ],
                'query_parameters': [characters_param],
            },
            {
                'sql': 'SELECT @roles',
                'expected': {
                    'hero': {'name': phred_name, 'age': phred_age},
                    'sidekick': {'name': bharney_name, 'age': bharney_age},
                },
                'query_parameters': [roles_param],
            },
            {
                'sql': 'SELECT ?',
                'expected': {
                    'friends': [phred_name, bharney_name],
                },
                'query_parameters': [with_friends_param],
            },
        ]
        for example in examples:
            jconfig = QueryJobConfig()
            jconfig.query_parameters = example['query_parameters']
            query_job = Config.CLIENT.query(
                example['sql'],
                job_config=jconfig,
                job_id_prefix='test_query_w_query_params')
            rows = list(query_job.result())
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example['expected'])

    def test_dbapi_w_query_parameters(self):
        examples = [
            {
                'sql': 'SELECT %(boolval)s',
                'expected': True,
                'query_parameters': {
                    'boolval': True,
                },
            },
            {
                'sql': 'SELECT %(a "very" weird `name`)s',
                'expected': True,
                'query_parameters': {
                    'a "very" weird `name`': True,
                },
            },
            {
                'sql': 'SELECT %(select)s',
                'expected': True,
                'query_parameters': {
                    'select': True,  # this name is a keyword
                },
            },
            {
                'sql': 'SELECT %s',
                'expected': False,
                'query_parameters': [False],
            },
            {
                'sql': 'SELECT %(intval)s',
                'expected': 123,
                'query_parameters': {
                    'intval': 123,
                },
            },
            {
                'sql': 'SELECT %s',
                'expected': -123456789,
                'query_parameters': [-123456789],
            },
            {
                'sql': 'SELECT %(floatval)s',
                'expected': 1.25,
                'query_parameters': {
                    'floatval': 1.25,
                },
            },
            {
                'sql': 'SELECT LOWER(%(strval)s)',
                'query_parameters': {
                    'strval': 'I Am A String',
                },
                'expected': 'i am a string',
            },
            {
                'sql': 'SELECT DATE_SUB(%(dateval)s, INTERVAL 1 DAY)',
                'query_parameters': {
                    'dateval': datetime.date(2017, 4, 2),
                },
                'expected': datetime.date(2017, 4, 1),
            },
            {
                'sql': 'SELECT TIME_ADD(%(timeval)s, INTERVAL 4 SECOND)',
                'query_parameters': {
                    'timeval': datetime.time(12, 34, 56),
                },
                'expected': datetime.time(12, 35, 0),
            },
            {
                'sql': (
                    'SELECT DATETIME_ADD(%(datetimeval)s, INTERVAL 53 SECOND)'
                ),
                'query_parameters': {
                    'datetimeval': datetime.datetime(2012, 3, 4, 5, 6, 7),
                },
                'expected': datetime.datetime(2012, 3, 4, 5, 7, 0),
            },
            {
                'sql': 'SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)',
                'query_parameters': {
                    'zoned': datetime.datetime(
                        2012, 3, 4, 5, 6, 7, tzinfo=UTC),
                },
                'expected': datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            },
            {
                'sql': 'SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)',
                'query_parameters': {
                    'zoned': datetime.datetime(
                        2012, 3, 4, 5, 6, 7, 250000, tzinfo=UTC),
                },
                'expected': datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            },
        ]
        for example in examples:
            msg = 'sql: {} query_parameters: {}'.format(
                example['sql'], example['query_parameters'])

            Config.CURSOR.execute(example['sql'], example['query_parameters'])

            self.assertEqual(Config.CURSOR.rowcount, 1, msg=msg)
            row = Config.CURSOR.fetchone()
            self.assertEqual(len(row), 1, msg=msg)
            self.assertEqual(row[0], example['expected'], msg=msg)
            row = Config.CURSOR.fetchone()
            self.assertIsNone(row, msg=msg)

    def test_large_query_w_public_data(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_ID = 'samples'
        TABLE_NAME = 'natality'
        LIMIT = 1000
        SQL = 'SELECT * from `{}.{}.{}` LIMIT {}'.format(
            PUBLIC, DATASET_ID, TABLE_NAME, LIMIT)

        query_job = Config.CLIENT.query(SQL)

        rows = list(query_job)
        self.assertEqual(len(rows), LIMIT)

    def test_query_future(self):
        query_job = Config.CLIENT.query('SELECT 1')
        iterator = query_job.result(timeout=JOB_TIMEOUT)
        row_tuples = [r.values() for r in iterator]
        self.assertEqual(row_tuples, [(1,)])

    def test_query_iter(self):
        import types
        query_job = Config.CLIENT.query('SELECT 1')
        self.assertIsInstance(iter(query_job), types.GeneratorType)
        row_tuples = [r.values() for r in query_job]
        self.assertEqual(row_tuples, [(1,)])

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_query_results_to_dataframe(self):
        QUERY = """
            SELECT id, author, time_ts, dead
            from `bigquery-public-data.hacker_news.comments`
            LIMIT 10
        """

        df = Config.CLIENT.query(QUERY).result().to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 10)  # verify the number of rows
        column_names = ['id', 'author', 'time_ts', 'dead']
        self.assertEqual(list(df), column_names)  # verify the column names
        exp_datatypes = {'id': int, 'author': six.text_type,
                         'time_ts': pandas.Timestamp, 'dead': bool}
        for index, row in df.iterrows():
            for col in column_names:
                # all the schema fields are nullable, so None is acceptable
                if not row[col] is None:
                    self.assertIsInstance(row[col], exp_datatypes[col])

    def test_insert_rows_nested_nested(self):
        # See #2951
        SF = bigquery.SchemaField
        schema = [
            SF('string_col', 'STRING', mode='NULLABLE'),
            SF('record_col', 'RECORD', mode='NULLABLE', fields=[
                SF('nested_string', 'STRING', mode='NULLABLE'),
                SF('nested_repeated', 'INTEGER', mode='REPEATED'),
                SF('nested_record', 'RECORD', mode='NULLABLE', fields=[
                    SF('nested_nested_string', 'STRING', mode='NULLABLE'),
                ]),
            ]),
        ]
        record = {
            'nested_string': 'another string value',
            'nested_repeated': [0, 1, 2],
            'nested_record': {'nested_nested_string': 'some deep insight'},
        }
        to_insert = [
            ('Some value', record)
        ]
        table_id = 'test_table'
        dataset = self.temp_dataset(_make_dataset_id('issue_2951'))
        table_arg = Table(dataset.table(table_id), schema=schema)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
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
            SF('string_col', 'STRING', mode='NULLABLE'),
            SF('record_col', 'RECORD', mode='NULLABLE', fields=[
                SF('nested_string', 'STRING', mode='NULLABLE'),
                SF('nested_repeated', 'INTEGER', mode='REPEATED'),
                SF('nested_record', 'RECORD', mode='NULLABLE', fields=[
                    SF('nested_nested_string', 'STRING', mode='NULLABLE'),
                ]),
            ]),
        ]
        record = {
            'nested_string': 'another string value',
            'nested_repeated': [0, 1, 2],
            'nested_record': {'nested_nested_string': 'some deep insight'},
        }
        to_insert = [
            {'string_col': 'Some value', 'record_col': record}
        ]
        table_id = 'test_table'
        dataset = self.temp_dataset(_make_dataset_id('issue_2951'))
        table_arg = Table(dataset.table(table_id), schema=schema)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        Config.CLIENT.insert_rows(table, to_insert)

        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)
        row_tuples = [r.values() for r in rows]
        expected_rows = [('Some value', record)]
        self.assertEqual(row_tuples, expected_rows)

    def test_create_table_rows_fetch_nested_schema(self):
        table_name = 'test_table'
        dataset = self.temp_dataset(
            _make_dataset_id('create_table_nested_schema'))
        schema = _load_json_schema()
        table_arg = Table(dataset.table(table_name), schema=schema)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)
        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_name)

        to_insert = []
        # Data is in "JSON Lines" format, see http://jsonlines.org/
        json_filename = os.path.join(WHERE, 'data', 'characters.jsonl')
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
            self.assertEqual(found[0], expected['Name'])
            self.assertEqual(found[1], int(expected['Age']))
            self.assertEqual(found[2], expected['Weight'])
            self.assertEqual(found[3], expected['IsMagic'])

            self.assertEqual(len(found[4]), len(expected['Spells']))
            for f_spell, e_spell in zip(found[4], expected['Spells']):
                self.assertEqual(f_spell['Name'], e_spell['Name'])
                parts = time.strptime(
                    e_spell['LastUsed'], '%Y-%m-%d %H:%M:%S UTC')
                e_used = datetime.datetime(*parts[0:6], tzinfo=UTC)
                self.assertEqual(f_spell['LastUsed'], e_used)
                self.assertEqual(f_spell['DiscoveredBy'],
                                 e_spell['DiscoveredBy'])
                self.assertEqual(f_spell['Properties'], e_spell['Properties'])

                e_icon = base64.standard_b64decode(
                    e_spell['Icon'].encode('ascii'))
                self.assertEqual(f_spell['Icon'], e_icon)

            parts = time.strptime(expected['TeaTime'], '%H:%M:%S')
            e_teatime = datetime.time(*parts[3:6])
            self.assertEqual(found[5], e_teatime)

            parts = time.strptime(expected['NextVacation'], '%Y-%m-%d')
            e_nextvac = datetime.date(*parts[0:3])
            self.assertEqual(found[6], e_nextvac)

            parts = time.strptime(expected['FavoriteTime'],
                                  '%Y-%m-%dT%H:%M:%S')
            e_favtime = datetime.datetime(*parts[0:6])
            self.assertEqual(found[7], e_favtime)
            self.assertEqual(found[8],
                             decimal.Decimal(expected['FavoriteNumber']))

    def _fetch_dataframe(self, query):
        return Config.CLIENT.query(query).result().to_dataframe()

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_nested_table_to_dataframe(self):
        from google.cloud.bigquery.job import SourceFormat
        from google.cloud.bigquery.job import WriteDisposition

        SF = bigquery.SchemaField
        schema = [
            SF('string_col', 'STRING', mode='NULLABLE'),
            SF('record_col', 'RECORD', mode='NULLABLE', fields=[
                SF('nested_string', 'STRING', mode='NULLABLE'),
                SF('nested_repeated', 'INTEGER', mode='REPEATED'),
                SF('nested_record', 'RECORD', mode='NULLABLE', fields=[
                    SF('nested_nested_string', 'STRING', mode='NULLABLE'),
                ]),
            ]),
        ]
        record = {
            'nested_string': 'another string value',
            'nested_repeated': [0, 1, 2],
            'nested_record': {'nested_nested_string': 'some deep insight'},
        }
        to_insert = [
            {'string_col': 'Some value', 'record_col': record},
        ]
        rows = [json.dumps(row) for row in to_insert]
        body = six.BytesIO('{}\n'.format('\n'.join(rows)).encode('ascii'))
        table_id = 'test_table'
        dataset = self.temp_dataset(_make_dataset_id('nested_df'))
        table = dataset.table(table_id)
        self.to_delete.insert(0, table)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = schema
        # Load a table using a local JSON file from memory.
        Config.CLIENT.load_table_from_file(
            body, table, job_config=job_config).result()

        df = Config.CLIENT.list_rows(
            table, selected_fields=schema).to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 1)  # verify the number of rows
        exp_columns = ['string_col', 'record_col']
        self.assertEqual(list(df), exp_columns)  # verify the column names
        row = df.iloc[0]
        # verify the row content
        self.assertEqual(row['string_col'], 'Some value')
        self.assertEqual(row['record_col'], record)
        # verify that nested data can be accessed with indices/keys
        self.assertEqual(row['record_col']['nested_repeated'][0], 0)
        self.assertEqual(
            row['record_col']['nested_record']['nested_nested_string'],
            'some deep insight')

    def test_list_rows_empty_table(self):
        from google.cloud.bigquery.table import RowIterator

        dataset_id = _make_dataset_id('empty_table')
        dataset = self.temp_dataset(dataset_id)
        table_ref = dataset.table('empty_table')
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
        schema = [SF('string_col', 'STRING', mode='NULLABLE')]
        to_insert = [{'string_col': 'item%d' % i} for i in range(num_items)]
        rows = [json.dumps(row) for row in to_insert]
        body = six.BytesIO('{}\n'.format('\n'.join(rows)).encode('ascii'))

        table_id = 'test_table'
        dataset = self.temp_dataset(_make_dataset_id('nested_df'))
        table = dataset.table(table_id)
        self.to_delete.insert(0, table)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = schema
        # Load a table using a local JSON file from memory.
        Config.CLIENT.load_table_from_file(
            body, table, job_config=job_config).result()

        df = Config.CLIENT.list_rows(
            table, selected_fields=schema, page_size=page_size)
        pages = df.pages

        for i in range(num_pages):
            page = next(pages)
            self.assertEqual(page.num_items, page_size)
        page = next(pages)
        self.assertEqual(page.num_items, num_last_page)

    def temp_dataset(self, dataset_id, location=None):
        dataset = Dataset(Config.CLIENT.dataset(dataset_id))
        if location:
            dataset.location = location
        dataset = retry_403(Config.CLIENT.create_dataset)(dataset)
        self.to_delete.append(dataset)
        return dataset


@pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
@pytest.mark.skipif(IPython is None, reason='Requires `ipython`')
@pytest.mark.usefixtures('ipython_interactive')
def test_bigquery_magic():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    sql = """
        SELECT
            CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
            view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10
    """
    with io.capture_output() as captured:
        result = ip.run_cell_magic('bigquery', '', sql)

    lines = re.split('\n|\r', captured.stdout)
    # Removes blanks & terminal code (result of display clearing)
    updates = list(filter(lambda x: bool(x) and x != '\x1b[2K', lines))
    assert re.match("Executing query with job ID: .*", updates[0])
    assert all(re.match("Query executing: .*s", line)
               for line in updates[1:-1])
    assert re.match("Query complete after .*s", updates[-1])
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 10                      # verify row count
    assert list(result) == ['url', 'view_count']  # verify column names


def _job_done(instance):
    return instance.state.lower() == 'done'


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


@pytest.fixture(scope='session')
def ipython():
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture()
def ipython_interactive(request, ipython):
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """
    with ipython.builtin_trap:
        yield ipython
