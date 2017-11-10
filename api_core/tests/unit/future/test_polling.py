# Copyright 2017, Google LLC
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

import concurrent.futures
import threading
import time

import mock
import pytest

from google.api_core.future import polling


class PollingFutureImpl(polling.PollingFuture):
    def done(self):
        return False

    def cancel(self):
        return True

    def cancelled(self):
        return False

    def running(self):
        return True


def test_polling_future_constructor():
    future = PollingFutureImpl()
    assert not future.done()
    assert not future.cancelled()
    assert future.running()
    assert future.cancel()


def test_set_result():
    future = PollingFutureImpl()
    callback = mock.Mock()

    future.set_result(1)

    assert future.result() == 1
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


def test_set_exception():
    future = PollingFutureImpl()
    exception = ValueError('meep')

    future.set_exception(exception)

    assert future.exception() == exception
    with pytest.raises(ValueError):
        future.result()

    callback = mock.Mock()
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


def test_invoke_callback_exception():
    future = PollingFutureImplWithPoll()
    future.set_result(42)

    # This should not raise, despite the callback causing an exception.
    callback = mock.Mock(side_effect=ValueError)
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


class PollingFutureImplWithPoll(PollingFutureImpl):
    def __init__(self):
        super(PollingFutureImplWithPoll, self).__init__()
        self.poll_count = 0
        self.event = threading.Event()

    def done(self):
        self.poll_count += 1
        self.event.wait()
        self.set_result(42)
        return True


def test_result_with_polling():
    future = PollingFutureImplWithPoll()

    future.event.set()
    result = future.result()

    assert result == 42
    assert future.poll_count == 1
    # Repeated calls should not cause additional polling
    assert future.result() == result
    assert future.poll_count == 1


class PollingFutureImplTimeout(PollingFutureImplWithPoll):
    def done(self):
        time.sleep(1)
        return False


def test_result_timeout():
    future = PollingFutureImplTimeout()
    with pytest.raises(concurrent.futures.TimeoutError):
        future.result(timeout=1)


def test_callback_background_thread():
    future = PollingFutureImplWithPoll()
    callback = mock.Mock()

    future.add_done_callback(callback)

    assert future._polling_thread is not None

    # Give the thread a second to poll
    time.sleep(1)
    assert future.poll_count == 1

    future.event.set()
    future._polling_thread.join()

    callback.assert_called_once_with(future)


def test_double_callback_background_thread():
    future = PollingFutureImplWithPoll()
    callback = mock.Mock()
    callback2 = mock.Mock()

    future.add_done_callback(callback)
    current_thread = future._polling_thread
    assert current_thread is not None

    # only one polling thread should be created.
    future.add_done_callback(callback2)
    assert future._polling_thread is current_thread

    future.event.set()
    future._polling_thread.join()

    assert future.poll_count == 1
    callback.assert_called_once_with(future)
    callback2.assert_called_once_with(future)
