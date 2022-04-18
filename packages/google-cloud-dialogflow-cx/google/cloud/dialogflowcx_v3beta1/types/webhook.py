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
import proto  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import response_message
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "Webhook",
        "ListWebhooksRequest",
        "ListWebhooksResponse",
        "GetWebhookRequest",
        "CreateWebhookRequest",
        "UpdateWebhookRequest",
        "DeleteWebhookRequest",
        "WebhookRequest",
        "WebhookResponse",
        "PageInfo",
        "SessionInfo",
    },
)


class Webhook(proto.Message):
    r"""Webhooks host the developer's business logic. During a
    session, webhooks allow the developer to use the data extracted
    by Dialogflow's natural language processing to generate dynamic
    responses, validate collected data, or trigger actions on the
    backend.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The unique identifier of the webhook. Required for the
            [Webhooks.UpdateWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.UpdateWebhook]
            method.
            [Webhooks.CreateWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.CreateWebhook]
            populates the name automatically. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/webhooks/<Webhook ID>``.
        display_name (str):
            Required. The human-readable name of the
            webhook, unique within the agent.
        generic_web_service (google.cloud.dialogflowcx_v3beta1.types.Webhook.GenericWebService):
            Configuration for a generic web service.

            This field is a member of `oneof`_ ``webhook``.
        service_directory (google.cloud.dialogflowcx_v3beta1.types.Webhook.ServiceDirectoryConfig):
            Configuration for a `Service
            Directory <https://cloud.google.com/service-directory>`__
            service.

            This field is a member of `oneof`_ ``webhook``.
        timeout (google.protobuf.duration_pb2.Duration):
            Webhook execution timeout. Execution is
            considered failed if Dialogflow doesn't receive
            a response from webhook at the end of the
            timeout period. Defaults to 5 seconds, maximum
            allowed timeout is 30 seconds.
        disabled (bool):
            Indicates whether the webhook is disabled.
    """

    class GenericWebService(proto.Message):
        r"""Represents configuration for a generic web service.

        Attributes:
            uri (str):
                Required. The webhook URI for receiving POST
                requests. It must use https protocol.
            username (str):
                The user name for HTTP Basic authentication.
            password (str):
                The password for HTTP Basic authentication.
            request_headers (Mapping[str, str]):
                The HTTP request headers to send together
                with webhook requests.
            allowed_ca_certs (Sequence[bytes]):
                Optional. Specifies a list of allowed custom CA certificates
                (in DER format) for HTTPS verification. This overrides the
                default SSL trust store. If this is empty or unspecified,
                Dialogflow will use Google's default trust store to verify
                certificates. N.B. Make sure the HTTPS server certificates
                are signed with "subject alt name". For instance a
                certificate can be self-signed using the following command,

                ::

                      openssl x509 -req -days 200 -in example.com.csr \
                        -signkey example.com.key \
                        -out example.com.crt \
                        -extfile <(printf "\nsubjectAltName='DNS:www.example.com'")
        """

        uri = proto.Field(
            proto.STRING,
            number=1,
        )
        username = proto.Field(
            proto.STRING,
            number=2,
        )
        password = proto.Field(
            proto.STRING,
            number=3,
        )
        request_headers = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=4,
        )
        allowed_ca_certs = proto.RepeatedField(
            proto.BYTES,
            number=5,
        )

    class ServiceDirectoryConfig(proto.Message):
        r"""Represents configuration for a `Service
        Directory <https://cloud.google.com/service-directory>`__ service.

        Attributes:
            service (str):
                Required. The name of `Service
                Directory <https://cloud.google.com/service-directory>`__
                service. Format:
                ``projects/<Project ID>/locations/<Location ID>/namespaces/<Namespace ID>/services/<Service ID>``.
                ``Location ID`` of the service directory must be the same as
                the location of the agent.
            generic_web_service (google.cloud.dialogflowcx_v3beta1.types.Webhook.GenericWebService):
                Generic Service configuration of this
                webhook.
        """

        service = proto.Field(
            proto.STRING,
            number=1,
        )
        generic_web_service = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Webhook.GenericWebService",
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    generic_web_service = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="webhook",
        message=GenericWebService,
    )
    service_directory = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="webhook",
        message=ServiceDirectoryConfig,
    )
    timeout = proto.Field(
        proto.MESSAGE,
        number=6,
        message=duration_pb2.Duration,
    )
    disabled = proto.Field(
        proto.BOOL,
        number=5,
    )


class ListWebhooksRequest(proto.Message):
    r"""The request message for
    [Webhooks.ListWebhooks][google.cloud.dialogflow.cx.v3beta1.Webhooks.ListWebhooks].

    Attributes:
        parent (str):
            Required. The agent to list all webhooks for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListWebhooksResponse(proto.Message):
    r"""The response message for
    [Webhooks.ListWebhooks][google.cloud.dialogflow.cx.v3beta1.Webhooks.ListWebhooks].

    Attributes:
        webhooks (Sequence[google.cloud.dialogflowcx_v3beta1.types.Webhook]):
            The list of webhooks. There will be a maximum number of
            items returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    webhooks = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Webhook",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetWebhookRequest(proto.Message):
    r"""The request message for
    [Webhooks.GetWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.GetWebhook].

    Attributes:
        name (str):
            Required. The name of the webhook. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/webhooks/<Webhook ID>``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateWebhookRequest(proto.Message):
    r"""The request message for
    [Webhooks.CreateWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.CreateWebhook].

    Attributes:
        parent (str):
            Required. The agent to create a webhook for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        webhook (google.cloud.dialogflowcx_v3beta1.types.Webhook):
            Required. The webhook to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    webhook = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Webhook",
    )


class UpdateWebhookRequest(proto.Message):
    r"""The request message for
    [Webhooks.UpdateWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.UpdateWebhook].

    Attributes:
        webhook (google.cloud.dialogflowcx_v3beta1.types.Webhook):
            Required. The webhook to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    webhook = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Webhook",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteWebhookRequest(proto.Message):
    r"""The request message for
    [Webhooks.DeleteWebhook][google.cloud.dialogflow.cx.v3beta1.Webhooks.DeleteWebhook].

    Attributes:
        name (str):
            Required. The name of the webhook to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/webhooks/<Webhook ID>``.
        force (bool):
            This field has no effect for webhook not being used. For
            webhooks that are used by pages/flows/transition route
            groups:

            -  If ``force`` is set to false, an error will be returned
               with message indicating the referenced resources.
            -  If ``force`` is set to true, Dialogflow will remove the
               webhook, as well as any references to the webhook (i.e.
               [Webhook][google.cloud.dialogflow.cx.v3beta1.Fulfillment.webhook]
               and
               [tag][google.cloud.dialogflow.cx.v3beta1.Fulfillment.tag]in
               fulfillments that point to this webhook will be removed).
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    force = proto.Field(
        proto.BOOL,
        number=2,
    )


class WebhookRequest(proto.Message):
    r"""The request message for a webhook call. The request is sent
    as a JSON object and the field names will be presented in camel
    cases.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        detect_intent_response_id (str):
            Always present. The unique identifier of the
            [DetectIntentResponse][google.cloud.dialogflow.cx.v3beta1.DetectIntentResponse]
            that will be returned to the API caller.
        text (str):
            If [natural language
            text][google.cloud.dialogflow.cx.v3beta1.TextInput] was
            provided as input, this field will contain a copy of the
            text.

            This field is a member of `oneof`_ ``query``.
        trigger_intent (str):
            If an
            [intent][google.cloud.dialogflow.cx.v3beta1.IntentInput] was
            provided as input, this field will contain a copy of the
            intent identifier. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.

            This field is a member of `oneof`_ ``query``.
        transcript (str):
            If [natural language speech
            audio][google.cloud.dialogflow.cx.v3beta1.AudioInput] was
            provided as input, this field will contain the transcript
            for the audio.

            This field is a member of `oneof`_ ``query``.
        trigger_event (str):
            If an [event][google.cloud.dialogflow.cx.v3beta1.EventInput]
            was provided as input, this field will contain the name of
            the event.

            This field is a member of `oneof`_ ``query``.
        language_code (str):
            The language code specified in the [original
            request][QueryInput.language_code].
        fulfillment_info (google.cloud.dialogflowcx_v3beta1.types.WebhookRequest.FulfillmentInfo):
            Always present. Information about the
            fulfillment that triggered this webhook call.
        intent_info (google.cloud.dialogflowcx_v3beta1.types.WebhookRequest.IntentInfo):
            Information about the last matched intent.
        page_info (google.cloud.dialogflowcx_v3beta1.types.PageInfo):
            Information about page status.
        session_info (google.cloud.dialogflowcx_v3beta1.types.SessionInfo):
            Information about session status.
        messages (Sequence[google.cloud.dialogflowcx_v3beta1.types.ResponseMessage]):
            The list of rich message responses to present to the user.
            Webhook can choose to append or replace this list in
            [WebhookResponse.fulfillment_response][google.cloud.dialogflow.cx.v3beta1.WebhookResponse.fulfillment_response];
        payload (google.protobuf.struct_pb2.Struct):
            Custom data set in
            [QueryParameters.payload][google.cloud.dialogflow.cx.v3beta1.QueryParameters.payload].
        sentiment_analysis_result (google.cloud.dialogflowcx_v3beta1.types.WebhookRequest.SentimentAnalysisResult):
            The sentiment analysis result of the current
            user request. The field is filled when sentiment
            analysis is configured to be enabled for the
            request.
    """

    class FulfillmentInfo(proto.Message):
        r"""Represents fulfillment information communicated to the
        webhook.

        Attributes:
            tag (str):
                Always present. The value of the
                [Fulfillment.tag][google.cloud.dialogflow.cx.v3beta1.Fulfillment.tag]
                field will be populated in this field by Dialogflow when the
                associated webhook is called. The tag is typically used by
                the webhook service to identify which fulfillment is being
                called, but it could be used for other purposes.
        """

        tag = proto.Field(
            proto.STRING,
            number=1,
        )

    class IntentInfo(proto.Message):
        r"""Represents intent information communicated to the webhook.

        Attributes:
            last_matched_intent (str):
                Always present. The unique identifier of the last matched
                [intent][google.cloud.dialogflow.cx.v3beta1.Intent]. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
            display_name (str):
                Always present. The display name of the last matched
                [intent][google.cloud.dialogflow.cx.v3beta1.Intent].
            parameters (Mapping[str, google.cloud.dialogflowcx_v3beta1.types.WebhookRequest.IntentInfo.IntentParameterValue]):
                Parameters identified as a result of intent
                matching. This is a map of the name of the
                identified parameter to the value of the
                parameter identified from the user's utterance.
                All parameters defined in the matched intent
                that are identified will be surfaced here.
            confidence (float):
                The confidence of the matched intent. Values
                range from 0.0 (completely uncertain) to 1.0
                (completely certain).
        """

        class IntentParameterValue(proto.Message):
            r"""Represents a value for an intent parameter.

            Attributes:
                original_value (str):
                    Always present. Original text value extracted
                    from user utterance.
                resolved_value (google.protobuf.struct_pb2.Value):
                    Always present. Structured value for the
                    parameter extracted from user utterance.
            """

            original_value = proto.Field(
                proto.STRING,
                number=1,
            )
            resolved_value = proto.Field(
                proto.MESSAGE,
                number=2,
                message=struct_pb2.Value,
            )

        last_matched_intent = proto.Field(
            proto.STRING,
            number=1,
        )
        display_name = proto.Field(
            proto.STRING,
            number=3,
        )
        parameters = proto.MapField(
            proto.STRING,
            proto.MESSAGE,
            number=2,
            message="WebhookRequest.IntentInfo.IntentParameterValue",
        )
        confidence = proto.Field(
            proto.FLOAT,
            number=4,
        )

    class SentimentAnalysisResult(proto.Message):
        r"""Represents the result of sentiment analysis.

        Attributes:
            score (float):
                Sentiment score between -1.0 (negative
                sentiment) and 1.0 (positive sentiment).
            magnitude (float):
                A non-negative number in the [0, +inf) range, which
                represents the absolute magnitude of sentiment, regardless
                of score (positive or negative).
        """

        score = proto.Field(
            proto.FLOAT,
            number=1,
        )
        magnitude = proto.Field(
            proto.FLOAT,
            number=2,
        )

    detect_intent_response_id = proto.Field(
        proto.STRING,
        number=1,
    )
    text = proto.Field(
        proto.STRING,
        number=10,
        oneof="query",
    )
    trigger_intent = proto.Field(
        proto.STRING,
        number=11,
        oneof="query",
    )
    transcript = proto.Field(
        proto.STRING,
        number=12,
        oneof="query",
    )
    trigger_event = proto.Field(
        proto.STRING,
        number=14,
        oneof="query",
    )
    language_code = proto.Field(
        proto.STRING,
        number=15,
    )
    fulfillment_info = proto.Field(
        proto.MESSAGE,
        number=6,
        message=FulfillmentInfo,
    )
    intent_info = proto.Field(
        proto.MESSAGE,
        number=3,
        message=IntentInfo,
    )
    page_info = proto.Field(
        proto.MESSAGE,
        number=4,
        message="PageInfo",
    )
    session_info = proto.Field(
        proto.MESSAGE,
        number=5,
        message="SessionInfo",
    )
    messages = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=response_message.ResponseMessage,
    )
    payload = proto.Field(
        proto.MESSAGE,
        number=8,
        message=struct_pb2.Struct,
    )
    sentiment_analysis_result = proto.Field(
        proto.MESSAGE,
        number=9,
        message=SentimentAnalysisResult,
    )


class WebhookResponse(proto.Message):
    r"""The response message for a webhook call.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        fulfillment_response (google.cloud.dialogflowcx_v3beta1.types.WebhookResponse.FulfillmentResponse):
            The fulfillment response to send to the user.
            This field can be omitted by the webhook if it
            does not intend to send any response to the
            user.
        page_info (google.cloud.dialogflowcx_v3beta1.types.PageInfo):
            Information about page status. This field can
            be omitted by the webhook if it does not intend
            to modify page status.
        session_info (google.cloud.dialogflowcx_v3beta1.types.SessionInfo):
            Information about session status. This field
            can be omitted by the webhook if it does not
            intend to modify session status.
        payload (google.protobuf.struct_pb2.Struct):
            Value to append directly to
            [QueryResult.webhook_payloads][google.cloud.dialogflow.cx.v3beta1.QueryResult.webhook_payloads].
        target_page (str):
            The target page to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.

            This field is a member of `oneof`_ ``transition``.
        target_flow (str):
            The target flow to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

            This field is a member of `oneof`_ ``transition``.
    """

    class FulfillmentResponse(proto.Message):
        r"""Represents a fulfillment response to the user.

        Attributes:
            messages (Sequence[google.cloud.dialogflowcx_v3beta1.types.ResponseMessage]):
                The list of rich message responses to present
                to the user.
            merge_behavior (google.cloud.dialogflowcx_v3beta1.types.WebhookResponse.FulfillmentResponse.MergeBehavior):
                Merge behavior for ``messages``.
        """

        class MergeBehavior(proto.Enum):
            r"""Defines merge behavior for ``messages``."""
            MERGE_BEHAVIOR_UNSPECIFIED = 0
            APPEND = 1
            REPLACE = 2

        messages = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=response_message.ResponseMessage,
        )
        merge_behavior = proto.Field(
            proto.ENUM,
            number=2,
            enum="WebhookResponse.FulfillmentResponse.MergeBehavior",
        )

    fulfillment_response = proto.Field(
        proto.MESSAGE,
        number=1,
        message=FulfillmentResponse,
    )
    page_info = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PageInfo",
    )
    session_info = proto.Field(
        proto.MESSAGE,
        number=3,
        message="SessionInfo",
    )
    payload = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )
    target_page = proto.Field(
        proto.STRING,
        number=5,
        oneof="transition",
    )
    target_flow = proto.Field(
        proto.STRING,
        number=6,
        oneof="transition",
    )


class PageInfo(proto.Message):
    r"""Represents page information communicated to and from the
    webhook.

    Attributes:
        current_page (str):
            Always present for
            [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
            Ignored for
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            The unique identifier of the current page. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
        display_name (str):
            Always present for
            [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
            Ignored for
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            The display name of the current page.
        form_info (google.cloud.dialogflowcx_v3beta1.types.PageInfo.FormInfo):
            Optional for both
            [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest]
            and
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            Information about the form.
    """

    class FormInfo(proto.Message):
        r"""Represents form information.

        Attributes:
            parameter_info (Sequence[google.cloud.dialogflowcx_v3beta1.types.PageInfo.FormInfo.ParameterInfo]):
                Optional for both
                [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest]
                and
                [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                The parameters contained in the form. Note that the webhook
                cannot add or remove any form parameter.
        """

        class ParameterInfo(proto.Message):
            r"""Represents parameter information.

            Attributes:
                display_name (str):
                    Always present for
                    [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
                    Required for
                    [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                    The human-readable name of the parameter, unique within the
                    form. This field cannot be modified by the webhook.
                required (bool):
                    Optional for both
                    [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest]
                    and
                    [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                    Indicates whether the parameter is required. Optional
                    parameters will not trigger prompts; however, they are
                    filled if the user specifies them. Required parameters must
                    be filled before form filling concludes.
                state (google.cloud.dialogflowcx_v3beta1.types.PageInfo.FormInfo.ParameterInfo.ParameterState):
                    Always present for
                    [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
                    Required for
                    [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                    The state of the parameter. This field can be set to
                    [INVALID][google.cloud.dialogflow.cx.v3beta1.PageInfo.FormInfo.ParameterInfo.ParameterState.INVALID]
                    by the webhook to invalidate the parameter; other values set
                    by the webhook will be ignored.
                value (google.protobuf.struct_pb2.Value):
                    Optional for both
                    [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest]
                    and
                    [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                    The value of the parameter. This field can be set by the
                    webhook to change the parameter value.
                just_collected (bool):
                    Optional for
                    [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
                    Ignored for
                    [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
                    Indicates if the parameter value was just collected on the
                    last conversation turn.
            """

            class ParameterState(proto.Enum):
                r"""Represents the state of a parameter."""
                PARAMETER_STATE_UNSPECIFIED = 0
                EMPTY = 1
                INVALID = 2
                FILLED = 3

            display_name = proto.Field(
                proto.STRING,
                number=1,
            )
            required = proto.Field(
                proto.BOOL,
                number=2,
            )
            state = proto.Field(
                proto.ENUM,
                number=3,
                enum="PageInfo.FormInfo.ParameterInfo.ParameterState",
            )
            value = proto.Field(
                proto.MESSAGE,
                number=4,
                message=struct_pb2.Value,
            )
            just_collected = proto.Field(
                proto.BOOL,
                number=5,
            )

        parameter_info = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="PageInfo.FormInfo.ParameterInfo",
        )

    current_page = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=4,
    )
    form_info = proto.Field(
        proto.MESSAGE,
        number=3,
        message=FormInfo,
    )


class SessionInfo(proto.Message):
    r"""Represents session information communicated to and from the
    webhook.

    Attributes:
        session (str):
            Always present for
            [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
            Ignored for
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            The unique identifier of the
            [session][google.cloud.dialogflow.cx.v3beta1.DetectIntentRequest.session].
            This field can be used by the webhook to identify a session.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
            or
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``
            if environment is specified.
        parameters (Mapping[str, google.protobuf.struct_pb2.Value]):
            Optional for
            [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest].
            Optional for
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            All parameters collected from forms and intents during the
            session. Parameters can be created, updated, or removed by
            the webhook. To remove a parameter from the session, the
            webhook should explicitly set the parameter value to null in
            [WebhookResponse][google.cloud.dialogflow.cx.v3beta1.WebhookResponse].
            The map is keyed by parameters' display names.
    """

    session = proto.Field(
        proto.STRING,
        number=1,
    )
    parameters = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
