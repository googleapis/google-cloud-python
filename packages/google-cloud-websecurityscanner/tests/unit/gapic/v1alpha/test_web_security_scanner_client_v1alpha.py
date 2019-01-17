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

from google.cloud import websecurityscanner_v1alpha
from google.cloud.websecurityscanner_v1alpha.proto import crawled_url_pb2
from google.cloud.websecurityscanner_v1alpha.proto import finding_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_config_pb2
from google.cloud.websecurityscanner_v1alpha.proto import scan_run_pb2
from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2
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


class TestWebSecurityScannerClient(object):
    def test_create_scan_config(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        max_qps = 844445913
        expected_response = {
            "name": name,
            "display_name": display_name,
            "max_qps": max_qps,
        }
        expected_response = scan_config_pb2.ScanConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        scan_config = {}

        response = client.create_scan_config(parent, scan_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.CreateScanConfigRequest(
            parent=parent, scan_config=scan_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_scan_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        scan_config = {}

        with pytest.raises(CustomException):
            client.create_scan_config(parent, scan_config)

    def test_delete_scan_config(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        client.delete_scan_config(name)

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.DeleteScanConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_scan_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        with pytest.raises(CustomException):
            client.delete_scan_config(name)

    def test_get_scan_config(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        max_qps = 844445913
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "max_qps": max_qps,
        }
        expected_response = scan_config_pb2.ScanConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        response = client.get_scan_config(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.GetScanConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_scan_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        with pytest.raises(CustomException):
            client.get_scan_config(name)

    def test_list_scan_configs(self):
        # Setup Expected Response
        next_page_token = ""
        scan_configs_element = {}
        scan_configs = [scan_configs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "scan_configs": scan_configs,
        }
        expected_response = web_security_scanner_pb2.ListScanConfigsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_scan_configs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.scan_configs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.ListScanConfigsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_scan_configs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_scan_configs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_scan_config(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        max_qps = 844445913
        expected_response = {
            "name": name,
            "display_name": display_name,
            "max_qps": max_qps,
        }
        expected_response = scan_config_pb2.ScanConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        scan_config = {}
        update_mask = {}

        response = client.update_scan_config(scan_config, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.UpdateScanConfigRequest(
            scan_config=scan_config, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_scan_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        scan_config = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_scan_config(scan_config, update_mask)

    def test_start_scan_run(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        urls_crawled_count = 1749797253
        urls_tested_count = 1498664068
        has_vulnerabilities = False
        progress_percent = 2137894861
        expected_response = {
            "name": name_2,
            "urls_crawled_count": urls_crawled_count,
            "urls_tested_count": urls_tested_count,
            "has_vulnerabilities": has_vulnerabilities,
            "progress_percent": progress_percent,
        }
        expected_response = scan_run_pb2.ScanRun(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        response = client.start_scan_run(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.StartScanRunRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_start_scan_run_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        with pytest.raises(CustomException):
            client.start_scan_run(name)

    def test_get_scan_run(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        urls_crawled_count = 1749797253
        urls_tested_count = 1498664068
        has_vulnerabilities = False
        progress_percent = 2137894861
        expected_response = {
            "name": name_2,
            "urls_crawled_count": urls_crawled_count,
            "urls_tested_count": urls_tested_count,
            "has_vulnerabilities": has_vulnerabilities,
            "progress_percent": progress_percent,
        }
        expected_response = scan_run_pb2.ScanRun(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        response = client.get_scan_run(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.GetScanRunRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_scan_run_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        with pytest.raises(CustomException):
            client.get_scan_run(name)

    def test_list_scan_runs(self):
        # Setup Expected Response
        next_page_token = ""
        scan_runs_element = {}
        scan_runs = [scan_runs_element]
        expected_response = {"next_page_token": next_page_token, "scan_runs": scan_runs}
        expected_response = web_security_scanner_pb2.ListScanRunsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        paged_list_response = client.list_scan_runs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.scan_runs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.ListScanRunsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_scan_runs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.scan_config_path("[PROJECT]", "[SCAN_CONFIG]")

        paged_list_response = client.list_scan_runs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_stop_scan_run(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        urls_crawled_count = 1749797253
        urls_tested_count = 1498664068
        has_vulnerabilities = False
        progress_percent = 2137894861
        expected_response = {
            "name": name_2,
            "urls_crawled_count": urls_crawled_count,
            "urls_tested_count": urls_tested_count,
            "has_vulnerabilities": has_vulnerabilities,
            "progress_percent": progress_percent,
        }
        expected_response = scan_run_pb2.ScanRun(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        response = client.stop_scan_run(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.StopScanRunRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_stop_scan_run_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        with pytest.raises(CustomException):
            client.stop_scan_run(name)

    def test_list_crawled_urls(self):
        # Setup Expected Response
        next_page_token = ""
        crawled_urls_element = {}
        crawled_urls = [crawled_urls_element]
        expected_response = {
            "next_page_token": next_page_token,
            "crawled_urls": crawled_urls,
        }
        expected_response = web_security_scanner_pb2.ListCrawledUrlsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        paged_list_response = client.list_crawled_urls(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.crawled_urls[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.ListCrawledUrlsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_crawled_urls_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        paged_list_response = client.list_crawled_urls(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_finding(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        http_method = "httpMethod820747384"
        fuzzed_url = "fuzzedUrl-2120677666"
        body = "body3029410"
        description = "description-1724546052"
        reproduction_url = "reproductionUrl-244934180"
        frame_url = "frameUrl545464221"
        final_url = "finalUrl355601190"
        tracking_id = "trackingId1878901667"
        expected_response = {
            "name": name_2,
            "http_method": http_method,
            "fuzzed_url": fuzzed_url,
            "body": body,
            "description": description,
            "reproduction_url": reproduction_url,
            "frame_url": frame_url,
            "final_url": final_url,
            "tracking_id": tracking_id,
        }
        expected_response = finding_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        name = client.finding_path(
            "[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]", "[FINDING]"
        )

        response = client.get_finding(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.GetFindingRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_finding_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        name = client.finding_path(
            "[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]", "[FINDING]"
        )

        with pytest.raises(CustomException):
            client.get_finding(name)

    def test_list_findings(self):
        # Setup Expected Response
        next_page_token = ""
        findings_element = {}
        findings = [findings_element]
        expected_response = {"next_page_token": next_page_token, "findings": findings}
        expected_response = web_security_scanner_pb2.ListFindingsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_findings(parent, filter_)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.findings[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.ListFindingsRequest(
            parent=parent, filter=filter_
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_findings_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")
        filter_ = "filter-1274492040"

        paged_list_response = client.list_findings(parent, filter_)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_finding_type_stats(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = web_security_scanner_pb2.ListFindingTypeStatsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup Request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        response = client.list_finding_type_stats(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = web_security_scanner_pb2.ListFindingTypeStatsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_finding_type_stats_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = websecurityscanner_v1alpha.WebSecurityScannerClient()

        # Setup request
        parent = client.scan_run_path("[PROJECT]", "[SCAN_CONFIG]", "[SCAN_RUN]")

        with pytest.raises(CustomException):
            client.list_finding_type_stats(parent)
