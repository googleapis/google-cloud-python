# Copyright 2017, Google LLC All rights reserved.
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

import time

import mock
from six.moves import queue

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import message


def create_message(data, ack_id='ACKID', **attrs):
    with mock.patch.object(message.Message, 'lease') as lease:
        with mock.patch.object(time, 'time') as time_:
            time_.return_value = 1335020400
            msg = message.Message(types.PubsubMessage(
                attributes=attrs,
                data=data,
                message_id='message_id',
                publish_time=types.Timestamp(seconds=1335020400 - 86400),
            ), ack_id, queue.Queue())
            lease.assert_called_once_with()
            return msg


def test_attributes():
    msg = create_message(b'foo', baz='bacon', spam='eggs')
    assert msg.attributes == {'baz': 'bacon', 'spam': 'eggs'}


def test_data():
    msg = create_message(b'foo')
    assert msg.data == b'foo'


def test_publish_time():
    msg = create_message(b'foo')
    assert msg.publish_time == types.Timestamp(seconds=1335020400 - 86400)


def test_ack():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        with mock.patch.object(message.Message, 'drop') as drop:
            msg.ack()
            put.assert_called_once_with(('ack', {
                'ack_id': 'bogus_ack_id',
                'byte_size': 25,
                'time_to_ack': mock.ANY,
            }))


def test_drop():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.drop()
        put.assert_called_once_with(('drop', {
            'ack_id': 'bogus_ack_id',
            'byte_size': 25,
        }))


def test_lease():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.lease()
        put.assert_called_once_with(('lease', {
            'ack_id': 'bogus_ack_id',
            'byte_size': 25,
        }))


def test_modify_ack_deadline():
    msg = create_message(b'foo', ack_id='bogus_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.modify_ack_deadline(60)
        put.assert_called_once_with(('modify_ack_deadline', {
            'ack_id': 'bogus_id',
            'seconds': 60,
        }))


def test_nack():
    msg = create_message(b'foo', ack_id='bogus_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.nack()
        put.assert_called_once_with(('nack', {
            'ack_id': 'bogus_id',
            'byte_size': 25,
        }))
