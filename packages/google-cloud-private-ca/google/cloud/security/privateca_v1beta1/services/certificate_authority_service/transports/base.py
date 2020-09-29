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

from google.cloud.security.privateca_v1beta1.types import resources
from google.cloud.security.privateca_v1beta1.types import service
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-security-private-ca",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class CertificateAuthorityServiceTransport(abc.ABC):
    """Abstract transport class for CertificateAuthorityService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "privateca.googleapis.com",
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
            self.create_certificate: gapic_v1.method.wrap_method(
                self.create_certificate, default_timeout=None, client_info=client_info,
            ),
            self.get_certificate: gapic_v1.method.wrap_method(
                self.get_certificate, default_timeout=None, client_info=client_info,
            ),
            self.list_certificates: gapic_v1.method.wrap_method(
                self.list_certificates, default_timeout=None, client_info=client_info,
            ),
            self.revoke_certificate: gapic_v1.method.wrap_method(
                self.revoke_certificate, default_timeout=None, client_info=client_info,
            ),
            self.update_certificate: gapic_v1.method.wrap_method(
                self.update_certificate, default_timeout=None, client_info=client_info,
            ),
            self.activate_certificate_authority: gapic_v1.method.wrap_method(
                self.activate_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_certificate_authority: gapic_v1.method.wrap_method(
                self.create_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.disable_certificate_authority: gapic_v1.method.wrap_method(
                self.disable_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.enable_certificate_authority: gapic_v1.method.wrap_method(
                self.enable_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_certificate_authority_csr: gapic_v1.method.wrap_method(
                self.fetch_certificate_authority_csr,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_certificate_authority: gapic_v1.method.wrap_method(
                self.get_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_certificate_authorities: gapic_v1.method.wrap_method(
                self.list_certificate_authorities,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restore_certificate_authority: gapic_v1.method.wrap_method(
                self.restore_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.schedule_delete_certificate_authority: gapic_v1.method.wrap_method(
                self.schedule_delete_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_certificate_authority: gapic_v1.method.wrap_method(
                self.update_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_certificate_revocation_list: gapic_v1.method.wrap_method(
                self.create_certificate_revocation_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_certificate_revocation_list: gapic_v1.method.wrap_method(
                self.get_certificate_revocation_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_certificate_revocation_lists: gapic_v1.method.wrap_method(
                self.list_certificate_revocation_lists,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_certificate_revocation_list: gapic_v1.method.wrap_method(
                self.update_certificate_revocation_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_reusable_config: gapic_v1.method.wrap_method(
                self.create_reusable_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_reusable_config: gapic_v1.method.wrap_method(
                self.delete_reusable_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_reusable_config: gapic_v1.method.wrap_method(
                self.get_reusable_config, default_timeout=None, client_info=client_info,
            ),
            self.list_reusable_configs: gapic_v1.method.wrap_method(
                self.list_reusable_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_reusable_config: gapic_v1.method.wrap_method(
                self.update_reusable_config,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_certificate(
        self,
    ) -> typing.Callable[
        [service.CreateCertificateRequest],
        typing.Union[resources.Certificate, typing.Awaitable[resources.Certificate]],
    ]:
        raise NotImplementedError()

    @property
    def get_certificate(
        self,
    ) -> typing.Callable[
        [service.GetCertificateRequest],
        typing.Union[resources.Certificate, typing.Awaitable[resources.Certificate]],
    ]:
        raise NotImplementedError()

    @property
    def list_certificates(
        self,
    ) -> typing.Callable[
        [service.ListCertificatesRequest],
        typing.Union[
            service.ListCertificatesResponse,
            typing.Awaitable[service.ListCertificatesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def revoke_certificate(
        self,
    ) -> typing.Callable[
        [service.RevokeCertificateRequest],
        typing.Union[resources.Certificate, typing.Awaitable[resources.Certificate]],
    ]:
        raise NotImplementedError()

    @property
    def update_certificate(
        self,
    ) -> typing.Callable[
        [service.UpdateCertificateRequest],
        typing.Union[resources.Certificate, typing.Awaitable[resources.Certificate]],
    ]:
        raise NotImplementedError()

    @property
    def activate_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.ActivateCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.CreateCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def disable_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.DisableCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def enable_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.EnableCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def fetch_certificate_authority_csr(
        self,
    ) -> typing.Callable[
        [service.FetchCertificateAuthorityCsrRequest],
        typing.Union[
            service.FetchCertificateAuthorityCsrResponse,
            typing.Awaitable[service.FetchCertificateAuthorityCsrResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.GetCertificateAuthorityRequest],
        typing.Union[
            resources.CertificateAuthority,
            typing.Awaitable[resources.CertificateAuthority],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_certificate_authorities(
        self,
    ) -> typing.Callable[
        [service.ListCertificateAuthoritiesRequest],
        typing.Union[
            service.ListCertificateAuthoritiesResponse,
            typing.Awaitable[service.ListCertificateAuthoritiesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def restore_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.RestoreCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def schedule_delete_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.ScheduleDeleteCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_certificate_authority(
        self,
    ) -> typing.Callable[
        [service.UpdateCertificateAuthorityRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_certificate_revocation_list(
        self,
    ) -> typing.Callable[
        [service.CreateCertificateRevocationListRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_certificate_revocation_list(
        self,
    ) -> typing.Callable[
        [service.GetCertificateRevocationListRequest],
        typing.Union[
            resources.CertificateRevocationList,
            typing.Awaitable[resources.CertificateRevocationList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_certificate_revocation_lists(
        self,
    ) -> typing.Callable[
        [service.ListCertificateRevocationListsRequest],
        typing.Union[
            service.ListCertificateRevocationListsResponse,
            typing.Awaitable[service.ListCertificateRevocationListsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_certificate_revocation_list(
        self,
    ) -> typing.Callable[
        [service.UpdateCertificateRevocationListRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_reusable_config(
        self,
    ) -> typing.Callable[
        [service.CreateReusableConfigRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_reusable_config(
        self,
    ) -> typing.Callable[
        [service.DeleteReusableConfigRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_reusable_config(
        self,
    ) -> typing.Callable[
        [service.GetReusableConfigRequest],
        typing.Union[
            resources.ReusableConfig, typing.Awaitable[resources.ReusableConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_reusable_configs(
        self,
    ) -> typing.Callable[
        [service.ListReusableConfigsRequest],
        typing.Union[
            service.ListReusableConfigsResponse,
            typing.Awaitable[service.ListReusableConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_reusable_config(
        self,
    ) -> typing.Callable[
        [service.UpdateReusableConfigRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("CertificateAuthorityServiceTransport",)
