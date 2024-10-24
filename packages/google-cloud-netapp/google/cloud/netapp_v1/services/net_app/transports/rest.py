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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.netapp_v1.types import active_directory as gcn_active_directory
from google.cloud.netapp_v1.types import active_directory
from google.cloud.netapp_v1.types import backup
from google.cloud.netapp_v1.types import backup as gcn_backup
from google.cloud.netapp_v1.types import backup_policy
from google.cloud.netapp_v1.types import backup_policy as gcn_backup_policy
from google.cloud.netapp_v1.types import backup_vault
from google.cloud.netapp_v1.types import backup_vault as gcn_backup_vault
from google.cloud.netapp_v1.types import kms
from google.cloud.netapp_v1.types import replication
from google.cloud.netapp_v1.types import replication as gcn_replication
from google.cloud.netapp_v1.types import snapshot
from google.cloud.netapp_v1.types import snapshot as gcn_snapshot
from google.cloud.netapp_v1.types import storage_pool
from google.cloud.netapp_v1.types import storage_pool as gcn_storage_pool
from google.cloud.netapp_v1.types import volume
from google.cloud.netapp_v1.types import volume as gcn_volume

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseNetAppRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class NetAppRestInterceptor:
    """Interceptor for NetApp.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the NetAppRestTransport.

    .. code-block:: python
        class MyCustomNetAppInterceptor(NetAppRestInterceptor):
            def pre_create_active_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_active_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_kms_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_kms_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_storage_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_storage_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_active_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_active_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_kms_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_kms_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_storage_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_storage_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_encrypt_volumes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_encrypt_volumes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_active_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_active_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_kms_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_kms_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_storage_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_storage_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_active_directories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_active_directories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_policies(self, response):
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

            def pre_list_kms_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_kms_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_replications(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_replications(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_snapshots(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_snapshots(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_storage_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_storage_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_volumes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volumes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resume_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resume_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reverse_replication_direction(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reverse_replication_direction(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_revert_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_revert_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_switch_active_replica_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_switch_active_replica_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_active_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_active_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup_vault(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup_vault(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_kms_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_kms_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_storage_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_storage_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_verify_kms_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_verify_kms_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = NetAppRestTransport(interceptor=MyCustomNetAppInterceptor())
        client = NetAppClient(transport=transport)


    """

    def pre_create_active_directory(
        self,
        request: gcn_active_directory.CreateActiveDirectoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_active_directory.CreateActiveDirectoryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_active_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_active_directory(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_active_directory

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup(
        self,
        request: gcn_backup.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_policy(
        self,
        request: gcn_backup_policy.CreateBackupPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup_policy.CreateBackupPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_backup_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_vault(
        self,
        request: gcn_backup_vault.CreateBackupVaultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup_vault.CreateBackupVaultRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_kms_config(
        self, request: kms.CreateKmsConfigRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.CreateKmsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_kms_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_kms_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_kms_config

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_replication(
        self,
        request: gcn_replication.CreateReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_replication.CreateReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_replication(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_snapshot(
        self,
        request: gcn_snapshot.CreateSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_snapshot.CreateSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_storage_pool(
        self,
        request: gcn_storage_pool.CreateStoragePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_storage_pool.CreateStoragePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_storage_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_storage_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_storage_pool

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_create_volume(
        self,
        request: gcn_volume.CreateVolumeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_volume.CreateVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_create_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_volume

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_active_directory(
        self,
        request: active_directory.DeleteActiveDirectoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        active_directory.DeleteActiveDirectoryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_active_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_active_directory(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_active_directory

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self, request: backup.DeleteBackupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[backup.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_policy(
        self,
        request: backup_policy.DeleteBackupPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_policy.DeleteBackupPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_backup_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_vault(
        self,
        request: backup_vault.DeleteBackupVaultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_vault.DeleteBackupVaultRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_kms_config(
        self, request: kms.DeleteKmsConfigRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.DeleteKmsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_kms_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_kms_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_kms_config

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_replication(
        self,
        request: replication.DeleteReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[replication.DeleteReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_replication(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_snapshot(
        self,
        request: snapshot.DeleteSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[snapshot.DeleteSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_storage_pool(
        self,
        request: storage_pool.DeleteStoragePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storage_pool.DeleteStoragePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_storage_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_storage_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_storage_pool

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_delete_volume(
        self, request: volume.DeleteVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.DeleteVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_volume

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_encrypt_volumes(
        self, request: kms.EncryptVolumesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.EncryptVolumesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for encrypt_volumes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_encrypt_volumes(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for encrypt_volumes

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_active_directory(
        self,
        request: active_directory.GetActiveDirectoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[active_directory.GetActiveDirectoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_active_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_active_directory(
        self, response: active_directory.ActiveDirectory
    ) -> active_directory.ActiveDirectory:
        """Post-rpc interceptor for get_active_directory

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self, request: backup.GetBackupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[backup.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_backup(self, response: backup.Backup) -> backup.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_policy(
        self,
        request: backup_policy.GetBackupPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_policy.GetBackupPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_backup_policy(
        self, response: backup_policy.BackupPolicy
    ) -> backup_policy.BackupPolicy:
        """Post-rpc interceptor for get_backup_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_vault(
        self,
        request: backup_vault.GetBackupVaultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_vault.GetBackupVaultRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_backup_vault(
        self, response: backup_vault.BackupVault
    ) -> backup_vault.BackupVault:
        """Post-rpc interceptor for get_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_kms_config(
        self, request: kms.GetKmsConfigRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.GetKmsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_kms_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_kms_config(self, response: kms.KmsConfig) -> kms.KmsConfig:
        """Post-rpc interceptor for get_kms_config

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_replication(
        self,
        request: replication.GetReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[replication.GetReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_replication(
        self, response: replication.Replication
    ) -> replication.Replication:
        """Post-rpc interceptor for get_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_snapshot(
        self, request: snapshot.GetSnapshotRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[snapshot.GetSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_snapshot(self, response: snapshot.Snapshot) -> snapshot.Snapshot:
        """Post-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_storage_pool(
        self,
        request: storage_pool.GetStoragePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storage_pool.GetStoragePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_storage_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_storage_pool(
        self, response: storage_pool.StoragePool
    ) -> storage_pool.StoragePool:
        """Post-rpc interceptor for get_storage_pool

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume(
        self, request: volume.GetVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.GetVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_volume(self, response: volume.Volume) -> volume.Volume:
        """Post-rpc interceptor for get_volume

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_active_directories(
        self,
        request: active_directory.ListActiveDirectoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        active_directory.ListActiveDirectoriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_active_directories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_active_directories(
        self, response: active_directory.ListActiveDirectoriesResponse
    ) -> active_directory.ListActiveDirectoriesResponse:
        """Post-rpc interceptor for list_active_directories

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_policies(
        self,
        request: backup_policy.ListBackupPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_policy.ListBackupPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backup_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_backup_policies(
        self, response: backup_policy.ListBackupPoliciesResponse
    ) -> backup_policy.ListBackupPoliciesResponse:
        """Post-rpc interceptor for list_backup_policies

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self, request: backup.ListBackupsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[backup.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_backups(
        self, response: backup.ListBackupsResponse
    ) -> backup.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_vaults(
        self,
        request: backup_vault.ListBackupVaultsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[backup_vault.ListBackupVaultsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backup_vaults

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_backup_vaults(
        self, response: backup_vault.ListBackupVaultsResponse
    ) -> backup_vault.ListBackupVaultsResponse:
        """Post-rpc interceptor for list_backup_vaults

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_kms_configs(
        self, request: kms.ListKmsConfigsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.ListKmsConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_kms_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_kms_configs(
        self, response: kms.ListKmsConfigsResponse
    ) -> kms.ListKmsConfigsResponse:
        """Post-rpc interceptor for list_kms_configs

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_replications(
        self,
        request: replication.ListReplicationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[replication.ListReplicationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_replications

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_replications(
        self, response: replication.ListReplicationsResponse
    ) -> replication.ListReplicationsResponse:
        """Post-rpc interceptor for list_replications

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_snapshots(
        self,
        request: snapshot.ListSnapshotsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[snapshot.ListSnapshotsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_snapshots(
        self, response: snapshot.ListSnapshotsResponse
    ) -> snapshot.ListSnapshotsResponse:
        """Post-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_storage_pools(
        self,
        request: storage_pool.ListStoragePoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storage_pool.ListStoragePoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_storage_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_storage_pools(
        self, response: storage_pool.ListStoragePoolsResponse
    ) -> storage_pool.ListStoragePoolsResponse:
        """Post-rpc interceptor for list_storage_pools

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_list_volumes(
        self, request: volume.ListVolumesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.ListVolumesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volumes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_volumes(
        self, response: volume.ListVolumesResponse
    ) -> volume.ListVolumesResponse:
        """Post-rpc interceptor for list_volumes

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_resume_replication(
        self,
        request: replication.ResumeReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[replication.ResumeReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resume_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_resume_replication(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for resume_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_reverse_replication_direction(
        self,
        request: replication.ReverseReplicationDirectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        replication.ReverseReplicationDirectionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for reverse_replication_direction

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_reverse_replication_direction(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reverse_replication_direction

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_revert_volume(
        self, request: volume.RevertVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.RevertVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for revert_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_revert_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for revert_volume

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_stop_replication(
        self,
        request: replication.StopReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[replication.StopReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_stop_replication(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_switch_active_replica_zone(
        self,
        request: storage_pool.SwitchActiveReplicaZoneRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[storage_pool.SwitchActiveReplicaZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for switch_active_replica_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_switch_active_replica_zone(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for switch_active_replica_zone

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_active_directory(
        self,
        request: gcn_active_directory.UpdateActiveDirectoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_active_directory.UpdateActiveDirectoryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_active_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_active_directory(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_active_directory

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: gcn_backup.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup.UpdateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup_policy(
        self,
        request: gcn_backup_policy.UpdateBackupPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup_policy.UpdateBackupPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_backup_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup_vault(
        self,
        request: gcn_backup_vault.UpdateBackupVaultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_backup_vault.UpdateBackupVaultRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup_vault

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_backup_vault(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup_vault

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_kms_config(
        self, request: kms.UpdateKmsConfigRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.UpdateKmsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_kms_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_kms_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_kms_config

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_replication(
        self,
        request: gcn_replication.UpdateReplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_replication.UpdateReplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_replication(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_replication

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_snapshot(
        self,
        request: gcn_snapshot.UpdateSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_snapshot.UpdateSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_storage_pool(
        self,
        request: gcn_storage_pool.UpdateStoragePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_storage_pool.UpdateStoragePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_storage_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_storage_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_storage_pool

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_update_volume(
        self,
        request: gcn_volume.UpdateVolumeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_volume.UpdateVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_update_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_volume

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response

    def pre_verify_kms_config(
        self, request: kms.VerifyKmsConfigRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[kms.VerifyKmsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for verify_kms_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_verify_kms_config(
        self, response: kms.VerifyKmsConfigResponse
    ) -> kms.VerifyKmsConfigResponse:
        """Post-rpc interceptor for verify_kms_config

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
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
        before they are sent to the NetApp server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the NetApp server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class NetAppRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: NetAppRestInterceptor


class NetAppRestTransport(_BaseNetAppRestTransport):
    """REST backend synchronous transport for NetApp.

    NetApp Files Google Cloud Service

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "netapp.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[NetAppRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'netapp.googleapis.com').
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
        self._interceptor = interceptor or NetAppRestInterceptor()
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

    class _CreateActiveDirectory(
        _BaseNetAppRestTransport._BaseCreateActiveDirectory, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateActiveDirectory")

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
            request: gcn_active_directory.CreateActiveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create active directory method over HTTP.

            Args:
                request (~.gcn_active_directory.CreateActiveDirectoryRequest):
                    The request object. CreateActiveDirectoryRequest for
                creating an active directory.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateActiveDirectory._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_active_directory(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseCreateActiveDirectory._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetAppRestTransport._BaseCreateActiveDirectory._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseCreateActiveDirectory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._CreateActiveDirectory._get_response(
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
            resp = self._interceptor.post_create_active_directory(resp)
            return resp

    class _CreateBackup(_BaseNetAppRestTransport._BaseCreateBackup, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateBackup")

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
            request: gcn_backup.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.gcn_backup.CreateBackupRequest):
                    The request object. CreateBackupRequest creates a backup.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateBackup._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseCreateBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateBackup._get_response(
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
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateBackupPolicy(
        _BaseNetAppRestTransport._BaseCreateBackupPolicy, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateBackupPolicy")

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
            request: gcn_backup_policy.CreateBackupPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup policy method over HTTP.

            Args:
                request (~.gcn_backup_policy.CreateBackupPolicyRequest):
                    The request object. CreateBackupPolicyRequest creates a
                backupPolicy.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateBackupPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup_policy(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseCreateBackupPolicy._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseNetAppRestTransport._BaseCreateBackupPolicy._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateBackupPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateBackupPolicy._get_response(
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
            resp = self._interceptor.post_create_backup_policy(resp)
            return resp

    class _CreateBackupVault(
        _BaseNetAppRestTransport._BaseCreateBackupVault, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateBackupVault")

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
            request: gcn_backup_vault.CreateBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup vault method over HTTP.

            Args:
                request (~.gcn_backup_vault.CreateBackupVaultRequest):
                    The request object. CreateBackupVaultRequest creates a
                backup vault.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateBackupVault._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup_vault(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateBackupVault._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseCreateBackupVault._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateBackupVault._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateBackupVault._get_response(
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
            return resp

    class _CreateKmsConfig(
        _BaseNetAppRestTransport._BaseCreateKmsConfig, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateKmsConfig")

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
            request: kms.CreateKmsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create kms config method over HTTP.

            Args:
                request (~.kms.CreateKmsConfigRequest):
                    The request object. CreateKmsConfigRequest creates a KMS
                Config.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateKmsConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_kms_config(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateKmsConfig._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseCreateKmsConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateKmsConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateKmsConfig._get_response(
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
            resp = self._interceptor.post_create_kms_config(resp)
            return resp

    class _CreateReplication(
        _BaseNetAppRestTransport._BaseCreateReplication, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateReplication")

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
            request: gcn_replication.CreateReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create replication method over HTTP.

            Args:
                request (~.gcn_replication.CreateReplicationRequest):
                    The request object. CreateReplicationRequest creates a
                replication.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_replication(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateReplication._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseCreateReplication._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateReplication._get_response(
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
            resp = self._interceptor.post_create_replication(resp)
            return resp

    class _CreateSnapshot(_BaseNetAppRestTransport._BaseCreateSnapshot, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateSnapshot")

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
            request: gcn_snapshot.CreateSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create snapshot method over HTTP.

            Args:
                request (~.gcn_snapshot.CreateSnapshotRequest):
                    The request object. CreateSnapshotRequest creates a
                snapshot.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_snapshot(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateSnapshot._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseCreateSnapshot._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateSnapshot._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateSnapshot._get_response(
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
            resp = self._interceptor.post_create_snapshot(resp)
            return resp

    class _CreateStoragePool(
        _BaseNetAppRestTransport._BaseCreateStoragePool, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateStoragePool")

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
            request: gcn_storage_pool.CreateStoragePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create storage pool method over HTTP.

            Args:
                request (~.gcn_storage_pool.CreateStoragePoolRequest):
                    The request object. CreateStoragePoolRequest creates a
                Storage Pool.
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateStoragePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_storage_pool(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateStoragePool._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseCreateStoragePool._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateStoragePool._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateStoragePool._get_response(
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
            resp = self._interceptor.post_create_storage_pool(resp)
            return resp

    class _CreateVolume(_BaseNetAppRestTransport._BaseCreateVolume, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.CreateVolume")

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
            request: gcn_volume.CreateVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create volume method over HTTP.

            Args:
                request (~.gcn_volume.CreateVolumeRequest):
                    The request object. Message for creating a Volume
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

            http_options = (
                _BaseNetAppRestTransport._BaseCreateVolume._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_volume(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCreateVolume._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseCreateVolume._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCreateVolume._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CreateVolume._get_response(
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
            resp = self._interceptor.post_create_volume(resp)
            return resp

    class _DeleteActiveDirectory(
        _BaseNetAppRestTransport._BaseDeleteActiveDirectory, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteActiveDirectory")

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
            request: active_directory.DeleteActiveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete active directory method over HTTP.

            Args:
                request (~.active_directory.DeleteActiveDirectoryRequest):
                    The request object. DeleteActiveDirectoryRequest for
                deleting a single active directory.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteActiveDirectory._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_active_directory(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseDeleteActiveDirectory._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseDeleteActiveDirectory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._DeleteActiveDirectory._get_response(
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
            resp = self._interceptor.post_delete_active_directory(resp)
            return resp

    class _DeleteBackup(_BaseNetAppRestTransport._BaseDeleteBackup, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteBackup")

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
            request: backup.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.backup.DeleteBackupRequest):
                    The request object. DeleteBackupRequest deletes a backup.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteBackup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteBackup._get_response(
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
            return resp

    class _DeleteBackupPolicy(
        _BaseNetAppRestTransport._BaseDeleteBackupPolicy, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteBackupPolicy")

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
            request: backup_policy.DeleteBackupPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup policy method over HTTP.

            Args:
                request (~.backup_policy.DeleteBackupPolicyRequest):
                    The request object. DeleteBackupPolicyRequest deletes a
                backup policy.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteBackupPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup_policy(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseDeleteBackupPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteBackupPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteBackupPolicy._get_response(
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
            resp = self._interceptor.post_delete_backup_policy(resp)
            return resp

    class _DeleteBackupVault(
        _BaseNetAppRestTransport._BaseDeleteBackupVault, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteBackupVault")

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
            request: backup_vault.DeleteBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup vault method over HTTP.

            Args:
                request (~.backup_vault.DeleteBackupVaultRequest):
                    The request object. DeleteBackupVaultRequest deletes a
                backupVault.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteBackupVault._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup_vault(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteBackupVault._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteBackupVault._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteBackupVault._get_response(
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
            return resp

    class _DeleteKmsConfig(
        _BaseNetAppRestTransport._BaseDeleteKmsConfig, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteKmsConfig")

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
            request: kms.DeleteKmsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete kms config method over HTTP.

            Args:
                request (~.kms.DeleteKmsConfigRequest):
                    The request object. DeleteKmsConfigRequest deletes a KMS
                Config.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteKmsConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_kms_config(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteKmsConfig._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteKmsConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteKmsConfig._get_response(
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
            resp = self._interceptor.post_delete_kms_config(resp)
            return resp

    class _DeleteReplication(
        _BaseNetAppRestTransport._BaseDeleteReplication, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteReplication")

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
            request: replication.DeleteReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete replication method over HTTP.

            Args:
                request (~.replication.DeleteReplicationRequest):
                    The request object. DeleteReplicationRequest deletes a
                replication.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_replication(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteReplication._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteReplication._get_response(
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
            resp = self._interceptor.post_delete_replication(resp)
            return resp

    class _DeleteSnapshot(_BaseNetAppRestTransport._BaseDeleteSnapshot, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteSnapshot")

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
            request: snapshot.DeleteSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete snapshot method over HTTP.

            Args:
                request (~.snapshot.DeleteSnapshotRequest):
                    The request object. DeleteSnapshotRequest deletes a
                snapshot.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_snapshot(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteSnapshot._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteSnapshot._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteSnapshot._get_response(
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
            resp = self._interceptor.post_delete_snapshot(resp)
            return resp

    class _DeleteStoragePool(
        _BaseNetAppRestTransport._BaseDeleteStoragePool, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteStoragePool")

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
            request: storage_pool.DeleteStoragePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete storage pool method over HTTP.

            Args:
                request (~.storage_pool.DeleteStoragePoolRequest):
                    The request object. DeleteStoragePoolRequest deletes a
                Storage Pool.
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteStoragePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_storage_pool(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteStoragePool._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteStoragePool._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteStoragePool._get_response(
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
            resp = self._interceptor.post_delete_storage_pool(resp)
            return resp

    class _DeleteVolume(_BaseNetAppRestTransport._BaseDeleteVolume, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteVolume")

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
            request: volume.DeleteVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete volume method over HTTP.

            Args:
                request (~.volume.DeleteVolumeRequest):
                    The request object. Message for deleting a Volume
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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteVolume._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_volume(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteVolume._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteVolume._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteVolume._get_response(
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
            resp = self._interceptor.post_delete_volume(resp)
            return resp

    class _EncryptVolumes(_BaseNetAppRestTransport._BaseEncryptVolumes, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.EncryptVolumes")

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
            request: kms.EncryptVolumesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the encrypt volumes method over HTTP.

            Args:
                request (~.kms.EncryptVolumesRequest):
                    The request object. EncryptVolumesRequest specifies the
                KMS config to encrypt existing volumes.
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

            http_options = (
                _BaseNetAppRestTransport._BaseEncryptVolumes._get_http_options()
            )
            request, metadata = self._interceptor.pre_encrypt_volumes(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseEncryptVolumes._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseEncryptVolumes._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseEncryptVolumes._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._EncryptVolumes._get_response(
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
            resp = self._interceptor.post_encrypt_volumes(resp)
            return resp

    class _GetActiveDirectory(
        _BaseNetAppRestTransport._BaseGetActiveDirectory, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.GetActiveDirectory")

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
            request: active_directory.GetActiveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> active_directory.ActiveDirectory:
            r"""Call the get active directory method over HTTP.

            Args:
                request (~.active_directory.GetActiveDirectoryRequest):
                    The request object. GetActiveDirectory for getting a
                single active directory.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.active_directory.ActiveDirectory:
                    ActiveDirectory is the public
                representation of the active directory
                config.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetActiveDirectory._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_active_directory(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseGetActiveDirectory._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetActiveDirectory._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetActiveDirectory._get_response(
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
            resp = active_directory.ActiveDirectory()
            pb_resp = active_directory.ActiveDirectory.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_active_directory(resp)
            return resp

    class _GetBackup(_BaseNetAppRestTransport._BaseGetBackup, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetBackup")

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
            request: backup.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.backup.GetBackupRequest):
                    The request object. GetBackupRequest gets the state of a
                backup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup.Backup:
                    A NetApp Backup.
            """

            http_options = _BaseNetAppRestTransport._BaseGetBackup._get_http_options()
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetBackup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetBackup._get_response(
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
            resp = backup.Backup()
            pb_resp = backup.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetBackupPolicy(
        _BaseNetAppRestTransport._BaseGetBackupPolicy, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.GetBackupPolicy")

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
            request: backup_policy.GetBackupPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_policy.BackupPolicy:
            r"""Call the get backup policy method over HTTP.

            Args:
                request (~.backup_policy.GetBackupPolicyRequest):
                    The request object. GetBackupPolicyRequest gets the state
                of a backupPolicy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_policy.BackupPolicy:
                    Backup Policy.
            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetBackupPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup_policy(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetBackupPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetBackupPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetBackupPolicy._get_response(
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
            resp = backup_policy.BackupPolicy()
            pb_resp = backup_policy.BackupPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup_policy(resp)
            return resp

    class _GetBackupVault(_BaseNetAppRestTransport._BaseGetBackupVault, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetBackupVault")

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
            request: backup_vault.GetBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_vault.BackupVault:
            r"""Call the get backup vault method over HTTP.

            Args:
                request (~.backup_vault.GetBackupVaultRequest):
                    The request object. GetBackupVaultRequest gets the state
                of a backupVault.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_vault.BackupVault:
                    A NetApp BackupVault.
            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetBackupVault._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup_vault(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetBackupVault._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetBackupVault._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetBackupVault._get_response(
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
            resp = backup_vault.BackupVault()
            pb_resp = backup_vault.BackupVault.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup_vault(resp)
            return resp

    class _GetKmsConfig(_BaseNetAppRestTransport._BaseGetKmsConfig, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetKmsConfig")

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
            request: kms.GetKmsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> kms.KmsConfig:
            r"""Call the get kms config method over HTTP.

            Args:
                request (~.kms.GetKmsConfigRequest):
                    The request object. GetKmsConfigRequest gets a KMS
                Config.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.kms.KmsConfig:
                    KmsConfig is the customer managed
                encryption key(CMEK) configuration.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetKmsConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_kms_config(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetKmsConfig._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetKmsConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetKmsConfig._get_response(
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
            resp = kms.KmsConfig()
            pb_resp = kms.KmsConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_kms_config(resp)
            return resp

    class _GetReplication(_BaseNetAppRestTransport._BaseGetReplication, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetReplication")

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
            request: replication.GetReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> replication.Replication:
            r"""Call the get replication method over HTTP.

            Args:
                request (~.replication.GetReplicationRequest):
                    The request object. GetReplicationRequest gets the state
                of a replication.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.replication.Replication:
                    Replication is a nested resource
                under Volume, that describes a
                cross-region replication relationship
                between 2 volumes in different regions.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_replication(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetReplication._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetReplication._get_response(
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
            resp = replication.Replication()
            pb_resp = replication.Replication.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_replication(resp)
            return resp

    class _GetSnapshot(_BaseNetAppRestTransport._BaseGetSnapshot, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetSnapshot")

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
            request: snapshot.GetSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshot.Snapshot:
            r"""Call the get snapshot method over HTTP.

            Args:
                request (~.snapshot.GetSnapshotRequest):
                    The request object. GetSnapshotRequest gets the state of
                a snapshot.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshot.Snapshot:
                    Snapshot is a point-in-time version
                of a Volume's content.

            """

            http_options = _BaseNetAppRestTransport._BaseGetSnapshot._get_http_options()
            request, metadata = self._interceptor.pre_get_snapshot(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetSnapshot._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetSnapshot._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetSnapshot._get_response(
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
            resp = snapshot.Snapshot()
            pb_resp = snapshot.Snapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_snapshot(resp)
            return resp

    class _GetStoragePool(_BaseNetAppRestTransport._BaseGetStoragePool, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetStoragePool")

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
            request: storage_pool.GetStoragePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storage_pool.StoragePool:
            r"""Call the get storage pool method over HTTP.

            Args:
                request (~.storage_pool.GetStoragePoolRequest):
                    The request object. GetStoragePoolRequest gets a Storage
                Pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storage_pool.StoragePool:
                    StoragePool is a container for
                volumes with a service level and
                capacity. Volumes can be created in a
                pool of sufficient available capacity.
                StoragePool capacity is what you are
                billed for.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseGetStoragePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_storage_pool(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetStoragePool._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetStoragePool._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetStoragePool._get_response(
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
            resp = storage_pool.StoragePool()
            pb_resp = storage_pool.StoragePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_storage_pool(resp)
            return resp

    class _GetVolume(_BaseNetAppRestTransport._BaseGetVolume, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetVolume")

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
            request: volume.GetVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.Volume:
            r"""Call the get volume method over HTTP.

            Args:
                request (~.volume.GetVolumeRequest):
                    The request object. Message for getting a Volume
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.Volume:
                    Volume provides a filesystem that you
                can mount.

            """

            http_options = _BaseNetAppRestTransport._BaseGetVolume._get_http_options()
            request, metadata = self._interceptor.pre_get_volume(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetVolume._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetVolume._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetVolume._get_response(
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
            resp = volume.Volume()
            pb_resp = volume.Volume.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume(resp)
            return resp

    class _ListActiveDirectories(
        _BaseNetAppRestTransport._BaseListActiveDirectories, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ListActiveDirectories")

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
            request: active_directory.ListActiveDirectoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> active_directory.ListActiveDirectoriesResponse:
            r"""Call the list active directories method over HTTP.

            Args:
                request (~.active_directory.ListActiveDirectoriesRequest):
                    The request object. ListActiveDirectoriesRequest for
                requesting multiple active directories.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.active_directory.ListActiveDirectoriesResponse:
                    ListActiveDirectoriesResponse
                contains all the active directories
                requested.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListActiveDirectories._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_active_directories(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseListActiveDirectories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseListActiveDirectories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._ListActiveDirectories._get_response(
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
            resp = active_directory.ListActiveDirectoriesResponse()
            pb_resp = active_directory.ListActiveDirectoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_active_directories(resp)
            return resp

    class _ListBackupPolicies(
        _BaseNetAppRestTransport._BaseListBackupPolicies, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ListBackupPolicies")

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
            request: backup_policy.ListBackupPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_policy.ListBackupPoliciesResponse:
            r"""Call the list backup policies method over HTTP.

            Args:
                request (~.backup_policy.ListBackupPoliciesRequest):
                    The request object. ListBackupPoliciesRequest for
                requesting multiple backup policies.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_policy.ListBackupPoliciesResponse:
                    ListBackupPoliciesResponse contains
                all the backup policies requested.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListBackupPolicies._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_backup_policies(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseListBackupPolicies._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListBackupPolicies._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListBackupPolicies._get_response(
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
            resp = backup_policy.ListBackupPoliciesResponse()
            pb_resp = backup_policy.ListBackupPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backup_policies(resp)
            return resp

    class _ListBackups(_BaseNetAppRestTransport._BaseListBackups, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListBackups")

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
            request: backup.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.backup.ListBackupsRequest):
                    The request object. ListBackupsRequest lists backups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup.ListBackupsResponse:
                    ListBackupsResponse is the result of
                ListBackupsRequest.

            """

            http_options = _BaseNetAppRestTransport._BaseListBackups._get_http_options()
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListBackups._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListBackups._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListBackups._get_response(
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
            resp = backup.ListBackupsResponse()
            pb_resp = backup.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListBackupVaults(
        _BaseNetAppRestTransport._BaseListBackupVaults, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ListBackupVaults")

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
            request: backup_vault.ListBackupVaultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_vault.ListBackupVaultsResponse:
            r"""Call the list backup vaults method over HTTP.

            Args:
                request (~.backup_vault.ListBackupVaultsRequest):
                    The request object. ListBackupVaultsRequest lists
                backupVaults.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_vault.ListBackupVaultsResponse:
                    ListBackupVaultsResponse is the
                result of ListBackupVaultsRequest.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListBackupVaults._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_backup_vaults(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListBackupVaults._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListBackupVaults._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListBackupVaults._get_response(
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
            resp = backup_vault.ListBackupVaultsResponse()
            pb_resp = backup_vault.ListBackupVaultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backup_vaults(resp)
            return resp

    class _ListKmsConfigs(_BaseNetAppRestTransport._BaseListKmsConfigs, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListKmsConfigs")

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
            request: kms.ListKmsConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> kms.ListKmsConfigsResponse:
            r"""Call the list kms configs method over HTTP.

            Args:
                request (~.kms.ListKmsConfigsRequest):
                    The request object. ListKmsConfigsRequest lists KMS
                Configs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.kms.ListKmsConfigsResponse:
                    ListKmsConfigsResponse is the
                response to a ListKmsConfigsRequest.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListKmsConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_kms_configs(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListKmsConfigs._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListKmsConfigs._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListKmsConfigs._get_response(
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
            resp = kms.ListKmsConfigsResponse()
            pb_resp = kms.ListKmsConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_kms_configs(resp)
            return resp

    class _ListReplications(
        _BaseNetAppRestTransport._BaseListReplications, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ListReplications")

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
            request: replication.ListReplicationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> replication.ListReplicationsResponse:
            r"""Call the list replications method over HTTP.

            Args:
                request (~.replication.ListReplicationsRequest):
                    The request object. ListReplications lists replications.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.replication.ListReplicationsResponse:
                    ListReplicationsResponse is the
                result of ListReplicationsRequest.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListReplications._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_replications(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListReplications._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListReplications._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListReplications._get_response(
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
            resp = replication.ListReplicationsResponse()
            pb_resp = replication.ListReplicationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_replications(resp)
            return resp

    class _ListSnapshots(_BaseNetAppRestTransport._BaseListSnapshots, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListSnapshots")

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
            request: snapshot.ListSnapshotsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshot.ListSnapshotsResponse:
            r"""Call the list snapshots method over HTTP.

            Args:
                request (~.snapshot.ListSnapshotsRequest):
                    The request object. ListSnapshotsRequest lists snapshots.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshot.ListSnapshotsResponse:
                    ListSnapshotsResponse is the result
                of ListSnapshotsRequest.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListSnapshots._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_snapshots(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListSnapshots._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListSnapshots._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListSnapshots._get_response(
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
            resp = snapshot.ListSnapshotsResponse()
            pb_resp = snapshot.ListSnapshotsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_snapshots(resp)
            return resp

    class _ListStoragePools(
        _BaseNetAppRestTransport._BaseListStoragePools, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ListStoragePools")

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
            request: storage_pool.ListStoragePoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> storage_pool.ListStoragePoolsResponse:
            r"""Call the list storage pools method over HTTP.

            Args:
                request (~.storage_pool.ListStoragePoolsRequest):
                    The request object. ListStoragePoolsRequest lists Storage
                Pools.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.storage_pool.ListStoragePoolsResponse:
                    ListStoragePoolsResponse is the
                response to a ListStoragePoolsRequest.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseListStoragePools._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_storage_pools(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListStoragePools._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListStoragePools._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListStoragePools._get_response(
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
            resp = storage_pool.ListStoragePoolsResponse()
            pb_resp = storage_pool.ListStoragePoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_storage_pools(resp)
            return resp

    class _ListVolumes(_BaseNetAppRestTransport._BaseListVolumes, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListVolumes")

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
            request: volume.ListVolumesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.ListVolumesResponse:
            r"""Call the list volumes method over HTTP.

            Args:
                request (~.volume.ListVolumesRequest):
                    The request object. Message for requesting list of
                Volumes
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.ListVolumesResponse:
                    Message for response to listing
                Volumes

            """

            http_options = _BaseNetAppRestTransport._BaseListVolumes._get_http_options()
            request, metadata = self._interceptor.pre_list_volumes(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListVolumes._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListVolumes._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListVolumes._get_response(
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
            resp = volume.ListVolumesResponse()
            pb_resp = volume.ListVolumesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volumes(resp)
            return resp

    class _ResumeReplication(
        _BaseNetAppRestTransport._BaseResumeReplication, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ResumeReplication")

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
            request: replication.ResumeReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the resume replication method over HTTP.

            Args:
                request (~.replication.ResumeReplicationRequest):
                    The request object. ResumeReplicationRequest resumes a
                stopped replication.
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

            http_options = (
                _BaseNetAppRestTransport._BaseResumeReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_resume_replication(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseResumeReplication._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseResumeReplication._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseResumeReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ResumeReplication._get_response(
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
            resp = self._interceptor.post_resume_replication(resp)
            return resp

    class _ReverseReplicationDirection(
        _BaseNetAppRestTransport._BaseReverseReplicationDirection, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.ReverseReplicationDirection")

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
            request: replication.ReverseReplicationDirectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reverse replication
            direction method over HTTP.

                Args:
                    request (~.replication.ReverseReplicationDirectionRequest):
                        The request object. ReverseReplicationDirectionRequest
                    reverses direction of replication.
                    Source becomes destination and
                    destination becomes source.
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

            http_options = (
                _BaseNetAppRestTransport._BaseReverseReplicationDirection._get_http_options()
            )
            request, metadata = self._interceptor.pre_reverse_replication_direction(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseReverseReplicationDirection._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetAppRestTransport._BaseReverseReplicationDirection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseReverseReplicationDirection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._ReverseReplicationDirection._get_response(
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
            resp = self._interceptor.post_reverse_replication_direction(resp)
            return resp

    class _RevertVolume(_BaseNetAppRestTransport._BaseRevertVolume, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.RevertVolume")

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
            request: volume.RevertVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the revert volume method over HTTP.

            Args:
                request (~.volume.RevertVolumeRequest):
                    The request object. RevertVolumeRequest reverts the given
                volume to the specified snapshot.
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

            http_options = (
                _BaseNetAppRestTransport._BaseRevertVolume._get_http_options()
            )
            request, metadata = self._interceptor.pre_revert_volume(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseRevertVolume._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseRevertVolume._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseRevertVolume._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._RevertVolume._get_response(
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
            resp = self._interceptor.post_revert_volume(resp)
            return resp

    class _StopReplication(
        _BaseNetAppRestTransport._BaseStopReplication, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.StopReplication")

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
            request: replication.StopReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop replication method over HTTP.

            Args:
                request (~.replication.StopReplicationRequest):
                    The request object. StopReplicationRequest stops a
                replication until resumed.
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

            http_options = (
                _BaseNetAppRestTransport._BaseStopReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_stop_replication(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseStopReplication._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseStopReplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseStopReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._StopReplication._get_response(
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
            resp = self._interceptor.post_stop_replication(resp)
            return resp

    class _SwitchActiveReplicaZone(
        _BaseNetAppRestTransport._BaseSwitchActiveReplicaZone, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.SwitchActiveReplicaZone")

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
            request: storage_pool.SwitchActiveReplicaZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the switch active replica
            zone method over HTTP.

                Args:
                    request (~.storage_pool.SwitchActiveReplicaZoneRequest):
                        The request object. SwitchActiveReplicaZoneRequest switch
                    the active/replica zone for a regional
                    storagePool.
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

            http_options = (
                _BaseNetAppRestTransport._BaseSwitchActiveReplicaZone._get_http_options()
            )
            request, metadata = self._interceptor.pre_switch_active_replica_zone(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseSwitchActiveReplicaZone._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetAppRestTransport._BaseSwitchActiveReplicaZone._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseSwitchActiveReplicaZone._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._SwitchActiveReplicaZone._get_response(
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
            resp = self._interceptor.post_switch_active_replica_zone(resp)
            return resp

    class _UpdateActiveDirectory(
        _BaseNetAppRestTransport._BaseUpdateActiveDirectory, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateActiveDirectory")

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
            request: gcn_active_directory.UpdateActiveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update active directory method over HTTP.

            Args:
                request (~.gcn_active_directory.UpdateActiveDirectoryRequest):
                    The request object. UpdateActiveDirectoryRequest for
                updating an active directory.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateActiveDirectory._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_active_directory(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseUpdateActiveDirectory._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetAppRestTransport._BaseUpdateActiveDirectory._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetAppRestTransport._BaseUpdateActiveDirectory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = NetAppRestTransport._UpdateActiveDirectory._get_response(
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
            resp = self._interceptor.post_update_active_directory(resp)
            return resp

    class _UpdateBackup(_BaseNetAppRestTransport._BaseUpdateBackup, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateBackup")

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
            request: gcn_backup.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.gcn_backup.UpdateBackupRequest):
                    The request object. UpdateBackupRequest updates
                description and/or labels for a backup.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateBackup._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseUpdateBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateBackup._get_response(
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
            return resp

    class _UpdateBackupPolicy(
        _BaseNetAppRestTransport._BaseUpdateBackupPolicy, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateBackupPolicy")

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
            request: gcn_backup_policy.UpdateBackupPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup policy method over HTTP.

            Args:
                request (~.gcn_backup_policy.UpdateBackupPolicyRequest):
                    The request object. UpdateBackupPolicyRequest for
                updating a backup policy.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateBackupPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_backup_policy(
                request, metadata
            )
            transcoded_request = _BaseNetAppRestTransport._BaseUpdateBackupPolicy._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseNetAppRestTransport._BaseUpdateBackupPolicy._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateBackupPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateBackupPolicy._get_response(
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
            resp = self._interceptor.post_update_backup_policy(resp)
            return resp

    class _UpdateBackupVault(
        _BaseNetAppRestTransport._BaseUpdateBackupVault, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateBackupVault")

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
            request: gcn_backup_vault.UpdateBackupVaultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup vault method over HTTP.

            Args:
                request (~.gcn_backup_vault.UpdateBackupVaultRequest):
                    The request object. UpdateBackupVaultRequest updates
                description and/or labels for a
                backupVault.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateBackupVault._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_backup_vault(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateBackupVault._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseUpdateBackupVault._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateBackupVault._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateBackupVault._get_response(
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
            return resp

    class _UpdateKmsConfig(
        _BaseNetAppRestTransport._BaseUpdateKmsConfig, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateKmsConfig")

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
            request: kms.UpdateKmsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update kms config method over HTTP.

            Args:
                request (~.kms.UpdateKmsConfigRequest):
                    The request object. UpdateKmsConfigRequest updates a KMS
                Config.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateKmsConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_kms_config(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateKmsConfig._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseUpdateKmsConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateKmsConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateKmsConfig._get_response(
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
            resp = self._interceptor.post_update_kms_config(resp)
            return resp

    class _UpdateReplication(
        _BaseNetAppRestTransport._BaseUpdateReplication, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateReplication")

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
            request: gcn_replication.UpdateReplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update replication method over HTTP.

            Args:
                request (~.gcn_replication.UpdateReplicationRequest):
                    The request object. UpdateReplicationRequest updates
                description and/or labels for a
                replication.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateReplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_replication(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateReplication._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseUpdateReplication._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateReplication._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateReplication._get_response(
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
            resp = self._interceptor.post_update_replication(resp)
            return resp

    class _UpdateSnapshot(_BaseNetAppRestTransport._BaseUpdateSnapshot, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateSnapshot")

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
            request: gcn_snapshot.UpdateSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update snapshot method over HTTP.

            Args:
                request (~.gcn_snapshot.UpdateSnapshotRequest):
                    The request object. UpdateSnapshotRequest updates
                description and/or labels for a
                snapshot.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_snapshot(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateSnapshot._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseUpdateSnapshot._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateSnapshot._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateSnapshot._get_response(
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
            resp = self._interceptor.post_update_snapshot(resp)
            return resp

    class _UpdateStoragePool(
        _BaseNetAppRestTransport._BaseUpdateStoragePool, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateStoragePool")

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
            request: gcn_storage_pool.UpdateStoragePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update storage pool method over HTTP.

            Args:
                request (~.gcn_storage_pool.UpdateStoragePoolRequest):
                    The request object. UpdateStoragePoolRequest updates a
                Storage Pool.
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateStoragePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_storage_pool(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateStoragePool._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseNetAppRestTransport._BaseUpdateStoragePool._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateStoragePool._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateStoragePool._get_response(
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
            resp = self._interceptor.post_update_storage_pool(resp)
            return resp

    class _UpdateVolume(_BaseNetAppRestTransport._BaseUpdateVolume, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.UpdateVolume")

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
            request: gcn_volume.UpdateVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update volume method over HTTP.

            Args:
                request (~.gcn_volume.UpdateVolumeRequest):
                    The request object. Message for updating a Volume
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

            http_options = (
                _BaseNetAppRestTransport._BaseUpdateVolume._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_volume(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseUpdateVolume._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseUpdateVolume._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseUpdateVolume._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._UpdateVolume._get_response(
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
            resp = self._interceptor.post_update_volume(resp)
            return resp

    class _VerifyKmsConfig(
        _BaseNetAppRestTransport._BaseVerifyKmsConfig, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.VerifyKmsConfig")

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
            request: kms.VerifyKmsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> kms.VerifyKmsConfigResponse:
            r"""Call the verify kms config method over HTTP.

            Args:
                request (~.kms.VerifyKmsConfigRequest):
                    The request object. VerifyKmsConfigRequest specifies the
                KMS config to be validated.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.kms.VerifyKmsConfigResponse:
                    VerifyKmsConfigResponse contains the
                information if the config is correctly
                and error message.

            """

            http_options = (
                _BaseNetAppRestTransport._BaseVerifyKmsConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_verify_kms_config(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseVerifyKmsConfig._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseVerifyKmsConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseVerifyKmsConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._VerifyKmsConfig._get_response(
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
            resp = kms.VerifyKmsConfigResponse()
            pb_resp = kms.VerifyKmsConfigResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_verify_kms_config(resp)
            return resp

    @property
    def create_active_directory(
        self,
    ) -> Callable[
        [gcn_active_directory.CreateActiveDirectoryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateActiveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup(
        self,
    ) -> Callable[[gcn_backup.CreateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_policy(
        self,
    ) -> Callable[
        [gcn_backup_policy.CreateBackupPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_vault(
        self,
    ) -> Callable[
        [gcn_backup_vault.CreateBackupVaultRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_kms_config(
        self,
    ) -> Callable[[kms.CreateKmsConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateKmsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_replication(
        self,
    ) -> Callable[[gcn_replication.CreateReplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_snapshot(
        self,
    ) -> Callable[[gcn_snapshot.CreateSnapshotRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_storage_pool(
        self,
    ) -> Callable[
        [gcn_storage_pool.CreateStoragePoolRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateStoragePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_volume(
        self,
    ) -> Callable[[gcn_volume.CreateVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_active_directory(
        self,
    ) -> Callable[
        [active_directory.DeleteActiveDirectoryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteActiveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[backup.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_policy(
        self,
    ) -> Callable[[backup_policy.DeleteBackupPolicyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_vault(
        self,
    ) -> Callable[[backup_vault.DeleteBackupVaultRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_kms_config(
        self,
    ) -> Callable[[kms.DeleteKmsConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteKmsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_replication(
        self,
    ) -> Callable[[replication.DeleteReplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_snapshot(
        self,
    ) -> Callable[[snapshot.DeleteSnapshotRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_storage_pool(
        self,
    ) -> Callable[[storage_pool.DeleteStoragePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteStoragePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_volume(
        self,
    ) -> Callable[[volume.DeleteVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def encrypt_volumes(
        self,
    ) -> Callable[[kms.EncryptVolumesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EncryptVolumes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_active_directory(
        self,
    ) -> Callable[
        [active_directory.GetActiveDirectoryRequest], active_directory.ActiveDirectory
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetActiveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(self) -> Callable[[backup.GetBackupRequest], backup.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_policy(
        self,
    ) -> Callable[[backup_policy.GetBackupPolicyRequest], backup_policy.BackupPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_vault(
        self,
    ) -> Callable[[backup_vault.GetBackupVaultRequest], backup_vault.BackupVault]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_kms_config(self) -> Callable[[kms.GetKmsConfigRequest], kms.KmsConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetKmsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_replication(
        self,
    ) -> Callable[[replication.GetReplicationRequest], replication.Replication]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_snapshot(
        self,
    ) -> Callable[[snapshot.GetSnapshotRequest], snapshot.Snapshot]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_storage_pool(
        self,
    ) -> Callable[[storage_pool.GetStoragePoolRequest], storage_pool.StoragePool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetStoragePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume(self) -> Callable[[volume.GetVolumeRequest], volume.Volume]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_active_directories(
        self,
    ) -> Callable[
        [active_directory.ListActiveDirectoriesRequest],
        active_directory.ListActiveDirectoriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListActiveDirectories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_policies(
        self,
    ) -> Callable[
        [backup_policy.ListBackupPoliciesRequest],
        backup_policy.ListBackupPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[[backup.ListBackupsRequest], backup.ListBackupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_vaults(
        self,
    ) -> Callable[
        [backup_vault.ListBackupVaultsRequest], backup_vault.ListBackupVaultsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupVaults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_kms_configs(
        self,
    ) -> Callable[[kms.ListKmsConfigsRequest], kms.ListKmsConfigsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListKmsConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_replications(
        self,
    ) -> Callable[
        [replication.ListReplicationsRequest], replication.ListReplicationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReplications(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_snapshots(
        self,
    ) -> Callable[[snapshot.ListSnapshotsRequest], snapshot.ListSnapshotsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSnapshots(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_storage_pools(
        self,
    ) -> Callable[
        [storage_pool.ListStoragePoolsRequest], storage_pool.ListStoragePoolsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListStoragePools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volumes(
        self,
    ) -> Callable[[volume.ListVolumesRequest], volume.ListVolumesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_replication(
        self,
    ) -> Callable[[replication.ResumeReplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumeReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reverse_replication_direction(
        self,
    ) -> Callable[
        [replication.ReverseReplicationDirectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReverseReplicationDirection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def revert_volume(
        self,
    ) -> Callable[[volume.RevertVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RevertVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_replication(
        self,
    ) -> Callable[[replication.StopReplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def switch_active_replica_zone(
        self,
    ) -> Callable[
        [storage_pool.SwitchActiveReplicaZoneRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SwitchActiveReplicaZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_active_directory(
        self,
    ) -> Callable[
        [gcn_active_directory.UpdateActiveDirectoryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateActiveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[[gcn_backup.UpdateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup_policy(
        self,
    ) -> Callable[
        [gcn_backup_policy.UpdateBackupPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackupPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup_vault(
        self,
    ) -> Callable[
        [gcn_backup_vault.UpdateBackupVaultRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackupVault(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_kms_config(
        self,
    ) -> Callable[[kms.UpdateKmsConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateKmsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_replication(
        self,
    ) -> Callable[[gcn_replication.UpdateReplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_snapshot(
        self,
    ) -> Callable[[gcn_snapshot.UpdateSnapshotRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_storage_pool(
        self,
    ) -> Callable[
        [gcn_storage_pool.UpdateStoragePoolRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateStoragePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_volume(
        self,
    ) -> Callable[[gcn_volume.UpdateVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def verify_kms_config(
        self,
    ) -> Callable[[kms.VerifyKmsConfigRequest], kms.VerifyKmsConfigResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._VerifyKmsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseNetAppRestTransport._BaseGetLocation, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetLocation")

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

            http_options = _BaseNetAppRestTransport._BaseGetLocation._get_http_options()
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetLocation._get_response(
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
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(_BaseNetAppRestTransport._BaseListLocations, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListLocations")

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

            http_options = (
                _BaseNetAppRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListLocations._get_response(
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
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseNetAppRestTransport._BaseCancelOperation, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.CancelOperation")

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

            http_options = (
                _BaseNetAppRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseNetAppRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._CancelOperation._get_response(
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
        _BaseNetAppRestTransport._BaseDeleteOperation, NetAppRestStub
    ):
        def __hash__(self):
            return hash("NetAppRestTransport.DeleteOperation")

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

            http_options = (
                _BaseNetAppRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseNetAppRestTransport._BaseDeleteOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._DeleteOperation._get_response(
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

    class _GetOperation(_BaseNetAppRestTransport._BaseGetOperation, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.GetOperation")

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

            http_options = (
                _BaseNetAppRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(_BaseNetAppRestTransport._BaseListOperations, NetAppRestStub):
        def __hash__(self):
            return hash("NetAppRestTransport.ListOperations")

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

            http_options = (
                _BaseNetAppRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseNetAppRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseNetAppRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = NetAppRestTransport._ListOperations._get_response(
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
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("NetAppRestTransport",)
