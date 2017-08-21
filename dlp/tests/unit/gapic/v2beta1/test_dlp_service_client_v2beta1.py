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

import mock
import unittest

from google.gax import errors
from google.rpc import status_pb2

from google.cloud import dlp_v2beta1
from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2
from google.cloud.proto.privacy.dlp.v2beta1 import storage_pb2
from google.longrunning import operations_pb2


class CustomException(Exception):
    pass


class TestDlpServiceClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_inspect_content(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        # Mock response
        expected_response = {}
        expected_response = dlp_pb2.InspectContentResponse(**expected_response)
        grpc_stub.InspectContent.return_value = expected_response

        response = client.inspect_content(inspect_config, items)
        self.assertEqual(expected_response, response)

        grpc_stub.InspectContent.assert_called_once()
        args, kwargs = grpc_stub.InspectContent.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.InspectContentRequest(
            inspect_config=inspect_config, items=items)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_inspect_content_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]

        # Mock exception response
        grpc_stub.InspectContent.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.inspect_content,
                          inspect_config, items)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_redact_content(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]
        name_2 = 'EMAIL_ADDRESS'
        info_type = {'name': name_2}
        replace_with = 'REDACTED'
        replace_configs_element = {
            'info_type': info_type,
            'replace_with': replace_with
        }
        replace_configs = [replace_configs_element]

        # Mock response
        expected_response = {}
        expected_response = dlp_pb2.RedactContentResponse(**expected_response)
        grpc_stub.RedactContent.return_value = expected_response

        response = client.redact_content(inspect_config, items,
                                         replace_configs)
        self.assertEqual(expected_response, response)

        grpc_stub.RedactContent.assert_called_once()
        args, kwargs = grpc_stub.RedactContent.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.RedactContentRequest(
            inspect_config=inspect_config,
            items=items,
            replace_configs=replace_configs)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_redact_content_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        type_ = 'text/plain'
        value = 'My email is example@example.com.'
        items_element = {'type': type_, 'value': value}
        items = [items_element]
        name_2 = 'EMAIL_ADDRESS'
        info_type = {'name': name_2}
        replace_with = 'REDACTED'
        replace_configs_element = {
            'info_type': info_type,
            'replace_with': replace_with
        }
        replace_configs = [replace_configs_element]

        # Mock exception response
        grpc_stub.RedactContent.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.redact_content,
                          inspect_config, items, replace_configs)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_inspect_operation(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        url = 'gs://example_bucket/example_file.png'
        file_set = {'url': url}
        cloud_storage_options = {'file_set': file_set}
        storage_config = {'cloud_storage_options': cloud_storage_options}
        output_config = {}

        # Mock response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = dlp_pb2.InspectOperationResult(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_create_inspect_operation', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.CreateInspectOperation.return_value = operation

        response = client.create_inspect_operation(
            inspect_config, storage_config, output_config)
        self.assertEqual(expected_response, response.result())

        grpc_stub.CreateInspectOperation.assert_called_once()
        args, kwargs = grpc_stub.CreateInspectOperation.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.CreateInspectOperationRequest(
            inspect_config=inspect_config,
            storage_config=storage_config,
            output_config=output_config)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_inspect_operation_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = 'EMAIL_ADDRESS'
        info_types_element = {'name': name}
        info_types = [info_types_element]
        inspect_config = {'info_types': info_types}
        url = 'gs://example_bucket/example_file.png'
        file_set = {'url': url}
        cloud_storage_options = {'file_set': file_set}
        storage_config = {'cloud_storage_options': cloud_storage_options}
        output_config = {}

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_create_inspect_operation_exception',
            done=True)
        operation.error.CopyFrom(error)
        grpc_stub.CreateInspectOperation.return_value = operation

        response = client.create_inspect_operation(
            inspect_config, storage_config, output_config)
        self.assertEqual(error, response.exception())

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_inspect_findings(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = client.result_path('[RESULT]')

        # Mock response
        next_page_token = 'nextPageToken-1530815211'
        expected_response = {'next_page_token': next_page_token}
        expected_response = dlp_pb2.ListInspectFindingsResponse(
            **expected_response)
        grpc_stub.ListInspectFindings.return_value = expected_response

        response = client.list_inspect_findings(name)
        self.assertEqual(expected_response, response)

        grpc_stub.ListInspectFindings.assert_called_once()
        args, kwargs = grpc_stub.ListInspectFindings.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.ListInspectFindingsRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_inspect_findings_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        name = client.result_path('[RESULT]')

        # Mock exception response
        grpc_stub.ListInspectFindings.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.list_inspect_findings, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_info_types(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        category = 'PII'
        language_code = 'en'

        # Mock response
        expected_response = {}
        expected_response = dlp_pb2.ListInfoTypesResponse(**expected_response)
        grpc_stub.ListInfoTypes.return_value = expected_response

        response = client.list_info_types(category, language_code)
        self.assertEqual(expected_response, response)

        grpc_stub.ListInfoTypes.assert_called_once()
        args, kwargs = grpc_stub.ListInfoTypes.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.ListInfoTypesRequest(
            category=category, language_code=language_code)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_info_types_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        category = 'PII'
        language_code = 'en'

        # Mock exception response
        grpc_stub.ListInfoTypes.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.list_info_types, category,
                          language_code)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_root_categories(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        language_code = 'en'

        # Mock response
        expected_response = {}
        expected_response = dlp_pb2.ListRootCategoriesResponse(
            **expected_response)
        grpc_stub.ListRootCategories.return_value = expected_response

        response = client.list_root_categories(language_code)
        self.assertEqual(expected_response, response)

        grpc_stub.ListRootCategories.assert_called_once()
        args, kwargs = grpc_stub.ListRootCategories.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = dlp_pb2.ListRootCategoriesRequest(
            language_code=language_code)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_root_categories_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = dlp_v2beta1.DlpServiceClient()

        # Mock request
        language_code = 'en'

        # Mock exception response
        grpc_stub.ListRootCategories.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.list_root_categories,
                          language_code)
