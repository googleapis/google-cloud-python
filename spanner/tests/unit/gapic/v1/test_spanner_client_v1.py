# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests."""

import mock
import pytest

from google.cloud.spanner_v1.gapic import spanner_client as spanner_v1
from google.cloud.spanner_v1.proto import keys_pb2
from google.cloud.spanner_v1.proto import result_set_pb2
from google.cloud.spanner_v1.proto import spanner_pb2
from google.cloud.spanner_v1.proto import transaction_pb2
from google.protobuf import empty_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)

    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSpannerClient(object):
    def test_create_session(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = spanner_pb2.Session(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        response = client.create_session(database)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.CreateSessionRequest(database=database)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_session_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.create_session(database)

    def test_batch_create_sessions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_pb2.BatchCreateSessionsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        response = client.batch_create_sessions(database)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.BatchCreateSessionsRequest(database=database)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_sessions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.batch_create_sessions(database)

    def test_get_session(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = spanner_pb2.Session(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        name = client.session_path("[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]")

        response = client.get_session(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.GetSessionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_session_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        name = client.session_path("[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]")

        with pytest.raises(CustomException):
            client.get_session(name)

    def test_list_sessions(self):
        # Setup Expected Response
        next_page_token = ""
        sessions_element = {}
        sessions = [sessions_element]
        expected_response = {"next_page_token": next_page_token, "sessions": sessions}
        expected_response = spanner_pb2.ListSessionsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        paged_list_response = client.list_sessions(database)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.sessions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ListSessionsRequest(database=database)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_sessions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        paged_list_response = client.list_sessions(database)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_session(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        name = client.session_path("[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]")

        client.delete_session(name)

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.DeleteSessionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_session_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        name = client.session_path("[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]")

        with pytest.raises(CustomException):
            client.delete_session(name)

    def test_execute_sql(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = result_set_pb2.ResultSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        response = client.execute_sql(session, sql)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ExecuteSqlRequest(session=session, sql=sql)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_execute_sql_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        with pytest.raises(CustomException):
            client.execute_sql(session, sql)

    def test_execute_streaming_sql(self):
        # Setup Expected Response
        chunked_value = True
        resume_token = b"103"
        expected_response = {
            "chunked_value": chunked_value,
            "resume_token": resume_token,
        }
        expected_response = result_set_pb2.PartialResultSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        response = client.execute_streaming_sql(session, sql)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ExecuteSqlRequest(session=session, sql=sql)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_execute_streaming_sql_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        with pytest.raises(CustomException):
            client.execute_streaming_sql(session, sql)

    def test_execute_batch_dml(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_pb2.ExecuteBatchDmlResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        transaction = {}
        statements = []
        seqno = 109325920

        response = client.execute_batch_dml(session, transaction, statements, seqno)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ExecuteBatchDmlRequest(
            session=session, transaction=transaction, statements=statements, seqno=seqno
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_execute_batch_dml_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        transaction = {}
        statements = []
        seqno = 109325920

        with pytest.raises(CustomException):
            client.execute_batch_dml(session, transaction, statements, seqno)

    def test_read(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = result_set_pb2.ResultSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        columns = []
        key_set = {}

        response = client.read(session, table, columns, key_set)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ReadRequest(
            session=session, table=table, columns=columns, key_set=key_set
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_read_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        columns = []
        key_set = {}

        with pytest.raises(CustomException):
            client.read(session, table, columns, key_set)

    def test_streaming_read(self):
        # Setup Expected Response
        chunked_value = True
        resume_token = b"103"
        expected_response = {
            "chunked_value": chunked_value,
            "resume_token": resume_token,
        }
        expected_response = result_set_pb2.PartialResultSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        columns = []
        key_set = {}

        response = client.streaming_read(session, table, columns, key_set)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.ReadRequest(
            session=session, table=table, columns=columns, key_set=key_set
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_streaming_read_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        columns = []
        key_set = {}

        with pytest.raises(CustomException):
            client.streaming_read(session, table, columns, key_set)

    def test_begin_transaction(self):
        # Setup Expected Response
        id_ = b"27"
        expected_response = {"id": id_}
        expected_response = transaction_pb2.Transaction(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        options_ = {}

        response = client.begin_transaction(session, options_)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.BeginTransactionRequest(
            session=session, options=options_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_begin_transaction_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        options_ = {}

        with pytest.raises(CustomException):
            client.begin_transaction(session, options_)

    def test_commit(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_pb2.CommitResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        mutations = []

        response = client.commit(session, mutations)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.CommitRequest(
            session=session, mutations=mutations
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_commit_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        mutations = []

        with pytest.raises(CustomException):
            client.commit(session, mutations)

    def test_rollback(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        transaction_id = b"28"

        client.rollback(session, transaction_id)

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.RollbackRequest(
            session=session, transaction_id=transaction_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_rollback_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        transaction_id = b"28"

        with pytest.raises(CustomException):
            client.rollback(session, transaction_id)

    def test_partition_query(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_pb2.PartitionResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        response = client.partition_query(session, sql)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.PartitionQueryRequest(session=session, sql=sql)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_partition_query_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        sql = "sql114126"

        with pytest.raises(CustomException):
            client.partition_query(session, sql)

    def test_partition_read(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_pb2.PartitionResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup Request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        key_set = {}

        response = client.partition_read(session, table, key_set)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_pb2.PartitionReadRequest(
            session=session, table=table, key_set=key_set
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_partition_read_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_v1.SpannerClient()

        # Setup request
        session = client.session_path(
            "[PROJECT]", "[INSTANCE]", "[DATABASE]", "[SESSION]"
        )
        table = "table110115790"
        key_set = {}

        with pytest.raises(CustomException):
            client.partition_read(session, table, key_set)
