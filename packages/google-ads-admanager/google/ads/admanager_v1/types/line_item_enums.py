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
        "LineItemCostTypeEnum",
        "CreativeRotationTypeEnum",
        "DeliveryRateTypeEnum",
        "LineItemDiscountTypeEnum",
        "LineItemTypeEnum",
        "ReservationStatusEnum",
    },
)


class LineItemCostTypeEnum(proto.Message):
    r"""Wrapper message for
    [LineItemCostType][google.ads.admanager.v1.LineItemCostTypeEnum.LineItemCostType].

    """

    class LineItemCostType(proto.Enum):
        r"""Describes the LineItem actions that are billable.

        Values:
            LINE_ITEM_COST_TYPE_UNSPECIFIED (0):
                Not specified value.
            CPA (1):
                Cost per action. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
                -  [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
                -  [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
            CPC (2):
                Cost per click. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
                -  [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
                -  [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
                -  [LineItemTypeEnum.LineItemType.HOUSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.HOUSE]
            CPD (3):
                Cost per day. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
                -  [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
            CPM (4):
                Cost per mille (thousand) impressions. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
                -  [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
                -  [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
                -  [LineItemTypeEnum.LineItemType.HOUSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.HOUSE]
            VCPM (5):
                Cost per mille (thousand) Active View viewable impressions.
                The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
            CPM_IN_TARGET (6):
                Cost per millie (thousand) in-target impressions. The line
                item [type][google.ads.admanager.v1.LineItem.line_item_type]
                must be one of:

                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
            CPF (7):
                Cost for the entire flight of the deal. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be must be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
        """
        LINE_ITEM_COST_TYPE_UNSPECIFIED = 0
        CPA = 1
        CPC = 2
        CPD = 3
        CPM = 4
        VCPM = 5
        CPM_IN_TARGET = 6
        CPF = 7


class CreativeRotationTypeEnum(proto.Message):
    r"""Wrapper message for
    [CreativeRotationType][google.ads.admanager.v1.CreativeRotationTypeEnum.CreativeRotationType].

    """

    class CreativeRotationType(proto.Enum):
        r"""The strategy to use for displaying multiple
        [creatives][google.ads.admanager.v1.Creative] that are associated
        with a line item.

        Values:
            CREATIVE_ROTATION_TYPE_UNSPECIFIED (0):
                Not specified value
            EVENLY (1):
                Creatives are displayed approximately the
                same number of times over the duration of the
                line item.
            OPTIMIZED (2):
                Creatives are served approximately
                proportionally to their performance.
            WEIGHTED (3):
                Creatives are served approximately proportionally to their
                weights, set on the ``LineItemCreativeAssociation``.
            SEQUENTIAL (4):
                Creatives are served exactly in sequential order, aka
                Storyboarding. Set on the ``LineItemCreativeAssociation``.
        """
        CREATIVE_ROTATION_TYPE_UNSPECIFIED = 0
        EVENLY = 1
        OPTIMIZED = 2
        WEIGHTED = 3
        SEQUENTIAL = 4


class DeliveryRateTypeEnum(proto.Message):
    r"""Wrapper message for
    [DeliveryRateType][google.ads.admanager.v1.DeliveryRateTypeEnum.DeliveryRateType].

    """

    class DeliveryRateType(proto.Enum):
        r"""Possible delivery rates for a line item. It dictates the
        manner in which the line item is served.

        Values:
            DELIVERY_RATE_TYPE_UNSPECIFIED (0):
                Not specified value
            EVENLY (1):
                Line items are served as evenly as possible across the
                number of days specified in a line item's
                [duration][LineItem.duration].
            FRONTLOADED (2):
                Line items are served more aggressively in
                the beginning of the flight date.
            AS_FAST_AS_POSSIBLE (3):
                The booked impressions may delivered well before the
                [end_time][google.ads.admanager.v1.LineItem.end_time]. Other
                lower-priority or lower-value line items will be stopped
                from delivering until the line item meets the number of
                impressions or clicks it is booked for.
        """
        DELIVERY_RATE_TYPE_UNSPECIFIED = 0
        EVENLY = 1
        FRONTLOADED = 2
        AS_FAST_AS_POSSIBLE = 3


class LineItemDiscountTypeEnum(proto.Message):
    r"""Wrapper message for
    [LineItemDiscountType][google.ads.admanager.v1.LineItemDiscountTypeEnum.LineItemDiscountType].

    """

    class LineItemDiscountType(proto.Enum):
        r"""Describes the possible discount types on the cost of booking
        a line item.

        Values:
            LINE_ITEM_DISCOUNT_TYPE_UNSPECIFIED (0):
                No value specified
            ABSOLUTE_VALUE (1):
                An absolute value will be discounted from the
                line item's cost.
            PERCENTAGE (2):
                A percentage of the cost will be discounted
                for booking the line item.
        """
        LINE_ITEM_DISCOUNT_TYPE_UNSPECIFIED = 0
        ABSOLUTE_VALUE = 1
        PERCENTAGE = 2


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
            LEGACY_DFP (8):
                Represents a legacy LineItem that has been
                migrated from the DFP system.
            CLICK_TRACKING (6):
                The type of LineItem used for ads that track
                ads being served externally of Ad Manager.
            ADSENSE (2):
                A LineItem using dynamic allocation backed by
                AdSense.
            AD_EXCHANGE (3):
                A LineItem using dynamic allocation backed by
                the Google Ad Exchange.
            BUMPER (5):
                Represents a non-monetizable video LineItem
                that targets one or more bumper positions, which
                are short house video messages used by
                publishers to separate content from ad breaks.
            ADMOB (1):
                A LineItem using dynamic allocation backed by
                AdMob.
            PREFERRED_DEAL (10):
                The type of LineItem for which there are no
                impressions reserved, and will serve for a
                second price bid.
        """
        LINE_ITEM_TYPE_UNSPECIFIED = 0
        SPONSORSHIP = 12
        STANDARD = 13
        NETWORK = 9
        BULK = 4
        PRICE_PRIORITY = 11
        HOUSE = 7
        LEGACY_DFP = 8
        CLICK_TRACKING = 6
        ADSENSE = 2
        AD_EXCHANGE = 3
        BUMPER = 5
        ADMOB = 1
        PREFERRED_DEAL = 10


class ReservationStatusEnum(proto.Message):
    r"""Wrapper message for
    [ReservationStatus][google.ads.admanager.v1.ReservationStatusEnum.ReservationStatus].

    """

    class ReservationStatus(proto.Enum):
        r"""Defines the different reservation statuses of a line item.

        Values:
            RESERVATION_STATUS_UNSPECIFIED (0):
                No value specified
            RESERVED (1):
                Indicates that inventory has been reserved
                for the line item.
            UNRESERVED (2):
                Indicates that inventory has not been
                reserved for the line item.
        """
        RESERVATION_STATUS_UNSPECIFIED = 0
        RESERVED = 1
        UNRESERVED = 2


__all__ = tuple(sorted(__protobuf__.manifest))
