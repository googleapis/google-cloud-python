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

from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.proto import jobs_pb2
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


class TestJobControllerClient(object):
    def test_submit_job(self):
        # Setup Expected Response
        driver_output_resource_uri = "driverOutputResourceUri-542229086"
        driver_control_files_uri = "driverControlFilesUri207057643"
        job_uuid = "jobUuid-1615012099"
        expected_response = {
            "driver_output_resource_uri": driver_output_resource_uri,
            "driver_control_files_uri": driver_control_files_uri,
            "job_uuid": job_uuid,
        }
        expected_response = jobs_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job = {}

        response = client.submit_job(project_id, region, job)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.SubmitJobRequest(
            project_id=project_id, region=region, job=job
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_submit_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job = {}

        with pytest.raises(CustomException):
            client.submit_job(project_id, region, job)

    def test_get_job(self):
        # Setup Expected Response
        driver_output_resource_uri = "driverOutputResourceUri-542229086"
        driver_control_files_uri = "driverControlFilesUri207057643"
        job_uuid = "jobUuid-1615012099"
        expected_response = {
            "driver_output_resource_uri": driver_output_resource_uri,
            "driver_control_files_uri": driver_control_files_uri,
            "job_uuid": job_uuid,
        }
        expected_response = jobs_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        response = client.get_job(project_id, region, job_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.GetJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        with pytest.raises(CustomException):
            client.get_job(project_id, region, job_id)

    def test_list_jobs(self):
        # Setup Expected Response
        next_page_token = ""
        jobs_element = {}
        jobs = [jobs_element]
        expected_response = {"next_page_token": next_page_token, "jobs": jobs}
        expected_response = jobs_pb2.ListJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"

        paged_list_response = client.list_jobs(project_id, region)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.ListJobsRequest(
            project_id=project_id, region=region
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"

        paged_list_response = client.list_jobs(project_id, region)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_job(self):
        # Setup Expected Response
        driver_output_resource_uri = "driverOutputResourceUri-542229086"
        driver_control_files_uri = "driverControlFilesUri207057643"
        job_uuid = "jobUuid-1615012099"
        expected_response = {
            "driver_output_resource_uri": driver_output_resource_uri,
            "driver_control_files_uri": driver_control_files_uri,
            "job_uuid": job_uuid,
        }
        expected_response = jobs_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"
        job = {}
        update_mask = {}

        response = client.update_job(project_id, region, job_id, job, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.UpdateJobRequest(
            project_id=project_id,
            region=region,
            job_id=job_id,
            job=job,
            update_mask=update_mask,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"
        job = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_job(project_id, region, job_id, job, update_mask)

    def test_cancel_job(self):
        # Setup Expected Response
        driver_output_resource_uri = "driverOutputResourceUri-542229086"
        driver_control_files_uri = "driverControlFilesUri207057643"
        job_uuid = "jobUuid-1615012099"
        expected_response = {
            "driver_output_resource_uri": driver_output_resource_uri,
            "driver_control_files_uri": driver_control_files_uri,
            "job_uuid": job_uuid,
        }
        expected_response = jobs_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        response = client.cancel_job(project_id, region, job_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.CancelJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_cancel_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        with pytest.raises(CustomException):
            client.cancel_job(project_id, region, job_id)

    def test_delete_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup Request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        client.delete_job(project_id, region, job_id)

        assert len(channel.requests) == 1
        expected_request = jobs_pb2.DeleteJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1.JobControllerClient()

        # Setup request
        project_id = "projectId-1969970175"
        region = "region-934795532"
        job_id = "jobId-1154752291"

        with pytest.raises(CustomException):
            client.delete_job(project_id, region, job_id)
