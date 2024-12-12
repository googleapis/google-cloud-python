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
from google.cloud.memorystore import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.memorystore_v1beta.services.memorystore.client import MemorystoreClient

from google.cloud.memorystore_v1beta.types.memorystore import CertificateAuthority
from google.cloud.memorystore_v1beta.types.memorystore import CreateInstanceRequest
from google.cloud.memorystore_v1beta.types.memorystore import DeleteInstanceRequest
from google.cloud.memorystore_v1beta.types.memorystore import DiscoveryEndpoint
from google.cloud.memorystore_v1beta.types.memorystore import GetCertificateAuthorityRequest
from google.cloud.memorystore_v1beta.types.memorystore import GetInstanceRequest
from google.cloud.memorystore_v1beta.types.memorystore import Instance
from google.cloud.memorystore_v1beta.types.memorystore import ListInstancesRequest
from google.cloud.memorystore_v1beta.types.memorystore import ListInstancesResponse
from google.cloud.memorystore_v1beta.types.memorystore import NodeConfig
from google.cloud.memorystore_v1beta.types.memorystore import OperationMetadata
from google.cloud.memorystore_v1beta.types.memorystore import PersistenceConfig
from google.cloud.memorystore_v1beta.types.memorystore import PscAutoConnection
from google.cloud.memorystore_v1beta.types.memorystore import PscConnection
from google.cloud.memorystore_v1beta.types.memorystore import UpdateInstanceRequest
from google.cloud.memorystore_v1beta.types.memorystore import ZoneDistributionConfig
from google.cloud.memorystore_v1beta.types.memorystore import ConnectionType
from google.cloud.memorystore_v1beta.types.memorystore import PscConnectionStatus

__all__ = ('MemorystoreClient',
    'CertificateAuthority',
    'CreateInstanceRequest',
    'DeleteInstanceRequest',
    'DiscoveryEndpoint',
    'GetCertificateAuthorityRequest',
    'GetInstanceRequest',
    'Instance',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'NodeConfig',
    'OperationMetadata',
    'PersistenceConfig',
    'PscAutoConnection',
    'PscConnection',
    'UpdateInstanceRequest',
    'ZoneDistributionConfig',
    'ConnectionType',
    'PscConnectionStatus',
)
