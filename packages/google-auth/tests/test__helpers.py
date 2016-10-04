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


import pytest

from google.auth import _helpers


def test_to_bytes_with_bytes():
    value = b'bytes-val'
    assert _helpers.to_bytes(value) == value


def test_to_bytes_with_unicode():
    value = u'string-val'
    encoded_value = b'string-val'
    assert _helpers.to_bytes(value) == encoded_value


def test_to_bytes_with_nonstring_type():
    with pytest.raises(ValueError):
        _helpers.to_bytes(object())


def test_from_bytes_with_unicode():
    value = u'bytes-val'
    assert _helpers.from_bytes(value) == value


def test_from_bytes_with_bytes():
    value = b'string-val'
    decoded_value = u'string-val'
    assert _helpers.from_bytes(value) == decoded_value


def test_from_bytes_with_nonstring_type():
    with pytest.raises(ValueError):
        _helpers.from_bytes(object())
