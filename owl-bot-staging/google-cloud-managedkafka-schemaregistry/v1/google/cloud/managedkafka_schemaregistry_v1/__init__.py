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
from google.cloud.managedkafka_schemaregistry_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.managed_schema_registry import ManagedSchemaRegistryClient
from .services.managed_schema_registry import ManagedSchemaRegistryAsyncClient

from .types.schema_registry import CheckCompatibilityRequest
from .types.schema_registry import CheckCompatibilityResponse
from .types.schema_registry import CreateSchemaRegistryRequest
from .types.schema_registry import CreateVersionRequest
from .types.schema_registry import CreateVersionResponse
from .types.schema_registry import DeleteSchemaConfigRequest
from .types.schema_registry import DeleteSchemaModeRequest
from .types.schema_registry import DeleteSchemaRegistryRequest
from .types.schema_registry import DeleteSubjectRequest
from .types.schema_registry import DeleteVersionRequest
from .types.schema_registry import GetContextRequest
from .types.schema_registry import GetSchemaConfigRequest
from .types.schema_registry import GetSchemaModeRequest
from .types.schema_registry import GetSchemaRegistryRequest
from .types.schema_registry import GetSchemaRequest
from .types.schema_registry import GetVersionRequest
from .types.schema_registry import ListContextsRequest
from .types.schema_registry import ListReferencedSchemasRequest
from .types.schema_registry import ListSchemaRegistriesRequest
from .types.schema_registry import ListSchemaRegistriesResponse
from .types.schema_registry import ListSchemaTypesRequest
from .types.schema_registry import ListSchemaVersionsRequest
from .types.schema_registry import ListSubjectsBySchemaIdRequest
from .types.schema_registry import ListSubjectsRequest
from .types.schema_registry import ListVersionsRequest
from .types.schema_registry import LookupVersionRequest
from .types.schema_registry import UpdateSchemaConfigRequest
from .types.schema_registry import UpdateSchemaModeRequest
from .types.schema_registry_resources import Context
from .types.schema_registry_resources import Schema
from .types.schema_registry_resources import SchemaConfig
from .types.schema_registry_resources import SchemaMode
from .types.schema_registry_resources import SchemaRegistry
from .types.schema_registry_resources import SchemaSubject
from .types.schema_registry_resources import SchemaVersion

__all__ = (
    'ManagedSchemaRegistryAsyncClient',
'CheckCompatibilityRequest',
'CheckCompatibilityResponse',
'Context',
'CreateSchemaRegistryRequest',
'CreateVersionRequest',
'CreateVersionResponse',
'DeleteSchemaConfigRequest',
'DeleteSchemaModeRequest',
'DeleteSchemaRegistryRequest',
'DeleteSubjectRequest',
'DeleteVersionRequest',
'GetContextRequest',
'GetSchemaConfigRequest',
'GetSchemaModeRequest',
'GetSchemaRegistryRequest',
'GetSchemaRequest',
'GetVersionRequest',
'ListContextsRequest',
'ListReferencedSchemasRequest',
'ListSchemaRegistriesRequest',
'ListSchemaRegistriesResponse',
'ListSchemaTypesRequest',
'ListSchemaVersionsRequest',
'ListSubjectsBySchemaIdRequest',
'ListSubjectsRequest',
'ListVersionsRequest',
'LookupVersionRequest',
'ManagedSchemaRegistryClient',
'Schema',
'SchemaConfig',
'SchemaMode',
'SchemaRegistry',
'SchemaSubject',
'SchemaVersion',
'UpdateSchemaConfigRequest',
'UpdateSchemaModeRequest',
)
