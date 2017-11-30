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

import types as base_types

from google.auth import credentials
import mock
import pytest
from six.moves import queue

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import _consumer
from google.cloud.pubsub_v1.subscriber import _helper_threads
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_consumer():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    subscription = client.subscribe('sub_name_e')
    return _consumer.Consumer(policy=subscription)


def test_send_request():
    consumer = create_consumer()
    request = types.StreamingPullRequest(subscription='foo')
    with mock.patch.object(queue.Queue, 'put') as put:
        consumer.send_request(request)
        put.assert_called_once_with(request)


def test_request_generator_thread():
    consumer = create_consumer()
    generator = consumer._request_generator_thread()

    # The first request that comes from the request generator thread
    # should always be the initial request.
    initial_request = next(generator)
    assert initial_request.subscription == 'sub_name_e'
    assert initial_request.stream_ack_deadline_seconds == 10

    # Subsequent requests correspond to items placed in the request queue.
    consumer.send_request(types.StreamingPullRequest(ack_ids=['i']))
    request = next(generator)
    assert request.ack_ids == ['i']

    # The poison pill should stop the loop.
    consumer.send_request(_helper_threads.STOP)
    with pytest.raises(StopIteration):
        next(generator)


def test_blocking_consume():
    consumer = create_consumer()
    Policy = type(consumer._policy)

    # Establish that we get responses until we run out of them.
    with mock.patch.object(Policy, 'call_rpc', autospec=True) as call_rpc:
        call_rpc.return_value = (mock.sentinel.A, mock.sentinel.B)
        with mock.patch.object(Policy, 'on_response', autospec=True) as on_res:
            consumer._blocking_consume()
            assert on_res.call_count == 2
            assert on_res.mock_calls[0][1][1] == mock.sentinel.A
            assert on_res.mock_calls[1][1][1] == mock.sentinel.B


class OnException(object):

    def __init__(self, exiting_event, acceptable=None):
        self.exiting_event = exiting_event
        self.acceptable = acceptable

    def __call__(self, exception):
        if exception is self.acceptable:
            return True
        else:
            self.exiting_event.set()
            return False


def test_blocking_consume_on_exception():
    policy = mock.Mock(spec=('call_rpc', 'on_response', 'on_exception'))
    policy.call_rpc.return_value = (mock.sentinel.A, mock.sentinel.B)
    exc = TypeError('Bad things!')
    policy.on_response.side_effect = exc

    consumer = _consumer.Consumer(policy=policy)
    policy.on_exception.side_effect = OnException(consumer._exiting)

    # Establish that we get responses until we are sent the exiting event.
    consumer._blocking_consume()

    # Check mocks.
    policy.call_rpc.assert_called_once()
    policy.on_response.assert_called_once_with(mock.sentinel.A)
    policy.on_exception.assert_called_once_with(exc)


def test_blocking_consume_two_exceptions():
    policy = mock.Mock(spec=('call_rpc', 'on_response', 'on_exception'))
    policy.call_rpc.side_effect = (
        (mock.sentinel.A,),
        (mock.sentinel.B,),
    )
    exc1 = NameError('Oh noes.')
    exc2 = ValueError('Something grumble.')
    policy.on_response.side_effect = (exc1, exc2)

    consumer = _consumer.Consumer(policy=policy)
    policy.on_exception.side_effect = OnException(
        consumer._exiting, acceptable=exc1)

    # Establish that we get responses until we are sent the exiting event.
    consumer._blocking_consume()

    # Check mocks.
    assert policy.call_rpc.call_count == 2
    policy.on_response.assert_has_calls(
        [mock.call(mock.sentinel.A), mock.call(mock.sentinel.B)])
    policy.on_exception.assert_has_calls(
        [mock.call(exc1), mock.call(exc2)])


def test_start_consuming():
    consumer = create_consumer()
    helper_threads = consumer.helper_threads
    with mock.patch.object(helper_threads, 'start', autospec=True) as start:
        consumer.start_consuming()
        assert consumer._exiting.is_set() is False
        assert consumer.active is True
        start.assert_called_once_with(
            'ConsumeBidirectionalStream',
            consumer._request_queue,
            consumer._blocking_consume,
        )
