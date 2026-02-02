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

from google.ads.datamanager_v1.types import item_parameter

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "CartData",
        "Item",
    },
)


class CartData(proto.Message):
    r"""The cart data associated with the event.

    Attributes:
        merchant_id (str):
            Optional. The Merchant Center ID associated
            with the items.
        merchant_feed_label (str):
            Optional. The Merchant Center feed label
            associated with the feed of the items.
        merchant_feed_language_code (str):
            Optional. The language code in ISO 639-1
            associated with the Merchant Center feed of the
            items.where your items are uploaded.
        transaction_discount (float):
            Optional. The sum of all discounts associated
            with the transaction.
        items (MutableSequence[google.ads.datamanager_v1.types.Item]):
            Optional. The list of items associated with
            the event.
    """

    merchant_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    merchant_feed_label: str = proto.Field(
        proto.STRING,
        number=2,
    )
    merchant_feed_language_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    transaction_discount: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )
    items: MutableSequence["Item"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Item",
    )


class Item(proto.Message):
    r"""Represents an item in the cart associated with the event.

    Attributes:
        merchant_product_id (str):
            Optional. The product ID within the Merchant
            Center account.
        quantity (int):
            Optional. The number of this item associated
            with the event.
        unit_price (float):
            Optional. The unit price excluding tax,
            shipping, and any transaction level discounts.
        item_id (str):
            Optional. A unique identifier to reference
            the item.
        additional_item_parameters (MutableSequence[google.ads.datamanager_v1.types.ItemParameter]):
            Optional. A bucket of any `event parameters related to an
            item <https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events>`__
            to be included within the event that were not already
            specified using other structured fields.
    """

    merchant_product_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    quantity: int = proto.Field(
        proto.INT64,
        number=2,
    )
    unit_price: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )
    item_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    additional_item_parameters: MutableSequence[item_parameter.ItemParameter] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message=item_parameter.ItemParameter,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
