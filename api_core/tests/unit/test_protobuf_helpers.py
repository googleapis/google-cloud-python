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

from google.api import http_pb2
from google.api_core import protobuf_helpers
from google.longrunning import operations_pb2
from google.protobuf import any_pb2
from google.protobuf import timestamp_pb2
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


def test_get_dict_absent():
    with pytest.raises(KeyError):
        assert protobuf_helpers.get({}, 'foo')


def test_get_dict_present():
    assert protobuf_helpers.get({'foo': 'bar'}, 'foo') == 'bar'


def test_get_dict_default():
    assert protobuf_helpers.get({}, 'foo', default='bar') == 'bar'


def test_get_dict_nested():
    assert protobuf_helpers.get({'foo': {'bar': 'baz'}}, 'foo.bar') == 'baz'


def test_get_dict_nested_default():
    assert protobuf_helpers.get({}, 'foo.baz', default='bacon') == 'bacon'
    assert (
        protobuf_helpers.get({'foo': {}}, 'foo.baz', default='bacon') ==
        'bacon')


def test_get_msg_sentinel():
    msg = timestamp_pb2.Timestamp()
    with pytest.raises(KeyError):
        assert protobuf_helpers.get(msg, 'foo')


def test_get_msg_present():
    msg = timestamp_pb2.Timestamp(seconds=42)
    assert protobuf_helpers.get(msg, 'seconds') == 42


def test_get_msg_default():
    msg = timestamp_pb2.Timestamp()
    assert protobuf_helpers.get(msg, 'foo', default='bar') == 'bar'


def test_invalid_object():
    with pytest.raises(TypeError):
        protobuf_helpers.get(object(), 'foo', 'bar')


def test_set_dict():
    mapping = {}
    protobuf_helpers.set(mapping, 'foo', 'bar')
    assert mapping == {'foo': 'bar'}


def test_set_msg():
    msg = timestamp_pb2.Timestamp()
    protobuf_helpers.set(msg, 'seconds', 42)
    assert msg.seconds == 42


def test_set_dict_nested():
    mapping = {}
    protobuf_helpers.set(mapping, 'foo.bar', 'baz')
    assert mapping == {'foo': {'bar': 'baz'}}


def test_set_invalid_object():
    with pytest.raises(TypeError):
        protobuf_helpers.set(object(), 'foo', 'bar')


def test_set_list():
    list_ops_response = operations_pb2.ListOperationsResponse()

    protobuf_helpers.set(list_ops_response, 'operations', [
        {'name': 'foo'},
        operations_pb2.Operation(name='bar'),
    ])

    assert len(list_ops_response.operations) == 2

    for operation in list_ops_response.operations:
        assert isinstance(operation, operations_pb2.Operation)

    assert list_ops_response.operations[0].name == 'foo'
    assert list_ops_response.operations[1].name == 'bar'


def test_set_list_clear_existing():
    list_ops_response = operations_pb2.ListOperationsResponse(
        operations=[{'name': 'baz'}],
    )

    protobuf_helpers.set(list_ops_response, 'operations', [
        {'name': 'foo'},
        operations_pb2.Operation(name='bar'),
    ])

    assert len(list_ops_response.operations) == 2
    for operation in list_ops_response.operations:
        assert isinstance(operation, operations_pb2.Operation)
    assert list_ops_response.operations[0].name == 'foo'
    assert list_ops_response.operations[1].name == 'bar'


def test_set_msg_with_msg_field():
    rule = http_pb2.HttpRule()
    pattern = http_pb2.CustomHttpPattern(kind='foo', path='bar')

    protobuf_helpers.set(rule, 'custom', pattern)

    assert rule.custom.kind == 'foo'
    assert rule.custom.path == 'bar'


def test_set_msg_with_dict_field():
    rule = http_pb2.HttpRule()
    pattern = {'kind': 'foo', 'path': 'bar'}

    protobuf_helpers.set(rule, 'custom', pattern)

    assert rule.custom.kind == 'foo'
    assert rule.custom.path == 'bar'


def test_set_msg_nested_key():
    rule = http_pb2.HttpRule(
        custom=http_pb2.CustomHttpPattern(kind='foo', path='bar'))

    protobuf_helpers.set(rule, 'custom.kind', 'baz')

    assert rule.custom.kind == 'baz'
    assert rule.custom.path == 'bar'


def test_setdefault_dict_unset():
    mapping = {}
    protobuf_helpers.setdefault(mapping, 'foo', 'bar')
    assert mapping == {'foo': 'bar'}


def test_setdefault_dict_falsy():
    mapping = {'foo': None}
    protobuf_helpers.setdefault(mapping, 'foo', 'bar')
    assert mapping == {'foo': 'bar'}


def test_setdefault_dict_truthy():
    mapping = {'foo': 'bar'}
    protobuf_helpers.setdefault(mapping, 'foo', 'baz')
    assert mapping == {'foo': 'bar'}


def test_setdefault_pb2_falsy():
    operation = operations_pb2.Operation()
    protobuf_helpers.setdefault(operation, 'name', 'foo')
    assert operation.name == 'foo'


def test_setdefault_pb2_truthy():
    operation = operations_pb2.Operation(name='bar')
    protobuf_helpers.setdefault(operation, 'name', 'foo')
    assert operation.name == 'bar'
