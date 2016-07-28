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

"""Google Cloud Bigtable HappyBase pool module."""


import contextlib
import threading

import six

from gcloud.bigtable.happybase.connection import Connection
from gcloud.bigtable.happybase.connection import _get_instance


_MIN_POOL_SIZE = 1
"""Minimum allowable size of a connection pool."""


class NoConnectionsAvailable(RuntimeError):
    """Exception raised when no connections are available.

    This happens if a timeout was specified when obtaining a connection,
    and no connection became available within the specified timeout.
    """


class ConnectionPool(object):
    """Thread-safe connection pool.

    .. note::

        All keyword arguments are passed unmodified to the
        :class:`Connection <.happybase.connection.Connection>` constructor
        **except** for ``autoconnect``. This is because the ``open`` /
        ``closed`` status of a connection is managed by the pool. In addition,
        if ``instance`` is not passed, the default / inferred instance is
        determined by the pool and then passed to each
        :class:`Connection <.happybase.connection.Connection>` that is created.

    :type size: int
    :param size: The maximum number of concurrently open connections.

    :type kwargs: dict
    :param kwargs: Keyword arguments passed to
                   :class:`Connection <.happybase.Connection>`
                   constructor.

    :raises: :class:`TypeError <exceptions.TypeError>` if ``size``
             is non an integer.
             :class:`ValueError <exceptions.ValueError>` if ``size``
             is not positive.
    """
    def __init__(self, size, **kwargs):
        if not isinstance(size, six.integer_types):
            raise TypeError('Pool size arg must be an integer')

        if size < _MIN_POOL_SIZE:
            raise ValueError('Pool size must be positive')

        self._lock = threading.Lock()
        self._queue = six.moves.queue.LifoQueue(maxsize=size)
        self._thread_connections = threading.local()

        connection_kwargs = kwargs
        connection_kwargs['autoconnect'] = False
        if 'instance' not in connection_kwargs:
            connection_kwargs['instance'] = _get_instance(
                timeout=kwargs.get('timeout'))

        for _ in six.moves.range(size):
            connection = Connection(**connection_kwargs)
            self._queue.put(connection)

    def _acquire_connection(self, timeout=None):
        """Acquire a connection from the pool.

        :type timeout: int
        :param timeout: (Optional) Time (in seconds) to wait for a connection
                        to open.

        :rtype: :class:`Connection <.happybase.Connection>`
        :returns: An active connection from the queue stored on the pool.
        :raises: :class:`NoConnectionsAvailable` if ``Queue.get`` fails
                 before the ``timeout`` (only if a timeout is specified).
        """
        try:
            return self._queue.get(block=True, timeout=timeout)
        except six.moves.queue.Empty:
            raise NoConnectionsAvailable('No connection available from pool '
                                         'within specified timeout')

    @contextlib.contextmanager
    def connection(self, timeout=None):
        """Obtain a connection from the pool.

        Must be used as a context manager, for example::

            with pool.connection() as connection:
                pass  # do something with the connection

        If ``timeout`` is omitted, this method waits forever for a connection
        to become available from the local queue.

        Yields an active :class:`Connection <.happybase.connection.Connection>`
        from the pool.

        :type timeout: int
        :param timeout: (Optional) Time (in seconds) to wait for a connection
                        to open.

        :raises: :class:`NoConnectionsAvailable` if no connection can be
                 retrieved from the pool before the ``timeout`` (only if
                 a timeout is specified).
        """
        connection = getattr(self._thread_connections, 'current', None)

        retrieved_new_cnxn = False
        if connection is None:
            # In this case we need to actually grab a connection from the
            # pool. After retrieval, the connection is stored on a thread
            # local so that nested connection requests from the same
            # thread can re-use the same connection instance.
            #
            # NOTE: This code acquires a lock before assigning to the
            #       thread local; see
            #       ('https://emptysqua.re/blog/'
            #        'another-thing-about-pythons-threadlocals/')
            retrieved_new_cnxn = True
            connection = self._acquire_connection(timeout)
            with self._lock:
                self._thread_connections.current = connection

        # This is a no-op for connections that have already been opened
        # since they just call Client.start().
        connection.open()
        yield connection

        # Remove thread local reference after the outermost 'with' block
        # ends. Afterwards the thread no longer owns the connection.
        if retrieved_new_cnxn:
            del self._thread_connections.current
            self._queue.put(connection)
