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
from google.cloud.vpcaccess_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.vpc_access_service import VpcAccessServiceClient
from .services.vpc_access_service import VpcAccessServiceAsyncClient

from .types.vpc_access import Connector
from .types.vpc_access import CreateConnectorRequest
from .types.vpc_access import DeleteConnectorRequest
from .types.vpc_access import GetConnectorRequest
from .types.vpc_access import ListConnectorsRequest
from .types.vpc_access import ListConnectorsResponse
from .types.vpc_access import OperationMetadata

__all__ = (
    'VpcAccessServiceAsyncClient',
'Connector',
'CreateConnectorRequest',
'DeleteConnectorRequest',
'GetConnectorRequest',
'ListConnectorsRequest',
'ListConnectorsResponse',
'OperationMetadata',
'VpcAccessServiceClient',
)
