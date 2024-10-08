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
        "DataSourceReference",
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
        default_rule (google.shopping.merchant_datasources_v1beta.types.PrimaryProductDataSource.DefaultRule):
            Optional. Default rule management of the data
            source. If set, the linked data sources will be
            replaced.
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
                products. Note: Products management through the
                API is not possible for this channel.
        """
        CHANNEL_UNSPECIFIED = 0
        ONLINE_PRODUCTS = 1
        LOCAL_PRODUCTS = 2
        PRODUCTS = 3

    class DefaultRule(proto.Message):
        r"""Default rule management of the data source.

        Attributes:
            take_from_data_sources (MutableSequence[google.shopping.merchant_datasources_v1beta.types.DataSourceReference]):
                Required. The list of data sources linked in the `default
                rule <https://support.google.com/merchants/answer/7450276>`__.
                This list is ordered by the default rule priority of joining
                the data. It might include none or multiple references to
                ``self`` and supplemental data sources.

                The list must not be empty.

                To link the data source to the default rule, you need to add
                a new reference to this list (in sequential order).

                To unlink the data source from the default rule, you need to
                remove the given reference from this list. To create
                attribute rules that are different from the default rule,
                see `Set up your attribute
                rules <//support.google.com/merchants/answer/14994083>`__.

                Changing the order of this list will result in changing the
                priority of data sources in the default rule.

                For example, providing the following list: [``1001``,
                ``self``] will take attribute values from supplemental data
                source ``1001``, and fallback to ``self`` if the attribute
                is not set in ``1001``.
        """

        take_from_data_sources: MutableSequence[
            "DataSourceReference"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="DataSourceReference",
        )

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
    default_rule: DefaultRule = proto.Field(
        proto.MESSAGE,
        number=7,
        message=DefaultRule,
    )


class SupplementalProductDataSource(proto.Message):
    r"""The supplemental data source for local and online products.
    Supplemental API data sources must not have ``feedLabel`` and
    ``contentLanguage`` fields set. You can only use supplemental data
    sources to update existing products. For information about creating
    a supplemental data source, see `Create a supplemental data source
    and link it to the primary data
    source </merchant/api/guides/data-sources/overview#create-supplemental-data-source>`__.


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
        referencing_primary_data_sources (MutableSequence[google.shopping.merchant_datasources_v1beta.types.DataSourceReference]):
            Output only. The (unordered and deduplicated)
            list of all primary data sources linked to this
            data source in either default or custom rules.
            Supplemental data source cannot be deleted
            before all links are removed.
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
    referencing_primary_data_sources: MutableSequence[
        "DataSourceReference"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="DataSourceReference",
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


class DataSourceReference(proto.Message):
    r"""Data source reference can be used to manage related data
    sources within the data source service.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        self_ (bool):
            Self should be used to reference the primary
            data source itself.

            This field is a member of `oneof`_ ``data_source_id``.
        primary_data_source_name (str):
            Optional. The name of the primary data source. Format:
            ``accounts/{account}/dataSources/{datasource}``

            This field is a member of `oneof`_ ``data_source_id``.
        supplemental_data_source_name (str):
            Optional. The name of the supplemental data source. Format:
            ``accounts/{account}/dataSources/{datasource}``

            This field is a member of `oneof`_ ``data_source_id``.
    """

    self_: bool = proto.Field(
        proto.BOOL,
        number=1,
        oneof="data_source_id",
    )
    primary_data_source_name: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="data_source_id",
    )
    supplemental_data_source_name: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="data_source_id",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
