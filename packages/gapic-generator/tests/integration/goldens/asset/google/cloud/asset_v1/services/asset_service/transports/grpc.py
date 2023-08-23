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
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.asset_v1.types import asset_service
from google.longrunning import operations_pb2 # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import AssetServiceTransport, DEFAULT_CLIENT_INFO


class AssetServiceGrpcTransport(AssetServiceTransport):
    """gRPC backend transport for AssetService.

    Asset service definition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'cloudasset.googleapis.com',
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
        self._operations_client: Optional[operations_v1.OperationsClient] = None

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
    def create_channel(cls,
                       host: str = 'cloudasset.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
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
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def export_assets(self) -> Callable[
            [asset_service.ExportAssetsRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the export assets method over gRPC.

        Exports assets with time and resource types to a given Cloud
        Storage location/BigQuery table. For Cloud Storage location
        destinations, the output format is newline-delimited JSON. Each
        line represents a
        [google.cloud.asset.v1.Asset][google.cloud.asset.v1.Asset] in
        the JSON format; for BigQuery table destinations, the output
        table stores the fields in asset Protobuf as columns. This API
        implements the
        [google.longrunning.Operation][google.longrunning.Operation]
        API, which allows you to keep track of the export. We recommend
        intervals of at least 2 seconds with exponential retry to poll
        the export operation result. For regular-size resource parent,
        the export operation usually finishes within 5 minutes.

        Returns:
            Callable[[~.ExportAssetsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'export_assets' not in self._stubs:
            self._stubs['export_assets'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/ExportAssets',
                request_serializer=asset_service.ExportAssetsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['export_assets']

    @property
    def list_assets(self) -> Callable[
            [asset_service.ListAssetsRequest],
            asset_service.ListAssetsResponse]:
        r"""Return a callable for the list assets method over gRPC.

        Lists assets with time and resource types and returns
        paged results in response.

        Returns:
            Callable[[~.ListAssetsRequest],
                    ~.ListAssetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_assets' not in self._stubs:
            self._stubs['list_assets'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/ListAssets',
                request_serializer=asset_service.ListAssetsRequest.serialize,
                response_deserializer=asset_service.ListAssetsResponse.deserialize,
            )
        return self._stubs['list_assets']

    @property
    def batch_get_assets_history(self) -> Callable[
            [asset_service.BatchGetAssetsHistoryRequest],
            asset_service.BatchGetAssetsHistoryResponse]:
        r"""Return a callable for the batch get assets history method over gRPC.

        Batch gets the update history of assets that overlap a time
        window. For IAM_POLICY content, this API outputs history when
        the asset and its attached IAM POLICY both exist. This can
        create gaps in the output history. Otherwise, this API outputs
        history with asset in both non-delete or deleted status. If a
        specified asset does not exist, this API returns an
        INVALID_ARGUMENT error.

        Returns:
            Callable[[~.BatchGetAssetsHistoryRequest],
                    ~.BatchGetAssetsHistoryResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_get_assets_history' not in self._stubs:
            self._stubs['batch_get_assets_history'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/BatchGetAssetsHistory',
                request_serializer=asset_service.BatchGetAssetsHistoryRequest.serialize,
                response_deserializer=asset_service.BatchGetAssetsHistoryResponse.deserialize,
            )
        return self._stubs['batch_get_assets_history']

    @property
    def create_feed(self) -> Callable[
            [asset_service.CreateFeedRequest],
            asset_service.Feed]:
        r"""Return a callable for the create feed method over gRPC.

        Creates a feed in a parent
        project/folder/organization to listen to its asset
        updates.

        Returns:
            Callable[[~.CreateFeedRequest],
                    ~.Feed]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_feed' not in self._stubs:
            self._stubs['create_feed'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/CreateFeed',
                request_serializer=asset_service.CreateFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs['create_feed']

    @property
    def get_feed(self) -> Callable[
            [asset_service.GetFeedRequest],
            asset_service.Feed]:
        r"""Return a callable for the get feed method over gRPC.

        Gets details about an asset feed.

        Returns:
            Callable[[~.GetFeedRequest],
                    ~.Feed]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_feed' not in self._stubs:
            self._stubs['get_feed'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/GetFeed',
                request_serializer=asset_service.GetFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs['get_feed']

    @property
    def list_feeds(self) -> Callable[
            [asset_service.ListFeedsRequest],
            asset_service.ListFeedsResponse]:
        r"""Return a callable for the list feeds method over gRPC.

        Lists all asset feeds in a parent
        project/folder/organization.

        Returns:
            Callable[[~.ListFeedsRequest],
                    ~.ListFeedsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_feeds' not in self._stubs:
            self._stubs['list_feeds'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/ListFeeds',
                request_serializer=asset_service.ListFeedsRequest.serialize,
                response_deserializer=asset_service.ListFeedsResponse.deserialize,
            )
        return self._stubs['list_feeds']

    @property
    def update_feed(self) -> Callable[
            [asset_service.UpdateFeedRequest],
            asset_service.Feed]:
        r"""Return a callable for the update feed method over gRPC.

        Updates an asset feed configuration.

        Returns:
            Callable[[~.UpdateFeedRequest],
                    ~.Feed]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_feed' not in self._stubs:
            self._stubs['update_feed'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/UpdateFeed',
                request_serializer=asset_service.UpdateFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs['update_feed']

    @property
    def delete_feed(self) -> Callable[
            [asset_service.DeleteFeedRequest],
            empty_pb2.Empty]:
        r"""Return a callable for the delete feed method over gRPC.

        Deletes an asset feed.

        Returns:
            Callable[[~.DeleteFeedRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_feed' not in self._stubs:
            self._stubs['delete_feed'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/DeleteFeed',
                request_serializer=asset_service.DeleteFeedRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_feed']

    @property
    def search_all_resources(self) -> Callable[
            [asset_service.SearchAllResourcesRequest],
            asset_service.SearchAllResourcesResponse]:
        r"""Return a callable for the search all resources method over gRPC.

        Searches all Google Cloud resources within the specified scope,
        such as a project, folder, or organization. The caller must be
        granted the ``cloudasset.assets.searchAllResources`` permission
        on the desired scope, otherwise the request will be rejected.

        Returns:
            Callable[[~.SearchAllResourcesRequest],
                    ~.SearchAllResourcesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'search_all_resources' not in self._stubs:
            self._stubs['search_all_resources'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/SearchAllResources',
                request_serializer=asset_service.SearchAllResourcesRequest.serialize,
                response_deserializer=asset_service.SearchAllResourcesResponse.deserialize,
            )
        return self._stubs['search_all_resources']

    @property
    def search_all_iam_policies(self) -> Callable[
            [asset_service.SearchAllIamPoliciesRequest],
            asset_service.SearchAllIamPoliciesResponse]:
        r"""Return a callable for the search all iam policies method over gRPC.

        Searches all IAM policies within the specified scope, such as a
        project, folder, or organization. The caller must be granted the
        ``cloudasset.assets.searchAllIamPolicies`` permission on the
        desired scope, otherwise the request will be rejected.

        Returns:
            Callable[[~.SearchAllIamPoliciesRequest],
                    ~.SearchAllIamPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'search_all_iam_policies' not in self._stubs:
            self._stubs['search_all_iam_policies'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/SearchAllIamPolicies',
                request_serializer=asset_service.SearchAllIamPoliciesRequest.serialize,
                response_deserializer=asset_service.SearchAllIamPoliciesResponse.deserialize,
            )
        return self._stubs['search_all_iam_policies']

    @property
    def analyze_iam_policy(self) -> Callable[
            [asset_service.AnalyzeIamPolicyRequest],
            asset_service.AnalyzeIamPolicyResponse]:
        r"""Return a callable for the analyze iam policy method over gRPC.

        Analyzes IAM policies to answer which identities have
        what accesses on which resources.

        Returns:
            Callable[[~.AnalyzeIamPolicyRequest],
                    ~.AnalyzeIamPolicyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_iam_policy' not in self._stubs:
            self._stubs['analyze_iam_policy'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeIamPolicy',
                request_serializer=asset_service.AnalyzeIamPolicyRequest.serialize,
                response_deserializer=asset_service.AnalyzeIamPolicyResponse.deserialize,
            )
        return self._stubs['analyze_iam_policy']

    @property
    def analyze_iam_policy_longrunning(self) -> Callable[
            [asset_service.AnalyzeIamPolicyLongrunningRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the analyze iam policy longrunning method over gRPC.

        Analyzes IAM policies asynchronously to answer which identities
        have what accesses on which resources, and writes the analysis
        results to a Google Cloud Storage or a BigQuery destination. For
        Cloud Storage destination, the output format is the JSON format
        that represents a
        [AnalyzeIamPolicyResponse][google.cloud.asset.v1.AnalyzeIamPolicyResponse].
        This method implements the
        [google.longrunning.Operation][google.longrunning.Operation],
        which allows you to track the operation status. We recommend
        intervals of at least 2 seconds with exponential backoff retry
        to poll the operation result. The metadata contains the metadata
        for the long-running operation.

        Returns:
            Callable[[~.AnalyzeIamPolicyLongrunningRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_iam_policy_longrunning' not in self._stubs:
            self._stubs['analyze_iam_policy_longrunning'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeIamPolicyLongrunning',
                request_serializer=asset_service.AnalyzeIamPolicyLongrunningRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['analyze_iam_policy_longrunning']

    @property
    def analyze_move(self) -> Callable[
            [asset_service.AnalyzeMoveRequest],
            asset_service.AnalyzeMoveResponse]:
        r"""Return a callable for the analyze move method over gRPC.

        Analyze moving a resource to a specified destination
        without kicking off the actual move. The analysis is
        best effort depending on the user's permissions of
        viewing different hierarchical policies and
        configurations. The policies and configuration are
        subject to change before the actual resource migration
        takes place.

        Returns:
            Callable[[~.AnalyzeMoveRequest],
                    ~.AnalyzeMoveResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_move' not in self._stubs:
            self._stubs['analyze_move'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeMove',
                request_serializer=asset_service.AnalyzeMoveRequest.serialize,
                response_deserializer=asset_service.AnalyzeMoveResponse.deserialize,
            )
        return self._stubs['analyze_move']

    @property
    def query_assets(self) -> Callable[
            [asset_service.QueryAssetsRequest],
            asset_service.QueryAssetsResponse]:
        r"""Return a callable for the query assets method over gRPC.

        Issue a job that queries assets using a SQL statement compatible
        with `BigQuery Standard
        SQL <http://cloud/bigquery/docs/reference/standard-sql/enabling-standard-sql>`__.

        If the query execution finishes within timeout and there's no
        pagination, the full query results will be returned in the
        ``QueryAssetsResponse``.

        Otherwise, full query results can be obtained by issuing extra
        requests with the ``job_reference`` from the a previous
        ``QueryAssets`` call.

        Note, the query result has approximately 10 GB limitation
        enforced by BigQuery
        https://cloud.google.com/bigquery/docs/best-practices-performance-output,
        queries return larger results will result in errors.

        Returns:
            Callable[[~.QueryAssetsRequest],
                    ~.QueryAssetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'query_assets' not in self._stubs:
            self._stubs['query_assets'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/QueryAssets',
                request_serializer=asset_service.QueryAssetsRequest.serialize,
                response_deserializer=asset_service.QueryAssetsResponse.deserialize,
            )
        return self._stubs['query_assets']

    @property
    def create_saved_query(self) -> Callable[
            [asset_service.CreateSavedQueryRequest],
            asset_service.SavedQuery]:
        r"""Return a callable for the create saved query method over gRPC.

        Creates a saved query in a parent
        project/folder/organization.

        Returns:
            Callable[[~.CreateSavedQueryRequest],
                    ~.SavedQuery]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_saved_query' not in self._stubs:
            self._stubs['create_saved_query'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/CreateSavedQuery',
                request_serializer=asset_service.CreateSavedQueryRequest.serialize,
                response_deserializer=asset_service.SavedQuery.deserialize,
            )
        return self._stubs['create_saved_query']

    @property
    def get_saved_query(self) -> Callable[
            [asset_service.GetSavedQueryRequest],
            asset_service.SavedQuery]:
        r"""Return a callable for the get saved query method over gRPC.

        Gets details about a saved query.

        Returns:
            Callable[[~.GetSavedQueryRequest],
                    ~.SavedQuery]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_saved_query' not in self._stubs:
            self._stubs['get_saved_query'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/GetSavedQuery',
                request_serializer=asset_service.GetSavedQueryRequest.serialize,
                response_deserializer=asset_service.SavedQuery.deserialize,
            )
        return self._stubs['get_saved_query']

    @property
    def list_saved_queries(self) -> Callable[
            [asset_service.ListSavedQueriesRequest],
            asset_service.ListSavedQueriesResponse]:
        r"""Return a callable for the list saved queries method over gRPC.

        Lists all saved queries in a parent
        project/folder/organization.

        Returns:
            Callable[[~.ListSavedQueriesRequest],
                    ~.ListSavedQueriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_saved_queries' not in self._stubs:
            self._stubs['list_saved_queries'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/ListSavedQueries',
                request_serializer=asset_service.ListSavedQueriesRequest.serialize,
                response_deserializer=asset_service.ListSavedQueriesResponse.deserialize,
            )
        return self._stubs['list_saved_queries']

    @property
    def update_saved_query(self) -> Callable[
            [asset_service.UpdateSavedQueryRequest],
            asset_service.SavedQuery]:
        r"""Return a callable for the update saved query method over gRPC.

        Updates a saved query.

        Returns:
            Callable[[~.UpdateSavedQueryRequest],
                    ~.SavedQuery]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_saved_query' not in self._stubs:
            self._stubs['update_saved_query'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/UpdateSavedQuery',
                request_serializer=asset_service.UpdateSavedQueryRequest.serialize,
                response_deserializer=asset_service.SavedQuery.deserialize,
            )
        return self._stubs['update_saved_query']

    @property
    def delete_saved_query(self) -> Callable[
            [asset_service.DeleteSavedQueryRequest],
            empty_pb2.Empty]:
        r"""Return a callable for the delete saved query method over gRPC.

        Deletes a saved query.

        Returns:
            Callable[[~.DeleteSavedQueryRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_saved_query' not in self._stubs:
            self._stubs['delete_saved_query'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/DeleteSavedQuery',
                request_serializer=asset_service.DeleteSavedQueryRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_saved_query']

    @property
    def batch_get_effective_iam_policies(self) -> Callable[
            [asset_service.BatchGetEffectiveIamPoliciesRequest],
            asset_service.BatchGetEffectiveIamPoliciesResponse]:
        r"""Return a callable for the batch get effective iam
        policies method over gRPC.

        Gets effective IAM policies for a batch of resources.

        Returns:
            Callable[[~.BatchGetEffectiveIamPoliciesRequest],
                    ~.BatchGetEffectiveIamPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_get_effective_iam_policies' not in self._stubs:
            self._stubs['batch_get_effective_iam_policies'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/BatchGetEffectiveIamPolicies',
                request_serializer=asset_service.BatchGetEffectiveIamPoliciesRequest.serialize,
                response_deserializer=asset_service.BatchGetEffectiveIamPoliciesResponse.deserialize,
            )
        return self._stubs['batch_get_effective_iam_policies']

    @property
    def analyze_org_policies(self) -> Callable[
            [asset_service.AnalyzeOrgPoliciesRequest],
            asset_service.AnalyzeOrgPoliciesResponse]:
        r"""Return a callable for the analyze org policies method over gRPC.

        Analyzes organization policies under a scope.

        Returns:
            Callable[[~.AnalyzeOrgPoliciesRequest],
                    ~.AnalyzeOrgPoliciesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_org_policies' not in self._stubs:
            self._stubs['analyze_org_policies'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeOrgPolicies',
                request_serializer=asset_service.AnalyzeOrgPoliciesRequest.serialize,
                response_deserializer=asset_service.AnalyzeOrgPoliciesResponse.deserialize,
            )
        return self._stubs['analyze_org_policies']

    @property
    def analyze_org_policy_governed_containers(self) -> Callable[
            [asset_service.AnalyzeOrgPolicyGovernedContainersRequest],
            asset_service.AnalyzeOrgPolicyGovernedContainersResponse]:
        r"""Return a callable for the analyze org policy governed
        containers method over gRPC.

        Analyzes organization policies governed containers
        (projects, folders or organization) under a scope.

        Returns:
            Callable[[~.AnalyzeOrgPolicyGovernedContainersRequest],
                    ~.AnalyzeOrgPolicyGovernedContainersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_org_policy_governed_containers' not in self._stubs:
            self._stubs['analyze_org_policy_governed_containers'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeOrgPolicyGovernedContainers',
                request_serializer=asset_service.AnalyzeOrgPolicyGovernedContainersRequest.serialize,
                response_deserializer=asset_service.AnalyzeOrgPolicyGovernedContainersResponse.deserialize,
            )
        return self._stubs['analyze_org_policy_governed_containers']

    @property
    def analyze_org_policy_governed_assets(self) -> Callable[
            [asset_service.AnalyzeOrgPolicyGovernedAssetsRequest],
            asset_service.AnalyzeOrgPolicyGovernedAssetsResponse]:
        r"""Return a callable for the analyze org policy governed
        assets method over gRPC.

        Analyzes organization policies governed assets (Google Cloud
        resources or policies) under a scope. This RPC supports custom
        constraints and the following 10 canned constraints:

        -  storage.uniformBucketLevelAccess
        -  iam.disableServiceAccountKeyCreation
        -  iam.allowedPolicyMemberDomains
        -  compute.vmExternalIpAccess
        -  appengine.enforceServiceAccountActAsCheck
        -  gcp.resourceLocations
        -  compute.trustedImageProjects
        -  compute.skipDefaultNetworkCreation
        -  compute.requireOsLogin
        -  compute.disableNestedVirtualization

        This RPC only returns either resources of types supported by
        `searchable asset
        types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__,
        or IAM policies.

        Returns:
            Callable[[~.AnalyzeOrgPolicyGovernedAssetsRequest],
                    ~.AnalyzeOrgPolicyGovernedAssetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'analyze_org_policy_governed_assets' not in self._stubs:
            self._stubs['analyze_org_policy_governed_assets'] = self.grpc_channel.unary_unary(
                '/google.cloud.asset.v1.AssetService/AnalyzeOrgPolicyGovernedAssets',
                request_serializer=asset_service.AnalyzeOrgPolicyGovernedAssetsRequest.serialize,
                response_deserializer=asset_service.AnalyzeOrgPolicyGovernedAssetsResponse.deserialize,
            )
        return self._stubs['analyze_org_policy_governed_assets']

    def close(self):
        self.grpc_channel.close()

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC.
        """
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
    def kind(self) -> str:
        return "grpc"


__all__ = (
    'AssetServiceGrpcTransport',
)
