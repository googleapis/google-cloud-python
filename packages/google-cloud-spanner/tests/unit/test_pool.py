# Copyright 2016 Google LLC All rights reserved.
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


from functools import total_ordering
import time
import unittest
from datetime import datetime, timedelta

import mock
from google.cloud.spanner_v1._opentelemetry_tracing import trace_call
from tests._helpers import (
    OpenTelemetryBase,
    LIB_VERSION,
    StatusCode,
    enrich_with_otel_scope,
    HAS_OPENTELEMETRY_INSTALLED,
)


def _make_database(name="name"):
    from google.cloud.spanner_v1.database import Database

    return mock.create_autospec(Database, instance=True)


def _make_session():
    from google.cloud.spanner_v1.database import Session

    return mock.create_autospec(Session, instance=True)


class TestAbstractSessionPool(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import AbstractSessionPool

        return AbstractSessionPool

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        pool = self._make_one()
        self.assertIsNone(pool._database)
        self.assertEqual(pool.labels, {})
        self.assertIsNone(pool.database_role)

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        database_role = "dummy-role"
        pool = self._make_one(labels=labels, database_role=database_role)
        self.assertIsNone(pool._database)
        self.assertEqual(pool.labels, labels)
        self.assertEqual(pool.database_role, database_role)

    def test_bind_abstract(self):
        pool = self._make_one()
        database = _make_database("name")
        with self.assertRaises(NotImplementedError):
            pool.bind(database)

    def test_get_abstract(self):
        pool = self._make_one()
        with self.assertRaises(NotImplementedError):
            pool.get()

    def test_put_abstract(self):
        pool = self._make_one()
        session = object()
        with self.assertRaises(NotImplementedError):
            pool.put(session)

    def test_clear_abstract(self):
        pool = self._make_one()
        with self.assertRaises(NotImplementedError):
            pool.clear()

    def test__new_session_wo_labels(self):
        pool = self._make_one()
        database = pool._database = _make_database("name")
        session = _make_session()
        database.session.return_value = session

        new_session = pool._new_session()

        self.assertIs(new_session, session)
        database.session.assert_called_once_with(labels={}, database_role=None)

    def test__new_session_w_labels(self):
        labels = {"foo": "bar"}
        pool = self._make_one(labels=labels)
        database = pool._database = _make_database("name")
        session = _make_session()
        database.session.return_value = session

        new_session = pool._new_session()

        self.assertIs(new_session, session)
        database.session.assert_called_once_with(labels=labels, database_role=None)

    def test__new_session_w_database_role(self):
        database_role = "dummy-role"
        pool = self._make_one(database_role=database_role)
        database = pool._database = _make_database("name")
        session = _make_session()
        database.session.return_value = session

        new_session = pool._new_session()

        self.assertIs(new_session, session)
        database.session.assert_called_once_with(labels={}, database_role=database_role)

    def test_session_wo_kwargs(self):
        from google.cloud.spanner_v1.pool import SessionCheckout

        pool = self._make_one()
        checkout = pool.session()
        self.assertIsInstance(checkout, SessionCheckout)
        self.assertIs(checkout._pool, pool)
        self.assertIsNone(checkout._session)
        self.assertEqual(checkout._kwargs, {})

    def test_session_w_kwargs(self):
        from google.cloud.spanner_v1.pool import SessionCheckout

        pool = self._make_one()
        checkout = pool.session(foo="bar")
        self.assertIsInstance(checkout, SessionCheckout)
        self.assertIs(checkout._pool, pool)
        self.assertIsNone(checkout._session)
        self.assertEqual(checkout._kwargs, {"foo": "bar"})


class TestFixedSizePool(OpenTelemetryBase):
    BASE_ATTRIBUTES = {
        "db.type": "spanner",
        "db.url": "spanner.googleapis.com",
        "db.instance": "name",
        "net.host.name": "spanner.googleapis.com",
        "gcp.client.service": "spanner",
        "gcp.client.version": LIB_VERSION,
        "gcp.client.repo": "googleapis/python-spanner",
    }
    enrich_with_otel_scope(BASE_ATTRIBUTES)

    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import FixedSizePool

        return FixedSizePool

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        pool = self._make_one()
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.default_timeout, 10)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, {})
        self.assertIsNone(pool.database_role)

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        database_role = "dummy-role"
        pool = self._make_one(
            size=4, default_timeout=30, labels=labels, database_role=database_role
        )
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 4)
        self.assertEqual(pool.default_timeout, 30)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)
        self.assertEqual(pool.database_role, database_role)

    def test_bind(self):
        database_role = "dummy-role"
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._database_role = database_role
        database._sessions.extend(SESSIONS)

        pool.bind(database)

        self.assertIs(pool._database, database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.database_role, database_role)
        self.assertEqual(pool.default_timeout, 10)
        self.assertTrue(pool._sessions.full())

        api = database.spanner_api
        self.assertEqual(api.batch_create_sessions.call_count, 5)
        for session in SESSIONS:
            session.create.assert_not_called()

    def test_get_active(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = sorted([_Session(database) for i in range(0, 4)])
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        # check if sessions returned in LIFO order
        for i in (3, 2, 1, 0):
            session = pool.get()
            self.assertIs(session, SESSIONS[i])
            self.assertFalse(session._exists_checked)
            self.assertFalse(pool._sessions.full())

    def test_get_non_expired(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        last_use_time = datetime.utcnow() - timedelta(minutes=56)
        SESSIONS = sorted(
            [_Session(database, last_use_time=last_use_time) for i in range(0, 4)]
        )
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        # check if sessions returned in LIFO order
        for i in (3, 2, 1, 0):
            session = pool.get()
            self.assertIs(session, SESSIONS[i])
            self.assertTrue(session._exists_checked)
            self.assertFalse(pool._sessions.full())

    def test_spans_bind_get(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # This tests retrieving 1 out of 4 sessions from the session pool.
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = sorted([_Session(database) for i in range(0, 4)])
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with trace_call("pool.Get", SESSIONS[0]):
            pool.get()

        span_list = self.get_finished_spans()
        got_span_names = [span.name for span in span_list]
        want_span_names = ["CloudSpanner.FixedPool.BatchCreateSessions", "pool.Get"]
        assert got_span_names == want_span_names

        attrs = TestFixedSizePool.BASE_ATTRIBUTES.copy()

        # Check for the overall spans.
        self.assertSpanAttributes(
            "CloudSpanner.FixedPool.BatchCreateSessions",
            status=StatusCode.OK,
            attributes=attrs,
            span=span_list[0],
        )

        self.assertSpanAttributes(
            "pool.Get",
            status=StatusCode.OK,
            attributes=TestFixedSizePool.BASE_ATTRIBUTES,
            span=span_list[-1],
        )
        wantEventNames = [
            "Acquiring session",
            "Waiting for a session to become available",
            "Acquired session",
        ]
        self.assertSpanEvents("pool.Get", wantEventNames, span_list[-1])

    def test_spans_bind_get_empty_pool(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # Tests trying to invoke pool.get() from an empty pool.
        pool = self._make_one(size=0)
        database = _Database("name")
        session1 = _Session(database)
        with trace_call("pool.Get", session1):
            try:
                pool.bind(database)
                database._sessions = database._sessions[:0]
                pool.get()
            except Exception:
                pass

        wantEventNames = [
            "Invalid session pool size(0) <= 0",
            "Acquiring session",
            "Waiting for a session to become available",
            "No sessions available in the pool",
        ]
        self.assertSpanEvents("pool.Get", wantEventNames)

        # Check for the overall spans too.
        self.assertSpanNames(["pool.Get"])
        self.assertSpanAttributes(
            "pool.Get",
            attributes=TestFixedSizePool.BASE_ATTRIBUTES,
        )

        span_list = self.get_finished_spans()
        got_all_events = []
        for span in span_list:
            for event in span.events:
                got_all_events.append((event.name, event.attributes))
        want_all_events = [
            ("Invalid session pool size(0) <= 0", {"kind": "FixedSizePool"}),
            ("Acquiring session", {"kind": "FixedSizePool"}),
            ("Waiting for a session to become available", {"kind": "FixedSizePool"}),
            ("No sessions available in the pool", {"kind": "FixedSizePool"}),
        ]
        assert got_all_events == want_all_events

    def test_spans_pool_bind(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # Tests the exception generated from invoking pool.bind when
        # you have an empty pool.
        pool = self._make_one(size=1)
        database = _Database("name")
        SESSIONS = []
        database._sessions.extend(SESSIONS)
        fauxSession = mock.Mock()
        setattr(fauxSession, "_database", database)
        try:
            with trace_call("testBind", fauxSession):
                pool.bind(database)
        except Exception:
            pass

        span_list = self.get_finished_spans()
        got_span_names = [span.name for span in span_list]
        want_span_names = ["testBind", "CloudSpanner.FixedPool.BatchCreateSessions"]
        assert got_span_names == want_span_names

        wantEventNames = [
            "Requesting 1 sessions",
            "exception",
        ]
        self.assertSpanEvents("testBind", wantEventNames, span_list[0])

        self.assertSpanAttributes(
            "testBind",
            status=StatusCode.ERROR,
            attributes=TestFixedSizePool.BASE_ATTRIBUTES,
            span=span_list[0],
        )

        got_all_events = []

        # Some event attributes are noisy/highly ephemeral
        # and can't be directly compared against.
        imprecise_event_attributes = ["exception.stacktrace", "delay_seconds", "cause"]
        for span in span_list:
            for event in span.events:
                evt_attributes = event.attributes.copy()
                for attr_name in imprecise_event_attributes:
                    if attr_name in evt_attributes:
                        evt_attributes[attr_name] = "EPHEMERAL"

                got_all_events.append((event.name, evt_attributes))

        want_all_events = [
            ("Requesting 1 sessions", {"kind": "FixedSizePool"}),
            (
                "exception",
                {
                    "exception.type": "IndexError",
                    "exception.message": "pop from empty list",
                    "exception.stacktrace": "EPHEMERAL",
                    "exception.escaped": "False",
                },
            ),
            ("Creating 1 sessions", {"kind": "FixedSizePool"}),
            ("Created sessions", {"count": 1}),
            (
                "exception",
                {
                    "exception.type": "IndexError",
                    "exception.message": "pop from empty list",
                    "exception.stacktrace": "EPHEMERAL",
                    "exception.escaped": "False",
                },
            ),
        ]
        assert got_all_events == want_all_events

    def test_get_expired(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        last_use_time = datetime.utcnow() - timedelta(minutes=65)
        SESSIONS = [_Session(database, last_use_time=last_use_time)] * 5
        SESSIONS[0]._exists = False
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        session = pool.get()

        self.assertIs(session, SESSIONS[4])
        session.create.assert_called()
        self.assertTrue(SESSIONS[0]._exists_checked)
        self.assertFalse(pool._sessions.full())

    def test_get_empty_default_timeout(self):
        import queue

        pool = self._make_one(size=1)
        session_queue = pool._sessions = _Queue()

        with self.assertRaises(queue.Empty):
            pool.get()

        self.assertEqual(session_queue._got, {"block": True, "timeout": 10})

    def test_get_empty_explicit_timeout(self):
        import queue

        pool = self._make_one(size=1, default_timeout=0.1)
        session_queue = pool._sessions = _Queue()

        with self.assertRaises(queue.Empty):
            pool.get(timeout=1)

        self.assertEqual(session_queue._got, {"block": True, "timeout": 1})

    def test_put_full(self):
        import queue

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.reset()

        with self.assertRaises(queue.Full):
            pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

    def test_put_non_full(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        pool._sessions.get()

        pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

    def test_clear(self):
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.assertTrue(pool._sessions.full())

        api = database.spanner_api
        self.assertEqual(api.batch_create_sessions.call_count, 5)
        for session in SESSIONS:
            session.create.assert_not_called()

        pool.clear()

        for session in SESSIONS:
            self.assertTrue(session._deleted)


class TestBurstyPool(OpenTelemetryBase):
    BASE_ATTRIBUTES = {
        "db.type": "spanner",
        "db.url": "spanner.googleapis.com",
        "db.instance": "name",
        "net.host.name": "spanner.googleapis.com",
        "gcp.client.service": "spanner",
        "gcp.client.version": LIB_VERSION,
        "gcp.client.repo": "googleapis/python-spanner",
    }
    enrich_with_otel_scope(BASE_ATTRIBUTES)

    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import BurstyPool

        return BurstyPool

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        pool = self._make_one()
        self.assertIsNone(pool._database)
        self.assertEqual(pool.target_size, 10)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, {})
        self.assertIsNone(pool.database_role)

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        database_role = "dummy-role"
        pool = self._make_one(target_size=4, labels=labels, database_role=database_role)
        self.assertIsNone(pool._database)
        self.assertEqual(pool.target_size, 4)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)
        self.assertEqual(pool.database_role, database_role)

    def test_ctor_explicit_w_database_role_in_db(self):
        database_role = "dummy-role"
        pool = self._make_one()
        database = pool._database = _Database("name")
        database._database_role = database_role
        pool.bind(database)
        self.assertEqual(pool.database_role, database_role)

    def test_get_empty(self):
        pool = self._make_one()
        database = _Database("name")
        database._sessions.append(_Session(database))
        pool.bind(database)

        session = pool.get()

        self.assertIsInstance(session, _Session)
        self.assertIs(session._database, database)
        session.create.assert_called()
        self.assertTrue(pool._sessions.empty())

    def test_spans_get_empty_pool(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # This scenario tests a pool that hasn't been filled up
        # and pool.get() acquires from a pool, waiting for a session
        # to become available.
        pool = self._make_one()
        database = _Database("name")
        session1 = _Session(database)
        database._sessions.append(session1)
        pool.bind(database)

        with trace_call("pool.Get", session1):
            session = pool.get()
            self.assertIsInstance(session, _Session)
            self.assertIs(session._database, database)
            session.create.assert_called()
            self.assertTrue(pool._sessions.empty())

        span_list = self.get_finished_spans()
        got_span_names = [span.name for span in span_list]
        want_span_names = ["pool.Get"]
        assert got_span_names == want_span_names

        create_span = span_list[-1]
        self.assertSpanAttributes(
            "pool.Get",
            attributes=TestBurstyPool.BASE_ATTRIBUTES,
            span=create_span,
        )
        wantEventNames = [
            "Acquiring session",
            "Waiting for a session to become available",
            "No sessions available in pool. Creating session",
        ]
        self.assertSpanEvents("pool.Get", wantEventNames, span=create_span)

    def test_get_non_empty_session_exists(self):
        pool = self._make_one()
        database = _Database("name")
        previous = _Session(database)
        pool.bind(database)
        pool.put(previous)

        session = pool.get()

        self.assertIs(session, previous)
        session.create.assert_not_called()
        self.assertTrue(session._exists_checked)
        self.assertTrue(pool._sessions.empty())

    def test_spans_get_non_empty_session_exists(self):
        # Tests the spans produces when you invoke pool.bind
        # and then insert a session into the pool.
        pool = self._make_one()
        database = _Database("name")
        previous = _Session(database)
        pool.bind(database)
        with trace_call("pool.Get", previous):
            pool.put(previous)
            session = pool.get()
            self.assertIs(session, previous)
            session.create.assert_not_called()
            self.assertTrue(session._exists_checked)
            self.assertTrue(pool._sessions.empty())

        self.assertSpanAttributes(
            "pool.Get",
            attributes=TestBurstyPool.BASE_ATTRIBUTES,
        )
        self.assertSpanEvents(
            "pool.Get",
            ["Acquiring session", "Waiting for a session to become available"],
        )

    def test_get_non_empty_session_expired(self):
        pool = self._make_one()
        database = _Database("name")
        previous = _Session(database, exists=False)
        newborn = _Session(database)
        database._sessions.append(newborn)
        pool.bind(database)
        pool.put(previous)

        session = pool.get()

        self.assertTrue(previous._exists_checked)
        self.assertIs(session, newborn)
        session.create.assert_called()
        self.assertFalse(session._exists_checked)
        self.assertTrue(pool._sessions.empty())

    def test_put_empty(self):
        pool = self._make_one()
        database = _Database("name")
        pool.bind(database)
        session = _Session(database)

        pool.put(session)

        self.assertFalse(pool._sessions.empty())

    def test_spans_put_empty(self):
        # Tests the spans produced when you put sessions into an empty pool.
        pool = self._make_one()
        database = _Database("name")
        pool.bind(database)
        session = _Session(database)

        with trace_call("pool.put", session):
            pool.put(session)
            self.assertFalse(pool._sessions.empty())

        self.assertSpanAttributes(
            "pool.put",
            attributes=TestBurstyPool.BASE_ATTRIBUTES,
        )

    def test_put_full(self):
        pool = self._make_one(target_size=1)
        database = _Database("name")
        pool.bind(database)
        older = _Session(database)
        pool.put(older)
        self.assertFalse(pool._sessions.empty())

        younger = _Session(database)
        pool.put(younger)  # discarded silently

        self.assertTrue(younger._deleted)
        self.assertIs(pool.get(), older)

    def test_spans_put_full(self):
        # This scenario tests the spans produced from putting an older
        # session into a pool that is already full.
        pool = self._make_one(target_size=1)
        database = _Database("name")
        pool.bind(database)
        older = _Session(database)
        with trace_call("pool.put", older):
            pool.put(older)
            self.assertFalse(pool._sessions.empty())

            younger = _Session(database)
            pool.put(younger)  # discarded silently

            self.assertTrue(younger._deleted)
            self.assertIs(pool.get(), older)

        self.assertSpanAttributes(
            "pool.put",
            attributes=TestBurstyPool.BASE_ATTRIBUTES,
        )

    def test_put_full_expired(self):
        pool = self._make_one(target_size=1)
        database = _Database("name")
        pool.bind(database)
        older = _Session(database)
        pool.put(older)
        self.assertFalse(pool._sessions.empty())

        younger = _Session(database, exists=False)
        pool.put(younger)  # discarded silently

        self.assertTrue(younger._deleted)
        self.assertIs(pool.get(), older)

    def test_clear(self):
        pool = self._make_one()
        database = _Database("name")
        pool.bind(database)
        previous = _Session(database)
        pool.put(previous)

        pool.clear()

        self.assertTrue(previous._deleted)
        self.assertNoSpans()


class TestPingingPool(OpenTelemetryBase):
    BASE_ATTRIBUTES = {
        "db.type": "spanner",
        "db.url": "spanner.googleapis.com",
        "db.instance": "name",
        "net.host.name": "spanner.googleapis.com",
        "gcp.client.service": "spanner",
        "gcp.client.version": LIB_VERSION,
        "gcp.client.repo": "googleapis/python-spanner",
    }
    enrich_with_otel_scope(BASE_ATTRIBUTES)

    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import PingingPool

        return PingingPool

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        pool = self._make_one()
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.default_timeout, 10)
        self.assertEqual(pool._delta.seconds, 3000)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, {})
        self.assertIsNone(pool.database_role)

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        database_role = "dummy-role"
        pool = self._make_one(
            size=4,
            default_timeout=30,
            ping_interval=1800,
            labels=labels,
            database_role=database_role,
        )
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 4)
        self.assertEqual(pool.default_timeout, 30)
        self.assertEqual(pool._delta.seconds, 1800)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)
        self.assertEqual(pool.database_role, database_role)

    def test_ctor_explicit_w_database_role_in_db(self):
        database_role = "dummy-role"
        pool = self._make_one()
        database = pool._database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._sessions.extend(SESSIONS)
        database._database_role = database_role
        pool.bind(database)
        self.assertEqual(pool.database_role, database_role)

    def test_bind(self):
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        self.assertIs(pool._database, database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.default_timeout, 10)
        self.assertEqual(pool._delta.seconds, 3000)
        self.assertTrue(pool._sessions.full())

        api = database.spanner_api
        self.assertEqual(api.batch_create_sessions.call_count, 5)
        for session in SESSIONS:
            session.create.assert_not_called()

    def test_get_hit_no_ping(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.reset()

        session = pool.get()

        self.assertIs(session, SESSIONS[0])
        self.assertFalse(session._exists_checked)
        self.assertFalse(pool._sessions.full())
        self.assertNoSpans()

    def test_get_hit_w_ping(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)

        sessions_created = datetime.datetime.utcnow() - datetime.timedelta(seconds=4000)

        with _Monkey(MUT, _NOW=lambda: sessions_created):
            pool.bind(database)

        self.reset()

        session = pool.get()

        self.assertIs(session, SESSIONS[0])
        self.assertTrue(session._exists_checked)
        self.assertFalse(pool._sessions.full())
        self.assertNoSpans()

    def test_get_hit_w_ping_expired(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 5
        SESSIONS[0]._exists = False
        database._sessions.extend(SESSIONS)

        sessions_created = datetime.datetime.utcnow() - datetime.timedelta(seconds=4000)

        with _Monkey(MUT, _NOW=lambda: sessions_created):
            pool.bind(database)
        self.reset()

        session = pool.get()

        self.assertIs(session, SESSIONS[4])
        session.create.assert_called()
        self.assertTrue(SESSIONS[0]._exists_checked)
        self.assertFalse(pool._sessions.full())
        self.assertNoSpans()

    def test_get_empty_default_timeout(self):
        import queue

        pool = self._make_one(size=1)
        session_queue = pool._sessions = _Queue()

        with self.assertRaises(queue.Empty):
            pool.get()

        self.assertEqual(session_queue._got, {"block": True, "timeout": 10})
        self.assertNoSpans()

    def test_get_empty_explicit_timeout(self):
        import queue

        pool = self._make_one(size=1, default_timeout=0.1)
        session_queue = pool._sessions = _Queue()

        with self.assertRaises(queue.Empty):
            pool.get(timeout=1)

        self.assertEqual(session_queue._got, {"block": True, "timeout": 1})
        self.assertNoSpans()

    def test_put_full(self):
        import queue

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with self.assertRaises(queue.Full):
            pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

    def test_spans_put_full(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        import queue

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with self.assertRaises(queue.Full):
            pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

        span_list = self.get_finished_spans()
        got_span_names = [span.name for span in span_list]
        want_span_names = ["CloudSpanner.PingingPool.BatchCreateSessions"]
        assert got_span_names == want_span_names

        attrs = TestPingingPool.BASE_ATTRIBUTES.copy()
        self.assertSpanAttributes(
            "CloudSpanner.PingingPool.BatchCreateSessions",
            attributes=attrs,
            span=span_list[-1],
        )
        wantEventNames = [
            "Created 2 sessions",
            "Created 2 sessions",
            "Requested for 4 sessions, returned 4",
        ]
        self.assertSpanEvents(
            "CloudSpanner.PingingPool.BatchCreateSessions", wantEventNames
        )

    def test_put_non_full(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=1)
        session_queue = pool._sessions = _Queue()

        now = datetime.datetime.utcnow()
        database = _Database("name")
        session = _Session(database)

        with _Monkey(MUT, _NOW=lambda: now):
            pool.put(session)

        self.assertEqual(len(session_queue._items), 1)
        ping_after, queued = session_queue._items[0]
        self.assertEqual(ping_after, now + datetime.timedelta(seconds=3000))
        self.assertIs(queued, session)
        self.assertNoSpans()

    def test_clear(self):
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.reset()
        self.assertTrue(pool._sessions.full())

        api = database.spanner_api
        self.assertEqual(api.batch_create_sessions.call_count, 5)
        for session in SESSIONS:
            session.create.assert_not_called()

        pool.clear()

        for session in SESSIONS:
            self.assertTrue(session._deleted)
        self.assertNoSpans()

    def test_ping_empty(self):
        pool = self._make_one(size=1)
        pool.ping()  # Does not raise 'Empty'
        self.assertNoSpans()

    def test_ping_oldest_fresh(self):
        pool = self._make_one(size=1)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 1
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.reset()

        pool.ping()

        self.assertFalse(SESSIONS[0]._pinged)
        self.assertNoSpans()

    def test_ping_oldest_stale_but_exists(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=1)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 1
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        later = datetime.datetime.utcnow() + datetime.timedelta(seconds=4000)
        with _Monkey(MUT, _NOW=lambda: later):
            pool.ping()

        self.assertTrue(SESSIONS[0]._pinged)

    def test_ping_oldest_stale_and_not_exists(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=1)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 2
        SESSIONS[0]._exists = False
        database._sessions.extend(SESSIONS)
        pool.bind(database)
        self.reset()

        later = datetime.datetime.utcnow() + datetime.timedelta(seconds=4000)
        with _Monkey(MUT, _NOW=lambda: later):
            pool.ping()

        self.assertTrue(SESSIONS[0]._pinged)
        SESSIONS[1].create.assert_called()
        self.assertNoSpans()

    def test_spans_get_and_leave_empty_pool(self):
        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # This scenario tests the spans generated from pulling a span
        # out the pool and leaving it empty.
        pool = self._make_one()
        database = _Database("name")
        session1 = _Session(database)
        database._sessions.append(session1)
        try:
            pool.bind(database)
        except Exception:
            pass

        with trace_call("pool.Get", session1):
            session = pool.get()
            self.assertIsInstance(session, _Session)
            self.assertIs(session._database, database)
            # session.create.assert_called()
            self.assertTrue(pool._sessions.empty())

        span_list = self.get_finished_spans()
        got_span_names = [span.name for span in span_list]
        want_span_names = ["CloudSpanner.PingingPool.BatchCreateSessions", "pool.Get"]
        assert got_span_names == want_span_names

        self.assertSpanAttributes(
            "pool.Get",
            attributes=TestPingingPool.BASE_ATTRIBUTES,
            span=span_list[-1],
        )
        wantEventNames = [
            "Waiting for a session to become available",
            "Acquired session",
        ]
        self.assertSpanEvents("pool.Get", wantEventNames, span_list[-1])


class TestSessionCheckout(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import SessionCheckout

        return SessionCheckout

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_wo_kwargs(self):
        pool = _Pool()
        checkout = self._make_one(pool)
        self.assertIs(checkout._pool, pool)
        self.assertIsNone(checkout._session)
        self.assertEqual(checkout._kwargs, {})

    def test_ctor_w_kwargs(self):
        pool = _Pool()
        checkout = self._make_one(pool, foo="bar", database_role="dummy-role")
        self.assertIs(checkout._pool, pool)
        self.assertIsNone(checkout._session)
        self.assertEqual(
            checkout._kwargs, {"foo": "bar", "database_role": "dummy-role"}
        )

    def test_context_manager_wo_kwargs(self):
        session = object()
        pool = _Pool(session)
        checkout = self._make_one(pool)

        self.assertEqual(len(pool._items), 1)
        self.assertIs(pool._items[0], session)

        with checkout as borrowed:
            self.assertIs(borrowed, session)
            self.assertEqual(len(pool._items), 0)

        self.assertEqual(len(pool._items), 1)
        self.assertIs(pool._items[0], session)
        self.assertEqual(pool._got, {})

    def test_context_manager_w_kwargs(self):
        session = object()
        pool = _Pool(session)
        checkout = self._make_one(pool, foo="bar")

        self.assertEqual(len(pool._items), 1)
        self.assertIs(pool._items[0], session)

        with checkout as borrowed:
            self.assertIs(borrowed, session)
            self.assertEqual(len(pool._items), 0)

        self.assertEqual(len(pool._items), 1)
        self.assertIs(pool._items[0], session)
        self.assertEqual(pool._got, {"foo": "bar"})


def _make_transaction(*args, **kw):
    from google.cloud.spanner_v1.transaction import Transaction

    txn = mock.create_autospec(Transaction)(*args, **kw)
    txn.committed = None
    txn.rolled_back = False
    return txn


@total_ordering
class _Session(object):
    _transaction = None

    def __init__(
        self, database, exists=True, transaction=None, last_use_time=datetime.utcnow()
    ):
        self._database = database
        self._exists = exists
        self._exists_checked = False
        self._pinged = False
        self.create = mock.Mock()
        self._deleted = False
        self._transaction = transaction
        self._last_use_time = last_use_time
        # Generate a faux id.
        self._session_id = f"{time.time()}"

    def __lt__(self, other):
        return id(self) < id(other)

    @property
    def last_use_time(self):
        return self._last_use_time

    def exists(self):
        self._exists_checked = True
        return self._exists

    def ping(self):
        from google.cloud.exceptions import NotFound

        self._pinged = True
        if not self._exists:
            raise NotFound("expired session")

    def delete(self):
        from google.cloud.exceptions import NotFound

        self._deleted = True
        if not self._exists:
            raise NotFound("unknown session")

    def transaction(self):
        txn = self._transaction = _make_transaction(self)
        return txn

    @property
    def session_id(self):
        return self._session_id


class _Database(object):
    def __init__(self, name):
        self.name = name
        self._sessions = []
        self._database_role = None
        self.database_id = name
        self._route_to_leader_enabled = True

        def mock_batch_create_sessions(
            request=None,
            timeout=10,
            metadata=[],
            labels={},
        ):
            from google.cloud.spanner_v1 import BatchCreateSessionsResponse
            from google.cloud.spanner_v1 import Session

            database_role = request.session_template.creator_role if request else None
            if request.session_count < 2:
                response = BatchCreateSessionsResponse(
                    session=[Session(creator_role=database_role, labels=labels)]
                )
            else:
                response = BatchCreateSessionsResponse(
                    session=[
                        Session(creator_role=database_role, labels=labels),
                        Session(creator_role=database_role, labels=labels),
                    ]
                )
            return response

        from google.cloud.spanner_v1 import SpannerClient

        self.spanner_api = mock.create_autospec(SpannerClient, instance=True)
        self.spanner_api.batch_create_sessions.side_effect = mock_batch_create_sessions

    @property
    def database_role(self):
        """Database role used in sessions to connect to this database.

        :rtype: str
        :returns: an str with the name of the database role.
        """
        return self._database_role

    def session(self, **kwargs):
        # always return first session in the list
        # to avoid reversing the order of putting
        # sessions into pool (important for order tests)
        return self._sessions.pop(0)

    @property
    def observability_options(self):
        return dict(db_name=self.name)


class _Queue(object):
    _size = 1

    def __init__(self, *items):
        self._items = list(items)

    def empty(self):
        return len(self._items) == 0

    def full(self):
        return len(self._items) >= self._size

    def get(self, **kwargs):
        import queue

        self._got = kwargs
        try:
            return self._items.pop()
        except IndexError:
            raise queue.Empty()

    def put(self, item, **kwargs):
        self._put = kwargs
        self._items.append(item)

    def put_nowait(self, item, **kwargs):
        self._put_nowait = kwargs
        self._items.append(item)


class _Pool(_Queue):
    _database = None
