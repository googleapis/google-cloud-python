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
    package="google.shopping.merchant.datasources.v1beta",
    manifest={
        "PrimaryProductDataSource",
        "SupplementalProductDataSource",
        "LocalInventoryDataSource",
        "RegionalInventoryDataSource",
        "PromotionDataSource",
    },
)


class PrimaryProductDataSource(proto.Message):
    r"""The primary data source for local and online products.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        channel (google.shopping.merchant_datasources_v1beta.types.PrimaryProductDataSource.Channel):
            Required. Immutable. Specifies the type of
            data source channel.
        feed_label (str):
            Optional. Immutable. The feed label that is specified on the
            data source level.

            Must be less than or equal to 20 uppercase letters (A-Z),
            numbers (0-9), and dashes (-).

            See also `migration to feed
            labels <https://developers.google.com/shopping-content/guides/products/feed-labels>`__.

            ``feedLabel`` and ``contentLanguage`` must be either both
            set or unset for data sources with product content type.
            They must be set for data sources with a file input.

            If set, the data source will only accept products matching
            this combination. If unset, the data source will accept
            products without that restriction.

            This field is a member of `oneof`_ ``_feed_label``.
        content_language (str):
            Optional. Immutable. The two-letter ISO 639-1 language of
            the items in the data source.

            ``feedLabel`` and ``contentLanguage`` must be either both
            set or unset. The fields can only be unset for data sources
            without file input.

            If set, the data source will only accept products matching
            this combination. If unset, the data source will accept
            products without that restriction.

            This field is a member of `oneof`_ ``_content_language``.
        countries (MutableSequence[str]):
            Optional. The countries where the items may be displayed.
            Represented as a `CLDR territory
            code <https://github.com/unicode-org/cldr/blob/latest/common/main/en.xml>`__.
    """

    class Channel(proto.Enum):
        r"""Data Source Channel.

        Channel is used to distinguish between data sources for
        different product verticals.

        Values:
            CHANNEL_UNSPECIFIED (0):
                Not specified.
            ONLINE_PRODUCTS (1):
                Online product.
            LOCAL_PRODUCTS (2):
                Local product.
            PRODUCTS (3):
                Unified data source for both local and online
                products.
        """
        CHANNEL_UNSPECIFIED = 0
        ONLINE_PRODUCTS = 1
        LOCAL_PRODUCTS = 2
        PRODUCTS = 3

    channel: Channel = proto.Field(
        proto.ENUM,
        number=3,
        enum=Channel,
    )
    feed_label: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    countries: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )


class SupplementalProductDataSource(proto.Message):
    r"""The supplemental data source for local and online products.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        feed_label (str):
            Optional. Immutable. The feed label that is specified on the
            data source level.

            Must be less than or equal to 20 uppercase letters (A-Z),
            numbers (0-9), and dashes (-).

            See also `migration to feed
            labels <https://developers.google.com/shopping-content/guides/products/feed-labels>`__.

            ``feedLabel`` and ``contentLanguage`` must be either both
            set or unset for data sources with product content type.
            They must be set for data sources with a file input.

            If set, the data source will only accept products matching
            this combination. If unset, the data source will accept
            produts without that restriction.

            This field is a member of `oneof`_ ``_feed_label``.
        content_language (str):
            Optional. Immutable. The two-letter ISO 639-1 language of
            the items in the data source.

            ``feedLabel`` and ``contentLanguage`` must be either both
            set or unset. The fields can only be unset for data sources
            without file input.

            If set, the data source will only accept products matching
            this combination. If unset, the data source will accept
            produts without that restriction.

            This field is a member of `oneof`_ ``_content_language``.
    """

    feed_label: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )


class LocalInventoryDataSource(proto.Message):
    r"""The local inventory data source.

    Attributes:
        feed_label (str):
            Required. Immutable. The feed label of the offers to which
            the local inventory is provided.

            Must be less than or equal to 20 uppercase letters (A-Z),
            numbers (0-9), and dashes (-).

            See also `migration to feed
            labels <https://developers.google.com/shopping-content/guides/products/feed-labels>`__.
        content_language (str):
            Required. Immutable. The two-letter ISO 639-1
            language of the items to which the local
            inventory is provided.
    """

    feed_label: str = proto.Field(
        proto.STRING,
        number=4,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=5,
    )


class RegionalInventoryDataSource(proto.Message):
    r"""The regional inventory data source.

    Attributes:
        feed_label (str):
            Required. Immutable. The feed label of the offers to which
            the regional inventory is provided.

            Must be less than or equal to 20 uppercase letters (A-Z),
            numbers (0-9), and dashes (-).

            See also `migration to feed
            labels <https://developers.google.com/shopping-content/guides/products/feed-labels>`__.
        content_language (str):
            Required. Immutable. The two-letter ISO 639-1
            language of the items to which the regional
            inventory is provided.
    """

    feed_label: str = proto.Field(
        proto.STRING,
        number=4,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=5,
    )


class PromotionDataSource(proto.Message):
    r"""The promotion data source.

    Attributes:
        target_country (str):
            Required. Immutable. The target country used as part of the
            unique identifier. Represented as a `CLDR territory
            code <https://github.com/unicode-org/cldr/blob/latest/common/main/en.xml>`__.

            Promotions are only available in selected
            `countries <https://support.google.com/merchants/answer/4588460>`__.
        content_language (str):
            Required. Immutable. The two-letter ISO 639-1
            language of the items in the data source.
    """

    target_country: str = proto.Field(
        proto.STRING,
        number=1,
    )
    content_language: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
