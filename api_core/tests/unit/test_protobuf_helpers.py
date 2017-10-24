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

import pytest

from google.api_core import protobuf_helpers
from google.protobuf import any_pb2
from google.protobuf.message import Message
from google.type import date_pb2
from google.type import timeofday_pb2


def test_from_any_pb_success():
    in_message = date_pb2.Date(year=1990)
    in_message_any = any_pb2.Any()
    in_message_any.Pack(in_message)
    out_message = protobuf_helpers.from_any_pb(date_pb2.Date, in_message_any)

    assert in_message == out_message


def test_from_any_pb_failure():
    in_message = any_pb2.Any()
    in_message.Pack(date_pb2.Date(year=1990))

    with pytest.raises(TypeError):
        protobuf_helpers.from_any_pb(timeofday_pb2.TimeOfDay, in_message)


def test_check_protobuf_helpers_ok():
    assert protobuf_helpers.check_oneof() is None
    assert protobuf_helpers.check_oneof(foo='bar') is None
    assert protobuf_helpers.check_oneof(foo='bar', baz=None) is None
    assert protobuf_helpers.check_oneof(foo=None, baz='bacon') is None
    assert (protobuf_helpers.check_oneof(foo='bar', spam=None, eggs=None)
            is None)


def test_check_protobuf_helpers_failures():
    with pytest.raises(ValueError):
        protobuf_helpers.check_oneof(foo='bar', spam='eggs')
    with pytest.raises(ValueError):
        protobuf_helpers.check_oneof(foo='bar', baz='bacon', spam='eggs')
    with pytest.raises(ValueError):
        protobuf_helpers.check_oneof(foo='bar', spam=0, eggs=None)


def test_get_messages():
    answer = protobuf_helpers.get_messages(date_pb2)

    # Ensure that Date was exported properly.
    assert answer['Date'] is date_pb2.Date

    # Ensure that no non-Message objects were exported.
    for value in answer.values():
        assert issubclass(value, Message)
