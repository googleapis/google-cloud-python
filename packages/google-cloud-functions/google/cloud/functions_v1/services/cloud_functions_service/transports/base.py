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

from google.cloud.functions_v1.types import functions
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-functions",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class CloudFunctionsServiceTransport(abc.ABC):
    """Abstract transport class for CloudFunctionsService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "cloudfunctions.googleapis.com",
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
            self.list_functions: gapic_v1.method.wrap_method(
                self.list_functions, default_timeout=None, client_info=client_info,
            ),
            self.get_function: gapic_v1.method.wrap_method(
                self.get_function, default_timeout=None, client_info=client_info,
            ),
            self.create_function: gapic_v1.method.wrap_method(
                self.create_function, default_timeout=None, client_info=client_info,
            ),
            self.update_function: gapic_v1.method.wrap_method(
                self.update_function, default_timeout=None, client_info=client_info,
            ),
            self.delete_function: gapic_v1.method.wrap_method(
                self.delete_function, default_timeout=None, client_info=client_info,
            ),
            self.call_function: gapic_v1.method.wrap_method(
                self.call_function, default_timeout=None, client_info=client_info,
            ),
            self.generate_upload_url: gapic_v1.method.wrap_method(
                self.generate_upload_url, default_timeout=None, client_info=client_info,
            ),
            self.generate_download_url: gapic_v1.method.wrap_method(
                self.generate_download_url,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_functions(
        self,
    ) -> typing.Callable[
        [functions.ListFunctionsRequest],
        typing.Union[
            functions.ListFunctionsResponse,
            typing.Awaitable[functions.ListFunctionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_function(
        self,
    ) -> typing.Callable[
        [functions.GetFunctionRequest],
        typing.Union[
            functions.CloudFunction, typing.Awaitable[functions.CloudFunction]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_function(
        self,
    ) -> typing.Callable[
        [functions.CreateFunctionRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_function(
        self,
    ) -> typing.Callable[
        [functions.UpdateFunctionRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_function(
        self,
    ) -> typing.Callable[
        [functions.DeleteFunctionRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def call_function(
        self,
    ) -> typing.Callable[
        [functions.CallFunctionRequest],
        typing.Union[
            functions.CallFunctionResponse,
            typing.Awaitable[functions.CallFunctionResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def generate_upload_url(
        self,
    ) -> typing.Callable[
        [functions.GenerateUploadUrlRequest],
        typing.Union[
            functions.GenerateUploadUrlResponse,
            typing.Awaitable[functions.GenerateUploadUrlResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def generate_download_url(
        self,
    ) -> typing.Callable[
        [functions.GenerateDownloadUrlRequest],
        typing.Union[
            functions.GenerateDownloadUrlResponse,
            typing.Awaitable[functions.GenerateDownloadUrlResponse],
        ],
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
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
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


__all__ = ("CloudFunctionsServiceTransport",)
