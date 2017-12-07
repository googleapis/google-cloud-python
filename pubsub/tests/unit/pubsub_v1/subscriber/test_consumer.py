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

import threading
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


def test_send_request():
    consumer = _consumer.Consumer()
    request = types.StreamingPullRequest(subscription='foo')
    with mock.patch.object(queue.Queue, 'put') as put:
        consumer.send_request(request)
        put.assert_called_once_with(request)


def test_request_generator_thread():
    consumer = _consumer.Consumer()
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    policy = client.subscribe('sub_name_e')
    generator = consumer._request_generator_thread(policy)

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
    policy = mock.Mock(spec=('call_rpc', 'on_response'))
    policy.call_rpc.return_value = (mock.sentinel.A, mock.sentinel.B)

    consumer = _consumer.Consumer()
    assert consumer._blocking_consume(policy) is None
    policy.call_rpc.assert_called_once()
    policy.on_response.assert_has_calls(
        [mock.call(mock.sentinel.A), mock.call(mock.sentinel.B)])


@mock.patch.object(_consumer, '_LOGGER')
def test_blocking_consume_when_exiting(_LOGGER):
    consumer = _consumer.Consumer()
    assert consumer.stopped.is_set() is False
    consumer.stopped.set()

    # Make sure method cleanly exits.
    assert consumer._blocking_consume(None) is None

    _LOGGER.debug.assert_called_once_with('Event signalled consumer exit.')


class OnException(object):

    def __init__(self, acceptable=None):
        self.acceptable = acceptable

    def __call__(self, exception):
        if exception is self.acceptable:
            return True
        else:
            return False


def test_blocking_consume_on_exception():
    policy = mock.Mock(spec=('call_rpc', 'on_response', 'on_exception'))
    policy.call_rpc.return_value = (mock.sentinel.A, mock.sentinel.B)
    exc = TypeError('Bad things!')
    policy.on_response.side_effect = exc

    consumer = _consumer.Consumer()
    consumer._consumer_thread = mock.Mock(spec=threading.Thread)
    policy.on_exception.side_effect = OnException()

    # Establish that we get responses until we are sent the exiting event.
    consumer._blocking_consume(policy)
    assert consumer._consumer_thread is None

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

    consumer = _consumer.Consumer()
    consumer._consumer_thread = mock.Mock(spec=threading.Thread)
    policy.on_exception.side_effect = OnException(acceptable=exc1)

    # Establish that we get responses until we are sent the exiting event.
    consumer._blocking_consume(policy)
    assert consumer._consumer_thread is None

    # Check mocks.
    assert policy.call_rpc.call_count == 2
    policy.on_response.assert_has_calls(
        [mock.call(mock.sentinel.A), mock.call(mock.sentinel.B)])
    policy.on_exception.assert_has_calls(
        [mock.call(exc1), mock.call(exc2)])


def test_start_consuming():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    policy = client.subscribe('sub_name_e')
    consumer = _consumer.Consumer()
    with mock.patch.object(threading, 'Thread', autospec=True) as Thread:
        consumer.start_consuming(policy)

    assert consumer.stopped.is_set() is False
    Thread.assert_called_once_with(
        name=_consumer._BIDIRECTIONAL_CONSUMER_NAME,
        target=consumer._blocking_consume,
        args=(policy,),
    )
    assert consumer._consumer_thread is Thread.return_value


def test_stop_consuming():
    consumer = _consumer.Consumer()
    assert consumer.stopped.is_set() is False
    thread = mock.Mock(spec=threading.Thread)
    consumer._consumer_thread = thread

    assert consumer.stop_consuming() is None

    # Make sure state was updated.
    assert consumer.stopped.is_set() is True
    assert consumer._consumer_thread is None
    # Check mocks.
    thread.join.assert_called_once_with()


def basic_queue_generator(queue, received):
    while True:
        value = queue.get()
        received.put(value)
        yield value


def test_stop_request_generator_not_running():
    # Model scenario tested:
    # - The request generator **is not** running
    # - The request queue **is not** empty
    # Expected result:
    # - ``_stop_request_generator()`` successfully calls ``.close()``
    consumer = _consumer.Consumer()
    queue_ = consumer._request_queue
    received = queue.Queue()
    request_generator = basic_queue_generator(queue_, received)

    item1 = 'unblock-please'
    item2 = 'still-here'
    queue_.put(item1)
    queue_.put(item2)
    assert not queue_.empty()
    assert received.empty()
    thread = threading.Thread(target=next, args=(request_generator,))
    thread.start()

    # Make sure the generator is not stuck at the blocked ``.get()``
    # in the thread.
    while request_generator.gi_running:
        pass
    assert received.get() == item1
    # Make sure it **isn't** done.
    assert request_generator.gi_frame is not None

    stopped = consumer._stop_request_generator(request_generator)
    assert stopped is True

    # Make sure it **is** done.
    assert not request_generator.gi_running
    assert request_generator.gi_frame is None
    assert not queue_.empty()
    assert queue_.get() == item2
    assert queue_.empty()


def test_stop_request_generator_close_failure():
    # Model scenario tested:
    # - The input isn't actually a generator
    # Expected result:
    # - ``_stop_request_generator()`` falls through to the ``LOGGER.error``
    #   case and returns ``False``
    consumer = _consumer.Consumer()

    request_generator = mock.Mock(spec=('close',))
    request_generator.close.side_effect = TypeError('Really, not a generator')

    stopped = consumer._stop_request_generator(request_generator)
    assert stopped is False

    # Make sure close() was only called once.
    request_generator.close.assert_called_once_with()


def test_stop_request_generator_queue_non_empty():
    # Model scenario tested:
    # - The request generator **is** running
    # - The request queue **is not** empty
    # Expected result:
    # - ``_stop_request_generator()`` can't call ``.close()`` (since
    #   the generator is running) but then returns with ``False`` because
    #   the queue **is not** empty
    consumer = _consumer.Consumer()
    # Attach a "fake" queue to the request generator so the generator can
    # block on an empty queue while the consumer's queue is not empty.
    queue_ = queue.Queue()
    received = queue.Queue()
    request_generator = basic_queue_generator(queue_, received)
    # Make sure the consumer's queue is not empty.
    item1 = 'not-empty'
    consumer._request_queue.put(item1)

    thread = threading.Thread(target=next, args=(request_generator,))
    thread.start()

    # Make sure the generator is stuck at the blocked ``.get()``
    # in ``thread``.
    while not request_generator.gi_running:
        pass
    assert received.empty()
    assert request_generator.gi_frame is not None

    stopped = consumer._stop_request_generator(request_generator)
    assert stopped is False

    # Make sure the generator is **still** not finished.
    assert request_generator.gi_running
    assert request_generator.gi_frame is not None
    assert consumer._request_queue.get() == item1
    # Allow the generator to exit.
    item2 = 'just-exit'
    queue_.put(item2)
    # Wait until it's actually done.
    while request_generator.gi_running:
        pass
    assert received.get() == item2


def test_stop_request_generator_running():
    # Model scenario tested:
    # - The request generator **is** running
    # - The request queue **is** empty
    # Expected result:
    # - ``_stop_request_generator()`` can't call ``.close()`` (since
    #   the generator is running) but then verifies that the queue is
    #   empty and sends ``STOP`` into the queue to successfully stop
    #   the generator
    consumer = _consumer.Consumer()
    queue_ = consumer._request_queue
    received = queue.Queue()
    request_generator = basic_queue_generator(queue_, received)

    thread = threading.Thread(target=next, args=(request_generator,))
    thread.start()

    # Make sure the generator is stuck at the blocked ``.get()``
    # in the thread.
    while not request_generator.gi_running:
        pass
    assert received.empty()
    assert request_generator.gi_frame is not None

    stopped = consumer._stop_request_generator(request_generator)
    assert stopped is True

    # Make sure it **is** done, though we may have to wait until
    # the generator finishes (it has a few instructions between the
    # ``get()`` and the ``break``).
    while request_generator.gi_running:
        pass
    request_generator.close()
    assert request_generator.gi_frame is None
    assert received.get() == _helper_threads.STOP
    assert queue_.empty()
