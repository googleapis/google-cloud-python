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
from google.cloud.vpcaccess import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.vpcaccess_v1.services.vpc_access_service.client import VpcAccessServiceClient
from google.cloud.vpcaccess_v1.services.vpc_access_service.async_client import VpcAccessServiceAsyncClient

from google.cloud.vpcaccess_v1.types.vpc_access import Connector
from google.cloud.vpcaccess_v1.types.vpc_access import CreateConnectorRequest
from google.cloud.vpcaccess_v1.types.vpc_access import DeleteConnectorRequest
from google.cloud.vpcaccess_v1.types.vpc_access import GetConnectorRequest
from google.cloud.vpcaccess_v1.types.vpc_access import ListConnectorsRequest
from google.cloud.vpcaccess_v1.types.vpc_access import ListConnectorsResponse
from google.cloud.vpcaccess_v1.types.vpc_access import OperationMetadata

__all__ = ('VpcAccessServiceClient',
    'VpcAccessServiceAsyncClient',
    'Connector',
    'CreateConnectorRequest',
    'DeleteConnectorRequest',
    'GetConnectorRequest',
    'ListConnectorsRequest',
    'ListConnectorsResponse',
    'OperationMetadata',
)
