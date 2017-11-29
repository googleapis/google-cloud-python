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

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher import futures
from google.cloud.pubsub_v1.publisher.batch import base


_LOGGER = logging.getLogger(__name__)


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
        self._status = base.BatchStatus.ACCEPTING_MESSAGES
        self._topic = topic

        # If max latency is specified, start a thread to monitor the batch and
        # commit when the max latency is reached.
        self._thread = None
        self._commit_lock = threading.Lock()
        if autocommit and self._settings.max_latency < float('inf'):
            self._thread = threading.Thread(
                name='Thread-MonitorBatchPublisher',
                target=self.monitor,
            )
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
        commit_thread = threading.Thread(
            name='Thread-CommitBatchPublisher',
            target=self._commit,
        )
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
        with self._commit_lock:
            # If, in the intervening period, the batch started to be committed,
            # or completed a commit, then no-op at this point.
            if self._status != base.BatchStatus.ACCEPTING_MESSAGES:
                return

            # Update the status.
            self._status = 'in-flight'

            # Sanity check: If there are no messages, no-op.
            if not self._messages:
                return

            # Begin the request to publish these messages.
            # Log how long the underlying request takes.
            start = time.time()
            response = self.client.api.publish(
                self._topic,
                self.messages,
            )
            end = time.time()
            _LOGGER.debug('gRPC Publish took {s} seconds.'.format(
                s=end - start,
            ))

            # We got a response from Pub/Sub; denote that we are processing.
            self._status = 'processing results'

            # Sanity check: If the number of message IDs is not equal to the
            # number of futures I have, then something went wrong.
            if len(response.message_ids) != len(self._futures):
                for future in self._futures:
                    future.set_exception(exceptions.PublishError(
                        'Some messages were not successfully published.',
                    ))
                return

            # Iterate over the futures on the queue and return the response
            # IDs. We are trusting that there is a 1:1 mapping, and raise an
            # exception if not.
            self._status = base.BatchStatus.SUCCESS
            for message_id, future in zip(response.message_ids, self._futures):
                future.set_result(message_id)

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
            ~google.api_core.future.Future: An object conforming to
                the :class:`concurrent.futures.Future` interface.
        """
        # Coerce the type, just in case.
        if not isinstance(message, types.PubsubMessage):
            message = types.PubsubMessage(**message)

        # Add the size to the running total of the size, so we know
        # if future messages need to be rejected.
        self._size += message.ByteSize()

        # Store the actual message in the batch's message queue.
        self._messages.append(message)
        if len(self._messages) >= self.settings.max_messages:
            self.commit()

        # Return a Future. That future needs to be aware of the status
        # of this batch.
        f = futures.Future()
        self._futures.append(f)
        return f
