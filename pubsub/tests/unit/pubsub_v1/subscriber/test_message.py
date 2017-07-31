# Copyright 2017, Google Inc. All rights reserved.
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

import queue
import time

import mock

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
            put.assert_called_once_with(('ack', 'bogus_ack_id', mock.ANY))
            drop.assert_called_once_with()


def test_drop():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.drop()
        put.assert_called_once_with(('drop', 'bogus_ack_id'))


def test_lease():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.lease()
        put.assert_called_once_with(('lease', 'bogus_ack_id'))


def test_modify_ack_deadline():
    msg = create_message(b'foo', ack_id='bogus_id')
    with mock.patch.object(msg._request_queue, 'put') as put:
        msg.modify_ack_deadline(60)
        put.assert_called_once_with(('modify_ack_deadline', 'bogus_id', 60))


def test_nack():
    msg = create_message(b'foo')
    with mock.patch.object(message.Message, 'modify_ack_deadline') as mad:
        with mock.patch.object(message.Message, 'drop') as drop:
            msg.nack()
            mad.assert_called_once_with(seconds=0)
            drop.assert_called_once_with()
