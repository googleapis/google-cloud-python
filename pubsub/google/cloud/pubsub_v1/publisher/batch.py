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

import collections
import queue
import time

from google.cloud.pubsub_v1.publisher import future


Message = collections.namedtuple('Message', ['data', 'attrs', '_client_id'])


class Batch(object):
    """A batch of messages.

    The batch is the internal group of messages which are either awaiting
    publication or currently in-flight.

    A batch is automatically created by the PublisherClient when the first
    message to be published is received; subsequent messages are added to
    that batch until the process of actual publishing _starts_.

    Once this occurs, any new messages sent to ``publish`` open a new batch.

    If you are using this library, you most likely do not need to instantiate
    batch objects directly; they will be created for you. If you want to
    change the actual batching settings, see the ``batching`` argument on
    :class:`google.cloud.pubsub_v1.PublisherClient`.

    Args:
        client (:class:`google.cloud.pubsub_v1.PublisherClient`): The
            publisher client used to create this batch. Batch settings are
            inferred from this.
        settings (:class:`google.cloud.pubsub_v1.types.Batching`): The
            settings for batch publishing. These should be considered
            immutable once the batch has been opened.
    """
    def __init__(self, client, settings):
        self._client = client
        self._settings = settings
        self._messages = queue.Queue()
        self._status = 'accepting messages'

        # Continually monitor the thread until it is time to commit the
        # batch, or the batch is explicitly committed.
        self._client.thread_class(self.monitor)

    @property
    def client(self):
        """Return the client that created this batch.

        Returns:
            :class:~`pubsub_v1.client.Client`: The client that created this
                batch.
        """
        return self._client

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

        This moves the batch out from being the active batch to an in-flight
        batch on the publisher, and then the batch is discarded upon
        completion.
        """
        # If this is the active batch on the cleint right now, remove it.
        if self._client._batch is self:
            self._client._batch = None

        # Begin the request to publish these messages.

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
        if self._status != 'accepting messages':
            return

        # Commit.
        return self.commit()

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
            Future: An object conforming to the ``concurrent.futures.Future``
                interface.
        """
        # Sanity check: Is the data being sent as a bytestring?
        # If it is literally anything else, complain loudly about it.
        if not isinstance(data, six.binary_type):
            raise TypeError('Data being published to Pub/Sub must be sent '
                            'as a bytestring.')

        # Coerce all attributes to text strings.
        for k, v in copy(attrs).items():
            if isinstance(data, six.text_type):
                continue
            if isinstance(data, six.binary_type):
                attrs[k] = v.decode('utf-8')
                continue
            raise TypeError('All attributes being published to Pub/Sub must '
                            'be sent as text strings.')

        # Add the message to the batch.
        #
        # We add an internal ID (note: a client-side ID, *not* the Pub/Sub
        # ID) so we can track the message later.
        _id = six.text_type(uuid.uuid4())
        self._messages.put(Message(data=data, attrs=attrs, client_id=_id))

        # Return a Future. That future needs to be aware of the status
        # of this batch.
        return future.Future(self)
