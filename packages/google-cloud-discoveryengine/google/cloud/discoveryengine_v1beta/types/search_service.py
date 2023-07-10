# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
        page_size (int):
            Maximum number of
            [Document][google.cloud.discoveryengine.v1beta.Document]s to
            return. If unspecified, defaults to a reasonable value. The
            maximum allowed value is 100. Values above 100 will be
            coerced to 100.

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
        filter (str):
            The filter syntax consists of an expression language for
            constructing a predicate from one or more fields of the
            documents being filtered. Filter expression is
            case-sensitive.

            If this field is unrecognizable, an ``INVALID_ARGUMENT`` is
            returned.
        order_by (str):
            The order in which documents are returned. Document can be
            ordered by a field in an
            [Document][google.cloud.discoveryengine.v1beta.Document]
            object. Leave it unset if ordered by relevance. OrderBy
            expression is case-sensitive.

            If this field is unrecognizable, an ``INVALID_ARGUMENT`` is
            returned.
        user_info (google.cloud.discoveryengine_v1beta.types.UserInfo):
            Information about the end user. Highly recommended for
            analytics. The user_agent string in UserInfo will be used to
            deduce device_type for analytics.
        facet_specs (MutableSequence[google.cloud.discoveryengine_v1beta.types.SearchRequest.FacetSpec]):
            Facet specifications for faceted search. If empty, no facets
            are returned.

            A maximum of 100 values are allowed. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.
        boost_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.BoostSpec):
            Boost specification to boost certain
            documents.
        params (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            Additional search parameters.

            For public website search only, supported values are:

            -  ``user_country_code``: string. Default empty. If set to
               non-empty, results are restricted or boosted based on the
               location provided.
            -  ``search_type``: double. Default empty. Enables
               non-webpage searching depending on the value. The only
               valid non-default value is 1, which enables image
               searching.
        query_expansion_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.QueryExpansionSpec):
            The query expansion specification that
            specifies the conditions under which query
            expansion will occur.
        spell_correction_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.SpellCorrectionSpec):
            The spell correction specification that
            specifies the mode under which spell correction
            will take effect.
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
            The content search spec that configs the
            desired behavior of content search.
        safe_search (bool):
            Whether to turn on safe search. This is only supported for
            [ContentConfig.PUBLIC_WEBSITE][].
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

    class FacetSpec(proto.Message):
        r"""A facet specification to perform faceted search.

        Attributes:
            facet_key (google.cloud.discoveryengine_v1beta.types.SearchRequest.FacetSpec.FacetKey):
                Required. The facet key specification.
            limit (int):
                Maximum of facet values that should be returned for this
                facet. If unspecified, defaults to 20. The maximum allowed
                value is 300. Values above 300 will be coerced to 300.

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
                determined automatically. It will be ordered together with
                dynamic facets if dynamic facets is enabled. If set to
                false, the position of this facet in the response will be
                the same as in the request, and it will be ranked before the
                facets with dynamic position enable and all dynamic facets.

                For example, you may always want to have rating facet
                returned in the response, but it's not necessarily to always
                display the rating facet at the top. In that case, you can
                set enable_dynamic_position to true so that the position of
                rating facet in response will be determined automatically.

                Another example, assuming you have the following facets in
                the request:

                -  "rating", enable_dynamic_position = true

                -  "price", enable_dynamic_position = false

                -  "brands", enable_dynamic_position = false

                And also you have a dynamic facets enable, which will
                generate a facet 'gender'. Then the final order of the
                facets in the response can be ("price", "brands", "rating",
                "gender") or ("price", "brands", "gender", "rating") depends
                on how API orders "gender" and "rating" facets. However,
                notice that "price" and "brands" will always be ranked at
                1st and 2nd position since their enable_dynamic_position are
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
                    Set only if values should be bucketized into
                    intervals. Must be set for facets with numerical
                    values. Must not be set for facet with text
                    values. Maximum number of intervals is 30.
                restricted_values (MutableSequence[str]):
                    Only get facet for the given restricted values. Only
                    supported on textual fields. For example, suppose "category"
                    has three values "Action > 2022", "Action > 2021" and
                    "Sci-Fi > 2022". If set "restricted_values" to "Action >
                    2022", the "category" facet will only contain "Action >
                    2022". Only supported on textual fields. Maximum is 10.
                prefixes (MutableSequence[str]):
                    Only get facet values that start with the
                    given string prefix. For example, suppose
                    "category" has three values "Action > 2022",
                    "Action > 2021" and "Sci-Fi > 2022". If set
                    "prefixes" to "Action", the "category" facet
                    will only contain "Action > 2022" and "Action >
                    2021". Only supported on textual fields. Maximum
                    is 10.
                contains (MutableSequence[str]):
                    Only get facet values that contains the given
                    strings. For example, suppose "category" has
                    three values "Action > 2022", "Action > 2021"
                    and "Sci-Fi > 2022". If set "contains" to
                    "2022", the "category" facet will only contain
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

                       -  (id: ANY("doc_1", "doc_2")) AND (color:
                          ANY("Red","Blue"))
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
        r"""The specification that configs the desired behavior of the
        UCS content search.

        Attributes:
            snippet_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SnippetSpec):
                If there is no snippet spec provided, there
                will be no snippet in the search result.
            summary_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.SummarySpec):
                If there is no summary spec provided, there
                will be no summary in the search response.
            extractive_content_spec (google.cloud.discoveryengine_v1beta.types.SearchRequest.ContentSearchSpec.ExtractiveContentSpec):
                If there is no extractive_content_spec provided, there will
                be no extractive answer in the search response.
        """

        class SnippetSpec(proto.Message):
            r"""The specification that configs the snippet in the search
            results.

            Attributes:
                max_snippet_count (int):
                    Max number of snippets returned in each search result.

                    A snippet is an infomartive summary of a content with
                    highlighting for UI rendering.

                    If the matching snippets is less than the max_snippet_count,
                    return all of the snippets; otherwise, return the
                    max_snippet_count.

                    At most 5 snippets will be returned for each SearchResult.
                reference_only (bool):
                    if true, only snippet reference is returned.
            """

            max_snippet_count: int = proto.Field(
                proto.INT32,
                number=1,
            )
            reference_only: bool = proto.Field(
                proto.BOOL,
                number=2,
            )

        class SummarySpec(proto.Message):
            r"""The specification that configs the summary in the search
            response.

            Attributes:
                summary_result_count (int):
                    The number of top results the summary should be generated
                    from. If the number of returned results is less than
                    summary_result_count, then the summary would be derived from
                    all the results; otherwise, the summary would be derived
                    from the top results.

                    At most 5 results can be used for generating summary.
            """

            summary_result_count: int = proto.Field(
                proto.INT32,
                number=1,
            )

        class ExtractiveContentSpec(proto.Message):
            r"""The specification that configs the extractive content in
            search results.

            Attributes:
                max_extractive_answer_count (int):
                    The max number of extractive answers returned in each search
                    result.

                    An extractive answer is a verbatim answer extracted from the
                    original document, which provides precise and contextually
                    relevant answer to the search query.

                    If the number of matching answers is less than the
                    extractive_answer_count, return all of the answers;
                    otherwise, return the extractive_answer_count.

                    At most 5 answers will be returned for each SearchResult.
                max_extractive_segment_count (int):
                    The max number of extractive segments returned in each
                    search result.

                    An extractive segment is a text segment extracted from the
                    original document which is relevant to the search query and
                    in general more verbose than an extrative answer. The
                    segment could then be used as input for LLMs to generate
                    summaries and answers.

                    If the number of matching segments is less than the
                    max_extractive_segment_count, return all of the segments;
                    otherwise, return the max_extractive_segment_count.

                    Currently one segment will be returned for each
                    SearchResult.
            """

            max_extractive_answer_count: int = proto.Field(
                proto.INT32,
                number=1,
            )
            max_extractive_segment_count: int = proto.Field(
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
    filter: str = proto.Field(
        proto.STRING,
        number=7,
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

    class Summary(proto.Message):
        r"""Summary of the top N search result specified by the summary
        spec.

        Attributes:
            summary_text (str):
                The summary content.
        """

        summary_text: str = proto.Field(
            proto.STRING,
            number=1,
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


__all__ = tuple(sorted(__protobuf__.manifest))
