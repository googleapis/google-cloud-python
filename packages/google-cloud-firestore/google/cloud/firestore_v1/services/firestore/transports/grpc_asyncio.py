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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.firestore_v1.types import document
from google.cloud.firestore_v1.types import document as gf_document
from google.cloud.firestore_v1.types import firestore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import FirestoreTransport, DEFAULT_CLIENT_INFO
from .grpc import FirestoreGrpcTransport


class FirestoreGrpcAsyncIOTransport(FirestoreTransport):
    """gRPC AsyncIO backend transport for Firestore.

    The Cloud Firestore service.
    Cloud Firestore is a fast, fully managed, serverless, cloud-
    native NoSQL document database that simplifies storing, syncing,
    and querying data for your mobile, web, and IoT apps at global
    scale. Its client libraries provide live synchronization and
    offline support, while its security features and integrations
    with Firebase and Google Cloud Platform (GCP) accelerate
    building truly serverless apps.

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
        host: str = "firestore.googleapis.com",
        credentials: credentials.Credentials = None,
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
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "firestore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def get_document(
        self,
    ) -> Callable[[firestore.GetDocumentRequest], Awaitable[document.Document]]:
        r"""Return a callable for the get document method over gRPC.

        Gets a single document.

        Returns:
            Callable[[~.GetDocumentRequest],
                    Awaitable[~.Document]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_document" not in self._stubs:
            self._stubs["get_document"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/GetDocument",
                request_serializer=firestore.GetDocumentRequest.serialize,
                response_deserializer=document.Document.deserialize,
            )
        return self._stubs["get_document"]

    @property
    def list_documents(
        self,
    ) -> Callable[
        [firestore.ListDocumentsRequest], Awaitable[firestore.ListDocumentsResponse]
    ]:
        r"""Return a callable for the list documents method over gRPC.

        Lists documents.

        Returns:
            Callable[[~.ListDocumentsRequest],
                    Awaitable[~.ListDocumentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_documents" not in self._stubs:
            self._stubs["list_documents"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/ListDocuments",
                request_serializer=firestore.ListDocumentsRequest.serialize,
                response_deserializer=firestore.ListDocumentsResponse.deserialize,
            )
        return self._stubs["list_documents"]

    @property
    def update_document(
        self,
    ) -> Callable[[firestore.UpdateDocumentRequest], Awaitable[gf_document.Document]]:
        r"""Return a callable for the update document method over gRPC.

        Updates or inserts a document.

        Returns:
            Callable[[~.UpdateDocumentRequest],
                    Awaitable[~.Document]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_document" not in self._stubs:
            self._stubs["update_document"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/UpdateDocument",
                request_serializer=firestore.UpdateDocumentRequest.serialize,
                response_deserializer=gf_document.Document.deserialize,
            )
        return self._stubs["update_document"]

    @property
    def delete_document(
        self,
    ) -> Callable[[firestore.DeleteDocumentRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete document method over gRPC.

        Deletes a document.

        Returns:
            Callable[[~.DeleteDocumentRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_document" not in self._stubs:
            self._stubs["delete_document"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/DeleteDocument",
                request_serializer=firestore.DeleteDocumentRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_document"]

    @property
    def batch_get_documents(
        self,
    ) -> Callable[
        [firestore.BatchGetDocumentsRequest],
        Awaitable[firestore.BatchGetDocumentsResponse],
    ]:
        r"""Return a callable for the batch get documents method over gRPC.

        Gets multiple documents.
        Documents returned by this method are not guaranteed to
        be returned in the same order that they were requested.

        Returns:
            Callable[[~.BatchGetDocumentsRequest],
                    Awaitable[~.BatchGetDocumentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_get_documents" not in self._stubs:
            self._stubs["batch_get_documents"] = self.grpc_channel.unary_stream(
                "/google.firestore.v1.Firestore/BatchGetDocuments",
                request_serializer=firestore.BatchGetDocumentsRequest.serialize,
                response_deserializer=firestore.BatchGetDocumentsResponse.deserialize,
            )
        return self._stubs["batch_get_documents"]

    @property
    def begin_transaction(
        self,
    ) -> Callable[
        [firestore.BeginTransactionRequest],
        Awaitable[firestore.BeginTransactionResponse],
    ]:
        r"""Return a callable for the begin transaction method over gRPC.

        Starts a new transaction.

        Returns:
            Callable[[~.BeginTransactionRequest],
                    Awaitable[~.BeginTransactionResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "begin_transaction" not in self._stubs:
            self._stubs["begin_transaction"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/BeginTransaction",
                request_serializer=firestore.BeginTransactionRequest.serialize,
                response_deserializer=firestore.BeginTransactionResponse.deserialize,
            )
        return self._stubs["begin_transaction"]

    @property
    def commit(
        self,
    ) -> Callable[[firestore.CommitRequest], Awaitable[firestore.CommitResponse]]:
        r"""Return a callable for the commit method over gRPC.

        Commits a transaction, while optionally updating
        documents.

        Returns:
            Callable[[~.CommitRequest],
                    Awaitable[~.CommitResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "commit" not in self._stubs:
            self._stubs["commit"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/Commit",
                request_serializer=firestore.CommitRequest.serialize,
                response_deserializer=firestore.CommitResponse.deserialize,
            )
        return self._stubs["commit"]

    @property
    def rollback(self) -> Callable[[firestore.RollbackRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the rollback method over gRPC.

        Rolls back a transaction.

        Returns:
            Callable[[~.RollbackRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rollback" not in self._stubs:
            self._stubs["rollback"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/Rollback",
                request_serializer=firestore.RollbackRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["rollback"]

    @property
    def run_query(
        self,
    ) -> Callable[[firestore.RunQueryRequest], Awaitable[firestore.RunQueryResponse]]:
        r"""Return a callable for the run query method over gRPC.

        Runs a query.

        Returns:
            Callable[[~.RunQueryRequest],
                    Awaitable[~.RunQueryResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_query" not in self._stubs:
            self._stubs["run_query"] = self.grpc_channel.unary_stream(
                "/google.firestore.v1.Firestore/RunQuery",
                request_serializer=firestore.RunQueryRequest.serialize,
                response_deserializer=firestore.RunQueryResponse.deserialize,
            )
        return self._stubs["run_query"]

    @property
    def partition_query(
        self,
    ) -> Callable[
        [firestore.PartitionQueryRequest], Awaitable[firestore.PartitionQueryResponse]
    ]:
        r"""Return a callable for the partition query method over gRPC.

        Partitions a query by returning partition cursors
        that can be used to run the query in parallel. The
        returned partition cursors are split points that can be
        used by RunQuery as starting/end points for the query
        results.

        Returns:
            Callable[[~.PartitionQueryRequest],
                    Awaitable[~.PartitionQueryResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "partition_query" not in self._stubs:
            self._stubs["partition_query"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/PartitionQuery",
                request_serializer=firestore.PartitionQueryRequest.serialize,
                response_deserializer=firestore.PartitionQueryResponse.deserialize,
            )
        return self._stubs["partition_query"]

    @property
    def write(
        self,
    ) -> Callable[[firestore.WriteRequest], Awaitable[firestore.WriteResponse]]:
        r"""Return a callable for the write method over gRPC.

        Streams batches of document updates and deletes, in
        order.

        Returns:
            Callable[[~.WriteRequest],
                    Awaitable[~.WriteResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "write" not in self._stubs:
            self._stubs["write"] = self.grpc_channel.stream_stream(
                "/google.firestore.v1.Firestore/Write",
                request_serializer=firestore.WriteRequest.serialize,
                response_deserializer=firestore.WriteResponse.deserialize,
            )
        return self._stubs["write"]

    @property
    def listen(
        self,
    ) -> Callable[[firestore.ListenRequest], Awaitable[firestore.ListenResponse]]:
        r"""Return a callable for the listen method over gRPC.

        Listens to changes.

        Returns:
            Callable[[~.ListenRequest],
                    Awaitable[~.ListenResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "listen" not in self._stubs:
            self._stubs["listen"] = self.grpc_channel.stream_stream(
                "/google.firestore.v1.Firestore/Listen",
                request_serializer=firestore.ListenRequest.serialize,
                response_deserializer=firestore.ListenResponse.deserialize,
            )
        return self._stubs["listen"]

    @property
    def list_collection_ids(
        self,
    ) -> Callable[
        [firestore.ListCollectionIdsRequest],
        Awaitable[firestore.ListCollectionIdsResponse],
    ]:
        r"""Return a callable for the list collection ids method over gRPC.

        Lists all the collection IDs underneath a document.

        Returns:
            Callable[[~.ListCollectionIdsRequest],
                    Awaitable[~.ListCollectionIdsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_collection_ids" not in self._stubs:
            self._stubs["list_collection_ids"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/ListCollectionIds",
                request_serializer=firestore.ListCollectionIdsRequest.serialize,
                response_deserializer=firestore.ListCollectionIdsResponse.deserialize,
            )
        return self._stubs["list_collection_ids"]

    @property
    def batch_write(
        self,
    ) -> Callable[
        [firestore.BatchWriteRequest], Awaitable[firestore.BatchWriteResponse]
    ]:
        r"""Return a callable for the batch write method over gRPC.

        Applies a batch of write operations.

        The BatchWrite method does not apply the write operations
        atomically and can apply them out of order. Method does not
        allow more than one write per document. Each write succeeds or
        fails independently. See the
        [BatchWriteResponse][google.firestore.v1.BatchWriteResponse] for
        the success status of each write.

        If you require an atomically applied set of writes, use
        [Commit][google.firestore.v1.Firestore.Commit] instead.

        Returns:
            Callable[[~.BatchWriteRequest],
                    Awaitable[~.BatchWriteResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_write" not in self._stubs:
            self._stubs["batch_write"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/BatchWrite",
                request_serializer=firestore.BatchWriteRequest.serialize,
                response_deserializer=firestore.BatchWriteResponse.deserialize,
            )
        return self._stubs["batch_write"]

    @property
    def create_document(
        self,
    ) -> Callable[[firestore.CreateDocumentRequest], Awaitable[document.Document]]:
        r"""Return a callable for the create document method over gRPC.

        Creates a new document.

        Returns:
            Callable[[~.CreateDocumentRequest],
                    Awaitable[~.Document]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_document" not in self._stubs:
            self._stubs["create_document"] = self.grpc_channel.unary_unary(
                "/google.firestore.v1.Firestore/CreateDocument",
                request_serializer=firestore.CreateDocumentRequest.serialize,
                response_deserializer=document.Document.deserialize,
            )
        return self._stubs["create_document"]


__all__ = ("FirestoreGrpcAsyncIOTransport",)
