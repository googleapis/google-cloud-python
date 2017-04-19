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

from gooresmed import _helpers
from gooresmed import exceptions


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
