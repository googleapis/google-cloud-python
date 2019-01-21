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

from google.cloud import securitycenter_v1beta1
from google.cloud.securitycenter_v1beta1 import enums
from google.cloud.securitycenter_v1beta1.proto import finding_pb2
from google.cloud.securitycenter_v1beta1.proto import organization_settings_pb2
from google.cloud.securitycenter_v1beta1.proto import security_marks_pb2
from google.cloud.securitycenter_v1beta1.proto import securitycenter_service_pb2
from google.cloud.securitycenter_v1beta1.proto import source_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2


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


class TestSecurityCenterClient(object):
    def test_create_source(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = source_pb2.Source(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")
        source = {}

        response = client.create_source(parent, source)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.CreateSourceRequest(
            parent=parent, source=source
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_source_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.organization_path("[ORGANIZATION]")
        source = {}

        with pytest.raises(CustomException):
            client.create_source(parent, source)

    def test_create_finding(self):
        # Setup Expected Response
        name = "name3373707"
        parent_2 = "parent21175163357"
        resource_name = "resourceName979421212"
        category = "category50511102"
        external_uri = "externalUri-1385596168"
        expected_response = {
            "name": name,
            "parent": parent_2,
            "resource_name": resource_name,
            "category": category,
            "external_uri": external_uri,
        }
        expected_response = finding_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")
        finding_id = "findingId728776081"
        finding = {}

        response = client.create_finding(parent, finding_id, finding)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.CreateFindingRequest(
            parent=parent, finding_id=finding_id, finding=finding
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_finding_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")
        finding_id = "findingId728776081"
        finding = {}

        with pytest.raises(CustomException):
            client.create_finding(parent, finding_id, finding)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")

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
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_get_organization_settings(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        enable_asset_discovery = False
        expected_response = {
            "name": name_2,
            "enable_asset_discovery": enable_asset_discovery,
        }
        expected_response = organization_settings_pb2.OrganizationSettings(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        name = client.organization_settings_path("[ORGANIZATION]")

        response = client.get_organization_settings(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.GetOrganizationSettingsRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_organization_settings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        name = client.organization_settings_path("[ORGANIZATION]")

        with pytest.raises(CustomException):
            client.get_organization_settings(name)

    def test_get_source(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
        }
        expected_response = source_pb2.Source(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        name = client.source_path("[ORGANIZATION]", "[SOURCE]")

        response = client.get_source(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.GetSourceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_source_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        name = client.source_path("[ORGANIZATION]", "[SOURCE]")

        with pytest.raises(CustomException):
            client.get_source(name)

    def test_group_assets(self):
        # Setup Expected Response
        next_page_token = ""
        group_by_results_element = {}
        group_by_results = [group_by_results_element]
        expected_response = {
            "next_page_token": next_page_token,
            "group_by_results": group_by_results,
        }
        expected_response = securitycenter_service_pb2.GroupAssetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")
        group_by = "groupBy506361367"

        paged_list_response = client.group_assets(parent, group_by)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.group_by_results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.GroupAssetsRequest(
            parent=parent, group_by=group_by
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_group_assets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.organization_path("[ORGANIZATION]")
        group_by = "groupBy506361367"

        paged_list_response = client.group_assets(parent, group_by)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_group_findings(self):
        # Setup Expected Response
        next_page_token = ""
        group_by_results_element = {}
        group_by_results = [group_by_results_element]
        expected_response = {
            "next_page_token": next_page_token,
            "group_by_results": group_by_results,
        }
        expected_response = securitycenter_service_pb2.GroupFindingsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")
        group_by = "groupBy506361367"

        paged_list_response = client.group_findings(parent, group_by)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.group_by_results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.GroupFindingsRequest(
            parent=parent, group_by=group_by
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_group_findings_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")
        group_by = "groupBy506361367"

        paged_list_response = client.group_findings(parent, group_by)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_assets(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        list_assets_results_element = {}
        list_assets_results = [list_assets_results_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "list_assets_results": list_assets_results,
        }
        expected_response = securitycenter_service_pb2.ListAssetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")

        paged_list_response = client.list_assets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.list_assets_results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.ListAssetsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_assets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.organization_path("[ORGANIZATION]")

        paged_list_response = client.list_assets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_findings(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        findings_element = {}
        findings = [findings_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "findings": findings,
        }
        expected_response = securitycenter_service_pb2.ListFindingsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")

        paged_list_response = client.list_findings(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.findings[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.ListFindingsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_findings_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.source_path("[ORGANIZATION]", "[SOURCE]")

        paged_list_response = client.list_findings(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_sources(self):
        # Setup Expected Response
        next_page_token = ""
        sources_element = {}
        sources = [sources_element]
        expected_response = {"next_page_token": next_page_token, "sources": sources}
        expected_response = securitycenter_service_pb2.ListSourcesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")

        paged_list_response = client.list_sources(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.sources[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.ListSourcesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_sources_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        parent = client.organization_path("[ORGANIZATION]")

        paged_list_response = client.list_sources(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_run_asset_discovery(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_run_asset_discovery", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")

        response = client.run_asset_discovery(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.RunAssetDiscoveryRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_asset_discovery_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_run_asset_discovery_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        parent = client.organization_path("[ORGANIZATION]")

        response = client.run_asset_discovery(parent)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_set_finding_state(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        parent = "parent-995424086"
        resource_name = "resourceName979421212"
        category = "category50511102"
        external_uri = "externalUri-1385596168"
        expected_response = {
            "name": name_2,
            "parent": parent,
            "resource_name": resource_name,
            "category": category,
            "external_uri": external_uri,
        }
        expected_response = finding_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        name = client.finding_path("[ORGANIZATION]", "[SOURCE]", "[FINDING]")
        state = enums.Finding.State.STATE_UNSPECIFIED
        start_time = {}

        response = client.set_finding_state(name, state, start_time)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.SetFindingStateRequest(
            name=name, state=state, start_time=start_time
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_finding_state_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        name = client.finding_path("[ORGANIZATION]", "[SOURCE]", "[FINDING]")
        state = enums.Finding.State.STATE_UNSPECIFIED
        start_time = {}

        with pytest.raises(CustomException):
            client.set_finding_state(name, state, start_time)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")
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
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")
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
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")
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
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        resource = client.source_path("[ORGANIZATION]", "[SOURCE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)

    def test_update_finding(self):
        # Setup Expected Response
        name = "name3373707"
        parent = "parent-995424086"
        resource_name = "resourceName979421212"
        category = "category50511102"
        external_uri = "externalUri-1385596168"
        expected_response = {
            "name": name,
            "parent": parent,
            "resource_name": resource_name,
            "category": category,
            "external_uri": external_uri,
        }
        expected_response = finding_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        finding = {}

        response = client.update_finding(finding)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.UpdateFindingRequest(
            finding=finding
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_finding_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        finding = {}

        with pytest.raises(CustomException):
            client.update_finding(finding)

    def test_update_organization_settings(self):
        # Setup Expected Response
        name = "name3373707"
        enable_asset_discovery = False
        expected_response = {
            "name": name,
            "enable_asset_discovery": enable_asset_discovery,
        }
        expected_response = organization_settings_pb2.OrganizationSettings(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        organization_settings = {}

        response = client.update_organization_settings(organization_settings)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.UpdateOrganizationSettingsRequest(
            organization_settings=organization_settings
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_organization_settings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        organization_settings = {}

        with pytest.raises(CustomException):
            client.update_organization_settings(organization_settings)

    def test_update_source(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = source_pb2.Source(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        source = {}

        response = client.update_source(source)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.UpdateSourceRequest(source=source)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_source_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        source = {}

        with pytest.raises(CustomException):
            client.update_source(source)

    def test_update_security_marks(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = security_marks_pb2.SecurityMarks(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup Request
        security_marks = {}

        response = client.update_security_marks(security_marks)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = securitycenter_service_pb2.UpdateSecurityMarksRequest(
            security_marks=security_marks
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_security_marks_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = securitycenter_v1beta1.SecurityCenterClient()

        # Setup request
        security_marks = {}

        with pytest.raises(CustomException):
            client.update_security_marks(security_marks)
