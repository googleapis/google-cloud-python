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

from google.cloud.dialogflowcx_v3.types import page
from google.cloud.dialogflowcx_v3.types import validation_message
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "NluSettings",
        "Flow",
        "CreateFlowRequest",
        "DeleteFlowRequest",
        "ListFlowsRequest",
        "ListFlowsResponse",
        "GetFlowRequest",
        "UpdateFlowRequest",
        "TrainFlowRequest",
        "ValidateFlowRequest",
        "GetFlowValidationResultRequest",
        "FlowValidationResult",
        "ImportFlowRequest",
        "ImportFlowResponse",
        "ExportFlowRequest",
        "ExportFlowResponse",
    },
)


class NluSettings(proto.Message):
    r"""Settings related to NLU.
    Attributes:
        model_type (google.cloud.dialogflowcx_v3.types.NluSettings.ModelType):
            Indicates the type of NLU model.
        classification_threshold (float):
            To filter out false positive results and
            still get variety in matched natural language
            inputs for your agent, you can tune the machine
            learning classification threshold. If the
            returned score value is less than the threshold
            value, then a no-match event will be triggered.
            The score values range from 0.0 (completely
            uncertain) to 1.0 (completely certain). If set
            to 0.0, the default of 0.3 is used.
        model_training_mode (google.cloud.dialogflowcx_v3.types.NluSettings.ModelTrainingMode):
            Indicates NLU model training mode.
    """

    class ModelType(proto.Enum):
        r"""NLU model type."""
        MODEL_TYPE_UNSPECIFIED = 0
        MODEL_TYPE_STANDARD = 1
        MODEL_TYPE_ADVANCED = 3

    class ModelTrainingMode(proto.Enum):
        r"""NLU model training mode."""
        MODEL_TRAINING_MODE_UNSPECIFIED = 0
        MODEL_TRAINING_MODE_AUTOMATIC = 1
        MODEL_TRAINING_MODE_MANUAL = 2

    model_type = proto.Field(proto.ENUM, number=1, enum=ModelType,)
    classification_threshold = proto.Field(proto.FLOAT, number=3,)
    model_training_mode = proto.Field(proto.ENUM, number=4, enum=ModelTrainingMode,)


class Flow(proto.Message):
    r"""Flows represents the conversation flows when you build your
    chatbot agent.
    A flow consists of many pages connected by the transition
    routes. Conversations always start with the built-in Start Flow
    (with an all-0 ID). Transition routes can direct the
    conversation session from the current flow (parent flow) to
    another flow (sub flow). When the sub flow is finished,
    Dialogflow will bring the session back to the parent flow, where
    the sub flow is started.

    Usually, when a transition route is followed by a matched
    intent, the intent will be "consumed". This means the intent
    won't activate more transition routes. However, when the
    followed transition route moves the conversation session into a
    different flow, the matched intent can be carried over and to be
    consumed in the target flow.

    Attributes:
        name (str):
            The unique identifier of the flow. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        display_name (str):
            Required. The human-readable name of the
            flow.
        description (str):
            The description of the flow. The maximum
            length is 500 characters. If exceeded, the
            request is rejected.
        transition_routes (Sequence[google.cloud.dialogflowcx_v3.types.TransitionRoute]):
            A flow's transition routes serve two purposes:

            -  They are responsible for matching the user's first
               utterances in the flow.
            -  They are inherited by every page's [transition
               routes][Page.transition_routes] and can support use cases
               such as the user saying "help" or "can I talk to a
               human?", which can be handled in a common way regardless
               of the current page. Transition routes defined in the
               page have higher priority than those defined in the flow.

            TransitionRoutes are evalauted in the following order:

            -  TransitionRoutes with intent specified..
            -  TransitionRoutes with only condition specified.

            TransitionRoutes with intent specified are inherited by
            pages in the flow.
        event_handlers (Sequence[google.cloud.dialogflowcx_v3.types.EventHandler]):
            A flow's event handlers serve two purposes:

            -  They are responsible for handling events (e.g. no match,
               webhook errors) in the flow.
            -  They are inherited by every page's [event
               handlers][Page.event_handlers], which can be used to
               handle common events regardless of the current page.
               Event handlers defined in the page have higher priority
               than those defined in the flow.

            Unlike
            [transition_routes][google.cloud.dialogflow.cx.v3.Flow.transition_routes],
            these handlers are evaluated on a first-match basis. The
            first one that matches the event get executed, with the rest
            being ignored.
        transition_route_groups (Sequence[str]):
            A flow's transition route group serve two purposes:

            -  They are responsible for matching the user's first
               utterances in the flow.
            -  They are inherited by every page's [transition route
               groups][Page.transition_route_groups]. Transition route
               groups defined in the page have higher priority than
               those defined in the flow.

            Format:\ ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/transitionRouteGroups/<TransitionRouteGroup ID>``.
        nlu_settings (google.cloud.dialogflowcx_v3.types.NluSettings):
            NLU related settings of the flow.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    transition_routes = proto.RepeatedField(
        proto.MESSAGE, number=4, message=page.TransitionRoute,
    )
    event_handlers = proto.RepeatedField(
        proto.MESSAGE, number=10, message=page.EventHandler,
    )
    transition_route_groups = proto.RepeatedField(proto.STRING, number=15,)
    nlu_settings = proto.Field(proto.MESSAGE, number=11, message="NluSettings",)


class CreateFlowRequest(proto.Message):
    r"""The request message for
    [Flows.CreateFlow][google.cloud.dialogflow.cx.v3.Flows.CreateFlow].

    Attributes:
        parent (str):
            Required. The agent to create a flow for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        flow (google.cloud.dialogflowcx_v3.types.Flow):
            Required. The flow to create.
        language_code (str):
            The language of the following fields in ``flow``:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.event_handlers.trigger_fulfillment.conditional_cases``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.conditional_cases``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/cx/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1,)
    flow = proto.Field(proto.MESSAGE, number=2, message="Flow",)
    language_code = proto.Field(proto.STRING, number=3,)


class DeleteFlowRequest(proto.Message):
    r"""The request message for
    [Flows.DeleteFlow][google.cloud.dialogflow.cx.v3.Flows.DeleteFlow].

    Attributes:
        name (str):
            Required. The name of the flow to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        force (bool):
            This field has no effect for flows with no incoming
            transitions. For flows with incoming transitions:

            -  If ``force`` is set to false, an error will be returned
               with message indicating the incoming transitions.
            -  If ``force`` is set to true, Dialogflow will remove the
               flow, as well as any transitions to the flow (i.e.
               [Target flow][EventHandler.target_flow] in event handlers
               or [Target flow][TransitionRoute.target_flow] in
               transition routes that point to this flow will be
               cleared).
    """

    name = proto.Field(proto.STRING, number=1,)
    force = proto.Field(proto.BOOL, number=2,)


class ListFlowsRequest(proto.Message):
    r"""The request message for
    [Flows.ListFlows][google.cloud.dialogflow.cx.v3.Flows.ListFlows].

    Attributes:
        parent (str):
            Required. The agent containing the flows. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
        language_code (str):
            The language to list flows for. The following fields are
            language dependent:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.event_handlers.trigger_fulfillment.conditional_cases``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.conditional_cases``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/cx/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    language_code = proto.Field(proto.STRING, number=4,)


class ListFlowsResponse(proto.Message):
    r"""The response message for
    [Flows.ListFlows][google.cloud.dialogflow.cx.v3.Flows.ListFlows].

    Attributes:
        flows (Sequence[google.cloud.dialogflowcx_v3.types.Flow]):
            The list of flows. There will be a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    flows = proto.RepeatedField(proto.MESSAGE, number=1, message="Flow",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetFlowRequest(proto.Message):
    r"""The response message for
    [Flows.GetFlow][google.cloud.dialogflow.cx.v3.Flows.GetFlow].

    Attributes:
        name (str):
            Required. The name of the flow to get. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        language_code (str):
            The language to retrieve the flow for. The following fields
            are language dependent:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.event_handlers.trigger_fulfillment.conditional_cases``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.conditional_cases``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/cx/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    name = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)


class UpdateFlowRequest(proto.Message):
    r"""The request message for
    [Flows.UpdateFlow][google.cloud.dialogflow.cx.v3.Flows.UpdateFlow].

    Attributes:
        flow (google.cloud.dialogflowcx_v3.types.Flow):
            Required. The flow to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The mask to control which fields get updated. If
            ``update_mask`` is not specified, an error will be returned.
        language_code (str):
            The language of the following fields in ``flow``:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.event_handlers.trigger_fulfillment.conditional_cases``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.conditional_cases``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/cx/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    flow = proto.Field(proto.MESSAGE, number=1, message="Flow",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )
    language_code = proto.Field(proto.STRING, number=3,)


class TrainFlowRequest(proto.Message):
    r"""The request message for
    [Flows.TrainFlow][google.cloud.dialogflow.cx.v3.Flows.TrainFlow].

    Attributes:
        name (str):
            Required. The flow to train. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ValidateFlowRequest(proto.Message):
    r"""The request message for
    [Flows.ValidateFlow][google.cloud.dialogflow.cx.v3.Flows.ValidateFlow].

    Attributes:
        name (str):
            Required. The flow to validate. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        language_code (str):
            If not specified, the agent's default
            language is used.
    """

    name = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)


class GetFlowValidationResultRequest(proto.Message):
    r"""The request message for
    [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3.Flows.GetFlowValidationResult].

    Attributes:
        name (str):
            Required. The flow name. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/validationResult``.
        language_code (str):
            If not specified, the agent's default
            language is used.
    """

    name = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)


class FlowValidationResult(proto.Message):
    r"""The response message for
    [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3.Flows.GetFlowValidationResult].

    Attributes:
        name (str):
            The unique identifier of the flow validation result. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/validationResult``.
        validation_messages (Sequence[google.cloud.dialogflowcx_v3.types.ValidationMessage]):
            Contains all validation messages.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time the flow was validated.
    """

    name = proto.Field(proto.STRING, number=1,)
    validation_messages = proto.RepeatedField(
        proto.MESSAGE, number=2, message=validation_message.ValidationMessage,
    )
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


class ImportFlowRequest(proto.Message):
    r"""The request message for
    [Flows.ImportFlow][google.cloud.dialogflow.cx.v3.Flows.ImportFlow].

    Attributes:
        parent (str):
            Required. The agent to import the flow into. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        flow_uri (str):
            The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI to
            import flow from. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``.
        flow_content (bytes):
            Uncompressed raw byte content for flow.
        import_option (google.cloud.dialogflowcx_v3.types.ImportFlowRequest.ImportOption):
            Flow import mode. If not specified, ``KEEP`` is assumed.
    """

    class ImportOption(proto.Enum):
        r"""Import option."""
        IMPORT_OPTION_UNSPECIFIED = 0
        KEEP = 1
        FALLBACK = 2

    parent = proto.Field(proto.STRING, number=1,)
    flow_uri = proto.Field(proto.STRING, number=2, oneof="flow",)
    flow_content = proto.Field(proto.BYTES, number=3, oneof="flow",)
    import_option = proto.Field(proto.ENUM, number=4, enum=ImportOption,)


class ImportFlowResponse(proto.Message):
    r"""The response message for
    [Flows.ImportFlow][google.cloud.dialogflow.cx.v3.Flows.ImportFlow].

    Attributes:
        flow (str):
            The unique identifier of the new flow. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
    """

    flow = proto.Field(proto.STRING, number=1,)


class ExportFlowRequest(proto.Message):
    r"""The request message for
    [Flows.ExportFlow][google.cloud.dialogflow.cx.v3.Flows.ExportFlow].

    Attributes:
        name (str):
            Required. The name of the flow to export. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        flow_uri (str):
            Optional. The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI to
            export the flow to. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``. If left unspecified,
            the serialized flow is returned inline.
        include_referenced_flows (bool):
            Optional. Whether to export flows referenced
            by the specified flow.
    """

    name = proto.Field(proto.STRING, number=1,)
    flow_uri = proto.Field(proto.STRING, number=2,)
    include_referenced_flows = proto.Field(proto.BOOL, number=4,)


class ExportFlowResponse(proto.Message):
    r"""The response message for
    [Flows.ExportFlow][google.cloud.dialogflow.cx.v3.Flows.ExportFlow].

    Attributes:
        flow_uri (str):
            The URI to a file containing the exported flow. This field
            is populated only if ``flow_uri`` is specified in
            [ExportFlowRequest][google.cloud.dialogflow.cx.v3.ExportFlowRequest].
        flow_content (bytes):
            Uncompressed raw byte content for flow.
    """

    flow_uri = proto.Field(proto.STRING, number=1, oneof="flow",)
    flow_content = proto.Field(proto.BYTES, number=2, oneof="flow",)


__all__ = tuple(sorted(__protobuf__.manifest))
