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

import google.protobuf.struct_pb2 as struct_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "OutputState",
        "PlaybookInput",
        "PlaybookOutput",
        "Action",
        "UserUtterance",
        "AgentUtterance",
        "ToolUse",
        "PlaybookInvocation",
        "FlowInvocation",
        "PlaybookTransition",
        "FlowTransition",
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


class PlaybookInput(proto.Message):
    r"""Input of the playbook.

    Attributes:
        preceding_conversation_summary (str):
            Optional. Summary string of the preceding
            conversation for the child playbook invocation.
    """

    preceding_conversation_summary: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PlaybookOutput(proto.Message):
    r"""Output of the playbook.

    Attributes:
        execution_summary (str):
            Optional. Summary string of the execution
            result of the child playbook.
    """

    execution_summary: str = proto.Field(
        proto.STRING,
        number=1,
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
        user_utterance (google.cloud.dialogflowcx_v3.types.UserUtterance):
            Optional. Agent obtained a message from the
            customer.

            This field is a member of `oneof`_ ``action``.
        agent_utterance (google.cloud.dialogflowcx_v3.types.AgentUtterance):
            Optional. Action performed by the agent as a
            message.

            This field is a member of `oneof`_ ``action``.
        tool_use (google.cloud.dialogflowcx_v3.types.ToolUse):
            Optional. Action performed on behalf of the
            agent by calling a plugin tool.

            This field is a member of `oneof`_ ``action``.
        playbook_invocation (google.cloud.dialogflowcx_v3.types.PlaybookInvocation):
            Optional. Action performed on behalf of the
            agent by invoking a child playbook.

            This field is a member of `oneof`_ ``action``.
        flow_invocation (google.cloud.dialogflowcx_v3.types.FlowInvocation):
            Optional. Action performed on behalf of the
            agent by invoking a CX flow.

            This field is a member of `oneof`_ ``action``.
        playbook_transition (google.cloud.dialogflowcx_v3.types.PlaybookTransition):
            Optional. Action performed on behalf of the
            agent by transitioning to a target playbook.

            This field is a member of `oneof`_ ``action``.
        flow_transition (google.cloud.dialogflowcx_v3.types.FlowTransition):
            Optional. Action performed on behalf of the
            agent by transitioning to a target CX flow.

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
    playbook_transition: "PlaybookTransition" = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="action",
        message="PlaybookTransition",
    )
    flow_transition: "FlowTransition" = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="action",
        message="FlowTransition",
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
            Required. The [tool][google.cloud.dialogflow.cx.v3.Tool]
            that should be used. Format:
            ``projects/<ProjectID>/locations/<LocationID>/agents/<AgentID>/tools/<ToolID>``.
        display_name (str):
            Output only. The display name of the tool.
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
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
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

    Attributes:
        playbook (str):
            Required. The unique identifier of the playbook. Format:
            ``projects/<ProjectID>/locations/<LocationID>/agents/<AgentID>/playbooks/<PlaybookID>``.
        display_name (str):
            Output only. The display name of the
            playbook.
        playbook_input (google.cloud.dialogflowcx_v3.types.PlaybookInput):
            Optional. Input of the child playbook
            invocation.
        playbook_output (google.cloud.dialogflowcx_v3.types.PlaybookOutput):
            Optional. Output of the child playbook
            invocation.
        playbook_state (google.cloud.dialogflowcx_v3.types.OutputState):
            Required. Playbook invocation's output state.
    """

    playbook: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
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

    Attributes:
        flow (str):
            Required. The unique identifier of the flow. Format:
            ``projects/<ProjectID>/locations/<LocationID>/agents/<AgentID>/flows/<FlowID>``.
        display_name (str):
            Output only. The display name of the flow.
        flow_state (google.cloud.dialogflowcx_v3.types.OutputState):
            Required. Flow invocation's output state.
    """

    flow: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    flow_state: "OutputState" = proto.Field(
        proto.ENUM,
        number=4,
        enum="OutputState",
    )


class PlaybookTransition(proto.Message):
    r"""Stores metadata of the transition to another target playbook.
    Playbook transition actions exit the caller playbook and enter
    the target playbook.

    Attributes:
        playbook (str):
            Required. The unique identifier of the playbook. Format:
            ``projects/<ProjectID>/locations/<LocationID>/agents/<AgentID>/playbooks/<PlaybookID>``.
        display_name (str):
            Output only. The display name of the
            playbook.
    """

    playbook: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


class FlowTransition(proto.Message):
    r"""Stores metadata of the transition to a target CX flow. Flow
    transition actions exit the caller playbook and enter the child
    flow.

    Attributes:
        flow (str):
            Required. The unique identifier of the flow. Format:
            ``projects/<ProjectID>/locations/<LocationID>/agents/<Agentflows/<FlowID>``.
        display_name (str):
            Output only. The display name of the flow.
    """

    flow: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
