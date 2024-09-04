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

from google.protobuf import struct_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1beta.types import chunk as gcd_chunk
from google.cloud.discoveryengine_v1beta.types import common
from google.cloud.discoveryengine_v1beta.types import document as gcd_document

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "SearchRequest",
        "SearchResponse",
    },
)


class SearchRequest(proto.Message):
    r"""Request message for
    [SearchService.Search][google.cloud.discoveryengine.v1beta.SearchService.Search]
    method.

    Attributes:
        serving_config (str):
            Required. The resource name of the Search serving config,
            such as
            ``projects/*/locations/global/collections/default_collection/engines/*/servingConfigs/default_serving_config``,
            or
            ``projects/*/locations/global/collections/default_collection/dataStores/default_data_store/servingConfigs/default_serving_config``.
            This field is used to identify the serving configuration
            name, set of models used to make the search.
        branch (str):
            The branch resource name, such as
            ``projects/*/locations/global/collections/default_collection/dataStores/default_data_store/branches/0``.

            Use ``default_branch`` as the branch ID or leave this field
            empty, to search documents under the default branch.
        query (str):
            Raw search query.
        image_query (google.cloud.discoveryengine_v1beta.types.SearchRequest.ImageQuery):
            Raw image query.
        page_size (int):
            Maximum number of
            [Document][google.cloud.discoveryengine.v1beta.Document]s to
            return. The maximum allowed value depends on the data type.
            Values above the maximum value are coerced to the maximum
            value.

            -  Websites with basic indexing: Default ``10``, Maximum
               ``25``.
            -  Websites with advanced indexing: Default ``25``, Maximum
               ``50``.
            -  Other: Default ``50``, Maximum ``100``.

            If this field is negative, an ``INVALID_ARGUMENT`` is
            returned.
        page_token (str):
            A page token received from a previous
            [SearchService.Search][google.cloud.discoveryengine.v1beta.SearchService.Search]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [SearchService.Search][google.cloud.discoveryengine.v1beta.SearchService.Search]
            must match the call that provided the page token. Otherwise,
            an ``INVALID_ARGUMENT`` error is returned.
        offset (int):
            A 0-indexed integer that specifies the current offset (that
            is, starting result location, amongst the
            [Document][google.cloud.discoveryengine.v1beta.Document]s
            deemed by the API as relevant) in search results. This field
            is only considered if
            [page_token][google.cloud.discoveryengine.v1beta.SearchRequest.page_token]
            is unset.

            If this field is negative, an ``INVALID_ARGUMENT`` is
            returned.
        data_store_specs (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.DataStoreSpec]):
            Specs defining dataStores to filter on in a
            search call and configurations for those
            dataStores. This is only considered for engines
            with multiple dataStores use case. For single
            dataStore within an engine, they should use the
            specs at the top level.
        filter (str):
            The filter syntax consists of an expression language for
            constructing a predicate from one or more fields of the
            documents being filtered. Filter expression is
            case-sensitive.

            If this field is unrecognizable, an ``INVALID_ARGUMENT`` is
            returned.

            Filtering in Vertex AI Search is done by mapping the LHS
            filter key to a key property defined in the Vertex AI Search
            backend -- this mapping is defined by the customer in their
            schema. For example a media customer might have a field
            'name' in their schema. In this case the filter would look
            like this: filter --> name:'ANY("king kong")'

            For more information about filtering including syntax and
            filter operators, see
            `Filter <https://cloud.google.com/generative-ai-app-builder/docs/filter-search-metadata>`__
        canonical_filter (str):
            The default filter that is applied when a user performs a
            search without checking any filters on the search page.

            The filter applied to every search request when quality
            improvement such as query expansion is needed. In the case a
            query does not have a sufficient amount of results this
            filter will be used to determine whether or not to enable
            the query expansion flow. The original filter will still be
            used for the query expanded search. This field is strongly
            recommended to achieve high search quality.

            For more information about filter syntax, see
            [SearchRequest.filter][google.cloud.discoveryengine.v1beta.SearchRequest.filter].
        order_by (str):
            The order in which documents are returned. Documents can be
            ordered by a field in an
            [Document][google.cloud.discoveryengine.v1beta.Document]
            object. Leave it unset if ordered by relevance. ``order_by``
            expression is case-sensitive.

            For more information on ordering the website search results,
            see `Order web search
            results <https://cloud.google.com/generative-ai-app-builder/docs/order-web-search-results>`__.
            For more information on ordering the healthcare search
            results, see `Order healthcare search
            results <https://cloud.google.com/generative-ai-app-builder/docs/order-hc-results>`__.
            If this field is unrecognizable, an ``INVALID_ARGUMENT`` is
            returned.
        user_info (google.cloud.discoveryengine_v1beta.types.UserInfo):
            Information about the end user. Highly recommended for
            analytics.
            [UserInfo.user_agent][google.cloud.discoveryengine.v1beta.UserInfo.user_agent]
            is used to deduce ``device_type`` for analytics.
        language_code (str):
            The BCP-47 language code, such as "en-US" or "sr-Latn". For
            more information, see `Standard
            fields <https://cloud.google.com/apis/design/standard_fields>`__.
            This field helps to better interpret the query. If a value
            isn't specified, the query language code is automatically
            detected, which may not be accurate.
        region_code (str):
            The Unicode country/region code (CLDR) of a location, such
            as "US" and "419". For more information, see `Standard
            fields <https://cloud.google.com/apis/design/standard_fields>`__.
            If set, then results will be boosted based on the
            region_code provided.
        facet_specs (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.FacetSpec]):
            Facet specifications for faceted search. If empty, no facets
            are returned.

            A maximum of 100 values are allowed. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.
        boost_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec):
            Boost specification to boost certain documents. For more
            information on boosting, see
            `Boosting <https://cloud.google.com/generative-ai-app-builder/docs/boost-search-results>`__
        params (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            Additional search parameters.

            For public website search only, supported values are:

            -  ``user_country_code``: string. Default empty. If set to
               non-empty, results are restricted or boosted based on the
               location provided. For example,
               ``user_country_code: "au"``

               For available codes see `Country
               Codes <https://developers.google.com/custom-search/docs/json_api_reference#countryCodes>`__

            -  ``search_type``: double. Default empty. Enables
               non-webpage searching depending on the value. The only
               valid non-default value is 1, which enables image
               searching. For example, ``search_type: 1``
        query_expansion_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.QueryExpansionSpec):
            The query expansion specification that
            specifies the conditions under which query
            expansion occurs.
        spell_correction_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.SpellCorrectionSpec):
            The spell correction specification that
            specifies the mode under which spell correction
            takes effect.
        user_pseudo_id (str):
            A unique identifier for tracking visitors. For example, this
            could be implemented with an HTTP cookie, which should be
            able to uniquely identify a visitor on a single device. This
            unique identifier should not change if the visitor logs in
            or out of the website.

            This field should NOT have a fixed value such as
            ``unknown_visitor``.

            This should be the same identifier as
            [UserEvent.user_pseudo_id][google.cloud.discoveryengine.v1beta.UserEvent.user_pseudo_id]
            and
            [CompleteQueryRequest.user_pseudo_id][google.cloud.discoveryengine.v1beta.CompleteQueryRequest.user_pseudo_id]

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an ``INVALID_ARGUMENT`` error
            is returned.
        content_search_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec):
            A specification for configuring the behavior
            of content search.
        embedding_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.EmbeddingSpec):
            Uses the provided embedding to do additional semantic
            document retrieval. The retrieval is based on the dot
            product of
            [SearchRequest.EmbeddingSpec.EmbeddingVector.vector][google.cloud.discoveryengine.v1beta.SearchRequest.EmbeddingSpec.EmbeddingVector.vector]
            and the document embedding that is provided in
            [SearchRequest.EmbeddingSpec.EmbeddingVector.field_path][google.cloud.discoveryengine.v1beta.SearchRequest.EmbeddingSpec.EmbeddingVector.field_path].

            If
            [SearchRequest.EmbeddingSpec.EmbeddingVector.field_path][google.cloud.discoveryengine.v1beta.SearchRequest.EmbeddingSpec.EmbeddingVector.field_path]
            is not provided, it will use
            [ServingConfig.EmbeddingConfig.field_path][google.cloud.discoveryengine.v1beta.ServingConfig.embedding_config].
        ranking_expression (str):
            The ranking expression controls the customized ranking on
            retrieval documents. This overrides
            [ServingConfig.ranking_expression][google.cloud.discoveryengine.v1beta.ServingConfig.ranking_expression].
            The ranking expression is a single function or multiple
            functions that are joined by "+".

            -  ranking_expression = function, { " + ", function };

            Supported functions:

            -  double \* relevance_score
            -  double \* dotProduct(embedding_field_path)

            Function variables:

            -  ``relevance_score``: pre-defined keywords, used for
               measure relevance between query and document.
            -  ``embedding_field_path``: the document embedding field
               used with query embedding vector.
            -  ``dotProduct``: embedding function between
               embedding_field_path and query embedding vector.

            Example ranking expression:

            ::

               If document has an embedding field doc_embedding, the ranking expression
               could be `0.5 * relevance_score + 0.3 * dotProduct(doc_embedding)`.
        safe_search (bool):
            Whether to turn on safe search. This is only
            supported for website search.
        user_labels (MutableMapping[str, str]):
            The user labels applied to a resource must meet the
            following requirements:

            -  Each resource can have multiple labels, up to a maximum
               of 64.
            -  Each label must be a key-value pair.
            -  Keys have a minimum length of 1 character and a maximum
               length of 63 characters and cannot be empty. Values can
               be empty and have a maximum length of 63 characters.
            -  Keys and values can contain only lowercase letters,
               numeric characters, underscores, and dashes. All
               characters must use UTF-8 encoding, and international
               characters are allowed.
            -  The key portion of a label must be unique. However, you
               can use the same key with multiple resources.
            -  Keys must start with a lowercase letter or international
               character.

            See `Google Cloud
            Document <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__
            for more details.
        natural_language_query_understanding_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.NaturalLanguageQueryUnderstandingSpec):
            If ``naturalLanguageQueryUnderstandingSpec`` is not
            specified, no additional natural language query
            understanding will be done.
        search_as_you_type_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.SearchAsYouTypeSpec):
            Search as you type configuration. Only supported for the
            [IndustryVertical.MEDIA][google.cloud.discoveryengine.v1beta.IndustryVertical.MEDIA]
            vertical.
        session (str):
            The session resource name. Optional.

            Session allows users to do multi-turn /search API calls or
            coordination between /search API calls and /answer API
            calls.

            Example #1 (multi-turn /search API calls):

            1. Call /search API with the auto-session mode (see below).
            2. Call /search API with the session ID generated in the
               first call. Here, the previous search query gets
               considered in query standing. I.e., if the first query is
               "How did Alphabet do in 2022?" and the current query is
               "How about 2023?", the current query will be interpreted
               as "How did Alphabet do in 2023?".

            Example #2 (coordination between /search API calls and
            /answer API calls):

            1. Call /search API with the auto-session mode (see below).
            2. Call /answer API with the session ID generated in the
               first call. Here, the answer generation happens in the
               context of the search results from the first search call.

            Auto-session mode: when ``projects/.../sessions/-`` is used,
            a new session gets automatically created. Otherwise, users
            can use the create-session API to create a session manually.

            Multi-turn Search feature is currently at private GA stage.
            Please use v1alpha or v1beta version instead before we
            launch this feature to public GA. Or ask for allowlisting
            through Google Support team.
        session_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.SessionSpec):
            Session specification.

            Can be used only when ``session`` is set.
        relevance_threshold (google.cloud.discoveryengine_v1beta.types.SearchRequest.RelevanceThreshold):
            The relevance threshold of the search
            results.
            Default to Google defined threshold, leveraging
            a balance of precision and recall to deliver
            both highly accurate results and comprehensive
            coverage of relevant information.
    """

    class RelevanceThreshold(proto.Enum):
        r"""The relevance threshold of the search results. The higher
        relevance threshold is, the higher relevant results are shown
        and the less number of results are returned.

        Values:
            RELEVANCE_THRESHOLD_UNSPECIFIED (0):
                Default value. In this case, server behavior
                defaults to Google defined threshold.
            LOWEST (1):
                Lowest relevance threshold.
            LOW (2):
                Low relevance threshold.
            MEDIUM (3):
                Medium relevance threshold.
            HIGH (4):
                High relevance threshold.
        """
        RELEVANCE_THRESHOLD_UNSPECIFIED = 0
        LOWEST = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4

    class ImageQuery(proto.Message):
        r"""Specifies the image query input.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            image_bytes (str):
                Base64 encoded image bytes. Supported image
                formats: JPEG, PNG, and BMP.

                This field is a member of `oneof`_ ``image``.
        """

        image_bytes: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="image",
        )

    class DataStoreSpec(proto.Message):
        r"""A struct to define data stores to filter on in a search call and
        configurations for those data stores. Otherwise, an
        ``INVALID_ARGUMENT`` error is returned.

        Attributes:
            data_store (str):
                Required. Full resource name of
                [DataStore][google.cloud.discoveryengine.v1beta.DataStore],
                such as
                ``projects/{project}/locations/{location}/collections/{collection_id}/dataStores/{data_store_id}``.
        """

        data_store: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class FacetSpec(proto.Message):
        r"""A facet specification to perform faceted search.

        Attributes:
            facet_key (google.cloud.discoveryengine_v1beta.types.SearchRequest.FacetSpec.FacetKey):
                Required. The facet key specification.
            limit (int):
                Maximum facet values that are returned for this facet. If
                unspecified, defaults to 20. The maximum allowed value is
                300. Values above 300 are coerced to 300. For aggregation in
                healthcare search, when the [FacetKey.key] is
                "healthcare_aggregation_key", the limit will be overridden
                to 10,000 internally, regardless of the value set here.

                If this field is negative, an ``INVALID_ARGUMENT`` is
                returned.
            excluded_filter_keys (MutableSequence[str]):
                List of keys to exclude when faceting.

                By default,
                [FacetKey.key][google.cloud.discoveryengine.v1beta.SearchRequest.FacetSpec.FacetKey.key]
                is not excluded from the filter unless it is listed in this
                field.

                Listing a facet key in this field allows its values to
                appear as facet results, even when they are filtered out of
                search results. Using this field does not affect what search
                results are returned.

                For example, suppose there are 100 documents with the color
                facet "Red" and 200 documents with the color facet "Blue". A
                query containing the filter "color:ANY("Red")" and having
                "color" as
                [FacetKey.key][google.cloud.discoveryengine.v1beta.SearchRequest.FacetSpec.FacetKey.key]
                would by default return only "Red" documents in the search
                results, and also return "Red" with count 100 as the only
                color facet. Although there are also blue documents
                available, "Blue" would not be shown as an available facet
                value.

                If "color" is listed in "excludedFilterKeys", then the query
                returns the facet values "Red" with count 100 and "Blue"
                with count 200, because the "color" key is now excluded from
                the filter. Because this field doesn't affect search
                results, the search results are still correctly filtered to
                return only "Red" documents.

                A maximum of 100 values are allowed. Otherwise, an
                ``INVALID_ARGUMENT`` error is returned.
            enable_dynamic_position (bool):
                Enables dynamic position for this facet. If set to true, the
                position of this facet among all facets in the response is
                determined automatically. If dynamic facets are enabled, it
                is ordered together. If set to false, the position of this
                facet in the response is the same as in the request, and it
                is ranked before the facets with dynamic position enable and
                all dynamic facets.

                For example, you may always want to have rating facet
                returned in the response, but it's not necessarily to always
                display the rating facet at the top. In that case, you can
                set enable_dynamic_position to true so that the position of
                rating facet in response is determined automatically.

                Another example, assuming you have the following facets in
                the request:

                -  "rating", enable_dynamic_position = true

                -  "price", enable_dynamic_position = false

                -  "brands", enable_dynamic_position = false

                And also you have a dynamic facets enabled, which generates
                a facet ``gender``. Then the final order of the facets in
                the response can be ("price", "brands", "rating", "gender")
                or ("price", "brands", "gender", "rating") depends on how
                API orders "gender" and "rating" facets. However, notice
                that "price" and "brands" are always ranked at first and
                second position because their enable_dynamic_position is
                false.
        """

        class FacetKey(proto.Message):
            r"""Specifies how a facet is computed.

            Attributes:
                key (str):
                    Required. Supported textual and numerical facet keys in
                    [Document][google.cloud.discoveryengine.v1beta.Document]
                    object, over which the facet values are computed. Facet key
                    is case-sensitive.
                intervals (MutableSequence[google.cloud.discoveryengine_v1beta.types.Interval]):
                    Set only if values should be bucketed into
                    intervals. Must be set for facets with numerical
                    values. Must not be set for facet with text
                    values. Maximum number of intervals is 30.
                restricted_values (MutableSequence[str]):
                    Only get facet for the given restricted values. Only
                    supported on textual fields. For example, suppose "category"
                    has three values "Action > 2022", "Action > 2021" and
                    "Sci-Fi > 2022". If set "restricted_values" to "Action >
                    2022", the "category" facet only contains "Action > 2022".
                    Only supported on textual fields. Maximum is 10.
                prefixes (MutableSequence[str]):
                    Only get facet values that start with the
                    given string prefix. For example, suppose
                    "category" has three values "Action > 2022",
                    "Action > 2021" and "Sci-Fi > 2022". If set
                    "prefixes" to "Action", the "category" facet
                    only contains "Action > 2022" and "Action >
                    2021". Only supported on textual fields. Maximum
                    is 10.
                contains (MutableSequence[str]):
                    Only get facet values that contain the given
                    strings. For example, suppose "category" has
                    three values "Action > 2022", "Action > 2021"
                    and "Sci-Fi > 2022". If set "contains" to
                    "2022", the "category" facet only contains
                    "Action > 2022" and "Sci-Fi > 2022". Only
                    supported on textual fields. Maximum is 10.
                case_insensitive (bool):
                    True to make facet keys case insensitive when
                    getting faceting values with prefixes or
                    contains; false otherwise.
                order_by (str):
                    The order in which documents are returned.

                    Allowed values are:

                    -  "count desc", which means order by
                       [SearchResponse.Facet.values.count][google.cloud.discoveryengine.v1beta.SearchResponse.Facet.FacetValue.count]
                       descending.

                    -  "value desc", which means order by
                       [SearchResponse.Facet.values.value][google.cloud.discoveryengine.v1beta.SearchResponse.Facet.FacetValue.value]
                       descending. Only applies to textual facets.

                    If not set, textual values are sorted in `natural
                    order <https://en.wikipedia.org/wiki/Natural_sort_order>`__;
                    numerical intervals are sorted in the order given by
                    [FacetSpec.FacetKey.intervals][google.cloud.discoveryengine.v1beta.SearchRequest.FacetSpec.FacetKey.intervals].
            """

            key: str = proto.Field(
                proto.STRING,
                number=1,
            )
            intervals: MutableSequence[common.Interval] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message=common.Interval,
            )
            restricted_values: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=3,
            )
            prefixes: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=4,
            )
            contains: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=5,
            )
            case_insensitive: bool = proto.Field(
                proto.BOOL,
                number=6,
            )
            order_by: str = proto.Field(
                proto.STRING,
                number=7,
            )

        facet_key: "SearchRequest.FacetSpec.FacetKey" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.FacetSpec.FacetKey",
        )
        limit: int = proto.Field(
            proto.INT32,
            number=2,
        )
        excluded_filter_keys: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        enable_dynamic_position: bool = proto.Field(
            proto.BOOL,
            number=4,
        )

    class BoostSpec(proto.Message):
        r"""Boost specification to boost certain documents.

        Attributes:
            condition_boost_specs (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec.ConditionBoostSpec]):
                Condition boost specifications. If a document
                matches multiple conditions in the
                specifictions, boost scores from these
                specifications are all applied and combined in a
                non-linear way. Maximum number of specifications
                is 20.
        """

        class ConditionBoostSpec(proto.Message):
            r"""Boost applies to documents which match a condition.

            Attributes:
                condition (str):
                    An expression which specifies a boost condition. The syntax
                    and supported fields are the same as a filter expression.
                    See
                    [SearchRequest.filter][google.cloud.discoveryengine.v1beta.SearchRequest.filter]
                    for detail syntax and limitations.

                    Examples:

                    -  To boost documents with document ID "doc_1" or "doc_2",
                       and color "Red" or "Blue":
                       ``(document_id: ANY("doc_1", "doc_2")) AND (color: ANY("Red", "Blue"))``
                boost (float):
                    Strength of the condition boost, which should be in [-1, 1].
                    Negative boost means demotion. Default is 0.0.

                    Setting to 1.0 gives the document a big promotion. However,
                    it does not necessarily mean that the boosted document will
                    be the top result at all times, nor that other documents
                    will be excluded. Results could still be shown even when
                    none of them matches the condition. And results that are
                    significantly more relevant to the search query can still
                    trump your heavily favored but irrelevant documents.

                    Setting to -1.0 gives the document a big demotion. However,
                    results that are deeply relevant might still be shown. The
                    document will have an upstream battle to get a fairly high
                    ranking, but it is not blocked out completely.

                    Setting to 0.0 means no boost applied. The boosting
                    condition is ignored. Only one of the (condition, boost)
                    combination or the boost_control_spec below are set. If both
                    are set then the global boost is ignored and the more
                    fine-grained boost_control_spec is applied.
                boost_control_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec):
                    Complex specification for custom ranking
                    based on customer defined attribute value.
            """

            class BoostControlSpec(proto.Message):
                r"""Specification for custom ranking based on customer specified
                attribute value. It provides more controls for customized
                ranking than the simple (condition, boost) combination above.

                Attributes:
                    field_name (str):
                        The name of the field whose value will be
                        used to determine the boost amount.
                    attribute_type (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.AttributeType):
                        The attribute type to be used to determine the boost amount.
                        The attribute value can be derived from the field value of
                        the specified field_name. In the case of numerical it is
                        straightforward i.e. attribute_value =
                        numerical_field_value. In the case of freshness however,
                        attribute_value = (time.now() - datetime_field_value).
                    interpolation_type (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.InterpolationType):
                        The interpolation type to be applied to
                        connect the control points listed below.
                    control_points (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.ControlPoint]):
                        The control points used to define the curve. The monotonic
                        function (defined through the interpolation_type above)
                        passes through the control points listed here.
                """

                class AttributeType(proto.Enum):
                    r"""The attribute(or function) for which the custom ranking is to
                    be applied.

                    Values:
                        ATTRIBUTE_TYPE_UNSPECIFIED (0):
                            Unspecified AttributeType.
                        NUMERICAL (1):
                            The value of the numerical field will be used to dynamically
                            update the boost amount. In this case, the attribute_value
                            (the x value) of the control point will be the actual value
                            of the numerical field for which the boost_amount is
                            specified.
                        FRESHNESS (2):
                            For the freshness use case the attribute value will be the
                            duration between the current time and the date in the
                            datetime field specified. The value must be formatted as an
                            XSD ``dayTimeDuration`` value (a restricted subset of an ISO
                            8601 duration value). The pattern for this is:
                            ``[nD][T[nH][nM][nS]]``. For example, ``5D``, ``3DT12H30M``,
                            ``T24H``.
                    """
                    ATTRIBUTE_TYPE_UNSPECIFIED = 0
                    NUMERICAL = 1
                    FRESHNESS = 2

                class InterpolationType(proto.Enum):
                    r"""The interpolation type to be applied. Default will be linear
                    (Piecewise Linear).

                    Values:
                        INTERPOLATION_TYPE_UNSPECIFIED (0):
                            Interpolation type is unspecified. In this
                            case, it defaults to Linear.
                        LINEAR (1):
                            Piecewise linear interpolation will be
                            applied.
                    """
                    INTERPOLATION_TYPE_UNSPECIFIED = 0
                    LINEAR = 1

                class ControlPoint(proto.Message):
                    r"""The control points used to define the curve. The curve
                    defined through these control points can only be monotonically
                    increasing or decreasing(constant values are acceptable).

                    Attributes:
                        attribute_value (str):
                            Can be one of:

                            1. The numerical field value.
                            2. The duration spec for freshness: The value must be
                               formatted as an XSD ``dayTimeDuration`` value (a
                               restricted subset of an ISO 8601 duration value). The
                               pattern for this is: ``[nD][T[nH][nM][nS]]``.
                        boost_amount (float):
                            The value between -1 to 1 by which to boost the score if the
                            attribute_value evaluates to the value specified above.
                    """

                    attribute_value: str = proto.Field(
                        proto.STRING,
                        number=1,
                    )
                    boost_amount: float = proto.Field(
                        proto.FLOAT,
                        number=2,
                    )

                field_name: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                attribute_type: "SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.AttributeType" = proto.Field(
                    proto.ENUM,
                    number=2,
                    enum="SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.AttributeType",
                )
                interpolation_type: "SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.InterpolationType" = proto.Field(
                    proto.ENUM,
                    number=3,
                    enum="SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.InterpolationType",
                )
                control_points: MutableSequence[
                    "SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.ControlPoint"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=4,
                    message="SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec.ControlPoint",
                )

            condition: str = proto.Field(
                proto.STRING,
                number=1,
            )
            boost: float = proto.Field(
                proto.FLOAT,
                number=2,
            )
            boost_control_spec: "SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec" = proto.Field(
                proto.MESSAGE,
                number=3,
                message="SearchRequest.BoostSpec.ConditionBoostSpec.BoostControlSpec",
            )

        condition_boost_specs: MutableSequence[
            "SearchRequest.BoostSpec.ConditionBoostSpec"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.BoostSpec.ConditionBoostSpec",
        )

    class QueryExpansionSpec(proto.Message):
        r"""Specification to determine under which conditions query
        expansion should occur.

        Attributes:
            condition (google.cloud.discoveryengine_v1beta.types.SearchRequest.QueryExpansionSpec.Condition):
                The condition under which query expansion should occur.
                Default to
                [Condition.DISABLED][google.cloud.discoveryengine.v1beta.SearchRequest.QueryExpansionSpec.Condition.DISABLED].
            pin_unexpanded_results (bool):
                Whether to pin unexpanded results. If this
                field is set to true, unexpanded products are
                always at the top of the search results,
                followed by the expanded results.
        """

        class Condition(proto.Enum):
            r"""Enum describing under which condition query expansion should
            occur.

            Values:
                CONDITION_UNSPECIFIED (0):
                    Unspecified query expansion condition. In this case, server
                    behavior defaults to
                    [Condition.DISABLED][google.cloud.discoveryengine.v1beta.SearchRequest.QueryExpansionSpec.Condition.DISABLED].
                DISABLED (1):
                    Disabled query expansion. Only the exact search query is
                    used, even if
                    [SearchResponse.total_size][google.cloud.discoveryengine.v1beta.SearchResponse.total_size]
                    is zero.
                AUTO (2):
                    Automatic query expansion built by the Search
                    API.
            """
            CONDITION_UNSPECIFIED = 0
            DISABLED = 1
            AUTO = 2

        condition: "SearchRequest.QueryExpansionSpec.Condition" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SearchRequest.QueryExpansionSpec.Condition",
        )
        pin_unexpanded_results: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    class SpellCorrectionSpec(proto.Message):
        r"""The specification for query spell correction.

        Attributes:
            mode (google.cloud.discoveryengine_v1beta.types.SearchRequest.SpellCorrectionSpec.Mode):
                The mode under which spell correction replaces the original
                search query. Defaults to
                [Mode.AUTO][google.cloud.discoveryengine.v1beta.SearchRequest.SpellCorrectionSpec.Mode.AUTO].
        """

        class Mode(proto.Enum):
            r"""Enum describing under which mode spell correction should
            occur.

            Values:
                MODE_UNSPECIFIED (0):
                    Unspecified spell correction mode. In this case, server
                    behavior defaults to
                    [Mode.AUTO][google.cloud.discoveryengine.v1beta.SearchRequest.SpellCorrectionSpec.Mode.AUTO].
                SUGGESTION_ONLY (1):
                    Search API tries to find a spelling suggestion. If a
                    suggestion is found, it is put in the
                    [SearchResponse.corrected_query][google.cloud.discoveryengine.v1beta.SearchResponse.corrected_query].
                    The spelling suggestion won't be used as the search query.
                AUTO (2):
                    Automatic spell correction built by the
                    Search API. Search will be based on the
                    corrected query if found.
            """
            MODE_UNSPECIFIED = 0
            SUGGESTION_ONLY = 1
            AUTO = 2

        mode: "SearchRequest.SpellCorrectionSpec.Mode" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SearchRequest.SpellCorrectionSpec.Mode",
        )

    class ContentSearchSpec(proto.Message):
        r"""A specification for configuring the behavior of content
        search.

        Attributes:
            snippet_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SnippetSpec):
                If ``snippetSpec`` is not specified, snippets are not
                included in the search response.
            summary_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SummarySpec):
                If ``summarySpec`` is not specified, summaries are not
                included in the search response.
            extractive_content_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.ExtractiveContentSpec):
                If there is no extractive_content_spec provided, there will
                be no extractive answer in the search response.
            search_result_mode (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SearchResultMode):
                Specifies the search result mode. If unspecified, the search
                result mode defaults to ``DOCUMENTS``.
            chunk_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.ChunkSpec):
                Specifies the chunk spec to be returned from the search
                response. Only available if the
                [SearchRequest.ContentSearchSpec.search_result_mode][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.search_result_mode]
                is set to
                [CHUNKS][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS]
        """

        class SearchResultMode(proto.Enum):
            r"""Specifies the search result mode. If unspecified, the search result
            mode defaults to ``DOCUMENTS``.

            Values:
                SEARCH_RESULT_MODE_UNSPECIFIED (0):
                    Default value.
                DOCUMENTS (1):
                    Returns documents in the search result.
                CHUNKS (2):
                    Returns chunks in the search result. Only available if the
                    [DataStore.DocumentProcessingConfig.chunking_config][] is
                    specified.
            """
            SEARCH_RESULT_MODE_UNSPECIFIED = 0
            DOCUMENTS = 1
            CHUNKS = 2

        class SnippetSpec(proto.Message):
            r"""A specification for configuring snippets in a search
            response.

            Attributes:
                max_snippet_count (int):
                    [DEPRECATED] This field is deprecated. To control snippet
                    return, use ``return_snippet`` field. For backwards
                    compatibility, we will return snippet if max_snippet_count >
                    0.
                reference_only (bool):
                    [DEPRECATED] This field is deprecated and will have no
                    affect on the snippet.
                return_snippet (bool):
                    If ``true``, then return snippet. If no snippet can be
                    generated, we return "No snippet is available for this
                    page." A ``snippet_status`` with ``SUCCESS`` or
                    ``NO_SNIPPET_AVAILABLE`` will also be returned.
            """

            max_snippet_count: int = proto.Field(
                proto.INT32,
                number=1,
            )
            reference_only: bool = proto.Field(
                proto.BOOL,
                number=2,
            )
            return_snippet: bool = proto.Field(
                proto.BOOL,
                number=3,
            )

        class SummarySpec(proto.Message):
            r"""A specification for configuring a summary returned in a
            search response.

            Attributes:
                summary_result_count (int):
                    The number of top results to generate the summary from. If
                    the number of results returned is less than
                    ``summaryResultCount``, the summary is generated from all of
                    the results.

                    At most 10 results for documents mode, or 50 for chunks
                    mode, can be used to generate a summary. The chunks mode is
                    used when
                    [SearchRequest.ContentSearchSpec.search_result_mode][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.search_result_mode]
                    is set to
                    [CHUNKS][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS].
                include_citations (bool):
                    Specifies whether to include citations in the summary. The
                    default value is ``false``.

                    When this field is set to ``true``, summaries include
                    in-line citation numbers.

                    Example summary including citations:

                    BigQuery is Google Cloud's fully managed and completely
                    serverless enterprise data warehouse [1]. BigQuery supports
                    all data types, works across clouds, and has built-in
                    machine learning and business intelligence, all within a
                    unified platform [2, 3].

                    The citation numbers refer to the returned search results
                    and are 1-indexed. For example, [1] means that the sentence
                    is attributed to the first search result. [2, 3] means that
                    the sentence is attributed to both the second and third
                    search results.
                ignore_adversarial_query (bool):
                    Specifies whether to filter out adversarial queries. The
                    default value is ``false``.

                    Google employs search-query classification to detect
                    adversarial queries. No summary is returned if the search
                    query is classified as an adversarial query. For example, a
                    user might ask a question regarding negative comments about
                    the company or submit a query designed to generate unsafe,
                    policy-violating output. If this field is set to ``true``,
                    we skip generating summaries for adversarial queries and
                    return fallback messages instead.
                ignore_non_summary_seeking_query (bool):
                    Specifies whether to filter out queries that are not
                    summary-seeking. The default value is ``false``.

                    Google employs search-query classification to detect
                    summary-seeking queries. No summary is returned if the
                    search query is classified as a non-summary seeking query.
                    For example, ``why is the sky blue`` and
                    ``Who is the best soccer player in the world?`` are
                    summary-seeking queries, but ``SFO airport`` and
                    ``world cup 2026`` are not. They are most likely
                    navigational queries. If this field is set to ``true``, we
                    skip generating summaries for non-summary seeking queries
                    and return fallback messages instead.
                ignore_low_relevant_content (bool):
                    Specifies whether to filter out queries that have low
                    relevance. The default value is ``false``.

                    If this field is set to ``false``, all search results are
                    used regardless of relevance to generate answers. If set to
                    ``true``, only queries with high relevance search results
                    will generate answers.
                model_prompt_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec):
                    If specified, the spec will be used to modify
                    the prompt provided to the LLM.
                language_code (str):
                    Language code for Summary. Use language tags defined by
                    `BCP47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__.
                    Note: This is an experimental feature.
                model_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec):
                    If specified, the spec will be used to modify
                    the model specification provided to the LLM.
                use_semantic_chunks (bool):
                    If true, answer will be generated from most
                    relevant chunks from top search results. This
                    feature will improve summary quality. Note that
                    with this feature enabled, not all top search
                    results will be referenced and included in the
                    reference list, so the citation source index
                    only points to the search results listed in the
                    reference list.
            """

            class ModelPromptSpec(proto.Message):
                r"""Specification of the prompt to use with the model.

                Attributes:
                    preamble (str):
                        Text at the beginning of the prompt that
                        instructs the assistant. Examples are available
                        in the user guide.
                """

                preamble: str = proto.Field(
                    proto.STRING,
                    number=1,
                )

            class ModelSpec(proto.Message):
                r"""Specification of the model.

                Attributes:
                    version (str):
                        The model version used to generate the summary.

                        Supported values are:

                        -  ``stable``: string. Default value when no value is
                           specified. Uses a generally available, fine-tuned model.
                           For more information, see `Answer generation model
                           versions and
                           lifecycle <https://cloud.google.com/generative-ai-app-builder/docs/answer-generation-models>`__.
                        -  ``preview``: string. (Public preview) Uses a preview
                           model. For more information, see `Answer generation model
                           versions and
                           lifecycle <https://cloud.google.com/generative-ai-app-builder/docs/answer-generation-models>`__.
                """

                version: str = proto.Field(
                    proto.STRING,
                    number=1,
                )

            summary_result_count: int = proto.Field(
                proto.INT32,
                number=1,
            )
            include_citations: bool = proto.Field(
                proto.BOOL,
                number=2,
            )
            ignore_adversarial_query: bool = proto.Field(
                proto.BOOL,
                number=3,
            )
            ignore_non_summary_seeking_query: bool = proto.Field(
                proto.BOOL,
                number=4,
            )
            ignore_low_relevant_content: bool = proto.Field(
                proto.BOOL,
                number=9,
            )
            model_prompt_spec: "SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec" = proto.Field(
                proto.MESSAGE,
                number=5,
                message="SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec",
            )
            language_code: str = proto.Field(
                proto.STRING,
                number=6,
            )
            model_spec: "SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec" = (
                proto.Field(
                    proto.MESSAGE,
                    number=7,
                    message="SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec",
                )
            )
            use_semantic_chunks: bool = proto.Field(
                proto.BOOL,
                number=8,
            )

        class ExtractiveContentSpec(proto.Message):
            r"""A specification for configuring the extractive content in a
            search response.

            Attributes:
                max_extractive_answer_count (int):
                    The maximum number of extractive answers returned in each
                    search result.

                    An extractive answer is a verbatim answer extracted from the
                    original document, which provides a precise and contextually
                    relevant answer to the search query.

                    If the number of matching answers is less than the
                    ``max_extractive_answer_count``, return all of the answers.
                    Otherwise, return the ``max_extractive_answer_count``.

                    At most five answers are returned for each
                    [SearchResult][google.cloud.discoveryengine.v1beta.SearchResponse.SearchResult].
                max_extractive_segment_count (int):
                    The max number of extractive segments returned in each
                    search result. Only applied if the
                    [DataStore][google.cloud.discoveryengine.v1beta.DataStore]
                    is set to
                    [DataStore.ContentConfig.CONTENT_REQUIRED][google.cloud.discoveryengine.v1beta.DataStore.ContentConfig.CONTENT_REQUIRED]
                    or
                    [DataStore.solution_types][google.cloud.discoveryengine.v1beta.DataStore.solution_types]
                    is
                    [SOLUTION_TYPE_CHAT][google.cloud.discoveryengine.v1beta.SolutionType.SOLUTION_TYPE_CHAT].

                    An extractive segment is a text segment extracted from the
                    original document that is relevant to the search query, and,
                    in general, more verbose than an extractive answer. The
                    segment could then be used as input for LLMs to generate
                    summaries and answers.

                    If the number of matching segments is less than
                    ``max_extractive_segment_count``, return all of the
                    segments. Otherwise, return the
                    ``max_extractive_segment_count``.
                return_extractive_segment_score (bool):
                    Specifies whether to return the confidence score from the
                    extractive segments in each search result. This feature is
                    available only for new or allowlisted data stores. To
                    allowlist your data store, contact your Customer Engineer.
                    The default value is ``false``.
                num_previous_segments (int):
                    Specifies whether to also include the adjacent from each
                    selected segments. Return at most ``num_previous_segments``
                    segments before each selected segments.
                num_next_segments (int):
                    Return at most ``num_next_segments`` segments after each
                    selected segments.
            """

            max_extractive_answer_count: int = proto.Field(
                proto.INT32,
                number=1,
            )
            max_extractive_segment_count: int = proto.Field(
                proto.INT32,
                number=2,
            )
            return_extractive_segment_score: bool = proto.Field(
                proto.BOOL,
                number=3,
            )
            num_previous_segments: int = proto.Field(
                proto.INT32,
                number=4,
            )
            num_next_segments: int = proto.Field(
                proto.INT32,
                number=5,
            )

        class ChunkSpec(proto.Message):
            r"""Specifies the chunk spec to be returned from the search response.
            Only available if the
            [SearchRequest.ContentSearchSpec.search_result_mode][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.search_result_mode]
            is set to
            [CHUNKS][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS]

            Attributes:
                num_previous_chunks (int):
                    The number of previous chunks to be returned
                    of the current chunk. The maximum allowed value
                    is 3. If not specified, no previous chunks will
                    be returned.
                num_next_chunks (int):
                    The number of next chunks to be returned of
                    the current chunk. The maximum allowed value is
                    3. If not specified, no next chunks will be
                    returned.
            """

            num_previous_chunks: int = proto.Field(
                proto.INT32,
                number=1,
            )
            num_next_chunks: int = proto.Field(
                proto.INT32,
                number=2,
            )

        snippet_spec: "SearchRequest.ContentSearchSpec.SnippetSpec" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.ContentSearchSpec.SnippetSpec",
        )
        summary_spec: "SearchRequest.ContentSearchSpec.SummarySpec" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="SearchRequest.ContentSearchSpec.SummarySpec",
        )
        extractive_content_spec: "SearchRequest.ContentSearchSpec.ExtractiveContentSpec" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="SearchRequest.ContentSearchSpec.ExtractiveContentSpec",
        )
        search_result_mode: "SearchRequest.ContentSearchSpec.SearchResultMode" = (
            proto.Field(
                proto.ENUM,
                number=4,
                enum="SearchRequest.ContentSearchSpec.SearchResultMode",
            )
        )
        chunk_spec: "SearchRequest.ContentSearchSpec.ChunkSpec" = proto.Field(
            proto.MESSAGE,
            number=5,
            message="SearchRequest.ContentSearchSpec.ChunkSpec",
        )

    class EmbeddingSpec(proto.Message):
        r"""The specification that uses customized query embedding vector
        to do semantic document retrieval.

        Attributes:
            embedding_vectors (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.EmbeddingSpec.EmbeddingVector]):
                The embedding vector used for retrieval.
                Limit to 1.
        """

        class EmbeddingVector(proto.Message):
            r"""Embedding vector.

            Attributes:
                field_path (str):
                    Embedding field path in schema.
                vector (MutableSequence[float]):
                    Query embedding vector.
            """

            field_path: str = proto.Field(
                proto.STRING,
                number=1,
            )
            vector: MutableSequence[float] = proto.RepeatedField(
                proto.FLOAT,
                number=2,
            )

        embedding_vectors: MutableSequence[
            "SearchRequest.EmbeddingSpec.EmbeddingVector"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.EmbeddingSpec.EmbeddingVector",
        )

    class NaturalLanguageQueryUnderstandingSpec(proto.Message):
        r"""Specification to enable natural language understanding
        capabilities for search requests.

        Attributes:
            filter_extraction_condition (google.cloud.discoveryengine_v1beta.types.SearchRequest.NaturalLanguageQueryUnderstandingSpec.FilterExtractionCondition):
                The condition under which filter extraction should occur.
                Default to [Condition.DISABLED][].
            geo_search_query_detection_field_names (MutableSequence[str]):
                Field names used for location-based filtering, where
                geolocation filters are detected in natural language search
                queries. Only valid when the FilterExtractionCondition is
                set to ``ENABLED``.

                If this field is set, it overrides the field names set in
                [ServingConfig.geo_search_query_detection_field_names][google.cloud.discoveryengine.v1beta.ServingConfig.geo_search_query_detection_field_names].
        """

        class FilterExtractionCondition(proto.Enum):
            r"""Enum describing under which condition filter extraction
            should occur.

            Values:
                CONDITION_UNSPECIFIED (0):
                    Server behavior defaults to [Condition.DISABLED][].
                DISABLED (1):
                    Disables NL filter extraction.
                ENABLED (2):
                    Enables NL filter extraction.
            """
            CONDITION_UNSPECIFIED = 0
            DISABLED = 1
            ENABLED = 2

        filter_extraction_condition: "SearchRequest.NaturalLanguageQueryUnderstandingSpec.FilterExtractionCondition" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SearchRequest.NaturalLanguageQueryUnderstandingSpec.FilterExtractionCondition",
        )
        geo_search_query_detection_field_names: MutableSequence[
            str
        ] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class SearchAsYouTypeSpec(proto.Message):
        r"""Specification for search as you type in search requests.

        Attributes:
            condition (google.cloud.discoveryengine_v1beta.types.SearchRequest.SearchAsYouTypeSpec.Condition):
                The condition under which search as you type should occur.
                Default to
                [Condition.DISABLED][google.cloud.discoveryengine.v1beta.SearchRequest.SearchAsYouTypeSpec.Condition.DISABLED].
        """

        class Condition(proto.Enum):
            r"""Enum describing under which condition search as you type
            should occur.

            Values:
                CONDITION_UNSPECIFIED (0):
                    Server behavior defaults to
                    [Condition.DISABLED][google.cloud.discoveryengine.v1beta.SearchRequest.SearchAsYouTypeSpec.Condition.DISABLED].
                DISABLED (1):
                    Disables Search As You Type.
                ENABLED (2):
                    Enables Search As You Type.
            """
            CONDITION_UNSPECIFIED = 0
            DISABLED = 1
            ENABLED = 2

        condition: "SearchRequest.SearchAsYouTypeSpec.Condition" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SearchRequest.SearchAsYouTypeSpec.Condition",
        )

    class SessionSpec(proto.Message):
        r"""Session specification.

        Multi-turn Search feature is currently at private GA stage.
        Please use v1alpha or v1beta version instead before we launch
        this feature to public GA. Or ask for allowlisting through
        Google Support team.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            query_id (str):
                If set, the search result gets stored to the "turn"
                specified by this query ID.

                Example: Let's say the session looks like this: session {
                name: ".../sessions/xxx" turns { query { text: "What is
                foo?" query_id: ".../questions/yyy" } answer: "Foo is ..." }
                turns { query { text: "How about bar then?" query_id:
                ".../questions/zzz" } } }

                The user can call /search API with a request like this:

                ::

                   session: ".../sessions/xxx"
                   session_spec { query_id: ".../questions/zzz" }

                Then, the API stores the search result, associated with the
                last turn. The stored search result can be used by a
                subsequent /answer API call (with the session ID and the
                query ID specified). Also, it is possible to call /search
                and /answer in parallel with the same session ID & query ID.
            search_result_persistence_count (int):
                The number of top search results to persist. The persisted
                search results can be used for the subsequent /answer api
                call.

                This field is simliar to the ``summary_result_count`` field
                in
                [SearchRequest.ContentSearchSpec.SummarySpec.summary_result_count][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SummarySpec.summary_result_count].

                At most 10 results for documents mode, or 50 for chunks
                mode.

                This field is a member of `oneof`_ ``_search_result_persistence_count``.
        """

        query_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        search_result_persistence_count: int = proto.Field(
            proto.INT32,
            number=2,
            optional=True,
        )

    serving_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    branch: str = proto.Field(
        proto.STRING,
        number=2,
    )
    query: str = proto.Field(
        proto.STRING,
        number=3,
    )
    image_query: ImageQuery = proto.Field(
        proto.MESSAGE,
        number=19,
        message=ImageQuery,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )
    offset: int = proto.Field(
        proto.INT32,
        number=6,
    )
    data_store_specs: MutableSequence[DataStoreSpec] = proto.RepeatedField(
        proto.MESSAGE,
        number=32,
        message=DataStoreSpec,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=7,
    )
    canonical_filter: str = proto.Field(
        proto.STRING,
        number=29,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=8,
    )
    user_info: common.UserInfo = proto.Field(
        proto.MESSAGE,
        number=21,
        message=common.UserInfo,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=35,
    )
    region_code: str = proto.Field(
        proto.STRING,
        number=36,
    )
    facet_specs: MutableSequence[FacetSpec] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=FacetSpec,
    )
    boost_spec: BoostSpec = proto.Field(
        proto.MESSAGE,
        number=10,
        message=BoostSpec,
    )
    params: MutableMapping[str, struct_pb2.Value] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=11,
        message=struct_pb2.Value,
    )
    query_expansion_spec: QueryExpansionSpec = proto.Field(
        proto.MESSAGE,
        number=13,
        message=QueryExpansionSpec,
    )
    spell_correction_spec: SpellCorrectionSpec = proto.Field(
        proto.MESSAGE,
        number=14,
        message=SpellCorrectionSpec,
    )
    user_pseudo_id: str = proto.Field(
        proto.STRING,
        number=15,
    )
    content_search_spec: ContentSearchSpec = proto.Field(
        proto.MESSAGE,
        number=24,
        message=ContentSearchSpec,
    )
    embedding_spec: EmbeddingSpec = proto.Field(
        proto.MESSAGE,
        number=23,
        message=EmbeddingSpec,
    )
    ranking_expression: str = proto.Field(
        proto.STRING,
        number=26,
    )
    safe_search: bool = proto.Field(
        proto.BOOL,
        number=20,
    )
    user_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=22,
    )
    natural_language_query_understanding_spec: NaturalLanguageQueryUnderstandingSpec = (
        proto.Field(
            proto.MESSAGE,
            number=28,
            message=NaturalLanguageQueryUnderstandingSpec,
        )
    )
    search_as_you_type_spec: SearchAsYouTypeSpec = proto.Field(
        proto.MESSAGE,
        number=31,
        message=SearchAsYouTypeSpec,
    )
    session: str = proto.Field(
        proto.STRING,
        number=41,
    )
    session_spec: SessionSpec = proto.Field(
        proto.MESSAGE,
        number=42,
        message=SessionSpec,
    )
    relevance_threshold: RelevanceThreshold = proto.Field(
        proto.ENUM,
        number=44,
        enum=RelevanceThreshold,
    )


class SearchResponse(proto.Message):
    r"""Response message for
    [SearchService.Search][google.cloud.discoveryengine.v1beta.SearchService.Search]
    method.

    Attributes:
        results (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.SearchResult]):
            A list of matched documents. The order
            represents the ranking.
        facets (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Facet]):
            Results of facets requested by user.
        guided_search_result (google.cloud.discoveryengine_v1beta.types.SearchResponse.GuidedSearchResult):
            Guided search result.
        total_size (int):
            The estimated total count of matched items irrespective of
            pagination. The count of
            [results][google.cloud.discoveryengine.v1beta.SearchResponse.results]
            returned by pagination may be less than the
            [total_size][google.cloud.discoveryengine.v1beta.SearchResponse.total_size]
            that matches.
        attribution_token (str):
            A unique search token. This should be included in the
            [UserEvent][google.cloud.discoveryengine.v1beta.UserEvent]
            logs resulting from this search, which enables accurate
            attribution of search model performance. This also helps to
            identify a request during the customer support scenarios.
        redirect_uri (str):
            The URI of a customer-defined redirect page. If redirect
            action is triggered, no search is performed, and only
            [redirect_uri][google.cloud.discoveryengine.v1beta.SearchResponse.redirect_uri]
            and
            [attribution_token][google.cloud.discoveryengine.v1beta.SearchResponse.attribution_token]
            are set in the response.
        next_page_token (str):
            A token that can be sent as
            [SearchRequest.page_token][google.cloud.discoveryengine.v1beta.SearchRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
        corrected_query (str):
            Contains the spell corrected query, if found. If the spell
            correction type is AUTOMATIC, then the search results are
            based on corrected_query. Otherwise the original query is
            used for search.
        summary (google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary):
            A summary as part of the search results. This field is only
            returned if
            [SearchRequest.ContentSearchSpec.summary_spec][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.summary_spec]
            is set.
        applied_controls (MutableSequence[str]):
            Controls applied as part of the Control
            service.
        geo_search_debug_info (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.GeoSearchDebugInfo]):

        query_expansion_info (google.cloud.discoveryengine_v1beta.types.SearchResponse.QueryExpansionInfo):
            Query expansion information for the returned
            results.
        natural_language_query_understanding_info (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo):
            Natural language query understanding
            information for the returned results.
        session_info (google.cloud.discoveryengine_v1beta.types.SearchResponse.SessionInfo):
            Session information.

            Only set if
            [SearchRequest.session][google.cloud.discoveryengine.v1beta.SearchRequest.session]
            is provided. See its description for more details.
        one_box_results (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.OneBoxResult]):
            A list of One Box results. There can be
            multiple One Box results of different types.
    """

    class SearchResult(proto.Message):
        r"""Represents the search results.

        Attributes:
            id (str):
                [Document.id][google.cloud.discoveryengine.v1beta.Document.id]
                of the searched
                [Document][google.cloud.discoveryengine.v1beta.Document].
            document (google.cloud.discoveryengine_v1beta.types.Document):
                The document data snippet in the search response. Only
                fields that are marked as ``retrievable`` are populated.
            chunk (google.cloud.discoveryengine_v1beta.types.Chunk):
                The chunk data in the search response if the
                [SearchRequest.ContentSearchSpec.search_result_mode][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.search_result_mode]
                is set to
                [CHUNKS][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS].
            model_scores (MutableMapping[str, google.cloud.discoveryengine_v1beta.types.DoubleList]):
                Google provided available scores.
        """

        id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        document: gcd_document.Document = proto.Field(
            proto.MESSAGE,
            number=2,
            message=gcd_document.Document,
        )
        chunk: gcd_chunk.Chunk = proto.Field(
            proto.MESSAGE,
            number=18,
            message=gcd_chunk.Chunk,
        )
        model_scores: MutableMapping[str, common.DoubleList] = proto.MapField(
            proto.STRING,
            proto.MESSAGE,
            number=4,
            message=common.DoubleList,
        )

    class Facet(proto.Message):
        r"""A facet result.

        Attributes:
            key (str):
                The key for this facet. For example, ``"colors"`` or
                ``"price"``. It matches
                [SearchRequest.FacetSpec.FacetKey.key][google.cloud.discoveryengine.v1beta.SearchRequest.FacetSpec.FacetKey.key].
            values (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Facet.FacetValue]):
                The facet values for this field.
            dynamic_facet (bool):
                Whether the facet is dynamically generated.
        """

        class FacetValue(proto.Message):
            r"""A facet value which contains value names and their count.

            This message has `oneof`_ fields (mutually exclusive fields).
            For each oneof, at most one member field can be set at the same time.
            Setting any member of the oneof automatically clears all other
            members.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                value (str):
                    Text value of a facet, such as "Black" for
                    facet "colors".

                    This field is a member of `oneof`_ ``facet_value``.
                interval (google.cloud.discoveryengine_v1beta.types.Interval):
                    Interval value for a facet, such as [10, 20) for facet
                    "price". It matches
                    [SearchRequest.FacetSpec.FacetKey.intervals][google.cloud.discoveryengine.v1beta.SearchRequest.FacetSpec.FacetKey.intervals].

                    This field is a member of `oneof`_ ``facet_value``.
                count (int):
                    Number of items that have this facet value.
            """

            value: str = proto.Field(
                proto.STRING,
                number=1,
                oneof="facet_value",
            )
            interval: common.Interval = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="facet_value",
                message=common.Interval,
            )
            count: int = proto.Field(
                proto.INT64,
                number=3,
            )

        key: str = proto.Field(
            proto.STRING,
            number=1,
        )
        values: MutableSequence[
            "SearchResponse.Facet.FacetValue"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="SearchResponse.Facet.FacetValue",
        )
        dynamic_facet: bool = proto.Field(
            proto.BOOL,
            number=3,
        )

    class GuidedSearchResult(proto.Message):
        r"""Guided search result. The guided search helps user to refine
        the search results and narrow down to the real needs from a
        broaded search results.

        Attributes:
            refinement_attributes (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.GuidedSearchResult.RefinementAttribute]):
                A list of ranked refinement attributes.
            follow_up_questions (MutableSequence[str]):
                Suggested follow-up questions.
        """

        class RefinementAttribute(proto.Message):
            r"""Useful attribute for search result refinements.

            Attributes:
                attribute_key (str):
                    Attribute key used to refine the results. For example,
                    ``"movie_type"``.
                attribute_value (str):
                    Attribute value used to refine the results. For example,
                    ``"drama"``.
            """

            attribute_key: str = proto.Field(
                proto.STRING,
                number=1,
            )
            attribute_value: str = proto.Field(
                proto.STRING,
                number=2,
            )

        refinement_attributes: MutableSequence[
            "SearchResponse.GuidedSearchResult.RefinementAttribute"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="SearchResponse.GuidedSearchResult.RefinementAttribute",
        )
        follow_up_questions: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class Summary(proto.Message):
        r"""Summary of the top N search results specified by the summary
        spec.

        Attributes:
            summary_text (str):
                The summary content.
            summary_skipped_reasons (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.SummarySkippedReason]):
                Additional summary-skipped reasons. This
                provides the reason for ignored cases. If
                nothing is skipped, this field is not set.
            safety_attributes (google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.SafetyAttributes):
                A collection of Safety Attribute categories
                and their associated confidence scores.
            summary_with_metadata (google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.SummaryWithMetadata):
                Summary with metadata information.
        """

        class SummarySkippedReason(proto.Enum):
            r"""An Enum for summary-skipped reasons.

            Values:
                SUMMARY_SKIPPED_REASON_UNSPECIFIED (0):
                    Default value. The summary skipped reason is
                    not specified.
                ADVERSARIAL_QUERY_IGNORED (1):
                    The adversarial query ignored case.

                    Only used when
                    [SummarySpec.ignore_adversarial_query][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SummarySpec.ignore_adversarial_query]
                    is set to ``true``.
                NON_SUMMARY_SEEKING_QUERY_IGNORED (2):
                    The non-summary seeking query ignored case.

                    Only used when
                    [SummarySpec.ignore_non_summary_seeking_query][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SummarySpec.ignore_non_summary_seeking_query]
                    is set to ``true``.
                OUT_OF_DOMAIN_QUERY_IGNORED (3):
                    The out-of-domain query ignored case.

                    Google skips the summary if there are no
                    high-relevance search results. For example, the
                    data store contains facts about company A but
                    the user query is asking questions about company
                    B.
                POTENTIAL_POLICY_VIOLATION (4):
                    The potential policy violation case.

                    Google skips the summary if there is a potential
                    policy violation detected. This includes content
                    that may be violent or toxic.
                LLM_ADDON_NOT_ENABLED (5):
                    The LLM addon not enabled case.

                    Google skips the summary if the LLM addon is not
                    enabled.
                NO_RELEVANT_CONTENT (6):
                    The no relevant content case.

                    Google skips the summary if there is no relevant
                    content in the retrieved search results.
                JAIL_BREAKING_QUERY_IGNORED (7):
                    The jail-breaking query ignored case.

                    For example, "Reply in the tone of a competing company's
                    CEO". Only used when
                    [SearchRequest.ContentSearchSpec.SummarySpec.ignore_jail_breaking_query]
                    is set to ``true``.
                CUSTOMER_POLICY_VIOLATION (8):
                    The customer policy violation case.

                    Google skips the summary if there is a customer
                    policy violation detected. The policy is defined
                    by the customer.
            """
            SUMMARY_SKIPPED_REASON_UNSPECIFIED = 0
            ADVERSARIAL_QUERY_IGNORED = 1
            NON_SUMMARY_SEEKING_QUERY_IGNORED = 2
            OUT_OF_DOMAIN_QUERY_IGNORED = 3
            POTENTIAL_POLICY_VIOLATION = 4
            LLM_ADDON_NOT_ENABLED = 5
            NO_RELEVANT_CONTENT = 6
            JAIL_BREAKING_QUERY_IGNORED = 7
            CUSTOMER_POLICY_VIOLATION = 8

        class SafetyAttributes(proto.Message):
            r"""Safety Attribute categories and their associated confidence
            scores.

            Attributes:
                categories (MutableSequence[str]):
                    The display names of Safety Attribute
                    categories associated with the generated
                    content. Order matches the Scores.
                scores (MutableSequence[float]):
                    The confidence scores of the each category,
                    higher value means higher confidence. Order
                    matches the Categories.
            """

            categories: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )
            scores: MutableSequence[float] = proto.RepeatedField(
                proto.FLOAT,
                number=2,
            )

        class CitationMetadata(proto.Message):
            r"""Citation metadata.

            Attributes:
                citations (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.Citation]):
                    Citations for segments.
            """

            citations: MutableSequence[
                "SearchResponse.Summary.Citation"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="SearchResponse.Summary.Citation",
            )

        class Citation(proto.Message):
            r"""Citation info for a segment.

            Attributes:
                start_index (int):
                    Index indicates the start of the segment,
                    measured in bytes/unicode.
                end_index (int):
                    End of the attributed segment, exclusive.
                sources (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.CitationSource]):
                    Citation sources for the attributed segment.
            """

            start_index: int = proto.Field(
                proto.INT64,
                number=1,
            )
            end_index: int = proto.Field(
                proto.INT64,
                number=2,
            )
            sources: MutableSequence[
                "SearchResponse.Summary.CitationSource"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="SearchResponse.Summary.CitationSource",
            )

        class CitationSource(proto.Message):
            r"""Citation source.

            Attributes:
                reference_index (int):
                    Document reference index from
                    SummaryWithMetadata.references. It is 0-indexed and the
                    value will be zero if the reference_index is not set
                    explicitly.
            """

            reference_index: int = proto.Field(
                proto.INT64,
                number=4,
            )

        class Reference(proto.Message):
            r"""Document reference.

            Attributes:
                title (str):
                    Title of the document.
                document (str):
                    Required.
                    [Document.name][google.cloud.discoveryengine.v1beta.Document.name]
                    of the document. Full resource name of the referenced
                    document, in the format
                    ``projects/*/locations/*/collections/*/dataStores/*/branches/*/documents/*``.
                uri (str):
                    Cloud Storage or HTTP uri for the document.
                chunk_contents (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.Reference.ChunkContent]):
                    List of cited chunk contents derived from
                    document content.
            """

            class ChunkContent(proto.Message):
                r"""Chunk content.

                Attributes:
                    content (str):
                        Chunk textual content.
                    page_identifier (str):
                        Page identifier.
                """

                content: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                page_identifier: str = proto.Field(
                    proto.STRING,
                    number=2,
                )

            title: str = proto.Field(
                proto.STRING,
                number=1,
            )
            document: str = proto.Field(
                proto.STRING,
                number=2,
            )
            uri: str = proto.Field(
                proto.STRING,
                number=3,
            )
            chunk_contents: MutableSequence[
                "SearchResponse.Summary.Reference.ChunkContent"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=4,
                message="SearchResponse.Summary.Reference.ChunkContent",
            )

        class SummaryWithMetadata(proto.Message):
            r"""Summary with metadata information.

            Attributes:
                summary (str):
                    Summary text with no citation information.
                citation_metadata (google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.CitationMetadata):
                    Citation metadata for given summary.
                references (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.Summary.Reference]):
                    Document References.
            """

            summary: str = proto.Field(
                proto.STRING,
                number=1,
            )
            citation_metadata: "SearchResponse.Summary.CitationMetadata" = proto.Field(
                proto.MESSAGE,
                number=2,
                message="SearchResponse.Summary.CitationMetadata",
            )
            references: MutableSequence[
                "SearchResponse.Summary.Reference"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="SearchResponse.Summary.Reference",
            )

        summary_text: str = proto.Field(
            proto.STRING,
            number=1,
        )
        summary_skipped_reasons: MutableSequence[
            "SearchResponse.Summary.SummarySkippedReason"
        ] = proto.RepeatedField(
            proto.ENUM,
            number=2,
            enum="SearchResponse.Summary.SummarySkippedReason",
        )
        safety_attributes: "SearchResponse.Summary.SafetyAttributes" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="SearchResponse.Summary.SafetyAttributes",
        )
        summary_with_metadata: "SearchResponse.Summary.SummaryWithMetadata" = (
            proto.Field(
                proto.MESSAGE,
                number=4,
                message="SearchResponse.Summary.SummaryWithMetadata",
            )
        )

    class GeoSearchDebugInfo(proto.Message):
        r"""Debug information specifically related to forward geocoding
        issues arising from Geolocation Search.

        Attributes:
            original_address_query (str):
                The address from which forward geocoding
                ingestion produced issues.
            error_message (str):
                The error produced.
        """

        original_address_query: str = proto.Field(
            proto.STRING,
            number=1,
        )
        error_message: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class QueryExpansionInfo(proto.Message):
        r"""Information describing query expansion including whether
        expansion has occurred.

        Attributes:
            expanded_query (bool):
                Bool describing whether query expansion has
                occurred.
            pinned_result_count (int):
                Number of pinned results. This field will only be set when
                expansion happens and
                [SearchRequest.QueryExpansionSpec.pin_unexpanded_results][google.cloud.discoveryengine.v1beta.SearchRequest.QueryExpansionSpec.pin_unexpanded_results]
                is set to true.
        """

        expanded_query: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        pinned_result_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class NaturalLanguageQueryUnderstandingInfo(proto.Message):
        r"""Information describing what natural language understanding
        was done on the input query.

        Attributes:
            extracted_filters (str):
                The filters that were extracted from the
                input query.
            rewritten_query (str):
                Rewritten input query minus the extracted
                filters.
            structured_extracted_filter (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter):
                The filters that were extracted from the
                input query represented in a structured form.
        """

        class StructuredExtractedFilter(proto.Message):
            r"""The filters that were extracted from the input query
            represented in a structured form.

            Attributes:
                expression (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression):
                    The expression denoting the filter that was
                    extracted from the input query in a structured
                    form. It can be a simple expression denoting a
                    single string, numerical or geolocation
                    constraint or a compound expression which is a
                    combination of multiple expressions connected
                    using logical (OR and AND) operators.
            """

            class StringConstraint(proto.Message):
                r"""Constraint expression of a string field.

                Attributes:
                    field_name (str):
                        Name of the string field as defined in the
                        schema.
                    values (MutableSequence[str]):
                        Values of the string field. The record will
                        only be returned if the field value matches one
                        of the values specified here.
                    query_segment (str):
                        Identifies the keywords within the search
                        query that match a filter.
                """

                field_name: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                values: MutableSequence[str] = proto.RepeatedField(
                    proto.STRING,
                    number=2,
                )
                query_segment: str = proto.Field(
                    proto.STRING,
                    number=3,
                )

            class NumberConstraint(proto.Message):
                r"""Constraint expression of a number field. Example: price <
                100.

                Attributes:
                    field_name (str):
                        Name of the numerical field as defined in the
                        schema.
                    comparison (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint.Comparison):
                        The comparison operation performed between
                        the field value and the value specified in the
                        constraint.
                    value (float):
                        The value specified in the numerical
                        constraint.
                    query_segment (str):
                        Identifies the keywords within the search
                        query that match a filter.
                """

                class Comparison(proto.Enum):
                    r"""The comparison operation that was performed.

                    Values:
                        COMPARISON_UNSPECIFIED (0):
                            Undefined comparison operator.
                        EQUALS (1):
                            Denotes equality ``=`` operator.
                        LESS_THAN_EQUALS (2):
                            Denotes less than or equal to ``<=`` operator.
                        LESS_THAN (3):
                            Denotes less than ``<`` operator.
                        GREATER_THAN_EQUALS (4):
                            Denotes greater than or equal to ``>=`` operator.
                        GREATER_THAN (5):
                            Denotes greater than ``>`` operator.
                    """
                    COMPARISON_UNSPECIFIED = 0
                    EQUALS = 1
                    LESS_THAN_EQUALS = 2
                    LESS_THAN = 3
                    GREATER_THAN_EQUALS = 4
                    GREATER_THAN = 5

                field_name: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                comparison: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint.Comparison" = proto.Field(
                    proto.ENUM,
                    number=2,
                    enum="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint.Comparison",
                )
                value: float = proto.Field(
                    proto.DOUBLE,
                    number=3,
                )
                query_segment: str = proto.Field(
                    proto.STRING,
                    number=4,
                )

            class GeolocationConstraint(proto.Message):
                r"""Constraint of a geolocation field.
                Name of the geolocation field as defined in the schema.

                Attributes:
                    field_name (str):
                        The name of the geolocation field as defined
                        in the schema.
                    address (str):
                        The reference address that was inferred from
                        the input query. The proximity of the reference
                        address to the geolocation field will be used to
                        filter the results.
                    latitude (float):
                        The latitude of the geolocation inferred from
                        the input query.
                    longitude (float):
                        The longitude of the geolocation inferred
                        from the input query.
                    radius_in_meters (float):
                        The radius in meters around the address. The
                        record is returned if the location of the
                        geolocation field is within the radius.
                """

                field_name: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                address: str = proto.Field(
                    proto.STRING,
                    number=2,
                )
                latitude: float = proto.Field(
                    proto.DOUBLE,
                    number=4,
                )
                longitude: float = proto.Field(
                    proto.DOUBLE,
                    number=5,
                )
                radius_in_meters: float = proto.Field(
                    proto.FLOAT,
                    number=3,
                )

            class AndExpression(proto.Message):
                r"""Logical ``And`` operator.

                Attributes:
                    expressions (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression]):
                        The expressions that were ANDed together.
                """

                expressions: MutableSequence[
                    "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression",
                )

            class OrExpression(proto.Message):
                r"""Logical ``Or`` operator.

                Attributes:
                    expressions (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression]):
                        The expressions that were ORed together.
                """

                expressions: MutableSequence[
                    "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression",
                )

            class Expression(proto.Message):
                r"""The expression denoting the filter that was extracted from
                the input query.

                This message has `oneof`_ fields (mutually exclusive fields).
                For each oneof, at most one member field can be set at the same time.
                Setting any member of the oneof automatically clears all other
                members.

                .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

                Attributes:
                    string_constraint (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.StringConstraint):
                        String constraint expression.

                        This field is a member of `oneof`_ ``expr``.
                    number_constraint (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint):
                        Numerical constraint expression.

                        This field is a member of `oneof`_ ``expr``.
                    geolocation_constraint (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.GeolocationConstraint):
                        Geolocation constraint expression.

                        This field is a member of `oneof`_ ``expr``.
                    and_expr (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.AndExpression):
                        Logical "And" compound operator connecting
                        multiple expressions.

                        This field is a member of `oneof`_ ``expr``.
                    or_expr (google.cloud.discoveryengine_v1beta.types.SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.OrExpression):
                        Logical "Or" compound operator connecting
                        multiple expressions.

                        This field is a member of `oneof`_ ``expr``.
                """

                string_constraint: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.StringConstraint" = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    oneof="expr",
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.StringConstraint",
                )
                number_constraint: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint" = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    oneof="expr",
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.NumberConstraint",
                )
                geolocation_constraint: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.GeolocationConstraint" = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    oneof="expr",
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.GeolocationConstraint",
                )
                and_expr: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.AndExpression" = proto.Field(
                    proto.MESSAGE,
                    number=4,
                    oneof="expr",
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.AndExpression",
                )
                or_expr: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.OrExpression" = proto.Field(
                    proto.MESSAGE,
                    number=5,
                    oneof="expr",
                    message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.OrExpression",
                )

            expression: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression" = proto.Field(
                proto.MESSAGE,
                number=1,
                message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter.Expression",
            )

        extracted_filters: str = proto.Field(
            proto.STRING,
            number=1,
        )
        rewritten_query: str = proto.Field(
            proto.STRING,
            number=2,
        )
        structured_extracted_filter: "SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="SearchResponse.NaturalLanguageQueryUnderstandingInfo.StructuredExtractedFilter",
        )

    class SessionInfo(proto.Message):
        r"""Information about the session.

        Attributes:
            name (str):
                Name of the session. If the auto-session mode is used (when
                [SearchRequest.session][google.cloud.discoveryengine.v1beta.SearchRequest.session]
                ends with "-"), this field holds the newly generated session
                name.
            query_id (str):
                Query ID that corresponds to this search API
                call. One session can have multiple turns, each
                with a unique query ID.

                By specifying the session name and this query ID
                in the Answer API call, the answer generation
                happens in the context of the search results
                from this search call.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        query_id: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class OneBoxResult(proto.Message):
        r"""OneBoxResult is a holder for all results of specific type
        that we want to display in UI differently.

        Attributes:
            one_box_type (google.cloud.discoveryengine_v1beta.types.SearchResponse.OneBoxResult.OneBoxType):
                The type of One Box result.
            search_results (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchResponse.SearchResult]):
                The search results for this One Box.
        """

        class OneBoxType(proto.Enum):
            r"""The type of One Box result.

            Values:
                ONE_BOX_TYPE_UNSPECIFIED (0):
                    Default value. Should not be used.
                PEOPLE (1):
                    One Box result contains people results.
                ORGANIZATION (2):
                    One Box result contains organization results.
                SLACK (3):
                    One Box result contains slack results.
            """
            ONE_BOX_TYPE_UNSPECIFIED = 0
            PEOPLE = 1
            ORGANIZATION = 2
            SLACK = 3

        one_box_type: "SearchResponse.OneBoxResult.OneBoxType" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SearchResponse.OneBoxResult.OneBoxType",
        )
        search_results: MutableSequence[
            "SearchResponse.SearchResult"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="SearchResponse.SearchResult",
        )

    @property
    def raw_page(self):
        return self

    results: MutableSequence[SearchResult] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=SearchResult,
    )
    facets: MutableSequence[Facet] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=Facet,
    )
    guided_search_result: GuidedSearchResult = proto.Field(
        proto.MESSAGE,
        number=8,
        message=GuidedSearchResult,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    attribution_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    redirect_uri: str = proto.Field(
        proto.STRING,
        number=12,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )
    corrected_query: str = proto.Field(
        proto.STRING,
        number=7,
    )
    summary: Summary = proto.Field(
        proto.MESSAGE,
        number=9,
        message=Summary,
    )
    applied_controls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    geo_search_debug_info: MutableSequence[GeoSearchDebugInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message=GeoSearchDebugInfo,
    )
    query_expansion_info: QueryExpansionInfo = proto.Field(
        proto.MESSAGE,
        number=14,
        message=QueryExpansionInfo,
    )
    natural_language_query_understanding_info: NaturalLanguageQueryUnderstandingInfo = (
        proto.Field(
            proto.MESSAGE,
            number=15,
            message=NaturalLanguageQueryUnderstandingInfo,
        )
    )
    session_info: SessionInfo = proto.Field(
        proto.MESSAGE,
        number=19,
        message=SessionInfo,
    )
    one_box_results: MutableSequence[OneBoxResult] = proto.RepeatedField(
        proto.MESSAGE,
        number=20,
        message=OneBoxResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
