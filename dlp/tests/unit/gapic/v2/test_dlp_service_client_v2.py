# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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

import pytest

from google.cloud import dlp_v2
from google.cloud.dlp_v2.proto import dlp_pb2
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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestDlpServiceClient(object):
    def test_inspect_content(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.InspectContentResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.inspect_content(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.InspectContentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_inspect_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.inspect_content(parent)

    def test_redact_image(self):
        # Setup Expected Response
        redacted_image = b'28'
        extracted_text = 'extractedText998260012'
        expected_response = {
            'redacted_image': redacted_image,
            'extracted_text': extracted_text
        }
        expected_response = dlp_pb2.RedactImageResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.redact_image(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.RedactImageRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_redact_image_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.redact_image(parent)

    def test_deidentify_content(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.DeidentifyContentResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.deidentify_content(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeidentifyContentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_deidentify_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.deidentify_content(parent)

    def test_reidentify_content(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.ReidentifyContentResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.reidentify_content(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ReidentifyContentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_reidentify_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.reidentify_content(parent)

    def test_list_info_types(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.ListInfoTypesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        response = client.list_info_types()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListInfoTypesRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_info_types_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        with pytest.raises(CustomException):
            client.list_info_types()

    def test_create_inspect_template(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.InspectTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        response = client.create_inspect_template(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateInspectTemplateRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_inspect_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        with pytest.raises(CustomException):
            client.create_inspect_template(parent)

    def test_update_inspect_template(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.InspectTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_inspect_template_path(
            '[ORGANIZATION]', '[INSPECT_TEMPLATE]')

        response = client.update_inspect_template(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.UpdateInspectTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_inspect_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_inspect_template_path(
            '[ORGANIZATION]', '[INSPECT_TEMPLATE]')

        with pytest.raises(CustomException):
            client.update_inspect_template(name)

    def test_get_inspect_template(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.InspectTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        response = client.get_inspect_template()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.GetInspectTemplateRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_inspect_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        with pytest.raises(CustomException):
            client.get_inspect_template()

    def test_list_inspect_templates(self):
        # Setup Expected Response
        next_page_token = ''
        inspect_templates_element = {}
        inspect_templates = [inspect_templates_element]
        expected_response = {
            'next_page_token': next_page_token,
            'inspect_templates': inspect_templates
        }
        expected_response = dlp_pb2.ListInspectTemplatesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_inspect_templates(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.inspect_templates[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListInspectTemplatesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_inspect_templates_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_inspect_templates(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_inspect_template(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_inspect_template_path(
            '[ORGANIZATION]', '[INSPECT_TEMPLATE]')

        client.delete_inspect_template(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeleteInspectTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_inspect_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_inspect_template_path(
            '[ORGANIZATION]', '[INSPECT_TEMPLATE]')

        with pytest.raises(CustomException):
            client.delete_inspect_template(name)

    def test_create_deidentify_template(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.DeidentifyTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        response = client.create_deidentify_template(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateDeidentifyTemplateRequest(
            parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_deidentify_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        with pytest.raises(CustomException):
            client.create_deidentify_template(parent)

    def test_update_deidentify_template(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.DeidentifyTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        response = client.update_deidentify_template(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.UpdateDeidentifyTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_deidentify_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        with pytest.raises(CustomException):
            client.update_deidentify_template(name)

    def test_get_deidentify_template(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.DeidentifyTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        response = client.get_deidentify_template(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.GetDeidentifyTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_deidentify_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        with pytest.raises(CustomException):
            client.get_deidentify_template(name)

    def test_list_deidentify_templates(self):
        # Setup Expected Response
        next_page_token = ''
        deidentify_templates_element = {}
        deidentify_templates = [deidentify_templates_element]
        expected_response = {
            'next_page_token': next_page_token,
            'deidentify_templates': deidentify_templates
        }
        expected_response = dlp_pb2.ListDeidentifyTemplatesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_deidentify_templates(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.deidentify_templates[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListDeidentifyTemplatesRequest(
            parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_deidentify_templates_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_deidentify_templates(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_deidentify_template(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        client.delete_deidentify_template(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeleteDeidentifyTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_deidentify_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_deidentify_template_path(
            '[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')

        with pytest.raises(CustomException):
            client.delete_deidentify_template(name)

    def test_create_dlp_job(self):
        # Setup Expected Response
        name = 'name3373707'
        job_trigger_name = 'jobTriggerName1819490804'
        expected_response = {
            'name': name,
            'job_trigger_name': job_trigger_name
        }
        expected_response = dlp_pb2.DlpJob(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.create_dlp_job(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateDlpJobRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_dlp_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.create_dlp_job(parent)

    def test_list_dlp_jobs(self):
        # Setup Expected Response
        next_page_token = ''
        jobs_element = {}
        jobs = [jobs_element]
        expected_response = {'next_page_token': next_page_token, 'jobs': jobs}
        expected_response = dlp_pb2.ListDlpJobsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.list_dlp_jobs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListDlpJobsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_dlp_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.list_dlp_jobs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_dlp_job(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        job_trigger_name = 'jobTriggerName1819490804'
        expected_response = {
            'name': name_2,
            'job_trigger_name': job_trigger_name
        }
        expected_response = dlp_pb2.DlpJob(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        response = client.get_dlp_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.GetDlpJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_dlp_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        with pytest.raises(CustomException):
            client.get_dlp_job(name)

    def test_delete_dlp_job(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        client.delete_dlp_job(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeleteDlpJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_dlp_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        with pytest.raises(CustomException):
            client.delete_dlp_job(name)

    def test_cancel_dlp_job(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        client.cancel_dlp_job(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CancelDlpJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_cancel_dlp_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')

        with pytest.raises(CustomException):
            client.cancel_dlp_job(name)

    def test_list_job_triggers(self):
        # Setup Expected Response
        next_page_token = ''
        job_triggers_element = {}
        job_triggers = [job_triggers_element]
        expected_response = {
            'next_page_token': next_page_token,
            'job_triggers': job_triggers
        }
        expected_response = dlp_pb2.ListJobTriggersResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.list_job_triggers(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.job_triggers[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListJobTriggersRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_job_triggers_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.list_job_triggers(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_job_trigger(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.JobTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')

        response = client.get_job_trigger(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.GetJobTriggerRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_job_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')

        with pytest.raises(CustomException):
            client.get_job_trigger(name)

    def test_delete_job_trigger(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = 'name3373707'

        client.delete_job_trigger(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeleteJobTriggerRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_job_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = 'name3373707'

        with pytest.raises(CustomException):
            client.delete_job_trigger(name)

    def test_update_job_trigger(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.JobTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')

        response = client.update_job_trigger(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.UpdateJobTriggerRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_job_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')

        with pytest.raises(CustomException):
            client.update_job_trigger(name)

    def test_create_job_trigger(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        description = 'description-1724546052'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'description': description
        }
        expected_response = dlp_pb2.JobTrigger(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.create_job_trigger(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateJobTriggerRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_job_trigger_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.create_job_trigger(parent)

    def test_create_stored_info_type(self):
        # Setup Expected Response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = dlp_pb2.StoredInfoType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        response = client.create_stored_info_type(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateStoredInfoTypeRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_stored_info_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        with pytest.raises(CustomException):
            client.create_stored_info_type(parent)

    def test_update_stored_info_type(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = dlp_pb2.StoredInfoType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        response = client.update_stored_info_type(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.UpdateStoredInfoTypeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_stored_info_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        with pytest.raises(CustomException):
            client.update_stored_info_type(name)

    def test_get_stored_info_type(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = dlp_pb2.StoredInfoType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        response = client.get_stored_info_type(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.GetStoredInfoTypeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_stored_info_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        with pytest.raises(CustomException):
            client.get_stored_info_type(name)

    def test_list_stored_info_types(self):
        # Setup Expected Response
        next_page_token = ''
        stored_info_types_element = {}
        stored_info_types = [stored_info_types_element]
        expected_response = {
            'next_page_token': next_page_token,
            'stored_info_types': stored_info_types
        }
        expected_response = dlp_pb2.ListStoredInfoTypesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_stored_info_types(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.stored_info_types[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListStoredInfoTypesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_stored_info_types_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        parent = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.list_stored_info_types(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_stored_info_type(self):
        channel = ChannelStub()
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        client.delete_stored_info_type(name)

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeleteStoredInfoTypeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_stored_info_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2.DlpServiceClient(channel=channel)

        # Setup request
        name = client.organization_stored_info_type_path(
            '[ORGANIZATION]', '[STORED_INFO_TYPE]')

        with pytest.raises(CustomException):
            client.delete_stored_info_type(name)
