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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.contentwarehouse_v1.types import (
    document_service,
    document_service_request,
)
from google.cloud.contentwarehouse_v1.types import document as gcc_document

from .base import DEFAULT_CLIENT_INFO, DocumentServiceTransport
from .grpc import DocumentServiceGrpcTransport


class DocumentServiceGrpcAsyncIOTransport(DocumentServiceTransport):
    """gRPC AsyncIO backend transport for DocumentService.

    This service lets you manage document.

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
        host: str = "contentwarehouse.googleapis.com",
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
        host: str = "contentwarehouse.googleapis.com",
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
                 The hostname to connect to (default: 'contentwarehouse.googleapis.com').
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
    def create_document(
        self,
    ) -> Callable[
        [document_service_request.CreateDocumentRequest],
        Awaitable[document_service.CreateDocumentResponse],
    ]:
        r"""Return a callable for the create document method over gRPC.

        Creates a document.

        Returns:
            Callable[[~.CreateDocumentRequest],
                    Awaitable[~.CreateDocumentResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_document" not in self._stubs:
            self._stubs["create_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/CreateDocument",
                request_serializer=document_service_request.CreateDocumentRequest.serialize,
                response_deserializer=document_service.CreateDocumentResponse.deserialize,
            )
        return self._stubs["create_document"]

    @property
    def get_document(
        self,
    ) -> Callable[
        [document_service_request.GetDocumentRequest], Awaitable[gcc_document.Document]
    ]:
        r"""Return a callable for the get document method over gRPC.

        Gets a document. Returns NOT_FOUND if the document does not
        exist.

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
                "/google.cloud.contentwarehouse.v1.DocumentService/GetDocument",
                request_serializer=document_service_request.GetDocumentRequest.serialize,
                response_deserializer=gcc_document.Document.deserialize,
            )
        return self._stubs["get_document"]

    @property
    def update_document(
        self,
    ) -> Callable[
        [document_service_request.UpdateDocumentRequest],
        Awaitable[document_service.UpdateDocumentResponse],
    ]:
        r"""Return a callable for the update document method over gRPC.

        Updates a document. Returns INVALID_ARGUMENT if the name of the
        document is non-empty and does not equal the existing name.

        Returns:
            Callable[[~.UpdateDocumentRequest],
                    Awaitable[~.UpdateDocumentResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_document" not in self._stubs:
            self._stubs["update_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/UpdateDocument",
                request_serializer=document_service_request.UpdateDocumentRequest.serialize,
                response_deserializer=document_service.UpdateDocumentResponse.deserialize,
            )
        return self._stubs["update_document"]

    @property
    def delete_document(
        self,
    ) -> Callable[
        [document_service_request.DeleteDocumentRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete document method over gRPC.

        Deletes a document. Returns NOT_FOUND if the document does not
        exist.

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
                "/google.cloud.contentwarehouse.v1.DocumentService/DeleteDocument",
                request_serializer=document_service_request.DeleteDocumentRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_document"]

    @property
    def search_documents(
        self,
    ) -> Callable[
        [document_service_request.SearchDocumentsRequest],
        Awaitable[document_service.SearchDocumentsResponse],
    ]:
        r"""Return a callable for the search documents method over gRPC.

        Searches for documents using provided
        [SearchDocumentsRequest][google.cloud.contentwarehouse.v1.SearchDocumentsRequest].
        This call only returns documents that the caller has permission
        to search against.

        Returns:
            Callable[[~.SearchDocumentsRequest],
                    Awaitable[~.SearchDocumentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_documents" not in self._stubs:
            self._stubs["search_documents"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/SearchDocuments",
                request_serializer=document_service_request.SearchDocumentsRequest.serialize,
                response_deserializer=document_service.SearchDocumentsResponse.deserialize,
            )
        return self._stubs["search_documents"]

    @property
    def lock_document(
        self,
    ) -> Callable[
        [document_service_request.LockDocumentRequest], Awaitable[gcc_document.Document]
    ]:
        r"""Return a callable for the lock document method over gRPC.

        Lock the document so the document cannot be updated
        by other users.

        Returns:
            Callable[[~.LockDocumentRequest],
                    Awaitable[~.Document]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "lock_document" not in self._stubs:
            self._stubs["lock_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/LockDocument",
                request_serializer=document_service_request.LockDocumentRequest.serialize,
                response_deserializer=gcc_document.Document.deserialize,
            )
        return self._stubs["lock_document"]

    @property
    def fetch_acl(
        self,
    ) -> Callable[
        [document_service_request.FetchAclRequest],
        Awaitable[document_service.FetchAclResponse],
    ]:
        r"""Return a callable for the fetch acl method over gRPC.

        Gets the access control policy for a resource. Returns NOT_FOUND
        error if the resource does not exist. Returns an empty policy if
        the resource exists but does not have a policy set.

        Returns:
            Callable[[~.FetchAclRequest],
                    Awaitable[~.FetchAclResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_acl" not in self._stubs:
            self._stubs["fetch_acl"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/FetchAcl",
                request_serializer=document_service_request.FetchAclRequest.serialize,
                response_deserializer=document_service.FetchAclResponse.deserialize,
            )
        return self._stubs["fetch_acl"]

    @property
    def set_acl(
        self,
    ) -> Callable[
        [document_service_request.SetAclRequest],
        Awaitable[document_service.SetAclResponse],
    ]:
        r"""Return a callable for the set acl method over gRPC.

        Sets the access control policy for a resource.
        Replaces any existing policy.

        Returns:
            Callable[[~.SetAclRequest],
                    Awaitable[~.SetAclResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_acl" not in self._stubs:
            self._stubs["set_acl"] = self.grpc_channel.unary_unary(
                "/google.cloud.contentwarehouse.v1.DocumentService/SetAcl",
                request_serializer=document_service_request.SetAclRequest.serialize,
                response_deserializer=document_service.SetAclResponse.deserialize,
            )
        return self._stubs["set_acl"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_document: self._wrap_method(
                self.create_document,
                default_timeout=180.0,
                client_info=client_info,
            ),
            self.get_document: self._wrap_method(
                self.get_document,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_document: self._wrap_method(
                self.update_document,
                default_timeout=180.0,
                client_info=client_info,
            ),
            self.delete_document: self._wrap_method(
                self.delete_document,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_documents: self._wrap_method(
                self.search_documents,
                default_timeout=180.0,
                client_info=client_info,
            ),
            self.lock_document: self._wrap_method(
                self.lock_document,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_acl: self._wrap_method(
                self.fetch_acl,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_acl: self._wrap_method(
                self.set_acl,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
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


__all__ = ("DocumentServiceGrpcAsyncIOTransport",)
