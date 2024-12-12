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
        "Product",
        "GetProductRequest",
        "ListProductsRequest",
        "ListProductsResponse",
    },
)


class Product(proto.Message):
    r"""The processed product, built from multiple [product
    inputs][google.shopping.merchant.products.v1main.ProductInput] after
    applying rules and supplemental data sources. This processed product
    matches what is shown in your Merchant Center account and in
    Shopping ads and other surfaces across Google. Each product is built
    from exactly one primary data source product input, and multiple
    supplemental data source inputs. After inserting, updating, or
    deleting a product input, it may take several minutes before the
    updated processed product can be retrieved.

    All fields in the processed product and its sub-messages match the
    name of their corresponding attribute in the `Product data
    specification <https://support.google.com/merchants/answer/7052112>`__
    with some exceptions.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The name of the product. Format:
            ``"{product.name=accounts/{account}/products/{product}}"``
            where the last section ``product`` consists of 4 parts:
            channel~content_language~feed_label~offer_id example for
            product name is "accounts/123/products/online~en~US~sku123".
        channel (google.shopping.type.types.Channel.ChannelEnum):
            Output only. The
            `channel <https://support.google.com/merchants/answer/7361332>`__
            of the product.
        offer_id (str):
            Output only. Your unique identifier for the product. This is
            the same for the product input and processed product.
            Leading and trailing whitespaces are stripped and multiple
            whitespaces are replaced by a single whitespace upon
            submission. See the `product data
            specification <https://support.google.com/merchants/answer/188494#id>`__
            for details.
        content_language (str):
            Output only. The two-letter `ISO
            639-1 <http://en.wikipedia.org/wiki/ISO_639-1>`__ language
            code for the product.
        feed_label (str):
            Output only. The feed label for the product.
        data_source (str):
            Output only. The primary data source of the
            product.
        version_number (int):
            Output only. Represents the existing version (freshness) of
            the product, which can be used to preserve the right order
            when multiple updates are done at the same time.

            If set, the insertion is prevented when version number is
            lower than the current version number of the existing
            product. Re-insertion (for example, product refresh after 30
            days) can be performed with the current ``version_number``.

            Only supported for insertions into primary data sources.

            If the operation is prevented, the aborted exception will be
            thrown.

            This field is a member of `oneof`_ ``_version_number``.
        attributes (google.shopping.merchant_products_v1beta.types.Attributes):
            Output only. A list of product attributes.
        custom_attributes (MutableSequence[google.shopping.type.types.CustomAttribute]):
            Output only. A list of custom (merchant-provided)
            attributes. It can also be used to submit any attribute of
            the data specification in its generic form (for example,
            ``{ "name": "size type", "value": "regular" }``). This is
            useful for submitting attributes not explicitly exposed by
            the API, such as additional attributes used for Buy on
            Google.
        product_status (google.shopping.merchant_products_v1beta.types.ProductStatus):
            Output only. The status of a product, data
            validation issues, that is, information about a
            product computed asynchronously.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    channel: types.Channel.ChannelEnum = proto.Field(
        proto.ENUM,
        number=2,
        enum=types.Channel.ChannelEnum,
    )
    offer_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=4,
    )
    feed_label: str = proto.Field(
        proto.STRING,
        number=5,
    )
    data_source: str = proto.Field(
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
    product_status: products_common.ProductStatus = proto.Field(
        proto.MESSAGE,
        number=10,
        message=products_common.ProductStatus,
    )


class GetProductRequest(proto.Message):
    r"""Request message for the GetProduct method.

    Attributes:
        name (str):
            Required. The name of the product to retrieve. Format:
            ``accounts/{account}/products/{product}`` where the last
            section ``product`` consists of 4 parts:
            channel~content_language~feed_label~offer_id example for
            product name is "accounts/123/products/online~en~US~sku123".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListProductsRequest(proto.Message):
    r"""Request message for the ListProducts method.

    Attributes:
        parent (str):
            Required. The account to list processed
            products for. Format: accounts/{account}
        page_size (int):
            The maximum number of products to return. The
            service may return fewer than this value.
            The maximum value is 250; values above 250 will
            be coerced to 250. If unspecified, the maximum
            number of products will be returned.
        page_token (str):
            A page token, received from a previous ``ListProducts``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListProducts`` must match the call that provided the page
            token.
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


class ListProductsResponse(proto.Message):
    r"""Response message for the ListProducts method.

    Attributes:
        products (MutableSequence[google.shopping.merchant_products_v1beta.types.Product]):
            The processed products from the specified
            account. These are your processed products after
            applying rules and supplemental data sources.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    products: MutableSequence["Product"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Product",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
