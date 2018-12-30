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

import grpc

from google.cloud.ndb import _eventloop

__all__ = [
    "add_flow_exception",
    "Future",
    "get_context",
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
    "TaskletFuture",
    "toplevel",
]


class Future:
    """Represents a task to be completed at an unspecified time in the future.

    This is the abstract base class from which all NDB ``Future`` classes are
    derived. A future represents a task that is to be performed
    asynchronously with the current flow of program control.

    Provides interface defined by :class:`concurrent.futures.Future` as well as
    that of the legacy Google App Engine NDB ``Future`` class.
    """

    def __init__(self):
        self._done = False
        self._result = None
        self._callbacks = []
        self._exception = None

    def done(self):
        """Get whether future has finished its task.

        Returns:
            bool: True if task has finished, False otherwise.
        """
        return self._done

    def running(self):
        """Get whether future's task is still running.

        Returns:
            bool: False if task has finished, True otherwise.
        """
        return not self._done

    def wait(self):
        """Wait for this future's task to complete.

        This future will be done and will have either a result or an exception
        after a call to this method.
        """
        while not self._done:
            _eventloop.run1()

    def check_success(self):
        """Check whether a future has completed without raising an exception.

        This will wait for the future to finish its task and will then raise
        the future's exception, if there is one, or else do nothing.
        """
        self.wait()

        if self._exception:
            raise self._exception

    def set_result(self, result):
        """Set the result for this future.

        Signals that this future has completed its task and sets the result.

        Should not be called from user code.
        """
        if self._done:
            raise RuntimeError("Cannot set result on future that is done.")

        self._result = result
        self._finish()

    def set_exception(self, exception):
        """Set an exception for this future.

        Signals that this future's task has resulted in an exception. The
        future is considered done but has no result. Once the exception is set,
        calls to :meth:`done` will return True, and calls to :meth:`result`
        will raise the exception.

        Should not be called from user code.

        Args:
            exception (Exception): The exception that was raised.
        """
        if self._done:
            raise RuntimeError("Cannot set exception on future that is done.")

        self._exception = exception
        self._finish()

    def _finish(self):
        """Wrap up future upon completion.

        Sets `_done` to True and calls any registered callbacks.
        """
        self._done = True

        for callback in self._callbacks:
            callback(self)

    def result(self):
        """Return the result of this future's task.

        If the task is finished, this will return immediately. Otherwise, this
        will block until a result is ready.

        Returns:
            Any: The result
        """
        self.check_success()
        return self._result

    get_result = result  # Legacy NDB interface

    def exception(self):
        """Get the exception for this future, if there is one.

        If the task has not yet finished, this will block until the task has
        finished. When the task has finished, this will get the exception
        raised during the task, or None, if no exception was raised.

        Returns:
            Union[Exception, None]: The exception, or None.
        """
        return self._exception

    get_exception = exception  # Legacy NDB interface

    def get_traceback(self):
        """Get the traceback for this future, if there is one.

        Included for backwards compatibility with legacy NDB. If there is an
        exception for this future, this just returns the ``__traceback__``
        attribute of that exception.

        Returns:
            Union[traceback, None]: The traceback, or None.
        """
        if self._exception:
            return self._exception.__traceback__

    def add_done_callback(self, callback):
        """Add a callback function to be run upon task completion.

        Args:
            callback (Callable): The function to execute.
        """
        self._callbacks.append(callback)

    def cancel(self):
        """Cancel the task for this future.

        Raises:
            NotImplementedError: Always, not supported.
        """
        raise NotImplementedError

    def cancelled(self):
        """Get whether task for this future has been cancelled.

        Returns:
            False: Always.
        """
        return False


class TaskletFuture(Future):
    """A future which waits on a tasklet.

    A future of this type wraps a generator derived from calling a tasklet. A
    tasklet's generator is expected to yield future objects, either an instance
    of :class:`ndb.Future` or :class:`grpc.Future'. The result of each yielded
    future is then sent back into the generator until the generator has
    completed and either returned a value or raised an exception.

    Args:
        Generator[Union[ndb.Future, grpc.Future], Any, Any]: The generator.
    """

    def __init__(self, generator):
        super(TaskletFuture, self).__init__()
        self.generator = generator

    def _advance_tasklet(self, send_value=None, error=None):
        """Advance a tasklet one step by sending in a value or error."""
        try:
            # Send the next value or exception into the generator
            if error:
                self.generator.throw(type(error), error)

            # send_value will be None if this is the first time
            yielded = self.generator.send(send_value)

        except StopIteration as stop:
            # Generator has signalled exit, get the return value. This tasklet
            # has finished.
            self.set_result(_get_return_value(stop))
            return

        except Exception as error:
            # An error has occurred in the tasklet. This tasklet has finished.
            self.set_exception(error)
            return

        # This tasklet has yielded a value. We expect this to be a future
        # object (either NDB or gRPC) or a sequence of futures, in the case of
        # parallel yield.

        def done_callback(yielded):
            # To be called when a dependent future has completed.
            # Advance the tasklet with the yielded value or error.
            error = yielded.exception()
            if error:
                self._advance_tasklet(error=error)
            else:
                self._advance_tasklet(yielded.result())

        if isinstance(yielded, Future):
            yielded.add_done_callback(done_callback)

        elif isinstance(yielded, grpc.Future):
            _eventloop.queue_rpc(yielded, done_callback)

        elif isinstance(yielded, (list, tuple)):
            raise NotImplementedError()

        else:
            raise RuntimeError(
                "A tasklet yielded an illegal value: {!r}".format(yielded)
            )


def _get_return_value(stop):
    """Inspect StopIteration instance for return value of tasklet.

    Args:
        stop (StopIteration): The StopIteration exception for the finished
            tasklet.
    """
    if len(stop.args) == 1:
        return stop.args[0]

    elif stop.args:
        return stop.args


def add_flow_exception(*args, **kwargs):
    raise NotImplementedError


def get_context(*args, **kwargs):
    raise NotImplementedError


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


def tasklet(*args, **kwargs):
    raise NotImplementedError


def toplevel(*args, **kwargs):
    raise NotImplementedError
