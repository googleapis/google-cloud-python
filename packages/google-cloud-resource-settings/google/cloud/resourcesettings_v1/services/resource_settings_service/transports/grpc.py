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

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.resourcesettings_v1.types import resource_settings
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import ResourceSettingsServiceTransport, DEFAULT_CLIENT_INFO


class ResourceSettingsServiceGrpcTransport(ResourceSettingsServiceTransport):
    """gRPC backend transport for ResourceSettingsService.

    An interface to interact with resource settings and setting values
    throughout the resource hierarchy.

    Services may surface a number of settings for users to control how
    their resources behave. Setting values applied on a given Cloud
    resource are evaluated hierarchically and inherited by all
    descendants of that resource.

    For all requests, returns a ``google.rpc.Status`` with
    ``google.rpc.Code.PERMISSION_DENIED`` if the IAM check fails or the
    ``parent`` resource is not in a Cloud Organization. For all
    requests, returns a ``google.rpc.Status`` with
    ``google.rpc.Code.INVALID_ARGUMENT`` if the request is malformed.

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
        host: str = "resourcesettings.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
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
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

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
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
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
        host: str = "resourcesettings.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
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
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def list_settings(
        self,
    ) -> Callable[
        [resource_settings.ListSettingsRequest], resource_settings.ListSettingsResponse
    ]:
        r"""Return a callable for the list settings method over gRPC.

        Lists all the settings that are available on the Cloud resource
        ``parent``.

        Returns:
            Callable[[~.ListSettingsRequest],
                    ~.ListSettingsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_settings" not in self._stubs:
            self._stubs["list_settings"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/ListSettings",
                request_serializer=resource_settings.ListSettingsRequest.serialize,
                response_deserializer=resource_settings.ListSettingsResponse.deserialize,
            )
        return self._stubs["list_settings"]

    @property
    def search_setting_values(
        self,
    ) -> Callable[
        [resource_settings.SearchSettingValuesRequest],
        resource_settings.SearchSettingValuesResponse,
    ]:
        r"""Return a callable for the search setting values method over gRPC.

        Searches for all setting values that exist on the resource
        ``parent``. The setting values are not limited to those of a
        particular setting.

        Returns:
            Callable[[~.SearchSettingValuesRequest],
                    ~.SearchSettingValuesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_setting_values" not in self._stubs:
            self._stubs["search_setting_values"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/SearchSettingValues",
                request_serializer=resource_settings.SearchSettingValuesRequest.serialize,
                response_deserializer=resource_settings.SearchSettingValuesResponse.deserialize,
            )
        return self._stubs["search_setting_values"]

    @property
    def get_setting_value(
        self,
    ) -> Callable[
        [resource_settings.GetSettingValueRequest], resource_settings.SettingValue
    ]:
        r"""Return a callable for the get setting value method over gRPC.

        Gets a setting value.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the setting value does not
        exist.

        Returns:
            Callable[[~.GetSettingValueRequest],
                    ~.SettingValue]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_setting_value" not in self._stubs:
            self._stubs["get_setting_value"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/GetSettingValue",
                request_serializer=resource_settings.GetSettingValueRequest.serialize,
                response_deserializer=resource_settings.SettingValue.deserialize,
            )
        return self._stubs["get_setting_value"]

    @property
    def lookup_effective_setting_value(
        self,
    ) -> Callable[
        [resource_settings.LookupEffectiveSettingValueRequest],
        resource_settings.SettingValue,
    ]:
        r"""Return a callable for the lookup effective setting value method over gRPC.

        Computes the effective setting value of a setting at the Cloud
        resource ``parent``. The effective setting value is the
        calculated setting value at a Cloud resource and evaluates to
        one of the following options in the given order (the next option
        is used if the previous one does not exist):

        1. the setting value on the given resource
        2. the setting value on the given resource's nearest ancestor
        3. the setting's default value
        4. an empty setting value, defined as a ``SettingValue`` with
           all fields unset

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the setting does not exist.

        Returns:
            Callable[[~.LookupEffectiveSettingValueRequest],
                    ~.SettingValue]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "lookup_effective_setting_value" not in self._stubs:
            self._stubs[
                "lookup_effective_setting_value"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/LookupEffectiveSettingValue",
                request_serializer=resource_settings.LookupEffectiveSettingValueRequest.serialize,
                response_deserializer=resource_settings.SettingValue.deserialize,
            )
        return self._stubs["lookup_effective_setting_value"]

    @property
    def create_setting_value(
        self,
    ) -> Callable[
        [resource_settings.CreateSettingValueRequest], resource_settings.SettingValue
    ]:
        r"""Return a callable for the create setting value method over gRPC.

        Creates a setting value.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the setting does not exist.
        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ALREADY_EXISTS`` if the setting value already
        exists on the given Cloud resource. Returns a
        ``google.rpc.Status`` with
        ``google.rpc.Code.FAILED_PRECONDITION`` if the setting is
        flagged as read only.

        Returns:
            Callable[[~.CreateSettingValueRequest],
                    ~.SettingValue]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_setting_value" not in self._stubs:
            self._stubs["create_setting_value"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/CreateSettingValue",
                request_serializer=resource_settings.CreateSettingValueRequest.serialize,
                response_deserializer=resource_settings.SettingValue.deserialize,
            )
        return self._stubs["create_setting_value"]

    @property
    def update_setting_value(
        self,
    ) -> Callable[
        [resource_settings.UpdateSettingValueRequest], resource_settings.SettingValue
    ]:
        r"""Return a callable for the update setting value method over gRPC.

        Updates a setting value.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the setting or the setting
        value does not exist. Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.FAILED_PRECONDITION`` if the setting is
        flagged as read only. Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ABORTED`` if the etag supplied in the request
        does not match the persisted etag of the setting value.

        Note: the supplied setting value will perform a full overwrite
        of all fields.

        Returns:
            Callable[[~.UpdateSettingValueRequest],
                    ~.SettingValue]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_setting_value" not in self._stubs:
            self._stubs["update_setting_value"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/UpdateSettingValue",
                request_serializer=resource_settings.UpdateSettingValueRequest.serialize,
                response_deserializer=resource_settings.SettingValue.deserialize,
            )
        return self._stubs["update_setting_value"]

    @property
    def delete_setting_value(
        self,
    ) -> Callable[[resource_settings.DeleteSettingValueRequest], empty.Empty]:
        r"""Return a callable for the delete setting value method over gRPC.

        Deletes a setting value. If the setting value does not exist,
        the operation is a no-op.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the setting or the setting
        value does not exist. The setting value will not exist if a
        prior call to ``DeleteSettingValue`` for the setting value
        already returned a success code. Returns a ``google.rpc.Status``
        with ``google.rpc.Code.FAILED_PRECONDITION`` if the setting is
        flagged as read only.

        Returns:
            Callable[[~.DeleteSettingValueRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_setting_value" not in self._stubs:
            self._stubs["delete_setting_value"] = self.grpc_channel.unary_unary(
                "/google.cloud.resourcesettings.v1.ResourceSettingsService/DeleteSettingValue",
                request_serializer=resource_settings.DeleteSettingValueRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_setting_value"]


__all__ = ("ResourceSettingsServiceGrpcTransport",)
