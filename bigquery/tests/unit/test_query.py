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


class TestQueryResults(unittest.TestCase):
    PROJECT = 'project'
    JOB_ID = 'test-synchronous-query'
    TOKEN = 'TOKEN'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import QueryResults

        return QueryResults

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _makeResource(self):
        return {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }

    def _verifySchema(self, query, resource):
        from google.cloud.bigquery.schema import SchemaField

        if 'schema' in resource:
            fields = resource['schema']['fields']
            self.assertEqual(len(query.schema), len(fields))
            for found, expected in zip(query.schema, fields):
                self.assertIsInstance(found, SchemaField)
                self.assertEqual(found.name, expected['name'])
                self.assertEqual(found.field_type, expected['type'])
                self.assertEqual(found.mode, expected['mode'])
                self.assertEqual(found.description,
                                 expected.get('description'))
                self.assertEqual(found.fields, expected.get('fields', ()))
        else:
            self.assertEqual(query.schema, ())

    def test_ctor_defaults(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.cache_hit)
        self.assertIsNone(query.complete)
        self.assertIsNone(query.errors)
        self.assertIsNone(query.page_token)
        self.assertEqual(query.project, self.PROJECT)
        self.assertEqual(query.rows, [])
        self.assertEqual(query.schema, ())
        self.assertIsNone(query.total_rows)
        self.assertIsNone(query.total_bytes_processed)

    def test_cache_hit_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.cache_hit)

    def test_cache_hit_present(self):
        resource = self._makeResource()
        resource['cacheHit'] = True
        query = self._make_one(resource)
        self.assertTrue(query.cache_hit)

    def test_complete_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.complete)

    def test_complete_present(self):
        resource = self._makeResource()
        resource['jobComplete'] = True
        query = self._make_one(resource)
        self.assertTrue(query.complete)

    def test_errors_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.errors)

    def test_errors_present(self):
        ERRORS = [
            {'reason': 'testing'},
        ]
        resource = self._makeResource()
        resource['errors'] = ERRORS
        query = self._make_one(resource)
        self.assertEqual(query.errors, ERRORS)

    def test_job_id_missing(self):
        with self.assertRaises(ValueError):
            self._make_one({})

    def test_job_id_broken_job_reference(self):
        resource = {'jobReference': {'bogus': 'BOGUS'}}
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_job_id_present(self):
        resource = self._makeResource()
        resource['jobReference']['jobId'] = 'custom-job'
        query = self._make_one(resource)
        self.assertEqual(query.job_id, 'custom-job')

    def test_page_token_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.page_token)

    def test_page_token_present(self):
        resource = self._makeResource()
        resource['pageToken'] = 'TOKEN'
        query = self._make_one(resource)
        self.assertEqual(query.page_token, 'TOKEN')

    def test_total_rows_present_integer(self):
        resource = self._makeResource()
        resource['totalRows'] = 42
        query = self._make_one(resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_rows_present_string(self):
        resource = self._makeResource()
        resource['totalRows'] = '42'
        query = self._make_one(resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_bytes_processed_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.total_bytes_processed)

    def test_total_bytes_processed_present_integer(self):
        resource = self._makeResource()
        resource['totalBytesProcessed'] = 123456
        query = self._make_one(resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_total_bytes_processed_present_string(self):
        resource = self._makeResource()
        resource['totalBytesProcessed'] = '123456'
        query = self._make_one(resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_num_dml_affected_rows_missing(self):
        query = self._make_one(self._makeResource())
        self.assertIsNone(query.num_dml_affected_rows)

    def test_num_dml_affected_rows_present_integer(self):
        resource = self._makeResource()
        resource['numDmlAffectedRows'] = 123456
        query = self._make_one(resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_num_dml_affected_rows_present_string(self):
        resource = self._makeResource()
        resource['numDmlAffectedRows'] = '123456'
        query = self._make_one(resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_schema(self):
        query = self._make_one(self._makeResource())
        self._verifySchema(query, self._makeResource())
        resource = self._makeResource()
        resource['schema'] = {
            'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
            ],
        }
        query._set_properties(resource)
        self._verifySchema(query, resource)
