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

from google.cloud import billing_budgets_v1beta1
from google.cloud.billing_budgets_v1beta1.proto import budget_model_pb2
from google.cloud.billing_budgets_v1beta1.proto import budget_service_pb2
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


class TestBudgetServiceClient(object):
    def test_create_budget(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name, "display_name": display_name, "etag": etag}
        expected_response = budget_model_pb2.Budget(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup Request
        parent = client.billing_account_path("[BILLING_ACCOUNT]")
        budget = {}

        response = client.create_budget(parent, budget)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = budget_service_pb2.CreateBudgetRequest(
            parent=parent, budget=budget
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_budget_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup request
        parent = client.billing_account_path("[BILLING_ACCOUNT]")
        budget = {}

        with pytest.raises(CustomException):
            client.create_budget(parent, budget)

    def test_update_budget(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name, "display_name": display_name, "etag": etag}
        expected_response = budget_model_pb2.Budget(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup Request
        budget = {}

        response = client.update_budget(budget)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = budget_service_pb2.UpdateBudgetRequest(budget=budget)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_budget_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup request
        budget = {}

        with pytest.raises(CustomException):
            client.update_budget(budget)

    def test_get_budget(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name_2, "display_name": display_name, "etag": etag}
        expected_response = budget_model_pb2.Budget(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup Request
        name = client.budget_path("[BILLING_ACCOUNT]", "[BUDGET]")

        response = client.get_budget(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = budget_service_pb2.GetBudgetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_budget_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup request
        name = client.budget_path("[BILLING_ACCOUNT]", "[BUDGET]")

        with pytest.raises(CustomException):
            client.get_budget(name)

    def test_list_budgets(self):
        # Setup Expected Response
        next_page_token = ""
        budgets_element = {}
        budgets = [budgets_element]
        expected_response = {"next_page_token": next_page_token, "budgets": budgets}
        expected_response = budget_service_pb2.ListBudgetsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup Request
        parent = client.billing_account_path("[BILLING_ACCOUNT]")

        paged_list_response = client.list_budgets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.budgets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = budget_service_pb2.ListBudgetsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_budgets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup request
        parent = client.billing_account_path("[BILLING_ACCOUNT]")

        paged_list_response = client.list_budgets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_budget(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup Request
        name = client.budget_path("[BILLING_ACCOUNT]", "[BUDGET]")

        client.delete_budget(name)

        assert len(channel.requests) == 1
        expected_request = budget_service_pb2.DeleteBudgetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_budget_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_budgets_v1beta1.BudgetServiceClient()

        # Setup request
        name = client.budget_path("[BILLING_ACCOUNT]", "[BUDGET]")

        with pytest.raises(CustomException):
            client.delete_budget(name)
