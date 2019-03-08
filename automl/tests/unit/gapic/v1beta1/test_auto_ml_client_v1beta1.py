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

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import dataset_pb2
from google.cloud.automl_v1beta1.proto import io_pb2
from google.cloud.automl_v1beta1.proto import model_evaluation_pb2
from google.cloud.automl_v1beta1.proto import model_pb2
from google.cloud.automl_v1beta1.proto import service_pb2
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


class TestAutoMlClient(object):
    def test_create_dataset(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        example_count = 1517063674
        expected_response = {
            "name": name,
            "display_name": display_name,
            "example_count": example_count,
        }
        expected_response = dataset_pb2.Dataset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        dataset = {}

        response = client.create_dataset(parent, dataset)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateDatasetRequest(
            parent=parent, dataset=dataset
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        dataset = {}

        with pytest.raises(CustomException):
            client.create_dataset(parent, dataset)

    def test_get_dataset(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        example_count = 1517063674
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "example_count": example_count,
        }
        expected_response = dataset_pb2.Dataset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")

        response = client.get_dataset(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetDatasetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")

        with pytest.raises(CustomException):
            client.get_dataset(name)

    def test_list_datasets(self):
        # Setup Expected Response
        next_page_token = ""
        datasets_element = {}
        datasets = [datasets_element]
        expected_response = {"next_page_token": next_page_token, "datasets": datasets}
        expected_response = service_pb2.ListDatasetsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_datasets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.datasets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListDatasetsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_datasets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_datasets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_dataset(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_delete_dataset", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")

        response = client.delete_dataset(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = service_pb2.DeleteDatasetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_dataset_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_dataset_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")

        response = client.delete_dataset(name)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_import_data(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_import_data", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")
        input_config = {}

        response = client.import_data(name, input_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = service_pb2.ImportDataRequest(
            name=name, input_config=input_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_data_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_import_data_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")
        input_config = {}

        response = client.import_data(name, input_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_export_data(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_export_data", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")
        output_config = {}

        response = client.export_data(name, output_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = service_pb2.ExportDataRequest(
            name=name, output_config=output_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_export_data_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_export_data_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[LOCATION]", "[DATASET]")
        output_config = {}

        response = client.export_data(name, output_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_create_model(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        dataset_id = "datasetId-2115646910"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "dataset_id": dataset_id,
        }
        expected_response = model_pb2.Model(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_model", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        model = {}

        response = client.create_model(parent, model)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateModelRequest(parent=parent, model=model)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_model_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_model_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        model = {}

        response = client.create_model(parent, model)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_model(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        dataset_id = "datasetId-2115646910"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "dataset_id": dataset_id,
        }
        expected_response = model_pb2.Model(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        response = client.get_model(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetModelRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        with pytest.raises(CustomException):
            client.get_model(name)

    def test_list_models(self):
        # Setup Expected Response
        next_page_token = ""
        model_element = {}
        model = [model_element]
        expected_response = {"next_page_token": next_page_token, "model": model}
        expected_response = service_pb2.ListModelsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_models(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.model[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListModelsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_models_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_models(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_model(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_delete_model", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        response = client.delete_model(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = service_pb2.DeleteModelRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_model_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_model_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        response = client.delete_model(name)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_deploy_model(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        done = True
        expected_response = {"name": name_2, "done": done}
        expected_response = operations_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        response = client.deploy_model(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.DeployModelRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_deploy_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        with pytest.raises(CustomException):
            client.deploy_model(name)

    def test_undeploy_model(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        done = True
        expected_response = {"name": name_2, "done": done}
        expected_response = operations_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        response = client.undeploy_model(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.UndeployModelRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_undeploy_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        name = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        with pytest.raises(CustomException):
            client.undeploy_model(name)

    def test_get_model_evaluation(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        annotation_spec_id = "annotationSpecId60690191"
        evaluated_example_count = 277565350
        expected_response = {
            "name": name_2,
            "annotation_spec_id": annotation_spec_id,
            "evaluated_example_count": evaluated_example_count,
        }
        expected_response = model_evaluation_pb2.ModelEvaluation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        name = client.model_evaluation_path(
            "[PROJECT]", "[LOCATION]", "[MODEL]", "[MODEL_EVALUATION]"
        )

        response = client.get_model_evaluation(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetModelEvaluationRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_model_evaluation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        name = client.model_evaluation_path(
            "[PROJECT]", "[LOCATION]", "[MODEL]", "[MODEL_EVALUATION]"
        )

        with pytest.raises(CustomException):
            client.get_model_evaluation(name)

    def test_list_model_evaluations(self):
        # Setup Expected Response
        next_page_token = ""
        model_evaluation_element = {}
        model_evaluation = [model_evaluation_element]
        expected_response = {
            "next_page_token": next_page_token,
            "model_evaluation": model_evaluation,
        }
        expected_response = service_pb2.ListModelEvaluationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup Request
        parent = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        paged_list_response = client.list_model_evaluations(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.model_evaluation[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListModelEvaluationsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_model_evaluations_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = automl_v1beta1.AutoMlClient()

        # Setup request
        parent = client.model_path("[PROJECT]", "[LOCATION]", "[MODEL]")

        paged_list_response = client.list_model_evaluations(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
