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

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Batch(object):
    """The base batching class for Pub/Sub publishing.

    Although the :class:`~.pubsub_v1.publisher.batch.thread.Batch` class, based
    on :class:`threading.Thread`, is fine for most cases, advanced
    users may need to implement something based on a different concurrency
    model.

    This class defines the interface for the Batch implementation;
    subclasses may be passed as the ``batch_class`` argument to
    :class:`~.pubsub_v1.client.PublisherClient`.

    The batching behavior works like this: When the
    :class:`~.pubsub_v1.publisher.client.Client` is asked to publish a new
    message, it requires a batch. The client will see if there is an
    already-opened batch for the given topic; if there is, then the message
    is sent to that batch. If there is not, then a new batch is created
    and the message put there.

    When a new batch is created, it automatically starts a timer counting
    down to the maximum latency before the batch should commit.
    Essentially, if enough time passes, the batch automatically commits
    regardless of how much is in it. However, if either the message count or
    size thresholds are encountered first, then the batch will commit early.
    """
    def __len__(self):
        """Return the number of messages currently in the batch."""
        return len(self.messages)

    @staticmethod
    @abc.abstractmethod
    def make_lock():
        """Return a lock in the chosen concurrency model.

        Returns:
            ContextManager: A newly created lock.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def messages(self):
        """Return the messages currently in the batch.

        Returns:
            Sequence: The messages currently in the batch.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def size(self):
        """Return the total size of all of the messages currently in the batch.

        Returns:
            int: The total size of all of the messages currently
                 in the batch, in bytes.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def settings(self):
        """Return the batch settings.

        Returns:
            ~.pubsub_v1.types.BatchSettings: The batch settings. These are
                considered immutable once the batch has been opened.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def status(self):
        """Return the status of this batch.

        Returns:
            str: The status of this batch. All statuses are human-readable,
                all-lowercase strings. The ones represented in the
                :class:`BaseBatch.Status` enum are special, but other statuses
                are permitted.
        """
        raise NotImplementedError

    def will_accept(self, message):
        """Return True if the batch is able to accept the message.

        In concurrent implementations, the attributes on the current batch
        may be modified by other workers. With this in mind, the caller will
        likely want to hold a lock that will make sure the state remains
        the same after the "will accept?" question is answered.

        Args:
            message (~.pubsub_v1.types.PubsubMessage): The Pub/Sub message.

        Returns:
            bool: Whether this batch can accept the message.
        """
        # If this batch is not accepting messages generally, return False.
        if self.status != BatchStatus.ACCEPTING_MESSAGES:
            return False

        # If this message will make the batch exceed the ``max_bytes``
        # setting, return False.
        if self.size + message.ByteSize() > self.settings.max_bytes:
            return False

        # If this message will make the batch exceed the ``max_messages``
        # setting, return False.
        if len(self.messages) >= self.settings.max_messages:
            return False

        # Okay, everything is good.
        return True

    @abc.abstractmethod
    def publish(self, message):
        """Publish a single message.

        Add the given message to this object; this will cause it to be
        published once the batch either has enough messages or a sufficient
        period of time has elapsed.

        This method is called by :meth:`~.PublisherClient.publish`.

        Args:
            message (~.pubsub_v1.types.PubsubMessage): The Pub/Sub message.

        Returns:
            ~google.api_core.future.Future: An object conforming to the
                :class:`concurrent.futures.Future` interface.
        """
        raise NotImplementedError


class BatchStatus(object):
    """An enum-like class representing valid statuses for a batch.

    It is acceptable for a class to use a status that is not on this
    class; this represents the list of statuses where the existing
    library hooks in functionality.
    """
    ACCEPTING_MESSAGES = 'accepting messages'
    STARTING = 'starting'
    IN_PROGRESS = 'in progress'
    ERROR = 'error'
    SUCCESS = 'success'
