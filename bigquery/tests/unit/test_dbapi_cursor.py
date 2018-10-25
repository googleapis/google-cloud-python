# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

import mock


class TestCursor(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dbapi import Cursor
        return Cursor

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _mock_client(
            self, rows=None, schema=None, num_dml_affected_rows=None):
        from google.cloud.bigquery import client

        if rows is None:
            total_rows = 0
        else:
            total_rows = len(rows)

        mock_client = mock.create_autospec(client.Client)
        mock_client.query.return_value = self._mock_job(
            total_rows=total_rows,
            schema=schema,
            num_dml_affected_rows=num_dml_affected_rows)
        mock_client.list_rows.return_value = rows
        return mock_client

    def _mock_job(
            self, total_rows=0, schema=None, num_dml_affected_rows=None):
        from google.cloud.bigquery import job
        mock_job = mock.create_autospec(job.QueryJob)
        mock_job.error_result = None
        mock_job.state = 'DONE'
        mock_job.result.return_value = mock_job
        mock_job._query_results = self._mock_results(
            total_rows=total_rows, schema=schema,
            num_dml_affected_rows=num_dml_affected_rows)

        if num_dml_affected_rows is None:
            mock_job.statement_type = None  # API sends back None for SELECT
        else:
            mock_job.statement_type = 'UPDATE'

        return mock_job

    def _mock_results(
            self, total_rows=0, schema=None, num_dml_affected_rows=None):
        from google.cloud.bigquery import query
        mock_results = mock.create_autospec(query._QueryResults)
        mock_results.schema = schema
        mock_results.num_dml_affected_rows = num_dml_affected_rows
        mock_results.total_rows = total_rows
        return mock_results

    def test_ctor(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import Cursor
        connection = connect(self._mock_client())
        cursor = self._make_one(connection)
        self.assertIsInstance(cursor, Cursor)
        self.assertIs(cursor.connection, connection)

    def test_close(self):
        from google.cloud.bigquery.dbapi import connect
        connection = connect(self._mock_client())
        cursor = connection.cursor()
        # close() is a no-op, there is nothing to test.
        cursor.close()

    def test_fetchone_wo_execute_raises_error(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(self._mock_client())
        cursor = connection.cursor()
        self.assertRaises(dbapi.Error, cursor.fetchone)

    def test_fetchone_w_row(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(
            self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute('SELECT 1;')
        row = cursor.fetchone()
        self.assertEqual(row, (1,))
        self.assertIsNone(cursor.fetchone())

    def test_fetchmany_wo_execute_raises_error(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(self._mock_client())
        cursor = connection.cursor()
        self.assertRaises(dbapi.Error, cursor.fetchmany)

    def test_fetchmany_w_row(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(
            self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute('SELECT 1;')
        rows = cursor.fetchmany()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (1,))

    def test_fetchmany_w_size(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(
            self._mock_client(
                rows=[
                    (1, 2, 3),
                    (4, 5, 6),
                    (7, 8, 9),
                ]))
        cursor = connection.cursor()
        cursor.execute('SELECT a, b, c;')
        rows = cursor.fetchmany(size=2)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (1, 2, 3))
        self.assertEqual(rows[1], (4, 5, 6))
        second_page = cursor.fetchmany(size=2)
        self.assertEqual(len(second_page), 1)
        self.assertEqual(second_page[0], (7, 8, 9))
        third_page = cursor.fetchmany(size=2)
        self.assertEqual(third_page, [])

    def test_fetchmany_w_arraysize(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(
            self._mock_client(
                rows=[
                    (1, 2, 3),
                    (4, 5, 6),
                    (7, 8, 9),
                ]))
        cursor = connection.cursor()
        cursor.execute('SELECT a, b, c;')
        cursor.arraysize = 2
        rows = cursor.fetchmany()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (1, 2, 3))
        self.assertEqual(rows[1], (4, 5, 6))
        second_page = cursor.fetchmany()
        self.assertEqual(len(second_page), 1)
        self.assertEqual(second_page[0], (7, 8, 9))
        third_page = cursor.fetchmany()
        self.assertEqual(third_page, [])

    def test_fetchall_wo_execute_raises_error(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(self._mock_client())
        cursor = connection.cursor()
        self.assertRaises(dbapi.Error, cursor.fetchall)

    def test_fetchall_w_row(self):
        from google.cloud.bigquery import dbapi
        connection = dbapi.connect(
            self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute('SELECT 1;')
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 1)
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (1,))

    def test_execute_custom_job_id(self):
        from google.cloud.bigquery.dbapi import connect
        client = self._mock_client(rows=[], num_dml_affected_rows=0)
        connection = connect(client)
        cursor = connection.cursor()
        cursor.execute('SELECT 1;', job_id='foo')
        args, kwargs = client.query.call_args
        self.assertEqual(args[0], 'SELECT 1;')
        self.assertEqual(kwargs['job_id'], 'foo')

    def test_execute_w_dml(self):
        from google.cloud.bigquery.dbapi import connect
        connection = connect(
            self._mock_client(rows=[], num_dml_affected_rows=12))
        cursor = connection.cursor()
        cursor.execute('DELETE FROM UserSessions WHERE user_id = \'test\';')
        rows = cursor.fetchall()
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 12)
        self.assertEqual(rows, [])

    def test_execute_w_query(self):
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(self._mock_client(
            rows=[('hello', 'world', 1), ('howdy', 'y\'all', 2)],
            schema=[
                SchemaField('a', 'STRING', mode='NULLABLE'),
                SchemaField('b', 'STRING', mode='REQUIRED'),
                SchemaField('c', 'INTEGER', mode='NULLABLE')]))
        cursor = connection.cursor()
        cursor.execute('SELECT a, b, c FROM hello_world WHERE d > 3;')

        # Verify the description.
        self.assertEqual(len(cursor.description), 3)
        a_name, a_type, _, _, _, _, a_null_ok = cursor.description[0]
        self.assertEqual(a_name, 'a')
        self.assertEqual(a_type, 'STRING')
        self.assertEqual(a_type, dbapi.STRING)
        self.assertTrue(a_null_ok)
        b_name, b_type, _, _, _, _, b_null_ok = cursor.description[1]
        self.assertEqual(b_name, 'b')
        self.assertEqual(b_type, 'STRING')
        self.assertEqual(b_type, dbapi.STRING)
        self.assertFalse(b_null_ok)
        c_name, c_type, _, _, _, _, c_null_ok = cursor.description[2]
        self.assertEqual(c_name, 'c')
        self.assertEqual(c_type, 'INTEGER')
        self.assertEqual(c_type, dbapi.NUMBER)
        self.assertTrue(c_null_ok)

        # Verify the results.
        self.assertEqual(cursor.rowcount, 2)
        row = cursor.fetchone()
        self.assertEqual(row, ('hello', 'world', 1))
        row = cursor.fetchone()
        self.assertEqual(row, ('howdy', 'y\'all', 2))
        row = cursor.fetchone()
        self.assertIsNone(row)

    def test_execute_raises_if_result_raises(self):
        import google.cloud.exceptions

        from google.cloud.bigquery import client
        from google.cloud.bigquery import job
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import exceptions

        job = mock.create_autospec(job.QueryJob)
        job.result.side_effect = google.cloud.exceptions.GoogleCloudError('')
        client = mock.create_autospec(client.Client)
        client.query.return_value = job
        connection = connect(client)
        cursor = connection.cursor()

        with self.assertRaises(exceptions.DatabaseError):
            cursor.execute('SELECT 1')

    def test_executemany_w_dml(self):
        from google.cloud.bigquery.dbapi import connect
        connection = connect(
            self._mock_client(rows=[], num_dml_affected_rows=12))
        cursor = connection.cursor()
        cursor.executemany(
            'DELETE FROM UserSessions WHERE user_id = %s;',
            (('test',), ('anothertest',)))
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 12)

    def test__format_operation_w_dict(self):
        from google.cloud.bigquery.dbapi import cursor
        formatted_operation = cursor._format_operation(
            'SELECT %(somevalue)s, %(a `weird` one)s;',
            {
                'somevalue': 'hi',
                'a `weird` one': 'world',
            })
        self.assertEqual(
            formatted_operation, 'SELECT @`somevalue`, @`a \\`weird\\` one`;')

    def test__format_operation_w_wrong_dict(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery.dbapi import cursor
        self.assertRaises(
            dbapi.ProgrammingError,
            cursor._format_operation,
            'SELECT %(somevalue)s, %(othervalue)s;',
            {
                'somevalue-not-here': 'hi',
                'othervalue': 'world',
            })

    def test__format_operation_w_sequence(self):
        from google.cloud.bigquery.dbapi import cursor
        formatted_operation = cursor._format_operation(
            'SELECT %s, %s;', ('hello', 'world'))
        self.assertEqual(formatted_operation, 'SELECT ?, ?;')

    def test__format_operation_w_too_short_sequence(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery.dbapi import cursor
        self.assertRaises(
            dbapi.ProgrammingError,
            cursor._format_operation,
            'SELECT %s, %s;',
            ('hello',))
