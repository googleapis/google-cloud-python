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
from google.cloud.servicecontrol_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.service_controller import ServiceControllerClient
from .services.service_controller import ServiceControllerAsyncClient

from .types.service_controller import CheckRequest
from .types.service_controller import CheckResponse
from .types.service_controller import ReportRequest
from .types.service_controller import ReportResponse
from .types.service_controller import ResourceInfo
from .types.service_controller import ResourceInfoList

__all__ = (
    'ServiceControllerAsyncClient',
'CheckRequest',
'CheckResponse',
'ReportRequest',
'ReportResponse',
'ResourceInfo',
'ResourceInfoList',
'ServiceControllerClient',
)
