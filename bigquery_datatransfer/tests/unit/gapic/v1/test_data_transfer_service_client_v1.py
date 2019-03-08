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

from google.cloud import bigquery_datatransfer_v1
from google.cloud.bigquery_datatransfer_v1.proto import datatransfer_pb2
from google.cloud.bigquery_datatransfer_v1.proto import transfer_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


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


class TestDataTransferServiceClient(object):
    def test_get_data_source(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        data_source_id = "dataSourceId-1015796374"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        client_id = "clientId-1904089585"
        supports_multiple_transfers = True
        update_deadline_seconds = 991471694
        default_schedule = "defaultSchedule-800168235"
        supports_custom_schedule = True
        help_url = "helpUrl-789431439"
        default_data_refresh_window_days = 1804935157
        manual_runs_disabled = True
        expected_response = {
            "name": name_2,
            "data_source_id": data_source_id,
            "display_name": display_name,
            "description": description,
            "client_id": client_id,
            "supports_multiple_transfers": supports_multiple_transfers,
            "update_deadline_seconds": update_deadline_seconds,
            "default_schedule": default_schedule,
            "supports_custom_schedule": supports_custom_schedule,
            "help_url": help_url,
            "default_data_refresh_window_days": default_data_refresh_window_days,
            "manual_runs_disabled": manual_runs_disabled,
        }
        expected_response = datatransfer_pb2.DataSource(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_data_source_path("[PROJECT]", "[DATA_SOURCE]")

        response = client.get_data_source(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.GetDataSourceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_data_source_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_data_source_path("[PROJECT]", "[DATA_SOURCE]")

        with pytest.raises(CustomException):
            client.get_data_source(name)

    def test_list_data_sources(self):
        # Setup Expected Response
        next_page_token = ""
        data_sources_element = {}
        data_sources = [data_sources_element]
        expected_response = {
            "next_page_token": next_page_token,
            "data_sources": data_sources,
        }
        expected_response = datatransfer_pb2.ListDataSourcesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_data_sources(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.data_sources[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.ListDataSourcesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_data_sources_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_data_sources(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_transfer_config(self):
        # Setup Expected Response
        name = "name3373707"
        destination_dataset_id = "destinationDatasetId1541564179"
        display_name = "displayName1615086568"
        data_source_id = "dataSourceId-1015796374"
        schedule = "schedule-697920873"
        data_refresh_window_days = 327632845
        disabled = True
        user_id = 147132913
        dataset_region = "datasetRegion959248539"
        expected_response = {
            "name": name,
            "destination_dataset_id": destination_dataset_id,
            "display_name": display_name,
            "data_source_id": data_source_id,
            "schedule": schedule,
            "data_refresh_window_days": data_refresh_window_days,
            "disabled": disabled,
            "user_id": user_id,
            "dataset_region": dataset_region,
        }
        expected_response = transfer_pb2.TransferConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        transfer_config = {}

        response = client.create_transfer_config(parent, transfer_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.CreateTransferConfigRequest(
            parent=parent, transfer_config=transfer_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_transfer_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        transfer_config = {}

        with pytest.raises(CustomException):
            client.create_transfer_config(parent, transfer_config)

    def test_update_transfer_config(self):
        # Setup Expected Response
        name = "name3373707"
        destination_dataset_id = "destinationDatasetId1541564179"
        display_name = "displayName1615086568"
        data_source_id = "dataSourceId-1015796374"
        schedule = "schedule-697920873"
        data_refresh_window_days = 327632845
        disabled = True
        user_id = 147132913
        dataset_region = "datasetRegion959248539"
        expected_response = {
            "name": name,
            "destination_dataset_id": destination_dataset_id,
            "display_name": display_name,
            "data_source_id": data_source_id,
            "schedule": schedule,
            "data_refresh_window_days": data_refresh_window_days,
            "disabled": disabled,
            "user_id": user_id,
            "dataset_region": dataset_region,
        }
        expected_response = transfer_pb2.TransferConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        transfer_config = {}
        update_mask = {}

        response = client.update_transfer_config(transfer_config, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.UpdateTransferConfigRequest(
            transfer_config=transfer_config, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_transfer_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        transfer_config = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_transfer_config(transfer_config, update_mask)

    def test_delete_transfer_config(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        client.delete_transfer_config(name)

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.DeleteTransferConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_transfer_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        with pytest.raises(CustomException):
            client.delete_transfer_config(name)

    def test_get_transfer_config(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        destination_dataset_id = "destinationDatasetId1541564179"
        display_name = "displayName1615086568"
        data_source_id = "dataSourceId-1015796374"
        schedule = "schedule-697920873"
        data_refresh_window_days = 327632845
        disabled = True
        user_id = 147132913
        dataset_region = "datasetRegion959248539"
        expected_response = {
            "name": name_2,
            "destination_dataset_id": destination_dataset_id,
            "display_name": display_name,
            "data_source_id": data_source_id,
            "schedule": schedule,
            "data_refresh_window_days": data_refresh_window_days,
            "disabled": disabled,
            "user_id": user_id,
            "dataset_region": dataset_region,
        }
        expected_response = transfer_pb2.TransferConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        response = client.get_transfer_config(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.GetTransferConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_transfer_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        with pytest.raises(CustomException):
            client.get_transfer_config(name)

    def test_list_transfer_configs(self):
        # Setup Expected Response
        next_page_token = ""
        transfer_configs_element = {}
        transfer_configs = [transfer_configs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "transfer_configs": transfer_configs,
        }
        expected_response = datatransfer_pb2.ListTransferConfigsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_transfer_configs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.transfer_configs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.ListTransferConfigsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_transfer_configs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_transfer_configs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_schedule_transfer_runs(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = datatransfer_pb2.ScheduleTransferRunsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")
        start_time = {}
        end_time = {}

        response = client.schedule_transfer_runs(parent, start_time, end_time)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.ScheduleTransferRunsRequest(
            parent=parent, start_time=start_time, end_time=end_time
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_schedule_transfer_runs_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")
        start_time = {}
        end_time = {}

        with pytest.raises(CustomException):
            client.schedule_transfer_runs(parent, start_time, end_time)

    def test_get_transfer_run(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        destination_dataset_id = "destinationDatasetId1541564179"
        data_source_id = "dataSourceId-1015796374"
        user_id = 147132913
        schedule = "schedule-697920873"
        expected_response = {
            "name": name_2,
            "destination_dataset_id": destination_dataset_id,
            "data_source_id": data_source_id,
            "user_id": user_id,
            "schedule": schedule,
        }
        expected_response = transfer_pb2.TransferRun(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        response = client.get_transfer_run(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.GetTransferRunRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_transfer_run_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        with pytest.raises(CustomException):
            client.get_transfer_run(name)

    def test_delete_transfer_run(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        client.delete_transfer_run(name)

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.DeleteTransferRunRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_transfer_run_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        with pytest.raises(CustomException):
            client.delete_transfer_run(name)

    def test_list_transfer_runs(self):
        # Setup Expected Response
        next_page_token = ""
        transfer_runs_element = {}
        transfer_runs = [transfer_runs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "transfer_runs": transfer_runs,
        }
        expected_response = datatransfer_pb2.ListTransferRunsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        paged_list_response = client.list_transfer_runs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.transfer_runs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.ListTransferRunsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_transfer_runs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_transfer_config_path("[PROJECT]", "[TRANSFER_CONFIG]")

        paged_list_response = client.list_transfer_runs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_transfer_logs(self):
        # Setup Expected Response
        next_page_token = ""
        transfer_messages_element = {}
        transfer_messages = [transfer_messages_element]
        expected_response = {
            "next_page_token": next_page_token,
            "transfer_messages": transfer_messages,
        }
        expected_response = datatransfer_pb2.ListTransferLogsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        parent = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        paged_list_response = client.list_transfer_logs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.transfer_messages[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.ListTransferLogsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_transfer_logs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        parent = client.project_run_path("[PROJECT]", "[TRANSFER_CONFIG]", "[RUN]")

        paged_list_response = client.list_transfer_logs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_check_valid_creds(self):
        # Setup Expected Response
        has_valid_creds = False
        expected_response = {"has_valid_creds": has_valid_creds}
        expected_response = datatransfer_pb2.CheckValidCredsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup Request
        name = client.project_data_source_path("[PROJECT]", "[DATA_SOURCE]")

        response = client.check_valid_creds(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datatransfer_pb2.CheckValidCredsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_check_valid_creds_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_datatransfer_v1.DataTransferServiceClient()

        # Setup request
        name = client.project_data_source_path("[PROJECT]", "[DATA_SOURCE]")

        with pytest.raises(CustomException):
            client.check_valid_creds(name)
