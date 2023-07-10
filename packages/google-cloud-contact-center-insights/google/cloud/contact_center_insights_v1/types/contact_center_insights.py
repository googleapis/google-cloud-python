# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.contact_center_insights_v1.types import resources

__protobuf__ = proto.module(
    package="google.cloud.contactcenterinsights.v1",
    manifest={
        "ConversationView",
        "CalculateStatsRequest",
        "CalculateStatsResponse",
        "CreateAnalysisOperationMetadata",
        "CreateConversationRequest",
        "UploadConversationRequest",
        "UploadConversationMetadata",
        "ListConversationsRequest",
        "ListConversationsResponse",
        "GetConversationRequest",
        "UpdateConversationRequest",
        "DeleteConversationRequest",
        "IngestConversationsRequest",
        "IngestConversationsMetadata",
        "IngestConversationsResponse",
        "CreateAnalysisRequest",
        "ListAnalysesRequest",
        "ListAnalysesResponse",
        "GetAnalysisRequest",
        "DeleteAnalysisRequest",
        "BulkAnalyzeConversationsRequest",
        "BulkAnalyzeConversationsMetadata",
        "BulkAnalyzeConversationsResponse",
        "ExportInsightsDataRequest",
        "ExportInsightsDataMetadata",
        "ExportInsightsDataResponse",
        "CreateIssueModelRequest",
        "CreateIssueModelMetadata",
        "UpdateIssueModelRequest",
        "ListIssueModelsRequest",
        "ListIssueModelsResponse",
        "GetIssueModelRequest",
        "DeleteIssueModelRequest",
        "DeleteIssueModelMetadata",
        "DeployIssueModelRequest",
        "DeployIssueModelResponse",
        "DeployIssueModelMetadata",
        "UndeployIssueModelRequest",
        "UndeployIssueModelResponse",
        "UndeployIssueModelMetadata",
        "GetIssueRequest",
        "ListIssuesRequest",
        "ListIssuesResponse",
        "UpdateIssueRequest",
        "DeleteIssueRequest",
        "CalculateIssueModelStatsRequest",
        "CalculateIssueModelStatsResponse",
        "CreatePhraseMatcherRequest",
        "ListPhraseMatchersRequest",
        "ListPhraseMatchersResponse",
        "GetPhraseMatcherRequest",
        "DeletePhraseMatcherRequest",
        "UpdatePhraseMatcherRequest",
        "GetSettingsRequest",
        "UpdateSettingsRequest",
        "CreateViewRequest",
        "GetViewRequest",
        "ListViewsRequest",
        "ListViewsResponse",
        "UpdateViewRequest",
        "DeleteViewRequest",
    },
)


class ConversationView(proto.Enum):
    r"""Represents the options for viewing a conversation.

    Values:
        CONVERSATION_VIEW_UNSPECIFIED (0):
            The conversation view is not specified.

            -  Defaults to ``FULL`` in ``GetConversationRequest``.
            -  Defaults to ``BASIC`` in ``ListConversationsRequest``.
        FULL (2):
            Populates all fields in the conversation.
        BASIC (1):
            Populates all fields in the conversation
            except the transcript.
    """
    CONVERSATION_VIEW_UNSPECIFIED = 0
    FULL = 2
    BASIC = 1


class CalculateStatsRequest(proto.Message):
    r"""The request for calculating conversation statistics.

    Attributes:
        location (str):
            Required. The location of the conversations.
        filter (str):
            A filter to reduce results to a specific
            subset. This field is useful for getting
            statistics about conversations with specific
            properties.
    """

    location: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CalculateStatsResponse(proto.Message):
    r"""The response for calculating conversation statistics.

    Attributes:
        average_duration (google.protobuf.duration_pb2.Duration):
            The average duration of all conversations.
            The average is calculated using only
            conversations that have a time duration.
        average_turn_count (int):
            The average number of turns per conversation.
        conversation_count (int):
            The total number of conversations.
        smart_highlighter_matches (MutableMapping[str, int]):
            A map associating each smart highlighter
            display name with its respective number of
            matches in the set of conversations.
        custom_highlighter_matches (MutableMapping[str, int]):
            A map associating each custom highlighter
            resource name with its respective number of
            matches in the set of conversations.
        issue_matches (MutableMapping[str, int]):
            A map associating each issue resource name with its
            respective number of matches in the set of conversations.
            Key has the format:
            ``projects/<Project-ID>/locations/<Location-ID>/issueModels/<Issue-Model-ID>/issues/<Issue-ID>``
            Deprecated, use ``issue_matches_stats`` field instead.
        issue_matches_stats (MutableMapping[str, google.cloud.contact_center_insights_v1.types.IssueModelLabelStats.IssueStats]):
            A map associating each issue resource name with its
            respective number of matches in the set of conversations.
            Key has the format:
            ``projects/<Project-ID>/locations/<Location-ID>/issueModels/<Issue-Model-ID>/issues/<Issue-ID>``
        conversation_count_time_series (google.cloud.contact_center_insights_v1.types.CalculateStatsResponse.TimeSeries):
            A time series representing the count of
            conversations created over time that match that
            requested filter criteria.
    """

    class TimeSeries(proto.Message):
        r"""A time series representing conversations over time.

        Attributes:
            interval_duration (google.protobuf.duration_pb2.Duration):
                The duration of each interval.
            points (MutableSequence[google.cloud.contact_center_insights_v1.types.CalculateStatsResponse.TimeSeries.Interval]):
                An ordered list of intervals from earliest to
                latest, where each interval represents the
                number of conversations that transpired during
                the time window.
        """

        class Interval(proto.Message):
            r"""A single interval in a time series.

            Attributes:
                start_time (google.protobuf.timestamp_pb2.Timestamp):
                    The start time of this interval.
                conversation_count (int):
                    The number of conversations created in this
                    interval.
            """

            start_time: timestamp_pb2.Timestamp = proto.Field(
                proto.MESSAGE,
                number=1,
                message=timestamp_pb2.Timestamp,
            )
            conversation_count: int = proto.Field(
                proto.INT32,
                number=2,
            )

        interval_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )
        points: MutableSequence[
            "CalculateStatsResponse.TimeSeries.Interval"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="CalculateStatsResponse.TimeSeries.Interval",
        )

    average_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )
    average_turn_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    conversation_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    smart_highlighter_matches: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT32,
        number=4,
    )
    custom_highlighter_matches: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT32,
        number=5,
    )
    issue_matches: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT32,
        number=6,
    )
    issue_matches_stats: MutableMapping[
        str, resources.IssueModelLabelStats.IssueStats
    ] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=8,
        message=resources.IssueModelLabelStats.IssueStats,
    )
    conversation_count_time_series: TimeSeries = proto.Field(
        proto.MESSAGE,
        number=7,
        message=TimeSeries,
    )


class CreateAnalysisOperationMetadata(proto.Message):
    r"""Metadata for a create analysis operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        conversation (str):
            Output only. The Conversation that this
            Analysis Operation belongs to.
        annotator_selector (google.cloud.contact_center_insights_v1.types.AnnotatorSelector):
            Output only. The annotator selector used for
            the analysis (if any).
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    conversation: str = proto.Field(
        proto.STRING,
        number=3,
    )
    annotator_selector: resources.AnnotatorSelector = proto.Field(
        proto.MESSAGE,
        number=4,
        message=resources.AnnotatorSelector,
    )


class CreateConversationRequest(proto.Message):
    r"""Request to create a conversation.

    Attributes:
        parent (str):
            Required. The parent resource of the
            conversation.
        conversation (google.cloud.contact_center_insights_v1.types.Conversation):
            Required. The conversation resource to
            create.
        conversation_id (str):
            A unique ID for the new conversation. This ID will become
            the final component of the conversation's resource name. If
            no ID is specified, a server-generated ID will be used.

            This value should be 4-64 characters and must match the
            regular expression ``^[a-z0-9-]{4,64}$``. Valid characters
            are ``[a-z][0-9]-``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation: resources.Conversation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Conversation,
    )
    conversation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UploadConversationRequest(proto.Message):
    r"""Request to upload a conversation.

    Attributes:
        parent (str):
            Required. The parent resource of the
            conversation.
        conversation (google.cloud.contact_center_insights_v1.types.Conversation):
            Required. The conversation resource to
            create.
        conversation_id (str):
            Optional. A unique ID for the new conversation. This ID will
            become the final component of the conversation's resource
            name. If no ID is specified, a server-generated ID will be
            used.

            This value should be 4-64 characters and must match the
            regular expression ``^[a-z0-9-]{4,64}$``. Valid characters
            are ``[a-z][0-9]-``
        redaction_config (google.cloud.contact_center_insights_v1.types.RedactionConfig):
            Optional. DLP settings for transcript
            redaction. Optional, will default to the config
            specified in Settings.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation: resources.Conversation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Conversation,
    )
    conversation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    redaction_config: resources.RedactionConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=resources.RedactionConfig,
    )


class UploadConversationMetadata(proto.Message):
    r"""The metadata for an UploadConversation operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.UploadConversationRequest):
            Output only. The original request.
        analysis_operation (str):
            Output only. The operation name for a
            successfully created analysis operation, if any.
        applied_redaction_config (google.cloud.contact_center_insights_v1.types.RedactionConfig):
            Output only. The redaction config applied to
            the uploaded conversation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "UploadConversationRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="UploadConversationRequest",
    )
    analysis_operation: str = proto.Field(
        proto.STRING,
        number=4,
    )
    applied_redaction_config: resources.RedactionConfig = proto.Field(
        proto.MESSAGE,
        number=5,
        message=resources.RedactionConfig,
    )


class ListConversationsRequest(proto.Message):
    r"""Request to list conversations.

    Attributes:
        parent (str):
            Required. The parent resource of the
            conversation.
        page_size (int):
            The maximum number of conversations to return
            in the response. A valid page size ranges from 0
            to 1,000 inclusive. If the page size is zero or
            unspecified, a default page size of 100 will be
            chosen. Note that a call might return fewer
            results than the requested page size.
        page_token (str):
            The value returned by the last
            ``ListConversationsResponse``. This value indicates that
            this is a continuation of a prior ``ListConversations`` call
            and that the system should return the next page of data.
        filter (str):
            A filter to reduce results to a specific
            subset. Useful for querying conversations with
            specific properties.
        view (google.cloud.contact_center_insights_v1.types.ConversationView):
            The level of details of the conversation. Default is
            ``BASIC``.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    view: "ConversationView" = proto.Field(
        proto.ENUM,
        number=5,
        enum="ConversationView",
    )


class ListConversationsResponse(proto.Message):
    r"""The response of listing conversations.

    Attributes:
        conversations (MutableSequence[google.cloud.contact_center_insights_v1.types.Conversation]):
            The conversations that match the request.
        next_page_token (str):
            A token which can be sent as ``page_token`` to retrieve the
            next page. If this field is set, it means there is another
            page available. If it is not set, it means no other pages
            are available.
    """

    @property
    def raw_page(self):
        return self

    conversations: MutableSequence[resources.Conversation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Conversation,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetConversationRequest(proto.Message):
    r"""The request to get a conversation.

    Attributes:
        name (str):
            Required. The name of the conversation to
            get.
        view (google.cloud.contact_center_insights_v1.types.ConversationView):
            The level of details of the conversation. Default is
            ``FULL``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "ConversationView" = proto.Field(
        proto.ENUM,
        number=2,
        enum="ConversationView",
    )


class UpdateConversationRequest(proto.Message):
    r"""The request to update a conversation.

    Attributes:
        conversation (google.cloud.contact_center_insights_v1.types.Conversation):
            Required. The new values for the
            conversation.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    conversation: resources.Conversation = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Conversation,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteConversationRequest(proto.Message):
    r"""The request to delete a conversation.

    Attributes:
        name (str):
            Required. The name of the conversation to
            delete.
        force (bool):
            If set to true, all of this conversation's
            analyses will also be deleted. Otherwise, the
            request will only succeed if the conversation
            has no analyses.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class IngestConversationsRequest(proto.Message):
    r"""The request to ingest conversations.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source (google.cloud.contact_center_insights_v1.types.IngestConversationsRequest.GcsSource):
            A cloud storage bucket source.

            This field is a member of `oneof`_ ``source``.
        transcript_object_config (google.cloud.contact_center_insights_v1.types.IngestConversationsRequest.TranscriptObjectConfig):
            Configuration for when ``source`` contains conversation
            transcripts.

            This field is a member of `oneof`_ ``object_config``.
        parent (str):
            Required. The parent resource for new
            conversations.
        conversation_config (google.cloud.contact_center_insights_v1.types.IngestConversationsRequest.ConversationConfig):
            Configuration that applies to all
            conversations.
    """

    class GcsSource(proto.Message):
        r"""Configuration for Cloud Storage bucket sources.

        Attributes:
            bucket_uri (str):
                Required. The Cloud Storage bucket containing
                source objects.
        """

        bucket_uri: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class TranscriptObjectConfig(proto.Message):
        r"""Configuration for processing transcript objects.

        Attributes:
            medium (google.cloud.contact_center_insights_v1.types.Conversation.Medium):
                Required. The medium transcript objects
                represent.
        """

        medium: resources.Conversation.Medium = proto.Field(
            proto.ENUM,
            number=1,
            enum=resources.Conversation.Medium,
        )

    class ConversationConfig(proto.Message):
        r"""Configuration that applies to all conversations.

        Attributes:
            agent_id (str):
                An opaque, user-specified string representing
                the human agent who handled the conversations.
        """

        agent_id: str = proto.Field(
            proto.STRING,
            number=1,
        )

    gcs_source: GcsSource = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message=GcsSource,
    )
    transcript_object_config: TranscriptObjectConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="object_config",
        message=TranscriptObjectConfig,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation_config: ConversationConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ConversationConfig,
    )


class IngestConversationsMetadata(proto.Message):
    r"""The metadata for an IngestConversations operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.IngestConversationsRequest):
            Output only. The original request for ingest.
        partial_errors (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Partial errors during ingest
            operation that might cause the operation output
            to be incomplete.
        ingest_conversations_stats (google.cloud.contact_center_insights_v1.types.IngestConversationsMetadata.IngestConversationsStats):
            Output only. Statistics for
            IngestConversations operation.
    """

    class IngestConversationsStats(proto.Message):
        r"""Statistics for IngestConversations operation.

        Attributes:
            processed_object_count (int):
                Output only. The number of objects processed
                during the ingest operation.
            duplicates_skipped_count (int):
                Output only. The number of objects skipped
                because another conversation with the same
                transcript uri had already been ingested.
            successful_ingest_count (int):
                Output only. The number of new conversations
                added during this ingest operation.
            failed_ingest_count (int):
                Output only. The number of objects which were unable to be
                ingested due to errors. The errors are populated in the
                partial_errors field.
        """

        processed_object_count: int = proto.Field(
            proto.INT32,
            number=1,
        )
        duplicates_skipped_count: int = proto.Field(
            proto.INT32,
            number=2,
        )
        successful_ingest_count: int = proto.Field(
            proto.INT32,
            number=3,
        )
        failed_ingest_count: int = proto.Field(
            proto.INT32,
            number=4,
        )

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "IngestConversationsRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="IngestConversationsRequest",
    )
    partial_errors: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )
    ingest_conversations_stats: IngestConversationsStats = proto.Field(
        proto.MESSAGE,
        number=5,
        message=IngestConversationsStats,
    )


class IngestConversationsResponse(proto.Message):
    r"""The response to an IngestConversations operation."""


class CreateAnalysisRequest(proto.Message):
    r"""The request to create an analysis.

    Attributes:
        parent (str):
            Required. The parent resource of the
            analysis.
        analysis (google.cloud.contact_center_insights_v1.types.Analysis):
            Required. The analysis to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    analysis: resources.Analysis = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Analysis,
    )


class ListAnalysesRequest(proto.Message):
    r"""The request to list analyses.

    Attributes:
        parent (str):
            Required. The parent resource of the
            analyses.
        page_size (int):
            The maximum number of analyses to return in the response. If
            this value is zero, the service will select a default size.
            A call might return fewer objects than requested. A
            non-empty ``next_page_token`` in the response indicates that
            more data is available.
        page_token (str):
            The value returned by the last ``ListAnalysesResponse``;
            indicates that this is a continuation of a prior
            ``ListAnalyses`` call and the system should return the next
            page of data.
        filter (str):
            A filter to reduce results to a specific
            subset. Useful for querying conversations with
            specific properties.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListAnalysesResponse(proto.Message):
    r"""The response to list analyses.

    Attributes:
        analyses (MutableSequence[google.cloud.contact_center_insights_v1.types.Analysis]):
            The analyses that match the request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    analyses: MutableSequence[resources.Analysis] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Analysis,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetAnalysisRequest(proto.Message):
    r"""The request to get an analysis.

    Attributes:
        name (str):
            Required. The name of the analysis to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteAnalysisRequest(proto.Message):
    r"""The request to delete an analysis.

    Attributes:
        name (str):
            Required. The name of the analysis to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class BulkAnalyzeConversationsRequest(proto.Message):
    r"""The request to analyze conversations in bulk.

    Attributes:
        parent (str):
            Required. The parent resource to create
            analyses in.
        filter (str):
            Required. Filter used to select the subset of
            conversations to analyze.
        analysis_percentage (float):
            Required. Percentage of selected conversation to analyze,
            between [0, 100].
        annotator_selector (google.cloud.contact_center_insights_v1.types.AnnotatorSelector):
            To select the annotators to run and the
            phrase matchers to use (if any). If not
            specified, all annotators will be run.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    analysis_percentage: float = proto.Field(
        proto.FLOAT,
        number=3,
    )
    annotator_selector: resources.AnnotatorSelector = proto.Field(
        proto.MESSAGE,
        number=8,
        message=resources.AnnotatorSelector,
    )


class BulkAnalyzeConversationsMetadata(proto.Message):
    r"""The metadata for a bulk analyze conversations operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        request (google.cloud.contact_center_insights_v1.types.BulkAnalyzeConversationsRequest):
            The original request for bulk analyze.
        completed_analyses_count (int):
            The number of requested analyses that have
            completed successfully so far.
        failed_analyses_count (int):
            The number of requested analyses that have
            failed so far.
        total_requested_analyses_count (int):
            Total number of analyses requested. Computed by the number
            of conversations returned by ``filter`` multiplied by
            ``analysis_percentage`` in the request.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "BulkAnalyzeConversationsRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BulkAnalyzeConversationsRequest",
    )
    completed_analyses_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    failed_analyses_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    total_requested_analyses_count: int = proto.Field(
        proto.INT32,
        number=6,
    )


class BulkAnalyzeConversationsResponse(proto.Message):
    r"""The response for a bulk analyze conversations operation.

    Attributes:
        successful_analysis_count (int):
            Count of successful analyses.
        failed_analysis_count (int):
            Count of failed analyses.
    """

    successful_analysis_count: int = proto.Field(
        proto.INT32,
        number=1,
    )
    failed_analysis_count: int = proto.Field(
        proto.INT32,
        number=2,
    )


class ExportInsightsDataRequest(proto.Message):
    r"""The request to export insights.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        big_query_destination (google.cloud.contact_center_insights_v1.types.ExportInsightsDataRequest.BigQueryDestination):
            Specified if sink is a BigQuery table.

            This field is a member of `oneof`_ ``destination``.
        parent (str):
            Required. The parent resource to export data
            from.
        filter (str):
            A filter to reduce results to a specific
            subset. Useful for exporting conversations with
            specific properties.
        kms_key (str):
            A fully qualified KMS key name for BigQuery
            tables protected by CMEK. Format:
            projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}/cryptoKeyVersions/{version}
        write_disposition (google.cloud.contact_center_insights_v1.types.ExportInsightsDataRequest.WriteDisposition):
            Options for what to do if the destination
            table already exists.
    """

    class WriteDisposition(proto.Enum):
        r"""Specifies the action that occurs if the destination table
        already exists.

        Values:
            WRITE_DISPOSITION_UNSPECIFIED (0):
                Write disposition is not specified. Defaults to
                WRITE_TRUNCATE.
            WRITE_TRUNCATE (1):
                If the table already exists, BigQuery will
                overwrite the table data and use the schema from
                the load.
            WRITE_APPEND (2):
                If the table already exists, BigQuery will
                append data to the table.
        """
        WRITE_DISPOSITION_UNSPECIFIED = 0
        WRITE_TRUNCATE = 1
        WRITE_APPEND = 2

    class BigQueryDestination(proto.Message):
        r"""A BigQuery Table Reference.

        Attributes:
            project_id (str):
                A project ID or number. If specified, then
                export will attempt to write data to this
                project instead of the resource project.
                Otherwise, the resource project will be used.
            dataset (str):
                Required. The name of the BigQuery dataset that the snapshot
                result should be exported to. If this dataset does not
                exist, the export call returns an INVALID_ARGUMENT error.
            table (str):
                The BigQuery table name to which the insights data should be
                written. If this table does not exist, the export call
                returns an INVALID_ARGUMENT error.
        """

        project_id: str = proto.Field(
            proto.STRING,
            number=3,
        )
        dataset: str = proto.Field(
            proto.STRING,
            number=1,
        )
        table: str = proto.Field(
            proto.STRING,
            number=2,
        )

    big_query_destination: BigQueryDestination = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="destination",
        message=BigQueryDestination,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )
    kms_key: str = proto.Field(
        proto.STRING,
        number=4,
    )
    write_disposition: WriteDisposition = proto.Field(
        proto.ENUM,
        number=5,
        enum=WriteDisposition,
    )


class ExportInsightsDataMetadata(proto.Message):
    r"""Metadata for an export insights operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.ExportInsightsDataRequest):
            The original request for export.
        partial_errors (MutableSequence[google.rpc.status_pb2.Status]):
            Partial errors during export operation that
            might cause the operation output to be
            incomplete.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "ExportInsightsDataRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ExportInsightsDataRequest",
    )
    partial_errors: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )


class ExportInsightsDataResponse(proto.Message):
    r"""Response for an export insights operation."""


class CreateIssueModelRequest(proto.Message):
    r"""The request to create an issue model.

    Attributes:
        parent (str):
            Required. The parent resource of the issue
            model.
        issue_model (google.cloud.contact_center_insights_v1.types.IssueModel):
            Required. The issue model to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    issue_model: resources.IssueModel = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.IssueModel,
    )


class CreateIssueModelMetadata(proto.Message):
    r"""Metadata for creating an issue model.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.CreateIssueModelRequest):
            The original request for creation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "CreateIssueModelRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="CreateIssueModelRequest",
    )


class UpdateIssueModelRequest(proto.Message):
    r"""The request to update an issue model.

    Attributes:
        issue_model (google.cloud.contact_center_insights_v1.types.IssueModel):
            Required. The new values for the issue model.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    issue_model: resources.IssueModel = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.IssueModel,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListIssueModelsRequest(proto.Message):
    r"""Request to list issue models.

    Attributes:
        parent (str):
            Required. The parent resource of the issue
            model.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListIssueModelsResponse(proto.Message):
    r"""The response of listing issue models.

    Attributes:
        issue_models (MutableSequence[google.cloud.contact_center_insights_v1.types.IssueModel]):
            The issue models that match the request.
    """

    issue_models: MutableSequence[resources.IssueModel] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.IssueModel,
    )


class GetIssueModelRequest(proto.Message):
    r"""The request to get an issue model.

    Attributes:
        name (str):
            Required. The name of the issue model to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteIssueModelRequest(proto.Message):
    r"""The request to delete an issue model.

    Attributes:
        name (str):
            Required. The name of the issue model to
            delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteIssueModelMetadata(proto.Message):
    r"""Metadata for deleting an issue model.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.DeleteIssueModelRequest):
            The original request for deletion.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "DeleteIssueModelRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DeleteIssueModelRequest",
    )


class DeployIssueModelRequest(proto.Message):
    r"""The request to deploy an issue model.

    Attributes:
        name (str):
            Required. The issue model to deploy.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeployIssueModelResponse(proto.Message):
    r"""The response to deploy an issue model."""


class DeployIssueModelMetadata(proto.Message):
    r"""Metadata for deploying an issue model.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.DeployIssueModelRequest):
            The original request for deployment.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "DeployIssueModelRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DeployIssueModelRequest",
    )


class UndeployIssueModelRequest(proto.Message):
    r"""The request to undeploy an issue model.

    Attributes:
        name (str):
            Required. The issue model to undeploy.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeployIssueModelResponse(proto.Message):
    r"""The response to undeploy an issue model."""


class UndeployIssueModelMetadata(proto.Message):
    r"""Metadata for undeploying an issue model.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        request (google.cloud.contact_center_insights_v1.types.UndeployIssueModelRequest):
            The original request for undeployment.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    request: "UndeployIssueModelRequest" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="UndeployIssueModelRequest",
    )


class GetIssueRequest(proto.Message):
    r"""The request to get an issue.

    Attributes:
        name (str):
            Required. The name of the issue to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListIssuesRequest(proto.Message):
    r"""Request to list issues.

    Attributes:
        parent (str):
            Required. The parent resource of the issue.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListIssuesResponse(proto.Message):
    r"""The response of listing issues.

    Attributes:
        issues (MutableSequence[google.cloud.contact_center_insights_v1.types.Issue]):
            The issues that match the request.
    """

    issues: MutableSequence[resources.Issue] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Issue,
    )


class UpdateIssueRequest(proto.Message):
    r"""The request to update an issue.

    Attributes:
        issue (google.cloud.contact_center_insights_v1.types.Issue):
            Required. The new values for the issue.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    issue: resources.Issue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Issue,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteIssueRequest(proto.Message):
    r"""The request to delete an issue.

    Attributes:
        name (str):
            Required. The name of the issue to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CalculateIssueModelStatsRequest(proto.Message):
    r"""Request to get statistics of an issue model.

    Attributes:
        issue_model (str):
            Required. The resource name of the issue
            model to query against.
    """

    issue_model: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CalculateIssueModelStatsResponse(proto.Message):
    r"""Response of querying an issue model's statistics.

    Attributes:
        current_stats (google.cloud.contact_center_insights_v1.types.IssueModelLabelStats):
            The latest label statistics for the queried
            issue model. Includes results on both training
            data and data labeled after deployment.
    """

    current_stats: resources.IssueModelLabelStats = proto.Field(
        proto.MESSAGE,
        number=4,
        message=resources.IssueModelLabelStats,
    )


class CreatePhraseMatcherRequest(proto.Message):
    r"""Request to create a phrase matcher.

    Attributes:
        parent (str):
            Required. The parent resource of the phrase matcher.
            Required. The location to create a phrase matcher for.
            Format: ``projects/<Project ID>/locations/<Location ID>`` or
            ``projects/<Project Number>/locations/<Location ID>``
        phrase_matcher (google.cloud.contact_center_insights_v1.types.PhraseMatcher):
            Required. The phrase matcher resource to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phrase_matcher: resources.PhraseMatcher = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.PhraseMatcher,
    )


class ListPhraseMatchersRequest(proto.Message):
    r"""Request to list phrase matchers.

    Attributes:
        parent (str):
            Required. The parent resource of the phrase
            matcher.
        page_size (int):
            The maximum number of phrase matchers to return in the
            response. If this value is zero, the service will select a
            default size. A call might return fewer objects than
            requested. A non-empty ``next_page_token`` in the response
            indicates that more data is available.
        page_token (str):
            The value returned by the last
            ``ListPhraseMatchersResponse``. This value indicates that
            this is a continuation of a prior ``ListPhraseMatchers``
            call and that the system should return the next page of
            data.
        filter (str):
            A filter to reduce results to a specific
            subset. Useful for querying phrase matchers with
            specific properties.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListPhraseMatchersResponse(proto.Message):
    r"""The response of listing phrase matchers.

    Attributes:
        phrase_matchers (MutableSequence[google.cloud.contact_center_insights_v1.types.PhraseMatcher]):
            The phrase matchers that match the request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    phrase_matchers: MutableSequence[resources.PhraseMatcher] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.PhraseMatcher,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPhraseMatcherRequest(proto.Message):
    r"""The request to get a a phrase matcher.

    Attributes:
        name (str):
            Required. The name of the phrase matcher to
            get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeletePhraseMatcherRequest(proto.Message):
    r"""The request to delete a phrase matcher.

    Attributes:
        name (str):
            Required. The name of the phrase matcher to
            delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdatePhraseMatcherRequest(proto.Message):
    r"""The request to update a phrase matcher.

    Attributes:
        phrase_matcher (google.cloud.contact_center_insights_v1.types.PhraseMatcher):
            Required. The new values for the phrase
            matcher.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    phrase_matcher: resources.PhraseMatcher = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.PhraseMatcher,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetSettingsRequest(proto.Message):
    r"""The request to get project-level settings.

    Attributes:
        name (str):
            Required. The name of the settings resource
            to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateSettingsRequest(proto.Message):
    r"""The request to update project-level settings.

    Attributes:
        settings (google.cloud.contact_center_insights_v1.types.Settings):
            Required. The new settings values.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated.
    """

    settings: resources.Settings = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Settings,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class CreateViewRequest(proto.Message):
    r"""The request to create a view.

    Attributes:
        parent (str):
            Required. The parent resource of the view. Required. The
            location to create a view for. Format:
            ``projects/<Project ID>/locations/<Location ID>`` or
            ``projects/<Project Number>/locations/<Location ID>``
        view (google.cloud.contact_center_insights_v1.types.View):
            Required. The view resource to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: resources.View = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.View,
    )


class GetViewRequest(proto.Message):
    r"""The request to get a view.

    Attributes:
        name (str):
            Required. The name of the view to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListViewsRequest(proto.Message):
    r"""The request to list views.

    Attributes:
        parent (str):
            Required. The parent resource of the views.
        page_size (int):
            The maximum number of views to return in the response. If
            this value is zero, the service will select a default size.
            A call may return fewer objects than requested. A non-empty
            ``next_page_token`` in the response indicates that more data
            is available.
        page_token (str):
            The value returned by the last ``ListViewsResponse``;
            indicates that this is a continuation of a prior
            ``ListViews`` call and the system should return the next
            page of data.
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


class ListViewsResponse(proto.Message):
    r"""The response of listing views.

    Attributes:
        views (MutableSequence[google.cloud.contact_center_insights_v1.types.View]):
            The views that match the request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    views: MutableSequence[resources.View] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.View,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateViewRequest(proto.Message):
    r"""The request to update a view.

    Attributes:
        view (google.cloud.contact_center_insights_v1.types.View):
            Required. The new view.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    view: resources.View = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.View,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteViewRequest(proto.Message):
    r"""The request to delete a view.

    Attributes:
        name (str):
            Required. The name of the view to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
