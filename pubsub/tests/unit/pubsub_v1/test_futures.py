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

import mock
import pytest

from google.cloud.pubsub_v1 import exceptions
from google.cloud.pubsub_v1 import futures


def _future(*args, **kwargs):
    return futures.Future(*args, **kwargs)


def test_constructor_defaults():
    with mock.patch.object(threading, 'Event', autospec=True) as Event:
        future = _future()

    assert future._result == futures.Future._SENTINEL
    assert future._exception == futures.Future._SENTINEL
    assert future._callbacks == []
    assert future._completed is Event.return_value

    Event.assert_called_once_with()


def test_constructor_explicit_completed():
    completed = mock.sentinel.completed
    future = _future(completed=completed)

    assert future._result == futures.Future._SENTINEL
    assert future._exception == futures.Future._SENTINEL
    assert future._callbacks == []
    assert future._completed is completed


def test_cancel():
    assert _future().cancel() is False


def test_cancelled():
    assert _future().cancelled() is False


def test_running():
    future = _future()
    assert future.running() is True
    future.set_result('foobar')
    assert future.running() is False


def test_done():
    future = _future()
    assert future.done() is False
    future.set_result('12345')
    assert future.done() is True


def test_exception_no_error():
    future = _future()
    future.set_result('12345')
    assert future.exception() is None


def test_exception_with_error():
    future = _future()
    error = RuntimeError('Something really bad happened.')
    future.set_exception(error)

    # Make sure that the exception that is returned is the batch's error.
    # Also check the type to ensure the batch's error did not somehow
    # change internally.
    assert future.exception() is error
    assert isinstance(future.exception(), RuntimeError)
    with pytest.raises(RuntimeError):
        future.result()


def test_exception_timeout():
    future = _future()
    with pytest.raises(exceptions.TimeoutError):
        future.exception(timeout=0.01)


def test_result_no_error():
    future = _future()
    future.set_result('42')
    assert future.result() == '42'


def test_result_with_error():
    future = _future()
    future.set_exception(RuntimeError('Something really bad happened.'))
    with pytest.raises(RuntimeError):
        future.result()


def test_add_done_callback_pending_batch():
    future = _future()
    callback = mock.Mock()
    future.add_done_callback(callback)
    assert len(future._callbacks) == 1
    assert callback in future._callbacks
    assert callback.call_count == 0


def test_add_done_callback_completed_batch():
    future = _future()
    future.set_result('12345')
    callback = mock.Mock(spec=())
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


def test_trigger():
    future = _future()
    callback = mock.Mock(spec=())
    future.add_done_callback(callback)
    assert callback.call_count == 0
    future.set_result('12345')
    callback.assert_called_once_with(future)


def test_set_result_once_only():
    future = _future()
    future.set_result('12345')
    with pytest.raises(RuntimeError):
        future.set_result('67890')


def test_set_exception_once_only():
    future = _future()
    future.set_exception(ValueError('wah wah'))
    with pytest.raises(RuntimeError):
        future.set_exception(TypeError('other wah wah'))
