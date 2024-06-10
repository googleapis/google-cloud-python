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

from google.shopping.type.types import types
import proto  # type: ignore

from google.shopping.merchant_products_v1beta.types import products_common

__protobuf__ = proto.module(
    package="google.shopping.merchant.products.v1beta",
    manifest={
        "ProductInput",
        "InsertProductInputRequest",
        "DeleteProductInputRequest",
    },
)


class ProductInput(proto.Message):
    r"""This resource represents input data you submit for a product, not
    the processed product that you see in Merchant Center, in Shopping
    ads, or across Google surfaces. Product inputs, rules and
    supplemental data source data are combined to create the processed
    [product][google.shopping.content.bundles.Products.Product].

    Required product input attributes to pass data validation checks are
    primarily defined in the `Products Data
    Specification <https://support.google.com/merchants/answer/188494>`__.

    The following attributes are required:
    [feedLabel][google.shopping.content.bundles.Products.feed_label],
    [contentLanguage][google.shopping.content.bundles.Products.content_language]
    and [offerId][google.shopping.content.bundles.Products.offer_id].

    After inserting, updating, or deleting a product input, it may take
    several minutes before the processed product can be retrieved.

    All fields in the product input and its sub-messages match the
    English name of their corresponding attribute in the vertical spec
    with `some
    exceptions <https://support.google.com/merchants/answer/7052112>`__.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. The name of the product input. Format:
            ``"{productinput.name=accounts/{account}/productInputs/{productinput}}"``
        product (str):
            Output only. The name of the processed product. Format:
            ``"{product.name=accounts/{account}/products/{product}}"``
        channel (google.shopping.type.types.Channel.ChannelEnum):
            Required. Immutable. The
            `channel <https://support.google.com/merchants/answer/7361332>`__
            of the product.
        offer_id (str):
            Required. Immutable. Your unique identifier for the product.
            This is the same for the product input and processed
            product. Leading and trailing whitespaces are stripped and
            multiple whitespaces are replaced by a single whitespace
            upon submission. See the `products data
            specification <https://support.google.com/merchants/answer/188494#id>`__
            for details.
        content_language (str):
            Required. Immutable. The two-letter `ISO
            639-1 <http://en.wikipedia.org/wiki/ISO_639-1>`__ language
            code for the product.
        feed_label (str):
            Required. Immutable. The `feed
            label <https://developers.google.com/shopping-content/guides/products/feed-labels>`__
            for the product.
        version_number (int):
            Optional. Represents the existing version (freshness) of the
            product, which can be used to preserve the right order when
            multiple updates are done at the same time.

            If set, the insertion is prevented when version number is
            lower than the current version number of the existing
            product. Re-insertion (for example, product refresh after 30
            days) can be performed with the current ``version_number``.

            Only supported for insertions into primary data sources.

            If the operation is prevented, the aborted exception will be
            thrown.

            This field is a member of `oneof`_ ``_version_number``.
        attributes (google.shopping.merchant_products_v1beta.types.Attributes):
            Optional. A list of product attributes.
        custom_attributes (MutableSequence[google.shopping.type.types.CustomAttribute]):
            Optional. A list of custom (merchant-provided) attributes.
            It can also be used for submitting any attribute of the data
            specification in its generic form (for example,
            ``{ "name": "size type", "value": "regular" }``). This is
            useful for submitting attributes not explicitly exposed by
            the API, such as additional attributes used for Buy on
            Google. Maximum allowed number of characters for each custom
            attribute is 10240 (represents sum of characters for name
            and value). Maximum 2500 custom attributes can be set per
            product, with total size of 102.4kB. Underscores in custom
            attribute names are replaced by spaces upon insertion.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    product: str = proto.Field(
        proto.STRING,
        number=2,
    )
    channel: types.Channel.ChannelEnum = proto.Field(
        proto.ENUM,
        number=3,
        enum=types.Channel.ChannelEnum,
    )
    offer_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=5,
    )
    feed_label: str = proto.Field(
        proto.STRING,
        number=6,
    )
    version_number: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )
    attributes: products_common.Attributes = proto.Field(
        proto.MESSAGE,
        number=8,
        message=products_common.Attributes,
    )
    custom_attributes: MutableSequence[types.CustomAttribute] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=types.CustomAttribute,
    )


class InsertProductInputRequest(proto.Message):
    r"""Request message for the InsertProductInput method.

    Attributes:
        parent (str):
            Required. The account where this product will
            be inserted. Format: accounts/{account}
        product_input (google.shopping.merchant_products_v1beta.types.ProductInput):
            Required. The product input to insert.
        data_source (str):
            Required. The primary or supplemental product data source
            name. If the product already exists and data source provided
            is different, then the product will be moved to a new data
            source. Format:
            ``accounts/{account}/dataSources/{datasource}``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    product_input: "ProductInput" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ProductInput",
    )
    data_source: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteProductInputRequest(proto.Message):
    r"""Request message for the DeleteProductInput method.

    Attributes:
        name (str):
            Required. The name of the product input
            resource to delete. Format:
            accounts/{account}/productInputs/{product}
        data_source (str):
            Required. The primary or supplemental data source from which
            the product input should be deleted. Format:
            ``accounts/{account}/dataSources/{datasource}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_source: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
