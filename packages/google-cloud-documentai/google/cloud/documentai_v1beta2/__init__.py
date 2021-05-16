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

from .services.document_understanding_service import DocumentUnderstandingServiceClient
from .services.document_understanding_service import (
    DocumentUnderstandingServiceAsyncClient,
)

from .types.document import Document
from .types.document_understanding import AutoMlParams
from .types.document_understanding import BatchProcessDocumentsRequest
from .types.document_understanding import BatchProcessDocumentsResponse
from .types.document_understanding import EntityExtractionParams
from .types.document_understanding import FormExtractionParams
from .types.document_understanding import GcsDestination
from .types.document_understanding import GcsSource
from .types.document_understanding import InputConfig
from .types.document_understanding import KeyValuePairHint
from .types.document_understanding import OcrParams
from .types.document_understanding import OperationMetadata
from .types.document_understanding import OutputConfig
from .types.document_understanding import ProcessDocumentRequest
from .types.document_understanding import ProcessDocumentResponse
from .types.document_understanding import TableBoundHint
from .types.document_understanding import TableExtractionParams
from .types.geometry import BoundingPoly
from .types.geometry import NormalizedVertex
from .types.geometry import Vertex

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
