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

from __future__ import absolute_import

from concurrent import futures
import threading

from google.api_core import exceptions
from google.auth import credentials
import mock
import pytest
from six.moves import queue

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber.futures import Future
from google.cloud.pubsub_v1.subscriber.policy import base
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
    dispatch_thread = mock.Mock(spec=threading.Thread)
    leases_thread = mock.Mock(spec=threading.Thread)

    policy = create_policy()
    policy._dispatch_thread = dispatch_thread
    policy._leases_thread = leases_thread
    future = mock.Mock(spec=('done',))
    future.done.return_value = True
    policy._future = future

    consumer = policy._consumer
    with mock.patch.object(consumer, 'stop_consuming') as stop_consuming:
        closed_fut = policy.close()
        stop_consuming.assert_called_once_with()

    assert policy._dispatch_thread is None
    dispatch_thread.join.assert_called_once_with()
    assert policy._leases_thread is None
    leases_thread.join.assert_called_once_with()
    assert closed_fut is future
    assert policy._future is None
    future.done.assert_called_once_with()


def test_close_without_future():
    policy = create_policy()
    assert policy._future is None

    with pytest.raises(ValueError) as exc_info:
        policy.close()

    assert exc_info.value.args == ('This policy has not been opened yet.',)


def test_close_with_unfinished_future():
    dispatch_thread = mock.Mock(spec=threading.Thread)
    leases_thread = mock.Mock(spec=threading.Thread)

    policy = create_policy()
    policy._dispatch_thread = dispatch_thread
    policy._leases_thread = leases_thread
    policy._future = Future(policy=policy)
    consumer = policy._consumer
    with mock.patch.object(consumer, 'stop_consuming') as stop_consuming:
        future = policy.future
        closed_fut = policy.close()
        stop_consuming.assert_called_once_with()

    assert policy._dispatch_thread is None
    dispatch_thread.join.assert_called_once_with()
    assert policy._leases_thread is None
    leases_thread.join.assert_called_once_with()
    assert policy._future is None
    assert closed_fut is future
    assert future.result() is None


def test_open():
    policy = create_policy()
    consumer = policy._consumer
    threads = (
        mock.Mock(spec=('name', 'start')),
        mock.Mock(spec=('name', 'start')),
        mock.Mock(spec=('name', 'start')),
    )
    with mock.patch.object(threading, 'Thread', side_effect=threads):
        policy.open(mock.sentinel.CALLBACK)

    assert policy._callback is mock.sentinel.CALLBACK

    assert policy._dispatch_thread is threads[0]
    threads[0].start.assert_called_once_with()

    assert consumer._consumer_thread is threads[1]
    threads[1].start.assert_called_once_with()

    assert policy._leases_thread is threads[2]
    threads[2].start.assert_called_once_with()


def test_open_already_open():
    policy = create_policy()
    policy._future = mock.sentinel.future

    with pytest.raises(ValueError) as exc_info:
        policy.open(None)

    assert exc_info.value.args == ('This policy has already been opened.',)


@pytest.mark.parametrize('item,method', [
    (base.AckRequest(0, 0, 0), 'ack'),
    (base.DropRequest(0, 0), 'drop'),
    (base.LeaseRequest(0, 0), 'lease'),
    (base.ModAckRequest(0, 0), 'modify_ack_deadline'),
    (base.NackRequest(0, 0), 'nack')
])
def test_dispatch_callback_valid(item, method):
    policy = create_policy()
    with mock.patch.object(policy, method) as mocked:
        items = [item]
        policy.dispatch_callback(items)
        mocked.assert_called_once_with([item])


def test_on_exception_deadline_exceeded():
    policy = create_policy()

    details = 'Bad thing happened. Time out, go sit in the corner.'
    exc = exceptions.DeadlineExceeded(details)

    assert policy.on_exception(exc) is True


def test_on_exception_unavailable():
    policy = create_policy()

    details = 'UNAVAILABLE. Service taking nap.'
    exc = exceptions.ServiceUnavailable(details)

    assert policy.on_exception(exc) is True


def test_on_exception_other():
    policy = create_policy()
    policy._future = Future(policy=policy)
    exc = TypeError('wahhhhhh')
    assert policy.on_exception(exc) is False
    with pytest.raises(TypeError):
        policy.future.result()


def test_on_response():
    callback = mock.Mock(spec=())

    # Create mock ThreadPoolExecutor, pass into create_policy(), and verify
    # that both executor.submit() and future.add_done_callback are called
    # twice.
    future = mock.Mock()
    attrs = {'submit.return_value': future}
    executor = mock.Mock(**attrs)

    # Set up the policy.
    policy = create_policy(executor=executor)
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

    # Actually run the method and prove that modack and executor.submit
    # are called in the expected way.
    modack_patch = mock.patch.object(
        policy, 'modify_ack_deadline', autospec=True)
    with modack_patch as modack:
        policy.on_response(response)

    modack.assert_called_once_with(
        [base.ModAckRequest('fack', 10),
         base.ModAckRequest('back', 10)]
    )

    submit_calls = [m for m in executor.method_calls if m[0] == 'submit']
    assert len(submit_calls) == 2
    for call in submit_calls:
        assert call[1][0] == callback
        assert isinstance(call[1][1], message.Message)
