# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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


from google.cloud.documentai_v1beta2.services.document_understanding_service.client import (
    DocumentUnderstandingServiceClient,
)
from google.cloud.documentai_v1beta2.types.document import Document
from google.cloud.documentai_v1beta2.types.document_understanding import AutoMlParams
from google.cloud.documentai_v1beta2.types.document_understanding import (
    BatchProcessDocumentsRequest,
)
from google.cloud.documentai_v1beta2.types.document_understanding import (
    BatchProcessDocumentsResponse,
)
from google.cloud.documentai_v1beta2.types.document_understanding import (
    EntityExtractionParams,
)
from google.cloud.documentai_v1beta2.types.document_understanding import (
    FormExtractionParams,
)
from google.cloud.documentai_v1beta2.types.document_understanding import GcsDestination
from google.cloud.documentai_v1beta2.types.document_understanding import GcsSource
from google.cloud.documentai_v1beta2.types.document_understanding import InputConfig
from google.cloud.documentai_v1beta2.types.document_understanding import (
    KeyValuePairHint,
)
from google.cloud.documentai_v1beta2.types.document_understanding import OcrParams
from google.cloud.documentai_v1beta2.types.document_understanding import (
    OperationMetadata,
)
from google.cloud.documentai_v1beta2.types.document_understanding import OutputConfig
from google.cloud.documentai_v1beta2.types.document_understanding import (
    ProcessDocumentRequest,
)
from google.cloud.documentai_v1beta2.types.document_understanding import (
    ProcessDocumentResponse,
)
from google.cloud.documentai_v1beta2.types.document_understanding import TableBoundHint
from google.cloud.documentai_v1beta2.types.document_understanding import (
    TableExtractionParams,
)
from google.cloud.documentai_v1beta2.types.geometry import BoundingPoly
from google.cloud.documentai_v1beta2.types.geometry import NormalizedVertex
from google.cloud.documentai_v1beta2.types.geometry import Vertex

__all__ = (
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
