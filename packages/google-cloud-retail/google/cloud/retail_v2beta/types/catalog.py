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

from google.cloud.retail_v2beta.types import common, import_config

__protobuf__ = proto.module(
    package="google.cloud.retail.v2beta",
    manifest={
        "ProductLevelConfig",
        "CatalogAttribute",
        "AttributesConfig",
        "CompletionConfig",
        "MerchantCenterLink",
        "MerchantCenterLinkingConfig",
        "Catalog",
    },
)


class ProductLevelConfig(proto.Message):
    r"""Configures what level the product should be uploaded with
    regards to how users will be send events and how predictions
    will be made.

    Attributes:
        ingestion_product_type (str):
            The type of [Product][google.cloud.retail.v2beta.Product]s
            allowed to be ingested into the catalog. Acceptable values
            are:

            -  ``primary`` (default): You can ingest
               [Product][google.cloud.retail.v2beta.Product]s of all
               types. When ingesting a
               [Product][google.cloud.retail.v2beta.Product], its type
               will default to
               [Product.Type.PRIMARY][google.cloud.retail.v2beta.Product.Type.PRIMARY]
               if unset.
            -  ``variant`` (incompatible with Retail Search): You can
               only ingest
               [Product.Type.VARIANT][google.cloud.retail.v2beta.Product.Type.VARIANT]
               [Product][google.cloud.retail.v2beta.Product]s. This
               means
               [Product.primary_product_id][google.cloud.retail.v2beta.Product.primary_product_id]
               cannot be empty.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``variant`` and
            [merchant_center_product_id_field][google.cloud.retail.v2beta.ProductLevelConfig.merchant_center_product_id_field]
            is ``itemGroupId``, an INVALID_ARGUMENT error is returned.

            See `Product
            levels <https://cloud.google.com/retail/docs/catalog#product-levels>`__
            for more details.
        merchant_center_product_id_field (str):
            Which field of `Merchant Center
            Product </bigquery-transfer/docs/merchant-center-products-schema>`__
            should be imported as
            [Product.id][google.cloud.retail.v2beta.Product.id].
            Acceptable values are:

            -  ``offerId`` (default): Import ``offerId`` as the product
               ID.
            -  ``itemGroupId``: Import ``itemGroupId`` as the product
               ID. Notice that Retail API will choose one item from the
               ones with the same ``itemGroupId``, and use it to
               represent the item group.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``itemGroupId`` and
            [ingestion_product_type][google.cloud.retail.v2beta.ProductLevelConfig.ingestion_product_type]
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
            [Product][google.cloud.retail.v2beta.Product] is using this
            attribute in
            [Product.attributes][google.cloud.retail.v2beta.Product.attributes].
            Otherwise, this field is ``False``.

            [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
            can be pre-loaded by using
            [CatalogService.AddCatalogAttribute][google.cloud.retail.v2beta.CatalogService.AddCatalogAttribute],
            [CatalogService.ImportCatalogAttributes][], or
            [CatalogService.UpdateAttributesConfig][google.cloud.retail.v2beta.CatalogService.UpdateAttributesConfig]
            APIs. This field is ``False`` for pre-loaded
            [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]s.

            Only pre-loaded
            [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]s
            that are neither in use by products nor predefined can be
            deleted.
            [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]s
            that are either in use by products or are predefined cannot
            be deleted; however, their configuration properties will
            reset to default values upon removal request.

            After catalog changes, it takes about 10 minutes for this
            field to update.
        type_ (google.cloud.retail_v2beta.types.CatalogAttribute.AttributeType):
            Output only. The type of this attribute. This is derived
            from the attribute in
            [Product.attributes][google.cloud.retail.v2beta.Product.attributes].
        indexable_option (google.cloud.retail_v2beta.types.CatalogAttribute.IndexableOption):
            When
            [AttributesConfig.attribute_config_level][google.cloud.retail.v2beta.AttributesConfig.attribute_config_level]
            is CATALOG_LEVEL_ATTRIBUTE_CONFIG, if INDEXABLE_ENABLED
            attribute values are indexed so that it can be filtered,
            faceted, or boosted in
            [SearchService.Search][google.cloud.retail.v2beta.SearchService.Search].
        dynamic_facetable_option (google.cloud.retail_v2beta.types.CatalogAttribute.DynamicFacetableOption):
            If DYNAMIC_FACETABLE_ENABLED, attribute values are available
            for dynamic facet. Could only be DYNAMIC_FACETABLE_DISABLED
            if
            [CatalogAttribute.indexable_option][google.cloud.retail.v2beta.CatalogAttribute.indexable_option]
            is INDEXABLE_DISABLED. Otherwise, an INVALID_ARGUMENT error
            is returned.
        searchable_option (google.cloud.retail_v2beta.types.CatalogAttribute.SearchableOption):
            When
            [AttributesConfig.attribute_config_level][google.cloud.retail.v2beta.AttributesConfig.attribute_config_level]
            is CATALOG_LEVEL_ATTRIBUTE_CONFIG, if SEARCHABLE_ENABLED,
            attribute values are searchable by text queries in
            [SearchService.Search][google.cloud.retail.v2beta.SearchService.Search].

            If SEARCHABLE_ENABLED but attribute type is numerical,
            attribute values will not be searchable by text queries in
            [SearchService.Search][google.cloud.retail.v2beta.SearchService.Search],
            as there are no text values associated to numerical
            attributes.
        recommendations_filtering_option (google.cloud.retail_v2beta.types.RecommendationsFilteringOption):
            When
            [AttributesConfig.attribute_config_level][google.cloud.retail.v2beta.AttributesConfig.attribute_config_level]
            is CATALOG_LEVEL_ATTRIBUTE_CONFIG, if
            RECOMMENDATIONS_FILTERING_ENABLED, attribute values are
            filterable for recommendations. This option works for
            categorical features only, does not work for numerical
            features, inventory filtering.
        exact_searchable_option (google.cloud.retail_v2beta.types.CatalogAttribute.ExactSearchableOption):
            If EXACT_SEARCHABLE_ENABLED, attribute values will be exact
            searchable. This property only applies to textual custom
            attributes and requires indexable set to enabled to enable
            exact-searchable.
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

    class ExactSearchableOption(proto.Enum):
        r"""The status of the exact-searchable option of a catalog
        attribute.
        """
        EXACT_SEARCHABLE_OPTION_UNSPECIFIED = 0
        EXACT_SEARCHABLE_ENABLED = 1
        EXACT_SEARCHABLE_DISABLED = 2

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
    recommendations_filtering_option: common.RecommendationsFilteringOption = (
        proto.Field(
            proto.ENUM,
            number=8,
            enum=common.RecommendationsFilteringOption,
        )
    )
    exact_searchable_option: ExactSearchableOption = proto.Field(
        proto.ENUM,
        number=11,
        enum=ExactSearchableOption,
    )


class AttributesConfig(proto.Message):
    r"""Catalog level attribute config.

    Attributes:
        name (str):
            Required. Immutable. The fully qualified resource name of
            the attribute config. Format:
            ``projects/*/locations/*/catalogs/*/attributesConfig``
        catalog_attributes (MutableMapping[str, google.cloud.retail_v2beta.types.CatalogAttribute]):
            Enable attribute(s) config at catalog level. For example,
            indexable, dynamic_facetable, or searchable for each
            attribute.

            The key is catalog attribute's name. For example: ``color``,
            ``brands``, ``attributes.custom_attribute``, such as
            ``attributes.xyz``.

            The maximum number of catalog attributes allowed in a
            request is 1000.
        attribute_config_level (google.cloud.retail_v2beta.types.AttributeConfigLevel):
            Output only. The
            [AttributeConfigLevel][google.cloud.retail.v2beta.AttributeConfigLevel]
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
            [CompleteQueryRequest][google.cloud.retail.v2beta.CompleteQueryRequest].
        suggestions_input_config (google.cloud.retail_v2beta.types.CompletionDataInputConfig):
            Output only. The source data for the latest
            import of the autocomplete suggestion phrases.
        last_suggestions_import_operation (str):
            Output only. Name of the LRO corresponding to the latest
            suggestion terms list import.

            Can use
            [GetOperation][google.longrunning.Operations.GetOperation]
            API to retrieve the latest state of the Long Running
            Operation.
        denylist_input_config (google.cloud.retail_v2beta.types.CompletionDataInputConfig):
            Output only. The source data for the latest
            import of the autocomplete denylist phrases.
        last_denylist_import_operation (str):
            Output only. Name of the LRO corresponding to the latest
            denylist import.

            Can use
            [GetOperation][google.longrunning.Operations.GetOperation]
            API to retrieve the latest state of the Long Running
            Operation.
        allowlist_input_config (google.cloud.retail_v2beta.types.CompletionDataInputConfig):
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


class MerchantCenterLink(proto.Message):
    r"""Represents a link between a Merchant Center account and a
    branch. Once a link is established, products from the linked
    merchant center account will be streamed to the linked branch.

    Attributes:
        merchant_center_account_id (int):
            Required. The linked `Merchant center account
            id <https://developers.google.com/shopping-content/guides/accountstatuses>`__.
            The account must be a standalone account or a sub-account of
            a MCA.
        branch_id (str):
            The branch id (e.g. 0/1/2) within this catalog that products
            from merchant_center_account_id are streamed to. When
            updating this field, an empty value will use the currently
            configured default branch. However, changing the default
            branch later on won't change the linked branch here.

            A single branch id can only have one linked merchant center
            account id.
        destinations (MutableSequence[str]):
            String representing the destination to import for, all if
            left empty. List of possible values is given in `Included
            destination <https://support.google.com/merchants/answer/7501026>`__.
            List of allowed string values: "Shopping_ads",
            "Buy_on_google_listings", "Display_ads", "Local_inventory
            \_ads", "Free_listings", "Free_local_listings" NOTE: The
            string values are case sensitive.
        region_code (str):
            Region code of offers to accept. 2-letter Uppercase ISO
            3166-1 alpha-2 code. List of values can be found
            `here <https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry>`__
            under the ``region`` tag. If left blank no region filtering
            will be performed.

            Example value: ``US``.
        language_code (str):
            Language of the title/description and other string
            attributes. Use language tags defined by `BCP
            47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__. ISO
            639-1.

            This specifies the language of offers in Merchant Center
            that will be accepted. If empty no language filtering will
            be performed.

            Example value: ``en``.
    """

    merchant_center_account_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    branch_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    destinations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    region_code: str = proto.Field(
        proto.STRING,
        number=4,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=5,
    )


class MerchantCenterLinkingConfig(proto.Message):
    r"""Configures Merchant Center linking.
    Links contained in the config will be used to sync data from a
    Merchant Center account to a Cloud Retail branch.

    Attributes:
        links (MutableSequence[google.cloud.retail_v2beta.types.MerchantCenterLink]):
            Links between Merchant Center accounts and
            branches.
    """

    links: MutableSequence["MerchantCenterLink"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="MerchantCenterLink",
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
        product_level_config (google.cloud.retail_v2beta.types.ProductLevelConfig):
            Required. The product level configuration.
        merchant_center_linking_config (google.cloud.retail_v2beta.types.MerchantCenterLinkingConfig):
            The Merchant Center linking configuration.
            Once a link is added, the data stream from
            Merchant Center to Cloud Retail will be enabled
            automatically. The requester must have access to
            the merchant center account in order to make
            changes to this field.
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
    merchant_center_linking_config: "MerchantCenterLinkingConfig" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="MerchantCenterLinkingConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
