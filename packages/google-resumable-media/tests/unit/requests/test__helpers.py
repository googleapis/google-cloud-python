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

from google.resumable_media.requests import _request_helpers

EXPECTED_TIMEOUT = (61, 60)


class TestRequestsMixin(object):
    def test__get_status_code(self):
        status_code = int(http_client.OK)
        response = _make_response(status_code)
        assert status_code == _request_helpers.RequestsMixin._get_status_code(response)

    def test__get_headers(self):
        headers = {u"fruit": u"apple"}
        response = mock.Mock(headers=headers, spec=["headers"])
        assert headers == _request_helpers.RequestsMixin._get_headers(response)

    def test__get_body(self):
        body = b"This is the payload."
        response = mock.Mock(content=body, spec=["content"])
        assert body == _request_helpers.RequestsMixin._get_body(response)


class TestRawRequestsMixin(object):
    def test__get_body_wo_content_consumed(self):
        body = b"This is the payload."
        raw = mock.Mock(spec=["stream"])
        raw.stream.return_value = iter([body])
        response = mock.Mock(raw=raw, _content=False, spec=["raw", "_content"])
        assert body == _request_helpers.RawRequestsMixin._get_body(response)
        raw.stream.assert_called_once_with(
            _request_helpers._SINGLE_GET_CHUNK_SIZE, decode_content=False
        )

    def test__get_body_w_content_consumed(self):
        body = b"This is the payload."
        response = mock.Mock(_content=body, spec=["_content"])
        assert body == _request_helpers.RawRequestsMixin._get_body(response)


def test_http_request():
    transport, responses = _make_transport(http_client.OK)
    method = u"POST"
    url = u"http://test.invalid"
    data = mock.sentinel.data
    headers = {u"one": u"fish", u"blue": u"fish"}
    timeout = mock.sentinel.timeout
    ret_val = _request_helpers.http_request(
        transport,
        method,
        url,
        data=data,
        headers=headers,
        extra1=b"work",
        extra2=125.5,
        timeout=timeout,
    )

    assert ret_val is responses[0]
    transport.request.assert_called_once_with(
        method,
        url,
        data=data,
        headers=headers,
        extra1=b"work",
        extra2=125.5,
        timeout=timeout,
    )


def test_http_request_defaults():
    transport, responses = _make_transport(http_client.OK)
    method = u"POST"
    url = u"http://test.invalid"
    ret_val = _request_helpers.http_request(transport, method, url)

    assert ret_val is responses[0]
    transport.request.assert_called_once_with(
        method, url, data=None, headers=None, timeout=EXPECTED_TIMEOUT
    )


def _make_response(status_code):
    return mock.Mock(status_code=status_code, spec=["status_code"])


def _make_transport(*status_codes):
    transport = mock.Mock(spec=["request"])
    responses = [_make_response(status_code) for status_code in status_codes]
    transport.request.side_effect = responses
    return transport, responses
