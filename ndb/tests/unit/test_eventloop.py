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

import collections
import unittest.mock

import pytest

from google.cloud.ndb import eventloop
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(eventloop)


def _Event(when=0, what="foo", args=(), kw={}):
    return eventloop._Event(when, what, args, kw)


class TestEventLoop:
    @staticmethod
    def _make_one(**attrs):
        ev = eventloop.EventLoop()
        for name, value in attrs.items():
            setattr(ev, name, value)
        return ev

    def test_constructor(self):
        ev = self._make_one()
        assert ev.current == collections.deque()
        assert ev.idlers == collections.deque()
        assert ev.inactive == 0
        assert ev.queue == []
        assert ev.rpcs == {}

    def test_clear_all(self):
        ev = self._make_one()
        ev.current.append("foo")
        ev.idlers.append("bar")
        ev.queue.append("baz")
        ev.rpcs["qux"] = "quux"
        ev.clear()
        assert not ev.current
        assert not ev.idlers
        assert not ev.queue
        assert not ev.rpcs

        # idemptotence (branch coverage)
        ev.clear()
        assert not ev.current
        assert not ev.idlers
        assert not ev.queue
        assert not ev.rpcs

    def test_clear_current(self):
        ev = self._make_one()
        ev.current.append("foo")
        ev.clear()
        assert not ev.current
        assert not ev.idlers
        assert not ev.queue
        assert not ev.rpcs

    def test_clear_idlers(self):
        ev = self._make_one()
        ev.idlers.append("foo")
        ev.clear()
        assert not ev.current
        assert not ev.idlers
        assert not ev.queue
        assert not ev.rpcs

    def test_insert_event_right_empty_queue(self):
        ev = self._make_one()
        event = _Event()
        ev.insort_event_right(event)
        assert ev.queue == [event]

    def test_insert_event_right_head(self):
        ev = self._make_one(queue=[_Event(1, "bar")])
        ev.insort_event_right(_Event(0, "foo"))
        assert ev.queue == [_Event(0, "foo"), _Event(1, "bar")]

    def test_insert_event_right_tail(self):
        ev = self._make_one(queue=[_Event(0, "foo")])
        ev.insort_event_right(_Event(1, "bar"))
        assert ev.queue == [_Event(0, "foo"), _Event(1, "bar")]

    def test_insert_event_right_middle(self):
        ev = self._make_one(queue=[_Event(0, "foo"), _Event(2, "baz")])
        ev.insort_event_right(_Event(1, "bar"))
        assert ev.queue == [
            _Event(0, "foo"),
            _Event(1, "bar"),
            _Event(2, "baz"),
        ]

    def test_insert_event_right_collision(self):
        ev = self._make_one(
            queue=[_Event(0, "foo"), _Event(1, "bar"), _Event(2, "baz")]
        )
        ev.insort_event_right(_Event(1, "barbar"))
        assert ev.queue == [
            _Event(0, "foo"),
            _Event(1, "bar"),
            _Event(1, "barbar"),
            _Event(2, "baz"),
        ]

    def test_queue_call_now(self):
        ev = self._make_one()
        ev.queue_call(None, "foo", "bar", baz="qux")
        assert list(ev.current) == [("foo", ("bar",), {"baz": "qux"})]
        assert not ev.queue

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_queue_call_soon(self, time):
        ev = self._make_one()
        time.time.return_value = 5
        ev.queue_call(5, "foo", "bar", baz="qux")
        assert not ev.current
        assert ev.queue == [_Event(10, "foo", ("bar",), {"baz": "qux"})]

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_queue_call_absolute(self, time):
        ev = self._make_one()
        time.time.return_value = 5
        ev.queue_call(10e10, "foo", "bar", baz="qux")
        assert not ev.current
        assert ev.queue == [_Event(10e10, "foo", ("bar",), {"baz": "qux"})]

    def test_queue_rpc(self):
        ev = self._make_one()
        with pytest.raises(NotImplementedError):
            ev.queue_rpc("rpc")

    def test_add_idle(self):
        ev = self._make_one()
        ev.add_idle("foo", "bar", baz="qux")
        assert list(ev.idlers) == [("foo", ("bar",), {"baz": "qux"})]

    def test_run_idle_no_idlers(self):
        ev = self._make_one()
        assert ev.run_idle() is False

    def test_run_idle_all_inactive(self):
        ev = self._make_one()
        ev.add_idle("foo")
        ev.inactive = 1
        assert ev.run_idle() is False

    def test_run_idle_remove_callback(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = None
        ev = self._make_one()
        ev.add_idle(callback, "foo", bar="baz")
        ev.add_idle("foo")
        assert ev.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(ev.idlers) == 1
        assert ev.inactive == 0

    def test_run_idle_did_work(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = True
        ev = self._make_one()
        ev.add_idle(callback, "foo", bar="baz")
        ev.add_idle("foo")
        ev.inactive = 1
        assert ev.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(ev.idlers) == 2
        assert ev.inactive == 0

    def test_run_idle_did_no_work(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = False
        ev = self._make_one()
        ev.add_idle(callback, "foo", bar="baz")
        ev.add_idle("foo")
        ev.inactive = 1
        assert ev.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(ev.idlers) == 2
        assert ev.inactive == 2

    def test_run0_nothing_to_do(self):
        ev = self._make_one()
        assert ev.run0() is None

    def test_run0_current(self):
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.queue_call(None, callback, "foo", bar="baz")
        ev.inactive = 88
        assert ev.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")
        assert len(ev.current) == 0
        assert ev.inactive == 0

    def test_run0_idler(self):
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.add_idle(callback, "foo", bar="baz")
        assert ev.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_run0_next_later(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.queue_call(5, callback, "foo", bar="baz")
        ev.inactive = 88
        assert ev.run0() == 5
        callback.assert_not_called()
        assert len(ev.queue) == 1
        assert ev.inactive == 88

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_run0_next_now(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.queue_call(6, "foo")
        ev.queue_call(5, callback, "foo", bar="baz")
        ev.inactive = 88
        time.time.return_value = 10
        assert ev.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")
        assert len(ev.queue) == 1
        assert ev.inactive == 0

    def test_run0_rpc(self):
        ev = self._make_one()
        ev.rpcs["foo"] = "bar"
        with pytest.raises(NotImplementedError):
            ev.run0()

    def test_run1_nothing_to_do(self):
        ev = self._make_one()
        assert ev.run1() is False

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_run1_has_work_now(self, time):
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.queue_call(None, callback)
        assert ev.run1() is True
        time.sleep.assert_not_called()
        callback.assert_called_once_with()

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_run1_has_work_later(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        ev = self._make_one()
        ev.queue_call(5, callback)
        assert ev.run1() is True
        time.sleep.assert_called_once_with(5)
        callback.assert_not_called()

    @unittest.mock.patch("google.cloud.ndb.eventloop.time")
    def test_run(self, time):
        time.time.return_value = 0

        def mock_sleep(seconds):
            time.time.return_value += seconds

        time.sleep = mock_sleep
        idler = unittest.mock.Mock(__name__="idler")
        idler.return_value = None
        runnow = unittest.mock.Mock(__name__="runnow")
        runlater = unittest.mock.Mock(__name__="runlater")
        ev = self._make_one()
        ev.add_idle(idler)
        ev.queue_call(None, runnow)
        ev.queue_call(5, runlater)
        ev.run()
        idler.assert_called_once_with()
        runnow.assert_called_once_with()
        runlater.assert_called_once_with()


def test_add_idle():
    with pytest.raises(NotImplementedError):
        eventloop.add_idle()


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
