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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.analytics.admin_v1alpha.types import channel_group as gaa_channel_group
from google.analytics.admin_v1alpha.types import (
    expanded_data_set as gaa_expanded_data_set,
)
from google.analytics.admin_v1alpha.types import (
    subproperty_event_filter as gaa_subproperty_event_filter,
)
from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import audience
from google.analytics.admin_v1alpha.types import audience as gaa_audience
from google.analytics.admin_v1alpha.types import channel_group
from google.analytics.admin_v1alpha.types import event_create_and_edit
from google.analytics.admin_v1alpha.types import expanded_data_set
from google.analytics.admin_v1alpha.types import resources
from google.analytics.admin_v1alpha.types import subproperty_event_filter

from .base import DEFAULT_CLIENT_INFO, AnalyticsAdminServiceTransport
from .grpc import AnalyticsAdminServiceGrpcTransport


class AnalyticsAdminServiceGrpcAsyncIOTransport(AnalyticsAdminServiceTransport):
    """gRPC AsyncIO backend transport for AnalyticsAdminService.

    Service Interface for the Analytics Admin API (GA4).

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
        host: str = "analyticsadmin.googleapis.com",
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
        host: str = "analyticsadmin.googleapis.com",
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
                 The hostname to connect to (default: 'analyticsadmin.googleapis.com').
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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def get_account(
        self,
    ) -> Callable[[analytics_admin.GetAccountRequest], Awaitable[resources.Account]]:
        r"""Return a callable for the get account method over gRPC.

        Lookup for a single Account.

        Returns:
            Callable[[~.GetAccountRequest],
                    Awaitable[~.Account]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_account" not in self._stubs:
            self._stubs["get_account"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetAccount",
                request_serializer=analytics_admin.GetAccountRequest.serialize,
                response_deserializer=resources.Account.deserialize,
            )
        return self._stubs["get_account"]

    @property
    def list_accounts(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountsRequest],
        Awaitable[analytics_admin.ListAccountsResponse],
    ]:
        r"""Return a callable for the list accounts method over gRPC.

        Returns all accounts accessible by the caller.

        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        Returns:
            Callable[[~.ListAccountsRequest],
                    Awaitable[~.ListAccountsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_accounts" not in self._stubs:
            self._stubs["list_accounts"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListAccounts",
                request_serializer=analytics_admin.ListAccountsRequest.serialize,
                response_deserializer=analytics_admin.ListAccountsResponse.deserialize,
            )
        return self._stubs["list_accounts"]

    @property
    def delete_account(
        self,
    ) -> Callable[[analytics_admin.DeleteAccountRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete account method over gRPC.

        Marks target Account as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        accounts. However, they can be restored using the Trash
        Can UI.

        If the accounts are not restored before the expiration
        time, the account and all child resources (eg:
        Properties, GoogleAdsLinks, Streams, AccessBindings)
        will be permanently purged.
        https://support.google.com/analytics/answer/6154772

        Returns an error if the target is not found.

        Returns:
            Callable[[~.DeleteAccountRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_account" not in self._stubs:
            self._stubs["delete_account"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteAccount",
                request_serializer=analytics_admin.DeleteAccountRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_account"]

    @property
    def update_account(
        self,
    ) -> Callable[[analytics_admin.UpdateAccountRequest], Awaitable[resources.Account]]:
        r"""Return a callable for the update account method over gRPC.

        Updates an account.

        Returns:
            Callable[[~.UpdateAccountRequest],
                    Awaitable[~.Account]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_account" not in self._stubs:
            self._stubs["update_account"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateAccount",
                request_serializer=analytics_admin.UpdateAccountRequest.serialize,
                response_deserializer=resources.Account.deserialize,
            )
        return self._stubs["update_account"]

    @property
    def provision_account_ticket(
        self,
    ) -> Callable[
        [analytics_admin.ProvisionAccountTicketRequest],
        Awaitable[analytics_admin.ProvisionAccountTicketResponse],
    ]:
        r"""Return a callable for the provision account ticket method over gRPC.

        Requests a ticket for creating an account.

        Returns:
            Callable[[~.ProvisionAccountTicketRequest],
                    Awaitable[~.ProvisionAccountTicketResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "provision_account_ticket" not in self._stubs:
            self._stubs["provision_account_ticket"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ProvisionAccountTicket",
                request_serializer=analytics_admin.ProvisionAccountTicketRequest.serialize,
                response_deserializer=analytics_admin.ProvisionAccountTicketResponse.deserialize,
            )
        return self._stubs["provision_account_ticket"]

    @property
    def list_account_summaries(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountSummariesRequest],
        Awaitable[analytics_admin.ListAccountSummariesResponse],
    ]:
        r"""Return a callable for the list account summaries method over gRPC.

        Returns summaries of all accounts accessible by the
        caller.

        Returns:
            Callable[[~.ListAccountSummariesRequest],
                    Awaitable[~.ListAccountSummariesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_account_summaries" not in self._stubs:
            self._stubs["list_account_summaries"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListAccountSummaries",
                request_serializer=analytics_admin.ListAccountSummariesRequest.serialize,
                response_deserializer=analytics_admin.ListAccountSummariesResponse.deserialize,
            )
        return self._stubs["list_account_summaries"]

    @property
    def get_property(
        self,
    ) -> Callable[[analytics_admin.GetPropertyRequest], Awaitable[resources.Property]]:
        r"""Return a callable for the get property method over gRPC.

        Lookup for a single "GA4" Property.

        Returns:
            Callable[[~.GetPropertyRequest],
                    Awaitable[~.Property]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_property" not in self._stubs:
            self._stubs["get_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetProperty",
                request_serializer=analytics_admin.GetPropertyRequest.serialize,
                response_deserializer=resources.Property.deserialize,
            )
        return self._stubs["get_property"]

    @property
    def list_properties(
        self,
    ) -> Callable[
        [analytics_admin.ListPropertiesRequest],
        Awaitable[analytics_admin.ListPropertiesResponse],
    ]:
        r"""Return a callable for the list properties method over gRPC.

        Returns child Properties under the specified parent
        Account.
        Only "GA4" properties will be returned.
        Properties will be excluded if the caller does not have
        access. Soft-deleted (ie: "trashed") properties are
        excluded by default. Returns an empty list if no
        relevant properties are found.

        Returns:
            Callable[[~.ListPropertiesRequest],
                    Awaitable[~.ListPropertiesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_properties" not in self._stubs:
            self._stubs["list_properties"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListProperties",
                request_serializer=analytics_admin.ListPropertiesRequest.serialize,
                response_deserializer=analytics_admin.ListPropertiesResponse.deserialize,
            )
        return self._stubs["list_properties"]

    @property
    def create_property(
        self,
    ) -> Callable[
        [analytics_admin.CreatePropertyRequest], Awaitable[resources.Property]
    ]:
        r"""Return a callable for the create property method over gRPC.

        Creates an "GA4" property with the specified location
        and attributes.

        Returns:
            Callable[[~.CreatePropertyRequest],
                    Awaitable[~.Property]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_property" not in self._stubs:
            self._stubs["create_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateProperty",
                request_serializer=analytics_admin.CreatePropertyRequest.serialize,
                response_deserializer=resources.Property.deserialize,
            )
        return self._stubs["create_property"]

    @property
    def delete_property(
        self,
    ) -> Callable[
        [analytics_admin.DeletePropertyRequest], Awaitable[resources.Property]
    ]:
        r"""Return a callable for the delete property method over gRPC.

        Marks target Property as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        properties. However, they can be restored using the
        Trash Can UI.

        If the properties are not restored before the expiration
        time, the Property and all child resources (eg:
        GoogleAdsLinks, Streams, AccessBindings) will be
        permanently purged.
        https://support.google.com/analytics/answer/6154772

        Returns an error if the target is not found, or is not a
        GA4 Property.

        Returns:
            Callable[[~.DeletePropertyRequest],
                    Awaitable[~.Property]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_property" not in self._stubs:
            self._stubs["delete_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteProperty",
                request_serializer=analytics_admin.DeletePropertyRequest.serialize,
                response_deserializer=resources.Property.deserialize,
            )
        return self._stubs["delete_property"]

    @property
    def update_property(
        self,
    ) -> Callable[
        [analytics_admin.UpdatePropertyRequest], Awaitable[resources.Property]
    ]:
        r"""Return a callable for the update property method over gRPC.

        Updates a property.

        Returns:
            Callable[[~.UpdatePropertyRequest],
                    Awaitable[~.Property]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_property" not in self._stubs:
            self._stubs["update_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateProperty",
                request_serializer=analytics_admin.UpdatePropertyRequest.serialize,
                response_deserializer=resources.Property.deserialize,
            )
        return self._stubs["update_property"]

    @property
    def create_firebase_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateFirebaseLinkRequest], Awaitable[resources.FirebaseLink]
    ]:
        r"""Return a callable for the create firebase link method over gRPC.

        Creates a FirebaseLink.

        Properties can have at most one FirebaseLink.

        Returns:
            Callable[[~.CreateFirebaseLinkRequest],
                    Awaitable[~.FirebaseLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_firebase_link" not in self._stubs:
            self._stubs["create_firebase_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateFirebaseLink",
                request_serializer=analytics_admin.CreateFirebaseLinkRequest.serialize,
                response_deserializer=resources.FirebaseLink.deserialize,
            )
        return self._stubs["create_firebase_link"]

    @property
    def delete_firebase_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteFirebaseLinkRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete firebase link method over gRPC.

        Deletes a FirebaseLink on a property

        Returns:
            Callable[[~.DeleteFirebaseLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_firebase_link" not in self._stubs:
            self._stubs["delete_firebase_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteFirebaseLink",
                request_serializer=analytics_admin.DeleteFirebaseLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_firebase_link"]

    @property
    def list_firebase_links(
        self,
    ) -> Callable[
        [analytics_admin.ListFirebaseLinksRequest],
        Awaitable[analytics_admin.ListFirebaseLinksResponse],
    ]:
        r"""Return a callable for the list firebase links method over gRPC.

        Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        Returns:
            Callable[[~.ListFirebaseLinksRequest],
                    Awaitable[~.ListFirebaseLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_firebase_links" not in self._stubs:
            self._stubs["list_firebase_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListFirebaseLinks",
                request_serializer=analytics_admin.ListFirebaseLinksRequest.serialize,
                response_deserializer=analytics_admin.ListFirebaseLinksResponse.deserialize,
            )
        return self._stubs["list_firebase_links"]

    @property
    def get_global_site_tag(
        self,
    ) -> Callable[
        [analytics_admin.GetGlobalSiteTagRequest], Awaitable[resources.GlobalSiteTag]
    ]:
        r"""Return a callable for the get global site tag method over gRPC.

        Returns the Site Tag for the specified web stream.
        Site Tags are immutable singletons.

        Returns:
            Callable[[~.GetGlobalSiteTagRequest],
                    Awaitable[~.GlobalSiteTag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_global_site_tag" not in self._stubs:
            self._stubs["get_global_site_tag"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetGlobalSiteTag",
                request_serializer=analytics_admin.GetGlobalSiteTagRequest.serialize,
                response_deserializer=resources.GlobalSiteTag.deserialize,
            )
        return self._stubs["get_global_site_tag"]

    @property
    def create_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateGoogleAdsLinkRequest], Awaitable[resources.GoogleAdsLink]
    ]:
        r"""Return a callable for the create google ads link method over gRPC.

        Creates a GoogleAdsLink.

        Returns:
            Callable[[~.CreateGoogleAdsLinkRequest],
                    Awaitable[~.GoogleAdsLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_google_ads_link" not in self._stubs:
            self._stubs["create_google_ads_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateGoogleAdsLink",
                request_serializer=analytics_admin.CreateGoogleAdsLinkRequest.serialize,
                response_deserializer=resources.GoogleAdsLink.deserialize,
            )
        return self._stubs["create_google_ads_link"]

    @property
    def update_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleAdsLinkRequest], Awaitable[resources.GoogleAdsLink]
    ]:
        r"""Return a callable for the update google ads link method over gRPC.

        Updates a GoogleAdsLink on a property

        Returns:
            Callable[[~.UpdateGoogleAdsLinkRequest],
                    Awaitable[~.GoogleAdsLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_google_ads_link" not in self._stubs:
            self._stubs["update_google_ads_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateGoogleAdsLink",
                request_serializer=analytics_admin.UpdateGoogleAdsLinkRequest.serialize,
                response_deserializer=resources.GoogleAdsLink.deserialize,
            )
        return self._stubs["update_google_ads_link"]

    @property
    def delete_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteGoogleAdsLinkRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete google ads link method over gRPC.

        Deletes a GoogleAdsLink on a property

        Returns:
            Callable[[~.DeleteGoogleAdsLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_google_ads_link" not in self._stubs:
            self._stubs["delete_google_ads_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteGoogleAdsLink",
                request_serializer=analytics_admin.DeleteGoogleAdsLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_google_ads_link"]

    @property
    def list_google_ads_links(
        self,
    ) -> Callable[
        [analytics_admin.ListGoogleAdsLinksRequest],
        Awaitable[analytics_admin.ListGoogleAdsLinksResponse],
    ]:
        r"""Return a callable for the list google ads links method over gRPC.

        Lists GoogleAdsLinks on a property.

        Returns:
            Callable[[~.ListGoogleAdsLinksRequest],
                    Awaitable[~.ListGoogleAdsLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_google_ads_links" not in self._stubs:
            self._stubs["list_google_ads_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListGoogleAdsLinks",
                request_serializer=analytics_admin.ListGoogleAdsLinksRequest.serialize,
                response_deserializer=analytics_admin.ListGoogleAdsLinksResponse.deserialize,
            )
        return self._stubs["list_google_ads_links"]

    @property
    def get_data_sharing_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataSharingSettingsRequest],
        Awaitable[resources.DataSharingSettings],
    ]:
        r"""Return a callable for the get data sharing settings method over gRPC.

        Get data sharing settings on an account.
        Data sharing settings are singletons.

        Returns:
            Callable[[~.GetDataSharingSettingsRequest],
                    Awaitable[~.DataSharingSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_sharing_settings" not in self._stubs:
            self._stubs["get_data_sharing_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDataSharingSettings",
                request_serializer=analytics_admin.GetDataSharingSettingsRequest.serialize,
                response_deserializer=resources.DataSharingSettings.deserialize,
            )
        return self._stubs["get_data_sharing_settings"]

    @property
    def get_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.GetMeasurementProtocolSecretRequest],
        Awaitable[resources.MeasurementProtocolSecret],
    ]:
        r"""Return a callable for the get measurement protocol
        secret method over gRPC.

        Lookup for a single "GA4" MeasurementProtocolSecret.

        Returns:
            Callable[[~.GetMeasurementProtocolSecretRequest],
                    Awaitable[~.MeasurementProtocolSecret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_measurement_protocol_secret" not in self._stubs:
            self._stubs[
                "get_measurement_protocol_secret"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetMeasurementProtocolSecret",
                request_serializer=analytics_admin.GetMeasurementProtocolSecretRequest.serialize,
                response_deserializer=resources.MeasurementProtocolSecret.deserialize,
            )
        return self._stubs["get_measurement_protocol_secret"]

    @property
    def list_measurement_protocol_secrets(
        self,
    ) -> Callable[
        [analytics_admin.ListMeasurementProtocolSecretsRequest],
        Awaitable[analytics_admin.ListMeasurementProtocolSecretsResponse],
    ]:
        r"""Return a callable for the list measurement protocol
        secrets method over gRPC.

        Returns child MeasurementProtocolSecrets under the
        specified parent Property.

        Returns:
            Callable[[~.ListMeasurementProtocolSecretsRequest],
                    Awaitable[~.ListMeasurementProtocolSecretsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_measurement_protocol_secrets" not in self._stubs:
            self._stubs[
                "list_measurement_protocol_secrets"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListMeasurementProtocolSecrets",
                request_serializer=analytics_admin.ListMeasurementProtocolSecretsRequest.serialize,
                response_deserializer=analytics_admin.ListMeasurementProtocolSecretsResponse.deserialize,
            )
        return self._stubs["list_measurement_protocol_secrets"]

    @property
    def create_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.CreateMeasurementProtocolSecretRequest],
        Awaitable[resources.MeasurementProtocolSecret],
    ]:
        r"""Return a callable for the create measurement protocol
        secret method over gRPC.

        Creates a measurement protocol secret.

        Returns:
            Callable[[~.CreateMeasurementProtocolSecretRequest],
                    Awaitable[~.MeasurementProtocolSecret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_measurement_protocol_secret" not in self._stubs:
            self._stubs[
                "create_measurement_protocol_secret"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateMeasurementProtocolSecret",
                request_serializer=analytics_admin.CreateMeasurementProtocolSecretRequest.serialize,
                response_deserializer=resources.MeasurementProtocolSecret.deserialize,
            )
        return self._stubs["create_measurement_protocol_secret"]

    @property
    def delete_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.DeleteMeasurementProtocolSecretRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete measurement protocol
        secret method over gRPC.

        Deletes target MeasurementProtocolSecret.

        Returns:
            Callable[[~.DeleteMeasurementProtocolSecretRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_measurement_protocol_secret" not in self._stubs:
            self._stubs[
                "delete_measurement_protocol_secret"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteMeasurementProtocolSecret",
                request_serializer=analytics_admin.DeleteMeasurementProtocolSecretRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_measurement_protocol_secret"]

    @property
    def update_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.UpdateMeasurementProtocolSecretRequest],
        Awaitable[resources.MeasurementProtocolSecret],
    ]:
        r"""Return a callable for the update measurement protocol
        secret method over gRPC.

        Updates a measurement protocol secret.

        Returns:
            Callable[[~.UpdateMeasurementProtocolSecretRequest],
                    Awaitable[~.MeasurementProtocolSecret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_measurement_protocol_secret" not in self._stubs:
            self._stubs[
                "update_measurement_protocol_secret"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateMeasurementProtocolSecret",
                request_serializer=analytics_admin.UpdateMeasurementProtocolSecretRequest.serialize,
                response_deserializer=resources.MeasurementProtocolSecret.deserialize,
            )
        return self._stubs["update_measurement_protocol_secret"]

    @property
    def acknowledge_user_data_collection(
        self,
    ) -> Callable[
        [analytics_admin.AcknowledgeUserDataCollectionRequest],
        Awaitable[analytics_admin.AcknowledgeUserDataCollectionResponse],
    ]:
        r"""Return a callable for the acknowledge user data
        collection method over gRPC.

        Acknowledges the terms of user data collection for
        the specified property.
        This acknowledgement must be completed (either in the
        Google Analytics UI or through this API) before
        MeasurementProtocolSecret resources may be created.

        Returns:
            Callable[[~.AcknowledgeUserDataCollectionRequest],
                    Awaitable[~.AcknowledgeUserDataCollectionResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "acknowledge_user_data_collection" not in self._stubs:
            self._stubs[
                "acknowledge_user_data_collection"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/AcknowledgeUserDataCollection",
                request_serializer=analytics_admin.AcknowledgeUserDataCollectionRequest.serialize,
                response_deserializer=analytics_admin.AcknowledgeUserDataCollectionResponse.deserialize,
            )
        return self._stubs["acknowledge_user_data_collection"]

    @property
    def get_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.GetSKAdNetworkConversionValueSchemaRequest],
        Awaitable[resources.SKAdNetworkConversionValueSchema],
    ]:
        r"""Return a callable for the get sk ad network conversion
        value schema method over gRPC.

        Looks up a single SKAdNetworkConversionValueSchema.

        Returns:
            Callable[[~.GetSKAdNetworkConversionValueSchemaRequest],
                    Awaitable[~.SKAdNetworkConversionValueSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_sk_ad_network_conversion_value_schema" not in self._stubs:
            self._stubs[
                "get_sk_ad_network_conversion_value_schema"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetSKAdNetworkConversionValueSchema",
                request_serializer=analytics_admin.GetSKAdNetworkConversionValueSchemaRequest.serialize,
                response_deserializer=resources.SKAdNetworkConversionValueSchema.deserialize,
            )
        return self._stubs["get_sk_ad_network_conversion_value_schema"]

    @property
    def create_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest],
        Awaitable[resources.SKAdNetworkConversionValueSchema],
    ]:
        r"""Return a callable for the create sk ad network
        conversion value schema method over gRPC.

        Creates a SKAdNetworkConversionValueSchema.

        Returns:
            Callable[[~.CreateSKAdNetworkConversionValueSchemaRequest],
                    Awaitable[~.SKAdNetworkConversionValueSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_sk_ad_network_conversion_value_schema" not in self._stubs:
            self._stubs[
                "create_sk_ad_network_conversion_value_schema"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateSKAdNetworkConversionValueSchema",
                request_serializer=analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest.serialize,
                response_deserializer=resources.SKAdNetworkConversionValueSchema.deserialize,
            )
        return self._stubs["create_sk_ad_network_conversion_value_schema"]

    @property
    def delete_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete sk ad network
        conversion value schema method over gRPC.

        Deletes target SKAdNetworkConversionValueSchema.

        Returns:
            Callable[[~.DeleteSKAdNetworkConversionValueSchemaRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_sk_ad_network_conversion_value_schema" not in self._stubs:
            self._stubs[
                "delete_sk_ad_network_conversion_value_schema"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteSKAdNetworkConversionValueSchema",
                request_serializer=analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_sk_ad_network_conversion_value_schema"]

    @property
    def update_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest],
        Awaitable[resources.SKAdNetworkConversionValueSchema],
    ]:
        r"""Return a callable for the update sk ad network
        conversion value schema method over gRPC.

        Updates a SKAdNetworkConversionValueSchema.

        Returns:
            Callable[[~.UpdateSKAdNetworkConversionValueSchemaRequest],
                    Awaitable[~.SKAdNetworkConversionValueSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_sk_ad_network_conversion_value_schema" not in self._stubs:
            self._stubs[
                "update_sk_ad_network_conversion_value_schema"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateSKAdNetworkConversionValueSchema",
                request_serializer=analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest.serialize,
                response_deserializer=resources.SKAdNetworkConversionValueSchema.deserialize,
            )
        return self._stubs["update_sk_ad_network_conversion_value_schema"]

    @property
    def list_sk_ad_network_conversion_value_schemas(
        self,
    ) -> Callable[
        [analytics_admin.ListSKAdNetworkConversionValueSchemasRequest],
        Awaitable[analytics_admin.ListSKAdNetworkConversionValueSchemasResponse],
    ]:
        r"""Return a callable for the list sk ad network conversion
        value schemas method over gRPC.

        Lists SKAdNetworkConversionValueSchema on a stream.
        Properties can have at most one
        SKAdNetworkConversionValueSchema.

        Returns:
            Callable[[~.ListSKAdNetworkConversionValueSchemasRequest],
                    Awaitable[~.ListSKAdNetworkConversionValueSchemasResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_sk_ad_network_conversion_value_schemas" not in self._stubs:
            self._stubs[
                "list_sk_ad_network_conversion_value_schemas"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListSKAdNetworkConversionValueSchemas",
                request_serializer=analytics_admin.ListSKAdNetworkConversionValueSchemasRequest.serialize,
                response_deserializer=analytics_admin.ListSKAdNetworkConversionValueSchemasResponse.deserialize,
            )
        return self._stubs["list_sk_ad_network_conversion_value_schemas"]

    @property
    def search_change_history_events(
        self,
    ) -> Callable[
        [analytics_admin.SearchChangeHistoryEventsRequest],
        Awaitable[analytics_admin.SearchChangeHistoryEventsResponse],
    ]:
        r"""Return a callable for the search change history events method over gRPC.

        Searches through all changes to an account or its
        children given the specified set of filters.

        Returns:
            Callable[[~.SearchChangeHistoryEventsRequest],
                    Awaitable[~.SearchChangeHistoryEventsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_change_history_events" not in self._stubs:
            self._stubs["search_change_history_events"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/SearchChangeHistoryEvents",
                request_serializer=analytics_admin.SearchChangeHistoryEventsRequest.serialize,
                response_deserializer=analytics_admin.SearchChangeHistoryEventsResponse.deserialize,
            )
        return self._stubs["search_change_history_events"]

    @property
    def get_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetGoogleSignalsSettingsRequest],
        Awaitable[resources.GoogleSignalsSettings],
    ]:
        r"""Return a callable for the get google signals settings method over gRPC.

        Lookup for Google Signals settings for a property.

        Returns:
            Callable[[~.GetGoogleSignalsSettingsRequest],
                    Awaitable[~.GoogleSignalsSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_google_signals_settings" not in self._stubs:
            self._stubs["get_google_signals_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetGoogleSignalsSettings",
                request_serializer=analytics_admin.GetGoogleSignalsSettingsRequest.serialize,
                response_deserializer=resources.GoogleSignalsSettings.deserialize,
            )
        return self._stubs["get_google_signals_settings"]

    @property
    def update_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleSignalsSettingsRequest],
        Awaitable[resources.GoogleSignalsSettings],
    ]:
        r"""Return a callable for the update google signals settings method over gRPC.

        Updates Google Signals settings for a property.

        Returns:
            Callable[[~.UpdateGoogleSignalsSettingsRequest],
                    Awaitable[~.GoogleSignalsSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_google_signals_settings" not in self._stubs:
            self._stubs[
                "update_google_signals_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateGoogleSignalsSettings",
                request_serializer=analytics_admin.UpdateGoogleSignalsSettingsRequest.serialize,
                response_deserializer=resources.GoogleSignalsSettings.deserialize,
            )
        return self._stubs["update_google_signals_settings"]

    @property
    def create_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.CreateConversionEventRequest],
        Awaitable[resources.ConversionEvent],
    ]:
        r"""Return a callable for the create conversion event method over gRPC.

        Deprecated: Use ``CreateKeyEvent`` instead. Creates a conversion
        event with the specified attributes.

        Returns:
            Callable[[~.CreateConversionEventRequest],
                    Awaitable[~.ConversionEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_conversion_event" not in self._stubs:
            self._stubs["create_conversion_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateConversionEvent",
                request_serializer=analytics_admin.CreateConversionEventRequest.serialize,
                response_deserializer=resources.ConversionEvent.deserialize,
            )
        return self._stubs["create_conversion_event"]

    @property
    def update_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.UpdateConversionEventRequest],
        Awaitable[resources.ConversionEvent],
    ]:
        r"""Return a callable for the update conversion event method over gRPC.

        Deprecated: Use ``UpdateKeyEvent`` instead. Updates a conversion
        event with the specified attributes.

        Returns:
            Callable[[~.UpdateConversionEventRequest],
                    Awaitable[~.ConversionEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_conversion_event" not in self._stubs:
            self._stubs["update_conversion_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateConversionEvent",
                request_serializer=analytics_admin.UpdateConversionEventRequest.serialize,
                response_deserializer=resources.ConversionEvent.deserialize,
            )
        return self._stubs["update_conversion_event"]

    @property
    def get_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.GetConversionEventRequest],
        Awaitable[resources.ConversionEvent],
    ]:
        r"""Return a callable for the get conversion event method over gRPC.

        Deprecated: Use ``GetKeyEvent`` instead. Retrieve a single
        conversion event.

        Returns:
            Callable[[~.GetConversionEventRequest],
                    Awaitable[~.ConversionEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_conversion_event" not in self._stubs:
            self._stubs["get_conversion_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetConversionEvent",
                request_serializer=analytics_admin.GetConversionEventRequest.serialize,
                response_deserializer=resources.ConversionEvent.deserialize,
            )
        return self._stubs["get_conversion_event"]

    @property
    def delete_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.DeleteConversionEventRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete conversion event method over gRPC.

        Deprecated: Use ``DeleteKeyEvent`` instead. Deletes a conversion
        event in a property.

        Returns:
            Callable[[~.DeleteConversionEventRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_conversion_event" not in self._stubs:
            self._stubs["delete_conversion_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteConversionEvent",
                request_serializer=analytics_admin.DeleteConversionEventRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_conversion_event"]

    @property
    def list_conversion_events(
        self,
    ) -> Callable[
        [analytics_admin.ListConversionEventsRequest],
        Awaitable[analytics_admin.ListConversionEventsResponse],
    ]:
        r"""Return a callable for the list conversion events method over gRPC.

        Deprecated: Use ``ListKeyEvents`` instead. Returns a list of
        conversion events in the specified parent property.

        Returns an empty list if no conversion events are found.

        Returns:
            Callable[[~.ListConversionEventsRequest],
                    Awaitable[~.ListConversionEventsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_conversion_events" not in self._stubs:
            self._stubs["list_conversion_events"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListConversionEvents",
                request_serializer=analytics_admin.ListConversionEventsRequest.serialize,
                response_deserializer=analytics_admin.ListConversionEventsResponse.deserialize,
            )
        return self._stubs["list_conversion_events"]

    @property
    def create_key_event(
        self,
    ) -> Callable[
        [analytics_admin.CreateKeyEventRequest], Awaitable[resources.KeyEvent]
    ]:
        r"""Return a callable for the create key event method over gRPC.

        Creates a Key Event.

        Returns:
            Callable[[~.CreateKeyEventRequest],
                    Awaitable[~.KeyEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_key_event" not in self._stubs:
            self._stubs["create_key_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateKeyEvent",
                request_serializer=analytics_admin.CreateKeyEventRequest.serialize,
                response_deserializer=resources.KeyEvent.deserialize,
            )
        return self._stubs["create_key_event"]

    @property
    def update_key_event(
        self,
    ) -> Callable[
        [analytics_admin.UpdateKeyEventRequest], Awaitable[resources.KeyEvent]
    ]:
        r"""Return a callable for the update key event method over gRPC.

        Updates a Key Event.

        Returns:
            Callable[[~.UpdateKeyEventRequest],
                    Awaitable[~.KeyEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_key_event" not in self._stubs:
            self._stubs["update_key_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateKeyEvent",
                request_serializer=analytics_admin.UpdateKeyEventRequest.serialize,
                response_deserializer=resources.KeyEvent.deserialize,
            )
        return self._stubs["update_key_event"]

    @property
    def get_key_event(
        self,
    ) -> Callable[[analytics_admin.GetKeyEventRequest], Awaitable[resources.KeyEvent]]:
        r"""Return a callable for the get key event method over gRPC.

        Retrieve a single Key Event.

        Returns:
            Callable[[~.GetKeyEventRequest],
                    Awaitable[~.KeyEvent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_key_event" not in self._stubs:
            self._stubs["get_key_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetKeyEvent",
                request_serializer=analytics_admin.GetKeyEventRequest.serialize,
                response_deserializer=resources.KeyEvent.deserialize,
            )
        return self._stubs["get_key_event"]

    @property
    def delete_key_event(
        self,
    ) -> Callable[[analytics_admin.DeleteKeyEventRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete key event method over gRPC.

        Deletes a Key Event.

        Returns:
            Callable[[~.DeleteKeyEventRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_key_event" not in self._stubs:
            self._stubs["delete_key_event"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteKeyEvent",
                request_serializer=analytics_admin.DeleteKeyEventRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_key_event"]

    @property
    def list_key_events(
        self,
    ) -> Callable[
        [analytics_admin.ListKeyEventsRequest],
        Awaitable[analytics_admin.ListKeyEventsResponse],
    ]:
        r"""Return a callable for the list key events method over gRPC.

        Returns a list of Key Events in the specified parent
        property. Returns an empty list if no Key Events are
        found.

        Returns:
            Callable[[~.ListKeyEventsRequest],
                    Awaitable[~.ListKeyEventsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_key_events" not in self._stubs:
            self._stubs["list_key_events"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListKeyEvents",
                request_serializer=analytics_admin.ListKeyEventsRequest.serialize,
                response_deserializer=analytics_admin.ListKeyEventsResponse.deserialize,
            )
        return self._stubs["list_key_events"]

    @property
    def get_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.GetDisplayVideo360AdvertiserLinkRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLink],
    ]:
        r"""Return a callable for the get display video360
        advertiser link method over gRPC.

        Look up a single DisplayVideo360AdvertiserLink

        Returns:
            Callable[[~.GetDisplayVideo360AdvertiserLinkRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_display_video360_advertiser_link" not in self._stubs:
            self._stubs[
                "get_display_video360_advertiser_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDisplayVideo360AdvertiserLink",
                request_serializer=analytics_admin.GetDisplayVideo360AdvertiserLinkRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLink.deserialize,
            )
        return self._stubs["get_display_video360_advertiser_link"]

    @property
    def list_display_video360_advertiser_links(
        self,
    ) -> Callable[
        [analytics_admin.ListDisplayVideo360AdvertiserLinksRequest],
        Awaitable[analytics_admin.ListDisplayVideo360AdvertiserLinksResponse],
    ]:
        r"""Return a callable for the list display video360
        advertiser links method over gRPC.

        Lists all DisplayVideo360AdvertiserLinks on a
        property.

        Returns:
            Callable[[~.ListDisplayVideo360AdvertiserLinksRequest],
                    Awaitable[~.ListDisplayVideo360AdvertiserLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_display_video360_advertiser_links" not in self._stubs:
            self._stubs[
                "list_display_video360_advertiser_links"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListDisplayVideo360AdvertiserLinks",
                request_serializer=analytics_admin.ListDisplayVideo360AdvertiserLinksRequest.serialize,
                response_deserializer=analytics_admin.ListDisplayVideo360AdvertiserLinksResponse.deserialize,
            )
        return self._stubs["list_display_video360_advertiser_links"]

    @property
    def create_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLink],
    ]:
        r"""Return a callable for the create display video360
        advertiser link method over gRPC.

        Creates a DisplayVideo360AdvertiserLink.
        This can only be utilized by users who have proper
        authorization both on the Google Analytics property and
        on the Display & Video 360 advertiser. Users who do not
        have access to the Display & Video 360 advertiser should
        instead seek to create a DisplayVideo360LinkProposal.

        Returns:
            Callable[[~.CreateDisplayVideo360AdvertiserLinkRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_display_video360_advertiser_link" not in self._stubs:
            self._stubs[
                "create_display_video360_advertiser_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateDisplayVideo360AdvertiserLink",
                request_serializer=analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLink.deserialize,
            )
        return self._stubs["create_display_video360_advertiser_link"]

    @property
    def delete_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete display video360
        advertiser link method over gRPC.

        Deletes a DisplayVideo360AdvertiserLink on a
        property.

        Returns:
            Callable[[~.DeleteDisplayVideo360AdvertiserLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_display_video360_advertiser_link" not in self._stubs:
            self._stubs[
                "delete_display_video360_advertiser_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteDisplayVideo360AdvertiserLink",
                request_serializer=analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_display_video360_advertiser_link"]

    @property
    def update_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLink],
    ]:
        r"""Return a callable for the update display video360
        advertiser link method over gRPC.

        Updates a DisplayVideo360AdvertiserLink on a
        property.

        Returns:
            Callable[[~.UpdateDisplayVideo360AdvertiserLinkRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_display_video360_advertiser_link" not in self._stubs:
            self._stubs[
                "update_display_video360_advertiser_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateDisplayVideo360AdvertiserLink",
                request_serializer=analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLink.deserialize,
            )
        return self._stubs["update_display_video360_advertiser_link"]

    @property
    def get_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLinkProposal],
    ]:
        r"""Return a callable for the get display video360
        advertiser link proposal method over gRPC.

        Lookup for a single
        DisplayVideo360AdvertiserLinkProposal.

        Returns:
            Callable[[~.GetDisplayVideo360AdvertiserLinkProposalRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLinkProposal]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_display_video360_advertiser_link_proposal" not in self._stubs:
            self._stubs[
                "get_display_video360_advertiser_link_proposal"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDisplayVideo360AdvertiserLinkProposal",
                request_serializer=analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLinkProposal.deserialize,
            )
        return self._stubs["get_display_video360_advertiser_link_proposal"]

    @property
    def list_display_video360_advertiser_link_proposals(
        self,
    ) -> Callable[
        [analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest],
        Awaitable[analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse],
    ]:
        r"""Return a callable for the list display video360
        advertiser link proposals method over gRPC.

        Lists DisplayVideo360AdvertiserLinkProposals on a
        property.

        Returns:
            Callable[[~.ListDisplayVideo360AdvertiserLinkProposalsRequest],
                    Awaitable[~.ListDisplayVideo360AdvertiserLinkProposalsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_display_video360_advertiser_link_proposals" not in self._stubs:
            self._stubs[
                "list_display_video360_advertiser_link_proposals"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListDisplayVideo360AdvertiserLinkProposals",
                request_serializer=analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest.serialize,
                response_deserializer=analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse.deserialize,
            )
        return self._stubs["list_display_video360_advertiser_link_proposals"]

    @property
    def create_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLinkProposal],
    ]:
        r"""Return a callable for the create display video360
        advertiser link proposal method over gRPC.

        Creates a DisplayVideo360AdvertiserLinkProposal.

        Returns:
            Callable[[~.CreateDisplayVideo360AdvertiserLinkProposalRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLinkProposal]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_display_video360_advertiser_link_proposal" not in self._stubs:
            self._stubs[
                "create_display_video360_advertiser_link_proposal"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateDisplayVideo360AdvertiserLinkProposal",
                request_serializer=analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLinkProposal.deserialize,
            )
        return self._stubs["create_display_video360_advertiser_link_proposal"]

    @property
    def delete_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete display video360
        advertiser link proposal method over gRPC.

        Deletes a DisplayVideo360AdvertiserLinkProposal on a
        property. This can only be used on cancelled proposals.

        Returns:
            Callable[[~.DeleteDisplayVideo360AdvertiserLinkProposalRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_display_video360_advertiser_link_proposal" not in self._stubs:
            self._stubs[
                "delete_display_video360_advertiser_link_proposal"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteDisplayVideo360AdvertiserLinkProposal",
                request_serializer=analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_display_video360_advertiser_link_proposal"]

    @property
    def approve_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest],
        Awaitable[analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse],
    ]:
        r"""Return a callable for the approve display video360
        advertiser link proposal method over gRPC.

        Approves a DisplayVideo360AdvertiserLinkProposal.
        The DisplayVideo360AdvertiserLinkProposal will be
        deleted and a new DisplayVideo360AdvertiserLink will be
        created.

        Returns:
            Callable[[~.ApproveDisplayVideo360AdvertiserLinkProposalRequest],
                    Awaitable[~.ApproveDisplayVideo360AdvertiserLinkProposalResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "approve_display_video360_advertiser_link_proposal" not in self._stubs:
            self._stubs[
                "approve_display_video360_advertiser_link_proposal"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ApproveDisplayVideo360AdvertiserLinkProposal",
                request_serializer=analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest.serialize,
                response_deserializer=analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse.deserialize,
            )
        return self._stubs["approve_display_video360_advertiser_link_proposal"]

    @property
    def cancel_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest],
        Awaitable[resources.DisplayVideo360AdvertiserLinkProposal],
    ]:
        r"""Return a callable for the cancel display video360
        advertiser link proposal method over gRPC.

        Cancels a DisplayVideo360AdvertiserLinkProposal.
        Cancelling can mean either:

        - Declining a proposal initiated from Display & Video
          360
        - Withdrawing a proposal initiated from Google Analytics
          After being cancelled, a proposal will eventually be
          deleted automatically.

        Returns:
            Callable[[~.CancelDisplayVideo360AdvertiserLinkProposalRequest],
                    Awaitable[~.DisplayVideo360AdvertiserLinkProposal]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_display_video360_advertiser_link_proposal" not in self._stubs:
            self._stubs[
                "cancel_display_video360_advertiser_link_proposal"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CancelDisplayVideo360AdvertiserLinkProposal",
                request_serializer=analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest.serialize,
                response_deserializer=resources.DisplayVideo360AdvertiserLinkProposal.deserialize,
            )
        return self._stubs["cancel_display_video360_advertiser_link_proposal"]

    @property
    def create_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.CreateCustomDimensionRequest],
        Awaitable[resources.CustomDimension],
    ]:
        r"""Return a callable for the create custom dimension method over gRPC.

        Creates a CustomDimension.

        Returns:
            Callable[[~.CreateCustomDimensionRequest],
                    Awaitable[~.CustomDimension]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_custom_dimension" not in self._stubs:
            self._stubs["create_custom_dimension"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateCustomDimension",
                request_serializer=analytics_admin.CreateCustomDimensionRequest.serialize,
                response_deserializer=resources.CustomDimension.deserialize,
            )
        return self._stubs["create_custom_dimension"]

    @property
    def update_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCustomDimensionRequest],
        Awaitable[resources.CustomDimension],
    ]:
        r"""Return a callable for the update custom dimension method over gRPC.

        Updates a CustomDimension on a property.

        Returns:
            Callable[[~.UpdateCustomDimensionRequest],
                    Awaitable[~.CustomDimension]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_custom_dimension" not in self._stubs:
            self._stubs["update_custom_dimension"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateCustomDimension",
                request_serializer=analytics_admin.UpdateCustomDimensionRequest.serialize,
                response_deserializer=resources.CustomDimension.deserialize,
            )
        return self._stubs["update_custom_dimension"]

    @property
    def list_custom_dimensions(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomDimensionsRequest],
        Awaitable[analytics_admin.ListCustomDimensionsResponse],
    ]:
        r"""Return a callable for the list custom dimensions method over gRPC.

        Lists CustomDimensions on a property.

        Returns:
            Callable[[~.ListCustomDimensionsRequest],
                    Awaitable[~.ListCustomDimensionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_custom_dimensions" not in self._stubs:
            self._stubs["list_custom_dimensions"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListCustomDimensions",
                request_serializer=analytics_admin.ListCustomDimensionsRequest.serialize,
                response_deserializer=analytics_admin.ListCustomDimensionsResponse.deserialize,
            )
        return self._stubs["list_custom_dimensions"]

    @property
    def archive_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.ArchiveCustomDimensionRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the archive custom dimension method over gRPC.

        Archives a CustomDimension on a property.

        Returns:
            Callable[[~.ArchiveCustomDimensionRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "archive_custom_dimension" not in self._stubs:
            self._stubs["archive_custom_dimension"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ArchiveCustomDimension",
                request_serializer=analytics_admin.ArchiveCustomDimensionRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["archive_custom_dimension"]

    @property
    def get_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.GetCustomDimensionRequest],
        Awaitable[resources.CustomDimension],
    ]:
        r"""Return a callable for the get custom dimension method over gRPC.

        Lookup for a single CustomDimension.

        Returns:
            Callable[[~.GetCustomDimensionRequest],
                    Awaitable[~.CustomDimension]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_custom_dimension" not in self._stubs:
            self._stubs["get_custom_dimension"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetCustomDimension",
                request_serializer=analytics_admin.GetCustomDimensionRequest.serialize,
                response_deserializer=resources.CustomDimension.deserialize,
            )
        return self._stubs["get_custom_dimension"]

    @property
    def create_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.CreateCustomMetricRequest], Awaitable[resources.CustomMetric]
    ]:
        r"""Return a callable for the create custom metric method over gRPC.

        Creates a CustomMetric.

        Returns:
            Callable[[~.CreateCustomMetricRequest],
                    Awaitable[~.CustomMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_custom_metric" not in self._stubs:
            self._stubs["create_custom_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateCustomMetric",
                request_serializer=analytics_admin.CreateCustomMetricRequest.serialize,
                response_deserializer=resources.CustomMetric.deserialize,
            )
        return self._stubs["create_custom_metric"]

    @property
    def update_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCustomMetricRequest], Awaitable[resources.CustomMetric]
    ]:
        r"""Return a callable for the update custom metric method over gRPC.

        Updates a CustomMetric on a property.

        Returns:
            Callable[[~.UpdateCustomMetricRequest],
                    Awaitable[~.CustomMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_custom_metric" not in self._stubs:
            self._stubs["update_custom_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateCustomMetric",
                request_serializer=analytics_admin.UpdateCustomMetricRequest.serialize,
                response_deserializer=resources.CustomMetric.deserialize,
            )
        return self._stubs["update_custom_metric"]

    @property
    def list_custom_metrics(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomMetricsRequest],
        Awaitable[analytics_admin.ListCustomMetricsResponse],
    ]:
        r"""Return a callable for the list custom metrics method over gRPC.

        Lists CustomMetrics on a property.

        Returns:
            Callable[[~.ListCustomMetricsRequest],
                    Awaitable[~.ListCustomMetricsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_custom_metrics" not in self._stubs:
            self._stubs["list_custom_metrics"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListCustomMetrics",
                request_serializer=analytics_admin.ListCustomMetricsRequest.serialize,
                response_deserializer=analytics_admin.ListCustomMetricsResponse.deserialize,
            )
        return self._stubs["list_custom_metrics"]

    @property
    def archive_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.ArchiveCustomMetricRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the archive custom metric method over gRPC.

        Archives a CustomMetric on a property.

        Returns:
            Callable[[~.ArchiveCustomMetricRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "archive_custom_metric" not in self._stubs:
            self._stubs["archive_custom_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ArchiveCustomMetric",
                request_serializer=analytics_admin.ArchiveCustomMetricRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["archive_custom_metric"]

    @property
    def get_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.GetCustomMetricRequest], Awaitable[resources.CustomMetric]
    ]:
        r"""Return a callable for the get custom metric method over gRPC.

        Lookup for a single CustomMetric.

        Returns:
            Callable[[~.GetCustomMetricRequest],
                    Awaitable[~.CustomMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_custom_metric" not in self._stubs:
            self._stubs["get_custom_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetCustomMetric",
                request_serializer=analytics_admin.GetCustomMetricRequest.serialize,
                response_deserializer=resources.CustomMetric.deserialize,
            )
        return self._stubs["get_custom_metric"]

    @property
    def get_data_retention_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataRetentionSettingsRequest],
        Awaitable[resources.DataRetentionSettings],
    ]:
        r"""Return a callable for the get data retention settings method over gRPC.

        Returns the singleton data retention settings for
        this property.

        Returns:
            Callable[[~.GetDataRetentionSettingsRequest],
                    Awaitable[~.DataRetentionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_retention_settings" not in self._stubs:
            self._stubs["get_data_retention_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDataRetentionSettings",
                request_serializer=analytics_admin.GetDataRetentionSettingsRequest.serialize,
                response_deserializer=resources.DataRetentionSettings.deserialize,
            )
        return self._stubs["get_data_retention_settings"]

    @property
    def update_data_retention_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDataRetentionSettingsRequest],
        Awaitable[resources.DataRetentionSettings],
    ]:
        r"""Return a callable for the update data retention settings method over gRPC.

        Updates the singleton data retention settings for
        this property.

        Returns:
            Callable[[~.UpdateDataRetentionSettingsRequest],
                    Awaitable[~.DataRetentionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_retention_settings" not in self._stubs:
            self._stubs[
                "update_data_retention_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateDataRetentionSettings",
                request_serializer=analytics_admin.UpdateDataRetentionSettingsRequest.serialize,
                response_deserializer=resources.DataRetentionSettings.deserialize,
            )
        return self._stubs["update_data_retention_settings"]

    @property
    def create_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.CreateDataStreamRequest], Awaitable[resources.DataStream]
    ]:
        r"""Return a callable for the create data stream method over gRPC.

        Creates a DataStream.

        Returns:
            Callable[[~.CreateDataStreamRequest],
                    Awaitable[~.DataStream]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_stream" not in self._stubs:
            self._stubs["create_data_stream"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateDataStream",
                request_serializer=analytics_admin.CreateDataStreamRequest.serialize,
                response_deserializer=resources.DataStream.deserialize,
            )
        return self._stubs["create_data_stream"]

    @property
    def delete_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.DeleteDataStreamRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete data stream method over gRPC.

        Deletes a DataStream on a property.

        Returns:
            Callable[[~.DeleteDataStreamRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_stream" not in self._stubs:
            self._stubs["delete_data_stream"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteDataStream",
                request_serializer=analytics_admin.DeleteDataStreamRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_data_stream"]

    @property
    def update_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDataStreamRequest], Awaitable[resources.DataStream]
    ]:
        r"""Return a callable for the update data stream method over gRPC.

        Updates a DataStream on a property.

        Returns:
            Callable[[~.UpdateDataStreamRequest],
                    Awaitable[~.DataStream]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_stream" not in self._stubs:
            self._stubs["update_data_stream"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateDataStream",
                request_serializer=analytics_admin.UpdateDataStreamRequest.serialize,
                response_deserializer=resources.DataStream.deserialize,
            )
        return self._stubs["update_data_stream"]

    @property
    def list_data_streams(
        self,
    ) -> Callable[
        [analytics_admin.ListDataStreamsRequest],
        Awaitable[analytics_admin.ListDataStreamsResponse],
    ]:
        r"""Return a callable for the list data streams method over gRPC.

        Lists DataStreams on a property.

        Returns:
            Callable[[~.ListDataStreamsRequest],
                    Awaitable[~.ListDataStreamsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_streams" not in self._stubs:
            self._stubs["list_data_streams"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListDataStreams",
                request_serializer=analytics_admin.ListDataStreamsRequest.serialize,
                response_deserializer=analytics_admin.ListDataStreamsResponse.deserialize,
            )
        return self._stubs["list_data_streams"]

    @property
    def get_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.GetDataStreamRequest], Awaitable[resources.DataStream]
    ]:
        r"""Return a callable for the get data stream method over gRPC.

        Lookup for a single DataStream.

        Returns:
            Callable[[~.GetDataStreamRequest],
                    Awaitable[~.DataStream]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_stream" not in self._stubs:
            self._stubs["get_data_stream"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDataStream",
                request_serializer=analytics_admin.GetDataStreamRequest.serialize,
                response_deserializer=resources.DataStream.deserialize,
            )
        return self._stubs["get_data_stream"]

    @property
    def get_audience(
        self,
    ) -> Callable[[analytics_admin.GetAudienceRequest], Awaitable[audience.Audience]]:
        r"""Return a callable for the get audience method over gRPC.

        Lookup for a single Audience.
        Audiences created before 2020 may not be supported.
        Default audiences will not show filter definitions.

        Returns:
            Callable[[~.GetAudienceRequest],
                    Awaitable[~.Audience]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_audience" not in self._stubs:
            self._stubs["get_audience"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetAudience",
                request_serializer=analytics_admin.GetAudienceRequest.serialize,
                response_deserializer=audience.Audience.deserialize,
            )
        return self._stubs["get_audience"]

    @property
    def list_audiences(
        self,
    ) -> Callable[
        [analytics_admin.ListAudiencesRequest],
        Awaitable[analytics_admin.ListAudiencesResponse],
    ]:
        r"""Return a callable for the list audiences method over gRPC.

        Lists Audiences on a property.
        Audiences created before 2020 may not be supported.
        Default audiences will not show filter definitions.

        Returns:
            Callable[[~.ListAudiencesRequest],
                    Awaitable[~.ListAudiencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_audiences" not in self._stubs:
            self._stubs["list_audiences"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListAudiences",
                request_serializer=analytics_admin.ListAudiencesRequest.serialize,
                response_deserializer=analytics_admin.ListAudiencesResponse.deserialize,
            )
        return self._stubs["list_audiences"]

    @property
    def create_audience(
        self,
    ) -> Callable[
        [analytics_admin.CreateAudienceRequest], Awaitable[gaa_audience.Audience]
    ]:
        r"""Return a callable for the create audience method over gRPC.

        Creates an Audience.

        Returns:
            Callable[[~.CreateAudienceRequest],
                    Awaitable[~.Audience]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_audience" not in self._stubs:
            self._stubs["create_audience"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateAudience",
                request_serializer=analytics_admin.CreateAudienceRequest.serialize,
                response_deserializer=gaa_audience.Audience.deserialize,
            )
        return self._stubs["create_audience"]

    @property
    def update_audience(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAudienceRequest], Awaitable[gaa_audience.Audience]
    ]:
        r"""Return a callable for the update audience method over gRPC.

        Updates an Audience on a property.

        Returns:
            Callable[[~.UpdateAudienceRequest],
                    Awaitable[~.Audience]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_audience" not in self._stubs:
            self._stubs["update_audience"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateAudience",
                request_serializer=analytics_admin.UpdateAudienceRequest.serialize,
                response_deserializer=gaa_audience.Audience.deserialize,
            )
        return self._stubs["update_audience"]

    @property
    def archive_audience(
        self,
    ) -> Callable[[analytics_admin.ArchiveAudienceRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the archive audience method over gRPC.

        Archives an Audience on a property.

        Returns:
            Callable[[~.ArchiveAudienceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "archive_audience" not in self._stubs:
            self._stubs["archive_audience"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ArchiveAudience",
                request_serializer=analytics_admin.ArchiveAudienceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["archive_audience"]

    @property
    def get_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.GetSearchAds360LinkRequest],
        Awaitable[resources.SearchAds360Link],
    ]:
        r"""Return a callable for the get search ads360 link method over gRPC.

        Look up a single SearchAds360Link

        Returns:
            Callable[[~.GetSearchAds360LinkRequest],
                    Awaitable[~.SearchAds360Link]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_search_ads360_link" not in self._stubs:
            self._stubs["get_search_ads360_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetSearchAds360Link",
                request_serializer=analytics_admin.GetSearchAds360LinkRequest.serialize,
                response_deserializer=resources.SearchAds360Link.deserialize,
            )
        return self._stubs["get_search_ads360_link"]

    @property
    def list_search_ads360_links(
        self,
    ) -> Callable[
        [analytics_admin.ListSearchAds360LinksRequest],
        Awaitable[analytics_admin.ListSearchAds360LinksResponse],
    ]:
        r"""Return a callable for the list search ads360 links method over gRPC.

        Lists all SearchAds360Links on a property.

        Returns:
            Callable[[~.ListSearchAds360LinksRequest],
                    Awaitable[~.ListSearchAds360LinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_search_ads360_links" not in self._stubs:
            self._stubs["list_search_ads360_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListSearchAds360Links",
                request_serializer=analytics_admin.ListSearchAds360LinksRequest.serialize,
                response_deserializer=analytics_admin.ListSearchAds360LinksResponse.deserialize,
            )
        return self._stubs["list_search_ads360_links"]

    @property
    def create_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateSearchAds360LinkRequest],
        Awaitable[resources.SearchAds360Link],
    ]:
        r"""Return a callable for the create search ads360 link method over gRPC.

        Creates a SearchAds360Link.

        Returns:
            Callable[[~.CreateSearchAds360LinkRequest],
                    Awaitable[~.SearchAds360Link]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_search_ads360_link" not in self._stubs:
            self._stubs["create_search_ads360_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateSearchAds360Link",
                request_serializer=analytics_admin.CreateSearchAds360LinkRequest.serialize,
                response_deserializer=resources.SearchAds360Link.deserialize,
            )
        return self._stubs["create_search_ads360_link"]

    @property
    def delete_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteSearchAds360LinkRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete search ads360 link method over gRPC.

        Deletes a SearchAds360Link on a property.

        Returns:
            Callable[[~.DeleteSearchAds360LinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_search_ads360_link" not in self._stubs:
            self._stubs["delete_search_ads360_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteSearchAds360Link",
                request_serializer=analytics_admin.DeleteSearchAds360LinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_search_ads360_link"]

    @property
    def update_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSearchAds360LinkRequest],
        Awaitable[resources.SearchAds360Link],
    ]:
        r"""Return a callable for the update search ads360 link method over gRPC.

        Updates a SearchAds360Link on a property.

        Returns:
            Callable[[~.UpdateSearchAds360LinkRequest],
                    Awaitable[~.SearchAds360Link]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_search_ads360_link" not in self._stubs:
            self._stubs["update_search_ads360_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateSearchAds360Link",
                request_serializer=analytics_admin.UpdateSearchAds360LinkRequest.serialize,
                response_deserializer=resources.SearchAds360Link.deserialize,
            )
        return self._stubs["update_search_ads360_link"]

    @property
    def get_attribution_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetAttributionSettingsRequest],
        Awaitable[resources.AttributionSettings],
    ]:
        r"""Return a callable for the get attribution settings method over gRPC.

        Lookup for a AttributionSettings singleton.

        Returns:
            Callable[[~.GetAttributionSettingsRequest],
                    Awaitable[~.AttributionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_attribution_settings" not in self._stubs:
            self._stubs["get_attribution_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetAttributionSettings",
                request_serializer=analytics_admin.GetAttributionSettingsRequest.serialize,
                response_deserializer=resources.AttributionSettings.deserialize,
            )
        return self._stubs["get_attribution_settings"]

    @property
    def update_attribution_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAttributionSettingsRequest],
        Awaitable[resources.AttributionSettings],
    ]:
        r"""Return a callable for the update attribution settings method over gRPC.

        Updates attribution settings on a property.

        Returns:
            Callable[[~.UpdateAttributionSettingsRequest],
                    Awaitable[~.AttributionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_attribution_settings" not in self._stubs:
            self._stubs["update_attribution_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateAttributionSettings",
                request_serializer=analytics_admin.UpdateAttributionSettingsRequest.serialize,
                response_deserializer=resources.AttributionSettings.deserialize,
            )
        return self._stubs["update_attribution_settings"]

    @property
    def run_access_report(
        self,
    ) -> Callable[
        [analytics_admin.RunAccessReportRequest],
        Awaitable[analytics_admin.RunAccessReportResponse],
    ]:
        r"""Return a callable for the run access report method over gRPC.

        Returns a customized report of data access records. The report
        provides records of each time a user reads Google Analytics
        reporting data. Access records are retained for up to 2 years.

        Data Access Reports can be requested for a property. Reports may
        be requested for any property, but dimensions that aren't
        related to quota can only be requested on Google Analytics 360
        properties. This method is only available to Administrators.

        These data access records include GA4 UI Reporting, GA4 UI
        Explorations, GA4 Data API, and other products like Firebase &
        Admob that can retrieve data from Google Analytics through a
        linkage. These records don't include property configuration
        changes like adding a stream or changing a property's time zone.
        For configuration change history, see
        `searchChangeHistoryEvents <https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/searchChangeHistoryEvents>`__.

        Returns:
            Callable[[~.RunAccessReportRequest],
                    Awaitable[~.RunAccessReportResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_access_report" not in self._stubs:
            self._stubs["run_access_report"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/RunAccessReport",
                request_serializer=analytics_admin.RunAccessReportRequest.serialize,
                response_deserializer=analytics_admin.RunAccessReportResponse.deserialize,
            )
        return self._stubs["run_access_report"]

    @property
    def create_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.CreateAccessBindingRequest], Awaitable[resources.AccessBinding]
    ]:
        r"""Return a callable for the create access binding method over gRPC.

        Creates an access binding on an account or property.

        Returns:
            Callable[[~.CreateAccessBindingRequest],
                    Awaitable[~.AccessBinding]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_access_binding" not in self._stubs:
            self._stubs["create_access_binding"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateAccessBinding",
                request_serializer=analytics_admin.CreateAccessBindingRequest.serialize,
                response_deserializer=resources.AccessBinding.deserialize,
            )
        return self._stubs["create_access_binding"]

    @property
    def get_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.GetAccessBindingRequest], Awaitable[resources.AccessBinding]
    ]:
        r"""Return a callable for the get access binding method over gRPC.

        Gets information about an access binding.

        Returns:
            Callable[[~.GetAccessBindingRequest],
                    Awaitable[~.AccessBinding]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_access_binding" not in self._stubs:
            self._stubs["get_access_binding"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetAccessBinding",
                request_serializer=analytics_admin.GetAccessBindingRequest.serialize,
                response_deserializer=resources.AccessBinding.deserialize,
            )
        return self._stubs["get_access_binding"]

    @property
    def update_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAccessBindingRequest], Awaitable[resources.AccessBinding]
    ]:
        r"""Return a callable for the update access binding method over gRPC.

        Updates an access binding on an account or property.

        Returns:
            Callable[[~.UpdateAccessBindingRequest],
                    Awaitable[~.AccessBinding]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_access_binding" not in self._stubs:
            self._stubs["update_access_binding"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateAccessBinding",
                request_serializer=analytics_admin.UpdateAccessBindingRequest.serialize,
                response_deserializer=resources.AccessBinding.deserialize,
            )
        return self._stubs["update_access_binding"]

    @property
    def delete_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.DeleteAccessBindingRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete access binding method over gRPC.

        Deletes an access binding on an account or property.

        Returns:
            Callable[[~.DeleteAccessBindingRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_access_binding" not in self._stubs:
            self._stubs["delete_access_binding"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteAccessBinding",
                request_serializer=analytics_admin.DeleteAccessBindingRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_access_binding"]

    @property
    def list_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.ListAccessBindingsRequest],
        Awaitable[analytics_admin.ListAccessBindingsResponse],
    ]:
        r"""Return a callable for the list access bindings method over gRPC.

        Lists all access bindings on an account or property.

        Returns:
            Callable[[~.ListAccessBindingsRequest],
                    Awaitable[~.ListAccessBindingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_access_bindings" not in self._stubs:
            self._stubs["list_access_bindings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListAccessBindings",
                request_serializer=analytics_admin.ListAccessBindingsRequest.serialize,
                response_deserializer=analytics_admin.ListAccessBindingsResponse.deserialize,
            )
        return self._stubs["list_access_bindings"]

    @property
    def batch_create_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchCreateAccessBindingsRequest],
        Awaitable[analytics_admin.BatchCreateAccessBindingsResponse],
    ]:
        r"""Return a callable for the batch create access bindings method over gRPC.

        Creates information about multiple access bindings to
        an account or property.

        This method is transactional. If any AccessBinding
        cannot be created, none of the AccessBindings will be
        created.

        Returns:
            Callable[[~.BatchCreateAccessBindingsRequest],
                    Awaitable[~.BatchCreateAccessBindingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_access_bindings" not in self._stubs:
            self._stubs["batch_create_access_bindings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchCreateAccessBindings",
                request_serializer=analytics_admin.BatchCreateAccessBindingsRequest.serialize,
                response_deserializer=analytics_admin.BatchCreateAccessBindingsResponse.deserialize,
            )
        return self._stubs["batch_create_access_bindings"]

    @property
    def batch_get_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchGetAccessBindingsRequest],
        Awaitable[analytics_admin.BatchGetAccessBindingsResponse],
    ]:
        r"""Return a callable for the batch get access bindings method over gRPC.

        Gets information about multiple access bindings to an
        account or property.

        Returns:
            Callable[[~.BatchGetAccessBindingsRequest],
                    Awaitable[~.BatchGetAccessBindingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_get_access_bindings" not in self._stubs:
            self._stubs["batch_get_access_bindings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchGetAccessBindings",
                request_serializer=analytics_admin.BatchGetAccessBindingsRequest.serialize,
                response_deserializer=analytics_admin.BatchGetAccessBindingsResponse.deserialize,
            )
        return self._stubs["batch_get_access_bindings"]

    @property
    def batch_update_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchUpdateAccessBindingsRequest],
        Awaitable[analytics_admin.BatchUpdateAccessBindingsResponse],
    ]:
        r"""Return a callable for the batch update access bindings method over gRPC.

        Updates information about multiple access bindings to
        an account or property.

        Returns:
            Callable[[~.BatchUpdateAccessBindingsRequest],
                    Awaitable[~.BatchUpdateAccessBindingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_update_access_bindings" not in self._stubs:
            self._stubs["batch_update_access_bindings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchUpdateAccessBindings",
                request_serializer=analytics_admin.BatchUpdateAccessBindingsRequest.serialize,
                response_deserializer=analytics_admin.BatchUpdateAccessBindingsResponse.deserialize,
            )
        return self._stubs["batch_update_access_bindings"]

    @property
    def batch_delete_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchDeleteAccessBindingsRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the batch delete access bindings method over gRPC.

        Deletes information about multiple users' links to an
        account or property.

        Returns:
            Callable[[~.BatchDeleteAccessBindingsRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_delete_access_bindings" not in self._stubs:
            self._stubs["batch_delete_access_bindings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchDeleteAccessBindings",
                request_serializer=analytics_admin.BatchDeleteAccessBindingsRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["batch_delete_access_bindings"]

    @property
    def get_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.GetExpandedDataSetRequest],
        Awaitable[expanded_data_set.ExpandedDataSet],
    ]:
        r"""Return a callable for the get expanded data set method over gRPC.

        Lookup for a single ExpandedDataSet.

        Returns:
            Callable[[~.GetExpandedDataSetRequest],
                    Awaitable[~.ExpandedDataSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_expanded_data_set" not in self._stubs:
            self._stubs["get_expanded_data_set"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetExpandedDataSet",
                request_serializer=analytics_admin.GetExpandedDataSetRequest.serialize,
                response_deserializer=expanded_data_set.ExpandedDataSet.deserialize,
            )
        return self._stubs["get_expanded_data_set"]

    @property
    def list_expanded_data_sets(
        self,
    ) -> Callable[
        [analytics_admin.ListExpandedDataSetsRequest],
        Awaitable[analytics_admin.ListExpandedDataSetsResponse],
    ]:
        r"""Return a callable for the list expanded data sets method over gRPC.

        Lists ExpandedDataSets on a property.

        Returns:
            Callable[[~.ListExpandedDataSetsRequest],
                    Awaitable[~.ListExpandedDataSetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_expanded_data_sets" not in self._stubs:
            self._stubs["list_expanded_data_sets"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListExpandedDataSets",
                request_serializer=analytics_admin.ListExpandedDataSetsRequest.serialize,
                response_deserializer=analytics_admin.ListExpandedDataSetsResponse.deserialize,
            )
        return self._stubs["list_expanded_data_sets"]

    @property
    def create_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.CreateExpandedDataSetRequest],
        Awaitable[gaa_expanded_data_set.ExpandedDataSet],
    ]:
        r"""Return a callable for the create expanded data set method over gRPC.

        Creates a ExpandedDataSet.

        Returns:
            Callable[[~.CreateExpandedDataSetRequest],
                    Awaitable[~.ExpandedDataSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_expanded_data_set" not in self._stubs:
            self._stubs["create_expanded_data_set"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateExpandedDataSet",
                request_serializer=analytics_admin.CreateExpandedDataSetRequest.serialize,
                response_deserializer=gaa_expanded_data_set.ExpandedDataSet.deserialize,
            )
        return self._stubs["create_expanded_data_set"]

    @property
    def update_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.UpdateExpandedDataSetRequest],
        Awaitable[gaa_expanded_data_set.ExpandedDataSet],
    ]:
        r"""Return a callable for the update expanded data set method over gRPC.

        Updates a ExpandedDataSet on a property.

        Returns:
            Callable[[~.UpdateExpandedDataSetRequest],
                    Awaitable[~.ExpandedDataSet]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_expanded_data_set" not in self._stubs:
            self._stubs["update_expanded_data_set"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateExpandedDataSet",
                request_serializer=analytics_admin.UpdateExpandedDataSetRequest.serialize,
                response_deserializer=gaa_expanded_data_set.ExpandedDataSet.deserialize,
            )
        return self._stubs["update_expanded_data_set"]

    @property
    def delete_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.DeleteExpandedDataSetRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete expanded data set method over gRPC.

        Deletes a ExpandedDataSet on a property.

        Returns:
            Callable[[~.DeleteExpandedDataSetRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_expanded_data_set" not in self._stubs:
            self._stubs["delete_expanded_data_set"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteExpandedDataSet",
                request_serializer=analytics_admin.DeleteExpandedDataSetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_expanded_data_set"]

    @property
    def get_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.GetChannelGroupRequest], Awaitable[channel_group.ChannelGroup]
    ]:
        r"""Return a callable for the get channel group method over gRPC.

        Lookup for a single ChannelGroup.

        Returns:
            Callable[[~.GetChannelGroupRequest],
                    Awaitable[~.ChannelGroup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_channel_group" not in self._stubs:
            self._stubs["get_channel_group"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetChannelGroup",
                request_serializer=analytics_admin.GetChannelGroupRequest.serialize,
                response_deserializer=channel_group.ChannelGroup.deserialize,
            )
        return self._stubs["get_channel_group"]

    @property
    def list_channel_groups(
        self,
    ) -> Callable[
        [analytics_admin.ListChannelGroupsRequest],
        Awaitable[analytics_admin.ListChannelGroupsResponse],
    ]:
        r"""Return a callable for the list channel groups method over gRPC.

        Lists ChannelGroups on a property.

        Returns:
            Callable[[~.ListChannelGroupsRequest],
                    Awaitable[~.ListChannelGroupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_channel_groups" not in self._stubs:
            self._stubs["list_channel_groups"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListChannelGroups",
                request_serializer=analytics_admin.ListChannelGroupsRequest.serialize,
                response_deserializer=analytics_admin.ListChannelGroupsResponse.deserialize,
            )
        return self._stubs["list_channel_groups"]

    @property
    def create_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.CreateChannelGroupRequest],
        Awaitable[gaa_channel_group.ChannelGroup],
    ]:
        r"""Return a callable for the create channel group method over gRPC.

        Creates a ChannelGroup.

        Returns:
            Callable[[~.CreateChannelGroupRequest],
                    Awaitable[~.ChannelGroup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_channel_group" not in self._stubs:
            self._stubs["create_channel_group"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateChannelGroup",
                request_serializer=analytics_admin.CreateChannelGroupRequest.serialize,
                response_deserializer=gaa_channel_group.ChannelGroup.deserialize,
            )
        return self._stubs["create_channel_group"]

    @property
    def update_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.UpdateChannelGroupRequest],
        Awaitable[gaa_channel_group.ChannelGroup],
    ]:
        r"""Return a callable for the update channel group method over gRPC.

        Updates a ChannelGroup.

        Returns:
            Callable[[~.UpdateChannelGroupRequest],
                    Awaitable[~.ChannelGroup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_channel_group" not in self._stubs:
            self._stubs["update_channel_group"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateChannelGroup",
                request_serializer=analytics_admin.UpdateChannelGroupRequest.serialize,
                response_deserializer=gaa_channel_group.ChannelGroup.deserialize,
            )
        return self._stubs["update_channel_group"]

    @property
    def delete_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.DeleteChannelGroupRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete channel group method over gRPC.

        Deletes a ChannelGroup on a property.

        Returns:
            Callable[[~.DeleteChannelGroupRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_channel_group" not in self._stubs:
            self._stubs["delete_channel_group"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteChannelGroup",
                request_serializer=analytics_admin.DeleteChannelGroupRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_channel_group"]

    @property
    def set_automated_ga4_configuration_opt_out(
        self,
    ) -> Callable[
        [analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest],
        Awaitable[analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse],
    ]:
        r"""Return a callable for the set automated ga4
        configuration opt out method over gRPC.

        Sets the opt out status for the automated GA4 setup
        process for a UA property.
        Note: this has no effect on GA4 property.

        Returns:
            Callable[[~.SetAutomatedGa4ConfigurationOptOutRequest],
                    Awaitable[~.SetAutomatedGa4ConfigurationOptOutResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_automated_ga4_configuration_opt_out" not in self._stubs:
            self._stubs[
                "set_automated_ga4_configuration_opt_out"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/SetAutomatedGa4ConfigurationOptOut",
                request_serializer=analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest.serialize,
                response_deserializer=analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse.deserialize,
            )
        return self._stubs["set_automated_ga4_configuration_opt_out"]

    @property
    def fetch_automated_ga4_configuration_opt_out(
        self,
    ) -> Callable[
        [analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest],
        Awaitable[analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse],
    ]:
        r"""Return a callable for the fetch automated ga4
        configuration opt out method over gRPC.

        Fetches the opt out status for the automated GA4
        setup process for a UA property.
        Note: this has no effect on GA4 property.

        Returns:
            Callable[[~.FetchAutomatedGa4ConfigurationOptOutRequest],
                    Awaitable[~.FetchAutomatedGa4ConfigurationOptOutResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_automated_ga4_configuration_opt_out" not in self._stubs:
            self._stubs[
                "fetch_automated_ga4_configuration_opt_out"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/FetchAutomatedGa4ConfigurationOptOut",
                request_serializer=analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest.serialize,
                response_deserializer=analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse.deserialize,
            )
        return self._stubs["fetch_automated_ga4_configuration_opt_out"]

    @property
    def create_big_query_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateBigQueryLinkRequest], Awaitable[resources.BigQueryLink]
    ]:
        r"""Return a callable for the create big query link method over gRPC.

        Creates a BigQueryLink.

        Returns:
            Callable[[~.CreateBigQueryLinkRequest],
                    Awaitable[~.BigQueryLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_big_query_link" not in self._stubs:
            self._stubs["create_big_query_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateBigQueryLink",
                request_serializer=analytics_admin.CreateBigQueryLinkRequest.serialize,
                response_deserializer=resources.BigQueryLink.deserialize,
            )
        return self._stubs["create_big_query_link"]

    @property
    def get_big_query_link(
        self,
    ) -> Callable[
        [analytics_admin.GetBigQueryLinkRequest], Awaitable[resources.BigQueryLink]
    ]:
        r"""Return a callable for the get big query link method over gRPC.

        Lookup for a single BigQuery Link.

        Returns:
            Callable[[~.GetBigQueryLinkRequest],
                    Awaitable[~.BigQueryLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_big_query_link" not in self._stubs:
            self._stubs["get_big_query_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetBigQueryLink",
                request_serializer=analytics_admin.GetBigQueryLinkRequest.serialize,
                response_deserializer=resources.BigQueryLink.deserialize,
            )
        return self._stubs["get_big_query_link"]

    @property
    def list_big_query_links(
        self,
    ) -> Callable[
        [analytics_admin.ListBigQueryLinksRequest],
        Awaitable[analytics_admin.ListBigQueryLinksResponse],
    ]:
        r"""Return a callable for the list big query links method over gRPC.

        Lists BigQuery Links on a property.

        Returns:
            Callable[[~.ListBigQueryLinksRequest],
                    Awaitable[~.ListBigQueryLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_big_query_links" not in self._stubs:
            self._stubs["list_big_query_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListBigQueryLinks",
                request_serializer=analytics_admin.ListBigQueryLinksRequest.serialize,
                response_deserializer=analytics_admin.ListBigQueryLinksResponse.deserialize,
            )
        return self._stubs["list_big_query_links"]

    @property
    def delete_big_query_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteBigQueryLinkRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete big query link method over gRPC.

        Deletes a BigQueryLink on a property.

        Returns:
            Callable[[~.DeleteBigQueryLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_big_query_link" not in self._stubs:
            self._stubs["delete_big_query_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteBigQueryLink",
                request_serializer=analytics_admin.DeleteBigQueryLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_big_query_link"]

    @property
    def update_big_query_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateBigQueryLinkRequest], Awaitable[resources.BigQueryLink]
    ]:
        r"""Return a callable for the update big query link method over gRPC.

        Updates a BigQueryLink.

        Returns:
            Callable[[~.UpdateBigQueryLinkRequest],
                    Awaitable[~.BigQueryLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_big_query_link" not in self._stubs:
            self._stubs["update_big_query_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateBigQueryLink",
                request_serializer=analytics_admin.UpdateBigQueryLinkRequest.serialize,
                response_deserializer=resources.BigQueryLink.deserialize,
            )
        return self._stubs["update_big_query_link"]

    @property
    def get_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetEnhancedMeasurementSettingsRequest],
        Awaitable[resources.EnhancedMeasurementSettings],
    ]:
        r"""Return a callable for the get enhanced measurement
        settings method over gRPC.

        Returns the enhanced measurement settings for this
        data stream. Note that the stream must enable enhanced
        measurement for these settings to take effect.

        Returns:
            Callable[[~.GetEnhancedMeasurementSettingsRequest],
                    Awaitable[~.EnhancedMeasurementSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_enhanced_measurement_settings" not in self._stubs:
            self._stubs[
                "get_enhanced_measurement_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetEnhancedMeasurementSettings",
                request_serializer=analytics_admin.GetEnhancedMeasurementSettingsRequest.serialize,
                response_deserializer=resources.EnhancedMeasurementSettings.deserialize,
            )
        return self._stubs["get_enhanced_measurement_settings"]

    @property
    def update_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEnhancedMeasurementSettingsRequest],
        Awaitable[resources.EnhancedMeasurementSettings],
    ]:
        r"""Return a callable for the update enhanced measurement
        settings method over gRPC.

        Updates the enhanced measurement settings for this
        data stream. Note that the stream must enable enhanced
        measurement for these settings to take effect.

        Returns:
            Callable[[~.UpdateEnhancedMeasurementSettingsRequest],
                    Awaitable[~.EnhancedMeasurementSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_enhanced_measurement_settings" not in self._stubs:
            self._stubs[
                "update_enhanced_measurement_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateEnhancedMeasurementSettings",
                request_serializer=analytics_admin.UpdateEnhancedMeasurementSettingsRequest.serialize,
                response_deserializer=resources.EnhancedMeasurementSettings.deserialize,
            )
        return self._stubs["update_enhanced_measurement_settings"]

    @property
    def create_connected_site_tag(
        self,
    ) -> Callable[
        [analytics_admin.CreateConnectedSiteTagRequest],
        Awaitable[analytics_admin.CreateConnectedSiteTagResponse],
    ]:
        r"""Return a callable for the create connected site tag method over gRPC.

        Creates a connected site tag for a Universal
        Analytics property. You can create a maximum of 20
        connected site tags per property. Note: This API cannot
        be used on GA4 properties.

        Returns:
            Callable[[~.CreateConnectedSiteTagRequest],
                    Awaitable[~.CreateConnectedSiteTagResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_connected_site_tag" not in self._stubs:
            self._stubs["create_connected_site_tag"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateConnectedSiteTag",
                request_serializer=analytics_admin.CreateConnectedSiteTagRequest.serialize,
                response_deserializer=analytics_admin.CreateConnectedSiteTagResponse.deserialize,
            )
        return self._stubs["create_connected_site_tag"]

    @property
    def delete_connected_site_tag(
        self,
    ) -> Callable[
        [analytics_admin.DeleteConnectedSiteTagRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete connected site tag method over gRPC.

        Deletes a connected site tag for a Universal
        Analytics property. Note: this has no effect on GA4
        properties.

        Returns:
            Callable[[~.DeleteConnectedSiteTagRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_connected_site_tag" not in self._stubs:
            self._stubs["delete_connected_site_tag"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteConnectedSiteTag",
                request_serializer=analytics_admin.DeleteConnectedSiteTagRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_connected_site_tag"]

    @property
    def list_connected_site_tags(
        self,
    ) -> Callable[
        [analytics_admin.ListConnectedSiteTagsRequest],
        Awaitable[analytics_admin.ListConnectedSiteTagsResponse],
    ]:
        r"""Return a callable for the list connected site tags method over gRPC.

        Lists the connected site tags for a Universal
        Analytics property. A maximum of 20 connected site tags
        will be returned. Note: this has no effect on GA4
        property.

        Returns:
            Callable[[~.ListConnectedSiteTagsRequest],
                    Awaitable[~.ListConnectedSiteTagsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_connected_site_tags" not in self._stubs:
            self._stubs["list_connected_site_tags"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListConnectedSiteTags",
                request_serializer=analytics_admin.ListConnectedSiteTagsRequest.serialize,
                response_deserializer=analytics_admin.ListConnectedSiteTagsResponse.deserialize,
            )
        return self._stubs["list_connected_site_tags"]

    @property
    def fetch_connected_ga4_property(
        self,
    ) -> Callable[
        [analytics_admin.FetchConnectedGa4PropertyRequest],
        Awaitable[analytics_admin.FetchConnectedGa4PropertyResponse],
    ]:
        r"""Return a callable for the fetch connected ga4 property method over gRPC.

        Given a specified UA property, looks up the GA4
        property connected to it. Note: this cannot be used with
        GA4 properties.

        Returns:
            Callable[[~.FetchConnectedGa4PropertyRequest],
                    Awaitable[~.FetchConnectedGa4PropertyResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_connected_ga4_property" not in self._stubs:
            self._stubs["fetch_connected_ga4_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/FetchConnectedGa4Property",
                request_serializer=analytics_admin.FetchConnectedGa4PropertyRequest.serialize,
                response_deserializer=analytics_admin.FetchConnectedGa4PropertyResponse.deserialize,
            )
        return self._stubs["fetch_connected_ga4_property"]

    @property
    def get_ad_sense_link(
        self,
    ) -> Callable[
        [analytics_admin.GetAdSenseLinkRequest], Awaitable[resources.AdSenseLink]
    ]:
        r"""Return a callable for the get ad sense link method over gRPC.

        Looks up a single AdSenseLink.

        Returns:
            Callable[[~.GetAdSenseLinkRequest],
                    Awaitable[~.AdSenseLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_ad_sense_link" not in self._stubs:
            self._stubs["get_ad_sense_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetAdSenseLink",
                request_serializer=analytics_admin.GetAdSenseLinkRequest.serialize,
                response_deserializer=resources.AdSenseLink.deserialize,
            )
        return self._stubs["get_ad_sense_link"]

    @property
    def create_ad_sense_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateAdSenseLinkRequest], Awaitable[resources.AdSenseLink]
    ]:
        r"""Return a callable for the create ad sense link method over gRPC.

        Creates an AdSenseLink.

        Returns:
            Callable[[~.CreateAdSenseLinkRequest],
                    Awaitable[~.AdSenseLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_ad_sense_link" not in self._stubs:
            self._stubs["create_ad_sense_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateAdSenseLink",
                request_serializer=analytics_admin.CreateAdSenseLinkRequest.serialize,
                response_deserializer=resources.AdSenseLink.deserialize,
            )
        return self._stubs["create_ad_sense_link"]

    @property
    def delete_ad_sense_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteAdSenseLinkRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete ad sense link method over gRPC.

        Deletes an AdSenseLink.

        Returns:
            Callable[[~.DeleteAdSenseLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_ad_sense_link" not in self._stubs:
            self._stubs["delete_ad_sense_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteAdSenseLink",
                request_serializer=analytics_admin.DeleteAdSenseLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_ad_sense_link"]

    @property
    def list_ad_sense_links(
        self,
    ) -> Callable[
        [analytics_admin.ListAdSenseLinksRequest],
        Awaitable[analytics_admin.ListAdSenseLinksResponse],
    ]:
        r"""Return a callable for the list ad sense links method over gRPC.

        Lists AdSenseLinks on a property.

        Returns:
            Callable[[~.ListAdSenseLinksRequest],
                    Awaitable[~.ListAdSenseLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_ad_sense_links" not in self._stubs:
            self._stubs["list_ad_sense_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListAdSenseLinks",
                request_serializer=analytics_admin.ListAdSenseLinksRequest.serialize,
                response_deserializer=analytics_admin.ListAdSenseLinksResponse.deserialize,
            )
        return self._stubs["list_ad_sense_links"]

    @property
    def get_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.GetEventCreateRuleRequest],
        Awaitable[event_create_and_edit.EventCreateRule],
    ]:
        r"""Return a callable for the get event create rule method over gRPC.

        Lookup for a single EventCreateRule.

        Returns:
            Callable[[~.GetEventCreateRuleRequest],
                    Awaitable[~.EventCreateRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_event_create_rule" not in self._stubs:
            self._stubs["get_event_create_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetEventCreateRule",
                request_serializer=analytics_admin.GetEventCreateRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventCreateRule.deserialize,
            )
        return self._stubs["get_event_create_rule"]

    @property
    def list_event_create_rules(
        self,
    ) -> Callable[
        [analytics_admin.ListEventCreateRulesRequest],
        Awaitable[analytics_admin.ListEventCreateRulesResponse],
    ]:
        r"""Return a callable for the list event create rules method over gRPC.

        Lists EventCreateRules on a web data stream.

        Returns:
            Callable[[~.ListEventCreateRulesRequest],
                    Awaitable[~.ListEventCreateRulesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_event_create_rules" not in self._stubs:
            self._stubs["list_event_create_rules"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListEventCreateRules",
                request_serializer=analytics_admin.ListEventCreateRulesRequest.serialize,
                response_deserializer=analytics_admin.ListEventCreateRulesResponse.deserialize,
            )
        return self._stubs["list_event_create_rules"]

    @property
    def create_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.CreateEventCreateRuleRequest],
        Awaitable[event_create_and_edit.EventCreateRule],
    ]:
        r"""Return a callable for the create event create rule method over gRPC.

        Creates an EventCreateRule.

        Returns:
            Callable[[~.CreateEventCreateRuleRequest],
                    Awaitable[~.EventCreateRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_event_create_rule" not in self._stubs:
            self._stubs["create_event_create_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateEventCreateRule",
                request_serializer=analytics_admin.CreateEventCreateRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventCreateRule.deserialize,
            )
        return self._stubs["create_event_create_rule"]

    @property
    def update_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEventCreateRuleRequest],
        Awaitable[event_create_and_edit.EventCreateRule],
    ]:
        r"""Return a callable for the update event create rule method over gRPC.

        Updates an EventCreateRule.

        Returns:
            Callable[[~.UpdateEventCreateRuleRequest],
                    Awaitable[~.EventCreateRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_event_create_rule" not in self._stubs:
            self._stubs["update_event_create_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateEventCreateRule",
                request_serializer=analytics_admin.UpdateEventCreateRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventCreateRule.deserialize,
            )
        return self._stubs["update_event_create_rule"]

    @property
    def delete_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.DeleteEventCreateRuleRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete event create rule method over gRPC.

        Deletes an EventCreateRule.

        Returns:
            Callable[[~.DeleteEventCreateRuleRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_event_create_rule" not in self._stubs:
            self._stubs["delete_event_create_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteEventCreateRule",
                request_serializer=analytics_admin.DeleteEventCreateRuleRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_event_create_rule"]

    @property
    def get_event_edit_rule(
        self,
    ) -> Callable[
        [analytics_admin.GetEventEditRuleRequest],
        Awaitable[event_create_and_edit.EventEditRule],
    ]:
        r"""Return a callable for the get event edit rule method over gRPC.

        Lookup for a single EventEditRule.

        Returns:
            Callable[[~.GetEventEditRuleRequest],
                    Awaitable[~.EventEditRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_event_edit_rule" not in self._stubs:
            self._stubs["get_event_edit_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetEventEditRule",
                request_serializer=analytics_admin.GetEventEditRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventEditRule.deserialize,
            )
        return self._stubs["get_event_edit_rule"]

    @property
    def list_event_edit_rules(
        self,
    ) -> Callable[
        [analytics_admin.ListEventEditRulesRequest],
        Awaitable[analytics_admin.ListEventEditRulesResponse],
    ]:
        r"""Return a callable for the list event edit rules method over gRPC.

        Lists EventEditRules on a web data stream.

        Returns:
            Callable[[~.ListEventEditRulesRequest],
                    Awaitable[~.ListEventEditRulesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_event_edit_rules" not in self._stubs:
            self._stubs["list_event_edit_rules"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListEventEditRules",
                request_serializer=analytics_admin.ListEventEditRulesRequest.serialize,
                response_deserializer=analytics_admin.ListEventEditRulesResponse.deserialize,
            )
        return self._stubs["list_event_edit_rules"]

    @property
    def create_event_edit_rule(
        self,
    ) -> Callable[
        [analytics_admin.CreateEventEditRuleRequest],
        Awaitable[event_create_and_edit.EventEditRule],
    ]:
        r"""Return a callable for the create event edit rule method over gRPC.

        Creates an EventEditRule.

        Returns:
            Callable[[~.CreateEventEditRuleRequest],
                    Awaitable[~.EventEditRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_event_edit_rule" not in self._stubs:
            self._stubs["create_event_edit_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateEventEditRule",
                request_serializer=analytics_admin.CreateEventEditRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventEditRule.deserialize,
            )
        return self._stubs["create_event_edit_rule"]

    @property
    def update_event_edit_rule(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEventEditRuleRequest],
        Awaitable[event_create_and_edit.EventEditRule],
    ]:
        r"""Return a callable for the update event edit rule method over gRPC.

        Updates an EventEditRule.

        Returns:
            Callable[[~.UpdateEventEditRuleRequest],
                    Awaitable[~.EventEditRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_event_edit_rule" not in self._stubs:
            self._stubs["update_event_edit_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateEventEditRule",
                request_serializer=analytics_admin.UpdateEventEditRuleRequest.serialize,
                response_deserializer=event_create_and_edit.EventEditRule.deserialize,
            )
        return self._stubs["update_event_edit_rule"]

    @property
    def delete_event_edit_rule(
        self,
    ) -> Callable[
        [analytics_admin.DeleteEventEditRuleRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete event edit rule method over gRPC.

        Deletes an EventEditRule.

        Returns:
            Callable[[~.DeleteEventEditRuleRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_event_edit_rule" not in self._stubs:
            self._stubs["delete_event_edit_rule"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteEventEditRule",
                request_serializer=analytics_admin.DeleteEventEditRuleRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_event_edit_rule"]

    @property
    def reorder_event_edit_rules(
        self,
    ) -> Callable[
        [analytics_admin.ReorderEventEditRulesRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the reorder event edit rules method over gRPC.

        Changes the processing order of event edit rules on
        the specified stream.

        Returns:
            Callable[[~.ReorderEventEditRulesRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reorder_event_edit_rules" not in self._stubs:
            self._stubs["reorder_event_edit_rules"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ReorderEventEditRules",
                request_serializer=analytics_admin.ReorderEventEditRulesRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["reorder_event_edit_rules"]

    @property
    def update_data_redaction_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDataRedactionSettingsRequest],
        Awaitable[resources.DataRedactionSettings],
    ]:
        r"""Return a callable for the update data redaction settings method over gRPC.

        Updates a DataRedactionSettings on a property.

        Returns:
            Callable[[~.UpdateDataRedactionSettingsRequest],
                    Awaitable[~.DataRedactionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_redaction_settings" not in self._stubs:
            self._stubs[
                "update_data_redaction_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateDataRedactionSettings",
                request_serializer=analytics_admin.UpdateDataRedactionSettingsRequest.serialize,
                response_deserializer=resources.DataRedactionSettings.deserialize,
            )
        return self._stubs["update_data_redaction_settings"]

    @property
    def get_data_redaction_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataRedactionSettingsRequest],
        Awaitable[resources.DataRedactionSettings],
    ]:
        r"""Return a callable for the get data redaction settings method over gRPC.

        Lookup for a single DataRedactionSettings.

        Returns:
            Callable[[~.GetDataRedactionSettingsRequest],
                    Awaitable[~.DataRedactionSettings]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_redaction_settings" not in self._stubs:
            self._stubs["get_data_redaction_settings"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetDataRedactionSettings",
                request_serializer=analytics_admin.GetDataRedactionSettingsRequest.serialize,
                response_deserializer=resources.DataRedactionSettings.deserialize,
            )
        return self._stubs["get_data_redaction_settings"]

    @property
    def get_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.GetCalculatedMetricRequest],
        Awaitable[resources.CalculatedMetric],
    ]:
        r"""Return a callable for the get calculated metric method over gRPC.

        Lookup for a single CalculatedMetric.

        Returns:
            Callable[[~.GetCalculatedMetricRequest],
                    Awaitable[~.CalculatedMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_calculated_metric" not in self._stubs:
            self._stubs["get_calculated_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetCalculatedMetric",
                request_serializer=analytics_admin.GetCalculatedMetricRequest.serialize,
                response_deserializer=resources.CalculatedMetric.deserialize,
            )
        return self._stubs["get_calculated_metric"]

    @property
    def create_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.CreateCalculatedMetricRequest],
        Awaitable[resources.CalculatedMetric],
    ]:
        r"""Return a callable for the create calculated metric method over gRPC.

        Creates a CalculatedMetric.

        Returns:
            Callable[[~.CreateCalculatedMetricRequest],
                    Awaitable[~.CalculatedMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_calculated_metric" not in self._stubs:
            self._stubs["create_calculated_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateCalculatedMetric",
                request_serializer=analytics_admin.CreateCalculatedMetricRequest.serialize,
                response_deserializer=resources.CalculatedMetric.deserialize,
            )
        return self._stubs["create_calculated_metric"]

    @property
    def list_calculated_metrics(
        self,
    ) -> Callable[
        [analytics_admin.ListCalculatedMetricsRequest],
        Awaitable[analytics_admin.ListCalculatedMetricsResponse],
    ]:
        r"""Return a callable for the list calculated metrics method over gRPC.

        Lists CalculatedMetrics on a property.

        Returns:
            Callable[[~.ListCalculatedMetricsRequest],
                    Awaitable[~.ListCalculatedMetricsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_calculated_metrics" not in self._stubs:
            self._stubs["list_calculated_metrics"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListCalculatedMetrics",
                request_serializer=analytics_admin.ListCalculatedMetricsRequest.serialize,
                response_deserializer=analytics_admin.ListCalculatedMetricsResponse.deserialize,
            )
        return self._stubs["list_calculated_metrics"]

    @property
    def update_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCalculatedMetricRequest],
        Awaitable[resources.CalculatedMetric],
    ]:
        r"""Return a callable for the update calculated metric method over gRPC.

        Updates a CalculatedMetric on a property.

        Returns:
            Callable[[~.UpdateCalculatedMetricRequest],
                    Awaitable[~.CalculatedMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_calculated_metric" not in self._stubs:
            self._stubs["update_calculated_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateCalculatedMetric",
                request_serializer=analytics_admin.UpdateCalculatedMetricRequest.serialize,
                response_deserializer=resources.CalculatedMetric.deserialize,
            )
        return self._stubs["update_calculated_metric"]

    @property
    def delete_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.DeleteCalculatedMetricRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete calculated metric method over gRPC.

        Deletes a CalculatedMetric on a property.

        Returns:
            Callable[[~.DeleteCalculatedMetricRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_calculated_metric" not in self._stubs:
            self._stubs["delete_calculated_metric"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteCalculatedMetric",
                request_serializer=analytics_admin.DeleteCalculatedMetricRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_calculated_metric"]

    @property
    def create_rollup_property(
        self,
    ) -> Callable[
        [analytics_admin.CreateRollupPropertyRequest],
        Awaitable[analytics_admin.CreateRollupPropertyResponse],
    ]:
        r"""Return a callable for the create rollup property method over gRPC.

        Create a roll-up property and all roll-up property
        source links.

        Returns:
            Callable[[~.CreateRollupPropertyRequest],
                    Awaitable[~.CreateRollupPropertyResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_rollup_property" not in self._stubs:
            self._stubs["create_rollup_property"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateRollupProperty",
                request_serializer=analytics_admin.CreateRollupPropertyRequest.serialize,
                response_deserializer=analytics_admin.CreateRollupPropertyResponse.deserialize,
            )
        return self._stubs["create_rollup_property"]

    @property
    def get_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.GetRollupPropertySourceLinkRequest],
        Awaitable[resources.RollupPropertySourceLink],
    ]:
        r"""Return a callable for the get rollup property source
        link method over gRPC.

        Lookup for a single roll-up property source Link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Returns:
            Callable[[~.GetRollupPropertySourceLinkRequest],
                    Awaitable[~.RollupPropertySourceLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_rollup_property_source_link" not in self._stubs:
            self._stubs[
                "get_rollup_property_source_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetRollupPropertySourceLink",
                request_serializer=analytics_admin.GetRollupPropertySourceLinkRequest.serialize,
                response_deserializer=resources.RollupPropertySourceLink.deserialize,
            )
        return self._stubs["get_rollup_property_source_link"]

    @property
    def list_rollup_property_source_links(
        self,
    ) -> Callable[
        [analytics_admin.ListRollupPropertySourceLinksRequest],
        Awaitable[analytics_admin.ListRollupPropertySourceLinksResponse],
    ]:
        r"""Return a callable for the list rollup property source
        links method over gRPC.

        Lists roll-up property source Links on a property.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Returns:
            Callable[[~.ListRollupPropertySourceLinksRequest],
                    Awaitable[~.ListRollupPropertySourceLinksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_rollup_property_source_links" not in self._stubs:
            self._stubs[
                "list_rollup_property_source_links"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListRollupPropertySourceLinks",
                request_serializer=analytics_admin.ListRollupPropertySourceLinksRequest.serialize,
                response_deserializer=analytics_admin.ListRollupPropertySourceLinksResponse.deserialize,
            )
        return self._stubs["list_rollup_property_source_links"]

    @property
    def create_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateRollupPropertySourceLinkRequest],
        Awaitable[resources.RollupPropertySourceLink],
    ]:
        r"""Return a callable for the create rollup property source
        link method over gRPC.

        Creates a roll-up property source link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Returns:
            Callable[[~.CreateRollupPropertySourceLinkRequest],
                    Awaitable[~.RollupPropertySourceLink]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_rollup_property_source_link" not in self._stubs:
            self._stubs[
                "create_rollup_property_source_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateRollupPropertySourceLink",
                request_serializer=analytics_admin.CreateRollupPropertySourceLinkRequest.serialize,
                response_deserializer=resources.RollupPropertySourceLink.deserialize,
            )
        return self._stubs["create_rollup_property_source_link"]

    @property
    def delete_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteRollupPropertySourceLinkRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete rollup property source
        link method over gRPC.

        Deletes a roll-up property source link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Returns:
            Callable[[~.DeleteRollupPropertySourceLinkRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_rollup_property_source_link" not in self._stubs:
            self._stubs[
                "delete_rollup_property_source_link"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteRollupPropertySourceLink",
                request_serializer=analytics_admin.DeleteRollupPropertySourceLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_rollup_property_source_link"]

    @property
    def provision_subproperty(
        self,
    ) -> Callable[
        [analytics_admin.ProvisionSubpropertyRequest],
        Awaitable[analytics_admin.ProvisionSubpropertyResponse],
    ]:
        r"""Return a callable for the provision subproperty method over gRPC.

        Create a subproperty and a subproperty event filter
        that applies to the created subproperty.

        Returns:
            Callable[[~.ProvisionSubpropertyRequest],
                    Awaitable[~.ProvisionSubpropertyResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "provision_subproperty" not in self._stubs:
            self._stubs["provision_subproperty"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ProvisionSubproperty",
                request_serializer=analytics_admin.ProvisionSubpropertyRequest.serialize,
                response_deserializer=analytics_admin.ProvisionSubpropertyResponse.deserialize,
            )
        return self._stubs["provision_subproperty"]

    @property
    def create_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.CreateSubpropertyEventFilterRequest],
        Awaitable[gaa_subproperty_event_filter.SubpropertyEventFilter],
    ]:
        r"""Return a callable for the create subproperty event
        filter method over gRPC.

        Creates a subproperty Event Filter.

        Returns:
            Callable[[~.CreateSubpropertyEventFilterRequest],
                    Awaitable[~.SubpropertyEventFilter]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_subproperty_event_filter" not in self._stubs:
            self._stubs[
                "create_subproperty_event_filter"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateSubpropertyEventFilter",
                request_serializer=analytics_admin.CreateSubpropertyEventFilterRequest.serialize,
                response_deserializer=gaa_subproperty_event_filter.SubpropertyEventFilter.deserialize,
            )
        return self._stubs["create_subproperty_event_filter"]

    @property
    def get_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.GetSubpropertyEventFilterRequest],
        Awaitable[subproperty_event_filter.SubpropertyEventFilter],
    ]:
        r"""Return a callable for the get subproperty event filter method over gRPC.

        Lookup for a single subproperty Event Filter.

        Returns:
            Callable[[~.GetSubpropertyEventFilterRequest],
                    Awaitable[~.SubpropertyEventFilter]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_subproperty_event_filter" not in self._stubs:
            self._stubs["get_subproperty_event_filter"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetSubpropertyEventFilter",
                request_serializer=analytics_admin.GetSubpropertyEventFilterRequest.serialize,
                response_deserializer=subproperty_event_filter.SubpropertyEventFilter.deserialize,
            )
        return self._stubs["get_subproperty_event_filter"]

    @property
    def list_subproperty_event_filters(
        self,
    ) -> Callable[
        [analytics_admin.ListSubpropertyEventFiltersRequest],
        Awaitable[analytics_admin.ListSubpropertyEventFiltersResponse],
    ]:
        r"""Return a callable for the list subproperty event filters method over gRPC.

        List all subproperty Event Filters on a property.

        Returns:
            Callable[[~.ListSubpropertyEventFiltersRequest],
                    Awaitable[~.ListSubpropertyEventFiltersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_subproperty_event_filters" not in self._stubs:
            self._stubs[
                "list_subproperty_event_filters"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListSubpropertyEventFilters",
                request_serializer=analytics_admin.ListSubpropertyEventFiltersRequest.serialize,
                response_deserializer=analytics_admin.ListSubpropertyEventFiltersResponse.deserialize,
            )
        return self._stubs["list_subproperty_event_filters"]

    @property
    def update_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSubpropertyEventFilterRequest],
        Awaitable[gaa_subproperty_event_filter.SubpropertyEventFilter],
    ]:
        r"""Return a callable for the update subproperty event
        filter method over gRPC.

        Updates a subproperty Event Filter.

        Returns:
            Callable[[~.UpdateSubpropertyEventFilterRequest],
                    Awaitable[~.SubpropertyEventFilter]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_subproperty_event_filter" not in self._stubs:
            self._stubs[
                "update_subproperty_event_filter"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateSubpropertyEventFilter",
                request_serializer=analytics_admin.UpdateSubpropertyEventFilterRequest.serialize,
                response_deserializer=gaa_subproperty_event_filter.SubpropertyEventFilter.deserialize,
            )
        return self._stubs["update_subproperty_event_filter"]

    @property
    def delete_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.DeleteSubpropertyEventFilterRequest],
        Awaitable[empty_pb2.Empty],
    ]:
        r"""Return a callable for the delete subproperty event
        filter method over gRPC.

        Deletes a subproperty event filter.

        Returns:
            Callable[[~.DeleteSubpropertyEventFilterRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_subproperty_event_filter" not in self._stubs:
            self._stubs[
                "delete_subproperty_event_filter"
            ] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteSubpropertyEventFilter",
                request_serializer=analytics_admin.DeleteSubpropertyEventFilterRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_subproperty_event_filter"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.get_account: self._wrap_method(
                self.get_account,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_accounts: self._wrap_method(
                self.list_accounts,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_account: self._wrap_method(
                self.delete_account,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_account: self._wrap_method(
                self.update_account,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.provision_account_ticket: self._wrap_method(
                self.provision_account_ticket,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_account_summaries: self._wrap_method(
                self.list_account_summaries,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_property: self._wrap_method(
                self.get_property,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_properties: self._wrap_method(
                self.list_properties,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_property: self._wrap_method(
                self.create_property,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_property: self._wrap_method(
                self.delete_property,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_property: self._wrap_method(
                self.update_property,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_firebase_link: self._wrap_method(
                self.create_firebase_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_firebase_link: self._wrap_method(
                self.delete_firebase_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_firebase_links: self._wrap_method(
                self.list_firebase_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_global_site_tag: self._wrap_method(
                self.get_global_site_tag,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_google_ads_link: self._wrap_method(
                self.create_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_google_ads_link: self._wrap_method(
                self.update_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_google_ads_link: self._wrap_method(
                self.delete_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_google_ads_links: self._wrap_method(
                self.list_google_ads_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_data_sharing_settings: self._wrap_method(
                self.get_data_sharing_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_measurement_protocol_secret: self._wrap_method(
                self.get_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_measurement_protocol_secrets: self._wrap_method(
                self.list_measurement_protocol_secrets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_measurement_protocol_secret: self._wrap_method(
                self.create_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_measurement_protocol_secret: self._wrap_method(
                self.delete_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_measurement_protocol_secret: self._wrap_method(
                self.update_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.acknowledge_user_data_collection: self._wrap_method(
                self.acknowledge_user_data_collection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_sk_ad_network_conversion_value_schema: self._wrap_method(
                self.get_sk_ad_network_conversion_value_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_sk_ad_network_conversion_value_schema: self._wrap_method(
                self.create_sk_ad_network_conversion_value_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_sk_ad_network_conversion_value_schema: self._wrap_method(
                self.delete_sk_ad_network_conversion_value_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_sk_ad_network_conversion_value_schema: self._wrap_method(
                self.update_sk_ad_network_conversion_value_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_sk_ad_network_conversion_value_schemas: self._wrap_method(
                self.list_sk_ad_network_conversion_value_schemas,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_change_history_events: self._wrap_method(
                self.search_change_history_events,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_google_signals_settings: self._wrap_method(
                self.get_google_signals_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_google_signals_settings: self._wrap_method(
                self.update_google_signals_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_conversion_event: self._wrap_method(
                self.create_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_conversion_event: self._wrap_method(
                self.update_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_conversion_event: self._wrap_method(
                self.get_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_conversion_event: self._wrap_method(
                self.delete_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_conversion_events: self._wrap_method(
                self.list_conversion_events,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_key_event: self._wrap_method(
                self.create_key_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_key_event: self._wrap_method(
                self.update_key_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_key_event: self._wrap_method(
                self.get_key_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_key_event: self._wrap_method(
                self.delete_key_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_key_events: self._wrap_method(
                self.list_key_events,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_display_video360_advertiser_link: self._wrap_method(
                self.get_display_video360_advertiser_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_display_video360_advertiser_links: self._wrap_method(
                self.list_display_video360_advertiser_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_display_video360_advertiser_link: self._wrap_method(
                self.create_display_video360_advertiser_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_display_video360_advertiser_link: self._wrap_method(
                self.delete_display_video360_advertiser_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_display_video360_advertiser_link: self._wrap_method(
                self.update_display_video360_advertiser_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_display_video360_advertiser_link_proposal: self._wrap_method(
                self.get_display_video360_advertiser_link_proposal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_display_video360_advertiser_link_proposals: self._wrap_method(
                self.list_display_video360_advertiser_link_proposals,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_display_video360_advertiser_link_proposal: self._wrap_method(
                self.create_display_video360_advertiser_link_proposal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_display_video360_advertiser_link_proposal: self._wrap_method(
                self.delete_display_video360_advertiser_link_proposal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.approve_display_video360_advertiser_link_proposal: self._wrap_method(
                self.approve_display_video360_advertiser_link_proposal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_display_video360_advertiser_link_proposal: self._wrap_method(
                self.cancel_display_video360_advertiser_link_proposal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_custom_dimension: self._wrap_method(
                self.create_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_custom_dimension: self._wrap_method(
                self.update_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_custom_dimensions: self._wrap_method(
                self.list_custom_dimensions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.archive_custom_dimension: self._wrap_method(
                self.archive_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_custom_dimension: self._wrap_method(
                self.get_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_custom_metric: self._wrap_method(
                self.create_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_custom_metric: self._wrap_method(
                self.update_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_custom_metrics: self._wrap_method(
                self.list_custom_metrics,
                default_timeout=None,
                client_info=client_info,
            ),
            self.archive_custom_metric: self._wrap_method(
                self.archive_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_custom_metric: self._wrap_method(
                self.get_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_retention_settings: self._wrap_method(
                self.get_data_retention_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_data_retention_settings: self._wrap_method(
                self.update_data_retention_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_data_stream: self._wrap_method(
                self.create_data_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_data_stream: self._wrap_method(
                self.delete_data_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_data_stream: self._wrap_method(
                self.update_data_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_data_streams: self._wrap_method(
                self.list_data_streams,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_stream: self._wrap_method(
                self.get_data_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_audience: self._wrap_method(
                self.get_audience,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_audiences: self._wrap_method(
                self.list_audiences,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_audience: self._wrap_method(
                self.create_audience,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_audience: self._wrap_method(
                self.update_audience,
                default_timeout=None,
                client_info=client_info,
            ),
            self.archive_audience: self._wrap_method(
                self.archive_audience,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_search_ads360_link: self._wrap_method(
                self.get_search_ads360_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_search_ads360_links: self._wrap_method(
                self.list_search_ads360_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_search_ads360_link: self._wrap_method(
                self.create_search_ads360_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_search_ads360_link: self._wrap_method(
                self.delete_search_ads360_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_search_ads360_link: self._wrap_method(
                self.update_search_ads360_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_attribution_settings: self._wrap_method(
                self.get_attribution_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_attribution_settings: self._wrap_method(
                self.update_attribution_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.run_access_report: self._wrap_method(
                self.run_access_report,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_access_binding: self._wrap_method(
                self.create_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_access_binding: self._wrap_method(
                self.get_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_access_binding: self._wrap_method(
                self.update_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_access_binding: self._wrap_method(
                self.delete_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_access_bindings: self._wrap_method(
                self.list_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_create_access_bindings: self._wrap_method(
                self.batch_create_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_get_access_bindings: self._wrap_method(
                self.batch_get_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_update_access_bindings: self._wrap_method(
                self.batch_update_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_delete_access_bindings: self._wrap_method(
                self.batch_delete_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_expanded_data_set: self._wrap_method(
                self.get_expanded_data_set,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_expanded_data_sets: self._wrap_method(
                self.list_expanded_data_sets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_expanded_data_set: self._wrap_method(
                self.create_expanded_data_set,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_expanded_data_set: self._wrap_method(
                self.update_expanded_data_set,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_expanded_data_set: self._wrap_method(
                self.delete_expanded_data_set,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_channel_group: self._wrap_method(
                self.get_channel_group,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_channel_groups: self._wrap_method(
                self.list_channel_groups,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_channel_group: self._wrap_method(
                self.create_channel_group,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_channel_group: self._wrap_method(
                self.update_channel_group,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_channel_group: self._wrap_method(
                self.delete_channel_group,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_automated_ga4_configuration_opt_out: self._wrap_method(
                self.set_automated_ga4_configuration_opt_out,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_automated_ga4_configuration_opt_out: self._wrap_method(
                self.fetch_automated_ga4_configuration_opt_out,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_big_query_link: self._wrap_method(
                self.create_big_query_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_big_query_link: self._wrap_method(
                self.get_big_query_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_big_query_links: self._wrap_method(
                self.list_big_query_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_big_query_link: self._wrap_method(
                self.delete_big_query_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_big_query_link: self._wrap_method(
                self.update_big_query_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_enhanced_measurement_settings: self._wrap_method(
                self.get_enhanced_measurement_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_enhanced_measurement_settings: self._wrap_method(
                self.update_enhanced_measurement_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_connected_site_tag: self._wrap_method(
                self.create_connected_site_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_connected_site_tag: self._wrap_method(
                self.delete_connected_site_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_connected_site_tags: self._wrap_method(
                self.list_connected_site_tags,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_connected_ga4_property: self._wrap_method(
                self.fetch_connected_ga4_property,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_ad_sense_link: self._wrap_method(
                self.get_ad_sense_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_ad_sense_link: self._wrap_method(
                self.create_ad_sense_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_ad_sense_link: self._wrap_method(
                self.delete_ad_sense_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_ad_sense_links: self._wrap_method(
                self.list_ad_sense_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_event_create_rule: self._wrap_method(
                self.get_event_create_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_event_create_rules: self._wrap_method(
                self.list_event_create_rules,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_event_create_rule: self._wrap_method(
                self.create_event_create_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_event_create_rule: self._wrap_method(
                self.update_event_create_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_event_create_rule: self._wrap_method(
                self.delete_event_create_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_event_edit_rule: self._wrap_method(
                self.get_event_edit_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_event_edit_rules: self._wrap_method(
                self.list_event_edit_rules,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_event_edit_rule: self._wrap_method(
                self.create_event_edit_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_event_edit_rule: self._wrap_method(
                self.update_event_edit_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_event_edit_rule: self._wrap_method(
                self.delete_event_edit_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.reorder_event_edit_rules: self._wrap_method(
                self.reorder_event_edit_rules,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_data_redaction_settings: self._wrap_method(
                self.update_data_redaction_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_redaction_settings: self._wrap_method(
                self.get_data_redaction_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_calculated_metric: self._wrap_method(
                self.get_calculated_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_calculated_metric: self._wrap_method(
                self.create_calculated_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_calculated_metrics: self._wrap_method(
                self.list_calculated_metrics,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_calculated_metric: self._wrap_method(
                self.update_calculated_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_calculated_metric: self._wrap_method(
                self.delete_calculated_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_rollup_property: self._wrap_method(
                self.create_rollup_property,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_rollup_property_source_link: self._wrap_method(
                self.get_rollup_property_source_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_rollup_property_source_links: self._wrap_method(
                self.list_rollup_property_source_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_rollup_property_source_link: self._wrap_method(
                self.create_rollup_property_source_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_rollup_property_source_link: self._wrap_method(
                self.delete_rollup_property_source_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.provision_subproperty: self._wrap_method(
                self.provision_subproperty,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_subproperty_event_filter: self._wrap_method(
                self.create_subproperty_event_filter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_subproperty_event_filter: self._wrap_method(
                self.get_subproperty_event_filter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_subproperty_event_filters: self._wrap_method(
                self.list_subproperty_event_filters,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_subproperty_event_filter: self._wrap_method(
                self.update_subproperty_event_filter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_subproperty_event_filter: self._wrap_method(
                self.delete_subproperty_event_filter,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("AnalyticsAdminServiceGrpcAsyncIOTransport",)
