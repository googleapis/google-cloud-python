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
import types

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _eventloop
from google.cloud.ndb import _remote

__all__ = [
    "add_flow_exception",
    "Future",
    "make_context",
    "make_default_context",
    "QueueFuture",
    "ReducingFuture",
    "Return",
    "SerialQueueFuture",
    "set_context",
    "sleep",
    "synctasklet",
    "tasklet",
    "toplevel",
    "wait_all",
    "wait_any",
]


class Future:
    """Represents a task to be completed at an unspecified time in the future.

    This is the abstract base class from which all NDB ``Future`` classes are
    derived. A future represents a task that is to be performed
    asynchronously with the current flow of program control.

    Provides interface defined by :class:`concurrent.futures.Future` as well as
    that of the legacy Google App Engine NDB ``Future`` class.
    """

    def __init__(self, info="Unknown"):
        self.info = info
        self._done = False
        self._result = None
        self._callbacks = []
        self._exception = None

    def __repr__(self):
        return "{}({!r}) <{}>".format(type(self).__name__, self.info, id(self))

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
            Union[types.TracebackType, None]: The traceback, or None.
        """
        if self._exception:
            return self._exception.__traceback__

    def add_done_callback(self, callback):
        """Add a callback function to be run upon task completion. Will run
        immediately if task has already finished.

        Args:
            callback (Callable): The function to execute.
        """
        if self._done:
            callback(self)
        else:
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
            :data:`False`: Always.
        """
        return False

    @staticmethod
    def wait_any(futures):
        """Calls :func:`wait_any`."""
        # For backwards compatibility
        return wait_any(futures)

    @staticmethod
    def wait_all(futures):
        """Calls :func:`wait_all`."""
        # For backwards compatibility
        return wait_all(futures)


class _TaskletFuture(Future):
    """A future which waits on a tasklet.

    A future of this type wraps a generator derived from calling a tasklet. A
    tasklet's generator is expected to yield future objects, either an instance
    of :class:`Future` or :class:`_remote.RemoteCall`. The result of each
    yielded future is then sent back into the generator until the generator has
    completed and either returned a value or raised an exception.

    Args:
        typing.Generator[Union[tasklets.Future, _remote.RemoteCall], Any, Any]:
            The generator.
    """

    def __init__(self, generator, context, info="Unknown"):
        super(_TaskletFuture, self).__init__(info=info)
        self.generator = generator
        self.context = context

    def _advance_tasklet(self, send_value=None, error=None):
        """Advance a tasklet one step by sending in a value or error."""
        try:
            with self.context.use():
                # Send the next value or exception into the generator
                if error:
                    self.generator.throw(type(error), error)

                # send_value will be None if this is the first time
                yielded = self.generator.send(send_value)

                # Context may have changed in tasklet
                self.context = context_module.get_context()

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
            # To be called when a future dependency has completed.  Advance the
            # tasklet with the yielded value or error.
            #
            # It was tempting to call `_advance_tasklet` (`_help_tasklet_along`
            # in Legacy) directly. Doing so, it has been found, can lead to
            # exceeding the maximum recursion depth. Queing it up to run on the
            # event loop avoids this issue by keeping the call stack shallow.
            error = yielded.exception()
            if error:
                _eventloop.call_soon(self._advance_tasklet, error=error)
            else:
                _eventloop.call_soon(self._advance_tasklet, yielded.result())

        if isinstance(yielded, Future):
            yielded.add_done_callback(done_callback)

        elif isinstance(yielded, _remote.RemoteCall):
            _eventloop.queue_rpc(yielded, done_callback)

        elif isinstance(yielded, (list, tuple)):
            future = _MultiFuture(yielded)
            future.add_done_callback(done_callback)

        else:
            raise RuntimeError(
                "A tasklet yielded an illegal value: {!r}".format(yielded)
            )


def _get_return_value(stop):
    """Inspect `StopIteration` instance for return value of tasklet.

    Args:
        stop (StopIteration): The `StopIteration` exception for the finished
            tasklet.
    """
    if len(stop.args) == 1:
        return stop.args[0]

    elif stop.args:
        return stop.args


class _MultiFuture(Future):
    """A future which depends on multiple other futures.

    This future will be done when either all dependencies have results or when
    one dependency has raised an exception.

    Args:
        dependencies (typing.Sequence[tasklets.Future]): A sequence of the
            futures this future depends on.
    """

    def __init__(self, dependencies):
        super(_MultiFuture, self).__init__()
        self._dependencies = dependencies

        for dependency in dependencies:
            dependency.add_done_callback(self._dependency_done)

    def __repr__(self):
        return "{}({}) <{}>".format(
            type(self).__name__,
            ", ".join(map(repr, self._dependencies)),
            id(self),
        )

    def _dependency_done(self, dependency):
        if self._done:
            return

        error = dependency.exception()
        if error is not None:
            self.set_exception(error)
            return

        all_done = all((future.done() for future in self._dependencies))
        if all_done:
            result = tuple((future.result() for future in self._dependencies))
            self.set_result(result)


def tasklet(wrapped):
    """
    A decorator to turn a function or method into a tasklet.

    Calling a tasklet will return a :class:`~Future` instance which can be used
    to get the eventual return value of the tasklet.

    For more information on tasklets and cooperative multitasking, see the main
    documentation.

    Args:
        wrapped (Callable): The wrapped function.
    """

    @functools.wraps(wrapped)
    def tasklet_wrapper(*args, **kwargs):
        # The normal case is that the wrapped function is a generator function
        # that returns a generator when called. We also support the case that
        # the user has wrapped a regular function with the tasklet decorator.
        # In this case, we fail to realize an actual tasklet, but we go ahead
        # and create a future object and set the result to the function's
        # return value so that from the user perspective there is no problem.
        # This permissive behavior is inherited from legacy NDB.
        context = context_module.get_context()

        try:
            returned = wrapped(*args, **kwargs)
        except StopIteration as stop:
            # If wrapped  is a regular function and the function uses the
            # deprecated "raise Return(result)" pattern rather than just
            # returning the result, then we'll extract the result from the
            # StopIteration exception.
            returned = _get_return_value(stop)

        if isinstance(returned, types.GeneratorType):
            # We have a tasklet, start it
            future = _TaskletFuture(returned, context, info=wrapped.__name__)
            future._advance_tasklet()

        else:
            # We don't have a tasklet, but we fake it anyway
            future = Future(info=wrapped.__name__)
            future.set_result(returned)

        return future

    return tasklet_wrapper


def wait_any(futures):
    """Wait for any of several futures to finish.

    Args:
        futures (typing.Sequence[Future]): The futures to wait on.

    Returns:
        Future: The first future to be found to have finished.
    """
    if not futures:
        return None

    while True:
        for future in futures:
            if future.done():
                return future

        _eventloop.run1()


def wait_all(futures):
    """Wait for all of several futures to finish.

    Args:
        futures (typing.Sequence[Future]): The futures to wait on.
    """
    if not futures:
        return

    for future in futures:
        future.wait()


class Return(StopIteration):
    """Alias for `StopIteration`.

    Older programs written with NDB may ``raise Return(result)`` in a tasklet.
    This is no longer necessary, but it is included for backwards
    compatibility. Tasklets should simply ``return`` their result.
    """

    # For reasons I don't entirely understand, Sphinx pukes if we just assign:
    # Return = StopIteration


def sleep(seconds):
    """Sleep some amount of time in a tasklet.
    Example:
        ..code-block:: python
            yield tasklets.sleep(0.5)  # Sleep for half a second.
    Arguments:
        seconds (float): Amount of time, in seconds, to sleep.
    Returns:
        Future: Future will be complete after ``seconds`` have elapsed.
    """
    future = Future(info="sleep({})".format(seconds))
    _eventloop.queue_call(seconds, future.set_result, None)
    return future


def add_flow_exception(*args, **kwargs):
    raise NotImplementedError


def make_context(*args, **kwargs):
    raise NotImplementedError


def make_default_context(*args, **kwargs):
    raise NotImplementedError


class QueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ReducingFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class SerialQueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def set_context(*args, **kwargs):
    raise NotImplementedError


def synctasklet(*args, **kwargs):
    raise NotImplementedError


def toplevel(*args, **kwargs):
    raise NotImplementedError
