# Copyright 2017 Google Inc.
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

import mock
from six.moves import http_client

from google.resumable_media.requests import _helpers


class TestRequestsMixin(object):

    def test__get_status_code(self):
        status_code = int(http_client.OK)
        response = _make_response(status_code)
        assert status_code == _helpers.RequestsMixin._get_status_code(response)

    def test__get_headers(self):
        headers = {u'fruit': u'apple'}
        response = mock.Mock(headers=headers, spec=[u'headers'])
        assert headers == _helpers.RequestsMixin._get_headers(response)

    def test__get_body(self):
        body = b'This is the payload.'
        response = mock.Mock(content=body, spec=[u'content'])
        assert body == _helpers.RequestsMixin._get_body(response)


def test_http_request():
    transport, responses = _make_transport(http_client.OK)
    method = u'POST'
    url = u'http://test.invalid'
    data = mock.sentinel.data
    headers = {u'one': u'fish', u'blue': u'fish'}
    ret_val = _helpers.http_request(
        transport, method, url, data=data, headers=headers)

    assert ret_val is responses[0]
    transport.request.assert_called_once_with(
        method, url, data=data, headers=headers)


def _make_response(status_code):
    return mock.Mock(status_code=status_code, spec=[u'status_code'])


def _make_transport(*status_codes):
    transport = mock.Mock(spec=[u'request'])
    responses = [
        _make_response(status_code) for status_code in status_codes]
    transport.request.side_effect = responses
    return transport, responses
