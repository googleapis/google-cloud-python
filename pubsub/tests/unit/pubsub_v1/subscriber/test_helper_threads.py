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
import threading

import mock

from google.cloud.pubsub_v1.subscriber import _helper_threads


def test_start():
    registry = _helper_threads.HelperThreadRegistry()
    queue_ = queue.Queue()
    target = mock.Mock(spec=())
    with mock.patch.object(threading.Thread, 'start', autospec=True) as start:
        registry.start('foo', queue_, target)
        assert start.called


def test_stop_noop():
    registry = _helper_threads.HelperThreadRegistry()
    assert len(registry._helper_threads) == 0
    registry.stop('foo')
    assert len(registry._helper_threads) == 0


def test_stop_dead_thread():
    registry = _helper_threads.HelperThreadRegistry()
    registry._helper_threads['foo'] = _helper_threads._HelperThread(
        name='foo',
        queue=None,
        thread=threading.Thread(target=lambda: None),
    )
    assert len(registry._helper_threads) == 1
    registry.stop('foo')
    assert len(registry._helper_threads) == 0


@mock.patch.object(queue.Queue, 'put')
@mock.patch.object(threading.Thread, 'is_alive')
@mock.patch.object(threading.Thread, 'join')
def test_stop_alive_thread(join, is_alive, put):
    is_alive.return_value = True

    # Set up a registry with a helper thread in it.
    registry = _helper_threads.HelperThreadRegistry()
    registry._helper_threads['foo'] = _helper_threads._HelperThread(
        name='foo',
        queue=queue.Queue(),
        thread=threading.Thread(target=lambda: None),
    )

    # Assert that the helper thread is present, and removed correctly
    # on stop.
    assert len(registry._helper_threads) == 1
    registry.stop('foo')
    assert len(registry._helper_threads) == 0

    # Assert that all of our mocks were called in the expected manner.
    is_alive.assert_called_once_with()
    join.assert_called_once_with()
    put.assert_called_once_with(_helper_threads.STOP)


def test_stop_all():
    registry = _helper_threads.HelperThreadRegistry()
    registry._helper_threads['foo'] = _helper_threads._HelperThread(
        name='foo',
        queue=None,
        thread=threading.Thread(target=lambda: None),
    )
    assert len(registry._helper_threads) == 1
    registry.stop_all()
    assert len(registry._helper_threads) == 0


def test_stop_all_noop():
    registry = _helper_threads.HelperThreadRegistry()
    assert len(registry._helper_threads) == 0
    registry.stop_all()
    assert len(registry._helper_threads) == 0


def test_queue_callback_thread():
    queue_ = queue.Queue()
    callback = mock.Mock(spec=())
    qct = _helper_threads.QueueCallbackThread(queue_, callback)

    # Set up an appropriate mock for the queue, and call the queue callback
    # thread.
    with mock.patch.object(queue.Queue, 'get') as get:
        get.side_effect = (mock.sentinel.A, _helper_threads.STOP)
        qct()

        # Assert that we got the expected calls.
        assert get.call_count == 2
        callback.assert_called_once_with(mock.sentinel.A)


def test_queue_callback_thread_exception():
    queue_ = queue.Queue()
    callback = mock.Mock(spec=(), side_effect=(Exception,))
    qct = _helper_threads.QueueCallbackThread(queue_, callback)

    # Set up an appropriate mock for the queue, and call the queue callback
    # thread.
    with mock.patch.object(queue.Queue, 'get') as get:
        get.side_effect = (mock.sentinel.A, _helper_threads.STOP)
        qct()

        # Assert that we got the expected calls.
        assert get.call_count == 2
        callback.assert_called_once_with(mock.sentinel.A)
