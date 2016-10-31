# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import requests
import requests.adapters
from six.moves import http_client

import google.auth.transport.requests
from tests.transport import compliance


class TestRequestResponse(compliance.RequestResponseTests):
    def make_request(self):
        return google.auth.transport.requests.Request()

    def test_timeout(self):
        http = mock.Mock()
        request = google.auth.transport.requests.Request(http)
        request(url='http://example.com', method='GET', timeout=5)

        assert http.request.call_args[1]['timeout'] == 5


class MockCredentials(object):
    def __init__(self, token='token'):
        self.token = token

    def apply(self, headers):
        headers['authorization'] = self.token

    def before_request(self, request, method, url, headers):
        self.apply(headers)

    def refresh(self, request):
        self.token += '1'


class MockAdapter(requests.adapters.BaseAdapter):
    def __init__(self, responses, headers=None):
        self.responses = responses
        self.requests = []
        self.headers = headers or {}

    def send(self, request, **kwargs):
        self.requests.append(request)
        return self.responses.pop(0)


def make_response(status=http_client.OK, data=None):
    response = requests.Response()
    response.status_code = status
    response._content = data
    return response


class TestAuthorizedHttp(object):
    TEST_URL = 'http://example.com/'

    def test_constructor(self):
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials)

        assert authed_session.credentials == mock.sentinel.credentials

    def test_request_no_refresh(self):
        mock_credentials = mock.Mock(wraps=MockCredentials())
        mock_response = make_response()
        mock_adapter = MockAdapter([mock_response])

        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock_credentials)
        authed_session.mount(self.TEST_URL, mock_adapter)

        response = authed_session.request('GET', self.TEST_URL)

        assert response == mock_response
        assert mock_credentials.before_request.called
        assert not mock_credentials.refresh.called
        assert len(mock_adapter.requests) == 1
        assert mock_adapter.requests[0].url == self.TEST_URL
        assert mock_adapter.requests[0].headers['authorization'] == 'token'

    def test_request_refresh(self):
        mock_credentials = mock.Mock(wraps=MockCredentials())
        mock_final_response = make_response(status=http_client.OK)
        # First request will 401, second request will succeed.
        mock_adapter = MockAdapter([
            make_response(status=http_client.UNAUTHORIZED),
            mock_final_response])

        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock_credentials)
        authed_session.mount(self.TEST_URL, mock_adapter)

        response = authed_session.request('GET', self.TEST_URL)

        assert response == mock_final_response
        assert mock_credentials.before_request.call_count == 2
        assert mock_credentials.refresh.called
        assert len(mock_adapter.requests) == 2

        assert mock_adapter.requests[0].url == self.TEST_URL
        assert mock_adapter.requests[0].headers['authorization'] == 'token'

        assert mock_adapter.requests[1].url == self.TEST_URL
        assert mock_adapter.requests[1].headers['authorization'] == 'token1'
