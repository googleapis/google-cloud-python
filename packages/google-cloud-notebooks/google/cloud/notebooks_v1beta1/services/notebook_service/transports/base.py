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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.notebooks_v1beta1.types import environment
from google.cloud.notebooks_v1beta1.types import instance
from google.cloud.notebooks_v1beta1.types import service
from google.longrunning import operations_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-notebooks",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None


class NotebookServiceTransport(abc.ABC):
    """Abstract transport class for NotebookService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "notebooks.googleapis.com"

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

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

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

        # If the credentials is service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): This method is in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-auth is increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

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
    ) -> Callable[
        [service.ListInstancesRequest],
        Union[service.ListInstancesResponse, Awaitable[service.ListInstancesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_instance(
        self,
    ) -> Callable[
        [service.GetInstanceRequest],
        Union[instance.Instance, Awaitable[instance.Instance]],
    ]:
        raise NotImplementedError()

    @property
    def create_instance(
        self,
    ) -> Callable[
        [service.CreateInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def register_instance(
        self,
    ) -> Callable[
        [service.RegisterInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_accelerator(
        self,
    ) -> Callable[
        [service.SetInstanceAcceleratorRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_machine_type(
        self,
    ) -> Callable[
        [service.SetInstanceMachineTypeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_labels(
        self,
    ) -> Callable[
        [service.SetInstanceLabelsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [service.DeleteInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_instance(
        self,
    ) -> Callable[
        [service.StartInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_instance(
        self,
    ) -> Callable[
        [service.StopInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def reset_instance(
        self,
    ) -> Callable[
        [service.ResetInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def report_instance_info(
        self,
    ) -> Callable[
        [service.ReportInstanceInfoRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def is_instance_upgradeable(
        self,
    ) -> Callable[
        [service.IsInstanceUpgradeableRequest],
        Union[
            service.IsInstanceUpgradeableResponse,
            Awaitable[service.IsInstanceUpgradeableResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def upgrade_instance(
        self,
    ) -> Callable[
        [service.UpgradeInstanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def upgrade_instance_internal(
        self,
    ) -> Callable[
        [service.UpgradeInstanceInternalRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_environments(
        self,
    ) -> Callable[
        [service.ListEnvironmentsRequest],
        Union[
            service.ListEnvironmentsResponse,
            Awaitable[service.ListEnvironmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_environment(
        self,
    ) -> Callable[
        [service.GetEnvironmentRequest],
        Union[environment.Environment, Awaitable[environment.Environment]],
    ]:
        raise NotImplementedError()

    @property
    def create_environment(
        self,
    ) -> Callable[
        [service.CreateEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_environment(
        self,
    ) -> Callable[
        [service.DeleteEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("NotebookServiceTransport",)
