# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.cloud.retail_v2.types import common
from google.cloud.retail_v2.types import product as gcr_product
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2", manifest={"SearchRequest", "SearchResponse",},
)


class SearchRequest(proto.Message):
    r"""Request message for
    [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
    method.

    Attributes:
        placement (str):
            Required. The resource name of the search engine placement,
            such as
            ``projects/*/locations/global/catalogs/default_catalog/placements/default_search``.
            This field is used to identify the set of models that will
            be used to make the search.

            We currently support one placement with the following ID:

            -  ``default_search``.
        branch (str):
            The branch resource name, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/0``.

            Use "default_branch" as the branch ID or leave this field
            empty, to search products under the default branch.
        query (str):
            Raw search query.
        visitor_id (str):
            Required. A unique identifier for tracking visitors. For
            example, this could be implemented with an HTTP cookie,
            which should be able to uniquely identify a visitor on a
            single device. This unique identifier should not change if
            the visitor logs in or out of the website.

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.
        user_info (google.cloud.retail_v2.types.UserInfo):
            User information.
        page_size (int):
            Maximum number of [Product][google.cloud.retail.v2.Product]s
            to return. If unspecified, defaults to a reasonable value.
            The maximum allowed value is 120. Values above 120 will be
            coerced to 120.

            If this field is negative, an INVALID_ARGUMENT is returned.
        page_token (str):
            A page token
            [SearchResponse.next_page_token][google.cloud.retail.v2.SearchResponse.next_page_token],
            received from a previous
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
            must match the call that provided the page token. Otherwise,
            an INVALID_ARGUMENT error is returned.
        offset (int):
            A 0-indexed integer that specifies the current offset (that
            is, starting result location, amongst the
            [Product][google.cloud.retail.v2.Product]s deemed by the API
            as relevant) in search results. This field is only
            considered if
            [page_token][google.cloud.retail.v2.SearchRequest.page_token]
            is unset.

            If this field is negative, an INVALID_ARGUMENT is returned.
        filter (str):
            The filter syntax consists of an expression language for
            constructing a predicate from one or more fields of the
            products being filtered. Filter expression is
            case-sensitive.

            If this field is unrecognizable, an INVALID_ARGUMENT is
            returned.
        canonical_filter (str):
            The filter applied to every search request when quality
            improvement such as query expansion is needed. For example,
            if a query does not have enough results, an expanded query
            with
            [SearchRequest.canonical_filter][google.cloud.retail.v2.SearchRequest.canonical_filter]
            will be returned as a supplement of the original query. This
            field is strongly recommended to achieve high search
            quality.

            See
            [SearchRequest.filter][google.cloud.retail.v2.SearchRequest.filter]
            for more details about filter syntax.
        order_by (str):
            The order in which products are returned. Products can be
            ordered by a field in an
            [Product][google.cloud.retail.v2.Product] object. Leave it
            unset if ordered by relevance. OrderBy expression is
            case-sensitive.

            If this field is unrecognizable, an INVALID_ARGUMENT is
            returned.
        facet_specs (Sequence[google.cloud.retail_v2.types.SearchRequest.FacetSpec]):
            Facet specifications for faceted search. If empty, no facets
            are returned.

            A maximum of 100 values are allowed. Otherwise, an
            INVALID_ARGUMENT error is returned.
        dynamic_facet_spec (google.cloud.retail_v2.types.SearchRequest.DynamicFacetSpec):
            The specification for dynamically generated
            facets. Notice that only textual facets can be
            dynamically generated.
            This feature requires additional allowlisting.
            Contact Retail Support (retail-search-
            support@google.com) if you are interested in
            using dynamic facet feature.
        boost_spec (google.cloud.retail_v2.types.SearchRequest.BoostSpec):
            Boost specification to boost certain
            products.
        query_expansion_spec (google.cloud.retail_v2.types.SearchRequest.QueryExpansionSpec):
            The query expansion specification that
            specifies the conditions under which query
            expansion will occur.
        variant_rollup_keys (Sequence[str]):
            The keys to fetch and rollup the matching
            [variant][google.cloud.retail.v2.Product.Type.VARIANT]
            [Product][google.cloud.retail.v2.Product]s attributes. The
            attributes from all the matching
            [variant][google.cloud.retail.v2.Product.Type.VARIANT]
            [Product][google.cloud.retail.v2.Product]s are merged and
            de-duplicated. Notice that rollup
            [variant][google.cloud.retail.v2.Product.Type.VARIANT]
            [Product][google.cloud.retail.v2.Product]s attributes will
            lead to extra query latency. Maximum number of keys is 10.

            For
            [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info],
            a fulfillment type and a fulfillment ID must be provided in
            the format of "fulfillmentType.filfillmentId". E.g., in
            "pickupInStore.store123", "pickupInStore" is fulfillment
            type and "store123" is the store ID.

            Supported keys are:

            -  colorFamilies
            -  price
            -  originalPrice
            -  discount
            -  attributes.key, where key is any key in the
               [Product.attributes][google.cloud.retail.v2.Product.attributes]
               map.
            -  pickupInStore.id, where id is any [FulfillmentInfo.ids][]
               for type [FulfillmentInfo.Type.PICKUP_IN_STORE][].
            -  shipToStore.id, where id is any [FulfillmentInfo.ids][]
               for type [FulfillmentInfo.Type.SHIP_TO_STORE][].
            -  sameDayDelivery.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.SAME_DAY_DELIVERY][].
            -  nextDayDelivery.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.NEXT_DAY_DELIVERY][].
            -  customFulfillment1.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.CUSTOM_TYPE_1][].
            -  customFulfillment2.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.CUSTOM_TYPE_2][].
            -  customFulfillment3.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.CUSTOM_TYPE_3][].
            -  customFulfillment4.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.CUSTOM_TYPE_4][].
            -  customFulfillment5.id, where id is any
               [FulfillmentInfo.ids][] for type
               [FulfillmentInfo.Type.CUSTOM_TYPE_5][].

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.
        page_categories (Sequence[str]):
            The categories associated with a category page. Required for
            category navigation queries to achieve good search quality.
            The format should be the same as
            [UserEvent.page_categories][google.cloud.retail.v2.UserEvent.page_categories];

            To represent full path of category, use '>' sign to separate
            different hierarchies. If '>' is part of the category name,
            please replace it with other character(s).

            Category pages include special pages such as sales or
            promotions. For instance, a special sale page may have the
            category hierarchy: "pageCategories" : ["Sales > 2017 Black
            Friday Deals"].
    """

    class FacetSpec(proto.Message):
        r"""A facet specification to perform faceted search.
        Attributes:
            facet_key (google.cloud.retail_v2.types.SearchRequest.FacetSpec.FacetKey):
                Required. The facet key specification.
            limit (int):
                Maximum of facet values that should be returned for this
                facet. If unspecified, defaults to 20. The maximum allowed
                value is 300. Values above 300 will be coerced to 300.

                If this field is negative, an INVALID_ARGUMENT is returned.
            excluded_filter_keys (Sequence[str]):
                List of keys to exclude when faceting.

                By default,
                [FacetKey.key][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.key]
                is not excluded from the filter unless it is listed in this
                field.

                For example, suppose there are 100 products with color facet
                "Red" and 200 products with color facet "Blue". A query
                containing the filter "colorFamilies:ANY("Red")" and have
                "colorFamilies" as
                [FacetKey.key][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.key]
                will by default return the "Red" with count 100.

                If this field contains "colorFamilies", then the query
                returns both the "Red" with count 100 and "Blue" with count
                200, because the "colorFamilies" key is now excluded from
                the filter.

                A maximum of 100 values are allowed. Otherwise, an
                INVALID_ARGUMENT error is returned.
            enable_dynamic_position (bool):
                Enables dynamic position for this facet. If set to true, the
                position of this facet among all facets in the response is
                determined by Google Retail Search. It will be ordered
                together with dynamic facets if dynamic facets is enabled.
                If set to false, the position of this facet in the response
                will be the same as in the request, and it will be ranked
                before the facets with dynamic position enable and all
                dynamic facets.

                For example, you may always want to have rating facet
                returned in the response, but it's not necessarily to always
                display the rating facet at the top. In that case, you can
                set enable_dynamic_position to true so that the position of
                rating facet in response will be determined by Google Retail
                Search.

                Another example, assuming you have the following facets in
                the request:

                -  "rating", enable_dynamic_position = true

                -  "price", enable_dynamic_position = false

                -  "brands", enable_dynamic_position = false

                And also you have a dynamic facets enable, which will
                generate a facet 'gender'. Then the final order of the
                facets in the response can be ("price", "brands", "rating",
                "gender") or ("price", "brands", "gender", "rating") depends
                on how Google Retail Search orders "gender" and "rating"
                facets. However, notice that "price" and "brands" will
                always be ranked at 1st and 2nd position since their
                enable_dynamic_position are false.
        """

        class FacetKey(proto.Message):
            r"""Specifies how a facet is computed.
            Attributes:
                key (str):
                    Required. Supported textual and numerical facet keys in
                    [Product][google.cloud.retail.v2.Product] object, over which
                    the facet values are computed. Facet key is case-sensitive.

                    Allowed facet keys when
                    [FacetKey.query][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.query]
                    is not specified:

                    Textual facet keys:

                    -  brands
                    -  categories
                    -  genders
                    -  ageGroups
                    -  availability
                    -  colorFamilies
                    -  colors
                    -  sizes
                    -  materials
                    -  patterns
                    -  conditions
                    -  attributes.key
                    -  pickupInStore
                    -  shipToStore
                    -  sameDayDelivery
                    -  nextDayDelivery
                    -  customFulfillment1
                    -  customFulfillment2
                    -  customFulfillment3
                    -  customFulfillment4
                    -  customFulfillment5

                    Numeric facet keys:

                    -  price
                    -  discount
                    -  rating
                    -  ratingCount
                    -  attributes.key
                intervals (Sequence[google.cloud.retail_v2.types.Interval]):
                    Set only if values should be bucketized into
                    intervals. Must be set for facets with numerical
                    values. Must not be set for facet with text
                    values. Maximum number of intervals is 30.
                restricted_values (Sequence[str]):
                    Only get facet for the given restricted values. For example,
                    when using "pickupInStore" as key and set restricted values
                    to ["store123", "store456"], only facets for "store123" and
                    "store456" are returned. Only supported on textual fields
                    and fulfillments. Maximum is 20.

                    Must be set for the fulfillment facet keys:

                    -  pickupInStore

                    -  shipToStore

                    -  sameDayDelivery

                    -  nextDayDelivery

                    -  customFulfillment1

                    -  customFulfillment2

                    -  customFulfillment3

                    -  customFulfillment4

                    -  customFulfillment5
                prefixes (Sequence[str]):
                    Only get facet values that start with the
                    given string prefix. For example, suppose
                    "categories" has three values "Women > Shoe",
                    "Women > Dress" and "Men > Shoe". If set
                    "prefixes" to "Women", the "categories" facet
                    will give only "Women > Shoe" and "Women >
                    Dress". Only supported on textual fields.
                    Maximum is 10.
                contains (Sequence[str]):
                    Only get facet values that contains the given
                    strings. For example, suppose "categories" has
                    three values "Women > Shoe", "Women > Dress" and
                    "Men > Shoe". If set "contains" to "Shoe", the
                    "categories" facet will give only "Women > Shoe"
                    and "Men > Shoe". Only supported on textual
                    fields. Maximum is 10.
                order_by (str):
                    The order in which [Facet.values][] are returned.

                    Allowed values are:

                    -  "count desc", which means order by
                       [Facet.FacetValue.count][] descending.

                    -  "value desc", which means order by
                       [Facet.FacetValue.value][] descending. Only applies to
                       textual facets.

                    If not set, textual values are sorted in `natural
                    order <https://en.wikipedia.org/wiki/Natural_sort_order>`__;
                    numerical intervals are sorted in the order given by
                    [FacetSpec.FacetKey.intervals][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.intervals];
                    [FulfillmentInfo.ids][] are sorted in the order given by
                    [FacetSpec.FacetKey.restricted_values][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.restricted_values].
                query (str):
                    The query that is used to compute facet for the given facet
                    key. When provided, it will override the default behavior of
                    facet computation. The query syntax is the same as a filter
                    expression. See
                    [SearchRequest.filter][google.cloud.retail.v2.SearchRequest.filter]
                    for detail syntax and limitations. Notice that there is no
                    limitation on
                    [FacetKey.key][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.key]
                    when query is specified.

                    In the response, [FacetValue.value][] will be always "1" and
                    [FacetValue.count][] will be the number of results that
                    matches the query.

                    For example, you can set a customized facet for
                    "shipToStore", where
                    [FacetKey.key][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.key]
                    is "customizedShipToStore", and
                    [FacetKey.query][google.cloud.retail.v2.SearchRequest.FacetSpec.FacetKey.query]
                    is "availability: ANY("IN_STOCK") AND shipToStore:
                    ANY("123")". Then the facet will count the products that are
                    both in stock and ship to store "123".
            """

            key = proto.Field(proto.STRING, number=1,)
            intervals = proto.RepeatedField(
                proto.MESSAGE, number=2, message=common.Interval,
            )
            restricted_values = proto.RepeatedField(proto.STRING, number=3,)
            prefixes = proto.RepeatedField(proto.STRING, number=8,)
            contains = proto.RepeatedField(proto.STRING, number=9,)
            order_by = proto.Field(proto.STRING, number=4,)
            query = proto.Field(proto.STRING, number=5,)

        facet_key = proto.Field(
            proto.MESSAGE, number=1, message="SearchRequest.FacetSpec.FacetKey",
        )
        limit = proto.Field(proto.INT32, number=2,)
        excluded_filter_keys = proto.RepeatedField(proto.STRING, number=3,)
        enable_dynamic_position = proto.Field(proto.BOOL, number=4,)

    class DynamicFacetSpec(proto.Message):
        r"""The specifications of dynamically generated facets.
        Attributes:
            mode (google.cloud.retail_v2.types.SearchRequest.DynamicFacetSpec.Mode):
                Mode of the DynamicFacet feature. Defaults to
                [Mode.DISABLED][google.cloud.retail.v2.SearchRequest.DynamicFacetSpec.Mode.DISABLED]
                if it's unset.
        """

        class Mode(proto.Enum):
            r"""Enum to control DynamicFacet mode"""
            MODE_UNSPECIFIED = 0
            DISABLED = 1
            ENABLED = 2

        mode = proto.Field(
            proto.ENUM, number=1, enum="SearchRequest.DynamicFacetSpec.Mode",
        )

    class BoostSpec(proto.Message):
        r"""Boost specification to boost certain items.
        Attributes:
            condition_boost_specs (Sequence[google.cloud.retail_v2.types.SearchRequest.BoostSpec.ConditionBoostSpec]):
                Condition boost specifications. If a product
                matches multiple conditions in the
                specifictions, boost scores from these
                specifications are all applied and combined in a
                non-linear way. Maximum number of specifications
                is 10.
        """

        class ConditionBoostSpec(proto.Message):
            r"""Boost applies to products which match a condition.
            Attributes:
                condition (str):
                    An expression which specifies a boost condition. The syntax
                    and supported fields are the same as a filter expression.
                    See
                    [SearchRequest.filter][google.cloud.retail.v2.SearchRequest.filter]
                    for detail syntax and limitations.

                    Examples:

                    -  To boost products with product ID "product_1" or
                       "product_2", and color "Red" or "Blue":
                       ::

                          (id: ANY("product_1", "product_2"))
                          AND
                          (colorFamilies: ANY("Red", "Blue"))
                boost (float):
                    Strength of the condition boost, which should be in [-1, 1].
                    Negative boost means demotion. Default is 0.0.

                    Setting to 1.0 gives the item a big promotion. However, it
                    does not necessarily mean that the boosted item will be the
                    top result at all times, nor that other items will be
                    excluded. Results could still be shown even when none of
                    them matches the condition. And results that are
                    significantly more relevant to the search query can still
                    trump your heavily favored but irrelevant items.

                    Setting to -1.0 gives the item a big demotion. However,
                    results that are deeply relevant might still be shown. The
                    item will have an upstream battle to get a fairly high
                    ranking, but it is not blocked out completely.

                    Setting to 0.0 means no boost applied. The boosting
                    condition is ignored.
            """

            condition = proto.Field(proto.STRING, number=1,)
            boost = proto.Field(proto.FLOAT, number=2,)

        condition_boost_specs = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.BoostSpec.ConditionBoostSpec",
        )

    class QueryExpansionSpec(proto.Message):
        r"""Specification to determine under which conditions query
        expansion should occur.

        Attributes:
            condition (google.cloud.retail_v2.types.SearchRequest.QueryExpansionSpec.Condition):
                The condition under which query expansion should occur.
                Default to
                [Condition.DISABLED][google.cloud.retail.v2.SearchRequest.QueryExpansionSpec.Condition.DISABLED].
        """

        class Condition(proto.Enum):
            r"""Enum describing under which condition query expansion should
            occur.
            """
            CONDITION_UNSPECIFIED = 0
            DISABLED = 1
            AUTO = 3

        condition = proto.Field(
            proto.ENUM, number=1, enum="SearchRequest.QueryExpansionSpec.Condition",
        )

    placement = proto.Field(proto.STRING, number=1,)
    branch = proto.Field(proto.STRING, number=2,)
    query = proto.Field(proto.STRING, number=3,)
    visitor_id = proto.Field(proto.STRING, number=4,)
    user_info = proto.Field(proto.MESSAGE, number=5, message=common.UserInfo,)
    page_size = proto.Field(proto.INT32, number=7,)
    page_token = proto.Field(proto.STRING, number=8,)
    offset = proto.Field(proto.INT32, number=9,)
    filter = proto.Field(proto.STRING, number=10,)
    canonical_filter = proto.Field(proto.STRING, number=28,)
    order_by = proto.Field(proto.STRING, number=11,)
    facet_specs = proto.RepeatedField(proto.MESSAGE, number=12, message=FacetSpec,)
    dynamic_facet_spec = proto.Field(
        proto.MESSAGE, number=21, message=DynamicFacetSpec,
    )
    boost_spec = proto.Field(proto.MESSAGE, number=13, message=BoostSpec,)
    query_expansion_spec = proto.Field(
        proto.MESSAGE, number=14, message=QueryExpansionSpec,
    )
    variant_rollup_keys = proto.RepeatedField(proto.STRING, number=17,)
    page_categories = proto.RepeatedField(proto.STRING, number=23,)


class SearchResponse(proto.Message):
    r"""Response message for
    [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
    method.

    Attributes:
        results (Sequence[google.cloud.retail_v2.types.SearchResponse.SearchResult]):
            A list of matched items. The order represents
            the ranking.
        facets (Sequence[google.cloud.retail_v2.types.SearchResponse.Facet]):
            Results of facets requested by user.
        total_size (int):
            The estimated total count of matched items irrespective of
            pagination. The count of
            [results][google.cloud.retail.v2.SearchResponse.results]
            returned by pagination may be less than the
            [total_size][google.cloud.retail.v2.SearchResponse.total_size]
            that matches.
        corrected_query (str):
            If spell correction applies, the corrected
            query. Otherwise, empty.
        attribution_token (str):
            A unique search token. This should be included in the
            [UserEvent][google.cloud.retail.v2.UserEvent] logs resulting
            from this search, which enables accurate attribution of
            search model performance.
        next_page_token (str):
            A token that can be sent as
            [SearchRequest.page_token][google.cloud.retail.v2.SearchRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
        query_expansion_info (google.cloud.retail_v2.types.SearchResponse.QueryExpansionInfo):
            Query expansion information for the returned
            results.
        redirect_uri (str):
            The URI of a customer-defined redirect page. If redirect
            action is triggered, no search will be performed, and only
            [redirect_uri][google.cloud.retail.v2.SearchResponse.redirect_uri]
            and
            [attribution_token][google.cloud.retail.v2.SearchResponse.attribution_token]
            will be set in the response.
    """

    class SearchResult(proto.Message):
        r"""Represents the search results.
        Attributes:
            id (str):
                [Product.id][google.cloud.retail.v2.Product.id] of the
                searched [Product][google.cloud.retail.v2.Product].
            product (google.cloud.retail_v2.types.Product):
                The product data snippet in the search response. Only
                [Product.name][google.cloud.retail.v2.Product.name] is
                guaranteed to be populated.

                [Product.variants][google.cloud.retail.v2.Product.variants]
                contains the product variants that match the search query.
                If there are multiple product variants matching the query,
                top 5 most relevant product variants are returned and
                ordered by relevancy.

                If relevancy can be deternmined, use
                [matching_variant_fields][google.cloud.retail.v2.SearchResponse.SearchResult.matching_variant_fields]
                to look up matched product variants fields. If relevancy
                cannot be determined, e.g. when searching "shoe" all
                products in a shoe product can be a match, 5 product
                variants are returned but order is meaningless.
            matching_variant_count (int):
                The count of matched
                [variant][google.cloud.retail.v2.Product.Type.VARIANT]
                [Product][google.cloud.retail.v2.Product]s.
            matching_variant_fields (Sequence[google.cloud.retail_v2.types.SearchResponse.SearchResult.MatchingVariantFieldsEntry]):
                If a [variant][google.cloud.retail.v2.Product.Type.VARIANT]
                [Product][google.cloud.retail.v2.Product] matches the search
                query, this map indicates which
                [Product][google.cloud.retail.v2.Product] fields are
                matched. The key is the
                [Product.name][google.cloud.retail.v2.Product.name], the
                value is a field mask of the matched
                [Product][google.cloud.retail.v2.Product] fields. If matched
                attributes cannot be determined, this map will be empty.

                For example, a key "sku1" with field mask
                "products.color_info" indicates there is a match between
                "sku1" [ColorInfo][google.cloud.retail.v2.ColorInfo] and the
                query.
            variant_rollup_values (Sequence[google.cloud.retail_v2.types.SearchResponse.SearchResult.VariantRollupValuesEntry]):
                The rollup matching
                [variant][google.cloud.retail.v2.Product.Type.VARIANT]
                [Product][google.cloud.retail.v2.Product] attributes. The
                key is one of the
                [SearchRequest.variant_rollup_keys][google.cloud.retail.v2.SearchRequest.variant_rollup_keys].
                The values are the merged and de-duplicated
                [Product][google.cloud.retail.v2.Product] attributes. Notice
                that the rollup values are respect filter. For example, when
                filtering by "colorFamilies:ANY("red")" and rollup
                "colorFamilies", only "red" is returned.

                For textual and numerical attributes, the rollup values is a
                list of string or double values with type
                [google.protobuf.ListValue][google.protobuf.ListValue]. For
                example, if there are two variants with colors "red" and
                "blue", the rollup values are

                ::

                    { key: "colorFamilies"
                      value {
                        list_value {
                          values { string_value: "red" }
                          values { string_value: "blue" }
                         }
                      }
                    }

                For
                [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info],
                the rollup values is a double value with type
                [google.protobuf.Value][google.protobuf.Value]. For example:
                ``{key: "pickupInStore.store1" value { number_value: 10 }}``
                means a there are 10 variants in this product are available
                in the store "store1".
        """

        id = proto.Field(proto.STRING, number=1,)
        product = proto.Field(proto.MESSAGE, number=2, message=gcr_product.Product,)
        matching_variant_count = proto.Field(proto.INT32, number=3,)
        matching_variant_fields = proto.MapField(
            proto.STRING, proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
        )
        variant_rollup_values = proto.MapField(
            proto.STRING, proto.MESSAGE, number=5, message=struct_pb2.Value,
        )

    class Facet(proto.Message):
        r"""A facet result.
        Attributes:
            key (str):
                The key for this facet. E.g., "colorFamilies"
                or "price" or "attributes.attr1".
            values (Sequence[google.cloud.retail_v2.types.SearchResponse.Facet.FacetValue]):
                The facet values for this field.
            dynamic_facet (bool):
                Whether the facet is dynamically generated.
        """

        class FacetValue(proto.Message):
            r"""A facet value which contains value names and their count.
            Attributes:
                value (str):
                    Text value of a facet, such as "Black" for
                    facet "colorFamilies".
                interval (google.cloud.retail_v2.types.Interval):
                    Interval value for a facet, such as [10, 20) for facet
                    "price".
                count (int):
                    Number of items that have this facet value.
            """

            value = proto.Field(proto.STRING, number=1, oneof="facet_value",)
            interval = proto.Field(
                proto.MESSAGE, number=2, oneof="facet_value", message=common.Interval,
            )
            count = proto.Field(proto.INT64, number=3,)

        key = proto.Field(proto.STRING, number=1,)
        values = proto.RepeatedField(
            proto.MESSAGE, number=2, message="SearchResponse.Facet.FacetValue",
        )
        dynamic_facet = proto.Field(proto.BOOL, number=3,)

    class QueryExpansionInfo(proto.Message):
        r"""Information describing query expansion including whether
        expansion has occurred.

        Attributes:
            expanded_query (bool):
                Bool describing whether query expansion has
                occurred.
        """

        expanded_query = proto.Field(proto.BOOL, number=1,)

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(proto.MESSAGE, number=1, message=SearchResult,)
    facets = proto.RepeatedField(proto.MESSAGE, number=2, message=Facet,)
    total_size = proto.Field(proto.INT32, number=3,)
    corrected_query = proto.Field(proto.STRING, number=4,)
    attribution_token = proto.Field(proto.STRING, number=5,)
    next_page_token = proto.Field(proto.STRING, number=6,)
    query_expansion_info = proto.Field(
        proto.MESSAGE, number=7, message=QueryExpansionInfo,
    )
    redirect_uri = proto.Field(proto.STRING, number=10,)


__all__ = tuple(sorted(__protobuf__.manifest))
