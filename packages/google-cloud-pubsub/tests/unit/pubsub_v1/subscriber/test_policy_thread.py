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

from __future__ import absolute_import

from concurrent import futures
import queue
import threading

import grpc

import mock

import pytest

from google.auth import credentials
from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import _helper_threads
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_policy(**kwargs):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    return thread.Policy(client, 'sub_name_c', **kwargs)


def test_init():
    policy = create_policy()
    policy._callback(None)


def test_init_with_executor():
    executor = futures.ThreadPoolExecutor(max_workers=25)
    policy = create_policy(executor=executor, queue=queue.Queue())
    assert policy._executor is executor


def test_close():
    policy = create_policy()
    consumer = policy._consumer
    with mock.patch.object(consumer, 'stop_consuming') as stop_consuming:
        policy.close()
        stop_consuming.assert_called_once_with()
    assert 'callback request worker' not in policy._consumer.helper_threads


@mock.patch.object(_helper_threads.HelperThreadRegistry, 'start')
@mock.patch.object(threading.Thread, 'start')
def test_open(thread_start, htr_start):
    policy = create_policy()
    with mock.patch.object(policy._consumer, 'start_consuming') as consuming:
        policy.open(mock.sentinel.CALLBACK)
        assert policy._callback is mock.sentinel.CALLBACK
        consuming.assert_called_once_with()
        htr_start.assert_called()
        thread_start.assert_called()


def test_on_callback_request():
    policy = create_policy()
    with mock.patch.object(policy, 'call_rpc') as call_rpc:
        policy.on_callback_request(('call_rpc', {'something': 42}))
        call_rpc.assert_called_once_with(something=42)


def test_on_exception_deadline_exceeded():
    policy = create_policy()
    exc = mock.Mock(spec=('code',))
    exc.code.return_value = grpc.StatusCode.DEADLINE_EXCEEDED
    assert policy.on_exception(exc) is None


def test_on_exception_other():
    policy = create_policy()
    exc = TypeError('wahhhhhh')
    with pytest.raises(TypeError):
        policy.on_exception(exc)


def test_on_response():
    callback = mock.Mock(spec=())

    # Set up the policy.
    policy = create_policy()
    policy._callback = callback

    # Set up the messages to send.
    messages = (
        types.PubsubMessage(data=b'foo', message_id='1'),
        types.PubsubMessage(data=b'bar', message_id='2'),
    )

    # Set up a valid response.
    response = types.StreamingPullResponse(
        received_messages=[
            {'ack_id': 'fack', 'message': messages[0]},
            {'ack_id': 'back', 'message': messages[1]},
        ],
    )

    # Actually run the method and prove that the callback was
    # called in the expected way.
    policy.on_response(response)
    assert callback.call_count == 2
    for call in callback.mock_calls:
        assert isinstance(call[1][0], message.Message)
