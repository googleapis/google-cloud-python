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

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import (
    computed_status_enum,
    creative_placeholder,
    environment_type_enum,
    goal,
    line_item_enums,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "LineItem",
        "GetLineItemRequest",
        "ListLineItemsRequest",
        "ListLineItemsResponse",
    },
)


class LineItem(proto.Message):
    r"""The LineItem resource.

    Attributes:
        name (str):
            Identifier. The resource name of the LineItem. Format:
            ``networks/{network_code}/orders/{order_id}/lineItems/{line_item_id}``
        display_name (str):
            Optional. Display name of the LineItem. This
            attribute has a maximum length of 255
            characters.
        archived (bool):
            Output only. The archival status of the
            LineItem.
        contracted_units_bought (int):
            Optional. This attribute is only applicable for certain
            [line item types][LineItemType] and acts as an "FYI" or
            note, which does not impact ad-serving or other backend
            systems.

            For [SPONSORSHIP][LineItemType.SPONSORSHIP] line items, this
            represents the minimum quantity, which is a lifetime
            impression volume goal for reporting purposes.

            For [STANDARD][LineItemType.STANDARD] line items, this
            represents the contracted quantity, which is the number of
            units specified in the contract that the advertiser has
            bought for this line item. This attribute is only available
            if you have this feature enabled on your network.
        cost_per_unit (google.type.money_pb2.Money):
            Required. The amount of money to spend per
            impression or click.
        cost_type (google.ads.admanager_v1.types.LineItemCostTypeEnum.LineItemCostType):
            Required. The method used for billing this
            line item.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant at which the
            LineItem was created. This attribute may be null
            for line items created before this feature was
            introduced.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant at which the
            LineItem was last updated
        creative_rotation_type (google.ads.admanager_v1.types.CreativeRotationTypeEnum.CreativeRotationType):
            Required. The strategy used for displaying multiple
            [creatives][google.ads.admanager.v1.Creative] that are
            associated with the line item.
        delivery_rate_type (google.ads.admanager_v1.types.DeliveryRateTypeEnum.DeliveryRateType):
            Non-empty default. The strategy for delivering ads over the
            duration of the line item. Defaults to
            [EVENLY][DeliveryRateType.EVENLY] or
            [FRONTLOADED][DeliveryRatetype.FRONTLOADED] depending on the
            network's configuration.
        discount (float):
            Optional. The number here is either a percentage or an
            absolute value depending on the
            [discount_type][google.ads.admanager.v1.LineItem.discount_type].
            If it is [PERCENTAGE][LineItemDiscountType.PERCENTAGE], then
            only non-fractional values are supported.
        discount_type (google.ads.admanager_v1.types.LineItemDiscountTypeEnum.LineItemDiscountType):
            Non-empty default. The type of discount applied to the line
            item. Defaults to
            [PERCENTAGE][LineItemDiscountType.PERCENTAGE].
        environment_type (google.ads.admanager_v1.types.EnvironmentTypeEnum.EnvironmentType):
            Non-empty default. The environment that the line item is
            targeting. The default value is
            [BROWSER][EnvironmentType.BROWSER]. If this value is
            [VIDEO_PLAYER][EnvironmentType.VIDEO_PLAYER], then this line
            item can only target
            [AdUnits][google.ads.admanager.v1.AdUnit] that have
            ``AdUnitSizes`` whose ``environment_type`` is also
            ``VIDEO_PLAYER``.
        external_id (str):
            Optional. Identifier for the LineItem that is
            meaningful to the publisher. This attribute has
            a maximum length of 255 characters.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. Time at which the LineItem will
            begin serving. This attribute must be in the
            future when creating a LineItem.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Time at which the LineItem will stop serving. This
            attribute is ignored when
            [unlimited_end_time][google.ads.admanager.v1.LineItem.unlimited_end_time]
            is ``true``. If specified, it must be after
            [start_time][google.ads.admanager.v1.LineItem.start_time].
            This end time does not include
            [auto_extension_days][google.ads.admanager.v1.LineItem.auto_extension_days].
        auto_extension_days (int):
            Optional. Number of days to allow a LineItem to deliver past
            its [end_time][google.ads.admanager.v1.LineItem.end_time]. A
            maximum of 7 days is allowed. This feature is only available
            for Ad Manager 360 accounts.
        unlimited_end_time (bool):
            Optional. Whether the LineItem has an
            [end_time][google.ads.admanager.v1.LineItem.end_time]. This
            attribute can be set to ``true`` for only LineItems with
            [line_item_type][google.ads.admanager.v1.LineItem.line_item_type]
            [SPONSORSHIP][LineItemType.SPONSORSHIP],
            [NETWORK][LineItemType.NETWORK],
            [PRICE_PRIORITY][LineItemType.PRICE_PRIORITY] and
            [HOUSE][LineItemType.HOUSE].
        last_modified_by_app (str):
            Output only. The application that last
            modified this line item.
        line_item_type (google.ads.admanager_v1.types.LineItemTypeEnum.LineItemType):
            Required. Determines the default priority of the LineItem
            for delivery. More information can be found on the `Ad
            Manager Help
            Center <https://support.google.com/dfp_premium/answer/177279>`__.
        missing_creatives (bool):
            Output only. Indicates if a line item is missing any
            [creatives][google.ads.admanager.v1.Creative] for the
            [creative_placeholders][google.ads.admanager.v1.LineItem.creative_placeholders]
            specified.

            [Creatives][google.ads.admanager.v1.Creative] can be
            considered missing for several reasons:

            -  Not enough [creatives][google.ads.admanager.v1.Creative]
               of a certain size have been uploaded, as determined by
               [expectedCreativeCount][google.ads.admanager.v1.CreativePlaceholder.expected_creative_count].
               For example a line item specifies 750x350, 400x200, but
               only a 750x350 was uploaded. Or line item specifies
               750x350 with an expected count of 2, but only one was
               uploaded.
            -  The [appliedLabels][Creative.applied_labels] of an
               associated [Creative][google.ads.admanager.v1.Creative]
               do not match the
               [effectiveAppliedLabels][CreativePlaceholder.effective_applied_labels]
               of the line item. For example if a line item specifies
               750x350 with a foo applied label, but a 750x350 creative
               without an applied label was uploaded.
        notes (str):
            Optional. Provides any additional notes that
            may annotate LineItem. This field has a maximum
            length of 65,535 characters.
        priority (int):
            Optional. Priority of the LineItem for delivery. Valid
            values range from 1 to 16. This field can only be changed by
            certain networks, otherwise a ``PERMISSION_DENIED`` error
            will occur.

            The following list shows the default, minimum, and maximum
            priority values for each [LineItemType][LineItemType]:
            formatted as ``LineItemType``: default priority (minimum
            priority, maximum priority):

            -  ``SPONSORSHIP``: 4 (2,5)
            -  ``STANDARD``: 8 (6,10)
            -  ``NETWORK``: 12 (11, 14)
            -  ``BULK``: 12 (11, 14)
            -  ``PRICE_PRIORITY``: 12 (11, 14)
            -  ``HOUSE``: 16 (15, 16)
            -  ``CLICK_TRACKING``: 16 (1, 16)
            -  ``AD_EXCHANGE``: 12 (1, 16)
            -  ``ADSENSE``: 12 (1, 16)
            -  ``BUMPER``: 16 (15, 16)
        reservation_status (google.ads.admanager_v1.types.ReservationStatusEnum.ReservationStatus):
            Output only. Describes whether or not
            inventory has been reserved for the line item.
        web_property_code (str):
            Optional. The web property code used for dynamic allocation
            line items. This web property is only required with line
            item types [AD_EXCHANGE][LineItemType.AD_EXCHANGE] and
            [ADSENSE][LineItemType.ADSENSE].
        creative_placeholders (MutableSequence[google.ads.admanager_v1.types.CreativePlaceholder]):
            Required. Details about the creatives that
            are expected to serve through this LineItem.
        status (google.ads.admanager_v1.types.ComputedStatusEnum.ComputedStatus):
            Output only. The status of the LineItem.
        primary_goal (google.ads.admanager_v1.types.Goal):
            Required. The primary goal that this LineItem
            is associated with, which is used in its pacing
            and budgeting.
        impression_limit (google.ads.admanager_v1.types.Goal):
            Optional. The impression limit for the LineItem. This field
            is meaningful only if the
            [LineItem.line_item_type][google.ads.admanager.v1.LineItem.line_item_type]
            is [LineItemType.SPONSORSHIP][] and
            [LineItem.cost_type][google.ads.admanager.v1.LineItem.cost_type]
            is [CostType.CPM][].
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    archived: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    contracted_units_bought: int = proto.Field(
        proto.INT64,
        number=18,
    )
    cost_per_unit: money_pb2.Money = proto.Field(
        proto.MESSAGE,
        number=15,
        message=money_pb2.Money,
    )
    cost_type: line_item_enums.LineItemCostTypeEnum.LineItemCostType = proto.Field(
        proto.ENUM,
        number=19,
        enum=line_item_enums.LineItemCostTypeEnum.LineItemCostType,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=31,
        message=timestamp_pb2.Timestamp,
    )
    creative_rotation_type: line_item_enums.CreativeRotationTypeEnum.CreativeRotationType = proto.Field(
        proto.ENUM,
        number=22,
        enum=line_item_enums.CreativeRotationTypeEnum.CreativeRotationType,
    )
    delivery_rate_type: line_item_enums.DeliveryRateTypeEnum.DeliveryRateType = (
        proto.Field(
            proto.ENUM,
            number=23,
            enum=line_item_enums.DeliveryRateTypeEnum.DeliveryRateType,
        )
    )
    discount: float = proto.Field(
        proto.DOUBLE,
        number=13,
    )
    discount_type: line_item_enums.LineItemDiscountTypeEnum.LineItemDiscountType = (
        proto.Field(
            proto.ENUM,
            number=24,
            enum=line_item_enums.LineItemDiscountTypeEnum.LineItemDiscountType,
        )
    )
    environment_type: environment_type_enum.EnvironmentTypeEnum.EnvironmentType = (
        proto.Field(
            proto.ENUM,
            number=25,
            enum=environment_type_enum.EnvironmentTypeEnum.EnvironmentType,
        )
    )
    external_id: str = proto.Field(
        proto.STRING,
        number=5,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    auto_extension_days: int = proto.Field(
        proto.INT32,
        number=8,
    )
    unlimited_end_time: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    last_modified_by_app: str = proto.Field(
        proto.STRING,
        number=17,
    )
    line_item_type: line_item_enums.LineItemTypeEnum.LineItemType = proto.Field(
        proto.ENUM,
        number=10,
        enum=line_item_enums.LineItemTypeEnum.LineItemType,
    )
    missing_creatives: bool = proto.Field(
        proto.BOOL,
        number=16,
    )
    notes: str = proto.Field(
        proto.STRING,
        number=20,
    )
    priority: int = proto.Field(
        proto.INT64,
        number=11,
    )
    reservation_status: line_item_enums.ReservationStatusEnum.ReservationStatus = (
        proto.Field(
            proto.ENUM,
            number=26,
            enum=line_item_enums.ReservationStatusEnum.ReservationStatus,
        )
    )
    web_property_code: str = proto.Field(
        proto.STRING,
        number=21,
    )
    creative_placeholders: MutableSequence[
        creative_placeholder.CreativePlaceholder
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=27,
        message=creative_placeholder.CreativePlaceholder,
    )
    status: computed_status_enum.ComputedStatusEnum.ComputedStatus = proto.Field(
        proto.ENUM,
        number=28,
        enum=computed_status_enum.ComputedStatusEnum.ComputedStatus,
    )
    primary_goal: goal.Goal = proto.Field(
        proto.MESSAGE,
        number=29,
        message=goal.Goal,
    )
    impression_limit: goal.Goal = proto.Field(
        proto.MESSAGE,
        number=30,
        message=goal.Goal,
    )


class GetLineItemRequest(proto.Message):
    r"""Request object for GetLineItem method.

    Attributes:
        name (str):
            Required. The resource name of the LineItem. Format:
            ``networks/{network_code}/orders/{order_id}/lineItems/{line_item_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListLineItemsRequest(proto.Message):
    r"""Request object for ListLineItems method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            LineItems. Format: networks/{network_code}/orders/{order_id}
        page_size (int):
            Optional. The maximum number of LineItems to
            return. The service may return fewer than this
            value. If unspecified, at most 50 line items
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListLineItems`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListLineItems`` must match the call that provided the page
            token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListLineItemsResponse(proto.Message):
    r"""Response object for ListLineItemsRequest containing matching
    LineItem resources.

    Attributes:
        line_items (MutableSequence[google.ads.admanager_v1.types.LineItem]):
            The LineItem from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of LineItems. If a filter was included in the
            request, this reflects the total number after the filtering
            is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    line_items: MutableSequence["LineItem"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LineItem",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
