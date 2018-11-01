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

"""Event loop for running callbacks.

This should handle both asynchronous ``ndb`` objects and arbitrary callbacks.
"""
import collections
import time

__all__ = [
    "add_idle",
    "EventLoop",
    "get_event_loop",
    "queue_call",
    "queue_rpc",
    "run",
    "run0",
    "run1",
]


def _logging_debug(*args, **kw):
    """Placeholder.

    See #6360."""


_Event = collections.namedtuple('_Event', (
    'when', 'callback', 'args', 'kwargs'))


class EventLoop:
    """Constructor.

    Fields:
      current: a FIFO list of (callback, args, kwds). These callbacks
        run immediately when the eventloop runs.
      idlers: a FIFO list of (callback, args, kwds). Thes callbacks
        run only when no other RPCs need to be fired first.
        For example, AutoBatcher uses idler to fire a batch RPC even before
        the batch is full.
      queue: a sorted list of (absolute time in sec, callback, args, kwds),
        sorted by time. These callbacks run only after the said time.
      rpcs: a map from rpc to (callback, args, kwds). Callback is called
        when the rpc finishes.
    """
    __slots__ = ('current', 'idlers', 'inactive', 'queue', 'rpcs')

    def __init__(self):
        self.current = collections.deque()
        self.idlers = collections.deque()
        self.inactive = 0
        self.queue = []
        self.rpcs = {}

    def clear(self):
        """Remove all pending events without running any."""
        while self.current or self.idlers or self.queue or self.rpcs:
            current = self.current
            idlers = self.idlers
            queue = self.queue
            rpcs = self.rpcs
            _logging_debug('Clearing stale EventLoop instance...')
            if current:
                _logging_debug('  current = %s', current)
            if idlers:
                _logging_debug('  idlers = %s', idlers)
            if queue:
                _logging_debug('  queue = %s', queue)
            if rpcs:
                _logging_debug('  rpcs = %s', rpcs)
            self.__init__()
            current.clear()
            idlers.clear()
            queue[:] = []
            rpcs.clear()
            _logging_debug('Cleared')

    def insort_event_right(self, event):
        """Insert event in queue, and keep it sorted by `event.when` assuming
        queue is sorted.

        For events with same `event.when`, new events are inserted to the
        right, to keep FIFO order.

        Args:
          event: a (time in sec since unix epoch, callback, args, kwargs)
          tuple.
        """
        queue = self.queue
        lo = 0
        hi = len(queue)
        while lo < hi:
            mid = (lo + hi) // 2
            if event.when < queue[mid].when:
                hi = mid
            else:
                lo = mid + 1
        queue.insert(lo, event)

    def queue_call(self, delay, callback, *args, **kwargs):
        """Schedule a function call at a specific time in the future."""
        if delay is None:
            self.current.append((callback, args, kwargs))
            return

        # Times over a billion seconds are assumed to be absolute
        when = time.time() + delay if delay < 1e9 else delay
        event = _Event(when, callback, args, kwargs)
        self.insort_event_right(event)

    def queue_rpc(self, rpc, callback=None, *args, **kwds):
        """Schedule an RPC with an optional callback.

        The caller must have previously sent the call to the service.
        The optional callback is called with the remaining arguments.

        NOTE: If the rpc is a MultiRpc, the callback will be called once
        for each sub-RPC.  TODO: Is this a good idea?
        """
        # TODO Integrate with gRPC
        raise NotImplementedError

    def add_idle(self, callback, *args, **kwargs):
        """Add an idle callback.

        An idle callback can return True, False or None.  These mean:

        - None: remove the callback (don't reschedule)
        - False: the callback did no work; reschedule later
        - True: the callback did some work; reschedule soon

        If the callback raises an exception, the traceback is logged and
        the callback is removed.
        """
        self.idlers.append((callback, args, kwargs))

    def run_idle(self):
        """Run one of the idle callbacks.

        Returns:
          True if one was called, False if no idle callback was called.
        """
        if not self.idlers or self.inactive >= len(self.idlers):
            return False
        idler = self.idlers.popleft()
        callback, args, kwargs = idler
        _logging_debug('idler: %s', callback.__name__)
        result = callback(*args, **kwargs)

        # See add_idle() for meaning of callback return value.
        if result is None:
            _logging_debug('idler %s removed', callback.__name__)
        else:
            if result:
                self.inactive = 0
            else:
                self.inactive += 1
            self.idlers.append(idler)
        return True

    def _run_current(self):
        """Run one current item.

        Returns:
            True if one was called, False if no callback was called.
        """
        if not self.current:
            return False

        self.inactive = 0
        callback, args, kwargs = self.current.popleft()
        _logging_debug('nowevent: %s', callback.__name__)
        callback(*args, **kwargs)
        return True

    def run0(self):
        """Run one item (a callback or an RPC wait_any).

        Returns:
          A time to sleep if something happened (may be 0);
          None if all queues are empty.
        """
        if self._run_current() or self.run_idle():
            return 0

        delay = None
        if self.queue:
            delay = self.queue[0][0] - time.time()
            if delay <= 0:
                self.inactive = 0
                _, callback, args, kwargs = self.queue.pop(0)
                _logging_debug('event: %s', callback.__name__)
                callback(*args, **kwargs)
                # TODO: What if it raises an exception?
                return 0

        if self.rpcs:
            raise NotImplementedError

        return delay

    def run1(self):
        """Run one item (a callback or an RPC wait_any) or sleep.

        Returns:
          True if something happened; False if all queues are empty.
        """
        delay = self.run0()
        if delay is None:
            return False
        if delay > 0:
            time.sleep(delay)
        return True

    def run(self):
        """Run until there's nothing left to do."""
        self.inactive = 0
        while True:
            if not self.run1():
                break


def add_idle(*args, **kwargs):
    raise NotImplementedError


def get_event_loop(*args, **kwargs):
    raise NotImplementedError


def queue_call(*args, **kwargs):
    raise NotImplementedError


def queue_rpc(*args, **kwargs):
    raise NotImplementedError


def run(*args, **kwargs):
    raise NotImplementedError


def run0(*args, **kwargs):
    raise NotImplementedError


def run1(*args, **kwargs):
    raise NotImplementedError
