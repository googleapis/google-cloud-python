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
import datetime
import json
import operator
import os
import time
import unittest

from google.cloud import bigquery
from google.cloud._helpers import UTC
from google.cloud.exceptions import Forbidden

from test_utils.retry import RetryErrors
from test_utils.retry import RetryInstanceState
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


WHERE = os.path.abspath(os.path.dirname(__file__))


def _has_rows(result):
    return len(result) > 0


def _make_dataset_name(prefix):
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
# See: https://cloud.google.com/bigquery/quota-policy
retry_403 = RetryErrors(Forbidden, error_predicate=_rate_limit_exceeded)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    Config.CLIENT = bigquery.Client()


class TestBigQuery(unittest.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        from google.cloud.bigquery.dataset import Dataset
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
                retry_in_use(doomed.delete)()
            else:
                doomed.delete()

    def test_create_dataset(self):
        DATASET_NAME = _make_dataset_name('create_dataset')
        dataset = Config.CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        self.assertTrue(dataset.exists())
        self.assertEqual(dataset.name, DATASET_NAME)

    def test_reload_dataset(self):
        DATASET_NAME = _make_dataset_name('reload_dataset')
        dataset = Config.CLIENT.dataset(DATASET_NAME)
        dataset.friendly_name = 'Friendly'
        dataset.description = 'Description'

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        other = Config.CLIENT.dataset(DATASET_NAME)
        other.reload()
        self.assertEqual(other.friendly_name, 'Friendly')
        self.assertEqual(other.description, 'Description')

    def test_patch_dataset(self):
        dataset = Config.CLIENT.dataset(_make_dataset_name('patch_dataset'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        self.assertTrue(dataset.exists())
        self.assertIsNone(dataset.friendly_name)
        self.assertIsNone(dataset.description)
        dataset.patch(friendly_name='Friendly', description='Description')
        self.assertEqual(dataset.friendly_name, 'Friendly')
        self.assertEqual(dataset.description, 'Description')

    def test_update_dataset(self):
        dataset = Config.CLIENT.dataset(_make_dataset_name('update_dataset'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        self.assertTrue(dataset.exists())
        after = [grant for grant in dataset.access_grants
                 if grant.entity_id != 'projectWriters']
        dataset.access_grants = after

        retry_403(dataset.update)()

        self.assertEqual(len(dataset.access_grants), len(after))
        for found, expected in zip(dataset.access_grants, after):
            self.assertEqual(found.role, expected.role)
            self.assertEqual(found.entity_type, expected.entity_type)
            self.assertEqual(found.entity_id, expected.entity_id)

    def test_list_datasets(self):
        datasets_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        for dataset_name in datasets_to_create:
            dataset = Config.CLIENT.dataset(dataset_name)
            retry_403(dataset.create)()
            self.to_delete.append(dataset)

        # Retrieve the datasets.
        iterator = Config.CLIENT.list_datasets()
        all_datasets = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [dataset for dataset in all_datasets
                   if dataset.name in datasets_to_create and
                   dataset.project == Config.CLIENT.project]
        self.assertEqual(len(created), len(datasets_to_create))

    def test_create_table(self):
        dataset = Config.CLIENT.dataset(_make_dataset_name('create_table'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        TABLE_NAME = 'test_table'
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        self.assertFalse(table.exists())
        table.create()
        self.to_delete.insert(0, table)
        self.assertTrue(table.exists())
        self.assertEqual(table.name, TABLE_NAME)

    def test_list_tables(self):
        DATASET_NAME = _make_dataset_name('list_tables')
        dataset = Config.CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        # Retrieve tables before any are created for the dataset.
        iterator = dataset.list_tables()
        all_tables = list(iterator)
        self.assertEqual(all_tables, [])
        self.assertIsNone(iterator.next_page_token)

        # Insert some tables to be listed.
        tables_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        for table_name in tables_to_create:
            table = dataset.table(table_name, schema=[full_name, age])
            table.create()
            self.to_delete.insert(0, table)

        # Retrieve the tables.
        iterator = dataset.list_tables()
        all_tables = list(iterator)
        self.assertIsNone(iterator.next_page_token)
        created = [table for table in all_tables
                   if (table.name in tables_to_create and
                       table.dataset_name == DATASET_NAME)]
        self.assertEqual(len(created), len(tables_to_create))

    def test_patch_table(self):
        dataset = Config.CLIENT.dataset(_make_dataset_name('patch_table'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        TABLE_NAME = 'test_table'
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        self.assertFalse(table.exists())
        table.create()
        self.to_delete.insert(0, table)
        self.assertTrue(table.exists())
        self.assertIsNone(table.friendly_name)
        self.assertIsNone(table.description)
        table.patch(friendly_name='Friendly', description='Description')
        self.assertEqual(table.friendly_name, 'Friendly')
        self.assertEqual(table.description, 'Description')

    def test_update_table(self):
        dataset = Config.CLIENT.dataset(_make_dataset_name('update_table'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        TABLE_NAME = 'test_table'
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        self.assertFalse(table.exists())
        table.create()
        self.to_delete.insert(0, table)
        self.assertTrue(table.exists())
        voter = bigquery.SchemaField('voter', 'BOOLEAN', mode='NULLABLE')
        schema = table.schema
        schema.append(voter)
        table.schema = schema
        table.update()
        self.assertEqual(len(table.schema), len(schema))
        for found, expected in zip(table.schema, schema):
            self.assertEqual(found.name, expected.name)
            self.assertEqual(found.field_type, expected.field_type)
            self.assertEqual(found.mode, expected.mode)

    @staticmethod
    def _fetch_single_page(table):
        import six

        iterator = table.fetch_data()
        page = six.next(iterator.pages)
        return list(page)

    def test_insert_data_then_dump_table(self):
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
        dataset = Config.CLIENT.dataset(
            _make_dataset_name('insert_data_then_dump'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        TABLE_NAME = 'test_table'
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        now = bigquery.SchemaField('now', 'TIMESTAMP')
        table = dataset.table(TABLE_NAME, schema=[full_name, age, now])
        self.assertFalse(table.exists())
        table.create()
        self.to_delete.insert(0, table)
        self.assertTrue(table.exists())

        errors = table.insert_data(ROWS, ROW_IDS)
        self.assertEqual(len(errors), 0)

        rows = ()

        # Allow for "warm up" before rows visible.  See:
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)

        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(rows, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_local_file_then_dump_table(self):
        import csv
        import tempfile
        ROWS = [
            ('Phred Phlyntstone', 32),
            ('Bharney Rhubble', 33),
            ('Wylma Phlyntstone', 29),
            ('Bhettye Rhubble', 27),
        ]
        TABLE_NAME = 'test_table'

        dataset = Config.CLIENT.dataset(
            _make_dataset_name('load_local_then_dump'))

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        table.create()
        self.to_delete.insert(0, table)

        with tempfile.NamedTemporaryFile(mode='w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('Full Name', 'Age'))
            writer.writerows(ROWS)
            csv_file.flush()

            with open(csv_file.name, 'rb') as csv_read:
                job = table.upload_from_file(
                    csv_read,
                    source_format='CSV',
                    skip_leading_rows=1,
                    create_disposition='CREATE_NEVER',
                    write_disposition='WRITE_EMPTY',
                )

        def _job_done(instance):
            return instance.state.lower() == 'done'

        # Retry until done.
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        self.assertEqual(job.output_rows, len(ROWS))

        rows = self._fetch_single_page(table)
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(rows, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_storage_then_dump_table(self):
        import csv
        import tempfile
        from google.cloud.storage import Client as StorageClient
        local_id = unique_resource_id()
        BUCKET_NAME = 'bq_load_test' + local_id
        BLOB_NAME = 'person_ages.csv'
        GS_URL = 'gs://%s/%s' % (BUCKET_NAME, BLOB_NAME)
        ROWS = [
            ('Phred Phlyntstone', 32),
            ('Bharney Rhubble', 33),
            ('Wylma Phlyntstone', 29),
            ('Bhettye Rhubble', 27),
        ]
        TABLE_NAME = 'test_table'

        s_client = StorageClient()

        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        bucket = s_client.create_bucket(BUCKET_NAME)
        self.to_delete.append(bucket)

        blob = bucket.blob(BLOB_NAME)

        with tempfile.TemporaryFile(mode='w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('Full Name', 'Age'))
            writer.writerows(ROWS)
            blob.upload_from_file(
                csv_file, rewind=True, content_type='text/csv')

        self.to_delete.insert(0, blob)

        dataset = Config.CLIENT.dataset(
            _make_dataset_name('load_gcs_then_dump'))

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        table.create()
        self.to_delete.insert(0, table)

        job = Config.CLIENT.load_table_from_storage(
            'bq_load_storage_test_' + local_id, table, GS_URL)
        job.create_disposition = 'CREATE_NEVER'
        job.skip_leading_rows = 1
        job.source_format = 'CSV'
        job.write_disposition = 'WRITE_EMPTY'

        job.begin()

        def _job_done(instance):
            return instance.state in ('DONE', 'done')

        # Allow for 90 seconds of "warm up" before rows visible.  See:
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
        # 8 tries -> 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds
        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        rows = self._fetch_single_page(table)
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(rows, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_job_cancel(self):
        DATASET_NAME = _make_dataset_name('job_cancel')
        JOB_NAME = 'fetch_' + DATASET_NAME
        TABLE_NAME = 'test_table'
        QUERY = 'SELECT * FROM %s.%s' % (DATASET_NAME, TABLE_NAME)

        dataset = Config.CLIENT.dataset(DATASET_NAME)

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        table.create()
        self.to_delete.insert(0, table)

        job = Config.CLIENT.run_async_query(JOB_NAME, QUERY)
        job.begin()
        job.cancel()

        def _job_done(instance):
            return instance.state in ('DONE', 'done')

        retry = RetryInstanceState(_job_done, max_tries=8)
        retry(job.reload)()

        # The `cancel` API doesn't leave any reliable traces on
        # the status of the job resource, so we can't really assert for
        # them here.  The best we can do is not that the API call didn't
        # raise an error, and that the job completed (in the `retry()`
        # above).

    def test_sync_query_w_legacy_sql_types(self):
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        stamp = '%s %s' % (naive.date().isoformat(), naive.time().isoformat())
        zoned = naive.replace(tzinfo=UTC)
        EXAMPLES = [
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
        for example in EXAMPLES:
            query = Config.CLIENT.run_sync_query(example['sql'])
            query.use_legacy_sql = True
            query.run()
            self.assertEqual(len(query.rows), 1)
            self.assertEqual(len(query.rows[0]), 1)
            self.assertEqual(query.rows[0][0], example['expected'])

    def test_sync_query_w_standard_sql_types(self):
        naive = datetime.datetime(2016, 12, 5, 12, 41, 9)
        stamp = '%s %s' % (naive.date().isoformat(), naive.time().isoformat())
        zoned = naive.replace(tzinfo=UTC)
        EXAMPLES = [
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
                'sql': 'SELECT DATETIME(TIMESTAMP "%s")' % (stamp,),
                'expected': naive,
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
        for example in EXAMPLES:
            query = Config.CLIENT.run_sync_query(example['sql'])
            query.use_legacy_sql = False
            query.run()
            self.assertEqual(len(query.rows), 1)
            self.assertEqual(len(query.rows[0]), 1)
            self.assertEqual(query.rows[0][0], example['expected'])

    def test_sync_query_w_query_params(self):
        from google.cloud.bigquery._helpers import ArrayQueryParameter
        from google.cloud.bigquery._helpers import ScalarQueryParameter
        from google.cloud.bigquery._helpers import StructQueryParameter
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
        EXAMPLES = [
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
        for example in EXAMPLES:
            query = Config.CLIENT.run_sync_query(
                example['sql'],
                query_parameters=example['query_parameters'])
            query.use_legacy_sql = False
            query.run()
            self.assertEqual(len(query.rows), 1)
            self.assertEqual(len(query.rows[0]), 1)
            self.assertEqual(query.rows[0][0], example['expected'])

    def test_dump_table_w_public_data(self):
        PUBLIC = 'bigquery-public-data'
        DATASET_NAME = 'samples'
        TABLE_NAME = 'natality'

        dataset = Config.CLIENT.dataset(DATASET_NAME, project=PUBLIC)
        table = dataset.table(TABLE_NAME)
        self._fetch_single_page(table)

    def test_insert_nested_nested(self):
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
        table_name = 'test_table'
        dataset = Config.CLIENT.dataset(
            _make_dataset_name('issue_2951'))

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        table = dataset.table(table_name, schema=schema)
        table.create()
        self.to_delete.insert(0, table)

        table.insert_data(to_insert)

        retry = RetryResult(_has_rows, max_tries=8)
        rows = retry(self._fetch_single_page)(table)

        self.assertEqual(rows, to_insert)

    def test_create_table_insert_fetch_nested_schema(self):

        table_name = 'test_table'
        dataset = Config.CLIENT.dataset(
            _make_dataset_name('create_table_nested_schema'))
        self.assertFalse(dataset.exists())

        retry_403(dataset.create)()
        self.to_delete.append(dataset)

        schema = _load_json_schema()
        table = dataset.table(table_name, schema=schema)
        table.create()
        self.to_delete.insert(0, table)
        self.assertTrue(table.exists())
        self.assertEqual(table.name, table_name)

        to_insert = []
        # Data is in "JSON Lines" format, see http://jsonlines.org/
        json_filename = os.path.join(WHERE, 'data', 'characters.jsonl')
        with open(json_filename) as rows_file:
            for line in rows_file:
                mapping = json.loads(line)
                to_insert.append(
                    tuple(mapping[field.name] for field in schema))

        errors = table.insert_data(to_insert)
        self.assertEqual(len(errors), 0)

        retry = RetryResult(_has_rows, max_tries=8)
        fetched = retry(self._fetch_single_page)(table)
        self.assertEqual(len(fetched), len(to_insert))

        for found, expected in zip(sorted(fetched), sorted(to_insert)):
            self.assertEqual(found[0], expected[0])            # Name
            self.assertEqual(found[1], int(expected[1]))       # Age
            self.assertEqual(found[2], expected[2])            # Weight
            self.assertEqual(found[3], expected[3])            # IsMagic

            self.assertEqual(len(found[4]), len(expected[4]))  # Spells
            for f_spell, e_spell in zip(found[4], expected[4]):
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

            parts = time.strptime(expected[5], '%H:%M:%S')
            e_teatime = datetime.time(*parts[3:6])
            self.assertEqual(found[5], e_teatime)              # TeaTime

            parts = time.strptime(expected[6], '%Y-%m-%d')
            e_nextvac = datetime.date(*parts[0:3])
            self.assertEqual(found[6], e_nextvac)              # NextVacation

            parts = time.strptime(expected[7], '%Y-%m-%dT%H:%M:%S')
            e_favtime = datetime.datetime(*parts[0:6])
            self.assertEqual(found[7], e_favtime)              # FavoriteTime
