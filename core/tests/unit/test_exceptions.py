# Copyright 2014 Google Inc.
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
import unittest

import requests
from six.moves import http_client

from google.cloud import exceptions


def test_create_google_cloud_error():
    exception = exceptions.GoogleCloudError('Testing')
    exception.code = 600
    assert str(exception) == '600 Testing'
    assert exception.message == 'Testing'
    assert exception.errors == []


def test_create_google_cloud_error_with_args():
    error = {
        'domain': 'global',
        'location': 'test',
        'locationType': 'testing',
        'message': 'Testing',
        'reason': 'test',
    }
    exception = exceptions.GoogleCloudError('Testing', [error])
    exception.code = 600
    assert str(exception) == '600 Testing'
    assert exception.message == 'Testing'
    assert exception.errors == [error]


def test_from_http_status():
    message = 'message'
    exception = exceptions.from_http_status(http_client.NOT_FOUND, message)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == message
    assert exception.errors == []


def test_from_http_status_with_errors():
    message = 'message'
    errors = ['1', '2']
    exception = exceptions.from_http_status(
        http_client.NOT_FOUND, message, errors=errors)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == message
    assert exception.errors == errors


def test_from_http_status_unknown_code():
    message = 'message'
    status_code = 156
    exception = exceptions.from_http_status(status_code, message)
    assert exception.code == status_code
    assert exception.message == message


def make_response(content):
    response = requests.Response()
    response._content = content
    response.status_code = http_client.NOT_FOUND
    response.request = requests.Request(
        method='POST', url='https://example.com').prepare()
    return response


def test_from_http_response_no_content():
    response = make_response(None)

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == 'POST https://example.com/: unknown error'
    assert exception.response == response


def test_from_http_response_text_content():
    response = make_response(b'message')

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == 'POST https://example.com/: message'


def test_from_http_response_json_content():
    response = make_response(json.dumps({
        'error': {
            'message': 'json message',
            'errors': ['1', '2']
        }
    }).encode('utf-8'))

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == 'POST https://example.com/: json message'
    assert exception.errors == ['1', '2']


def test_from_http_response_bad_json_content():
    response = make_response(json.dumps({'meep': 'moop'}).encode('utf-8'))

    exception = exceptions.from_http_response(response)

    assert isinstance(exception, exceptions.NotFound)
    assert exception.code == http_client.NOT_FOUND
    assert exception.message == 'POST https://example.com/: unknown error'


@unittest.skipUnless(exceptions._HAVE_GRPC, 'No gRPC')
class Test__catch_remap_gax_error(unittest.TestCase):

    def _call_fut(self):
        from google.cloud.exceptions import _catch_remap_gax_error

        return _catch_remap_gax_error()

    @staticmethod
    def _fake_method(exc, result=None):
        if exc is None:
            return result
        else:
            raise exc

    @staticmethod
    def _make_rendezvous(status_code, details):
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, status_code, details)
        return GrpcRendezvous(exc_state, None, None, None)

    def test_success(self):
        expected = object()
        with self._call_fut():
            result = self._fake_method(None, expected)
        self.assertIs(result, expected)

    def test_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        with self.assertRaises(RuntimeError):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode
        from google.cloud.exceptions import Forbidden

        # First, create low-level GrpcRendezvous exception.
        details = 'Some error details.'
        cause = self._make_rendezvous(StatusCode.PERMISSION_DENIED, details)
        # Then put it into a high-level GaxError.
        msg = 'GAX Error content.'
        exc = GaxError(msg, cause=cause)

        with self.assertRaises(Forbidden):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error_not_mapped(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode

        cause = self._make_rendezvous(StatusCode.CANCELLED, None)
        exc = GaxError(None, cause=cause)

        with self.assertRaises(GaxError):
            with self._call_fut():
                self._fake_method(exc)
