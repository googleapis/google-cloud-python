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

from google.rpc import status_pb2

from google.cloud import dataproc_v1beta2
from google.cloud.dataproc_v1beta2.proto import clusters_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


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


class TestClusterControllerClient(object):
    def test_create_cluster(self):
        # Setup Expected Response
        project_id_2 = "projectId2939242356"
        cluster_name = "clusterName-1018081872"
        cluster_uuid = "clusterUuid-1017854240"
        expected_response = {
            "project_id": project_id_2,
            "cluster_name": cluster_name,
            "cluster_uuid": cluster_uuid,
        }
        expected_response = clusters_pb2.Cluster(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster = {}

        response = client.create_cluster(project_id, region, cluster)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.CreateClusterRequest(
            project_id=project_id, region=region, cluster=cluster
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_cluster_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_cluster_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster = {}

        response = client.create_cluster(project_id, region, cluster)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_update_cluster(self):
        # Setup Expected Response
        project_id_2 = "projectId2939242356"
        cluster_name_2 = "clusterName2875867491"
        cluster_uuid = "clusterUuid-1017854240"
        expected_response = {
            "project_id": project_id_2,
            "cluster_name": cluster_name_2,
            "cluster_uuid": cluster_uuid,
        }
        expected_response = clusters_pb2.Cluster(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"
        cluster = {}
        update_mask = {}

        response = client.update_cluster(
            project_id, region, cluster_name, cluster, update_mask
        )
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.UpdateClusterRequest(
            project_id=project_id,
            region=region,
            cluster_name=cluster_name,
            cluster=cluster,
            update_mask=update_mask,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_cluster_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_update_cluster_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"
        cluster = {}
        update_mask = {}

        response = client.update_cluster(
            project_id, region, cluster_name, cluster, update_mask
        )
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_cluster(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_delete_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        response = client.delete_cluster(project_id, region, cluster_name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.DeleteClusterRequest(
            project_id=project_id, region=region, cluster_name=cluster_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_cluster_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_cluster_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        response = client.delete_cluster(project_id, region, cluster_name)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_cluster(self):
        # Setup Expected Response
        project_id_2 = "projectId2939242356"
        cluster_name_2 = "clusterName2875867491"
        cluster_uuid = "clusterUuid-1017854240"
        expected_response = {
            "project_id": project_id_2,
            "cluster_name": cluster_name_2,
            "cluster_uuid": cluster_uuid,
        }
        expected_response = clusters_pb2.Cluster(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        response = client.get_cluster(project_id, region, cluster_name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.GetClusterRequest(
            project_id=project_id, region=region, cluster_name=cluster_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        with pytest.raises(CustomException):
            client.get_cluster(project_id, region, cluster_name)

    def test_list_clusters(self):
        # Setup Expected Response
        next_page_token = ""
        clusters_element = {}
        clusters = [clusters_element]
        expected_response = {"next_page_token": next_page_token, "clusters": clusters}
        expected_response = clusters_pb2.ListClustersResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"

        paged_list_response = client.list_clusters(project_id, region)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.clusters[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.ListClustersRequest(
            project_id=project_id, region=region
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_clusters_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"

        paged_list_response = client.list_clusters(project_id, region)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_diagnose_cluster(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_diagnose_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        response = client.diagnose_cluster(project_id, region, cluster_name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = clusters_pb2.DiagnoseClusterRequest(
            project_id=project_id, region=region, cluster_name=cluster_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_diagnose_cluster_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_diagnose_cluster_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.ClusterControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        cluster_name = "clusterName-1018081872"

        response = client.diagnose_cluster(project_id, region, cluster_name)
        exception = response.exception()
        assert exception.errors[0] == error
