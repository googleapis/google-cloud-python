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

import datetime
import json
import math
import time

from google.api_core import datetime_helpers
from google.cloud.pubsub_v1.subscriber._protocol import requests


_MESSAGE_REPR = """\
Message {{
  data: {!r}
  attributes: {}
}}"""


def _indent(lines, prefix="  "):
    """Indent some text.

    Note that this is present as ``textwrap.indent``, but not in Python 2.

    Args:
        lines (str): The newline delimited string to be indented.
        prefix (Optional[str]): The prefix to indent each line with. Default
            to two spaces.

    Returns:
        str: The newly indented content.
    """
    indented = []
    for line in lines.split("\n"):
        indented.append(prefix + line)
    return "\n".join(indented)


class Message(object):
    """A representation of a single Pub/Sub message.

    The common way to interact with
    :class:`~.pubsub_v1.subscriber.message.Message` objects is to receive
    them in callbacks on subscriptions; most users should never have a need
    to instantiate them by hand. (The exception to this is if you are
    implementing a custom subclass to
    :class:`~.pubsub_v1.subscriber._consumer.Consumer`.)

    Attributes:
        message_id (str): The message ID. In general, you should not need
            to use this directly.
        data (bytes): The data in the message. Note that this will be a
            :class:`bytes`, not a text string.
        attributes (.ScalarMapContainer): The attributes sent along with the
            message. See :attr:`attributes` for more information on this type.
        publish_time (datetime): The time that this message was originally
            published.
    """

    def __init__(self, message, ack_id, request_queue):
        """Construct the Message.

        .. note::

            This class should not be constructed directly; it is the
            responsibility of :class:`BasePolicy` subclasses to do so.

        Args:
            message (~.pubsub_v1.types.PubsubMessage): The message received
                from Pub/Sub.
            ack_id (str): The ack_id received from Pub/Sub.
            request_queue (queue.Queue): A queue provided by the policy that
                can accept requests; the policy is responsible for handling
                those requests.
        """
        self._message = message
        self._ack_id = ack_id
        self._request_queue = request_queue
        self.message_id = message.message_id

        # The instantiation time is the time that this message
        # was received. Tracking this provides us a way to be smart about
        # the default lease deadline.
        self._received_timestamp = time.time()

    def __repr__(self):
        # Get an abbreviated version of the data.
        abbv_data = self._message.data
        if len(abbv_data) > 50:
            abbv_data = abbv_data[:50] + b"..."

        pretty_attrs = json.dumps(
            dict(self.attributes), indent=2, separators=(",", ": "), sort_keys=True
        )
        pretty_attrs = _indent(pretty_attrs)
        # We don't actually want the first line indented.
        pretty_attrs = pretty_attrs.lstrip()
        return _MESSAGE_REPR.format(abbv_data, pretty_attrs)

    @property
    def attributes(self):
        """Return the attributes of the underlying Pub/Sub Message.

        .. warning::

            A ``ScalarMapContainer`` behaves slightly differently than a
            ``dict``. For a Pub / Sub message this is a ``string->string`` map.
            When trying to access a value via ``map['key']``, if the key is
            not in the map, then the default value for the string type will
            be returned, which is an empty string. It may be more intuitive
            to just cast the map to a ``dict`` or to one use ``map.get``.

        Returns:
            .ScalarMapContainer: The message's attributes. This is a
            ``dict``-like object provided by ``google.protobuf``.
        """
        return self._message.attributes

    @property
    def data(self):
        """Return the data for the underlying Pub/Sub Message.

        Returns:
            bytes: The message data. This is always a bytestring; if you
                want a text string, call :meth:`bytes.decode`.
        """
        return self._message.data

    @property
    def publish_time(self):
        """Return the time that the message was originally published.

        Returns:
            datetime: The date and time that the message was published.
        """
        timestamp = self._message.publish_time
        delta = datetime.timedelta(
            seconds=timestamp.seconds, microseconds=timestamp.nanos // 1000
        )
        return datetime_helpers._UTC_EPOCH + delta

    @property
    def size(self):
        """Return the size of the underlying message, in bytes."""
        return self._message.ByteSize()

    @property
    def ack_id(self):
        """str: the ID used to ack the message."""
        return self._ack_id

    def ack(self):
        """Acknowledge the given message.

        Acknowledging a message in Pub/Sub means that you are done
        with it, and it will not be delivered to this subscription again.
        You should avoid acknowledging messages until you have
        *finished* processing them, so that in the event of a failure,
        you receive the message again.

        .. warning::
            Acks in Pub/Sub are best effort. You should always
            ensure that your processing code is idempotent, as you may
            receive any given message more than once.
        """
        time_to_ack = math.ceil(time.time() - self._received_timestamp)
        self._request_queue.put(
            requests.AckRequest(
                ack_id=self._ack_id, byte_size=self.size, time_to_ack=time_to_ack
            )
        )

    def drop(self):
        """Release the message from lease management.

        This informs the policy to no longer hold on to the lease for this
        message. Pub/Sub will re-deliver the message if it is not acknowledged
        before the existing lease expires.

        .. warning::
            For most use cases, the only reason to drop a message from
            lease management is on :meth:`ack` or :meth:`nack`; these methods
            both call this one. You probably do not want to call this method
            directly.
        """
        self._request_queue.put(
            requests.DropRequest(ack_id=self._ack_id, byte_size=self.size)
        )

    def modify_ack_deadline(self, seconds):
        """Resets the deadline for acknowledgement.

        New deadline will be the given value of seconds from now.

        The default implementation handles this for you; you should not need
        to manually deal with setting ack deadlines. The exception case is
        if you are implementing your own custom subclass of
        :class:`~.pubsub_v1.subcriber._consumer.Consumer`.

        Args:
            seconds (int): The number of seconds to set the lease deadline
                to. This should be between 0 and 600. Due to network latency,
                values below 10 are advised against.
        """
        self._request_queue.put(
            requests.ModAckRequest(ack_id=self._ack_id, seconds=seconds)
        )

    def nack(self):
        """Decline to acknowldge the given message.

        This will cause the message to be re-delivered to the subscription.
        """
        self._request_queue.put(
            requests.NackRequest(ack_id=self._ack_id, byte_size=self.size)
        )
