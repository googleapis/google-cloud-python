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

from google.cloud.storage_transfer_v1 import gapic_version as package_version
from google.cloud.storage_transfer_v1.types import transfer, transfer_types

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class StorageTransferServiceTransport(abc.ABC):
    """Abstract transport class for StorageTransferService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "storagetransfer.googleapis.com"

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
                 The hostname to connect to (default: 'storagetransfer.googleapis.com').
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
            self.get_google_service_account: gapic_v1.method.wrap_method(
                self.get_google_service_account,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_transfer_job: gapic_v1.method.wrap_method(
                self.create_transfer_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_transfer_job: gapic_v1.method.wrap_method(
                self.update_transfer_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_transfer_job: gapic_v1.method.wrap_method(
                self.get_transfer_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_transfer_jobs: gapic_v1.method.wrap_method(
                self.list_transfer_jobs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.pause_transfer_operation: gapic_v1.method.wrap_method(
                self.pause_transfer_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.resume_transfer_operation: gapic_v1.method.wrap_method(
                self.resume_transfer_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.run_transfer_job: gapic_v1.method.wrap_method(
                self.run_transfer_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_transfer_job: gapic_v1.method.wrap_method(
                self.delete_transfer_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_agent_pool: gapic_v1.method.wrap_method(
                self.create_agent_pool,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_agent_pool: gapic_v1.method.wrap_method(
                self.update_agent_pool,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_agent_pool: gapic_v1.method.wrap_method(
                self.get_agent_pool,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_agent_pools: gapic_v1.method.wrap_method(
                self.list_agent_pools,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_agent_pool: gapic_v1.method.wrap_method(
                self.delete_agent_pool,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: gapic_v1.method.wrap_method(
                self.cancel_operation,
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
    def get_google_service_account(
        self,
    ) -> Callable[
        [transfer.GetGoogleServiceAccountRequest],
        Union[
            transfer_types.GoogleServiceAccount,
            Awaitable[transfer_types.GoogleServiceAccount],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_transfer_job(
        self,
    ) -> Callable[
        [transfer.CreateTransferJobRequest],
        Union[transfer_types.TransferJob, Awaitable[transfer_types.TransferJob]],
    ]:
        raise NotImplementedError()

    @property
    def update_transfer_job(
        self,
    ) -> Callable[
        [transfer.UpdateTransferJobRequest],
        Union[transfer_types.TransferJob, Awaitable[transfer_types.TransferJob]],
    ]:
        raise NotImplementedError()

    @property
    def get_transfer_job(
        self,
    ) -> Callable[
        [transfer.GetTransferJobRequest],
        Union[transfer_types.TransferJob, Awaitable[transfer_types.TransferJob]],
    ]:
        raise NotImplementedError()

    @property
    def list_transfer_jobs(
        self,
    ) -> Callable[
        [transfer.ListTransferJobsRequest],
        Union[
            transfer.ListTransferJobsResponse,
            Awaitable[transfer.ListTransferJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def pause_transfer_operation(
        self,
    ) -> Callable[
        [transfer.PauseTransferOperationRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def resume_transfer_operation(
        self,
    ) -> Callable[
        [transfer.ResumeTransferOperationRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def run_transfer_job(
        self,
    ) -> Callable[
        [transfer.RunTransferJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_transfer_job(
        self,
    ) -> Callable[
        [transfer.DeleteTransferJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_agent_pool(
        self,
    ) -> Callable[
        [transfer.CreateAgentPoolRequest],
        Union[transfer_types.AgentPool, Awaitable[transfer_types.AgentPool]],
    ]:
        raise NotImplementedError()

    @property
    def update_agent_pool(
        self,
    ) -> Callable[
        [transfer.UpdateAgentPoolRequest],
        Union[transfer_types.AgentPool, Awaitable[transfer_types.AgentPool]],
    ]:
        raise NotImplementedError()

    @property
    def get_agent_pool(
        self,
    ) -> Callable[
        [transfer.GetAgentPoolRequest],
        Union[transfer_types.AgentPool, Awaitable[transfer_types.AgentPool]],
    ]:
        raise NotImplementedError()

    @property
    def list_agent_pools(
        self,
    ) -> Callable[
        [transfer.ListAgentPoolsRequest],
        Union[
            transfer.ListAgentPoolsResponse, Awaitable[transfer.ListAgentPoolsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_agent_pool(
        self,
    ) -> Callable[
        [transfer.DeleteAgentPoolRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
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
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("StorageTransferServiceTransport",)
