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

import six

from google.cloud.pubsub_v1.subscriber import histogram


@six.add_metaclass(abc.ABCMeta)
class BaseConsumer(object):
    """Abstract base class for consumers.

    Although the :class:`~.pubsub_v1.subscriber.consumer.mp.Consumer` class,
    based on :class:`multiprocessing.Process`, is fine for most cases,
    advanced users may need to implement something based on a different
    concurrency model.

    This class defines the interface for the consumer implementation;
    subclasses may be passed as the ``consumer_class`` argument to
    :class:`~.pubsub_v1.client.SubscriberClient`.
    """
    def __init__(self, client, subscription):
        self._client = client
        self._subscription = subscription
        self._ack_deadline = 10
        self._last_histogram_size = 0
        self.histogram = histogram.Histogram()

    @property
    def ack_deadline(self):
        """Return the appropriate ack deadline.

        This method is "sticky". It will only perform the computations to
        check on the right ack deadline if the histogram has gained a
        significant amount of new information.

        Returns:
            int: The correct ack deadline.
        """
        if len(self.histogram) > self._last_histogram_size * 2:
            self._ack_deadline = self.histogram.percentile(percent=99)
        return self._ack_deadline

    @abc.abstractmethod
    def ack(self, ack_id):
        """Acknowledge the message corresponding to the given ack_id."""
        raise NotImplementedError

    @abc.abstractmethod
    def modify_ack_deadline(self, ack_id, seconds):
        """Modify the ack deadline for the given ack_id."""
        raise NotImplementedError

    @abc.abstractmethod
    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.
        """
        raise NotImplementedError
