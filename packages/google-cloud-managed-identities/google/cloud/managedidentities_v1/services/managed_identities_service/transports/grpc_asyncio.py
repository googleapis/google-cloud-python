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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.managedidentities_v1.types import managed_identities_service, resource

from .base import DEFAULT_CLIENT_INFO, ManagedIdentitiesServiceTransport
from .grpc import ManagedIdentitiesServiceGrpcTransport


class ManagedIdentitiesServiceGrpcAsyncIOTransport(ManagedIdentitiesServiceTransport):
    """gRPC AsyncIO backend transport for ManagedIdentitiesService.

    API Overview

    The ``managedidentites.googleapis.com`` service implements the
    Google Cloud Managed Identites API for identity services (e.g.
    Microsoft Active Directory).

    The Managed Identities service provides methods to manage
    (create/read/update/delete) domains, reset managed identities admin
    password, add/remove domain controllers in GCP regions and
    add/remove VPC peering.

    Data Model

    The Managed Identities service exposes the following resources:

    -  Locations as global, named as follows:
       ``projects/{project_id}/locations/global``.

    -  Domains, named as follows:
       ``/projects/{project_id}/locations/global/domain/{domain_name}``.

    The ``{domain_name}`` refers to fully qualified domain name in the
    customer project e.g. mydomain.myorganization.com, with the
    following restrictions:

    -  Must contain only lowercase letters, numbers, periods and
       hyphens.
    -  Must start with a letter.
    -  Must contain between 2-64 characters.
    -  Must end with a number or a letter.
    -  Must not start with period.
    -  First segement length (mydomain form example above) shouldn't
       exceed 15 chars.
    -  The last segment cannot be fully numeric.
    -  Must be unique within the customer project.

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
        host: str = "managedidentities.googleapis.com",
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
        host: str = "managedidentities.googleapis.com",
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
                 The hostname to connect to (default: 'managedidentities.googleapis.com').
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

        # Wrap messages. This must be done after self._grpc_channel exists
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
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_microsoft_ad_domain(
        self,
    ) -> Callable[
        [managed_identities_service.CreateMicrosoftAdDomainRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create microsoft ad domain method over gRPC.

        Creates a Microsoft AD domain.

        Returns:
            Callable[[~.CreateMicrosoftAdDomainRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_microsoft_ad_domain" not in self._stubs:
            self._stubs["create_microsoft_ad_domain"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/CreateMicrosoftAdDomain",
                request_serializer=managed_identities_service.CreateMicrosoftAdDomainRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_microsoft_ad_domain"]

    @property
    def reset_admin_password(
        self,
    ) -> Callable[
        [managed_identities_service.ResetAdminPasswordRequest],
        Awaitable[managed_identities_service.ResetAdminPasswordResponse],
    ]:
        r"""Return a callable for the reset admin password method over gRPC.

        Resets a domain's administrator password.

        Returns:
            Callable[[~.ResetAdminPasswordRequest],
                    Awaitable[~.ResetAdminPasswordResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_admin_password" not in self._stubs:
            self._stubs["reset_admin_password"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/ResetAdminPassword",
                request_serializer=managed_identities_service.ResetAdminPasswordRequest.serialize,
                response_deserializer=managed_identities_service.ResetAdminPasswordResponse.deserialize,
            )
        return self._stubs["reset_admin_password"]

    @property
    def list_domains(
        self,
    ) -> Callable[
        [managed_identities_service.ListDomainsRequest],
        Awaitable[managed_identities_service.ListDomainsResponse],
    ]:
        r"""Return a callable for the list domains method over gRPC.

        Lists domains in a project.

        Returns:
            Callable[[~.ListDomainsRequest],
                    Awaitable[~.ListDomainsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_domains" not in self._stubs:
            self._stubs["list_domains"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/ListDomains",
                request_serializer=managed_identities_service.ListDomainsRequest.serialize,
                response_deserializer=managed_identities_service.ListDomainsResponse.deserialize,
            )
        return self._stubs["list_domains"]

    @property
    def get_domain(
        self,
    ) -> Callable[
        [managed_identities_service.GetDomainRequest], Awaitable[resource.Domain]
    ]:
        r"""Return a callable for the get domain method over gRPC.

        Gets information about a domain.

        Returns:
            Callable[[~.GetDomainRequest],
                    Awaitable[~.Domain]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_domain" not in self._stubs:
            self._stubs["get_domain"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/GetDomain",
                request_serializer=managed_identities_service.GetDomainRequest.serialize,
                response_deserializer=resource.Domain.deserialize,
            )
        return self._stubs["get_domain"]

    @property
    def update_domain(
        self,
    ) -> Callable[
        [managed_identities_service.UpdateDomainRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update domain method over gRPC.

        Updates the metadata and configuration of a domain.

        Returns:
            Callable[[~.UpdateDomainRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_domain" not in self._stubs:
            self._stubs["update_domain"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/UpdateDomain",
                request_serializer=managed_identities_service.UpdateDomainRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_domain"]

    @property
    def delete_domain(
        self,
    ) -> Callable[
        [managed_identities_service.DeleteDomainRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete domain method over gRPC.

        Deletes a domain.

        Returns:
            Callable[[~.DeleteDomainRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_domain" not in self._stubs:
            self._stubs["delete_domain"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/DeleteDomain",
                request_serializer=managed_identities_service.DeleteDomainRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_domain"]

    @property
    def attach_trust(
        self,
    ) -> Callable[
        [managed_identities_service.AttachTrustRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the attach trust method over gRPC.

        Adds an AD trust to a domain.

        Returns:
            Callable[[~.AttachTrustRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "attach_trust" not in self._stubs:
            self._stubs["attach_trust"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/AttachTrust",
                request_serializer=managed_identities_service.AttachTrustRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["attach_trust"]

    @property
    def reconfigure_trust(
        self,
    ) -> Callable[
        [managed_identities_service.ReconfigureTrustRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the reconfigure trust method over gRPC.

        Updates the DNS conditional forwarder.

        Returns:
            Callable[[~.ReconfigureTrustRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reconfigure_trust" not in self._stubs:
            self._stubs["reconfigure_trust"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/ReconfigureTrust",
                request_serializer=managed_identities_service.ReconfigureTrustRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reconfigure_trust"]

    @property
    def detach_trust(
        self,
    ) -> Callable[
        [managed_identities_service.DetachTrustRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the detach trust method over gRPC.

        Removes an AD trust.

        Returns:
            Callable[[~.DetachTrustRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "detach_trust" not in self._stubs:
            self._stubs["detach_trust"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/DetachTrust",
                request_serializer=managed_identities_service.DetachTrustRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["detach_trust"]

    @property
    def validate_trust(
        self,
    ) -> Callable[
        [managed_identities_service.ValidateTrustRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the validate trust method over gRPC.

        Validates a trust state, that the target domain is
        reachable, and that the target domain is able to accept
        incoming trust requests.

        Returns:
            Callable[[~.ValidateTrustRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "validate_trust" not in self._stubs:
            self._stubs["validate_trust"] = self.grpc_channel.unary_unary(
                "/google.cloud.managedidentities.v1.ManagedIdentitiesService/ValidateTrust",
                request_serializer=managed_identities_service.ValidateTrustRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["validate_trust"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_microsoft_ad_domain: gapic_v1.method_async.wrap_method(
                self.create_microsoft_ad_domain,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.reset_admin_password: gapic_v1.method_async.wrap_method(
                self.reset_admin_password,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_domains: gapic_v1.method_async.wrap_method(
                self.list_domains,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_domain: gapic_v1.method_async.wrap_method(
                self.get_domain,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_domain: gapic_v1.method_async.wrap_method(
                self.update_domain,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_domain: gapic_v1.method_async.wrap_method(
                self.delete_domain,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.attach_trust: gapic_v1.method_async.wrap_method(
                self.attach_trust,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.reconfigure_trust: gapic_v1.method_async.wrap_method(
                self.reconfigure_trust,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.detach_trust: gapic_v1.method_async.wrap_method(
                self.detach_trust,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.validate_trust: gapic_v1.method_async.wrap_method(
                self.validate_trust,
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()


__all__ = ("ManagedIdentitiesServiceGrpcAsyncIOTransport",)
