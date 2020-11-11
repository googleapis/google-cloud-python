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
import unittest

import mock


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

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        pool = self._make_one(labels=labels)
        self.assertIsNone(pool._database)
        self.assertEqual(pool.labels, labels)

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
        database.session.assert_called_once_with()

    def test__new_session_w_labels(self):
        labels = {"foo": "bar"}
        pool = self._make_one(labels=labels)
        database = pool._database = _make_database("name")
        session = _make_session()
        database.session.return_value = session

        new_session = pool._new_session()

        self.assertIs(new_session, session)
        database.session.assert_called_once_with(labels=labels)

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


class TestFixedSizePool(unittest.TestCase):
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

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        pool = self._make_one(size=4, default_timeout=30, labels=labels)
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 4)
        self.assertEqual(pool.default_timeout, 30)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)

    def test_bind(self):
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database)] * 10
        database._sessions.extend(SESSIONS)

        pool.bind(database)

        self.assertIs(pool._database, database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.default_timeout, 10)
        self.assertTrue(pool._sessions.full())

        api = database.spanner_api
        self.assertEqual(api.batch_create_sessions.call_count, 5)
        for session in SESSIONS:
            session.create.assert_not_called()

    def test_get_non_expired(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = sorted([_Session(database) for i in range(0, 4)])
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        # check if sessions returned in LIFO order
        for i in (3, 2, 1, 0):
            session = pool.get()
            self.assertIs(session, SESSIONS[i])
            self.assertTrue(session._exists_checked)
            self.assertFalse(pool._sessions.full())

    def test_get_expired(self):
        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 5
        SESSIONS[0]._exists = False
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        session = pool.get()

        self.assertIs(session, SESSIONS[4])
        session.create.assert_called()
        self.assertTrue(SESSIONS[0]._exists_checked)
        self.assertFalse(pool._sessions.full())

    def test_get_empty_default_timeout(self):
        from six.moves.queue import Empty

        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()

        with self.assertRaises(Empty):
            pool.get()

        self.assertEqual(queue._got, {"block": True, "timeout": 10})

    def test_get_empty_explicit_timeout(self):
        from six.moves.queue import Empty

        pool = self._make_one(size=1, default_timeout=0.1)
        queue = pool._sessions = _Queue()

        with self.assertRaises(Empty):
            pool.get(timeout=1)

        self.assertEqual(queue._got, {"block": True, "timeout": 1})

    def test_put_full(self):
        from six.moves.queue import Full

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with self.assertRaises(Full):
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


class TestBurstyPool(unittest.TestCase):
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

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        pool = self._make_one(target_size=4, labels=labels)
        self.assertIsNone(pool._database)
        self.assertEqual(pool.target_size, 4)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)

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


class TestPingingPool(unittest.TestCase):
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

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        pool = self._make_one(
            size=4, default_timeout=30, ping_interval=1800, labels=labels
        )
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 4)
        self.assertEqual(pool.default_timeout, 30)
        self.assertEqual(pool._delta.seconds, 1800)
        self.assertTrue(pool._sessions.empty())
        self.assertEqual(pool.labels, labels)

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

        session = pool.get()

        self.assertIs(session, SESSIONS[0])
        self.assertFalse(session._exists_checked)
        self.assertFalse(pool._sessions.full())

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

        session = pool.get()

        self.assertIs(session, SESSIONS[0])
        self.assertTrue(session._exists_checked)
        self.assertFalse(pool._sessions.full())

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

        session = pool.get()

        self.assertIs(session, SESSIONS[4])
        session.create.assert_called()
        self.assertTrue(SESSIONS[0]._exists_checked)
        self.assertFalse(pool._sessions.full())

    def test_get_empty_default_timeout(self):
        from six.moves.queue import Empty

        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()

        with self.assertRaises(Empty):
            pool.get()

        self.assertEqual(queue._got, {"block": True, "timeout": 10})

    def test_get_empty_explicit_timeout(self):
        from six.moves.queue import Empty

        pool = self._make_one(size=1, default_timeout=0.1)
        queue = pool._sessions = _Queue()

        with self.assertRaises(Empty):
            pool.get(timeout=1)

        self.assertEqual(queue._got, {"block": True, "timeout": 1})

    def test_put_full(self):
        from six.moves.queue import Full

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 4
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with self.assertRaises(Full):
            pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

    def test_put_non_full(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()

        now = datetime.datetime.utcnow()
        database = _Database("name")
        session = _Session(database)

        with _Monkey(MUT, _NOW=lambda: now):
            pool.put(session)

        self.assertEqual(len(queue._items), 1)
        ping_after, queued = queue._items[0]
        self.assertEqual(ping_after, now + datetime.timedelta(seconds=3000))
        self.assertIs(queued, session)

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

    def test_ping_empty(self):
        pool = self._make_one(size=1)
        pool.ping()  # Does not raise 'Empty'

    def test_ping_oldest_fresh(self):
        pool = self._make_one(size=1)
        database = _Database("name")
        SESSIONS = [_Session(database)] * 1
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        pool.ping()

        self.assertFalse(SESSIONS[0]._pinged)

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

        later = datetime.datetime.utcnow() + datetime.timedelta(seconds=4000)
        with _Monkey(MUT, _NOW=lambda: later):
            pool.ping()

        self.assertTrue(SESSIONS[0]._pinged)
        SESSIONS[1].create.assert_called()


class TestTransactionPingingPool(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.pool import TransactionPingingPool

        return TransactionPingingPool

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        pool = self._make_one()
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 10)
        self.assertEqual(pool.default_timeout, 10)
        self.assertEqual(pool._delta.seconds, 3000)
        self.assertTrue(pool._sessions.empty())
        self.assertTrue(pool._pending_sessions.empty())
        self.assertEqual(pool.labels, {})

    def test_ctor_explicit(self):
        labels = {"foo": "bar"}
        pool = self._make_one(
            size=4, default_timeout=30, ping_interval=1800, labels=labels
        )
        self.assertIsNone(pool._database)
        self.assertEqual(pool.size, 4)
        self.assertEqual(pool.default_timeout, 30)
        self.assertEqual(pool._delta.seconds, 1800)
        self.assertTrue(pool._sessions.empty())
        self.assertTrue(pool._pending_sessions.empty())
        self.assertEqual(pool.labels, labels)

    def test_bind(self):
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database) for _ in range(10)]
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
            txn = session._transaction
            txn.begin.assert_called_once_with()

        self.assertTrue(pool._pending_sessions.empty())

    def test_bind_w_timestamp_race(self):
        import datetime
        from google.cloud._testing import _Monkey
        from google.cloud.spanner_v1 import pool as MUT

        NOW = datetime.datetime.utcnow()
        pool = self._make_one()
        database = _Database("name")
        SESSIONS = [_Session(database) for _ in range(10)]
        database._sessions.extend(SESSIONS)

        with _Monkey(MUT, _NOW=lambda: NOW):
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
            txn = session._transaction
            txn.begin.assert_called_once_with()

        self.assertTrue(pool._pending_sessions.empty())

    def test_put_full(self):
        from six.moves.queue import Full

        pool = self._make_one(size=4)
        database = _Database("name")
        SESSIONS = [_Session(database) for _ in range(4)]
        database._sessions.extend(SESSIONS)
        pool.bind(database)

        with self.assertRaises(Full):
            pool.put(_Session(database))

        self.assertTrue(pool._sessions.full())

    def test_put_non_full_w_active_txn(self):
        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()
        pending = pool._pending_sessions = _Queue()
        database = _Database("name")
        session = _Session(database)
        txn = session.transaction()

        pool.put(session)

        self.assertEqual(len(queue._items), 1)
        _, queued = queue._items[0]
        self.assertIs(queued, session)

        self.assertEqual(len(pending._items), 0)
        txn.begin.assert_not_called()

    def test_put_non_full_w_committed_txn(self):
        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()
        pending = pool._pending_sessions = _Queue()
        database = _Database("name")
        session = _Session(database)
        committed = session.transaction()
        committed.committed = True

        pool.put(session)

        self.assertEqual(len(queue._items), 0)

        self.assertEqual(len(pending._items), 1)
        self.assertIs(pending._items[0], session)
        self.assertIsNot(session._transaction, committed)
        session._transaction.begin.assert_not_called()

    def test_put_non_full(self):
        pool = self._make_one(size=1)
        queue = pool._sessions = _Queue()
        pending = pool._pending_sessions = _Queue()
        database = _Database("name")
        session = _Session(database)

        pool.put(session)

        self.assertEqual(len(queue._items), 0)
        self.assertEqual(len(pending._items), 1)
        self.assertIs(pending._items[0], session)

        self.assertFalse(pending.empty())

    def test_begin_pending_transactions_empty(self):
        pool = self._make_one(size=1)
        pool.begin_pending_transactions()  # no raise

    def test_begin_pending_transactions_non_empty(self):
        pool = self._make_one(size=1)
        pool._sessions = _Queue()

        database = _Database("name")
        TRANSACTIONS = [_make_transaction(object())]
        PENDING_SESSIONS = [_Session(database, transaction=txn) for txn in TRANSACTIONS]

        pending = pool._pending_sessions = _Queue(*PENDING_SESSIONS)
        self.assertFalse(pending.empty())

        pool.begin_pending_transactions()  # no raise

        for txn in TRANSACTIONS:
            txn.begin.assert_called_once_with()

        self.assertTrue(pending.empty())


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
        checkout = self._make_one(pool, foo="bar")
        self.assertIs(checkout._pool, pool)
        self.assertIsNone(checkout._session)
        self.assertEqual(checkout._kwargs, {"foo": "bar"})

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

    def __init__(self, database, exists=True, transaction=None):
        self._database = database
        self._exists = exists
        self._exists_checked = False
        self._pinged = False
        self.create = mock.Mock()
        self._deleted = False
        self._transaction = transaction

    def __lt__(self, other):
        return id(self) < id(other)

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


class _Database(object):
    def __init__(self, name):
        self.name = name
        self._sessions = []

        def mock_batch_create_sessions(
            database=None, session_count=10, timeout=10, metadata=[]
        ):
            from google.cloud.spanner_v1 import BatchCreateSessionsResponse
            from google.cloud.spanner_v1 import Session

            if session_count < 2:
                response = BatchCreateSessionsResponse(session=[Session()])
            else:
                response = BatchCreateSessionsResponse(session=[Session(), Session()])
            return response

        from google.cloud.spanner_v1 import SpannerClient

        self.spanner_api = mock.create_autospec(SpannerClient, instance=True)
        self.spanner_api.batch_create_sessions.side_effect = mock_batch_create_sessions

    def session(self):
        # always return first session in the list
        # to avoid reversing the order of putting
        # sessions into pool (important for order tests)
        return self._sessions.pop(0)


class _Queue(object):

    _size = 1

    def __init__(self, *items):
        self._items = list(items)

    def empty(self):
        return len(self._items) == 0

    def full(self):
        return len(self._items) >= self._size

    def get(self, **kwargs):
        from six.moves.queue import Empty

        self._got = kwargs
        try:
            return self._items.pop()
        except IndexError:
            raise Empty()

    def put(self, item, **kwargs):
        self._put = kwargs
        self._items.append(item)

    def put_nowait(self, item, **kwargs):
        self._put_nowait = kwargs
        self._items.append(item)


class _Pool(_Queue):

    _database = None
