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

from collections import OrderedDict
import os
import re
from typing import Callable, Dict, Iterable, Iterator, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.firestore_v1.services.firestore import pagers
from google.cloud.firestore_v1.types import common
from google.cloud.firestore_v1.types import document
from google.cloud.firestore_v1.types import document as gf_document
from google.cloud.firestore_v1.types import firestore
from google.cloud.firestore_v1.types import query
from google.cloud.firestore_v1.types import write as gf_write
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import FirestoreTransport
from .transports.grpc import FirestoreGrpcTransport
from .transports.grpc_asyncio import FirestoreGrpcAsyncIOTransport


class FirestoreClientMeta(type):
    """Metaclass for the Firestore client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[FirestoreTransport]]
    _transport_registry["grpc"] = FirestoreGrpcTransport
    _transport_registry["grpc_asyncio"] = FirestoreGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[FirestoreTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class FirestoreClient(metaclass=FirestoreClientMeta):
    """The Cloud Firestore service.
    Cloud Firestore is a fast, fully managed, serverless, cloud-
    native NoSQL document database that simplifies storing, syncing,
    and querying data for your mobile, web, and IoT apps at global
    scale. Its client libraries provide live synchronization and
    offline support, while its security features and integrations
    with Firebase and Google Cloud Platform (GCP) accelerate
    building truly serverless apps.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "firestore.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, FirestoreTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the firestore client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FirestoreTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, FirestoreTransport):
            # transport is a FirestoreTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def get_document(
        self,
        request: firestore.GetDocumentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Gets a single document.

        Args:
            request (:class:`~.firestore.GetDocumentRequest`):
                The request object. The request for
                [Firestore.GetDocument][google.firestore.v1.Firestore.GetDocument].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.document.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.

        request = firestore.GetDocumentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_document,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_documents(
        self,
        request: firestore.ListDocumentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDocumentsPager:
        r"""Lists documents.

        Args:
            request (:class:`~.firestore.ListDocumentsRequest`):
                The request object. The request for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListDocumentsPager:
                The response for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.

        request = firestore.ListDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_documents,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDocumentsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_document(
        self,
        request: firestore.UpdateDocumentRequest = None,
        *,
        document: gf_document.Document = None,
        update_mask: common.DocumentMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gf_document.Document:
        r"""Updates or inserts a document.

        Args:
            request (:class:`~.firestore.UpdateDocumentRequest`):
                The request object. The request for
                [Firestore.UpdateDocument][google.firestore.v1.Firestore.UpdateDocument].
            document (:class:`~.gf_document.Document`):
                Required. The updated document.
                Creates the document if it does not
                already exist.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.common.DocumentMask`):
                The fields to update.
                None of the field paths in the mask may
                contain a reserved name.
                If the document exists on the server and
                has fields not referenced in the mask,
                they are left unchanged.
                Fields referenced in the mask, but not
                present in the input document, are
                deleted from the document on the server.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gf_document.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([document, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.UpdateDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if document is not None:
            request.document = document
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_document,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("document.name", request.document.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_document(
        self,
        request: firestore.DeleteDocumentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a document.

        Args:
            request (:class:`~.firestore.DeleteDocumentRequest`):
                The request object. The request for
                [Firestore.DeleteDocument][google.firestore.v1.Firestore.DeleteDocument].
            name (:class:`str`):
                Required. The resource name of the Document to delete.
                In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.DeleteDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_document,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def batch_get_documents(
        self,
        request: firestore.BatchGetDocumentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[firestore.BatchGetDocumentsResponse]:
        r"""Gets multiple documents.
        Documents returned by this method are not guaranteed to
        be returned in the same order that they were requested.

        Args:
            request (:class:`~.firestore.BatchGetDocumentsRequest`):
                The request object. The request for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.firestore.BatchGetDocumentsResponse]:
                The streamed response for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].

        """
        # Create or coerce a protobuf request object.

        request = firestore.BatchGetDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.batch_get_documents,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def begin_transaction(
        self,
        request: firestore.BeginTransactionRequest = None,
        *,
        database: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firestore.BeginTransactionResponse:
        r"""Starts a new transaction.

        Args:
            request (:class:`~.firestore.BeginTransactionRequest`):
                The request object. The request for
                [Firestore.BeginTransaction][google.firestore.v1.Firestore.BeginTransaction].
            database (:class:`str`):
                Required. The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.firestore.BeginTransactionResponse:
                The response for
                [Firestore.BeginTransaction][google.firestore.v1.Firestore.BeginTransaction].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([database]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.BeginTransactionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if database is not None:
            request.database = database

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.begin_transaction,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def commit(
        self,
        request: firestore.CommitRequest = None,
        *,
        database: str = None,
        writes: Sequence[gf_write.Write] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firestore.CommitResponse:
        r"""Commits a transaction, while optionally updating
        documents.

        Args:
            request (:class:`~.firestore.CommitRequest`):
                The request object. The request for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].
            database (:class:`str`):
                Required. The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            writes (:class:`Sequence[~.gf_write.Write]`):
                The writes to apply.
                Always executed atomically and in order.
                This corresponds to the ``writes`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.firestore.CommitResponse:
                The response for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([database, writes]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.CommitRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if database is not None:
            request.database = database
        if writes is not None:
            request.writes = writes

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.commit, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def rollback(
        self,
        request: firestore.RollbackRequest = None,
        *,
        database: str = None,
        transaction: bytes = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Rolls back a transaction.

        Args:
            request (:class:`~.firestore.RollbackRequest`):
                The request object. The request for
                [Firestore.Rollback][google.firestore.v1.Firestore.Rollback].
            database (:class:`str`):
                Required. The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transaction (:class:`bytes`):
                Required. The transaction to roll
                back.
                This corresponds to the ``transaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([database, transaction]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.RollbackRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if database is not None:
            request.database = database
        if transaction is not None:
            request.transaction = transaction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.rollback, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def run_query(
        self,
        request: firestore.RunQueryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[firestore.RunQueryResponse]:
        r"""Runs a query.

        Args:
            request (:class:`~.firestore.RunQueryRequest`):
                The request object. The request for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.firestore.RunQueryResponse]:
                The response for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].

        """
        # Create or coerce a protobuf request object.

        request = firestore.RunQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.run_query, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def partition_query(
        self,
        request: firestore.PartitionQueryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.PartitionQueryPager:
        r"""Partitions a query by returning partition cursors
        that can be used to run the query in parallel. The
        returned partition cursors are split points that can be
        used by RunQuery as starting/end points for the query
        results.

        Args:
            request (:class:`~.firestore.PartitionQueryRequest`):
                The request object. The request for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.PartitionQueryPager:
                The response for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.

        request = firestore.PartitionQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.partition_query,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.PartitionQueryPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def write(
        self,
        requests: Iterator[firestore.WriteRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[firestore.WriteResponse]:
        r"""Streams batches of document updates and deletes, in
        order.

        Args:
            requests (Iterator[`~.firestore.WriteRequest`]):
                The request object iterator. The request for
                [Firestore.Write][google.firestore.v1.Firestore.Write].
                The first request creates a stream, or resumes an
                existing one from a token.
                When creating a new stream, the server replies with a
                response containing only an ID and a token, to use in
                the next request.

                When resuming a stream, the server first streams any
                responses later than the given token, then a response
                containing only an up-to-date token, to use in the next
                request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.firestore.WriteResponse]:
                The response for
                [Firestore.Write][google.firestore.v1.Firestore.Write].

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.write, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (gapic_v1.routing_header.to_grpc_metadata(()),)

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def listen(
        self,
        requests: Iterator[firestore.ListenRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[firestore.ListenResponse]:
        r"""Listens to changes.

        Args:
            requests (Iterator[`~.firestore.ListenRequest`]):
                The request object iterator. A request for
                [Firestore.Listen][google.firestore.v1.Firestore.Listen]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.firestore.ListenResponse]:
                The response for
                [Firestore.Listen][google.firestore.v1.Firestore.Listen].

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.listen, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (gapic_v1.routing_header.to_grpc_metadata(()),)

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_collection_ids(
        self,
        request: firestore.ListCollectionIdsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firestore.ListCollectionIdsResponse:
        r"""Lists all the collection IDs underneath a document.

        Args:
            request (:class:`~.firestore.ListCollectionIdsRequest`):
                The request object. The request for
                [Firestore.ListCollectionIds][google.firestore.v1.Firestore.ListCollectionIds].
            parent (:class:`str`):
                Required. The parent document. In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                For example:
                ``projects/my-project/databases/my-database/documents/chatrooms/my-chatroom``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.firestore.ListCollectionIdsResponse:
                The response from
                [Firestore.ListCollectionIds][google.firestore.v1.Firestore.ListCollectionIds].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.ListCollectionIdsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_collection_ids,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_write(
        self,
        request: firestore.BatchWriteRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firestore.BatchWriteResponse:
        r"""Applies a batch of write operations.

        The BatchWrite method does not apply the write operations
        atomically and can apply them out of order. Method does not
        allow more than one write per document. Each write succeeds or
        fails independently. See the
        [BatchWriteResponse][google.firestore.v1.BatchWriteResponse] for
        the success status of each write.

        If you require an atomically applied set of writes, use
        [Commit][google.firestore.v1.Firestore.Commit] instead.

        Args:
            request (:class:`~.firestore.BatchWriteRequest`):
                The request object. The request for
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.firestore.BatchWriteResponse:
                The response from
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].

        """
        # Create or coerce a protobuf request object.

        request = firestore.BatchWriteRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.batch_write, default_timeout=None, client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_document(
        self,
        request: firestore.CreateDocumentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Creates a new document.

        Args:
            request (:class:`~.firestore.CreateDocumentRequest`):
                The request object. The request for
                [Firestore.CreateDocument][google.firestore.v1.Firestore.CreateDocument].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.document.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.

        request = firestore.CreateDocumentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_document,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-firestore",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("FirestoreClient",)
