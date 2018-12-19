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

"""Provides a tasklet decorator and related helpers.

Tasklets are a way to write concurrently running functions without
threads.
"""

import functools
import grpc
import types

from google.cloud.ndb import _eventloop

__all__ = [
    "add_flow_exception",
    "Future",
    "get_context",
    "get_return_value",
    "make_context",
    "make_default_context",
    "MultiFuture",
    "QueueFuture",
    "ReducingFuture",
    "Return",
    "SerialQueueFuture",
    "set_context",
    "sleep",
    "synctasklet",
    "tasklet",
    "toplevel",
]


def add_flow_exception(*args, **kwargs):
    raise NotImplementedError


class Future:
    """Base class for all NDB futures.

    Provides interface defined by :class:`concurrent.futures.Future` as well as
    legacy NDB ``Future`` class.

    Sketchy code, very incomplete.
    """
    def __init__(self):
        self._done = False
        self._result = None

    def set_result(self, result):
        self._result = result
        self._done = True

    def done(self):
        return self._done

    def result(self):
        while not self._done:
            _eventloop.run1()
        return self._result


class TaskletFuture(Future):
    """A Future for an NDB tasklet.

    Sketchy code, very incomplete.
    """
    def __init__(self, generator):
        super(TaskletFuture, self).__init__()
        self.generator = generator

    def _advance_tasklet(self, send_value=None):
        """Advances tasklet one step given a value to send into generator."""
        try:
            # Send next value in to generator (will be None if just starting)
            yielded = self.generator.send(send_value)

        except StopIteration as stop:
            # Tasklet has finished
            self.set_result(get_return_value(stop))

        else:
            # Tasklet has yielded a value. We expect this to either be a gRPC
            # future, or a Future from another tasklet
            if isinstance(yielded, grpc.Future):
                _eventloop.queue_rpc(self, yielded)

            elif isinstance(yielded, Future):
                raise NotImplementedError

            else:
                raise RuntimeError(
                    "A tasklet yielded an illegal value: {:r}".format(yielded)
                )


def get_context(*args, **kwargs):
    raise NotImplementedError


def get_return_value(stop: StopIteration):
    """Inspect StopIteration instance for return value of tasklet."""
    if not stop.args:
        result = None
    elif len(stop.args) == 1:
        result = stop.args[0]
    else:
        result = stop.args
    return result


def make_context(*args, **kwargs):
    raise NotImplementedError


def make_default_context(*args, **kwargs):
    raise NotImplementedError


class MultiFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class QueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ReducingFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


Return = StopIteration


class SerialQueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def set_context(*args, **kwargs):
    raise NotImplementedError


def sleep(*args, **kwargs):
    raise NotImplementedError


def synctasklet(*args, **kwargs):
    raise NotImplementedError


def tasklet(wrapped):
    """Turns a function or method into a tasklet."""
    @functools.wraps(wrapped)
    def tasklet_wrapper(*args, **kwargs):
        try:
            result = wrapped(*args, **kwargs)
        except StopIteration as stop:
            # Just in case the function is not a generator but still uses
            # the "raise Return(...)" idiom, we'll extract the return value.
            result = get_return_value(stop)

        if isinstance(result, types.GeneratorType):
            future = TaskletFuture(result)
            future._advance_tasklet()
        else:
            future = Future()
            future.set_result(result)

        return future

    return tasklet_wrapper



def toplevel(*args, **kwargs):
    raise NotImplementedError
