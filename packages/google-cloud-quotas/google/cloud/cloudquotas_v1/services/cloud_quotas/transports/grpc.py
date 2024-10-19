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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import grpc  # type: ignore

from google.cloud.cloudquotas_v1.types import cloudquotas, resources

from .base import DEFAULT_CLIENT_INFO, CloudQuotasTransport


class CloudQuotasGrpcTransport(CloudQuotasTransport):
    """gRPC backend transport for CloudQuotas.

    The Cloud Quotas API is an infrastructure service for Google
    Cloud that lets service consumers list and manage their resource
    usage limits.

    - List/Get the metadata and current status of the quotas for a
      service.
    - Create/Update quota preferencess that declare the preferred
      quota values.
    - Check the status of a quota preference request.
    - List/Get pending and historical quota preference.

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
        host: str = "cloudquotas.googleapis.com",
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
                 The hostname to connect to (default: 'cloudquotas.googleapis.com').
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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudquotas.googleapis.com",
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
    def list_quota_infos(
        self,
    ) -> Callable[
        [cloudquotas.ListQuotaInfosRequest], cloudquotas.ListQuotaInfosResponse
    ]:
        r"""Return a callable for the list quota infos method over gRPC.

        Lists QuotaInfos of all quotas for a given project,
        folder or organization.

        Returns:
            Callable[[~.ListQuotaInfosRequest],
                    ~.ListQuotaInfosResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_quota_infos" not in self._stubs:
            self._stubs["list_quota_infos"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/ListQuotaInfos",
                request_serializer=cloudquotas.ListQuotaInfosRequest.serialize,
                response_deserializer=cloudquotas.ListQuotaInfosResponse.deserialize,
            )
        return self._stubs["list_quota_infos"]

    @property
    def get_quota_info(
        self,
    ) -> Callable[[cloudquotas.GetQuotaInfoRequest], resources.QuotaInfo]:
        r"""Return a callable for the get quota info method over gRPC.

        Retrieve the QuotaInfo of a quota for a project,
        folder or organization.

        Returns:
            Callable[[~.GetQuotaInfoRequest],
                    ~.QuotaInfo]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_quota_info" not in self._stubs:
            self._stubs["get_quota_info"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/GetQuotaInfo",
                request_serializer=cloudquotas.GetQuotaInfoRequest.serialize,
                response_deserializer=resources.QuotaInfo.deserialize,
            )
        return self._stubs["get_quota_info"]

    @property
    def list_quota_preferences(
        self,
    ) -> Callable[
        [cloudquotas.ListQuotaPreferencesRequest],
        cloudquotas.ListQuotaPreferencesResponse,
    ]:
        r"""Return a callable for the list quota preferences method over gRPC.

        Lists QuotaPreferences in a given project, folder or
        organization.

        Returns:
            Callable[[~.ListQuotaPreferencesRequest],
                    ~.ListQuotaPreferencesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_quota_preferences" not in self._stubs:
            self._stubs["list_quota_preferences"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/ListQuotaPreferences",
                request_serializer=cloudquotas.ListQuotaPreferencesRequest.serialize,
                response_deserializer=cloudquotas.ListQuotaPreferencesResponse.deserialize,
            )
        return self._stubs["list_quota_preferences"]

    @property
    def get_quota_preference(
        self,
    ) -> Callable[[cloudquotas.GetQuotaPreferenceRequest], resources.QuotaPreference]:
        r"""Return a callable for the get quota preference method over gRPC.

        Gets details of a single QuotaPreference.

        Returns:
            Callable[[~.GetQuotaPreferenceRequest],
                    ~.QuotaPreference]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_quota_preference" not in self._stubs:
            self._stubs["get_quota_preference"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/GetQuotaPreference",
                request_serializer=cloudquotas.GetQuotaPreferenceRequest.serialize,
                response_deserializer=resources.QuotaPreference.deserialize,
            )
        return self._stubs["get_quota_preference"]

    @property
    def create_quota_preference(
        self,
    ) -> Callable[
        [cloudquotas.CreateQuotaPreferenceRequest], resources.QuotaPreference
    ]:
        r"""Return a callable for the create quota preference method over gRPC.

        Creates a new QuotaPreference that declares the
        desired value for a quota.

        Returns:
            Callable[[~.CreateQuotaPreferenceRequest],
                    ~.QuotaPreference]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_quota_preference" not in self._stubs:
            self._stubs["create_quota_preference"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/CreateQuotaPreference",
                request_serializer=cloudquotas.CreateQuotaPreferenceRequest.serialize,
                response_deserializer=resources.QuotaPreference.deserialize,
            )
        return self._stubs["create_quota_preference"]

    @property
    def update_quota_preference(
        self,
    ) -> Callable[
        [cloudquotas.UpdateQuotaPreferenceRequest], resources.QuotaPreference
    ]:
        r"""Return a callable for the update quota preference method over gRPC.

        Updates the parameters of a single QuotaPreference.
        It can updates the config in any states, not just the
        ones pending approval.

        Returns:
            Callable[[~.UpdateQuotaPreferenceRequest],
                    ~.QuotaPreference]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_quota_preference" not in self._stubs:
            self._stubs["update_quota_preference"] = self.grpc_channel.unary_unary(
                "/google.api.cloudquotas.v1.CloudQuotas/UpdateQuotaPreference",
                request_serializer=cloudquotas.UpdateQuotaPreferenceRequest.serialize,
                response_deserializer=resources.QuotaPreference.deserialize,
            )
        return self._stubs["update_quota_preference"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("CloudQuotasGrpcTransport",)
