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

from google.cloud import bigtable_admin_v2
from google.cloud.bigtable_admin_v2 import enums
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2
from google.cloud.bigtable_admin_v2.proto import instance_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestBigtableInstanceAdminClient(object):
    def test_create_instance(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = instance_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instance_id = "instanceId-2101995259"
        instance = {}
        clusters = {}

        response = client.create_instance(parent, instance_id, instance, clusters)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.CreateInstanceRequest(
            parent=parent, instance_id=instance_id, instance=instance, clusters=clusters
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_instance_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_instance_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instance_id = "instanceId-2101995259"
        instance = {}
        clusters = {}

        response = client.create_instance(parent, instance_id, instance, clusters)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_instance(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = instance_pb2.Instance(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        response = client.get_instance(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.GetInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.get_instance(name)

    def test_list_instances(self):
        # Setup Expected Response
        next_page_token = "nextPageToken-1530815211"
        expected_response = {"next_page_token": next_page_token}
        expected_response = bigtable_instance_admin_pb2.ListInstancesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        response = client.list_instances(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.ListInstancesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_instances_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        with pytest.raises(CustomException):
            client.list_instances(parent)

    def test_update_instance(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name_2 = "displayName21615000987"
        expected_response = {"name": name_2, "display_name": display_name_2}
        expected_response = instance_pb2.Instance(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")
        display_name = "displayName1615086568"
        type_ = enums.Instance.Type.TYPE_UNSPECIFIED
        labels = {}

        response = client.update_instance(name, display_name, type_, labels)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = instance_pb2.Instance(
            name=name, display_name=display_name, type=type_, labels=labels
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")
        display_name = "displayName1615086568"
        type_ = enums.Instance.Type.TYPE_UNSPECIFIED
        labels = {}

        with pytest.raises(CustomException):
            client.update_instance(name, display_name, type_, labels)

    def test_partial_update_instance(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = instance_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_partial_update_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        instance = {}
        update_mask = {}

        response = client.partial_update_instance(instance, update_mask)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.PartialUpdateInstanceRequest(
            instance=instance, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_partial_update_instance_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_partial_update_instance_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        instance = {}
        update_mask = {}

        response = client.partial_update_instance(instance, update_mask)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_instance(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        client.delete_instance(name)

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.DeleteInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.delete_instance(name)

    def test_create_cluster(self):
        # Setup Expected Response
        name = "name3373707"
        location = "location1901043637"
        serve_nodes = 1288838783
        expected_response = {
            "name": name,
            "location": location,
            "serve_nodes": serve_nodes,
        }
        expected_response = instance_pb2.Cluster(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        cluster_id = "clusterId240280960"
        cluster = {}

        response = client.create_cluster(parent, cluster_id, cluster)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.CreateClusterRequest(
            parent=parent, cluster_id=cluster_id, cluster=cluster
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
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        cluster_id = "clusterId240280960"
        cluster = {}

        response = client.create_cluster(parent, cluster_id, cluster)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_cluster(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        location = "location1901043637"
        serve_nodes = 1288838783
        expected_response = {
            "name": name_2,
            "location": location,
            "serve_nodes": serve_nodes,
        }
        expected_response = instance_pb2.Cluster(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        response = client.get_cluster(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.GetClusterRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        with pytest.raises(CustomException):
            client.get_cluster(name)

    def test_list_clusters(self):
        # Setup Expected Response
        next_page_token = "nextPageToken-1530815211"
        expected_response = {"next_page_token": next_page_token}
        expected_response = bigtable_instance_admin_pb2.ListClustersResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        response = client.list_clusters(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.ListClustersRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_clusters_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.list_clusters(parent)

    def test_update_cluster(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        location = "location1901043637"
        serve_nodes_2 = 1623486220
        expected_response = {
            "name": name_2,
            "location": location,
            "serve_nodes": serve_nodes_2,
        }
        expected_response = instance_pb2.Cluster(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_cluster", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")
        serve_nodes = 1288838783

        response = client.update_cluster(name, serve_nodes)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = instance_pb2.Cluster(name=name, serve_nodes=serve_nodes)
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
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")
        serve_nodes = 1288838783

        response = client.update_cluster(name, serve_nodes)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_cluster(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        client.delete_cluster(name)

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.DeleteClusterRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        with pytest.raises(CustomException):
            client.delete_cluster(name)

    def test_create_app_profile(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        description = "description-1724546052"
        expected_response = {"name": name, "etag": etag, "description": description}
        expected_response = instance_pb2.AppProfile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        app_profile_id = "appProfileId1262094415"
        app_profile = {}

        response = client.create_app_profile(parent, app_profile_id, app_profile)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.CreateAppProfileRequest(
            parent=parent, app_profile_id=app_profile_id, app_profile=app_profile
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_app_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        app_profile_id = "appProfileId1262094415"
        app_profile = {}

        with pytest.raises(CustomException):
            client.create_app_profile(parent, app_profile_id, app_profile)

    def test_get_app_profile(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        description = "description-1724546052"
        expected_response = {"name": name_2, "etag": etag, "description": description}
        expected_response = instance_pb2.AppProfile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.app_profile_path("[PROJECT]", "[INSTANCE]", "[APP_PROFILE]")

        response = client.get_app_profile(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.GetAppProfileRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_app_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.app_profile_path("[PROJECT]", "[INSTANCE]", "[APP_PROFILE]")

        with pytest.raises(CustomException):
            client.get_app_profile(name)

    def test_list_app_profiles(self):
        # Setup Expected Response
        next_page_token = ""
        app_profiles_element = {}
        app_profiles = [app_profiles_element]
        expected_response = {
            "next_page_token": next_page_token,
            "app_profiles": app_profiles,
        }
        expected_response = bigtable_instance_admin_pb2.ListAppProfilesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_app_profiles(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.app_profiles[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.ListAppProfilesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_app_profiles_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_app_profiles(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_app_profile(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        description = "description-1724546052"
        expected_response = {"name": name, "etag": etag, "description": description}
        expected_response = instance_pb2.AppProfile(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_app_profile", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        app_profile = {}
        update_mask = {}

        response = client.update_app_profile(app_profile, update_mask)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.UpdateAppProfileRequest(
            app_profile=app_profile, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_app_profile_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_update_app_profile_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        app_profile = {}
        update_mask = {}

        response = client.update_app_profile(app_profile, update_mask)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_app_profile(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        name = client.app_profile_path("[PROJECT]", "[INSTANCE]", "[APP_PROFILE]")
        ignore_warnings = True

        client.delete_app_profile(name, ignore_warnings)

        assert len(channel.requests) == 1
        expected_request = bigtable_instance_admin_pb2.DeleteAppProfileRequest(
            name=name, ignore_warnings=ignore_warnings
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_app_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        name = client.app_profile_path("[PROJECT]", "[INSTANCE]", "[APP_PROFILE]")
        ignore_warnings = True

        with pytest.raises(CustomException):
            client.delete_app_profile(name, ignore_warnings)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"etag3123477"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")

        response = client.get_iam_policy(resource)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"etag3123477"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
        policy = {}

        response = client.set_iam_policy(resource, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_test_iam_permissions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
        permissions = []

        response = client.test_iam_permissions(resource, permissions)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableInstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
