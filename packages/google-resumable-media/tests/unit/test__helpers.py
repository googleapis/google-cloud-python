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
import pytest
from six.moves import http_client

from google.resumable_media import _helpers
from google.resumable_media import exceptions


def test__do_nothing():
    ret_val = _helpers._do_nothing()
    assert ret_val is None


def test_get_headers():
    headers = {u'fruit': u'apple'}
    response = mock.Mock(headers=headers, spec=[u'headers'])
    assert headers == _helpers.get_headers(response)


class Test_header_required(object):

    def test_success(self):
        name = u'some-header'
        value = u'The Right Hand Side'
        headers = {name: value, u'other-name': u'other-value'}
        response = mock.Mock(headers=headers, spec=[u'headers'])
        result = _helpers.header_required(response, name)
        assert result == value

    def test_failure(self):
        response = mock.Mock(headers={}, spec=[u'headers'])
        name = u'any-name'
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            _helpers.header_required(response, name)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 2
        assert error.args[1] == name


def test_get_status_code():
    status_code = 200
    response = mock.Mock(status_code=status_code, spec=[u'status_code'])
    assert status_code == _helpers.get_status_code(response)


def test_get_body():
    body = b'This is the payload.'
    response = mock.Mock(content=body, spec=[u'content'])
    assert body == _helpers.get_body(response)


class Test_require_status_code(object):

    def test_success(self):
        status_codes = (http_client.OK, http_client.CREATED)
        acceptable = (
            http_client.OK,
            int(http_client.OK),
            http_client.CREATED,
            int(http_client.CREATED),
        )
        for value in acceptable:
            response = mock.Mock(status_code=value, spec=[u'status_code'])
            status_code = _helpers.require_status_code(response, status_codes)
            assert value == status_code

    def test_failure(self):
        status_codes = (http_client.CREATED, http_client.NO_CONTENT)
        response = mock.Mock(status_code=http_client.OK, spec=[u'status_code'])
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            _helpers.require_status_code(response, status_codes)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 5
        assert error.args[1] == response.status_code
        assert error.args[3:] == status_codes
