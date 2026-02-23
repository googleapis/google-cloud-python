# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
        "LineItemTypeEnum",
    },
)


class LineItemTypeEnum(proto.Message):
    r"""Wrapper message for
    [LineItemType][google.ads.admanager.v1.LineItemTypeEnum.LineItemType].

    """

    class LineItemType(proto.Enum):
        r"""Indicates the priority of a LineItem, determined by the way
        in which impressions are reserved to be served for it.

        Values:
            LINE_ITEM_TYPE_UNSPECIFIED (0):
                Not specified value.
            SPONSORSHIP (12):
                The type of LineItem for which a percentage
                of all the impressions that are being sold are
                reserved.
            STANDARD (13):
                The type of LineItem for which a fixed
                quantity of impressions or clicks are reserved.
            NETWORK (9):
                The type of LineItem most commonly used to
                fill a site's unsold inventory if not
                contractually obligated to deliver a requested
                number of impressions. Uses daily percentage of
                unsold impressions or clicks.
            BULK (4):
                The type of LineItem for which a fixed
                quantity of impressions or clicks will be
                delivered at a priority lower than the STANDARD
                type.
            PRICE_PRIORITY (11):
                The type of LineItem most commonly used to
                fill a site's unsold inventory if not
                contractually obligated to deliver a requested
                number of impressions. Uses fixed quantity
                percentage of unsold impressions or clicks.
            HOUSE (7):
                The type of LineItem typically used for ads
                that promote products and services chosen by the
                publisher.
            CLICK_TRACKING (6):
                The type of LineItem used for ads that track
                ads being served externally of Ad Manager.
            ADSENSE (2):
                Targets the LineItem to specific inventory
                available to AdSense buyers.
            AD_EXCHANGE (3):
                Targets the LineItem to specific inventory
                available to Authorized Buyers and the Open
                Auction.
            BUMPER (5):
                Represents a non-monetizable video LineItem
                that targets one or more bumper positions, which
                are short house video messages used by
                publishers to separate content from ad breaks.
            PREFERRED_DEAL (10):
                The type of LineItem for which there are no
                impressions reserved, and will serve for a
                second price bid.
            AUDIENCE_EXTENSION (14):
                The type of LineItem used for configuring
                audience extension campaigns.
        """

        LINE_ITEM_TYPE_UNSPECIFIED = 0
        SPONSORSHIP = 12
        STANDARD = 13
        NETWORK = 9
        BULK = 4
        PRICE_PRIORITY = 11
        HOUSE = 7
        CLICK_TRACKING = 6
        ADSENSE = 2
        AD_EXCHANGE = 3
        BUMPER = 5
        PREFERRED_DEAL = 10
        AUDIENCE_EXTENSION = 14


__all__ = tuple(sorted(__protobuf__.manifest))
