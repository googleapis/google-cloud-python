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
from six.moves import http_client
import urllib3

import google.auth.credentials
import google.auth.transport.urllib3
from tests.transport import compliance


class TestRequestResponse(compliance.RequestResponseTests):
    def make_request(self):
        http = urllib3.PoolManager()
        return google.auth.transport.urllib3.Request(http)

    def test_timeout(self):
        http = mock.create_autospec(urllib3.PoolManager)
        request = google.auth.transport.urllib3.Request(http)
        request(url='http://example.com', method='GET', timeout=5)

        assert http.request.call_args[1]['timeout'] == 5


def test__make_default_http_with_certfi():
    http = google.auth.transport.urllib3._make_default_http()
    assert 'cert_reqs' in http.connection_pool_kw


@mock.patch.object(google.auth.transport.urllib3, 'certifi', new=None)
def test__make_default_http_without_certfi():
    http = google.auth.transport.urllib3._make_default_http()
    assert 'cert_reqs' not in http.connection_pool_kw


class CredentialsStub(google.auth.credentials.Credentials):
    def __init__(self, token='token'):
        super(CredentialsStub, self).__init__()
        self.token = token

    def apply(self, headers, token=None):
        headers['authorization'] = self.token

    def before_request(self, request, method, url, headers):
        self.apply(headers)

    def refresh(self, request):
        self.token += '1'


class HttpStub(object):
    def __init__(self, responses, headers=None):
        self.responses = responses
        self.requests = []
        self.headers = headers or {}

    def urlopen(self, method, url, body=None, headers=None, **kwargs):
        self.requests.append((method, url, body, headers, kwargs))
        return self.responses.pop(0)


class ResponseStub(object):
    def __init__(self, status=http_client.OK, data=None):
        self.status = status
        self.data = data


class TestAuthorizedHttp(object):
    TEST_URL = 'http://example.com'

    def test_authed_http_defaults(self):
        authed_http = google.auth.transport.urllib3.AuthorizedHttp(
            mock.sentinel.credentials)

        assert authed_http.credentials == mock.sentinel.credentials
        assert isinstance(authed_http.http, urllib3.PoolManager)

    def test_urlopen_no_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        response = ResponseStub()
        http = HttpStub([response])

        authed_http = google.auth.transport.urllib3.AuthorizedHttp(
            credentials, http=http)

        result = authed_http.urlopen('GET', self.TEST_URL)

        assert result == response
        assert credentials.before_request.called
        assert not credentials.refresh.called
        assert http.requests == [
            ('GET', self.TEST_URL, None, {'authorization': 'token'}, {})]

    def test_urlopen_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = ResponseStub(status=http_client.OK)
        # First request will 401, second request will succeed.
        http = HttpStub([
            ResponseStub(status=http_client.UNAUTHORIZED),
            final_response])

        authed_http = google.auth.transport.urllib3.AuthorizedHttp(
            credentials, http=http)

        authed_http = authed_http.urlopen('GET', 'http://example.com')

        assert authed_http == final_response
        assert credentials.before_request.call_count == 2
        assert credentials.refresh.called
        assert http.requests == [
            ('GET', self.TEST_URL, None, {'authorization': 'token'}, {}),
            ('GET', self.TEST_URL, None, {'authorization': 'token1'}, {})]

    def test_proxies(self):
        http = mock.create_autospec(urllib3.PoolManager)
        authed_http = google.auth.transport.urllib3.AuthorizedHttp(
            None, http=http)

        with authed_http:
            pass

        assert http.__enter__.called
        assert http.__exit__.called

        authed_http.headers = mock.sentinel.headers
        assert authed_http.headers == http.headers
