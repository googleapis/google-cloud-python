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

from google.rpc import status_pb2

from google.cloud.devtools import cloudbuild_v1
from google.cloud.devtools.cloudbuild_v1.proto import cloudbuild_pb2
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


class TestCloudBuildClient(object):
    def test_list_builds(self):
        # Setup Expected Response
        next_page_token = ""
        builds_element = {}
        builds = [builds_element]
        expected_response = {"next_page_token": next_page_token, "builds": builds}
        expected_response = cloudbuild_pb2.ListBuildsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_builds(project_id)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.builds[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.ListBuildsRequest(project_id=project_id)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_builds_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_builds(project_id)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_build_trigger(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"

        client.delete_build_trigger(project_id, trigger_id)

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.DeleteBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_build_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"

        with pytest.raises(CustomException):
            client.delete_build_trigger(project_id, trigger_id)

    def test_create_build(self):
        # Setup Expected Response
        id_ = "id3355"
        project_id_2 = "projectId2939242356"
        status_detail = "statusDetail2089931070"
        logs_bucket = "logsBucket1565363834"
        build_trigger_id = "buildTriggerId1105559411"
        log_url = "logUrl342054388"
        expected_response = {
            "id": id_,
            "project_id": project_id_2,
            "status_detail": status_detail,
            "logs_bucket": logs_bucket,
            "build_trigger_id": build_trigger_id,
            "log_url": log_url,
        }
        expected_response = cloudbuild_pb2.Build(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_build", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        build = {}

        response = client.create_build(project_id, build)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.CreateBuildRequest(
            project_id=project_id, build=build
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_build_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_build_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        build = {}

        response = client.create_build(project_id, build)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_build(self):
        # Setup Expected Response
        id_2 = "id23227150"
        project_id_2 = "projectId2939242356"
        status_detail = "statusDetail2089931070"
        logs_bucket = "logsBucket1565363834"
        build_trigger_id = "buildTriggerId1105559411"
        log_url = "logUrl342054388"
        expected_response = {
            "id": id_2,
            "project_id": project_id_2,
            "status_detail": status_detail,
            "logs_bucket": logs_bucket,
            "build_trigger_id": build_trigger_id,
            "log_url": log_url,
        }
        expected_response = cloudbuild_pb2.Build(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        response = client.get_build(project_id, id_)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.GetBuildRequest(project_id=project_id, id=id_)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_build_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        with pytest.raises(CustomException):
            client.get_build(project_id, id_)

    def test_cancel_build(self):
        # Setup Expected Response
        id_2 = "id23227150"
        project_id_2 = "projectId2939242356"
        status_detail = "statusDetail2089931070"
        logs_bucket = "logsBucket1565363834"
        build_trigger_id = "buildTriggerId1105559411"
        log_url = "logUrl342054388"
        expected_response = {
            "id": id_2,
            "project_id": project_id_2,
            "status_detail": status_detail,
            "logs_bucket": logs_bucket,
            "build_trigger_id": build_trigger_id,
            "log_url": log_url,
        }
        expected_response = cloudbuild_pb2.Build(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        response = client.cancel_build(project_id, id_)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.CancelBuildRequest(
            project_id=project_id, id=id_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_cancel_build_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        with pytest.raises(CustomException):
            client.cancel_build(project_id, id_)

    def test_retry_build(self):
        # Setup Expected Response
        id_2 = "id23227150"
        project_id_2 = "projectId2939242356"
        status_detail = "statusDetail2089931070"
        logs_bucket = "logsBucket1565363834"
        build_trigger_id = "buildTriggerId1105559411"
        log_url = "logUrl342054388"
        expected_response = {
            "id": id_2,
            "project_id": project_id_2,
            "status_detail": status_detail,
            "logs_bucket": logs_bucket,
            "build_trigger_id": build_trigger_id,
            "log_url": log_url,
        }
        expected_response = cloudbuild_pb2.Build(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_retry_build", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        response = client.retry_build(project_id, id_)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.RetryBuildRequest(
            project_id=project_id, id=id_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_retry_build_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_retry_build_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        id_ = "id3355"

        response = client.retry_build(project_id, id_)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_create_build_trigger(self):
        # Setup Expected Response
        id_ = "id3355"
        description = "description-1724546052"
        name = "name3373707"
        filename = "filename-734768633"
        disabled = True
        expected_response = {
            "id": id_,
            "description": description,
            "name": name,
            "filename": filename,
            "disabled": disabled,
        }
        expected_response = cloudbuild_pb2.BuildTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger = {}

        response = client.create_build_trigger(project_id, trigger)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.CreateBuildTriggerRequest(
            project_id=project_id, trigger=trigger
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_build_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        trigger = {}

        with pytest.raises(CustomException):
            client.create_build_trigger(project_id, trigger)

    def test_get_build_trigger(self):
        # Setup Expected Response
        id_ = "id3355"
        description = "description-1724546052"
        name = "name3373707"
        filename = "filename-734768633"
        disabled = True
        expected_response = {
            "id": id_,
            "description": description,
            "name": name,
            "filename": filename,
            "disabled": disabled,
        }
        expected_response = cloudbuild_pb2.BuildTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"

        response = client.get_build_trigger(project_id, trigger_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.GetBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_build_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"

        with pytest.raises(CustomException):
            client.get_build_trigger(project_id, trigger_id)

    def test_list_build_triggers(self):
        # Setup Expected Response
        next_page_token = ""
        triggers_element = {}
        triggers = [triggers_element]
        expected_response = {"next_page_token": next_page_token, "triggers": triggers}
        expected_response = cloudbuild_pb2.ListBuildTriggersResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_build_triggers(project_id)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.triggers[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.ListBuildTriggersRequest(
            project_id=project_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_build_triggers_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_build_triggers(project_id)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_build_trigger(self):
        # Setup Expected Response
        id_ = "id3355"
        description = "description-1724546052"
        name = "name3373707"
        filename = "filename-734768633"
        disabled = True
        expected_response = {
            "id": id_,
            "description": description,
            "name": name,
            "filename": filename,
            "disabled": disabled,
        }
        expected_response = cloudbuild_pb2.BuildTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"
        trigger = {}

        response = client.update_build_trigger(project_id, trigger_id, trigger)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.UpdateBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id, trigger=trigger
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_build_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"
        trigger = {}

        with pytest.raises(CustomException):
            client.update_build_trigger(project_id, trigger_id, trigger)

    def test_run_build_trigger(self):
        # Setup Expected Response
        id_ = "id3355"
        project_id_2 = "projectId2939242356"
        status_detail = "statusDetail2089931070"
        logs_bucket = "logsBucket1565363834"
        build_trigger_id = "buildTriggerId1105559411"
        log_url = "logUrl342054388"
        expected_response = {
            "id": id_,
            "project_id": project_id_2,
            "status_detail": status_detail,
            "logs_bucket": logs_bucket,
            "build_trigger_id": build_trigger_id,
            "log_url": log_url,
        }
        expected_response = cloudbuild_pb2.Build(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_run_build_trigger", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"
        source = {}

        response = client.run_build_trigger(project_id, trigger_id, source)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.RunBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id, source=source
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_build_trigger_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_run_build_trigger_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trigger_id = "triggerId1363517698"
        source = {}

        response = client.run_build_trigger(project_id, trigger_id, source)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_create_worker_pool(self):
        # Setup Expected Response
        name = "name3373707"
        project_id = "projectId-1969970175"
        service_account_email = "serviceAccountEmail-1300473088"
        worker_count = 372044046
        expected_response = {
            "name": name,
            "project_id": project_id,
            "service_account_email": service_account_email,
            "worker_count": worker_count,
        }
        expected_response = cloudbuild_pb2.WorkerPool(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        response = client.create_worker_pool()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.CreateWorkerPoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_worker_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        with pytest.raises(CustomException):
            client.create_worker_pool()

    def test_get_worker_pool(self):
        # Setup Expected Response
        name = "name3373707"
        project_id = "projectId-1969970175"
        service_account_email = "serviceAccountEmail-1300473088"
        worker_count = 372044046
        expected_response = {
            "name": name,
            "project_id": project_id,
            "service_account_email": service_account_email,
            "worker_count": worker_count,
        }
        expected_response = cloudbuild_pb2.WorkerPool(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        response = client.get_worker_pool()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.GetWorkerPoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_worker_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        with pytest.raises(CustomException):
            client.get_worker_pool()

    def test_delete_worker_pool(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        client.delete_worker_pool()

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.DeleteWorkerPoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_worker_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        with pytest.raises(CustomException):
            client.delete_worker_pool()

    def test_update_worker_pool(self):
        # Setup Expected Response
        name = "name3373707"
        project_id = "projectId-1969970175"
        service_account_email = "serviceAccountEmail-1300473088"
        worker_count = 372044046
        expected_response = {
            "name": name,
            "project_id": project_id,
            "service_account_email": service_account_email,
            "worker_count": worker_count,
        }
        expected_response = cloudbuild_pb2.WorkerPool(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        response = client.update_worker_pool()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.UpdateWorkerPoolRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_worker_pool_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        with pytest.raises(CustomException):
            client.update_worker_pool()

    def test_list_worker_pools(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cloudbuild_pb2.ListWorkerPoolsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        response = client.list_worker_pools()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudbuild_pb2.ListWorkerPoolsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_worker_pools_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = cloudbuild_v1.CloudBuildClient()

        with pytest.raises(CustomException):
            client.list_worker_pools()
