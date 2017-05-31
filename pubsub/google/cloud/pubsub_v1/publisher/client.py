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

import functools
import multiprocessing
import pkg_resources

import six

from google.cloud.gapic.pubsub.v1 import publisher_client

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher.batch import Batch
from google.cloud.pubsub_v1.publisher.batch import FAKE


__VERSION__ = pkg_resources.get_distribution('google-cloud-pubsub').version


@_gapic.add_methods(publisher_client.PublisherClient, blacklist=('publish',))
class PublisherClient(object):
    """A publisher client for Cloud Pub/Sub.

    This creates an object that is capable of publishing messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        batching (:class:`google.cloud.pubsub_v1.types.Batching`): The
            settings for batch publishing.
        thread_class (class): Any class that is duck-type compatible with
            :class:`threading.Thread`.
            The default is :class:`multiprocessing.Process`
        kwargs (dict): Any additional arguments provided are sent as keyword
            arguments to the underlying
            :class:`~gapic.pubsub.v1.publisher_client.PublisherClient`.
            Generally, you should not need to set additional keyword arguments.
    """
    _gapic_class = publisher_client.PublisherClient

    def __init__(self, batching=(), thread_class=multiprocessing.Process,
                 queue_class=multiprocessing.Queue, **kwargs):
        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        kwargs['lib_name'] = 'gccl'
        kwargs['lib_version'] = __VERSION__
        self.api = self._gapic_class(**kwargs)
        self.batching = types.Batching(*batching)

        # Set the manager, which is responsible for granting shared memory
        # objects.
        self._manager = multiprocessing.Manager()

        # Set the thread class.
        self._thread_class = thread_class

        # The batches on the publisher client are responsible for holding
        # messages. One batch exists for each topic.
        self._batches = {}

    @property
    def manager(self):
        """Return the manager.

        Returns:
            :class:`multiprocessing.Manager`: The manager responsible for
                handling shared memory objects.
        """
        return self._manager

    @property
    def thread_class(self):
        """Return the thread class provided at instantiation.

        Returns:
            class: A class duck-type compatible with :class:`threading.Thread`.
        """
        return self._thread_class

    def batch(self, topic, create=True, autocommit=True):
        """Return the current batch.

        This will create a new batch only if no batch currently exists.

        Args:
            topic (str): A string representing the topic.
            create (bool): Whether to create a new batch if no batch is
                found. Defaults to True.
            autocommit (bool): Whether to autocommit this batch.
                This is primarily useful for debugging.

        Returns:
            :class:~`pubsub_v1.batch.Batch` The batch object.
        """
        # If there is no matching batch yet, then potentially create one
        # and place it on the batches dictionary.
        if self._batches.get(topic, FAKE).status != 'accepting messages':
            if not create:
                return None
            self._batches[topic] = Batch(
                autocommit=autocommit,
                client=self,
                settings=self.batching,
                topic=topic,
            )

        # Simply return the appropriate batch.
        return self._batches[topic]

    def publish(self, topic, data, **attrs):
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

        Example:
            >>> from google.cloud.pubsub_v1 import publisher_client
            >>> client = publisher_client.PublisherClient()
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> data = b'The rain in Wales falls mainly on the snails.'
            >>> response = client.publish(topic, data, username='guido')

        Args:
            topic (:class:~`pubsub_v1.types.Topic`): The topic to publish
                messages to.
            data (bytes): A bytestring representing the message body. This
                must be a bytestring (a text string will raise TypeError).
            attrs (Mapping[str, str]): A dictionary of attributes to be
                sent as metadata. (These may be text strings or byte strings.)

        Raises:
            :exc:`TypeError`: If the ``data`` sent is not a bytestring, or
                if the ``attrs`` are not either a ``str`` or ``bytes``.

        Returns:
            :class:~`pubsub_v1.publisher.futures.Future`: An object conforming
                to the ``concurrent.futures.Future`` interface.
        """
        return self.batch(topic).publish(data, *attrs)
