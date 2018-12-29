# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

import pytest

from google.cloud.ndb import tasklets
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(tasklets)


def test_add_flow_exception():
    with pytest.raises(NotImplementedError):
        tasklets.add_flow_exception()


class TestFuture:
    @staticmethod
    def test_constructor():
        future = tasklets.Future()
        assert future.running()
        assert not future.done()

    @staticmethod
    def test_set_result():
        future = tasklets.Future()
        future.set_result(42)
        assert future.result() == 42
        assert future.get_result() == 42
        assert future.done()
        assert not future.running()
        assert future.exception() is None
        assert future.get_exception() is None
        assert future.get_traceback() is None

    @staticmethod
    def test_set_result_already_done():
        future = tasklets.Future()
        future.set_result(42)
        with pytest.raises(RuntimeError):
            future.set_result(42)

    @staticmethod
    def test_add_done_callback():
        callback1 = mock.Mock()
        callback2 = mock.Mock()
        future = tasklets.Future()
        future.add_done_callback(callback1)
        future.add_done_callback(callback2)
        future.set_result(42)

        callback1.assert_called_once_with(future)
        callback2.assert_called_once_with(future)

    @staticmethod
    def test_set_exception():
        future = tasklets.Future()
        error = Exception("Spurious Error")
        future.set_exception(error)
        assert future.exception() is error
        assert future.get_exception() is error
        assert future.get_traceback() is error.__traceback__

    @staticmethod
    def test_set_exception_already_done():
        future = tasklets.Future()
        error = Exception("Spurious Error")
        future.set_exception(error)
        with pytest.raises(RuntimeError):
            future.set_exception(error)

    @staticmethod
    @mock.patch("google.cloud.ndb.tasklets._eventloop")
    def test_wait(_eventloop):
        def side_effects(future):
            yield
            yield
            future.set_result(42)
            yield

        future = tasklets.Future()
        _eventloop.run1.side_effect = side_effects(future)
        future.wait()
        assert future.result() == 42
        assert _eventloop.run1.call_count == 3

    @staticmethod
    @mock.patch("google.cloud.ndb.tasklets._eventloop")
    def test_check_success(_eventloop):
        def side_effects(future):
            yield
            yield
            future.set_result(42)
            yield

        future = tasklets.Future()
        _eventloop.run1.side_effect = side_effects(future)
        future.check_success()
        assert future.result() == 42
        assert _eventloop.run1.call_count == 3

    @staticmethod
    @mock.patch("google.cloud.ndb.tasklets._eventloop")
    def test_check_success_failure(_eventloop):
        error = Exception("Spurious error")

        def side_effects(future):
            yield
            yield
            future.set_exception(error)
            yield

        future = tasklets.Future()
        _eventloop.run1.side_effect = side_effects(future)
        with pytest.raises(Exception) as error_context:
            future.check_success()

        assert error_context.value is error

    @staticmethod
    @mock.patch("google.cloud.ndb.tasklets._eventloop")
    def test_result_block_for_result(_eventloop):
        def side_effects(future):
            yield
            yield
            future.set_result(42)
            yield

        future = tasklets.Future()
        _eventloop.run1.side_effect = side_effects(future)
        assert future.result() == 42
        assert _eventloop.run1.call_count == 3

    @staticmethod
    def test_cancel():
        future = tasklets.Future()
        with pytest.raises(NotImplementedError):
            future.cancel()

    @staticmethod
    def test_cancelled():
        future = tasklets.Future()
        assert future.cancelled() is False


def test_get_context():
    with pytest.raises(NotImplementedError):
        tasklets.get_context()


def test_get_return_value():
    with pytest.raises(NotImplementedError):
        tasklets.get_return_value()


def test_make_context():
    with pytest.raises(NotImplementedError):
        tasklets.make_context()


def test_make_default_context():
    with pytest.raises(NotImplementedError):
        tasklets.make_default_context()


class TestMultiFuture:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            tasklets.MultiFuture()


class TestQueueFuture:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            tasklets.QueueFuture()


class TestReducingFuture:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            tasklets.ReducingFuture()


def test_Return():
    assert tasklets.Return is StopIteration


class TestSerialQueueFuture:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            tasklets.SerialQueueFuture()


def test_set_context():
    with pytest.raises(NotImplementedError):
        tasklets.set_context()


def test_sleep():
    with pytest.raises(NotImplementedError):
        tasklets.sleep()


def test_synctasklet():
    with pytest.raises(NotImplementedError):
        tasklets.synctasklet()


def test_tasklet():
    with pytest.raises(NotImplementedError):
        tasklets.tasklet()


def test_toplevel():
    with pytest.raises(NotImplementedError):
        tasklets.toplevel()
