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
from google.cloud.documentai_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.document_understanding_service import (
    DocumentUnderstandingServiceAsyncClient,
    DocumentUnderstandingServiceClient,
)
from .types.document import Document
from .types.document_understanding import (
    AutoMlParams,
    BatchProcessDocumentsRequest,
    BatchProcessDocumentsResponse,
    EntityExtractionParams,
    FormExtractionParams,
    GcsDestination,
    GcsSource,
    InputConfig,
    KeyValuePairHint,
    OcrParams,
    OperationMetadata,
    OutputConfig,
    ProcessDocumentRequest,
    ProcessDocumentResponse,
    TableBoundHint,
    TableExtractionParams,
)
from .types.geometry import BoundingPoly, NormalizedVertex, Vertex

__all__ = (
    "DocumentUnderstandingServiceAsyncClient",
    "AutoMlParams",
    "BatchProcessDocumentsRequest",
    "BatchProcessDocumentsResponse",
    "BoundingPoly",
    "Document",
    "DocumentUnderstandingServiceClient",
    "EntityExtractionParams",
    "FormExtractionParams",
    "GcsDestination",
    "GcsSource",
    "InputConfig",
    "KeyValuePairHint",
    "NormalizedVertex",
    "OcrParams",
    "OperationMetadata",
    "OutputConfig",
    "ProcessDocumentRequest",
    "ProcessDocumentResponse",
    "TableBoundHint",
    "TableExtractionParams",
    "Vertex",
)
