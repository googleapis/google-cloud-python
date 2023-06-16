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
from google.cloud.documentai_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.document_processor_service import DocumentProcessorServiceClient
from .services.document_processor_service import DocumentProcessorServiceAsyncClient

from .types.barcode import Barcode
from .types.document import Document
from .types.document_io import BatchDocumentsInputConfig
from .types.document_io import DocumentOutputConfig
from .types.document_io import GcsDocument
from .types.document_io import GcsDocuments
from .types.document_io import GcsPrefix
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
from .types.document_processor_service import ListEvaluationsRequest
from .types.document_processor_service import ListEvaluationsResponse
from .types.document_processor_service import ListProcessorsRequest
from .types.document_processor_service import ListProcessorsResponse
from .types.document_processor_service import ListProcessorTypesRequest
from .types.document_processor_service import ListProcessorTypesResponse
from .types.document_processor_service import ListProcessorVersionsRequest
from .types.document_processor_service import ListProcessorVersionsResponse
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
from .types.evaluation import Evaluation
from .types.evaluation import EvaluationReference
from .types.geometry import BoundingPoly
from .types.geometry import NormalizedVertex
from .types.geometry import Vertex
from .types.operation_metadata import CommonOperationMetadata
from .types.processor import Processor
from .types.processor import ProcessorVersion
from .types.processor_type import ProcessorType

__all__ = (
    'DocumentProcessorServiceAsyncClient',
'Barcode',
'BatchDocumentsInputConfig',
'BatchProcessMetadata',
'BatchProcessRequest',
'BatchProcessResponse',
'BoundingPoly',
'CommonOperationMetadata',
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
'Document',
'DocumentOutputConfig',
'DocumentProcessorServiceClient',
'DocumentSchema',
'EnableProcessorMetadata',
'EnableProcessorRequest',
'EnableProcessorResponse',
'EvaluateProcessorVersionMetadata',
'EvaluateProcessorVersionRequest',
'EvaluateProcessorVersionResponse',
'Evaluation',
'EvaluationReference',
'FetchProcessorTypesRequest',
'FetchProcessorTypesResponse',
'GcsDocument',
'GcsDocuments',
'GcsPrefix',
'GetEvaluationRequest',
'GetProcessorRequest',
'GetProcessorTypeRequest',
'GetProcessorVersionRequest',
'HumanReviewStatus',
'ListEvaluationsRequest',
'ListEvaluationsResponse',
'ListProcessorTypesRequest',
'ListProcessorTypesResponse',
'ListProcessorVersionsRequest',
'ListProcessorVersionsResponse',
'ListProcessorsRequest',
'ListProcessorsResponse',
'NormalizedVertex',
'ProcessRequest',
'ProcessResponse',
'Processor',
'ProcessorType',
'ProcessorVersion',
'RawDocument',
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
'Vertex',
)
