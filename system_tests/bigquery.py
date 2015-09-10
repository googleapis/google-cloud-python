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

import operator
import time

import unittest2

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import bigquery


_helpers.PROJECT = TESTS_PROJECT
CLIENT = bigquery.Client()
DATASET_NAME = 'system_tests_%012d' % (1000 * time.time(),)


class TestBigQuery(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_dataset(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
        self.to_delete.append(dataset)
        self.assertTrue(dataset.exists())
        self.assertEqual(dataset.name, DATASET_NAME)

    def test_reload_dataset(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        dataset.friendly_name = 'Friendly'
        dataset.description = 'Description'
        dataset.create()
        self.to_delete.append(dataset)
        other = CLIENT.dataset(DATASET_NAME)
        other.reload()
        self.assertEqual(other.friendly_name, 'Friendly')
        self.assertEqual(other.description, 'Description')

    def test_patch_dataset(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
        self.to_delete.append(dataset)
        self.assertTrue(dataset.exists())
        self.assertEqual(dataset.friendly_name, None)
        self.assertEqual(dataset.description, None)
        dataset.patch(friendly_name='Friendly', description='Description')
        self.assertEqual(dataset.friendly_name, 'Friendly')
        self.assertEqual(dataset.description, 'Description')

    def test_update_dataset(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
        self.to_delete.append(dataset)
        self.assertTrue(dataset.exists())
        after = [grant for grant in dataset.access_grants
                 if grant.entity_id != 'projectWriters']
        dataset.access_grants = after
        dataset.update()
        self.assertEqual(len(dataset.access_grants), len(after))
        for found, expected in zip(dataset.access_grants, after):
            self.assertEqual(found.role, expected.role)
            self.assertEqual(found.entity_type, expected.entity_type)
            self.assertEqual(found.entity_id, expected.entity_id)

    def test_list_datasets(self):
        datasets_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        for dataset_name in datasets_to_create:
            dataset = CLIENT.dataset(dataset_name)
            dataset.create()
            self.to_delete.append(dataset)

        # Retrieve the datasets.
        all_datasets, token = CLIENT.list_datasets()
        self.assertTrue(token is None)
        created = [dataset for dataset in all_datasets
                   if dataset.name in datasets_to_create and
                   dataset.project == CLIENT.project]
        self.assertEqual(len(created), len(datasets_to_create))

    def test_create_table(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
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
        self.assertTrue(table._dataset is dataset)

    def test_list_tables(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
        self.to_delete.append(dataset)
        tables_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        for table_name in tables_to_create:
            table = dataset.table(table_name, schema=[full_name, age])
            table.create()
            self.to_delete.insert(0, table)

        # Retrieve the tables.
        all_tables, token = dataset.list_tables()
        self.assertTrue(token is None)
        created = [table for table in all_tables
                   if table.name in tables_to_create and
                   table._dataset.name == DATASET_NAME]
        self.assertEqual(len(created), len(tables_to_create))

    def test_patch_table(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
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
        self.assertEqual(table.friendly_name, None)
        self.assertEqual(table.description, None)
        table.patch(friendly_name='Friendly', description='Description')
        self.assertEqual(table.friendly_name, 'Friendly')
        self.assertEqual(table.description, 'Description')

    def test_update_table(self):
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
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

    def test_load_table_then_dump_table(self):
        ROWS = [
            ('Phred Phlyntstone', 32),
            ('Bharney Rhubble', 33),
            ('Wylma Phlyntstone', 29),
            ('Bhettye Rhubble', 27),
        ]
        ROW_IDS = range(len(ROWS))
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
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

        errors = table.insert_data(ROWS, ROW_IDS)
        self.assertEqual(len(errors), 0)

        rows = ()
        counter = 9
        # Allow for 90 seconds of "warm up" before rows visible.  See:
        # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability

        while len(rows) == 0 and counter > 0:
            counter -= 1
            rows, _, _ = table.fetch_data()
            if len(rows) == 0:
                time.sleep(10)

        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(rows, key=by_age),
                         sorted(ROWS, key=by_age))

    def test_load_table_from_storage_then_dump_table(self):
        import csv
        import tempfile
        from gcloud.storage import Client as StorageClient
        TIMESTAMP = 1000 * time.time()
        BUCKET_NAME = 'bq_load_test_%d' % (TIMESTAMP,)
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

        dataset = CLIENT.dataset(DATASET_NAME)
        dataset.create()
        self.to_delete.append(dataset)

        full_name = bigquery.SchemaField('full_name', 'STRING',
                                         mode='REQUIRED')
        age = bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table(TABLE_NAME, schema=[full_name, age])
        table.create()
        self.to_delete.insert(0, table)

        job = CLIENT.load_table_from_storage(
            'bq_load_storage_test_%d' % (TIMESTAMP,), table, GS_URL)
        job.create_disposition = 'CREATE_NEVER'
        job.skip_leading_rows = 1
        job.source_format = 'CSV'
        job.write_disposition = 'WRITE_EMPTY'

        job.begin()

        counter = 9  # Allow for 90 seconds of lag.

        while job.state not in ('DONE', 'done') and counter > 0:
            counter -= 1
            job.reload()
            if job.state not in ('DONE', 'done'):
                time.sleep(10)

        self.assertTrue(job.state in ('DONE', 'done'))

        rows, _, _ = table.fetch_data()
        by_age = operator.itemgetter(1)
        self.assertEqual(sorted(rows, key=by_age),
                         sorted(ROWS, key=by_age))
