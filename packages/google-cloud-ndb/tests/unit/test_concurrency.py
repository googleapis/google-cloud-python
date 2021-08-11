# Copyright 2021 Google LLC
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
import logging

try:
    from unittest import mock
except ImportError:  # pragma: NO PY3 COVER
    import mock

from google.cloud.ndb import _cache
from google.cloud.ndb import _eventloop
from google.cloud.ndb import global_cache as global_cache_module
from google.cloud.ndb import tasklets
from google.cloud.ndb import utils


log = logging.getLogger(__name__)


class Delay(object):
    """A tasklet wrapper which delays the return of a tasklet.

    Used to orchestrate timing of events in async code to test particular scenarios
    involving concurrency. Use with `mock.patch` to replace particular tasklets with
    wrapped versions. When those tasklets are called, they will execute and then the
    wrapper will hang on to the result until :meth:`Delay.advance()` is called, at which
    time the tasklet's caller will receive the result.

    Args:
        wrapped (tasklets.Tasklet): The tasklet to be delayed.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.info = "Delay {}".format(self.wrapped.__name__)
        self._futures = collections.deque()

    @tasklets.tasklet
    def __call__(self, *args, **kwargs):
        future = tasklets.Future(self.info)
        self._futures.append(future)

        result = yield self.wrapped(*args, **kwargs)
        yield future
        raise tasklets.Return(result)

    def advance(self):
        """Allow a call to the wrapper to proceed.

        Calls are advanced in the order in which they were orignally made.
        """
        self._futures.popleft().set_result(None)


def run_until():
    """Do all queued work on the event loop.

    This will allow any currently running tasklets to execute up to the point that they
    hit a call to a tasklet that is delayed by :class:`Delay`. When this call is
    finished, either all in progress tasklets will have been completed, or a call to
    :class:`Delay.advance` will be required to move execution forward again.
    """
    while _eventloop.run1():
        pass


def test_global_cache_concurrent_writes_692(in_context):
    """Regression test for #692

    https://github.com/googleapis/python-ndb/issues/692
    """
    key = b"somekey"

    @tasklets.tasklet
    def run_test():
        lock1 = yield _cache.global_lock_for_write(key)
        lock2, _ = yield (
            _cache.global_lock_for_write(key),
            _cache.global_unlock_for_write(key, lock1),
        )
        yield _cache.global_unlock_for_write(key, lock2)

    delay_global_get = Delay(_cache.global_get)
    with mock.patch("google.cloud.ndb._cache._global_get", delay_global_get):
        global_cache = global_cache_module._InProcessGlobalCache()
        with in_context.new(global_cache=global_cache).use():
            future = run_test()

            # Run until the global_cache_get call in the first global_lock_for_write
            # call
            run_until()
            utils.logging_debug(log, "zero")

            # Let the first global_cache_get call return and advance to the
            # global_cache_get calls in the first call to global_unlock_for_write and
            # second call to global_lock_for_write. They will have both gotten the same
            # "old" value from the cache
            delay_global_get.advance()
            run_until()
            utils.logging_debug(log, "one")

            # Let the global_cache_get call return in the second global_lock_for_write
            # call. It should write a new lock value containing both locks.
            delay_global_get.advance()
            run_until()
            utils.logging_debug(log, "two")

            # Let the global_cache_get call return in the first global_unlock_for_write
            # call. Since its "old" cache value contained only the first lock, it might
            # think it's done and delete the key, since as far as it's concerned, there
            # are no more locks. This is the bug exposed by this test.
            delay_global_get.advance()
            run_until()
            utils.logging_debug(log, "three")

            # Since we've fixed the bug now, what we expect it to do instead is attempt
            # to write a new cache value that is a write lock value but contains no
            # locks. This attempt will fail since the cache value was changed out from
            # under it by the second global_lock_write call occurring in parallel. When
            # this attempt fails it will call global_get again to get the new value
            # containing both locks and recompute a value that only includes the second
            # lock and write it.
            delay_global_get.advance()
            run_until()
            utils.logging_debug(log, "four")

            # Now the last call to global_unlock_for_write will call global_get to get
            # the current lock value with only one write lock, and then write an empty
            # write lock.
            delay_global_get.advance()
            run_until()
            utils.logging_debug(log, "five")

            # Make sure we can get to the end without raising an exception
            future.result()

            # Make sure the empty write lock registers as "not locked".
            assert not _cache.is_locked_value(_cache.global_get(key).result())
