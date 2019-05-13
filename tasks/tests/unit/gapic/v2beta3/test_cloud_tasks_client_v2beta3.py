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

from google.cloud import tasks_v2beta3
from google.cloud.tasks_v2beta3.proto import cloudtasks_pb2
from google.cloud.tasks_v2beta3.proto import queue_pb2
from google.cloud.tasks_v2beta3.proto import task_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestCloudTasksClient(object):
    def test_list_queues(self):
        # Setup Expected Response
        next_page_token = ""
        queues_element = {}
        queues = [queues_element]
        expected_response = {"next_page_token": next_page_token, "queues": queues}
        expected_response = cloudtasks_pb2.ListQueuesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_queues(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.queues[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.ListQueuesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_queues_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_queues(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_queue(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        response = client.get_queue(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.GetQueueRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.get_queue(name)

    def test_create_queue(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        queue = {}

        response = client.create_queue(parent, queue)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.CreateQueueRequest(parent=parent, queue=queue)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        queue = {}

        with pytest.raises(CustomException):
            client.create_queue(parent, queue)

    def test_update_queue(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        queue = {}

        response = client.update_queue(queue)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.UpdateQueueRequest(queue=queue)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        queue = {}

        with pytest.raises(CustomException):
            client.update_queue(queue)

    def test_delete_queue(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        client.delete_queue(name)

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.DeleteQueueRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.delete_queue(name)

    def test_purge_queue(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        response = client.purge_queue(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.PurgeQueueRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_purge_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.purge_queue(name)

    def test_pause_queue(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        response = client.pause_queue(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.PauseQueueRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_pause_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.pause_queue(name)

    def test_resume_queue(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = queue_pb2.Queue(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        response = client.resume_queue(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.ResumeQueueRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_resume_queue_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.resume_queue(name)

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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
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
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        resource = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)

    def test_list_tasks(self):
        # Setup Expected Response
        next_page_token = ""
        tasks_element = {}
        tasks = [tasks_element]
        expected_response = {"next_page_token": next_page_token, "tasks": tasks}
        expected_response = cloudtasks_pb2.ListTasksResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        parent = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        paged_list_response = client.list_tasks(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.tasks[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.ListTasksRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_tasks_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        parent = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")

        paged_list_response = client.list_tasks(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_task(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        dispatch_count = 1217252086
        response_count = 424727441
        expected_response = {
            "name": name_2,
            "dispatch_count": dispatch_count,
            "response_count": response_count,
        }
        expected_response = task_pb2.Task(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        response = client.get_task(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.GetTaskRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_task_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        with pytest.raises(CustomException):
            client.get_task(name)

    def test_create_task(self):
        # Setup Expected Response
        name = "name3373707"
        dispatch_count = 1217252086
        response_count = 424727441
        expected_response = {
            "name": name,
            "dispatch_count": dispatch_count,
            "response_count": response_count,
        }
        expected_response = task_pb2.Task(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        parent = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
        task = {}

        response = client.create_task(parent, task)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.CreateTaskRequest(parent=parent, task=task)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_task_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        parent = client.queue_path("[PROJECT]", "[LOCATION]", "[QUEUE]")
        task = {}

        with pytest.raises(CustomException):
            client.create_task(parent, task)

    def test_delete_task(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        client.delete_task(name)

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.DeleteTaskRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_task_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        with pytest.raises(CustomException):
            client.delete_task(name)

    def test_run_task(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        dispatch_count = 1217252086
        response_count = 424727441
        expected_response = {
            "name": name_2,
            "dispatch_count": dispatch_count,
            "response_count": response_count,
        }
        expected_response = task_pb2.Task(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup Request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        response = client.run_task(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudtasks_pb2.RunTaskRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_task_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = tasks_v2beta3.CloudTasksClient()

        # Setup request
        name = client.task_path("[PROJECT]", "[LOCATION]", "[QUEUE]", "[TASK]")

        with pytest.raises(CustomException):
            client.run_task(name)
