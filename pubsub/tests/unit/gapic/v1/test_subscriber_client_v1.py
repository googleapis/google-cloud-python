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

import pytest

from google.cloud.pubsub_v1.gapic import subscriber_client
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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)

    def stream_stream(self,
                      method,
                      request_serializer=None,
                      response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSubscriberClient(object):
    def test_create_subscription(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        topic_2 = 'topic2-1139259102'
        ack_deadline_seconds = 2135351438
        retain_acked_messages = False
        expected_response = {
            'name': name_2,
            'topic': topic_2,
            'ack_deadline_seconds': ack_deadline_seconds,
            'retain_acked_messages': retain_acked_messages
        }
        expected_response = pubsub_pb2.Subscription(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        name = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        topic = client.topic_path('[PROJECT]', '[TOPIC]')

        response = client.create_subscription(name, topic)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.Subscription(name=name, topic=topic)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        name = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        topic = client.topic_path('[PROJECT]', '[TOPIC]')

        with pytest.raises(CustomException):
            client.create_subscription(name, topic)

    def test_get_subscription(self):
        # Setup Expected Response
        name = 'name3373707'
        topic = 'topic110546223'
        ack_deadline_seconds = 2135351438
        retain_acked_messages = False
        expected_response = {
            'name': name,
            'topic': topic,
            'ack_deadline_seconds': ack_deadline_seconds,
            'retain_acked_messages': retain_acked_messages
        }
        expected_response = pubsub_pb2.Subscription(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        response = client.get_subscription(subscription)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.GetSubscriptionRequest(
            subscription=subscription)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        with pytest.raises(CustomException):
            client.get_subscription(subscription)

    def test_update_subscription(self):
        # Setup Expected Response
        name = 'name3373707'
        topic = 'topic110546223'
        ack_deadline_seconds = 2135351438
        retain_acked_messages = False
        expected_response = {
            'name': name,
            'topic': topic,
            'ack_deadline_seconds': ack_deadline_seconds,
            'retain_acked_messages': retain_acked_messages
        }
        expected_response = pubsub_pb2.Subscription(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = {}
        update_mask = {}

        response = client.update_subscription(subscription, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.UpdateSubscriptionRequest(
            subscription=subscription, update_mask=update_mask)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_subscription(subscription, update_mask)

    def test_list_subscriptions(self):
        # Setup Expected Response
        next_page_token = ''
        subscriptions_element = {}
        subscriptions = [subscriptions_element]
        expected_response = {
            'next_page_token': next_page_token,
            'subscriptions': subscriptions
        }
        expected_response = pubsub_pb2.ListSubscriptionsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        project = client.project_path('[PROJECT]')

        paged_list_response = client.list_subscriptions(project)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.subscriptions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ListSubscriptionsRequest(project=project)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_subscriptions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        project = client.project_path('[PROJECT]')

        paged_list_response = client.list_subscriptions(project)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_subscription(self):
        channel = ChannelStub()
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        client.delete_subscription(subscription)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.DeleteSubscriptionRequest(
            subscription=subscription)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        with pytest.raises(CustomException):
            client.delete_subscription(subscription)

    def test_modify_ack_deadline(self):
        channel = ChannelStub()
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        ack_ids = []
        ack_deadline_seconds = 2135351438

        client.modify_ack_deadline(subscription, ack_ids, ack_deadline_seconds)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ModifyAckDeadlineRequest(
            subscription=subscription,
            ack_ids=ack_ids,
            ack_deadline_seconds=ack_deadline_seconds)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_ack_deadline_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        ack_ids = []
        ack_deadline_seconds = 2135351438

        with pytest.raises(CustomException):
            client.modify_ack_deadline(subscription, ack_ids,
                                       ack_deadline_seconds)

    def test_acknowledge(self):
        channel = ChannelStub()
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        ack_ids = []

        client.acknowledge(subscription, ack_ids)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.AcknowledgeRequest(
            subscription=subscription, ack_ids=ack_ids)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_acknowledge_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        ack_ids = []

        with pytest.raises(CustomException):
            client.acknowledge(subscription, ack_ids)

    def test_pull(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = pubsub_pb2.PullResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        max_messages = 496131527

        response = client.pull(subscription, max_messages)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.PullRequest(
            subscription=subscription, max_messages=max_messages)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_pull_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        max_messages = 496131527

        with pytest.raises(CustomException):
            client.pull(subscription, max_messages)

    def test_streaming_pull(self):
        # Setup Expected Response
        received_messages_element = {}
        received_messages = [received_messages_element]
        expected_response = {'received_messages': received_messages}
        expected_response = pubsub_pb2.StreamingPullResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        stream_ack_deadline_seconds = 1875467245
        request = {
            'subscription': subscription,
            'stream_ack_deadline_seconds': stream_ack_deadline_seconds
        }
        request = pubsub_pb2.StreamingPullRequest(**request)
        requests = [request]

        response = client.streaming_pull(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_streaming_pull_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        stream_ack_deadline_seconds = 1875467245
        request = {
            'subscription': subscription,
            'stream_ack_deadline_seconds': stream_ack_deadline_seconds
        }

        request = pubsub_pb2.StreamingPullRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client.streaming_pull(requests)

    def test_modify_push_config(self):
        channel = ChannelStub()
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        push_config = {}

        client.modify_push_config(subscription, push_config)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ModifyPushConfigRequest(
            subscription=subscription, push_config=push_config)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_push_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        push_config = {}

        with pytest.raises(CustomException):
            client.modify_push_config(subscription, push_config)

    def test_list_snapshots(self):
        # Setup Expected Response
        next_page_token = ''
        snapshots_element = {}
        snapshots = [snapshots_element]
        expected_response = {
            'next_page_token': next_page_token,
            'snapshots': snapshots
        }
        expected_response = pubsub_pb2.ListSnapshotsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        project = client.project_path('[PROJECT]')

        paged_list_response = client.list_snapshots(project)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.snapshots[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.ListSnapshotsRequest(project=project)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_snapshots_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        project = client.project_path('[PROJECT]')

        paged_list_response = client.list_snapshots(project)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_snapshot(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        topic = 'topic110546223'
        expected_response = {'name': name_2, 'topic': topic}
        expected_response = pubsub_pb2.Snapshot(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        name = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        response = client.create_snapshot(name, subscription)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.CreateSnapshotRequest(
            name=name, subscription=subscription)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_snapshot_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        name = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        with pytest.raises(CustomException):
            client.create_snapshot(name, subscription)

    def test_update_snapshot(self):
        # Setup Expected Response
        name = 'name3373707'
        topic = 'topic110546223'
        expected_response = {'name': name, 'topic': topic}
        expected_response = pubsub_pb2.Snapshot(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        snapshot = {}
        update_mask = {}

        response = client.update_snapshot(snapshot, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.UpdateSnapshotRequest(
            snapshot=snapshot, update_mask=update_mask)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_snapshot_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        snapshot = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_snapshot(snapshot, update_mask)

    def test_delete_snapshot(self):
        channel = ChannelStub()
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        snapshot = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')

        client.delete_snapshot(snapshot)

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.DeleteSnapshotRequest(snapshot=snapshot)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_snapshot_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        snapshot = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')

        with pytest.raises(CustomException):
            client.delete_snapshot(snapshot)

    def test_seek(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = pubsub_pb2.SeekResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        response = client.seek(subscription)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = pubsub_pb2.SeekRequest(subscription=subscription)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_seek_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        with pytest.raises(CustomException):
            client.seek(subscription)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        policy = {}

        response = client.set_iam_policy(resource, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        response = client.get_iam_policy(resource)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_test_iam_permissions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup Request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        permissions = []

        response = client.test_iam_permissions(resource, permissions)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = subscriber_client.SubscriberClient(channel=channel)

        # Setup request
        resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
