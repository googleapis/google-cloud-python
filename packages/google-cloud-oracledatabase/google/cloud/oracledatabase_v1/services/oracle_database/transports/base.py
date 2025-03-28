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

from google.cloud.oracledatabase_v1 import gapic_version as package_version
from google.cloud.oracledatabase_v1.types import (
    autonomous_database,
    exadata_infra,
    oracledatabase,
    vm_cluster,
)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class OracleDatabaseTransport(abc.ABC):
    """Abstract transport class for OracleDatabase."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "oracledatabase.googleapis.com"

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
                 The hostname to connect to (default: 'oracledatabase.googleapis.com').
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
            self.list_cloud_exadata_infrastructures: gapic_v1.method.wrap_method(
                self.list_cloud_exadata_infrastructures,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_cloud_exadata_infrastructure: gapic_v1.method.wrap_method(
                self.get_cloud_exadata_infrastructure,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_cloud_exadata_infrastructure: gapic_v1.method.wrap_method(
                self.create_cloud_exadata_infrastructure,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_cloud_exadata_infrastructure: gapic_v1.method.wrap_method(
                self.delete_cloud_exadata_infrastructure,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_cloud_vm_clusters: gapic_v1.method.wrap_method(
                self.list_cloud_vm_clusters,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_cloud_vm_cluster: gapic_v1.method.wrap_method(
                self.get_cloud_vm_cluster,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_cloud_vm_cluster: gapic_v1.method.wrap_method(
                self.create_cloud_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_cloud_vm_cluster: gapic_v1.method.wrap_method(
                self.delete_cloud_vm_cluster,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_entitlements: gapic_v1.method.wrap_method(
                self.list_entitlements,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_servers: gapic_v1.method.wrap_method(
                self.list_db_servers,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_nodes: gapic_v1.method.wrap_method(
                self.list_db_nodes,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_gi_versions: gapic_v1.method.wrap_method(
                self.list_gi_versions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_db_system_shapes: gapic_v1.method.wrap_method(
                self.list_db_system_shapes,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_databases: gapic_v1.method.wrap_method(
                self.list_autonomous_databases,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_autonomous_database: gapic_v1.method.wrap_method(
                self.get_autonomous_database,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_autonomous_database: gapic_v1.method.wrap_method(
                self.create_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_autonomous_database: gapic_v1.method.wrap_method(
                self.delete_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restore_autonomous_database: gapic_v1.method.wrap_method(
                self.restore_autonomous_database,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_autonomous_database_wallet: gapic_v1.method.wrap_method(
                self.generate_autonomous_database_wallet,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_autonomous_db_versions: gapic_v1.method.wrap_method(
                self.list_autonomous_db_versions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_database_character_sets: gapic_v1.method.wrap_method(
                self.list_autonomous_database_character_sets,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_autonomous_database_backups: gapic_v1.method.wrap_method(
                self.list_autonomous_database_backups,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_location: gapic_v1.method.wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: gapic_v1.method.wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: gapic_v1.method.wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: gapic_v1.method.wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: gapic_v1.method.wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: gapic_v1.method.wrap_method(
                self.list_operations,
                default_timeout=None,
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
    def list_cloud_exadata_infrastructures(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudExadataInfrastructuresRequest],
        Union[
            oracledatabase.ListCloudExadataInfrastructuresResponse,
            Awaitable[oracledatabase.ListCloudExadataInfrastructuresResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.GetCloudExadataInfrastructureRequest],
        Union[
            exadata_infra.CloudExadataInfrastructure,
            Awaitable[exadata_infra.CloudExadataInfrastructure],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudExadataInfrastructureRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_cloud_exadata_infrastructure(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudExadataInfrastructureRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_cloud_vm_clusters(
        self,
    ) -> Callable[
        [oracledatabase.ListCloudVmClustersRequest],
        Union[
            oracledatabase.ListCloudVmClustersResponse,
            Awaitable[oracledatabase.ListCloudVmClustersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.GetCloudVmClusterRequest],
        Union[vm_cluster.CloudVmCluster, Awaitable[vm_cluster.CloudVmCluster]],
    ]:
        raise NotImplementedError()

    @property
    def create_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.CreateCloudVmClusterRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_cloud_vm_cluster(
        self,
    ) -> Callable[
        [oracledatabase.DeleteCloudVmClusterRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_entitlements(
        self,
    ) -> Callable[
        [oracledatabase.ListEntitlementsRequest],
        Union[
            oracledatabase.ListEntitlementsResponse,
            Awaitable[oracledatabase.ListEntitlementsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_db_servers(
        self,
    ) -> Callable[
        [oracledatabase.ListDbServersRequest],
        Union[
            oracledatabase.ListDbServersResponse,
            Awaitable[oracledatabase.ListDbServersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_db_nodes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbNodesRequest],
        Union[
            oracledatabase.ListDbNodesResponse,
            Awaitable[oracledatabase.ListDbNodesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_gi_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListGiVersionsRequest],
        Union[
            oracledatabase.ListGiVersionsResponse,
            Awaitable[oracledatabase.ListGiVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_db_system_shapes(
        self,
    ) -> Callable[
        [oracledatabase.ListDbSystemShapesRequest],
        Union[
            oracledatabase.ListDbSystemShapesResponse,
            Awaitable[oracledatabase.ListDbSystemShapesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_autonomous_databases(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabasesRequest],
        Union[
            oracledatabase.ListAutonomousDatabasesResponse,
            Awaitable[oracledatabase.ListAutonomousDatabasesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.GetAutonomousDatabaseRequest],
        Union[
            autonomous_database.AutonomousDatabase,
            Awaitable[autonomous_database.AutonomousDatabase],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.CreateAutonomousDatabaseRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.DeleteAutonomousDatabaseRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def restore_autonomous_database(
        self,
    ) -> Callable[
        [oracledatabase.RestoreAutonomousDatabaseRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def generate_autonomous_database_wallet(
        self,
    ) -> Callable[
        [oracledatabase.GenerateAutonomousDatabaseWalletRequest],
        Union[
            oracledatabase.GenerateAutonomousDatabaseWalletResponse,
            Awaitable[oracledatabase.GenerateAutonomousDatabaseWalletResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_autonomous_db_versions(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDbVersionsRequest],
        Union[
            oracledatabase.ListAutonomousDbVersionsResponse,
            Awaitable[oracledatabase.ListAutonomousDbVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_autonomous_database_character_sets(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseCharacterSetsRequest],
        Union[
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
            Awaitable[oracledatabase.ListAutonomousDatabaseCharacterSetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_autonomous_database_backups(
        self,
    ) -> Callable[
        [oracledatabase.ListAutonomousDatabaseBackupsRequest],
        Union[
            oracledatabase.ListAutonomousDatabaseBackupsResponse,
            Awaitable[oracledatabase.ListAutonomousDatabaseBackupsResponse],
        ],
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


__all__ = ("OracleDatabaseTransport",)
