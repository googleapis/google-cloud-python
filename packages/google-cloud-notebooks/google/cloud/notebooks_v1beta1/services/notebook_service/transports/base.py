# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
import typing

from google import auth
from google.api_core import exceptions  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.notebooks_v1beta1.types import environment
from google.cloud.notebooks_v1beta1.types import instance
from google.cloud.notebooks_v1beta1.types import service
from google.longrunning import operations_pb2 as operations  # type: ignore


class NotebookServiceTransport(abc.ABC):
    """Abstract transport class for NotebookService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "notebooks.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_instances(
        self,
    ) -> typing.Callable[
        [service.ListInstancesRequest],
        typing.Union[
            service.ListInstancesResponse,
            typing.Awaitable[service.ListInstancesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_instance(
        self,
    ) -> typing.Callable[
        [service.GetInstanceRequest],
        typing.Union[instance.Instance, typing.Awaitable[instance.Instance]],
    ]:
        raise NotImplementedError()

    @property
    def create_instance(
        self,
    ) -> typing.Callable[
        [service.CreateInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def register_instance(
        self,
    ) -> typing.Callable[
        [service.RegisterInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_accelerator(
        self,
    ) -> typing.Callable[
        [service.SetInstanceAcceleratorRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_machine_type(
        self,
    ) -> typing.Callable[
        [service.SetInstanceMachineTypeRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_labels(
        self,
    ) -> typing.Callable[
        [service.SetInstanceLabelsRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_instance(
        self,
    ) -> typing.Callable[
        [service.DeleteInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_instance(
        self,
    ) -> typing.Callable[
        [service.StartInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_instance(
        self,
    ) -> typing.Callable[
        [service.StopInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def reset_instance(
        self,
    ) -> typing.Callable[
        [service.ResetInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def report_instance_info(
        self,
    ) -> typing.Callable[
        [service.ReportInstanceInfoRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def is_instance_upgradeable(
        self,
    ) -> typing.Callable[
        [service.IsInstanceUpgradeableRequest],
        typing.Union[
            service.IsInstanceUpgradeableResponse,
            typing.Awaitable[service.IsInstanceUpgradeableResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def upgrade_instance(
        self,
    ) -> typing.Callable[
        [service.UpgradeInstanceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def upgrade_instance_internal(
        self,
    ) -> typing.Callable[
        [service.UpgradeInstanceInternalRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_environments(
        self,
    ) -> typing.Callable[
        [service.ListEnvironmentsRequest],
        typing.Union[
            service.ListEnvironmentsResponse,
            typing.Awaitable[service.ListEnvironmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_environment(
        self,
    ) -> typing.Callable[
        [service.GetEnvironmentRequest],
        typing.Union[
            environment.Environment, typing.Awaitable[environment.Environment]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_environment(
        self,
    ) -> typing.Callable[
        [service.CreateEnvironmentRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_environment(
        self,
    ) -> typing.Callable[
        [service.DeleteEnvironmentRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("NotebookServiceTransport",)
