# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

import threading
import uuid

import google.api_core.future
from google.cloud.pubsub_v1.publisher import exceptions


class Future(google.api_core.future.Future):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from asychronous Pub/Sub calls, and is the
    interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        completed (Optional[Any]): An event, with the same interface as
            :class:`threading.Event`. This is provided so that callers
            with different concurrency models (e.g. ``threading`` or
            ``multiprocessing``) can supply an event that is compatible
            with that model. The ``wait()`` and ``set()`` methods will be
            used. If this argument is not provided, then a new
            :class:`threading.Event` will be created and used.
    """

    # This could be a sentinel object or None, but the sentinel object's ID
    # can change if the process is forked, and None has the possibility of
    # actually being a result.
    _SENTINEL = uuid.uuid4()

    def __init__(self, completed=None):
        self._result = self._SENTINEL
        self._exception = self._SENTINEL
        self._callbacks = []
        if completed is None:
            completed = threading.Event()
        self._completed = completed

    def cancel(self):
        """Actions in Pub/Sub generally may not be canceled.

        This method always returns False.
        """
        return False

    def cancelled(self):
        """Actions in Pub/Sub generally may not be canceled.

        This method always returns False.
        """
        return False

    def running(self):
        """Actions in Pub/Sub generally may not be canceled.

        Returns:
            bool: ``True`` if this method has not yet completed, or
                ``False`` if it has completed.
        """
        return not self.done()

    def done(self):
        """Return True the future is done, False otherwise.

        This still returns True in failure cases; checking :meth:`result` or
        :meth:`exception` is the canonical way to assess success or failure.
        """
        return self._exception != self._SENTINEL or self._result != self._SENTINEL

    def result(self, timeout=None):
        """Resolve the future and return a value where appropriate.

        Args:
            timeout (Union[int, float]): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            concurrent.futures.TimeoutError: If the request times out.
            Exception: For undefined exceptions in the underlying
                call execution.
        """
        # Attempt to get the exception if there is one.
        # If there is not one, then we know everything worked, and we can
        # return an appropriate value.
        err = self.exception(timeout=timeout)
        if err is None:
            return self._result
        raise err

    def exception(self, timeout=None):
        """Return the exception raised by the call, if any.

        Args:
            timeout (Union[int, float]): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            concurrent.futures.TimeoutError: If the request times out.

        Returns:
            Exception: The exception raised by the call, if any.
        """
        # Wait until the future is done.
        if not self._completed.wait(timeout=timeout):
            raise exceptions.TimeoutError("Timed out waiting for result.")

        # If the batch completed successfully, this should return None.
        if self._result != self._SENTINEL:
            return None

        # Okay, this batch had an error; this should return it.
        return self._exception

    def add_done_callback(self, callback):
        """Attach the provided callable to the future.

        The provided function is called, with this future as its only argument,
        when the future finishes running.

        Args:
            callback (Callable): The function to call.

        Returns:
            None
        """
        if self.done():
            return callback(self)
        self._callbacks.append(callback)

    def set_result(self, result):
        """Set the result of the future to the provided result.

        Args:
            result (Any): The result
        """
        # Sanity check: A future can only complete once.
        if self.done():
            raise RuntimeError("set_result can only be called once.")

        # Set the result and trigger the future.
        self._result = result
        self._trigger()

    def set_exception(self, exception):
        """Set the result of the future to the given exception.

        Args:
            exception (:exc:`Exception`): The exception raised.
        """
        # Sanity check: A future can only complete once.
        if self.done():
            raise RuntimeError("set_exception can only be called once.")

        # Set the exception and trigger the future.
        self._exception = exception
        self._trigger()

    def _trigger(self):
        """Trigger all callbacks registered to this Future.

        This method is called internally by the batch once the batch
        completes.

        Args:
            message_id (str): The message ID, as a string.
        """
        self._completed.set()
        for callback in self._callbacks:
            callback(self)
