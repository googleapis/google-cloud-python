# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.analytics.admin_v1alpha.types import analytics_admin, resources

from .base import DEFAULT_CLIENT_INFO, AnalyticsAdminServiceTransport


class AnalyticsAdminServiceGrpcTransport(AnalyticsAdminServiceTransport):
    """gRPC backend transport for AnalyticsAdminService.

    Service Interface for the Analytics Admin API (GA4).

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
        host: str = "analyticsadmin.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
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
        host: str = "analyticsadmin.googleapis.com",
        credentials: ga_credentials.Credentials = None,
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
    def get_account(
        self,
    ) -> Callable[[analytics_admin.GetAccountRequest], resources.Account]:
        r"""Return a callable for the get account method over gRPC.

        Lookup for a single Account.

        Returns:
            Callable[[~.GetAccountRequest],
                    ~.Account]:
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
        [analytics_admin.ListAccountsRequest], analytics_admin.ListAccountsResponse
    ]:
        r"""Return a callable for the list accounts method over gRPC.

        Returns all accounts accessible by the caller.
        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        Returns:
            Callable[[~.ListAccountsRequest],
                    ~.ListAccountsResponse]:
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
    ) -> Callable[[analytics_admin.DeleteAccountRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete account method over gRPC.

        Marks target Account as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        accounts. However, they can be restored using the Trash
        Can UI.
        If the accounts are not restored before the expiration
        time, the account and all child resources (eg:
        Properties, GoogleAdsLinks, Streams, UserLinks) will be
        permanently purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found.

        Returns:
            Callable[[~.DeleteAccountRequest],
                    ~.Empty]:
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
    ) -> Callable[[analytics_admin.UpdateAccountRequest], resources.Account]:
        r"""Return a callable for the update account method over gRPC.

        Updates an account.

        Returns:
            Callable[[~.UpdateAccountRequest],
                    ~.Account]:
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
        analytics_admin.ProvisionAccountTicketResponse,
    ]:
        r"""Return a callable for the provision account ticket method over gRPC.

        Requests a ticket for creating an account.

        Returns:
            Callable[[~.ProvisionAccountTicketRequest],
                    ~.ProvisionAccountTicketResponse]:
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
        analytics_admin.ListAccountSummariesResponse,
    ]:
        r"""Return a callable for the list account summaries method over gRPC.

        Returns summaries of all accounts accessible by the
        caller.

        Returns:
            Callable[[~.ListAccountSummariesRequest],
                    ~.ListAccountSummariesResponse]:
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
    ) -> Callable[[analytics_admin.GetPropertyRequest], resources.Property]:
        r"""Return a callable for the get property method over gRPC.

        Lookup for a single "GA4" Property.

        Returns:
            Callable[[~.GetPropertyRequest],
                    ~.Property]:
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
        [analytics_admin.ListPropertiesRequest], analytics_admin.ListPropertiesResponse
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
                    ~.ListPropertiesResponse]:
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
    ) -> Callable[[analytics_admin.CreatePropertyRequest], resources.Property]:
        r"""Return a callable for the create property method over gRPC.

        Creates an "GA4" property with the specified location
        and attributes.

        Returns:
            Callable[[~.CreatePropertyRequest],
                    ~.Property]:
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
    ) -> Callable[[analytics_admin.DeletePropertyRequest], resources.Property]:
        r"""Return a callable for the delete property method over gRPC.

        Marks target Property as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        properties. However, they can be restored using the
        Trash Can UI.
        If the properties are not restored before the expiration
        time, the Property and all child resources (eg:
        GoogleAdsLinks, Streams, UserLinks) will be permanently
        purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found, or is not
        an GA4 Property.

        Returns:
            Callable[[~.DeletePropertyRequest],
                    ~.Property]:
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
    ) -> Callable[[analytics_admin.UpdatePropertyRequest], resources.Property]:
        r"""Return a callable for the update property method over gRPC.

        Updates a property.

        Returns:
            Callable[[~.UpdatePropertyRequest],
                    ~.Property]:
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
    def get_user_link(
        self,
    ) -> Callable[[analytics_admin.GetUserLinkRequest], resources.UserLink]:
        r"""Return a callable for the get user link method over gRPC.

        Gets information about a user's link to an account or
        property.

        Returns:
            Callable[[~.GetUserLinkRequest],
                    ~.UserLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_user_link" not in self._stubs:
            self._stubs["get_user_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/GetUserLink",
                request_serializer=analytics_admin.GetUserLinkRequest.serialize,
                response_deserializer=resources.UserLink.deserialize,
            )
        return self._stubs["get_user_link"]

    @property
    def batch_get_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchGetUserLinksRequest],
        analytics_admin.BatchGetUserLinksResponse,
    ]:
        r"""Return a callable for the batch get user links method over gRPC.

        Gets information about multiple users' links to an
        account or property.

        Returns:
            Callable[[~.BatchGetUserLinksRequest],
                    ~.BatchGetUserLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_get_user_links" not in self._stubs:
            self._stubs["batch_get_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchGetUserLinks",
                request_serializer=analytics_admin.BatchGetUserLinksRequest.serialize,
                response_deserializer=analytics_admin.BatchGetUserLinksResponse.deserialize,
            )
        return self._stubs["batch_get_user_links"]

    @property
    def list_user_links(
        self,
    ) -> Callable[
        [analytics_admin.ListUserLinksRequest], analytics_admin.ListUserLinksResponse
    ]:
        r"""Return a callable for the list user links method over gRPC.

        Lists all user links on an account or property.

        Returns:
            Callable[[~.ListUserLinksRequest],
                    ~.ListUserLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_user_links" not in self._stubs:
            self._stubs["list_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/ListUserLinks",
                request_serializer=analytics_admin.ListUserLinksRequest.serialize,
                response_deserializer=analytics_admin.ListUserLinksResponse.deserialize,
            )
        return self._stubs["list_user_links"]

    @property
    def audit_user_links(
        self,
    ) -> Callable[
        [analytics_admin.AuditUserLinksRequest], analytics_admin.AuditUserLinksResponse
    ]:
        r"""Return a callable for the audit user links method over gRPC.

        Lists all user links on an account or property,
        including implicit ones that come from effective
        permissions granted by groups or organization admin
        roles.

        If a returned user link does not have direct
        permissions, they cannot be removed from the account or
        property directly with the DeleteUserLink command. They
        have to be removed from the group/etc that gives them
        permissions, which is currently only usable/discoverable
        in the GA or GMP UIs.

        Returns:
            Callable[[~.AuditUserLinksRequest],
                    ~.AuditUserLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "audit_user_links" not in self._stubs:
            self._stubs["audit_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/AuditUserLinks",
                request_serializer=analytics_admin.AuditUserLinksRequest.serialize,
                response_deserializer=analytics_admin.AuditUserLinksResponse.deserialize,
            )
        return self._stubs["audit_user_links"]

    @property
    def create_user_link(
        self,
    ) -> Callable[[analytics_admin.CreateUserLinkRequest], resources.UserLink]:
        r"""Return a callable for the create user link method over gRPC.

        Creates a user link on an account or property.
        If the user with the specified email already has
        permissions on the account or property, then the user's
        existing permissions will be unioned with the
        permissions specified in the new UserLink.

        Returns:
            Callable[[~.CreateUserLinkRequest],
                    ~.UserLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_user_link" not in self._stubs:
            self._stubs["create_user_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/CreateUserLink",
                request_serializer=analytics_admin.CreateUserLinkRequest.serialize,
                response_deserializer=resources.UserLink.deserialize,
            )
        return self._stubs["create_user_link"]

    @property
    def batch_create_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchCreateUserLinksRequest],
        analytics_admin.BatchCreateUserLinksResponse,
    ]:
        r"""Return a callable for the batch create user links method over gRPC.

        Creates information about multiple users' links to an
        account or property.
        This method is transactional. If any UserLink cannot be
        created, none of the UserLinks will be created.

        Returns:
            Callable[[~.BatchCreateUserLinksRequest],
                    ~.BatchCreateUserLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_user_links" not in self._stubs:
            self._stubs["batch_create_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchCreateUserLinks",
                request_serializer=analytics_admin.BatchCreateUserLinksRequest.serialize,
                response_deserializer=analytics_admin.BatchCreateUserLinksResponse.deserialize,
            )
        return self._stubs["batch_create_user_links"]

    @property
    def update_user_link(
        self,
    ) -> Callable[[analytics_admin.UpdateUserLinkRequest], resources.UserLink]:
        r"""Return a callable for the update user link method over gRPC.

        Updates a user link on an account or property.

        Returns:
            Callable[[~.UpdateUserLinkRequest],
                    ~.UserLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_user_link" not in self._stubs:
            self._stubs["update_user_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/UpdateUserLink",
                request_serializer=analytics_admin.UpdateUserLinkRequest.serialize,
                response_deserializer=resources.UserLink.deserialize,
            )
        return self._stubs["update_user_link"]

    @property
    def batch_update_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchUpdateUserLinksRequest],
        analytics_admin.BatchUpdateUserLinksResponse,
    ]:
        r"""Return a callable for the batch update user links method over gRPC.

        Updates information about multiple users' links to an
        account or property.

        Returns:
            Callable[[~.BatchUpdateUserLinksRequest],
                    ~.BatchUpdateUserLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_update_user_links" not in self._stubs:
            self._stubs["batch_update_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchUpdateUserLinks",
                request_serializer=analytics_admin.BatchUpdateUserLinksRequest.serialize,
                response_deserializer=analytics_admin.BatchUpdateUserLinksResponse.deserialize,
            )
        return self._stubs["batch_update_user_links"]

    @property
    def delete_user_link(
        self,
    ) -> Callable[[analytics_admin.DeleteUserLinkRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete user link method over gRPC.

        Deletes a user link on an account or property.

        Returns:
            Callable[[~.DeleteUserLinkRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_user_link" not in self._stubs:
            self._stubs["delete_user_link"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/DeleteUserLink",
                request_serializer=analytics_admin.DeleteUserLinkRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_user_link"]

    @property
    def batch_delete_user_links(
        self,
    ) -> Callable[[analytics_admin.BatchDeleteUserLinksRequest], empty_pb2.Empty]:
        r"""Return a callable for the batch delete user links method over gRPC.

        Deletes information about multiple users' links to an
        account or property.

        Returns:
            Callable[[~.BatchDeleteUserLinksRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_delete_user_links" not in self._stubs:
            self._stubs["batch_delete_user_links"] = self.grpc_channel.unary_unary(
                "/google.analytics.admin.v1alpha.AnalyticsAdminService/BatchDeleteUserLinks",
                request_serializer=analytics_admin.BatchDeleteUserLinksRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["batch_delete_user_links"]

    @property
    def create_firebase_link(
        self,
    ) -> Callable[[analytics_admin.CreateFirebaseLinkRequest], resources.FirebaseLink]:
        r"""Return a callable for the create firebase link method over gRPC.

        Creates a FirebaseLink.
        Properties can have at most one FirebaseLink.

        Returns:
            Callable[[~.CreateFirebaseLinkRequest],
                    ~.FirebaseLink]:
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
    ) -> Callable[[analytics_admin.DeleteFirebaseLinkRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete firebase link method over gRPC.

        Deletes a FirebaseLink on a property

        Returns:
            Callable[[~.DeleteFirebaseLinkRequest],
                    ~.Empty]:
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
        analytics_admin.ListFirebaseLinksResponse,
    ]:
        r"""Return a callable for the list firebase links method over gRPC.

        Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        Returns:
            Callable[[~.ListFirebaseLinksRequest],
                    ~.ListFirebaseLinksResponse]:
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
    ) -> Callable[[analytics_admin.GetGlobalSiteTagRequest], resources.GlobalSiteTag]:
        r"""Return a callable for the get global site tag method over gRPC.

        Returns the Site Tag for the specified web stream.
        Site Tags are immutable singletons.

        Returns:
            Callable[[~.GetGlobalSiteTagRequest],
                    ~.GlobalSiteTag]:
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
        [analytics_admin.CreateGoogleAdsLinkRequest], resources.GoogleAdsLink
    ]:
        r"""Return a callable for the create google ads link method over gRPC.

        Creates a GoogleAdsLink.

        Returns:
            Callable[[~.CreateGoogleAdsLinkRequest],
                    ~.GoogleAdsLink]:
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
        [analytics_admin.UpdateGoogleAdsLinkRequest], resources.GoogleAdsLink
    ]:
        r"""Return a callable for the update google ads link method over gRPC.

        Updates a GoogleAdsLink on a property

        Returns:
            Callable[[~.UpdateGoogleAdsLinkRequest],
                    ~.GoogleAdsLink]:
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
    ) -> Callable[[analytics_admin.DeleteGoogleAdsLinkRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete google ads link method over gRPC.

        Deletes a GoogleAdsLink on a property

        Returns:
            Callable[[~.DeleteGoogleAdsLinkRequest],
                    ~.Empty]:
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
        analytics_admin.ListGoogleAdsLinksResponse,
    ]:
        r"""Return a callable for the list google ads links method over gRPC.

        Lists GoogleAdsLinks on a property.

        Returns:
            Callable[[~.ListGoogleAdsLinksRequest],
                    ~.ListGoogleAdsLinksResponse]:
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
        [analytics_admin.GetDataSharingSettingsRequest], resources.DataSharingSettings
    ]:
        r"""Return a callable for the get data sharing settings method over gRPC.

        Get data sharing settings on an account.
        Data sharing settings are singletons.

        Returns:
            Callable[[~.GetDataSharingSettingsRequest],
                    ~.DataSharingSettings]:
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
        resources.MeasurementProtocolSecret,
    ]:
        r"""Return a callable for the get measurement protocol
        secret method over gRPC.

        Lookup for a single "GA4" MeasurementProtocolSecret.

        Returns:
            Callable[[~.GetMeasurementProtocolSecretRequest],
                    ~.MeasurementProtocolSecret]:
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
        analytics_admin.ListMeasurementProtocolSecretsResponse,
    ]:
        r"""Return a callable for the list measurement protocol
        secrets method over gRPC.

        Returns child MeasurementProtocolSecrets under the
        specified parent Property.

        Returns:
            Callable[[~.ListMeasurementProtocolSecretsRequest],
                    ~.ListMeasurementProtocolSecretsResponse]:
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
        resources.MeasurementProtocolSecret,
    ]:
        r"""Return a callable for the create measurement protocol
        secret method over gRPC.

        Creates a measurement protocol secret.

        Returns:
            Callable[[~.CreateMeasurementProtocolSecretRequest],
                    ~.MeasurementProtocolSecret]:
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
        [analytics_admin.DeleteMeasurementProtocolSecretRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the delete measurement protocol
        secret method over gRPC.

        Deletes target MeasurementProtocolSecret.

        Returns:
            Callable[[~.DeleteMeasurementProtocolSecretRequest],
                    ~.Empty]:
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
        resources.MeasurementProtocolSecret,
    ]:
        r"""Return a callable for the update measurement protocol
        secret method over gRPC.

        Updates a measurement protocol secret.

        Returns:
            Callable[[~.UpdateMeasurementProtocolSecretRequest],
                    ~.MeasurementProtocolSecret]:
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
        analytics_admin.AcknowledgeUserDataCollectionResponse,
    ]:
        r"""Return a callable for the acknowledge user data
        collection method over gRPC.

        Acknowledges the terms of user data collection for
        the specified property.
        This acknowledgement must be completed (either in the
        Google Analytics UI or via this API) before
        MeasurementProtocolSecret resources may be created.

        Returns:
            Callable[[~.AcknowledgeUserDataCollectionRequest],
                    ~.AcknowledgeUserDataCollectionResponse]:
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
    def search_change_history_events(
        self,
    ) -> Callable[
        [analytics_admin.SearchChangeHistoryEventsRequest],
        analytics_admin.SearchChangeHistoryEventsResponse,
    ]:
        r"""Return a callable for the search change history events method over gRPC.

        Searches through all changes to an account or its
        children given the specified set of filters.

        Returns:
            Callable[[~.SearchChangeHistoryEventsRequest],
                    ~.SearchChangeHistoryEventsResponse]:
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
        resources.GoogleSignalsSettings,
    ]:
        r"""Return a callable for the get google signals settings method over gRPC.

        Lookup for Google Signals settings for a property.

        Returns:
            Callable[[~.GetGoogleSignalsSettingsRequest],
                    ~.GoogleSignalsSettings]:
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
        resources.GoogleSignalsSettings,
    ]:
        r"""Return a callable for the update google signals settings method over gRPC.

        Updates Google Signals settings for a property.

        Returns:
            Callable[[~.UpdateGoogleSignalsSettingsRequest],
                    ~.GoogleSignalsSettings]:
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
        [analytics_admin.CreateConversionEventRequest], resources.ConversionEvent
    ]:
        r"""Return a callable for the create conversion event method over gRPC.

        Creates a conversion event with the specified
        attributes.

        Returns:
            Callable[[~.CreateConversionEventRequest],
                    ~.ConversionEvent]:
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
    def get_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.GetConversionEventRequest], resources.ConversionEvent
    ]:
        r"""Return a callable for the get conversion event method over gRPC.

        Retrieve a single conversion event.

        Returns:
            Callable[[~.GetConversionEventRequest],
                    ~.ConversionEvent]:
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
    ) -> Callable[[analytics_admin.DeleteConversionEventRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete conversion event method over gRPC.

        Deletes a conversion event in a property.

        Returns:
            Callable[[~.DeleteConversionEventRequest],
                    ~.Empty]:
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
        analytics_admin.ListConversionEventsResponse,
    ]:
        r"""Return a callable for the list conversion events method over gRPC.

        Returns a list of conversion events in the specified
        parent property.
        Returns an empty list if no conversion events are found.

        Returns:
            Callable[[~.ListConversionEventsRequest],
                    ~.ListConversionEventsResponse]:
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
    def get_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.GetDisplayVideo360AdvertiserLinkRequest],
        resources.DisplayVideo360AdvertiserLink,
    ]:
        r"""Return a callable for the get display video360
        advertiser link method over gRPC.

        Look up a single DisplayVideo360AdvertiserLink

        Returns:
            Callable[[~.GetDisplayVideo360AdvertiserLinkRequest],
                    ~.DisplayVideo360AdvertiserLink]:
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
        analytics_admin.ListDisplayVideo360AdvertiserLinksResponse,
    ]:
        r"""Return a callable for the list display video360
        advertiser links method over gRPC.

        Lists all DisplayVideo360AdvertiserLinks on a
        property.

        Returns:
            Callable[[~.ListDisplayVideo360AdvertiserLinksRequest],
                    ~.ListDisplayVideo360AdvertiserLinksResponse]:
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
        resources.DisplayVideo360AdvertiserLink,
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
                    ~.DisplayVideo360AdvertiserLink]:
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
        [analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the delete display video360
        advertiser link method over gRPC.

        Deletes a DisplayVideo360AdvertiserLink on a
        property.

        Returns:
            Callable[[~.DeleteDisplayVideo360AdvertiserLinkRequest],
                    ~.Empty]:
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
        resources.DisplayVideo360AdvertiserLink,
    ]:
        r"""Return a callable for the update display video360
        advertiser link method over gRPC.

        Updates a DisplayVideo360AdvertiserLink on a
        property.

        Returns:
            Callable[[~.UpdateDisplayVideo360AdvertiserLinkRequest],
                    ~.DisplayVideo360AdvertiserLink]:
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
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        r"""Return a callable for the get display video360
        advertiser link proposal method over gRPC.

        Lookup for a single
        DisplayVideo360AdvertiserLinkProposal.

        Returns:
            Callable[[~.GetDisplayVideo360AdvertiserLinkProposalRequest],
                    ~.DisplayVideo360AdvertiserLinkProposal]:
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
        analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse,
    ]:
        r"""Return a callable for the list display video360
        advertiser link proposals method over gRPC.

        Lists DisplayVideo360AdvertiserLinkProposals on a
        property.

        Returns:
            Callable[[~.ListDisplayVideo360AdvertiserLinkProposalsRequest],
                    ~.ListDisplayVideo360AdvertiserLinkProposalsResponse]:
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
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        r"""Return a callable for the create display video360
        advertiser link proposal method over gRPC.

        Creates a DisplayVideo360AdvertiserLinkProposal.

        Returns:
            Callable[[~.CreateDisplayVideo360AdvertiserLinkProposalRequest],
                    ~.DisplayVideo360AdvertiserLinkProposal]:
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
        empty_pb2.Empty,
    ]:
        r"""Return a callable for the delete display video360
        advertiser link proposal method over gRPC.

        Deletes a DisplayVideo360AdvertiserLinkProposal on a
        property. This can only be used on cancelled proposals.

        Returns:
            Callable[[~.DeleteDisplayVideo360AdvertiserLinkProposalRequest],
                    ~.Empty]:
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
        analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse,
    ]:
        r"""Return a callable for the approve display video360
        advertiser link proposal method over gRPC.

        Approves a DisplayVideo360AdvertiserLinkProposal.
        The DisplayVideo360AdvertiserLinkProposal will be
        deleted and a new DisplayVideo360AdvertiserLink will be
        created.

        Returns:
            Callable[[~.ApproveDisplayVideo360AdvertiserLinkProposalRequest],
                    ~.ApproveDisplayVideo360AdvertiserLinkProposalResponse]:
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
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        r"""Return a callable for the cancel display video360
        advertiser link proposal method over gRPC.

        Cancels a DisplayVideo360AdvertiserLinkProposal.
        Cancelling can mean either:
        - Declining a proposal initiated from Display & Video
        360 - Withdrawing a proposal initiated from Google
        Analytics After being cancelled, a proposal will
        eventually be deleted automatically.

        Returns:
            Callable[[~.CancelDisplayVideo360AdvertiserLinkProposalRequest],
                    ~.DisplayVideo360AdvertiserLinkProposal]:
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
        [analytics_admin.CreateCustomDimensionRequest], resources.CustomDimension
    ]:
        r"""Return a callable for the create custom dimension method over gRPC.

        Creates a CustomDimension.

        Returns:
            Callable[[~.CreateCustomDimensionRequest],
                    ~.CustomDimension]:
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
        [analytics_admin.UpdateCustomDimensionRequest], resources.CustomDimension
    ]:
        r"""Return a callable for the update custom dimension method over gRPC.

        Updates a CustomDimension on a property.

        Returns:
            Callable[[~.UpdateCustomDimensionRequest],
                    ~.CustomDimension]:
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
        analytics_admin.ListCustomDimensionsResponse,
    ]:
        r"""Return a callable for the list custom dimensions method over gRPC.

        Lists CustomDimensions on a property.

        Returns:
            Callable[[~.ListCustomDimensionsRequest],
                    ~.ListCustomDimensionsResponse]:
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
    ) -> Callable[[analytics_admin.ArchiveCustomDimensionRequest], empty_pb2.Empty]:
        r"""Return a callable for the archive custom dimension method over gRPC.

        Archives a CustomDimension on a property.

        Returns:
            Callable[[~.ArchiveCustomDimensionRequest],
                    ~.Empty]:
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
        [analytics_admin.GetCustomDimensionRequest], resources.CustomDimension
    ]:
        r"""Return a callable for the get custom dimension method over gRPC.

        Lookup for a single CustomDimension.

        Returns:
            Callable[[~.GetCustomDimensionRequest],
                    ~.CustomDimension]:
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
    ) -> Callable[[analytics_admin.CreateCustomMetricRequest], resources.CustomMetric]:
        r"""Return a callable for the create custom metric method over gRPC.

        Creates a CustomMetric.

        Returns:
            Callable[[~.CreateCustomMetricRequest],
                    ~.CustomMetric]:
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
    ) -> Callable[[analytics_admin.UpdateCustomMetricRequest], resources.CustomMetric]:
        r"""Return a callable for the update custom metric method over gRPC.

        Updates a CustomMetric on a property.

        Returns:
            Callable[[~.UpdateCustomMetricRequest],
                    ~.CustomMetric]:
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
        analytics_admin.ListCustomMetricsResponse,
    ]:
        r"""Return a callable for the list custom metrics method over gRPC.

        Lists CustomMetrics on a property.

        Returns:
            Callable[[~.ListCustomMetricsRequest],
                    ~.ListCustomMetricsResponse]:
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
    ) -> Callable[[analytics_admin.ArchiveCustomMetricRequest], empty_pb2.Empty]:
        r"""Return a callable for the archive custom metric method over gRPC.

        Archives a CustomMetric on a property.

        Returns:
            Callable[[~.ArchiveCustomMetricRequest],
                    ~.Empty]:
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
    ) -> Callable[[analytics_admin.GetCustomMetricRequest], resources.CustomMetric]:
        r"""Return a callable for the get custom metric method over gRPC.

        Lookup for a single CustomMetric.

        Returns:
            Callable[[~.GetCustomMetricRequest],
                    ~.CustomMetric]:
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
        resources.DataRetentionSettings,
    ]:
        r"""Return a callable for the get data retention settings method over gRPC.

        Returns the singleton data retention settings for
        this property.

        Returns:
            Callable[[~.GetDataRetentionSettingsRequest],
                    ~.DataRetentionSettings]:
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
        resources.DataRetentionSettings,
    ]:
        r"""Return a callable for the update data retention settings method over gRPC.

        Updates the singleton data retention settings for
        this property.

        Returns:
            Callable[[~.UpdateDataRetentionSettingsRequest],
                    ~.DataRetentionSettings]:
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
    ) -> Callable[[analytics_admin.CreateDataStreamRequest], resources.DataStream]:
        r"""Return a callable for the create data stream method over gRPC.

        Creates a DataStream.

        Returns:
            Callable[[~.CreateDataStreamRequest],
                    ~.DataStream]:
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
    ) -> Callable[[analytics_admin.DeleteDataStreamRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete data stream method over gRPC.

        Deletes a DataStream on a property.

        Returns:
            Callable[[~.DeleteDataStreamRequest],
                    ~.Empty]:
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
    ) -> Callable[[analytics_admin.UpdateDataStreamRequest], resources.DataStream]:
        r"""Return a callable for the update data stream method over gRPC.

        Updates a DataStream on a property.

        Returns:
            Callable[[~.UpdateDataStreamRequest],
                    ~.DataStream]:
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
        analytics_admin.ListDataStreamsResponse,
    ]:
        r"""Return a callable for the list data streams method over gRPC.

        Lists DataStreams on a property.

        Returns:
            Callable[[~.ListDataStreamsRequest],
                    ~.ListDataStreamsResponse]:
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
    ) -> Callable[[analytics_admin.GetDataStreamRequest], resources.DataStream]:
        r"""Return a callable for the get data stream method over gRPC.

        Lookup for a single DataStream.

        Returns:
            Callable[[~.GetDataStreamRequest],
                    ~.DataStream]:
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

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("AnalyticsAdminServiceGrpcTransport",)
