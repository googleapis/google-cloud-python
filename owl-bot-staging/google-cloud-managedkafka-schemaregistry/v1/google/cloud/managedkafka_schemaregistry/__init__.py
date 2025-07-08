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
from google.cloud.managedkafka_schemaregistry import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.managedkafka_schemaregistry_v1.services.managed_schema_registry.client import ManagedSchemaRegistryClient
from google.cloud.managedkafka_schemaregistry_v1.services.managed_schema_registry.async_client import ManagedSchemaRegistryAsyncClient

from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import CheckCompatibilityRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import CheckCompatibilityResponse
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import CreateSchemaRegistryRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import CreateVersionRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import CreateVersionResponse
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import DeleteSchemaConfigRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import DeleteSchemaModeRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import DeleteSchemaRegistryRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import DeleteSubjectRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import DeleteVersionRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetContextRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetSchemaConfigRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetSchemaModeRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetSchemaRegistryRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetSchemaRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import GetVersionRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListContextsRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListReferencedSchemasRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSchemaRegistriesRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSchemaRegistriesResponse
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSchemaTypesRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSchemaVersionsRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSubjectsBySchemaIdRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListSubjectsRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import ListVersionsRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import LookupVersionRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import UpdateSchemaConfigRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry import UpdateSchemaModeRequest
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import Context
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import Schema
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import SchemaConfig
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import SchemaMode
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import SchemaRegistry
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import SchemaSubject
from google.cloud.managedkafka_schemaregistry_v1.types.schema_registry_resources import SchemaVersion

__all__ = ('ManagedSchemaRegistryClient',
    'ManagedSchemaRegistryAsyncClient',
    'CheckCompatibilityRequest',
    'CheckCompatibilityResponse',
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
    'UpdateSchemaConfigRequest',
    'UpdateSchemaModeRequest',
    'Context',
    'Schema',
    'SchemaConfig',
    'SchemaMode',
    'SchemaRegistry',
    'SchemaSubject',
    'SchemaVersion',
)
