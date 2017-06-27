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

import copy
import multiprocessing
import time
import uuid

import six

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher.batch import base


class Batch(base.BaseBatch):
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
        settings (~.pubsub_v1.types.Batching): The settings for batch
            publishing. These should be considered immutable once the batch
            has been opened.
        autocommit (bool): Whether to autocommit the batch when the time
            has elapsed. Defaults to True unless ``settings.max_latency`` is
            inf.
    """
    def __init__(self, client, topic, settings, autocommit=True):
        self._client = client
        self._manager = multiprocessing.Manager()

        # Create a namespace that is owned by the client manager; this
        # is necessary to be able to have these values be communicable between
        # processes.
        self._shared = self.manager.Namespace()
        self._shared.futures = self.manager.list()
        self._shared.messages = self.manager.list()
        self._shared.message_ids = self.manager.dict()
        self._shared.settings = settings
        self._shared.status = self.Status.ACCEPTING_MESSAGES
        self._shared.topic = topic

        # This is purely internal tracking.
        self._process = None

        # Continually monitor the thread until it is time to commit the
        # batch, or the batch is explicitly committed.
        if autocommit and self._shared.settings.max_latency < float('inf'):
            self._process = multiprocessing.Process(target=self.monitor)
            self._process.start()

    @property
    def client(self):
        """Return the client used to create this batch.

        Returns:
            ~.pubsub_v1.client.PublisherClient: A publisher client.
        """
        return self._client

    @property
    def manager(self):
        """Return the client's manager.

        Returns:
            :class:`multiprocessing.Manager`: The manager responsible for
                handling shared memory objects.
        """
        return self._manager

    @property
    def status(self):
        """Return the status of this batch.

        Returns:
            str: The status of this batch. All statuses are human-readable,
                all-lowercase strings.
        """
        return self._shared.status

    def commit(self):
        """Actually publish all of the messages on the active batch.

        This moves the batch out from being the active batch to an in-flight
        batch on the publisher, and then the batch is discarded upon
        completion.
        """
        # Update the status.
        self._shared.status = 'in-flight'

        # Begin the request to publish these messages.
        if len(self._shared.messages) == 0:
            raise Exception('Empty queue')
        response = self._client.api.publish(
            self._shared.topic,
            self._shared.messages,
        )

        # FIXME (lukesneeringer): Check for failures; retry.

        # We got a response from Pub/Sub; denote that we are processing.
        self._status = 'processing results'

        # Sanity check: If the number of message IDs is not equal to the
        # number of futures I have, then something went wrong.
        if len(response.message_ids) != len(self._shared.futures):
            raise exceptions.PublishError(
                'Some messages were not successfully published.',
            )

        # Iterate over the futures on the queue and return the response IDs.
        # We are trusting that there is a 1:1 mapping, and raise an exception
        # if not.
        self._shared.status = self.Status.SUCCESS
        for message_id, fut in zip(response.message_ids, self._shared.futures):
            self._shared.message_ids[hash(fut)] = message_id
            fut._trigger()

    def monitor(self):
        """Commit this batch after sufficient time has elapsed.

        This simply sleeps for ``self._settings.max_latency`` seconds,
        and then calls commit unless the batch has already been committed.
        """
        # Note: This thread blocks; it is up to the calling code to call it
        # in a separate thread.
        #
        # Sleep for however long we should be waiting.
        time.sleep(self._shared.settings.max_latency)

        # If, in the intervening period, the batch started to be committed,
        # then no-op at this point.
        if self._shared.status != self.Status.ACCEPTING_MESSAGES:
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
            ~.pubsub_v1.publisher.batch.mp.Future: An object conforming to the
                :class:`concurrent.futures.Future` interface.
        """
        # Sanity check: Is the data being sent as a bytestring?
        # If it is literally anything else, complain loudly about it.
        if not isinstance(data, six.binary_type):
            raise TypeError('Data being published to Pub/Sub must be sent '
                            'as a bytestring.')

        # Coerce all attributes to text strings.
        for k, v in copy.copy(attrs).items():
            if isinstance(data, six.text_type):
                continue
            if isinstance(data, six.binary_type):
                attrs[k] = v.decode('utf-8')
                continue
            raise TypeError('All attributes being published to Pub/Sub must '
                            'be sent as text strings.')

        # Store the actual message in the batch's message queue.
        self._shared.messages.append(
            types.PubsubMessage(data=data, attributes=attrs),
        )

        # Return a Future. That future needs to be aware of the status
        # of this batch.
        f = Future(self._shared)
        self._shared.futures.append(f)
        return f


class Future(object):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from asychronous Pub/Sub calls, and is the
    interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        batch (:class:`multiprocessing.Namespace`): Information about the
            batch object that is committing this message.
    """
    def __init__(self, batch_info):
        self._batch_info = batch_info
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

        This still returns True in failure cases; checking `result` or
        `exception` is the canonical way to assess success or failure.
        """
        return self._batch_info.status in ('success', 'error')

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
            return self._batch_info.message_ids[hash(self)]
        raise err

    def exception(self, timeout=None, _wait=1):
        """Return the exception raised by the call, if any.

        This blocks until the message has successfully been published, and
        returns the exception. If the call succeeded, return None.

        Args:
            timeout (int|float): The number of seconds before this call
                times out and raises TimeoutError.

        Raises:
            :exc:`TimeoutError`: If the request times out.

        Returns:
            :class:`Exception`: The exception raised by the call, if any.
        """
        # If the batch completed successfully, this should return None.
        if self._batch_info.status == 'success':
            return None

        # If this batch had an error, this should return it.
        if self._batch_info.status == 'error':
            return self._batch_info.error

        # If the timeout has been exceeded, raise TimeoutError.
        if timeout and timeout < 0:
            raise exceptions.TimeoutError('Timed out waiting for exception.')

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
