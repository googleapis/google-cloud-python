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

from google.cloud.networkconnectivity_v1alpha1.types import hub
from google.cloud.networkconnectivity_v1alpha1.types import hub as gcn_hub
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-network-connectivity",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class HubServiceTransport(abc.ABC):
    """Abstract transport class for HubService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "networkconnectivity.googleapis.com",
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
            self.list_hubs: gapic_v1.method.wrap_method(
                self.list_hubs, default_timeout=None, client_info=client_info,
            ),
            self.get_hub: gapic_v1.method.wrap_method(
                self.get_hub, default_timeout=None, client_info=client_info,
            ),
            self.create_hub: gapic_v1.method.wrap_method(
                self.create_hub, default_timeout=60.0, client_info=client_info,
            ),
            self.update_hub: gapic_v1.method.wrap_method(
                self.update_hub, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_hub: gapic_v1.method.wrap_method(
                self.delete_hub, default_timeout=60.0, client_info=client_info,
            ),
            self.list_spokes: gapic_v1.method.wrap_method(
                self.list_spokes, default_timeout=None, client_info=client_info,
            ),
            self.get_spoke: gapic_v1.method.wrap_method(
                self.get_spoke, default_timeout=None, client_info=client_info,
            ),
            self.create_spoke: gapic_v1.method.wrap_method(
                self.create_spoke, default_timeout=60.0, client_info=client_info,
            ),
            self.update_spoke: gapic_v1.method.wrap_method(
                self.update_spoke, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_spoke: gapic_v1.method.wrap_method(
                self.delete_spoke, default_timeout=60.0, client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_hubs(
        self,
    ) -> typing.Callable[
        [hub.ListHubsRequest],
        typing.Union[hub.ListHubsResponse, typing.Awaitable[hub.ListHubsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_hub(
        self,
    ) -> typing.Callable[
        [hub.GetHubRequest], typing.Union[hub.Hub, typing.Awaitable[hub.Hub]]
    ]:
        raise NotImplementedError()

    @property
    def create_hub(
        self,
    ) -> typing.Callable[
        [gcn_hub.CreateHubRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_hub(
        self,
    ) -> typing.Callable[
        [gcn_hub.UpdateHubRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_hub(
        self,
    ) -> typing.Callable[
        [hub.DeleteHubRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_spokes(
        self,
    ) -> typing.Callable[
        [hub.ListSpokesRequest],
        typing.Union[hub.ListSpokesResponse, typing.Awaitable[hub.ListSpokesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_spoke(
        self,
    ) -> typing.Callable[
        [hub.GetSpokeRequest], typing.Union[hub.Spoke, typing.Awaitable[hub.Spoke]]
    ]:
        raise NotImplementedError()

    @property
    def create_spoke(
        self,
    ) -> typing.Callable[
        [hub.CreateSpokeRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_spoke(
        self,
    ) -> typing.Callable[
        [hub.UpdateSpokeRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_spoke(
        self,
    ) -> typing.Callable[
        [hub.DeleteSpokeRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("HubServiceTransport",)
