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


class TestBigQuery(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_dataset(self):
        DATASET_NAME = 'system_tests'
        dataset = CLIENT.dataset(DATASET_NAME)
        self.assertFalse(dataset.exists())
        dataset.create()
        self.to_delete.append(dataset)
        self.assertTrue(dataset.exists())
        self.assertEqual(dataset.name, DATASET_NAME)

    def test_reload_dataset(self):
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
        DATASET_NAME = 'system_tests'
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
