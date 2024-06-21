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
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "OutputState",
        "CreateExampleRequest",
        "DeleteExampleRequest",
        "ListExamplesRequest",
        "ListExamplesResponse",
        "GetExampleRequest",
        "UpdateExampleRequest",
        "Example",
        "PlaybookInput",
        "PlaybookOutput",
        "Action",
        "UserUtterance",
        "AgentUtterance",
        "ToolUse",
        "PlaybookInvocation",
        "FlowInvocation",
    },
)


class OutputState(proto.Enum):
    r"""Output state.

    Values:
        OUTPUT_STATE_UNSPECIFIED (0):
            Unspecified output.
        OUTPUT_STATE_OK (1):
            Succeeded.
        OUTPUT_STATE_CANCELLED (2):
            Cancelled.
        OUTPUT_STATE_FAILED (3):
            Failed.
        OUTPUT_STATE_ESCALATED (4):
            Escalated.
        OUTPUT_STATE_PENDING (5):
            Pending.
    """
    OUTPUT_STATE_UNSPECIFIED = 0
    OUTPUT_STATE_OK = 1
    OUTPUT_STATE_CANCELLED = 2
    OUTPUT_STATE_FAILED = 3
    OUTPUT_STATE_ESCALATED = 4
    OUTPUT_STATE_PENDING = 5


class CreateExampleRequest(proto.Message):
    r"""The request message for
    [Examples.CreateExample][google.cloud.dialogflow.cx.v3beta1.Examples.CreateExample].

    Attributes:
        parent (str):
            Required. The playbook to create an example for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        example (google.cloud.dialogflowcx_v3beta1.types.Example):
            Required. The example to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    example: "Example" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Example",
    )


class DeleteExampleRequest(proto.Message):
    r"""The request message for
    [Examples.DeleteExample][google.cloud.dialogflow.cx.v3beta1.Examples.DeleteExample].

    Attributes:
        name (str):
            Required. The name of the example to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/examples/<Example ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListExamplesRequest(proto.Message):
    r"""The request message for
    [Examples.ListExamples][google.cloud.dialogflow.cx.v3beta1.Examples.ListExamples].

    Attributes:
        parent (str):
            Required. The playbook to list the examples from. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The
            [next_page_token][ListExampleResponse.next_page_token] value
            returned from a previous list request.
        language_code (str):
            Optional. The language to list examples for.
            If not specified, the agent's default language
            is used. Note: languages must be enabled in the
            agent before they can be used.
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
    language_code: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListExamplesResponse(proto.Message):
    r"""The response message for
    [Examples.ListExamples][google.cloud.dialogflow.cx.v3beta1.Examples.ListExamples].

    Attributes:
        examples (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Example]):
            The list of examples. There will be a maximum number of
            items returned based on the
            [page_size][google.cloud.dialogflow.cx.v3beta1.ListExamplesRequest.page_size]
            field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    examples: MutableSequence["Example"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Example",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetExampleRequest(proto.Message):
    r"""The request message for
    [Examples.GetExample][google.cloud.dialogflow.cx.v3beta1.Examples.GetExample].

    Attributes:
        name (str):
            Required. The name of the example. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/examples/<Example ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateExampleRequest(proto.Message):
    r"""The request message for
    [Examples.UpdateExample][google.cloud.dialogflow.cx.v3beta1.Examples.UpdateExample].

    Attributes:
        example (google.cloud.dialogflowcx_v3beta1.types.Example):
            Required. The example to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The mask to control which fields
            get updated. If the mask is not present, all
            fields will be updated.
    """

    example: "Example" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Example",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class Example(proto.Message):
    r"""Example represents a sample execution of the playbook in the
    conversation.
    An example consists of a list of ordered actions performed by
    end user or Dialogflow agent according the playbook instructions
    to fulfill the task.

    Attributes:
        name (str):
            The unique identifier of the playbook example. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/examples/<Example ID>``.
        playbook_input (google.cloud.dialogflowcx_v3beta1.types.PlaybookInput):
            Optional. The input to the playbook in the
            example.
        playbook_output (google.cloud.dialogflowcx_v3beta1.types.PlaybookOutput):
            Optional. The output of the playbook in the
            example.
        actions (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Action]):
            Required. The ordered list of actions
            performed by the end user and the Dialogflow
            agent.
        display_name (str):
            Required. The display name of the example.
        description (str):
            Optional. The high level concise description
            of the example. The max number of characters is
            200.
        token_count (int):
            Output only. Estimated number of tokes
            current example takes when sent to the LLM.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp of initial example
            creation.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last time the example was
            updated.
        conversation_state (google.cloud.dialogflowcx_v3beta1.types.OutputState):
            Required. Example's output state.
        language_code (str):
            Optional. The language code of the example.
            If not specified, the agent's default language
            is used. Note: languages must be enabled in the
            agent before they can be used.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    playbook_input: "PlaybookInput" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PlaybookInput",
    )
    playbook_output: "PlaybookOutput" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="PlaybookOutput",
    )
    actions: MutableSequence["Action"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Action",
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    description: str = proto.Field(
        proto.STRING,
        number=8,
    )
    token_count: int = proto.Field(
        proto.INT64,
        number=9,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    conversation_state: "OutputState" = proto.Field(
        proto.ENUM,
        number=12,
        enum="OutputState",
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=13,
    )


class PlaybookInput(proto.Message):
    r"""Input of the playbook.

    Attributes:
        preceding_conversation_summary (str):
            Optional. Summary string of the preceding
            conversation for the child playbook invocation.
        action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A list of input parameters for the
            action.
    """

    preceding_conversation_summary: str = proto.Field(
        proto.STRING,
        number=1,
    )
    action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )


class PlaybookOutput(proto.Message):
    r"""Output of the playbook.

    Attributes:
        execution_summary (str):
            Optional. Summary string of the execution
            result of the child playbook.
        action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A Struct object of output
            parameters for the action.
    """

    execution_summary: str = proto.Field(
        proto.STRING,
        number=1,
    )
    action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )


class Action(proto.Message):
    r"""Action performed by end user or Dialogflow agent in the
    conversation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        user_utterance (google.cloud.dialogflowcx_v3beta1.types.UserUtterance):
            Optional. Agent obtained a message from the
            customer.

            This field is a member of `oneof`_ ``action``.
        agent_utterance (google.cloud.dialogflowcx_v3beta1.types.AgentUtterance):
            Optional. Action performed by the agent as a
            message.

            This field is a member of `oneof`_ ``action``.
        tool_use (google.cloud.dialogflowcx_v3beta1.types.ToolUse):
            Optional. Action performed on behalf of the
            agent by calling a plugin tool.

            This field is a member of `oneof`_ ``action``.
        playbook_invocation (google.cloud.dialogflowcx_v3beta1.types.PlaybookInvocation):
            Optional. Action performed on behalf of the
            agent by invoking a child playbook.

            This field is a member of `oneof`_ ``action``.
        flow_invocation (google.cloud.dialogflowcx_v3beta1.types.FlowInvocation):
            Optional. Action performed on behalf of the
            agent by invoking a CX flow.

            This field is a member of `oneof`_ ``action``.
    """

    user_utterance: "UserUtterance" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="action",
        message="UserUtterance",
    )
    agent_utterance: "AgentUtterance" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="action",
        message="AgentUtterance",
    )
    tool_use: "ToolUse" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="action",
        message="ToolUse",
    )
    playbook_invocation: "PlaybookInvocation" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="action",
        message="PlaybookInvocation",
    )
    flow_invocation: "FlowInvocation" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="action",
        message="FlowInvocation",
    )


class UserUtterance(proto.Message):
    r"""UserUtterance represents one message sent by the customer.

    Attributes:
        text (str):
            Required. Message content in text.
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AgentUtterance(proto.Message):
    r"""AgentUtterance represents one message sent by the agent.

    Attributes:
        text (str):
            Required. Message content in text.
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ToolUse(proto.Message):
    r"""Stores metadata of the invocation of an action supported by a
    tool.

    Attributes:
        tool (str):
            Required. The
            [tool][google.cloud.dialogflow.cx.v3beta1.Tool] that should
            be used. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/tools/<Tool ID>``.
        action (str):
            Optional. Name of the action to be called
            during the tool use.
        input_action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A list of input parameters for the
            action.
        output_action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A list of output parameters
            generated by the action.
    """

    tool: str = proto.Field(
        proto.STRING,
        number=1,
    )
    action: str = proto.Field(
        proto.STRING,
        number=2,
    )
    input_action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )
    output_action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )


class PlaybookInvocation(proto.Message):
    r"""Stores metadata of the invocation of a child playbook.
    Next Id: 5

    Attributes:
        playbook (str):
            Required. The unique identifier of the playbook. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        playbook_input (google.cloud.dialogflowcx_v3beta1.types.PlaybookInput):
            Optional. Input of the child playbook
            invocation.
        playbook_output (google.cloud.dialogflowcx_v3beta1.types.PlaybookOutput):
            Optional. Output of the child playbook
            invocation.
        playbook_state (google.cloud.dialogflowcx_v3beta1.types.OutputState):
            Required. Playbook invocation's output state.
    """

    playbook: str = proto.Field(
        proto.STRING,
        number=1,
    )
    playbook_input: "PlaybookInput" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PlaybookInput",
    )
    playbook_output: "PlaybookOutput" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PlaybookOutput",
    )
    playbook_state: "OutputState" = proto.Field(
        proto.ENUM,
        number=4,
        enum="OutputState",
    )


class FlowInvocation(proto.Message):
    r"""Stores metadata of the invocation of a CX flow.
    Next Id: 7

    Attributes:
        flow (str):
            Required. The unique identifier of the flow. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent flows/<Flow ID>``.
        input_action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A list of input parameters for the
            flow.
        output_action_parameters (google.protobuf.struct_pb2.Struct):
            Optional. A list of output parameters
            generated by the flow invocation.
        flow_state (google.cloud.dialogflowcx_v3beta1.types.OutputState):
            Required. Flow invocation's output state.
    """

    flow: str = proto.Field(
        proto.STRING,
        number=1,
    )
    input_action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )
    output_action_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    flow_state: "OutputState" = proto.Field(
        proto.ENUM,
        number=4,
        enum="OutputState",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
