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

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={
        "TriggerEvent",
        "CreateGeneratorRequest",
        "GetGeneratorRequest",
        "ListGeneratorsRequest",
        "ListGeneratorsResponse",
        "DeleteGeneratorRequest",
        "UpdateGeneratorRequest",
        "MessageEntry",
        "ConversationContext",
        "SummarizationSectionList",
        "FewShotExample",
        "InferenceParameter",
        "SummarizationSection",
        "SummarizationContext",
        "Generator",
        "SummarySuggestion",
        "GeneratorSuggestion",
    },
)


class TriggerEvent(proto.Enum):
    r"""The event that triggers the generator and LLM execution.

    Values:
        TRIGGER_EVENT_UNSPECIFIED (0):
            Default value for TriggerEvent.
        END_OF_UTTERANCE (1):
            Triggers when each chat message or voice
            utterance ends.
        MANUAL_CALL (2):
            Triggers on the conversation manually by API
            calls, such as
            Conversations.GenerateStatelessSuggestion and
            Conversations.GenerateSuggestions.
    """
    TRIGGER_EVENT_UNSPECIFIED = 0
    END_OF_UTTERANCE = 1
    MANUAL_CALL = 2


class CreateGeneratorRequest(proto.Message):
    r"""Request message of CreateGenerator.

    Attributes:
        parent (str):
            Required. The project/location to create generator for.
            Format: ``projects/<Project ID>/locations/<Location ID>``
        generator (google.cloud.dialogflow_v2.types.Generator):
            Required. The generator to create.
        generator_id (str):
            Optional. The ID to use for the generator, which will become
            the final component of the generator's resource name.

            The generator ID must be compliant with the regression
            formula ``[a-zA-Z][a-zA-Z0-9_-]*`` with the characters
            length in range of [3,64]. If the field is not provided, an
            Id will be auto-generated. If the field is provided, the
            caller is responsible for

            1. the uniqueness of the ID, otherwise the request will be
               rejected.
            2. the consistency for whether to use custom ID or not under
               a project to better ensure uniqueness.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    generator: "Generator" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Generator",
    )
    generator_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GetGeneratorRequest(proto.Message):
    r"""Request message of GetGenerator.

    Attributes:
        name (str):
            Required. The generator resource name to retrieve. Format:
            ``projects/<Project ID>/locations/<Location ID>/generators/<Generator ID>``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListGeneratorsRequest(proto.Message):
    r"""Request message of ListGenerators.

    Attributes:
        parent (str):
            Required. The project/location to list generators for.
            Format: ``projects/<Project ID>/locations/<Location ID>``
        page_size (int):
            Optional. Maximum number of conversation
            models to return in a single page. Default to
            10.
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


class ListGeneratorsResponse(proto.Message):
    r"""Response of ListGenerators.

    Attributes:
        generators (MutableSequence[google.cloud.dialogflow_v2.types.Generator]):
            List of generators retrieved.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    generators: MutableSequence["Generator"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Generator",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteGeneratorRequest(proto.Message):
    r"""Request of DeleteGenerator.

    Attributes:
        name (str):
            Required. The generator resource name to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/generators/<Generator ID>``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateGeneratorRequest(proto.Message):
    r"""Request of UpdateGenerator.

    Attributes:
        generator (google.cloud.dialogflow_v2.types.Generator):
            Required. The generator to update.
            The name field of generator is to identify the
            generator to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The list of fields to update.
    """

    generator: "Generator" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Generator",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class MessageEntry(proto.Message):
    r"""Represents a message entry of a conversation.

    Attributes:
        role (google.cloud.dialogflow_v2.types.MessageEntry.Role):
            Optional. Participant role of the message.
        text (str):
            Optional. Transcript content of the message.
        language_code (str):
            Optional. The language of the text. See `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Create time of the message entry.
    """

    class Role(proto.Enum):
        r"""Enumeration of the roles a participant can play in a
        conversation.

        Values:
            ROLE_UNSPECIFIED (0):
                Participant role not set.
            HUMAN_AGENT (1):
                Participant is a human agent.
            AUTOMATED_AGENT (2):
                Participant is an automated agent, such as a
                Dialogflow agent.
            END_USER (3):
                Participant is an end user that has called or
                chatted with Dialogflow services.
        """
        ROLE_UNSPECIFIED = 0
        HUMAN_AGENT = 1
        AUTOMATED_AGENT = 2
        END_USER = 3

    role: Role = proto.Field(
        proto.ENUM,
        number=1,
        enum=Role,
    )
    text: str = proto.Field(
        proto.STRING,
        number=2,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class ConversationContext(proto.Message):
    r"""Context of the conversation, including transcripts.

    Attributes:
        message_entries (MutableSequence[google.cloud.dialogflow_v2.types.MessageEntry]):
            Optional. List of message transcripts in the
            conversation.
    """

    message_entries: MutableSequence["MessageEntry"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="MessageEntry",
    )


class SummarizationSectionList(proto.Message):
    r"""List of summarization sections.

    Attributes:
        summarization_sections (MutableSequence[google.cloud.dialogflow_v2.types.SummarizationSection]):
            Optional. Summarization sections.
    """

    summarization_sections: MutableSequence[
        "SummarizationSection"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SummarizationSection",
    )


class FewShotExample(proto.Message):
    r"""Providing examples in the generator (i.e. building a few-shot
    generator) helps convey the desired format of the LLM response.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        conversation_context (google.cloud.dialogflow_v2.types.ConversationContext):
            Optional. Conversation transcripts.
        extra_info (MutableMapping[str, str]):
            Optional. Key is the placeholder field name
            in input, value is the value of the placeholder.
            E.g. instruction contains "@price", and ingested
            data has <"price", "10">
        summarization_section_list (google.cloud.dialogflow_v2.types.SummarizationSectionList):
            Summarization sections.

            This field is a member of `oneof`_ ``instruction_list``.
        output (google.cloud.dialogflow_v2.types.GeneratorSuggestion):
            Required. Example output of the model.
    """

    conversation_context: "ConversationContext" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ConversationContext",
    )
    extra_info: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    summarization_section_list: "SummarizationSectionList" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="instruction_list",
        message="SummarizationSectionList",
    )
    output: "GeneratorSuggestion" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="GeneratorSuggestion",
    )


class InferenceParameter(proto.Message):
    r"""The parameters of inference.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        max_output_tokens (int):
            Optional. Maximum number of the output tokens
            for the generator.

            This field is a member of `oneof`_ ``_max_output_tokens``.
        temperature (float):
            Optional. Controls the randomness of LLM
            predictions. Low temperature = less random. High
            temperature = more random. If unset (or 0), uses
            a default value of 0.

            This field is a member of `oneof`_ ``_temperature``.
        top_k (int):
            Optional. Top-k changes how the model selects tokens for
            output. A top-k of 1 means the selected token is the most
            probable among all tokens in the model's vocabulary (also
            called greedy decoding), while a top-k of 3 means that the
            next token is selected from among the 3 most probable tokens
            (using temperature). For each token selection step, the top
            K tokens with the highest probabilities are sampled. Then
            tokens are further filtered based on topP with the final
            token selected using temperature sampling. Specify a lower
            value for less random responses and a higher value for more
            random responses. Acceptable value is [1, 40], default to
            40.

            This field is a member of `oneof`_ ``_top_k``.
        top_p (float):
            Optional. Top-p changes how the model selects tokens for
            output. Tokens are selected from most K (see topK parameter)
            probable to least until the sum of their probabilities
            equals the top-p value. For example, if tokens A, B, and C
            have a probability of 0.3, 0.2, and 0.1 and the top-p value
            is 0.5, then the model will select either A or B as the next
            token (using temperature) and doesn't consider C. The
            default top-p value is 0.95. Specify a lower value for less
            random responses and a higher value for more random
            responses. Acceptable value is [0.0, 1.0], default to 0.95.

            This field is a member of `oneof`_ ``_top_p``.
    """

    max_output_tokens: int = proto.Field(
        proto.INT32,
        number=1,
        optional=True,
    )
    temperature: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )
    top_k: int = proto.Field(
        proto.INT32,
        number=3,
        optional=True,
    )
    top_p: float = proto.Field(
        proto.DOUBLE,
        number=4,
        optional=True,
    )


class SummarizationSection(proto.Message):
    r"""Represents the section of summarization.

    Attributes:
        key (str):
            Optional. Name of the section, for example,
            "situation".
        definition (str):
            Optional. Definition of the section, for
            example, "what the customer needs help with or
            has question about.".
        type_ (google.cloud.dialogflow_v2.types.SummarizationSection.Type):
            Optional. Type of the summarization section.
    """

    class Type(proto.Enum):
        r"""Type enum of the summarization sections.

        Values:
            TYPE_UNSPECIFIED (0):
                Undefined section type, does not return
                anything.
            SITUATION (1):
                What the customer needs help with or has
                question about. Section name: "situation".
            ACTION (2):
                What the agent does to help the customer.
                Section name: "action".
            RESOLUTION (3):
                Result of the customer service. A single word
                describing the result of the conversation.
                Section name: "resolution".
            REASON_FOR_CANCELLATION (4):
                Reason for cancellation if the customer requests for a
                cancellation. "N/A" otherwise. Section name:
                "reason_for_cancellation".
            CUSTOMER_SATISFACTION (5):
                "Unsatisfied" or "Satisfied" depending on the customer's
                feelings at the end of the conversation. Section name:
                "customer_satisfaction".
            ENTITIES (6):
                Key entities extracted from the conversation,
                such as ticket number, order number, dollar
                amount, etc. Section names are prefixed by
                "entities/".
            CUSTOMER_DEFINED (7):
                Customer defined sections.
        """
        TYPE_UNSPECIFIED = 0
        SITUATION = 1
        ACTION = 2
        RESOLUTION = 3
        REASON_FOR_CANCELLATION = 4
        CUSTOMER_SATISFACTION = 5
        ENTITIES = 6
        CUSTOMER_DEFINED = 7

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    definition: str = proto.Field(
        proto.STRING,
        number=2,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=3,
        enum=Type,
    )


class SummarizationContext(proto.Message):
    r"""Summarization context that customer can configure.

    Attributes:
        summarization_sections (MutableSequence[google.cloud.dialogflow_v2.types.SummarizationSection]):
            Optional. List of sections. Note it contains
            both predefined section sand customer defined
            sections.
        few_shot_examples (MutableSequence[google.cloud.dialogflow_v2.types.FewShotExample]):
            Optional. List of few shot examples.
        version (str):
            Optional. Version of the feature. If not set, default to
            latest version. Current candidates are ["1.0"].
        output_language_code (str):
            Optional. The target language of the
            generated summary. The language code for
            conversation will be used if this field is
            empty. Supported 2.0 and later versions.
    """

    summarization_sections: MutableSequence[
        "SummarizationSection"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SummarizationSection",
    )
    few_shot_examples: MutableSequence["FewShotExample"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="FewShotExample",
    )
    version: str = proto.Field(
        proto.STRING,
        number=3,
    )
    output_language_code: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Generator(proto.Message):
    r"""LLM generator.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. Identifier. The resource name of the generator.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/generators/<Generator ID>``
        description (str):
            Optional. Human readable description of the
            generator.
        summarization_context (google.cloud.dialogflow_v2.types.SummarizationContext):
            Input of prebuilt Summarization feature.

            This field is a member of `oneof`_ ``context``.
        inference_parameter (google.cloud.dialogflow_v2.types.InferenceParameter):
            Optional. Inference parameters for this
            generator.
        trigger_event (google.cloud.dialogflow_v2.types.TriggerEvent):
            Optional. The trigger event of the generator.
            It defines when the generator is triggered in a
            conversation.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this generator.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time of this generator.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    summarization_context: "SummarizationContext" = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="context",
        message="SummarizationContext",
    )
    inference_parameter: "InferenceParameter" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="InferenceParameter",
    )
    trigger_event: "TriggerEvent" = proto.Field(
        proto.ENUM,
        number=5,
        enum="TriggerEvent",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )


class SummarySuggestion(proto.Message):
    r"""Suggested summary of the conversation.

    Attributes:
        summary_sections (MutableSequence[google.cloud.dialogflow_v2.types.SummarySuggestion.SummarySection]):
            Required. All the parts of generated summary.
    """

    class SummarySection(proto.Message):
        r"""A component of the generated summary.

        Attributes:
            section (str):
                Required. Name of the section.
            summary (str):
                Required. Summary text for the section.
        """

        section: str = proto.Field(
            proto.STRING,
            number=1,
        )
        summary: str = proto.Field(
            proto.STRING,
            number=2,
        )

    summary_sections: MutableSequence[SummarySection] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=SummarySection,
    )


class GeneratorSuggestion(proto.Message):
    r"""Suggestion generated using a Generator.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        summary_suggestion (google.cloud.dialogflow_v2.types.SummarySuggestion):
            Optional. Suggested summary.

            This field is a member of `oneof`_ ``suggestion``.
    """

    summary_suggestion: "SummarySuggestion" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="suggestion",
        message="SummarySuggestion",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
