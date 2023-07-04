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
from google.cloud.functions import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.functions_v2.services.function_service.client import FunctionServiceClient
from google.cloud.functions_v2.services.function_service.async_client import FunctionServiceAsyncClient

from google.cloud.functions_v2.types.functions import BuildConfig
from google.cloud.functions_v2.types.functions import CreateFunctionRequest
from google.cloud.functions_v2.types.functions import DeleteFunctionRequest
from google.cloud.functions_v2.types.functions import EventFilter
from google.cloud.functions_v2.types.functions import EventTrigger
from google.cloud.functions_v2.types.functions import Function
from google.cloud.functions_v2.types.functions import GenerateDownloadUrlRequest
from google.cloud.functions_v2.types.functions import GenerateDownloadUrlResponse
from google.cloud.functions_v2.types.functions import GenerateUploadUrlRequest
from google.cloud.functions_v2.types.functions import GenerateUploadUrlResponse
from google.cloud.functions_v2.types.functions import GetFunctionRequest
from google.cloud.functions_v2.types.functions import ListFunctionsRequest
from google.cloud.functions_v2.types.functions import ListFunctionsResponse
from google.cloud.functions_v2.types.functions import ListRuntimesRequest
from google.cloud.functions_v2.types.functions import ListRuntimesResponse
from google.cloud.functions_v2.types.functions import LocationMetadata
from google.cloud.functions_v2.types.functions import OperationMetadata
from google.cloud.functions_v2.types.functions import RepoSource
from google.cloud.functions_v2.types.functions import SecretEnvVar
from google.cloud.functions_v2.types.functions import SecretVolume
from google.cloud.functions_v2.types.functions import ServiceConfig
from google.cloud.functions_v2.types.functions import Source
from google.cloud.functions_v2.types.functions import SourceProvenance
from google.cloud.functions_v2.types.functions import Stage
from google.cloud.functions_v2.types.functions import StateMessage
from google.cloud.functions_v2.types.functions import StorageSource
from google.cloud.functions_v2.types.functions import UpdateFunctionRequest
from google.cloud.functions_v2.types.functions import Environment

__all__ = ('FunctionServiceClient',
    'FunctionServiceAsyncClient',
    'BuildConfig',
    'CreateFunctionRequest',
    'DeleteFunctionRequest',
    'EventFilter',
    'EventTrigger',
    'Function',
    'GenerateDownloadUrlRequest',
    'GenerateDownloadUrlResponse',
    'GenerateUploadUrlRequest',
    'GenerateUploadUrlResponse',
    'GetFunctionRequest',
    'ListFunctionsRequest',
    'ListFunctionsResponse',
    'ListRuntimesRequest',
    'ListRuntimesResponse',
    'LocationMetadata',
    'OperationMetadata',
    'RepoSource',
    'SecretEnvVar',
    'SecretVolume',
    'ServiceConfig',
    'Source',
    'SourceProvenance',
    'Stage',
    'StateMessage',
    'StorageSource',
    'UpdateFunctionRequest',
    'Environment',
)
