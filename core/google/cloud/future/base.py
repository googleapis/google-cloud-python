# Copyright 2017, Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstract and helper bases for Future implementations."""

import abc

import six

from google.cloud.future import _helpers


@six.add_metaclass(abc.ABCMeta)
class Future(object):
    # pylint: disable=missing-docstring, invalid-name
    # We inherit the interfaces here from concurrent.futures.

    """Future interface.

    This interface is based on :class:`concurrent.futures.Future`.
    """

    @abc.abstractmethod
    def cancel(self):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def cancelled(self):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def running(self):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def done(self):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def result(self, timeout=None):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def exception(self, timeout=None):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def add_done_callback(self, fn):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def set_result(self, result):  # pragma: NO COVER
        raise NotImplementedError()

    @abc.abstractmethod
    def set_exception(self, exception):  # pragma: NO COVER
        raise NotImplementedError()


class PollingFuture(Future):
    """A Future that needs to poll some service to check its status.

    The private :meth:`_blocking_poll` method should be implemented by
    subclasses.

    .. note: Privacy here is intended to prevent the final class from
    overexposing, not to prevent subclasses from accessing methods.
    """
    def __init__(self):
        super(PollingFuture, self).__init__()
        self._result = None
        self._exception = None
        self._result_set = False
        """bool: Set to True when the result has been set via set_result or
        set_exception."""
        self._polling_thread = None
        self._done_callbacks = []

    @abc.abstractmethod
    def _blocking_poll(self, timeout=None):  # pragma: NO COVER
        """Poll and wait for the Future to be resolved.

        Args:
            timeout (int): How long to wait for the operation to complete.
                If None, wait indefinitely.
        """
        raise NotImplementedError()

    def result(self, timeout=None):
        """Get the result of the operation, blocking if necessary.

        Args:
            timeout (int): How long to wait for the operation to complete.
                If None, wait indefinitely.

        Returns:
            google.protobuf.Message: The Operation's result.

        Raises:
            google.gax.GaxError: If the operation errors or if the timeout is
                reached before the operation completes.
        """
        self._blocking_poll()

        if self._exception is not None:
            # pylint: disable=raising-bad-type
            # Pylint doesn't recognize that this is valid in this case.
            raise self._exception

        return self._result

    def exception(self, timeout=None):
        """Get the exception from the operation, blocking if necessary.

        Args:
            timeout (int): How long to wait for the operation to complete.
                If None, wait indefinitely.

        Returns:
            Optional[google.gax.GaxError]: The operation's error.
        """
        self._blocking_poll()
        return self._exception

    def add_done_callback(self, fn):
        """Add a callback to be executed when the operation is complete.

        If the operation is not already complete, this will start a helper
        thread to poll for the status of the operation in the background.

        Args:
            fn (Callable[Future]): The callback to execute when the operation
                is complete.
        """
        if self._result_set:
            _helpers.safe_invoke_callback(fn, self)
            return

        self._done_callbacks.append(fn)

        if self._polling_thread is None:
            # The polling thread will exit on its own as soon as the operation
            # is done.
            self._polling_thread = _helpers.start_daemon_thread(
                target=self._blocking_poll)

    def _invoke_callbacks(self, *args, **kwargs):
        """Invoke all done callbacks."""
        for callback in self._done_callbacks:
            _helpers.safe_invoke_callback(callback, *args, **kwargs)

    def set_result(self, result):
        """Set the Future's result."""
        self._result = result
        self._result_set = True
        self._invoke_callbacks(self)

    def set_exception(self, exception):
        """Set the Future's exception."""
        self._exception = exception
        self._result_set = True
        self._invoke_callbacks(self)
