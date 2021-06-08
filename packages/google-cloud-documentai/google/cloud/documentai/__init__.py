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

from google.cloud.documentai_v1.services.document_processor_service.client import (
    DocumentProcessorServiceClient,
)
from google.cloud.documentai_v1.services.document_processor_service.async_client import (
    DocumentProcessorServiceAsyncClient,
)

from google.cloud.documentai_v1.types.document import Document
from google.cloud.documentai_v1.types.document_io import BatchDocumentsInputConfig
from google.cloud.documentai_v1.types.document_io import DocumentOutputConfig
from google.cloud.documentai_v1.types.document_io import GcsDocument
from google.cloud.documentai_v1.types.document_io import GcsDocuments
from google.cloud.documentai_v1.types.document_io import GcsPrefix
from google.cloud.documentai_v1.types.document_io import RawDocument
from google.cloud.documentai_v1.types.document_processor_service import (
    BatchProcessMetadata,
)
from google.cloud.documentai_v1.types.document_processor_service import (
    BatchProcessRequest,
)
from google.cloud.documentai_v1.types.document_processor_service import (
    BatchProcessResponse,
)
from google.cloud.documentai_v1.types.document_processor_service import (
    HumanReviewStatus,
)
from google.cloud.documentai_v1.types.document_processor_service import ProcessRequest
from google.cloud.documentai_v1.types.document_processor_service import ProcessResponse
from google.cloud.documentai_v1.types.document_processor_service import (
    ReviewDocumentOperationMetadata,
)
from google.cloud.documentai_v1.types.document_processor_service import (
    ReviewDocumentRequest,
)
from google.cloud.documentai_v1.types.document_processor_service import (
    ReviewDocumentResponse,
)
from google.cloud.documentai_v1.types.geometry import BoundingPoly
from google.cloud.documentai_v1.types.geometry import NormalizedVertex
from google.cloud.documentai_v1.types.geometry import Vertex
from google.cloud.documentai_v1.types.operation_metadata import CommonOperationMetadata

__all__ = (
    "DocumentProcessorServiceClient",
    "DocumentProcessorServiceAsyncClient",
    "Document",
    "BatchDocumentsInputConfig",
    "DocumentOutputConfig",
    "GcsDocument",
    "GcsDocuments",
    "GcsPrefix",
    "RawDocument",
    "BatchProcessMetadata",
    "BatchProcessRequest",
    "BatchProcessResponse",
    "HumanReviewStatus",
    "ProcessRequest",
    "ProcessResponse",
    "ReviewDocumentOperationMetadata",
    "ReviewDocumentRequest",
    "ReviewDocumentResponse",
    "BoundingPoly",
    "NormalizedVertex",
    "Vertex",
    "CommonOperationMetadata",
)
