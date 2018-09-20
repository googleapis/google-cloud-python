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

from google.cloud.ndb import eventloop
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(eventloop)


def test_add_idle():
    with pytest.raises(NotImplementedError):
        eventloop.add_idle()


class TestEventLoop:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            eventloop.EventLoop()


def test_get_event_loop():
    with pytest.raises(NotImplementedError):
        eventloop.get_event_loop()


def test_queue_call():
    with pytest.raises(NotImplementedError):
        eventloop.queue_call()


def test_queue_rpc():
    with pytest.raises(NotImplementedError):
        eventloop.queue_rpc()


def test_run():
    with pytest.raises(NotImplementedError):
        eventloop.run()


def test_run0():
    with pytest.raises(NotImplementedError):
        eventloop.run0()


def test_run1():
    with pytest.raises(NotImplementedError):
        eventloop.run1()
