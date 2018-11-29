# Copyright 2014 Google LLC
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

import json

import requests
from six.moves import http_client

from google.cloud import exceptions


def test_create_google_cloud_error():
    exception = exceptions.GoogleCloudError("Testing")
    exception.code = 600
    assert str(exception) == "600 Testing"
    assert exception.message == "Testing"
    assert exception.errors == []


def test_create_google_cloud_error_with_args():
    error = {
        "domain": "global",
        "location": "test",
        "locationType": "testing",
        "message": "Testing",
        "reason": "test",
    }
    exception = exceptions.GoogleCloudError("Testing", [error])
    exception.code = 600
    assert str(exception) == "600 Testing"
    assert exception.message == "Testing"
    assert exception.errors == [error]


def test_from_http_status():
    message = "message"
    exception = exceptions.from_http_status(http_client.NOT_FOUND, message)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == message
    assert exception.errors == []


def test_from_http_status_with_errors():
    message = "message"
    errors = ["1", "2"]
    exception = exceptions.from_http_status(
        http_client.NOT_FOUND, message, errors=errors
    )

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == message
    assert exception.errors == errors


def test_from_http_status_unknown_code():
    message = "message"
    status_code = 156
    exception = exceptions.from_http_status(status_code, message)
    assert exception.code == status_code
    assert exception.message == message


def make_response(content):
    response = requests.Response()
    response._content = content
    response.status_code = http_client.NOT_FOUND
    response.request = requests.Request(
        method="POST", url="https://example.com"
    ).prepare()
    return response


def test_from_http_response_no_content():
    response = make_response(None)

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == "POST https://example.com/: unknown error"
    assert exception.response == response


def test_from_http_response_text_content():
    response = make_response(b"message")

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == "POST https://example.com/: message"


def test_from_http_response_json_content():
    response = make_response(
        json.dumps({"error": {"message": "json message", "errors": ["1", "2"]}}).encode(
            "utf-8"
        )
    )

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == "POST https://example.com/: json message"
    assert exception.errors == ["1", "2"]


def test_from_http_response_bad_json_content():
    response = make_response(json.dumps({"meep": "moop"}).encode("utf-8"))

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == "POST https://example.com/: unknown error"
