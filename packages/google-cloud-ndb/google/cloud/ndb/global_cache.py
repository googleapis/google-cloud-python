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

"""GlobalCache interface and its implementations."""

import abc
import base64
import collections
import os
import pymemcache.exceptions
import redis.exceptions
import threading
import time
import uuid

import pymemcache
import redis as redis_module


class GlobalCache(object):
    """Abstract base class for a global entity cache.

    A global entity cache is shared across contexts, sessions, and possibly
    even servers. A concrete implementation is available which uses Redis.

    Essentially, this class models a simple key/value store where keys and
    values are arbitrary ``bytes`` instances. "Compare and swap", aka
    "optimistic transactions" should also be supported.

    Concrete implementations can either by synchronous or asynchronous.
    Asynchronous implementations should return
    :class:`~google.cloud.ndb.tasklets.Future` instances whose eventual results
    match the return value described for each method. Because coordinating with
    the single threaded event model used by ``NDB`` can be tricky with remote
    services, it's not recommended that casual users write asynchronous
    implementations, as some specialized knowledge is required.

    Attributes:
        strict_read (bool): If :data:`True`, transient errors that occur as part of a
            entity lookup operation will be logged as warnings but not raised to the
            application layer.
        strict_write (bool): If :data:`True`, transient errors that occur as part of
            a put or delete operation will be logged as warnings, but not raised to the
            application layer. Setting this to :data:`True` somewhat increases the risk
            that other clients might read stale data from the cache.
    """

    __metaclass__ = abc.ABCMeta

    transient_errors = ()
    """Exceptions that should be treated as transient errors in non-strict modes.

    Instances of these exceptions, if raised, will be logged as warnings but will not
    be raised to the application layer, depending on the values of the ``strict_read``
    and ``strict_write`` attributes of the instance.

    This should be overridden by subclasses.
    """

    clear_cache_soon = False
    strict_read = True
    strict_write = True

    @abc.abstractmethod
    def get(self, keys):
        """Retrieve entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to get.

        Returns:
            List[Union[bytes, None]]]: Serialized entities, or :data:`None`,
                for each key.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, items, expires=None):
        """Store entities in the cache.

        Arguments:
            items (Dict[bytes, Union[bytes, None]]): Mapping of keys to
                serialized entities.
            expires (Optional[float]): Number of seconds until value expires.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, keys):
        """Remove entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to remove.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def watch(self, keys):
        """Begin an optimistic transaction for the given keys.

        A future call to :meth:`compare_and_swap` will only set values for keys
        whose values haven't changed since the call to this method.

        Arguments:
            keys (List[bytes]): The keys to watch.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def unwatch(self, keys):
        """End an optimistic transaction for the given keys.

        Indicates that value for the key wasn't found in the database, so there will not
        be a future call to :meth:`compare_and_swap`, and we no longer need to watch
        this key.

        Arguments:
            keys (List[bytes]): The keys to watch.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compare_and_swap(self, items, expires=None):
        """Like :meth:`set` but using an optimistic transaction.

        Only keys whose values haven't changed since a preceding call to
        :meth:`watch` will be changed.

        Arguments:
            items (Dict[bytes, Union[bytes, None]]): Mapping of keys to
                serialized entities.
            expires (Optional[float]): Number of seconds until value expires.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self):
        """Clear all keys from global cache.

        Will be called if there previously was a connection error, to prevent clients
        from reading potentially stale data from the cache.
        """
        raise NotImplementedError


class _InProcessGlobalCache(GlobalCache):
    """Reference implementation of :class:`GlobalCache`.

    Not intended for production use. Uses a single process wide dictionary to
    keep an in memory cache. For use in testing and to have an easily grokkable
    reference implementation. Thread safety is potentially a little sketchy.
    """

    cache = {}
    """Dict: The cache.

    Relies on atomicity of ``__setitem__`` for thread safety. See:
    http://effbot.org/pyfaq/what-kinds-of-global-value-mutation-are-thread-safe.htm
    """

    def __init__(self):
        self._watch_keys = {}

    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""
        now = time.time()
        results = [self.cache.get(key) for key in keys]
        entity_pbs = []
        for result in results:
            if result is not None:
                entity_pb, expires = result
                if expires and expires < now:
                    entity_pb = None
            else:
                entity_pb = None

            entity_pbs.append(entity_pb)

        return entity_pbs

    def set(self, items, expires=None):
        """Implements :meth:`GlobalCache.set`."""
        if expires:
            expires = time.time() + expires

        for key, value in items.items():
            self.cache[key] = (value, expires)  # Supposedly threadsafe

    def delete(self, keys):
        """Implements :meth:`GlobalCache.delete`."""
        for key in keys:
            self.cache.pop(key, None)  # Threadsafe?

    def watch(self, keys):
        """Implements :meth:`GlobalCache.watch`."""
        for key in keys:
            self._watch_keys[key] = self.cache.get(key)

    def unwatch(self, keys):
        """Implements :meth:`GlobalCache.unwatch`."""
        for key in keys:
            self._watch_keys.pop(key, None)

    def compare_and_swap(self, items, expires=None):
        """Implements :meth:`GlobalCache.compare_and_swap`."""
        if expires:
            expires = time.time() + expires

        for key, new_value in items.items():
            watch_value = self._watch_keys.get(key)
            current_value = self.cache.get(key)
            if watch_value == current_value:
                self.cache[key] = (new_value, expires)

    def clear(self):
        """Implements :meth:`GlobalCache.clear`."""
        self.cache.clear()


_Pipeline = collections.namedtuple("_Pipeline", ("pipe", "id"))


class RedisCache(GlobalCache):
    """Redis implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Redis
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        redis (redis.Redis): Instance of Redis client to use.
        strict_read (bool): If :data:`False`, connection errors during read operations
            will be logged with a warning and treated as cache misses, but will not
            raise an exception in the application, with connection errors during reads
            being treated as cache misses.  If :data:`True`, connection errors will be
            raised as exceptions in the application. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an exception in
            the application. If :data:`True`, connection errors during write will be
            raised as exceptions in the application. Because write operations involve
            cache invalidation, setting this to :data:`False` may allow other clients to
            retrieve stale data from the cache.  If there is a connection error, an
            internal flag will be set to clear the cache the next time any method is
            called on this object, to try and minimize the opportunity for clients to
            read stale data from the cache.  Default: :data:`True`.
    """

    transient_errors = (
        redis.exceptions.ConnectionError,
        redis.exceptions.TimeoutError,
    )

    @classmethod
    def from_environment(cls, strict_read=False, strict_write=True):
        """Generate a class:`RedisCache` from an environment variable.

        This class method looks for the ``REDIS_CACHE_URL`` environment
        variable and, if it is set, passes its value to ``Redis.from_url`` to
        construct a ``Redis`` instance which is then used to instantiate a
        ``RedisCache`` instance.

        Args:
            strict_read (bool): If :data:`False`, connection errors during read
                operations will be logged with a warning and treated as cache misses,
                but will not raise an exception in the application, with connection
                errors during reads being treated as cache misses.  If :data:`True`,
                connection errors will be raised as exceptions in the application.
                Default: :data:`False`.
            strict_write (bool): If :data:`False`, connection errors during write
                operations will be logged with a warning, but will not raise an
                exception in the application. If :data:`True`, connection errors during
                write will be raised as exceptions in the application. Because write
                operations involve cache invalidation, setting this to :data:`False` may
                allow other clients to retrieve stale data from the cache.  If there is
                a connection error, an internal flag will be set to clear the cache the
                next time any method is called on this object, to try and minimize the
                opportunity for clients to read stale data from the cache.  Default:
                :data:`True`.

        Returns:
            Optional[RedisCache]: A :class:`RedisCache` instance or
                :data:`None`, if ``REDIS_CACHE_URL`` is not set in the
                environment.
        """
        url = os.environ.get("REDIS_CACHE_URL")
        if url:
            return cls(redis_module.Redis.from_url(url))

    def __init__(self, redis, strict_read=False, strict_write=True):
        self.redis = redis
        self.strict_read = strict_read
        self.strict_write = strict_write
        self._pipes = threading.local()

    @property
    def pipes(self):
        local = self._pipes
        if not hasattr(local, "pipes"):
            local.pipes = {}
        return local.pipes

    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""
        res = self.redis.mget(keys)
        return res

    def set(self, items, expires=None):
        """Implements :meth:`GlobalCache.set`."""
        self.redis.mset(items)
        if expires:
            for key in items.keys():
                self.redis.expire(key, expires)

    def delete(self, keys):
        """Implements :meth:`GlobalCache.delete`."""
        self.redis.delete(*keys)

    def watch(self, keys):
        """Implements :meth:`GlobalCache.watch`."""
        pipe = self.redis.pipeline()
        pipe.watch(*keys)
        holder = _Pipeline(pipe, str(uuid.uuid4()))
        for key in keys:
            self.pipes[key] = holder

    def unwatch(self, keys):
        """Implements :meth:`GlobalCache.watch`."""
        for key in keys:
            holder = self.pipes.pop(key, None)
            if holder:
                holder.pipe.reset()

    def compare_and_swap(self, items, expires=None):
        """Implements :meth:`GlobalCache.compare_and_swap`."""
        pipes = {}
        mappings = {}
        remove_keys = []

        # get associated pipes
        for key, value in items.items():
            remove_keys.append(key)
            if key not in self.pipes:
                continue

            pipe = self.pipes[key]
            pipes[pipe.id] = pipe
            mapping = mappings.setdefault(pipe.id, {})
            mapping[key] = value

        # execute transaction for each pipes
        for pipe_id, mapping in mappings.items():
            pipe = pipes[pipe_id].pipe
            try:
                pipe.multi()
                pipe.mset(mapping)
                if expires:
                    for key in mapping.keys():
                        pipe.expire(key, expires)
                pipe.execute()

            except redis_module.exceptions.WatchError:
                pass

            finally:
                pipe.reset()

        # get keys associated to pipes but not updated
        for key, pipe in self.pipes.items():
            if pipe.id in pipes:
                remove_keys.append(key)

        # remove keys
        for key in remove_keys:
            self.pipes.pop(key, None)

    def clear(self):
        """Implements :meth:`GlobalCache.clear`."""
        self.redis.flushdb()


class MemcacheCache(GlobalCache):
    """Memcache implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Memcache
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        client (pymemcache.Client): Instance of Memcache client to use.
        strict_read (bool): If :data:`False`, connection errors during read operations
            will be logged with a warning and treated as cache misses, but will not
            raise an exception in the application, with connection errors during reads
            being treated as cache misses.  If :data:`True`, connection errors will be
            raised as exceptions in the application. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an exception in
            the application. If :data:`True`, connection errors during write will be
            raised as exceptions in the application. Because write operations involve
            cache invalidation, setting this to :data:`False` may allow other clients to
            retrieve stale data from the cache.  If there is a connection error, an
            internal flag will be set to clear the cache the next time any method is
            called on this object, to try and minimize the opportunity for clients to
            read stale data from the cache.  Default: :data:`True`.
    """

    transient_errors = (
        IOError,
        pymemcache.exceptions.MemcacheServerError,
        pymemcache.exceptions.MemcacheUnexpectedCloseError,
    )

    @staticmethod
    def _parse_host_string(host_string):
        split = host_string.split(":")
        if len(split) == 1:
            return split[0], 11211

        elif len(split) == 2:
            host, port = split
            try:
                port = int(port)
                return host, port
            except ValueError:
                pass

        raise ValueError("Invalid memcached host_string: {}".format(host_string))

    @staticmethod
    def _key(key):
        return base64.b64encode(key)

    @classmethod
    def from_environment(cls, max_pool_size=4, strict_read=False, strict_write=True):
        """Generate a ``pymemcache.Client`` from an environment variable.

        This class method looks for the ``MEMCACHED_HOSTS`` environment
        variable and, if it is set, parses the value as a space delimited list of
        hostnames, optionally with ports. For example:

            "localhost"
            "localhost:11211"
            "1.1.1.1:11211 2.2.2.2:11211 3.3.3.3:11211"

        Args:
            max_pool_size (int): Size of connection pool to be used by client. If set to
                ``0`` or ``1``, connection pooling will not be used. Default: ``4``
            strict_read (bool): If :data:`False`, connection errors during read
                operations will be logged with a warning and treated as cache misses,
                but will not raise an exception in the application, with connection
                errors during reads being treated as cache misses.  If :data:`True`,
                connection errors will be raised as exceptions in the application.
                Default: :data:`False`.
            strict_write (bool): If :data:`False`, connection errors during write
                operations will be logged with a warning, but will not raise an
                exception in the application. If :data:`True`, connection errors during
                write will be raised as exceptions in the application. Because write
                operations involve cache invalidation, setting this to :data:`False` may
                allow other clients to retrieve stale data from the cache.  If there is
                a connection error, an internal flag will be set to clear the cache the
                next time any method is called on this object, to try and minimize the
                opportunity for clients to read stale data from the cache.  Default:
                :data:`True`.

        Returns:
            Optional[MemcacheCache]: A :class:`MemcacheCache` instance or
                :data:`None`, if ``MEMCACHED_HOSTS`` is not set in the
                environment.
        """
        hosts_string = os.environ.get("MEMCACHED_HOSTS")
        if not hosts_string:
            return None

        hosts = [
            cls._parse_host_string(host_string.strip())
            for host_string in hosts_string.split()
        ]

        if not max_pool_size:
            max_pool_size = 1

        if len(hosts) == 1:
            client = pymemcache.PooledClient(hosts[0], max_pool_size=max_pool_size)

        else:
            client = pymemcache.HashClient(
                hosts, use_pooling=True, max_pool_size=max_pool_size
            )

        return cls(client, strict_read=strict_read, strict_write=strict_write)

    def __init__(self, client, strict_read=False, strict_write=True):
        self.client = client
        self.strict_read = strict_read
        self.strict_write = strict_write
        self._cas = threading.local()

    @property
    def caskeys(self):
        local = self._cas
        if not hasattr(local, "caskeys"):
            local.caskeys = {}
        return local.caskeys

    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""
        keys = [self._key(key) for key in keys]
        result = self.client.get_many(keys)
        return [result.get(key) for key in keys]

    def set(self, items, expires=None):
        """Implements :meth:`GlobalCache.set`."""
        items = {self._key(key): value for key, value in items.items()}
        expires = expires if expires else 0
        self.client.set_many(items, expire=expires)

    def delete(self, keys):
        """Implements :meth:`GlobalCache.delete`."""
        keys = [self._key(key) for key in keys]
        self.client.delete_many(keys)

    def watch(self, keys):
        """Implements :meth:`GlobalCache.watch`."""
        keys = [self._key(key) for key in keys]
        caskeys = self.caskeys
        for key, (value, caskey) in self.client.gets_many(keys).items():
            caskeys[key] = caskey

    def unwatch(self, keys):
        """Implements :meth:`GlobalCache.unwatch`."""
        keys = [self._key(key) for key in keys]
        caskeys = self.caskeys
        for key in keys:
            caskeys.pop(key, None)

    def compare_and_swap(self, items, expires=None):
        """Implements :meth:`GlobalCache.compare_and_swap`."""
        caskeys = self.caskeys
        for key, value in items.items():
            key = self._key(key)
            caskey = caskeys.pop(key, None)
            if caskey is None:
                continue

            expires = expires if expires else 0
            self.client.cas(key, value, caskey, expire=expires)

    def clear(self):
        """Implements :meth:`GlobalCache.clear`."""
        self.client.flush_all()
