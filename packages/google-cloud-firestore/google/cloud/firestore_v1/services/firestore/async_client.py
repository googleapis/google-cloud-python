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
import functools
import re
from typing import (
    Dict,
    AsyncIterable,
    Awaitable,
    AsyncIterator,
    Sequence,
    Tuple,
    Type,
    Union,
)
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.firestore_v1.services.firestore import pagers
from google.cloud.firestore_v1.types import common
from google.cloud.firestore_v1.types import document
from google.cloud.firestore_v1.types import document as gf_document
from google.cloud.firestore_v1.types import firestore
from google.cloud.firestore_v1.types import query
from google.cloud.firestore_v1.types import write as gf_write
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import FirestoreTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import FirestoreGrpcAsyncIOTransport
from .client import FirestoreClient


class FirestoreAsyncClient:
    """The Cloud Firestore service.
    Cloud Firestore is a fast, fully managed, serverless, cloud-
    native NoSQL document database that simplifies storing, syncing,
    and querying data for your mobile, web, and IoT apps at global
    scale. Its client libraries provide live synchronization and
    offline support, while its security features and integrations
    with Firebase and Google Cloud Platform (GCP) accelerate
    building truly serverless apps.
    """

    _client: FirestoreClient

    DEFAULT_ENDPOINT = FirestoreClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = FirestoreClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        FirestoreClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        FirestoreClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(FirestoreClient.common_folder_path)
    parse_common_folder_path = staticmethod(FirestoreClient.parse_common_folder_path)
    common_organization_path = staticmethod(FirestoreClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        FirestoreClient.parse_common_organization_path
    )
    common_project_path = staticmethod(FirestoreClient.common_project_path)
    parse_common_project_path = staticmethod(FirestoreClient.parse_common_project_path)
    common_location_path = staticmethod(FirestoreClient.common_location_path)
    parse_common_location_path = staticmethod(
        FirestoreClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FirestoreAsyncClient: The constructed client.
        """
        return FirestoreClient.from_service_account_info.__func__(FirestoreAsyncClient, info, *args, **kwargs)  # type: ignore

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
            FirestoreAsyncClient: The constructed client.
        """
        return FirestoreClient.from_service_account_file.__func__(FirestoreAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FirestoreTransport:
        """Returns the transport used by the client instance.

        Returns:
            FirestoreTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(FirestoreClient).get_transport_class, type(FirestoreClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, FirestoreTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the firestore client.

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
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = FirestoreClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_document(
        self,
        request: firestore.GetDocumentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Gets a single document.

        Args:
            request (:class:`google.cloud.firestore_v1.types.GetDocumentRequest`):
                The request object. The request for
                [Firestore.GetDocument][google.firestore.v1.Firestore.GetDocument].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.firestore_v1.types.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.
        request = firestore.GetDocumentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_document,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_documents(
        self,
        request: firestore.ListDocumentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDocumentsAsyncPager:
        r"""Lists documents.

        Args:
            request (:class:`google.cloud.firestore_v1.types.ListDocumentsRequest`):
                The request object. The request for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.firestore_v1.services.firestore.pagers.ListDocumentsAsyncPager:
                The response for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = firestore.ListDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_documents,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDocumentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_document(
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
            request (:class:`google.cloud.firestore_v1.types.UpdateDocumentRequest`):
                The request object. The request for
                [Firestore.UpdateDocument][google.firestore.v1.Firestore.UpdateDocument].
            document (:class:`google.cloud.firestore_v1.types.Document`):
                Required. The updated document.
                Creates the document if it does not
                already exist.

                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.cloud.firestore_v1.types.DocumentMask`):
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
            google.cloud.firestore_v1.types.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, update_mask])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_document,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("document.name", request.document.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_document(
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
            request (:class:`google.cloud.firestore_v1.types.DeleteDocumentRequest`):
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_document,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def batch_get_documents(
        self,
        request: firestore.BatchGetDocumentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[firestore.BatchGetDocumentsResponse]]:
        r"""Gets multiple documents.
        Documents returned by this method are not guaranteed to
        be returned in the same order that they were requested.

        Args:
            request (:class:`google.cloud.firestore_v1.types.BatchGetDocumentsRequest`):
                The request object. The request for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.firestore_v1.types.BatchGetDocumentsResponse]:
                The streamed response for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].

        """
        # Create or coerce a protobuf request object.
        request = firestore.BatchGetDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_get_documents,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def begin_transaction(
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
            request (:class:`google.cloud.firestore_v1.types.BeginTransactionRequest`):
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
            google.cloud.firestore_v1.types.BeginTransactionResponse:
                The response for
                [Firestore.BeginTransaction][google.firestore.v1.Firestore.BeginTransaction].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([database])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.begin_transaction,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def commit(
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
            request (:class:`google.cloud.firestore_v1.types.CommitRequest`):
                The request object. The request for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].
            database (:class:`str`):
                Required. The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.

                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            writes (:class:`Sequence[google.cloud.firestore_v1.types.Write]`):
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
            google.cloud.firestore_v1.types.CommitResponse:
                The response for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([database, writes])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = firestore.CommitRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if database is not None:
            request.database = database
        if writes:
            request.writes.extend(writes)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.commit,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def rollback(
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
            request (:class:`google.cloud.firestore_v1.types.RollbackRequest`):
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
        has_flattened_params = any([database, transaction])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rollback,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def run_query(
        self,
        request: firestore.RunQueryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[firestore.RunQueryResponse]]:
        r"""Runs a query.

        Args:
            request (:class:`google.cloud.firestore_v1.types.RunQueryRequest`):
                The request object. The request for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.firestore_v1.types.RunQueryResponse]:
                The response for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].

        """
        # Create or coerce a protobuf request object.
        request = firestore.RunQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_query,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def partition_query(
        self,
        request: firestore.PartitionQueryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.PartitionQueryAsyncPager:
        r"""Partitions a query by returning partition cursors
        that can be used to run the query in parallel. The
        returned partition cursors are split points that can be
        used by RunQuery as starting/end points for the query
        results.

        Args:
            request (:class:`google.cloud.firestore_v1.types.PartitionQueryRequest`):
                The request object. The request for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.firestore_v1.services.firestore.pagers.PartitionQueryAsyncPager:
                The response for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = firestore.PartitionQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.partition_query,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.PartitionQueryAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def write(
        self,
        requests: AsyncIterator[firestore.WriteRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[firestore.WriteResponse]]:
        r"""Streams batches of document updates and deletes, in
        order.

        Args:
            requests (AsyncIterator[`google.cloud.firestore_v1.types.WriteRequest`]):
                The request object AsyncIterator. The request for
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
            AsyncIterable[google.cloud.firestore_v1.types.WriteResponse]:
                The response for
                [Firestore.Write][google.firestore.v1.Firestore.Write].

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.write,
            default_timeout=86400.0,
            client_info=DEFAULT_CLIENT_INFO,
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
        requests: AsyncIterator[firestore.ListenRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[firestore.ListenResponse]]:
        r"""Listens to changes.

        Args:
            requests (AsyncIterator[`google.cloud.firestore_v1.types.ListenRequest`]):
                The request object AsyncIterator. A request for
                [Firestore.Listen][google.firestore.v1.Firestore.Listen]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.firestore_v1.types.ListenResponse]:
                The response for
                [Firestore.Listen][google.firestore.v1.Firestore.Listen].

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.listen,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=86400.0,
            ),
            default_timeout=86400.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (gapic_v1.routing_header.to_grpc_metadata(()),)

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_collection_ids(
        self,
        request: firestore.ListCollectionIdsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCollectionIdsAsyncPager:
        r"""Lists all the collection IDs underneath a document.

        Args:
            request (:class:`google.cloud.firestore_v1.types.ListCollectionIdsRequest`):
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
            google.cloud.firestore_v1.services.firestore.pagers.ListCollectionIdsAsyncPager:
                The response from
                [Firestore.ListCollectionIds][google.firestore.v1.Firestore.ListCollectionIds].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_collection_ids,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCollectionIdsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_write(
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
            request (:class:`google.cloud.firestore_v1.types.BatchWriteRequest`):
                The request object. The request for
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.firestore_v1.types.BatchWriteResponse:
                The response from
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].

        """
        # Create or coerce a protobuf request object.
        request = firestore.BatchWriteRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_write,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_document(
        self,
        request: firestore.CreateDocumentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Creates a new document.

        Args:
            request (:class:`google.cloud.firestore_v1.types.CreateDocumentRequest`):
                The request object. The request for
                [Firestore.CreateDocument][google.firestore.v1.Firestore.CreateDocument].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.firestore_v1.types.Document:
                A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

        """
        # Create or coerce a protobuf request object.
        request = firestore.CreateDocumentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_document,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-firestore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FirestoreAsyncClient",)
