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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.contactcenterinsights.v1",
    manifest={
        "Conversation",
        "Analysis",
        "ConversationDataSource",
        "GcsSource",
        "DialogflowSource",
        "AnalysisResult",
        "IssueModelResult",
        "ConversationLevelSentiment",
        "IssueAssignment",
        "CallAnnotation",
        "AnnotationBoundary",
        "Entity",
        "Intent",
        "PhraseMatchData",
        "DialogflowIntent",
        "InterruptionData",
        "SilenceData",
        "HoldData",
        "EntityMentionData",
        "IntentMatchData",
        "SentimentData",
        "IssueModel",
        "Issue",
        "IssueModelLabelStats",
        "PhraseMatcher",
        "PhraseMatchRuleGroup",
        "PhraseMatchRule",
        "PhraseMatchRuleConfig",
        "ExactMatchConfig",
        "Settings",
        "RuntimeAnnotation",
        "AnswerFeedback",
        "ArticleSuggestionData",
        "FaqAnswerData",
        "SmartReplyData",
        "SmartComposeSuggestionData",
        "DialogflowInteractionData",
        "ConversationParticipant",
        "View",
    },
)


class Conversation(proto.Message):
    r"""The conversation resource.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        call_metadata (google.cloud.contact_center_insights_v1.types.Conversation.CallMetadata):
            Call-specific metadata.

            This field is a member of `oneof`_ ``metadata``.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which this conversation should
            expire. After this time, the conversation data
            and any associated analyses will be deleted.

            This field is a member of `oneof`_ ``expiration``.
        ttl (google.protobuf.duration_pb2.Duration):
            Input only. The TTL for this resource. If
            specified, then this TTL will be used to
            calculate the expire time.

            This field is a member of `oneof`_ ``expiration``.
        name (str):
            Immutable. The resource name of the
            conversation. Format:
            projects/{project}/locations/{location}/conversations/{conversation}
        data_source (google.cloud.contact_center_insights_v1.types.ConversationDataSource):
            The source of the audio and transcription for
            the conversation.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the
            conversation was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time at which
            the conversation was updated.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the conversation started.
        language_code (str):
            A user-specified language code for the
            conversation.
        agent_id (str):
            An opaque, user-specified string representing
            the human agent who handled the conversation.
        labels (Sequence[google.cloud.contact_center_insights_v1.types.Conversation.LabelsEntry]):
            A map for the user to specify any custom
            fields. A maximum of 20 labels per conversation
            is allowed, with a maximum of 256 characters per
            entry.
        transcript (google.cloud.contact_center_insights_v1.types.Conversation.Transcript):
            Output only. The conversation transcript.
        medium (google.cloud.contact_center_insights_v1.types.Conversation.Medium):
            Immutable. The conversation medium, if unspecified will
            default to PHONE_CALL.
        duration (google.protobuf.duration_pb2.Duration):
            Output only. The duration of the
            conversation.
        turn_count (int):
            Output only. The number of turns in the
            conversation.
        latest_analysis (google.cloud.contact_center_insights_v1.types.Analysis):
            Output only. The conversation's latest
            analysis, if one exists.
        runtime_annotations (Sequence[google.cloud.contact_center_insights_v1.types.RuntimeAnnotation]):
            Output only. The annotations that were
            generated during the customer and agent
            interaction.
        dialogflow_intents (Sequence[google.cloud.contact_center_insights_v1.types.Conversation.DialogflowIntentsEntry]):
            Output only. All the matched Dialogflow
            intents in the call. The key corresponds to a
            Dialogflow intent, format:
            projects/{project}/agent/{agent}/intents/{intent}
        obfuscated_user_id (str):
            Obfuscated user ID which the customer sent to
            us.
    """

    class Medium(proto.Enum):
        r"""Possible media for the conversation."""
        MEDIUM_UNSPECIFIED = 0
        PHONE_CALL = 1
        CHAT = 2

    class CallMetadata(proto.Message):
        r"""Call-specific metadata.

        Attributes:
            customer_channel (int):
                The audio channel that contains the customer.
            agent_channel (int):
                The audio channel that contains the agent.
        """

        customer_channel = proto.Field(proto.INT32, number=1,)
        agent_channel = proto.Field(proto.INT32, number=2,)

    class Transcript(proto.Message):
        r"""A message representing the transcript of a conversation.

        Attributes:
            transcript_segments (Sequence[google.cloud.contact_center_insights_v1.types.Conversation.Transcript.TranscriptSegment]):
                A list of sequential transcript segments that
                comprise the conversation.
        """

        class TranscriptSegment(proto.Message):
            r"""A segment of a full transcript.

            Attributes:
                message_time (google.protobuf.timestamp_pb2.Timestamp):
                    The time that the message occurred, if
                    provided.
                text (str):
                    The text of this segment.
                confidence (float):
                    A confidence estimate between 0.0 and 1.0 of
                    the fidelity of this segment. A default value of
                    0.0 indicates that the value is unset.
                words (Sequence[google.cloud.contact_center_insights_v1.types.Conversation.Transcript.TranscriptSegment.WordInfo]):
                    A list of the word-specific information for
                    each word in the segment.
                language_code (str):
                    The language code of this segment as a
                    `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
                    language tag. Example: "en-US".
                channel_tag (int):
                    For conversations derived from multi-channel
                    audio, this is the channel number corresponding
                    to the audio from that channel. For
                    audioChannelCount = N, its output values can
                    range from '1' to 'N'. A channel tag of 0
                    indicates that the audio is mono.
                segment_participant (google.cloud.contact_center_insights_v1.types.ConversationParticipant):
                    The participant of this segment.
                dialogflow_segment_metadata (google.cloud.contact_center_insights_v1.types.Conversation.Transcript.TranscriptSegment.DialogflowSegmentMetadata):
                    CCAI metadata relating to the current
                    transcript segment.
                sentiment (google.cloud.contact_center_insights_v1.types.SentimentData):
                    The sentiment for this transcript segment.
            """

            class WordInfo(proto.Message):
                r"""Word-level info for words in a transcript.

                Attributes:
                    start_offset (google.protobuf.duration_pb2.Duration):
                        Time offset of the start of this word
                        relative to the beginning of the total
                        conversation.
                    end_offset (google.protobuf.duration_pb2.Duration):
                        Time offset of the end of this word relative
                        to the beginning of the total conversation.
                    word (str):
                        The word itself. Includes punctuation marks
                        that surround the word.
                    confidence (float):
                        A confidence estimate between 0.0 and 1.0 of
                        the fidelity of this word. A default value of
                        0.0 indicates that the value is unset.
                """

                start_offset = proto.Field(
                    proto.MESSAGE, number=1, message=duration_pb2.Duration,
                )
                end_offset = proto.Field(
                    proto.MESSAGE, number=2, message=duration_pb2.Duration,
                )
                word = proto.Field(proto.STRING, number=3,)
                confidence = proto.Field(proto.FLOAT, number=4,)

            class DialogflowSegmentMetadata(proto.Message):
                r"""Metadata from Dialogflow relating to the current transcript
                segment.

                Attributes:
                    smart_reply_allowlist_covered (bool):
                        Whether the transcript segment was covered
                        under the configured smart reply allowlist in
                        Agent Assist.
                """

                smart_reply_allowlist_covered = proto.Field(proto.BOOL, number=1,)

            message_time = proto.Field(
                proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
            )
            text = proto.Field(proto.STRING, number=1,)
            confidence = proto.Field(proto.FLOAT, number=2,)
            words = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="Conversation.Transcript.TranscriptSegment.WordInfo",
            )
            language_code = proto.Field(proto.STRING, number=4,)
            channel_tag = proto.Field(proto.INT32, number=5,)
            segment_participant = proto.Field(
                proto.MESSAGE, number=9, message="ConversationParticipant",
            )
            dialogflow_segment_metadata = proto.Field(
                proto.MESSAGE,
                number=10,
                message="Conversation.Transcript.TranscriptSegment.DialogflowSegmentMetadata",
            )
            sentiment = proto.Field(proto.MESSAGE, number=11, message="SentimentData",)

        transcript_segments = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Conversation.Transcript.TranscriptSegment",
        )

    call_metadata = proto.Field(
        proto.MESSAGE, number=7, oneof="metadata", message=CallMetadata,
    )
    expire_time = proto.Field(
        proto.MESSAGE, number=15, oneof="expiration", message=timestamp_pb2.Timestamp,
    )
    ttl = proto.Field(
        proto.MESSAGE, number=16, oneof="expiration", message=duration_pb2.Duration,
    )
    name = proto.Field(proto.STRING, number=1,)
    data_source = proto.Field(
        proto.MESSAGE, number=2, message="ConversationDataSource",
    )
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    start_time = proto.Field(proto.MESSAGE, number=17, message=timestamp_pb2.Timestamp,)
    language_code = proto.Field(proto.STRING, number=14,)
    agent_id = proto.Field(proto.STRING, number=5,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=6,)
    transcript = proto.Field(proto.MESSAGE, number=8, message=Transcript,)
    medium = proto.Field(proto.ENUM, number=9, enum=Medium,)
    duration = proto.Field(proto.MESSAGE, number=10, message=duration_pb2.Duration,)
    turn_count = proto.Field(proto.INT32, number=11,)
    latest_analysis = proto.Field(proto.MESSAGE, number=12, message="Analysis",)
    runtime_annotations = proto.RepeatedField(
        proto.MESSAGE, number=13, message="RuntimeAnnotation",
    )
    dialogflow_intents = proto.MapField(
        proto.STRING, proto.MESSAGE, number=18, message="DialogflowIntent",
    )
    obfuscated_user_id = proto.Field(proto.STRING, number=21,)


class Analysis(proto.Message):
    r"""The analysis resource.

    Attributes:
        name (str):
            Immutable. The resource name of the analysis.
            Format:
            projects/{project}/locations/{location}/conversations/{conversation}/analyses/{analysis}
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the analysis
            was requested.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the analysis
            was created, which occurs when the long-running
            operation completes.
        analysis_result (google.cloud.contact_center_insights_v1.types.AnalysisResult):
            Output only. The result of the analysis,
            which is populated when the analysis finishes.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_time = proto.Field(
        proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,
    )
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    analysis_result = proto.Field(proto.MESSAGE, number=7, message="AnalysisResult",)


class ConversationDataSource(proto.Message):
    r"""The conversation source, which is a combination of transcript
    and audio.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source (google.cloud.contact_center_insights_v1.types.GcsSource):
            A Cloud Storage location specification for
            the audio and transcript.

            This field is a member of `oneof`_ ``source``.
        dialogflow_source (google.cloud.contact_center_insights_v1.types.DialogflowSource):
            The source when the conversation comes from
            Dialogflow.

            This field is a member of `oneof`_ ``source``.
    """

    gcs_source = proto.Field(
        proto.MESSAGE, number=1, oneof="source", message="GcsSource",
    )
    dialogflow_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message="DialogflowSource",
    )


class GcsSource(proto.Message):
    r"""A Cloud Storage source of conversation data.

    Attributes:
        audio_uri (str):
            Cloud Storage URI that points to a file that
            contains the conversation audio.
        transcript_uri (str):
            Immutable. Cloud Storage URI that points to a
            file that contains the conversation transcript.
    """

    audio_uri = proto.Field(proto.STRING, number=1,)
    transcript_uri = proto.Field(proto.STRING, number=2,)


class DialogflowSource(proto.Message):
    r"""A Dialogflow source of conversation data.

    Attributes:
        dialogflow_conversation (str):
            Output only. The name of the Dialogflow
            conversation that this conversation resource is
            derived from. Format:
            projects/{project}/locations/{location}/conversations/{conversation}
        audio_uri (str):
            Cloud Storage URI that points to a file that
            contains the conversation audio.
    """

    dialogflow_conversation = proto.Field(proto.STRING, number=1,)
    audio_uri = proto.Field(proto.STRING, number=3,)


class AnalysisResult(proto.Message):
    r"""The result of an analysis.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        call_analysis_metadata (google.cloud.contact_center_insights_v1.types.AnalysisResult.CallAnalysisMetadata):
            Call-specific metadata created by the
            analysis.

            This field is a member of `oneof`_ ``metadata``.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the analysis ended.
    """

    class CallAnalysisMetadata(proto.Message):
        r"""Call-specific metadata created during analysis.

        Attributes:
            annotations (Sequence[google.cloud.contact_center_insights_v1.types.CallAnnotation]):
                A list of call annotations that apply to this
                call.
            entities (Sequence[google.cloud.contact_center_insights_v1.types.AnalysisResult.CallAnalysisMetadata.EntitiesEntry]):
                All the entities in the call.
            sentiments (Sequence[google.cloud.contact_center_insights_v1.types.ConversationLevelSentiment]):
                Overall conversation-level sentiment for each
                channel of the call.
            intents (Sequence[google.cloud.contact_center_insights_v1.types.AnalysisResult.CallAnalysisMetadata.IntentsEntry]):
                All the matched intents in the call.
            phrase_matchers (Sequence[google.cloud.contact_center_insights_v1.types.AnalysisResult.CallAnalysisMetadata.PhraseMatchersEntry]):
                All the matched phrase matchers in the call.
            issue_model_result (google.cloud.contact_center_insights_v1.types.IssueModelResult):
                Overall conversation-level issue modeling
                result.
        """

        annotations = proto.RepeatedField(
            proto.MESSAGE, number=2, message="CallAnnotation",
        )
        entities = proto.MapField(
            proto.STRING, proto.MESSAGE, number=3, message="Entity",
        )
        sentiments = proto.RepeatedField(
            proto.MESSAGE, number=4, message="ConversationLevelSentiment",
        )
        intents = proto.MapField(
            proto.STRING, proto.MESSAGE, number=6, message="Intent",
        )
        phrase_matchers = proto.MapField(
            proto.STRING, proto.MESSAGE, number=7, message="PhraseMatchData",
        )
        issue_model_result = proto.Field(
            proto.MESSAGE, number=8, message="IssueModelResult",
        )

    call_analysis_metadata = proto.Field(
        proto.MESSAGE, number=2, oneof="metadata", message=CallAnalysisMetadata,
    )
    end_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)


class IssueModelResult(proto.Message):
    r"""Issue Modeling result on a conversation.

    Attributes:
        issue_model (str):
            Issue model that generates the result. Format:
            projects/{project}/locations/{location}/issueModels/{issue_model}
        issues (Sequence[google.cloud.contact_center_insights_v1.types.IssueAssignment]):
            All the matched issues.
    """

    issue_model = proto.Field(proto.STRING, number=1,)
    issues = proto.RepeatedField(proto.MESSAGE, number=2, message="IssueAssignment",)


class ConversationLevelSentiment(proto.Message):
    r"""One channel of conversation-level sentiment data.

    Attributes:
        channel_tag (int):
            The channel of the audio that the data
            applies to.
        sentiment_data (google.cloud.contact_center_insights_v1.types.SentimentData):
            Data specifying sentiment.
    """

    channel_tag = proto.Field(proto.INT32, number=1,)
    sentiment_data = proto.Field(proto.MESSAGE, number=2, message="SentimentData",)


class IssueAssignment(proto.Message):
    r"""Information about the issue.

    Attributes:
        issue (str):
            Resource name of the assigned issue.
        score (float):
            Score indicating the likelihood of the issue assignment.
            currently bounded on [0,1].
        display_name (str):
            Immutable. Display name of the assigned
            issue. This field is set at time of analyis and
            immutable since then.
    """

    issue = proto.Field(proto.STRING, number=1,)
    score = proto.Field(proto.DOUBLE, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)


class CallAnnotation(proto.Message):
    r"""A piece of metadata that applies to a window of a call.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        interruption_data (google.cloud.contact_center_insights_v1.types.InterruptionData):
            Data specifying an interruption.

            This field is a member of `oneof`_ ``data``.
        sentiment_data (google.cloud.contact_center_insights_v1.types.SentimentData):
            Data specifying sentiment.

            This field is a member of `oneof`_ ``data``.
        silence_data (google.cloud.contact_center_insights_v1.types.SilenceData):
            Data specifying silence.

            This field is a member of `oneof`_ ``data``.
        hold_data (google.cloud.contact_center_insights_v1.types.HoldData):
            Data specifying a hold.

            This field is a member of `oneof`_ ``data``.
        entity_mention_data (google.cloud.contact_center_insights_v1.types.EntityMentionData):
            Data specifying an entity mention.

            This field is a member of `oneof`_ ``data``.
        intent_match_data (google.cloud.contact_center_insights_v1.types.IntentMatchData):
            Data specifying an intent match.

            This field is a member of `oneof`_ ``data``.
        phrase_match_data (google.cloud.contact_center_insights_v1.types.PhraseMatchData):
            Data specifying a phrase match.

            This field is a member of `oneof`_ ``data``.
        channel_tag (int):
            The channel of the audio where the annotation
            occurs. For single-channel audio, this field is
            not populated.
        annotation_start_boundary (google.cloud.contact_center_insights_v1.types.AnnotationBoundary):
            The boundary in the conversation where the
            annotation starts, inclusive.
        annotation_end_boundary (google.cloud.contact_center_insights_v1.types.AnnotationBoundary):
            The boundary in the conversation where the
            annotation ends, inclusive.
    """

    interruption_data = proto.Field(
        proto.MESSAGE, number=10, oneof="data", message="InterruptionData",
    )
    sentiment_data = proto.Field(
        proto.MESSAGE, number=11, oneof="data", message="SentimentData",
    )
    silence_data = proto.Field(
        proto.MESSAGE, number=12, oneof="data", message="SilenceData",
    )
    hold_data = proto.Field(proto.MESSAGE, number=13, oneof="data", message="HoldData",)
    entity_mention_data = proto.Field(
        proto.MESSAGE, number=15, oneof="data", message="EntityMentionData",
    )
    intent_match_data = proto.Field(
        proto.MESSAGE, number=16, oneof="data", message="IntentMatchData",
    )
    phrase_match_data = proto.Field(
        proto.MESSAGE, number=17, oneof="data", message="PhraseMatchData",
    )
    channel_tag = proto.Field(proto.INT32, number=1,)
    annotation_start_boundary = proto.Field(
        proto.MESSAGE, number=4, message="AnnotationBoundary",
    )
    annotation_end_boundary = proto.Field(
        proto.MESSAGE, number=5, message="AnnotationBoundary",
    )


class AnnotationBoundary(proto.Message):
    r"""A point in a conversation that marks the start or the end of
    an annotation.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        word_index (int):
            The word index of this boundary with respect
            to the first word in the transcript piece. This
            index starts at zero.

            This field is a member of `oneof`_ ``detailed_boundary``.
        transcript_index (int):
            The index in the sequence of transcribed
            pieces of the conversation where the boundary is
            located. This index starts at zero.
    """

    word_index = proto.Field(proto.INT32, number=3, oneof="detailed_boundary",)
    transcript_index = proto.Field(proto.INT32, number=1,)


class Entity(proto.Message):
    r"""The data for an entity annotation.
    Represents a phrase in the conversation that is a known entity,
    such as a person, an organization, or location.

    Attributes:
        display_name (str):
            The representative name for the entity.
        type_ (google.cloud.contact_center_insights_v1.types.Entity.Type):
            The entity type.
        metadata (Sequence[google.cloud.contact_center_insights_v1.types.Entity.MetadataEntry]):
            Metadata associated with the entity.

            For most entity types, the metadata is a Wikipedia URL
            (``wikipedia_url``) and Knowledge Graph MID (``mid``), if
            they are available. For the metadata associated with other
            entity types, see the Type table below.
        salience (float):
            The salience score associated with the entity in the [0,
            1.0] range.

            The salience score for an entity provides information about
            the importance or centrality of that entity to the entire
            document text. Scores closer to 0 are less salient, while
            scores closer to 1.0 are highly salient.
        sentiment (google.cloud.contact_center_insights_v1.types.SentimentData):
            The aggregate sentiment expressed for this
            entity in the conversation.
    """

    class Type(proto.Enum):
        r"""The type of the entity. For most entity types, the associated
        metadata is a Wikipedia URL (``wikipedia_url``) and Knowledge Graph
        MID (``mid``). The table below lists the associated fields for
        entities that have different metadata.
        """
        TYPE_UNSPECIFIED = 0
        PERSON = 1
        LOCATION = 2
        ORGANIZATION = 3
        EVENT = 4
        WORK_OF_ART = 5
        CONSUMER_GOOD = 6
        OTHER = 7
        PHONE_NUMBER = 9
        ADDRESS = 10
        DATE = 11
        NUMBER = 12
        PRICE = 13

    display_name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=3,)
    salience = proto.Field(proto.FLOAT, number=4,)
    sentiment = proto.Field(proto.MESSAGE, number=5, message="SentimentData",)


class Intent(proto.Message):
    r"""The data for an intent. Represents a detected intent in the
    conversation, for example MAKES_PROMISE.

    Attributes:
        id (str):
            The unique identifier of the intent.
        display_name (str):
            The human-readable name of the intent.
    """

    id = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)


class PhraseMatchData(proto.Message):
    r"""The data for a matched phrase matcher.
    Represents information identifying a phrase matcher for a given
    match.

    Attributes:
        phrase_matcher (str):
            The unique identifier (the resource name) of
            the phrase matcher.
        display_name (str):
            The human-readable name of the phrase
            matcher.
    """

    phrase_matcher = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)


class DialogflowIntent(proto.Message):
    r"""The data for a Dialogflow intent. Represents a detected intent in
    the conversation, e.g. MAKES_PROMISE.

    Attributes:
        display_name (str):
            The human-readable name of the intent.
    """

    display_name = proto.Field(proto.STRING, number=1,)


class InterruptionData(proto.Message):
    r"""The data for an interruption annotation.
    """


class SilenceData(proto.Message):
    r"""The data for a silence annotation.
    """


class HoldData(proto.Message):
    r"""The data for a hold annotation.
    """


class EntityMentionData(proto.Message):
    r"""The data for an entity mention annotation. This represents a mention
    of an ``Entity`` in the conversation.

    Attributes:
        entity_unique_id (str):
            The key of this entity in conversation entities. Can be used
            to retrieve the exact ``Entity`` this mention is attached
            to.
        type_ (google.cloud.contact_center_insights_v1.types.EntityMentionData.MentionType):
            The type of the entity mention.
        sentiment (google.cloud.contact_center_insights_v1.types.SentimentData):
            Sentiment expressed for this mention of the
            entity.
    """

    class MentionType(proto.Enum):
        r"""The supported types of mentions."""
        MENTION_TYPE_UNSPECIFIED = 0
        PROPER = 1
        COMMON = 2

    entity_unique_id = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=MentionType,)
    sentiment = proto.Field(proto.MESSAGE, number=3, message="SentimentData",)


class IntentMatchData(proto.Message):
    r"""The data for an intent match.
    Represents an intent match for a text segment in the
    conversation. A text segment can be part of a sentence, a
    complete sentence, or an utterance with multiple sentences.

    Attributes:
        intent_unique_id (str):
            The id of the matched intent.
            Can be used to retrieve the corresponding intent
            information.
    """

    intent_unique_id = proto.Field(proto.STRING, number=1,)


class SentimentData(proto.Message):
    r"""The data for a sentiment annotation.

    Attributes:
        magnitude (float):
            A non-negative number from 0 to infinity
            which represents the abolute magnitude of
            sentiment regardless of score.
        score (float):
            The sentiment score between -1.0 (negative)
            and 1.0 (positive).
    """

    magnitude = proto.Field(proto.FLOAT, number=1,)
    score = proto.Field(proto.FLOAT, number=2,)


class IssueModel(proto.Message):
    r"""The issue model resource.

    Attributes:
        name (str):
            Immutable. The resource name of the issue model. Format:
            projects/{project}/locations/{location}/issueModels/{issue_model}
        display_name (str):
            The representative name for the issue model.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this issue
            model was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time at which
            the issue model was updated.
        state (google.cloud.contact_center_insights_v1.types.IssueModel.State):
            Output only. State of the model.
        input_data_config (google.cloud.contact_center_insights_v1.types.IssueModel.InputDataConfig):
            Configs for the input data that used to
            create the issue model.
        training_stats (google.cloud.contact_center_insights_v1.types.IssueModelLabelStats):
            Output only. Immutable. The issue model's
            label statistics on its training data.
    """

    class State(proto.Enum):
        r"""State of the model."""
        STATE_UNSPECIFIED = 0
        UNDEPLOYED = 1
        DEPLOYING = 2
        DEPLOYED = 3
        UNDEPLOYING = 4
        DELETING = 5

    class InputDataConfig(proto.Message):
        r"""Configs for the input data used to create the issue model.

        Attributes:
            medium (google.cloud.contact_center_insights_v1.types.Conversation.Medium):
                Medium of conversations used in training data. This field is
                being deprecated. To specify the medium to be used in
                training a new issue model, set the ``medium`` field on
                ``filter``.
            training_conversations_count (int):
                Output only. Number of conversations used in
                training. Output only.
            filter (str):
                A filter to reduce the conversations used for
                training the model to a specific subset.
        """

        medium = proto.Field(proto.ENUM, number=1, enum="Conversation.Medium",)
        training_conversations_count = proto.Field(proto.INT64, number=2,)
        filter = proto.Field(proto.STRING, number=3,)

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)
    input_data_config = proto.Field(proto.MESSAGE, number=6, message=InputDataConfig,)
    training_stats = proto.Field(
        proto.MESSAGE, number=7, message="IssueModelLabelStats",
    )


class Issue(proto.Message):
    r"""The issue resource.

    Attributes:
        name (str):
            Immutable. The resource name of the issue. Format:
            projects/{project}/locations/{location}/issueModels/{issue_model}/issues/{issue}
        display_name (str):
            The representative name for the issue.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this issue was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time that this
            issue was updated.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class IssueModelLabelStats(proto.Message):
    r"""Aggregated statistics about an issue model.

    Attributes:
        analyzed_conversations_count (int):
            Number of conversations the issue model has
            analyzed at this point in time.
        unclassified_conversations_count (int):
            Number of analyzed conversations for which no
            issue was applicable at this point in time.
        issue_stats (Sequence[google.cloud.contact_center_insights_v1.types.IssueModelLabelStats.IssueStatsEntry]):
            Statistics on each issue. Key is the issue's
            resource name.
    """

    class IssueStats(proto.Message):
        r"""Aggregated statistics about an issue.

        Attributes:
            issue (str):
                Issue resource. Format:
                projects/{project}/locations/{location}/issueModels/{issue_model}/issues/{issue}
            labeled_conversations_count (int):
                Number of conversations attached to the issue
                at this point in time.
            display_name (str):
                Display name of the issue.
        """

        issue = proto.Field(proto.STRING, number=1,)
        labeled_conversations_count = proto.Field(proto.INT64, number=2,)
        display_name = proto.Field(proto.STRING, number=3,)

    analyzed_conversations_count = proto.Field(proto.INT64, number=1,)
    unclassified_conversations_count = proto.Field(proto.INT64, number=2,)
    issue_stats = proto.MapField(
        proto.STRING, proto.MESSAGE, number=3, message=IssueStats,
    )


class PhraseMatcher(proto.Message):
    r"""The phrase matcher resource.

    Attributes:
        name (str):
            The resource name of the phrase matcher. Format:
            projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher}
        revision_id (str):
            Output only. Immutable. The revision ID of
            the phrase matcher. A new revision is committed
            whenever the matcher is changed, except when it
            is activated or deactivated. A server generated
            random ID will be used. Example:
            locations/global/phraseMatchers/my-first-
            matcher@1234567
        version_tag (str):
            The customized version tag to use for the phrase matcher. If
            not specified, it will default to ``revision_id``.
        revision_create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp of when the
            revision was created. It is also the create time
            when a new matcher is added.
        display_name (str):
            The human-readable name of the phrase
            matcher.
        type_ (google.cloud.contact_center_insights_v1.types.PhraseMatcher.PhraseMatcherType):
            Required. The type of this phrase matcher.
        active (bool):
            Applies the phrase matcher only when it is
            active.
        phrase_match_rule_groups (Sequence[google.cloud.contact_center_insights_v1.types.PhraseMatchRuleGroup]):
            A list of phase match rule groups that are
            included in this matcher.
        activation_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time at which
            the activation status was updated.
        role_match (google.cloud.contact_center_insights_v1.types.ConversationParticipant.Role):
            The role whose utterances the phrase matcher should be
            matched against. If the role is ROLE_UNSPECIFIED it will be
            matched against any utterances in the transcript.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time at which
            the phrase matcher was updated.
    """

    class PhraseMatcherType(proto.Enum):
        r"""Specifies how to combine each phrase match rule group to
        determine whether there is a match.
        """
        PHRASE_MATCHER_TYPE_UNSPECIFIED = 0
        ALL_OF = 1
        ANY_OF = 2

    name = proto.Field(proto.STRING, number=1,)
    revision_id = proto.Field(proto.STRING, number=2,)
    version_tag = proto.Field(proto.STRING, number=3,)
    revision_create_time = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )
    display_name = proto.Field(proto.STRING, number=5,)
    type_ = proto.Field(proto.ENUM, number=6, enum=PhraseMatcherType,)
    active = proto.Field(proto.BOOL, number=7,)
    phrase_match_rule_groups = proto.RepeatedField(
        proto.MESSAGE, number=8, message="PhraseMatchRuleGroup",
    )
    activation_update_time = proto.Field(
        proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,
    )
    role_match = proto.Field(
        proto.ENUM, number=10, enum="ConversationParticipant.Role",
    )
    update_time = proto.Field(
        proto.MESSAGE, number=11, message=timestamp_pb2.Timestamp,
    )


class PhraseMatchRuleGroup(proto.Message):
    r"""A message representing a rule in the phrase matcher.

    Attributes:
        type_ (google.cloud.contact_center_insights_v1.types.PhraseMatchRuleGroup.PhraseMatchRuleGroupType):
            Required. The type of this phrase match rule
            group.
        phrase_match_rules (Sequence[google.cloud.contact_center_insights_v1.types.PhraseMatchRule]):
            A list of phase match rules that are included
            in this group.
    """

    class PhraseMatchRuleGroupType(proto.Enum):
        r"""Specifies how to combine each phrase match rule for whether
        there is a match.
        """
        PHRASE_MATCH_RULE_GROUP_TYPE_UNSPECIFIED = 0
        ALL_OF = 1
        ANY_OF = 2

    type_ = proto.Field(proto.ENUM, number=1, enum=PhraseMatchRuleGroupType,)
    phrase_match_rules = proto.RepeatedField(
        proto.MESSAGE, number=2, message="PhraseMatchRule",
    )


class PhraseMatchRule(proto.Message):
    r"""The data for a phrase match rule.

    Attributes:
        query (str):
            Required. The phrase to be matched.
        negated (bool):
            Specifies whether the phrase must be missing
            from the transcript segment or present in the
            transcript segment.
        config (google.cloud.contact_center_insights_v1.types.PhraseMatchRuleConfig):
            Provides additional information about the
            rule that specifies how to apply the rule.
    """

    query = proto.Field(proto.STRING, number=1,)
    negated = proto.Field(proto.BOOL, number=2,)
    config = proto.Field(proto.MESSAGE, number=3, message="PhraseMatchRuleConfig",)


class PhraseMatchRuleConfig(proto.Message):
    r"""Configuration information of a phrase match rule.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        exact_match_config (google.cloud.contact_center_insights_v1.types.ExactMatchConfig):
            The configuration for the exact match rule.

            This field is a member of `oneof`_ ``config``.
    """

    exact_match_config = proto.Field(
        proto.MESSAGE, number=1, oneof="config", message="ExactMatchConfig",
    )


class ExactMatchConfig(proto.Message):
    r"""Exact match configuration.

    Attributes:
        case_sensitive (bool):
            Whether to consider case sensitivity when
            performing an exact match.
    """

    case_sensitive = proto.Field(proto.BOOL, number=1,)


class Settings(proto.Message):
    r"""The settings resource.

    Attributes:
        name (str):
            Immutable. The resource name of the settings
            resource. Format:
            projects/{project}/locations/{location}/settings
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the settings
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the settings
            were last updated.
        language_code (str):
            A language code to be applied to each
            transcript segment unless the segment already
            specifies a language code. Language code
            defaults to "en-US" if it is neither specified
            on the segment nor here.
        conversation_ttl (google.protobuf.duration_pb2.Duration):
            The default TTL for newly-created
            conversations. If a conversation has a specified
            expiration, that value will be used instead.
            Changing this value will not change the
            expiration of existing conversations.
            Conversations with no expire time persist until
            they are deleted.
        pubsub_notification_settings (Sequence[google.cloud.contact_center_insights_v1.types.Settings.PubsubNotificationSettingsEntry]):
            A map that maps a notification trigger to a Pub/Sub topic.
            Each time a specified trigger occurs, Insights will notify
            the corresponding Pub/Sub topic.

            Keys are notification triggers. Supported keys are:

            -  "all-triggers": Notify each time any of the supported
               triggers occurs.
            -  "create-analysis": Notify each time an analysis is
               created.
            -  "create-conversation": Notify each time a conversation is
               created.
            -  "export-insights-data": Notify each time an export is
               complete.
            -  "update-conversation": Notify each time a conversation is
               updated via UpdateConversation.

            Values are Pub/Sub topics. The format of each Pub/Sub topic
            is: projects/{project}/topics/{topic}
        analysis_config (google.cloud.contact_center_insights_v1.types.Settings.AnalysisConfig):
            Default analysis settings.
    """

    class AnalysisConfig(proto.Message):
        r"""Default configuration when creating Analyses in Insights.

        Attributes:
            runtime_integration_analysis_percentage (float):
                Percentage of conversations created using Dialogflow runtime
                integration to analyze automatically, between [0, 100].
        """

        runtime_integration_analysis_percentage = proto.Field(proto.DOUBLE, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    language_code = proto.Field(proto.STRING, number=4,)
    conversation_ttl = proto.Field(
        proto.MESSAGE, number=5, message=duration_pb2.Duration,
    )
    pubsub_notification_settings = proto.MapField(proto.STRING, proto.STRING, number=6,)
    analysis_config = proto.Field(proto.MESSAGE, number=7, message=AnalysisConfig,)


class RuntimeAnnotation(proto.Message):
    r"""An annotation that was generated during the customer and
    agent interaction.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        article_suggestion (google.cloud.contact_center_insights_v1.types.ArticleSuggestionData):
            Agent Assist Article Suggestion data.

            This field is a member of `oneof`_ ``data``.
        faq_answer (google.cloud.contact_center_insights_v1.types.FaqAnswerData):
            Agent Assist FAQ answer data.

            This field is a member of `oneof`_ ``data``.
        smart_reply (google.cloud.contact_center_insights_v1.types.SmartReplyData):
            Agent Assist Smart Reply data.

            This field is a member of `oneof`_ ``data``.
        smart_compose_suggestion (google.cloud.contact_center_insights_v1.types.SmartComposeSuggestionData):
            Agent Assist Smart Compose suggestion data.

            This field is a member of `oneof`_ ``data``.
        dialogflow_interaction (google.cloud.contact_center_insights_v1.types.DialogflowInteractionData):
            Dialogflow interaction data.

            This field is a member of `oneof`_ ``data``.
        annotation_id (str):
            The unique identifier of the annotation. Format:
            projects/{project}/locations/{location}/conversationDatasets/{dataset}/conversationDataItems/{data_item}/conversationAnnotations/{annotation}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which this annotation was
            created.
        start_boundary (google.cloud.contact_center_insights_v1.types.AnnotationBoundary):
            The boundary in the conversation where the
            annotation starts, inclusive.
        end_boundary (google.cloud.contact_center_insights_v1.types.AnnotationBoundary):
            The boundary in the conversation where the
            annotation ends, inclusive.
        answer_feedback (google.cloud.contact_center_insights_v1.types.AnswerFeedback):
            The feedback that the customer has about the answer in
            ``data``.
    """

    article_suggestion = proto.Field(
        proto.MESSAGE, number=6, oneof="data", message="ArticleSuggestionData",
    )
    faq_answer = proto.Field(
        proto.MESSAGE, number=7, oneof="data", message="FaqAnswerData",
    )
    smart_reply = proto.Field(
        proto.MESSAGE, number=8, oneof="data", message="SmartReplyData",
    )
    smart_compose_suggestion = proto.Field(
        proto.MESSAGE, number=9, oneof="data", message="SmartComposeSuggestionData",
    )
    dialogflow_interaction = proto.Field(
        proto.MESSAGE, number=10, oneof="data", message="DialogflowInteractionData",
    )
    annotation_id = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    start_boundary = proto.Field(proto.MESSAGE, number=3, message="AnnotationBoundary",)
    end_boundary = proto.Field(proto.MESSAGE, number=4, message="AnnotationBoundary",)
    answer_feedback = proto.Field(proto.MESSAGE, number=5, message="AnswerFeedback",)


class AnswerFeedback(proto.Message):
    r"""The feedback that the customer has about a certain answer in
    the conversation.

    Attributes:
        correctness_level (google.cloud.contact_center_insights_v1.types.AnswerFeedback.CorrectnessLevel):
            The correctness level of an answer.
        clicked (bool):
            Indicates whether an answer or item was
            clicked by the human agent.
        displayed (bool):
            Indicates whether an answer or item was
            displayed to the human agent in the agent
            desktop UI.
    """

    class CorrectnessLevel(proto.Enum):
        r"""The correctness level of an answer."""
        CORRECTNESS_LEVEL_UNSPECIFIED = 0
        NOT_CORRECT = 1
        PARTIALLY_CORRECT = 2
        FULLY_CORRECT = 3

    correctness_level = proto.Field(proto.ENUM, number=1, enum=CorrectnessLevel,)
    clicked = proto.Field(proto.BOOL, number=2,)
    displayed = proto.Field(proto.BOOL, number=3,)


class ArticleSuggestionData(proto.Message):
    r"""Agent Assist Article Suggestion data.

    Attributes:
        title (str):
            Article title.
        uri (str):
            Article URI.
        confidence_score (float):
            The system's confidence score that this
            article is a good match for this conversation,
            ranging from 0.0 (completely uncertain) to 1.0
            (completely certain).
        metadata (Sequence[google.cloud.contact_center_insights_v1.types.ArticleSuggestionData.MetadataEntry]):
            Map that contains metadata about the Article
            Suggestion and the document that it originates
            from.
        query_record (str):
            Name of the query record. Format:
            projects/{project}/locations/{location}/queryRecords/{query_record}
        source (str):
            The knowledge document that this answer was extracted from.
            Format:
            projects/{project}/knowledgeBases/{knowledge_base}/documents/{document}
    """

    title = proto.Field(proto.STRING, number=1,)
    uri = proto.Field(proto.STRING, number=2,)
    confidence_score = proto.Field(proto.FLOAT, number=3,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=4,)
    query_record = proto.Field(proto.STRING, number=5,)
    source = proto.Field(proto.STRING, number=6,)


class FaqAnswerData(proto.Message):
    r"""Agent Assist frequently-asked-question answer data.

    Attributes:
        answer (str):
            The piece of text from the ``source`` knowledge base
            document.
        confidence_score (float):
            The system's confidence score that this
            answer is a good match for this conversation,
            ranging from 0.0 (completely uncertain) to 1.0
            (completely certain).
        question (str):
            The corresponding FAQ question.
        metadata (Sequence[google.cloud.contact_center_insights_v1.types.FaqAnswerData.MetadataEntry]):
            Map that contains metadata about the FAQ
            answer and the document that it originates from.
        query_record (str):
            Name of the query record. Format:
            projects/{project}/locations/{location}/queryRecords/{query_record}.
        source (str):
            The knowledge document that this answer was extracted from.
            Format:
            projects/{project}/knowledgeBases/{knowledge_base}/documents/{document}.
    """

    answer = proto.Field(proto.STRING, number=1,)
    confidence_score = proto.Field(proto.FLOAT, number=2,)
    question = proto.Field(proto.STRING, number=3,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=4,)
    query_record = proto.Field(proto.STRING, number=5,)
    source = proto.Field(proto.STRING, number=6,)


class SmartReplyData(proto.Message):
    r"""Agent Assist Smart Reply data.

    Attributes:
        reply (str):
            The content of the reply.
        confidence_score (float):
            The system's confidence score that this reply
            is a good match for this conversation, ranging
            from 0.0 (completely uncertain) to 1.0
            (completely certain).
        metadata (Sequence[google.cloud.contact_center_insights_v1.types.SmartReplyData.MetadataEntry]):
            Map that contains metadata about the Smart
            Reply and the document from which it originates.
        query_record (str):
            Name of the query record. Format:
            projects/{project}/locations/{location}/queryRecords/{query_record}
    """

    reply = proto.Field(proto.STRING, number=1,)
    confidence_score = proto.Field(proto.DOUBLE, number=2,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=3,)
    query_record = proto.Field(proto.STRING, number=4,)


class SmartComposeSuggestionData(proto.Message):
    r"""Agent Assist Smart Compose suggestion data.

    Attributes:
        suggestion (str):
            The content of the suggestion.
        confidence_score (float):
            The system's confidence score that this
            suggestion is a good match for this
            conversation, ranging from 0.0 (completely
            uncertain) to 1.0 (completely certain).
        metadata (Sequence[google.cloud.contact_center_insights_v1.types.SmartComposeSuggestionData.MetadataEntry]):
            Map that contains metadata about the Smart
            Compose suggestion and the document from which
            it originates.
        query_record (str):
            Name of the query record. Format:
            projects/{project}/locations/{location}/queryRecords/{query_record}
    """

    suggestion = proto.Field(proto.STRING, number=1,)
    confidence_score = proto.Field(proto.DOUBLE, number=2,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=3,)
    query_record = proto.Field(proto.STRING, number=4,)


class DialogflowInteractionData(proto.Message):
    r"""Dialogflow interaction data.

    Attributes:
        dialogflow_intent_id (str):
            The Dialogflow intent resource path. Format:
            projects/{project}/agent/{agent}/intents/{intent}
        confidence (float):
            The confidence of the match ranging from 0.0
            (completely uncertain) to 1.0 (completely
            certain).
    """

    dialogflow_intent_id = proto.Field(proto.STRING, number=1,)
    confidence = proto.Field(proto.FLOAT, number=2,)


class ConversationParticipant(proto.Message):
    r"""The call participant speaking for a given utterance.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dialogflow_participant_name (str):
            The name of the participant provided by
            Dialogflow. Format:
            projects/{project}/locations/{location}/conversations/{conversation}/participants/{participant}

            This field is a member of `oneof`_ ``participant``.
        user_id (str):
            A user-specified ID representing the
            participant.

            This field is a member of `oneof`_ ``participant``.
        dialogflow_participant (str):
            Deprecated. Use ``dialogflow_participant_name`` instead. The
            name of the Dialogflow participant. Format:
            projects/{project}/locations/{location}/conversations/{conversation}/participants/{participant}
        obfuscated_external_user_id (str):
            Obfuscated user ID from Dialogflow.
        role (google.cloud.contact_center_insights_v1.types.ConversationParticipant.Role):
            The role of the participant.
    """

    class Role(proto.Enum):
        r"""The role of the participant."""
        ROLE_UNSPECIFIED = 0
        HUMAN_AGENT = 1
        AUTOMATED_AGENT = 2
        END_USER = 3
        ANY_AGENT = 4

    dialogflow_participant_name = proto.Field(
        proto.STRING, number=5, oneof="participant",
    )
    user_id = proto.Field(proto.STRING, number=6, oneof="participant",)
    dialogflow_participant = proto.Field(proto.STRING, number=1,)
    obfuscated_external_user_id = proto.Field(proto.STRING, number=3,)
    role = proto.Field(proto.ENUM, number=2, enum=Role,)


class View(proto.Message):
    r"""The View resource.

    Attributes:
        name (str):
            Immutable. The resource name of the view.
            Format:
            projects/{project}/locations/{location}/views/{view}
        display_name (str):
            The human-readable display name of the view.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this view was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time at which
            the view was updated.
        value (str):
            String with specific view properties.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    value = proto.Field(proto.STRING, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
