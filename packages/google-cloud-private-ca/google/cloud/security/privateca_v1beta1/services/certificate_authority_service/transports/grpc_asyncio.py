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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.security.privateca_v1beta1.types import resources, service

from .base import DEFAULT_CLIENT_INFO, CertificateAuthorityServiceTransport
from .grpc import CertificateAuthorityServiceGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.security.privateca.v1beta1.CertificateAuthorityService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.security.privateca.v1beta1.CertificateAuthorityService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class CertificateAuthorityServiceGrpcAsyncIOTransport(
    CertificateAuthorityServiceTransport
):
    """gRPC AsyncIO backend transport for CertificateAuthorityService.

    [Certificate Authority
    Service][google.cloud.security.privateca.v1beta1.CertificateAuthorityService]
    manages private certificate authorities and issued certificates.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_certificate(
        self,
    ) -> Callable[[service.CreateCertificateRequest], Awaitable[resources.Certificate]]:
        r"""Return a callable for the create certificate method over gRPC.

        Create a new
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
        in a given Project, Location from a particular
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.CreateCertificateRequest],
                    Awaitable[~.Certificate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_certificate" not in self._stubs:
            self._stubs["create_certificate"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/CreateCertificate",
                request_serializer=service.CreateCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["create_certificate"]

    @property
    def get_certificate(
        self,
    ) -> Callable[[service.GetCertificateRequest], Awaitable[resources.Certificate]]:
        r"""Return a callable for the get certificate method over gRPC.

        Returns a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.GetCertificateRequest],
                    Awaitable[~.Certificate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate" not in self._stubs:
            self._stubs["get_certificate"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificate",
                request_serializer=service.GetCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["get_certificate"]

    @property
    def list_certificates(
        self,
    ) -> Callable[
        [service.ListCertificatesRequest], Awaitable[service.ListCertificatesResponse]
    ]:
        r"""Return a callable for the list certificates method over gRPC.

        Lists
        [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.ListCertificatesRequest],
                    Awaitable[~.ListCertificatesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificates" not in self._stubs:
            self._stubs["list_certificates"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificates",
                request_serializer=service.ListCertificatesRequest.serialize,
                response_deserializer=service.ListCertificatesResponse.deserialize,
            )
        return self._stubs["list_certificates"]

    @property
    def revoke_certificate(
        self,
    ) -> Callable[[service.RevokeCertificateRequest], Awaitable[resources.Certificate]]:
        r"""Return a callable for the revoke certificate method over gRPC.

        Revoke a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.RevokeCertificateRequest],
                    Awaitable[~.Certificate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "revoke_certificate" not in self._stubs:
            self._stubs["revoke_certificate"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/RevokeCertificate",
                request_serializer=service.RevokeCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["revoke_certificate"]

    @property
    def update_certificate(
        self,
    ) -> Callable[[service.UpdateCertificateRequest], Awaitable[resources.Certificate]]:
        r"""Return a callable for the update certificate method over gRPC.

        Update a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].
        Currently, the only field you can update is the
        [labels][google.cloud.security.privateca.v1beta1.Certificate.labels]
        field.

        Returns:
            Callable[[~.UpdateCertificateRequest],
                    Awaitable[~.Certificate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate" not in self._stubs:
            self._stubs["update_certificate"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificate",
                request_serializer=service.UpdateCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["update_certificate"]

    @property
    def activate_certificate_authority(
        self,
    ) -> Callable[
        [service.ActivateCertificateAuthorityRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the activate certificate authority method over gRPC.

        Activate a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        After the parent Certificate Authority signs a certificate
        signing request from
        [FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr],
        this method can complete the activation process.

        Returns:
            Callable[[~.ActivateCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "activate_certificate_authority" not in self._stubs:
            self._stubs[
                "activate_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ActivateCertificateAuthority",
                request_serializer=service.ActivateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["activate_certificate_authority"]

    @property
    def create_certificate_authority(
        self,
    ) -> Callable[
        [service.CreateCertificateAuthorityRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create certificate authority method over gRPC.

        Create a new
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        in a given Project and Location.

        Returns:
            Callable[[~.CreateCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_certificate_authority" not in self._stubs:
            self._stubs[
                "create_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/CreateCertificateAuthority",
                request_serializer=service.CreateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_certificate_authority"]

    @property
    def disable_certificate_authority(
        self,
    ) -> Callable[
        [service.DisableCertificateAuthorityRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the disable certificate authority method over gRPC.

        Disable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.DisableCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_certificate_authority" not in self._stubs:
            self._stubs[
                "disable_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/DisableCertificateAuthority",
                request_serializer=service.DisableCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["disable_certificate_authority"]

    @property
    def enable_certificate_authority(
        self,
    ) -> Callable[
        [service.EnableCertificateAuthorityRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the enable certificate authority method over gRPC.

        Enable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.EnableCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_certificate_authority" not in self._stubs:
            self._stubs[
                "enable_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/EnableCertificateAuthority",
                request_serializer=service.EnableCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["enable_certificate_authority"]

    @property
    def fetch_certificate_authority_csr(
        self,
    ) -> Callable[
        [service.FetchCertificateAuthorityCsrRequest],
        Awaitable[service.FetchCertificateAuthorityCsrResponse],
    ]:
        r"""Return a callable for the fetch certificate authority
        csr method over gRPC.

        Fetch a certificate signing request (CSR) from a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        The CSR must then be signed by the desired parent Certificate
        Authority, which could be another
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        resource, or could be an on-prem certificate authority. See also
        [ActivateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ActivateCertificateAuthority].

        Returns:
            Callable[[~.FetchCertificateAuthorityCsrRequest],
                    Awaitable[~.FetchCertificateAuthorityCsrResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_certificate_authority_csr" not in self._stubs:
            self._stubs[
                "fetch_certificate_authority_csr"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/FetchCertificateAuthorityCsr",
                request_serializer=service.FetchCertificateAuthorityCsrRequest.serialize,
                response_deserializer=service.FetchCertificateAuthorityCsrResponse.deserialize,
            )
        return self._stubs["fetch_certificate_authority_csr"]

    @property
    def get_certificate_authority(
        self,
    ) -> Callable[
        [service.GetCertificateAuthorityRequest],
        Awaitable[resources.CertificateAuthority],
    ]:
        r"""Return a callable for the get certificate authority method over gRPC.

        Returns a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.GetCertificateAuthorityRequest],
                    Awaitable[~.CertificateAuthority]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate_authority" not in self._stubs:
            self._stubs["get_certificate_authority"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificateAuthority",
                request_serializer=service.GetCertificateAuthorityRequest.serialize,
                response_deserializer=resources.CertificateAuthority.deserialize,
            )
        return self._stubs["get_certificate_authority"]

    @property
    def list_certificate_authorities(
        self,
    ) -> Callable[
        [service.ListCertificateAuthoritiesRequest],
        Awaitable[service.ListCertificateAuthoritiesResponse],
    ]:
        r"""Return a callable for the list certificate authorities method over gRPC.

        Lists
        [CertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.ListCertificateAuthoritiesRequest],
                    Awaitable[~.ListCertificateAuthoritiesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificate_authorities" not in self._stubs:
            self._stubs[
                "list_certificate_authorities"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificateAuthorities",
                request_serializer=service.ListCertificateAuthoritiesRequest.serialize,
                response_deserializer=service.ListCertificateAuthoritiesResponse.deserialize,
            )
        return self._stubs["list_certificate_authorities"]

    @property
    def restore_certificate_authority(
        self,
    ) -> Callable[
        [service.RestoreCertificateAuthorityRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the restore certificate authority method over gRPC.

        Restore a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is scheduled for deletion.

        Returns:
            Callable[[~.RestoreCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_certificate_authority" not in self._stubs:
            self._stubs[
                "restore_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/RestoreCertificateAuthority",
                request_serializer=service.RestoreCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_certificate_authority"]

    @property
    def schedule_delete_certificate_authority(
        self,
    ) -> Callable[
        [service.ScheduleDeleteCertificateAuthorityRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the schedule delete certificate
        authority method over gRPC.

        Schedule a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        for deletion.

        Returns:
            Callable[[~.ScheduleDeleteCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "schedule_delete_certificate_authority" not in self._stubs:
            self._stubs[
                "schedule_delete_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ScheduleDeleteCertificateAuthority",
                request_serializer=service.ScheduleDeleteCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["schedule_delete_certificate_authority"]

    @property
    def update_certificate_authority(
        self,
    ) -> Callable[
        [service.UpdateCertificateAuthorityRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update certificate authority method over gRPC.

        Update a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.UpdateCertificateAuthorityRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate_authority" not in self._stubs:
            self._stubs[
                "update_certificate_authority"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificateAuthority",
                request_serializer=service.UpdateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_certificate_authority"]

    @property
    def get_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.GetCertificateRevocationListRequest],
        Awaitable[resources.CertificateRevocationList],
    ]:
        r"""Return a callable for the get certificate revocation
        list method over gRPC.

        Returns a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.GetCertificateRevocationListRequest],
                    Awaitable[~.CertificateRevocationList]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate_revocation_list" not in self._stubs:
            self._stubs[
                "get_certificate_revocation_list"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificateRevocationList",
                request_serializer=service.GetCertificateRevocationListRequest.serialize,
                response_deserializer=resources.CertificateRevocationList.deserialize,
            )
        return self._stubs["get_certificate_revocation_list"]

    @property
    def list_certificate_revocation_lists(
        self,
    ) -> Callable[
        [service.ListCertificateRevocationListsRequest],
        Awaitable[service.ListCertificateRevocationListsResponse],
    ]:
        r"""Return a callable for the list certificate revocation
        lists method over gRPC.

        Lists
        [CertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.ListCertificateRevocationListsRequest],
                    Awaitable[~.ListCertificateRevocationListsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificate_revocation_lists" not in self._stubs:
            self._stubs[
                "list_certificate_revocation_lists"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificateRevocationLists",
                request_serializer=service.ListCertificateRevocationListsRequest.serialize,
                response_deserializer=service.ListCertificateRevocationListsResponse.deserialize,
            )
        return self._stubs["list_certificate_revocation_lists"]

    @property
    def update_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.UpdateCertificateRevocationListRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update certificate revocation
        list method over gRPC.

        Update a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.UpdateCertificateRevocationListRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate_revocation_list" not in self._stubs:
            self._stubs[
                "update_certificate_revocation_list"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificateRevocationList",
                request_serializer=service.UpdateCertificateRevocationListRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_certificate_revocation_list"]

    @property
    def get_reusable_config(
        self,
    ) -> Callable[
        [service.GetReusableConfigRequest], Awaitable[resources.ReusableConfig]
    ]:
        r"""Return a callable for the get reusable config method over gRPC.

        Returns a
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Returns:
            Callable[[~.GetReusableConfigRequest],
                    Awaitable[~.ReusableConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_reusable_config" not in self._stubs:
            self._stubs["get_reusable_config"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetReusableConfig",
                request_serializer=service.GetReusableConfigRequest.serialize,
                response_deserializer=resources.ReusableConfig.deserialize,
            )
        return self._stubs["get_reusable_config"]

    @property
    def list_reusable_configs(
        self,
    ) -> Callable[
        [service.ListReusableConfigsRequest],
        Awaitable[service.ListReusableConfigsResponse],
    ]:
        r"""Return a callable for the list reusable configs method over gRPC.

        Lists
        [ReusableConfigs][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Returns:
            Callable[[~.ListReusableConfigsRequest],
                    Awaitable[~.ListReusableConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_reusable_configs" not in self._stubs:
            self._stubs["list_reusable_configs"] = self._logged_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListReusableConfigs",
                request_serializer=service.ListReusableConfigsRequest.serialize,
                response_deserializer=service.ListReusableConfigsResponse.deserialize,
            )
        return self._stubs["list_reusable_configs"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_certificate: self._wrap_method(
                self.create_certificate,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_certificate: self._wrap_method(
                self.get_certificate,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_certificates: self._wrap_method(
                self.list_certificates,
                default_timeout=None,
                client_info=client_info,
            ),
            self.revoke_certificate: self._wrap_method(
                self.revoke_certificate,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_certificate: self._wrap_method(
                self.update_certificate,
                default_timeout=None,
                client_info=client_info,
            ),
            self.activate_certificate_authority: self._wrap_method(
                self.activate_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_certificate_authority: self._wrap_method(
                self.create_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.disable_certificate_authority: self._wrap_method(
                self.disable_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.enable_certificate_authority: self._wrap_method(
                self.enable_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_certificate_authority_csr: self._wrap_method(
                self.fetch_certificate_authority_csr,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_certificate_authority: self._wrap_method(
                self.get_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_certificate_authorities: self._wrap_method(
                self.list_certificate_authorities,
                default_timeout=None,
                client_info=client_info,
            ),
            self.restore_certificate_authority: self._wrap_method(
                self.restore_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.schedule_delete_certificate_authority: self._wrap_method(
                self.schedule_delete_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_certificate_authority: self._wrap_method(
                self.update_certificate_authority,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_certificate_revocation_list: self._wrap_method(
                self.get_certificate_revocation_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_certificate_revocation_lists: self._wrap_method(
                self.list_certificate_revocation_lists,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_certificate_revocation_list: self._wrap_method(
                self.update_certificate_revocation_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_reusable_config: self._wrap_method(
                self.get_reusable_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_reusable_configs: self._wrap_method(
                self.list_reusable_configs,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("CertificateAuthorityServiceGrpcAsyncIOTransport",)
