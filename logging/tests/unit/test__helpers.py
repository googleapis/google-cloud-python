# Copyright 2016 Google LLC
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


import unittest

import mock


class Test_entry_from_resource(unittest.TestCase):
    @staticmethod
    def _call_fut(resource, client, loggers):
        from google.cloud.logging._helpers import entry_from_resource

        return entry_from_resource(resource, client, loggers)

    def _payload_helper(self, key, class_name):
        import mock

        resource = {}
        if key is not None:
            resource[key] = "yup"
        client = object()
        loggers = {}
        mock_class = EntryMock()

        name = "google.cloud.logging._helpers." + class_name
        with mock.patch(name, new=mock_class):
            result = self._call_fut(resource, client, loggers)

        self.assertIs(result, mock_class.sentinel)
        self.assertEqual(mock_class.called, (resource, client, loggers))

    def test_wo_payload(self):
        self._payload_helper(None, "LogEntry")

    def test_text_payload(self):
        self._payload_helper("textPayload", "TextEntry")

    def test_json_payload(self):
        self._payload_helper("jsonPayload", "StructEntry")

    def test_proto_payload(self):
        self._payload_helper("protoPayload", "ProtobufEntry")


class Test_retrieve_metadata_server(unittest.TestCase):
    @staticmethod
    def _call_fut(metadata_key):
        from google.cloud.logging._helpers import retrieve_metadata_server

        return retrieve_metadata_server(metadata_key)

    def test_metadata_exists(self):
        status_code_ok = 200
        response_text = "my-gke-cluster"
        metadata_key = "test_key"

        response_mock = ResponseMock(status_code=status_code_ok)
        response_mock.text = response_text

        requests_mock = mock.Mock()
        requests_mock.get.return_value = response_mock
        requests_mock.codes.ok = status_code_ok

        patch = mock.patch("google.cloud.logging._helpers.requests", requests_mock)

        with patch:
            metadata = self._call_fut(metadata_key)

        self.assertEqual(metadata, response_text)

    def test_metadata_does_not_exist(self):
        status_code_ok = 200
        status_code_not_found = 404
        metadata_key = "test_key"

        response_mock = ResponseMock(status_code=status_code_not_found)

        requests_mock = mock.Mock()
        requests_mock.get.return_value = response_mock
        requests_mock.codes.ok = status_code_ok

        patch = mock.patch("google.cloud.logging._helpers.requests", requests_mock)

        with patch:
            metadata = self._call_fut(metadata_key)

        self.assertIsNone(metadata)

    def test_request_exception(self):
        import requests

        metadata_key = "test_url_cannot_connect"
        metadata_url = "http://metadata.invalid/"

        requests_get_mock = mock.Mock(spec=["__call__"])
        requests_get_mock.side_effect = requests.exceptions.RequestException

        requests_get_patch = mock.patch("requests.get", requests_get_mock)

        url_patch = mock.patch(
            "google.cloud.logging._helpers.METADATA_URL", new=metadata_url
        )

        with requests_get_patch:
            with url_patch:
                metadata = self._call_fut(metadata_key)

        self.assertIsNone(metadata)


class EntryMock(object):
    def __init__(self):
        self.sentinel = object()
        self.called = None

    def from_api_repr(self, resource, client, loggers):
        self.called = (resource, client, loggers)
        return self.sentinel


class ResponseMock(object):
    def __init__(self, status_code, text="test_response_text"):
        self.status_code = status_code
        self.text = text
