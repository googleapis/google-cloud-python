# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "ComputedStatusEnum",
    },
)


class ComputedStatusEnum(proto.Message):
    r"""Wrapper message for
    [ComputedStatus][google.ads.admanager.v1.ComputedStatusEnum.ComputedStatus].

    """

    class ComputedStatus(proto.Enum):
        r"""Describes the computed LineItem status that is derived from
        the current state of the LineItem.

        Values:
            COMPUTED_STATUS_UNSPECIFIED (0):
                No value specified.
            DELIVERY_EXTENDED (1):
                The LineItem has past its link
                LineItem#endDateTime with an auto extension, but
                hasn't met its goal.
            DELIVERING (2):
                The LineItem has begun serving.
            READY (3):
                The LineItem has been activated and is ready
                to serve.
            PAUSED (4):
                The LineItem has been paused from serving.
            INACTIVE (5):
                The LineItem is inactive. It is either caused
                by missing creatives or the network disabling
                auto-activation.
            PAUSED_INVENTORY_RELEASED (6):
                The LineItem has been paused and its reserved
                inventory has been released. The LineItem will
                not serve.
            PENDING_APPROVAL (7):
                The LineItem has been submitted for approval.
            COMPLETED (8):
                The LineItem has completed its run.
            DISAPPROVED (9):
                The LineItem has been disapproved and is not
                eligible to serve.
            DRAFT (10):
                The LineItem is still being drafted.
            CANCELED (11):
                The LineItem has been canceled and is no
                longer eligible to serve. This is a legacy
                status imported from Google Ad Manager orders.
        """
        COMPUTED_STATUS_UNSPECIFIED = 0
        DELIVERY_EXTENDED = 1
        DELIVERING = 2
        READY = 3
        PAUSED = 4
        INACTIVE = 5
        PAUSED_INVENTORY_RELEASED = 6
        PENDING_APPROVAL = 7
        COMPLETED = 8
        DISAPPROVED = 9
        DRAFT = 10
        CANCELED = 11


__all__ = tuple(sorted(__protobuf__.manifest))
