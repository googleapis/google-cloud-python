# Copyright 2017, Google Inc. All rights reserved.
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
"""Unit tests."""

import mock
import unittest

from google.gax import errors

# -----------------------------------------------------------------------------
# Manual change to the GAPIC unit tests because we do not export
# the `SpannerClient` at the usual location because there is a thick wrapper
# around it.
from google.cloud.spanner_v1.gapic import spanner_client as spanner_v1
# -----------------------------------------------------------------------------

from google.cloud.spanner_v1.proto import keys_pb2
from google.cloud.spanner_v1.proto import result_set_pb2
from google.cloud.spanner_v1.proto import spanner_pb2
from google.cloud.spanner_v1.proto import transaction_pb2
from google.protobuf import empty_pb2


class CustomException(Exception):
    pass


class TestSpannerClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_session(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = spanner_pb2.Session(**expected_response)
        grpc_stub.CreateSession.return_value = expected_response

        response = client.create_session(database)
        self.assertEqual(expected_response, response)

        grpc_stub.CreateSession.assert_called_once()
        args, kwargs = grpc_stub.CreateSession.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.CreateSessionRequest(database=database)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_session_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock exception response
        grpc_stub.CreateSession.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.create_session, database)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_session(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                   '[SESSION]')

        # Mock response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = spanner_pb2.Session(**expected_response)
        grpc_stub.GetSession.return_value = expected_response

        response = client.get_session(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetSession.assert_called_once()
        args, kwargs = grpc_stub.GetSession.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.GetSessionRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_session_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                   '[SESSION]')

        # Mock exception response
        grpc_stub.GetSession.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_session, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_session(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                   '[SESSION]')

        client.delete_session(name)

        grpc_stub.DeleteSession.assert_called_once()
        args, kwargs = grpc_stub.DeleteSession.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.DeleteSessionRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_session_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                   '[SESSION]')

        # Mock exception response
        grpc_stub.DeleteSession.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.delete_session, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_execute_sql(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        sql = 'sql114126'

        # Mock response
        expected_response = {}
        expected_response = result_set_pb2.ResultSet(**expected_response)
        grpc_stub.ExecuteSql.return_value = expected_response

        response = client.execute_sql(session, sql)
        self.assertEqual(expected_response, response)

        grpc_stub.ExecuteSql.assert_called_once()
        args, kwargs = grpc_stub.ExecuteSql.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.ExecuteSqlRequest(
            session=session, sql=sql)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_execute_sql_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        sql = 'sql114126'

        # Mock exception response
        grpc_stub.ExecuteSql.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.execute_sql, session, sql)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_execute_streaming_sql(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        sql = 'sql114126'

        # Mock response
        chunked_value = True
        resume_token = b'103'
        expected_response = {
            'chunked_value': chunked_value,
            'resume_token': resume_token
        }
        expected_response = result_set_pb2.PartialResultSet(
            **expected_response)
        grpc_stub.ExecuteStreamingSql.return_value = iter([expected_response])

        response = client.execute_streaming_sql(session, sql)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.ExecuteStreamingSql.assert_called_once()
        args, kwargs = grpc_stub.ExecuteStreamingSql.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.ExecuteSqlRequest(
            session=session, sql=sql)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_execute_streaming_sql_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        sql = 'sql114126'

        # Mock exception response
        grpc_stub.ExecuteStreamingSql.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.execute_streaming_sql,
                          session, sql)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_read(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        table = 'table110115790'
        columns = []
        key_set = {}

        # Mock response
        expected_response = {}
        expected_response = result_set_pb2.ResultSet(**expected_response)
        grpc_stub.Read.return_value = expected_response

        response = client.read(session, table, columns, key_set)
        self.assertEqual(expected_response, response)

        grpc_stub.Read.assert_called_once()
        args, kwargs = grpc_stub.Read.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.ReadRequest(
            session=session, table=table, columns=columns, key_set=key_set)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_read_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        table = 'table110115790'
        columns = []
        key_set = {}

        # Mock exception response
        grpc_stub.Read.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.read, session, table,
                          columns, key_set)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_streaming_read(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        table = 'table110115790'
        columns = []
        key_set = {}

        # Mock response
        chunked_value = True
        resume_token = b'103'
        expected_response = {
            'chunked_value': chunked_value,
            'resume_token': resume_token
        }
        expected_response = result_set_pb2.PartialResultSet(
            **expected_response)
        grpc_stub.StreamingRead.return_value = iter([expected_response])

        response = client.streaming_read(session, table, columns, key_set)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.StreamingRead.assert_called_once()
        args, kwargs = grpc_stub.StreamingRead.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.ReadRequest(
            session=session, table=table, columns=columns, key_set=key_set)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_streaming_read_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        table = 'table110115790'
        columns = []
        key_set = {}

        # Mock exception response
        grpc_stub.StreamingRead.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.streaming_read, session,
                          table, columns, key_set)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_begin_transaction(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        options_ = {}

        # Mock response
        id_ = b'27'
        expected_response = {'id': id_}
        expected_response = transaction_pb2.Transaction(**expected_response)
        grpc_stub.BeginTransaction.return_value = expected_response

        response = client.begin_transaction(session, options_)
        self.assertEqual(expected_response, response)

        grpc_stub.BeginTransaction.assert_called_once()
        args, kwargs = grpc_stub.BeginTransaction.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.BeginTransactionRequest(
            session=session, options=options_)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_begin_transaction_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        options_ = {}

        # Mock exception response
        grpc_stub.BeginTransaction.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.begin_transaction, session,
                          options_)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_commit(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        mutations = []

        # Mock response
        expected_response = {}
        expected_response = spanner_pb2.CommitResponse(**expected_response)
        grpc_stub.Commit.return_value = expected_response

        response = client.commit(session, mutations)
        self.assertEqual(expected_response, response)

        grpc_stub.Commit.assert_called_once()
        args, kwargs = grpc_stub.Commit.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.CommitRequest(
            session=session, mutations=mutations)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_commit_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        mutations = []

        # Mock exception response
        grpc_stub.Commit.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.commit, session, mutations)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_rollback(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        transaction_id = b'28'

        client.rollback(session, transaction_id)

        grpc_stub.Rollback.assert_called_once()
        args, kwargs = grpc_stub.Rollback.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_pb2.RollbackRequest(
            session=session, transaction_id=transaction_id)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_rollback_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_v1.SpannerClient()

        # Mock request
        session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]',
                                      '[SESSION]')
        transaction_id = b'28'

        # Mock exception response
        grpc_stub.Rollback.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.rollback, session,
                          transaction_id)
