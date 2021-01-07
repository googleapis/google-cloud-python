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

from google.cloud.compute_v1.types import compute


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ProjectsTransport(abc.ABC):
    """Abstract transport class for Projects."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
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
            self.disable_xpn_host: gapic_v1.method.wrap_method(
                self.disable_xpn_host, default_timeout=None, client_info=client_info,
            ),
            self.disable_xpn_resource: gapic_v1.method.wrap_method(
                self.disable_xpn_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.enable_xpn_host: gapic_v1.method.wrap_method(
                self.enable_xpn_host, default_timeout=None, client_info=client_info,
            ),
            self.enable_xpn_resource: gapic_v1.method.wrap_method(
                self.enable_xpn_resource, default_timeout=None, client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get, default_timeout=None, client_info=client_info,
            ),
            self.get_xpn_host: gapic_v1.method.wrap_method(
                self.get_xpn_host, default_timeout=None, client_info=client_info,
            ),
            self.get_xpn_resources: gapic_v1.method.wrap_method(
                self.get_xpn_resources, default_timeout=None, client_info=client_info,
            ),
            self.list_xpn_hosts: gapic_v1.method.wrap_method(
                self.list_xpn_hosts, default_timeout=None, client_info=client_info,
            ),
            self.move_disk: gapic_v1.method.wrap_method(
                self.move_disk, default_timeout=None, client_info=client_info,
            ),
            self.move_instance: gapic_v1.method.wrap_method(
                self.move_instance, default_timeout=None, client_info=client_info,
            ),
            self.set_common_instance_metadata: gapic_v1.method.wrap_method(
                self.set_common_instance_metadata,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_default_network_tier: gapic_v1.method.wrap_method(
                self.set_default_network_tier,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_usage_export_bucket: gapic_v1.method.wrap_method(
                self.set_usage_export_bucket,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def disable_xpn_host(
        self,
    ) -> typing.Callable[
        [compute.DisableXpnHostProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def disable_xpn_resource(
        self,
    ) -> typing.Callable[
        [compute.DisableXpnResourceProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def enable_xpn_host(
        self,
    ) -> typing.Callable[
        [compute.EnableXpnHostProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def enable_xpn_resource(
        self,
    ) -> typing.Callable[
        [compute.EnableXpnResourceProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> typing.Callable[
        [compute.GetProjectRequest],
        typing.Union[compute.Project, typing.Awaitable[compute.Project]],
    ]:
        raise NotImplementedError()

    @property
    def get_xpn_host(
        self,
    ) -> typing.Callable[
        [compute.GetXpnHostProjectRequest],
        typing.Union[compute.Project, typing.Awaitable[compute.Project]],
    ]:
        raise NotImplementedError()

    @property
    def get_xpn_resources(
        self,
    ) -> typing.Callable[
        [compute.GetXpnResourcesProjectsRequest],
        typing.Union[
            compute.ProjectsGetXpnResources,
            typing.Awaitable[compute.ProjectsGetXpnResources],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_xpn_hosts(
        self,
    ) -> typing.Callable[
        [compute.ListXpnHostsProjectsRequest],
        typing.Union[compute.XpnHostList, typing.Awaitable[compute.XpnHostList]],
    ]:
        raise NotImplementedError()

    @property
    def move_disk(
        self,
    ) -> typing.Callable[
        [compute.MoveDiskProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def move_instance(
        self,
    ) -> typing.Callable[
        [compute.MoveInstanceProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_common_instance_metadata(
        self,
    ) -> typing.Callable[
        [compute.SetCommonInstanceMetadataProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_default_network_tier(
        self,
    ) -> typing.Callable[
        [compute.SetDefaultNetworkTierProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_usage_export_bucket(
        self,
    ) -> typing.Callable[
        [compute.SetUsageExportBucketProjectRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("ProjectsTransport",)
