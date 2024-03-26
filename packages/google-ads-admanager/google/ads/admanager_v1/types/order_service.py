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
import proto  # type: ignore

from google.ads.admanager_v1.types import applied_label

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Order",
        "GetOrderRequest",
        "ListOrdersRequest",
        "ListOrdersResponse",
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
            This value is required to create an order and
            has a maximum length of 255 characters.
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
            Company.Type.ADVERTISER, to which this order belongs. This
            attribute is required. Format:
            "networks/{network_code}/companies/{company_id}".
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
        status (google.ads.admanager_v1.types.Order.Status):
            Output only. The status of the Order.
        salesperson (str):
            Optional. The resource name of the User responsible for the
            sales of the Order. Format:
            "networks/{network_code}/users/{user_id}".
        secondary_salespeople (MutableSequence[str]):
            Optional. The resource names of the secondary salespeople
            associated with the order. Format:
            "networks/{network_code}/users/{user_id}".
        secondary_traffickers (MutableSequence[str]):
            Optional. The resource names of the secondary traffickers
            associated with the order. Format:
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
    """

    class Status(proto.Enum):
        r"""The status of an Order.

        Values:
            STATUS_UNSPECIFIED (0):
                Default value. This value is unused.
            DRAFT (2):
                Indicates that the Order has just been
                created but no approval has been requested yet.
            PENDING_APPROVAL (3):
                Indicates that a request for approval for the
                Order has been made.
            APPROVED (4):
                Indicates that the Order has been approved
                and is ready to serve.
            DISAPPROVED (5):
                Indicates that the Order has been disapproved
                and is not eligible to serve.
            PAUSED (6):
                This is a legacy state. Paused status should
                be checked on LineItems within the order.
            CANCELED (7):
                Indicates that the Order has been canceled
                and cannot serve.
            DELETED (8):
                Indicates that the Order has been deleted.
        """
        STATUS_UNSPECIFIED = 0
        DRAFT = 2
        PENDING_APPROVAL = 3
        APPROVED = 4
        DISAPPROVED = 5
        PAUSED = 6
        CANCELED = 7
        DELETED = 8

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
    status: Status = proto.Field(
        proto.ENUM,
        number=20,
        enum=Status,
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


class GetOrderRequest(proto.Message):
    r"""Request object for ``GetOrder`` method.

    Attributes:
        name (str):
            Required. The resource name of the Order. Format:
            ``networks/{network_code}/orders/{order_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListOrdersRequest(proto.Message):
    r"""Request object for ``ListOrders`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of Orders.
            Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of ``Orders`` to return. The
            service may return fewer than this value. If unspecified, at
            most 50 ``Orders`` will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListOrders`` call. Provide this to retrieve the subsequent
            page.

            When paginating, all other parameters provided to
            ``ListOrders`` must match the call that provided the page
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


class ListOrdersResponse(proto.Message):
    r"""Response object for ``ListOrdersRequest`` containing matching
    ``Order`` resources.

    Attributes:
        orders (MutableSequence[google.ads.admanager_v1.types.Order]):
            The ``Order`` from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of ``Orders``. If a filter was included in the
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

    orders: MutableSequence["Order"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Order",
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
