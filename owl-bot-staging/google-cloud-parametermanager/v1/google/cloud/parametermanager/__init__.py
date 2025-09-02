# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.parametermanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.parametermanager_v1.services.parameter_manager.client import ParameterManagerClient
from google.cloud.parametermanager_v1.services.parameter_manager.async_client import ParameterManagerAsyncClient

from google.cloud.parametermanager_v1.types.service import CreateParameterRequest
from google.cloud.parametermanager_v1.types.service import CreateParameterVersionRequest
from google.cloud.parametermanager_v1.types.service import DeleteParameterRequest
from google.cloud.parametermanager_v1.types.service import DeleteParameterVersionRequest
from google.cloud.parametermanager_v1.types.service import GetParameterRequest
from google.cloud.parametermanager_v1.types.service import GetParameterVersionRequest
from google.cloud.parametermanager_v1.types.service import ListParametersRequest
from google.cloud.parametermanager_v1.types.service import ListParametersResponse
from google.cloud.parametermanager_v1.types.service import ListParameterVersionsRequest
from google.cloud.parametermanager_v1.types.service import ListParameterVersionsResponse
from google.cloud.parametermanager_v1.types.service import Parameter
from google.cloud.parametermanager_v1.types.service import ParameterVersion
from google.cloud.parametermanager_v1.types.service import ParameterVersionPayload
from google.cloud.parametermanager_v1.types.service import RenderParameterVersionRequest
from google.cloud.parametermanager_v1.types.service import RenderParameterVersionResponse
from google.cloud.parametermanager_v1.types.service import UpdateParameterRequest
from google.cloud.parametermanager_v1.types.service import UpdateParameterVersionRequest
from google.cloud.parametermanager_v1.types.service import ParameterFormat
from google.cloud.parametermanager_v1.types.service import View

__all__ = ('ParameterManagerClient',
    'ParameterManagerAsyncClient',
    'CreateParameterRequest',
    'CreateParameterVersionRequest',
    'DeleteParameterRequest',
    'DeleteParameterVersionRequest',
    'GetParameterRequest',
    'GetParameterVersionRequest',
    'ListParametersRequest',
    'ListParametersResponse',
    'ListParameterVersionsRequest',
    'ListParameterVersionsResponse',
    'Parameter',
    'ParameterVersion',
    'ParameterVersionPayload',
    'RenderParameterVersionRequest',
    'RenderParameterVersionResponse',
    'UpdateParameterRequest',
    'UpdateParameterVersionRequest',
    'ParameterFormat',
    'View',
)
