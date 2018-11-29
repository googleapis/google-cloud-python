# Copyright 2018 Google LLC
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

import pytest

from google.cloud import datastore_v1
from google.cloud.datastore_v1 import enums
from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import entity_pb2


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


class CustomException(Exception):
    pass


class TestDatastoreClient(object):
    def test_lookup(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datastore_pb2.LookupResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        keys = []

        response = client.lookup(project_id, keys)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.LookupRequest(project_id=project_id, keys=keys)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_lookup_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        keys = []

        with pytest.raises(CustomException):
            client.lookup(project_id, keys)

    def test_run_query(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datastore_pb2.RunQueryResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        partition_id = {}

        response = client.run_query(project_id, partition_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.RunQueryRequest(
            project_id=project_id, partition_id=partition_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_query_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        partition_id = {}

        with pytest.raises(CustomException):
            client.run_query(project_id, partition_id)

    def test_begin_transaction(self):
        # Setup Expected Response
        transaction = b"-34"
        expected_response = {"transaction": transaction}
        expected_response = datastore_pb2.BeginTransactionResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"

        response = client.begin_transaction(project_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.BeginTransactionRequest(project_id=project_id)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_begin_transaction_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"

        with pytest.raises(CustomException):
            client.begin_transaction(project_id)

    def test_commit(self):
        # Setup Expected Response
        index_updates = 1425228195
        expected_response = {"index_updates": index_updates}
        expected_response = datastore_pb2.CommitResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        mode = enums.CommitRequest.Mode.MODE_UNSPECIFIED
        mutations = []

        response = client.commit(project_id, mode, mutations)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.CommitRequest(
            project_id=project_id, mode=mode, mutations=mutations
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_commit_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        mode = enums.CommitRequest.Mode.MODE_UNSPECIFIED
        mutations = []

        with pytest.raises(CustomException):
            client.commit(project_id, mode, mutations)

    def test_rollback(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datastore_pb2.RollbackResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        transaction = b"-34"

        response = client.rollback(project_id, transaction)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.RollbackRequest(
            project_id=project_id, transaction=transaction
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_rollback_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        transaction = b"-34"

        with pytest.raises(CustomException):
            client.rollback(project_id, transaction)

    def test_allocate_ids(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datastore_pb2.AllocateIdsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        keys = []

        response = client.allocate_ids(project_id, keys)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.AllocateIdsRequest(
            project_id=project_id, keys=keys
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_allocate_ids_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        keys = []

        with pytest.raises(CustomException):
            client.allocate_ids(project_id, keys)

    def test_reserve_ids(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datastore_pb2.ReserveIdsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup Request
        project_id = "projectId-1969970175"
        keys = []

        response = client.reserve_ids(project_id, keys)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datastore_pb2.ReserveIdsRequest(
            project_id=project_id, keys=keys
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_reserve_ids_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = datastore_v1.DatastoreClient(channel=channel)

        # Setup request
        project_id = "projectId-1969970175"
        keys = []

        with pytest.raises(CustomException):
            client.reserve_ids(project_id, keys)
