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
        "Goal",
        "GoalTypeEnum",
        "UnitTypeEnum",
    },
)


class Goal(proto.Message):
    r"""Defines the criteria a [LineItem][google.ads.admanager.v1.LineItem]
    needs to satisfy to meet its delivery goal.

    Attributes:
        goal_type (google.ads.admanager_v1.types.GoalTypeEnum.GoalType):
            The type of the goal for the LineItem. It
            defines the period over which the goal should be
            reached.
        unit_type (google.ads.admanager_v1.types.UnitTypeEnum.UnitType):
            The type of the goal unit for the LineItem.
        units (int):
            If this is a primary goal, it represents the number or
            percentage of impressions or clicks that will be reserved.
            If the line item is of type
            [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP],
            it represents the percentage of available impressions
            reserved. If the line item is of type
            [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
            or
            [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY],
            it represents the number of remaining impressions reserved.
            If the line item is of type
            [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
            or
            [LineItemTypeEnum.LineItemType.HOUSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.HOUSE],
            it represents the percentage of remaining impressions
            reserved. If this is an impression cap goal, it represents
            the number of impressions or conversions that the line item
            will stop serving at if reached. For valid line item types,
            see [LineItem.impressions_cap][].
    """

    goal_type: "GoalTypeEnum.GoalType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="GoalTypeEnum.GoalType",
    )
    unit_type: "UnitTypeEnum.UnitType" = proto.Field(
        proto.ENUM,
        number=2,
        enum="UnitTypeEnum.UnitType",
    )
    units: int = proto.Field(
        proto.INT64,
        number=3,
    )


class GoalTypeEnum(proto.Message):
    r"""Wrapper message for
    [GoalType][google.ads.admanager.v1.GoalTypeEnum.GoalType].

    """

    class GoalType(proto.Enum):
        r"""Specifies the type of the goal for a LineItem.

        Values:
            GOAL_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            NONE (1):
                No goal is specified for the number of ads delivered. The
                line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
                -  [LineItemTypeEnum.LineItemType.AD_EXCHANGE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.AD_EXCHANGE]
                -  [LineItemTypeEnum.LineItemType.CLICK_TRACKING][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.CLICK_TRACKING]
            LIFETIME (2):
                There is a goal on the number of ads delivered for this line
                item during its entire lifetime. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
                -  [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
                -  [LineItemTypeEnum.LineItemType.ADSENSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.ADSENSE]
                -  [LineItemTypeEnum.LineItemType.AD_EXCHANGE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.AD_EXCHANGE]
                -  [LineItemTypeEnum.LineItemType.ADMOB][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.ADMOB]
                -  [LineItemTypeEnum.LineItemType.CLICK_TRACKING][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.CLICK_TRACKING]
            DAILY (3):
                There is a daily goal on the number of ads delivered for
                this line item. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.SPONSORSHIP][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.SPONSORSHIP]
                -  [LineItemTypeEnum.LineItemType.NETWORK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.NETWORK]
                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
                -  [LineItemTypeEnum.LineItemType.HOUSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.HOUSE]
                -  [LineItemTypeEnum.LineItemType.ADSENSE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.ADSENSE]
                -  [LineItemTypeEnum.LineItemType.AD_EXCHANGE][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.AD_EXCHANGE]
                -  [LineItemTypeEnum.LineItemType.ADMOB][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.ADMOB]
                -  [LineItemTypeEnum.LineItemType.BUMPER][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BUMPER]
        """
        GOAL_TYPE_UNSPECIFIED = 0
        NONE = 1
        LIFETIME = 2
        DAILY = 3


class UnitTypeEnum(proto.Message):
    r"""Wrapper message for
    [UnitType][google.ads.admanager.v1.UnitTypeEnum.UnitType].

    """

    class UnitType(proto.Enum):
        r"""Indicates the type of unit used for defining a reservation. The
        [LineItem.cost_type][google.ads.admanager.v1.LineItem.cost_type] can
        differ from the UnitType - an ad can have an impression goal, but be
        billed by its click. Usually CostType and UnitType will refer to the
        same unit.

        Values:
            UNIT_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            IMPRESSIONS (1):
                The number of impressions served by creatives
                associated with the line item.
            CLICKS (2):
                The number of clicks reported by creatives associated with
                the line item. The line item
                [type][google.ads.admanager.v1.LineItem.line_item_type] must
                be one of:

                -  [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD]
                -  [LineItemTypeEnum.LineItemType.BULK][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.BULK]
                -  [LineItemTypeEnum.LineItemType.PRICE_PRIORITY][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.PRICE_PRIORITY]
            CLICK_THROUGH_CPA_CONVERSIONS (3):
                The number of view-through Cost-Per-Action (CPA) conversions
                from creatives associated with the line item. This is only
                supported as secondary goal and the
                [LineItem.cost_type][google.ads.admanager.v1.LineItem.cost_type]
                must be [CostTypeEnum.CostType.CPA][].
            VIEW_THROUGH_CPA_CONVERSIONS (4):
                The number of view-through Cost-Per-Action (CPA) conversions
                from creatives associated with the line item. This is only
                supported as secondary goal and the
                [LineItem.cost_type][google.ads.admanager.v1.LineItem.cost_type]
                must be [CostTypeEnum.CostType.CPA}.
            TOTAL_CPA_CONVERSIONS (5):
                The number of total Cost-Per-Action (CPA) conversions from
                creatives associated with the line item. This is only
                supported as secondary goal and the [LineItem.cost_type}
                must be [CostTypeEnum.CostType.CPA}.
            VIEWABLE_IMPRESSIONS (6):
                The number of viewable impressions reported by creatives
                associated with the line item. The
                [LineItem.line_item_type][google.ads.admanager.v1.LineItem.line_item_type]
                must be
                [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD].
            IN_TARGET_IMPRESSIONS (7):
                The number of in-target impressions reported by third party
                measurements. The
                [LineItem.line_item_type][google.ads.admanager.v1.LineItem.line_item_type]
                must be
                [LineItemTypeEnum.LineItemType.STANDARD][google.ads.admanager.v1.LineItemTypeEnum.LineItemType.STANDARD].
        """
        UNIT_TYPE_UNSPECIFIED = 0
        IMPRESSIONS = 1
        CLICKS = 2
        CLICK_THROUGH_CPA_CONVERSIONS = 3
        VIEW_THROUGH_CPA_CONVERSIONS = 4
        TOTAL_CPA_CONVERSIONS = 5
        VIEWABLE_IMPRESSIONS = 6
        IN_TARGET_IMPRESSIONS = 7


__all__ = tuple(sorted(__protobuf__.manifest))
