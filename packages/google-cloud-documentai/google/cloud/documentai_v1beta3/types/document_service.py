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

from google.protobuf import field_mask_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.documentai_v1beta3.types import document_io, operation_metadata
from google.cloud.documentai_v1beta3.types import dataset as gcd_dataset
from google.cloud.documentai_v1beta3.types import document as gcd_document

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3",
    manifest={
        "DatasetSplitType",
        "UpdateDatasetRequest",
        "UpdateDatasetOperationMetadata",
        "ImportDocumentsRequest",
        "ImportDocumentsResponse",
        "ImportDocumentsMetadata",
        "GetDocumentRequest",
        "GetDocumentResponse",
        "BatchDeleteDocumentsRequest",
        "BatchDeleteDocumentsResponse",
        "BatchDeleteDocumentsMetadata",
        "GetDatasetSchemaRequest",
        "UpdateDatasetSchemaRequest",
        "DocumentPageRange",
    },
)


class DatasetSplitType(proto.Enum):
    r"""Documents belonging to a dataset will be split into different
    groups referred to as splits: train, test.

    Values:
        DATASET_SPLIT_TYPE_UNSPECIFIED (0):
            Default value if the enum is not set.
            go/protodosdonts#do-include-an-unspecified-value-in-an-enum
        DATASET_SPLIT_TRAIN (1):
            Identifies the train documents.
        DATASET_SPLIT_TEST (2):
            Identifies the test documents.
        DATASET_SPLIT_UNASSIGNED (3):
            Identifies the unassigned documents.
    """
    DATASET_SPLIT_TYPE_UNSPECIFIED = 0
    DATASET_SPLIT_TRAIN = 1
    DATASET_SPLIT_TEST = 2
    DATASET_SPLIT_UNASSIGNED = 3


class UpdateDatasetRequest(proto.Message):
    r"""

    Attributes:
        dataset (google.cloud.documentai_v1beta3.types.Dataset):
            Required. The ``name`` field of the ``Dataset`` is used to
            identify the resource to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the resource.
    """

    dataset: gcd_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_dataset.Dataset,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class UpdateDatasetOperationMetadata(proto.Message):
    r"""

    Attributes:
        common_metadata (google.cloud.documentai_v1beta3.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class ImportDocumentsRequest(proto.Message):
    r"""

    Attributes:
        dataset (str):
            Required. The dataset resource name.
            Format:

            projects/{project}/locations/{location}/processors/{processor}/dataset
        batch_documents_import_configs (MutableSequence[google.cloud.documentai_v1beta3.types.ImportDocumentsRequest.BatchDocumentsImportConfig]):
            Required. The Cloud Storage uri containing
            raw documents that must be imported.
    """

    class BatchDocumentsImportConfig(proto.Message):
        r"""Config for importing documents.
        Each batch can have its own dataset split type.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            dataset_split (google.cloud.documentai_v1beta3.types.DatasetSplitType):
                Target dataset split where the documents must
                be stored.

                This field is a member of `oneof`_ ``split_type_config``.
            auto_split_config (google.cloud.documentai_v1beta3.types.ImportDocumentsRequest.BatchDocumentsImportConfig.AutoSplitConfig):
                If set, documents will be automatically split
                into training and test split category with the
                specified ratio.

                This field is a member of `oneof`_ ``split_type_config``.
            batch_input_config (google.cloud.documentai_v1beta3.types.BatchDocumentsInputConfig):
                The common config to specify a set of
                documents used as input.
        """

        class AutoSplitConfig(proto.Message):
            r"""The config for auto-split.

            Attributes:
                training_split_ratio (float):
                    Ratio of training dataset split.
            """

            training_split_ratio: float = proto.Field(
                proto.FLOAT,
                number=1,
            )

        dataset_split: "DatasetSplitType" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="split_type_config",
            enum="DatasetSplitType",
        )
        auto_split_config: "ImportDocumentsRequest.BatchDocumentsImportConfig.AutoSplitConfig" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="split_type_config",
            message="ImportDocumentsRequest.BatchDocumentsImportConfig.AutoSplitConfig",
        )
        batch_input_config: document_io.BatchDocumentsInputConfig = proto.Field(
            proto.MESSAGE,
            number=1,
            message=document_io.BatchDocumentsInputConfig,
        )

    dataset: str = proto.Field(
        proto.STRING,
        number=1,
    )
    batch_documents_import_configs: MutableSequence[
        BatchDocumentsImportConfig
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=BatchDocumentsImportConfig,
    )


class ImportDocumentsResponse(proto.Message):
    r"""Response of the import document operation."""


class ImportDocumentsMetadata(proto.Message):
    r"""Metadata of the import document operation.

    Attributes:
        common_metadata (google.cloud.documentai_v1beta3.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
        individual_import_statuses (MutableSequence[google.cloud.documentai_v1beta3.types.ImportDocumentsMetadata.IndividualImportStatus]):
            The list of response details of each
            document.
        import_config_validation_results (MutableSequence[google.cloud.documentai_v1beta3.types.ImportDocumentsMetadata.ImportConfigValidationResult]):
            Validation statuses of the batch documents
            import config.
        total_document_count (int):
            Total number of the documents that are
            qualified for importing.
    """

    class IndividualImportStatus(proto.Message):
        r"""The status of each individual document in the import process.

        Attributes:
            input_gcs_source (str):
                The source Cloud Storage URI of the document.
            status (google.rpc.status_pb2.Status):
                The status of the importing of the document.
            output_document_id (google.cloud.documentai_v1beta3.types.DocumentId):
                The document id of imported document if it
                was successful, otherwise empty.
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
        output_document_id: gcd_dataset.DocumentId = proto.Field(
            proto.MESSAGE,
            number=4,
            message=gcd_dataset.DocumentId,
        )

    class ImportConfigValidationResult(proto.Message):
        r"""The validation status of each import config. Status is set to errors
        if there is no documents to import in the import_config, or OK if
        the operation will try to proceed at least one document.

        Attributes:
            input_gcs_source (str):
                The source Cloud Storage URI specified in the
                import config.
            status (google.rpc.status_pb2.Status):
                The validation status of import config.
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

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )
    individual_import_statuses: MutableSequence[
        IndividualImportStatus
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=IndividualImportStatus,
    )
    import_config_validation_results: MutableSequence[
        ImportConfigValidationResult
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=ImportConfigValidationResult,
    )
    total_document_count: int = proto.Field(
        proto.INT32,
        number=3,
    )


class GetDocumentRequest(proto.Message):
    r"""

    Attributes:
        dataset (str):
            Required. The resource name of the dataset
            that the document belongs to . Format:

            projects/{project}/locations/{location}/processors/{processor}/dataset
        document_id (google.cloud.documentai_v1beta3.types.DocumentId):
            Required. Document identifier.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            If set, only fields listed here will be
            returned. Otherwise, all fields will be returned
            by default.
        page_range (google.cloud.documentai_v1beta3.types.DocumentPageRange):
            List of pages for which the fields specified in the
            ``read_mask`` must be served.
    """

    dataset: str = proto.Field(
        proto.STRING,
        number=1,
    )
    document_id: gcd_dataset.DocumentId = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_dataset.DocumentId,
    )
    read_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )
    page_range: "DocumentPageRange" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="DocumentPageRange",
    )


class GetDocumentResponse(proto.Message):
    r"""

    Attributes:
        document (google.cloud.documentai_v1beta3.types.Document):

    """

    document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_document.Document,
    )


class BatchDeleteDocumentsRequest(proto.Message):
    r"""

    Attributes:
        dataset (str):
            Required. The dataset resource name.
            Format:

            projects/{project}/locations/{location}/processors/{processor}/dataset
        dataset_documents (google.cloud.documentai_v1beta3.types.BatchDatasetDocuments):
            Required. Dataset documents input. If given ``filter``, all
            documents satisfying the filter will be deleted. If given
            documentIds, a maximum of 50 documents can be deleted in a
            batch. The request will be rejected if more than 50
            document_ids are provided.
    """

    dataset: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_documents: gcd_dataset.BatchDatasetDocuments = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcd_dataset.BatchDatasetDocuments,
    )


class BatchDeleteDocumentsResponse(proto.Message):
    r"""Response of the delete documents operation."""


class BatchDeleteDocumentsMetadata(proto.Message):
    r"""

    Attributes:
        common_metadata (google.cloud.documentai_v1beta3.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
        individual_batch_delete_statuses (MutableSequence[google.cloud.documentai_v1beta3.types.BatchDeleteDocumentsMetadata.IndividualBatchDeleteStatus]):
            The list of response details of each
            document.
        total_document_count (int):
            Total number of documents deleting from
            dataset.
        error_document_count (int):
            Total number of documents that failed to be
            deleted in storage.
    """

    class IndividualBatchDeleteStatus(proto.Message):
        r"""The status of each individual document in the batch delete
        process.

        Attributes:
            document_id (google.cloud.documentai_v1beta3.types.DocumentId):
                The document id of the document.
            status (google.rpc.status_pb2.Status):
                The status of deleting the document in
                storage.
        """

        document_id: gcd_dataset.DocumentId = proto.Field(
            proto.MESSAGE,
            number=1,
            message=gcd_dataset.DocumentId,
        )
        status: status_pb2.Status = proto.Field(
            proto.MESSAGE,
            number=2,
            message=status_pb2.Status,
        )

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )
    individual_batch_delete_statuses: MutableSequence[
        IndividualBatchDeleteStatus
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=IndividualBatchDeleteStatus,
    )
    total_document_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    error_document_count: int = proto.Field(
        proto.INT32,
        number=4,
    )


class GetDatasetSchemaRequest(proto.Message):
    r"""Request for ``GetDatasetSchema``.

    Attributes:
        name (str):
            Required. The dataset schema resource name.
            Format:

            projects/{project}/locations/{location}/processors/{processor}/dataset/datasetSchema
        visible_fields_only (bool):
            If set, only returns the visible fields of
            the schema.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    visible_fields_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class UpdateDatasetSchemaRequest(proto.Message):
    r"""Request for ``UpdateDatasetSchema``.

    Attributes:
        dataset_schema (google.cloud.documentai_v1beta3.types.DatasetSchema):
            Required. The name field of the ``DatasetSchema`` is used to
            identify the resource to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the resource.
    """

    dataset_schema: gcd_dataset.DatasetSchema = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_dataset.DatasetSchema,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DocumentPageRange(proto.Message):
    r"""Range of pages present in a document.

    Attributes:
        start (int):
            First page number (one-based index) to be
            returned.
        end (int):
            Last page number (one-based index) to be
            returned.
    """

    start: int = proto.Field(
        proto.INT32,
        number=1,
    )
    end: int = proto.Field(
        proto.INT32,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
