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

"""Context for currently running tasks and transactions."""

import collections
import contextlib
import threading

from google.cloud.ndb import _datastore_api
from google.cloud.ndb import _eventloop
from google.cloud.ndb import exceptions


__all__ = [
    "AutoBatcher",
    "Context",
    "ContextOptions",
    "get_context",
    "TransactionOptions",
]


_ContextTuple = collections.namedtuple(
    "_ContextTuple",
    [
        "client",
        "eventloop",
        "stub",
        "batches",
        "commit_batches",
        "transaction",
    ],
)


class _LocalState(threading.local):
    """Thread local state."""

    __slots__ = ("context",)

    def __init__(self):
        self.context = None


_state = _LocalState()


def get_context():
    """Get the current context.

    This function should be called within a context established by
    :meth:`google.cloud.ndb.client.Client.context`.

    Returns:
        Context: The current context.

    Raises:
        .ContextError: If called outside of a context
            established by :meth:`google.cloud.ndb.client.Client.context`.
    """
    context = _state.context
    if context:
        return context

    raise exceptions.ContextError()


class _Context(_ContextTuple):
    """Current runtime state.

    Instances of this class hold on to runtime state such as the current event
    loop, current transaction, etc. Instances are shallowly immutable, but
    contain references to data structures which are mutable, such as the event
    loop. A new context can be derived from an existing context using
    :meth:`new`.

    :class:`Context` is a subclass of :class:`_Context` which provides
    only publicly facing interface. The use of two classes is only to provide a
    distinction between public and private API.

    Arguments:
        client (client.Client): The NDB client for this context.
    """

    def __new__(
        cls,
        client,
        eventloop=None,
        stub=None,
        batches=None,
        commit_batches=None,
        transaction=None,
    ):
        if eventloop is None:
            eventloop = _eventloop.EventLoop()

        if stub is None:
            stub = _datastore_api.make_stub(client)

        if batches is None:
            batches = {}

        if commit_batches is None:
            commit_batches = {}

        return super(_Context, cls).__new__(
            cls,
            client=client,
            eventloop=eventloop,
            stub=stub,
            batches=batches,
            commit_batches=commit_batches,
            transaction=transaction,
        )

    def new(self, **kwargs):
        """Create a new :class:`_Context` instance.

        New context will be the same as context except values from ``kwargs``
        will be substituted.
        """
        state = {name: getattr(self, name) for name in self._fields}
        state.update(kwargs)
        return type(self)(**state)

    @contextlib.contextmanager
    def use(self):
        """Use this context as the current context.

        This method returns a context manager for use with the ``with``
        statement. Code inside the ``with`` context will see this context as
        the current context.
        """
        prev_context = _state.context
        _state.context = self
        try:
            yield self
        finally:
            _state.context = prev_context


class Context(_Context):
    """User management of cache and other policy."""

    def clear_cache(self):
        """Clears the in-memory cache.

        This does not affect memcache.
        """
        raise NotImplementedError

    def flush(self):
        """Force any pending batch operations to go ahead and run."""
        raise NotImplementedError

    def get_cache_policy(self):
        """Return the current context cache policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached.  May be :data:`None`.
        """
        raise NotImplementedError

    def get_datastore_policy(self):
        """Return the current context datastore policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should use the datastore. May be :data:`None`.
        """
        raise NotImplementedError

    def get_memcache_policy(self):
        """Return the current memcache policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached. May be :data:`None`.
        """
        raise NotImplementedError

    def get_memcache_timeout_policy(self):
        """Return the current policy function memcache timeout (expiration).

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns an ``int`` indicating the
                timeout, in seconds, for the key. :data:`0` implies the default
                timeout. May be :data:`None`.
        """
        raise NotImplementedError

    def set_cache_policy(self, policy):
        """Set the context cache policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached.  May be :data:`None`.
        """
        raise NotImplementedError

    def set_datastore_policy(self, policy):
        """Set the context datastore policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should use the datastore.  May be :data:`None`.
        """
        raise NotImplementedError

    def set_memcache_policy(self, policy):
        """Set the memcache policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached.  May be :data:`None`.
        """
        raise NotImplementedError

    def set_memcache_timeout_policy(self, policy):
        """Set the policy function for memcache timeout (expiration).

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns an ``int`` indicating the
                timeout, in seconds, for the key. :data:`0` implies the default
                timout. May be :data:`None`.
        """
        raise NotImplementedError

    def call_on_commit(self, callback):
        """Call a callback upon successful commit of a transaction.

        If not in a transaction, the callback is called immediately.

        In a transaction, multiple callbacks may be registered and will be
        called once the transaction commits, in the order in which they
        were registered.  If the transaction fails, the callbacks will not
        be called.

        If the callback raises an exception, it bubbles up normally.  This
        means: If the callback is called immediately, any exception it
        raises will bubble up immediately.  If the call is postponed until
        commit, remaining callbacks will be skipped and the exception will
        bubble up through the transaction() call.  (However, the
        transaction is already committed at that point.)

        Args:
            callback (Callable): The callback function.
        """
        raise NotImplementedError

    def in_transaction(self):
        """Get whether a transaction is currently active.

        Returns:
            bool: :data:`True` if currently in a transaction, otherwise
                :data:`False`.
        """
        raise NotImplementedError

    @staticmethod
    def default_cache_policy(key):
        """Default cache policy.

        This defers to :meth:`~google.cloud.ndb.model.Model._use_cache`.

        Args:
            key (google.cloud.ndb.model.key.Key): The key.

        Returns:
            Union[bool, NoneType]: Whether to cache the key.
        """
        raise NotImplementedError

    @staticmethod
    def default_datastore_policy(key):
        """Default cache policy.

        This defers to :meth:`~google.cloud.ndb.model.Model._use_datastore`.

        Args:
            key (google.cloud.ndb.model.key.Key): The key.

        Returns:
            Union[bool, NoneType]: Whether to use datastore.
        """
        raise NotImplementedError

    @staticmethod
    def default_memcache_policy(key):
        """Default memcache policy.

        This defers to :meth:`~google.cloud.ndb.model.Model._use_memcache`.

        Args:
            key (google.cloud.ndb.model.key.Key): The key.

        Returns:
            Union[bool, NoneType]: Whether to cache the key.
        """
        raise NotImplementedError

    @staticmethod
    def default_memcache_timeout_policy(key):
        """Default memcache timeout policy.

        This defers to :meth:`~google.cloud.ndb.model.Model._memcache_timeout`.

        Args:
            key (google.cloud.ndb.model.key.Key): The key.

        Returns:
            Union[int, NoneType]: Memcache timeout to use.
        """
        raise NotImplementedError

    def memcache_add(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_cas(self, *args, **kwargs):
        """Direct pass-through to memcache client."""

        raise NotImplementedError

    def memcache_decr(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_delete(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_get(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_gets(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_incr(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_replace(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def memcache_set(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise NotImplementedError

    def urlfetch(self, *args, **kwargs):
        """Fetch a resource using HTTP."""
        raise NotImplementedError


class ContextOptions:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TransactionOptions:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class AutoBatcher:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise exceptions.NoLongerImplementedError()
