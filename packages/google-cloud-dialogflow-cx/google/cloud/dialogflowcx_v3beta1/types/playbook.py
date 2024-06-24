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
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import (
    example,
    generative_settings,
    parameter_definition,
)

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "CreatePlaybookRequest",
        "DeletePlaybookRequest",
        "ListPlaybooksRequest",
        "ListPlaybooksResponse",
        "GetPlaybookRequest",
        "UpdatePlaybookRequest",
        "Playbook",
        "CreatePlaybookVersionRequest",
        "PlaybookVersion",
        "GetPlaybookVersionRequest",
        "ListPlaybookVersionsRequest",
        "ListPlaybookVersionsResponse",
        "DeletePlaybookVersionRequest",
    },
)


class CreatePlaybookRequest(proto.Message):
    r"""The request message for
    [Playbooks.CreatePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.CreatePlaybook].

    Attributes:
        parent (str):
            Required. The agent to create a playbook for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        playbook (google.cloud.dialogflowcx_v3beta1.types.Playbook):
            Required. The playbook to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    playbook: "Playbook" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Playbook",
    )


class DeletePlaybookRequest(proto.Message):
    r"""The request message for
    [Playbooks.DeletePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.DeletePlaybook].

    Attributes:
        name (str):
            Required. The name of the playbook to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPlaybooksRequest(proto.Message):
    r"""The request message for
    [Playbooks.ListPlaybooks][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybooks].

    Attributes:
        parent (str):
            Required. The agent to list playbooks from. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
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


class ListPlaybooksResponse(proto.Message):
    r"""The response message for
    [Playbooks.ListPlaybooks][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybooks].

    Attributes:
        playbooks (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Playbook]):
            The list of playbooks. There will be a maximum number of
            items returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    playbooks: MutableSequence["Playbook"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Playbook",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPlaybookRequest(proto.Message):
    r"""The request message for
    [Playbooks.GetPlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.GetPlaybook].

    Attributes:
        name (str):
            Required. The name of the playbook. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdatePlaybookRequest(proto.Message):
    r"""The request message for
    [Playbooks.UpdatePlaybook][google.cloud.dialogflow.cx.v3beta1.Playbooks.UpdatePlaybook].

    Attributes:
        playbook (google.cloud.dialogflowcx_v3beta1.types.Playbook):
            Required. The playbook to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    playbook: "Playbook" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Playbook",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class Playbook(proto.Message):
    r"""Playbook is the basic building block to instruct the LLM how
    to execute a certain task.

    A playbook consists of a goal to accomplish, an optional list of
    step by step instructions (the step instruction may refers to
    name of the custom or default plugin tools to use) to perform
    the task,
    a list of contextual input data to be passed in at the beginning
    of the invoked, and a list of output parameters to store the
    playbook result.

    Attributes:
        name (str):
            The unique identifier of the playbook. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        display_name (str):
            Required. The human-readable name of the
            playbook, unique within an agent.
        goal (str):
            Required. High level description of the goal
            the playbook intend to accomplish.
        input_parameter_definitions (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.ParameterDefinition]):
            Optional. Defined structured input parameters
            for this playbook.
        output_parameter_definitions (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.ParameterDefinition]):
            Optional. Defined structured output
            parameters for this playbook.
        instruction (google.cloud.dialogflowcx_v3beta1.types.Playbook.Instruction):
            Instruction to accomplish target goal.
        token_count (int):
            Output only. Estimated number of tokes
            current playbook takes when sent to the LLM.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp of initial
            playbook creation.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last time the playbook version
            was updated.
        referenced_playbooks (MutableSequence[str]):
            Output only. The resource name of other
            playbooks referenced by the current playbook in
            the instructions.
        referenced_flows (MutableSequence[str]):
            Output only. The resource name of flows
            referenced by the current playbook in the
            instructions.
        referenced_tools (MutableSequence[str]):
            Optional. The resource name of tools
            referenced by the current playbook in the
            instructions. If not provided explicitly, they
            are will be implied using the tool being
            referenced in goal and steps.
        llm_model_settings (google.cloud.dialogflowcx_v3beta1.types.LlmModelSettings):
            Optional. Llm model settings for the
            playbook.
    """

    class Step(proto.Message):
        r"""Message of single step execution.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            text (str):
                Step instruction in text format.

                This field is a member of `oneof`_ ``instruction``.
            steps (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Playbook.Step]):
                Sub-processing needed to execute the current
                step.
        """

        text: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="instruction",
        )
        steps: MutableSequence["Playbook.Step"] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Playbook.Step",
        )

    class Instruction(proto.Message):
        r"""Message of the Instruction of the playbook.

        Attributes:
            steps (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Playbook.Step]):
                Ordered list of step by step execution
                instructions to accomplish target goal.
        """

        steps: MutableSequence["Playbook.Step"] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Playbook.Step",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    goal: str = proto.Field(
        proto.STRING,
        number=3,
    )
    input_parameter_definitions: MutableSequence[
        parameter_definition.ParameterDefinition
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=parameter_definition.ParameterDefinition,
    )
    output_parameter_definitions: MutableSequence[
        parameter_definition.ParameterDefinition
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=parameter_definition.ParameterDefinition,
    )
    instruction: Instruction = proto.Field(
        proto.MESSAGE,
        number=17,
        message=Instruction,
    )
    token_count: int = proto.Field(
        proto.INT64,
        number=8,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    referenced_playbooks: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=11,
    )
    referenced_flows: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=12,
    )
    referenced_tools: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    llm_model_settings: generative_settings.LlmModelSettings = proto.Field(
        proto.MESSAGE,
        number=14,
        message=generative_settings.LlmModelSettings,
    )


class CreatePlaybookVersionRequest(proto.Message):
    r"""The request message for
    [Playbooks.CreatePlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.CreatePlaybookVersion].

    Attributes:
        parent (str):
            Required. The playbook to create a version for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        playbook_version (google.cloud.dialogflowcx_v3beta1.types.PlaybookVersion):
            Required. The playbook version to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    playbook_version: "PlaybookVersion" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PlaybookVersion",
    )


class PlaybookVersion(proto.Message):
    r"""Playbook version is a snapshot of the playbook at certain
    timestamp.

    Attributes:
        name (str):
            The unique identifier of the playbook version. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/versions/<Version ID>``.
        description (str):
            Optional. The description of the playbook
            version.
        playbook (google.cloud.dialogflowcx_v3beta1.types.Playbook):
            Output only. Snapshot of the playbook when
            the playbook version is created.
        examples (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Example]):
            Output only. Snapshot of the examples
            belonging to the playbook when the playbook
            version is created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last time the playbook version
            was created or modified.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    playbook: "Playbook" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Playbook",
    )
    examples: MutableSequence[example.Example] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=example.Example,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class GetPlaybookVersionRequest(proto.Message):
    r"""The request message for
    [Playbooks.GetPlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.GetPlaybookVersion].

    Attributes:
        name (str):
            Required. The name of the playbook version. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/versions/<Version ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPlaybookVersionsRequest(proto.Message):
    r"""The request message for
    [Playbooks.ListPlaybookVersions][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybookVersions].

    Attributes:
        parent (str):
            Required. The playbook to list versions for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
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


class ListPlaybookVersionsResponse(proto.Message):
    r"""The response message for
    [Playbooks.ListPlaybookVersions][google.cloud.dialogflow.cx.v3beta1.Playbooks.ListPlaybookVersions].

    Attributes:
        playbook_versions (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.PlaybookVersion]):
            The list of playbook version. There will be a maximum number
            of items returned based on the page_size field in the
            request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    playbook_versions: MutableSequence["PlaybookVersion"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PlaybookVersion",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeletePlaybookVersionRequest(proto.Message):
    r"""The request message for
    [Playbooks.DeletePlaybookVersion][google.cloud.dialogflow.cx.v3beta1.Playbooks.DeletePlaybookVersion].

    Attributes:
        name (str):
            Required. The name of the playbook version to delete.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/playbooks/<Playbook ID>/versions/<Version ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
