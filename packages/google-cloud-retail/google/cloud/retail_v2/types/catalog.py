# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.retail_v2.types import common, import_config

__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={
        "ProductLevelConfig",
        "CatalogAttribute",
        "AttributesConfig",
        "CompletionConfig",
        "Catalog",
    },
)


class ProductLevelConfig(proto.Message):
    r"""Configures what level the product should be uploaded with
    regards to how users will be send events and how predictions
    will be made.

    Attributes:
        ingestion_product_type (str):
            The type of [Product][google.cloud.retail.v2.Product]s
            allowed to be ingested into the catalog. Acceptable values
            are:

            -  ``primary`` (default): You can ingest
               [Product][google.cloud.retail.v2.Product]s of all types.
               When ingesting a
               [Product][google.cloud.retail.v2.Product], its type will
               default to
               [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
               if unset.
            -  ``variant`` (incompatible with Retail Search): You can
               only ingest
               [Product.Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]
               [Product][google.cloud.retail.v2.Product]s. This means
               [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id]
               cannot be empty.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``variant`` and
            [merchant_center_product_id_field][google.cloud.retail.v2.ProductLevelConfig.merchant_center_product_id_field]
            is ``itemGroupId``, an INVALID_ARGUMENT error is returned.

            See `Product
            levels <https://cloud.google.com/retail/docs/catalog#product-levels>`__
            for more details.
        merchant_center_product_id_field (str):
            Which field of `Merchant Center
            Product </bigquery-transfer/docs/merchant-center-products-schema>`__
            should be imported as
            [Product.id][google.cloud.retail.v2.Product.id]. Acceptable
            values are:

            -  ``offerId`` (default): Import ``offerId`` as the product
               ID.
            -  ``itemGroupId``: Import ``itemGroupId`` as the product
               ID. Notice that Retail API will choose one item from the
               ones with the same ``itemGroupId``, and use it to
               represent the item group.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``itemGroupId`` and
            [ingestion_product_type][google.cloud.retail.v2.ProductLevelConfig.ingestion_product_type]
            is ``variant``, an INVALID_ARGUMENT error is returned.

            See `Product
            levels <https://cloud.google.com/retail/docs/catalog#product-levels>`__
            for more details.
    """

    ingestion_product_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    merchant_center_product_id_field: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CatalogAttribute(proto.Message):
    r"""Catalog level attribute config for an attribute. For example,
    if customers want to enable/disable facet for a specific
    attribute.

    Attributes:
        key (str):
            Required. Attribute name. For example: ``color``,
            ``brands``, ``attributes.custom_attribute``, such as
            ``attributes.xyz``. To be indexable, the attribute name can
            contain only alpha-numeric characters and underscores. For
            example, an attribute named ``attributes.abc_xyz`` can be
            indexed, but an attribute named ``attributes.abc-xyz``
            cannot be indexed.
        in_use (bool):
            Output only. Indicates whether this attribute has been used
            by any products. ``True`` if at least one
            [Product][google.cloud.retail.v2.Product] is using this
            attribute in
            [Product.attributes][google.cloud.retail.v2.Product.attributes].
            Otherwise, this field is ``False``.

            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]
            can be pre-loaded by using
            [CatalogService.AddCatalogAttribute][google.cloud.retail.v2.CatalogService.AddCatalogAttribute],
            [CatalogService.ImportCatalogAttributes][], or
            [CatalogService.UpdateAttributesConfig][google.cloud.retail.v2.CatalogService.UpdateAttributesConfig]
            APIs. This field is ``False`` for pre-loaded
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]s.

            Only pre-loaded
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]s
            that are neither in use by products nor predefined can be
            deleted.
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]s
            that are either in use by products or are predefined cannot
            be deleted; however, their configuration properties will
            reset to default values upon removal request.

            After catalog changes, it takes about 10 minutes for this
            field to update.
        type_ (google.cloud.retail_v2.types.CatalogAttribute.AttributeType):
            Output only. The type of this attribute. This is derived
            from the attribute in
            [Product.attributes][google.cloud.retail.v2.Product.attributes].
        indexable_option (google.cloud.retail_v2.types.CatalogAttribute.IndexableOption):
            When
            [AttributesConfig.attribute_config_level][google.cloud.retail.v2.AttributesConfig.attribute_config_level]
            is CATALOG_LEVEL_ATTRIBUTE_CONFIG, if INDEXABLE_ENABLED
            attribute values are indexed so that it can be filtered,
            faceted, or boosted in
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].
        dynamic_facetable_option (google.cloud.retail_v2.types.CatalogAttribute.DynamicFacetableOption):
            If DYNAMIC_FACETABLE_ENABLED, attribute values are available
            for dynamic facet. Could only be DYNAMIC_FACETABLE_DISABLED
            if
            [CatalogAttribute.indexable_option][google.cloud.retail.v2.CatalogAttribute.indexable_option]
            is INDEXABLE_DISABLED. Otherwise, an INVALID_ARGUMENT error
            is returned.
        searchable_option (google.cloud.retail_v2.types.CatalogAttribute.SearchableOption):
            When
            [AttributesConfig.attribute_config_level][google.cloud.retail.v2.AttributesConfig.attribute_config_level]
            is CATALOG_LEVEL_ATTRIBUTE_CONFIG, if SEARCHABLE_ENABLED,
            attribute values are searchable by text queries in
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].

            If SEARCHABLE_ENABLED but attribute type is numerical,
            attribute values will not be searchable by text queries in
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search],
            as there are no text values associated to numerical
            attributes.
    """

    class AttributeType(proto.Enum):
        r"""The type of an attribute."""
        UNKNOWN = 0
        TEXTUAL = 1
        NUMERICAL = 2

    class IndexableOption(proto.Enum):
        r"""The status of the indexable option of a catalog attribute."""
        INDEXABLE_OPTION_UNSPECIFIED = 0
        INDEXABLE_ENABLED = 1
        INDEXABLE_DISABLED = 2

    class DynamicFacetableOption(proto.Enum):
        r"""The status of the dynamic facetable option of a catalog
        attribute.
        """
        DYNAMIC_FACETABLE_OPTION_UNSPECIFIED = 0
        DYNAMIC_FACETABLE_ENABLED = 1
        DYNAMIC_FACETABLE_DISABLED = 2

    class SearchableOption(proto.Enum):
        r"""The status of the searchable option of a catalog attribute."""
        SEARCHABLE_OPTION_UNSPECIFIED = 0
        SEARCHABLE_ENABLED = 1
        SEARCHABLE_DISABLED = 2

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    in_use: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    type_: AttributeType = proto.Field(
        proto.ENUM,
        number=10,
        enum=AttributeType,
    )
    indexable_option: IndexableOption = proto.Field(
        proto.ENUM,
        number=5,
        enum=IndexableOption,
    )
    dynamic_facetable_option: DynamicFacetableOption = proto.Field(
        proto.ENUM,
        number=6,
        enum=DynamicFacetableOption,
    )
    searchable_option: SearchableOption = proto.Field(
        proto.ENUM,
        number=7,
        enum=SearchableOption,
    )


class AttributesConfig(proto.Message):
    r"""Catalog level attribute config.

    Attributes:
        name (str):
            Required. Immutable. The fully qualified resource name of
            the attribute config. Format:
            ``projects/*/locations/*/catalogs/*/attributesConfig``
        catalog_attributes (MutableMapping[str, google.cloud.retail_v2.types.CatalogAttribute]):
            Enable attribute(s) config at catalog level. For example,
            indexable, dynamic_facetable, or searchable for each
            attribute.

            The key is catalog attribute's name. For example: ``color``,
            ``brands``, ``attributes.custom_attribute``, such as
            ``attributes.xyz``.

            The maximum number of catalog attributes allowed in a
            request is 1000.
        attribute_config_level (google.cloud.retail_v2.types.AttributeConfigLevel):
            Output only. The
            [AttributeConfigLevel][google.cloud.retail.v2.AttributeConfigLevel]
            used for this catalog.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    catalog_attributes: MutableMapping[str, "CatalogAttribute"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message="CatalogAttribute",
    )
    attribute_config_level: common.AttributeConfigLevel = proto.Field(
        proto.ENUM,
        number=3,
        enum=common.AttributeConfigLevel,
    )


class CompletionConfig(proto.Message):
    r"""Catalog level autocomplete config for customers to customize
    autocomplete feature's settings.

    Attributes:
        name (str):
            Required. Immutable. Fully qualified name
            ``projects/*/locations/*/catalogs/*/completionConfig``
        matching_order (str):
            Specifies the matching order for autocomplete suggestions,
            e.g., a query consisting of 'sh' with 'out-of-order'
            specified would suggest "women's shoes", whereas a query of
            'red s' with 'exact-prefix' specified would suggest "red
            shoes". Currently supported values:

            -  'out-of-order'
            -  'exact-prefix'

            Default value: 'exact-prefix'.
        max_suggestions (int):
            The maximum number of autocomplete
            suggestions returned per term. Default value is
            20. If left unset or set to 0, then will
            fallback to default value.

            Value range is 1 to 20.
        min_prefix_length (int):
            The minimum number of characters needed to be
            typed in order to get suggestions. Default value
            is 2. If left unset or set to 0, then will
            fallback to default value.

            Value range is 1 to 20.
        auto_learning (bool):
            If set to true, the auto learning function is enabled. Auto
            learning uses user data to generate suggestions using ML
            techniques. Default value is false. Only after enabling auto
            learning can users use ``cloud-retail`` data in
            [CompleteQueryRequest][google.cloud.retail.v2.CompleteQueryRequest].
        suggestions_input_config (google.cloud.retail_v2.types.CompletionDataInputConfig):
            Output only. The source data for the latest
            import of the autocomplete suggestion phrases.
        last_suggestions_import_operation (str):
            Output only. Name of the LRO corresponding to the latest
            suggestion terms list import.

            Can use
            [GetOperation][google.longrunning.Operations.GetOperation]
            API to retrieve the latest state of the Long Running
            Operation.
        denylist_input_config (google.cloud.retail_v2.types.CompletionDataInputConfig):
            Output only. The source data for the latest
            import of the autocomplete denylist phrases.
        last_denylist_import_operation (str):
            Output only. Name of the LRO corresponding to the latest
            denylist import.

            Can use
            [GetOperation][google.longrunning.Operations.GetOperation]
            API to retrieve the latest state of the Long Running
            Operation.
        allowlist_input_config (google.cloud.retail_v2.types.CompletionDataInputConfig):
            Output only. The source data for the latest
            import of the autocomplete allowlist phrases.
        last_allowlist_import_operation (str):
            Output only. Name of the LRO corresponding to the latest
            allowlist import.

            Can use
            [GetOperation][google.longrunning.Operations.GetOperation]
            API to retrieve the latest state of the Long Running
            Operation.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    matching_order: str = proto.Field(
        proto.STRING,
        number=2,
    )
    max_suggestions: int = proto.Field(
        proto.INT32,
        number=3,
    )
    min_prefix_length: int = proto.Field(
        proto.INT32,
        number=4,
    )
    auto_learning: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    suggestions_input_config: import_config.CompletionDataInputConfig = proto.Field(
        proto.MESSAGE,
        number=5,
        message=import_config.CompletionDataInputConfig,
    )
    last_suggestions_import_operation: str = proto.Field(
        proto.STRING,
        number=6,
    )
    denylist_input_config: import_config.CompletionDataInputConfig = proto.Field(
        proto.MESSAGE,
        number=7,
        message=import_config.CompletionDataInputConfig,
    )
    last_denylist_import_operation: str = proto.Field(
        proto.STRING,
        number=8,
    )
    allowlist_input_config: import_config.CompletionDataInputConfig = proto.Field(
        proto.MESSAGE,
        number=9,
        message=import_config.CompletionDataInputConfig,
    )
    last_allowlist_import_operation: str = proto.Field(
        proto.STRING,
        number=10,
    )


class Catalog(proto.Message):
    r"""The catalog configuration.

    Attributes:
        name (str):
            Required. Immutable. The fully qualified
            resource name of the catalog.
        display_name (str):
            Required. Immutable. The catalog display name.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.
        product_level_config (google.cloud.retail_v2.types.ProductLevelConfig):
            Required. The product level configuration.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    product_level_config: "ProductLevelConfig" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ProductLevelConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
