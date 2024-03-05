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

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.discoveryengine_v1.types import (
    site_search_engine,
    site_search_engine_service,
)

from .base import DEFAULT_CLIENT_INFO, SiteSearchEngineServiceTransport
from .grpc import SiteSearchEngineServiceGrpcTransport


class SiteSearchEngineServiceGrpcAsyncIOTransport(SiteSearchEngineServiceTransport):
    """gRPC AsyncIO backend transport for SiteSearchEngineService.

    Service for managing site search related resources.

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
        host: str = "discoveryengine.googleapis.com",
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
                This argument is ignored if ``channel`` is provided.
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
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[aio.Channel] = None,
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
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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
    def get_site_search_engine(
        self,
    ) -> Callable[
        [site_search_engine_service.GetSiteSearchEngineRequest],
        Awaitable[site_search_engine.SiteSearchEngine],
    ]:
        r"""Return a callable for the get site search engine method over gRPC.

        Gets the
        [SiteSearchEngine][google.cloud.discoveryengine.v1.SiteSearchEngine].

        Returns:
            Callable[[~.GetSiteSearchEngineRequest],
                    Awaitable[~.SiteSearchEngine]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_site_search_engine" not in self._stubs:
            self._stubs["get_site_search_engine"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/GetSiteSearchEngine",
                request_serializer=site_search_engine_service.GetSiteSearchEngineRequest.serialize,
                response_deserializer=site_search_engine.SiteSearchEngine.deserialize,
            )
        return self._stubs["get_site_search_engine"]

    @property
    def create_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.CreateTargetSiteRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create target site method over gRPC.

        Creates a
        [TargetSite][google.cloud.discoveryengine.v1.TargetSite].

        Returns:
            Callable[[~.CreateTargetSiteRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_target_site" not in self._stubs:
            self._stubs["create_target_site"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/CreateTargetSite",
                request_serializer=site_search_engine_service.CreateTargetSiteRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_target_site"]

    @property
    def batch_create_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.BatchCreateTargetSitesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch create target sites method over gRPC.

        Creates [TargetSite][google.cloud.discoveryengine.v1.TargetSite]
        in a batch.

        Returns:
            Callable[[~.BatchCreateTargetSitesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_target_sites" not in self._stubs:
            self._stubs["batch_create_target_sites"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/BatchCreateTargetSites",
                request_serializer=site_search_engine_service.BatchCreateTargetSitesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_create_target_sites"]

    @property
    def get_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.GetTargetSiteRequest],
        Awaitable[site_search_engine.TargetSite],
    ]:
        r"""Return a callable for the get target site method over gRPC.

        Gets a [TargetSite][google.cloud.discoveryengine.v1.TargetSite].

        Returns:
            Callable[[~.GetTargetSiteRequest],
                    Awaitable[~.TargetSite]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_target_site" not in self._stubs:
            self._stubs["get_target_site"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/GetTargetSite",
                request_serializer=site_search_engine_service.GetTargetSiteRequest.serialize,
                response_deserializer=site_search_engine.TargetSite.deserialize,
            )
        return self._stubs["get_target_site"]

    @property
    def update_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.UpdateTargetSiteRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update target site method over gRPC.

        Updates a
        [TargetSite][google.cloud.discoveryengine.v1.TargetSite].

        Returns:
            Callable[[~.UpdateTargetSiteRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_target_site" not in self._stubs:
            self._stubs["update_target_site"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/UpdateTargetSite",
                request_serializer=site_search_engine_service.UpdateTargetSiteRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_target_site"]

    @property
    def delete_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.DeleteTargetSiteRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete target site method over gRPC.

        Deletes a
        [TargetSite][google.cloud.discoveryengine.v1.TargetSite].

        Returns:
            Callable[[~.DeleteTargetSiteRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_target_site" not in self._stubs:
            self._stubs["delete_target_site"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/DeleteTargetSite",
                request_serializer=site_search_engine_service.DeleteTargetSiteRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_target_site"]

    @property
    def list_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.ListTargetSitesRequest],
        Awaitable[site_search_engine_service.ListTargetSitesResponse],
    ]:
        r"""Return a callable for the list target sites method over gRPC.

        Gets a list of
        [TargetSite][google.cloud.discoveryengine.v1.TargetSite]s.

        Returns:
            Callable[[~.ListTargetSitesRequest],
                    Awaitable[~.ListTargetSitesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_target_sites" not in self._stubs:
            self._stubs["list_target_sites"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/ListTargetSites",
                request_serializer=site_search_engine_service.ListTargetSitesRequest.serialize,
                response_deserializer=site_search_engine_service.ListTargetSitesResponse.deserialize,
            )
        return self._stubs["list_target_sites"]

    @property
    def enable_advanced_site_search(
        self,
    ) -> Callable[
        [site_search_engine_service.EnableAdvancedSiteSearchRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the enable advanced site search method over gRPC.

        Upgrade from basic site search to advanced site
        search.

        Returns:
            Callable[[~.EnableAdvancedSiteSearchRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_advanced_site_search" not in self._stubs:
            self._stubs["enable_advanced_site_search"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/EnableAdvancedSiteSearch",
                request_serializer=site_search_engine_service.EnableAdvancedSiteSearchRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["enable_advanced_site_search"]

    @property
    def disable_advanced_site_search(
        self,
    ) -> Callable[
        [site_search_engine_service.DisableAdvancedSiteSearchRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the disable advanced site search method over gRPC.

        Downgrade from advanced site search to basic site
        search.

        Returns:
            Callable[[~.DisableAdvancedSiteSearchRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_advanced_site_search" not in self._stubs:
            self._stubs["disable_advanced_site_search"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/DisableAdvancedSiteSearch",
                request_serializer=site_search_engine_service.DisableAdvancedSiteSearchRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["disable_advanced_site_search"]

    @property
    def recrawl_uris(
        self,
    ) -> Callable[
        [site_search_engine_service.RecrawlUrisRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the recrawl uris method over gRPC.

        Request on-demand recrawl for a list of URIs.

        Returns:
            Callable[[~.RecrawlUrisRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "recrawl_uris" not in self._stubs:
            self._stubs["recrawl_uris"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/RecrawlUris",
                request_serializer=site_search_engine_service.RecrawlUrisRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["recrawl_uris"]

    @property
    def batch_verify_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.BatchVerifyTargetSitesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch verify target sites method over gRPC.

        Verify target sites' ownership and validity.
        This API sends all the target sites under site search
        engine for verification.

        Returns:
            Callable[[~.BatchVerifyTargetSitesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_verify_target_sites" not in self._stubs:
            self._stubs["batch_verify_target_sites"] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/BatchVerifyTargetSites",
                request_serializer=site_search_engine_service.BatchVerifyTargetSitesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_verify_target_sites"]

    @property
    def fetch_domain_verification_status(
        self,
    ) -> Callable[
        [site_search_engine_service.FetchDomainVerificationStatusRequest],
        Awaitable[site_search_engine_service.FetchDomainVerificationStatusResponse],
    ]:
        r"""Return a callable for the fetch domain verification
        status method over gRPC.

        Returns list of target sites with its domain verification
        status. This method can only be called under data store with
        BASIC_SITE_SEARCH state at the moment.

        Returns:
            Callable[[~.FetchDomainVerificationStatusRequest],
                    Awaitable[~.FetchDomainVerificationStatusResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_domain_verification_status" not in self._stubs:
            self._stubs[
                "fetch_domain_verification_status"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.discoveryengine.v1.SiteSearchEngineService/FetchDomainVerificationStatus",
                request_serializer=site_search_engine_service.FetchDomainVerificationStatusRequest.serialize,
                response_deserializer=site_search_engine_service.FetchDomainVerificationStatusResponse.deserialize,
            )
        return self._stubs["fetch_domain_verification_status"]

    def close(self):
        return self.grpc_channel.close()

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]


__all__ = ("SiteSearchEngineServiceGrpcAsyncIOTransport",)
