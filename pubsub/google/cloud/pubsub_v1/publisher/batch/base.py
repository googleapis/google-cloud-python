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

import abc
import collections

import six


@six.add_metaclass(abc.ABCMeta)
class BaseBatch(object):
    """The base batching class for Pub/Sub publishing.

    Although the :class:`~.pubsub_v1.publisher.batch.mp.Batch` class, based
    on :class:`multiprocessing.Process`, is fine for most cases, advanced
    users may need to implement something based on a different concurrency
    model.

    This class defines the interface for the Batch implementation;
    subclasses may be passed as the ``batch_class`` argument to
    :class:`~.pubsub_v1.client.PublisherClient`.
    """
    @property
    @abc.abstractmethod
    def client(self):
        """Return the client used to create this batch.

        Returns:
            ~.pubsub_v1.client.PublisherClient: A publisher client.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def settings(self):
        """Return the settings for this batch.

        Returns:
            ~.pubsub_v1.types.Batching: The settings for batch
                publishing. These should be considered immutable once the batch
                has been opened.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def status(self):
        """Return the status of this batch.

        Returns:
            str: The status of this batch. All statuses are human-readable,
                all-lowercase strings, and represented in the
                :class:`BaseBatch.Status` enum.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        """Asychronously commit everything in this batch.

        Subclasses must define this as an asychronous method; it may be called
        from the primary process by :meth:`check_limits`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def publish(self, data, **attrs):
        """Publish a single message.

        .. note::
            Messages in Pub/Sub are blobs of bytes. They are *binary* data,
            not text. You must send data as a bytestring
            (``bytes`` in Python 3; ``str`` in Python 2), and this library
            will raise an exception if you send a text string.

            The reason that this is so important (and why we do not try to
            coerce for you) is because Pub/Sub is also platform independent
            and there is no way to know how to decode messages properly on
            the other side; therefore, encoding and decoding is a required
            exercise for the developer.

        Add the given message to this object; this will cause it to be
        published once the batch either has enough messages or a sufficient
        period of time has elapsed.

        Args:
            data (bytes): A bytestring representing the message body. This
                must be a bytestring (a text string will raise TypeError).
            attrs (Mapping[str, str]): A dictionary of attributes to be
                sent as metadata. (These may be text strings or byte strings.)

        Raises:
            TypeError: If the ``data`` sent is not a bytestring, or if the
                ``attrs`` are not either a ``str`` or ``bytes``.

        Returns:
            ~.pubsub_v1.publisher.future.Future: An object conforming to the
                :class:`concurrent.futures.Future` interface.
        """
        raise NotImplementedError

    class Status(object):
        """An enum class representing valid statuses for a batch.

        It is acceptable for a class to use a status that is not on this
        class; this represents the list of statuses where the existing
        library hooks in functionality.
        """
        ACCEPTING_MESSAGES = 'accepting messages'
        ERROR = 'error'
        SUCCESS = 'success'


# Make a fake batch. This is used by the client to do single-op checks
# for batch existence.
FakeBatch = collections.namedtuple('FakeBatch', ['status'])
FAKE = FakeBatch(status='fake')
