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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "AgentCoachingInstruction",
    },
)


class AgentCoachingInstruction(proto.Message):
    r"""Agent Coaching instructions that customer can configure.

    Attributes:
        display_name (str):
            Optional. Display name for the instruction.
        display_details (str):
            Optional. The detailed description of this
            instruction.
        condition (str):
            Optional. The condition of the instruction.
            For example, "the customer wants to cancel an
            order".  If the users want the instruction to be
            triggered unconditionally, the condition can be
            empty.
        agent_action (str):
            Optional. The action that human agent should take. For
            example, "apologize for the slow shipping". If the users
            only want to use agent coaching for intent detection,
            agent_action can be empty
        system_action (str):
            Optional. The action that system should take. For example,
            "call GetOrderTime with order_number={order number provided
            by the customer}". If the users don't have plugins or don't
            want to trigger plugins, the system_action can be empty
        duplicate_check_result (google.cloud.dialogflow_v2beta1.types.AgentCoachingInstruction.DuplicateCheckResult):
            Output only. Duplication check for the
            AgentCoachingInstruction.
    """

    class DuplicateCheckResult(proto.Message):
        r"""Duplication check for the suggestion.

        Attributes:
            duplicate_suggestions (MutableSequence[google.cloud.dialogflow_v2beta1.types.AgentCoachingInstruction.DuplicateCheckResult.DuplicateSuggestion]):
                Output only. The duplicate suggestions.
        """

        class DuplicateSuggestion(proto.Message):
            r"""The duplicate suggestion details.

            Attributes:
                answer_record (str):
                    Output only. The answer record id of the past
                    duplicate suggestion.
                suggestion_index (int):
                    Output only. The index of the duplicate
                    suggestion in the past suggestion list.
                similarity_score (float):
                    Output only. The similarity score of between
                    the past and current suggestion.
            """

            answer_record: str = proto.Field(
                proto.STRING,
                number=1,
            )
            suggestion_index: int = proto.Field(
                proto.INT32,
                number=3,
            )
            similarity_score: float = proto.Field(
                proto.FLOAT,
                number=4,
            )

        duplicate_suggestions: MutableSequence[
            "AgentCoachingInstruction.DuplicateCheckResult.DuplicateSuggestion"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="AgentCoachingInstruction.DuplicateCheckResult.DuplicateSuggestion",
        )

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_details: str = proto.Field(
        proto.STRING,
        number=2,
    )
    condition: str = proto.Field(
        proto.STRING,
        number=3,
    )
    agent_action: str = proto.Field(
        proto.STRING,
        number=4,
    )
    system_action: str = proto.Field(
        proto.STRING,
        number=5,
    )
    duplicate_check_result: DuplicateCheckResult = proto.Field(
        proto.MESSAGE,
        number=8,
        message=DuplicateCheckResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
