# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.security.privateca_v1beta1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCertificateAuthorityServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CertificateAuthorityServiceRestInterceptor:
    """Interceptor for CertificateAuthorityService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CertificateAuthorityServiceRestTransport.

    .. code-block:: python
        class MyCustomCertificateAuthorityServiceInterceptor(CertificateAuthorityServiceRestInterceptor):
            def pre_activate_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_activate_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_certificate_authority_csr(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_certificate_authority_csr(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate_revocation_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate_revocation_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_reusable_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_reusable_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificate_authorities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificate_authorities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificate_revocation_lists(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificate_revocation_lists(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_reusable_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_reusable_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_revoke_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_revoke_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_schedule_delete_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_schedule_delete_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate_revocation_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate_revocation_list(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CertificateAuthorityServiceRestTransport(interceptor=MyCustomCertificateAuthorityServiceInterceptor())
        client = CertificateAuthorityServiceClient(transport=transport)


    """

    def pre_activate_certificate_authority(
        self,
        request: service.ActivateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ActivateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for activate_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_activate_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for activate_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_certificate(
        self,
        request: service.CreateCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for create_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_certificate_authority(
        self,
        request: service.CreateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_disable_certificate_authority(
        self,
        request: service.DisableCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DisableCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_disable_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_enable_certificate_authority(
        self,
        request: service.EnableCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.EnableCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_enable_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_certificate_authority_csr(
        self,
        request: service.FetchCertificateAuthorityCsrRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.FetchCertificateAuthorityCsrRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_certificate_authority_csr

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_fetch_certificate_authority_csr(
        self, response: service.FetchCertificateAuthorityCsrResponse
    ) -> service.FetchCertificateAuthorityCsrResponse:
        """Post-rpc interceptor for fetch_certificate_authority_csr

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate(
        self,
        request: service.GetCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for get_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate_authority(
        self,
        request: service.GetCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate_authority(
        self, response: resources.CertificateAuthority
    ) -> resources.CertificateAuthority:
        """Post-rpc interceptor for get_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate_revocation_list(
        self,
        request: service.GetCertificateRevocationListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateRevocationListRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate_revocation_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate_revocation_list(
        self, response: resources.CertificateRevocationList
    ) -> resources.CertificateRevocationList:
        """Post-rpc interceptor for get_certificate_revocation_list

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_reusable_config(
        self,
        request: service.GetReusableConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetReusableConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_reusable_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_reusable_config(
        self, response: resources.ReusableConfig
    ) -> resources.ReusableConfig:
        """Post-rpc interceptor for get_reusable_config

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificate_authorities(
        self,
        request: service.ListCertificateAuthoritiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCertificateAuthoritiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_certificate_authorities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificate_authorities(
        self, response: service.ListCertificateAuthoritiesResponse
    ) -> service.ListCertificateAuthoritiesResponse:
        """Post-rpc interceptor for list_certificate_authorities

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificate_revocation_lists(
        self,
        request: service.ListCertificateRevocationListsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.ListCertificateRevocationListsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_certificate_revocation_lists

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificate_revocation_lists(
        self, response: service.ListCertificateRevocationListsResponse
    ) -> service.ListCertificateRevocationListsResponse:
        """Post-rpc interceptor for list_certificate_revocation_lists

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificates(
        self,
        request: service.ListCertificatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCertificatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_certificates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificates(
        self, response: service.ListCertificatesResponse
    ) -> service.ListCertificatesResponse:
        """Post-rpc interceptor for list_certificates

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_reusable_configs(
        self,
        request: service.ListReusableConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListReusableConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_reusable_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_reusable_configs(
        self, response: service.ListReusableConfigsResponse
    ) -> service.ListReusableConfigsResponse:
        """Post-rpc interceptor for list_reusable_configs

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_restore_certificate_authority(
        self,
        request: service.RestoreCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.RestoreCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for restore_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_restore_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_revoke_certificate(
        self,
        request: service.RevokeCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.RevokeCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for revoke_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_revoke_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for revoke_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_schedule_delete_certificate_authority(
        self,
        request: service.ScheduleDeleteCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.ScheduleDeleteCertificateAuthorityRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for schedule_delete_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_schedule_delete_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for schedule_delete_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate(
        self,
        request: service.UpdateCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for update_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate_authority(
        self,
        request: service.UpdateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate_revocation_list(
        self,
        request: service.UpdateCertificateRevocationListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.UpdateCertificateRevocationListRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_certificate_revocation_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate_revocation_list(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_certificate_revocation_list

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CertificateAuthorityServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CertificateAuthorityServiceRestInterceptor


class CertificateAuthorityServiceRestTransport(
    _BaseCertificateAuthorityServiceRestTransport
):
    """REST backend synchronous transport for CertificateAuthorityService.

    [Certificate Authority
    Service][google.cloud.security.privateca.v1beta1.CertificateAuthorityService]
    manages private certificate authorities and issued certificates.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CertificateAuthorityServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'privateca.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CertificateAuthorityServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _ActivateCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseActivateCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.ActivateCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.ActivateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the activate certificate
            authority method over HTTP.

                Args:
                    request (~.service.ActivateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ActivateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ActivateCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseActivateCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_activate_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseActivateCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseActivateCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseActivateCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ActivateCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_activate_certificate_authority(resp)
            return resp

    class _CreateCertificate(
        _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificate,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.CreateCertificate")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the create certificate method over HTTP.

            Args:
                request (~.service.CreateCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.CreateCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificate._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_certificate(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificate._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._CreateCertificate._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_certificate(resp)
            return resp

    class _CreateCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.CreateCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create certificate
            authority method over HTTP.

                Args:
                    request (~.service.CreateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.CreateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseCreateCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._CreateCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_certificate_authority(resp)
            return resp

    class _DisableCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseDisableCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.DisableCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.DisableCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable certificate
            authority method over HTTP.

                Args:
                    request (~.service.DisableCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.DisableCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.DisableCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseDisableCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_disable_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseDisableCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseDisableCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseDisableCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._DisableCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_disable_certificate_authority(resp)
            return resp

    class _EnableCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseEnableCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.EnableCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.EnableCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable certificate
            authority method over HTTP.

                Args:
                    request (~.service.EnableCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.EnableCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.EnableCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseEnableCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_enable_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseEnableCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseEnableCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseEnableCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._EnableCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enable_certificate_authority(resp)
            return resp

    class _FetchCertificateAuthorityCsr(
        _BaseCertificateAuthorityServiceRestTransport._BaseFetchCertificateAuthorityCsr,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.FetchCertificateAuthorityCsr"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.FetchCertificateAuthorityCsrRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.FetchCertificateAuthorityCsrResponse:
            r"""Call the fetch certificate
            authority csr method over HTTP.

                Args:
                    request (~.service.FetchCertificateAuthorityCsrRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.FetchCertificateAuthorityCsrResponse:
                        Response message for
                    [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseFetchCertificateAuthorityCsr._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_certificate_authority_csr(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseFetchCertificateAuthorityCsr._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseFetchCertificateAuthorityCsr._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._FetchCertificateAuthorityCsr._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.FetchCertificateAuthorityCsrResponse()
            pb_resp = service.FetchCertificateAuthorityCsrResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_certificate_authority_csr(resp)
            return resp

    class _GetCertificate(
        _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificate,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.GetCertificate")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the get certificate method over HTTP.

            Args:
                request (~.service.GetCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificate._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_certificate(request, metadata)
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificate._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                CertificateAuthorityServiceRestTransport._GetCertificate._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate(resp)
            return resp

    class _GetCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.GetCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CertificateAuthority:
            r"""Call the get certificate authority method over HTTP.

            Args:
                request (~.service.GetCertificateAuthorityRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificateAuthority].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CertificateAuthority:
                    A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._GetCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CertificateAuthority()
            pb_resp = resources.CertificateAuthority.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate_authority(resp)
            return resp

    class _GetCertificateRevocationList(
        _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateRevocationList,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.GetCertificateRevocationList"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetCertificateRevocationListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CertificateRevocationList:
            r"""Call the get certificate
            revocation list method over HTTP.

                Args:
                    request (~.service.GetCertificateRevocationListRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.GetCertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificateRevocationList].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.CertificateRevocationList:
                        A
                    [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                    corresponds to a signed X.509 certificate Revocation
                    List (CRL). A CRL contains the serial numbers of
                    certificates that should no longer be trusted.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateRevocationList._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_certificate_revocation_list(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateRevocationList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseGetCertificateRevocationList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._GetCertificateRevocationList._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CertificateRevocationList()
            pb_resp = resources.CertificateRevocationList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate_revocation_list(resp)
            return resp

    class _GetReusableConfig(
        _BaseCertificateAuthorityServiceRestTransport._BaseGetReusableConfig,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.GetReusableConfig")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetReusableConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ReusableConfig:
            r"""Call the get reusable config method over HTTP.

            Args:
                request (~.service.GetReusableConfigRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetReusableConfig][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetReusableConfig].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ReusableConfig:
                    A
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                refers to a managed
                [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
                Those, in turn, are used to describe certain fields of
                an X.509 certificate, such as the key usage fields,
                fields specific to CA certificates, certificate policy
                extensions and custom extensions.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseGetReusableConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_reusable_config(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseGetReusableConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseGetReusableConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._GetReusableConfig._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.ReusableConfig()
            pb_resp = resources.ReusableConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_reusable_config(resp)
            return resp

    class _ListCertificateAuthorities(
        _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateAuthorities,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.ListCertificateAuthorities"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListCertificateAuthoritiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificateAuthoritiesResponse:
            r"""Call the list certificate
            authorities method over HTTP.

                Args:
                    request (~.service.ListCertificateAuthoritiesRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateAuthorities].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListCertificateAuthoritiesResponse:
                        Response message for
                    [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateAuthorities].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateAuthorities._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_certificate_authorities(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateAuthorities._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateAuthorities._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ListCertificateAuthorities._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListCertificateAuthoritiesResponse()
            pb_resp = service.ListCertificateAuthoritiesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificate_authorities(resp)
            return resp

    class _ListCertificateRevocationLists(
        _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateRevocationLists,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.ListCertificateRevocationLists"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListCertificateRevocationListsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificateRevocationListsResponse:
            r"""Call the list certificate
            revocation lists method over HTTP.

                Args:
                    request (~.service.ListCertificateRevocationListsRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateRevocationLists].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListCertificateRevocationListsResponse:
                        Response message for
                    [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateRevocationLists].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateRevocationLists._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_certificate_revocation_lists(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateRevocationLists._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificateRevocationLists._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ListCertificateRevocationLists._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListCertificateRevocationListsResponse()
            pb_resp = service.ListCertificateRevocationListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificate_revocation_lists(resp)
            return resp

    class _ListCertificates(
        _BaseCertificateAuthorityServiceRestTransport._BaseListCertificates,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.ListCertificates")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListCertificatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificatesResponse:
            r"""Call the list certificates method over HTTP.

            Args:
                request (~.service.ListCertificatesRequest):
                    The request object. Request message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificates].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCertificatesResponse:
                    Response message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificates].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseListCertificates._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_certificates(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificates._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseListCertificates._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ListCertificates._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListCertificatesResponse()
            pb_resp = service.ListCertificatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificates(resp)
            return resp

    class _ListReusableConfigs(
        _BaseCertificateAuthorityServiceRestTransport._BaseListReusableConfigs,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.ListReusableConfigs")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListReusableConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListReusableConfigsResponse:
            r"""Call the list reusable configs method over HTTP.

            Args:
                request (~.service.ListReusableConfigsRequest):
                    The request object. Request message for
                [CertificateAuthorityService.ListReusableConfigs][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListReusableConfigs].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListReusableConfigsResponse:
                    Response message for
                [CertificateAuthorityService.ListReusableConfigs][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListReusableConfigs].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseListReusableConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_reusable_configs(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseListReusableConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseListReusableConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ListReusableConfigs._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListReusableConfigsResponse()
            pb_resp = service.ListReusableConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_reusable_configs(resp)
            return resp

    class _RestoreCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseRestoreCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.RestoreCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.RestoreCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore certificate
            authority method over HTTP.

                Args:
                    request (~.service.RestoreCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.RestoreCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.RestoreCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseRestoreCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_restore_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseRestoreCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseRestoreCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseRestoreCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._RestoreCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_certificate_authority(resp)
            return resp

    class _RevokeCertificate(
        _BaseCertificateAuthorityServiceRestTransport._BaseRevokeCertificate,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.RevokeCertificate")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.RevokeCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the revoke certificate method over HTTP.

            Args:
                request (~.service.RevokeCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.RevokeCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.RevokeCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseRevokeCertificate._get_http_options()
            )
            request, metadata = self._interceptor.pre_revoke_certificate(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseRevokeCertificate._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseRevokeCertificate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseRevokeCertificate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._RevokeCertificate._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_revoke_certificate(resp)
            return resp

    class _ScheduleDeleteCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseScheduleDeleteCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.ScheduleDeleteCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.ScheduleDeleteCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the schedule delete
            certificate authority method over HTTP.

                Args:
                    request (~.service.ScheduleDeleteCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ScheduleDeleteCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ScheduleDeleteCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseScheduleDeleteCertificateAuthority._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_schedule_delete_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseScheduleDeleteCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseScheduleDeleteCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseScheduleDeleteCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._ScheduleDeleteCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_schedule_delete_certificate_authority(resp)
            return resp

    class _UpdateCertificate(
        _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificate,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash("CertificateAuthorityServiceRestTransport.UpdateCertificate")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the update certificate method over HTTP.

            Args:
                request (~.service.UpdateCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.UpdateCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificate._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_certificate(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificate._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._UpdateCertificate._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_certificate(resp)
            return resp

    class _UpdateCertificateAuthority(
        _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateAuthority,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.UpdateCertificateAuthority"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update certificate
            authority method over HTTP.

                Args:
                    request (~.service.UpdateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UpdateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificateAuthority].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateAuthority._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateAuthority._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._UpdateCertificateAuthority._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_certificate_authority(resp)
            return resp

    class _UpdateCertificateRevocationList(
        _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateRevocationList,
        CertificateAuthorityServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CertificateAuthorityServiceRestTransport.UpdateCertificateRevocationList"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateCertificateRevocationListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update certificate
            revocation list method over HTTP.

                Args:
                    request (~.service.UpdateCertificateRevocationListRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UpdateCertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificateRevocationList].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateRevocationList._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_certificate_revocation_list(
                request, metadata
            )
            transcoded_request = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateRevocationList._get_transcoded_request(
                http_options, request
            )

            body = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateRevocationList._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCertificateAuthorityServiceRestTransport._BaseUpdateCertificateRevocationList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CertificateAuthorityServiceRestTransport._UpdateCertificateRevocationList._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_certificate_revocation_list(resp)
            return resp

    @property
    def activate_certificate_authority(
        self,
    ) -> Callable[
        [service.ActivateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ActivateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_certificate(
        self,
    ) -> Callable[[service.CreateCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_certificate_authority(
        self,
    ) -> Callable[
        [service.CreateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_certificate_authority(
        self,
    ) -> Callable[
        [service.DisableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_certificate_authority(
        self,
    ) -> Callable[
        [service.EnableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_certificate_authority_csr(
        self,
    ) -> Callable[
        [service.FetchCertificateAuthorityCsrRequest],
        service.FetchCertificateAuthorityCsrResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchCertificateAuthorityCsr(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate(
        self,
    ) -> Callable[[service.GetCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate_authority(
        self,
    ) -> Callable[
        [service.GetCertificateAuthorityRequest], resources.CertificateAuthority
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.GetCertificateRevocationListRequest],
        resources.CertificateRevocationList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificateRevocationList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_reusable_config(
        self,
    ) -> Callable[[service.GetReusableConfigRequest], resources.ReusableConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReusableConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificate_authorities(
        self,
    ) -> Callable[
        [service.ListCertificateAuthoritiesRequest],
        service.ListCertificateAuthoritiesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificateAuthorities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificate_revocation_lists(
        self,
    ) -> Callable[
        [service.ListCertificateRevocationListsRequest],
        service.ListCertificateRevocationListsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificateRevocationLists(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificates(
        self,
    ) -> Callable[[service.ListCertificatesRequest], service.ListCertificatesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_reusable_configs(
        self,
    ) -> Callable[
        [service.ListReusableConfigsRequest], service.ListReusableConfigsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReusableConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_certificate_authority(
        self,
    ) -> Callable[
        [service.RestoreCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def revoke_certificate(
        self,
    ) -> Callable[[service.RevokeCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RevokeCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def schedule_delete_certificate_authority(
        self,
    ) -> Callable[
        [service.ScheduleDeleteCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ScheduleDeleteCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate(
        self,
    ) -> Callable[[service.UpdateCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate_authority(
        self,
    ) -> Callable[
        [service.UpdateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.UpdateCertificateRevocationListRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificateRevocationList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CertificateAuthorityServiceRestTransport",)
