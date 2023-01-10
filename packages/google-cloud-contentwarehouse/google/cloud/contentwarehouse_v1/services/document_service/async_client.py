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
from collections import OrderedDict
import functools
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.contentwarehouse_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.contentwarehouse_v1.services.document_service import pagers
from google.cloud.contentwarehouse_v1.types import (
    document_service,
    document_service_request,
    rule_engine,
)
from google.cloud.contentwarehouse_v1.types import common
from google.cloud.contentwarehouse_v1.types import document as gcc_document

from .client import DocumentServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, DocumentServiceTransport
from .transports.grpc_asyncio import DocumentServiceGrpcAsyncIOTransport


class DocumentServiceAsyncClient:
    """This service lets you manage document."""

    _client: DocumentServiceClient

    DEFAULT_ENDPOINT = DocumentServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DocumentServiceClient.DEFAULT_MTLS_ENDPOINT

    document_path = staticmethod(DocumentServiceClient.document_path)
    parse_document_path = staticmethod(DocumentServiceClient.parse_document_path)
    document_schema_path = staticmethod(DocumentServiceClient.document_schema_path)
    parse_document_schema_path = staticmethod(
        DocumentServiceClient.parse_document_schema_path
    )
    location_path = staticmethod(DocumentServiceClient.location_path)
    parse_location_path = staticmethod(DocumentServiceClient.parse_location_path)
    common_billing_account_path = staticmethod(
        DocumentServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DocumentServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DocumentServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        DocumentServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        DocumentServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        DocumentServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DocumentServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        DocumentServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(DocumentServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        DocumentServiceClient.parse_common_location_path
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
            DocumentServiceAsyncClient: The constructed client.
        """
        return DocumentServiceClient.from_service_account_info.__func__(DocumentServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DocumentServiceAsyncClient: The constructed client.
        """
        return DocumentServiceClient.from_service_account_file.__func__(DocumentServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return DocumentServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> DocumentServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DocumentServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DocumentServiceClient).get_transport_class, type(DocumentServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, DocumentServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the document service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DocumentServiceTransport]): The
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
        self._client = DocumentServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_document(
        self,
        request: Optional[
            Union[document_service_request.CreateDocumentRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        document: Optional[gcc_document.Document] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document_service.CreateDocumentResponse:
        r"""Creates a document.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_create_document():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                document = contentwarehouse_v1.Document()
                document.plain_text = "plain_text_value"
                document.raw_document_path = "raw_document_path_value"
                document.display_name = "display_name_value"

                request = contentwarehouse_v1.CreateDocumentRequest(
                    parent="parent_value",
                    document=document,
                )

                # Make the request
                response = await client.create_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.CreateDocumentRequest, dict]]):
                The request object. Request message for
                DocumentService.CreateDocument.
            parent (:class:`str`):
                Required. The parent name. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            document (:class:`google.cloud.contentwarehouse_v1.types.Document`):
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
            google.cloud.contentwarehouse_v1.types.CreateDocumentResponse:
                Response message for
                DocumentService.CreateDocument.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, document])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.CreateDocumentRequest(request)

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
            default_timeout=180.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_document(
        self,
        request: Optional[
            Union[document_service_request.GetDocumentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcc_document.Document:
        r"""Gets a document. Returns NOT_FOUND if the document does not
        exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_get_document():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.GetDocumentRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.GetDocumentRequest, dict]]):
                The request object. Request message for
                DocumentService.GetDocument.
            name (:class:`str`):
                Required. The name of the document to retrieve. Format:
                projects/{project_number}/locations/{location}/documents/{document_id}
                or
                projects/{project_number}/locations/{location}/documents/referenceId/{reference_id}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.Document:
                Defines the structure for content
                warehouse document proto.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.GetDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_document,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_document(
        self,
        request: Optional[
            Union[document_service_request.UpdateDocumentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        document: Optional[gcc_document.Document] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document_service.UpdateDocumentResponse:
        r"""Updates a document. Returns INVALID_ARGUMENT if the name of the
        document is non-empty and does not equal the existing name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_update_document():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                document = contentwarehouse_v1.Document()
                document.plain_text = "plain_text_value"
                document.raw_document_path = "raw_document_path_value"
                document.display_name = "display_name_value"

                request = contentwarehouse_v1.UpdateDocumentRequest(
                    name="name_value",
                    document=document,
                )

                # Make the request
                response = await client.update_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.UpdateDocumentRequest, dict]]):
                The request object. Request message for
                DocumentService.UpdateDocument.
            name (:class:`str`):
                Required. The name of the document to update. Format:
                projects/{project_number}/locations/{location}/documents/{document_id}
                or
                projects/{project_number}/locations/{location}/documents/referenceId/{reference_id}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            document (:class:`google.cloud.contentwarehouse_v1.types.Document`):
                Required. The document to update.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.UpdateDocumentResponse:
                Response message for
                DocumentService.UpdateDocument.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, document])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.UpdateDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if document is not None:
            request.document = document

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_document,
            default_timeout=180.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_document(
        self,
        request: Optional[
            Union[document_service_request.DeleteDocumentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a document. Returns NOT_FOUND if the document does not
        exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_delete_document():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.DeleteDocumentRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_document(request=request)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.DeleteDocumentRequest, dict]]):
                The request object. Request message for
                DocumentService.DeleteDocument.
            name (:class:`str`):
                Required. The name of the document to delete. Format:
                projects/{project_number}/locations/{location}/documents/{document_id}
                or
                projects/{project_number}/locations/{location}/documents/referenceId/{reference_id}.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.DeleteDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_document,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def search_documents(
        self,
        request: Optional[
            Union[document_service_request.SearchDocumentsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchDocumentsAsyncPager:
        r"""Searches for documents using provided
        [SearchDocumentsRequest][google.cloud.contentwarehouse.v1.SearchDocumentsRequest].
        This call only returns documents that the caller has permission
        to search against.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_search_documents():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.SearchDocumentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.search_documents(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.SearchDocumentsRequest, dict]]):
                The request object. Request message for
                DocumentService.SearchDocuments.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                documents. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.services.document_service.pagers.SearchDocumentsAsyncPager:
                Response message for
                DocumentService.SearchDocuments.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.SearchDocumentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_documents,
            default_timeout=180.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.SearchDocumentsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def fetch_acl(
        self,
        request: Optional[Union[document_service_request.FetchAclRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document_service.FetchAclResponse:
        r"""Gets the access control policy for a resource. Returns NOT_FOUND
        error if the resource does not exist. Returns an empty policy if
        the resource exists but does not have a policy set.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_fetch_acl():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.FetchAclRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.fetch_acl(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.FetchAclRequest, dict]]):
                The request object. Request message for
                DocumentService.FetchAcl
            resource (:class:`str`):
                Required. REQUIRED: The resource for which the policy is
                being requested. Format for document:
                projects/{project_number}/locations/{location}/documents/{document_id}.
                Format for project: projects/{project_number}.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.FetchAclResponse:
                Response message for
                DocumentService.FetchAcl.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.FetchAclRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_acl,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def set_acl(
        self,
        request: Optional[Union[document_service_request.SetAclRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        policy: Optional[policy_pb2.Policy] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document_service.SetAclResponse:
        r"""Sets the access control policy for a resource.
        Replaces any existing policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_set_acl():
                # Create a client
                client = contentwarehouse_v1.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.SetAclRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.set_acl(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.SetAclRequest, dict]]):
                The request object. Request message for
                DocumentService.SetAcl.
            resource (:class:`str`):
                Required. REQUIRED: The resource for which the policy is
                being requested. Format for document:
                projects/{project_number}/locations/{location}/documents/{document_id}.
                Format for project: projects/{project_number}.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            policy (:class:`google.iam.v1.policy_pb2.Policy`):
                Required. REQUIRED: The complete policy to be applied to
                the ``resource``. The size of the policy is limited to a
                few 10s of KB.

                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.SetAclResponse:
                Response message for
                DocumentService.SetAcl.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service_request.SetAclRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if resource is not None:
            request.resource = resource
        if policy is not None:
            request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_acl,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("DocumentServiceAsyncClient",)
