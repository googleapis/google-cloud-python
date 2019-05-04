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

from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.proto import workflow_templates_pb2
from google.longrunning import operations_pb2
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


class TestWorkflowTemplateServiceClient(object):
    def test_create_workflow_template(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        version = 351608024
        expected_response = {"id": id_, "name": name, "version": version}
        expected_response = workflow_templates_pb2.WorkflowTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")
        template = {}

        response = client.create_workflow_template(parent, template)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.CreateWorkflowTemplateRequest(
            parent=parent, template=template
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_workflow_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup request
        parent = client.region_path("[PROJECT]", "[REGION]")
        template = {}

        with pytest.raises(CustomException):
            client.create_workflow_template(parent, template)

    def test_get_workflow_template(self):
        # Setup Expected Response
        id_ = "id3355"
        name_2 = "name2-1052831874"
        version = 351608024
        expected_response = {"id": id_, "name": name_2, "version": version}
        expected_response = workflow_templates_pb2.WorkflowTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        response = client.get_workflow_template(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.GetWorkflowTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_workflow_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        with pytest.raises(CustomException):
            client.get_workflow_template(name)

    def test_instantiate_workflow_template(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_instantiate_workflow_template", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        response = client.instantiate_workflow_template(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.InstantiateWorkflowTemplateRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_instantiate_workflow_template_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_instantiate_workflow_template_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        response = client.instantiate_workflow_template(name)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_instantiate_inline_workflow_template(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_instantiate_inline_workflow_template", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")
        template = {}

        response = client.instantiate_inline_workflow_template(parent, template)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.InstantiateInlineWorkflowTemplateRequest(
            parent=parent, template=template
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_instantiate_inline_workflow_template_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_instantiate_inline_workflow_template_exception",
            done=True,
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")
        template = {}

        response = client.instantiate_inline_workflow_template(parent, template)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_update_workflow_template(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        version = 351608024
        expected_response = {"id": id_, "name": name, "version": version}
        expected_response = workflow_templates_pb2.WorkflowTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        template = {}

        response = client.update_workflow_template(template)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.UpdateWorkflowTemplateRequest(
            template=template
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_workflow_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup request
        template = {}

        with pytest.raises(CustomException):
            client.update_workflow_template(template)

    def test_list_workflow_templates(self):
        # Setup Expected Response
        next_page_token = ""
        templates_element = {}
        templates = [templates_element]
        expected_response = {"next_page_token": next_page_token, "templates": templates}
        expected_response = workflow_templates_pb2.ListWorkflowTemplatesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")

        paged_list_response = client.list_workflow_templates(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.templates[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.ListWorkflowTemplatesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_workflow_templates_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup request
        parent = client.region_path("[PROJECT]", "[REGION]")

        paged_list_response = client.list_workflow_templates(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_workflow_template(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup Request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        client.delete_workflow_template(name)

        assert len(channel.requests) == 1
        expected_request = workflow_templates_pb2.DeleteWorkflowTemplateRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_workflow_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.WorkflowTemplateServiceClient()

        # Setup request
        name = client.workflow_template_path(
            "[PROJECT]", "[REGION]", "[WORKFLOW_TEMPLATE]"
        )

        with pytest.raises(CustomException):
            client.delete_workflow_template(name)
