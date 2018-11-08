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

from google.cloud.ndb import _eventloop as eventloop
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(eventloop)


def _Event(when=0, what="foo", args=(), kw={}):
    return eventloop._Event(when, what, args, kw)


class TestEventLoop:
    @staticmethod
    def _make_one(**attrs):
        loop = eventloop.EventLoop()
        for name, value in attrs.items():
            setattr(loop, name, value)
        return loop

    def test_constructor(self):
        loop = self._make_one()
        assert loop.current == collections.deque()
        assert loop.idlers == collections.deque()
        assert loop.inactive == 0
        assert loop.queue == []
        assert loop.rpcs == {}

    def test_clear_all(self):
        loop = self._make_one()
        loop.current.append("foo")
        loop.idlers.append("bar")
        loop.queue.append("baz")
        loop.rpcs["qux"] = "quux"
        loop.clear()
        assert not loop.current
        assert not loop.idlers
        assert not loop.queue
        assert not loop.rpcs

        # idemptotence (branch coverage)
        loop.clear()
        assert not loop.current
        assert not loop.idlers
        assert not loop.queue
        assert not loop.rpcs

    def test_clear_current(self):
        loop = self._make_one()
        loop.current.append("foo")
        loop.clear()
        assert not loop.current
        assert not loop.idlers
        assert not loop.queue
        assert not loop.rpcs

    def test_clear_idlers(self):
        loop = self._make_one()
        loop.idlers.append("foo")
        loop.clear()
        assert not loop.current
        assert not loop.idlers
        assert not loop.queue
        assert not loop.rpcs

    def test_insert_event_right_empty_queue(self):
        loop = self._make_one()
        event = _Event()
        loop.insort_event_right(event)
        assert loop.queue == [event]

    def test_insert_event_right_head(self):
        loop = self._make_one(queue=[_Event(1, "bar")])
        loop.insort_event_right(_Event(0, "foo"))
        assert loop.queue == [_Event(0, "foo"), _Event(1, "bar")]

    def test_insert_event_right_tail(self):
        loop = self._make_one(queue=[_Event(0, "foo")])
        loop.insort_event_right(_Event(1, "bar"))
        assert loop.queue == [_Event(0, "foo"), _Event(1, "bar")]

    def test_insert_event_right_middle(self):
        loop = self._make_one(queue=[_Event(0, "foo"), _Event(2, "baz")])
        loop.insort_event_right(_Event(1, "bar"))
        assert loop.queue == [
            _Event(0, "foo"),
            _Event(1, "bar"),
            _Event(2, "baz"),
        ]

    def test_insert_event_right_collision(self):
        loop = self._make_one(
            queue=[_Event(0, "foo"), _Event(1, "bar"), _Event(2, "baz")]
        )
        loop.insort_event_right(_Event(1, "barbar"))
        assert loop.queue == [
            _Event(0, "foo"),
            _Event(1, "bar"),
            _Event(1, "barbar"),
            _Event(2, "baz"),
        ]

    def test_queue_call_now(self):
        loop = self._make_one()
        loop.queue_call(None, "foo", "bar", baz="qux")
        assert list(loop.current) == [("foo", ("bar",), {"baz": "qux"})]
        assert not loop.queue

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_queue_call_soon(self, time):
        loop = self._make_one()
        time.time.return_value = 5
        loop.queue_call(5, "foo", "bar", baz="qux")
        assert not loop.current
        assert loop.queue == [_Event(10, "foo", ("bar",), {"baz": "qux"})]

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_queue_call_absolute(self, time):
        loop = self._make_one()
        time.time.return_value = 5
        loop.queue_call(10e10, "foo", "bar", baz="qux")
        assert not loop.current
        assert loop.queue == [_Event(10e10, "foo", ("bar",), {"baz": "qux"})]

    def test_queue_rpc(self):
        loop = self._make_one()
        with pytest.raises(NotImplementedError):
            loop.queue_rpc("rpc")

    def test_add_idle(self):
        loop = self._make_one()
        loop.add_idle("foo", "bar", baz="qux")
        assert list(loop.idlers) == [("foo", ("bar",), {"baz": "qux"})]

    def test_run_idle_no_idlers(self):
        loop = self._make_one()
        assert loop.run_idle() is False

    def test_run_idle_all_inactive(self):
        loop = self._make_one()
        loop.add_idle("foo")
        loop.inactive = 1
        assert loop.run_idle() is False

    def test_run_idle_remove_callback(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = None
        loop = self._make_one()
        loop.add_idle(callback, "foo", bar="baz")
        loop.add_idle("foo")
        assert loop.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(loop.idlers) == 1
        assert loop.inactive == 0

    def test_run_idle_did_work(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = True
        loop = self._make_one()
        loop.add_idle(callback, "foo", bar="baz")
        loop.add_idle("foo")
        loop.inactive = 1
        assert loop.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(loop.idlers) == 2
        assert loop.inactive == 0

    def test_run_idle_did_no_work(self):
        callback = unittest.mock.Mock(__name__="callback")
        callback.return_value = False
        loop = self._make_one()
        loop.add_idle(callback, "foo", bar="baz")
        loop.add_idle("foo")
        loop.inactive = 1
        assert loop.run_idle() is True
        callback.assert_called_once_with("foo", bar="baz")
        assert len(loop.idlers) == 2
        assert loop.inactive == 2

    def test_run0_nothing_to_do(self):
        loop = self._make_one()
        assert loop.run0() is None

    def test_run0_current(self):
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.queue_call(None, callback, "foo", bar="baz")
        loop.inactive = 88
        assert loop.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")
        assert len(loop.current) == 0
        assert loop.inactive == 0

    def test_run0_idler(self):
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.add_idle(callback, "foo", bar="baz")
        assert loop.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_run0_next_later(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.queue_call(5, callback, "foo", bar="baz")
        loop.inactive = 88
        assert loop.run0() == 5
        callback.assert_not_called()
        assert len(loop.queue) == 1
        assert loop.inactive == 88

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_run0_next_now(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.queue_call(6, "foo")
        loop.queue_call(5, callback, "foo", bar="baz")
        loop.inactive = 88
        time.time.return_value = 10
        assert loop.run0() == 0
        callback.assert_called_once_with("foo", bar="baz")
        assert len(loop.queue) == 1
        assert loop.inactive == 0

    def test_run0_rpc(self):
        loop = self._make_one()
        loop.rpcs["foo"] = "bar"
        with pytest.raises(NotImplementedError):
            loop.run0()

    def test_run1_nothing_to_do(self):
        loop = self._make_one()
        assert loop.run1() is False

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_run1_has_work_now(self, time):
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.queue_call(None, callback)
        assert loop.run1() is True
        time.sleep.assert_not_called()
        callback.assert_called_once_with()

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_run1_has_work_later(self, time):
        time.time.return_value = 0
        callback = unittest.mock.Mock(__name__="callback")
        loop = self._make_one()
        loop.queue_call(5, callback)
        assert loop.run1() is True
        time.sleep.assert_called_once_with(5)
        callback.assert_not_called()

    @unittest.mock.patch("google.cloud.ndb._eventloop.time")
    def test_run(self, time):
        time.time.return_value = 0

        def mock_sleep(seconds):
            time.time.return_value += seconds

        time.sleep = mock_sleep
        idler = unittest.mock.Mock(__name__="idler")
        idler.return_value = None
        runnow = unittest.mock.Mock(__name__="runnow")
        runlater = unittest.mock.Mock(__name__="runlater")
        loop = self._make_one()
        loop.add_idle(idler)
        loop.queue_call(None, runnow)
        loop.queue_call(5, runlater)
        loop.run()
        idler.assert_called_once_with()
        runnow.assert_called_once_with()
        runlater.assert_called_once_with()


@unittest.mock.patch("google.cloud.ndb._eventloop.EventLoop")
def test_async_context(EventLoop):
    one = unittest.mock.Mock(spec=("run",))
    two = unittest.mock.Mock(spec=("run",))
    EventLoop.side_effect = [one, two]
    assert eventloop.contexts.current() is None

    with eventloop.async_context():
        assert eventloop.contexts.current() is one
        one.run.assert_not_called()

        with eventloop.async_context():
            assert eventloop.contexts.current() is two
            two.run.assert_not_called()

        assert eventloop.contexts.current() is one
        one.run.assert_not_called()
        two.run.assert_called_once_with()

    assert eventloop.contexts.current() is None
    one.run.assert_called_once_with()


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
