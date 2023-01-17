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
from google.cloud.documentai import gapic_version as package_version

__version__ = package_version.__version__


from .services.document_processor_service import (
    DocumentProcessorServiceAsyncClient,
    DocumentProcessorServiceClient,
)
from .types.barcode import Barcode
from .types.document import Document
from .types.document_io import (
    BatchDocumentsInputConfig,
    DocumentOutputConfig,
    GcsDocument,
    GcsDocuments,
    GcsPrefix,
    RawDocument,
)
from .types.document_processor_service import (
    BatchProcessMetadata,
    BatchProcessRequest,
    BatchProcessResponse,
    CreateProcessorRequest,
    DeleteProcessorMetadata,
    DeleteProcessorRequest,
    DeleteProcessorVersionMetadata,
    DeleteProcessorVersionRequest,
    DeployProcessorVersionMetadata,
    DeployProcessorVersionRequest,
    DeployProcessorVersionResponse,
    DisableProcessorMetadata,
    DisableProcessorRequest,
    DisableProcessorResponse,
    EnableProcessorMetadata,
    EnableProcessorRequest,
    EnableProcessorResponse,
    FetchProcessorTypesRequest,
    FetchProcessorTypesResponse,
    GetProcessorRequest,
    GetProcessorTypeRequest,
    GetProcessorVersionRequest,
    HumanReviewStatus,
    ListProcessorsRequest,
    ListProcessorsResponse,
    ListProcessorTypesRequest,
    ListProcessorTypesResponse,
    ListProcessorVersionsRequest,
    ListProcessorVersionsResponse,
    ProcessRequest,
    ProcessResponse,
    ReviewDocumentOperationMetadata,
    ReviewDocumentRequest,
    ReviewDocumentResponse,
    SetDefaultProcessorVersionMetadata,
    SetDefaultProcessorVersionRequest,
    SetDefaultProcessorVersionResponse,
    UndeployProcessorVersionMetadata,
    UndeployProcessorVersionRequest,
    UndeployProcessorVersionResponse,
)
from .types.document_schema import DocumentSchema
from .types.geometry import BoundingPoly, NormalizedVertex, Vertex
from .types.operation_metadata import CommonOperationMetadata
from .types.processor import Processor, ProcessorVersion
from .types.processor_type import ProcessorType

__all__ = (
    "DocumentProcessorServiceAsyncClient",
    "Barcode",
    "BatchDocumentsInputConfig",
    "BatchProcessMetadata",
    "BatchProcessRequest",
    "BatchProcessResponse",
    "BoundingPoly",
    "CommonOperationMetadata",
    "CreateProcessorRequest",
    "DeleteProcessorMetadata",
    "DeleteProcessorRequest",
    "DeleteProcessorVersionMetadata",
    "DeleteProcessorVersionRequest",
    "DeployProcessorVersionMetadata",
    "DeployProcessorVersionRequest",
    "DeployProcessorVersionResponse",
    "DisableProcessorMetadata",
    "DisableProcessorRequest",
    "DisableProcessorResponse",
    "Document",
    "DocumentOutputConfig",
    "DocumentProcessorServiceClient",
    "DocumentSchema",
    "EnableProcessorMetadata",
    "EnableProcessorRequest",
    "EnableProcessorResponse",
    "FetchProcessorTypesRequest",
    "FetchProcessorTypesResponse",
    "GcsDocument",
    "GcsDocuments",
    "GcsPrefix",
    "GetProcessorRequest",
    "GetProcessorTypeRequest",
    "GetProcessorVersionRequest",
    "HumanReviewStatus",
    "ListProcessorTypesRequest",
    "ListProcessorTypesResponse",
    "ListProcessorVersionsRequest",
    "ListProcessorVersionsResponse",
    "ListProcessorsRequest",
    "ListProcessorsResponse",
    "NormalizedVertex",
    "ProcessRequest",
    "ProcessResponse",
    "Processor",
    "ProcessorType",
    "ProcessorVersion",
    "RawDocument",
    "ReviewDocumentOperationMetadata",
    "ReviewDocumentRequest",
    "ReviewDocumentResponse",
    "SetDefaultProcessorVersionMetadata",
    "SetDefaultProcessorVersionRequest",
    "SetDefaultProcessorVersionResponse",
    "UndeployProcessorVersionMetadata",
    "UndeployProcessorVersionRequest",
    "UndeployProcessorVersionResponse",
    "Vertex",
)
