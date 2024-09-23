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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.oracledatabase_v1.types import (
    autonomous_database,
    exadata_infra,
    oracledatabase,
    vm_cluster,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import OracleDatabaseTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


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

            def pre_list_db_system_shapes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_db_system_shapes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entitlements(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entitlements(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_gi_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_gi_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_autonomous_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_autonomous_database(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OracleDatabaseRestTransport(interceptor=MyCustomOracleDatabaseInterceptor())
        client = OracleDatabaseClient(transport=transport)


    """

    def pre_create_autonomous_database(
        self,
        request: oracledatabase.CreateAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.CreateAutonomousDatabaseRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_create_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.CreateCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.CreateCloudExadataInfrastructureRequest,
        Sequence[Tuple[str, str]],
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_create_cloud_vm_cluster(
        self,
        request: oracledatabase.CreateCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.CreateCloudVmClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_create_cloud_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cloud_vm_cluster

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_delete_autonomous_database(
        self,
        request: oracledatabase.DeleteAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.DeleteAutonomousDatabaseRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.DeleteCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.DeleteCloudExadataInfrastructureRequest,
        Sequence[Tuple[str, str]],
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cloud_vm_cluster(
        self,
        request: oracledatabase.DeleteCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.DeleteCloudVmClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_delete_cloud_vm_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cloud_vm_cluster

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_generate_autonomous_database_wallet(
        self,
        request: oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        Sequence[Tuple[str, str]],
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_get_autonomous_database(
        self,
        request: oracledatabase.GetAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.GetAutonomousDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_autonomous_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_autonomous_database(
        self, response: autonomous_database.AutonomousDatabase
    ) -> autonomous_database.AutonomousDatabase:
        """Post-rpc interceptor for get_autonomous_database

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_get_cloud_exadata_infrastructure(
        self,
        request: oracledatabase.GetCloudExadataInfrastructureRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.GetCloudExadataInfrastructureRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_get_cloud_vm_cluster(
        self,
        request: oracledatabase.GetCloudVmClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.GetCloudVmClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cloud_vm_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_get_cloud_vm_cluster(
        self, response: vm_cluster.CloudVmCluster
    ) -> vm_cluster.CloudVmCluster:
        """Post-rpc interceptor for get_cloud_vm_cluster

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_autonomous_database_backups(
        self,
        request: oracledatabase.ListAutonomousDatabaseBackupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseBackupsRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_autonomous_database_character_sets(
        self,
        request: oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        Sequence[Tuple[str, str]],
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_autonomous_databases(
        self,
        request: oracledatabase.ListAutonomousDatabasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDatabasesRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_autonomous_db_versions(
        self,
        request: oracledatabase.ListAutonomousDbVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.ListAutonomousDbVersionsRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_cloud_exadata_infrastructures(
        self,
        request: oracledatabase.ListCloudExadataInfrastructuresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.ListCloudExadataInfrastructuresRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_cloud_vm_clusters(
        self,
        request: oracledatabase.ListCloudVmClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListCloudVmClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_cloud_vm_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_cloud_vm_clusters(
        self, response: oracledatabase.ListCloudVmClustersResponse
    ) -> oracledatabase.ListCloudVmClustersResponse:
        """Post-rpc interceptor for list_cloud_vm_clusters

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_db_nodes(
        self,
        request: oracledatabase.ListDbNodesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListDbNodesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_db_nodes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_nodes(
        self, response: oracledatabase.ListDbNodesResponse
    ) -> oracledatabase.ListDbNodesResponse:
        """Post-rpc interceptor for list_db_nodes

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_db_servers(
        self,
        request: oracledatabase.ListDbServersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListDbServersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_db_servers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_servers(
        self, response: oracledatabase.ListDbServersResponse
    ) -> oracledatabase.ListDbServersResponse:
        """Post-rpc interceptor for list_db_servers

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_db_system_shapes(
        self,
        request: oracledatabase.ListDbSystemShapesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListDbSystemShapesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_db_system_shapes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_db_system_shapes(
        self, response: oracledatabase.ListDbSystemShapesResponse
    ) -> oracledatabase.ListDbSystemShapesResponse:
        """Post-rpc interceptor for list_db_system_shapes

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_entitlements(
        self,
        request: oracledatabase.ListEntitlementsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListEntitlementsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_entitlements

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_entitlements(
        self, response: oracledatabase.ListEntitlementsResponse
    ) -> oracledatabase.ListEntitlementsResponse:
        """Post-rpc interceptor for list_entitlements

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_list_gi_versions(
        self,
        request: oracledatabase.ListGiVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[oracledatabase.ListGiVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_gi_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OracleDatabase server.
        """
        return request, metadata

    def post_list_gi_versions(
        self, response: oracledatabase.ListGiVersionsResponse
    ) -> oracledatabase.ListGiVersionsResponse:
        """Post-rpc interceptor for list_gi_versions

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_restore_autonomous_database(
        self,
        request: oracledatabase.RestoreAutonomousDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        oracledatabase.RestoreAutonomousDatabaseRequest, Sequence[Tuple[str, str]]
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

        Override in a subclass to manipulate the response
        after it is returned by the OracleDatabase server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
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


class OracleDatabaseRestTransport(OracleDatabaseTransport):
    """REST backend transport for OracleDatabase.

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

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
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

    class _CreateAutonomousDatabase(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("CreateAutonomousDatabase")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "autonomousDatabaseId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.CreateAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.CreateAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Create``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/autonomousDatabases",
                    "body": "autonomous_database",
                },
            ]
            request, metadata = self._interceptor.pre_create_autonomous_database(
                request, metadata
            )
            pb_request = oracledatabase.CreateAutonomousDatabaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_autonomous_database(resp)
            return resp

    class _CreateCloudExadataInfrastructure(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("CreateCloudExadataInfrastructure")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "cloudExadataInfrastructureId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.CreateCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.CreateCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Create``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/cloudExadataInfrastructures",
                    "body": "cloud_exadata_infrastructure",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_cloud_exadata_infrastructure(
                request, metadata
            )
            pb_request = oracledatabase.CreateCloudExadataInfrastructureRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cloud_exadata_infrastructure(resp)
            return resp

    class _CreateCloudVmCluster(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("CreateCloudVmCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "cloudVmClusterId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.CreateCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.CreateCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Create``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/cloudVmClusters",
                    "body": "cloud_vm_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_cloud_vm_cluster(
                request, metadata
            )
            pb_request = oracledatabase.CreateCloudVmClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cloud_vm_cluster(resp)
            return resp

    class _DeleteAutonomousDatabase(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("DeleteAutonomousDatabase")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.DeleteAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.DeleteAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Delete``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/autonomousDatabases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_autonomous_database(
                request, metadata
            )
            pb_request = oracledatabase.DeleteAutonomousDatabaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_autonomous_database(resp)
            return resp

    class _DeleteCloudExadataInfrastructure(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("DeleteCloudExadataInfrastructure")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.DeleteCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.DeleteCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Delete``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/cloudExadataInfrastructures/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_cloud_exadata_infrastructure(
                request, metadata
            )
            pb_request = oracledatabase.DeleteCloudExadataInfrastructureRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_cloud_exadata_infrastructure(resp)
            return resp

    class _DeleteCloudVmCluster(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("DeleteCloudVmCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.DeleteCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.DeleteCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Delete``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/cloudVmClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_cloud_vm_cluster(
                request, metadata
            )
            pb_request = oracledatabase.DeleteCloudVmClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_cloud_vm_cluster(resp)
            return resp

    class _GenerateAutonomousDatabaseWallet(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("GenerateAutonomousDatabaseWallet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.GenerateAutonomousDatabaseWalletRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.GenerateAutonomousDatabaseWalletResponse:
            r"""Call the generate autonomous
            database wallet method over HTTP.

                Args:
                    request (~.oracledatabase.GenerateAutonomousDatabaseWalletRequest):
                        The request object. The request for ``AutonomousDatabase.GenerateWallet``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.oracledatabase.GenerateAutonomousDatabaseWalletResponse:
                        The response for ``AutonomousDatabase.GenerateWallet``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/autonomousDatabases/*}:generateWallet",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_generate_autonomous_database_wallet(
                request, metadata
            )
            pb_request = oracledatabase.GenerateAutonomousDatabaseWalletRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
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
            return resp

    class _GetAutonomousDatabase(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("GetAutonomousDatabase")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.GetAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> autonomous_database.AutonomousDatabase:
            r"""Call the get autonomous database method over HTTP.

            Args:
                request (~.oracledatabase.GetAutonomousDatabaseRequest):
                    The request object. The request for ``AutonomousDatabase.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.autonomous_database.AutonomousDatabase:
                    Details of the Autonomous Database
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/autonomousDatabases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_autonomous_database(
                request, metadata
            )
            pb_request = oracledatabase.GetAutonomousDatabaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _GetCloudExadataInfrastructure(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("GetCloudExadataInfrastructure")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.GetCloudExadataInfrastructureRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> exadata_infra.CloudExadataInfrastructure:
            r"""Call the get cloud exadata
            infrastructure method over HTTP.

                Args:
                    request (~.oracledatabase.GetCloudExadataInfrastructureRequest):
                        The request object. The request for ``CloudExadataInfrastructure.Get``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.exadata_infra.CloudExadataInfrastructure:
                        Represents CloudExadataInfrastructure
                    resource.
                    https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudExadataInfrastructure/

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/cloudExadataInfrastructures/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cloud_exadata_infrastructure(
                request, metadata
            )
            pb_request = oracledatabase.GetCloudExadataInfrastructureRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _GetCloudVmCluster(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("GetCloudVmCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.GetCloudVmClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vm_cluster.CloudVmCluster:
            r"""Call the get cloud vm cluster method over HTTP.

            Args:
                request (~.oracledatabase.GetCloudVmClusterRequest):
                    The request object. The request for ``CloudVmCluster.Get``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vm_cluster.CloudVmCluster:
                    Details of the Cloud VM Cluster
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudVmCluster/

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/cloudVmClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cloud_vm_cluster(
                request, metadata
            )
            pb_request = oracledatabase.GetCloudVmClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListAutonomousDatabaseBackups(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListAutonomousDatabaseBackups")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabaseBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListAutonomousDatabaseBackupsResponse:
            r"""Call the list autonomous database
            backups method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDatabaseBackupsRequest):
                        The request object. The request for ``AutonomousDatabaseBackup.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.oracledatabase.ListAutonomousDatabaseBackupsResponse:
                        The response for ``AutonomousDatabaseBackup.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/autonomousDatabaseBackups",
                },
            ]
            request, metadata = self._interceptor.pre_list_autonomous_database_backups(
                request, metadata
            )
            pb_request = oracledatabase.ListAutonomousDatabaseBackupsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListAutonomousDatabaseCharacterSets(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListAutonomousDatabaseCharacterSets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListAutonomousDatabaseCharacterSetsResponse:
            r"""Call the list autonomous database
            character sets method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDatabaseCharacterSetsRequest):
                        The request object. The request for ``AutonomousDatabaseCharacterSet.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.oracledatabase.ListAutonomousDatabaseCharacterSetsResponse:
                        The response for
                    ``AutonomousDatabaseCharacterSet.List``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/autonomousDatabaseCharacterSets",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_autonomous_database_character_sets(
                request, metadata
            )
            pb_request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListAutonomousDatabases(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListAutonomousDatabases")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDatabasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListAutonomousDatabasesResponse:
            r"""Call the list autonomous databases method over HTTP.

            Args:
                request (~.oracledatabase.ListAutonomousDatabasesRequest):
                    The request object. The request for ``AutonomousDatabase.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListAutonomousDatabasesResponse:
                    The response for ``AutonomousDatabase.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/autonomousDatabases",
                },
            ]
            request, metadata = self._interceptor.pre_list_autonomous_databases(
                request, metadata
            )
            pb_request = oracledatabase.ListAutonomousDatabasesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListAutonomousDbVersions(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListAutonomousDbVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListAutonomousDbVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListAutonomousDbVersionsResponse:
            r"""Call the list autonomous db
            versions method over HTTP.

                Args:
                    request (~.oracledatabase.ListAutonomousDbVersionsRequest):
                        The request object. The request for ``AutonomousDbVersion.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.oracledatabase.ListAutonomousDbVersionsResponse:
                        The response for ``AutonomousDbVersion.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/autonomousDbVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_autonomous_db_versions(
                request, metadata
            )
            pb_request = oracledatabase.ListAutonomousDbVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListCloudExadataInfrastructures(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListCloudExadataInfrastructures")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListCloudExadataInfrastructuresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListCloudExadataInfrastructuresResponse:
            r"""Call the list cloud exadata
            infrastructures method over HTTP.

                Args:
                    request (~.oracledatabase.ListCloudExadataInfrastructuresRequest):
                        The request object. The request for ``CloudExadataInfrastructures.List``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.oracledatabase.ListCloudExadataInfrastructuresResponse:
                        The response for ``CloudExadataInfrastructures.list``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/cloudExadataInfrastructures",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_cloud_exadata_infrastructures(
                request, metadata
            )
            pb_request = oracledatabase.ListCloudExadataInfrastructuresRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListCloudVmClusters(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListCloudVmClusters")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListCloudVmClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListCloudVmClustersResponse:
            r"""Call the list cloud vm clusters method over HTTP.

            Args:
                request (~.oracledatabase.ListCloudVmClustersRequest):
                    The request object. The request for ``CloudVmCluster.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListCloudVmClustersResponse:
                    The response for ``CloudVmCluster.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/cloudVmClusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_cloud_vm_clusters(
                request, metadata
            )
            pb_request = oracledatabase.ListCloudVmClustersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListDbNodes(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListDbNodes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListDbNodesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListDbNodesResponse:
            r"""Call the list db nodes method over HTTP.

            Args:
                request (~.oracledatabase.ListDbNodesRequest):
                    The request object. The request for ``DbNode.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListDbNodesResponse:
                    The response for ``DbNode.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/cloudVmClusters/*}/dbNodes",
                },
            ]
            request, metadata = self._interceptor.pre_list_db_nodes(request, metadata)
            pb_request = oracledatabase.ListDbNodesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListDbServers(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListDbServers")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListDbServersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListDbServersResponse:
            r"""Call the list db servers method over HTTP.

            Args:
                request (~.oracledatabase.ListDbServersRequest):
                    The request object. The request for ``DbServer.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListDbServersResponse:
                    The response for ``DbServer.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/cloudExadataInfrastructures/*}/dbServers",
                },
            ]
            request, metadata = self._interceptor.pre_list_db_servers(request, metadata)
            pb_request = oracledatabase.ListDbServersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListDbSystemShapes(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListDbSystemShapes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListDbSystemShapesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListDbSystemShapesResponse:
            r"""Call the list db system shapes method over HTTP.

            Args:
                request (~.oracledatabase.ListDbSystemShapesRequest):
                    The request object. The request for ``DbSystemShape.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListDbSystemShapesResponse:
                    The response for ``DbSystemShape.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/dbSystemShapes",
                },
            ]
            request, metadata = self._interceptor.pre_list_db_system_shapes(
                request, metadata
            )
            pb_request = oracledatabase.ListDbSystemShapesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListEntitlements(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListEntitlements")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListEntitlementsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListEntitlementsResponse:
            r"""Call the list entitlements method over HTTP.

            Args:
                request (~.oracledatabase.ListEntitlementsRequest):
                    The request object. The request for ``Entitlement.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListEntitlementsResponse:
                    The response for ``Entitlement.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/entitlements",
                },
            ]
            request, metadata = self._interceptor.pre_list_entitlements(
                request, metadata
            )
            pb_request = oracledatabase.ListEntitlementsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _ListGiVersions(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("ListGiVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.ListGiVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> oracledatabase.ListGiVersionsResponse:
            r"""Call the list gi versions method over HTTP.

            Args:
                request (~.oracledatabase.ListGiVersionsRequest):
                    The request object. The request for ``GiVersion.List``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.oracledatabase.ListGiVersionsResponse:
                    The response for ``GiVersion.List``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/giVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_gi_versions(
                request, metadata
            )
            pb_request = oracledatabase.ListGiVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
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
            return resp

    class _RestoreAutonomousDatabase(OracleDatabaseRestStub):
        def __hash__(self):
            return hash("RestoreAutonomousDatabase")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: oracledatabase.RestoreAutonomousDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore autonomous
            database method over HTTP.

                Args:
                    request (~.oracledatabase.RestoreAutonomousDatabaseRequest):
                        The request object. The request for ``AutonomousDatabase.Restore``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/autonomousDatabases/*}:restore",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_restore_autonomous_database(
                request, metadata
            )
            pb_request = oracledatabase.RestoreAutonomousDatabaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_autonomous_database(resp)
            return resp

    @property
    def create_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.CreateAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAutonomousDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudExadataInfrastructureRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCloudExadataInfrastructure(self._session, self._host, self._interceptor)  # type: ignore

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
    def delete_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.DeleteAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAutonomousDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudExadataInfrastructureRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCloudExadataInfrastructure(self._session, self._host, self._interceptor)  # type: ignore

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
    def generate_autonomous_database_wallet(
        self,
    ) -> Callable[
        [oracledatabase.GenerateAutonomousDatabaseWalletRequest],
        oracledatabase.GenerateAutonomousDatabaseWalletResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAutonomousDatabaseWallet(self._session, self._host, self._interceptor)  # type: ignore

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
        return self._GetCloudExadataInfrastructure(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cloud_vm_cluster(
        self,
    ) -> Callable[[oracledatabase.GetCloudVmClusterRequest], vm_cluster.CloudVmCluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCloudVmCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autonomous_database_backups(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseBackupsRequest],
        oracledatabase.ListAutonomousDatabaseBackupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabaseBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autonomous_database_character_sets(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseCharacterSetsRequest],
        oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabaseCharacterSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autonomous_databases(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabasesRequest],
        oracledatabase.ListAutonomousDatabasesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDatabases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autonomous_db_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDbVersionsRequest],
        oracledatabase.ListAutonomousDbVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutonomousDbVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cloud_exadata_infrastructures(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudExadataInfrastructuresRequest],
        oracledatabase.ListCloudExadataInfrastructuresResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCloudExadataInfrastructures(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_gi_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListGiVersionsRequest], oracledatabase.ListGiVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGiVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestoreAutonomousDatabaseRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreAutonomousDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(OracleDatabaseRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(OracleDatabaseRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(OracleDatabaseRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(OracleDatabaseRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(OracleDatabaseRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(OracleDatabaseRestStub):
        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("OracleDatabaseRestTransport",)
