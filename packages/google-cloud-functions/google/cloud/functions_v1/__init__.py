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
from google.cloud.functions_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_functions_service import (
    CloudFunctionsServiceAsyncClient,
    CloudFunctionsServiceClient,
)
from .types.functions import (
    CallFunctionRequest,
    CallFunctionResponse,
    CloudFunction,
    CloudFunctionStatus,
    CreateFunctionRequest,
    DeleteFunctionRequest,
    EventTrigger,
    FailurePolicy,
    GenerateDownloadUrlRequest,
    GenerateDownloadUrlResponse,
    GenerateUploadUrlRequest,
    GenerateUploadUrlResponse,
    GetFunctionRequest,
    HttpsTrigger,
    ListFunctionsRequest,
    ListFunctionsResponse,
    SecretEnvVar,
    SecretVolume,
    SourceRepository,
    UpdateFunctionRequest,
)
from .types.operations import OperationMetadataV1, OperationType

__all__ = (
    "CloudFunctionsServiceAsyncClient",
    "CallFunctionRequest",
    "CallFunctionResponse",
    "CloudFunction",
    "CloudFunctionStatus",
    "CloudFunctionsServiceClient",
    "CreateFunctionRequest",
    "DeleteFunctionRequest",
    "EventTrigger",
    "FailurePolicy",
    "GenerateDownloadUrlRequest",
    "GenerateDownloadUrlResponse",
    "GenerateUploadUrlRequest",
    "GenerateUploadUrlResponse",
    "GetFunctionRequest",
    "HttpsTrigger",
    "ListFunctionsRequest",
    "ListFunctionsResponse",
    "OperationMetadataV1",
    "OperationType",
    "SecretEnvVar",
    "SecretVolume",
    "SourceRepository",
    "UpdateFunctionRequest",
)
