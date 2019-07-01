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

from google.cloud import datalabeling_v1beta1
from google.cloud.datalabeling_v1beta1 import enums
from google.cloud.datalabeling_v1beta1.proto import annotation_spec_set_pb2
from google.cloud.datalabeling_v1beta1.proto import data_labeling_service_pb2
from google.cloud.datalabeling_v1beta1.proto import dataset_pb2
from google.cloud.datalabeling_v1beta1.proto import evaluation_job_pb2
from google.cloud.datalabeling_v1beta1.proto import evaluation_pb2
from google.cloud.datalabeling_v1beta1.proto import human_annotation_config_pb2
from google.cloud.datalabeling_v1beta1.proto import instruction_pb2
from google.cloud.datalabeling_v1beta1.proto import (
    operations_pb2 as proto_operations_pb2,
)
from google.longrunning import operations_pb2 as longrunning_operations_pb2
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


class TestDataLabelingServiceClient(object):
    def test_create_dataset(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        data_item_count = 2014260376
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "data_item_count": data_item_count,
        }
        expected_response = dataset_pb2.Dataset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        dataset = {}

        response = client.create_dataset(parent, dataset)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.CreateDatasetRequest(
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
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        dataset = {}

        with pytest.raises(CustomException):
            client.create_dataset(parent, dataset)

    def test_get_dataset(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        data_item_count = 2014260376
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
            "data_item_count": data_item_count,
        }
        expected_response = dataset_pb2.Dataset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")

        response = client.get_dataset(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetDatasetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.dataset_path("[PROJECT]", "[DATASET]")

        with pytest.raises(CustomException):
            client.get_dataset(name)

    def test_list_datasets(self):
        # Setup Expected Response
        next_page_token = ""
        datasets_element = {}
        datasets = [datasets_element]
        expected_response = {"next_page_token": next_page_token, "datasets": datasets}
        expected_response = data_labeling_service_pb2.ListDatasetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_datasets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.datasets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListDatasetsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_datasets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_datasets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_dataset(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")

        client.delete_dataset(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.DeleteDatasetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.dataset_path("[PROJECT]", "[DATASET]")

        with pytest.raises(CustomException):
            client.delete_dataset(name)

    def test_import_data(self):
        # Setup Expected Response
        dataset = "dataset1443214456"
        total_count = 407761836
        import_count = 1721296907
        expected_response = {
            "dataset": dataset,
            "total_count": total_count,
            "import_count": import_count,
        }
        expected_response = proto_operations_pb2.ImportDataOperationResponse(
            **expected_response
        )
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_import_data", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")
        input_config = {}

        response = client.import_data(name, input_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ImportDataRequest(
            name=name, input_config=input_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_data_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_import_data_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")
        input_config = {}

        response = client.import_data(name, input_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_export_data(self):
        # Setup Expected Response
        dataset = "dataset1443214456"
        total_count = 407761836
        export_count = 529256252
        expected_response = {
            "dataset": dataset,
            "total_count": total_count,
            "export_count": export_count,
        }
        expected_response = proto_operations_pb2.ExportDataOperationResponse(
            **expected_response
        )
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_export_data", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")
        annotated_dataset = "annotatedDataset-1407812655"
        output_config = {}

        response = client.export_data(name, annotated_dataset, output_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ExportDataRequest(
            name=name, annotated_dataset=annotated_dataset, output_config=output_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_export_data_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_export_data_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.dataset_path("[PROJECT]", "[DATASET]")
        annotated_dataset = "annotatedDataset-1407812655"
        output_config = {}

        response = client.export_data(name, annotated_dataset, output_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_data_item(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = dataset_pb2.DataItem(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.data_item_path("[PROJECT]", "[DATASET]", "[DATA_ITEM]")

        response = client.get_data_item(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetDataItemRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_data_item_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.data_item_path("[PROJECT]", "[DATASET]", "[DATA_ITEM]")

        with pytest.raises(CustomException):
            client.get_data_item(name)

    def test_list_data_items(self):
        # Setup Expected Response
        next_page_token = ""
        data_items_element = {}
        data_items = [data_items_element]
        expected_response = {
            "next_page_token": next_page_token,
            "data_items": data_items,
        }
        expected_response = data_labeling_service_pb2.ListDataItemsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")

        paged_list_response = client.list_data_items(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.data_items[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListDataItemsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_data_items_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")

        paged_list_response = client.list_data_items(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_annotated_dataset(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        example_count = 1517063674
        completed_example_count = 612567290
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
            "example_count": example_count,
            "completed_example_count": completed_example_count,
        }
        expected_response = dataset_pb2.AnnotatedDataset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.annotated_dataset_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]"
        )

        response = client.get_annotated_dataset(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetAnnotatedDatasetRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_annotated_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.annotated_dataset_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]"
        )

        with pytest.raises(CustomException):
            client.get_annotated_dataset(name)

    def test_list_annotated_datasets(self):
        # Setup Expected Response
        next_page_token = ""
        annotated_datasets_element = {}
        annotated_datasets = [annotated_datasets_element]
        expected_response = {
            "next_page_token": next_page_token,
            "annotated_datasets": annotated_datasets,
        }
        expected_response = data_labeling_service_pb2.ListAnnotatedDatasetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")

        paged_list_response = client.list_annotated_datasets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.annotated_datasets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListAnnotatedDatasetsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_annotated_datasets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")

        paged_list_response = client.list_annotated_datasets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_label_image(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        example_count = 1517063674
        completed_example_count = 612567290
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "example_count": example_count,
            "completed_example_count": completed_example_count,
        }
        expected_response = dataset_pb2.AnnotatedDataset(**expected_response)
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_image", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelImageRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_image(parent, basic_config, feature)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.LabelImageRequest(
            parent=parent, basic_config=basic_config, feature=feature
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_label_image_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_image_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelImageRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_image(parent, basic_config, feature)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_label_video(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        example_count = 1517063674
        completed_example_count = 612567290
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "example_count": example_count,
            "completed_example_count": completed_example_count,
        }
        expected_response = dataset_pb2.AnnotatedDataset(**expected_response)
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_video", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelVideoRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_video(parent, basic_config, feature)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.LabelVideoRequest(
            parent=parent, basic_config=basic_config, feature=feature
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_label_video_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_video_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelVideoRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_video(parent, basic_config, feature)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_label_text(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        example_count = 1517063674
        completed_example_count = 612567290
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "example_count": example_count,
            "completed_example_count": completed_example_count,
        }
        expected_response = dataset_pb2.AnnotatedDataset(**expected_response)
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_text", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelTextRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_text(parent, basic_config, feature)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.LabelTextRequest(
            parent=parent, basic_config=basic_config, feature=feature
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_label_text_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_label_text_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.dataset_path("[PROJECT]", "[DATASET]")
        basic_config = {}
        feature = enums.LabelTextRequest.Feature.FEATURE_UNSPECIFIED

        response = client.label_text(parent, basic_config, feature)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_example(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = dataset_pb2.Example(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.example_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]", "[EXAMPLE]"
        )

        response = client.get_example(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetExampleRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_example_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.example_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]", "[EXAMPLE]"
        )

        with pytest.raises(CustomException):
            client.get_example(name)

    def test_list_examples(self):
        # Setup Expected Response
        next_page_token = ""
        examples_element = {}
        examples = [examples_element]
        expected_response = {"next_page_token": next_page_token, "examples": examples}
        expected_response = data_labeling_service_pb2.ListExamplesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.annotated_dataset_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]"
        )

        paged_list_response = client.list_examples(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.examples[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListExamplesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_examples_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.annotated_dataset_path(
            "[PROJECT]", "[DATASET]", "[ANNOTATED_DATASET]"
        )

        paged_list_response = client.list_examples(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_annotation_spec_set(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = annotation_spec_set_pb2.AnnotationSpecSet(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        annotation_spec_set = {}

        response = client.create_annotation_spec_set(parent, annotation_spec_set)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.CreateAnnotationSpecSetRequest(
            parent=parent, annotation_spec_set=annotation_spec_set
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_annotation_spec_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        annotation_spec_set = {}

        with pytest.raises(CustomException):
            client.create_annotation_spec_set(parent, annotation_spec_set)

    def test_get_annotation_spec_set(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
        }
        expected_response = annotation_spec_set_pb2.AnnotationSpecSet(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.annotation_spec_set_path("[PROJECT]", "[ANNOTATION_SPEC_SET]")

        response = client.get_annotation_spec_set(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetAnnotationSpecSetRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_annotation_spec_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.annotation_spec_set_path("[PROJECT]", "[ANNOTATION_SPEC_SET]")

        with pytest.raises(CustomException):
            client.get_annotation_spec_set(name)

    def test_list_annotation_spec_sets(self):
        # Setup Expected Response
        next_page_token = ""
        annotation_spec_sets_element = {}
        annotation_spec_sets = [annotation_spec_sets_element]
        expected_response = {
            "next_page_token": next_page_token,
            "annotation_spec_sets": annotation_spec_sets,
        }
        expected_response = data_labeling_service_pb2.ListAnnotationSpecSetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_annotation_spec_sets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.annotation_spec_sets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListAnnotationSpecSetsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_annotation_spec_sets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_annotation_spec_sets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_annotation_spec_set(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.annotation_spec_set_path("[PROJECT]", "[ANNOTATION_SPEC_SET]")

        client.delete_annotation_spec_set(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.DeleteAnnotationSpecSetRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_annotation_spec_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.annotation_spec_set_path("[PROJECT]", "[ANNOTATION_SPEC_SET]")

        with pytest.raises(CustomException):
            client.delete_annotation_spec_set(name)

    def test_create_instruction(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = instruction_pb2.Instruction(**expected_response)
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_create_instruction", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instruction = {}

        response = client.create_instruction(parent, instruction)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.CreateInstructionRequest(
            parent=parent, instruction=instruction
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_instruction_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = longrunning_operations_pb2.Operation(
            name="operations/test_create_instruction_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instruction = {}

        response = client.create_instruction(parent, instruction)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_instruction(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
        }
        expected_response = instruction_pb2.Instruction(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.instruction_path("[PROJECT]", "[INSTRUCTION]")

        response = client.get_instruction(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetInstructionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_instruction_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.instruction_path("[PROJECT]", "[INSTRUCTION]")

        with pytest.raises(CustomException):
            client.get_instruction(name)

    def test_list_instructions(self):
        # Setup Expected Response
        next_page_token = ""
        instructions_element = {}
        instructions = [instructions_element]
        expected_response = {
            "next_page_token": next_page_token,
            "instructions": instructions,
        }
        expected_response = data_labeling_service_pb2.ListInstructionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instructions(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.instructions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListInstructionsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_instructions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instructions(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_instruction(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.instruction_path("[PROJECT]", "[INSTRUCTION]")

        client.delete_instruction(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.DeleteInstructionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_instruction_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.instruction_path("[PROJECT]", "[INSTRUCTION]")

        with pytest.raises(CustomException):
            client.delete_instruction(name)

    def test_get_evaluation(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        evaluated_item_count = 358077111
        expected_response = {
            "name": name_2,
            "evaluated_item_count": evaluated_item_count,
        }
        expected_response = evaluation_pb2.Evaluation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.evaluation_path("[PROJECT]", "[DATASET]", "[EVALUATION]")

        response = client.get_evaluation(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetEvaluationRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_evaluation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.evaluation_path("[PROJECT]", "[DATASET]", "[EVALUATION]")

        with pytest.raises(CustomException):
            client.get_evaluation(name)

    def test_search_evaluations(self):
        # Setup Expected Response
        next_page_token = ""
        evaluations_element = {}
        evaluations = [evaluations_element]
        expected_response = {
            "next_page_token": next_page_token,
            "evaluations": evaluations,
        }
        expected_response = data_labeling_service_pb2.SearchEvaluationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.search_evaluations(parent, filter_)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.evaluations[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.SearchEvaluationsRequest(
            parent=parent, filter=filter_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_evaluations_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.search_evaluations(parent, filter_)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_search_example_comparisons(self):
        # Setup Expected Response
        next_page_token = ""
        example_comparisons_element = {}
        example_comparisons = [example_comparisons_element]
        expected_response = {
            "next_page_token": next_page_token,
            "example_comparisons": example_comparisons,
        }
        expected_response = data_labeling_service_pb2.SearchExampleComparisonsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.evaluation_path("[PROJECT]", "[DATASET]", "[EVALUATION]")

        paged_list_response = client.search_example_comparisons(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.example_comparisons[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.SearchExampleComparisonsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_example_comparisons_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.evaluation_path("[PROJECT]", "[DATASET]", "[EVALUATION]")

        paged_list_response = client.search_example_comparisons(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_evaluation_job(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        model_version = "modelVersion-1669102142"
        annotation_spec_set = "annotationSpecSet1881405678"
        label_missing_ground_truth = False
        expected_response = {
            "name": name,
            "description": description,
            "schedule": schedule,
            "model_version": model_version,
            "annotation_spec_set": annotation_spec_set,
            "label_missing_ground_truth": label_missing_ground_truth,
        }
        expected_response = evaluation_job_pb2.EvaluationJob(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        job = {}

        response = client.create_evaluation_job(parent, job)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.CreateEvaluationJobRequest(
            parent=parent, job=job
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        job = {}

        with pytest.raises(CustomException):
            client.create_evaluation_job(parent, job)

    def test_update_evaluation_job(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        model_version = "modelVersion-1669102142"
        annotation_spec_set = "annotationSpecSet1881405678"
        label_missing_ground_truth = False
        expected_response = {
            "name": name,
            "description": description,
            "schedule": schedule,
            "model_version": model_version,
            "annotation_spec_set": annotation_spec_set,
            "label_missing_ground_truth": label_missing_ground_truth,
        }
        expected_response = evaluation_job_pb2.EvaluationJob(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        evaluation_job = {}
        update_mask = {}

        response = client.update_evaluation_job(evaluation_job, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.UpdateEvaluationJobRequest(
            evaluation_job=evaluation_job, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        evaluation_job = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_evaluation_job(evaluation_job, update_mask)

    def test_get_evaluation_job(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        schedule = "schedule-697920873"
        model_version = "modelVersion-1669102142"
        annotation_spec_set = "annotationSpecSet1881405678"
        label_missing_ground_truth = False
        expected_response = {
            "name": name_2,
            "description": description,
            "schedule": schedule,
            "model_version": model_version,
            "annotation_spec_set": annotation_spec_set,
            "label_missing_ground_truth": label_missing_ground_truth,
        }
        expected_response = evaluation_job_pb2.EvaluationJob(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        response = client.get_evaluation_job(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.GetEvaluationJobRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        with pytest.raises(CustomException):
            client.get_evaluation_job(name)

    def test_pause_evaluation_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        client.pause_evaluation_job(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.PauseEvaluationJobRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_pause_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        with pytest.raises(CustomException):
            client.pause_evaluation_job(name)

    def test_resume_evaluation_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        client.resume_evaluation_job(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ResumeEvaluationJobRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_resume_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        with pytest.raises(CustomException):
            client.resume_evaluation_job(name)

    def test_delete_evaluation_job(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        client.delete_evaluation_job(name)

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.DeleteEvaluationJobRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_evaluation_job_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        name = client.evaluation_job_path("[PROJECT]", "[EVALUATION_JOB]")

        with pytest.raises(CustomException):
            client.delete_evaluation_job(name)

    def test_list_evaluation_jobs(self):
        # Setup Expected Response
        next_page_token = ""
        evaluation_jobs_element = {}
        evaluation_jobs = [evaluation_jobs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "evaluation_jobs": evaluation_jobs,
        }
        expected_response = data_labeling_service_pb2.ListEvaluationJobsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_evaluation_jobs(parent, filter_)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.evaluation_jobs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.ListEvaluationJobsRequest(
            parent=parent, filter=filter_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_evaluation_jobs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_evaluation_jobs(parent, filter_)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_annotated_dataset(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        client.delete_annotated_dataset()

        assert len(channel.requests) == 1
        expected_request = data_labeling_service_pb2.DeleteAnnotatedDatasetRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_annotated_dataset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datalabeling_v1beta1.DataLabelingServiceClient()

        with pytest.raises(CustomException):
            client.delete_annotated_dataset()
