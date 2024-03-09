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

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1alpha.types import conversation as gcd_conversation
from google.cloud.discoveryengine_v1alpha.types import search_service

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1alpha",
    manifest={
        "ConverseConversationRequest",
        "ConverseConversationResponse",
        "CreateConversationRequest",
        "UpdateConversationRequest",
        "DeleteConversationRequest",
        "GetConversationRequest",
        "ListConversationsRequest",
        "ListConversationsResponse",
    },
)


class ConverseConversationRequest(proto.Message):
    r"""Request message for
    [ConversationalSearchService.ConverseConversation][google.cloud.discoveryengine.v1alpha.ConversationalSearchService.ConverseConversation]
    method.

    Attributes:
        name (str):
            Required. The resource name of the Conversation to get.
            Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}/conversations/{conversation_id}``.
            Use
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}/conversations/-``
            to activate auto session mode, which automatically creates a
            new conversation inside a ConverseConversation session.
        query (google.cloud.discoveryengine_v1alpha.types.TextInput):
            Required. Current user input.
        serving_config (str):
            The resource name of the Serving Config to use. Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}/servingConfigs/{serving_config_id}``
            If this is not set, the default serving config will be used.
        conversation (google.cloud.discoveryengine_v1alpha.types.Conversation):
            The conversation to be used by auto session
            only. The name field will be ignored as we
            automatically assign new name for the
            conversation in auto session.
        safe_search (bool):
            Whether to turn on safe search.
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
        summary_spec (google.cloud.discoveryengine_v1alpha.types.SearchRequest.ContentSearchSpec.SummarySpec):
            A specification for configuring the summary
            returned in the response.
        filter (str):
            The filter syntax consists of an expression language for
            constructing a predicate from one or more fields of the
            documents being filtered. Filter expression is
            case-sensitive. This will be used to filter search results
            which may affect the summary response.

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
        boost_spec (google.cloud.discoveryengine_v1alpha.types.SearchRequest.BoostSpec):
            Boost specification to boost certain documents in search
            results which may affect the converse response. For more
            information on boosting, see
            `Boosting <https://cloud.google.com/retail/docs/boosting#boost>`__
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: gcd_conversation.TextInput = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_conversation.TextInput,
    )
    serving_config: str = proto.Field(
        proto.STRING,
        number=3,
    )
    conversation: gcd_conversation.Conversation = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcd_conversation.Conversation,
    )
    safe_search: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    user_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    summary_spec: search_service.SearchRequest.ContentSearchSpec.SummarySpec = (
        proto.Field(
            proto.MESSAGE,
            number=8,
            message=search_service.SearchRequest.ContentSearchSpec.SummarySpec,
        )
    )
    filter: str = proto.Field(
        proto.STRING,
        number=9,
    )
    boost_spec: search_service.SearchRequest.BoostSpec = proto.Field(
        proto.MESSAGE,
        number=10,
        message=search_service.SearchRequest.BoostSpec,
    )


class ConverseConversationResponse(proto.Message):
    r"""Response message for
    [ConversationalSearchService.ConverseConversation][google.cloud.discoveryengine.v1alpha.ConversationalSearchService.ConverseConversation]
    method.

    Attributes:
        reply (google.cloud.discoveryengine_v1alpha.types.Reply):
            Answer to the current query.
        conversation (google.cloud.discoveryengine_v1alpha.types.Conversation):
            Updated conversation including the answer.
        related_questions (MutableSequence[str]):
            Suggested related questions.
        search_results (MutableSequence[google.cloud.discoveryengine_v1alpha.types.SearchResponse.SearchResult]):
            Search Results.
    """

    reply: gcd_conversation.Reply = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_conversation.Reply,
    )
    conversation: gcd_conversation.Conversation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_conversation.Conversation,
    )
    related_questions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    search_results: MutableSequence[
        search_service.SearchResponse.SearchResult
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=search_service.SearchResponse.SearchResult,
    )


class CreateConversationRequest(proto.Message):
    r"""Request for CreateConversation method.

    Attributes:
        parent (str):
            Required. Full resource name of parent data store. Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}``
        conversation (google.cloud.discoveryengine_v1alpha.types.Conversation):
            Required. The conversation to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation: gcd_conversation.Conversation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_conversation.Conversation,
    )


class UpdateConversationRequest(proto.Message):
    r"""Request for UpdateConversation method.

    Attributes:
        conversation (google.cloud.discoveryengine_v1alpha.types.Conversation):
            Required. The Conversation to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [Conversation][google.cloud.discoveryengine.v1alpha.Conversation]
            to update. The following are NOT supported:

            -  [Conversation.name][google.cloud.discoveryengine.v1alpha.Conversation.name]

            If not set or empty, all supported fields are updated.
    """

    conversation: gcd_conversation.Conversation = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_conversation.Conversation,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteConversationRequest(proto.Message):
    r"""Request for DeleteConversation method.

    Attributes:
        name (str):
            Required. The resource name of the Conversation to delete.
            Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}/conversations/{conversation_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetConversationRequest(proto.Message):
    r"""Request for GetConversation method.

    Attributes:
        name (str):
            Required. The resource name of the Conversation to get.
            Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}/conversations/{conversation_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListConversationsRequest(proto.Message):
    r"""Request for ListConversations method.

    Attributes:
        parent (str):
            Required. The data store resource name. Format:
            ``projects/{project_number}/locations/{location_id}/collections/{collection}/dataStores/{data_store_id}``
        page_size (int):
            Maximum number of results to return. If
            unspecified, defaults to 50. Max allowed value
            is 1000.
        page_token (str):
            A page token, received from a previous ``ListConversations``
            call. Provide this to retrieve the subsequent page.
        filter (str):
            A filter to apply on the list results. The supported
            features are: user_pseudo_id, state.

            Example: "user_pseudo_id = some_id".
        order_by (str):
            A comma-separated list of fields to order by, sorted in
            ascending order. Use "desc" after a field name for
            descending. Supported fields:

            -  ``update_time``
            -  ``create_time``
            -  ``conversation_name``

            Example: "update_time desc" "create_time".
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListConversationsResponse(proto.Message):
    r"""Response for ListConversations method.

    Attributes:
        conversations (MutableSequence[google.cloud.discoveryengine_v1alpha.types.Conversation]):
            All the Conversations for a given data store.
        next_page_token (str):
            Pagination token, if not returned indicates
            the last page.
    """

    @property
    def raw_page(self):
        return self

    conversations: MutableSequence[gcd_conversation.Conversation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_conversation.Conversation,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
