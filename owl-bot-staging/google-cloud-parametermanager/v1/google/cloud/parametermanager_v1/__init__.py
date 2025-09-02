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
from google.cloud.parametermanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.parameter_manager import ParameterManagerClient
from .services.parameter_manager import ParameterManagerAsyncClient

from .types.service import CreateParameterRequest
from .types.service import CreateParameterVersionRequest
from .types.service import DeleteParameterRequest
from .types.service import DeleteParameterVersionRequest
from .types.service import GetParameterRequest
from .types.service import GetParameterVersionRequest
from .types.service import ListParametersRequest
from .types.service import ListParametersResponse
from .types.service import ListParameterVersionsRequest
from .types.service import ListParameterVersionsResponse
from .types.service import Parameter
from .types.service import ParameterVersion
from .types.service import ParameterVersionPayload
from .types.service import RenderParameterVersionRequest
from .types.service import RenderParameterVersionResponse
from .types.service import UpdateParameterRequest
from .types.service import UpdateParameterVersionRequest
from .types.service import ParameterFormat
from .types.service import View

__all__ = (
    'ParameterManagerAsyncClient',
'CreateParameterRequest',
'CreateParameterVersionRequest',
'DeleteParameterRequest',
'DeleteParameterVersionRequest',
'GetParameterRequest',
'GetParameterVersionRequest',
'ListParameterVersionsRequest',
'ListParameterVersionsResponse',
'ListParametersRequest',
'ListParametersResponse',
'Parameter',
'ParameterFormat',
'ParameterManagerClient',
'ParameterVersion',
'ParameterVersionPayload',
'RenderParameterVersionRequest',
'RenderParameterVersionResponse',
'UpdateParameterRequest',
'UpdateParameterVersionRequest',
'View',
)
