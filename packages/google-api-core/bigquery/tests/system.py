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

import base64
import csv
import datetime
import json
import operator
import os
import time
import unittest
import uuid

import six

from google.api_core.exceptions import PreconditionFailed
from google.cloud import bigquery
from google.cloud.bigquery.dataset import Dataset, DatasetReference
from google.cloud.bigquery.table import Table
from google.cloud._helpers import UTC
from google.cloud.bigquery import dbapi
from google.cloud.exceptions import Forbidden, NotFound

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
            elif isinstance(doomed, Dataset):
                retry_in_use(Config.CLIENT.delete_dataset)(doomed)
            elif isinstance(doomed, Table):
                retry_in_use(Config.CLIENT.delete_table)(doomed)
            else:
                doomed.delete()

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

    def test_create_table(self):
        dataset = self.temp_dataset(_make_dataset_id('create_table'))
        table_id = 'test_table'
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        self.assertFalse(_table_exists(table_arg))

        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        self.assertTrue(_table_exists(table))
        self.assertEqual(table.table_id, table_id)

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

    def test_list_dataset_tables(self):
        DATASET_ID = _make_dataset_id('list_tables')
        dataset = self.temp_dataset(DATASET_ID)
        # Retrieve tables before any are created for the dataset.
        iterator = Config.CLIENT.list_dataset_tables(dataset)
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
        iterator = Config.CLIENT.list_dataset_tables(dataset)
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

    def test_create_rows_then_dump_table(self):
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

        dataset = self.temp_dataset(_make_dataset_id('create_rows_then_dump'))
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

        errors = Config.CLIENT.create_rows(table, ROWS, row_ids=ROW_IDS)
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

    def test_load_table_from_local_file_then_dump_table(self):
        from google.cloud._testing import _NamedTemporaryFile

        TABLE_NAME = 'test_table'

        dataset = self.temp_dataset(_make_dataset_id('load_local_then_dump'))
        table_ref = dataset.table(TABLE_NAME)
        table_arg = Table(table_ref, schema=SCHEMA)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(HEADER_ROW)
                writer.writerows(ROWS)

            with open(temp.name, 'rb') as csv_read:
                config = bigquery.LoadJobConfig()
                config.source_format = 'CSV'
                config.skip_leading_rows = 1
                config.create_disposition = 'CREATE_NEVER'
                config.write_disposition = 'WRITE_EMPTY'
                config.schema = table.schema
                job = Config.CLIENT.load_table_from_file(
                    csv_read, table_ref, job_config=config)

        # Retry until done.
        job.result(timeout=JOB_TIMEOUT)

        self.assertEqual(job.output_rows, len(ROWS))

        rows = self._fetch_single_page(table)
        row_tuples = [r.values() for r in rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_local_avro_file_then_dump_table(self):
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
            config.source_format = 'AVRO'
            config.write_disposition = 'WRITE_TRUNCATE'
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

    def test_load_table_from_uri_then_dump_table(self):
        TABLE_ID = 'test_table'
        GS_URL = self._write_csv_to_storage(
            'bq_load_test' + unique_resource_id(), 'person_ages.csv',
            HEADER_ROW, ROWS)

        dataset = self.temp_dataset(_make_dataset_id('load_gcs_then_dump'))

        table_arg = Table(dataset.table(TABLE_ID), schema=SCHEMA)
        table = retry_403(Config.CLIENT.create_table)(table_arg)
        self.to_delete.insert(0, table)

        config = bigquery.LoadJobConfig()
        config.create_disposition = 'CREATE_NEVER'
        config.skip_leading_rows = 1
        config.source_format = 'CSV'
        config.write_disposition = 'WRITE_EMPTY'
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

    def test_load_table_from_uri_w_autodetect_schema_then_get_job(self):
        from google.cloud.bigquery import SchemaField
        from google.cloud.bigquery.job import LoadJob

        rows = ROWS * 100
        # BigQuery internally uses the first 100 rows to detect schema

        gs_url = self._write_csv_to_storage(
            'bq_load_test' + unique_resource_id(), 'person_ages.csv',
            HEADER_ROW, rows)
        dataset = self.temp_dataset(_make_dataset_id('load_gcs_then_dump'))
        table_ref = dataset.table('test_table')
        JOB_ID = 'load_table_w_autodetect_{}'.format(str(uuid.uuid4()))

        config = bigquery.LoadJobConfig()
        config.autodetect = True
        job = Config.CLIENT.load_table_from_uri(
            gs_url, table_ref, job_config=config, job_id=JOB_ID)

        # Allow for 90 seconds of "warm up" before rows visible.  See
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        table = Config.CLIENT.get_table(table_ref)
        self.to_delete.insert(0, table)
        field_name = SchemaField(
            u'Full_Name', u'string', u'NULLABLE', None, ())
        field_age = SchemaField(u'Age', u'integer', u'NULLABLE', None, ())
        self.assertEqual(table.schema, [field_name, field_age])

        actual_rows = self._fetch_single_page(table)
        actual_row_tuples = [r.values() for r in actual_rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(
            sorted(actual_row_tuples, key=by_age), sorted(rows, key=by_age))

        fetched_job = Config.CLIENT.get_job(JOB_ID)

        self.assertIsInstance(fetched_job, LoadJob)
        self.assertEqual(fetched_job.job_id, JOB_ID)
        self.assertEqual(fetched_job.autodetect, True)

    def _write_csv_to_storage(self, bucket_name, blob_name, header_row,
                              data_rows):
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.storage import Client as StorageClient

        storage_client = StorageClient()

        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        bucket = storage_client.create_bucket(bucket_name)
        self.to_delete.append(bucket)

        blob = bucket.blob(blob_name)

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as csv_write:
                writer = csv.writer(csv_write)
                writer.writerow(header_row)
                writer.writerows(data_rows)

            with open(temp.name, 'rb') as csv_read:
                blob.upload_from_file(csv_read, content_type='text/csv')

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

    def test_extract_table_w_job_config(self):
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

        job_config = bigquery.ExtractJobConfig()
        job_config.destination_format = 'NEWLINE_DELIMITED_JSON'
        job = Config.CLIENT.extract_table(
            table, destination_uri, job_config=job_config)
        job.result()

        self.to_delete.insert(0, destination)
        got = destination.download_as_string().decode('utf-8')
        self.assertIn('"Bharney Rhubble"', got)

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

    def test_query_rows_w_legacy_sql_types(self):
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
            rows = list(Config.CLIENT.query_rows(
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

    def test_query_rows_w_standard_sql_types(self):
        examples = self._generate_standard_sql_types_examples()
        for example in examples:
            rows = list(Config.CLIENT.query_rows(example['sql']))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0]), 1)
            self.assertEqual(rows[0][0], example['expected'])

    def test_query_rows_w_failed_query(self):
        from google.api_core.exceptions import BadRequest

        with self.assertRaises(BadRequest):
            Config.CLIENT.query_rows('invalid syntax;')
            # TODO(swast): Ensure that job ID is surfaced in the exception.

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
                config.source_format = 'CSV'
                config.skip_leading_rows = 1
                config.create_disposition = 'CREATE_NEVER'
                config.write_disposition = 'WRITE_EMPTY'
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

    def test_dump_table_w_public_data(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_ID = 'samples'
        TABLE_NAME = 'natality'

        table_ref = DatasetReference(PUBLIC, DATASET_ID).table(TABLE_NAME)
        table = Config.CLIENT.get_table(table_ref)
        self._fetch_single_page(table)

    def test_dump_table_w_public_data_selected_fields(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_ID = 'samples'
        TABLE_NAME = 'natality'
        selected_fields = [
            bigquery.SchemaField('year', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('month', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('day', 'INTEGER', mode='NULLABLE'),
        ]
        table_ref = DatasetReference(PUBLIC, DATASET_ID).table(TABLE_NAME)

        rows = self._fetch_single_page(
            table_ref, selected_fields=selected_fields)

        self.assertGreater(len(rows), 0)
        self.assertEqual(len(rows[0]), 3)

    def test_large_query_w_public_data(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_ID = 'samples'
        TABLE_NAME = 'natality'
        LIMIT = 1000
        SQL = 'SELECT * from `{}.{}.{}` LIMIT {}'.format(
            PUBLIC, DATASET_ID, TABLE_NAME, LIMIT)

        iterator = Config.CLIENT.query_rows(SQL)

        rows = list(iterator)
        self.assertEqual(len(rows), LIMIT)

    def test_query_future(self):
        query_job = Config.CLIENT.query('SELECT 1')
        iterator = query_job.result(timeout=JOB_TIMEOUT)
        row_tuples = [r.values() for r in iterator]
        self.assertEqual(row_tuples, [(1,)])

    def test_query_table_def(self):
        gs_url = self._write_csv_to_storage(
            'bq_external_test' + unique_resource_id(), 'person_ages.csv',
            HEADER_ROW, ROWS)

        job_config = bigquery.QueryJobConfig()
        table_id = 'flintstones'
        ec = bigquery.ExternalConfig('CSV')
        ec.source_uris = [gs_url]
        ec.schema = SCHEMA
        ec.options.skip_leading_rows = 1  # skip the header row
        job_config.table_definitions = {table_id: ec}
        sql = 'SELECT * FROM %s' % table_id

        got_rows = Config.CLIENT.query_rows(sql, job_config=job_config)

        row_tuples = [r.values() for r in got_rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_query_external_table(self):
        gs_url = self._write_csv_to_storage(
            'bq_external_test' + unique_resource_id(), 'person_ages.csv',
            HEADER_ROW, ROWS)
        dataset_id = _make_dataset_id('query_external_table')
        dataset = self.temp_dataset(dataset_id)
        table_id = 'flintstones'
        table_arg = Table(dataset.table(table_id), schema=SCHEMA)
        ec = bigquery.ExternalConfig('CSV')
        ec.source_uris = [gs_url]
        ec.options.skip_leading_rows = 1  # skip the header row
        table_arg.external_data_configuration = ec
        table = Config.CLIENT.create_table(table_arg)
        self.to_delete.insert(0, table)

        sql = 'SELECT * FROM %s.%s' % (dataset_id, table_id)

        got_rows = Config.CLIENT.query_rows(sql)

        row_tuples = [r.values() for r in got_rows]
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(row_tuples, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_create_rows_nested_nested(self):
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

        Config.CLIENT.create_rows(table, to_insert)

        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)
        row_tuples = [r.values() for r in rows]
        self.assertEqual(row_tuples, to_insert)

    def test_create_rows_nested_nested_dictionary(self):
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

        Config.CLIENT.create_rows(table, to_insert)

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

        errors = Config.CLIENT.create_rows_json(table, to_insert)
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

    def temp_dataset(self, dataset_id):
        dataset = retry_403(Config.CLIENT.create_dataset)(
            Dataset(Config.CLIENT.dataset(dataset_id)))
        self.to_delete.append(dataset)
        return dataset


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
