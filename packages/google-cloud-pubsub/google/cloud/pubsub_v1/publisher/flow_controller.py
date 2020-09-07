# Copyright 2020, Google LLC All rights reserved.
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

from collections import deque
import logging
import threading
import warnings

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions


_LOGGER = logging.getLogger(__name__)


class _QuantityReservation(object):
    """A (partial) reservation of a quantifiable resource."""

    def __init__(self, reserved, needed):
        self.reserved = reserved
        self.needed = needed


class FlowController(object):
    """A class used to control the flow of messages passing through it.

    Args:
        settings (~google.cloud.pubsub_v1.types.PublishFlowControl):
            Desired flow control configuration.
    """

    def __init__(self, settings):
        self._settings = settings

        # Load statistics. They represent the number of messages added, but not
        # yet released (and their total size).
        self._message_count = 0
        self._total_bytes = 0

        # A FIFO queue of threads blocked on adding a message, from first to last.
        # Only relevant if the configured limit exceeded behavior is BLOCK.
        self._waiting = deque()

        # Reservations of available flow control bytes by the waiting threads.
        # Each value is a _QuantityReservation instance.
        self._byte_reservations = dict()
        self._reserved_bytes = 0

        # The lock is used to protect all internal state (message and byte count,
        # waiting threads to add, etc.).
        self._operational_lock = threading.Lock()

        # The condition for blocking the flow if capacity is exceeded.
        self._has_capacity = threading.Condition(lock=self._operational_lock)

    def add(self, message):
        """Add a message to flow control.

        Adding a message updates the internal load statistics, and an action is
        taken if these limits are exceeded (depending on the flow control settings).

        Args:
            message (:class:`~google.cloud.pubsub_v1.types.PubsubMessage`):
                The message entering the flow control.

        Raises:
            :exception:`~pubsub_v1.publisher.exceptions.FlowControlLimitError`:
                Raised when the desired action is
                :attr:`~google.cloud.pubsub_v1.types.LimitExceededBehavior.ERROR` and
                the message would exceed flow control limits, or when the desired action
                is :attr:`~google.cloud.pubsub_v1.types.LimitExceededBehavior.BLOCK` and
                the message would block forever against the flow control limits.
        """
        if self._settings.limit_exceeded_behavior == types.LimitExceededBehavior.IGNORE:
            return

        with self._operational_lock:
            if not self._would_overflow(message):
                self._message_count += 1
                self._total_bytes += message._pb.ByteSize()
                return

            # Adding a message would overflow, react.
            if (
                self._settings.limit_exceeded_behavior
                == types.LimitExceededBehavior.ERROR
            ):
                # Raising an error means rejecting a message, thus we do not
                # add anything to the existing load, but we do report the would-be
                # load if we accepted the message.
                load_info = self._load_info(
                    message_count=self._message_count + 1,
                    total_bytes=self._total_bytes + message._pb.ByteSize(),
                )
                error_msg = "Flow control limits would be exceeded - {}.".format(
                    load_info
                )
                raise exceptions.FlowControlLimitError(error_msg)

            assert (
                self._settings.limit_exceeded_behavior
                == types.LimitExceededBehavior.BLOCK
            )

            # Sanity check - if a message exceeds total flow control limits all
            # by itself, it would block forever, thus raise error.
            if (
                message._pb.ByteSize() > self._settings.byte_limit
                or self._settings.message_limit < 1
            ):
                load_info = self._load_info(
                    message_count=1, total_bytes=message._pb.ByteSize()
                )
                error_msg = (
                    "Total flow control limits too low for the message, "
                    "would block forever - {}.".format(load_info)
                )
                raise exceptions.FlowControlLimitError(error_msg)

            current_thread = threading.current_thread()

            while self._would_overflow(message):
                if current_thread not in self._byte_reservations:
                    self._waiting.append(current_thread)
                    self._byte_reservations[current_thread] = _QuantityReservation(
                        reserved=0, needed=message._pb.ByteSize()
                    )

                _LOGGER.debug(
                    "Blocking until there is enough free capacity in the flow - "
                    "{}.".format(self._load_info())
                )

                self._has_capacity.wait()

                _LOGGER.debug(
                    "Woke up from waiting on free capacity in the flow - "
                    "{}.".format(self._load_info())
                )

            # Message accepted, increase the load and remove thread stats.
            self._message_count += 1
            self._total_bytes += message._pb.ByteSize()
            self._reserved_bytes -= self._byte_reservations[current_thread].reserved
            del self._byte_reservations[current_thread]
            self._waiting.remove(current_thread)

    def release(self, message):
        """Release a mesage from flow control.

        Args:
            message (:class:`~google.cloud.pubsub_v1.types.PubsubMessage`):
                The message entering the flow control.
        """
        if self._settings.limit_exceeded_behavior == types.LimitExceededBehavior.IGNORE:
            return

        with self._operational_lock:
            # Releasing a message decreases the load.
            self._message_count -= 1
            self._total_bytes -= message._pb.ByteSize()

            if self._message_count < 0 or self._total_bytes < 0:
                warnings.warn(
                    "Releasing a message that was never added or already released.",
                    category=RuntimeWarning,
                    stacklevel=2,
                )
                self._message_count = max(0, self._message_count)
                self._total_bytes = max(0, self._total_bytes)

            self._distribute_available_bytes()

            # If at least one thread waiting to add() can be unblocked, wake them up.
            if self._ready_to_unblock():
                _LOGGER.debug("Notifying threads waiting to add messages to flow.")
                self._has_capacity.notify_all()

    def _distribute_available_bytes(self):
        """Distribute availalbe free capacity among the waiting threads in FIFO order.

        The method assumes that the caller has obtained ``_operational_lock``.
        """
        available = self._settings.byte_limit - self._total_bytes - self._reserved_bytes

        for thread in self._waiting:
            if available <= 0:
                break

            reservation = self._byte_reservations[thread]
            still_needed = reservation.needed - reservation.reserved

            # Sanity check for any internal inconsistencies.
            if still_needed < 0:
                msg = "Too many bytes reserved: {} / {}".format(
                    reservation.reserved, reservation.needed
                )
                warnings.warn(msg, category=RuntimeWarning)
                still_needed = 0

            can_give = min(still_needed, available)
            reservation.reserved += can_give
            self._reserved_bytes += can_give
            available -= can_give

    def _ready_to_unblock(self):
        """Determine if any of the threads waiting to add a message can proceed.

        The method assumes that the caller has obtained ``_operational_lock``.

        Returns:
            bool
        """
        if self._waiting:
            # It's enough to only check the head of the queue, because FIFO
            # distribution of any free capacity.
            reservation = self._byte_reservations[self._waiting[0]]
            return (
                reservation.reserved >= reservation.needed
                and self._message_count < self._settings.message_limit
            )

        return False

    def _would_overflow(self, message):
        """Determine if accepting a message would exceed flow control limits.

        The method assumes that the caller has obtained ``_operational_lock``.

        Args:
            message (:class:`~google.cloud.pubsub_v1.types.PubsubMessage`):
                The message entering the flow control.

        Returns:
            bool
        """
        reservation = self._byte_reservations.get(threading.current_thread())

        if reservation:
            enough_reserved = reservation.reserved >= reservation.needed
        else:
            enough_reserved = False

        bytes_taken = self._total_bytes + self._reserved_bytes + message._pb.ByteSize()
        size_overflow = bytes_taken > self._settings.byte_limit and not enough_reserved
        msg_count_overflow = self._message_count + 1 > self._settings.message_limit

        return size_overflow or msg_count_overflow

    def _load_info(self, message_count=None, total_bytes=None, reserved_bytes=None):
        """Return the current flow control load information.

        The caller can optionally adjust some of the values to fit its reporting
        needs.

        The method assumes that the caller has obtained ``_operational_lock``.

        Args:
            message_count (Optional[int]):
                The value to override the current message count with.
            total_bytes (Optional[int]):
                The value to override the current total bytes with.
            reserved_bytes (Optional[int]):
                The value to override the current number of reserved bytes with.

        Returns:
            str
        """
        msg = "messages: {} / {}, bytes: {} / {} (reserved: {})"

        if message_count is None:
            message_count = self._message_count

        if total_bytes is None:
            total_bytes = self._total_bytes

        if reserved_bytes is None:
            reserved_bytes = self._reserved_bytes

        return msg.format(
            message_count,
            self._settings.message_limit,
            total_bytes,
            self._settings.byte_limit,
            reserved_bytes,
        )
