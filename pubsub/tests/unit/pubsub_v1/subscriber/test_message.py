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

import time

import mock

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_message(data, ack_id='ACKID', **attrs):
    client = subscriber.Client()
    policy = thread.Policy(client, 'sub_name')
    with mock.patch.object(message.Message, 'lease') as lease:
        with mock.patch.object(time, 'time') as time_:
            time_.return_value = 1335020400
            msg = message.Message(policy, ack_id, types.PubsubMessage(
                attributes=attrs,
                data=data,
                message_id='message_id',
                publish_time=types.Timestamp(seconds=1335020400 - 86400),
            ))
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
    with mock.patch.object(thread.Policy, 'ack') as ack:
        with mock.patch.object(message.Message, 'drop') as drop:
            msg.ack()
            ack.assert_called_once_with('bogus_ack_id')
            drop.assert_called_once_with()


def test_drop():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(thread.Policy, 'drop') as drop:
        msg.drop()
        drop.assert_called_once_with('bogus_ack_id')


def test_lease():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(thread.Policy, 'lease') as lease:
        msg.lease()
        lease.assert_called_once_with('bogus_ack_id')


def test_modify_ack_deadline():
    msg = create_message(b'foo', ack_id='bogus_ack_id')
    with mock.patch.object(thread.Policy, 'modify_ack_deadline') as mad:
        msg.modify_ack_deadline(60)
        mad.assert_called_once_with('bogus_ack_id', 60)


def test_nack():
    msg = create_message(b'foo')
    with mock.patch.object(message.Message, 'modify_ack_deadline') as mad:
        with mock.patch.object(message.Message, 'drop') as drop:
            msg.nack()
            mad.assert_called_once_with(seconds=0)
            drop.assert_called_once_with()
