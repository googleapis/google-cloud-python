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
    """

    __metaclass__ = abc.ABCMeta

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

    def compare_and_swap(self, items, expires=None):
        """Implements :meth:`GlobalCache.compare_and_swap`."""
        if expires:
            expires = time.time() + expires

        for key, new_value in items.items():
            watch_value = self._watch_keys.get(key)
            current_value = self.cache.get(key)
            if watch_value == current_value:
                self.cache[key] = (new_value, expires)


_Pipeline = collections.namedtuple("_Pipeline", ("pipe", "id"))


class RedisCache(GlobalCache):
    """Redis implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Redis
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        redis (redis.Redis): Instance of Redis client to use.
    """

    @classmethod
    def from_environment(cls):
        """Generate a class:`RedisCache` from an environment variable.

        This class method looks for the ``REDIS_CACHE_URL`` environment
        variable and, if it is set, passes its value to ``Redis.from_url`` to
        construct a ``Redis`` instance which is then used to instantiate a
        ``RedisCache`` instance.

        Returns:
            Optional[RedisCache]: A :class:`RedisCache` instance or
                :data:`None`, if ``REDIS_CACHE_URL`` is not set in the
                environment.
        """
        url = os.environ.get("REDIS_CACHE_URL")
        if url:
            return cls(redis_module.Redis.from_url(url))

    def __init__(self, redis):
        self.redis = redis
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

    def compare_and_swap(self, items, expires=None):
        """Implements :meth:`GlobalCache.compare_and_swap`."""
        pipes = {}
        mappings = {}
        results = {}
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

        # remote keys
        for key in remove_keys:
            self.pipes.pop(key, None)

        return results


class MemcacheCache(GlobalCache):
    """Memcache implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Memcache
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        client (pymemcache.Client): Instance of Memcache client to use.
    """

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
    def from_environment(cls, max_pool_size=4):
        """Generate a ``pymemcache.Client`` from an environment variable.

        This class method looks for the ``MEMCACHED_HOSTS`` environment
        variable and, if it is set, parses the value as a space delimited list of
        hostnames, optionally with ports. For example:

            "localhost"
            "localhost:11211"
            "1.1.1.1:11211 2.2.2.2:11211 3.3.3.3:11211"

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

        return cls(client)

    def __init__(self, client):
        self.client = client
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
