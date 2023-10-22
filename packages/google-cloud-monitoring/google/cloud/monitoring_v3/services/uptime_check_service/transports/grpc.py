# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.monitoring_v3.types import uptime
from google.cloud.monitoring_v3.types import uptime_service
from google.protobuf import empty_pb2  # type: ignore
from .base import UptimeCheckServiceTransport, DEFAULT_CLIENT_INFO


class UptimeCheckServiceGrpcTransport(UptimeCheckServiceTransport):
    """gRPC backend transport for UptimeCheckService.

    The UptimeCheckService API is used to manage (list, create, delete,
    edit) Uptime check configurations in the Cloud Monitoring product.
    An Uptime check is a piece of configuration that determines which
    resources and services to monitor for availability. These
    configurations can also be configured interactively by navigating to
    the [Cloud console] (https://console.cloud.google.com), selecting
    the appropriate project, clicking on "Monitoring" on the left-hand
    side to navigate to Cloud Monitoring, and then clicking on "Uptime".

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
        host: str = "monitoring.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
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
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
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

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
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
            self._grpc_channel = type(self).create_channel(
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
        host: str = "monitoring.googleapis.com",
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
    def list_uptime_check_configs(
        self,
    ) -> Callable[
        [uptime_service.ListUptimeCheckConfigsRequest],
        uptime_service.ListUptimeCheckConfigsResponse,
    ]:
        r"""Return a callable for the list uptime check configs method over gRPC.

        Lists the existing valid Uptime check configurations
        for the project (leaving out any invalid
        configurations).

        Returns:
            Callable[[~.ListUptimeCheckConfigsRequest],
                    ~.ListUptimeCheckConfigsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_uptime_check_configs" not in self._stubs:
            self._stubs["list_uptime_check_configs"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/ListUptimeCheckConfigs",
                request_serializer=uptime_service.ListUptimeCheckConfigsRequest.serialize,
                response_deserializer=uptime_service.ListUptimeCheckConfigsResponse.deserialize,
            )
        return self._stubs["list_uptime_check_configs"]

    @property
    def get_uptime_check_config(
        self,
    ) -> Callable[
        [uptime_service.GetUptimeCheckConfigRequest], uptime.UptimeCheckConfig
    ]:
        r"""Return a callable for the get uptime check config method over gRPC.

        Gets a single Uptime check configuration.

        Returns:
            Callable[[~.GetUptimeCheckConfigRequest],
                    ~.UptimeCheckConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_uptime_check_config" not in self._stubs:
            self._stubs["get_uptime_check_config"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/GetUptimeCheckConfig",
                request_serializer=uptime_service.GetUptimeCheckConfigRequest.serialize,
                response_deserializer=uptime.UptimeCheckConfig.deserialize,
            )
        return self._stubs["get_uptime_check_config"]

    @property
    def create_uptime_check_config(
        self,
    ) -> Callable[
        [uptime_service.CreateUptimeCheckConfigRequest], uptime.UptimeCheckConfig
    ]:
        r"""Return a callable for the create uptime check config method over gRPC.

        Creates a new Uptime check configuration.

        Returns:
            Callable[[~.CreateUptimeCheckConfigRequest],
                    ~.UptimeCheckConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_uptime_check_config" not in self._stubs:
            self._stubs["create_uptime_check_config"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/CreateUptimeCheckConfig",
                request_serializer=uptime_service.CreateUptimeCheckConfigRequest.serialize,
                response_deserializer=uptime.UptimeCheckConfig.deserialize,
            )
        return self._stubs["create_uptime_check_config"]

    @property
    def update_uptime_check_config(
        self,
    ) -> Callable[
        [uptime_service.UpdateUptimeCheckConfigRequest], uptime.UptimeCheckConfig
    ]:
        r"""Return a callable for the update uptime check config method over gRPC.

        Updates an Uptime check configuration. You can either replace
        the entire configuration with a new one or replace only certain
        fields in the current configuration by specifying the fields to
        be updated via ``updateMask``. Returns the updated
        configuration.

        Returns:
            Callable[[~.UpdateUptimeCheckConfigRequest],
                    ~.UptimeCheckConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_uptime_check_config" not in self._stubs:
            self._stubs["update_uptime_check_config"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/UpdateUptimeCheckConfig",
                request_serializer=uptime_service.UpdateUptimeCheckConfigRequest.serialize,
                response_deserializer=uptime.UptimeCheckConfig.deserialize,
            )
        return self._stubs["update_uptime_check_config"]

    @property
    def delete_uptime_check_config(
        self,
    ) -> Callable[[uptime_service.DeleteUptimeCheckConfigRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete uptime check config method over gRPC.

        Deletes an Uptime check configuration. Note that this
        method will fail if the Uptime check configuration is
        referenced by an alert policy or other dependent configs
        that would be rendered invalid by the deletion.

        Returns:
            Callable[[~.DeleteUptimeCheckConfigRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_uptime_check_config" not in self._stubs:
            self._stubs["delete_uptime_check_config"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/DeleteUptimeCheckConfig",
                request_serializer=uptime_service.DeleteUptimeCheckConfigRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_uptime_check_config"]

    @property
    def list_uptime_check_ips(
        self,
    ) -> Callable[
        [uptime_service.ListUptimeCheckIpsRequest],
        uptime_service.ListUptimeCheckIpsResponse,
    ]:
        r"""Return a callable for the list uptime check ips method over gRPC.

        Returns the list of IP addresses that checkers run
        from

        Returns:
            Callable[[~.ListUptimeCheckIpsRequest],
                    ~.ListUptimeCheckIpsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_uptime_check_ips" not in self._stubs:
            self._stubs["list_uptime_check_ips"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.UptimeCheckService/ListUptimeCheckIps",
                request_serializer=uptime_service.ListUptimeCheckIpsRequest.serialize,
                response_deserializer=uptime_service.ListUptimeCheckIpsResponse.deserialize,
            )
        return self._stubs["list_uptime_check_ips"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("UptimeCheckServiceGrpcTransport",)
