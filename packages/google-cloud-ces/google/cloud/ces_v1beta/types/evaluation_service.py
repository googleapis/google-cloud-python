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

import google.protobuf.duration_pb2 as duration_pb2  # type: ignore
import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore
import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.ces_v1beta.types import conversation as gcc_conversation
from google.cloud.ces_v1beta.types import evaluation as gcc_evaluation

__protobuf__ = proto.module(
    package="google.cloud.ces.v1beta",
    manifest={
        "RunEvaluationResponse",
        "RunEvaluationOperationMetadata",
        "GenerateEvaluationOperationMetadata",
        "DeleteEvaluationRunOperationMetadata",
        "CreateEvaluationRequest",
        "GenerateEvaluationRequest",
        "ImportEvaluationsRequest",
        "ImportEvaluationsResponse",
        "ImportEvaluationsOperationMetadata",
        "CreateEvaluationDatasetRequest",
        "UpdateEvaluationRequest",
        "UpdateEvaluationDatasetRequest",
        "DeleteEvaluationRequest",
        "DeleteEvaluationResultRequest",
        "DeleteEvaluationDatasetRequest",
        "DeleteEvaluationRunRequest",
        "GetEvaluationRequest",
        "GetEvaluationResultRequest",
        "GetEvaluationDatasetRequest",
        "GetEvaluationRunRequest",
        "ListEvaluationsRequest",
        "ListEvaluationResultsRequest",
        "ListEvaluationDatasetsRequest",
        "ListEvaluationRunsRequest",
        "ListEvaluationsResponse",
        "ListEvaluationResultsResponse",
        "ListEvaluationDatasetsResponse",
        "ListEvaluationRunsResponse",
        "CreateScheduledEvaluationRunRequest",
        "GetScheduledEvaluationRunRequest",
        "ListScheduledEvaluationRunsRequest",
        "ListScheduledEvaluationRunsResponse",
        "UpdateScheduledEvaluationRunRequest",
        "DeleteScheduledEvaluationRunRequest",
        "TestPersonaVoiceRequest",
        "UploadEvaluationAudioRequest",
        "UploadEvaluationAudioResponse",
        "TestPersonaVoiceResponse",
        "CreateEvaluationExpectationRequest",
        "UpdateEvaluationExpectationRequest",
        "DeleteEvaluationExpectationRequest",
        "GetEvaluationExpectationRequest",
        "ListEvaluationExpectationsRequest",
        "ListEvaluationExpectationsResponse",
    },
)


class RunEvaluationResponse(proto.Message):
    r"""Response message for
    [EvaluationService.RunEvaluation][google.cloud.ces.v1beta.EvaluationService.RunEvaluation].

    Attributes:
        evaluation_run (str):
            The name of the evaluation run that was created. Format:
            ``projects/{project}/locations/{location}/apps/{app}/evaluationRuns/{evaluation_run}``
    """

    evaluation_run: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RunEvaluationOperationMetadata(proto.Message):
    r"""Operation metadata for
    [EvaluationService.RunEvaluation][google.cloud.ces.v1beta.EvaluationService.RunEvaluation]

    Attributes:
        evaluations (MutableSequence[str]):
            Output only. The list of evaluations that were run. Format:
            ``projects/{project}/locations/{location}/apps/{app}/evaluations/{evaluation}``
        evaluation_run (str):
            Output only. The evaluation run that was created. Format:
            ``projects/{project}/locations/{location}/apps/{app}/evaluationRuns/{evaluation_run}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation
            completed.
        verb (str):
            Output only. The verb of the operation.
        cancel_requested (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have
            [google.longrunning.Operation.error][google.longrunning.Operation.error]
            value with a
            [google.rpc.Status.code][google.rpc.Status.code] of ``1``,
            corresponding to ``Code.CANCELLED``.
    """

    evaluations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    evaluation_run: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=5,
    )
    cancel_requested: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class GenerateEvaluationOperationMetadata(proto.Message):
    r"""Operation metadata for
    [EvaluationService.GenerateEvaluation][google.cloud.ces.v1beta.EvaluationService.GenerateEvaluation].

    """


class DeleteEvaluationRunOperationMetadata(proto.Message):
    r"""Operation metadata for
    [EvaluationService.DeleteEvaluationRun][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluationRun].

    """


class CreateEvaluationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.CreateEvaluation][google.cloud.ces.v1beta.EvaluationService.CreateEvaluation].

    Attributes:
        parent (str):
            Required. The app to create the evaluation for. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        evaluation_id (str):
            Optional. The ID to use for the evaluation,
            which will become the final component of the
            evaluation's resource name. If not provided, a
            unique ID will be automatically assigned for the
            evaluation.
        evaluation (google.cloud.ces_v1beta.types.Evaluation):
            Required. The evaluation to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    evaluation_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    evaluation: gcc_evaluation.Evaluation = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcc_evaluation.Evaluation,
    )


class GenerateEvaluationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GenerateEvaluation][google.cloud.ces.v1beta.EvaluationService.GenerateEvaluation].

    Attributes:
        conversation (str):
            Required. The conversation to create the golden evaluation
            for. Format:
            ``projects/{project}/locations/{location}/apps/{app}/conversations/{conversation}``
        source (google.cloud.ces_v1beta.types.Conversation.Source):
            Optional. Indicate the source of the
            conversation. If not set, all sources will be
            searched.
    """

    conversation: str = proto.Field(
        proto.STRING,
        number=1,
    )
    source: gcc_conversation.Conversation.Source = proto.Field(
        proto.ENUM,
        number=2,
        enum=gcc_conversation.Conversation.Source,
    )


class ImportEvaluationsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ImportEvaluations][google.cloud.ces.v1beta.EvaluationService.ImportEvaluations].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        conversation_list (google.cloud.ces_v1beta.types.ImportEvaluationsRequest.ConversationList):
            The conversations to import the evaluations
            from.

            This field is a member of `oneof`_ ``source``.
        gcs_uri (str):
            The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI from
            which to import evaluations. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``.

            This field is a member of `oneof`_ ``source``.
        csv_content (bytes):
            Raw bytes representing the csv file with the
            evaluations structure.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. The app to import the evaluations into. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        import_options (google.cloud.ces_v1beta.types.ImportEvaluationsRequest.ImportOptions):
            Optional. Options governing the import
            process for the evaluations.
    """

    class ConversationList(proto.Message):
        r"""A list of conversation resource names.

        Attributes:
            conversations (MutableSequence[str]):
                Optional. Conversation resource names.
        """

        conversations: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class ImportOptions(proto.Message):
        r"""Configuration options for the evaluation import process.
        These options control how the import behaves, particularly when
        conflicts arise with existing evaluations data.

        Attributes:
            conflict_resolution_strategy (google.cloud.ces_v1beta.types.ImportEvaluationsRequest.ImportOptions.ConflictResolutionStrategy):
                Optional. The strategy to use when resolving
                conflicts during import.
        """

        class ConflictResolutionStrategy(proto.Enum):
            r"""Defines the strategy for handling conflicts when an
            evaluation with the same evaluation ID already exists in the
            app.

            Values:
                CONFLICT_RESOLUTION_STRATEGY_UNSPECIFIED (0):
                    The conflict resolution strategy is
                    unspecified.
                OVERWRITE (1):
                    Overwrite the existing evaluation with the
                    new one.
                SKIP (2):
                    Keep the existing evaluation and skip the new
                    one.
                DUPLICATE (3):
                    Keep the existing evaluation and duplicate
                    the new one as a new evaluation.
            """

            CONFLICT_RESOLUTION_STRATEGY_UNSPECIFIED = 0
            OVERWRITE = 1
            SKIP = 2
            DUPLICATE = 3

        conflict_resolution_strategy: "ImportEvaluationsRequest.ImportOptions.ConflictResolutionStrategy" = proto.Field(
            proto.ENUM,
            number=1,
            enum="ImportEvaluationsRequest.ImportOptions.ConflictResolutionStrategy",
        )

    conversation_list: ConversationList = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message=ConversationList,
    )
    gcs_uri: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="source",
    )
    csv_content: bytes = proto.Field(
        proto.BYTES,
        number=4,
        oneof="source",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    import_options: ImportOptions = proto.Field(
        proto.MESSAGE,
        number=5,
        message=ImportOptions,
    )


class ImportEvaluationsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ImportEvaluations][google.cloud.ces.v1beta.EvaluationService.ImportEvaluations].

    Attributes:
        evaluations (MutableSequence[google.cloud.ces_v1beta.types.Evaluation]):
            The list of evaluations that were imported
            into the app.
        error_messages (MutableSequence[str]):
            Optional. A list of error messages associated
            with evaluations that failed to be imported.
        import_failure_count (int):
            The number of evaluations that were not
            imported due to errors.
    """

    evaluations: MutableSequence[gcc_evaluation.Evaluation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.Evaluation,
    )
    error_messages: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    import_failure_count: int = proto.Field(
        proto.INT32,
        number=3,
    )


class ImportEvaluationsOperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation for
    [EvaluationService.ImportEvaluations][google.cloud.ces.v1beta.EvaluationService.ImportEvaluations].

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
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
    status_message: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateEvaluationDatasetRequest(proto.Message):
    r"""Request message for
    [EvaluationService.CreateEvaluationDataset][google.cloud.ces.v1beta.EvaluationService.CreateEvaluationDataset].

    Attributes:
        parent (str):
            Required. The app to create the evaluation for. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        evaluation_dataset_id (str):
            Optional. The ID to use for the evaluation
            dataset, which will become the final component
            of the evaluation dataset's resource name. If
            not provided, a unique ID will be automatically
            assigned for the evaluation.
        evaluation_dataset (google.cloud.ces_v1beta.types.EvaluationDataset):
            Required. The evaluation dataset to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    evaluation_dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    evaluation_dataset: gcc_evaluation.EvaluationDataset = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcc_evaluation.EvaluationDataset,
    )


class UpdateEvaluationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.UpdateEvaluation][google.cloud.ces.v1beta.EvaluationService.UpdateEvaluation].

    Attributes:
        evaluation (google.cloud.ces_v1beta.types.Evaluation):
            Required. The evaluation to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to control which
            fields get updated. If the mask is not present,
            all fields will be updated.
    """

    evaluation: gcc_evaluation.Evaluation = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.Evaluation,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class UpdateEvaluationDatasetRequest(proto.Message):
    r"""Request message for
    [EvaluationService.UpdateEvaluationDataset][google.cloud.ces.v1beta.EvaluationService.UpdateEvaluationDataset].

    Attributes:
        evaluation_dataset (google.cloud.ces_v1beta.types.EvaluationDataset):
            Required. The evaluation dataset to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to control which
            fields get updated. If the mask is not present,
            all fields will be updated.
    """

    evaluation_dataset: gcc_evaluation.EvaluationDataset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.EvaluationDataset,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteEvaluationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteEvaluation][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluation].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            to delete.
        force (bool):
            Optional. Indicates whether to forcefully delete the
            evaluation, even if it is still referenced by evaluation
            datasets.

            - If ``force = false``, the deletion will fail if any
              datasets still reference the evaluation.
            - If ``force = true``, all existing references from datasets
              will be removed and the evaluation will be deleted.
        etag (str):
            Optional. The current etag of the evaluation.
            If an etag is not provided, the deletion will
            overwrite any concurrent changes. If an etag is
            provided and does not match the current etag of
            the evaluation, deletion will be blocked and an
            ABORTED error will be returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteEvaluationResultRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteEvaluationResult][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluationResult].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            result to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteEvaluationDatasetRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteEvaluationDataset][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluationDataset].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            dataset to delete.
        etag (str):
            Optional. The current etag of the evaluation
            dataset. If an etag is not provided, the
            deletion will overwrite any concurrent changes.
            If an etag is provided and does not match the
            current etag of the evaluation dataset, deletion
            will be blocked and an ABORTED error will be
            returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteEvaluationRun][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluationRun].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            run to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetEvaluationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetEvaluation][google.cloud.ces.v1beta.EvaluationService.GetEvaluation].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetEvaluationResultRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetEvaluationResult][google.cloud.ces.v1beta.EvaluationService.GetEvaluationResult].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            result to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetEvaluationDatasetRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetEvaluationDataset][google.cloud.ces.v1beta.EvaluationService.GetEvaluationDataset].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            dataset to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetEvaluationRun][google.cloud.ces.v1beta.EvaluationService.GetEvaluationRun].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            run to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListEvaluationsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListEvaluations][google.cloud.ces.v1beta.EvaluationService.ListEvaluations].

    Attributes:
        parent (str):
            Required. The resource name of the app to
            list evaluations from.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListEvaluationsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListEvaluations][google.cloud.ces.v1beta.EvaluationService.ListEvaluations]
            call.
        filter (str):
            Optional. Deprecated: Use evaluation_filter and
            evaluation_run_filter instead.
        evaluation_filter (str):
            Optional. Filter to be applied on the evaluation when
            listing the evaluations. See https://google.aip.dev/160 for
            more details. Supported fields: evaluation_datasets
        evaluation_run_filter (str):
            Optional. Filter string for fields on the associated
            EvaluationRun resources. See https://google.aip.dev/160 for
            more details. Supported fields: create_time, initiated_by,
            app_version_display_name
        order_by (str):
            Optional. Field to sort by. Only "name" and "create_time",
            and "update_time" are supported. Time fields are ordered in
            descending order, and the name field is ordered in ascending
            order. If not included, "update_time" will be the default.
            See https://google.aip.dev/132#ordering for more details.
        last_ten_results (bool):
            Optional. Whether to include the last 10
            evaluation results for each evaluation in the
            response.
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
    evaluation_filter: str = proto.Field(
        proto.STRING,
        number=7,
    )
    evaluation_run_filter: str = proto.Field(
        proto.STRING,
        number=8,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    last_ten_results: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class ListEvaluationResultsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListEvaluationResults][google.cloud.ces.v1beta.EvaluationService.ListEvaluationResults].

    Attributes:
        parent (str):
            Required. The resource name of the evaluation to list
            evaluation results from. To filter by evaluation run, use
            ``-`` as the evaluation ID and specify the evaluation run ID
            in the filter. For example:
            ``projects/{project}/locations/{location}/apps/{app}/evaluations/-``
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListEvaluationResultsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListEvaluationResults][google.cloud.ces.v1beta.EvaluationService.ListEvaluationResults]
            call.
        filter (str):
            Optional. Filter to be applied when listing
            the evaluation results. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. Only "name" and "create_time",
            and "update_time" are supported. Time fields are ordered in
            descending order, and the name field is ordered in ascending
            order. If not included, "update_time" will be the default.
            See https://google.aip.dev/132#ordering for more details.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListEvaluationDatasetsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListEvaluationDatasets][google.cloud.ces.v1beta.EvaluationService.ListEvaluationDatasets].

    Attributes:
        parent (str):
            Required. The resource name of the app to
            list evaluation datasets from.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListEvaluationDatasetsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListEvaluationDatasets][google.cloud.ces.v1beta.EvaluationService.ListEvaluationDatasets]
            call.
        filter (str):
            Optional. Filter to be applied when listing
            the evaluation datasets. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. Only "name" and "create_time",
            and "update_time" are supported. Time fields are ordered in
            descending order, and the name field is ordered in ascending
            order. If not included, "update_time" will be the default.
            See https://google.aip.dev/132#ordering for more details.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListEvaluationRunsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListEvaluationRuns].

    Attributes:
        parent (str):
            Required. The resource name of the app to
            list evaluation runs from.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListEvaluationRunsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListEvaluationRuns]
            call.
        filter (str):
            Optional. Filter to be applied when listing
            the evaluation runs. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. Only "name" and "create_time",
            and "update_time" are supported. Time fields are ordered in
            descending order, and the name field is ordered in ascending
            order. If not included, "update_time" will be the default.
            See https://google.aip.dev/132#ordering for more details.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListEvaluationsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListEvaluations][google.cloud.ces.v1beta.EvaluationService.ListEvaluations].

    Attributes:
        evaluations (MutableSequence[google.cloud.ces_v1beta.types.Evaluation]):
            The list of evaluations.
        next_page_token (str):
            A token that can be sent as
            [ListEvaluationsRequest.page_token][google.cloud.ces.v1beta.ListEvaluationsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    evaluations: MutableSequence[gcc_evaluation.Evaluation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.Evaluation,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEvaluationResultsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListEvaluationResults][google.cloud.ces.v1beta.EvaluationService.ListEvaluationResults].

    Attributes:
        evaluation_results (MutableSequence[google.cloud.ces_v1beta.types.EvaluationResult]):
            The list of evaluation results.
        next_page_token (str):
            A token that can be sent as
            [ListEvaluationResultsRequest.page_token][google.cloud.ces.v1beta.ListEvaluationResultsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    evaluation_results: MutableSequence[gcc_evaluation.EvaluationResult] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=gcc_evaluation.EvaluationResult,
        )
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEvaluationDatasetsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListEvaluationDatasets][google.cloud.ces.v1beta.EvaluationService.ListEvaluationDatasets].

    Attributes:
        evaluation_datasets (MutableSequence[google.cloud.ces_v1beta.types.EvaluationDataset]):
            The list of evaluation datasets.
        next_page_token (str):
            A token that can be sent as
            [ListEvaluationDatasetsRequest.page_token][google.cloud.ces.v1beta.ListEvaluationDatasetsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    evaluation_datasets: MutableSequence[gcc_evaluation.EvaluationDataset] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=gcc_evaluation.EvaluationDataset,
        )
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEvaluationRunsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListEvaluationRuns].

    Attributes:
        evaluation_runs (MutableSequence[google.cloud.ces_v1beta.types.EvaluationRun]):
            The list of evaluation runs.
        next_page_token (str):
            A token that can be sent as
            [ListEvaluationRunsRequest.page_token][google.cloud.ces.v1beta.ListEvaluationRunsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    evaluation_runs: MutableSequence[gcc_evaluation.EvaluationRun] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=gcc_evaluation.EvaluationRun,
        )
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateScheduledEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.CreateScheduledEvaluationRun][google.cloud.ces.v1beta.EvaluationService.CreateScheduledEvaluationRun].

    Attributes:
        parent (str):
            Required. The app to create the scheduled evaluation run
            for. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        scheduled_evaluation_run_id (str):
            Optional. The ID to use for the scheduled
            evaluation run, which will become the final
            component of the scheduled evaluation run's
            resource name. If not provided, a unique ID will
            be automatically assigned.
        scheduled_evaluation_run (google.cloud.ces_v1beta.types.ScheduledEvaluationRun):
            Required. The scheduled evaluation run to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    scheduled_evaluation_run_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    scheduled_evaluation_run: gcc_evaluation.ScheduledEvaluationRun = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcc_evaluation.ScheduledEvaluationRun,
    )


class GetScheduledEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetScheduledEvaluationRun][google.cloud.ces.v1beta.EvaluationService.GetScheduledEvaluationRun].

    Attributes:
        name (str):
            Required. The resource name of the scheduled
            evaluation run to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListScheduledEvaluationRunsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListScheduledEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListScheduledEvaluationRuns].

    Attributes:
        parent (str):
            Required. The resource name of the app to
            list scheduled evaluation runs from.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListScheduledEvaluationRunsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListScheduledEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListScheduledEvaluationRuns]
            call.
        filter (str):
            Optional. Filter to be applied when listing the scheduled
            evaluation runs. See https://google.aip.dev/160 for more
            details. Currently supports filtering by:

            - request.evaluations:evaluation_id
            - request.evaluation_dataset:evaluation_dataset_id
        order_by (str):
            Optional. Field to sort by. Supported fields are: "name"
            (ascending), "create_time" (descending), "update_time"
            (descending), "next_scheduled_execution" (ascending), and
            "last_completed_run.create_time" (descending). If not
            included, "update_time" will be the default. See
            https://google.aip.dev/132#ordering for more details.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListScheduledEvaluationRunsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListScheduledEvaluationRuns][google.cloud.ces.v1beta.EvaluationService.ListScheduledEvaluationRuns].

    Attributes:
        scheduled_evaluation_runs (MutableSequence[google.cloud.ces_v1beta.types.ScheduledEvaluationRun]):
            The list of scheduled evaluation runs.
        next_page_token (str):
            A token that can be sent as
            [ListScheduledEvaluationRunsRequest.page_token][google.cloud.ces.v1beta.ListScheduledEvaluationRunsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    scheduled_evaluation_runs: MutableSequence[
        gcc_evaluation.ScheduledEvaluationRun
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.ScheduledEvaluationRun,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateScheduledEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.UpdateScheduledEvaluationRun][google.cloud.ces.v1beta.EvaluationService.UpdateScheduledEvaluationRun].

    Attributes:
        scheduled_evaluation_run (google.cloud.ces_v1beta.types.ScheduledEvaluationRun):
            Required. The scheduled evaluation run to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to control which
            fields get updated. If the mask is not present,
            all fields will be updated.
    """

    scheduled_evaluation_run: gcc_evaluation.ScheduledEvaluationRun = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.ScheduledEvaluationRun,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteScheduledEvaluationRunRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteScheduledEvaluationRun][google.cloud.ces.v1beta.EvaluationService.DeleteScheduledEvaluationRun].

    Attributes:
        name (str):
            Required. The resource name of the scheduled
            evaluation run to delete.
        etag (str):
            Optional. The etag of the
            ScheduledEvaluationRun. If provided, it must
            match the server's etag.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TestPersonaVoiceRequest(proto.Message):
    r"""Request message for
    [EvaluationService.TestPersonaVoice][google.cloud.ces.v1beta.EvaluationService.TestPersonaVoice].

    Attributes:
        app (str):
            Required. the resource name of the app to test the persona
            voice for. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        persona_id (str):
            Required. The persona ID to test the voice
            for. Also accepts "default".
        text (str):
            Required. The text to test the voice for.
    """

    app: str = proto.Field(
        proto.STRING,
        number=1,
    )
    persona_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    text: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UploadEvaluationAudioRequest(proto.Message):
    r"""Request message for
    [EvaluationService.UploadEvaluationAudio][google.cloud.ces.v1beta.EvaluationService.UploadEvaluationAudio].

    Attributes:
        app (str):
            Required. The resource name of the App for which to upload
            the evaluation audio. Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        audio_content (bytes):
            Required. The raw audio bytes.
            The format of the audio must be single-channel
            LINEAR16 with a sample rate of 16kHz (default
            InputAudioConfig).
    """

    app: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audio_content: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class UploadEvaluationAudioResponse(proto.Message):
    r"""Response message for
    [EvaluationService.UploadEvaluationAudio][google.cloud.ces.v1beta.EvaluationService.UploadEvaluationAudio].

    Attributes:
        audio_gcs_uri (str):
            The Google Cloud Storage URI where the uploaded audio file
            is stored. Format: ``gs://<bucket-name>/<object-name>``
        audio_transcript (str):
            The transcribed text from the audio,
            generated by Cloud Speech-to-Text.
        audio_duration (google.protobuf.duration_pb2.Duration):
            The duration of the audio.
    """

    audio_gcs_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audio_transcript: str = proto.Field(
        proto.STRING,
        number=2,
    )
    audio_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )


class TestPersonaVoiceResponse(proto.Message):
    r"""Response message for
    [EvaluationService.TestPersonaVoice][google.cloud.ces.v1beta.EvaluationService.TestPersonaVoice].

    Attributes:
        audio (bytes):
            The audio data bytes of the synthesized
            voice.
    """

    audio: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


class CreateEvaluationExpectationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.CreateEvaluationExpectation][google.cloud.ces.v1beta.EvaluationService.CreateEvaluationExpectation].

    Attributes:
        parent (str):
            Required. The app to create the evaluation expectation for.
            Format:
            ``projects/{project}/locations/{location}/apps/{app}``
        evaluation_expectation_id (str):
            Optional. The ID to use for the evaluation
            expectation, which will become the final
            component of the evaluation expectation's
            resource name. If not provided, a unique ID will
            be automatically assigned for the evaluation
            expectation.
        evaluation_expectation (google.cloud.ces_v1beta.types.EvaluationExpectation):
            Required. The evaluation expectation to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    evaluation_expectation_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    evaluation_expectation: gcc_evaluation.EvaluationExpectation = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcc_evaluation.EvaluationExpectation,
    )


class UpdateEvaluationExpectationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.UpdateEvaluationExpectation][google.cloud.ces.v1beta.EvaluationService.UpdateEvaluationExpectation].

    Attributes:
        evaluation_expectation (google.cloud.ces_v1beta.types.EvaluationExpectation):
            Required. The evaluation expectation to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to control which
            fields get updated. If the mask is not present,
            all fields will be updated.
    """

    evaluation_expectation: gcc_evaluation.EvaluationExpectation = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_evaluation.EvaluationExpectation,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteEvaluationExpectationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.DeleteEvaluationExpectation][google.cloud.ces.v1beta.EvaluationService.DeleteEvaluationExpectation].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            expectation to delete.
        etag (str):
            Optional. The current etag of the evaluation
            expectation. If an etag is not provided, the
            deletion will overwrite any concurrent changes.
            If an etag is provided and does not match the
            current etag of the evaluation expectation,
            deletion will be blocked and an ABORTED error
            will be returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEvaluationExpectationRequest(proto.Message):
    r"""Request message for
    [EvaluationService.GetEvaluationExpectation][google.cloud.ces.v1beta.EvaluationService.GetEvaluationExpectation].

    Attributes:
        name (str):
            Required. The resource name of the evaluation
            expectation to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListEvaluationExpectationsRequest(proto.Message):
    r"""Request message for
    [EvaluationService.ListEvaluationExpectations][google.cloud.ces.v1beta.EvaluationService.ListEvaluationExpectations].

    Attributes:
        parent (str):
            Required. The resource name of the app to
            list evaluation expectations from.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. The
            [next_page_token][google.cloud.ces.v1beta.ListEvaluationExpectationsResponse.next_page_token]
            value returned from a previous list
            [EvaluationService.ListEvaluationExpectations][google.cloud.ces.v1beta.EvaluationService.ListEvaluationExpectations]
            call.
        filter (str):
            Optional. Filter to be applied when listing
            the evaluation expectations. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. Only "name" and "create_time",
            and "update_time" are supported. Time fields are ordered in
            descending order, and the name field is ordered in ascending
            order. If not included, "update_time" will be the default.
            See https://google.aip.dev/132#ordering for more details.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListEvaluationExpectationsResponse(proto.Message):
    r"""Response message for
    [EvaluationService.ListEvaluationExpectations][google.cloud.ces.v1beta.EvaluationService.ListEvaluationExpectations].

    Attributes:
        evaluation_expectations (MutableSequence[google.cloud.ces_v1beta.types.EvaluationExpectation]):
            The list of evaluation expectations.
        next_page_token (str):
            A token that can be sent as
            [ListEvaluationExpectationsRequest.page_token][google.cloud.ces.v1beta.ListEvaluationExpectationsRequest.page_token]
            to retrieve the next page. Absence of this field indicates
            there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    evaluation_expectations: MutableSequence[gcc_evaluation.EvaluationExpectation] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=gcc_evaluation.EvaluationExpectation,
        )
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
