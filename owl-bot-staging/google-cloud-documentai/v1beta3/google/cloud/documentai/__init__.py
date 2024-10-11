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
from google.cloud.documentai import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.documentai_v1beta3.services.document_processor_service.client import DocumentProcessorServiceClient
from google.cloud.documentai_v1beta3.services.document_processor_service.async_client import DocumentProcessorServiceAsyncClient
from google.cloud.documentai_v1beta3.services.document_service.client import DocumentServiceClient
from google.cloud.documentai_v1beta3.services.document_service.async_client import DocumentServiceAsyncClient

from google.cloud.documentai_v1beta3.types.barcode import Barcode
from google.cloud.documentai_v1beta3.types.dataset import BatchDatasetDocuments
from google.cloud.documentai_v1beta3.types.dataset import Dataset
from google.cloud.documentai_v1beta3.types.dataset import DatasetSchema
from google.cloud.documentai_v1beta3.types.dataset import DocumentId
from google.cloud.documentai_v1beta3.types.document import Document
from google.cloud.documentai_v1beta3.types.document import RevisionRef
from google.cloud.documentai_v1beta3.types.document_io import BatchDocumentsInputConfig
from google.cloud.documentai_v1beta3.types.document_io import DocumentOutputConfig
from google.cloud.documentai_v1beta3.types.document_io import GcsDocument
from google.cloud.documentai_v1beta3.types.document_io import GcsDocuments
from google.cloud.documentai_v1beta3.types.document_io import GcsPrefix
from google.cloud.documentai_v1beta3.types.document_io import OcrConfig
from google.cloud.documentai_v1beta3.types.document_io import RawDocument
from google.cloud.documentai_v1beta3.types.document_processor_service import BatchProcessMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import BatchProcessRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import BatchProcessResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import CreateProcessorRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import DeleteProcessorMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import DeleteProcessorRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import DeleteProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import DeleteProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import DeployProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import DeployProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import DeployProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import DisableProcessorMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import DisableProcessorRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import DisableProcessorResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import EnableProcessorMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import EnableProcessorRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import EnableProcessorResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import EvaluateProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import EvaluateProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import EvaluateProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import FetchProcessorTypesRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import FetchProcessorTypesResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import GetEvaluationRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import GetProcessorRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import GetProcessorTypeRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import GetProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import HumanReviewStatus
from google.cloud.documentai_v1beta3.types.document_processor_service import ImportProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import ImportProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ImportProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ListEvaluationsRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ListEvaluationsResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorsRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorsResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorTypesRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorTypesResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorVersionsRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ListProcessorVersionsResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ProcessOptions
from google.cloud.documentai_v1beta3.types.document_processor_service import ProcessRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ProcessResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import ReviewDocumentOperationMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import ReviewDocumentRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import ReviewDocumentResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import SetDefaultProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import SetDefaultProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import SetDefaultProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import TrainProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import TrainProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import TrainProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_processor_service import UndeployProcessorVersionMetadata
from google.cloud.documentai_v1beta3.types.document_processor_service import UndeployProcessorVersionRequest
from google.cloud.documentai_v1beta3.types.document_processor_service import UndeployProcessorVersionResponse
from google.cloud.documentai_v1beta3.types.document_schema import DocumentSchema
from google.cloud.documentai_v1beta3.types.document_schema import EntityTypeMetadata
from google.cloud.documentai_v1beta3.types.document_schema import FieldExtractionMetadata
from google.cloud.documentai_v1beta3.types.document_schema import PropertyMetadata
from google.cloud.documentai_v1beta3.types.document_schema import SummaryOptions
from google.cloud.documentai_v1beta3.types.document_service import BatchDeleteDocumentsMetadata
from google.cloud.documentai_v1beta3.types.document_service import BatchDeleteDocumentsRequest
from google.cloud.documentai_v1beta3.types.document_service import BatchDeleteDocumentsResponse
from google.cloud.documentai_v1beta3.types.document_service import DocumentMetadata
from google.cloud.documentai_v1beta3.types.document_service import DocumentPageRange
from google.cloud.documentai_v1beta3.types.document_service import GetDatasetSchemaRequest
from google.cloud.documentai_v1beta3.types.document_service import GetDocumentRequest
from google.cloud.documentai_v1beta3.types.document_service import GetDocumentResponse
from google.cloud.documentai_v1beta3.types.document_service import ImportDocumentsMetadata
from google.cloud.documentai_v1beta3.types.document_service import ImportDocumentsRequest
from google.cloud.documentai_v1beta3.types.document_service import ImportDocumentsResponse
from google.cloud.documentai_v1beta3.types.document_service import ListDocumentsRequest
from google.cloud.documentai_v1beta3.types.document_service import ListDocumentsResponse
from google.cloud.documentai_v1beta3.types.document_service import UpdateDatasetOperationMetadata
from google.cloud.documentai_v1beta3.types.document_service import UpdateDatasetRequest
from google.cloud.documentai_v1beta3.types.document_service import UpdateDatasetSchemaRequest
from google.cloud.documentai_v1beta3.types.document_service import DatasetSplitType
from google.cloud.documentai_v1beta3.types.document_service import DocumentLabelingState
from google.cloud.documentai_v1beta3.types.evaluation import Evaluation
from google.cloud.documentai_v1beta3.types.evaluation import EvaluationReference
from google.cloud.documentai_v1beta3.types.geometry import BoundingPoly
from google.cloud.documentai_v1beta3.types.geometry import NormalizedVertex
from google.cloud.documentai_v1beta3.types.geometry import Vertex
from google.cloud.documentai_v1beta3.types.operation_metadata import CommonOperationMetadata
from google.cloud.documentai_v1beta3.types.processor import Processor
from google.cloud.documentai_v1beta3.types.processor import ProcessorVersion
from google.cloud.documentai_v1beta3.types.processor import ProcessorVersionAlias
from google.cloud.documentai_v1beta3.types.processor_type import ProcessorType

__all__ = ('DocumentProcessorServiceClient',
    'DocumentProcessorServiceAsyncClient',
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'Barcode',
    'BatchDatasetDocuments',
    'Dataset',
    'DatasetSchema',
    'DocumentId',
    'Document',
    'RevisionRef',
    'BatchDocumentsInputConfig',
    'DocumentOutputConfig',
    'GcsDocument',
    'GcsDocuments',
    'GcsPrefix',
    'OcrConfig',
    'RawDocument',
    'BatchProcessMetadata',
    'BatchProcessRequest',
    'BatchProcessResponse',
    'CreateProcessorRequest',
    'DeleteProcessorMetadata',
    'DeleteProcessorRequest',
    'DeleteProcessorVersionMetadata',
    'DeleteProcessorVersionRequest',
    'DeployProcessorVersionMetadata',
    'DeployProcessorVersionRequest',
    'DeployProcessorVersionResponse',
    'DisableProcessorMetadata',
    'DisableProcessorRequest',
    'DisableProcessorResponse',
    'EnableProcessorMetadata',
    'EnableProcessorRequest',
    'EnableProcessorResponse',
    'EvaluateProcessorVersionMetadata',
    'EvaluateProcessorVersionRequest',
    'EvaluateProcessorVersionResponse',
    'FetchProcessorTypesRequest',
    'FetchProcessorTypesResponse',
    'GetEvaluationRequest',
    'GetProcessorRequest',
    'GetProcessorTypeRequest',
    'GetProcessorVersionRequest',
    'HumanReviewStatus',
    'ImportProcessorVersionMetadata',
    'ImportProcessorVersionRequest',
    'ImportProcessorVersionResponse',
    'ListEvaluationsRequest',
    'ListEvaluationsResponse',
    'ListProcessorsRequest',
    'ListProcessorsResponse',
    'ListProcessorTypesRequest',
    'ListProcessorTypesResponse',
    'ListProcessorVersionsRequest',
    'ListProcessorVersionsResponse',
    'ProcessOptions',
    'ProcessRequest',
    'ProcessResponse',
    'ReviewDocumentOperationMetadata',
    'ReviewDocumentRequest',
    'ReviewDocumentResponse',
    'SetDefaultProcessorVersionMetadata',
    'SetDefaultProcessorVersionRequest',
    'SetDefaultProcessorVersionResponse',
    'TrainProcessorVersionMetadata',
    'TrainProcessorVersionRequest',
    'TrainProcessorVersionResponse',
    'UndeployProcessorVersionMetadata',
    'UndeployProcessorVersionRequest',
    'UndeployProcessorVersionResponse',
    'DocumentSchema',
    'EntityTypeMetadata',
    'FieldExtractionMetadata',
    'PropertyMetadata',
    'SummaryOptions',
    'BatchDeleteDocumentsMetadata',
    'BatchDeleteDocumentsRequest',
    'BatchDeleteDocumentsResponse',
    'DocumentMetadata',
    'DocumentPageRange',
    'GetDatasetSchemaRequest',
    'GetDocumentRequest',
    'GetDocumentResponse',
    'ImportDocumentsMetadata',
    'ImportDocumentsRequest',
    'ImportDocumentsResponse',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'UpdateDatasetOperationMetadata',
    'UpdateDatasetRequest',
    'UpdateDatasetSchemaRequest',
    'DatasetSplitType',
    'DocumentLabelingState',
    'Evaluation',
    'EvaluationReference',
    'BoundingPoly',
    'NormalizedVertex',
    'Vertex',
    'CommonOperationMetadata',
    'Processor',
    'ProcessorVersion',
    'ProcessorVersionAlias',
    'ProcessorType',
)
