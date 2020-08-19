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


from google.cloud.dialogflowcx_v3beta1.types import response_message
from google.protobuf import struct_pb2 as struct  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1", manifest={"Fulfillment",},
)


class Fulfillment(proto.Message):
    r"""A fulfillment can do one or more of the following actions at the
    same time:

    -  Generate rich message responses.
    -  Set parameter values.
    -  Call the webhook.

    Fulfillments can be called at various stages in the
    [Page][google.cloud.dialogflow.cx.v3beta1.Page] or
    [Form][google.cloud.dialogflow.cx.v3beta1.Form] lifecycle. For
    example, when a
    [DetectIntentRequest][google.cloud.dialogflow.cx.v3beta1.DetectIntentRequest]
    drives a session to enter a new page, the page's entry fulfillment
    can add a static response to the
    [QueryResult][google.cloud.dialogflow.cx.v3beta1.QueryResult] in the
    returning
    [DetectIntentResponse][google.cloud.dialogflow.cx.v3beta1.DetectIntentResponse],
    call the webhook (for example, to load user data from a database),
    or both.

    Attributes:
        messages (Sequence[~.response_message.ResponseMessage]):
            The list of rich message responses to present
            to the user.
        webhook (str):
            The webhook to call. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/webhooks/<Webhook ID>``.
        tag (str):
            The tag used by the webhook to identify which fulfillment is
            being called. This field is required if ``webhook`` is
            specified.
        set_parameter_actions (Sequence[~.fulfillment.Fulfillment.SetParameterAction]):
            Set parameter values before executing the
            webhook.
        conditional_cases (Sequence[~.fulfillment.Fulfillment.ConditionalCases]):
            Conditional cases for this fulfillment.
    """

    class SetParameterAction(proto.Message):
        r"""Setting a parameter value.

        Attributes:
            parameter (str):
                Display name of the parameter.
            value (~.struct.Value):
                The new value of the parameter. A null value
                clears the parameter.
        """

        parameter = proto.Field(proto.STRING, number=1)

        value = proto.Field(proto.MESSAGE, number=2, message=struct.Value,)

    class ConditionalCases(proto.Message):
        r"""A list of cascading if-else conditions. Cases are mutually
        exclusive. The first one with a matching condition is selected,
        all the rest ignored.

        Attributes:
            cases (Sequence[~.fulfillment.Fulfillment.ConditionalCases.Case]):
                A list of cascading if-else conditions.
        """

        class Case(proto.Message):
            r"""Each case has a Boolean condition. When it is evaluated to be
            True, the corresponding messages will be selected and evaluated
            recursively.

            Attributes:
                condition (str):
                    The condition to activate and select this case. Empty means
                    the condition is always true. The condition is evaluated
                    against [form parameters][Form.parameters] or [session
                    parameters][SessionInfo.parameters].

                    See the `conditions
                    reference <https://cloud.google.com/dialogflow/cx/docs/reference/condition>`__.
                case_content (Sequence[~.fulfillment.Fulfillment.ConditionalCases.Case.CaseContent]):
                    A list of case content.
            """

            class CaseContent(proto.Message):
                r"""The list of messages or conditional cases to activate for
                this case.

                Attributes:
                    message (~.response_message.ResponseMessage):
                        Returned message.
                    additional_cases (~.fulfillment.Fulfillment.ConditionalCases):
                        Additional cases to be evaluated.
                """

                message = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    oneof="cases_or_message",
                    message=response_message.ResponseMessage,
                )

                additional_cases = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    oneof="cases_or_message",
                    message="Fulfillment.ConditionalCases",
                )

            condition = proto.Field(proto.STRING, number=1)

            case_content = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Fulfillment.ConditionalCases.Case.CaseContent",
            )

        cases = proto.RepeatedField(
            proto.MESSAGE, number=1, message="Fulfillment.ConditionalCases.Case",
        )

    messages = proto.RepeatedField(
        proto.MESSAGE, number=1, message=response_message.ResponseMessage,
    )

    webhook = proto.Field(proto.STRING, number=2)

    tag = proto.Field(proto.STRING, number=3)

    set_parameter_actions = proto.RepeatedField(
        proto.MESSAGE, number=4, message=SetParameterAction,
    )

    conditional_cases = proto.RepeatedField(
        proto.MESSAGE, number=5, message=ConditionalCases,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
