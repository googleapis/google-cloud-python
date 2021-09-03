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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dialogflow_v2beta1.services.documents import pagers
from google.cloud.dialogflow_v2beta1.types import document
from google.cloud.dialogflow_v2beta1.types import document as gcd_document
from google.cloud.dialogflow_v2beta1.types import gcs
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import DocumentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DocumentsGrpcAsyncIOTransport
from .client import DocumentsClient


class DocumentsAsyncClient:
    """Service for managing knowledge
    [Documents][google.cloud.dialogflow.v2beta1.Document].
    """

    _client: DocumentsClient

    DEFAULT_ENDPOINT = DocumentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DocumentsClient.DEFAULT_MTLS_ENDPOINT

    document_path = staticmethod(DocumentsClient.document_path)
    parse_document_path = staticmethod(DocumentsClient.parse_document_path)
    common_billing_account_path = staticmethod(
        DocumentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DocumentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DocumentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(DocumentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(DocumentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        DocumentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DocumentsClient.common_project_path)
    parse_common_project_path = staticmethod(DocumentsClient.parse_common_project_path)
    common_location_path = staticmethod(DocumentsClient.common_location_path)
    parse_common_location_path = staticmethod(
        DocumentsClient.parse_common_location_path
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
            DocumentsAsyncClient: The constructed client.
        """
        return DocumentsClient.from_service_account_info.__func__(DocumentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DocumentsAsyncClient: The constructed client.
        """
        return DocumentsClient.from_service_account_file.__func__(DocumentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DocumentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            DocumentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DocumentsClient).get_transport_class, type(DocumentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DocumentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the documents client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DocumentsTransport]): The
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
        self._client = DocumentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_documents(
        self,
        request: document.ListDocumentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDocumentsAsyncPager:
        r"""Returns the list of all documents of the knowledge base.

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ListDocumentsRequest`):
                The request object. Request message for
                [Documents.ListDocuments][google.cloud.dialogflow.v2beta1.Documents.ListDocuments].
            parent (:class:`str`):
                Required. The knowledge base to list all documents for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.documents.pagers.ListDocumentsAsyncPager:
                Response message for
                [Documents.ListDocuments][google.cloud.dialogflow.v2beta1.Documents.ListDocuments].

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

        request = document.ListDocumentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_documents,
            default_timeout=None,
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

    async def get_document(
        self,
        request: document.GetDocumentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Retrieves the specified document.

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.GetDocumentRequest`):
                The request object. Request message for
                [Documents.GetDocument][google.cloud.dialogflow.v2beta1.Documents.GetDocument].
            name (:class:`str`):
                Required. The name of the document to retrieve. Format
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Document:
                A knowledge document to be used by a
                [KnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBase].

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases.documents
                   resource is deprecated; only use
                   projects.knowledgeBases.documents.

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

        request = document.GetDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_document,
            default_timeout=None,
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

    async def create_document(
        self,
        request: gcd_document.CreateDocumentRequest = None,
        *,
        parent: str = None,
        document: gcd_document.Document = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new document.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [KnowledgeOperationMetadata][google.cloud.dialogflow.v2beta1.KnowledgeOperationMetadata]
        -  ``response``:
           [Document][google.cloud.dialogflow.v2beta1.Document]

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.CreateDocumentRequest`):
                The request object. Request message for
                [Documents.CreateDocument][google.cloud.dialogflow.v2beta1.Documents.CreateDocument].
            parent (:class:`str`):
                Required. The knowledge base to create a document for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            document (:class:`google.cloud.dialogflow_v2beta1.types.Document`):
                Required. The document to create.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2beta1.types.Document`
                A knowledge document to be used by a
                [KnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBase].

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases.documents
                   resource is deprecated; only use
                   projects.knowledgeBases.documents.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, document])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_document.CreateDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if document is not None:
            request.document = document

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_document,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcd_document.Document,
            metadata_type=gcd_document.KnowledgeOperationMetadata,
        )

        # Done; return the response.
        return response

    async def import_documents(
        self,
        request: document.ImportDocumentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create documents by importing data from external sources.
        Dialogflow supports up to 350 documents in each request. If you
        try to import more, Dialogflow will return an error.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [KnowledgeOperationMetadata][google.cloud.dialogflow.v2beta1.KnowledgeOperationMetadata]
        -  ``response``:
           [ImportDocumentsResponse][google.cloud.dialogflow.v2beta1.ImportDocumentsResponse]

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ImportDocumentsRequest`):
                The request object. Request message for
                [Documents.ImportDocuments][google.cloud.dialogflow.v2beta1.Documents.ImportDocuments].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2beta1.types.ImportDocumentsResponse`
                Response message for
                [Documents.ImportDocuments][google.cloud.dialogflow.v2beta1.Documents.ImportDocuments].

        """
        # Create or coerce a protobuf request object.
        request = document.ImportDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_documents,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            document.ImportDocumentsResponse,
            metadata_type=document.KnowledgeOperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_document(
        self,
        request: document.DeleteDocumentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes the specified document.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [KnowledgeOperationMetadata][google.cloud.dialogflow.v2beta1.KnowledgeOperationMetadata]
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.DeleteDocumentRequest`):
                The request object. Request message for
                [Documents.DeleteDocument][google.cloud.dialogflow.v2beta1.Documents.DeleteDocument].
            name (:class:`str`):
                Required. The name of the document to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = document.DeleteDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_document,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=document.KnowledgeOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_document(
        self,
        request: gcd_document.UpdateDocumentRequest = None,
        *,
        document: gcd_document.Document = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified document.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [KnowledgeOperationMetadata][google.cloud.dialogflow.v2beta1.KnowledgeOperationMetadata]
        -  ``response``:
           [Document][google.cloud.dialogflow.v2beta1.Document]

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.UpdateDocumentRequest`):
                The request object. Request message for
                [Documents.UpdateDocument][google.cloud.dialogflow.v2beta1.Documents.UpdateDocument].
            document (:class:`google.cloud.dialogflow_v2beta1.types.Document`):
                Required. The document to update.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Not specified means ``update all``. Currently,
                only ``display_name`` can be updated, an InvalidArgument
                will be returned for attempting to update other fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2beta1.types.Document`
                A knowledge document to be used by a
                [KnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBase].

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases.documents
                   resource is deprecated; only use
                   projects.knowledgeBases.documents.

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

        request = gcd_document.UpdateDocumentRequest(request)

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
            default_timeout=None,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcd_document.Document,
            metadata_type=gcd_document.KnowledgeOperationMetadata,
        )

        # Done; return the response.
        return response

    async def reload_document(
        self,
        request: document.ReloadDocumentRequest = None,
        *,
        name: str = None,
        gcs_source: gcs.GcsSource = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Reloads the specified document from its specified source,
        content_uri or content. The previously loaded content of the
        document will be deleted. Note: Even when the content of the
        document has not changed, there still may be side effects
        because of internal implementation changes. Note: If the
        document source is Google Cloud Storage URI, its metadata will
        be replaced with the custom metadata from Google Cloud Storage
        if the ``import_gcs_custom_metadata`` field is set to true in
        the request.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [KnowledgeOperationMetadata][google.cloud.dialogflow.v2beta1.KnowledgeOperationMetadata]
        -  ``response``:
           [Document][google.cloud.dialogflow.v2beta1.Document]

        Note: The ``projects.agent.knowledgeBases.documents`` resource
        is deprecated; only use ``projects.knowledgeBases.documents``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ReloadDocumentRequest`):
                The request object. Request message for
                [Documents.ReloadDocument][google.cloud.dialogflow.v2beta1.Documents.ReloadDocument].
            name (:class:`str`):
                Required. The name of the document to reload. Format:
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gcs_source (:class:`google.cloud.dialogflow_v2beta1.types.GcsSource`):
                The path for a Cloud Storage source
                file for reloading document content. If
                not provided, the Document's existing
                source will be reloaded.

                This corresponds to the ``gcs_source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2beta1.types.Document`
                A knowledge document to be used by a
                [KnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBase].

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases.documents
                   resource is deprecated; only use
                   projects.knowledgeBases.documents.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, gcs_source])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document.ReloadDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if gcs_source is not None:
            request.gcs_source = gcs_source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reload_document,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            document.Document,
            metadata_type=document.KnowledgeOperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DocumentsAsyncClient",)
