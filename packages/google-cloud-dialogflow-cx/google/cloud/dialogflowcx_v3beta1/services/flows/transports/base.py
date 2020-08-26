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

from google.cloud.dialogflowcx_v3beta1.types import flow
from google.cloud.dialogflowcx_v3beta1.types import flow as gcdc_flow
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class FlowsTransport(abc.ABC):
    """Abstract transport class for Flows."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/dialogflow",
    )

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
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
            self.create_flow: gapic_v1.method.wrap_method(
                self.create_flow, default_timeout=None, client_info=client_info,
            ),
            self.delete_flow: gapic_v1.method.wrap_method(
                self.delete_flow, default_timeout=None, client_info=client_info,
            ),
            self.list_flows: gapic_v1.method.wrap_method(
                self.list_flows, default_timeout=None, client_info=client_info,
            ),
            self.get_flow: gapic_v1.method.wrap_method(
                self.get_flow, default_timeout=None, client_info=client_info,
            ),
            self.update_flow: gapic_v1.method.wrap_method(
                self.update_flow, default_timeout=None, client_info=client_info,
            ),
            self.train_flow: gapic_v1.method.wrap_method(
                self.train_flow, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_flow(
        self,
    ) -> typing.Callable[
        [gcdc_flow.CreateFlowRequest],
        typing.Union[gcdc_flow.Flow, typing.Awaitable[gcdc_flow.Flow]],
    ]:
        raise NotImplementedError()

    @property
    def delete_flow(
        self,
    ) -> typing.Callable[
        [flow.DeleteFlowRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_flows(
        self,
    ) -> typing.Callable[
        [flow.ListFlowsRequest],
        typing.Union[flow.ListFlowsResponse, typing.Awaitable[flow.ListFlowsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_flow(
        self,
    ) -> typing.Callable[
        [flow.GetFlowRequest], typing.Union[flow.Flow, typing.Awaitable[flow.Flow]]
    ]:
        raise NotImplementedError()

    @property
    def update_flow(
        self,
    ) -> typing.Callable[
        [gcdc_flow.UpdateFlowRequest],
        typing.Union[gcdc_flow.Flow, typing.Awaitable[gcdc_flow.Flow]],
    ]:
        raise NotImplementedError()

    @property
    def train_flow(
        self,
    ) -> typing.Callable[
        [flow.TrainFlowRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("FlowsTransport",)
