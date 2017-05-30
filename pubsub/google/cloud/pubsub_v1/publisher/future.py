# Copyright 2017, Google Inc. All rights reserved.
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

import queue
import uuid


class Future(object):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from asychronous Pub/Sub calls, and is the
    interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        batch (:class:~`pubsub_v1.batch.Batch`): The batch object that
            is committing this message.
        client_id (str): The client ID of the message.
    """
    def __init__(self, batch, client_id):
        self._batch = batch
        self._hash = hash(uuid.uuid4())
        self._callbacks = queue.Queue()

    def __hash__(self):
        return self._hash

    def cancel(self):
        """Publishes in Pub/Sub currently may not be canceled.

        This method always returns False.
        """
        return False

    def cancelled(self):
        """Publishes in Pub/Sub currently may not be canceled.

        This method always returns False.
        """
        return False

    def running(self):
        """Publishes in Pub/Sub currently may not be canceled.

        This method always returns True.
        """
        return True

    def done(self):
        """Return True if the publish has completed, False otherwise.

        This still returns True in failure cases; checking `result` or
        `exception` is the canonical way to assess success or failure.
        """
        return self.batch.status in ('success', 'error')

    def result(self, timeout=None):
        """Return the message ID, or raise an exception.

        This blocks until the message has successfully been published, and
        returns the message ID.

        Args:
            timeout (int|float): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            :class:~`pubsub_v1.TimeoutError`: If the request times out.
            :class:~`Exception`: For undefined exceptions in the underlying
                call execution.
        """
        # Attempt to get the exception if there is one.
        # If there is not one, then we know everything worked, and we can
        # return an appropriate value.
        err = self.exception(timeout=timeout)
        if err is None:
            return self.batch.get_message_id(self._client_id)
        raise err

    def exception(self, timeout=None, _wait=1):
        """Return the exception raised by the call, if any.

        This blocks until the message has successfully been published, and
        returns the exception. If the call succeeded, return None.

        Args:
            timeout (int|float): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            :class:~`pubsub_v1.TimeoutError`: If the request times out.

        Returns:
            :class:`Exception`: The exception raised by the call, if any.
        """
        # If the batch completed successfully, this should return None.
        if self.batch.status == 'success':
            return None

        # If this batch had an error, this should return it.
        if self.batch.status == 'error':
            return self.batch._error

        # If the timeout has been exceeded, raise TimeoutError.
        if timeout < 0:
            raise TimeoutError('Timed out waiting for an exception.')

        # Wait a little while and try again.
        time.sleep(_wait)
        return self.exception(
            timeout=timeout - _wait,
            _wait=min(_wait * 2, 60),
        )

    def add_done_callback(self, fn):
        """Attach the provided callable to the future.

        The provided function is called, with this future as its only argument,
        when the future finishes running.
        """
        if self.done():
            fn(self)
        self._callbacks.put(fn)

    def _trigger(self):
        """Trigger all callbacks registered to this Future.

        This method is called internally by the batch once the batch
        completes.

        Args:
            message_id (str): The message ID, as a string.
        """
        try:
            while True:
                callback = self._callbacks.get(block=False)
                callback(self)
        except queue.Empty:
            return None


class TimeoutError(object):
    """Exception subclass for timeout-related errors.

    This exception is only returned by the :class:~`pubsub_v1.future.Future`
    class.
    """
    pass
