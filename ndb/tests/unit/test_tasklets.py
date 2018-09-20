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

import pytest

from google.cloud.ndb import tasklets


def test___all__():
    expected = [name for name in dir(tasklets) if not name.startswith("_")]
    expected.sort(key=str.lower)
    assert sorted(tasklets.__all__, key=str.lower) == expected


def test_add_flow_exception():
    with pytest.raises(NotImplementedError):
        tasklets.add_flow_exception()


class TestFuture:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            tasklets.Future()


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
