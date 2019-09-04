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

from google.cloud import talent_v4beta1
from google.cloud.talent_v4beta1.proto import common_pb2
from google.cloud.talent_v4beta1.proto import job_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2
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


class TestJobServiceClient(object):
    def test_create_job(self):
        # Setup Expected Response
        name = "name3373707"
        company = "company950484093"
        requisition_id = "requisitionId980224926"
        title = "title110371416"
        description = "description-1724546052"
        department = "department848184146"
        incentives = "incentives-1262874520"
        language_code = "languageCode-412800396"
        promotion_value = 353413845
        qualifications = "qualifications1903501412"
        responsibilities = "responsibilities-926952660"
        company_display_name = "companyDisplayName1982424170"
        expected_response = {
            "name": name,
            "company": company,
            "requisition_id": requisition_id,
            "title": title,
            "description": description,
            "department": department,
            "incentives": incentives,
            "language_code": language_code,
            "promotion_value": promotion_value,
            "qualifications": qualifications,
            "responsibilities": responsibilities,
            "company_display_name": company_display_name,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        job = {}

        response = client.create_job(parent, job)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.CreateJobRequest(parent=parent, job=job)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        job = {}

        with pytest.raises(CustomException):
            client.create_job(parent, job)

    def test_get_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        company = "company950484093"
        requisition_id = "requisitionId980224926"
        title = "title110371416"
        description = "description-1724546052"
        department = "department848184146"
        incentives = "incentives-1262874520"
        language_code = "languageCode-412800396"
        promotion_value = 353413845
        qualifications = "qualifications1903501412"
        responsibilities = "responsibilities-926952660"
        company_display_name = "companyDisplayName1982424170"
        expected_response = {
            "name": name_2,
            "company": company,
            "requisition_id": requisition_id,
            "title": title,
            "description": description,
            "department": department,
            "incentives": incentives,
            "language_code": language_code,
            "promotion_value": promotion_value,
            "qualifications": qualifications,
            "responsibilities": responsibilities,
            "company_display_name": company_display_name,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[TENANT]", "[JOBS]")

        response = client.get_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.GetJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[TENANT]", "[JOBS]")

        with pytest.raises(CustomException):
            client.get_job(name)

    def test_update_job(self):
        # Setup Expected Response
        name = "name3373707"
        company = "company950484093"
        requisition_id = "requisitionId980224926"
        title = "title110371416"
        description = "description-1724546052"
        department = "department848184146"
        incentives = "incentives-1262874520"
        language_code = "languageCode-412800396"
        promotion_value = 353413845
        qualifications = "qualifications1903501412"
        responsibilities = "responsibilities-926952660"
        company_display_name = "companyDisplayName1982424170"
        expected_response = {
            "name": name,
            "company": company,
            "requisition_id": requisition_id,
            "title": title,
            "description": description,
            "department": department,
            "incentives": incentives,
            "language_code": language_code,
            "promotion_value": promotion_value,
            "qualifications": qualifications,
            "responsibilities": responsibilities,
            "company_display_name": company_display_name,
        }
        expected_response = job_pb2.Job(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        job = {}

        response = client.update_job(job)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.UpdateJobRequest(job=job)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        job = {}

        with pytest.raises(CustomException):
            client.update_job(job)

    def test_delete_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        name = client.job_path("[PROJECT]", "[TENANT]", "[JOBS]")

        client.delete_job(name)

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.DeleteJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        name = client.job_path("[PROJECT]", "[TENANT]", "[JOBS]")

        with pytest.raises(CustomException):
            client.delete_job(name)

    def test_list_jobs(self):
        # Setup Expected Response
        next_page_token = ""
        jobs_element = {}
        jobs = [jobs_element]
        expected_response = {"next_page_token": next_page_token, "jobs": jobs}
        expected_response = job_service_pb2.ListJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_jobs(parent, filter_)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.ListJobsRequest(
            parent=parent, filter=filter_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_jobs(parent, filter_)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_batch_delete_jobs(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        filter_ = "filter-1274492040"

        client.batch_delete_jobs(parent, filter_)

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.BatchDeleteJobsRequest(
            parent=parent, filter=filter_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_delete_jobs_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        filter_ = "filter-1274492040"

        with pytest.raises(CustomException):
            client.batch_delete_jobs(parent, filter_)

    def test_search_jobs(self):
        # Setup Expected Response
        next_page_token = ""
        estimated_total_size = 1882144769
        total_size = 705419236
        broadened_query_jobs_count = 1432104658
        matching_jobs_element = {}
        matching_jobs = [matching_jobs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "estimated_total_size": estimated_total_size,
            "total_size": total_size,
            "broadened_query_jobs_count": broadened_query_jobs_count,
            "matching_jobs": matching_jobs,
        }
        expected_response = job_service_pb2.SearchJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_jobs(parent, request_metadata)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.matching_jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.SearchJobsRequest(
            parent=parent, request_metadata=request_metadata
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_jobs(parent, request_metadata)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_search_jobs_for_alert(self):
        # Setup Expected Response
        next_page_token = ""
        estimated_total_size = 1882144769
        total_size = 705419236
        broadened_query_jobs_count = 1432104658
        matching_jobs_element = {}
        matching_jobs = [matching_jobs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "estimated_total_size": estimated_total_size,
            "total_size": total_size,
            "broadened_query_jobs_count": broadened_query_jobs_count,
            "matching_jobs": matching_jobs,
        }
        expected_response = job_service_pb2.SearchJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_jobs_for_alert(parent, request_metadata)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.matching_jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.SearchJobsRequest(
            parent=parent, request_metadata=request_metadata
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_jobs_for_alert_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_jobs_for_alert(parent, request_metadata)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_batch_create_jobs(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = job_service_pb2.JobOperationResult(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_batch_create_jobs", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        jobs = []

        response = client.batch_create_jobs(parent, jobs)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.BatchCreateJobsRequest(
            parent=parent, jobs=jobs
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_jobs_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_batch_create_jobs_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        jobs = []

        response = client.batch_create_jobs(parent, jobs)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_update_jobs(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = job_service_pb2.JobOperationResult(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_batch_update_jobs", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        jobs = []

        response = client.batch_update_jobs(parent, jobs)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = job_service_pb2.BatchUpdateJobsRequest(
            parent=parent, jobs=jobs
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_update_jobs_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_batch_update_jobs_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.JobServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        jobs = []

        response = client.batch_update_jobs(parent, jobs)
        exception = response.exception()
        assert exception.errors[0] == error
