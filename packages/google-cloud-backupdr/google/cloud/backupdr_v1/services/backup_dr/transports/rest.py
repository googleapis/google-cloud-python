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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.backupdr_v1.types import (
    backupdr,
    backupplan,
    backupplanassociation,
    backupvault,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseBackupDRRestTransport

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


class BackupDRRestInterceptor:
    """Interceptor for BackupDR.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BackupDRRestTransport.

    .. code-block:: python
        class MyCustomBackupDRInterceptor(BackupDRRestInterceptor):
            def pre_create_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup_plan_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_plan_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_management_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_management_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_plan_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_plan_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_management_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_management_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_usable_backup_vaults(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_usable_backup_vaults(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_plan_association(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_plan_association(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_management_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_management_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_plan_associations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_plan_associations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_plans(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_plans(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_vaults(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_vaults(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_management_servers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_management_servers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_trigger_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_trigger_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BackupDRRestTransport(interceptor=MyCustomBackupDRInterceptor())
        client = BackupDRClient(transport=transport)


    """

    def pre_create_backup_plan(
        self,
        request: backupplan.CreateBackupPlanRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplan.CreateBackupPlanRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_create_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_plan_association(
        self,
        request: backupplanassociation.CreateBackupPlanAssociationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplanassociation.CreateBackupPlanAssociationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_backup_plan_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_create_backup_plan_association(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_plan_association

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_vault(
        self,
        request: backupvault.CreateBackupVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.CreateBackupVaultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_create_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_create_management_server(
        self,
        request: backupdr.CreateManagementServerRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupdr.CreateManagementServerRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_management_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_create_management_server(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_management_server

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: backupvault.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.DeleteBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_plan(
        self,
        request: backupplan.DeleteBackupPlanRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplan.DeleteBackupPlanRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_plan_association(
        self,
        request: backupplanassociation.DeleteBackupPlanAssociationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplanassociation.DeleteBackupPlanAssociationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_backup_plan_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_backup_plan_association(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_plan_association

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_vault(
        self,
        request: backupvault.DeleteBackupVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.DeleteBackupVaultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_delete_management_server(
        self,
        request: backupdr.DeleteManagementServerRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupdr.DeleteManagementServerRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_management_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_management_server(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_management_server

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_usable_backup_vaults(
        self,
        request: backupvault.FetchUsableBackupVaultsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.FetchUsableBackupVaultsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for fetch_usable_backup_vaults

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_fetch_usable_backup_vaults(
        self, response: backupvault.FetchUsableBackupVaultsResponse
    ) -> backupvault.FetchUsableBackupVaultsResponse:
        """Post-rpc interceptor for fetch_usable_backup_vaults

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self,
        request: backupvault.GetBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[backupvault.GetBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_backup(self, response: backupvault.Backup) -> backupvault.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_plan(
        self,
        request: backupplan.GetBackupPlanRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplan.GetBackupPlanRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_backup_plan(
        self, response: backupplan.BackupPlan
    ) -> backupplan.BackupPlan:
        """Post-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_plan_association(
        self,
        request: backupplanassociation.GetBackupPlanAssociationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplanassociation.GetBackupPlanAssociationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_backup_plan_association

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_backup_plan_association(
        self, response: backupplanassociation.BackupPlanAssociation
    ) -> backupplanassociation.BackupPlanAssociation:
        """Post-rpc interceptor for get_backup_plan_association

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_vault(
        self,
        request: backupvault.GetBackupVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.GetBackupVaultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_backup_vault(
        self, response: backupvault.BackupVault
    ) -> backupvault.BackupVault:
        """Post-rpc interceptor for get_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_source(
        self,
        request: backupvault.GetDataSourceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.GetDataSourceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_data_source(
        self, response: backupvault.DataSource
    ) -> backupvault.DataSource:
        """Post-rpc interceptor for get_data_source

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_management_server(
        self,
        request: backupdr.GetManagementServerRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupdr.GetManagementServerRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_management_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_management_server(
        self, response: backupdr.ManagementServer
    ) -> backupdr.ManagementServer:
        """Post-rpc interceptor for get_management_server

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_plan_associations(
        self,
        request: backupplanassociation.ListBackupPlanAssociationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplanassociation.ListBackupPlanAssociationsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_backup_plan_associations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_backup_plan_associations(
        self, response: backupplanassociation.ListBackupPlanAssociationsResponse
    ) -> backupplanassociation.ListBackupPlanAssociationsResponse:
        """Post-rpc interceptor for list_backup_plan_associations

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_plans(
        self,
        request: backupplan.ListBackupPlansRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplan.ListBackupPlansRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_backup_plans(
        self, response: backupplan.ListBackupPlansResponse
    ) -> backupplan.ListBackupPlansResponse:
        """Post-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self,
        request: backupvault.ListBackupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[backupvault.ListBackupsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_backups(
        self, response: backupvault.ListBackupsResponse
    ) -> backupvault.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_vaults(
        self,
        request: backupvault.ListBackupVaultsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.ListBackupVaultsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_backup_vaults

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_backup_vaults(
        self, response: backupvault.ListBackupVaultsResponse
    ) -> backupvault.ListBackupVaultsResponse:
        """Post-rpc interceptor for list_backup_vaults

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_sources(
        self,
        request: backupvault.ListDataSourcesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.ListDataSourcesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_data_sources(
        self, response: backupvault.ListDataSourcesResponse
    ) -> backupvault.ListDataSourcesResponse:
        """Post-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_list_management_servers(
        self,
        request: backupdr.ListManagementServersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupdr.ListManagementServersRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_management_servers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_management_servers(
        self, response: backupdr.ListManagementServersResponse
    ) -> backupdr.ListManagementServersResponse:
        """Post-rpc interceptor for list_management_servers

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_restore_backup(
        self,
        request: backupvault.RestoreBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.RestoreBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for restore_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_restore_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_trigger_backup(
        self,
        request: backupplanassociation.TriggerBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupplanassociation.TriggerBackupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for trigger_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_trigger_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for trigger_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: backupvault.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.UpdateBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_update_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup_vault(
        self,
        request: backupvault.UpdateBackupVaultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.UpdateBackupVaultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_update_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_source(
        self,
        request: backupvault.UpdateDataSourceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        backupvault.UpdateDataSourceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_update_data_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_data_source

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
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
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.TestIamPermissionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
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
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
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
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
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
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
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
        before they are sent to the BackupDR server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the BackupDR server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BackupDRRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BackupDRRestInterceptor


class BackupDRRestTransport(_BaseBackupDRRestTransport):
    """REST backend synchronous transport for BackupDR.

    The BackupDR Service

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "backupdr.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BackupDRRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'backupdr.googleapis.com').
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
        self._interceptor = interceptor or BackupDRRestInterceptor()
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

    class _CreateBackupPlan(
        _BaseBackupDRRestTransport._BaseCreateBackupPlan, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.CreateBackupPlan")

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
            request: backupplan.CreateBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup plan method over HTTP.

            Args:
                request (~.backupplan.CreateBackupPlanRequest):
                    The request object. The request message for creating a ``BackupPlan``.
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
                _BaseBackupDRRestTransport._BaseCreateBackupPlan._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_backup_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseCreateBackupPlan._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBackupDRRestTransport._BaseCreateBackupPlan._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseCreateBackupPlan._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.CreateBackupPlan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupPlan",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._CreateBackupPlan._get_response(
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

            resp = self._interceptor.post_create_backup_plan(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.create_backup_plan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupPlan",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateBackupPlanAssociation(
        _BaseBackupDRRestTransport._BaseCreateBackupPlanAssociation, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.CreateBackupPlanAssociation")

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
            request: backupplanassociation.CreateBackupPlanAssociationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup plan
            association method over HTTP.

                Args:
                    request (~.backupplanassociation.CreateBackupPlanAssociationRequest):
                        The request object. Request message for creating a backup
                    plan.
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
                _BaseBackupDRRestTransport._BaseCreateBackupPlanAssociation._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_backup_plan_association(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseCreateBackupPlanAssociation._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupDRRestTransport._BaseCreateBackupPlanAssociation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseCreateBackupPlanAssociation._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.CreateBackupPlanAssociation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupPlanAssociation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._CreateBackupPlanAssociation._get_response(
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

            resp = self._interceptor.post_create_backup_plan_association(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.create_backup_plan_association",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupPlanAssociation",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateBackupVault(
        _BaseBackupDRRestTransport._BaseCreateBackupVault, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.CreateBackupVault")

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
            request: backupvault.CreateBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup vault method over HTTP.

            Args:
                request (~.backupvault.CreateBackupVaultRequest):
                    The request object. Message for creating a BackupVault.
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
                _BaseBackupDRRestTransport._BaseCreateBackupVault._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_backup_vault(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseCreateBackupVault._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupDRRestTransport._BaseCreateBackupVault._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseCreateBackupVault._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.CreateBackupVault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._CreateBackupVault._get_response(
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

            resp = self._interceptor.post_create_backup_vault(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.create_backup_vault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateBackupVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateManagementServer(
        _BaseBackupDRRestTransport._BaseCreateManagementServer, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.CreateManagementServer")

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
            request: backupdr.CreateManagementServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create management server method over HTTP.

            Args:
                request (~.backupdr.CreateManagementServerRequest):
                    The request object. Request message for creating a
                management server instance.
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
                _BaseBackupDRRestTransport._BaseCreateManagementServer._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_management_server(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseCreateManagementServer._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupDRRestTransport._BaseCreateManagementServer._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseCreateManagementServer._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.CreateManagementServer",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateManagementServer",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._CreateManagementServer._get_response(
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

            resp = self._interceptor.post_create_management_server(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.create_management_server",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CreateManagementServer",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteBackup(_BaseBackupDRRestTransport._BaseDeleteBackup, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteBackup")

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
            request: backupvault.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.backupvault.DeleteBackupRequest):
                    The request object. Message for deleting a Backup.
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
                _BaseBackupDRRestTransport._BaseDeleteBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseDeleteBackup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseDeleteBackup._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteBackup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteBackup._get_response(
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

            resp = self._interceptor.post_delete_backup(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.delete_backup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteBackupPlan(
        _BaseBackupDRRestTransport._BaseDeleteBackupPlan, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteBackupPlan")

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
            request: backupplan.DeleteBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup plan method over HTTP.

            Args:
                request (~.backupplan.DeleteBackupPlanRequest):
                    The request object. The request message for deleting a ``BackupPlan``.
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
                _BaseBackupDRRestTransport._BaseDeleteBackupPlan._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_backup_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseDeleteBackupPlan._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseDeleteBackupPlan._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteBackupPlan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupPlan",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteBackupPlan._get_response(
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

            resp = self._interceptor.post_delete_backup_plan(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.delete_backup_plan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupPlan",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteBackupPlanAssociation(
        _BaseBackupDRRestTransport._BaseDeleteBackupPlanAssociation, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteBackupPlanAssociation")

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
            request: backupplanassociation.DeleteBackupPlanAssociationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup plan
            association method over HTTP.

                Args:
                    request (~.backupplanassociation.DeleteBackupPlanAssociationRequest):
                        The request object. Request message for deleting a backup
                    plan association.
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
                _BaseBackupDRRestTransport._BaseDeleteBackupPlanAssociation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_backup_plan_association(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseDeleteBackupPlanAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseDeleteBackupPlanAssociation._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteBackupPlanAssociation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupPlanAssociation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteBackupPlanAssociation._get_response(
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

            resp = self._interceptor.post_delete_backup_plan_association(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.delete_backup_plan_association",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupPlanAssociation",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteBackupVault(
        _BaseBackupDRRestTransport._BaseDeleteBackupVault, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteBackupVault")

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
            request: backupvault.DeleteBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup vault method over HTTP.

            Args:
                request (~.backupvault.DeleteBackupVaultRequest):
                    The request object. Message for deleting a BackupVault.
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
                _BaseBackupDRRestTransport._BaseDeleteBackupVault._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_backup_vault(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseDeleteBackupVault._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseDeleteBackupVault._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteBackupVault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteBackupVault._get_response(
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

            resp = self._interceptor.post_delete_backup_vault(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.delete_backup_vault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteBackupVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteManagementServer(
        _BaseBackupDRRestTransport._BaseDeleteManagementServer, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteManagementServer")

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
            request: backupdr.DeleteManagementServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete management server method over HTTP.

            Args:
                request (~.backupdr.DeleteManagementServerRequest):
                    The request object. Request message for deleting a
                management server instance.
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
                _BaseBackupDRRestTransport._BaseDeleteManagementServer._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_management_server(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseDeleteManagementServer._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseDeleteManagementServer._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteManagementServer",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteManagementServer",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteManagementServer._get_response(
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

            resp = self._interceptor.post_delete_management_server(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.delete_management_server",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteManagementServer",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchUsableBackupVaults(
        _BaseBackupDRRestTransport._BaseFetchUsableBackupVaults, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.FetchUsableBackupVaults")

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
            request: backupvault.FetchUsableBackupVaultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.FetchUsableBackupVaultsResponse:
            r"""Call the fetch usable backup
            vaults method over HTTP.

                Args:
                    request (~.backupvault.FetchUsableBackupVaultsRequest):
                        The request object. Request message for fetching usable
                    BackupVaults.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.backupvault.FetchUsableBackupVaultsResponse:
                        Response message for fetching usable
                    BackupVaults.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseFetchUsableBackupVaults._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_usable_backup_vaults(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseFetchUsableBackupVaults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseFetchUsableBackupVaults._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.FetchUsableBackupVaults",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "FetchUsableBackupVaults",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._FetchUsableBackupVaults._get_response(
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
            resp = backupvault.FetchUsableBackupVaultsResponse()
            pb_resp = backupvault.FetchUsableBackupVaultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_usable_backup_vaults(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        backupvault.FetchUsableBackupVaultsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.fetch_usable_backup_vaults",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "FetchUsableBackupVaults",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackup(_BaseBackupDRRestTransport._BaseGetBackup, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetBackup")

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
            request: backupvault.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.backupvault.GetBackupRequest):
                    The request object. Request message for getting a Backup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.Backup:
                    Message describing a Backup object.
            """

            http_options = _BaseBackupDRRestTransport._BaseGetBackup._get_http_options()

            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetBackup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetBackup._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetBackup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetBackup._get_response(
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
            resp = backupvault.Backup()
            pb_resp = backupvault.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.Backup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_backup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackupPlan(
        _BaseBackupDRRestTransport._BaseGetBackupPlan, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetBackupPlan")

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
            request: backupplan.GetBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupplan.BackupPlan:
            r"""Call the get backup plan method over HTTP.

            Args:
                request (~.backupplan.GetBackupPlanRequest):
                    The request object. The request message for getting a ``BackupPlan``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupplan.BackupPlan:
                    A ``BackupPlan`` specifies some common fields, such as
                ``description`` as well as one or more ``BackupRule``
                messages. Each ``BackupRule`` has a retention policy and
                defines a schedule by which the system is to perform
                backup workloads.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetBackupPlan._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_backup_plan(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetBackupPlan._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetBackupPlan._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetBackupPlan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupPlan",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetBackupPlan._get_response(
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
            resp = backupplan.BackupPlan()
            pb_resp = backupplan.BackupPlan.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup_plan(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupplan.BackupPlan.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_backup_plan",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupPlan",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackupPlanAssociation(
        _BaseBackupDRRestTransport._BaseGetBackupPlanAssociation, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetBackupPlanAssociation")

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
            request: backupplanassociation.GetBackupPlanAssociationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupplanassociation.BackupPlanAssociation:
            r"""Call the get backup plan
            association method over HTTP.

                Args:
                    request (~.backupplanassociation.GetBackupPlanAssociationRequest):
                        The request object. Request message for getting a
                    BackupPlanAssociation resource.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.backupplanassociation.BackupPlanAssociation:
                        A BackupPlanAssociation represents a
                    single BackupPlanAssociation which
                    contains details like workload, backup
                    plan etc

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetBackupPlanAssociation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_backup_plan_association(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseGetBackupPlanAssociation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseGetBackupPlanAssociation._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetBackupPlanAssociation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupPlanAssociation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetBackupPlanAssociation._get_response(
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
            resp = backupplanassociation.BackupPlanAssociation()
            pb_resp = backupplanassociation.BackupPlanAssociation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup_plan_association(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        backupplanassociation.BackupPlanAssociation.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_backup_plan_association",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupPlanAssociation",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackupVault(
        _BaseBackupDRRestTransport._BaseGetBackupVault, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetBackupVault")

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
            request: backupvault.GetBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.BackupVault:
            r"""Call the get backup vault method over HTTP.

            Args:
                request (~.backupvault.GetBackupVaultRequest):
                    The request object. Request message for getting a
                BackupVault.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.BackupVault:
                    Message describing a BackupVault
                object.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetBackupVault._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_backup_vault(
                request, metadata
            )
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetBackupVault._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetBackupVault._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetBackupVault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetBackupVault._get_response(
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
            resp = backupvault.BackupVault()
            pb_resp = backupvault.BackupVault.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup_vault(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.BackupVault.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_backup_vault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetBackupVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetDataSource(
        _BaseBackupDRRestTransport._BaseGetDataSource, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetDataSource")

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
            request: backupvault.GetDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.DataSource:
            r"""Call the get data source method over HTTP.

            Args:
                request (~.backupvault.GetDataSourceRequest):
                    The request object. Request message for getting a
                DataSource instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.DataSource:
                    Message describing a DataSource
                object. Datasource object used to
                represent Datasource details for both
                admin and basic view.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetDataSource._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_data_source(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetDataSource._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetDataSource._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetDataSource",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetDataSource",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetDataSource._get_response(
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
            resp = backupvault.DataSource()
            pb_resp = backupvault.DataSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_data_source(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.DataSource.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_data_source",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetDataSource",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetManagementServer(
        _BaseBackupDRRestTransport._BaseGetManagementServer, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetManagementServer")

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
            request: backupdr.GetManagementServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupdr.ManagementServer:
            r"""Call the get management server method over HTTP.

            Args:
                request (~.backupdr.GetManagementServerRequest):
                    The request object. Request message for getting a
                management server instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupdr.ManagementServer:
                    ManagementServer describes a single
                BackupDR ManagementServer instance.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetManagementServer._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_management_server(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseGetManagementServer._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseGetManagementServer._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetManagementServer",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetManagementServer",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetManagementServer._get_response(
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
            resp = backupdr.ManagementServer()
            pb_resp = backupdr.ManagementServer.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_management_server(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupdr.ManagementServer.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.get_management_server",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetManagementServer",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackupPlanAssociations(
        _BaseBackupDRRestTransport._BaseListBackupPlanAssociations, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListBackupPlanAssociations")

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
            request: backupplanassociation.ListBackupPlanAssociationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupplanassociation.ListBackupPlanAssociationsResponse:
            r"""Call the list backup plan
            associations method over HTTP.

                Args:
                    request (~.backupplanassociation.ListBackupPlanAssociationsRequest):
                        The request object. Request message for List
                    BackupPlanAssociation
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.backupplanassociation.ListBackupPlanAssociationsResponse:
                        Response message for List
                    BackupPlanAssociation

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListBackupPlanAssociations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backup_plan_associations(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseListBackupPlanAssociations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseListBackupPlanAssociations._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListBackupPlanAssociations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupPlanAssociations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListBackupPlanAssociations._get_response(
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
            resp = backupplanassociation.ListBackupPlanAssociationsResponse()
            pb_resp = backupplanassociation.ListBackupPlanAssociationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backup_plan_associations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupplanassociation.ListBackupPlanAssociationsResponse.to_json(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_backup_plan_associations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupPlanAssociations",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackupPlans(
        _BaseBackupDRRestTransport._BaseListBackupPlans, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListBackupPlans")

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
            request: backupplan.ListBackupPlansRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupplan.ListBackupPlansResponse:
            r"""Call the list backup plans method over HTTP.

            Args:
                request (~.backupplan.ListBackupPlansRequest):
                    The request object. The request message for getting a list ``BackupPlan``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupplan.ListBackupPlansResponse:
                    The response message for getting a list of
                ``BackupPlan``.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListBackupPlans._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backup_plans(
                request, metadata
            )
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseListBackupPlans._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListBackupPlans._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListBackupPlans",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupPlans",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListBackupPlans._get_response(
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
            resp = backupplan.ListBackupPlansResponse()
            pb_resp = backupplan.ListBackupPlansResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backup_plans(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupplan.ListBackupPlansResponse.to_json(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_backup_plans",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupPlans",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackups(_BaseBackupDRRestTransport._BaseListBackups, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListBackups")

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
            request: backupvault.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.backupvault.ListBackupsRequest):
                    The request object. Request message for listing Backups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.ListBackupsResponse:
                    Response message for listing Backups.
            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListBackups._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseListBackups._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListBackups._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListBackups",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackups",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListBackups._get_response(
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
            resp = backupvault.ListBackupsResponse()
            pb_resp = backupvault.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backups(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.ListBackupsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_backups",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackups",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackupVaults(
        _BaseBackupDRRestTransport._BaseListBackupVaults, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListBackupVaults")

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
            request: backupvault.ListBackupVaultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.ListBackupVaultsResponse:
            r"""Call the list backup vaults method over HTTP.

            Args:
                request (~.backupvault.ListBackupVaultsRequest):
                    The request object. Request message for listing
                backupvault stores.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.ListBackupVaultsResponse:
                    Response message for listing
                BackupVaults.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListBackupVaults._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backup_vaults(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseListBackupVaults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListBackupVaults._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListBackupVaults",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupVaults",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListBackupVaults._get_response(
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
            resp = backupvault.ListBackupVaultsResponse()
            pb_resp = backupvault.ListBackupVaultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backup_vaults(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.ListBackupVaultsResponse.to_json(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_backup_vaults",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListBackupVaults",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDataSources(
        _BaseBackupDRRestTransport._BaseListDataSources, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListDataSources")

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
            request: backupvault.ListDataSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupvault.ListDataSourcesResponse:
            r"""Call the list data sources method over HTTP.

            Args:
                request (~.backupvault.ListDataSourcesRequest):
                    The request object. Request message for listing
                DataSources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupvault.ListDataSourcesResponse:
                    Response message for listing
                DataSources.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListDataSources._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_data_sources(
                request, metadata
            )
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseListDataSources._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListDataSources._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListDataSources",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListDataSources",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListDataSources._get_response(
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
            resp = backupvault.ListDataSourcesResponse()
            pb_resp = backupvault.ListDataSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_data_sources(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupvault.ListDataSourcesResponse.to_json(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_data_sources",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListDataSources",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListManagementServers(
        _BaseBackupDRRestTransport._BaseListManagementServers, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListManagementServers")

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
            request: backupdr.ListManagementServersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> backupdr.ListManagementServersResponse:
            r"""Call the list management servers method over HTTP.

            Args:
                request (~.backupdr.ListManagementServersRequest):
                    The request object. Request message for listing
                management servers.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.backupdr.ListManagementServersResponse:
                    Response message for listing
                management servers.

            """

            http_options = (
                _BaseBackupDRRestTransport._BaseListManagementServers._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_management_servers(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseListManagementServers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseListManagementServers._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListManagementServers",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListManagementServers",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListManagementServers._get_response(
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
            resp = backupdr.ListManagementServersResponse()
            pb_resp = backupdr.ListManagementServersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_management_servers(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = backupdr.ListManagementServersResponse.to_json(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.list_management_servers",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListManagementServers",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RestoreBackup(
        _BaseBackupDRRestTransport._BaseRestoreBackup, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.RestoreBackup")

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
            request: backupvault.RestoreBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore backup method over HTTP.

            Args:
                request (~.backupvault.RestoreBackupRequest):
                    The request object. Request message for restoring from a
                Backup.
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
                _BaseBackupDRRestTransport._BaseRestoreBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_restore_backup(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseRestoreBackup._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBackupDRRestTransport._BaseRestoreBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseRestoreBackup._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.RestoreBackup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "RestoreBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._RestoreBackup._get_response(
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

            resp = self._interceptor.post_restore_backup(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.restore_backup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "RestoreBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TriggerBackup(
        _BaseBackupDRRestTransport._BaseTriggerBackup, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.TriggerBackup")

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
            request: backupplanassociation.TriggerBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the trigger backup method over HTTP.

            Args:
                request (~.backupplanassociation.TriggerBackupRequest):
                    The request object. Request message for triggering a
                backup.
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
                _BaseBackupDRRestTransport._BaseTriggerBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_trigger_backup(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseTriggerBackup._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBackupDRRestTransport._BaseTriggerBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseTriggerBackup._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.TriggerBackup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "TriggerBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._TriggerBackup._get_response(
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

            resp = self._interceptor.post_trigger_backup(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.trigger_backup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "TriggerBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateBackup(_BaseBackupDRRestTransport._BaseUpdateBackup, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.UpdateBackup")

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
            request: backupvault.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.backupvault.UpdateBackupRequest):
                    The request object. Request message for updating a
                Backup.
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
                _BaseBackupDRRestTransport._BaseUpdateBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseUpdateBackup._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBackupDRRestTransport._BaseUpdateBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseUpdateBackup._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.UpdateBackup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._UpdateBackup._get_response(
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

            resp = self._interceptor.post_update_backup(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.update_backup",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateBackupVault(
        _BaseBackupDRRestTransport._BaseUpdateBackupVault, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.UpdateBackupVault")

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
            request: backupvault.UpdateBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup vault method over HTTP.

            Args:
                request (~.backupvault.UpdateBackupVaultRequest):
                    The request object. Request message for updating a
                BackupVault.
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
                _BaseBackupDRRestTransport._BaseUpdateBackupVault._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_backup_vault(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseUpdateBackupVault._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupDRRestTransport._BaseUpdateBackupVault._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseUpdateBackupVault._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.UpdateBackupVault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateBackupVault",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._UpdateBackupVault._get_response(
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

            resp = self._interceptor.post_update_backup_vault(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.update_backup_vault",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateBackupVault",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateDataSource(
        _BaseBackupDRRestTransport._BaseUpdateDataSource, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.UpdateDataSource")

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
            request: backupvault.UpdateDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update data source method over HTTP.

            Args:
                request (~.backupvault.UpdateDataSourceRequest):
                    The request object. Request message for updating a data
                source instance.
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
                _BaseBackupDRRestTransport._BaseUpdateDataSource._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_data_source(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseUpdateDataSource._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBackupDRRestTransport._BaseUpdateDataSource._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseUpdateDataSource._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.UpdateDataSource",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateDataSource",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._UpdateDataSource._get_response(
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

            resp = self._interceptor.post_update_data_source(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRClient.update_data_source",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "UpdateDataSource",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_backup_plan(
        self,
    ) -> Callable[[backupplan.CreateBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.CreateBackupPlanAssociationRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupPlanAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_vault(
        self,
    ) -> Callable[[backupvault.CreateBackupVaultRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_management_server(
        self,
    ) -> Callable[[backupdr.CreateManagementServerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateManagementServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[backupvault.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_plan(
        self,
    ) -> Callable[[backupplan.DeleteBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.DeleteBackupPlanAssociationRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupPlanAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_vault(
        self,
    ) -> Callable[[backupvault.DeleteBackupVaultRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_management_server(
        self,
    ) -> Callable[[backupdr.DeleteManagementServerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteManagementServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_usable_backup_vaults(
        self,
    ) -> Callable[
        [backupvault.FetchUsableBackupVaultsRequest],
        backupvault.FetchUsableBackupVaultsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchUsableBackupVaults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(
        self,
    ) -> Callable[[backupvault.GetBackupRequest], backupvault.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_plan(
        self,
    ) -> Callable[[backupplan.GetBackupPlanRequest], backupplan.BackupPlan]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.GetBackupPlanAssociationRequest],
        backupplanassociation.BackupPlanAssociation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupPlanAssociation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_vault(
        self,
    ) -> Callable[[backupvault.GetBackupVaultRequest], backupvault.BackupVault]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_source(
        self,
    ) -> Callable[[backupvault.GetDataSourceRequest], backupvault.DataSource]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_management_server(
        self,
    ) -> Callable[[backupdr.GetManagementServerRequest], backupdr.ManagementServer]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetManagementServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_plan_associations(
        self,
    ) -> Callable[
        [backupplanassociation.ListBackupPlanAssociationsRequest],
        backupplanassociation.ListBackupPlanAssociationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupPlanAssociations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_plans(
        self,
    ) -> Callable[
        [backupplan.ListBackupPlansRequest], backupplan.ListBackupPlansResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupPlans(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[[backupvault.ListBackupsRequest], backupvault.ListBackupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_vaults(
        self,
    ) -> Callable[
        [backupvault.ListBackupVaultsRequest], backupvault.ListBackupVaultsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupVaults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_sources(
        self,
    ) -> Callable[
        [backupvault.ListDataSourcesRequest], backupvault.ListDataSourcesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_management_servers(
        self,
    ) -> Callable[
        [backupdr.ListManagementServersRequest], backupdr.ListManagementServersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListManagementServers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_backup(
        self,
    ) -> Callable[[backupvault.RestoreBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def trigger_backup(
        self,
    ) -> Callable[
        [backupplanassociation.TriggerBackupRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TriggerBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[[backupvault.UpdateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup_vault(
        self,
    ) -> Callable[[backupvault.UpdateBackupVaultRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_source(
        self,
    ) -> Callable[[backupvault.UpdateDataSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseBackupDRRestTransport._BaseGetLocation, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetLocation")

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
                _BaseBackupDRRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetLocation._get_response(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
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
        _BaseBackupDRRestTransport._BaseListLocations, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListLocations")

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
                _BaseBackupDRRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListLocations._get_response(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(_BaseBackupDRRestTransport._BaseGetIamPolicy, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseBackupDRRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetIamPolicy._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(_BaseBackupDRRestTransport._BaseSetIamPolicy, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseBackupDRRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseSetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBackupDRRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseSetIamPolicy._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "SetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseBackupDRRestTransport._BaseTestIamPermissions, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseBackupDRRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseBackupDRRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupDRRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupDRRestTransport._BaseTestIamPermissions._get_query_params_json(
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "TestIamPermissions",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseBackupDRRestTransport._BaseCancelOperation, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.CancelOperation")

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

            http_options = (
                _BaseBackupDRRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseBackupDRRestTransport._BaseCancelOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._CancelOperation._get_response(
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
        _BaseBackupDRRestTransport._BaseDeleteOperation, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.DeleteOperation")

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

            http_options = (
                _BaseBackupDRRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseDeleteOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._DeleteOperation._get_response(
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

    class _GetOperation(_BaseBackupDRRestTransport._BaseGetOperation, BackupDRRestStub):
        def __hash__(self):
            return hash("BackupDRRestTransport.GetOperation")

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
                _BaseBackupDRRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
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
        _BaseBackupDRRestTransport._BaseListOperations, BackupDRRestStub
    ):
        def __hash__(self):
            return hash("BackupDRRestTransport.ListOperations")

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
                _BaseBackupDRRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseBackupDRRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupDRRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.backupdr_v1.BackupDRClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = BackupDRRestTransport._ListOperations._get_response(
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
                    "Received response for google.cloud.backupdr_v1.BackupDRAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.backupdr.v1.BackupDR",
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


__all__ = ("BackupDRRestTransport",)
