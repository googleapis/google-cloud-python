# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import pkg_resources

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.clouddms_v1.types import clouddms
from google.cloud.clouddms_v1.types import clouddms_resources
from google.longrunning import operations_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dms",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DataMigrationServiceTransport(abc.ABC):
    """Abstract transport class for DataMigrationService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "datamigration.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes

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
        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
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

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_migration_jobs: gapic_v1.method.wrap_method(
                self.list_migration_jobs, default_timeout=60.0, client_info=client_info,
            ),
            self.get_migration_job: gapic_v1.method.wrap_method(
                self.get_migration_job, default_timeout=60.0, client_info=client_info,
            ),
            self.create_migration_job: gapic_v1.method.wrap_method(
                self.create_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_migration_job: gapic_v1.method.wrap_method(
                self.update_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_migration_job: gapic_v1.method.wrap_method(
                self.delete_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.start_migration_job: gapic_v1.method.wrap_method(
                self.start_migration_job, default_timeout=60.0, client_info=client_info,
            ),
            self.stop_migration_job: gapic_v1.method.wrap_method(
                self.stop_migration_job, default_timeout=60.0, client_info=client_info,
            ),
            self.resume_migration_job: gapic_v1.method.wrap_method(
                self.resume_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.promote_migration_job: gapic_v1.method.wrap_method(
                self.promote_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.verify_migration_job: gapic_v1.method.wrap_method(
                self.verify_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.restart_migration_job: gapic_v1.method.wrap_method(
                self.restart_migration_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.generate_ssh_script: gapic_v1.method.wrap_method(
                self.generate_ssh_script, default_timeout=60.0, client_info=client_info,
            ),
            self.list_connection_profiles: gapic_v1.method.wrap_method(
                self.list_connection_profiles,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_connection_profile: gapic_v1.method.wrap_method(
                self.get_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_connection_profile: gapic_v1.method.wrap_method(
                self.create_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_connection_profile: gapic_v1.method.wrap_method(
                self.update_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_connection_profile: gapic_v1.method.wrap_method(
                self.delete_connection_profile,
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
    def list_migration_jobs(
        self,
    ) -> Callable[
        [clouddms.ListMigrationJobsRequest],
        Union[
            clouddms.ListMigrationJobsResponse,
            Awaitable[clouddms.ListMigrationJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_migration_job(
        self,
    ) -> Callable[
        [clouddms.GetMigrationJobRequest],
        Union[
            clouddms_resources.MigrationJob, Awaitable[clouddms_resources.MigrationJob]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_migration_job(
        self,
    ) -> Callable[
        [clouddms.CreateMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_migration_job(
        self,
    ) -> Callable[
        [clouddms.UpdateMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_migration_job(
        self,
    ) -> Callable[
        [clouddms.DeleteMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_migration_job(
        self,
    ) -> Callable[
        [clouddms.StartMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_migration_job(
        self,
    ) -> Callable[
        [clouddms.StopMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def resume_migration_job(
        self,
    ) -> Callable[
        [clouddms.ResumeMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def promote_migration_job(
        self,
    ) -> Callable[
        [clouddms.PromoteMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def verify_migration_job(
        self,
    ) -> Callable[
        [clouddms.VerifyMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def restart_migration_job(
        self,
    ) -> Callable[
        [clouddms.RestartMigrationJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def generate_ssh_script(
        self,
    ) -> Callable[
        [clouddms.GenerateSshScriptRequest],
        Union[clouddms.SshScript, Awaitable[clouddms.SshScript]],
    ]:
        raise NotImplementedError()

    @property
    def list_connection_profiles(
        self,
    ) -> Callable[
        [clouddms.ListConnectionProfilesRequest],
        Union[
            clouddms.ListConnectionProfilesResponse,
            Awaitable[clouddms.ListConnectionProfilesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_connection_profile(
        self,
    ) -> Callable[
        [clouddms.GetConnectionProfileRequest],
        Union[
            clouddms_resources.ConnectionProfile,
            Awaitable[clouddms_resources.ConnectionProfile],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_connection_profile(
        self,
    ) -> Callable[
        [clouddms.CreateConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_connection_profile(
        self,
    ) -> Callable[
        [clouddms.UpdateConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_connection_profile(
        self,
    ) -> Callable[
        [clouddms.DeleteConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("DataMigrationServiceTransport",)
