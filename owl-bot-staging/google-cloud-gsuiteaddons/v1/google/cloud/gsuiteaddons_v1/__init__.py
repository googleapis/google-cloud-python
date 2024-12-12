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
from google.cloud.gsuiteaddons_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.g_suite_add_ons import GSuiteAddOnsClient
from .services.g_suite_add_ons import GSuiteAddOnsAsyncClient

from .types.gsuiteaddons import AddOns
from .types.gsuiteaddons import Authorization
from .types.gsuiteaddons import CreateDeploymentRequest
from .types.gsuiteaddons import DeleteDeploymentRequest
from .types.gsuiteaddons import Deployment
from .types.gsuiteaddons import GetAuthorizationRequest
from .types.gsuiteaddons import GetDeploymentRequest
from .types.gsuiteaddons import GetInstallStatusRequest
from .types.gsuiteaddons import InstallDeploymentRequest
from .types.gsuiteaddons import InstallStatus
from .types.gsuiteaddons import ListDeploymentsRequest
from .types.gsuiteaddons import ListDeploymentsResponse
from .types.gsuiteaddons import ReplaceDeploymentRequest
from .types.gsuiteaddons import UninstallDeploymentRequest

__all__ = (
    'GSuiteAddOnsAsyncClient',
'AddOns',
'Authorization',
'CreateDeploymentRequest',
'DeleteDeploymentRequest',
'Deployment',
'GSuiteAddOnsClient',
'GetAuthorizationRequest',
'GetDeploymentRequest',
'GetInstallStatusRequest',
'InstallDeploymentRequest',
'InstallStatus',
'ListDeploymentsRequest',
'ListDeploymentsResponse',
'ReplaceDeploymentRequest',
'UninstallDeploymentRequest',
)
