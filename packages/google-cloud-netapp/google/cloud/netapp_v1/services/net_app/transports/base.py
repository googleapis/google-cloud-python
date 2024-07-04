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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, operations_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.netapp_v1 import gapic_version as package_version
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

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class NetAppTransport(abc.ABC):
    """Abstract transport class for NetApp."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "netapp.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
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
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_storage_pools: gapic_v1.method.wrap_method(
                self.list_storage_pools,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_storage_pool: gapic_v1.method.wrap_method(
                self.create_storage_pool,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_storage_pool: gapic_v1.method.wrap_method(
                self.get_storage_pool,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_storage_pool: gapic_v1.method.wrap_method(
                self.update_storage_pool,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_storage_pool: gapic_v1.method.wrap_method(
                self.delete_storage_pool,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_volumes: gapic_v1.method.wrap_method(
                self.list_volumes,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_volume: gapic_v1.method.wrap_method(
                self.get_volume,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_volume: gapic_v1.method.wrap_method(
                self.create_volume,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_volume: gapic_v1.method.wrap_method(
                self.update_volume,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_volume: gapic_v1.method.wrap_method(
                self.delete_volume,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.revert_volume: gapic_v1.method.wrap_method(
                self.revert_volume,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_snapshots: gapic_v1.method.wrap_method(
                self.list_snapshots,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_snapshot: gapic_v1.method.wrap_method(
                self.get_snapshot,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_snapshot: gapic_v1.method.wrap_method(
                self.create_snapshot,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_snapshot: gapic_v1.method.wrap_method(
                self.delete_snapshot,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_snapshot: gapic_v1.method.wrap_method(
                self.update_snapshot,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_active_directories: gapic_v1.method.wrap_method(
                self.list_active_directories,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_active_directory: gapic_v1.method.wrap_method(
                self.get_active_directory,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_active_directory: gapic_v1.method.wrap_method(
                self.create_active_directory,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_active_directory: gapic_v1.method.wrap_method(
                self.update_active_directory,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_active_directory: gapic_v1.method.wrap_method(
                self.delete_active_directory,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_kms_configs: gapic_v1.method.wrap_method(
                self.list_kms_configs,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_kms_config: gapic_v1.method.wrap_method(
                self.create_kms_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_kms_config: gapic_v1.method.wrap_method(
                self.get_kms_config,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_kms_config: gapic_v1.method.wrap_method(
                self.update_kms_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.encrypt_volumes: gapic_v1.method.wrap_method(
                self.encrypt_volumes,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.verify_kms_config: gapic_v1.method.wrap_method(
                self.verify_kms_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_kms_config: gapic_v1.method.wrap_method(
                self.delete_kms_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_replications: gapic_v1.method.wrap_method(
                self.list_replications,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_replication: gapic_v1.method.wrap_method(
                self.get_replication,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_replication: gapic_v1.method.wrap_method(
                self.create_replication,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_replication: gapic_v1.method.wrap_method(
                self.delete_replication,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_replication: gapic_v1.method.wrap_method(
                self.update_replication,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.stop_replication: gapic_v1.method.wrap_method(
                self.stop_replication,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.resume_replication: gapic_v1.method.wrap_method(
                self.resume_replication,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.reverse_replication_direction: gapic_v1.method.wrap_method(
                self.reverse_replication_direction,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_backup_vault: gapic_v1.method.wrap_method(
                self.create_backup_vault,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup_vault: gapic_v1.method.wrap_method(
                self.get_backup_vault,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_backup_vaults: gapic_v1.method.wrap_method(
                self.list_backup_vaults,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup_vault: gapic_v1.method.wrap_method(
                self.update_backup_vault,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup_vault: gapic_v1.method.wrap_method(
                self.delete_backup_vault,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_backup: gapic_v1.method.wrap_method(
                self.create_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup: gapic_v1.method.wrap_method(
                self.get_backup,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_backups: gapic_v1.method.wrap_method(
                self.list_backups,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup: gapic_v1.method.wrap_method(
                self.delete_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup: gapic_v1.method.wrap_method(
                self.update_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_backup_policy: gapic_v1.method.wrap_method(
                self.create_backup_policy,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup_policy: gapic_v1.method.wrap_method(
                self.get_backup_policy,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_backup_policies: gapic_v1.method.wrap_method(
                self.list_backup_policies,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup_policy: gapic_v1.method.wrap_method(
                self.update_backup_policy,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup_policy: gapic_v1.method.wrap_method(
                self.delete_backup_policy,
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_storage_pools(
        self,
    ) -> Callable[
        [storage_pool.ListStoragePoolsRequest],
        Union[
            storage_pool.ListStoragePoolsResponse,
            Awaitable[storage_pool.ListStoragePoolsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_storage_pool(
        self,
    ) -> Callable[
        [gcn_storage_pool.CreateStoragePoolRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_storage_pool(
        self,
    ) -> Callable[
        [storage_pool.GetStoragePoolRequest],
        Union[storage_pool.StoragePool, Awaitable[storage_pool.StoragePool]],
    ]:
        raise NotImplementedError()

    @property
    def update_storage_pool(
        self,
    ) -> Callable[
        [gcn_storage_pool.UpdateStoragePoolRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_storage_pool(
        self,
    ) -> Callable[
        [storage_pool.DeleteStoragePoolRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_volumes(
        self,
    ) -> Callable[
        [volume.ListVolumesRequest],
        Union[volume.ListVolumesResponse, Awaitable[volume.ListVolumesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_volume(
        self,
    ) -> Callable[
        [volume.GetVolumeRequest], Union[volume.Volume, Awaitable[volume.Volume]]
    ]:
        raise NotImplementedError()

    @property
    def create_volume(
        self,
    ) -> Callable[
        [gcn_volume.CreateVolumeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_volume(
        self,
    ) -> Callable[
        [gcn_volume.UpdateVolumeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_volume(
        self,
    ) -> Callable[
        [volume.DeleteVolumeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def revert_volume(
        self,
    ) -> Callable[
        [volume.RevertVolumeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_snapshots(
        self,
    ) -> Callable[
        [snapshot.ListSnapshotsRequest],
        Union[
            snapshot.ListSnapshotsResponse, Awaitable[snapshot.ListSnapshotsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_snapshot(
        self,
    ) -> Callable[
        [snapshot.GetSnapshotRequest],
        Union[snapshot.Snapshot, Awaitable[snapshot.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def create_snapshot(
        self,
    ) -> Callable[
        [gcn_snapshot.CreateSnapshotRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_snapshot(
        self,
    ) -> Callable[
        [snapshot.DeleteSnapshotRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_snapshot(
        self,
    ) -> Callable[
        [gcn_snapshot.UpdateSnapshotRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_active_directories(
        self,
    ) -> Callable[
        [active_directory.ListActiveDirectoriesRequest],
        Union[
            active_directory.ListActiveDirectoriesResponse,
            Awaitable[active_directory.ListActiveDirectoriesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_active_directory(
        self,
    ) -> Callable[
        [active_directory.GetActiveDirectoryRequest],
        Union[
            active_directory.ActiveDirectory,
            Awaitable[active_directory.ActiveDirectory],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_active_directory(
        self,
    ) -> Callable[
        [gcn_active_directory.CreateActiveDirectoryRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_active_directory(
        self,
    ) -> Callable[
        [gcn_active_directory.UpdateActiveDirectoryRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_active_directory(
        self,
    ) -> Callable[
        [active_directory.DeleteActiveDirectoryRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_kms_configs(
        self,
    ) -> Callable[
        [kms.ListKmsConfigsRequest],
        Union[kms.ListKmsConfigsResponse, Awaitable[kms.ListKmsConfigsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_kms_config(
        self,
    ) -> Callable[
        [kms.CreateKmsConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_kms_config(
        self,
    ) -> Callable[
        [kms.GetKmsConfigRequest], Union[kms.KmsConfig, Awaitable[kms.KmsConfig]]
    ]:
        raise NotImplementedError()

    @property
    def update_kms_config(
        self,
    ) -> Callable[
        [kms.UpdateKmsConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def encrypt_volumes(
        self,
    ) -> Callable[
        [kms.EncryptVolumesRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def verify_kms_config(
        self,
    ) -> Callable[
        [kms.VerifyKmsConfigRequest],
        Union[kms.VerifyKmsConfigResponse, Awaitable[kms.VerifyKmsConfigResponse]],
    ]:
        raise NotImplementedError()

    @property
    def delete_kms_config(
        self,
    ) -> Callable[
        [kms.DeleteKmsConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_replications(
        self,
    ) -> Callable[
        [replication.ListReplicationsRequest],
        Union[
            replication.ListReplicationsResponse,
            Awaitable[replication.ListReplicationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_replication(
        self,
    ) -> Callable[
        [replication.GetReplicationRequest],
        Union[replication.Replication, Awaitable[replication.Replication]],
    ]:
        raise NotImplementedError()

    @property
    def create_replication(
        self,
    ) -> Callable[
        [gcn_replication.CreateReplicationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_replication(
        self,
    ) -> Callable[
        [replication.DeleteReplicationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_replication(
        self,
    ) -> Callable[
        [gcn_replication.UpdateReplicationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_replication(
        self,
    ) -> Callable[
        [replication.StopReplicationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def resume_replication(
        self,
    ) -> Callable[
        [replication.ResumeReplicationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def reverse_replication_direction(
        self,
    ) -> Callable[
        [replication.ReverseReplicationDirectionRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_backup_vault(
        self,
    ) -> Callable[
        [gcn_backup_vault.CreateBackupVaultRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_backup_vault(
        self,
    ) -> Callable[
        [backup_vault.GetBackupVaultRequest],
        Union[backup_vault.BackupVault, Awaitable[backup_vault.BackupVault]],
    ]:
        raise NotImplementedError()

    @property
    def list_backup_vaults(
        self,
    ) -> Callable[
        [backup_vault.ListBackupVaultsRequest],
        Union[
            backup_vault.ListBackupVaultsResponse,
            Awaitable[backup_vault.ListBackupVaultsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_backup_vault(
        self,
    ) -> Callable[
        [gcn_backup_vault.UpdateBackupVaultRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_backup_vault(
        self,
    ) -> Callable[
        [backup_vault.DeleteBackupVaultRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_backup(
        self,
    ) -> Callable[
        [gcn_backup.CreateBackupRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_backup(
        self,
    ) -> Callable[
        [backup.GetBackupRequest], Union[backup.Backup, Awaitable[backup.Backup]]
    ]:
        raise NotImplementedError()

    @property
    def list_backups(
        self,
    ) -> Callable[
        [backup.ListBackupsRequest],
        Union[backup.ListBackupsResponse, Awaitable[backup.ListBackupsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def delete_backup(
        self,
    ) -> Callable[
        [backup.DeleteBackupRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_backup(
        self,
    ) -> Callable[
        [gcn_backup.UpdateBackupRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_backup_policy(
        self,
    ) -> Callable[
        [gcn_backup_policy.CreateBackupPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_backup_policy(
        self,
    ) -> Callable[
        [backup_policy.GetBackupPolicyRequest],
        Union[backup_policy.BackupPolicy, Awaitable[backup_policy.BackupPolicy]],
    ]:
        raise NotImplementedError()

    @property
    def list_backup_policies(
        self,
    ) -> Callable[
        [backup_policy.ListBackupPoliciesRequest],
        Union[
            backup_policy.ListBackupPoliciesResponse,
            Awaitable[backup_policy.ListBackupPoliciesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_backup_policy(
        self,
    ) -> Callable[
        [gcn_backup_policy.UpdateBackupPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_backup_policy(
        self,
    ) -> Callable[
        [backup_policy.DeleteBackupPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def get_location(
        self,
    ) -> Callable[
        [locations_pb2.GetLocationRequest],
        Union[locations_pb2.Location, Awaitable[locations_pb2.Location]],
    ]:
        raise NotImplementedError()

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest],
        Union[
            locations_pb2.ListLocationsResponse,
            Awaitable[locations_pb2.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("NetAppTransport",)
