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
from google.cloud.functions_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.function_service import FunctionServiceAsyncClient, FunctionServiceClient
from .types.functions import (
    BuildConfig,
    CreateFunctionRequest,
    DeleteFunctionRequest,
    Environment,
    EventFilter,
    EventTrigger,
    Function,
    GenerateDownloadUrlRequest,
    GenerateDownloadUrlResponse,
    GenerateUploadUrlRequest,
    GenerateUploadUrlResponse,
    GetFunctionRequest,
    ListFunctionsRequest,
    ListFunctionsResponse,
    ListRuntimesRequest,
    ListRuntimesResponse,
    LocationMetadata,
    OperationMetadata,
    RepoSource,
    SecretEnvVar,
    SecretVolume,
    ServiceConfig,
    Source,
    SourceProvenance,
    Stage,
    StateMessage,
    StorageSource,
    UpdateFunctionRequest,
)

__all__ = (
    "FunctionServiceAsyncClient",
    "BuildConfig",
    "CreateFunctionRequest",
    "DeleteFunctionRequest",
    "Environment",
    "EventFilter",
    "EventTrigger",
    "Function",
    "FunctionServiceClient",
    "GenerateDownloadUrlRequest",
    "GenerateDownloadUrlResponse",
    "GenerateUploadUrlRequest",
    "GenerateUploadUrlResponse",
    "GetFunctionRequest",
    "ListFunctionsRequest",
    "ListFunctionsResponse",
    "ListRuntimesRequest",
    "ListRuntimesResponse",
    "LocationMetadata",
    "OperationMetadata",
    "RepoSource",
    "SecretEnvVar",
    "SecretVolume",
    "ServiceConfig",
    "Source",
    "SourceProvenance",
    "Stage",
    "StateMessage",
    "StorageSource",
    "UpdateFunctionRequest",
)
