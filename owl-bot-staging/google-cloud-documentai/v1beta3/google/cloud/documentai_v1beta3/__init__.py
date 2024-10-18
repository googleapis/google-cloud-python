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
from google.cloud.documentai_v1beta3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.document_processor_service import DocumentProcessorServiceClient
from .services.document_processor_service import DocumentProcessorServiceAsyncClient
from .services.document_service import DocumentServiceClient
from .services.document_service import DocumentServiceAsyncClient

from .types.barcode import Barcode
from .types.dataset import BatchDatasetDocuments
from .types.dataset import Dataset
from .types.dataset import DatasetSchema
from .types.dataset import DocumentId
from .types.document import Document
from .types.document import RevisionRef
from .types.document_io import BatchDocumentsInputConfig
from .types.document_io import DocumentOutputConfig
from .types.document_io import GcsDocument
from .types.document_io import GcsDocuments
from .types.document_io import GcsPrefix
from .types.document_io import OcrConfig
from .types.document_io import RawDocument
from .types.document_processor_service import BatchProcessMetadata
from .types.document_processor_service import BatchProcessRequest
from .types.document_processor_service import BatchProcessResponse
from .types.document_processor_service import CreateProcessorRequest
from .types.document_processor_service import DeleteProcessorMetadata
from .types.document_processor_service import DeleteProcessorRequest
from .types.document_processor_service import DeleteProcessorVersionMetadata
from .types.document_processor_service import DeleteProcessorVersionRequest
from .types.document_processor_service import DeployProcessorVersionMetadata
from .types.document_processor_service import DeployProcessorVersionRequest
from .types.document_processor_service import DeployProcessorVersionResponse
from .types.document_processor_service import DisableProcessorMetadata
from .types.document_processor_service import DisableProcessorRequest
from .types.document_processor_service import DisableProcessorResponse
from .types.document_processor_service import EnableProcessorMetadata
from .types.document_processor_service import EnableProcessorRequest
from .types.document_processor_service import EnableProcessorResponse
from .types.document_processor_service import EvaluateProcessorVersionMetadata
from .types.document_processor_service import EvaluateProcessorVersionRequest
from .types.document_processor_service import EvaluateProcessorVersionResponse
from .types.document_processor_service import FetchProcessorTypesRequest
from .types.document_processor_service import FetchProcessorTypesResponse
from .types.document_processor_service import GetEvaluationRequest
from .types.document_processor_service import GetProcessorRequest
from .types.document_processor_service import GetProcessorTypeRequest
from .types.document_processor_service import GetProcessorVersionRequest
from .types.document_processor_service import HumanReviewStatus
from .types.document_processor_service import ImportProcessorVersionMetadata
from .types.document_processor_service import ImportProcessorVersionRequest
from .types.document_processor_service import ImportProcessorVersionResponse
from .types.document_processor_service import ListEvaluationsRequest
from .types.document_processor_service import ListEvaluationsResponse
from .types.document_processor_service import ListProcessorsRequest
from .types.document_processor_service import ListProcessorsResponse
from .types.document_processor_service import ListProcessorTypesRequest
from .types.document_processor_service import ListProcessorTypesResponse
from .types.document_processor_service import ListProcessorVersionsRequest
from .types.document_processor_service import ListProcessorVersionsResponse
from .types.document_processor_service import ProcessOptions
from .types.document_processor_service import ProcessRequest
from .types.document_processor_service import ProcessResponse
from .types.document_processor_service import ReviewDocumentOperationMetadata
from .types.document_processor_service import ReviewDocumentRequest
from .types.document_processor_service import ReviewDocumentResponse
from .types.document_processor_service import SetDefaultProcessorVersionMetadata
from .types.document_processor_service import SetDefaultProcessorVersionRequest
from .types.document_processor_service import SetDefaultProcessorVersionResponse
from .types.document_processor_service import TrainProcessorVersionMetadata
from .types.document_processor_service import TrainProcessorVersionRequest
from .types.document_processor_service import TrainProcessorVersionResponse
from .types.document_processor_service import UndeployProcessorVersionMetadata
from .types.document_processor_service import UndeployProcessorVersionRequest
from .types.document_processor_service import UndeployProcessorVersionResponse
from .types.document_schema import DocumentSchema
from .types.document_schema import EntityTypeMetadata
from .types.document_schema import FieldExtractionMetadata
from .types.document_schema import PropertyMetadata
from .types.document_schema import SummaryOptions
from .types.document_service import BatchDeleteDocumentsMetadata
from .types.document_service import BatchDeleteDocumentsRequest
from .types.document_service import BatchDeleteDocumentsResponse
from .types.document_service import DocumentMetadata
from .types.document_service import DocumentPageRange
from .types.document_service import GetDatasetSchemaRequest
from .types.document_service import GetDocumentRequest
from .types.document_service import GetDocumentResponse
from .types.document_service import ImportDocumentsMetadata
from .types.document_service import ImportDocumentsRequest
from .types.document_service import ImportDocumentsResponse
from .types.document_service import ListDocumentsRequest
from .types.document_service import ListDocumentsResponse
from .types.document_service import UpdateDatasetOperationMetadata
from .types.document_service import UpdateDatasetRequest
from .types.document_service import UpdateDatasetSchemaRequest
from .types.document_service import DatasetSplitType
from .types.document_service import DocumentLabelingState
from .types.evaluation import Evaluation
from .types.evaluation import EvaluationReference
from .types.geometry import BoundingPoly
from .types.geometry import NormalizedVertex
from .types.geometry import Vertex
from .types.operation_metadata import CommonOperationMetadata
from .types.processor import Processor
from .types.processor import ProcessorVersion
from .types.processor import ProcessorVersionAlias
from .types.processor_type import ProcessorType

__all__ = (
    'DocumentProcessorServiceAsyncClient',
    'DocumentServiceAsyncClient',
'Barcode',
'BatchDatasetDocuments',
'BatchDeleteDocumentsMetadata',
'BatchDeleteDocumentsRequest',
'BatchDeleteDocumentsResponse',
'BatchDocumentsInputConfig',
'BatchProcessMetadata',
'BatchProcessRequest',
'BatchProcessResponse',
'BoundingPoly',
'CommonOperationMetadata',
'CreateProcessorRequest',
'Dataset',
'DatasetSchema',
'DatasetSplitType',
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
'Document',
'DocumentId',
'DocumentLabelingState',
'DocumentMetadata',
'DocumentOutputConfig',
'DocumentPageRange',
'DocumentProcessorServiceClient',
'DocumentSchema',
'DocumentServiceClient',
'EnableProcessorMetadata',
'EnableProcessorRequest',
'EnableProcessorResponse',
'EntityTypeMetadata',
'EvaluateProcessorVersionMetadata',
'EvaluateProcessorVersionRequest',
'EvaluateProcessorVersionResponse',
'Evaluation',
'EvaluationReference',
'FetchProcessorTypesRequest',
'FetchProcessorTypesResponse',
'FieldExtractionMetadata',
'GcsDocument',
'GcsDocuments',
'GcsPrefix',
'GetDatasetSchemaRequest',
'GetDocumentRequest',
'GetDocumentResponse',
'GetEvaluationRequest',
'GetProcessorRequest',
'GetProcessorTypeRequest',
'GetProcessorVersionRequest',
'HumanReviewStatus',
'ImportDocumentsMetadata',
'ImportDocumentsRequest',
'ImportDocumentsResponse',
'ImportProcessorVersionMetadata',
'ImportProcessorVersionRequest',
'ImportProcessorVersionResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'ListEvaluationsRequest',
'ListEvaluationsResponse',
'ListProcessorTypesRequest',
'ListProcessorTypesResponse',
'ListProcessorVersionsRequest',
'ListProcessorVersionsResponse',
'ListProcessorsRequest',
'ListProcessorsResponse',
'NormalizedVertex',
'OcrConfig',
'ProcessOptions',
'ProcessRequest',
'ProcessResponse',
'Processor',
'ProcessorType',
'ProcessorVersion',
'ProcessorVersionAlias',
'PropertyMetadata',
'RawDocument',
'ReviewDocumentOperationMetadata',
'ReviewDocumentRequest',
'ReviewDocumentResponse',
'RevisionRef',
'SetDefaultProcessorVersionMetadata',
'SetDefaultProcessorVersionRequest',
'SetDefaultProcessorVersionResponse',
'SummaryOptions',
'TrainProcessorVersionMetadata',
'TrainProcessorVersionRequest',
'TrainProcessorVersionResponse',
'UndeployProcessorVersionMetadata',
'UndeployProcessorVersionRequest',
'UndeployProcessorVersionResponse',
'UpdateDatasetOperationMetadata',
'UpdateDatasetRequest',
'UpdateDatasetSchemaRequest',
'Vertex',
)
