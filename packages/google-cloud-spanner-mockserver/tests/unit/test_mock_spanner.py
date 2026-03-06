import unittest
from unittest import mock

import google.cloud.spanner_v1.types.result_set as result_set
import google.cloud.spanner_v1.types.spanner as spanner

from spannermockserver.mock_spanner import MockSpanner, SpannerServicer


class TestMockSpannerUnit(unittest.TestCase):
    def setUp(self):
        self.mock_spanner = MockSpanner()
        self.servicer = SpannerServicer()

    def test_mock_spanner_add_get_result(self):
        sql = "SELECT * FROM Users"
        result = result_set.ResultSet()
        self.mock_spanner.add_result(sql, result)

        self.assertEqual(self.mock_spanner.get_result(sql), result)
        self.assertEqual(self.mock_spanner.get_result(sql.upper()), result)

        with self.assertRaises(ValueError):
            self.mock_spanner.get_result("SELECT * FROM NonExistent")

    def test_mock_spanner_add_get_streaming_results(self):
        sql = "SELECT * FROM Users"
        partials = [result_set.PartialResultSet()]
        self.mock_spanner.add_execute_streaming_sql_results(sql, partials)

        # No transaction provided
        results = self.mock_spanner.get_execute_streaming_sql_results(sql, None)
        self.assertEqual(results, partials)

    def test_mock_spanner_add_pop_error(self):
        error = mock.MagicMock()
        method_name = "test_method"

        self.mock_spanner.add_error(method_name, error)

        # We need to simulate the calling frame name matching the method name.
        # Since pop_error uses inspect.currentframe().f_back.f_code.co_name,
        # we can just test if the error is stored and popped properly.
        self.assertIn(method_name, self.mock_spanner.errors)
        self.assertEqual(self.mock_spanner.errors[method_name], error)

        # Test pop_error
        mock_context = mock.MagicMock()

        def test_method():
            self.mock_spanner.pop_error(mock_context)

        test_method()
        mock_context.abort_with_status.assert_called_once_with(error)

    def test_servicer_create_session(self):
        request = mock.MagicMock()
        request.database = "projects/p/instances/i/databases/d"
        request.session = spanner.Session()
        context = mock.MagicMock()

        session = self.servicer.CreateSession(request, context)
        self.assertIn(
            "projects/p/instances/i/databases/d/sessions/1", session.name
        )
        self.assertEqual(self.servicer.session_counter, 1)

    def test_servicer_get_session(self):
        request = mock.MagicMock()
        context = mock.MagicMock()

        session = self.servicer.GetSession(request, context)
        self.assertIsInstance(session, spanner.Session)

    def test_servicer_list_sessions(self):
        request = mock.MagicMock()
        context = mock.MagicMock()

        sessions = self.servicer.ListSessions(request, context)
        self.assertEqual(len(sessions), 1)
        self.assertIsInstance(sessions[0], spanner.Session)

    def test_servicer_delete_session(self):
        request = mock.MagicMock()
        context = mock.MagicMock()

        response = self.servicer.DeleteSession(request, context)
        self.assertIsNotNone(response)

    def test_servicer_execute_sql(self):
        sql = "SELECT 1"
        result = result_set.ResultSet()
        self.servicer.mock_spanner.add_result(sql, result)

        request = mock.MagicMock()
        request.sql = sql
        # Provide an empty transaction options so no transaction is created
        request.transaction.begin = mock.MagicMock()
        request.transaction.begin.__eq__.return_value = True

        context = mock.MagicMock()

        response = self.servicer.ExecuteSql(request, context)
        self.assertEqual(response, result)

    def test_servicer_read(self):
        request = mock.MagicMock()
        context = mock.MagicMock()

        response = self.servicer.Read(request, context)
        self.assertIsInstance(response, result_set.ResultSet)
