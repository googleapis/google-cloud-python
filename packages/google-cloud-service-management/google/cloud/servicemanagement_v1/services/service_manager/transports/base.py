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

from google.api import service_pb2 as service  # type: ignore
from google.cloud.servicemanagement_v1.types import resources
from google.cloud.servicemanagement_v1.types import servicemanager
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-service-management",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ServiceManagerTransport(abc.ABC):
    """Abstract transport class for ServiceManager."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/service.management",
        "https://www.googleapis.com/auth/service.management.readonly",
    )

    def __init__(
        self,
        *,
        host: str = "servicemanagement.googleapis.com",
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

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_services: gapic_v1.method.wrap_method(
                self.list_services, default_timeout=None, client_info=client_info,
            ),
            self.get_service: gapic_v1.method.wrap_method(
                self.get_service, default_timeout=None, client_info=client_info,
            ),
            self.create_service: gapic_v1.method.wrap_method(
                self.create_service, default_timeout=None, client_info=client_info,
            ),
            self.delete_service: gapic_v1.method.wrap_method(
                self.delete_service, default_timeout=None, client_info=client_info,
            ),
            self.undelete_service: gapic_v1.method.wrap_method(
                self.undelete_service, default_timeout=None, client_info=client_info,
            ),
            self.list_service_configs: gapic_v1.method.wrap_method(
                self.list_service_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_config: gapic_v1.method.wrap_method(
                self.get_service_config, default_timeout=None, client_info=client_info,
            ),
            self.create_service_config: gapic_v1.method.wrap_method(
                self.create_service_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.submit_config_source: gapic_v1.method.wrap_method(
                self.submit_config_source,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_service_rollouts: gapic_v1.method.wrap_method(
                self.list_service_rollouts,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_rollout: gapic_v1.method.wrap_method(
                self.get_service_rollout, default_timeout=None, client_info=client_info,
            ),
            self.create_service_rollout: gapic_v1.method.wrap_method(
                self.create_service_rollout,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_config_report: gapic_v1.method.wrap_method(
                self.generate_config_report,
                default_timeout=None,
                client_info=client_info,
            ),
            self.enable_service: gapic_v1.method.wrap_method(
                self.enable_service, default_timeout=None, client_info=client_info,
            ),
            self.disable_service: gapic_v1.method.wrap_method(
                self.disable_service, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_services(
        self,
    ) -> typing.Callable[
        [servicemanager.ListServicesRequest],
        typing.Union[
            servicemanager.ListServicesResponse,
            typing.Awaitable[servicemanager.ListServicesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service(
        self,
    ) -> typing.Callable[
        [servicemanager.GetServiceRequest],
        typing.Union[
            resources.ManagedService, typing.Awaitable[resources.ManagedService]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_service(
        self,
    ) -> typing.Callable[
        [servicemanager.CreateServiceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_service(
        self,
    ) -> typing.Callable[
        [servicemanager.DeleteServiceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def undelete_service(
        self,
    ) -> typing.Callable[
        [servicemanager.UndeleteServiceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_service_configs(
        self,
    ) -> typing.Callable[
        [servicemanager.ListServiceConfigsRequest],
        typing.Union[
            servicemanager.ListServiceConfigsResponse,
            typing.Awaitable[servicemanager.ListServiceConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service_config(
        self,
    ) -> typing.Callable[
        [servicemanager.GetServiceConfigRequest],
        typing.Union[service.Service, typing.Awaitable[service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def create_service_config(
        self,
    ) -> typing.Callable[
        [servicemanager.CreateServiceConfigRequest],
        typing.Union[service.Service, typing.Awaitable[service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def submit_config_source(
        self,
    ) -> typing.Callable[
        [servicemanager.SubmitConfigSourceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_service_rollouts(
        self,
    ) -> typing.Callable[
        [servicemanager.ListServiceRolloutsRequest],
        typing.Union[
            servicemanager.ListServiceRolloutsResponse,
            typing.Awaitable[servicemanager.ListServiceRolloutsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service_rollout(
        self,
    ) -> typing.Callable[
        [servicemanager.GetServiceRolloutRequest],
        typing.Union[resources.Rollout, typing.Awaitable[resources.Rollout]],
    ]:
        raise NotImplementedError()

    @property
    def create_service_rollout(
        self,
    ) -> typing.Callable[
        [servicemanager.CreateServiceRolloutRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def generate_config_report(
        self,
    ) -> typing.Callable[
        [servicemanager.GenerateConfigReportRequest],
        typing.Union[
            servicemanager.GenerateConfigReportResponse,
            typing.Awaitable[servicemanager.GenerateConfigReportResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def enable_service(
        self,
    ) -> typing.Callable[
        [servicemanager.EnableServiceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def disable_service(
        self,
    ) -> typing.Callable[
        [servicemanager.DisableServiceRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("ServiceManagerTransport",)
