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

from google.cloud.secretmanager_v1beta1.types import resources
from google.cloud.secretmanager_v1beta1.types import service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-secretmanager",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class SecretManagerServiceTransport(abc.ABC):
    """Abstract transport class for SecretManagerService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "secretmanager.googleapis.com",
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
            self.list_secrets: gapic_v1.method.wrap_method(
                self.list_secrets, default_timeout=60.0, client_info=client_info,
            ),
            self.create_secret: gapic_v1.method.wrap_method(
                self.create_secret, default_timeout=60.0, client_info=client_info,
            ),
            self.add_secret_version: gapic_v1.method.wrap_method(
                self.add_secret_version, default_timeout=60.0, client_info=client_info,
            ),
            self.get_secret: gapic_v1.method.wrap_method(
                self.get_secret, default_timeout=60.0, client_info=client_info,
            ),
            self.update_secret: gapic_v1.method.wrap_method(
                self.update_secret, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_secret: gapic_v1.method.wrap_method(
                self.delete_secret, default_timeout=60.0, client_info=client_info,
            ),
            self.list_secret_versions: gapic_v1.method.wrap_method(
                self.list_secret_versions,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_secret_version: gapic_v1.method.wrap_method(
                self.get_secret_version, default_timeout=60.0, client_info=client_info,
            ),
            self.access_secret_version: gapic_v1.method.wrap_method(
                self.access_secret_version,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.disable_secret_version: gapic_v1.method.wrap_method(
                self.disable_secret_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.enable_secret_version: gapic_v1.method.wrap_method(
                self.enable_secret_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.destroy_secret_version: gapic_v1.method.wrap_method(
                self.destroy_secret_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=60.0, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=60.0, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def list_secrets(
        self,
    ) -> typing.Callable[
        [service.ListSecretsRequest],
        typing.Union[
            service.ListSecretsResponse, typing.Awaitable[service.ListSecretsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_secret(
        self,
    ) -> typing.Callable[
        [service.CreateSecretRequest],
        typing.Union[resources.Secret, typing.Awaitable[resources.Secret]],
    ]:
        raise NotImplementedError()

    @property
    def add_secret_version(
        self,
    ) -> typing.Callable[
        [service.AddSecretVersionRequest],
        typing.Union[
            resources.SecretVersion, typing.Awaitable[resources.SecretVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_secret(
        self,
    ) -> typing.Callable[
        [service.GetSecretRequest],
        typing.Union[resources.Secret, typing.Awaitable[resources.Secret]],
    ]:
        raise NotImplementedError()

    @property
    def update_secret(
        self,
    ) -> typing.Callable[
        [service.UpdateSecretRequest],
        typing.Union[resources.Secret, typing.Awaitable[resources.Secret]],
    ]:
        raise NotImplementedError()

    @property
    def delete_secret(
        self,
    ) -> typing.Callable[
        [service.DeleteSecretRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_secret_versions(
        self,
    ) -> typing.Callable[
        [service.ListSecretVersionsRequest],
        typing.Union[
            service.ListSecretVersionsResponse,
            typing.Awaitable[service.ListSecretVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_secret_version(
        self,
    ) -> typing.Callable[
        [service.GetSecretVersionRequest],
        typing.Union[
            resources.SecretVersion, typing.Awaitable[resources.SecretVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def access_secret_version(
        self,
    ) -> typing.Callable[
        [service.AccessSecretVersionRequest],
        typing.Union[
            service.AccessSecretVersionResponse,
            typing.Awaitable[service.AccessSecretVersionResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def disable_secret_version(
        self,
    ) -> typing.Callable[
        [service.DisableSecretVersionRequest],
        typing.Union[
            resources.SecretVersion, typing.Awaitable[resources.SecretVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def enable_secret_version(
        self,
    ) -> typing.Callable[
        [service.EnableSecretVersionRequest],
        typing.Union[
            resources.SecretVersion, typing.Awaitable[resources.SecretVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def destroy_secret_version(
        self,
    ) -> typing.Callable[
        [service.DestroySecretVersionRequest],
        typing.Union[
            resources.SecretVersion, typing.Awaitable[resources.SecretVersion]
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


__all__ = ("SecretManagerServiceTransport",)
