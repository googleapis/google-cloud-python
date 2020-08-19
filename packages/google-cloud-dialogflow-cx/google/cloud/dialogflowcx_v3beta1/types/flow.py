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


from google.cloud.dialogflowcx_v3beta1.types import page
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
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
    },
)


class NluSettings(proto.Message):
    r"""Settings related to NLU.

    Attributes:
        model_type (~.gcdc_flow.NluSettings.ModelType):
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
        model_training_mode (~.gcdc_flow.NluSettings.ModelTrainingMode):
            Indicates NLU model training mode.
        enable_spell_correction (bool):
            Indicates if automatic spell correction is
            enabled in detect intent requests.
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

    classification_threshold = proto.Field(proto.FLOAT, number=3)

    model_training_mode = proto.Field(proto.ENUM, number=4, enum=ModelTrainingMode,)

    enable_spell_correction = proto.Field(proto.BOOL, number=5)


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
        transition_routes (Sequence[~.page.TransitionRoute]):
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
        event_handlers (Sequence[~.page.EventHandler]):
            A flow's event handlers serve two purposes:

            -  They are responsible for handling events (e.g. no match,
               webhook errors) in the flow.
            -  They are inherited by every page's [event
               handlers][Page.event_handlers], which can be used to
               handle common events regardless of the current page.
               Event handlers defined in the page have higher priority
               than those defined in the flow.

            Unlike
            [transition_routes][google.cloud.dialogflow.cx.v3beta1.Flow.transition_routes],
            these handlers are evaluated on a first-match basis. The
            first one that matches the event get executed, with the rest
            being ignored.
        nlu_settings (~.gcdc_flow.NluSettings):
            NLU related settings of the flow.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    transition_routes = proto.RepeatedField(
        proto.MESSAGE, number=4, message=page.TransitionRoute,
    )

    event_handlers = proto.RepeatedField(
        proto.MESSAGE, number=10, message=page.EventHandler,
    )

    nlu_settings = proto.Field(proto.MESSAGE, number=11, message=NluSettings,)


class CreateFlowRequest(proto.Message):
    r"""The request message for
    [Flows.CreateFlow][google.cloud.dialogflow.cx.v3beta1.Flows.CreateFlow].

    Attributes:
        parent (str):
            Required. The agent to create a flow for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        flow (~.gcdc_flow.Flow):
            Required. The flow to create.
        language_code (str):
            The language of the following fields in ``flow``:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1)

    flow = proto.Field(proto.MESSAGE, number=2, message=Flow,)

    language_code = proto.Field(proto.STRING, number=3)


class DeleteFlowRequest(proto.Message):
    r"""The request message for
    [Flows.DeleteFlow][google.cloud.dialogflow.cx.v3beta1.Flows.DeleteFlow].

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

    name = proto.Field(proto.STRING, number=1)

    force = proto.Field(proto.BOOL, number=2)


class ListFlowsRequest(proto.Message):
    r"""The request message for
    [Flows.ListFlows][google.cloud.dialogflow.cx.v3beta1.Flows.ListFlows].

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
            -  ``Flow.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    language_code = proto.Field(proto.STRING, number=4)


class ListFlowsResponse(proto.Message):
    r"""The response message for
    [Flows.ListFlows][google.cloud.dialogflow.cx.v3beta1.Flows.ListFlows].

    Attributes:
        flows (Sequence[~.gcdc_flow.Flow]):
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

    flows = proto.RepeatedField(proto.MESSAGE, number=1, message=Flow,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetFlowRequest(proto.Message):
    r"""The response message for
    [Flows.GetFlow][google.cloud.dialogflow.cx.v3beta1.Flows.GetFlow].

    Attributes:
        name (str):
            Required. The name of the flow to get. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        language_code (str):
            The language to retrieve the flow for. The following fields
            are language dependent:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    name = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)


class UpdateFlowRequest(proto.Message):
    r"""The request message for
    [Flows.UpdateFlow][google.cloud.dialogflow.cx.v3beta1.Flows.UpdateFlow].

    Attributes:
        flow (~.gcdc_flow.Flow):
            Required. The flow to update.
        update_mask (~.field_mask.FieldMask):
            Required. The mask to control which fields get updated. If
            ``update_mask`` is not specified, an error will be returned.
        language_code (str):
            The language of the following fields in ``flow``:

            -  ``Flow.event_handlers.trigger_fulfillment.messages``
            -  ``Flow.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    flow = proto.Field(proto.MESSAGE, number=1, message=Flow,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)

    language_code = proto.Field(proto.STRING, number=3)


class TrainFlowRequest(proto.Message):
    r"""The request message for
    [Flows.TrainFlow][google.cloud.dialogflow.cx.v3beta1.Flows.TrainFlow].

    Attributes:
        name (str):
            Required. The flow to train. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
