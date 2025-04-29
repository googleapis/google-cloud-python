# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.cloud.retail_v2alpha.types import common, search_service

__protobuf__ = proto.module(
    package="google.cloud.retail.v2alpha",
    manifest={
        "ConversationalSearchRequest",
        "ConversationalSearchResponse",
    },
)


class ConversationalSearchRequest(proto.Message):
    r"""Request message for
    [ConversationalSearchService.ConversationalSearch][google.cloud.retail.v2alpha.ConversationalSearchService.ConversationalSearch]
    method.

    Attributes:
        placement (str):
            Required. The resource name of the search engine placement,
            such as
            ``projects/*/locations/global/catalogs/default_catalog/placements/default_search``
            or
            ``projects/*/locations/global/catalogs/default_catalog/servingConfigs/default_serving_config``
            This field is used to identify the serving config name and
            the set of models that will be used to make the search.
        branch (str):
            Required. The branch resource name, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/0``.

            Use "default_branch" as the branch ID or leave this field
            empty, to search products under the default branch.
        query (str):
            Optional. Raw search query to be searched
            for.
            If this field is empty, the request is
            considered a category browsing request.
        page_categories (MutableSequence[str]):
            Optional. The categories associated with a category page.
            Must be set for category navigation queries to achieve good
            search quality. The format should be the same as
            [UserEvent.page_categories][google.cloud.retail.v2alpha.UserEvent.page_categories];

            To represent full path of category, use '>' sign to separate
            different hierarchies. If '>' is part of the category name,
            replace it with other character(s).

            Category pages include special pages such as sales or
            promotions. For instance, a special sale page may have the
            category hierarchy: "pageCategories" : ["Sales > 2017 Black
            Friday Deals"].
        conversation_id (str):
            Optional. This field specifies the conversation id, which
            maintains the state of the conversation between client side
            and server side. Use the value from the previous
            [ConversationalSearchResponse.conversation_id][google.cloud.retail.v2alpha.ConversationalSearchResponse.conversation_id].
            For the initial request, this should be empty.
        search_params (google.cloud.retail_v2alpha.types.ConversationalSearchRequest.SearchParams):
            Optional. Search parameters.
        visitor_id (str):
            Required. A unique identifier for tracking visitors. For
            example, this could be implemented with an HTTP cookie,
            which should be able to uniquely identify a visitor on a
            single device. This unique identifier should not change if
            the visitor logs in or out of the website.

            This should be the same identifier as
            [UserEvent.visitor_id][google.cloud.retail.v2alpha.UserEvent.visitor_id].

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.
        user_info (google.cloud.retail_v2alpha.types.UserInfo):
            Optional. User information.
        conversational_filtering_spec (google.cloud.retail_v2alpha.types.ConversationalSearchRequest.ConversationalFilteringSpec):
            Optional. This field specifies all
            conversational filtering related parameters.
    """

    class SearchParams(proto.Message):
        r"""Search parameters.

        Attributes:
            filter (str):
                Optional. The filter string to restrict search results.

                The syntax of the filter string is the same as
                [SearchRequest.filter][google.cloud.retail.v2alpha.SearchRequest.filter].
            canonical_filter (str):
                Optional. The canonical filter string to restrict search
                results.

                The syntax of the canonical filter string is the same as
                [SearchRequest.canonical_filter][google.cloud.retail.v2alpha.SearchRequest.canonical_filter].
            sort_by (str):
                Optional. The sort string to specify the sorting of search
                results.

                The syntax of the sort string is the same as
                [SearchRequest.sort][].
            boost_spec (google.cloud.retail_v2alpha.types.SearchRequest.BoostSpec):
                Optional. The boost spec to specify the boosting of search
                results.

                The syntax of the boost spec is the same as
                [SearchRequest.boost_spec][google.cloud.retail.v2alpha.SearchRequest.boost_spec].
        """

        filter: str = proto.Field(
            proto.STRING,
            number=1,
        )
        canonical_filter: str = proto.Field(
            proto.STRING,
            number=2,
        )
        sort_by: str = proto.Field(
            proto.STRING,
            number=3,
        )
        boost_spec: search_service.SearchRequest.BoostSpec = proto.Field(
            proto.MESSAGE,
            number=4,
            message=search_service.SearchRequest.BoostSpec,
        )

    class UserAnswer(proto.Message):
        r"""This field specifies the current user answer during the
        conversational filtering search. This can be either user
        selected from suggested answers or user input plain text.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            text_answer (str):
                This field specifies the incremental input
                text from the user during the conversational
                search.

                This field is a member of `oneof`_ ``type``.
            selected_answer (google.cloud.retail_v2alpha.types.ConversationalSearchRequest.UserAnswer.SelectedAnswer):
                Optional. This field specifies the selected answer during
                the conversational search. This should be a subset of
                [ConversationalSearchResponse.followup_question.suggested_answers][].

                This field is a member of `oneof`_ ``type``.
        """

        class SelectedAnswer(proto.Message):
            r"""This field specifies the selected answers during the
            conversational search.

            Attributes:
                product_attribute_value (google.cloud.retail_v2alpha.types.ProductAttributeValue):
                    Optional. This field specifies the selected
                    answer which is a attribute key-value.
            """

            product_attribute_value: search_service.ProductAttributeValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=search_service.ProductAttributeValue,
            )

        text_answer: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="type",
        )
        selected_answer: "ConversationalSearchRequest.UserAnswer.SelectedAnswer" = (
            proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="type",
                message="ConversationalSearchRequest.UserAnswer.SelectedAnswer",
            )
        )

    class ConversationalFilteringSpec(proto.Message):
        r"""This field specifies all conversational filtering related
        parameters addition to conversational retail search.

        Attributes:
            enable_conversational_filtering (bool):
                Optional. This field is deprecated. Please use
                [ConversationalFilteringSpec.conversational_filtering_mode][google.cloud.retail.v2alpha.ConversationalSearchRequest.ConversationalFilteringSpec.conversational_filtering_mode]
                instead.
            user_answer (google.cloud.retail_v2alpha.types.ConversationalSearchRequest.UserAnswer):
                Optional. This field specifies the current
                user answer during the conversational filtering
                search. It can be either user selected from
                suggested answers or user input plain text.
            conversational_filtering_mode (google.cloud.retail_v2alpha.types.ConversationalSearchRequest.ConversationalFilteringSpec.Mode):
                Optional. Mode to control Conversational Filtering. Defaults
                to
                [Mode.DISABLED][google.cloud.retail.v2alpha.ConversationalSearchRequest.ConversationalFilteringSpec.Mode.DISABLED]
                if it's unset.
        """

        class Mode(proto.Enum):
            r"""Enum to control Conversational Filtering mode.

            Values:
                MODE_UNSPECIFIED (0):
                    Default value.
                CONVERSATIONAL_FILTER_ONLY (3):
                    Enabled Conversational Filtering without
                    default Conversational Search.
            """
            MODE_UNSPECIFIED = 0
            CONVERSATIONAL_FILTER_ONLY = 3

        enable_conversational_filtering: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        user_answer: "ConversationalSearchRequest.UserAnswer" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="ConversationalSearchRequest.UserAnswer",
        )
        conversational_filtering_mode: "ConversationalSearchRequest.ConversationalFilteringSpec.Mode" = proto.Field(
            proto.ENUM,
            number=4,
            enum="ConversationalSearchRequest.ConversationalFilteringSpec.Mode",
        )

    placement: str = proto.Field(
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
    page_categories: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    conversation_id: str = proto.Field(
        proto.STRING,
        number=5,
    )
    search_params: SearchParams = proto.Field(
        proto.MESSAGE,
        number=6,
        message=SearchParams,
    )
    visitor_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    user_info: common.UserInfo = proto.Field(
        proto.MESSAGE,
        number=7,
        message=common.UserInfo,
    )
    conversational_filtering_spec: ConversationalFilteringSpec = proto.Field(
        proto.MESSAGE,
        number=8,
        message=ConversationalFilteringSpec,
    )


class ConversationalSearchResponse(proto.Message):
    r"""Response message for
    [ConversationalSearchService.ConversationalSearch][google.cloud.retail.v2alpha.ConversationalSearchService.ConversationalSearch]
    method.

    Attributes:
        conversation_id (str):
            Conversation UUID. This field will be stored in client side
            storage to maintain the conversation session with server and
            will be used for next search request's
            [ConversationalSearchRequest.conversation_id][google.cloud.retail.v2alpha.ConversationalSearchRequest.conversation_id]
            to restore conversation state in server.
        refined_search (MutableSequence[google.cloud.retail_v2alpha.types.ConversationalSearchResponse.RefinedSearch]):
            The proposed refined search queries. They can be used to
            fetch the relevant search results. When using
            CONVERSATIONAL_FILTER_ONLY mode, the refined_query from
            search response will be populated here.
        conversational_filtering_result (google.cloud.retail_v2alpha.types.ConversationalSearchResponse.ConversationalFilteringResult):
            This field specifies all related information
            that is needed on client side for UI rendering
            of conversational filtering search.
    """

    class FollowupQuestion(proto.Message):
        r"""The conversational followup question generated for Intent
        refinement.

        Attributes:
            followup_question (str):
                The conversational followup question
                generated for Intent refinement.
            suggested_answers (MutableSequence[google.cloud.retail_v2alpha.types.ConversationalSearchResponse.FollowupQuestion.SuggestedAnswer]):
                The answer options provided to client for the
                follow-up question.
        """

        class SuggestedAnswer(proto.Message):
            r"""Suggested answers to the follow-up question.

            Attributes:
                product_attribute_value (google.cloud.retail_v2alpha.types.ProductAttributeValue):
                    Product attribute value, including an
                    attribute key and an attribute value. Other
                    types can be added here in the future.
            """

            product_attribute_value: search_service.ProductAttributeValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=search_service.ProductAttributeValue,
            )

        followup_question: str = proto.Field(
            proto.STRING,
            number=1,
        )
        suggested_answers: MutableSequence[
            "ConversationalSearchResponse.FollowupQuestion.SuggestedAnswer"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ConversationalSearchResponse.FollowupQuestion.SuggestedAnswer",
        )

    class RefinedSearch(proto.Message):
        r"""The proposed refined search for intent-refinement/bundled shopping
        conversation. When using CONVERSATIONAL_FILTER_ONLY mode, the
        refined_query from search response will be populated here.

        Attributes:
            query (str):
                The query to be used for search.
        """

        query: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class ConversationalFilteringResult(proto.Message):
        r"""This field specifies all related information that is needed
        on client side for UI rendering of conversational filtering
        search.

        Attributes:
            followup_question (google.cloud.retail_v2alpha.types.ConversationalSearchResponse.FollowupQuestion):
                The conversational filtering question.
            additional_filter (google.cloud.retail_v2alpha.types.ConversationalSearchResponse.ConversationalFilteringResult.AdditionalFilter):
                This is the incremental additional filters implied from the
                current user answer. User should add the suggested addition
                filters to the previous
                [ConversationalSearchRequest.search_params.filter][] and
                [SearchRequest.filter][google.cloud.retail.v2alpha.SearchRequest.filter],
                and use the merged filter in the follow up requests.
        """

        class AdditionalFilter(proto.Message):
            r"""Additional filter that client side need to apply.

            Attributes:
                product_attribute_value (google.cloud.retail_v2alpha.types.ProductAttributeValue):
                    Product attribute value, including an
                    attribute key and an attribute value. Other
                    types can be added here in the future.
            """

            product_attribute_value: search_service.ProductAttributeValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=search_service.ProductAttributeValue,
            )

        followup_question: "ConversationalSearchResponse.FollowupQuestion" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                message="ConversationalSearchResponse.FollowupQuestion",
            )
        )
        additional_filter: "ConversationalSearchResponse.ConversationalFilteringResult.AdditionalFilter" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="ConversationalSearchResponse.ConversationalFilteringResult.AdditionalFilter",
        )

    conversation_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    refined_search: MutableSequence[RefinedSearch] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=RefinedSearch,
    )
    conversational_filtering_result: ConversationalFilteringResult = proto.Field(
        proto.MESSAGE,
        number=7,
        message=ConversationalFilteringResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
