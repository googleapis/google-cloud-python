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


from google.cloud.dialogflowcx_v3beta1.types import fulfillment
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "Page",
        "Form",
        "EventHandler",
        "TransitionRoute",
        "ListPagesRequest",
        "ListPagesResponse",
        "GetPageRequest",
        "CreatePageRequest",
        "UpdatePageRequest",
        "DeletePageRequest",
    },
)


class Page(proto.Message):
    r"""A Dialogflow CX conversation (session) can be described and
    visualized as a state machine. The states of a CX session are
    represented by pages.

    For each flow, you define many pages, where your combined pages can
    handle a complete conversation on the topics the flow is designed
    for. At any given moment, exactly one page is the current page, the
    current page is considered active, and the flow associated with that
    page is considered active. Every flow has a special start page. When
    a flow initially becomes active, the start page page becomes the
    current page. For each conversational turn, the current page will
    either stay the same or transition to another page.

    You configure each page to collect information from the end-user
    that is relevant for the conversational state represented by the
    page.

    For more information, see the `Page
    guide <https://cloud.google.com/dialogflow/cx/docs/concept/page>`__.

    Attributes:
        name (str):
            The unique identifier of the page. Required for the
            [Pages.UpdatePage][google.cloud.dialogflow.cx.v3beta1.Pages.UpdatePage]
            method.
            [Pages.CreatePage][google.cloud.dialogflow.cx.v3beta1.Pages.CreatePage]
            populates the name automatically. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
        display_name (str):
            Required. The human-readable name of the
            page, unique within the agent.
        entry_fulfillment (~.fulfillment.Fulfillment):
            The fulfillment to call when the session is
            entering the page.
        form (~.gcdc_page.Form):
            The form associated with the page, used for
            collecting parameters relevant to the page.
        transition_route_groups (Sequence[str]):
            Ordered list of
            [``TransitionRouteGroups``][google.cloud.dialogflow.cx.v3beta1.TransitionRouteGroup]
            associated with the page. Transition route groups must be
            unique within a page.

            -  If multiple transition routes within a page scope refer
               to the same intent, then the precedence order is: page's
               transition route -> page's transition route group ->
               flow's transition routes.

            -  If multiple transition route groups within a page contain
               the same intent, then the first group in the ordered list
               takes precedence.

            Format:\ ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/transitionRouteGroups/<TransitionRouteGroup ID>``.
        transition_routes (Sequence[~.gcdc_page.TransitionRoute]):
            A list of transitions for the transition rules of this page.
            They route the conversation to another page in the same
            flow, or another flow.

            When we are in a certain page, the TransitionRoutes are
            evalauted in the following order:

            -  TransitionRoutes defined in the page with intent
               specified.
            -  TransitionRoutes defined in the [transition route
               groups][google.cloud.dialogflow.cx.v3beta1.Page.transition_route_groups].
            -  TransitionRoutes defined in flow with intent specified.
            -  TransitionRoutes defined in the page with only condition
               specified.
        event_handlers (Sequence[~.gcdc_page.EventHandler]):
            Handlers associated with the page to handle
            events such as webhook errors, no match or no
            input.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    entry_fulfillment = proto.Field(
        proto.MESSAGE, number=7, message=fulfillment.Fulfillment,
    )

    form = proto.Field(proto.MESSAGE, number=4, message="Form",)

    transition_route_groups = proto.RepeatedField(proto.STRING, number=11)

    transition_routes = proto.RepeatedField(
        proto.MESSAGE, number=9, message="TransitionRoute",
    )

    event_handlers = proto.RepeatedField(
        proto.MESSAGE, number=10, message="EventHandler",
    )


class Form(proto.Message):
    r"""A form is a data model that groups related parameters that can be
    collected from the user. The process in which the agent prompts the
    user and collects parameter values from the user is called form
    filling. A form can be added to a
    [page][google.cloud.dialogflow.cx.v3beta1.Page]. When form filling
    is done, the filled parameters will be written to the
    [session][google.cloud.dialogflow.cx.v3beta1.SessionInfo.parameters].

    Attributes:
        parameters (Sequence[~.gcdc_page.Form.Parameter]):
            Parameters to collect from the user.
    """

    class Parameter(proto.Message):
        r"""Represents a form parameter.

        Attributes:
            display_name (str):
                Required. The human-readable name of the
                parameter, unique within the form.
            required (bool):
                Indicates whether the parameter is required.
                Optional parameters will not trigger prompts;
                however, they are filled if the user specifies
                them. Required parameters must be filled before
                form filling concludes.
            entity_type (str):
                Required. The entity type of the parameter. Format:
                ``projects/-/locations/-/agents/-/entityTypes/<System Entity Type ID>``
                for system entity types (for example,
                ``projects/-/locations/-/agents/-/entityTypes/sys.date``),
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``
                for developer entity types.
            is_list (bool):
                Indicates whether the parameter represents a
                list of values.
            fill_behavior (~.gcdc_page.Form.Parameter.FillBehavior):
                Required. Defines fill behavior for the
                parameter.
            default_value (~.struct.Value):
                The default value of an optional parameter.
                If the parameter is required, the default value
                will be ignored.
        """

        class FillBehavior(proto.Message):
            r"""Configuration for how the filling of a parameter should be
            handled.

            Attributes:
                initial_prompt_fulfillment (~.fulfillment.Fulfillment):
                    Required. The fulfillment to provide the
                    initial prompt that the agent can present to the
                    user in order to fill the parameter.
                reprompt_event_handlers (Sequence[~.gcdc_page.EventHandler]):
                    The handlers for parameter-level events, used to provide
                    reprompt for the parameter or transition to a different
                    page/flow. The supported events are:

                    -  ``sys.no-match-<N>``, where N can be from 1 to 6
                    -  ``sys.no-match-default``
                    -  ``sys.no-input-<N>``, where N can be from 1 to 6
                    -  ``sys.no-input-default``
                    -  ``sys.invalid-parameter``

                    ``initial_prompt_fulfillment`` provides the first prompt for
                    the parameter.

                    If the user's response does not fill the parameter, a
                    no-match/no-input event will be triggered, and the
                    fulfillment associated with the
                    ``sys.no-match-1``/``sys.no-input-1`` handler (if defined)
                    will be called to provide a prompt. The
                    ``sys.no-match-2``/``sys.no-input-2`` handler (if defined)
                    will respond to the next no-match/no-input event, and so on.

                    A ``sys.no-match-default`` or ``sys.no-input-default``
                    handler will be used to handle all following
                    no-match/no-input events after all numbered
                    no-match/no-input handlers for the parameter are consumed.

                    A ``sys.invalid-parameter`` handler can be defined to handle
                    the case where the parameter values have been
                    ``invalidated`` by webhook. For example, if the user's
                    response fill the parameter, however the parameter was
                    invalidated by webhook, the fulfillment associated with the
                    ``sys.invalid-parameter`` handler (if defined) will be
                    called to provide a prompt.

                    If the event handler for the corresponding event can't be
                    found on the parameter, ``initial_prompt_fulfillment`` will
                    be re-prompted.
            """

            initial_prompt_fulfillment = proto.Field(
                proto.MESSAGE, number=3, message=fulfillment.Fulfillment,
            )

            reprompt_event_handlers = proto.RepeatedField(
                proto.MESSAGE, number=5, message="EventHandler",
            )

        display_name = proto.Field(proto.STRING, number=1)

        required = proto.Field(proto.BOOL, number=2)

        entity_type = proto.Field(proto.STRING, number=3)

        is_list = proto.Field(proto.BOOL, number=4)

        fill_behavior = proto.Field(
            proto.MESSAGE, number=7, message="Form.Parameter.FillBehavior",
        )

        default_value = proto.Field(proto.MESSAGE, number=9, message=struct.Value,)

    parameters = proto.RepeatedField(proto.MESSAGE, number=1, message=Parameter,)


class EventHandler(proto.Message):
    r"""An event handler specifies an
    [event][google.cloud.dialogflow.cx.v3beta1.EventHandler.event] that
    can be handled during a session. When the specified event happens,
    the following actions are taken in order:

    -  If there is a
       [``trigger_fulfillment``][google.cloud.dialogflow.cx.v3beta1.EventHandler.trigger_fulfillment]
       associated with the event, it will be called.
    -  If there is a
       [``target_page``][google.cloud.dialogflow.cx.v3beta1.EventHandler.target_page]
       associated with the event, the session will transition into the
       specified page.
    -  If there is a
       [``target_flow``][google.cloud.dialogflow.cx.v3beta1.EventHandler.target_flow]
       associated with the event, the session will transition into the
       specified flow.

    Attributes:
        name (str):
            Output only. The unique identifier of this
            event handler.
        event (str):
            Required. The name of the event to handle.
        trigger_fulfillment (~.fulfillment.Fulfillment):
            The fulfillment to call when the event
            occurs. Handling webhook errors with a
            fulfillment enabled with webhook could cause
            infinite loop. It is invalid to specify such
            fulfillment for a handler handling webhooks.
        target_page (str):
            The target page to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
        target_flow (str):
            The target flow to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
    """

    name = proto.Field(proto.STRING, number=6)

    event = proto.Field(proto.STRING, number=4)

    trigger_fulfillment = proto.Field(
        proto.MESSAGE, number=5, message=fulfillment.Fulfillment,
    )

    target_page = proto.Field(proto.STRING, number=2, oneof="target")

    target_flow = proto.Field(proto.STRING, number=3, oneof="target")


class TransitionRoute(proto.Message):
    r"""A transition route specifies a
    [intent][google.cloud.dialogflow.cx.v3beta1.Intent] that can be
    matched and/or a data condition that can be evaluated during a
    session. When a specified transition is matched, the following
    actions are taken in order:

    -  If there is a
       [``trigger_fulfillment``][google.cloud.dialogflow.cx.v3beta1.TransitionRoute.trigger_fulfillment]
       associated with the transition, it will be called.
    -  If there is a
       [``target_page``][google.cloud.dialogflow.cx.v3beta1.TransitionRoute.target_page]
       associated with the transition, the session will transition into
       the specified page.
    -  If there is a
       [``target_flow``][google.cloud.dialogflow.cx.v3beta1.TransitionRoute.target_flow]
       associated with the transition, the session will transition into
       the specified flow.

    Attributes:
        name (str):
            Output only. The unique identifier of this
            transition route.
        intent (str):
            The unique identifier of an
            [Intent][google.cloud.dialogflow.cx.v3beta1.Intent]. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
            Indicates that the transition can only happen when the given
            intent is matched. At least one of ``intent`` or
            ``condition`` must be specified. When both ``intent`` and
            ``condition`` are specified, the transition can only happen
            when both are fulfilled.
        condition (str):
            The condition to evaluate against [form
            parameters][google.cloud.dialogflow.cx.v3beta1.Form.parameters]
            or [session
            parameters][google.cloud.dialogflow.cx.v3beta1.SessionInfo.parameters].

            See the `conditions
            reference <https://cloud.google.com/dialogflow/cx/docs/reference/condition>`__.
            At least one of ``intent`` or ``condition`` must be
            specified. When both ``intent`` and ``condition`` are
            specified, the transition can only happen when both are
            fulfilled.
        trigger_fulfillment (~.fulfillment.Fulfillment):
            The fulfillment to call when the condition is satisfied. At
            least one of ``trigger_fulfillment`` and ``target`` must be
            specified. When both are defined, ``trigger_fulfillment`` is
            executed first.
        target_page (str):
            The target page to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
        target_flow (str):
            The target flow to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
    """

    name = proto.Field(proto.STRING, number=6)

    intent = proto.Field(proto.STRING, number=1)

    condition = proto.Field(proto.STRING, number=2)

    trigger_fulfillment = proto.Field(
        proto.MESSAGE, number=3, message=fulfillment.Fulfillment,
    )

    target_page = proto.Field(proto.STRING, number=4, oneof="target")

    target_flow = proto.Field(proto.STRING, number=5, oneof="target")


class ListPagesRequest(proto.Message):
    r"""The request message for
    [Pages.ListPages][google.cloud.dialogflow.cx.v3beta1.Pages.ListPages].

    Attributes:
        parent (str):
            Required. The flow to list all pages for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        language_code (str):
            The language to list pages for. The following fields are
            language dependent:

            -  ``Page.entry_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.initial_prompt_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.reprompt_event_handlers.messages``
            -  ``Page.transition_routes.trigger_fulfillment.messages``
            -

            ``Page.transition_route_groups.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListPagesResponse(proto.Message):
    r"""The response message for
    [Pages.ListPages][google.cloud.dialogflow.cx.v3beta1.Pages.ListPages].

    Attributes:
        pages (Sequence[~.gcdc_page.Page]):
            The list of pages. There will be a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    pages = proto.RepeatedField(proto.MESSAGE, number=1, message=Page,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetPageRequest(proto.Message):
    r"""The request message for
    [Pages.GetPage][google.cloud.dialogflow.cx.v3beta1.Pages.GetPage].

    Attributes:
        name (str):
            Required. The name of the page. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
        language_code (str):
            The language to retrieve the page for. The following fields
            are language dependent:

            -  ``Page.entry_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.initial_prompt_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.reprompt_event_handlers.messages``
            -  ``Page.transition_routes.trigger_fulfillment.messages``
            -

            ``Page.transition_route_groups.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    name = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)


class CreatePageRequest(proto.Message):
    r"""The request message for
    [Pages.CreatePage][google.cloud.dialogflow.cx.v3beta1.Pages.CreatePage].

    Attributes:
        parent (str):
            Required. The flow to create a page for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        page (~.gcdc_page.Page):
            Required. The page to create.
        language_code (str):
            The language of the following fields in ``page``:

            -  ``Page.entry_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.initial_prompt_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.reprompt_event_handlers.messages``
            -  ``Page.transition_routes.trigger_fulfillment.messages``
            -

            ``Page.transition_route_groups.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1)

    page = proto.Field(proto.MESSAGE, number=2, message=Page,)

    language_code = proto.Field(proto.STRING, number=3)


class UpdatePageRequest(proto.Message):
    r"""The request message for
    [Pages.UpdatePage][google.cloud.dialogflow.cx.v3beta1.Pages.UpdatePage].

    Attributes:
        page (~.gcdc_page.Page):
            Required. The page to update.
        language_code (str):
            The language of the following fields in ``page``:

            -  ``Page.entry_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.initial_prompt_fulfillment.messages``
            -  ``Page.form.parameters.fill_behavior.reprompt_event_handlers.messages``
            -  ``Page.transition_routes.trigger_fulfillment.messages``
            -

            ``Page.transition_route_groups.transition_routes.trigger_fulfillment.messages``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        update_mask (~.field_mask.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    page = proto.Field(proto.MESSAGE, number=1, message=Page,)

    language_code = proto.Field(proto.STRING, number=2)

    update_mask = proto.Field(proto.MESSAGE, number=3, message=field_mask.FieldMask,)


class DeletePageRequest(proto.Message):
    r"""The request message for
    [Pages.DeletePage][google.cloud.dialogflow.cx.v3beta1.Pages.DeletePage].

    Attributes:
        name (str):
            Required. The name of the page to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/Flows/<flow ID>/pages/<Page ID>``.
        force (bool):
            This field has no effect for pages with no incoming
            transitions. For pages with incoming transitions:

            -  If ``force`` is set to false, an error will be returned
               with message indicating the incoming transitions.
            -  If ``force`` is set to true, Dialogflow will remove the
               page, as well as any transitions to the page (i.e.
               [Target page][EventHandler.target_page] in event handlers
               or [Target page][TransitionRoute.target_page] in
               transition routes that point to this page will be
               cleared).
    """

    name = proto.Field(proto.STRING, number=1)

    force = proto.Field(proto.BOOL, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
