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

from google.cloud.dialogflow_v2.types import participant
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={
        "AnswerRecord",
        "ListAnswerRecordsRequest",
        "ListAnswerRecordsResponse",
        "UpdateAnswerRecordRequest",
        "AnswerFeedback",
        "AgentAssistantFeedback",
        "AgentAssistantRecord",
    },
)


class AnswerRecord(proto.Message):
    r"""Answer records are records to manage answer history and feedbacks
    for Dialogflow.

    Currently, answer record includes:

    -  human agent assistant article suggestion
    -  human agent assistant faq article

    It doesn't include:

    -  ``DetectIntent`` intent matching
    -  ``DetectIntent`` knowledge

    Answer records are not related to the conversation history in the
    Dialogflow Console. A Record is generated even when the end-user
    disables conversation history in the console. Records are created
    when there's a human agent assistant suggestion generated.

    A typical workflow for customers provide feedback to an answer is:

    1. For human agent assistant, customers get suggestion via
       ListSuggestions API. Together with the answers,
       [AnswerRecord.name][google.cloud.dialogflow.v2.AnswerRecord.name]
       are returned to the customers.
    2. The customer uses the
       [AnswerRecord.name][google.cloud.dialogflow.v2.AnswerRecord.name]
       to call the [UpdateAnswerRecord][] method to send feedback about
       a specific answer that they believe is wrong.

    Attributes:
        name (str):
            The unique identifier of this answer record. Format:
            ``projects/<Project ID>/locations/<Location ID>/answerRecords/<Answer Record ID>``.
        answer_feedback (google.cloud.dialogflow_v2.types.AnswerFeedback):
            Required. The AnswerFeedback for this record. You can set
            this with
            [AnswerRecords.UpdateAnswerRecord][google.cloud.dialogflow.v2.AnswerRecords.UpdateAnswerRecord]
            in order to give us feedback about this answer.
        agent_assistant_record (google.cloud.dialogflow_v2.types.AgentAssistantRecord):
            Output only. The record for human agent
            assistant.
    """

    name = proto.Field(proto.STRING, number=1,)
    answer_feedback = proto.Field(proto.MESSAGE, number=2, message="AnswerFeedback",)
    agent_assistant_record = proto.Field(
        proto.MESSAGE, number=4, oneof="record", message="AgentAssistantRecord",
    )


class ListAnswerRecordsRequest(proto.Message):
    r"""Request message for
    [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2.AnswerRecords.ListAnswerRecords].

    Attributes:
        parent (str):
            Required. The project to list all answer records for in
            reverse chronological order. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        filter (str):
            Required. Filters to restrict results to specific answer
            records. Filter on answer record type. Currently predicates
            on ``type`` is supported, valid values are
            ``ARTICLE_ANSWER``, ``FAQ_ANSWER``.

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
        page_size (int):
            Optional. The maximum number of records to
            return in a single page. The server may return
            fewer records than this. If unspecified, we use
            10. The maximum is 100.
        page_token (str):
            Optional. The
            [ListAnswerRecordsResponse.next_page_token][google.cloud.dialogflow.v2.ListAnswerRecordsResponse.next_page_token]
            value returned from a previous list request used to continue
            listing on the next page.
    """

    parent = proto.Field(proto.STRING, number=1,)
    filter = proto.Field(proto.STRING, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)


class ListAnswerRecordsResponse(proto.Message):
    r"""Response message for
    [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2.AnswerRecords.ListAnswerRecords].

    Attributes:
        answer_records (Sequence[google.cloud.dialogflow_v2.types.AnswerRecord]):
            The list of answer records.
        next_page_token (str):
            A token to retrieve next page of results. Or empty if there
            are no more results. Pass this value in the
            [ListAnswerRecordsRequest.page_token][google.cloud.dialogflow.v2.ListAnswerRecordsRequest.page_token]
            field in the subsequent call to ``ListAnswerRecords`` method
            to retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    answer_records = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AnswerRecord",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class UpdateAnswerRecordRequest(proto.Message):
    r"""Request message for
    [AnswerRecords.UpdateAnswerRecord][google.cloud.dialogflow.v2.AnswerRecords.UpdateAnswerRecord].

    Attributes:
        answer_record (google.cloud.dialogflow_v2.types.AnswerRecord):
            Required. Answer record to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The mask to control which fields
            get updated.
    """

    answer_record = proto.Field(proto.MESSAGE, number=1, message="AnswerRecord",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class AnswerFeedback(proto.Message):
    r"""Represents feedback the customer has about the quality &
    correctness of a certain answer in a conversation.

    Attributes:
        correctness_level (google.cloud.dialogflow_v2.types.AnswerFeedback.CorrectnessLevel):
            The correctness level of the specific answer.
        agent_assistant_detail_feedback (google.cloud.dialogflow_v2.types.AgentAssistantFeedback):
            Detail feedback of agent assist suggestions.
        clicked (bool):
            Indicates whether the answer/item was clicked
            by the human agent or not. Default to false.
        click_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when the answer/item was clicked.
        displayed (bool):
            Indicates whether the answer/item was
            displayed to the human agent in the agent
            desktop UI. Default to false.
        display_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when the answer/item was displayed.
    """

    class CorrectnessLevel(proto.Enum):
        r"""The correctness level of an answer."""
        CORRECTNESS_LEVEL_UNSPECIFIED = 0
        NOT_CORRECT = 1
        PARTIALLY_CORRECT = 2
        FULLY_CORRECT = 3

    correctness_level = proto.Field(proto.ENUM, number=1, enum=CorrectnessLevel,)
    agent_assistant_detail_feedback = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="detail_feedback",
        message="AgentAssistantFeedback",
    )
    clicked = proto.Field(proto.BOOL, number=3,)
    click_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    displayed = proto.Field(proto.BOOL, number=4,)
    display_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )


class AgentAssistantFeedback(proto.Message):
    r"""Detail feedback of Agent Assist result.
    Attributes:
        answer_relevance (google.cloud.dialogflow_v2.types.AgentAssistantFeedback.AnswerRelevance):
            Optional. Whether or not the suggested answer is relevant.

            For example:

            -  Query: "Can I change my mailing address?"
            -  Suggested document says: "Items must be
               returned/exchanged within 60 days of the purchase date."
            -  [answer_relevance][google.cloud.dialogflow.v2.AgentAssistantFeedback.answer_relevance]:
               [AnswerRelevance.IRRELEVANT][google.cloud.dialogflow.v2.AgentAssistantFeedback.AnswerRelevance.IRRELEVANT]
        document_correctness (google.cloud.dialogflow_v2.types.AgentAssistantFeedback.DocumentCorrectness):
            Optional. Whether or not the information in the document is
            correct.

            For example:

            -  Query: "Can I return the package in 2 days once
               received?"
            -  Suggested document says: "Items must be
               returned/exchanged within 60 days of the purchase date."
            -  Ground truth: "No return or exchange is allowed."
            -
        document_efficiency (google.cloud.dialogflow_v2.types.AgentAssistantFeedback.DocumentEfficiency):
            Optional. Whether or not the suggested document is
            efficient. For example, if the document is poorly written,
            hard to understand, hard to use or too long to find useful
            information,
            [document_efficiency][google.cloud.dialogflow.v2.AgentAssistantFeedback.document_efficiency]
            is
            [DocumentEfficiency.INEFFICIENT][google.cloud.dialogflow.v2.AgentAssistantFeedback.DocumentEfficiency.INEFFICIENT].
    """

    class AnswerRelevance(proto.Enum):
        r"""Relevance of an answer."""
        ANSWER_RELEVANCE_UNSPECIFIED = 0
        IRRELEVANT = 1
        RELEVANT = 2

    class DocumentCorrectness(proto.Enum):
        r"""Correctness of document."""
        DOCUMENT_CORRECTNESS_UNSPECIFIED = 0
        INCORRECT = 1
        CORRECT = 2

    class DocumentEfficiency(proto.Enum):
        r"""Efficiency of document."""
        DOCUMENT_EFFICIENCY_UNSPECIFIED = 0
        INEFFICIENT = 1
        EFFICIENT = 2

    answer_relevance = proto.Field(proto.ENUM, number=1, enum=AnswerRelevance,)
    document_correctness = proto.Field(proto.ENUM, number=2, enum=DocumentCorrectness,)
    document_efficiency = proto.Field(proto.ENUM, number=3, enum=DocumentEfficiency,)


class AgentAssistantRecord(proto.Message):
    r"""Represents a record of a human agent assist answer.
    Attributes:
        article_suggestion_answer (google.cloud.dialogflow_v2.types.ArticleAnswer):
            Output only. The article suggestion answer.
        faq_answer (google.cloud.dialogflow_v2.types.FaqAnswer):
            Output only. The FAQ answer.
    """

    article_suggestion_answer = proto.Field(
        proto.MESSAGE, number=5, oneof="answer", message=participant.ArticleAnswer,
    )
    faq_answer = proto.Field(
        proto.MESSAGE, number=6, oneof="answer", message=participant.FaqAnswer,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
