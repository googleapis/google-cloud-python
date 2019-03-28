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

from google.cloud import scheduler_v1
from google.cloud.scheduler_v1.proto import cloudscheduler_pb2
from google.cloud.scheduler_v1.proto import job_pb2
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


class TestCloudSchedulerClient(object):
    def test_list_jobs(self):
        # Setup Expected Response
        next_page_token = ""
        jobs_element = {}
        jobs = [jobs_element]
        expected_response = {"next_page_token": next_page_token, "jobs": jobs}
        expected_response = cloudscheduler_pb2.ListJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_jobs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.ListJobsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_jobs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name_2,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        response = client.get_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.GetJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        with pytest.raises(CustomException):
            client.get_job(name)

    def test_create_job(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        job = {}

        response = client.create_job(parent, job)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.CreateJobRequest(parent=parent, job=job)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        job = {}

        with pytest.raises(CustomException):
            client.create_job(parent, job)

    def test_update_job(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        job = {}
        update_mask = {}

        response = client.update_job(job, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.UpdateJobRequest(
            job=job, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        job = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_job(job, update_mask)

    def test_delete_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        client.delete_job(name)

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.DeleteJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        with pytest.raises(CustomException):
            client.delete_job(name)

    def test_pause_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name_2,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        response = client.pause_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.PauseJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_pause_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        with pytest.raises(CustomException):
            client.pause_job(name)

    def test_resume_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name_2,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        response = client.resume_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.ResumeJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_resume_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        with pytest.raises(CustomException):
            client.resume_job(name)

    def test_run_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        time_zone = "timeZone36848094"
        expected_response = {
            "name": name_2,
            "description": description,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        response = client.run_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloudscheduler_pb2.RunJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = scheduler_v1.CloudSchedulerClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[LOCATION]", "[JOB]")

        with pytest.raises(CustomException):
            client.run_job(name)
