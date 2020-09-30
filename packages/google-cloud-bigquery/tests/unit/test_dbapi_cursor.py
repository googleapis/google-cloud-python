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

import operator as op
import unittest

import mock
import six

try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None

from google.api_core import exceptions

try:
    from google.cloud import bigquery_storage
except ImportError:  # pragma: NO COVER
    bigquery_storage = None

from tests.unit.helpers import _to_pyarrow


class TestCursor(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dbapi import Cursor

        return Cursor

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _mock_client(
        self,
        rows=None,
        schema=None,
        num_dml_affected_rows=None,
        default_query_job_config=None,
        dry_run_job=False,
        total_bytes_processed=0,
    ):
        from google.cloud.bigquery import client

        if rows is None:
            total_rows = 0
        else:
            total_rows = len(rows)

        mock_client = mock.create_autospec(client.Client)
        mock_client.query.return_value = self._mock_job(
            total_rows=total_rows,
            schema=schema,
            num_dml_affected_rows=num_dml_affected_rows,
            dry_run=dry_run_job,
            total_bytes_processed=total_bytes_processed,
        )
        mock_client.list_rows.return_value = rows
        mock_client._default_query_job_config = default_query_job_config

        # Assure that the REST client gets used, not the BQ Storage client.
        mock_client._create_bqstorage_client.return_value = None

        return mock_client

    def _mock_bqstorage_client(self, rows=None, stream_count=0):
        if rows is None:
            rows = []

        mock_client = mock.create_autospec(bigquery_storage.BigQueryReadClient)
        mock_read_session = mock.MagicMock(
            streams=[
                bigquery_storage.types.ReadStream(name="streams/stream_{}".format(i))
                for i in range(stream_count)
            ]
        )

        mock_client.create_read_session.return_value = mock_read_session

        mock_rows_stream = mock.MagicMock()
        mock_rows_stream.rows.return_value = iter(rows)
        mock_client.read_rows.return_value = mock_rows_stream

        return mock_client

    def _mock_job(
        self,
        total_rows=0,
        schema=None,
        num_dml_affected_rows=None,
        dry_run=False,
        total_bytes_processed=0,
    ):
        from google.cloud.bigquery import job

        mock_job = mock.create_autospec(job.QueryJob)
        mock_job.error_result = None
        mock_job.state = "DONE"
        mock_job.dry_run = dry_run

        if dry_run:
            mock_job.result.side_effect = exceptions.NotFound
            mock_job.total_bytes_processed = total_bytes_processed
        else:
            mock_job.result.return_value = mock_job
            mock_job._query_results = self._mock_results(
                total_rows=total_rows,
                schema=schema,
                num_dml_affected_rows=num_dml_affected_rows,
            )
            mock_job.destination.to_bqstorage.return_value = (
                "projects/P/datasets/DS/tables/T"
            )

        if num_dml_affected_rows is None:
            mock_job.statement_type = None  # API sends back None for SELECT
        else:
            mock_job.statement_type = "UPDATE"

        return mock_job

    def _mock_results(self, total_rows=0, schema=None, num_dml_affected_rows=None):
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

    def test_raises_error_if_closed(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi.exceptions import ProgrammingError

        connection = connect(self._mock_client())
        cursor = connection.cursor()
        cursor.close()

        method_names = (
            "close",
            "execute",
            "executemany",
            "fetchall",
            "fetchmany",
            "fetchone",
            "setinputsizes",
            "setoutputsize",
        )

        for method in method_names:
            with six.assertRaisesRegex(
                self, ProgrammingError, r"Operating on a closed cursor\."
            ):
                getattr(cursor, method)()

    def test_fetchone_wo_execute_raises_error(self):
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(self._mock_client())
        cursor = connection.cursor()
        self.assertRaises(dbapi.Error, cursor.fetchone)

    def test_fetchone_w_row(self):
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
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

        connection = dbapi.connect(self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        rows = cursor.fetchmany()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (1,))

    def test_fetchmany_w_size(self):
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(
            self._mock_client(rows=[(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        )
        cursor = connection.cursor()
        cursor.execute("SELECT a, b, c;")
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
            self._mock_client(rows=[(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        )
        cursor = connection.cursor()
        cursor.execute("SELECT a, b, c;")
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

        connection = dbapi.connect(self._mock_client(rows=[(1,)]))
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 1)
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (1,))

    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    @unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
    def test_fetchall_w_bqstorage_client_fetch_success(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery import table

        # use unordered data to also test any non-determenistic key order in dicts
        row_data = [
            table.Row([1.4, 1.1, 1.3, 1.2], {"bar": 3, "baz": 2, "foo": 1, "quux": 0}),
            table.Row([2.4, 2.1, 2.3, 2.2], {"bar": 3, "baz": 2, "foo": 1, "quux": 0}),
        ]
        bqstorage_streamed_rows = [
            {
                "bar": _to_pyarrow(1.2),
                "foo": _to_pyarrow(1.1),
                "quux": _to_pyarrow(1.4),
                "baz": _to_pyarrow(1.3),
            },
            {
                "bar": _to_pyarrow(2.2),
                "foo": _to_pyarrow(2.1),
                "quux": _to_pyarrow(2.4),
                "baz": _to_pyarrow(2.3),
            },
        ]

        mock_client = self._mock_client(rows=row_data)
        mock_bqstorage_client = self._mock_bqstorage_client(
            stream_count=1, rows=bqstorage_streamed_rows,
        )

        connection = dbapi.connect(
            client=mock_client, bqstorage_client=mock_bqstorage_client,
        )
        cursor = connection.cursor()
        cursor.execute("SELECT foo, bar FROM some_table")

        rows = cursor.fetchall()

        # the default client was not used
        mock_client.list_rows.assert_not_called()

        # check the data returned
        field_value = op.itemgetter(1)
        sorted_row_data = [sorted(row.items(), key=field_value) for row in rows]
        expected_row_data = [
            [("foo", 1.1), ("bar", 1.2), ("baz", 1.3), ("quux", 1.4)],
            [("foo", 2.1), ("bar", 2.2), ("baz", 2.3), ("quux", 2.4)],
        ]

        self.assertEqual(sorted_row_data, expected_row_data)

    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_fetchall_w_bqstorage_client_fetch_no_rows(self):
        from google.cloud.bigquery import dbapi

        mock_client = self._mock_client(rows=[])
        mock_bqstorage_client = self._mock_bqstorage_client(stream_count=0)

        connection = dbapi.connect(
            client=mock_client, bqstorage_client=mock_bqstorage_client,
        )
        cursor = connection.cursor()
        cursor.execute("SELECT foo, bar FROM some_table")

        rows = cursor.fetchall()

        # # the default client was not used
        mock_client.list_rows.assert_not_called()

        # check the data returned
        self.assertEqual(rows, [])

    @unittest.skipIf(
        bigquery_storage is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_fetchall_w_bqstorage_client_fetch_error_no_fallback(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery import table

        row_data = [table.Row([1.1, 1.2], {"foo": 0, "bar": 1})]

        mock_client = self._mock_client(rows=row_data)
        mock_bqstorage_client = self._mock_bqstorage_client(
            stream_count=1, rows=row_data,
        )
        no_access_error = exceptions.Forbidden("invalid credentials")
        mock_bqstorage_client.create_read_session.side_effect = no_access_error

        connection = dbapi.connect(
            client=mock_client, bqstorage_client=mock_bqstorage_client,
        )
        cursor = connection.cursor()
        cursor.execute("SELECT foo, bar FROM some_table")

        with six.assertRaisesRegex(self, exceptions.Forbidden, "invalid credentials"):
            cursor.fetchall()

        # the default client was not used
        mock_client.list_rows.assert_not_called()

    def test_execute_custom_job_id(self):
        from google.cloud.bigquery.dbapi import connect

        client = self._mock_client(rows=[], num_dml_affected_rows=0)
        connection = connect(client)
        cursor = connection.cursor()
        cursor.execute("SELECT 1;", job_id="foo")
        args, kwargs = client.query.call_args
        self.assertEqual(args[0], "SELECT 1;")
        self.assertEqual(kwargs["job_id"], "foo")

    def test_execute_w_default_config(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery import job

        default_config = job.QueryJobConfig(use_legacy_sql=False, flatten_results=True)
        client = self._mock_client(
            rows=[], num_dml_affected_rows=0, default_query_job_config=default_config
        )
        connection = connect(client)
        cursor = connection.cursor()

        cursor.execute("SELECT 1;", job_id="foo")

        _, kwargs = client.query.call_args
        used_config = kwargs["job_config"]
        expected_config = job.QueryJobConfig(
            use_legacy_sql=False, flatten_results=True, query_parameters=[]
        )
        self.assertEqual(used_config._properties, expected_config._properties)

    def test_execute_custom_job_config_wo_default_config(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery import job

        config = job.QueryJobConfig(use_legacy_sql=True)
        client = self._mock_client(rows=[], num_dml_affected_rows=0)
        connection = connect(client)
        cursor = connection.cursor()
        cursor.execute("SELECT 1;", job_id="foo", job_config=config)
        args, kwargs = client.query.call_args
        self.assertEqual(args[0], "SELECT 1;")
        self.assertEqual(kwargs["job_id"], "foo")
        self.assertEqual(kwargs["job_config"], config)

    def test_execute_custom_job_config_w_default_config(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery import job

        default_config = job.QueryJobConfig(use_legacy_sql=False, flatten_results=True)
        client = self._mock_client(
            rows=[], num_dml_affected_rows=0, default_query_job_config=default_config
        )
        connection = connect(client)
        cursor = connection.cursor()
        config = job.QueryJobConfig(use_legacy_sql=True)

        cursor.execute("SELECT 1;", job_id="foo", job_config=config)

        _, kwargs = client.query.call_args
        used_config = kwargs["job_config"]
        expected_config = job.QueryJobConfig(
            use_legacy_sql=True,  # the config passed to execute() prevails
            flatten_results=True,  # from the default
            query_parameters=[],
        )
        self.assertEqual(used_config._properties, expected_config._properties)

    def test_execute_w_dml(self):
        from google.cloud.bigquery.dbapi import connect

        connection = connect(self._mock_client(rows=[], num_dml_affected_rows=12))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM UserSessions WHERE user_id = 'test';")
        rows = cursor.fetchall()
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 12)
        self.assertEqual(rows, [])

    def test_execute_w_query(self):
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(
            self._mock_client(
                rows=[("hello", "world", 1), ("howdy", "y'all", 2)],
                schema=[
                    SchemaField("a", "STRING", mode="NULLABLE"),
                    SchemaField("b", "STRING", mode="REQUIRED"),
                    SchemaField("c", "INTEGER", mode="NULLABLE"),
                ],
            )
        )
        cursor = connection.cursor()
        cursor.execute("SELECT a, b, c FROM hello_world WHERE d > 3;")

        # Verify the description.
        self.assertEqual(len(cursor.description), 3)
        a_name, a_type, _, _, _, _, a_null_ok = cursor.description[0]
        self.assertEqual(a_name, "a")
        self.assertEqual(a_type, "STRING")
        self.assertEqual(a_type, dbapi.STRING)
        self.assertTrue(a_null_ok)
        b_name, b_type, _, _, _, _, b_null_ok = cursor.description[1]
        self.assertEqual(b_name, "b")
        self.assertEqual(b_type, "STRING")
        self.assertEqual(b_type, dbapi.STRING)
        self.assertFalse(b_null_ok)
        c_name, c_type, _, _, _, _, c_null_ok = cursor.description[2]
        self.assertEqual(c_name, "c")
        self.assertEqual(c_type, "INTEGER")
        self.assertEqual(c_type, dbapi.NUMBER)
        self.assertTrue(c_null_ok)

        # Verify the results.
        self.assertEqual(cursor.rowcount, 2)
        row = cursor.fetchone()
        self.assertEqual(row, ("hello", "world", 1))
        row = cursor.fetchone()
        self.assertEqual(row, ("howdy", "y'all", 2))
        row = cursor.fetchone()
        self.assertIsNone(row)

    def test_execute_w_query_dry_run(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery import dbapi

        connection = dbapi.connect(
            self._mock_client(
                rows=[("hello", "world", 1), ("howdy", "y'all", 2)],
                schema=[
                    SchemaField("a", "STRING", mode="NULLABLE"),
                    SchemaField("b", "STRING", mode="REQUIRED"),
                    SchemaField("c", "INTEGER", mode="NULLABLE"),
                ],
                dry_run_job=True,
                total_bytes_processed=12345,
            )
        )
        cursor = connection.cursor()

        cursor.execute(
            "SELECT a, b, c FROM hello_world WHERE d > 3;",
            job_config=QueryJobConfig(dry_run=True),
        )

        self.assertEqual(cursor.rowcount, 0)
        self.assertIsNone(cursor.description)
        rows = cursor.fetchall()
        self.assertEqual(list(rows), [])

    def test_execute_raises_if_result_raises(self):
        import google.cloud.exceptions

        from google.cloud.bigquery import client
        from google.cloud.bigquery import job
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import exceptions

        job = mock.create_autospec(job.QueryJob)
        job.dry_run = None
        job.result.side_effect = google.cloud.exceptions.GoogleCloudError("")
        client = mock.create_autospec(client.Client)
        client._default_query_job_config = None
        client.query.return_value = job
        connection = connect(client)
        cursor = connection.cursor()

        with self.assertRaises(exceptions.DatabaseError):
            cursor.execute("SELECT 1")

    def test_executemany_w_dml(self):
        from google.cloud.bigquery.dbapi import connect

        connection = connect(self._mock_client(rows=[], num_dml_affected_rows=12))
        cursor = connection.cursor()
        cursor.executemany(
            "DELETE FROM UserSessions WHERE user_id = %s;",
            (("test",), ("anothertest",)),
        )
        self.assertIsNone(cursor.description)
        self.assertEqual(cursor.rowcount, 12)

    def test__format_operation_w_dict(self):
        from google.cloud.bigquery.dbapi import cursor

        formatted_operation = cursor._format_operation(
            "SELECT %(somevalue)s, %(a `weird` one)s;",
            {"somevalue": "hi", "a `weird` one": "world"},
        )
        self.assertEqual(
            formatted_operation, "SELECT @`somevalue`, @`a \\`weird\\` one`;"
        )

    def test__format_operation_w_wrong_dict(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery.dbapi import cursor

        self.assertRaises(
            dbapi.ProgrammingError,
            cursor._format_operation,
            "SELECT %(somevalue)s, %(othervalue)s;",
            {"somevalue-not-here": "hi", "othervalue": "world"},
        )

    def test__format_operation_w_sequence(self):
        from google.cloud.bigquery.dbapi import cursor

        formatted_operation = cursor._format_operation(
            "SELECT %s, %s;", ("hello", "world")
        )
        self.assertEqual(formatted_operation, "SELECT ?, ?;")

    def test__format_operation_w_too_short_sequence(self):
        from google.cloud.bigquery import dbapi
        from google.cloud.bigquery.dbapi import cursor

        self.assertRaises(
            dbapi.ProgrammingError,
            cursor._format_operation,
            "SELECT %s, %s;",
            ("hello",),
        )
