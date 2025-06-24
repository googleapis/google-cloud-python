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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import applied_label, custom_field_value, order_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Order",
    },
)


class Order(proto.Message):
    r"""The ``Order`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the ``Order``. Format:
            ``networks/{network_code}/orders/{order_id}``
        order_id (int):
            Output only. Order ID.
        display_name (str):
            Required. The display name of the Order.
            This value has a maximum length of 255
            characters.
        programmatic (bool):
            Optional. Specifies whether or not the Order
            is a programmatic order.
        trafficker (str):
            Required. The resource name of the User responsible for
            trafficking the Order. Format:
            "networks/{network_code}/users/{user_id}".
        advertiser_contacts (MutableSequence[str]):
            Optional. The resource names of Contacts from the advertiser
            of this Order. Format:
            "networks/{network_code}/contacts/{contact_id}".
        advertiser (str):
            Required. The resource name of the Company, which is of type
            Company.Type.ADVERTISER, to which this order belongs.
            Format: "networks/{network_code}/companies/{company_id}".
        agency_contacts (MutableSequence[str]):
            Optional. The resource names of Contacts from the
            advertising Agency of this Order. Format:
            "networks/{network_code}/contacts/{contact_id}".
        agency (str):
            Optional. The resource name of the Company, which is of type
            Company.Type.AGENCY, with which this order is associated.
            Format: "networks/{network_code}/companies/{company_id}".
        applied_teams (MutableSequence[str]):
            Optional. The resource names of Teams directly applied to
            this Order. Format:
            "networks/{network_code}/teams/{team_id}".
        effective_teams (MutableSequence[str]):
            Output only. The resource names of Teams applied to this
            Order including inherited values. Format:
            "networks/{network_code}/teams/{team_id}".
        creator (str):
            Output only. The resource name of the User who created the
            Order on behalf of the advertiser. This value is assigned by
            Google. Format: "networks/{network_code}/users/{user_id}".
        currency_code (str):
            Output only. The ISO 4217 3-letter currency
            code for the currency used by the Order. This
            value is the network's currency code.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant at which the Order and its
            associated line items are eligible to begin serving. This
            attribute is derived from the line item of the order that
            has the earliest LineItem.start_time.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant at which the Order and its
            associated line items stop being served. This attribute is
            derived from the line item of the order that has the latest
            LineItem.end_time.
        unlimited_end_time (bool):
            Output only. Indicates whether or not this
            Order has an end time.
        external_order_id (int):
            Optional. An arbitrary ID to associate to the
            Order, which can be used as a key to an external
            system.
        archived (bool):
            Output only. The archival status of the
            Order.
        last_modified_by_app (str):
            Output only. The application which modified
            this order. This attribute is assigned by
            Google.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this Order was last
            modified.
        notes (str):
            Optional. Provides any additional notes that
            may annotate the Order. This attribute has a
            maximum length of 65,535 characters.
        po_number (str):
            Optional. The purchase order number for the
            Order. This value has a maximum length of 63
            characters.
        status (google.ads.admanager_v1.types.OrderStatusEnum.OrderStatus):
            Output only. The status of the Order.
        salesperson (str):
            Optional. The resource name of the User responsible for the
            sales of the Order. Format:
            "networks/{network_code}/users/{user_id}".
        secondary_salespeople (MutableSequence[str]):
            Optional. Unordered list. The resource names of the
            secondary salespeople associated with the order. Format:
            "networks/{network_code}/users/{user_id}".
        secondary_traffickers (MutableSequence[str]):
            Optional. Unordered list. The resource names of the
            secondary traffickers associated with the order. Format:
            "networks/{network_code}/users/{user_id}".
        applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Optional. The set of labels applied directly
            to this order.
        effective_applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Output only. Contains the set of labels
            applied directly to the order as well as those
            inherited from the company that owns the order.
            If a label has been negated, only the negated
            label is returned. This field is assigned by
            Google.
        custom_field_values (MutableSequence[google.ads.admanager_v1.types.CustomFieldValue]):
            Optional. The set of custom field values to
            this order.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    order_id: int = proto.Field(
        proto.INT64,
        number=4,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    programmatic: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    trafficker: str = proto.Field(
        proto.STRING,
        number=23,
    )
    advertiser_contacts: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    advertiser: str = proto.Field(
        proto.STRING,
        number=6,
    )
    agency_contacts: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    agency: str = proto.Field(
        proto.STRING,
        number=8,
    )
    applied_teams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    effective_teams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=28,
    )
    creator: str = proto.Field(
        proto.STRING,
        number=10,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=11,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=19,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    unlimited_end_time: bool = proto.Field(
        proto.BOOL,
        number=45,
    )
    external_order_id: int = proto.Field(
        proto.INT64,
        number=13,
    )
    archived: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    last_modified_by_app: str = proto.Field(
        proto.STRING,
        number=15,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=16,
        message=timestamp_pb2.Timestamp,
    )
    notes: str = proto.Field(
        proto.STRING,
        number=17,
    )
    po_number: str = proto.Field(
        proto.STRING,
        number=18,
    )
    status: order_enums.OrderStatusEnum.OrderStatus = proto.Field(
        proto.ENUM,
        number=20,
        enum=order_enums.OrderStatusEnum.OrderStatus,
    )
    salesperson: str = proto.Field(
        proto.STRING,
        number=21,
    )
    secondary_salespeople: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=22,
    )
    secondary_traffickers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=24,
    )
    applied_labels: MutableSequence[applied_label.AppliedLabel] = proto.RepeatedField(
        proto.MESSAGE,
        number=25,
        message=applied_label.AppliedLabel,
    )
    effective_applied_labels: MutableSequence[
        applied_label.AppliedLabel
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=26,
        message=applied_label.AppliedLabel,
    )
    custom_field_values: MutableSequence[
        custom_field_value.CustomFieldValue
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=38,
        message=custom_field_value.CustomFieldValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
