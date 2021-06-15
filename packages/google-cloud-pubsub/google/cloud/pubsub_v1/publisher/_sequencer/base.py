# Copyright 2019, Google LLC All rights reserved.
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

from google.api_core import gapic_v1
from google.pubsub_v1 import types as gapic_types


class Sequencer(metaclass=abc.ABCMeta):
    """The base class for sequencers for Pub/Sub publishing. A sequencer
       sequences messages to be published.
    """

    @staticmethod
    @abc.abstractmethod
    def is_finished(self):  # pragma: NO COVER
        """ Whether the sequencer is finished and should be cleaned up.

            Returns:
                bool: Whether the sequencer is finished and should be cleaned up.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def unpause(self, message):  # pragma: NO COVER
        """ Unpauses this sequencer.

        Raises:
            RuntimeError:
                If called when the sequencer has not been paused.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def publish(
        self,
        message,
        retry=None,
        timeout: gapic_types.TimeoutType = gapic_v1.method.DEFAULT,
    ):  # pragma: NO COVER
        """ Publish message for this ordering key.

        Args:
            message (~.pubsub_v1.types.PubsubMessage):
                The Pub/Sub message.
            retry (Optional[google.api_core.retry.Retry]):
                The retry settings to apply when publishing the message.
            timeout (:class:`~.pubsub_v1.types.TimeoutType`):
                The timeout to apply when publishing the message.

        Returns:
            A class instance that conforms to Python Standard library's
            :class:`~concurrent.futures.Future` interface (but not an
            instance of that class). The future might return immediately with a
            `pubsub_v1.publisher.exceptions.PublishToPausedOrderingKeyException`
            if the ordering key is paused.  Otherwise, the future tracks the
            lifetime of the message publish.

        Raises:
            RuntimeError:
                If called after this sequencer has been stopped, either by
                a call to stop() or after all batches have been published.
        """
        raise NotImplementedError
