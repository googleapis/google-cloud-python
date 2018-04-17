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

from google.auth import credentials
import grpc
import mock
from six.moves import queue

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import _consumer
from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber.policy import base


class Test_RequestQueueGenerator(object):

    def test_bounded_consume(self):
        rpc = mock.create_autospec(grpc.RpcContext, instance=True)
        rpc.is_active.return_value = True

        def queue_generator(rpc):
            yield mock.sentinel.A
            yield queue.Empty()
            yield mock.sentinel.B
            rpc.is_active.return_value = False
            yield mock.sentinel.C

        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue_generator(rpc)

        generator = _consumer._RequestQueueGenerator(q)
        generator.rpc = rpc

        items = list(generator)

        assert items == [mock.sentinel.A, mock.sentinel.B]

    def test_yield_initial_and_exit(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue.Empty()
        rpc = mock.create_autospec(grpc.RpcContext, instance=True)
        rpc.is_active.return_value = False

        generator = _consumer._RequestQueueGenerator(
            q, initial_request=mock.sentinel.A)
        generator.rpc = rpc

        items = list(generator)

        assert items == [mock.sentinel.A]

    def test_exit_when_inactive_with_item(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = [mock.sentinel.A, queue.Empty()]
        rpc = mock.create_autospec(grpc.RpcContext, instance=True)
        rpc.is_active.return_value = False

        generator = _consumer._RequestQueueGenerator(q)
        generator.rpc = rpc

        items = list(generator)

        assert items == []
        # Make sure it put the item back.
        q.put.assert_called_once_with(mock.sentinel.A)

    def test_exit_when_inactive_empty(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue.Empty()
        rpc = mock.create_autospec(grpc.RpcContext, instance=True)
        rpc.is_active.return_value = False

        generator = _consumer._RequestQueueGenerator(q)
        generator.rpc = rpc

        items = list(generator)

        assert items == []

    def test_exit_with_stop(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = [helper_threads.STOP, queue.Empty()]
        rpc = mock.create_autospec(grpc.RpcContext, instance=True)
        rpc.is_active.return_value = True

        generator = _consumer._RequestQueueGenerator(q)
        generator.rpc = rpc

        items = list(generator)

        assert items == []


class _ResponseIterator(object):
    def __init__(self, items, active=True):
        self._items = iter(items)
        self._active = active

    def is_active(self):
        return self._active

    def __next__(self):
        return next(self._items)

    next = __next__


def test__pausable_response_iterator_active_but_cant_consume():
    # Note: we can't autospec threading.Event because it's goofy on Python 2.
    can_consume = mock.Mock(spec=['wait'])
    # First call will return false, indicating the loop should try again.
    # second call will allow it to consume the first (and only) item.
    can_consume.wait.side_effect = [False, True]
    iterator = _ResponseIterator([1])

    pausable_iter = _consumer._pausable_response_iterator(
        iterator, can_consume)

    items = list(pausable_iter)

    assert items == [1]


def test_send_request():
    consumer = _consumer.Consumer()
    request = types.StreamingPullRequest(subscription='foo')
    with mock.patch.object(queue.Queue, 'put') as put:
        consumer.send_request(request)
        put.assert_called_once_with(request)


def test_blocking_consume():
    policy = mock.create_autospec(base.BasePolicy, instance=True)
    policy.call_rpc.return_value = iter((mock.sentinel.A, mock.sentinel.B))

    consumer = _consumer.Consumer()
    consumer.resume()

    assert consumer._blocking_consume(policy) is None
    policy.call_rpc.assert_called_once()
    policy.on_response.assert_has_calls(
        [mock.call(mock.sentinel.A), mock.call(mock.sentinel.B)])


@mock.patch.object(_consumer, '_LOGGER')
def test_blocking_consume_when_exiting(_LOGGER):
    consumer = _consumer.Consumer()
    assert consumer._stopped.is_set() is False
    consumer._stopped.set()

    # Make sure method cleanly exits.
    assert consumer._blocking_consume(None) is None

    _LOGGER.debug.assert_called_once_with('Event signaled consumer exit.')


class OnException(object):

    def __init__(self, acceptable=None):
        self.acceptable = acceptable

    def __call__(self, exception):
        if exception is self.acceptable:
            return True
        else:
            return False


def test_blocking_consume_on_exception():
    policy = mock.create_autospec(base.BasePolicy, instance=True)
    policy.call_rpc.return_value = iter((mock.sentinel.A, mock.sentinel.B))
    exc = TypeError('Bad things!')
    policy.on_response.side_effect = exc

    consumer = _consumer.Consumer()
    consumer.resume()
    consumer._consumer_thread = mock.Mock(spec=threading.Thread)
    policy.on_exception.side_effect = OnException()

    # Establish that we get responses until we are sent the exiting event.
    consumer._blocking_consume(policy)
    assert consumer._consumer_thread is None

    # Check mocks.
    policy.call_rpc.assert_called_once()
    policy.on_response.assert_called_once_with(mock.sentinel.A)
    policy.on_exception.assert_called_once_with(exc)


class RaisingResponseGenerator(object):
    # NOTE: This is needed because defining `.next` on an **instance**
    #       rather than the **class** will not be iterable in Python 2.
    #       This is problematic since a `Mock` just sets members.

    def __init__(self, exception, active=True):
        self.exception = exception
        self.next_calls = 0
        self._active = active

    def __next__(self):
        self.next_calls += 1
        raise self.exception

    def next(self):
        return self.__next__()  # Python 2

    def is_active(self):
        return self._active


def test_blocking_consume_iter_exception_while_paused():
    policy = mock.create_autospec(base.BasePolicy, instance=True)
    exc = TypeError('Bad things!')
    policy.call_rpc.return_value = RaisingResponseGenerator(
        exc, active=False)

    consumer = _consumer.Consumer()
    # Ensure the consume is paused.
    consumer.pause()
    consumer._consumer_thread = mock.Mock(spec=threading.Thread)
    policy.on_exception.side_effect = OnException()

    # Start the thread. It should not block forever but should notice the rpc
    # is inactive and raise the exception from the stream and then exit
    # because on_exception returns false.
    consumer._blocking_consume(policy)
    assert consumer._consumer_thread is None

    # Check mocks.
    policy.call_rpc.assert_called_once()
    policy.on_exception.assert_called_once_with(exc)


def test_blocking_consume_two_exceptions():
    policy = mock.create_autospec(base.BasePolicy, instance=True)

    exc1 = NameError('Oh noes.')
    exc2 = ValueError('Something grumble.')
    policy.on_exception.side_effect = OnException(acceptable=exc1)

    response_generator1 = RaisingResponseGenerator(exc1)
    response_generator2 = RaisingResponseGenerator(exc2)
    policy.call_rpc.side_effect = (response_generator1, response_generator2)

    consumer = _consumer.Consumer()
    consumer.resume()
    consumer._consumer_thread = mock.create_autospec(
        threading.Thread, instance=True)

    # Establish that we get responses until we are sent the exiting event.
    assert consumer._blocking_consume(policy) is None
    assert consumer._consumer_thread is None

    # Check mocks.
    assert policy.call_rpc.call_count == 2
    assert response_generator1.next_calls == 1
    assert response_generator2.next_calls == 1
    policy.on_exception.assert_has_calls(
        [mock.call(exc1), mock.call(exc2)])


def test_paused():
    consumer = _consumer.Consumer()
    assert consumer.paused is True

    consumer._can_consume.set()
    assert consumer.paused is False

    consumer._can_consume.clear()
    assert consumer.paused is True


@mock.patch.object(_consumer, '_LOGGER')
def test_pause(_LOGGER):
    consumer = _consumer.Consumer()
    consumer._can_consume.set()

    assert consumer.pause() is None
    assert not consumer._can_consume.is_set()
    _LOGGER.debug.assert_called_once_with('Pausing consumer')


@mock.patch.object(_consumer, '_LOGGER')
def test_resume(_LOGGER):
    consumer = _consumer.Consumer()
    consumer._can_consume.clear()

    assert consumer.resume() is None
    assert consumer._can_consume.is_set()
    _LOGGER.debug.assert_called_once_with('Resuming consumer')


def test_start_consuming():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    policy = client.subscribe('sub_name_e')
    consumer = _consumer.Consumer()
    with mock.patch.object(threading, 'Thread', autospec=True) as Thread:
        consumer.start_consuming(policy)

    assert consumer._stopped.is_set() is False
    Thread.assert_called_once_with(
        name=_consumer._BIDIRECTIONAL_CONSUMER_NAME,
        target=consumer._blocking_consume,
        args=(policy,),
    )
    assert consumer._consumer_thread is Thread.return_value


def test_stop_consuming():
    consumer = _consumer.Consumer()
    assert consumer._stopped.is_set() is False
    thread = mock.Mock(spec=threading.Thread)
    consumer._consumer_thread = thread

    assert consumer.stop_consuming() is None

    # Make sure state was updated.
    assert consumer._stopped.is_set() is True
    assert consumer._consumer_thread is None
    # Check mocks.
    thread.join.assert_called_once_with()
