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
from collections import OrderedDict
import re
from typing import (
    Callable,
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
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.vision_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from google.cloud.vision_v1.types import image_annotator

from .client import ImageAnnotatorClient
from .transports.base import DEFAULT_CLIENT_INFO, ImageAnnotatorTransport
from .transports.grpc_asyncio import ImageAnnotatorGrpcAsyncIOTransport


class ImageAnnotatorAsyncClient:
    """Service that performs Google Cloud Vision API detection tasks
    over client images, such as face, landmark, logo, label, and
    text detection. The ImageAnnotator service returns detected
    entities from the images.
    """

    _client: ImageAnnotatorClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ImageAnnotatorClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ImageAnnotatorClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = ImageAnnotatorClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = ImageAnnotatorClient._DEFAULT_UNIVERSE

    product_path = staticmethod(ImageAnnotatorClient.product_path)
    parse_product_path = staticmethod(ImageAnnotatorClient.parse_product_path)
    product_set_path = staticmethod(ImageAnnotatorClient.product_set_path)
    parse_product_set_path = staticmethod(ImageAnnotatorClient.parse_product_set_path)
    common_billing_account_path = staticmethod(
        ImageAnnotatorClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ImageAnnotatorClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ImageAnnotatorClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ImageAnnotatorClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ImageAnnotatorClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ImageAnnotatorClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ImageAnnotatorClient.common_project_path)
    parse_common_project_path = staticmethod(
        ImageAnnotatorClient.parse_common_project_path
    )
    common_location_path = staticmethod(ImageAnnotatorClient.common_location_path)
    parse_common_location_path = staticmethod(
        ImageAnnotatorClient.parse_common_location_path
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
            ImageAnnotatorAsyncClient: The constructed client.
        """
        return ImageAnnotatorClient.from_service_account_info.__func__(ImageAnnotatorAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ImageAnnotatorAsyncClient: The constructed client.
        """
        return ImageAnnotatorClient.from_service_account_file.__func__(ImageAnnotatorAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ImageAnnotatorClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ImageAnnotatorTransport:
        """Returns the transport used by the client instance.

        Returns:
            ImageAnnotatorTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = ImageAnnotatorClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, ImageAnnotatorTransport, Callable[..., ImageAnnotatorTransport]]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the image annotator async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ImageAnnotatorTransport,Callable[..., ImageAnnotatorTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ImageAnnotatorTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = ImageAnnotatorClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def batch_annotate_images(
        self,
        request: Optional[
            Union[image_annotator.BatchAnnotateImagesRequest, dict]
        ] = None,
        *,
        requests: Optional[
            MutableSequence[image_annotator.AnnotateImageRequest]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> image_annotator.BatchAnnotateImagesResponse:
        r"""Run image detection and annotation for a batch of
        images.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import vision_v1

            async def sample_batch_annotate_images():
                # Create a client
                client = vision_v1.ImageAnnotatorAsyncClient()

                # Initialize request argument(s)
                request = vision_v1.BatchAnnotateImagesRequest(
                )

                # Make the request
                response = await client.batch_annotate_images(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.vision_v1.types.BatchAnnotateImagesRequest, dict]]):
                The request object. Multiple image annotation requests
                are batched into a single service call.
            requests (:class:`MutableSequence[google.cloud.vision_v1.types.AnnotateImageRequest]`):
                Required. Individual image annotation
                requests for this batch.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vision_v1.types.BatchAnnotateImagesResponse:
                Response to a batch image annotation
                request.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, image_annotator.BatchAnnotateImagesRequest):
            request = image_annotator.BatchAnnotateImagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if requests:
            request.requests.extend(requests)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.batch_annotate_images
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_annotate_files(
        self,
        request: Optional[
            Union[image_annotator.BatchAnnotateFilesRequest, dict]
        ] = None,
        *,
        requests: Optional[MutableSequence[image_annotator.AnnotateFileRequest]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> image_annotator.BatchAnnotateFilesResponse:
        r"""Service that performs image detection and annotation
        for a batch of files. Now only "application/pdf",
        "image/tiff" and "image/gif" are supported.

        This service will extract at most 5 (customers can
        specify which 5 in AnnotateFileRequest.pages) frames
        (gif) or pages (pdf or tiff) from each file provided and
        perform detection and annotation for each image
        extracted.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import vision_v1

            async def sample_batch_annotate_files():
                # Create a client
                client = vision_v1.ImageAnnotatorAsyncClient()

                # Initialize request argument(s)
                request = vision_v1.BatchAnnotateFilesRequest(
                )

                # Make the request
                response = await client.batch_annotate_files(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.vision_v1.types.BatchAnnotateFilesRequest, dict]]):
                The request object. A list of requests to annotate files
                using the BatchAnnotateFiles API.
            requests (:class:`MutableSequence[google.cloud.vision_v1.types.AnnotateFileRequest]`):
                Required. The list of file annotation
                requests. Right now we support only one
                AnnotateFileRequest in
                BatchAnnotateFilesRequest.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vision_v1.types.BatchAnnotateFilesResponse:
                A list of file annotation responses.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, image_annotator.BatchAnnotateFilesRequest):
            request = image_annotator.BatchAnnotateFilesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if requests:
            request.requests.extend(requests)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.batch_annotate_files
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def async_batch_annotate_images(
        self,
        request: Optional[
            Union[image_annotator.AsyncBatchAnnotateImagesRequest, dict]
        ] = None,
        *,
        requests: Optional[
            MutableSequence[image_annotator.AnnotateImageRequest]
        ] = None,
        output_config: Optional[image_annotator.OutputConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Run asynchronous image detection and annotation for a list of
        images.

        Progress and results can be retrieved through the
        ``google.longrunning.Operations`` interface.
        ``Operation.metadata`` contains ``OperationMetadata``
        (metadata). ``Operation.response`` contains
        ``AsyncBatchAnnotateImagesResponse`` (results).

        This service will write image annotation outputs to json files
        in customer GCS bucket, each json file containing
        BatchAnnotateImagesResponse proto.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import vision_v1

            async def sample_async_batch_annotate_images():
                # Create a client
                client = vision_v1.ImageAnnotatorAsyncClient()

                # Initialize request argument(s)
                request = vision_v1.AsyncBatchAnnotateImagesRequest(
                )

                # Make the request
                operation = client.async_batch_annotate_images(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.vision_v1.types.AsyncBatchAnnotateImagesRequest, dict]]):
                The request object. Request for async image annotation
                for a list of images.
            requests (:class:`MutableSequence[google.cloud.vision_v1.types.AnnotateImageRequest]`):
                Required. Individual image annotation
                requests for this batch.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`google.cloud.vision_v1.types.OutputConfig`):
                Required. The desired output location
                and metadata (e.g. format).

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vision_v1.types.AsyncBatchAnnotateImagesResponse`
                Response to an async batch image annotation request.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([requests, output_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, image_annotator.AsyncBatchAnnotateImagesRequest):
            request = image_annotator.AsyncBatchAnnotateImagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if output_config is not None:
            request.output_config = output_config
        if requests:
            request.requests.extend(requests)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.async_batch_annotate_images
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

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
            image_annotator.AsyncBatchAnnotateImagesResponse,
            metadata_type=image_annotator.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def async_batch_annotate_files(
        self,
        request: Optional[
            Union[image_annotator.AsyncBatchAnnotateFilesRequest, dict]
        ] = None,
        *,
        requests: Optional[
            MutableSequence[image_annotator.AsyncAnnotateFileRequest]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Run asynchronous image detection and annotation for a list of
        generic files, such as PDF files, which may contain multiple
        pages and multiple images per page. Progress and results can be
        retrieved through the ``google.longrunning.Operations``
        interface. ``Operation.metadata`` contains ``OperationMetadata``
        (metadata). ``Operation.response`` contains
        ``AsyncBatchAnnotateFilesResponse`` (results).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import vision_v1

            async def sample_async_batch_annotate_files():
                # Create a client
                client = vision_v1.ImageAnnotatorAsyncClient()

                # Initialize request argument(s)
                request = vision_v1.AsyncBatchAnnotateFilesRequest(
                )

                # Make the request
                operation = client.async_batch_annotate_files(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.vision_v1.types.AsyncBatchAnnotateFilesRequest, dict]]):
                The request object. Multiple async file annotation
                requests are batched into a single
                service call.
            requests (:class:`MutableSequence[google.cloud.vision_v1.types.AsyncAnnotateFileRequest]`):
                Required. Individual async file
                annotation requests for this batch.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vision_v1.types.AsyncBatchAnnotateFilesResponse`
                Response to an async batch file annotation request.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, image_annotator.AsyncBatchAnnotateFilesRequest):
            request = image_annotator.AsyncBatchAnnotateFilesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if requests:
            request.requests.extend(requests)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.async_batch_annotate_files
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

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
            image_annotator.AsyncBatchAnnotateFilesResponse,
            metadata_type=image_annotator.OperationMetadata,
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
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
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
        rpc = self.transport._wrapped_methods[self._client._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "ImageAnnotatorAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ImageAnnotatorAsyncClient",)
