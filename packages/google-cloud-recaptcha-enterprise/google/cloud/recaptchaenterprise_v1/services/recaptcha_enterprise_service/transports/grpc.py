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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise

from .base import DEFAULT_CLIENT_INFO, RecaptchaEnterpriseServiceTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
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
                    "serviceName": "google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
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
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class RecaptchaEnterpriseServiceGrpcTransport(RecaptchaEnterpriseServiceTransport):
    """gRPC backend transport for RecaptchaEnterpriseService.

    Service to determine the likelihood an event is legitimate.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "recaptchaenterprise.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
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
                 The hostname to connect to (default: 'recaptchaenterprise.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
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

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "recaptchaenterprise.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def create_assessment(
        self,
    ) -> Callable[
        [recaptchaenterprise.CreateAssessmentRequest], recaptchaenterprise.Assessment
    ]:
        r"""Return a callable for the create assessment method over gRPC.

        Creates an Assessment of the likelihood an event is
        legitimate.

        Returns:
            Callable[[~.CreateAssessmentRequest],
                    ~.Assessment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_assessment" not in self._stubs:
            self._stubs["create_assessment"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/CreateAssessment",
                request_serializer=recaptchaenterprise.CreateAssessmentRequest.serialize,
                response_deserializer=recaptchaenterprise.Assessment.deserialize,
            )
        return self._stubs["create_assessment"]

    @property
    def annotate_assessment(
        self,
    ) -> Callable[
        [recaptchaenterprise.AnnotateAssessmentRequest],
        recaptchaenterprise.AnnotateAssessmentResponse,
    ]:
        r"""Return a callable for the annotate assessment method over gRPC.

        Annotates a previously created Assessment to provide
        additional information on whether the event turned out
        to be authentic or fraudulent.

        Returns:
            Callable[[~.AnnotateAssessmentRequest],
                    ~.AnnotateAssessmentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "annotate_assessment" not in self._stubs:
            self._stubs["annotate_assessment"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/AnnotateAssessment",
                request_serializer=recaptchaenterprise.AnnotateAssessmentRequest.serialize,
                response_deserializer=recaptchaenterprise.AnnotateAssessmentResponse.deserialize,
            )
        return self._stubs["annotate_assessment"]

    @property
    def create_key(
        self,
    ) -> Callable[[recaptchaenterprise.CreateKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the create key method over gRPC.

        Creates a new reCAPTCHA Enterprise key.

        Returns:
            Callable[[~.CreateKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_key" not in self._stubs:
            self._stubs["create_key"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/CreateKey",
                request_serializer=recaptchaenterprise.CreateKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["create_key"]

    @property
    def list_keys(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListKeysRequest], recaptchaenterprise.ListKeysResponse
    ]:
        r"""Return a callable for the list keys method over gRPC.

        Returns the list of all keys that belong to a
        project.

        Returns:
            Callable[[~.ListKeysRequest],
                    ~.ListKeysResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_keys" not in self._stubs:
            self._stubs["list_keys"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListKeys",
                request_serializer=recaptchaenterprise.ListKeysRequest.serialize,
                response_deserializer=recaptchaenterprise.ListKeysResponse.deserialize,
            )
        return self._stubs["list_keys"]

    @property
    def retrieve_legacy_secret_key(
        self,
    ) -> Callable[
        [recaptchaenterprise.RetrieveLegacySecretKeyRequest],
        recaptchaenterprise.RetrieveLegacySecretKeyResponse,
    ]:
        r"""Return a callable for the retrieve legacy secret key method over gRPC.

        Returns the secret key related to the specified
        public key. You must use the legacy secret key only in a
        3rd party integration with legacy reCAPTCHA.

        Returns:
            Callable[[~.RetrieveLegacySecretKeyRequest],
                    ~.RetrieveLegacySecretKeyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "retrieve_legacy_secret_key" not in self._stubs:
            self._stubs[
                "retrieve_legacy_secret_key"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/RetrieveLegacySecretKey",
                request_serializer=recaptchaenterprise.RetrieveLegacySecretKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.RetrieveLegacySecretKeyResponse.deserialize,
            )
        return self._stubs["retrieve_legacy_secret_key"]

    @property
    def get_key(
        self,
    ) -> Callable[[recaptchaenterprise.GetKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the get key method over gRPC.

        Returns the specified key.

        Returns:
            Callable[[~.GetKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_key" not in self._stubs:
            self._stubs["get_key"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/GetKey",
                request_serializer=recaptchaenterprise.GetKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["get_key"]

    @property
    def update_key(
        self,
    ) -> Callable[[recaptchaenterprise.UpdateKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the update key method over gRPC.

        Updates the specified key.

        Returns:
            Callable[[~.UpdateKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_key" not in self._stubs:
            self._stubs["update_key"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/UpdateKey",
                request_serializer=recaptchaenterprise.UpdateKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["update_key"]

    @property
    def delete_key(
        self,
    ) -> Callable[[recaptchaenterprise.DeleteKeyRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete key method over gRPC.

        Deletes the specified key.

        Returns:
            Callable[[~.DeleteKeyRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_key" not in self._stubs:
            self._stubs["delete_key"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/DeleteKey",
                request_serializer=recaptchaenterprise.DeleteKeyRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_key"]

    @property
    def migrate_key(
        self,
    ) -> Callable[[recaptchaenterprise.MigrateKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the migrate key method over gRPC.

        Migrates an existing key from reCAPTCHA to reCAPTCHA
        Enterprise. Once a key is migrated, it can be used from
        either product. SiteVerify requests are billed as
        CreateAssessment calls. You must be authenticated as one
        of the current owners of the reCAPTCHA Key, and your
        user must have the reCAPTCHA Enterprise Admin IAM role
        in the destination project.

        Returns:
            Callable[[~.MigrateKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "migrate_key" not in self._stubs:
            self._stubs["migrate_key"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/MigrateKey",
                request_serializer=recaptchaenterprise.MigrateKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["migrate_key"]

    @property
    def add_ip_override(
        self,
    ) -> Callable[
        [recaptchaenterprise.AddIpOverrideRequest],
        recaptchaenterprise.AddIpOverrideResponse,
    ]:
        r"""Return a callable for the add ip override method over gRPC.

        Adds an IP override to a key. The following restrictions hold:

        -  The maximum number of IP overrides per key is 100.
        -  For any conflict (such as IP already exists or IP part of an
           existing IP range), an error is returned.

        Returns:
            Callable[[~.AddIpOverrideRequest],
                    ~.AddIpOverrideResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_ip_override" not in self._stubs:
            self._stubs["add_ip_override"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/AddIpOverride",
                request_serializer=recaptchaenterprise.AddIpOverrideRequest.serialize,
                response_deserializer=recaptchaenterprise.AddIpOverrideResponse.deserialize,
            )
        return self._stubs["add_ip_override"]

    @property
    def remove_ip_override(
        self,
    ) -> Callable[
        [recaptchaenterprise.RemoveIpOverrideRequest],
        recaptchaenterprise.RemoveIpOverrideResponse,
    ]:
        r"""Return a callable for the remove ip override method over gRPC.

        Removes an IP override from a key. The following restrictions
        hold:

        -  If the IP isn't found in an existing IP override, a
           ``NOT_FOUND`` error is returned.
        -  If the IP is found in an existing IP override, but the
           override type does not match, a ``NOT_FOUND`` error is
           returned.

        Returns:
            Callable[[~.RemoveIpOverrideRequest],
                    ~.RemoveIpOverrideResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_ip_override" not in self._stubs:
            self._stubs["remove_ip_override"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/RemoveIpOverride",
                request_serializer=recaptchaenterprise.RemoveIpOverrideRequest.serialize,
                response_deserializer=recaptchaenterprise.RemoveIpOverrideResponse.deserialize,
            )
        return self._stubs["remove_ip_override"]

    @property
    def list_ip_overrides(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListIpOverridesRequest],
        recaptchaenterprise.ListIpOverridesResponse,
    ]:
        r"""Return a callable for the list ip overrides method over gRPC.

        Lists all IP overrides for a key.

        Returns:
            Callable[[~.ListIpOverridesRequest],
                    ~.ListIpOverridesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_ip_overrides" not in self._stubs:
            self._stubs["list_ip_overrides"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListIpOverrides",
                request_serializer=recaptchaenterprise.ListIpOverridesRequest.serialize,
                response_deserializer=recaptchaenterprise.ListIpOverridesResponse.deserialize,
            )
        return self._stubs["list_ip_overrides"]

    @property
    def get_metrics(
        self,
    ) -> Callable[[recaptchaenterprise.GetMetricsRequest], recaptchaenterprise.Metrics]:
        r"""Return a callable for the get metrics method over gRPC.

        Get some aggregated metrics for a Key. This data can
        be used to build dashboards.

        Returns:
            Callable[[~.GetMetricsRequest],
                    ~.Metrics]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_metrics" not in self._stubs:
            self._stubs["get_metrics"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/GetMetrics",
                request_serializer=recaptchaenterprise.GetMetricsRequest.serialize,
                response_deserializer=recaptchaenterprise.Metrics.deserialize,
            )
        return self._stubs["get_metrics"]

    @property
    def create_firewall_policy(
        self,
    ) -> Callable[
        [recaptchaenterprise.CreateFirewallPolicyRequest],
        recaptchaenterprise.FirewallPolicy,
    ]:
        r"""Return a callable for the create firewall policy method over gRPC.

        Creates a new FirewallPolicy, specifying conditions
        at which reCAPTCHA Enterprise actions can be executed. A
        project may have a maximum of 1000 policies.

        Returns:
            Callable[[~.CreateFirewallPolicyRequest],
                    ~.FirewallPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_firewall_policy" not in self._stubs:
            self._stubs["create_firewall_policy"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/CreateFirewallPolicy",
                request_serializer=recaptchaenterprise.CreateFirewallPolicyRequest.serialize,
                response_deserializer=recaptchaenterprise.FirewallPolicy.deserialize,
            )
        return self._stubs["create_firewall_policy"]

    @property
    def list_firewall_policies(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListFirewallPoliciesRequest],
        recaptchaenterprise.ListFirewallPoliciesResponse,
    ]:
        r"""Return a callable for the list firewall policies method over gRPC.

        Returns the list of all firewall policies that belong
        to a project.

        Returns:
            Callable[[~.ListFirewallPoliciesRequest],
                    ~.ListFirewallPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_firewall_policies" not in self._stubs:
            self._stubs["list_firewall_policies"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListFirewallPolicies",
                request_serializer=recaptchaenterprise.ListFirewallPoliciesRequest.serialize,
                response_deserializer=recaptchaenterprise.ListFirewallPoliciesResponse.deserialize,
            )
        return self._stubs["list_firewall_policies"]

    @property
    def get_firewall_policy(
        self,
    ) -> Callable[
        [recaptchaenterprise.GetFirewallPolicyRequest],
        recaptchaenterprise.FirewallPolicy,
    ]:
        r"""Return a callable for the get firewall policy method over gRPC.

        Returns the specified firewall policy.

        Returns:
            Callable[[~.GetFirewallPolicyRequest],
                    ~.FirewallPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_firewall_policy" not in self._stubs:
            self._stubs["get_firewall_policy"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/GetFirewallPolicy",
                request_serializer=recaptchaenterprise.GetFirewallPolicyRequest.serialize,
                response_deserializer=recaptchaenterprise.FirewallPolicy.deserialize,
            )
        return self._stubs["get_firewall_policy"]

    @property
    def update_firewall_policy(
        self,
    ) -> Callable[
        [recaptchaenterprise.UpdateFirewallPolicyRequest],
        recaptchaenterprise.FirewallPolicy,
    ]:
        r"""Return a callable for the update firewall policy method over gRPC.

        Updates the specified firewall policy.

        Returns:
            Callable[[~.UpdateFirewallPolicyRequest],
                    ~.FirewallPolicy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_firewall_policy" not in self._stubs:
            self._stubs["update_firewall_policy"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/UpdateFirewallPolicy",
                request_serializer=recaptchaenterprise.UpdateFirewallPolicyRequest.serialize,
                response_deserializer=recaptchaenterprise.FirewallPolicy.deserialize,
            )
        return self._stubs["update_firewall_policy"]

    @property
    def delete_firewall_policy(
        self,
    ) -> Callable[[recaptchaenterprise.DeleteFirewallPolicyRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete firewall policy method over gRPC.

        Deletes the specified firewall policy.

        Returns:
            Callable[[~.DeleteFirewallPolicyRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_firewall_policy" not in self._stubs:
            self._stubs["delete_firewall_policy"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/DeleteFirewallPolicy",
                request_serializer=recaptchaenterprise.DeleteFirewallPolicyRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_firewall_policy"]

    @property
    def reorder_firewall_policies(
        self,
    ) -> Callable[
        [recaptchaenterprise.ReorderFirewallPoliciesRequest],
        recaptchaenterprise.ReorderFirewallPoliciesResponse,
    ]:
        r"""Return a callable for the reorder firewall policies method over gRPC.

        Reorders all firewall policies.

        Returns:
            Callable[[~.ReorderFirewallPoliciesRequest],
                    ~.ReorderFirewallPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reorder_firewall_policies" not in self._stubs:
            self._stubs["reorder_firewall_policies"] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ReorderFirewallPolicies",
                request_serializer=recaptchaenterprise.ReorderFirewallPoliciesRequest.serialize,
                response_deserializer=recaptchaenterprise.ReorderFirewallPoliciesResponse.deserialize,
            )
        return self._stubs["reorder_firewall_policies"]

    @property
    def list_related_account_groups(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListRelatedAccountGroupsRequest],
        recaptchaenterprise.ListRelatedAccountGroupsResponse,
    ]:
        r"""Return a callable for the list related account groups method over gRPC.

        List groups of related accounts.

        Returns:
            Callable[[~.ListRelatedAccountGroupsRequest],
                    ~.ListRelatedAccountGroupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_related_account_groups" not in self._stubs:
            self._stubs[
                "list_related_account_groups"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListRelatedAccountGroups",
                request_serializer=recaptchaenterprise.ListRelatedAccountGroupsRequest.serialize,
                response_deserializer=recaptchaenterprise.ListRelatedAccountGroupsResponse.deserialize,
            )
        return self._stubs["list_related_account_groups"]

    @property
    def list_related_account_group_memberships(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest],
        recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse,
    ]:
        r"""Return a callable for the list related account group
        memberships method over gRPC.

        Get memberships in a group of related accounts.

        Returns:
            Callable[[~.ListRelatedAccountGroupMembershipsRequest],
                    ~.ListRelatedAccountGroupMembershipsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_related_account_group_memberships" not in self._stubs:
            self._stubs[
                "list_related_account_group_memberships"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListRelatedAccountGroupMemberships",
                request_serializer=recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest.serialize,
                response_deserializer=recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse.deserialize,
            )
        return self._stubs["list_related_account_group_memberships"]

    @property
    def search_related_account_group_memberships(
        self,
    ) -> Callable[
        [recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest],
        recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse,
    ]:
        r"""Return a callable for the search related account group
        memberships method over gRPC.

        Search group memberships related to a given account.

        Returns:
            Callable[[~.SearchRelatedAccountGroupMembershipsRequest],
                    ~.SearchRelatedAccountGroupMembershipsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_related_account_group_memberships" not in self._stubs:
            self._stubs[
                "search_related_account_group_memberships"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/SearchRelatedAccountGroupMemberships",
                request_serializer=recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest.serialize,
                response_deserializer=recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse.deserialize,
            )
        return self._stubs["search_related_account_group_memberships"]

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("RecaptchaEnterpriseServiceGrpcTransport",)
