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

import threading
import time
import uuid

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher.batch import base


class Batch(base.Batch):
    """A batch of messages.

    The batch is the internal group of messages which are either awaiting
    publication or currently in-flight.

    A batch is automatically created by the PublisherClient when the first
    message to be published is received; subsequent messages are added to
    that batch until the process of actual publishing _starts_.

    Once this occurs, any new messages sent to :meth:`publish` open a new
    batch.

    If you are using this library, you most likely do not need to instantiate
    batch objects directly; they will be created for you. If you want to
    change the actual batching settings, see the ``batching`` argument on
    :class:`~.pubsub_v1.PublisherClient`.

    Any properties or methods on this class which are not defined in
    :class:`~.pubsub_v1.publisher.batch.BaseBatch` should be considered
    implementation details.

    Args:
        client (~.pubsub_v1.PublisherClient): The publisher client used to
            create this batch.
        topic (str): The topic. The format for this is
            ``projects/{project}/topics/{topic}``.
        settings (~.pubsub_v1.types.BatchSettings): The settings for batch
            publishing. These should be considered immutable once the batch
            has been opened.
        autocommit (bool): Whether to autocommit the batch when the time
            has elapsed. Defaults to True unless ``settings.max_latency`` is
            inf.
    """
    def __init__(self, client, topic, settings, autocommit=True):
        self._client = client

        # These objects are all communicated between threads; ensure that
        # any writes to them are atomic.
        self._futures = []
        self._messages = []
        self._size = 0
        self._settings = settings
        self._status = self.Status.ACCEPTING_MESSAGES
        self._topic = topic
        self.message_ids = {}

        # If max latency is specified, start a thread to monitor the batch and
        # commit when the max latency is reached.
        self._thread = None
        if autocommit and self._settings.max_latency < float('inf'):
            self._thread = threading.Thread(target=self.monitor)
            self._thread.start()

    @property
    def client(self):
        """~.pubsub_v1.client.PublisherClient: A publisher client."""
        return self._client

    @property
    def messages(self):
        """Sequence: The messages currently in the batch."""
        return self._messages

    @property
    def settings(self):
        """Return the batch settings.

        Returns:
            ~.pubsub_v1.types.BatchSettings: The batch settings. These are
                considered immutable once the batch has been opened.
        """
        return self._settings

    @property
    def size(self):
        """Return the total size of all of the messages currently in the batch.

        Returns:
            int: The total size of all of the messages currently
                 in the batch, in bytes.
        """
        return self._size

    @property
    def status(self):
        """Return the status of this batch.

        Returns:
            str: The status of this batch. All statuses are human-readable,
                all-lowercase strings.
        """
        return self._status

    def commit(self):
        """Actually publish all of the messages on the active batch.

        This synchronously sets the batch status to in-flight, and then opens
        a new thread, which handles actually sending the messages to Pub/Sub.

        .. note::

            This method is non-blocking. It opens a new thread, which calls
            :meth:`_commit`, which does block.
        """
        # Set the status to in-flight synchronously, to ensure that
        # this batch will necessarily not accept new messages.
        #
        # Yes, this is repeated in `_commit`, because that method is called
        # directly by `monitor`.
        self._status = 'in-flight'

        # Start a new thread to actually handle the commit.
        commit_thread = threading.Thread(target=self._commit)
        commit_thread.start()

    def _commit(self):
        """Actually publish all of the messages on the active batch.

        This moves the batch out from being the active batch to an in-flight
        batch on the publisher, and then the batch is discarded upon
        completion.

        .. note::

            This method blocks. The :meth:`commit` method is the non-blocking
            version, which calls this one.
        """
        # Update the status.
        self._status = 'in-flight'

        # Sanity check: If there are no messages, no-op.
        if len(self._messages) == 0:
            return

        # Begin the request to publish these messages.
        response = self.client.api.publish(
            self._topic,
            self.messages,
        )

        # We got a response from Pub/Sub; denote that we are processing.
        self._status = 'processing results'

        # Sanity check: If the number of message IDs is not equal to the
        # number of futures I have, then something went wrong.
        if len(response.message_ids) != len(self._futures):
            raise exceptions.PublishError(
                'Some messages were not successfully published.',
            )

        # Iterate over the futures on the queue and return the response IDs.
        # We are trusting that there is a 1:1 mapping, and raise an exception
        # if not.
        self._status = self.Status.SUCCESS
        for message_id, future in zip(response.message_ids, self._futures):
            self.message_ids[hash(future)] = message_id
            future._trigger()

    def monitor(self):
        """Commit this batch after sufficient time has elapsed.

        This simply sleeps for ``self._settings.max_latency`` seconds,
        and then calls commit unless the batch has already been committed.
        """
        # Note: This thread blocks; it is up to the calling code to call it
        # in a separate thread.
        #
        # Sleep for however long we should be waiting.
        time.sleep(self._settings.max_latency)

        # If, in the intervening period, the batch started to be committed,
        # then no-op at this point.
        if self._status != self.Status.ACCEPTING_MESSAGES:
            return

        # Commit.
        return self._commit()

    def publish(self, message):
        """Publish a single message.

        Add the given message to this object; this will cause it to be
        published once the batch either has enough messages or a sufficient
        period of time has elapsed.

        This method is called by :meth:`~.PublisherClient.publish`.

        Args:
            message (~.pubsub_v1.types.PubsubMessage): The Pub/Sub message.

        Returns:
            ~.pubsub_v1.publisher.batch.mp.Future: An object conforming to the
                :class:`concurrent.futures.Future` interface.
        """
        # Coerce the type, just in case.
        if not isinstance(message, types.PubsubMessage):
            message = types.PubsubMessage(**message)

        # Add the size to the running total of the size, so we know
        # if future messages need to be rejected.
        self._size += message.ByteSize()

        # Store the actual message in the batch's message queue.
        self._messages.append(message)

        # Return a Future. That future needs to be aware of the status
        # of this batch.
        f = Future(self)
        self._futures.append(f)
        return f


class Future(object):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from asychronous Pub/Sub calls, and is the
    interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        batch (`~.Batch`): The batch object that is committing
            this message.
    """
    def __init__(self, batch):
        self._batch = batch
        self._callbacks = []
        self._hash = hash(uuid.uuid4())

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

        This still returns True in failure cases; checking :meth:`result` or
        :meth:`exception` is the canonical way to assess success or failure.
        """
        return self._batch.status in (
            self._batch.Status.SUCCESS,
            self._batch.Status.ERROR,
        )

    def result(self, timeout=None):
        """Return the message ID, or raise an exception.

        This blocks until the message has successfully been published, and
        returns the message ID.

        Args:
            timeout (int|float): The number of seconds before this call
                times out and raises TimeoutError.

        Returns:
            str: The message ID.

        Raises:
            ~.pubsub_v1.TimeoutError: If the request times out.
            Exception: For undefined exceptions in the underlying
                call execution.
        """
        # Attempt to get the exception if there is one.
        # If there is not one, then we know everything worked, and we can
        # return an appropriate value.
        err = self.exception(timeout=timeout)
        if err is None:
            return self._batch.message_ids[hash(self)]
        raise err

    def exception(self, timeout=None, _wait=1):
        """Return the exception raised by the call, if any.

        This blocks until the message has successfully been published, and
        returns the exception. If the call succeeded, return None.

        Args:
            timeout (int|float): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            TimeoutError: If the request times out.

        Returns:
            Exception: The exception raised by the call, if any.
        """
        # If no timeout was specified, use inf.
        if timeout is None:
            timeout = float('inf')

        # If the batch completed successfully, this should return None.
        if self._batch.status == 'success':
            return None

        # If this batch had an error, this should return it.
        if self._batch.status == 'error':
            return self._batch.error

        # If the timeout has been exceeded, raise TimeoutError.
        if timeout <= 0:
            raise exceptions.TimeoutError('Timed out waiting for exception.')

        # Wait a little while and try again.
        time.sleep(_wait)
        return self.exception(
            timeout=timeout - _wait,
            _wait=min(_wait * 2, timeout, 60),
        )

    def add_done_callback(self, fn):
        """Attach the provided callable to the future.

        The provided function is called, with this future as its only argument,
        when the future finishes running.
        """
        if self.done():
            fn(self)
        self._callbacks.append(fn)

    def _trigger(self):
        """Trigger all callbacks registered to this Future.

        This method is called internally by the batch once the batch
        completes.

        Args:
            message_id (str): The message ID, as a string.
        """
        for callback in self._callbacks:
            callback(self)
