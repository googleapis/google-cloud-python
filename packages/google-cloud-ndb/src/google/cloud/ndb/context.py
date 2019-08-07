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

from google.cloud.ndb import _cache
from google.cloud.ndb import _datastore_api
from google.cloud.ndb import _eventloop
from google.cloud.ndb import exceptions
from google.cloud.ndb import model
from google.cloud.ndb import tasklets


__all__ = [
    "AutoBatcher",
    "Context",
    "ContextOptions",
    "get_context",
    "TransactionOptions",
]


class _LocalState(threading.local):
    """Thread local state."""

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


def _default_cache_policy(key):
    """The default cache policy.

    Defers to ``_use_cache`` on the Model class for the key's kind.

    See: :meth:`~google.cloud.ndb.context.Context.set_cache_policy`
    """
    flag = None
    if key is not None:
        modelclass = model.Model._kind_map.get(key.kind())
        if modelclass is not None:
            policy = getattr(modelclass, "_use_cache", None)
            if policy is not None:
                if isinstance(policy, bool):
                    flag = policy
                else:
                    flag = policy(key)

    return flag


def _default_global_cache_policy(key):
    """The default global cache policy.

    Defers to ``_use_global_cache`` on the Model class for the key's kind.
    See: :meth:`~google.cloud.ndb.context.Context.set_global_cache_policy`
    """
    flag = None
    if key is not None:
        modelclass = model.Model._kind_map.get(key.kind)
        if modelclass is not None:
            policy = getattr(modelclass, "_use_global_cache", None)
            if policy is not None:
                if isinstance(policy, bool):
                    flag = policy
                else:
                    flag = policy(key)

    return flag


def _default_global_cache_timeout_policy(key):
    """The default global cache timeout policy.

    Defers to ``_global_cache_timeout`` on the Model class for the key's kind.
    See:
    :meth:`~google.cloud.ndb.context.Context.set_global_cache_timeout_policy`
    """
    timeout = None
    if key is not None:
        modelclass = model.Model._kind_map.get(key.kind)
        if modelclass is not None:
            policy = getattr(modelclass, "_global_cache_timeout", None)
            if policy is not None:
                if isinstance(policy, int):
                    timeout = policy
                else:
                    timeout = policy(key)

    return timeout


_ContextTuple = collections.namedtuple(
    "_ContextTuple",
    [
        "client",
        "eventloop",
        "stub",
        "batches",
        "commit_batches",
        "transaction",
        "cache",
        "global_cache",
    ],
)


class _Context(_ContextTuple):
    """Current runtime state.

    Instances of this class hold on to runtime state such as the current event
    loop, current transaction, etc. Instances are shallowly immutable, but
    contain references to data structures which are mutable, such as the event
    loop. A new context can be derived from an existing context using
    :meth:`new`.

    :class:`Context` is a subclass of :class:`_Context` which provides only
    publicly facing interface. The use of two classes is only to provide a
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
        cache=None,
        cache_policy=None,
        global_cache=None,
        global_cache_policy=None,
        global_cache_timeout_policy=None,
    ):
        if eventloop is None:
            eventloop = _eventloop.EventLoop()

        if stub is None:
            stub = _datastore_api.make_stub(client)

        if batches is None:
            batches = {}

        if commit_batches is None:
            commit_batches = {}

        # Create a cache and, if an existing cache was passed into this
        # method, duplicate its entries.
        new_cache = _cache.ContextCache()
        if cache:
            new_cache.update(cache)

        context = super(_Context, cls).__new__(
            cls,
            client=client,
            eventloop=eventloop,
            stub=stub,
            batches=batches,
            commit_batches=commit_batches,
            transaction=transaction,
            cache=new_cache,
            global_cache=global_cache,
        )

        context.set_cache_policy(cache_policy)
        context.set_global_cache_policy(global_cache_policy)
        context.set_global_cache_timeout_policy(global_cache_timeout_policy)

        return context

    def new(self, **kwargs):
        """Create a new :class:`_Context` instance.

        New context will be the same as context except values from ``kwargs``
        will be substituted.
        """
        fields = self._fields + tuple(self.__dict__.keys())
        state = {name: getattr(self, name) for name in fields}
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
            if prev_context:
                prev_context.cache.update(self.cache)
            _state.context = prev_context

    @tasklets.tasklet
    def _clear_global_cache(self):
        """Clears the global cache.

        Clears keys from the global cache that appear in the local context
        cache. In this way, only keys that were touched in the current context
        are affected.
        """
        keys = [
            _cache.global_cache_key(key._key)
            for key in self.cache
            if self._use_global_cache(key)
        ]
        if keys:
            yield [_cache.global_delete(key) for key in keys]

    def _use_cache(self, key, options):
        """Return whether to use the context cache for this key."""
        flag = options.use_cache
        if flag is None:
            flag = self.cache_policy(key)
        if flag is None:
            flag = True
        return flag

    def _use_global_cache(self, key, options=None):
        """Return whether to use the global cache for this key."""
        if self.global_cache is None:
            return False

        flag = options.use_global_cache if options else None
        if flag is None:
            flag = self.global_cache_policy(key)
        if flag is None:
            flag = True
        return flag

    def _global_cache_timeout(self, key, options):
        """Return  global cache timeout (expiration) for this key."""
        timeout = None
        if options:
            timeout = options.global_cache_timeout
        if timeout is None:
            timeout = self.global_cache_timeout_policy(key)
        return timeout


class Context(_Context):
    """User management of cache and other policy."""

    def clear_cache(self):
        """Clears the in-memory cache.

        This does not affect global cache.
        """
        self.cache.clear()

    def flush(self):
        """Force any pending batch operations to go ahead and run."""
        raise NotImplementedError

    def get_cache_policy(self):
        """Return the current context cache policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached. May be :data:`None`.
        """
        return self.cache_policy

    def get_datastore_policy(self):
        """Return the current context datastore policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should use the datastore. May be :data:`None`.
        """
        raise NotImplementedError

    def get_global_cache_policy(self):
        """Return the current memcache policy function.

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached. May be :data:`None`.
        """
        return self.global_cache_policy

    get_memcache_policy = get_global_cache_policy  # backwards compatability

    def get_global_cache_timeout_policy(self):
        """Return the current policy function memcache timeout (expiration).

        Returns:
            Callable: A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns an ``int`` indicating the
                timeout, in seconds, for the key. ``0`` implies the default
                timeout. May be :data:`None`.
        """
        return self.global_cache_timeout_policy

    get_memcache_timeout_policy = get_global_cache_timeout_policy

    def set_cache_policy(self, policy):
        """Set the context cache policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached.  May be :data:`None`.
        """
        if policy is None:
            policy = _default_cache_policy

        elif isinstance(policy, bool):
            flag = policy

            def policy(key):
                return flag

        self.cache_policy = policy

    def set_datastore_policy(self, policy):
        """Set the context datastore policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should use the datastore.  May be :data:`None`.
        """
        raise NotImplementedError

    def set_global_cache_policy(self, policy):
        """Set the memcache policy function.

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns a ``bool`` indicating if it
                should be cached.  May be :data:`None`.
        """
        if policy is None:
            policy = _default_global_cache_policy

        elif isinstance(policy, bool):
            flag = policy

            def policy(key):
                return flag

        self.global_cache_policy = policy

    set_memcache_policy = set_global_cache_policy  # backwards compatibility

    def set_global_cache_timeout_policy(self, policy):
        """Set the policy function for memcache timeout (expiration).

        Args:
            policy (Callable): A function that accepts a
                :class:`~google.cloud.ndb.key.Key` instance as a single
                positional argument and returns an ``int`` indicating the
                timeout, in seconds, for the key. ``0`` implies the default
                timeout. May be :data:`None`.
        """
        if policy is None:
            policy = _default_global_cache_timeout_policy

        elif isinstance(policy, int):
            timeout = policy

            def policy(key):
                return timeout

        self.global_cache_timeout_policy = policy

    set_memcache_timeout_policy = set_global_cache_timeout_policy

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
        return self.transaction is not None

    @staticmethod
    def default_datastore_policy(key):
        """Default cache policy.

        This defers to ``Model._use_datastore``.

        Args:
            key (google.cloud.ndb.key.Key): The key.

        Returns:
            Union[bool, None]: Whether to use datastore.
        """
        raise NotImplementedError

    def memcache_add(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_cas(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_decr(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_delete(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_get(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_gets(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_incr(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_replace(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def memcache_set(self, *args, **kwargs):
        """Direct pass-through to memcache client."""
        raise exceptions.NoLongerImplementedError()

    def urlfetch(self, *args, **kwargs):
        """Fetch a resource using HTTP."""
        raise exceptions.NoLongerImplementedError()


class ContextOptions:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise exceptions.NoLongerImplementedError()


class TransactionOptions:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise exceptions.NoLongerImplementedError()


class AutoBatcher:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise exceptions.NoLongerImplementedError()
