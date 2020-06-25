# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud import container_v1
from google.cloud.container_v1 import enums
from google.cloud.container_v1.proto import cluster_service_pb2
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


class CustomException(Exception):
    pass


class TestClusterManagerClient(object):
    def test_delete_cluster(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.delete_cluster()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.DeleteClusterRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.delete_cluster()

    def test_delete_node_pool(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.delete_node_pool()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.DeleteNodePoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_node_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.delete_node_pool()

    def test_list_clusters(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cluster_service_pb2.ListClustersResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.list_clusters()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.ListClustersRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_clusters_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.list_clusters()

    def test_get_cluster(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        initial_node_count = 1682564205
        logging_service = "loggingService-1700501035"
        monitoring_service = "monitoringService1469270462"
        network = "network1843485230"
        cluster_ipv4_cidr = "clusterIpv4Cidr-141875831"
        subnetwork = "subnetwork-1302785042"
        enable_kubernetes_alpha = False
        label_fingerprint = "labelFingerprint714995737"
        self_link = "selfLink-1691268851"
        zone = "zone3744684"
        endpoint = "endpoint1741102485"
        initial_cluster_version = "initialClusterVersion-276373352"
        current_master_version = "currentMasterVersion-920953983"
        current_node_version = "currentNodeVersion-407476063"
        create_time = "createTime-493574096"
        status_message = "statusMessage-239442758"
        node_ipv4_cidr_size = 1181176815
        services_ipv4_cidr = "servicesIpv4Cidr1966438125"
        current_node_count = 178977560
        expire_time = "expireTime-96179731"
        location = "location1901043637"
        enable_tpu = False
        tpu_ipv4_cidr_block = "tpuIpv4CidrBlock1137906646"
        expected_response = {
            "name": name,
            "description": description,
            "initial_node_count": initial_node_count,
            "logging_service": logging_service,
            "monitoring_service": monitoring_service,
            "network": network,
            "cluster_ipv4_cidr": cluster_ipv4_cidr,
            "subnetwork": subnetwork,
            "enable_kubernetes_alpha": enable_kubernetes_alpha,
            "label_fingerprint": label_fingerprint,
            "self_link": self_link,
            "zone": zone,
            "endpoint": endpoint,
            "initial_cluster_version": initial_cluster_version,
            "current_master_version": current_master_version,
            "current_node_version": current_node_version,
            "create_time": create_time,
            "status_message": status_message,
            "node_ipv4_cidr_size": node_ipv4_cidr_size,
            "services_ipv4_cidr": services_ipv4_cidr,
            "current_node_count": current_node_count,
            "expire_time": expire_time,
            "location": location,
            "enable_tpu": enable_tpu,
            "tpu_ipv4_cidr_block": tpu_ipv4_cidr_block,
        }
        expected_response = cluster_service_pb2.Cluster(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.get_cluster()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.GetClusterRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.get_cluster()

    def test_create_cluster(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        cluster = {}

        response = client.create_cluster(cluster)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.CreateClusterRequest(cluster=cluster)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        cluster = {}

        with pytest.raises(CustomException):
            client.create_cluster(cluster)

    def test_update_cluster(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        update = {}

        response = client.update_cluster(update)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.UpdateClusterRequest(update=update)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_cluster_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        update = {}

        with pytest.raises(CustomException):
            client.update_cluster(update)

    def test_update_node_pool(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        node_version = "nodeVersion1790136219"
        image_type = "imageType-1442758754"

        response = client.update_node_pool(node_version, image_type)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.UpdateNodePoolRequest(
            node_version=node_version, image_type=image_type
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_node_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        node_version = "nodeVersion1790136219"
        image_type = "imageType-1442758754"

        with pytest.raises(CustomException):
            client.update_node_pool(node_version, image_type)

    def test_set_node_pool_autoscaling(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        autoscaling = {}

        response = client.set_node_pool_autoscaling(autoscaling)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetNodePoolAutoscalingRequest(
            autoscaling=autoscaling
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_node_pool_autoscaling_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        autoscaling = {}

        with pytest.raises(CustomException):
            client.set_node_pool_autoscaling(autoscaling)

    def test_set_logging_service(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        logging_service = "loggingService-1700501035"

        response = client.set_logging_service(logging_service)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetLoggingServiceRequest(
            logging_service=logging_service
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_logging_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        logging_service = "loggingService-1700501035"

        with pytest.raises(CustomException):
            client.set_logging_service(logging_service)

    def test_set_monitoring_service(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        monitoring_service = "monitoringService1469270462"

        response = client.set_monitoring_service(monitoring_service)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetMonitoringServiceRequest(
            monitoring_service=monitoring_service
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_monitoring_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        monitoring_service = "monitoringService1469270462"

        with pytest.raises(CustomException):
            client.set_monitoring_service(monitoring_service)

    def test_set_addons_config(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        addons_config = {}

        response = client.set_addons_config(addons_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetAddonsConfigRequest(
            addons_config=addons_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_addons_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        addons_config = {}

        with pytest.raises(CustomException):
            client.set_addons_config(addons_config)

    def test_set_locations(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        locations = []

        response = client.set_locations(locations)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetLocationsRequest(locations=locations)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_locations_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        locations = []

        with pytest.raises(CustomException):
            client.set_locations(locations)

    def test_update_master(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        master_version = "masterVersion-2139460613"

        response = client.update_master(master_version)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.UpdateMasterRequest(
            master_version=master_version
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_master_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        master_version = "masterVersion-2139460613"

        with pytest.raises(CustomException):
            client.update_master(master_version)

    def test_set_master_auth(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        action = enums.SetMasterAuthRequest.Action.UNKNOWN
        update = {}

        response = client.set_master_auth(action, update)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetMasterAuthRequest(
            action=action, update=update
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_master_auth_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        action = enums.SetMasterAuthRequest.Action.UNKNOWN
        update = {}

        with pytest.raises(CustomException):
            client.set_master_auth(action, update)

    def test_list_operations(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cluster_service_pb2.ListOperationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.list_operations()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.ListOperationsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_operations_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.list_operations()

    def test_get_operation(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.get_operation()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.GetOperationRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_operation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.get_operation()

    def test_cancel_operation(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        client.cancel_operation()

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.CancelOperationRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_cancel_operation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.cancel_operation()

    def test_get_server_config(self):
        # Setup Expected Response
        default_cluster_version = "defaultClusterVersion111003029"
        default_image_type = "defaultImageType-918225828"
        expected_response = {
            "default_cluster_version": default_cluster_version,
            "default_image_type": default_image_type,
        }
        expected_response = cluster_service_pb2.ServerConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.get_server_config()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.GetServerConfigRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_server_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.get_server_config()

    def test_list_node_pools(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cluster_service_pb2.ListNodePoolsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.list_node_pools()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.ListNodePoolsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_node_pools_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.list_node_pools()

    def test_get_node_pool(self):
        # Setup Expected Response
        name = "name3373707"
        initial_node_count = 1682564205
        self_link = "selfLink-1691268851"
        version = "version351608024"
        status_message = "statusMessage-239442758"
        pod_ipv4_cidr_size = 1098768716
        expected_response = {
            "name": name,
            "initial_node_count": initial_node_count,
            "self_link": self_link,
            "version": version,
            "status_message": status_message,
            "pod_ipv4_cidr_size": pod_ipv4_cidr_size,
        }
        expected_response = cluster_service_pb2.NodePool(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.get_node_pool()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.GetNodePoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_node_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.get_node_pool()

    def test_create_node_pool(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        node_pool = {}

        response = client.create_node_pool(node_pool)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.CreateNodePoolRequest(
            node_pool=node_pool
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_node_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        node_pool = {}

        with pytest.raises(CustomException):
            client.create_node_pool(node_pool)

    def test_rollback_node_pool_upgrade(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.rollback_node_pool_upgrade()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.RollbackNodePoolUpgradeRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_rollback_node_pool_upgrade_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.rollback_node_pool_upgrade()

    def test_set_node_pool_management(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        management = {}

        response = client.set_node_pool_management(management)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetNodePoolManagementRequest(
            management=management
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_node_pool_management_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        management = {}

        with pytest.raises(CustomException):
            client.set_node_pool_management(management)

    def test_set_labels(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        resource_labels = {}
        label_fingerprint = "labelFingerprint714995737"

        response = client.set_labels(resource_labels, label_fingerprint)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetLabelsRequest(
            resource_labels=resource_labels, label_fingerprint=label_fingerprint
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_labels_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        resource_labels = {}
        label_fingerprint = "labelFingerprint714995737"

        with pytest.raises(CustomException):
            client.set_labels(resource_labels, label_fingerprint)

    def test_set_legacy_abac(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        enabled = False

        response = client.set_legacy_abac(enabled)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetLegacyAbacRequest(enabled=enabled)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_legacy_abac_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        enabled = False

        with pytest.raises(CustomException):
            client.set_legacy_abac(enabled)

    def test_start_i_p_rotation(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.start_i_p_rotation()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.StartIPRotationRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_start_i_p_rotation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.start_i_p_rotation()

    def test_complete_i_p_rotation(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        response = client.complete_i_p_rotation()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.CompleteIPRotationRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_complete_i_p_rotation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        with pytest.raises(CustomException):
            client.complete_i_p_rotation()

    def test_set_node_pool_size(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        node_count = 1539922066

        response = client.set_node_pool_size(node_count)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetNodePoolSizeRequest(
            node_count=node_count
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_node_pool_size_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        node_count = 1539922066

        with pytest.raises(CustomException):
            client.set_node_pool_size(node_count)

    def test_set_network_policy(self):
        # Setup Expected Response
        name = "name3373707"
        zone = "zone3744684"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        network_policy = {}

        response = client.set_network_policy(network_policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetNetworkPolicyRequest(
            network_policy=network_policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_network_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        network_policy = {}

        with pytest.raises(CustomException):
            client.set_network_policy(network_policy)

    def test_set_maintenance_policy(self):
        # Setup Expected Response
        name = "name3373707"
        zone_2 = "zone2-696322977"
        detail = "detail-1335224239"
        status_message = "statusMessage-239442758"
        self_link = "selfLink-1691268851"
        target_link = "targetLink-2084812312"
        location = "location1901043637"
        start_time = "startTime-1573145462"
        end_time = "endTime1725551537"
        expected_response = {
            "name": name,
            "zone": zone_2,
            "detail": detail,
            "status_message": status_message,
            "self_link": self_link,
            "target_link": target_link,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
        }
        expected_response = cluster_service_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        zone = "zone3744684"
        cluster_id = "clusterId240280960"
        maintenance_policy = {}

        response = client.set_maintenance_policy(
            project_id, zone, cluster_id, maintenance_policy
        )
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.SetMaintenancePolicyRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            maintenance_policy=maintenance_policy,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_maintenance_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        # Setup request
        project_id = "projectId-1969970175"
        zone = "zone3744684"
        cluster_id = "clusterId240280960"
        maintenance_policy = {}

        with pytest.raises(CustomException):
            client.set_maintenance_policy(
                project_id, zone, cluster_id, maintenance_policy
            )

    def test_list_usable_subnetworks(self):
        # Setup Expected Response
        next_page_token = ""
        subnetworks_element = {}
        subnetworks = [subnetworks_element]
        expected_response = {
            "next_page_token": next_page_token,
            "subnetworks": subnetworks,
        }
        expected_response = cluster_service_pb2.ListUsableSubnetworksResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        paged_list_response = client.list_usable_subnetworks()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.subnetworks[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cluster_service_pb2.ListUsableSubnetworksRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_usable_subnetworks_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = container_v1.ClusterManagerClient()

        paged_list_response = client.list_usable_subnetworks()
        with pytest.raises(CustomException):
            list(paged_list_response)
