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
from google.auth import credentials  # type: ignore

from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-service-directory",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class RegistrationServiceTransport(abc.ABC):
    """Abstract transport class for RegistrationService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "servicedirectory.googleapis.com",
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
            self.create_namespace: gapic_v1.method.wrap_method(
                self.create_namespace, default_timeout=None, client_info=client_info,
            ),
            self.list_namespaces: gapic_v1.method.wrap_method(
                self.list_namespaces, default_timeout=None, client_info=client_info,
            ),
            self.get_namespace: gapic_v1.method.wrap_method(
                self.get_namespace, default_timeout=None, client_info=client_info,
            ),
            self.update_namespace: gapic_v1.method.wrap_method(
                self.update_namespace, default_timeout=None, client_info=client_info,
            ),
            self.delete_namespace: gapic_v1.method.wrap_method(
                self.delete_namespace, default_timeout=None, client_info=client_info,
            ),
            self.create_service: gapic_v1.method.wrap_method(
                self.create_service, default_timeout=None, client_info=client_info,
            ),
            self.list_services: gapic_v1.method.wrap_method(
                self.list_services, default_timeout=None, client_info=client_info,
            ),
            self.get_service: gapic_v1.method.wrap_method(
                self.get_service, default_timeout=None, client_info=client_info,
            ),
            self.update_service: gapic_v1.method.wrap_method(
                self.update_service, default_timeout=None, client_info=client_info,
            ),
            self.delete_service: gapic_v1.method.wrap_method(
                self.delete_service, default_timeout=None, client_info=client_info,
            ),
            self.create_endpoint: gapic_v1.method.wrap_method(
                self.create_endpoint, default_timeout=None, client_info=client_info,
            ),
            self.list_endpoints: gapic_v1.method.wrap_method(
                self.list_endpoints, default_timeout=None, client_info=client_info,
            ),
            self.get_endpoint: gapic_v1.method.wrap_method(
                self.get_endpoint, default_timeout=None, client_info=client_info,
            ),
            self.update_endpoint: gapic_v1.method.wrap_method(
                self.update_endpoint, default_timeout=None, client_info=client_info,
            ),
            self.delete_endpoint: gapic_v1.method.wrap_method(
                self.delete_endpoint, default_timeout=None, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def create_namespace(
        self,
    ) -> typing.Callable[
        [registration_service.CreateNamespaceRequest],
        typing.Union[
            gcs_namespace.Namespace, typing.Awaitable[gcs_namespace.Namespace]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_namespaces(
        self,
    ) -> typing.Callable[
        [registration_service.ListNamespacesRequest],
        typing.Union[
            registration_service.ListNamespacesResponse,
            typing.Awaitable[registration_service.ListNamespacesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_namespace(
        self,
    ) -> typing.Callable[
        [registration_service.GetNamespaceRequest],
        typing.Union[namespace.Namespace, typing.Awaitable[namespace.Namespace]],
    ]:
        raise NotImplementedError()

    @property
    def update_namespace(
        self,
    ) -> typing.Callable[
        [registration_service.UpdateNamespaceRequest],
        typing.Union[
            gcs_namespace.Namespace, typing.Awaitable[gcs_namespace.Namespace]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_namespace(
        self,
    ) -> typing.Callable[
        [registration_service.DeleteNamespaceRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_service(
        self,
    ) -> typing.Callable[
        [registration_service.CreateServiceRequest],
        typing.Union[gcs_service.Service, typing.Awaitable[gcs_service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def list_services(
        self,
    ) -> typing.Callable[
        [registration_service.ListServicesRequest],
        typing.Union[
            registration_service.ListServicesResponse,
            typing.Awaitable[registration_service.ListServicesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service(
        self,
    ) -> typing.Callable[
        [registration_service.GetServiceRequest],
        typing.Union[service.Service, typing.Awaitable[service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def update_service(
        self,
    ) -> typing.Callable[
        [registration_service.UpdateServiceRequest],
        typing.Union[gcs_service.Service, typing.Awaitable[gcs_service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def delete_service(
        self,
    ) -> typing.Callable[
        [registration_service.DeleteServiceRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_endpoint(
        self,
    ) -> typing.Callable[
        [registration_service.CreateEndpointRequest],
        typing.Union[gcs_endpoint.Endpoint, typing.Awaitable[gcs_endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def list_endpoints(
        self,
    ) -> typing.Callable[
        [registration_service.ListEndpointsRequest],
        typing.Union[
            registration_service.ListEndpointsResponse,
            typing.Awaitable[registration_service.ListEndpointsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_endpoint(
        self,
    ) -> typing.Callable[
        [registration_service.GetEndpointRequest],
        typing.Union[endpoint.Endpoint, typing.Awaitable[endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def update_endpoint(
        self,
    ) -> typing.Callable[
        [registration_service.UpdateEndpointRequest],
        typing.Union[gcs_endpoint.Endpoint, typing.Awaitable[gcs_endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def delete_endpoint(
        self,
    ) -> typing.Callable[
        [registration_service.DeleteEndpointRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("RegistrationServiceTransport",)
