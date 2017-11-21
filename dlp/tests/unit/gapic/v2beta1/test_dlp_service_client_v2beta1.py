# Copyright 2017, Google LLC All rights reserved.
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

from google.rpc import status_pb2

from google.cloud import dlp_v2beta1
from google.cloud.dlp_v2beta1.proto import dlp_pb2
from google.cloud.dlp_v2beta1.proto import storage_pb2
from google.longrunning import operations_pb2


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
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        response = client.inspect_content(inspect_config, items)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.InspectContentRequest(
            inspect_config=inspect_config, items=items)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_inspect_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        with pytest.raises(CustomException):
            client.inspect_content(inspect_config, items)

    def test_redact_content(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.RedactContentResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        response = client.redact_content(inspect_config, items)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.RedactContentRequest(
            inspect_config=inspect_config, items=items)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_redact_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        with pytest.raises(CustomException):
            client.redact_content(inspect_config, items)

    def test_deidentify_content(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.DeidentifyContentResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        deidentify_config = {}
        inspect_config = {}
        items = []

        response = client.deidentify_content(deidentify_config, inspect_config,
                                             items)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.DeidentifyContentRequest(
            deidentify_config=deidentify_config,
            inspect_config=inspect_config,
            items=items)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_deidentify_content_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        deidentify_config = {}
        inspect_config = {}
        items = []

        with pytest.raises(CustomException):
            client.deidentify_content(deidentify_config, inspect_config, items)

    def test_analyze_data_source_risk(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.RiskAnalysisOperationResult(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_analyze_data_source_risk', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        privacy_metric = {}
        source_table = {}

        response = client.analyze_data_source_risk(privacy_metric,
                                                   source_table)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.AnalyzeDataSourceRiskRequest(
            privacy_metric=privacy_metric, source_table=source_table)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_analyze_data_source_risk_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_analyze_data_source_risk_exception',
            done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        privacy_metric = {}
        source_table = {}

        response = client.analyze_data_source_risk(privacy_metric,
                                                   source_table)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_create_inspect_operation(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = dlp_pb2.InspectOperationResult(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_create_inspect_operation', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        url = 'gs://example_bucket/example_file.png'
        file_set = {'url': url}
        cloud_storage_options = {'file_set': file_set}
        storage_config = {'cloud_storage_options': cloud_storage_options}
        output_config = {}

        response = client.create_inspect_operation(
            inspect_config, storage_config, output_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.CreateInspectOperationRequest(
            inspect_config=inspect_config,
            storage_config=storage_config,
            output_config=output_config)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_inspect_operation_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_create_inspect_operation_exception',
            done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        url = 'gs://example_bucket/example_file.png'
        file_set = {'url': url}
        cloud_storage_options = {'file_set': file_set}
        storage_config = {'cloud_storage_options': cloud_storage_options}
        output_config = {}

        response = client.create_inspect_operation(
            inspect_config, storage_config, output_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_list_inspect_findings(self):
        # Setup Expected Response
        next_page_token = 'nextPageToken-1530815211'
        expected_response = {'next_page_token': next_page_token}
        expected_response = dlp_pb2.ListInspectFindingsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        name = client.result_path('[RESULT]')

        response = client.list_inspect_findings(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListInspectFindingsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_inspect_findings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        name = client.result_path('[RESULT]')

        with pytest.raises(CustomException):
            client.list_inspect_findings(name)

    def test_list_info_types(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.ListInfoTypesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        category = 'PII'
        language_code = 'en'

        response = client.list_info_types(category, language_code)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListInfoTypesRequest(
            category=category, language_code=language_code)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_info_types_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        category = 'PII'
        language_code = 'en'

        with pytest.raises(CustomException):
            client.list_info_types(category, language_code)

    def test_list_root_categories(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = dlp_pb2.ListRootCategoriesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup Request
        language_code = 'en'

        response = client.list_root_categories(language_code)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dlp_pb2.ListRootCategoriesRequest(
            language_code=language_code)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_root_categories_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dlp_v2beta1.DlpServiceClient(channel=channel)

        # Setup request
        language_code = 'en'

        with pytest.raises(CustomException):
            client.list_root_categories(language_code)
