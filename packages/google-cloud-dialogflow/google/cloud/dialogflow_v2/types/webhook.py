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

from google.protobuf import struct_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dialogflow_v2.types import context, intent
from google.cloud.dialogflow_v2.types import session as gcd_session
from google.cloud.dialogflow_v2.types import session_entity_type

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={
        "WebhookRequest",
        "WebhookResponse",
        "OriginalDetectIntentRequest",
    },
)


class WebhookRequest(proto.Message):
    r"""The request message for a webhook call.

    Attributes:
        session (str):
            The unique identifier of detectIntent request session. Can
            be used to identify end-user inside webhook implementation.
            Format:
            ``projects/<Project ID>/agent/sessions/<Session ID>``, or
            ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``.
        response_id (str):
            The unique identifier of the response. Contains the same
            value as ``[Streaming]DetectIntentResponse.response_id``.
        query_result (google.cloud.dialogflow_v2.types.QueryResult):
            The result of the conversational query or event processing.
            Contains the same value as
            ``[Streaming]DetectIntentResponse.query_result``.
        original_detect_intent_request (google.cloud.dialogflow_v2.types.OriginalDetectIntentRequest):
            Optional. The contents of the original request that was
            passed to ``[Streaming]DetectIntent`` call.
    """

    session: str = proto.Field(
        proto.STRING,
        number=4,
    )
    response_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query_result: gcd_session.QueryResult = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_session.QueryResult,
    )
    original_detect_intent_request: "OriginalDetectIntentRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OriginalDetectIntentRequest",
    )


class WebhookResponse(proto.Message):
    r"""The response message for a webhook call.

    This response is validated by the Dialogflow server. If validation
    fails, an error will be returned in the
    [QueryResult.diagnostic_info][google.cloud.dialogflow.v2.QueryResult.diagnostic_info]
    field. Setting JSON fields to an empty value with the wrong type is
    a common error. To avoid this error:

    -  Use ``""`` for empty strings
    -  Use ``{}`` or ``null`` for empty objects
    -  Use ``[]`` or ``null`` for empty arrays

    For more information, see the `Protocol Buffers Language
    Guide <https://developers.google.com/protocol-buffers/docs/proto3#json>`__.

    Attributes:
        fulfillment_text (str):
            Optional. The text response message intended for the
            end-user. It is recommended to use
            ``fulfillment_messages.text.text[0]`` instead. When
            provided, Dialogflow uses this field to populate
            [QueryResult.fulfillment_text][google.cloud.dialogflow.v2.QueryResult.fulfillment_text]
            sent to the integration or API caller.
        fulfillment_messages (MutableSequence[google.cloud.dialogflow_v2.types.Intent.Message]):
            Optional. The rich response messages intended for the
            end-user. When provided, Dialogflow uses this field to
            populate
            [QueryResult.fulfillment_messages][google.cloud.dialogflow.v2.QueryResult.fulfillment_messages]
            sent to the integration or API caller.
        source (str):
            Optional. A custom field used to identify the webhook
            source. Arbitrary strings are supported. When provided,
            Dialogflow uses this field to populate
            [QueryResult.webhook_source][google.cloud.dialogflow.v2.QueryResult.webhook_source]
            sent to the integration or API caller.
        payload (google.protobuf.struct_pb2.Struct):
            Optional. This field can be used to pass custom data from
            your webhook to the integration or API caller. Arbitrary
            JSON objects are supported. When provided, Dialogflow uses
            this field to populate
            [QueryResult.webhook_payload][google.cloud.dialogflow.v2.QueryResult.webhook_payload]
            sent to the integration or API caller. This field is also
            used by the `Google Assistant
            integration <https://cloud.google.com/dialogflow/docs/integrations/aog>`__
            for rich response messages. See the format definition at
            `Google Assistant Dialogflow webhook
            format <https://developers.google.com/assistant/actions/build/json/dialogflow-webhook-json>`__
        output_contexts (MutableSequence[google.cloud.dialogflow_v2.types.Context]):
            Optional. The collection of output contexts that will
            overwrite currently active contexts for the session and
            reset their lifespans. When provided, Dialogflow uses this
            field to populate
            [QueryResult.output_contexts][google.cloud.dialogflow.v2.QueryResult.output_contexts]
            sent to the integration or API caller.
        followup_event_input (google.cloud.dialogflow_v2.types.EventInput):
            Optional. Invokes the supplied events. When this field is
            set, Dialogflow ignores the ``fulfillment_text``,
            ``fulfillment_messages``, and ``payload`` fields.
        session_entity_types (MutableSequence[google.cloud.dialogflow_v2.types.SessionEntityType]):
            Optional. Additional session entity types to replace or
            extend developer entity types with. The entity synonyms
            apply to all languages and persist for the session. Setting
            this data from a webhook overwrites the session entity types
            that have been set using ``detectIntent``,
            ``streamingDetectIntent`` or
            [SessionEntityType][google.cloud.dialogflow.v2.SessionEntityType]
            management methods.
    """

    fulfillment_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    fulfillment_messages: MutableSequence[intent.Intent.Message] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=intent.Intent.Message,
    )
    source: str = proto.Field(
        proto.STRING,
        number=3,
    )
    payload: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )
    output_contexts: MutableSequence[context.Context] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=context.Context,
    )
    followup_event_input: gcd_session.EventInput = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gcd_session.EventInput,
    )
    session_entity_types: MutableSequence[
        session_entity_type.SessionEntityType
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=session_entity_type.SessionEntityType,
    )


class OriginalDetectIntentRequest(proto.Message):
    r"""Represents the contents of the original request that was passed to
    the ``[Streaming]DetectIntent`` call.

    Attributes:
        source (str):
            The source of this request, e.g., ``google``, ``facebook``,
            ``slack``. It is set by Dialogflow-owned servers.
        version (str):
            Optional. The version of the protocol used
            for this request. This field is AoG-specific.
        payload (google.protobuf.struct_pb2.Struct):
            Optional. This field is set to the value of the
            ``QueryParameters.payload`` field passed in the request.
            Some integrations that query a Dialogflow agent may provide
            additional information in the payload.

            In particular, for the Dialogflow Phone Gateway integration,
            this field has the form:

            .. raw:: html

                <pre>{
                 "telephony": {
                   "caller_id": "+18558363987"
                 }
                }</pre>

            Note: The caller ID field (``caller_id``) will be redacted
            for Trial Edition agents and populated with the caller ID in
            `E.164 format <https://en.wikipedia.org/wiki/E.164>`__ for
            Essentials Edition agents.
    """

    source: str = proto.Field(
        proto.STRING,
        number=1,
    )
    version: str = proto.Field(
        proto.STRING,
        number=2,
    )
    payload: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
