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

import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import google.type.money_pb2 as money_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import custom_field_value
from google.ads.admanager_v1.types import goal as gaa_goal
from google.ads.admanager_v1.types import line_item_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "LineItem",
    },
)


class LineItem(proto.Message):
    r"""A LineItem contains information about how specific ad
    creatives are intended to serve to your website or app along
    with pricing and other delivery details.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. The resource name of the ``LineItem``. Format:
            ``networks/{network_code}/lineItems/{line_item_id}``
        order (str):
            Output only. The ID of the Order to which the LineItem
            belongs. This attribute is required. Format:
            ``networks/{network_code}/orders/{order}``

            This field is a member of `oneof`_ ``_order``.
        display_name (str):
            Required. The name of the line item. This
            attribute is required and has a maximum length
            of 255 characters.

            This field is a member of `oneof`_ ``_display_name``.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The date and time on which the
            LineItem is enabled to begin serving. This
            attribute is required and must be in the future.

            This field is a member of `oneof`_ ``_start_time``.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the LineItem
            will stop serving. This attribute is read-only
            and includes auto extension days.

            This field is a member of `oneof`_ ``_end_time``.
        line_item_type (google.ads.admanager_v1.types.LineItemTypeEnum.LineItemType):
            Required. Indicates the line item type of a
            LineItem. This attribute is required. The line
            item type determines the default priority of the
            line item. More information can be found at
            https://support.google.com/admanager/answer/177279.

            This field is a member of `oneof`_ ``_line_item_type``.
        rate (google.type.money_pb2.Money):
            Required. The amount of money to spend per
            impression or click.

            This field is a member of `oneof`_ ``_rate``.
        budget (google.type.money_pb2.Money):
            Output only. The amount of money allocated to
            the LineItem. This attribute is readonly and is
            populated by Google. The currency code is
            readonly.

            This field is a member of `oneof`_ ``_budget``.
        custom_field_values (MutableSequence[google.ads.admanager_v1.types.CustomFieldValue]):
            Optional. The values of the custom fields
            associated with this line item.
        goal (google.ads.admanager_v1.types.Goal):
            Optional. The primary goal that this LineItem
            is associated with, which is used in its pacing
            and budgeting.

            This field is a member of `oneof`_ ``_goal``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    order: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        optional=True,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        optional=True,
        message=timestamp_pb2.Timestamp,
    )
    line_item_type: line_item_enums.LineItemTypeEnum.LineItemType = proto.Field(
        proto.ENUM,
        number=17,
        optional=True,
        enum=line_item_enums.LineItemTypeEnum.LineItemType,
    )
    rate: money_pb2.Money = proto.Field(
        proto.MESSAGE,
        number=20,
        optional=True,
        message=money_pb2.Money,
    )
    budget: money_pb2.Money = proto.Field(
        proto.MESSAGE,
        number=35,
        optional=True,
        message=money_pb2.Money,
    )
    custom_field_values: MutableSequence[
        custom_field_value.CustomFieldValue
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=59,
        message=custom_field_value.CustomFieldValue,
    )
    goal: gaa_goal.Goal = proto.Field(
        proto.MESSAGE,
        number=76,
        optional=True,
        message=gaa_goal.Goal,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
