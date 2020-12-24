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
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.notebooks_v1beta1.types import environment
from google.cloud.notebooks_v1beta1.types import instance
from google.cloud.notebooks_v1beta1.types import service
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-notebooks",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


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
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
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

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_instances: gapic_v1.method.wrap_method(
                self.list_instances, default_timeout=60.0, client_info=client_info,
            ),
            self.get_instance: gapic_v1.method.wrap_method(
                self.get_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.create_instance: gapic_v1.method.wrap_method(
                self.create_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.register_instance: gapic_v1.method.wrap_method(
                self.register_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.set_instance_accelerator: gapic_v1.method.wrap_method(
                self.set_instance_accelerator,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_instance_machine_type: gapic_v1.method.wrap_method(
                self.set_instance_machine_type,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_instance_labels: gapic_v1.method.wrap_method(
                self.set_instance_labels, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_instance: gapic_v1.method.wrap_method(
                self.delete_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.start_instance: gapic_v1.method.wrap_method(
                self.start_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.stop_instance: gapic_v1.method.wrap_method(
                self.stop_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.reset_instance: gapic_v1.method.wrap_method(
                self.reset_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.report_instance_info: gapic_v1.method.wrap_method(
                self.report_instance_info,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.is_instance_upgradeable: gapic_v1.method.wrap_method(
                self.is_instance_upgradeable,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.upgrade_instance: gapic_v1.method.wrap_method(
                self.upgrade_instance, default_timeout=60.0, client_info=client_info,
            ),
            self.upgrade_instance_internal: gapic_v1.method.wrap_method(
                self.upgrade_instance_internal,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_environments: gapic_v1.method.wrap_method(
                self.list_environments, default_timeout=60.0, client_info=client_info,
            ),
            self.get_environment: gapic_v1.method.wrap_method(
                self.get_environment, default_timeout=60.0, client_info=client_info,
            ),
            self.create_environment: gapic_v1.method.wrap_method(
                self.create_environment, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_environment: gapic_v1.method.wrap_method(
                self.delete_environment, default_timeout=60.0, client_info=client_info,
            ),
        }

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
