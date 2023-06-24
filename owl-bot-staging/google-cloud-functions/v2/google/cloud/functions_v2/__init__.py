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
from google.cloud.functions_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.function_service import FunctionServiceClient
from .services.function_service import FunctionServiceAsyncClient

from .types.functions import BuildConfig
from .types.functions import CreateFunctionRequest
from .types.functions import DeleteFunctionRequest
from .types.functions import EventFilter
from .types.functions import EventTrigger
from .types.functions import Function
from .types.functions import GenerateDownloadUrlRequest
from .types.functions import GenerateDownloadUrlResponse
from .types.functions import GenerateUploadUrlRequest
from .types.functions import GenerateUploadUrlResponse
from .types.functions import GetFunctionRequest
from .types.functions import ListFunctionsRequest
from .types.functions import ListFunctionsResponse
from .types.functions import ListRuntimesRequest
from .types.functions import ListRuntimesResponse
from .types.functions import LocationMetadata
from .types.functions import OperationMetadata
from .types.functions import RepoSource
from .types.functions import SecretEnvVar
from .types.functions import SecretVolume
from .types.functions import ServiceConfig
from .types.functions import Source
from .types.functions import SourceProvenance
from .types.functions import Stage
from .types.functions import StateMessage
from .types.functions import StorageSource
from .types.functions import UpdateFunctionRequest
from .types.functions import Environment

__all__ = (
    'FunctionServiceAsyncClient',
'BuildConfig',
'CreateFunctionRequest',
'DeleteFunctionRequest',
'Environment',
'EventFilter',
'EventTrigger',
'Function',
'FunctionServiceClient',
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
)
