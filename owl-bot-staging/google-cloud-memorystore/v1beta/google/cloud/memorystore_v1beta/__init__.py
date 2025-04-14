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
from google.cloud.memorystore_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.memorystore import MemorystoreClient

from .types.memorystore import CertificateAuthority
from .types.memorystore import CreateInstanceRequest
from .types.memorystore import DeleteInstanceRequest
from .types.memorystore import DiscoveryEndpoint
from .types.memorystore import GetCertificateAuthorityRequest
from .types.memorystore import GetInstanceRequest
from .types.memorystore import Instance
from .types.memorystore import ListInstancesRequest
from .types.memorystore import ListInstancesResponse
from .types.memorystore import NodeConfig
from .types.memorystore import OperationMetadata
from .types.memorystore import PersistenceConfig
from .types.memorystore import PscAutoConnection
from .types.memorystore import PscConnection
from .types.memorystore import UpdateInstanceRequest
from .types.memorystore import ZoneDistributionConfig
from .types.memorystore import ConnectionType
from .types.memorystore import PscConnectionStatus

__all__ = (
'CertificateAuthority',
'ConnectionType',
'CreateInstanceRequest',
'DeleteInstanceRequest',
'DiscoveryEndpoint',
'GetCertificateAuthorityRequest',
'GetInstanceRequest',
'Instance',
'ListInstancesRequest',
'ListInstancesResponse',
'MemorystoreClient',
'NodeConfig',
'OperationMetadata',
'PersistenceConfig',
'PscAutoConnection',
'PscConnection',
'PscConnectionStatus',
'UpdateInstanceRequest',
'ZoneDistributionConfig',
)
