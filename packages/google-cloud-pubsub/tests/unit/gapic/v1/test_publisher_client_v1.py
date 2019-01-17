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

from google.cloud.pubsub_v1.gapic import publisher_client
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestPublisherClient(object):
    def test_create_topic(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = pubsub_pb2.Topic(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        name = client.topic_path("[PROJECT]", "[TOPIC]")

        response = client.create_topic(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.Topic(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_topic_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        name = client.topic_path("[PROJECT]", "[TOPIC]")

        with pytest.raises(CustomException):
            client.create_topic(name)

    def test_update_topic(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = pubsub_pb2.Topic(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        topic = {}
        update_mask = {}

        response = client.update_topic(topic, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.UpdateTopicRequest(
            topic=topic, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_topic_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        topic = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_topic(topic, update_mask)

    def test_publish(self):
        # Setup Expected Response
        message_ids_element = "messageIdsElement-744837059"
        message_ids = [message_ids_element]
        expected_response = {"message_ids": message_ids}
        expected_response = pubsub_pb2.PublishResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")
        data = b"-86"
        messages_element = {"data": data}
        messages = [messages_element]

        response = client.publish(topic, messages)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.PublishRequest(topic=topic, messages=messages)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_publish_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")
        data = b"-86"
        messages_element = {"data": data}
        messages = [messages_element]

        with pytest.raises(CustomException):
            client.publish(topic, messages)

    def test_get_topic(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = pubsub_pb2.Topic(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        response = client.get_topic(topic)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.GetTopicRequest(topic=topic)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_topic_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        with pytest.raises(CustomException):
            client.get_topic(topic)

    def test_list_topics(self):
        # Setup Expected Response
        next_page_token = ""
        topics_element = {}
        topics = [topics_element]
        expected_response = {"next_page_token": next_page_token, "topics": topics}
        expected_response = pubsub_pb2.ListTopicsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        project = client.project_path("[PROJECT]")

        paged_list_response = client.list_topics(project)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.topics[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ListTopicsRequest(project=project)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_topics_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        project = client.project_path("[PROJECT]")

        paged_list_response = client.list_topics(project)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_topic_subscriptions(self):
        # Setup Expected Response
        next_page_token = ""
        subscriptions_element = "subscriptionsElement1698708147"
        subscriptions = [subscriptions_element]
        expected_response = {
            "next_page_token": next_page_token,
            "subscriptions": subscriptions,
        }
        expected_response = pubsub_pb2.ListTopicSubscriptionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        paged_list_response = client.list_topic_subscriptions(topic)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.subscriptions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ListTopicSubscriptionsRequest(topic=topic)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_topic_subscriptions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        paged_list_response = client.list_topic_subscriptions(topic)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_topic(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup Request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        client.delete_topic(topic)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.DeleteTopicRequest(topic=topic)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_topic_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = publisher_client.PublisherClient()

        # Setup request
        topic = client.topic_path("[PROJECT]", "[TOPIC]")

        with pytest.raises(CustomException):
            client.delete_topic(topic)

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
            client = publisher_client.PublisherClient()

        # Setup Request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")
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
            client = publisher_client.PublisherClient()

        # Setup request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

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
            client = publisher_client.PublisherClient()

        # Setup Request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")

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
            client = publisher_client.PublisherClient()

        # Setup request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

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
            client = publisher_client.PublisherClient()

        # Setup Request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")
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
            client = publisher_client.PublisherClient()

        # Setup request
        resource = client.topic_path("[PROJECT]", "[TOPIC]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
