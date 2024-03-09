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
            return. If unspecified, defaults to a reasonable value. The
            maximum allowed value is 100. Values above 100 are coerced
            to 100.

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
            A list of data store specs to apply on a
            search call.
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
            expression is case-sensitive. For more information on
            ordering, see
            `Ordering <https://cloud.google.com/retail/docs/filter-and-order#order>`__

            If this field is unrecognizable, an ``INVALID_ARGUMENT`` is
            returned.
        user_info (google.cloud.discoveryengine_v1beta.types.UserInfo):
            Information about the end user. Highly recommended for
            analytics.
            [UserInfo.user_agent][google.cloud.discoveryengine.v1beta.UserInfo.user_agent]
            is used to deduce ``device_type`` for analytics.
        facet_specs (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.FacetSpec]):
            Facet specifications for faceted search. If empty, no facets
            are returned.

            A maximum of 100 values are allowed. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.
        boost_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec):
            Boost specification to boost certain documents. For more
            information on boosting, see
            `Boosting <https://cloud.google.com/retail/docs/boosting#boost>`__
        params (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            Additional search parameters.

            For public website search only, supported values are:

            -  ``user_country_code``: string. Default empty. If set to
               non-empty, results are restricted or boosted based on the
               location provided. Example: user_country_code: "au"

               For available codes see `Country
               Codes <https://developers.google.com/custom-search/docs/json_api_reference#countryCodes>`__

            -  ``search_type``: double. Default empty. Enables
               non-webpage searching depending on the value. The only
               valid non-default value is 1, which enables image
               searching. Example: search_type: 1
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
            [ServingConfig.EmbeddingConfig.field_path][].
        ranking_expression (str):
            The ranking expression controls the customized ranking on
            retrieval documents. This overrides
            [ServingConfig.ranking_expression][google.cloud.discoveryengine.v1beta.ServingConfig.ranking_expression].
            The ranking expression is a single function or multiple
            functions that are joint by "+".

            -  ranking_expression = function, { " + ", function };
               Supported functions:
            -  double \* relevance_score
            -  double \* dotProduct(embedding_field_path) Function
               variables: ``relevance_score``: pre-defined keywords,
               used for measure relevance between query and document.
               ``embedding_field_path``: the document embedding field
               used with query embedding vector. ``dotProduct``:
               embedding function between embedding_field_path and query
               embedding vector.

            Example ranking expression: If document has an embedding
            field doc_embedding, the ranking expression could be
            ``0.5 * relevance_score + 0.3 * dotProduct(doc_embedding)``.
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
    """

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
        r"""A struct to define data stores to filter on in a search call.

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
                Maximum of facet values that should be returned for this
                facet. If unspecified, defaults to 20. The maximum allowed
                value is 300. Values above 300 are coerced to 300.

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
                    Only get facet values that contains the given
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
                    condition is ignored.
            """

            condition: str = proto.Field(
                proto.STRING,
                number=1,
            )
            boost: float = proto.Field(
                proto.FLOAT,
                number=2,
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
                The mode under which spell correction should take effect to
                replace the original search query. Default to
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
                    Search API will try to find a spell suggestion if there is
                    any and put in the
                    [SearchResponse.corrected_query][google.cloud.discoveryengine.v1beta.SearchResponse.corrected_query].
                    The spell suggestion will not be used as the search query.
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
        """

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

                    At most 10 results can be used to generate a summary.
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
                           specified. Uses a generally available, fine-tuned version
                           of the text-bison@001 model.
                        -  ``preview``: string. (Public preview) Uses a fine-tuned
                           version of the text-bison@002 model. This model works
                           only for summaries in English.
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
                    extractive segments in each search result. The default value
                    is ``false``.

                    Note: this is a priavte preview feature and only works for
                    allowlisted users, please reach out to Cloud Support team if
                    you want to use it.
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
            attribution of search model performance.
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
        query_expansion_info (google.cloud.discoveryengine_v1beta.types.SearchResponse.QueryExpansionInfo):
            Query expansion information for the returned
            results.
    """

    class SearchResult(proto.Message):
        r"""Represents the search results.

        Attributes:
            id (str):
                [Document.id][google.cloud.discoveryengine.v1beta.Document.id]
                of the searched
                [Document][google.cloud.discoveryengine.v1beta.Document].
            document (google.cloud.discoveryengine_v1beta.types.Document):
                The document data snippet in the search
                response. Only fields that are marked as
                retrievable are populated.
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
                The key for this facet. E.g., "colors" or "price". It
                matches
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
                    Attribute key used to refine the results e.g. 'movie_type'.
                attribute_value (str):
                    Attribute value used to refine the results
                    e.g. 'drama'.
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
        r"""Summary of the top N search result specified by the summary
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

                    Only populated when
                    [SummarySpec.ignore_adversarial_query][google.cloud.discoveryengine.v1beta.SearchRequest.ContentSearchSpec.SummarySpec.ignore_adversarial_query]
                    is set to ``true``.
                NON_SUMMARY_SEEKING_QUERY_IGNORED (2):
                    The non-summary seeking query ignored case.

                    Only populated when
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
            """
            SUMMARY_SKIPPED_REASON_UNSPECIFIED = 0
            ADVERSARIAL_QUERY_IGNORED = 1
            NON_SUMMARY_SEEKING_QUERY_IGNORED = 2
            OUT_OF_DOMAIN_QUERY_IGNORED = 3
            POTENTIAL_POLICY_VIOLATION = 4
            LLM_ADDON_NOT_ENABLED = 5

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
            """

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
    query_expansion_info: QueryExpansionInfo = proto.Field(
        proto.MESSAGE,
        number=14,
        message=QueryExpansionInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
