# Copyright 2016 Google Inc. All rights reserved.
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


import unittest2


class TestConnectionPool(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.pool import ConnectionPool
        return ConnectionPool

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        import six
        import threading
        from gcloud.bigtable.happybase.connection import Connection

        size = 11
        cluster_copy = _Cluster()
        all_copies = [cluster_copy] * size
        cluster = _Cluster(copies=all_copies)  # Avoid implicit environ check.
        pool = self._makeOne(size, cluster=cluster)

        self.assertTrue(isinstance(pool._lock, type(threading.Lock())))
        self.assertTrue(isinstance(pool._thread_connections, threading.local))
        self.assertEqual(pool._thread_connections.__dict__, {})

        queue = pool._queue
        self.assertTrue(isinstance(queue, six.moves.queue.LifoQueue))
        self.assertTrue(queue.full())
        self.assertEqual(queue.maxsize, size)
        for connection in queue.queue:
            self.assertTrue(isinstance(connection, Connection))
            self.assertTrue(connection._cluster is cluster_copy)

    def test_constructor_passes_kwargs(self):
        table_prefix = 'foo'
        table_prefix_separator = '<>'
        cluster = _Cluster()  # Avoid implicit environ check.

        size = 1
        pool = self._makeOne(size, table_prefix=table_prefix,
                             table_prefix_separator=table_prefix_separator,
                             cluster=cluster)

        for connection in pool._queue.queue:
            self.assertEqual(connection.table_prefix, table_prefix)
            self.assertEqual(connection.table_prefix_separator,
                             table_prefix_separator)

    def test_constructor_ignores_autoconnect(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase.connection import Connection
        from gcloud.bigtable.happybase import pool as MUT

        class ConnectionWithOpen(Connection):

            _open_called = False

            def open(self):
                self._open_called = True

        # First make sure the custom Connection class does as expected.
        cluster_copy1 = _Cluster()
        cluster_copy2 = _Cluster()
        cluster_copy3 = _Cluster()
        cluster = _Cluster(
            copies=[cluster_copy1, cluster_copy2, cluster_copy3])
        connection = ConnectionWithOpen(autoconnect=False, cluster=cluster)
        self.assertFalse(connection._open_called)
        self.assertTrue(connection._cluster is cluster_copy1)
        connection = ConnectionWithOpen(autoconnect=True, cluster=cluster)
        self.assertTrue(connection._open_called)
        self.assertTrue(connection._cluster is cluster_copy2)

        # Then make sure autoconnect=True is ignored in a pool.
        size = 1
        with _Monkey(MUT, Connection=ConnectionWithOpen):
            pool = self._makeOne(size, autoconnect=True, cluster=cluster)

        for connection in pool._queue.queue:
            self.assertTrue(isinstance(connection, ConnectionWithOpen))
            self.assertTrue(connection._cluster is cluster_copy3)
            self.assertFalse(connection._open_called)

    def test_constructor_infers_cluster(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase.connection import Connection
        from gcloud.bigtable.happybase import pool as MUT

        size = 1
        cluster_copy = _Cluster()
        all_copies = [cluster_copy] * size
        cluster = _Cluster(copies=all_copies)
        get_cluster_calls = []

        def mock_get_cluster(timeout=None):
            get_cluster_calls.append(timeout)
            return cluster

        with _Monkey(MUT, _get_cluster=mock_get_cluster):
            pool = self._makeOne(size)

        for connection in pool._queue.queue:
            self.assertTrue(isinstance(connection, Connection))
            # We know that the Connection() constructor will
            # call cluster.copy().
            self.assertTrue(connection._cluster is cluster_copy)

        self.assertEqual(get_cluster_calls, [None])

    def test_constructor_non_integer_size(self):
        size = None
        with self.assertRaises(TypeError):
            self._makeOne(size)

    def test_constructor_non_positive_size(self):
        size = -10
        with self.assertRaises(ValueError):
            self._makeOne(size)
        size = 0
        with self.assertRaises(ValueError):
            self._makeOne(size)

    def _makeOneWithMockQueue(self, queue_return):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import pool as MUT

        # We are going to use a fake queue, so we don't want any connections
        # or clusters to be created in the constructor.
        size = -1
        cluster = object()
        with _Monkey(MUT, _MIN_POOL_SIZE=size):
            pool = self._makeOne(size, cluster=cluster)

        pool._queue = _Queue(queue_return)
        return pool

    def test__acquire_connection(self):
        queue_return = object()
        pool = self._makeOneWithMockQueue(queue_return)

        timeout = 432
        connection = pool._acquire_connection(timeout=timeout)
        self.assertTrue(connection is queue_return)
        self.assertEqual(pool._queue._get_calls, [(True, timeout)])
        self.assertEqual(pool._queue._put_calls, [])

    def test__acquire_connection_failure(self):
        from gcloud.bigtable.happybase.pool import NoConnectionsAvailable

        pool = self._makeOneWithMockQueue(None)
        timeout = 1027
        with self.assertRaises(NoConnectionsAvailable):
            pool._acquire_connection(timeout=timeout)
        self.assertEqual(pool._queue._get_calls, [(True, timeout)])
        self.assertEqual(pool._queue._put_calls, [])

    def test_connection_is_context_manager(self):
        import contextlib
        import six

        queue_return = _Connection()
        pool = self._makeOneWithMockQueue(queue_return)
        cnxn_context = pool.connection()
        if six.PY3:  # pragma: NO COVER Python 3
            self.assertTrue(isinstance(cnxn_context,
                                       contextlib._GeneratorContextManager))
        else:
            self.assertTrue(isinstance(cnxn_context,
                                       contextlib.GeneratorContextManager))

    def test_connection_no_current_cnxn(self):
        queue_return = _Connection()
        pool = self._makeOneWithMockQueue(queue_return)
        timeout = 55

        self.assertFalse(hasattr(pool._thread_connections, 'current'))
        with pool.connection(timeout=timeout) as connection:
            self.assertEqual(pool._thread_connections.current, queue_return)
            self.assertTrue(connection is queue_return)
        self.assertFalse(hasattr(pool._thread_connections, 'current'))

        self.assertEqual(pool._queue._get_calls, [(True, timeout)])
        self.assertEqual(pool._queue._put_calls,
                         [(queue_return, None, None)])

    def test_connection_with_current_cnxn(self):
        current_cnxn = _Connection()
        queue_return = _Connection()
        pool = self._makeOneWithMockQueue(queue_return)
        pool._thread_connections.current = current_cnxn
        timeout = 8001

        with pool.connection(timeout=timeout) as connection:
            self.assertTrue(connection is current_cnxn)

        self.assertEqual(pool._queue._get_calls, [])
        self.assertEqual(pool._queue._put_calls, [])
        self.assertEqual(pool._thread_connections.current, current_cnxn)


class _Client(object):

    def __init__(self):
        self.stop_calls = 0

    def stop(self):
        self.stop_calls += 1


class _Connection(object):

    def open(self):
        pass


class _Cluster(object):

    def __init__(self, copies=()):
        self.copies = list(copies)
        # Included to support Connection.__del__
        self._client = _Client()

    def copy(self):
        if self.copies:
            result = self.copies[0]
            self.copies[:] = self.copies[1:]
            return result
        else:
            return self


class _Queue(object):

    def __init__(self, result=None):
        self.result = result
        self._get_calls = []
        self._put_calls = []

    def get(self, block=None, timeout=None):
        self._get_calls.append((block, timeout))
        if self.result is None:
            import six
            raise six.moves.queue.Empty
        else:
            return self.result

    def put(self, item, block=None, timeout=None):
        self._put_calls.append((item, block, timeout))
