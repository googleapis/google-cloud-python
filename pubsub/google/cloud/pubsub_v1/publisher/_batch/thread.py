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

import logging
import threading
import time

import six

import google.api_core.exceptions
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher import futures
from google.cloud.pubsub_v1.publisher._batch import base


_LOGGER = logging.getLogger(__name__)
_CAN_COMMIT = (base.BatchStatus.ACCEPTING_MESSAGES, base.BatchStatus.STARTING)
_SERVER_PUBLISH_MAX_BYTES = 10 * 1000 * 1000  # max accepted size of PublishRequest


class Batch(base.Batch):
    """A batch of messages.

    The batch is the internal group of messages which are either awaiting
    publication or currently in progress.

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
        self._topic = topic
        self._settings = settings

        self._state_lock = threading.Lock()
        # These members are all communicated between threads; ensure that
        # any writes to them use the "state lock" to remain atomic.
        # _futures list should remain unchanged after batch
        # status changed from ACCEPTING_MESSAGES to any other
        # in order to avoid race conditions
        self._futures = []
        self._messages = []
        self._status = base.BatchStatus.ACCEPTING_MESSAGES

        # The initial size is not zero, we need to account for the size overhead
        # of the PublishRequest message itself.
        self._base_request_size = types.PublishRequest(topic=topic).ByteSize()
        self._size = self._base_request_size

        # If max latency is specified, start a thread to monitor the batch and
        # commit when the max latency is reached.
        self._thread = None
        if autocommit and self.settings.max_latency < float("inf"):
            self._thread = threading.Thread(
                name="Thread-MonitorBatchPublisher", target=self.monitor
            )
            self._thread.start()

    @staticmethod
    def make_lock():
        """Return a threading lock.

        Returns:
            _thread.Lock: A newly created lock.
        """
        return threading.Lock()

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

        The size includes any overhead of the actual ``PublishRequest`` that is
        sent to the backend.

        Returns:
            int: The total size of all of the messages currently
                 in the batch (including the request overhead), in bytes.
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

        .. note::

            This method is non-blocking. It opens a new thread, which calls
            :meth:`_commit`, which does block.

        This synchronously sets the batch status to "starting", and then opens
        a new thread, which handles actually sending the messages to Pub/Sub.

        If the current batch is **not** accepting messages, this method
        does nothing.
        """
        # Set the status to "starting" synchronously, to ensure that
        # this batch will necessarily not accept new messages.
        with self._state_lock:
            if self._status == base.BatchStatus.ACCEPTING_MESSAGES:
                self._status = base.BatchStatus.STARTING
            else:
                return

        # Start a new thread to actually handle the commit.
        commit_thread = threading.Thread(
            name="Thread-CommitBatchPublisher", target=self._commit
        )
        commit_thread.start()

    def _commit(self):
        """Actually publish all of the messages on the active batch.

        This moves the batch out from being the active batch to an in progress
        batch on the publisher, and then the batch is discarded upon
        completion.

        .. note::

            This method blocks. The :meth:`commit` method is the non-blocking
            version, which calls this one.
        """
        with self._state_lock:
            if self._status in _CAN_COMMIT:
                self._status = base.BatchStatus.IN_PROGRESS
            else:
                # If, in the intervening period between when this method was
                # called and now, the batch started to be committed, or
                # completed a commit, then no-op at this point.
                _LOGGER.debug("Batch is already in progress, exiting commit")
                return

        # Once in the IN_PROGRESS state, no other thread can publish additional
        # messages or initiate a commit (those operations become a no-op), thus
        # it is safe to release the state lock here. Releasing the lock avoids
        # blocking other threads in case api.publish() below takes a long time
        # to complete.
        # https://github.com/googleapis/google-cloud-python/issues/8036

        # Sanity check: If there are no messages, no-op.
        if not self._messages:
            _LOGGER.debug("No messages to publish, exiting commit")
            self._status = base.BatchStatus.SUCCESS
            return

        # Begin the request to publish these messages.
        # Log how long the underlying request takes.
        start = time.time()

        try:
            response = self._client.api.publish(self._topic, self._messages)
        except google.api_core.exceptions.GoogleAPIError as exc:
            # We failed to publish, set the exception on all futures and
            # exit.
            self._status = base.BatchStatus.ERROR

            for future in self._futures:
                future.set_exception(exc)

            _LOGGER.exception("Failed to publish %s messages.", len(self._futures))
            return

        end = time.time()
        _LOGGER.debug("gRPC Publish took %s seconds.", end - start)

        if len(response.message_ids) == len(self._futures):
            # Iterate over the futures on the queue and return the response
            # IDs. We are trusting that there is a 1:1 mapping, and raise
            # an exception if not.
            self._status = base.BatchStatus.SUCCESS
            zip_iter = six.moves.zip(response.message_ids, self._futures)
            for message_id, future in zip_iter:
                future.set_result(message_id)
        else:
            # Sanity check: If the number of message IDs is not equal to
            # the number of futures I have, then something went wrong.
            self._status = base.BatchStatus.ERROR
            exception = exceptions.PublishError(
                "Some messages were not successfully published."
            )

            for future in self._futures:
                future.set_exception(exception)

            _LOGGER.error(
                "Only %s of %s messages were published.",
                len(response.message_ids),
                len(self._futures),
            )

    def monitor(self):
        """Commit this batch after sufficient time has elapsed.

        This simply sleeps for ``self.settings.max_latency`` seconds,
        and then calls commit unless the batch has already been committed.
        """
        # NOTE: This blocks; it is up to the calling code to call it
        #       in a separate thread.

        # Sleep for however long we should be waiting.
        time.sleep(self.settings.max_latency)

        _LOGGER.debug("Monitor is waking up")
        return self._commit()

    def publish(self, message):
        """Publish a single message.

        Add the given message to this object; this will cause it to be
        published once the batch either has enough messages or a sufficient
        period of time has elapsed. If the batch is full or the commit is
        already in progress, the method does not do anything.

        This method is called by :meth:`~.PublisherClient.publish`.

        Args:
            message (~.pubsub_v1.types.PubsubMessage): The Pub/Sub message.

        Returns:
            Optional[~google.api_core.future.Future]: An object conforming to
            the :class:`~concurrent.futures.Future` interface or :data:`None`.
            If :data:`None` is returned, that signals that the batch cannot
            accept a message.

        Raises:
            pubsub_v1.publisher.exceptions.MessageTooLargeError: If publishing
                the ``message`` would exceed the max size limit on the backend.
        """
        # Coerce the type, just in case.
        if not isinstance(message, types.PubsubMessage):
            message = types.PubsubMessage(**message)

        future = None

        with self._state_lock:
            if not self.will_accept(message):
                return future

            size_increase = types.PublishRequest(messages=[message]).ByteSize()

            if (self._base_request_size + size_increase) > _SERVER_PUBLISH_MAX_BYTES:
                err_msg = (
                    "The message being published would produce too large a publish "
                    "request that would exceed the maximum allowed size on the "
                    "backend ({} bytes).".format(_SERVER_PUBLISH_MAX_BYTES)
                )
                raise exceptions.MessageTooLargeError(err_msg)

            new_size = self._size + size_increase
            new_count = len(self._messages) + 1

            size_limit = min(self.settings.max_bytes, _SERVER_PUBLISH_MAX_BYTES)
            overflow = new_size > size_limit or new_count >= self.settings.max_messages

            if not self._messages or not overflow:

                # Store the actual message in the batch's message queue.
                self._messages.append(message)
                self._size = new_size

                # Track the future on this batch (so that the result of the
                # future can be set).
                future = futures.Future(completed=threading.Event())
                self._futures.append(future)

        # Try to commit, but it must be **without** the lock held, since
        # ``commit()`` will try to obtain the lock.
        if overflow:
            self.commit()

        return future
