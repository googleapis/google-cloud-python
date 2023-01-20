# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.documentai_v1.types import document_schema as gcd_document_schema
from google.cloud.documentai_v1.types import document as gcd_document
from google.cloud.documentai_v1.types import document_io
from google.cloud.documentai_v1.types import operation_metadata
from google.cloud.documentai_v1.types import processor as gcd_processor
from google.cloud.documentai_v1.types import processor_type

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1",
    manifest={
        "ProcessRequest",
        "HumanReviewStatus",
        "ProcessResponse",
        "BatchProcessRequest",
        "BatchProcessResponse",
        "BatchProcessMetadata",
        "FetchProcessorTypesRequest",
        "FetchProcessorTypesResponse",
        "ListProcessorTypesRequest",
        "ListProcessorTypesResponse",
        "ListProcessorsRequest",
        "ListProcessorsResponse",
        "GetProcessorTypeRequest",
        "GetProcessorRequest",
        "GetProcessorVersionRequest",
        "ListProcessorVersionsRequest",
        "ListProcessorVersionsResponse",
        "DeleteProcessorVersionRequest",
        "DeleteProcessorVersionMetadata",
        "DeployProcessorVersionRequest",
        "DeployProcessorVersionResponse",
        "DeployProcessorVersionMetadata",
        "UndeployProcessorVersionRequest",
        "UndeployProcessorVersionResponse",
        "UndeployProcessorVersionMetadata",
        "CreateProcessorRequest",
        "DeleteProcessorRequest",
        "DeleteProcessorMetadata",
        "EnableProcessorRequest",
        "EnableProcessorResponse",
        "EnableProcessorMetadata",
        "DisableProcessorRequest",
        "DisableProcessorResponse",
        "DisableProcessorMetadata",
        "SetDefaultProcessorVersionRequest",
        "SetDefaultProcessorVersionResponse",
        "SetDefaultProcessorVersionMetadata",
        "ReviewDocumentRequest",
        "ReviewDocumentResponse",
        "ReviewDocumentOperationMetadata",
    },
)


class ProcessRequest(proto.Message):
    r"""Request message for the process document method.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inline_document (google.cloud.documentai_v1.types.Document):
            An inline document proto.

            This field is a member of `oneof`_ ``source``.
        raw_document (google.cloud.documentai_v1.types.RawDocument):
            A raw document content (bytes).

            This field is a member of `oneof`_ ``source``.
        name (str):
            Required. The resource name of the
            [Processor][google.cloud.documentai.v1.Processor] or
            [ProcessorVersion][google.cloud.documentai.v1.ProcessorVersion]
            to use for processing. If a
            [Processor][google.cloud.documentai.v1.Processor] is
            specified, the server will use its [default
            version][google.cloud.documentai.v1.Processor.default_processor_version].
            Format:
            ``projects/{project}/locations/{location}/processors/{processor}``,
            or
            ``projects/{project}/locations/{location}/processors/{processor}/processorVersions/{processorVersion}``
        skip_human_review (bool):
            Whether Human Review feature should be
            skipped for this request. Default to false.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            Specifies which fields to include in ProcessResponse's
            document. Only supports top level document and pages field
            so it must be in the form of ``{document_field_name}`` or
            ``pages.{page_field_name}``.
    """

    inline_document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="source",
        message=gcd_document.Document,
    )
    raw_document: document_io.RawDocument = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="source",
        message=document_io.RawDocument,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    skip_human_review: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    field_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=6,
        message=field_mask_pb2.FieldMask,
    )


class HumanReviewStatus(proto.Message):
    r"""The status of human review on a processed document.

    Attributes:
        state (google.cloud.documentai_v1.types.HumanReviewStatus.State):
            The state of human review on the processing
            request.
        state_message (str):
            A message providing more details about the
            human review state.
        human_review_operation (str):
            The name of the operation triggered by the processed
            document. This field is populated only when the [state] is
            [HUMAN_REVIEW_IN_PROGRESS]. It has the same response type
            and metadata as the long running operation returned by
            [ReviewDocument] method.
    """

    class State(proto.Enum):
        r"""The final state of human review on a processed document.

        Values:
            STATE_UNSPECIFIED (0):
                Human review state is unspecified. Most
                likely due to an internal error.
            SKIPPED (1):
                Human review is skipped for the document.
                This can happen because human review is not
                enabled on the processor or the processing
                request has been set to skip this document.
            VALIDATION_PASSED (2):
                Human review validation is triggered and
                passed, so no review is needed.
            IN_PROGRESS (3):
                Human review validation is triggered and the
                document is under review.
            ERROR (4):
                Some error happened during triggering human review, see the
                [state_message] for details.
        """
        STATE_UNSPECIFIED = 0
        SKIPPED = 1
        VALIDATION_PASSED = 2
        IN_PROGRESS = 3
        ERROR = 4

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    state_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    human_review_operation: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ProcessResponse(proto.Message):
    r"""Response message for the process document method.

    Attributes:
        document (google.cloud.documentai_v1.types.Document):
            The document payload, will populate fields
            based on the processor's behavior.
        human_review_status (google.cloud.documentai_v1.types.HumanReviewStatus):
            The status of human review on the processed
            document.
    """

    document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_document.Document,
    )
    human_review_status: "HumanReviewStatus" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="HumanReviewStatus",
    )


class BatchProcessRequest(proto.Message):
    r"""Request message for batch process document method.

    Attributes:
        name (str):
            Required. The resource name of
            [Processor][google.cloud.documentai.v1.Processor] or
            [ProcessorVersion][google.cloud.documentai.v1.ProcessorVersion].
            Format:
            ``projects/{project}/locations/{location}/processors/{processor}``,
            or
            ``projects/{project}/locations/{location}/processors/{processor}/processorVersions/{processorVersion}``
        input_documents (google.cloud.documentai_v1.types.BatchDocumentsInputConfig):
            The input documents for batch process.
        document_output_config (google.cloud.documentai_v1.types.DocumentOutputConfig):
            The overall output config for batch process.
        skip_human_review (bool):
            Whether Human Review feature should be
            skipped for this request. Default to false.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    input_documents: document_io.BatchDocumentsInputConfig = proto.Field(
        proto.MESSAGE,
        number=5,
        message=document_io.BatchDocumentsInputConfig,
    )
    document_output_config: document_io.DocumentOutputConfig = proto.Field(
        proto.MESSAGE,
        number=6,
        message=document_io.DocumentOutputConfig,
    )
    skip_human_review: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class BatchProcessResponse(proto.Message):
    r"""Response message for batch process document method."""


class BatchProcessMetadata(proto.Message):
    r"""The long running operation metadata for batch process method.

    Attributes:
        state (google.cloud.documentai_v1.types.BatchProcessMetadata.State):
            The state of the current batch processing.
        state_message (str):
            A message providing more details about the
            current state of processing. For example, the
            error message if the operation is failed.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The creation time of the operation.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The last update time of the operation.
        individual_process_statuses (MutableSequence[google.cloud.documentai_v1.types.BatchProcessMetadata.IndividualProcessStatus]):
            The list of response details of each
            document.
    """

    class State(proto.Enum):
        r"""Possible states of the batch processing operation.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            WAITING (1):
                Request operation is waiting for scheduling.
            RUNNING (2):
                Request is being processed.
            SUCCEEDED (3):
                The batch processing completed successfully.
            CANCELLING (4):
                The batch processing was being cancelled.
            CANCELLED (5):
                The batch processing was cancelled.
            FAILED (6):
                The batch processing has failed.
        """
        STATE_UNSPECIFIED = 0
        WAITING = 1
        RUNNING = 2
        SUCCEEDED = 3
        CANCELLING = 4
        CANCELLED = 5
        FAILED = 6

    class IndividualProcessStatus(proto.Message):
        r"""The status of a each individual document in the batch
        process.

        Attributes:
            input_gcs_source (str):
                The source of the document, same as the [input_gcs_source]
                field in the request when the batch process started. The
                batch process is started by take snapshot of that document,
                since a user can move or change that document during the
                process.
            status (google.rpc.status_pb2.Status):
                The status processing the document.
            output_gcs_destination (str):
                The output_gcs_destination (in the request as
                ``output_gcs_destination``) of the processed document if it
                was successful, otherwise empty.
            human_review_status (google.cloud.documentai_v1.types.HumanReviewStatus):
                The status of human review on the processed
                document.
        """

        input_gcs_source: str = proto.Field(
            proto.STRING,
            number=1,
        )
        status: status_pb2.Status = proto.Field(
            proto.MESSAGE,
            number=2,
            message=status_pb2.Status,
        )
        output_gcs_destination: str = proto.Field(
            proto.STRING,
            number=3,
        )
        human_review_status: "HumanReviewStatus" = proto.Field(
            proto.MESSAGE,
            number=5,
            message="HumanReviewStatus",
        )

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    state_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    individual_process_statuses: MutableSequence[
        IndividualProcessStatus
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=IndividualProcessStatus,
    )


class FetchProcessorTypesRequest(proto.Message):
    r"""Request message for fetch processor types.

    Attributes:
        parent (str):
            Required. The project of processor type to list. The
            available processor types may depend on the allow-listing on
            projects. Format:
            ``projects/{project}/locations/{location}``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchProcessorTypesResponse(proto.Message):
    r"""Response message for fetch processor types.

    Attributes:
        processor_types (MutableSequence[google.cloud.documentai_v1.types.ProcessorType]):
            The list of processor types.
    """

    processor_types: MutableSequence[
        processor_type.ProcessorType
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=processor_type.ProcessorType,
    )


class ListProcessorTypesRequest(proto.Message):
    r"""Request message for list processor types.

    Attributes:
        parent (str):
            Required. The location of processor type to list. The
            available processor types may depend on the allow-listing on
            projects. Format:
            ``projects/{project}/locations/{location}``
        page_size (int):
            The maximum number of processor types to
            return. If unspecified, at most 100 processor
            types will be returned. The maximum value is
            500; values above 500 will be coerced to 500.
        page_token (str):
            Used to retrieve the next page of results,
            empty if at the end of the list.
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


class ListProcessorTypesResponse(proto.Message):
    r"""Response message for list processor types.

    Attributes:
        processor_types (MutableSequence[google.cloud.documentai_v1.types.ProcessorType]):
            The processor types.
        next_page_token (str):
            Points to the next page, otherwise empty.
    """

    @property
    def raw_page(self):
        return self

    processor_types: MutableSequence[
        processor_type.ProcessorType
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=processor_type.ProcessorType,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListProcessorsRequest(proto.Message):
    r"""Request message for list all processors belongs to a project.

    Attributes:
        parent (str):
            Required. The parent (project and location) which owns this
            collection of Processors. Format:
            ``projects/{project}/locations/{location}``
        page_size (int):
            The maximum number of processors to return.
            If unspecified, at most 50 processors will be
            returned. The maximum value is 100; values above
            100 will be coerced to 100.
        page_token (str):
            We will return the processors sorted by
            creation time. The page token will point to the
            next processor.
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


class ListProcessorsResponse(proto.Message):
    r"""Response message for list processors.

    Attributes:
        processors (MutableSequence[google.cloud.documentai_v1.types.Processor]):
            The list of processors.
        next_page_token (str):
            Points to the next processor, otherwise
            empty.
    """

    @property
    def raw_page(self):
        return self

    processors: MutableSequence[gcd_processor.Processor] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_processor.Processor,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetProcessorTypeRequest(proto.Message):
    r"""Request message for get processor.

    Attributes:
        name (str):
            Required. The processor type resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetProcessorRequest(proto.Message):
    r"""Request message for get processor.

    Attributes:
        name (str):
            Required. The processor resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetProcessorVersionRequest(proto.Message):
    r"""Request message for get processor version.

    Attributes:
        name (str):
            Required. The processor resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListProcessorVersionsRequest(proto.Message):
    r"""Request message for list all processor versions belongs to a
    processor.

    Attributes:
        parent (str):
            Required. The parent (project, location and processor) to
            list all versions. Format:
            ``projects/{project}/locations/{location}/processors/{processor}``
        page_size (int):
            The maximum number of processor versions to
            return. If unspecified, at most 10 processor
            versions will be returned. The maximum value is
            20; values above 20 will be coerced to 20.
        page_token (str):
            We will return the processor versions sorted
            by creation time. The page token will point to
            the next processor version.
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


class ListProcessorVersionsResponse(proto.Message):
    r"""Response message for list processors.

    Attributes:
        processor_versions (MutableSequence[google.cloud.documentai_v1.types.ProcessorVersion]):
            The list of processors.
        next_page_token (str):
            Points to the next processor, otherwise
            empty.
    """

    @property
    def raw_page(self):
        return self

    processor_versions: MutableSequence[
        gcd_processor.ProcessorVersion
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_processor.ProcessorVersion,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteProcessorVersionRequest(proto.Message):
    r"""Request message for the delete processor version method.

    Attributes:
        name (str):
            Required. The processor version resource name
            to be deleted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteProcessorVersionMetadata(proto.Message):
    r"""The long running operation metadata for delete processor
    version method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class DeployProcessorVersionRequest(proto.Message):
    r"""Request message for the deploy processor version method.

    Attributes:
        name (str):
            Required. The processor version resource name
            to be deployed.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeployProcessorVersionResponse(proto.Message):
    r"""Response message for the deploy processor version method."""


class DeployProcessorVersionMetadata(proto.Message):
    r"""The long running operation metadata for deploy processor
    version method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class UndeployProcessorVersionRequest(proto.Message):
    r"""Request message for the undeploy processor version method.

    Attributes:
        name (str):
            Required. The processor version resource name
            to be undeployed.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeployProcessorVersionResponse(proto.Message):
    r"""Response message for the undeploy processor version method."""


class UndeployProcessorVersionMetadata(proto.Message):
    r"""The long running operation metadata for the undeploy
    processor version method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class CreateProcessorRequest(proto.Message):
    r"""Request message for create a processor. Notice this request
    is sent to a regionalized backend service, and if the processor
    type is not available on that region, the creation will fail.

    Attributes:
        parent (str):
            Required. The parent (project and location) under which to
            create the processor. Format:
            ``projects/{project}/locations/{location}``
        processor (google.cloud.documentai_v1.types.Processor):
            Required. The processor to be created, requires
            [processor_type] and [display_name] to be set. Also, the
            processor is under CMEK if CMEK fields are set.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    processor: gcd_processor.Processor = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_processor.Processor,
    )


class DeleteProcessorRequest(proto.Message):
    r"""Request message for the delete processor method.

    Attributes:
        name (str):
            Required. The processor resource name to be
            deleted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteProcessorMetadata(proto.Message):
    r"""The long running operation metadata for delete processor
    method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=5,
        message=operation_metadata.CommonOperationMetadata,
    )


class EnableProcessorRequest(proto.Message):
    r"""Request message for the enable processor method.

    Attributes:
        name (str):
            Required. The processor resource name to be
            enabled.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EnableProcessorResponse(proto.Message):
    r"""Response message for the enable processor method.
    Intentionally empty proto for adding fields in future.

    """


class EnableProcessorMetadata(proto.Message):
    r"""The long running operation metadata for enable processor
    method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=5,
        message=operation_metadata.CommonOperationMetadata,
    )


class DisableProcessorRequest(proto.Message):
    r"""Request message for the disable processor method.

    Attributes:
        name (str):
            Required. The processor resource name to be
            disabled.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DisableProcessorResponse(proto.Message):
    r"""Response message for the disable processor method.
    Intentionally empty proto for adding fields in future.

    """


class DisableProcessorMetadata(proto.Message):
    r"""The long running operation metadata for disable processor
    method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=5,
        message=operation_metadata.CommonOperationMetadata,
    )


class SetDefaultProcessorVersionRequest(proto.Message):
    r"""Request message for the set default processor version method.

    Attributes:
        processor (str):
            Required. The resource name of the
            [Processor][google.cloud.documentai.v1.Processor] to change
            default version.
        default_processor_version (str):
            Required. The resource name of child
            [ProcessorVersion][google.cloud.documentai.v1.ProcessorVersion]
            to use as default. Format:
            ``projects/{project}/locations/{location}/processors/{processor}/processorVersions/{version}``
    """

    processor: str = proto.Field(
        proto.STRING,
        number=1,
    )
    default_processor_version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SetDefaultProcessorVersionResponse(proto.Message):
    r"""Response message for set default processor version method."""


class SetDefaultProcessorVersionMetadata(proto.Message):
    r"""The long running operation metadata for set default processor
    version method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class ReviewDocumentRequest(proto.Message):
    r"""Request message for review document method.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inline_document (google.cloud.documentai_v1.types.Document):
            An inline document proto.

            This field is a member of `oneof`_ ``source``.
        human_review_config (str):
            Required. The resource name of the
            HumanReviewConfig that the document will be
            reviewed with.
        enable_schema_validation (bool):
            Whether the validation should be performed on
            the ad-hoc review request.
        priority (google.cloud.documentai_v1.types.ReviewDocumentRequest.Priority):
            The priority of the human review task.
        document_schema (google.cloud.documentai_v1.types.DocumentSchema):
            The document schema of the human review task.
    """

    class Priority(proto.Enum):
        r"""The priority level of the human review task.

        Values:
            DEFAULT (0):
                The default priority level.
            URGENT (1):
                The urgent priority level. The labeling
                manager should allocate labeler resource to the
                urgent task queue to respect this priority
                level.
        """
        DEFAULT = 0
        URGENT = 1

    inline_document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="source",
        message=gcd_document.Document,
    )
    human_review_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    enable_schema_validation: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    priority: Priority = proto.Field(
        proto.ENUM,
        number=5,
        enum=Priority,
    )
    document_schema: gcd_document_schema.DocumentSchema = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gcd_document_schema.DocumentSchema,
    )


class ReviewDocumentResponse(proto.Message):
    r"""Response message for review document method.

    Attributes:
        gcs_destination (str):
            The Cloud Storage uri for the human reviewed
            document if the review is succeeded.
        state (google.cloud.documentai_v1.types.ReviewDocumentResponse.State):
            The state of the review operation.
        rejection_reason (str):
            The reason why the review is rejected by
            reviewer.
    """

    class State(proto.Enum):
        r"""Possible states of the review operation.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            REJECTED (1):
                The review operation is rejected by the
                reviewer.
            SUCCEEDED (2):
                The review operation is succeeded.
        """
        STATE_UNSPECIFIED = 0
        REJECTED = 1
        SUCCEEDED = 2

    gcs_destination: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    rejection_reason: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ReviewDocumentOperationMetadata(proto.Message):
    r"""The long running operation metadata for review document
    method.

    Attributes:
        common_metadata (google.cloud.documentai_v1.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
        question_id (str):
            The Crowd Compute question ID.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=5,
        message=operation_metadata.CommonOperationMetadata,
    )
    question_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
