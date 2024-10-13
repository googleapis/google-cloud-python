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
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.orchestration.airflow.service_v1beta1 import (
    gapic_version as package_version,
)
from google.cloud.orchestration.airflow.service_v1beta1.types import environments

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class EnvironmentsTransport(abc.ABC):
    """Abstract transport class for Environments."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "composer.googleapis.com"

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
                 The hostname to connect to (default: 'composer.googleapis.com').
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
            self.create_environment: gapic_v1.method.wrap_method(
                self.create_environment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_environment: gapic_v1.method.wrap_method(
                self.get_environment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_environments: gapic_v1.method.wrap_method(
                self.list_environments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_environment: gapic_v1.method.wrap_method(
                self.update_environment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_environment: gapic_v1.method.wrap_method(
                self.delete_environment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restart_web_server: gapic_v1.method.wrap_method(
                self.restart_web_server,
                default_timeout=None,
                client_info=client_info,
            ),
            self.check_upgrade: gapic_v1.method.wrap_method(
                self.check_upgrade,
                default_timeout=None,
                client_info=client_info,
            ),
            self.execute_airflow_command: gapic_v1.method.wrap_method(
                self.execute_airflow_command,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop_airflow_command: gapic_v1.method.wrap_method(
                self.stop_airflow_command,
                default_timeout=None,
                client_info=client_info,
            ),
            self.poll_airflow_command: gapic_v1.method.wrap_method(
                self.poll_airflow_command,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_workloads: gapic_v1.method.wrap_method(
                self.list_workloads,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_user_workloads_secret: gapic_v1.method.wrap_method(
                self.create_user_workloads_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_user_workloads_secret: gapic_v1.method.wrap_method(
                self.get_user_workloads_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_user_workloads_secrets: gapic_v1.method.wrap_method(
                self.list_user_workloads_secrets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_user_workloads_secret: gapic_v1.method.wrap_method(
                self.update_user_workloads_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_user_workloads_secret: gapic_v1.method.wrap_method(
                self.delete_user_workloads_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_user_workloads_config_map: gapic_v1.method.wrap_method(
                self.create_user_workloads_config_map,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_user_workloads_config_map: gapic_v1.method.wrap_method(
                self.get_user_workloads_config_map,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_user_workloads_config_maps: gapic_v1.method.wrap_method(
                self.list_user_workloads_config_maps,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_user_workloads_config_map: gapic_v1.method.wrap_method(
                self.update_user_workloads_config_map,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_user_workloads_config_map: gapic_v1.method.wrap_method(
                self.delete_user_workloads_config_map,
                default_timeout=None,
                client_info=client_info,
            ),
            self.save_snapshot: gapic_v1.method.wrap_method(
                self.save_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.load_snapshot: gapic_v1.method.wrap_method(
                self.load_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.database_failover: gapic_v1.method.wrap_method(
                self.database_failover,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_database_properties: gapic_v1.method.wrap_method(
                self.fetch_database_properties,
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
    def create_environment(
        self,
    ) -> Callable[
        [environments.CreateEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_environment(
        self,
    ) -> Callable[
        [environments.GetEnvironmentRequest],
        Union[environments.Environment, Awaitable[environments.Environment]],
    ]:
        raise NotImplementedError()

    @property
    def list_environments(
        self,
    ) -> Callable[
        [environments.ListEnvironmentsRequest],
        Union[
            environments.ListEnvironmentsResponse,
            Awaitable[environments.ListEnvironmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_environment(
        self,
    ) -> Callable[
        [environments.UpdateEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_environment(
        self,
    ) -> Callable[
        [environments.DeleteEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def restart_web_server(
        self,
    ) -> Callable[
        [environments.RestartWebServerRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def check_upgrade(
        self,
    ) -> Callable[
        [environments.CheckUpgradeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def execute_airflow_command(
        self,
    ) -> Callable[
        [environments.ExecuteAirflowCommandRequest],
        Union[
            environments.ExecuteAirflowCommandResponse,
            Awaitable[environments.ExecuteAirflowCommandResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def stop_airflow_command(
        self,
    ) -> Callable[
        [environments.StopAirflowCommandRequest],
        Union[
            environments.StopAirflowCommandResponse,
            Awaitable[environments.StopAirflowCommandResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def poll_airflow_command(
        self,
    ) -> Callable[
        [environments.PollAirflowCommandRequest],
        Union[
            environments.PollAirflowCommandResponse,
            Awaitable[environments.PollAirflowCommandResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_workloads(
        self,
    ) -> Callable[
        [environments.ListWorkloadsRequest],
        Union[
            environments.ListWorkloadsResponse,
            Awaitable[environments.ListWorkloadsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.CreateUserWorkloadsSecretRequest],
        Union[
            environments.UserWorkloadsSecret,
            Awaitable[environments.UserWorkloadsSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.GetUserWorkloadsSecretRequest],
        Union[
            environments.UserWorkloadsSecret,
            Awaitable[environments.UserWorkloadsSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_user_workloads_secrets(
        self,
    ) -> Callable[
        [environments.ListUserWorkloadsSecretsRequest],
        Union[
            environments.ListUserWorkloadsSecretsResponse,
            Awaitable[environments.ListUserWorkloadsSecretsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.UpdateUserWorkloadsSecretRequest],
        Union[
            environments.UserWorkloadsSecret,
            Awaitable[environments.UserWorkloadsSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.DeleteUserWorkloadsSecretRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.CreateUserWorkloadsConfigMapRequest],
        Union[
            environments.UserWorkloadsConfigMap,
            Awaitable[environments.UserWorkloadsConfigMap],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.GetUserWorkloadsConfigMapRequest],
        Union[
            environments.UserWorkloadsConfigMap,
            Awaitable[environments.UserWorkloadsConfigMap],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_user_workloads_config_maps(
        self,
    ) -> Callable[
        [environments.ListUserWorkloadsConfigMapsRequest],
        Union[
            environments.ListUserWorkloadsConfigMapsResponse,
            Awaitable[environments.ListUserWorkloadsConfigMapsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.UpdateUserWorkloadsConfigMapRequest],
        Union[
            environments.UserWorkloadsConfigMap,
            Awaitable[environments.UserWorkloadsConfigMap],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.DeleteUserWorkloadsConfigMapRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def save_snapshot(
        self,
    ) -> Callable[
        [environments.SaveSnapshotRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def load_snapshot(
        self,
    ) -> Callable[
        [environments.LoadSnapshotRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def database_failover(
        self,
    ) -> Callable[
        [environments.DatabaseFailoverRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def fetch_database_properties(
        self,
    ) -> Callable[
        [environments.FetchDatabasePropertiesRequest],
        Union[
            environments.FetchDatabasePropertiesResponse,
            Awaitable[environments.FetchDatabasePropertiesResponse],
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
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("EnvironmentsTransport",)
