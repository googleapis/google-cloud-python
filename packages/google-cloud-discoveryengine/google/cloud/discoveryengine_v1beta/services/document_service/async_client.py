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

from google.cloud.discoveryengine_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import struct_pb2  # type: ignore

from google.cloud.discoveryengine_v1beta.services.document_service import pagers
from google.cloud.discoveryengine_v1beta.types import (
    document_service,
    import_config,
    purge_config,
)
from google.cloud.discoveryengine_v1beta.types import document
from google.cloud.discoveryengine_v1beta.types import document as gcd_document

from .client import DocumentServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, DocumentServiceTransport
from .transports.grpc_asyncio import DocumentServiceGrpcAsyncIOTransport


class DocumentServiceAsyncClient:
    """Service for ingesting
    [Document][google.cloud.discoveryengine.v1beta.Document] information
    of the customer's website.
    """

    _client: DocumentServiceClient

    DEFAULT_ENDPOINT = DocumentServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DocumentServiceClient.DEFAULT_MTLS_ENDPOINT

    branch_path = staticmethod(DocumentServiceClient.branch_path)
    parse_branch_path = staticmethod(DocumentServiceClient.parse_branch_path)
    document_path = staticmethod(DocumentServiceClient.document_path)
    parse_document_path = staticmethod(DocumentServiceClient.parse_document_path)
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

    async def get_document(
        self,
        request: Optional[Union[document_service.GetDocumentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Gets a [Document][google.cloud.discoveryengine.v1beta.Document].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_get_document():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.GetDocumentRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.GetDocumentRequest, dict]]):
                The request object. Request message for
                [DocumentService.GetDocument][google.cloud.discoveryengine.v1beta.DocumentService.GetDocument]
                method.
            name (:class:`str`):
                Required. Full resource name of
                [Document][google.cloud.discoveryengine.v1beta.Document],
                such as
                ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}/documents/{document}``.

                If the caller does not have permission to access the
                [Document][google.cloud.discoveryengine.v1beta.Document],
                regardless of whether or not it exists, a
                ``PERMISSION_DENIED`` error is returned.

                If the requested
                [Document][google.cloud.discoveryengine.v1beta.Document]
                does not exist, a ``NOT_FOUND`` error is returned.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.discoveryengine_v1beta.types.Document:
                Document captures all raw metadata
                information of items to be recommended
                or searched.

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

        request = document_service.GetDocumentRequest(request)

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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_documents(
        self,
        request: Optional[Union[document_service.ListDocumentsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDocumentsAsyncPager:
        r"""Gets a list of
        [Document][google.cloud.discoveryengine.v1beta.Document]s.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_list_documents():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.ListDocumentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_documents(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.ListDocumentsRequest, dict]]):
                The request object. Request message for
                [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
                method.
            parent (:class:`str`):
                Required. The parent branch resource name, such as
                ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
                Use ``default_branch`` as the branch ID, to list
                documents under the default branch.

                If the caller does not have permission to list
                [Documents][]s under this branch, regardless of whether
                or not this branch exists, a ``PERMISSION_DENIED`` error
                is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.discoveryengine_v1beta.services.document_service.pagers.ListDocumentsAsyncPager:
                Response message for
                   [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = document_service.ListDocumentsRequest(request)

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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDocumentsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_document(
        self,
        request: Optional[Union[document_service.CreateDocumentRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        document: Optional[gcd_document.Document] = None,
        document_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_document.Document:
        r"""Creates a
        [Document][google.cloud.discoveryengine.v1beta.Document].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_create_document():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.CreateDocumentRequest(
                    parent="parent_value",
                    document_id="document_id_value",
                )

                # Make the request
                response = await client.create_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.CreateDocumentRequest, dict]]):
                The request object. Request message for
                [DocumentService.CreateDocument][google.cloud.discoveryengine.v1beta.DocumentService.CreateDocument]
                method.
            parent (:class:`str`):
                Required. The parent resource name, such as
                ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            document (:class:`google.cloud.discoveryengine_v1beta.types.Document`):
                Required. The
                [Document][google.cloud.discoveryengine.v1beta.Document]
                to create.

                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            document_id (:class:`str`):
                Required. The ID to use for the
                [Document][google.cloud.discoveryengine.v1beta.Document],
                which will become the final component of the
                [Document.name][google.cloud.discoveryengine.v1beta.Document.name].

                If the caller does not have permission to create the
                [Document][google.cloud.discoveryengine.v1beta.Document],
                regardless of whether or not it exists, a
                ``PERMISSION_DENIED`` error is returned.

                This field must be unique among all
                [Document][google.cloud.discoveryengine.v1beta.Document]s
                with the same
                [parent][google.cloud.discoveryengine.v1beta.CreateDocumentRequest.parent].
                Otherwise, an ``ALREADY_EXISTS`` error is returned.

                This field must conform to
                `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__
                standard with a length limit of 63 characters.
                Otherwise, an ``INVALID_ARGUMENT`` error is returned.

                This corresponds to the ``document_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.discoveryengine_v1beta.types.Document:
                Document captures all raw metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, document, document_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = document_service.CreateDocumentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if document is not None:
            request.document = document
        if document_id is not None:
            request.document_id = document_id

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
        request: Optional[Union[document_service.UpdateDocumentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> document.Document:
        r"""Updates a
        [Document][google.cloud.discoveryengine.v1beta.Document].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_update_document():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.UpdateDocumentRequest(
                )

                # Make the request
                response = await client.update_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.UpdateDocumentRequest, dict]]):
                The request object. Request message for
                [DocumentService.UpdateDocument][google.cloud.discoveryengine.v1beta.DocumentService.UpdateDocument]
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.discoveryengine_v1beta.types.Document:
                Document captures all raw metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        request = document_service.UpdateDocumentRequest(request)

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
        request: Optional[Union[document_service.DeleteDocumentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a
        [Document][google.cloud.discoveryengine.v1beta.Document].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_delete_document():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.DeleteDocumentRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_document(request=request)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.DeleteDocumentRequest, dict]]):
                The request object. Request message for
                [DocumentService.DeleteDocument][google.cloud.discoveryengine.v1beta.DocumentService.DeleteDocument]
                method.
            name (:class:`str`):
                Required. Full resource name of
                [Document][google.cloud.discoveryengine.v1beta.Document],
                such as
                ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}/documents/{document}``.

                If the caller does not have permission to delete the
                [Document][google.cloud.discoveryengine.v1beta.Document],
                regardless of whether or not it exists, a
                ``PERMISSION_DENIED`` error is returned.

                If the
                [Document][google.cloud.discoveryengine.v1beta.Document]
                to delete does not exist, a ``NOT_FOUND`` error is
                returned.

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

        request = document_service.DeleteDocumentRequest(request)

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
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def import_documents(
        self,
        request: Optional[Union[import_config.ImportDocumentsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Bulk import of multiple
        [Document][google.cloud.discoveryengine.v1beta.Document]s.
        Request processing may be synchronous. Non-existing items will
        be created.

        Note: It is possible for a subset of the
        [Document][google.cloud.discoveryengine.v1beta.Document]s to be
        successfully updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_import_documents():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.ImportDocumentsRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.import_documents(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.ImportDocumentsRequest, dict]]):
                The request object. Request message for Import methods.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.discoveryengine_v1beta.types.ImportDocumentsResponse` Response of the
                   [ImportDocumentsRequest][google.cloud.discoveryengine.v1beta.ImportDocumentsRequest].
                   If the long running operation is done, then this
                   message is returned by the
                   google.longrunning.Operations.response field if the
                   operation was successful.

        """
        # Create or coerce a protobuf request object.
        request = import_config.ImportDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_documents,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            import_config.ImportDocumentsResponse,
            metadata_type=import_config.ImportDocumentsMetadata,
        )

        # Done; return the response.
        return response

    async def purge_documents(
        self,
        request: Optional[Union[purge_config.PurgeDocumentsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Permanently deletes all selected
        [Document][google.cloud.discoveryengine.v1beta.Document]s in a
        branch.

        This process is asynchronous. Depending on the number of
        [Document][google.cloud.discoveryengine.v1beta.Document]s to be
        deleted, this operation can take hours to complete. Before the
        delete operation completes, some
        [Document][google.cloud.discoveryengine.v1beta.Document]s might
        still be returned by
        [DocumentService.GetDocument][google.cloud.discoveryengine.v1beta.DocumentService.GetDocument]
        or
        [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments].

        To get a list of the
        [Document][google.cloud.discoveryengine.v1beta.Document]s to be
        deleted, set
        [PurgeDocumentsRequest.force][google.cloud.discoveryengine.v1beta.PurgeDocumentsRequest.force]
        to false.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import discoveryengine_v1beta

            async def sample_purge_documents():
                # Create a client
                client = discoveryengine_v1beta.DocumentServiceAsyncClient()

                # Initialize request argument(s)
                request = discoveryengine_v1beta.PurgeDocumentsRequest(
                    parent="parent_value",
                    filter="filter_value",
                )

                # Make the request
                operation = client.purge_documents(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.discoveryengine_v1beta.types.PurgeDocumentsRequest, dict]]):
                The request object. Request message for
                [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1beta.DocumentService.PurgeDocuments]
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.discoveryengine_v1beta.types.PurgeDocumentsResponse` Response message for
                   [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1beta.DocumentService.PurgeDocuments]
                   method. If the long running operation is successfully
                   done, then this message is returned by the
                   google.longrunning.Operations.response field.

        """
        # Create or coerce a protobuf request object.
        request = purge_config.PurgeDocumentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.purge_documents,
            default_timeout=None,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            purge_config.PurgeDocumentsResponse,
            metadata_type=purge_config.PurgeDocumentsMetadata,
        )

        # Done; return the response.
        return response

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.list_operations,
            default_timeout=None,
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

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_operation,
            default_timeout=None,
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

    async def __aenter__(self) -> "DocumentServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("DocumentServiceAsyncClient",)
