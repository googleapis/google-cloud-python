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

from google.cloud.discoveryengine_v1.types import common
from google.cloud.discoveryengine_v1.types import document as gcd_document

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1",
    manifest={
        "SearchRequest",
        "SearchResponse",
    },
)


class SearchRequest(proto.Message):
    r"""Request message for
    [SearchService.Search][google.cloud.discoveryengine.v1.SearchService.Search]
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
            [Document][google.cloud.discoveryengine.v1.Document]s to
            return. If unspecified, defaults to a reasonable value. The
            maximum allowed value is 100. Values above 100 will be
            coerced to 100.

            If this field is negative, an ``INVALID_ARGUMENT`` is
            returned.
        page_token (str):
            A page token received from a previous
            [SearchService.Search][google.cloud.discoveryengine.v1.SearchService.Search]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [SearchService.Search][google.cloud.discoveryengine.v1.SearchService.Search]
            must match the call that provided the page token. Otherwise,
            an ``INVALID_ARGUMENT`` error is returned.
        offset (int):
            A 0-indexed integer that specifies the current offset (that
            is, starting result location, amongst the
            [Document][google.cloud.discoveryengine.v1.Document]s deemed
            by the API as relevant) in search results. This field is
            only considered if
            [page_token][google.cloud.discoveryengine.v1.SearchRequest.page_token]
            is unset.

            If this field is negative, an ``INVALID_ARGUMENT`` is
            returned.
        user_info (google.cloud.discoveryengine_v1.types.UserInfo):
            Information about the end user. Highly recommended for
            analytics. The user_agent string in UserInfo will be used to
            deduce device_type for analytics.
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
        query_expansion_spec (google.cloud.discoveryengine_v1.types.SearchRequest.QueryExpansionSpec):
            The query expansion specification that
            specifies the conditions under which query
            expansion will occur.
        spell_correction_spec (google.cloud.discoveryengine_v1.types.SearchRequest.SpellCorrectionSpec):
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
            [UserEvent.user_pseudo_id][google.cloud.discoveryengine.v1.UserEvent.user_pseudo_id]
            and
            [CompleteQueryRequest.user_pseudo_id][google.cloud.discoveryengine.v1.CompleteQueryRequest.user_pseudo_id]

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an ``INVALID_ARGUMENT`` error
            is returned.
        content_search_spec (google.cloud.discoveryengine_v1.types.SearchRequest.ContentSearchSpec):
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

    class QueryExpansionSpec(proto.Message):
        r"""Specification to determine under which conditions query
        expansion should occur.

        Attributes:
            condition (google.cloud.discoveryengine_v1.types.SearchRequest.QueryExpansionSpec.Condition):
                The condition under which query expansion should occur.
                Default to
                [Condition.DISABLED][google.cloud.discoveryengine.v1.SearchRequest.QueryExpansionSpec.Condition.DISABLED].
        """

        class Condition(proto.Enum):
            r"""Enum describing under which condition query expansion should
            occur.

            Values:
                CONDITION_UNSPECIFIED (0):
                    Unspecified query expansion condition. In this case, server
                    behavior defaults to
                    [Condition.DISABLED][google.cloud.discoveryengine.v1.SearchRequest.QueryExpansionSpec.Condition.DISABLED].
                DISABLED (1):
                    Disabled query expansion. Only the exact search query is
                    used, even if
                    [SearchResponse.total_size][google.cloud.discoveryengine.v1.SearchResponse.total_size]
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
            mode (google.cloud.discoveryengine_v1.types.SearchRequest.SpellCorrectionSpec.Mode):
                The mode under which spell correction should take effect to
                replace the original search query. Default to
                [Mode.AUTO][google.cloud.discoveryengine.v1.SearchRequest.SpellCorrectionSpec.Mode.AUTO].
        """

        class Mode(proto.Enum):
            r"""Enum describing under which mode spell correction should
            occur.

            Values:
                MODE_UNSPECIFIED (0):
                    Unspecified spell correction mode. In this case, server
                    behavior defaults to
                    [Mode.AUTO][google.cloud.discoveryengine.v1.SearchRequest.SpellCorrectionSpec.Mode.AUTO].
                SUGGESTION_ONLY (1):
                    Search API will try to find a spell suggestion if there is
                    any and put in the
                    [SearchResponse.corrected_query][google.cloud.discoveryengine.v1.SearchResponse.corrected_query].
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
            snippet_spec (google.cloud.discoveryengine_v1.types.SearchRequest.ContentSearchSpec.SnippetSpec):
                If there is no snippet spec provided, there
                will be no snippet in the search result.
        """

        class SnippetSpec(proto.Message):
            r"""The specification that configs the snippet in the search
            results.

            Attributes:
                max_snippet_count (int):
                    Max number of snippets returned in each search result. If
                    the matching snippets is less than the max_snippet_count,
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

        snippet_spec: "SearchRequest.ContentSearchSpec.SnippetSpec" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="SearchRequest.ContentSearchSpec.SnippetSpec",
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
    user_info: common.UserInfo = proto.Field(
        proto.MESSAGE,
        number=21,
        message=common.UserInfo,
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
    [SearchService.Search][google.cloud.discoveryengine.v1.SearchService.Search]
    method.

    Attributes:
        results (MutableSequence[google.cloud.discoveryengine_v1.types.SearchResponse.SearchResult]):
            A list of matched documents. The order
            represents the ranking.
        total_size (int):
            The estimated total count of matched items irrespective of
            pagination. The count of
            [results][google.cloud.discoveryengine.v1.SearchResponse.results]
            returned by pagination may be less than the
            [total_size][google.cloud.discoveryengine.v1.SearchResponse.total_size]
            that matches.
        attribution_token (str):
            A unique search token. This should be included in the
            [UserEvent][google.cloud.discoveryengine.v1.UserEvent] logs
            resulting from this search, which enables accurate
            attribution of search model performance.
        next_page_token (str):
            A token that can be sent as
            [SearchRequest.page_token][google.cloud.discoveryengine.v1.SearchRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
        corrected_query (str):
            Contains the spell corrected query, if found. If the spell
            correction type is AUTOMATIC, then the search results are
            based on corrected_query. Otherwise the original query is
            used for search.
    """

    class SearchResult(proto.Message):
        r"""Represents the search results.

        Attributes:
            id (str):
                [Document.id][google.cloud.discoveryengine.v1.Document.id]
                of the searched
                [Document][google.cloud.discoveryengine.v1.Document].
            document (google.cloud.discoveryengine_v1.types.Document):
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

    @property
    def raw_page(self):
        return self

    results: MutableSequence[SearchResult] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=SearchResult,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    attribution_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )
    corrected_query: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
