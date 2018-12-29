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

import grpc
import pytest

from google.cloud.ndb import _eventloop
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
        with pytest.raises(Exception):
            future.result()

    @staticmethod
    def test_set_exception_with_callback():
        callback = mock.Mock()
        future = tasklets.Future()
        future.add_done_callback(callback)
        error = Exception("Spurious Error")
        future.set_exception(error)
        assert future.exception() is error
        assert future.get_exception() is error
        assert future.get_traceback() is error.__traceback__
        callback.assert_called_once_with(future)

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


class TestTaskletFuture:
    @staticmethod
    def test_constructor():
        generator = object()
        future = tasklets.TaskletFuture(generator)
        assert future.generator is generator

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_return():
        def generator_function():
            yield
            return 42

        generator = generator_function()
        next(generator)  # skip ahead to return
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()
        assert future.result() == 42

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_generator_raises():
        error = Exception("Spurious error.")

        def generator_function():
            yield
            raise error

        generator = generator_function()
        next(generator)  # skip ahead to return
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()
        assert future.exception() is error

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_bad_yield():
        def generator_function():
            yield 42

        generator = generator_function()
        future = tasklets.TaskletFuture(generator)
        with pytest.raises(RuntimeError):
            future._advance_tasklet()

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_dependent_returns():
        def generator_function(dependent):
            some_value = yield dependent
            return some_value + 42

        dependent = tasklets.Future()
        generator = generator_function(dependent)
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()
        dependent.set_result(21)
        assert future.result() == 63

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_dependent_raises():
        def generator_function(dependent):
            yield dependent

        error = Exception("Spurious error.")
        dependent = tasklets.Future()
        generator = generator_function(dependent)
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()
        dependent.set_exception(error)
        assert future.exception() is error
        with pytest.raises(Exception):
            future.result()

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    @mock.patch("google.cloud.ndb.tasklets._eventloop")
    def test__advance_tasklet_yields_rpc(_eventloop):
        def generator_function(dependent):
            yield dependent

        dependent = mock.Mock(spec=grpc.Future)
        generator = generator_function(dependent)
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()
        _eventloop.queue_rpc.assert_called_once_with(future, dependent)

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_yields_rpc_integration():
        def generator_function(dependent):
            value = yield dependent
            return value + 3

        dependent = mock.Mock(spec=grpc.Future)
        dependent.exception.return_value = None
        dependent.result.return_value = 8
        generator = generator_function(dependent)
        future = tasklets.TaskletFuture(generator)
        future._advance_tasklet()

        callback = dependent.add_done_callback.call_args[0][0]
        callback(dependent)
        _eventloop.run()
        assert future.result() == 11

    @staticmethod
    @pytest.mark.usefixtures("with_runstate_context")
    def test__advance_tasklet_parallel_yield():
        def generator_function(*dependent):
            yield dependents

        dependents = (tasklets.Future(), tasklets.Future())
        generator = generator_function(dependents)
        future = tasklets.TaskletFuture(generator)
        with pytest.raises(NotImplementedError):
            future._advance_tasklet()


def test_get_context():
    with pytest.raises(NotImplementedError):
        tasklets.get_context()


class Test__get_return_value:
    @staticmethod
    def test_no_args():
        stop = StopIteration()
        assert tasklets._get_return_value(stop) is None

    @staticmethod
    def test_one_arg():
        stop = StopIteration(42)
        assert tasklets._get_return_value(stop) == 42

    @staticmethod
    def test_two_args():
        stop = StopIteration(42, 21)
        assert tasklets._get_return_value(stop) == (42, 21)


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
