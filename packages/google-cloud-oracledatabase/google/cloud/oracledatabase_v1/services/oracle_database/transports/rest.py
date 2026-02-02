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
import dataclasses
import json  # type: ignore
import logging
import warnings
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import google.protobuf
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.oracledatabase_v1.types import (
    autonomous_database,
    database,
    database_character_set,
    db_system,
    db_system_initial_storage_size,
    db_version,
    exadata_infra,
    exadb_vm_cluster,
    exascale_db_storage_vault,
    minor_version,
    odb_network,
    odb_subnet,
    oracledatabase,
    pluggable_database,
    vm_cluster,
)
from google.cloud.oracledatabase_v1.types import db_system as gco_db_system
from google.cloud.oracledatabase_v1.types import (
    exascale_db_storage_vault as gco_exascale_db_storage_vault,
)
from google.cloud.oracledatabase_v1.types import odb_network as gco_odb_network
from google.cloud.oracledatabase_v1.types import odb_subnet as gco_odb_subnet

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseOracleDatabaseRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class OracleDatabaseRestInterceptor:
    """Interceptor for OracleDatabase.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the OracleDatabaseRestTransport.

    .. code-block:: python
        class MyCustomOracleDatabaseInterceptor(OracleDatabaseRestInterceptor):
            def pre_create_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_cloud_exadata_infrastructure(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cloud_exadata_infrastructure(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_cloud_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cloud_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_db_system(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_db_system(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_exadb_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_exadb_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_exascale_db_storage_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_exascale_db_storage_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_odb_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_odb_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_odb_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_odb_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cloud_exadata_infrastructure(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cloud_exadata_infrastructure(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cloud_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cloud_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_db_system(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_db_system(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_exadb_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_exadb_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_exascale_db_storage_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_exascale_db_storage_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_odb_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_odb_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_odb_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_odb_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_failover_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_failover_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_autonomous_database_wallet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_autonomous_database_wallet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cloud_exadata_infrastructure(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cloud_exadata_infrastructure(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cloud_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cloud_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_db_system(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_db_system(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_exadb_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_exadb_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_exascale_db_storage_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_exascale_db_storage_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_odb_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_odb_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_odb_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_odb_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_pluggable_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_pluggable_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_autonomous_database_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_autonomous_database_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_autonomous_database_character_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_autonomous_database_character_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_autonomous_databases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_autonomous_databases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_autonomous_db_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_autonomous_db_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cloud_exadata_infrastructures(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cloud_exadata_infrastructures(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cloud_vm_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cloud_vm_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_database_character_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_database_character_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_databases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_databases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_nodes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_nodes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_servers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_servers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_system_initial_storage_sizes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_system_initial_storage_sizes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_systems(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_systems(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_system_shapes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_system_shapes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_db_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entitlements(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entitlements(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_exadb_vm_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_exadb_vm_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_exascale_db_storage_vaults(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_exascale_db_storage_vaults(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_gi_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_gi_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_minor_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_minor_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_odb_networks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_odb_networks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_odb_subnets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_odb_subnets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_pluggable_databases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_pluggable_databases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_virtual_machine_exadb_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_virtual_machine_exadb_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restart_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restart_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_switchover_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_switchover_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_exadb_vm_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_exadb_vm_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OracleDatabaseRestTransport(interceptor=MyCustomOracleDatabaseInterceptor())
        client = OracleDatabaseClient(transport=transport)


    """

    def pre_create_autonomous_database(
        self,
        request: oracledatabase.CreateAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.CreateAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_autonomous_database

        DEPRECATED. Please use the `post_create_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_autonomous_database` interceptor runs
        before the `post_create_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_create_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_create_autonomous_database` interceptor.
        When both interceptors are used, this `post_create_autonomous_database_with_metadata` interceptor runs after the
        `post_create_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_create_autonomous_database` will be passed to
        `post_create_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_create_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.CreateCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.CreateCloudExadataInfrastructureRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_cloud_exadata_infrastructure

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_cloud_exadata_infrastructure(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cloud_exadata_infrastructure

        DEPRECATED. Please use the `post_create_cloud_exadata_infrastructure_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_cloud_exadata_infrastructure` interceptor runs
        before the `post_create_cloud_exadata_infrastructure_with_metadata` interceptor.
        """
        return response

    def post_create_cloud_exadata_infrastructure_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_cloud_exadata_infrastructure

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_cloud_exadata_infrastructure_with_metadata`
        interceptor in new development instead of the `post_create_cloud_exadata_infrastructure` interceptor.
        When both interceptors are used, this `post_create_cloud_exadata_infrastructure_with_metadata` interceptor runs after the
        `post_create_cloud_exadata_infrastructure` interceptor. The (possibly modified) response returned by
        `post_create_cloud_exadata_infrastructure` will be passed to
        `post_create_cloud_exadata_infrastructure_with_metadata`.
        """
        return response, metadata

    def pre_create_cloud_vm_cluster(
        self,
        request: oracledatabase.CreateCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.CreateCloudVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_cloud_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cloud_vm_cluster

        DEPRECATED. Please use the `post_create_cloud_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_cloud_vm_cluster` interceptor runs
        before the `post_create_cloud_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_create_cloud_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_cloud_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_cloud_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_create_cloud_vm_cluster` interceptor.
        When both interceptors are used, this `post_create_cloud_vm_cluster_with_metadata` interceptor runs after the
        `post_create_cloud_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_create_cloud_vm_cluster` will be passed to
        `post_create_cloud_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_create_db_system(
        self,
        request: gco_db_system.CreateDbSystemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gco_db_system.CreateDbSystemRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_db_system

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_db_system(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_db_system

        DEPRECATED. Please use the `post_create_db_system_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_db_system` interceptor runs
        before the `post_create_db_system_with_metadata` interceptor.
        """
        return response

    def post_create_db_system_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_db_system

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_db_system_with_metadata`
        interceptor in new development instead of the `post_create_db_system` interceptor.
        When both interceptors are used, this `post_create_db_system_with_metadata` interceptor runs after the
        `post_create_db_system` interceptor. The (possibly modified) response returned by
        `post_create_db_system` will be passed to
        `post_create_db_system_with_metadata`.
        """
        return response, metadata

    def pre_create_exadb_vm_cluster(
        self,
        request: oracledatabase.CreateExadbVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.CreateExadbVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_exadb_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_exadb_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_exadb_vm_cluster

        DEPRECATED. Please use the `post_create_exadb_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_exadb_vm_cluster` interceptor runs
        before the `post_create_exadb_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_create_exadb_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_exadb_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_exadb_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_create_exadb_vm_cluster` interceptor.
        When both interceptors are used, this `post_create_exadb_vm_cluster_with_metadata` interceptor runs after the
        `post_create_exadb_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_create_exadb_vm_cluster` will be passed to
        `post_create_exadb_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_create_exascale_db_storage_vault(
        self,
        request: gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_exascale_db_storage_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_exascale_db_storage_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_exascale_db_storage_vault

        DEPRECATED. Please use the `post_create_exascale_db_storage_vault_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_exascale_db_storage_vault` interceptor runs
        before the `post_create_exascale_db_storage_vault_with_metadata` interceptor.
        """
        return response

    def post_create_exascale_db_storage_vault_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_exascale_db_storage_vault

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_exascale_db_storage_vault_with_metadata`
        interceptor in new development instead of the `post_create_exascale_db_storage_vault` interceptor.
        When both interceptors are used, this `post_create_exascale_db_storage_vault_with_metadata` interceptor runs after the
        `post_create_exascale_db_storage_vault` interceptor. The (possibly modified) response returned by
        `post_create_exascale_db_storage_vault` will be passed to
        `post_create_exascale_db_storage_vault_with_metadata`.
        """
        return response, metadata

    def pre_create_odb_network(
        self,
        request: gco_odb_network.CreateOdbNetworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gco_odb_network.CreateOdbNetworkRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_odb_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_odb_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_odb_network

        DEPRECATED. Please use the `post_create_odb_network_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_odb_network` interceptor runs
        before the `post_create_odb_network_with_metadata` interceptor.
        """
        return response

    def post_create_odb_network_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_odb_network

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_odb_network_with_metadata`
        interceptor in new development instead of the `post_create_odb_network` interceptor.
        When both interceptors are used, this `post_create_odb_network_with_metadata` interceptor runs after the
        `post_create_odb_network` interceptor. The (possibly modified) response returned by
        `post_create_odb_network` will be passed to
        `post_create_odb_network_with_metadata`.
        """
        return response, metadata

    def pre_create_odb_subnet(
        self,
        request: gco_odb_subnet.CreateOdbSubnetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gco_odb_subnet.CreateOdbSubnetRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_odb_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_odb_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_odb_subnet

        DEPRECATED. Please use the `post_create_odb_subnet_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_create_odb_subnet` interceptor runs
        before the `post_create_odb_subnet_with_metadata` interceptor.
        """
        return response

    def post_create_odb_subnet_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_odb_subnet

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_create_odb_subnet_with_metadata`
        interceptor in new development instead of the `post_create_odb_subnet` interceptor.
        When both interceptors are used, this `post_create_odb_subnet_with_metadata` interceptor runs after the
        `post_create_odb_subnet` interceptor. The (possibly modified) response returned by
        `post_create_odb_subnet` will be passed to
        `post_create_odb_subnet_with_metadata`.
        """
        return response, metadata

    def pre_delete_autonomous_database(
        self,
        request: oracledatabase.DeleteAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.DeleteAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_autonomous_database

        DEPRECATED. Please use the `post_delete_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_autonomous_database` interceptor runs
        before the `post_delete_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_delete_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_delete_autonomous_database` interceptor.
        When both interceptors are used, this `post_delete_autonomous_database_with_metadata` interceptor runs after the
        `post_delete_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_delete_autonomous_database` will be passed to
        `post_delete_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_delete_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.DeleteCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.DeleteCloudExadataInfrastructureRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_cloud_exadata_infrastructure

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_cloud_exadata_infrastructure(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cloud_exadata_infrastructure

        DEPRECATED. Please use the `post_delete_cloud_exadata_infrastructure_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_cloud_exadata_infrastructure` interceptor runs
        before the `post_delete_cloud_exadata_infrastructure_with_metadata` interceptor.
        """
        return response

    def post_delete_cloud_exadata_infrastructure_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_cloud_exadata_infrastructure

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_cloud_exadata_infrastructure_with_metadata`
        interceptor in new development instead of the `post_delete_cloud_exadata_infrastructure` interceptor.
        When both interceptors are used, this `post_delete_cloud_exadata_infrastructure_with_metadata` interceptor runs after the
        `post_delete_cloud_exadata_infrastructure` interceptor. The (possibly modified) response returned by
        `post_delete_cloud_exadata_infrastructure` will be passed to
        `post_delete_cloud_exadata_infrastructure_with_metadata`.
        """
        return response, metadata

    def pre_delete_cloud_vm_cluster(
        self,
        request: oracledatabase.DeleteCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.DeleteCloudVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_cloud_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cloud_vm_cluster

        DEPRECATED. Please use the `post_delete_cloud_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_cloud_vm_cluster` interceptor runs
        before the `post_delete_cloud_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_delete_cloud_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_cloud_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_cloud_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_delete_cloud_vm_cluster` interceptor.
        When both interceptors are used, this `post_delete_cloud_vm_cluster_with_metadata` interceptor runs after the
        `post_delete_cloud_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_delete_cloud_vm_cluster` will be passed to
        `post_delete_cloud_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_delete_db_system(
        self,
        request: db_system.DeleteDbSystemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_system.DeleteDbSystemRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_db_system

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_db_system(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_db_system

        DEPRECATED. Please use the `post_delete_db_system_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_db_system` interceptor runs
        before the `post_delete_db_system_with_metadata` interceptor.
        """
        return response

    def post_delete_db_system_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_db_system

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_db_system_with_metadata`
        interceptor in new development instead of the `post_delete_db_system` interceptor.
        When both interceptors are used, this `post_delete_db_system_with_metadata` interceptor runs after the
        `post_delete_db_system` interceptor. The (possibly modified) response returned by
        `post_delete_db_system` will be passed to
        `post_delete_db_system_with_metadata`.
        """
        return response, metadata

    def pre_delete_exadb_vm_cluster(
        self,
        request: oracledatabase.DeleteExadbVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.DeleteExadbVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_exadb_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_exadb_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_exadb_vm_cluster

        DEPRECATED. Please use the `post_delete_exadb_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_exadb_vm_cluster` interceptor runs
        before the `post_delete_exadb_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_delete_exadb_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_exadb_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_exadb_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_delete_exadb_vm_cluster` interceptor.
        When both interceptors are used, this `post_delete_exadb_vm_cluster_with_metadata` interceptor runs after the
        `post_delete_exadb_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_delete_exadb_vm_cluster` will be passed to
        `post_delete_exadb_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_delete_exascale_db_storage_vault(
        self,
        request: exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_exascale_db_storage_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_exascale_db_storage_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_exascale_db_storage_vault

        DEPRECATED. Please use the `post_delete_exascale_db_storage_vault_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_exascale_db_storage_vault` interceptor runs
        before the `post_delete_exascale_db_storage_vault_with_metadata` interceptor.
        """
        return response

    def post_delete_exascale_db_storage_vault_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_exascale_db_storage_vault

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_exascale_db_storage_vault_with_metadata`
        interceptor in new development instead of the `post_delete_exascale_db_storage_vault` interceptor.
        When both interceptors are used, this `post_delete_exascale_db_storage_vault_with_metadata` interceptor runs after the
        `post_delete_exascale_db_storage_vault` interceptor. The (possibly modified) response returned by
        `post_delete_exascale_db_storage_vault` will be passed to
        `post_delete_exascale_db_storage_vault_with_metadata`.
        """
        return response, metadata

    def pre_delete_odb_network(
        self,
        request: odb_network.DeleteOdbNetworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_network.DeleteOdbNetworkRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_odb_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_odb_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_odb_network

        DEPRECATED. Please use the `post_delete_odb_network_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_odb_network` interceptor runs
        before the `post_delete_odb_network_with_metadata` interceptor.
        """
        return response

    def post_delete_odb_network_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_odb_network

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_odb_network_with_metadata`
        interceptor in new development instead of the `post_delete_odb_network` interceptor.
        When both interceptors are used, this `post_delete_odb_network_with_metadata` interceptor runs after the
        `post_delete_odb_network` interceptor. The (possibly modified) response returned by
        `post_delete_odb_network` will be passed to
        `post_delete_odb_network_with_metadata`.
        """
        return response, metadata

    def pre_delete_odb_subnet(
        self,
        request: odb_subnet.DeleteOdbSubnetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_subnet.DeleteOdbSubnetRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_odb_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_odb_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_odb_subnet

        DEPRECATED. Please use the `post_delete_odb_subnet_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_delete_odb_subnet` interceptor runs
        before the `post_delete_odb_subnet_with_metadata` interceptor.
        """
        return response

    def post_delete_odb_subnet_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_odb_subnet

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_delete_odb_subnet_with_metadata`
        interceptor in new development instead of the `post_delete_odb_subnet` interceptor.
        When both interceptors are used, this `post_delete_odb_subnet_with_metadata` interceptor runs after the
        `post_delete_odb_subnet` interceptor. The (possibly modified) response returned by
        `post_delete_odb_subnet` will be passed to
        `post_delete_odb_subnet_with_metadata`.
        """
        return response, metadata

    def pre_failover_autonomous_database(
        self,
        request: oracledatabase.FailoverAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.FailoverAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for failover_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_failover_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for failover_autonomous_database

        DEPRECATED. Please use the `post_failover_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_failover_autonomous_database` interceptor runs
        before the `post_failover_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_failover_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for failover_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_failover_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_failover_autonomous_database` interceptor.
        When both interceptors are used, this `post_failover_autonomous_database_with_metadata` interceptor runs after the
        `post_failover_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_failover_autonomous_database` will be passed to
        `post_failover_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_generate_autonomous_database_wallet(
        self,
        request: oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for generate_autonomous_database_wallet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_generate_autonomous_database_wallet(
        self, response: oracledatabase.GenerateAutonomousDatabaseWalletResponse
    ) -> oracledatabase.GenerateAutonomousDatabaseWalletResponse:
        """Post-rpc interceptor for generate_autonomous_database_wallet

        DEPRECATED. Please use the `post_generate_autonomous_database_wallet_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_generate_autonomous_database_wallet` interceptor runs
        before the `post_generate_autonomous_database_wallet_with_metadata` interceptor.
        """
        return response

    def post_generate_autonomous_database_wallet_with_metadata(
        self,
        response: oracledatabase.GenerateAutonomousDatabaseWalletResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GenerateAutonomousDatabaseWalletResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for generate_autonomous_database_wallet

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_generate_autonomous_database_wallet_with_metadata`
        interceptor in new development instead of the `post_generate_autonomous_database_wallet` interceptor.
        When both interceptors are used, this `post_generate_autonomous_database_wallet_with_metadata` interceptor runs after the
        `post_generate_autonomous_database_wallet` interceptor. The (possibly modified) response returned by
        `post_generate_autonomous_database_wallet` will be passed to
        `post_generate_autonomous_database_wallet_with_metadata`.
        """
        return response, metadata

    def pre_get_autonomous_database(
        self,
        request: oracledatabase.GetAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GetAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_autonomous_database(
        self, response: autonomous_database.AutonomousDatabase
    ) -> autonomous_database.AutonomousDatabase:
        """Post-rpc interceptor for get_autonomous_database

        DEPRECATED. Please use the `post_get_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_autonomous_database` interceptor runs
        before the `post_get_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_get_autonomous_database_with_metadata(
        self,
        response: autonomous_database.AutonomousDatabase,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        autonomous_database.AutonomousDatabase, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_get_autonomous_database` interceptor.
        When both interceptors are used, this `post_get_autonomous_database_with_metadata` interceptor runs after the
        `post_get_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_get_autonomous_database` will be passed to
        `post_get_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_get_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.GetCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GetCloudExadataInfrastructureRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_cloud_exadata_infrastructure

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_cloud_exadata_infrastructure(
        self, response: exadata_infra.CloudExadataInfrastructure
    ) -> exadata_infra.CloudExadataInfrastructure:
        """Post-rpc interceptor for get_cloud_exadata_infrastructure

        DEPRECATED. Please use the `post_get_cloud_exadata_infrastructure_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_cloud_exadata_infrastructure` interceptor runs
        before the `post_get_cloud_exadata_infrastructure_with_metadata` interceptor.
        """
        return response

    def post_get_cloud_exadata_infrastructure_with_metadata(
        self,
        response: exadata_infra.CloudExadataInfrastructure,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exadata_infra.CloudExadataInfrastructure,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for get_cloud_exadata_infrastructure

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_cloud_exadata_infrastructure_with_metadata`
        interceptor in new development instead of the `post_get_cloud_exadata_infrastructure` interceptor.
        When both interceptors are used, this `post_get_cloud_exadata_infrastructure_with_metadata` interceptor runs after the
        `post_get_cloud_exadata_infrastructure` interceptor. The (possibly modified) response returned by
        `post_get_cloud_exadata_infrastructure` will be passed to
        `post_get_cloud_exadata_infrastructure_with_metadata`.
        """
        return response, metadata

    def pre_get_cloud_vm_cluster(
        self,
        request: oracledatabase.GetCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GetCloudVmClusterRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_cloud_vm_cluster(
        self, response: vm_cluster.CloudVmCluster
    ) -> vm_cluster.CloudVmCluster:
        """Post-rpc interceptor for get_cloud_vm_cluster

        DEPRECATED. Please use the `post_get_cloud_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_cloud_vm_cluster` interceptor runs
        before the `post_get_cloud_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_get_cloud_vm_cluster_with_metadata(
        self,
        response: vm_cluster.CloudVmCluster,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[vm_cluster.CloudVmCluster, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_cloud_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_cloud_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_get_cloud_vm_cluster` interceptor.
        When both interceptors are used, this `post_get_cloud_vm_cluster_with_metadata` interceptor runs after the
        `post_get_cloud_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_get_cloud_vm_cluster` will be passed to
        `post_get_cloud_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_get_database(
        self,
        request: database.GetDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[database.GetDatabaseRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_database(self, response: database.Database) -> database.Database:
        """Post-rpc interceptor for get_database

        DEPRECATED. Please use the `post_get_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_database` interceptor runs
        before the `post_get_database_with_metadata` interceptor.
        """
        return response

    def post_get_database_with_metadata(
        self,
        response: database.Database,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[database.Database, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_database_with_metadata`
        interceptor in new development instead of the `post_get_database` interceptor.
        When both interceptors are used, this `post_get_database_with_metadata` interceptor runs after the
        `post_get_database` interceptor. The (possibly modified) response returned by
        `post_get_database` will be passed to
        `post_get_database_with_metadata`.
        """
        return response, metadata

    def pre_get_db_system(
        self,
        request: db_system.GetDbSystemRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[db_system.GetDbSystemRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_db_system

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_db_system(self, response: db_system.DbSystem) -> db_system.DbSystem:
        """Post-rpc interceptor for get_db_system

        DEPRECATED. Please use the `post_get_db_system_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_db_system` interceptor runs
        before the `post_get_db_system_with_metadata` interceptor.
        """
        return response

    def post_get_db_system_with_metadata(
        self,
        response: db_system.DbSystem,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[db_system.DbSystem, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_db_system

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_db_system_with_metadata`
        interceptor in new development instead of the `post_get_db_system` interceptor.
        When both interceptors are used, this `post_get_db_system_with_metadata` interceptor runs after the
        `post_get_db_system` interceptor. The (possibly modified) response returned by
        `post_get_db_system` will be passed to
        `post_get_db_system_with_metadata`.
        """
        return response, metadata

    def pre_get_exadb_vm_cluster(
        self,
        request: oracledatabase.GetExadbVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.GetExadbVmClusterRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_exadb_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_exadb_vm_cluster(
        self, response: exadb_vm_cluster.ExadbVmCluster
    ) -> exadb_vm_cluster.ExadbVmCluster:
        """Post-rpc interceptor for get_exadb_vm_cluster

        DEPRECATED. Please use the `post_get_exadb_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_exadb_vm_cluster` interceptor runs
        before the `post_get_exadb_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_get_exadb_vm_cluster_with_metadata(
        self,
        response: exadb_vm_cluster.ExadbVmCluster,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exadb_vm_cluster.ExadbVmCluster, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_exadb_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_exadb_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_get_exadb_vm_cluster` interceptor.
        When both interceptors are used, this `post_get_exadb_vm_cluster_with_metadata` interceptor runs after the
        `post_get_exadb_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_get_exadb_vm_cluster` will be passed to
        `post_get_exadb_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_get_exascale_db_storage_vault(
        self,
        request: exascale_db_storage_vault.GetExascaleDbStorageVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exascale_db_storage_vault.GetExascaleDbStorageVaultRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_exascale_db_storage_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_exascale_db_storage_vault(
        self, response: exascale_db_storage_vault.ExascaleDbStorageVault
    ) -> exascale_db_storage_vault.ExascaleDbStorageVault:
        """Post-rpc interceptor for get_exascale_db_storage_vault

        DEPRECATED. Please use the `post_get_exascale_db_storage_vault_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_exascale_db_storage_vault` interceptor runs
        before the `post_get_exascale_db_storage_vault_with_metadata` interceptor.
        """
        return response

    def post_get_exascale_db_storage_vault_with_metadata(
        self,
        response: exascale_db_storage_vault.ExascaleDbStorageVault,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exascale_db_storage_vault.ExascaleDbStorageVault,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for get_exascale_db_storage_vault

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_exascale_db_storage_vault_with_metadata`
        interceptor in new development instead of the `post_get_exascale_db_storage_vault` interceptor.
        When both interceptors are used, this `post_get_exascale_db_storage_vault_with_metadata` interceptor runs after the
        `post_get_exascale_db_storage_vault` interceptor. The (possibly modified) response returned by
        `post_get_exascale_db_storage_vault` will be passed to
        `post_get_exascale_db_storage_vault_with_metadata`.
        """
        return response, metadata

    def pre_get_odb_network(
        self,
        request: odb_network.GetOdbNetworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_network.GetOdbNetworkRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_odb_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_odb_network(
        self, response: odb_network.OdbNetwork
    ) -> odb_network.OdbNetwork:
        """Post-rpc interceptor for get_odb_network

        DEPRECATED. Please use the `post_get_odb_network_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_odb_network` interceptor runs
        before the `post_get_odb_network_with_metadata` interceptor.
        """
        return response

    def post_get_odb_network_with_metadata(
        self,
        response: odb_network.OdbNetwork,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[odb_network.OdbNetwork, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_odb_network

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_odb_network_with_metadata`
        interceptor in new development instead of the `post_get_odb_network` interceptor.
        When both interceptors are used, this `post_get_odb_network_with_metadata` interceptor runs after the
        `post_get_odb_network` interceptor. The (possibly modified) response returned by
        `post_get_odb_network` will be passed to
        `post_get_odb_network_with_metadata`.
        """
        return response, metadata

    def pre_get_odb_subnet(
        self,
        request: odb_subnet.GetOdbSubnetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[odb_subnet.GetOdbSubnetRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_odb_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_odb_subnet(
        self, response: odb_subnet.OdbSubnet
    ) -> odb_subnet.OdbSubnet:
        """Post-rpc interceptor for get_odb_subnet

        DEPRECATED. Please use the `post_get_odb_subnet_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_odb_subnet` interceptor runs
        before the `post_get_odb_subnet_with_metadata` interceptor.
        """
        return response

    def post_get_odb_subnet_with_metadata(
        self,
        response: odb_subnet.OdbSubnet,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[odb_subnet.OdbSubnet, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_odb_subnet

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_odb_subnet_with_metadata`
        interceptor in new development instead of the `post_get_odb_subnet` interceptor.
        When both interceptors are used, this `post_get_odb_subnet_with_metadata` interceptor runs after the
        `post_get_odb_subnet` interceptor. The (possibly modified) response returned by
        `post_get_odb_subnet` will be passed to
        `post_get_odb_subnet_with_metadata`.
        """
        return response, metadata

    def pre_get_pluggable_database(
        self,
        request: pluggable_database.GetPluggableDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        pluggable_database.GetPluggableDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_pluggable_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_pluggable_database(
        self, response: pluggable_database.PluggableDatabase
    ) -> pluggable_database.PluggableDatabase:
        """Post-rpc interceptor for get_pluggable_database

        DEPRECATED. Please use the `post_get_pluggable_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_get_pluggable_database` interceptor runs
        before the `post_get_pluggable_database_with_metadata` interceptor.
        """
        return response

    def post_get_pluggable_database_with_metadata(
        self,
        response: pluggable_database.PluggableDatabase,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        pluggable_database.PluggableDatabase, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_pluggable_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_get_pluggable_database_with_metadata`
        interceptor in new development instead of the `post_get_pluggable_database` interceptor.
        When both interceptors are used, this `post_get_pluggable_database_with_metadata` interceptor runs after the
        `post_get_pluggable_database` interceptor. The (possibly modified) response returned by
        `post_get_pluggable_database` will be passed to
        `post_get_pluggable_database_with_metadata`.
        """
        return response, metadata

    def pre_list_autonomous_database_backups(
        self,
        request: oracledatabase.ListAutonomousDatabaseBackupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseBackupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_autonomous_database_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_autonomous_database_backups(
        self, response: oracledatabase.ListAutonomousDatabaseBackupsResponse
    ) -> oracledatabase.ListAutonomousDatabaseBackupsResponse:
        """Post-rpc interceptor for list_autonomous_database_backups

        DEPRECATED. Please use the `post_list_autonomous_database_backups_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_autonomous_database_backups` interceptor runs
        before the `post_list_autonomous_database_backups_with_metadata` interceptor.
        """
        return response

    def post_list_autonomous_database_backups_with_metadata(
        self,
        response: oracledatabase.ListAutonomousDatabaseBackupsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseBackupsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_autonomous_database_backups

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_autonomous_database_backups_with_metadata`
        interceptor in new development instead of the `post_list_autonomous_database_backups` interceptor.
        When both interceptors are used, this `post_list_autonomous_database_backups_with_metadata` interceptor runs after the
        `post_list_autonomous_database_backups` interceptor. The (possibly modified) response returned by
        `post_list_autonomous_database_backups` will be passed to
        `post_list_autonomous_database_backups_with_metadata`.
        """
        return response, metadata

    def pre_list_autonomous_database_character_sets(
        self,
        request: oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_autonomous_database_character_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_autonomous_database_character_sets(
        self, response: oracledatabase.ListAutonomousDatabaseCharacterSetsResponse
    ) -> oracledatabase.ListAutonomousDatabaseCharacterSetsResponse:
        """Post-rpc interceptor for list_autonomous_database_character_sets

        DEPRECATED. Please use the `post_list_autonomous_database_character_sets_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_autonomous_database_character_sets` interceptor runs
        before the `post_list_autonomous_database_character_sets_with_metadata` interceptor.
        """
        return response

    def post_list_autonomous_database_character_sets_with_metadata(
        self,
        response: oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_autonomous_database_character_sets

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_autonomous_database_character_sets_with_metadata`
        interceptor in new development instead of the `post_list_autonomous_database_character_sets` interceptor.
        When both interceptors are used, this `post_list_autonomous_database_character_sets_with_metadata` interceptor runs after the
        `post_list_autonomous_database_character_sets` interceptor. The (possibly modified) response returned by
        `post_list_autonomous_database_character_sets` will be passed to
        `post_list_autonomous_database_character_sets_with_metadata`.
        """
        return response, metadata

    def pre_list_autonomous_databases(
        self,
        request: oracledatabase.ListAutonomousDatabasesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabasesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_autonomous_databases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_autonomous_databases(
        self, response: oracledatabase.ListAutonomousDatabasesResponse
    ) -> oracledatabase.ListAutonomousDatabasesResponse:
        """Post-rpc interceptor for list_autonomous_databases

        DEPRECATED. Please use the `post_list_autonomous_databases_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_autonomous_databases` interceptor runs
        before the `post_list_autonomous_databases_with_metadata` interceptor.
        """
        return response

    def post_list_autonomous_databases_with_metadata(
        self,
        response: oracledatabase.ListAutonomousDatabasesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabasesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_autonomous_databases

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_autonomous_databases_with_metadata`
        interceptor in new development instead of the `post_list_autonomous_databases` interceptor.
        When both interceptors are used, this `post_list_autonomous_databases_with_metadata` interceptor runs after the
        `post_list_autonomous_databases` interceptor. The (possibly modified) response returned by
        `post_list_autonomous_databases` will be passed to
        `post_list_autonomous_databases_with_metadata`.
        """
        return response, metadata

    def pre_list_autonomous_db_versions(
        self,
        request: oracledatabase.ListAutonomousDbVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDbVersionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_autonomous_db_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_autonomous_db_versions(
        self, response: oracledatabase.ListAutonomousDbVersionsResponse
    ) -> oracledatabase.ListAutonomousDbVersionsResponse:
        """Post-rpc interceptor for list_autonomous_db_versions

        DEPRECATED. Please use the `post_list_autonomous_db_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_autonomous_db_versions` interceptor runs
        before the `post_list_autonomous_db_versions_with_metadata` interceptor.
        """
        return response

    def post_list_autonomous_db_versions_with_metadata(
        self,
        response: oracledatabase.ListAutonomousDbVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDbVersionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_autonomous_db_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_autonomous_db_versions_with_metadata`
        interceptor in new development instead of the `post_list_autonomous_db_versions` interceptor.
        When both interceptors are used, this `post_list_autonomous_db_versions_with_metadata` interceptor runs after the
        `post_list_autonomous_db_versions` interceptor. The (possibly modified) response returned by
        `post_list_autonomous_db_versions` will be passed to
        `post_list_autonomous_db_versions_with_metadata`.
        """
        return response, metadata

    def pre_list_cloud_exadata_infrastructures(
        self,
        request: oracledatabase.ListCloudExadataInfrastructuresRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListCloudExadataInfrastructuresRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_cloud_exadata_infrastructures

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_cloud_exadata_infrastructures(
        self, response: oracledatabase.ListCloudExadataInfrastructuresResponse
    ) -> oracledatabase.ListCloudExadataInfrastructuresResponse:
        """Post-rpc interceptor for list_cloud_exadata_infrastructures

        DEPRECATED. Please use the `post_list_cloud_exadata_infrastructures_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_cloud_exadata_infrastructures` interceptor runs
        before the `post_list_cloud_exadata_infrastructures_with_metadata` interceptor.
        """
        return response

    def post_list_cloud_exadata_infrastructures_with_metadata(
        self,
        response: oracledatabase.ListCloudExadataInfrastructuresResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListCloudExadataInfrastructuresResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_cloud_exadata_infrastructures

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_cloud_exadata_infrastructures_with_metadata`
        interceptor in new development instead of the `post_list_cloud_exadata_infrastructures` interceptor.
        When both interceptors are used, this `post_list_cloud_exadata_infrastructures_with_metadata` interceptor runs after the
        `post_list_cloud_exadata_infrastructures` interceptor. The (possibly modified) response returned by
        `post_list_cloud_exadata_infrastructures` will be passed to
        `post_list_cloud_exadata_infrastructures_with_metadata`.
        """
        return response, metadata

    def pre_list_cloud_vm_clusters(
        self,
        request: oracledatabase.ListCloudVmClustersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListCloudVmClustersRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_cloud_vm_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_cloud_vm_clusters(
        self, response: oracledatabase.ListCloudVmClustersResponse
    ) -> oracledatabase.ListCloudVmClustersResponse:
        """Post-rpc interceptor for list_cloud_vm_clusters

        DEPRECATED. Please use the `post_list_cloud_vm_clusters_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_cloud_vm_clusters` interceptor runs
        before the `post_list_cloud_vm_clusters_with_metadata` interceptor.
        """
        return response

    def post_list_cloud_vm_clusters_with_metadata(
        self,
        response: oracledatabase.ListCloudVmClustersResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListCloudVmClustersResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_cloud_vm_clusters

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_cloud_vm_clusters_with_metadata`
        interceptor in new development instead of the `post_list_cloud_vm_clusters` interceptor.
        When both interceptors are used, this `post_list_cloud_vm_clusters_with_metadata` interceptor runs after the
        `post_list_cloud_vm_clusters` interceptor. The (possibly modified) response returned by
        `post_list_cloud_vm_clusters` will be passed to
        `post_list_cloud_vm_clusters_with_metadata`.
        """
        return response, metadata

    def pre_list_database_character_sets(
        self,
        request: database_character_set.ListDatabaseCharacterSetsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        database_character_set.ListDatabaseCharacterSetsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_database_character_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_database_character_sets(
        self, response: database_character_set.ListDatabaseCharacterSetsResponse
    ) -> database_character_set.ListDatabaseCharacterSetsResponse:
        """Post-rpc interceptor for list_database_character_sets

        DEPRECATED. Please use the `post_list_database_character_sets_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_database_character_sets` interceptor runs
        before the `post_list_database_character_sets_with_metadata` interceptor.
        """
        return response

    def post_list_database_character_sets_with_metadata(
        self,
        response: database_character_set.ListDatabaseCharacterSetsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        database_character_set.ListDatabaseCharacterSetsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_database_character_sets

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_database_character_sets_with_metadata`
        interceptor in new development instead of the `post_list_database_character_sets` interceptor.
        When both interceptors are used, this `post_list_database_character_sets_with_metadata` interceptor runs after the
        `post_list_database_character_sets` interceptor. The (possibly modified) response returned by
        `post_list_database_character_sets` will be passed to
        `post_list_database_character_sets_with_metadata`.
        """
        return response, metadata

    def pre_list_databases(
        self,
        request: database.ListDatabasesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[database.ListDatabasesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_databases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_databases(
        self, response: database.ListDatabasesResponse
    ) -> database.ListDatabasesResponse:
        """Post-rpc interceptor for list_databases

        DEPRECATED. Please use the `post_list_databases_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_databases` interceptor runs
        before the `post_list_databases_with_metadata` interceptor.
        """
        return response

    def post_list_databases_with_metadata(
        self,
        response: database.ListDatabasesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[database.ListDatabasesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_databases

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_databases_with_metadata`
        interceptor in new development instead of the `post_list_databases` interceptor.
        When both interceptors are used, this `post_list_databases_with_metadata` interceptor runs after the
        `post_list_databases` interceptor. The (possibly modified) response returned by
        `post_list_databases` will be passed to
        `post_list_databases_with_metadata`.
        """
        return response, metadata

    def pre_list_db_nodes(
        self,
        request: oracledatabase.ListDbNodesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbNodesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_db_nodes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_nodes(
        self, response: oracledatabase.ListDbNodesResponse
    ) -> oracledatabase.ListDbNodesResponse:
        """Post-rpc interceptor for list_db_nodes

        DEPRECATED. Please use the `post_list_db_nodes_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_nodes` interceptor runs
        before the `post_list_db_nodes_with_metadata` interceptor.
        """
        return response

    def post_list_db_nodes_with_metadata(
        self,
        response: oracledatabase.ListDbNodesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbNodesResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_db_nodes

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_nodes_with_metadata`
        interceptor in new development instead of the `post_list_db_nodes` interceptor.
        When both interceptors are used, this `post_list_db_nodes_with_metadata` interceptor runs after the
        `post_list_db_nodes` interceptor. The (possibly modified) response returned by
        `post_list_db_nodes` will be passed to
        `post_list_db_nodes_with_metadata`.
        """
        return response, metadata

    def pre_list_db_servers(
        self,
        request: oracledatabase.ListDbServersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbServersRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_db_servers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_servers(
        self, response: oracledatabase.ListDbServersResponse
    ) -> oracledatabase.ListDbServersResponse:
        """Post-rpc interceptor for list_db_servers

        DEPRECATED. Please use the `post_list_db_servers_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_servers` interceptor runs
        before the `post_list_db_servers_with_metadata` interceptor.
        """
        return response

    def post_list_db_servers_with_metadata(
        self,
        response: oracledatabase.ListDbServersResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbServersResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_db_servers

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_servers_with_metadata`
        interceptor in new development instead of the `post_list_db_servers` interceptor.
        When both interceptors are used, this `post_list_db_servers_with_metadata` interceptor runs after the
        `post_list_db_servers` interceptor. The (possibly modified) response returned by
        `post_list_db_servers` will be passed to
        `post_list_db_servers_with_metadata`.
        """
        return response, metadata

    def pre_list_db_system_initial_storage_sizes(
        self,
        request: db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_db_system_initial_storage_sizes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_system_initial_storage_sizes(
        self,
        response: db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse,
    ) -> db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse:
        """Post-rpc interceptor for list_db_system_initial_storage_sizes

        DEPRECATED. Please use the `post_list_db_system_initial_storage_sizes_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_system_initial_storage_sizes` interceptor runs
        before the `post_list_db_system_initial_storage_sizes_with_metadata` interceptor.
        """
        return response

    def post_list_db_system_initial_storage_sizes_with_metadata(
        self,
        response: db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_db_system_initial_storage_sizes

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_system_initial_storage_sizes_with_metadata`
        interceptor in new development instead of the `post_list_db_system_initial_storage_sizes` interceptor.
        When both interceptors are used, this `post_list_db_system_initial_storage_sizes_with_metadata` interceptor runs after the
        `post_list_db_system_initial_storage_sizes` interceptor. The (possibly modified) response returned by
        `post_list_db_system_initial_storage_sizes` will be passed to
        `post_list_db_system_initial_storage_sizes_with_metadata`.
        """
        return response, metadata

    def pre_list_db_systems(
        self,
        request: db_system.ListDbSystemsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[db_system.ListDbSystemsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_db_systems

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_systems(
        self, response: db_system.ListDbSystemsResponse
    ) -> db_system.ListDbSystemsResponse:
        """Post-rpc interceptor for list_db_systems

        DEPRECATED. Please use the `post_list_db_systems_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_systems` interceptor runs
        before the `post_list_db_systems_with_metadata` interceptor.
        """
        return response

    def post_list_db_systems_with_metadata(
        self,
        response: db_system.ListDbSystemsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_system.ListDbSystemsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_db_systems

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_systems_with_metadata`
        interceptor in new development instead of the `post_list_db_systems` interceptor.
        When both interceptors are used, this `post_list_db_systems_with_metadata` interceptor runs after the
        `post_list_db_systems` interceptor. The (possibly modified) response returned by
        `post_list_db_systems` will be passed to
        `post_list_db_systems_with_metadata`.
        """
        return response, metadata

    def pre_list_db_system_shapes(
        self,
        request: oracledatabase.ListDbSystemShapesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbSystemShapesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_db_system_shapes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_system_shapes(
        self, response: oracledatabase.ListDbSystemShapesResponse
    ) -> oracledatabase.ListDbSystemShapesResponse:
        """Post-rpc interceptor for list_db_system_shapes

        DEPRECATED. Please use the `post_list_db_system_shapes_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_system_shapes` interceptor runs
        before the `post_list_db_system_shapes_with_metadata` interceptor.
        """
        return response

    def post_list_db_system_shapes_with_metadata(
        self,
        response: oracledatabase.ListDbSystemShapesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListDbSystemShapesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_db_system_shapes

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_system_shapes_with_metadata`
        interceptor in new development instead of the `post_list_db_system_shapes` interceptor.
        When both interceptors are used, this `post_list_db_system_shapes_with_metadata` interceptor runs after the
        `post_list_db_system_shapes` interceptor. The (possibly modified) response returned by
        `post_list_db_system_shapes` will be passed to
        `post_list_db_system_shapes_with_metadata`.
        """
        return response, metadata

    def pre_list_db_versions(
        self,
        request: db_version.ListDbVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_version.ListDbVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_db_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_versions(
        self, response: db_version.ListDbVersionsResponse
    ) -> db_version.ListDbVersionsResponse:
        """Post-rpc interceptor for list_db_versions

        DEPRECATED. Please use the `post_list_db_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_db_versions` interceptor runs
        before the `post_list_db_versions_with_metadata` interceptor.
        """
        return response

    def post_list_db_versions_with_metadata(
        self,
        response: db_version.ListDbVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        db_version.ListDbVersionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_db_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_db_versions_with_metadata`
        interceptor in new development instead of the `post_list_db_versions` interceptor.
        When both interceptors are used, this `post_list_db_versions_with_metadata` interceptor runs after the
        `post_list_db_versions` interceptor. The (possibly modified) response returned by
        `post_list_db_versions` will be passed to
        `post_list_db_versions_with_metadata`.
        """
        return response, metadata

    def pre_list_entitlements(
        self,
        request: oracledatabase.ListEntitlementsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListEntitlementsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_entitlements

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_entitlements(
        self, response: oracledatabase.ListEntitlementsResponse
    ) -> oracledatabase.ListEntitlementsResponse:
        """Post-rpc interceptor for list_entitlements

        DEPRECATED. Please use the `post_list_entitlements_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_entitlements` interceptor runs
        before the `post_list_entitlements_with_metadata` interceptor.
        """
        return response

    def post_list_entitlements_with_metadata(
        self,
        response: oracledatabase.ListEntitlementsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListEntitlementsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_entitlements

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_entitlements_with_metadata`
        interceptor in new development instead of the `post_list_entitlements` interceptor.
        When both interceptors are used, this `post_list_entitlements_with_metadata` interceptor runs after the
        `post_list_entitlements` interceptor. The (possibly modified) response returned by
        `post_list_entitlements` will be passed to
        `post_list_entitlements_with_metadata`.
        """
        return response, metadata

    def pre_list_exadb_vm_clusters(
        self,
        request: oracledatabase.ListExadbVmClustersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListExadbVmClustersRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_exadb_vm_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_exadb_vm_clusters(
        self, response: oracledatabase.ListExadbVmClustersResponse
    ) -> oracledatabase.ListExadbVmClustersResponse:
        """Post-rpc interceptor for list_exadb_vm_clusters

        DEPRECATED. Please use the `post_list_exadb_vm_clusters_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_exadb_vm_clusters` interceptor runs
        before the `post_list_exadb_vm_clusters_with_metadata` interceptor.
        """
        return response

    def post_list_exadb_vm_clusters_with_metadata(
        self,
        response: oracledatabase.ListExadbVmClustersResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListExadbVmClustersResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_exadb_vm_clusters

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_exadb_vm_clusters_with_metadata`
        interceptor in new development instead of the `post_list_exadb_vm_clusters` interceptor.
        When both interceptors are used, this `post_list_exadb_vm_clusters_with_metadata` interceptor runs after the
        `post_list_exadb_vm_clusters` interceptor. The (possibly modified) response returned by
        `post_list_exadb_vm_clusters` will be passed to
        `post_list_exadb_vm_clusters_with_metadata`.
        """
        return response, metadata

    def pre_list_exascale_db_storage_vaults(
        self,
        request: exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_exascale_db_storage_vaults

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_exascale_db_storage_vaults(
        self, response: exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse
    ) -> exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse:
        """Post-rpc interceptor for list_exascale_db_storage_vaults

        DEPRECATED. Please use the `post_list_exascale_db_storage_vaults_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_exascale_db_storage_vaults` interceptor runs
        before the `post_list_exascale_db_storage_vaults_with_metadata` interceptor.
        """
        return response

    def post_list_exascale_db_storage_vaults_with_metadata(
        self,
        response: exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_exascale_db_storage_vaults

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_exascale_db_storage_vaults_with_metadata`
        interceptor in new development instead of the `post_list_exascale_db_storage_vaults` interceptor.
        When both interceptors are used, this `post_list_exascale_db_storage_vaults_with_metadata` interceptor runs after the
        `post_list_exascale_db_storage_vaults` interceptor. The (possibly modified) response returned by
        `post_list_exascale_db_storage_vaults` will be passed to
        `post_list_exascale_db_storage_vaults_with_metadata`.
        """
        return response, metadata

    def pre_list_gi_versions(
        self,
        request: oracledatabase.ListGiVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListGiVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_gi_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_gi_versions(
        self, response: oracledatabase.ListGiVersionsResponse
    ) -> oracledatabase.ListGiVersionsResponse:
        """Post-rpc interceptor for list_gi_versions

        DEPRECATED. Please use the `post_list_gi_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_gi_versions` interceptor runs
        before the `post_list_gi_versions_with_metadata` interceptor.
        """
        return response

    def post_list_gi_versions_with_metadata(
        self,
        response: oracledatabase.ListGiVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.ListGiVersionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_gi_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_gi_versions_with_metadata`
        interceptor in new development instead of the `post_list_gi_versions` interceptor.
        When both interceptors are used, this `post_list_gi_versions_with_metadata` interceptor runs after the
        `post_list_gi_versions` interceptor. The (possibly modified) response returned by
        `post_list_gi_versions` will be passed to
        `post_list_gi_versions_with_metadata`.
        """
        return response, metadata

    def pre_list_minor_versions(
        self,
        request: minor_version.ListMinorVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        minor_version.ListMinorVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_minor_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_minor_versions(
        self, response: minor_version.ListMinorVersionsResponse
    ) -> minor_version.ListMinorVersionsResponse:
        """Post-rpc interceptor for list_minor_versions

        DEPRECATED. Please use the `post_list_minor_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_minor_versions` interceptor runs
        before the `post_list_minor_versions_with_metadata` interceptor.
        """
        return response

    def post_list_minor_versions_with_metadata(
        self,
        response: minor_version.ListMinorVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        minor_version.ListMinorVersionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_minor_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_minor_versions_with_metadata`
        interceptor in new development instead of the `post_list_minor_versions` interceptor.
        When both interceptors are used, this `post_list_minor_versions_with_metadata` interceptor runs after the
        `post_list_minor_versions` interceptor. The (possibly modified) response returned by
        `post_list_minor_versions` will be passed to
        `post_list_minor_versions_with_metadata`.
        """
        return response, metadata

    def pre_list_odb_networks(
        self,
        request: odb_network.ListOdbNetworksRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_network.ListOdbNetworksRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_odb_networks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_odb_networks(
        self, response: odb_network.ListOdbNetworksResponse
    ) -> odb_network.ListOdbNetworksResponse:
        """Post-rpc interceptor for list_odb_networks

        DEPRECATED. Please use the `post_list_odb_networks_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_odb_networks` interceptor runs
        before the `post_list_odb_networks_with_metadata` interceptor.
        """
        return response

    def post_list_odb_networks_with_metadata(
        self,
        response: odb_network.ListOdbNetworksResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_network.ListOdbNetworksResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_odb_networks

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_odb_networks_with_metadata`
        interceptor in new development instead of the `post_list_odb_networks` interceptor.
        When both interceptors are used, this `post_list_odb_networks_with_metadata` interceptor runs after the
        `post_list_odb_networks` interceptor. The (possibly modified) response returned by
        `post_list_odb_networks` will be passed to
        `post_list_odb_networks_with_metadata`.
        """
        return response, metadata

    def pre_list_odb_subnets(
        self,
        request: odb_subnet.ListOdbSubnetsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_subnet.ListOdbSubnetsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_odb_subnets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_odb_subnets(
        self, response: odb_subnet.ListOdbSubnetsResponse
    ) -> odb_subnet.ListOdbSubnetsResponse:
        """Post-rpc interceptor for list_odb_subnets

        DEPRECATED. Please use the `post_list_odb_subnets_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_odb_subnets` interceptor runs
        before the `post_list_odb_subnets_with_metadata` interceptor.
        """
        return response

    def post_list_odb_subnets_with_metadata(
        self,
        response: odb_subnet.ListOdbSubnetsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        odb_subnet.ListOdbSubnetsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_odb_subnets

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_odb_subnets_with_metadata`
        interceptor in new development instead of the `post_list_odb_subnets` interceptor.
        When both interceptors are used, this `post_list_odb_subnets_with_metadata` interceptor runs after the
        `post_list_odb_subnets` interceptor. The (possibly modified) response returned by
        `post_list_odb_subnets` will be passed to
        `post_list_odb_subnets_with_metadata`.
        """
        return response, metadata

    def pre_list_pluggable_databases(
        self,
        request: pluggable_database.ListPluggableDatabasesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        pluggable_database.ListPluggableDatabasesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_pluggable_databases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_pluggable_databases(
        self, response: pluggable_database.ListPluggableDatabasesResponse
    ) -> pluggable_database.ListPluggableDatabasesResponse:
        """Post-rpc interceptor for list_pluggable_databases

        DEPRECATED. Please use the `post_list_pluggable_databases_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_list_pluggable_databases` interceptor runs
        before the `post_list_pluggable_databases_with_metadata` interceptor.
        """
        return response

    def post_list_pluggable_databases_with_metadata(
        self,
        response: pluggable_database.ListPluggableDatabasesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        pluggable_database.ListPluggableDatabasesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_pluggable_databases

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_list_pluggable_databases_with_metadata`
        interceptor in new development instead of the `post_list_pluggable_databases` interceptor.
        When both interceptors are used, this `post_list_pluggable_databases_with_metadata` interceptor runs after the
        `post_list_pluggable_databases` interceptor. The (possibly modified) response returned by
        `post_list_pluggable_databases` will be passed to
        `post_list_pluggable_databases_with_metadata`.
        """
        return response, metadata

    def pre_remove_virtual_machine_exadb_vm_cluster(
        self,
        request: oracledatabase.RemoveVirtualMachineExadbVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.RemoveVirtualMachineExadbVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for remove_virtual_machine_exadb_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_remove_virtual_machine_exadb_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_virtual_machine_exadb_vm_cluster

        DEPRECATED. Please use the `post_remove_virtual_machine_exadb_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_remove_virtual_machine_exadb_vm_cluster` interceptor runs
        before the `post_remove_virtual_machine_exadb_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_remove_virtual_machine_exadb_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for remove_virtual_machine_exadb_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_remove_virtual_machine_exadb_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_remove_virtual_machine_exadb_vm_cluster` interceptor.
        When both interceptors are used, this `post_remove_virtual_machine_exadb_vm_cluster_with_metadata` interceptor runs after the
        `post_remove_virtual_machine_exadb_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_remove_virtual_machine_exadb_vm_cluster` will be passed to
        `post_remove_virtual_machine_exadb_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_restart_autonomous_database(
        self,
        request: oracledatabase.RestartAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.RestartAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for restart_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_restart_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restart_autonomous_database

        DEPRECATED. Please use the `post_restart_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_restart_autonomous_database` interceptor runs
        before the `post_restart_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_restart_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for restart_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_restart_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_restart_autonomous_database` interceptor.
        When both interceptors are used, this `post_restart_autonomous_database_with_metadata` interceptor runs after the
        `post_restart_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_restart_autonomous_database` will be passed to
        `post_restart_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_restore_autonomous_database(
        self,
        request: oracledatabase.RestoreAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.RestoreAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for restore_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_restore_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_autonomous_database

        DEPRECATED. Please use the `post_restore_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_restore_autonomous_database` interceptor runs
        before the `post_restore_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_restore_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for restore_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_restore_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_restore_autonomous_database` interceptor.
        When both interceptors are used, this `post_restore_autonomous_database_with_metadata` interceptor runs after the
        `post_restore_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_restore_autonomous_database` will be passed to
        `post_restore_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_start_autonomous_database(
        self,
        request: oracledatabase.StartAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.StartAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for start_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_start_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_autonomous_database

        DEPRECATED. Please use the `post_start_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_start_autonomous_database` interceptor runs
        before the `post_start_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_start_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for start_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_start_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_start_autonomous_database` interceptor.
        When both interceptors are used, this `post_start_autonomous_database_with_metadata` interceptor runs after the
        `post_start_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_start_autonomous_database` will be passed to
        `post_start_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_stop_autonomous_database(
        self,
        request: oracledatabase.StopAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.StopAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for stop_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_stop_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_autonomous_database

        DEPRECATED. Please use the `post_stop_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_stop_autonomous_database` interceptor runs
        before the `post_stop_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_stop_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for stop_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_stop_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_stop_autonomous_database` interceptor.
        When both interceptors are used, this `post_stop_autonomous_database_with_metadata` interceptor runs after the
        `post_stop_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_stop_autonomous_database` will be passed to
        `post_stop_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_switchover_autonomous_database(
        self,
        request: oracledatabase.SwitchoverAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.SwitchoverAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for switchover_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_switchover_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for switchover_autonomous_database

        DEPRECATED. Please use the `post_switchover_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_switchover_autonomous_database` interceptor runs
        before the `post_switchover_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_switchover_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for switchover_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_switchover_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_switchover_autonomous_database` interceptor.
        When both interceptors are used, this `post_switchover_autonomous_database_with_metadata` interceptor runs after the
        `post_switchover_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_switchover_autonomous_database` will be passed to
        `post_switchover_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_update_autonomous_database(
        self,
        request: oracledatabase.UpdateAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.UpdateAutonomousDatabaseRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_update_autonomous_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_autonomous_database

        DEPRECATED. Please use the `post_update_autonomous_database_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_update_autonomous_database` interceptor runs
        before the `post_update_autonomous_database_with_metadata` interceptor.
        """
        return response

    def post_update_autonomous_database_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_autonomous_database

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_update_autonomous_database_with_metadata`
        interceptor in new development instead of the `post_update_autonomous_database` interceptor.
        When both interceptors are used, this `post_update_autonomous_database_with_metadata` interceptor runs after the
        `post_update_autonomous_database` interceptor. The (possibly modified) response returned by
        `post_update_autonomous_database` will be passed to
        `post_update_autonomous_database_with_metadata`.
        """
        return response, metadata

    def pre_update_exadb_vm_cluster(
        self,
        request: oracledatabase.UpdateExadbVmClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        oracledatabase.UpdateExadbVmClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_exadb_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_update_exadb_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_exadb_vm_cluster

        DEPRECATED. Please use the `post_update_exadb_vm_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code. This `post_update_exadb_vm_cluster` interceptor runs
        before the `post_update_exadb_vm_cluster_with_metadata` interceptor.
        """
        return response

    def post_update_exadb_vm_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_exadb_vm_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OracleDatabase server but before it is returned to user code.

        We recommend only using this `post_update_exadb_vm_cluster_with_metadata`
        interceptor in new development instead of the `post_update_exadb_vm_cluster` interceptor.
        When both interceptors are used, this `post_update_exadb_vm_cluster_with_metadata` interceptor runs after the
        `post_update_exadb_vm_cluster` interceptor. The (possibly modified) response returned by
        `post_update_exadb_vm_cluster` will be passed to
        `post_update_exadb_vm_cluster_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class OracleDatabaseRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: OracleDatabaseRestInterceptor


class OracleDatabaseRestTransport(_BaseOracleDatabaseRestTransport):
    """REST backend synchronous transport for OracleDatabase.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "oracledatabase.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[OracleDatabaseRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'oracledatabase.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or OracleDatabaseRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseCreateAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.CreateAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.CreateAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Create``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_create_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._CreateAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateCloudExadataInfrastructure(
        _BaseOracleDatabaseRestTransport._BaseCreateCloudExadataInfrastructure,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateCloudExadataInfrastructure")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.CreateCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.CreateCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Create``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateCloudExadataInfrastructure._get_http_options()

            request, metadata = (
                self._interceptor.pre_create_cloud_exadata_infrastructure(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateCloudExadataInfrastructure._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateCloudExadataInfrastructure._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateCloudExadataInfrastructure._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateCloudExadataInfrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateCloudExadataInfrastructure",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateCloudExadataInfrastructure._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_cloud_exadata_infrastructure(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_create_cloud_exadata_infrastructure_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_cloud_exadata_infrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateCloudExadataInfrastructure",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateCloudVmCluster(
        _BaseOracleDatabaseRestTransport._BaseCreateCloudVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateCloudVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.CreateCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.CreateCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateCloudVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_create_cloud_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateCloudVmCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateCloudVmCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateCloudVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateCloudVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateCloudVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateCloudVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_cloud_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_cloud_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_cloud_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateCloudVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateDbSystem(
        _BaseOracleDatabaseRestTransport._BaseCreateDbSystem, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateDbSystem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gco_db_system.CreateDbSystemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create db system method over HTTP.

            Args:
                request (~.gco_db_system.CreateDbSystemRequest):
                    The request object. The request for ``DbSystem.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseCreateDbSystem._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_db_system(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateDbSystem._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateDbSystem._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateDbSystem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateDbSystem",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateDbSystem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateDbSystem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_db_system(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_db_system_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_db_system",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateDbSystem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateExadbVmCluster(
        _BaseOracleDatabaseRestTransport._BaseCreateExadbVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateExadbVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.CreateExadbVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create exadb vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.CreateExadbVmClusterRequest):
                    The request object. The request for ``ExadbVmCluster.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateExadbVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_create_exadb_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateExadbVmCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateExadbVmCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateExadbVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateExadbVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateExadbVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateExadbVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_exadb_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_exadb_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_exadb_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateExadbVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateExascaleDbStorageVault(
        _BaseOracleDatabaseRestTransport._BaseCreateExascaleDbStorageVault,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateExascaleDbStorageVault")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create exascale db
            storage vault method over HTTP.

                Args:
                    request (~.gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest):
                        The request object. The request for ``ExascaleDbStorageVault.Create``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateExascaleDbStorageVault._get_http_options()

            request, metadata = self._interceptor.pre_create_exascale_db_storage_vault(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateExascaleDbStorageVault._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateExascaleDbStorageVault._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateExascaleDbStorageVault._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateExascaleDbStorageVault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateExascaleDbStorageVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._CreateExascaleDbStorageVault._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_exascale_db_storage_vault(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_create_exascale_db_storage_vault_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_exascale_db_storage_vault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateExascaleDbStorageVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateOdbNetwork(
        _BaseOracleDatabaseRestTransport._BaseCreateOdbNetwork, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateOdbNetwork")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gco_odb_network.CreateOdbNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create odb network method over HTTP.

            Args:
                request (~.gco_odb_network.CreateOdbNetworkRequest):
                    The request object. The request for ``OdbNetwork.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateOdbNetwork._get_http_options()

            request, metadata = self._interceptor.pre_create_odb_network(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateOdbNetwork._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateOdbNetwork._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateOdbNetwork._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateOdbNetwork",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateOdbNetwork",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateOdbNetwork._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_odb_network(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_odb_network_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_odb_network",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateOdbNetwork",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateOdbSubnet(
        _BaseOracleDatabaseRestTransport._BaseCreateOdbSubnet, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CreateOdbSubnet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gco_odb_subnet.CreateOdbSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create odb subnet method over HTTP.

            Args:
                request (~.gco_odb_subnet.CreateOdbSubnetRequest):
                    The request object. The request for ``OdbSubnet.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCreateOdbSubnet._get_http_options()

            request, metadata = self._interceptor.pre_create_odb_subnet(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCreateOdbSubnet._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCreateOdbSubnet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCreateOdbSubnet._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CreateOdbSubnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateOdbSubnet",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CreateOdbSubnet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_odb_subnet(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_odb_subnet_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.create_odb_subnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CreateOdbSubnet",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseDeleteAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.DeleteAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.DeleteAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Delete``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_delete_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._DeleteAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCloudExadataInfrastructure(
        _BaseOracleDatabaseRestTransport._BaseDeleteCloudExadataInfrastructure,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteCloudExadataInfrastructure")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.DeleteCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.DeleteCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Delete``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteCloudExadataInfrastructure._get_http_options()

            request, metadata = (
                self._interceptor.pre_delete_cloud_exadata_infrastructure(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteCloudExadataInfrastructure._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteCloudExadataInfrastructure._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteCloudExadataInfrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteCloudExadataInfrastructure",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteCloudExadataInfrastructure._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_cloud_exadata_infrastructure(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_delete_cloud_exadata_infrastructure_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_cloud_exadata_infrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteCloudExadataInfrastructure",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCloudVmCluster(
        _BaseOracleDatabaseRestTransport._BaseDeleteCloudVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteCloudVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.DeleteCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.DeleteCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteCloudVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_delete_cloud_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteCloudVmCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteCloudVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteCloudVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteCloudVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteCloudVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_cloud_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_cloud_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_cloud_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteCloudVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteDbSystem(
        _BaseOracleDatabaseRestTransport._BaseDeleteDbSystem, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteDbSystem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: db_system.DeleteDbSystemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete db system method over HTTP.

            Args:
                request (~.db_system.DeleteDbSystemRequest):
                    The request object. The request for ``DbSystem.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseDeleteDbSystem._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_db_system(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteDbSystem._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteDbSystem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteDbSystem",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteDbSystem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteDbSystem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_db_system(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_db_system_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_db_system",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteDbSystem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteExadbVmCluster(
        _BaseOracleDatabaseRestTransport._BaseDeleteExadbVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteExadbVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.DeleteExadbVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete exadb vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.DeleteExadbVmClusterRequest):
                    The request object. The request for ``ExadbVmCluster.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteExadbVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_delete_exadb_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteExadbVmCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteExadbVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteExadbVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteExadbVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteExadbVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_exadb_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_exadb_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_exadb_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteExadbVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteExascaleDbStorageVault(
        _BaseOracleDatabaseRestTransport._BaseDeleteExascaleDbStorageVault,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteExascaleDbStorageVault")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete exascale db
            storage vault method over HTTP.

                Args:
                    request (~.exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest):
                        The request object. The request message for
                    ``ExascaleDbStorageVault.Delete``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteExascaleDbStorageVault._get_http_options()

            request, metadata = self._interceptor.pre_delete_exascale_db_storage_vault(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteExascaleDbStorageVault._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteExascaleDbStorageVault._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteExascaleDbStorageVault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteExascaleDbStorageVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._DeleteExascaleDbStorageVault._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_exascale_db_storage_vault(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_delete_exascale_db_storage_vault_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_exascale_db_storage_vault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteExascaleDbStorageVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteOdbNetwork(
        _BaseOracleDatabaseRestTransport._BaseDeleteOdbNetwork, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteOdbNetwork")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_network.DeleteOdbNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete odb network method over HTTP.

            Args:
                request (~.odb_network.DeleteOdbNetworkRequest):
                    The request object. The request for ``OdbNetwork.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteOdbNetwork._get_http_options()

            request, metadata = self._interceptor.pre_delete_odb_network(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteOdbNetwork._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteOdbNetwork._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteOdbNetwork",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteOdbNetwork",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteOdbNetwork._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_odb_network(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_odb_network_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_odb_network",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteOdbNetwork",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteOdbSubnet(
        _BaseOracleDatabaseRestTransport._BaseDeleteOdbSubnet, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteOdbSubnet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_subnet.DeleteOdbSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete odb subnet method over HTTP.

            Args:
                request (~.odb_subnet.DeleteOdbSubnetRequest):
                    The request object. The request for ``OdbSubnet.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteOdbSubnet._get_http_options()

            request, metadata = self._interceptor.pre_delete_odb_subnet(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteOdbSubnet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteOdbSubnet._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteOdbSubnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteOdbSubnet",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteOdbSubnet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_odb_subnet(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_odb_subnet_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.delete_odb_subnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteOdbSubnet",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FailoverAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseFailoverAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.FailoverAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.FailoverAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the failover autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.FailoverAutonomousDatabaseRequest):
                        The request object. The request for
                    ``OracleDatabase.FailoverAutonomousDatabase``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseFailoverAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_failover_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseFailoverAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseFailoverAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseFailoverAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.FailoverAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "FailoverAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._FailoverAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_failover_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_failover_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.failover_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "FailoverAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GenerateAutonomousDatabaseWallet(
        _BaseOracleDatabaseRestTransport._BaseGenerateAutonomousDatabaseWallet,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GenerateAutonomousDatabaseWallet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.GenerateAutonomousDatabaseWalletRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.GenerateAutonomousDatabaseWalletResponse:
            r"""Call the generate autonomous
            database wallet method over HTTP.

                Args:
                    request (~.oracledatabase.GenerateAutonomousDatabaseWalletRequest):
                        The request object. The request for ``AutonomousDatabase.GenerateWallet``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.oracledatabase.GenerateAutonomousDatabaseWalletResponse:
                        The response for ``AutonomousDatabase.GenerateWallet``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGenerateAutonomousDatabaseWallet._get_http_options()

            request, metadata = (
                self._interceptor.pre_generate_autonomous_database_wallet(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGenerateAutonomousDatabaseWallet._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseGenerateAutonomousDatabaseWallet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGenerateAutonomousDatabaseWallet._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GenerateAutonomousDatabaseWallet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GenerateAutonomousDatabaseWallet",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GenerateAutonomousDatabaseWallet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
            pb_resp = oracledatabase.GenerateAutonomousDatabaseWalletResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_generate_autonomous_database_wallet(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_generate_autonomous_database_wallet_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.GenerateAutonomousDatabaseWalletResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.generate_autonomous_database_wallet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GenerateAutonomousDatabaseWallet",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseGetAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.GetAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> autonomous_database.AutonomousDatabase:
            r"""Call the get autonomous database method over HTTP.

            Args:
                request (~.oracledatabase.GetAutonomousDatabaseRequest):
                    The request object. The request for ``AutonomousDatabase.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.autonomous_database.AutonomousDatabase:
                    Details of the Autonomous Database
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_get_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetAutonomousDatabase._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = autonomous_database.AutonomousDatabase()
            pb_resp = autonomous_database.AutonomousDatabase.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = autonomous_database.AutonomousDatabase.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetCloudExadataInfrastructure(
        _BaseOracleDatabaseRestTransport._BaseGetCloudExadataInfrastructure,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetCloudExadataInfrastructure")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.GetCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> exadata_infra.CloudExadataInfrastructure:
            r"""Call the get cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.GetCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Get``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.exadata_infra.CloudExadataInfrastructure:
                        Represents CloudExadataInfrastructure
                    resource.
                    https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudExadataInfrastructure/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetCloudExadataInfrastructure._get_http_options()

            request, metadata = self._interceptor.pre_get_cloud_exadata_infrastructure(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetCloudExadataInfrastructure._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetCloudExadataInfrastructure._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetCloudExadataInfrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetCloudExadataInfrastructure",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetCloudExadataInfrastructure._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = exadata_infra.CloudExadataInfrastructure()
            pb_resp = exadata_infra.CloudExadataInfrastructure.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_cloud_exadata_infrastructure(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_get_cloud_exadata_infrastructure_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = exadata_infra.CloudExadataInfrastructure.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_cloud_exadata_infrastructure",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetCloudExadataInfrastructure",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetCloudVmCluster(
        _BaseOracleDatabaseRestTransport._BaseGetCloudVmCluster, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetCloudVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.GetCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> vm_cluster.CloudVmCluster:
            r"""Call the get cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.GetCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.vm_cluster.CloudVmCluster:
                    Details of the Cloud VM Cluster
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudVmCluster/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetCloudVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_get_cloud_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetCloudVmCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetCloudVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetCloudVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetCloudVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetCloudVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = vm_cluster.CloudVmCluster()
            pb_resp = vm_cluster.CloudVmCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_cloud_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_cloud_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = vm_cluster.CloudVmCluster.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_cloud_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetCloudVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetDatabase(
        _BaseOracleDatabaseRestTransport._BaseGetDatabase, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: database.GetDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> database.Database:
            r"""Call the get database method over HTTP.

            Args:
                request (~.database.GetDatabaseRequest):
                    The request object. The request for ``Database.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.database.Database:
                    Details of the Database resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/Database/

            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetDatabase._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_database(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetDatabase._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = database.Database()
            pb_resp = database.Database.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = database.Database.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetDbSystem(
        _BaseOracleDatabaseRestTransport._BaseGetDbSystem, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetDbSystem")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: db_system.GetDbSystemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> db_system.DbSystem:
            r"""Call the get db system method over HTTP.

            Args:
                request (~.db_system.GetDbSystemRequest):
                    The request object. The request for ``DbSystem.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.db_system.DbSystem:
                    Details of the DbSystem (BaseDB)
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/DbSystem/

            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetDbSystem._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_db_system(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetDbSystem._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetDbSystem._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetDbSystem",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetDbSystem",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetDbSystem._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = db_system.DbSystem()
            pb_resp = db_system.DbSystem.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_db_system(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_db_system_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = db_system.DbSystem.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_db_system",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetDbSystem",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetExadbVmCluster(
        _BaseOracleDatabaseRestTransport._BaseGetExadbVmCluster, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetExadbVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.GetExadbVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> exadb_vm_cluster.ExadbVmCluster:
            r"""Call the get exadb vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.GetExadbVmClusterRequest):
                    The request object. The request for ``ExadbVmCluster.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.exadb_vm_cluster.ExadbVmCluster:
                    ExadbVmCluster represents a cluster
                of VMs that are used to run Exadata
                workloads.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/ExadbVmCluster/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetExadbVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_get_exadb_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetExadbVmCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetExadbVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetExadbVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetExadbVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetExadbVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = exadb_vm_cluster.ExadbVmCluster()
            pb_resp = exadb_vm_cluster.ExadbVmCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_exadb_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_exadb_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = exadb_vm_cluster.ExadbVmCluster.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_exadb_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetExadbVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetExascaleDbStorageVault(
        _BaseOracleDatabaseRestTransport._BaseGetExascaleDbStorageVault,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetExascaleDbStorageVault")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: exascale_db_storage_vault.GetExascaleDbStorageVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> exascale_db_storage_vault.ExascaleDbStorageVault:
            r"""Call the get exascale db storage
            vault method over HTTP.

                Args:
                    request (~.exascale_db_storage_vault.GetExascaleDbStorageVaultRequest):
                        The request object. The request for ``ExascaleDbStorageVault.Get``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.exascale_db_storage_vault.ExascaleDbStorageVault:
                        ExascaleDbStorageVault represents a
                    storage vault exadb vm cluster resource.
                    https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/ExascaleDbStorageVault/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetExascaleDbStorageVault._get_http_options()

            request, metadata = self._interceptor.pre_get_exascale_db_storage_vault(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetExascaleDbStorageVault._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetExascaleDbStorageVault._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetExascaleDbStorageVault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetExascaleDbStorageVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._GetExascaleDbStorageVault._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = exascale_db_storage_vault.ExascaleDbStorageVault()
            pb_resp = exascale_db_storage_vault.ExascaleDbStorageVault.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_exascale_db_storage_vault(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_get_exascale_db_storage_vault_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        exascale_db_storage_vault.ExascaleDbStorageVault.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_exascale_db_storage_vault",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetExascaleDbStorageVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetOdbNetwork(
        _BaseOracleDatabaseRestTransport._BaseGetOdbNetwork, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetOdbNetwork")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_network.GetOdbNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> odb_network.OdbNetwork:
            r"""Call the get odb network method over HTTP.

            Args:
                request (~.odb_network.GetOdbNetworkRequest):
                    The request object. The request for ``OdbNetwork.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.odb_network.OdbNetwork:
                    Represents OdbNetwork resource.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetOdbNetwork._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_odb_network(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetOdbNetwork._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetOdbNetwork._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetOdbNetwork",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOdbNetwork",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetOdbNetwork._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = odb_network.OdbNetwork()
            pb_resp = odb_network.OdbNetwork.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_odb_network(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_odb_network_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = odb_network.OdbNetwork.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_odb_network",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOdbNetwork",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetOdbSubnet(
        _BaseOracleDatabaseRestTransport._BaseGetOdbSubnet, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetOdbSubnet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_subnet.GetOdbSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> odb_subnet.OdbSubnet:
            r"""Call the get odb subnet method over HTTP.

            Args:
                request (~.odb_subnet.GetOdbSubnetRequest):
                    The request object. The request for ``OdbSubnet.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.odb_subnet.OdbSubnet:
                    Represents OdbSubnet resource.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetOdbSubnet._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_odb_subnet(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetOdbSubnet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetOdbSubnet._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetOdbSubnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOdbSubnet",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetOdbSubnet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = odb_subnet.OdbSubnet()
            pb_resp = odb_subnet.OdbSubnet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_odb_subnet(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_odb_subnet_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = odb_subnet.OdbSubnet.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_odb_subnet",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOdbSubnet",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetPluggableDatabase(
        _BaseOracleDatabaseRestTransport._BaseGetPluggableDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetPluggableDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: pluggable_database.GetPluggableDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> pluggable_database.PluggableDatabase:
            r"""Call the get pluggable database method over HTTP.

            Args:
                request (~.pluggable_database.GetPluggableDatabaseRequest):
                    The request object. The request for ``PluggableDatabase.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.pluggable_database.PluggableDatabase:
                    The PluggableDatabase resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/PluggableDatabase/

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseGetPluggableDatabase._get_http_options()

            request, metadata = self._interceptor.pre_get_pluggable_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetPluggableDatabase._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetPluggableDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetPluggableDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetPluggableDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetPluggableDatabase._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = pluggable_database.PluggableDatabase()
            pb_resp = pluggable_database.PluggableDatabase.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_pluggable_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_pluggable_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = pluggable_database.PluggableDatabase.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.get_pluggable_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetPluggableDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAutonomousDatabaseBackups(
        _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseBackups,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListAutonomousDatabaseBackups")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabaseBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListAutonomousDatabaseBackupsResponse:
            r"""Call the list autonomous database
            backups method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDatabaseBackupsRequest):
                        The request object. The request for ``AutonomousDatabaseBackup.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.oracledatabase.ListAutonomousDatabaseBackupsResponse:
                        The response for ``AutonomousDatabaseBackup.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseBackups._get_http_options()

            request, metadata = self._interceptor.pre_list_autonomous_database_backups(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseBackups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseBackups._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListAutonomousDatabaseBackups",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabaseBackups",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListAutonomousDatabaseBackups._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListAutonomousDatabaseBackupsResponse()
            pb_resp = oracledatabase.ListAutonomousDatabaseBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_autonomous_database_backups(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_list_autonomous_database_backups_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListAutonomousDatabaseBackupsResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_autonomous_database_backups",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabaseBackups",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAutonomousDatabaseCharacterSets(
        _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseCharacterSets,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash(
                "OracleDatabaseRestTransport.ListAutonomousDatabaseCharacterSets"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListAutonomousDatabaseCharacterSetsResponse:
            r"""Call the list autonomous database
            character sets method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDatabaseCharacterSetsRequest):
                        The request object. The request for ``AutonomousDatabaseCharacterSet.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.oracledatabase.ListAutonomousDatabaseCharacterSetsResponse:
                        The response for
                    ``AutonomousDatabaseCharacterSet.List``.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseCharacterSets._get_http_options()

            request, metadata = (
                self._interceptor.pre_list_autonomous_database_character_sets(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseCharacterSets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabaseCharacterSets._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListAutonomousDatabaseCharacterSets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabaseCharacterSets",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListAutonomousDatabaseCharacterSets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
            pb_resp = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_autonomous_database_character_sets(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_list_autonomous_database_character_sets_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_autonomous_database_character_sets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabaseCharacterSets",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAutonomousDatabases(
        _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabases,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListAutonomousDatabases")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListAutonomousDatabasesResponse:
            r"""Call the list autonomous databases method over HTTP.

            Args:
                request (~.oracledatabase.ListAutonomousDatabasesRequest):
                    The request object. The request for ``AutonomousDatabase.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListAutonomousDatabasesResponse:
                    The response for ``AutonomousDatabase.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabases._get_http_options()

            request, metadata = self._interceptor.pre_list_autonomous_databases(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabases._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListAutonomousDatabases._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListAutonomousDatabases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabases",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._ListAutonomousDatabases._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListAutonomousDatabasesResponse()
            pb_resp = oracledatabase.ListAutonomousDatabasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_autonomous_databases(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_autonomous_databases_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListAutonomousDatabasesResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_autonomous_databases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDatabases",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAutonomousDbVersions(
        _BaseOracleDatabaseRestTransport._BaseListAutonomousDbVersions,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListAutonomousDbVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDbVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListAutonomousDbVersionsResponse:
            r"""Call the list autonomous db
            versions method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDbVersionsRequest):
                        The request object. The request for ``AutonomousDbVersion.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.oracledatabase.ListAutonomousDbVersionsResponse:
                        The response for ``AutonomousDbVersion.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListAutonomousDbVersions._get_http_options()

            request, metadata = self._interceptor.pre_list_autonomous_db_versions(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListAutonomousDbVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListAutonomousDbVersions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListAutonomousDbVersions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDbVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._ListAutonomousDbVersions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListAutonomousDbVersionsResponse()
            pb_resp = oracledatabase.ListAutonomousDbVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_autonomous_db_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_autonomous_db_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListAutonomousDbVersionsResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_autonomous_db_versions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListAutonomousDbVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCloudExadataInfrastructures(
        _BaseOracleDatabaseRestTransport._BaseListCloudExadataInfrastructures,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListCloudExadataInfrastructures")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListCloudExadataInfrastructuresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListCloudExadataInfrastructuresResponse:
            r"""Call the list cloud exadata
            infrastructures method over HTTP.

                Args:
                    request (~.oracledatabase.ListCloudExadataInfrastructuresRequest):
                        The request object. The request for ``CloudExadataInfrastructures.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.oracledatabase.ListCloudExadataInfrastructuresResponse:
                        The response for ``CloudExadataInfrastructures.list``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListCloudExadataInfrastructures._get_http_options()

            request, metadata = (
                self._interceptor.pre_list_cloud_exadata_infrastructures(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListCloudExadataInfrastructures._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListCloudExadataInfrastructures._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListCloudExadataInfrastructures",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListCloudExadataInfrastructures",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListCloudExadataInfrastructures._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListCloudExadataInfrastructuresResponse()
            pb_resp = oracledatabase.ListCloudExadataInfrastructuresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_cloud_exadata_infrastructures(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_list_cloud_exadata_infrastructures_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListCloudExadataInfrastructuresResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_cloud_exadata_infrastructures",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListCloudExadataInfrastructures",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCloudVmClusters(
        _BaseOracleDatabaseRestTransport._BaseListCloudVmClusters,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListCloudVmClusters")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListCloudVmClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListCloudVmClustersResponse:
            r"""Call the list cloud vm clusters method over HTTP.

            Args:
                request (~.oracledatabase.ListCloudVmClustersRequest):
                    The request object. The request for ``CloudVmCluster.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListCloudVmClustersResponse:
                    The response for ``CloudVmCluster.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListCloudVmClusters._get_http_options()

            request, metadata = self._interceptor.pre_list_cloud_vm_clusters(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListCloudVmClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListCloudVmClusters._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListCloudVmClusters",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListCloudVmClusters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListCloudVmClusters._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListCloudVmClustersResponse()
            pb_resp = oracledatabase.ListCloudVmClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_cloud_vm_clusters(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_cloud_vm_clusters_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListCloudVmClustersResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_cloud_vm_clusters",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListCloudVmClusters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDatabaseCharacterSets(
        _BaseOracleDatabaseRestTransport._BaseListDatabaseCharacterSets,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDatabaseCharacterSets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: database_character_set.ListDatabaseCharacterSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> database_character_set.ListDatabaseCharacterSetsResponse:
            r"""Call the list database character
            sets method over HTTP.

                Args:
                    request (~.database_character_set.ListDatabaseCharacterSetsRequest):
                        The request object. The request for ``DatabaseCharacterSet.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.database_character_set.ListDatabaseCharacterSetsResponse:
                        The response for ``DatabaseCharacterSet.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListDatabaseCharacterSets._get_http_options()

            request, metadata = self._interceptor.pre_list_database_character_sets(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDatabaseCharacterSets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDatabaseCharacterSets._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDatabaseCharacterSets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDatabaseCharacterSets",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._ListDatabaseCharacterSets._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = database_character_set.ListDatabaseCharacterSetsResponse()
            pb_resp = database_character_set.ListDatabaseCharacterSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_database_character_sets(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_database_character_sets_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = database_character_set.ListDatabaseCharacterSetsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_database_character_sets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDatabaseCharacterSets",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDatabases(
        _BaseOracleDatabaseRestTransport._BaseListDatabases, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDatabases")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: database.ListDatabasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> database.ListDatabasesResponse:
            r"""Call the list databases method over HTTP.

            Args:
                request (~.database.ListDatabasesRequest):
                    The request object. The request for ``Database.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.database.ListDatabasesResponse:
                    The response for ``Database.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListDatabases._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_databases(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDatabases._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDatabases._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDatabases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDatabases",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDatabases._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = database.ListDatabasesResponse()
            pb_resp = database.ListDatabasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_databases(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_databases_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = database.ListDatabasesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_databases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDatabases",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbNodes(
        _BaseOracleDatabaseRestTransport._BaseListDbNodes, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbNodes")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListDbNodesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListDbNodesResponse:
            r"""Call the list db nodes method over HTTP.

            Args:
                request (~.oracledatabase.ListDbNodesRequest):
                    The request object. The request for ``DbNode.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListDbNodesResponse:
                    The response for ``DbNode.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListDbNodes._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_db_nodes(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbNodes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbNodes._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbNodes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbNodes",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbNodes._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListDbNodesResponse()
            pb_resp = oracledatabase.ListDbNodesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_nodes(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_db_nodes_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = oracledatabase.ListDbNodesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_nodes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbNodes",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbServers(
        _BaseOracleDatabaseRestTransport._BaseListDbServers, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbServers")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListDbServersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListDbServersResponse:
            r"""Call the list db servers method over HTTP.

            Args:
                request (~.oracledatabase.ListDbServersRequest):
                    The request object. The request for ``DbServer.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListDbServersResponse:
                    The response for ``DbServer.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListDbServers._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_db_servers(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbServers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbServers._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbServers",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbServers",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbServers._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListDbServersResponse()
            pb_resp = oracledatabase.ListDbServersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_servers(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_db_servers_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = oracledatabase.ListDbServersResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_servers",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbServers",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbSystemInitialStorageSizes(
        _BaseOracleDatabaseRestTransport._BaseListDbSystemInitialStorageSizes,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbSystemInitialStorageSizes")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse:
            r"""Call the list db system initial
            storage sizes method over HTTP.

                Args:
                    request (~.db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest):
                        The request object. The request for ``DbSystemInitialStorageSizes.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse:
                        The response for ``DbSystemInitialStorageSizes.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListDbSystemInitialStorageSizes._get_http_options()

            request, metadata = (
                self._interceptor.pre_list_db_system_initial_storage_sizes(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbSystemInitialStorageSizes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbSystemInitialStorageSizes._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbSystemInitialStorageSizes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystemInitialStorageSizes",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbSystemInitialStorageSizes._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse()
            )
            pb_resp = db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_system_initial_storage_sizes(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_list_db_system_initial_storage_sizes_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_system_initial_storage_sizes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystemInitialStorageSizes",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbSystems(
        _BaseOracleDatabaseRestTransport._BaseListDbSystems, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbSystems")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: db_system.ListDbSystemsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> db_system.ListDbSystemsResponse:
            r"""Call the list db systems method over HTTP.

            Args:
                request (~.db_system.ListDbSystemsRequest):
                    The request object. The request for ``DbSystem.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.db_system.ListDbSystemsResponse:
                    The response for ``DbSystem.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListDbSystems._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_db_systems(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbSystems._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbSystems._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbSystems",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystems",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbSystems._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = db_system.ListDbSystemsResponse()
            pb_resp = db_system.ListDbSystemsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_systems(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_db_systems_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = db_system.ListDbSystemsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_systems",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystems",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbSystemShapes(
        _BaseOracleDatabaseRestTransport._BaseListDbSystemShapes, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbSystemShapes")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListDbSystemShapesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListDbSystemShapesResponse:
            r"""Call the list db system shapes method over HTTP.

            Args:
                request (~.oracledatabase.ListDbSystemShapesRequest):
                    The request object. The request for ``DbSystemShape.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListDbSystemShapesResponse:
                    The response for ``DbSystemShape.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListDbSystemShapes._get_http_options()

            request, metadata = self._interceptor.pre_list_db_system_shapes(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbSystemShapes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbSystemShapes._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbSystemShapes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystemShapes",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbSystemShapes._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListDbSystemShapesResponse()
            pb_resp = oracledatabase.ListDbSystemShapesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_system_shapes(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_db_system_shapes_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListDbSystemShapesResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_system_shapes",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbSystemShapes",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDbVersions(
        _BaseOracleDatabaseRestTransport._BaseListDbVersions, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListDbVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: db_version.ListDbVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> db_version.ListDbVersionsResponse:
            r"""Call the list db versions method over HTTP.

            Args:
                request (~.db_version.ListDbVersionsRequest):
                    The request object. The request for ``DbVersions.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.db_version.ListDbVersionsResponse:
                    The response for ``DbVersions.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListDbVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_db_versions(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListDbVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListDbVersions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListDbVersions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListDbVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = db_version.ListDbVersionsResponse()
            pb_resp = db_version.ListDbVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_db_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_db_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = db_version.ListDbVersionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_db_versions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListDbVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListEntitlements(
        _BaseOracleDatabaseRestTransport._BaseListEntitlements, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListEntitlements")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListEntitlementsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListEntitlementsResponse:
            r"""Call the list entitlements method over HTTP.

            Args:
                request (~.oracledatabase.ListEntitlementsRequest):
                    The request object. The request for ``Entitlement.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListEntitlementsResponse:
                    The response for ``Entitlement.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListEntitlements._get_http_options()

            request, metadata = self._interceptor.pre_list_entitlements(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListEntitlements._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListEntitlements._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListEntitlements",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListEntitlements",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListEntitlements._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListEntitlementsResponse()
            pb_resp = oracledatabase.ListEntitlementsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_entitlements(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_entitlements_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = oracledatabase.ListEntitlementsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_entitlements",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListEntitlements",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListExadbVmClusters(
        _BaseOracleDatabaseRestTransport._BaseListExadbVmClusters,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListExadbVmClusters")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListExadbVmClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListExadbVmClustersResponse:
            r"""Call the list exadb vm clusters method over HTTP.

            Args:
                request (~.oracledatabase.ListExadbVmClustersRequest):
                    The request object. The request for ``ExadbVmCluster.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListExadbVmClustersResponse:
                    The response for ``ExadbVmCluster.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListExadbVmClusters._get_http_options()

            request, metadata = self._interceptor.pre_list_exadb_vm_clusters(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListExadbVmClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListExadbVmClusters._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListExadbVmClusters",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListExadbVmClusters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListExadbVmClusters._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListExadbVmClustersResponse()
            pb_resp = oracledatabase.ListExadbVmClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_exadb_vm_clusters(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_exadb_vm_clusters_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        oracledatabase.ListExadbVmClustersResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_exadb_vm_clusters",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListExadbVmClusters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListExascaleDbStorageVaults(
        _BaseOracleDatabaseRestTransport._BaseListExascaleDbStorageVaults,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListExascaleDbStorageVaults")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse:
            r"""Call the list exascale db storage
            vaults method over HTTP.

                Args:
                    request (~.exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest):
                        The request object. The request for ``ExascaleDbStorageVault.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse:
                        The response for ``ExascaleDbStorageVault.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListExascaleDbStorageVaults._get_http_options()

            request, metadata = self._interceptor.pre_list_exascale_db_storage_vaults(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListExascaleDbStorageVaults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListExascaleDbStorageVaults._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListExascaleDbStorageVaults",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListExascaleDbStorageVaults",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._ListExascaleDbStorageVaults._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse()
            pb_resp = exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_exascale_db_storage_vaults(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_list_exascale_db_storage_vaults_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_exascale_db_storage_vaults",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListExascaleDbStorageVaults",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListGiVersions(
        _BaseOracleDatabaseRestTransport._BaseListGiVersions, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListGiVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: oracledatabase.ListGiVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> oracledatabase.ListGiVersionsResponse:
            r"""Call the list gi versions method over HTTP.

            Args:
                request (~.oracledatabase.ListGiVersionsRequest):
                    The request object. The request for ``GiVersion.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.oracledatabase.ListGiVersionsResponse:
                    The response for ``GiVersion.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListGiVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_gi_versions(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListGiVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListGiVersions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListGiVersions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListGiVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListGiVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = oracledatabase.ListGiVersionsResponse()
            pb_resp = oracledatabase.ListGiVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_gi_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_gi_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = oracledatabase.ListGiVersionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_gi_versions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListGiVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMinorVersions(
        _BaseOracleDatabaseRestTransport._BaseListMinorVersions, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListMinorVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: minor_version.ListMinorVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> minor_version.ListMinorVersionsResponse:
            r"""Call the list minor versions method over HTTP.

            Args:
                request (~.minor_version.ListMinorVersionsRequest):
                    The request object. The request for ``MinorVersion.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.minor_version.ListMinorVersionsResponse:
                    The response for ``MinorVersion.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListMinorVersions._get_http_options()

            request, metadata = self._interceptor.pre_list_minor_versions(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListMinorVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListMinorVersions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListMinorVersions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListMinorVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListMinorVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = minor_version.ListMinorVersionsResponse()
            pb_resp = minor_version.ListMinorVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_minor_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_minor_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = minor_version.ListMinorVersionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_minor_versions",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListMinorVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListOdbNetworks(
        _BaseOracleDatabaseRestTransport._BaseListOdbNetworks, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListOdbNetworks")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_network.ListOdbNetworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> odb_network.ListOdbNetworksResponse:
            r"""Call the list odb networks method over HTTP.

            Args:
                request (~.odb_network.ListOdbNetworksRequest):
                    The request object. The request for ``OdbNetwork.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.odb_network.ListOdbNetworksResponse:
                    The response for ``OdbNetwork.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListOdbNetworks._get_http_options()

            request, metadata = self._interceptor.pre_list_odb_networks(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListOdbNetworks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListOdbNetworks._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListOdbNetworks",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOdbNetworks",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListOdbNetworks._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = odb_network.ListOdbNetworksResponse()
            pb_resp = odb_network.ListOdbNetworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_odb_networks(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_odb_networks_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = odb_network.ListOdbNetworksResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_odb_networks",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOdbNetworks",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListOdbSubnets(
        _BaseOracleDatabaseRestTransport._BaseListOdbSubnets, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListOdbSubnets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: odb_subnet.ListOdbSubnetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> odb_subnet.ListOdbSubnetsResponse:
            r"""Call the list odb subnets method over HTTP.

            Args:
                request (~.odb_subnet.ListOdbSubnetsRequest):
                    The request object. The request for ``OdbSubnet.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.odb_subnet.ListOdbSubnetsResponse:
                    The response for ``OdbSubnet.List``.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListOdbSubnets._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_odb_subnets(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListOdbSubnets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListOdbSubnets._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListOdbSubnets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOdbSubnets",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListOdbSubnets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = odb_subnet.ListOdbSubnetsResponse()
            pb_resp = odb_subnet.ListOdbSubnetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_odb_subnets(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_odb_subnets_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = odb_subnet.ListOdbSubnetsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_odb_subnets",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOdbSubnets",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListPluggableDatabases(
        _BaseOracleDatabaseRestTransport._BaseListPluggableDatabases,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListPluggableDatabases")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: pluggable_database.ListPluggableDatabasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> pluggable_database.ListPluggableDatabasesResponse:
            r"""Call the list pluggable databases method over HTTP.

            Args:
                request (~.pluggable_database.ListPluggableDatabasesRequest):
                    The request object. The request for ``PluggableDatabase.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.pluggable_database.ListPluggableDatabasesResponse:
                    The response for ``PluggableDatabase.List``.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseListPluggableDatabases._get_http_options()

            request, metadata = self._interceptor.pre_list_pluggable_databases(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListPluggableDatabases._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListPluggableDatabases._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListPluggableDatabases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListPluggableDatabases",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._ListPluggableDatabases._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = pluggable_database.ListPluggableDatabasesResponse()
            pb_resp = pluggable_database.ListPluggableDatabasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_pluggable_databases(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_pluggable_databases_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        pluggable_database.ListPluggableDatabasesResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.list_pluggable_databases",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListPluggableDatabases",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RemoveVirtualMachineExadbVmCluster(
        _BaseOracleDatabaseRestTransport._BaseRemoveVirtualMachineExadbVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash(
                "OracleDatabaseRestTransport.RemoveVirtualMachineExadbVmCluster"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.RemoveVirtualMachineExadbVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove virtual machine
            exadb vm cluster method over HTTP.

                Args:
                    request (~.oracledatabase.RemoveVirtualMachineExadbVmClusterRequest):
                        The request object. The request for ``ExadbVmCluster.RemoveVirtualMachine``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseRemoveVirtualMachineExadbVmCluster._get_http_options()

            request, metadata = (
                self._interceptor.pre_remove_virtual_machine_exadb_vm_cluster(
                    request, metadata
                )
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseRemoveVirtualMachineExadbVmCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseRemoveVirtualMachineExadbVmCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseRemoveVirtualMachineExadbVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.RemoveVirtualMachineExadbVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RemoveVirtualMachineExadbVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._RemoveVirtualMachineExadbVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_remove_virtual_machine_exadb_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_remove_virtual_machine_exadb_vm_cluster_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.remove_virtual_machine_exadb_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RemoveVirtualMachineExadbVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RestartAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseRestartAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.RestartAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.RestartAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restart autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.RestartAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Restart``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseRestartAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_restart_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseRestartAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseRestartAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseRestartAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.RestartAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RestartAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._RestartAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_restart_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_restart_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.restart_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RestartAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RestoreAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseRestoreAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.RestoreAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.RestoreAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.RestoreAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Restore``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseRestoreAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_restore_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseRestoreAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseRestoreAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseRestoreAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.RestoreAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RestoreAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._RestoreAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_restore_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_restore_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.restore_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "RestoreAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StartAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseStartAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.StartAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.StartAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start autonomous database method over HTTP.

            Args:
                request (~.oracledatabase.StartAutonomousDatabaseRequest):
                    The request object. The request for ``AutonomousDatabase.Start``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseStartAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_start_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseStartAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseStartAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseStartAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.StartAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "StartAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._StartAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_start_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_start_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.start_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "StartAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StopAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseStopAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.StopAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.StopAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop autonomous database method over HTTP.

            Args:
                request (~.oracledatabase.StopAutonomousDatabaseRequest):
                    The request object. The request for ``AutonomousDatabase.Stop``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseStopAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_stop_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseStopAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseStopAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseStopAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.StopAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "StopAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._StopAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_stop_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_stop_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.stop_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "StopAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SwitchoverAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseSwitchoverAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.SwitchoverAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.SwitchoverAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the switchover autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.SwitchoverAutonomousDatabaseRequest):
                        The request object. The request for
                    ``OracleDatabase.SwitchoverAutonomousDatabase``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseSwitchoverAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_switchover_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseSwitchoverAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseSwitchoverAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseSwitchoverAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.SwitchoverAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "SwitchoverAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._SwitchoverAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_switchover_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = (
                self._interceptor.post_switchover_autonomous_database_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.switchover_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "SwitchoverAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateAutonomousDatabase(
        _BaseOracleDatabaseRestTransport._BaseUpdateAutonomousDatabase,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.UpdateAutonomousDatabase")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.UpdateAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.UpdateAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Update``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseUpdateAutonomousDatabase._get_http_options()

            request, metadata = self._interceptor.pre_update_autonomous_database(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseUpdateAutonomousDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseUpdateAutonomousDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseUpdateAutonomousDatabase._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.UpdateAutonomousDatabase",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "UpdateAutonomousDatabase",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OracleDatabaseRestTransport._UpdateAutonomousDatabase._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_autonomous_database(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_autonomous_database_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.update_autonomous_database",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "UpdateAutonomousDatabase",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateExadbVmCluster(
        _BaseOracleDatabaseRestTransport._BaseUpdateExadbVmCluster,
        OracleDatabaseRestStub,
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.UpdateExadbVmCluster")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: oracledatabase.UpdateExadbVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update exadb vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.UpdateExadbVmClusterRequest):
                    The request object. The request for ``ExadbVmCluster.Update``. We only
                support adding the Virtual Machine to the
                ExadbVmCluster. Rest of the fields in ExadbVmCluster are
                immutable.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = _BaseOracleDatabaseRestTransport._BaseUpdateExadbVmCluster._get_http_options()

            request, metadata = self._interceptor.pre_update_exadb_vm_cluster(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseUpdateExadbVmCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseUpdateExadbVmCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseUpdateExadbVmCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.UpdateExadbVmCluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "UpdateExadbVmCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._UpdateExadbVmCluster._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_exadb_vm_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_exadb_vm_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseClient.update_exadb_vm_cluster",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "UpdateExadbVmCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.CreateAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def create_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudExadataInfrastructureRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCloudExadataInfrastructure(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def create_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudVmClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCloudVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_db_system(
        self,
    ) -> Callable[[gco_db_system.CreateDbSystemRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDbSystem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.CreateExadbVmClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExadbVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [gco_exascale_db_storage_vault.CreateExascaleDbStorageVaultRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExascaleDbStorageVault(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def create_odb_network(
        self,
    ) -> Callable[[gco_odb_network.CreateOdbNetworkRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOdbNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_odb_subnet(
        self,
    ) -> Callable[[gco_odb_subnet.CreateOdbSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOdbSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.DeleteAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def delete_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudExadataInfrastructureRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCloudExadataInfrastructure(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def delete_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudVmClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCloudVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_db_system(
        self,
    ) -> Callable[[db_system.DeleteDbSystemRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDbSystem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.DeleteExadbVmClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExadbVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.DeleteExascaleDbStorageVaultRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExascaleDbStorageVault(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def delete_odb_network(
        self,
    ) -> Callable[[odb_network.DeleteOdbNetworkRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOdbNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_odb_subnet(
        self,
    ) -> Callable[[odb_subnet.DeleteOdbSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOdbSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def failover_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.FailoverAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FailoverAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def generate_autonomous_database_wallet(
        self,
    ) -> Callable[
        [oracledatabase.GenerateAutonomousDatabaseWalletRequest],
        oracledatabase.GenerateAutonomousDatabaseWalletResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAutonomousDatabaseWallet(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def get_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.GetAutonomousDatabaseRequest],
        autonomous_database.AutonomousDatabase,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAutonomousDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.GetCloudExadataInfrastructureRequest],
        exadata_infra.CloudExadataInfrastructure,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCloudExadataInfrastructure(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def get_cloud_vm_cluster(
        self,
    ) -> Callable[[oracledatabase.GetCloudVmClusterRequest], vm_cluster.CloudVmCluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCloudVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_database(
        self,
    ) -> Callable[[database.GetDatabaseRequest], database.Database]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_db_system(
        self,
    ) -> Callable[[db_system.GetDbSystemRequest], db_system.DbSystem]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDbSystem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.GetExadbVmClusterRequest], exadb_vm_cluster.ExadbVmCluster
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExadbVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_exascale_db_storage_vault(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.GetExascaleDbStorageVaultRequest],
        exascale_db_storage_vault.ExascaleDbStorageVault,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExascaleDbStorageVault(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def get_odb_network(
        self,
    ) -> Callable[[odb_network.GetOdbNetworkRequest], odb_network.OdbNetwork]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOdbNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_odb_subnet(
        self,
    ) -> Callable[[odb_subnet.GetOdbSubnetRequest], odb_subnet.OdbSubnet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOdbSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_pluggable_database(
        self,
    ) -> Callable[
        [pluggable_database.GetPluggableDatabaseRequest],
        pluggable_database.PluggableDatabase,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPluggableDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autonomous_database_backups(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseBackupsRequest],
        oracledatabase.ListAutonomousDatabaseBackupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabaseBackups(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_autonomous_database_character_sets(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseCharacterSetsRequest],
        oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabaseCharacterSets(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_autonomous_databases(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabasesRequest],
        oracledatabase.ListAutonomousDatabasesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabases(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_autonomous_db_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDbVersionsRequest],
        oracledatabase.ListAutonomousDbVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDbVersions(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_cloud_exadata_infrastructures(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudExadataInfrastructuresRequest],
        oracledatabase.ListCloudExadataInfrastructuresResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCloudExadataInfrastructures(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_cloud_vm_clusters(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudVmClustersRequest],
        oracledatabase.ListCloudVmClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCloudVmClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_database_character_sets(
        self,
    ) -> Callable[
        [database_character_set.ListDatabaseCharacterSetsRequest],
        database_character_set.ListDatabaseCharacterSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatabaseCharacterSets(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_databases(
        self,
    ) -> Callable[[database.ListDatabasesRequest], database.ListDatabasesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatabases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_db_nodes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbNodesRequest], oracledatabase.ListDbNodesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbNodes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_db_servers(
        self,
    ) -> Callable[
        [oracledatabase.ListDbServersRequest], oracledatabase.ListDbServersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbServers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_db_system_initial_storage_sizes(
        self,
    ) -> Callable[
        [db_system_initial_storage_size.ListDbSystemInitialStorageSizesRequest],
        db_system_initial_storage_size.ListDbSystemInitialStorageSizesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbSystemInitialStorageSizes(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_db_systems(
        self,
    ) -> Callable[[db_system.ListDbSystemsRequest], db_system.ListDbSystemsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbSystems(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_db_system_shapes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbSystemShapesRequest],
        oracledatabase.ListDbSystemShapesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbSystemShapes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_db_versions(
        self,
    ) -> Callable[
        [db_version.ListDbVersionsRequest], db_version.ListDbVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDbVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entitlements(
        self,
    ) -> Callable[
        [oracledatabase.ListEntitlementsRequest],
        oracledatabase.ListEntitlementsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntitlements(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_exadb_vm_clusters(
        self,
    ) -> Callable[
        [oracledatabase.ListExadbVmClustersRequest],
        oracledatabase.ListExadbVmClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExadbVmClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_exascale_db_storage_vaults(
        self,
    ) -> Callable[
        [exascale_db_storage_vault.ListExascaleDbStorageVaultsRequest],
        exascale_db_storage_vault.ListExascaleDbStorageVaultsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExascaleDbStorageVaults(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def list_gi_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListGiVersionsRequest], oracledatabase.ListGiVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGiVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_minor_versions(
        self,
    ) -> Callable[
        [minor_version.ListMinorVersionsRequest],
        minor_version.ListMinorVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMinorVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_odb_networks(
        self,
    ) -> Callable[
        [odb_network.ListOdbNetworksRequest], odb_network.ListOdbNetworksResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOdbNetworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_odb_subnets(
        self,
    ) -> Callable[
        [odb_subnet.ListOdbSubnetsRequest], odb_subnet.ListOdbSubnetsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOdbSubnets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_pluggable_databases(
        self,
    ) -> Callable[
        [pluggable_database.ListPluggableDatabasesRequest],
        pluggable_database.ListPluggableDatabasesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPluggableDatabases(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def remove_virtual_machine_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.RemoveVirtualMachineExadbVmClusterRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveVirtualMachineExadbVmCluster(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def restart_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestartAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestartAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def restore_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestoreAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def start_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.StartAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def stop_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.StopAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def switchover_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.SwitchoverAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SwitchoverAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def update_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.UpdateAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAutonomousDatabase(
            self._session, self._host, self._interceptor
        )  # type: ignore

    @property
    def update_exadb_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.UpdateExadbVmClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExadbVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseOracleDatabaseRestTransport._BaseGetLocation, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseOracleDatabaseRestTransport._BaseListLocations, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseOracleDatabaseRestTransport._BaseCancelOperation, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseCancelOperation._get_http_options()

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseOracleDatabaseRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseOracleDatabaseRestTransport._BaseDeleteOperation, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = _BaseOracleDatabaseRestTransport._BaseDeleteOperation._get_http_options()

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._DeleteOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseOracleDatabaseRestTransport._BaseGetOperation, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseOracleDatabaseRestTransport._BaseListOperations, OracleDatabaseRestStub
    ):
        def __hash__(self):
            return hash("OracleDatabaseRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseOracleDatabaseRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseOracleDatabaseRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOracleDatabaseRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.oracledatabase_v1.OracleDatabaseClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OracleDatabaseRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.oracledatabase_v1.OracleDatabaseAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("OracleDatabaseRestTransport",)
