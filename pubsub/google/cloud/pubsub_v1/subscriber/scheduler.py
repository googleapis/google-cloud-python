# Copyright 2018, Google LLC
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

"""Schedulers provide means to *schedule* callbacks asynchronously.

These are used by the subscriber to call the user-provided callback to process
each message.
"""

import abc
import concurrent.futures
import sys

import six
from six.moves import queue


@six.add_metaclass(abc.ABCMeta)
class Scheduler(object):
    """Abstract base class for schedulers.

    Schedulers are used to schedule callbacks asynchronously.
    """

    @property
    @abc.abstractmethod
    def queue(self):
        """Queue: A concurrency-safe queue specific to the underlying
        concurrency implementation.

        This queue is used to send messages *back* to the scheduling actor.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def schedule(self, callback, *args, **kwargs):
        """Schedule the callback to be called asynchronously.

        Args:
            callback (Callable): The function to call.
            args: Positional arguments passed to the function.
            kwargs: Key-word arguments passed to the function.

        Returns:
            None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def shutdown(self):
        """Shuts down the scheduler and immediately end all pending callbacks.
        """
        raise NotImplementedError


def _make_default_thread_pool_executor():
    # Python 2.7 and 3.6+ have the thread_name_prefix argument, which is useful
    # for debugging.
    executor_kwargs = {}
    if sys.version_info[:2] == (2, 7) or sys.version_info >= (3, 6):
        executor_kwargs["thread_name_prefix"] = "ThreadPoolExecutor-ThreadScheduler"
    return concurrent.futures.ThreadPoolExecutor(max_workers=10, **executor_kwargs)


class ThreadScheduler(Scheduler):
    """A thread pool-based scheduler.

    This scheduler is useful in typical I/O-bound message processing.

    Args:
        executor(concurrent.futures.ThreadPoolExecutor): An optional executor
            to use. If not specified, a default one will be created.
    """

    def __init__(self, executor=None):
        self._queue = queue.Queue()
        if executor is None:
            self._executor = _make_default_thread_pool_executor()
        else:
            self._executor = executor

    @property
    def queue(self):
        """Queue: A thread-safe queue used for communication between callbacks
        and the scheduling thread."""
        return self._queue

    def schedule(self, callback, *args, **kwargs):
        """Schedule the callback to be called asynchronously in a thread pool.

        Args:
            callback (Callable): The function to call.
            args: Positional arguments passed to the function.
            kwargs: Key-word arguments passed to the function.

        Returns:
            None
        """
        self._executor.submit(callback, *args, **kwargs)

    def shutdown(self):
        """Shuts down the scheduler and immediately end all pending callbacks.
        """
        # Drop all pending item from the executor. Without this, the executor
        # will block until all pending items are complete, which is
        # undesirable.
        try:
            while True:
                self._executor._work_queue.get(block=False)
        except queue.Empty:
            pass
        self._executor.shutdown()
