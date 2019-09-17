# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.api_core import operation
from google.cloud.vision_v1.types import image_annotator

from .transports.base import ImageAnnotatorTransport
from .transports.grpc import ImageAnnotatorGrpcTransport


class ImageAnnotatorMeta(type):
    """Metaclass for the ImageAnnotator client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ImageAnnotatorTransport]]
    _transport_registry["grpc"] = ImageAnnotatorGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[ImageAnnotatorTransport]:
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


class ImageAnnotator(metaclass=ImageAnnotatorMeta):
    """Service that performs Google Cloud Vision API detection tasks
    over client images, such as face, landmark, logo, label, and
    text detection. The ImageAnnotator service returns detected
    entities from the images.
    """

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        transport: Union[str, ImageAnnotatorTransport] = None,
    ) -> None:
        """Instantiate the image annotator.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ImageAnnotatorTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
        """
        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ImageAnnotatorTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(credentials=credentials, host=host)

    def batch_annotate_images(
        self,
        request: image_annotator.BatchAnnotateImagesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> image_annotator.BatchAnnotateImagesResponse:
        r"""Run image detection and annotation for a batch of
        images.

        Args:
            request (:class:`~.image_annotator.BatchAnnotateImagesRequest`):
                The request object. Multiple image annotation requests
                are batched into a single service call.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.image_annotator.BatchAnnotateImagesResponse:
                Response to a batch image annotation
                request.

        """
        # Create or coerce a protobuf request object.
        request = image_annotator.BatchAnnotateImagesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.batch_annotate_images,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def batch_annotate_files(
        self,
        request: image_annotator.BatchAnnotateFilesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
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

        Args:
            request (:class:`~.image_annotator.BatchAnnotateFilesRequest`):
                The request object. A list of requests to annotate files
                using the BatchAnnotateFiles API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.image_annotator.BatchAnnotateFilesResponse:
                A list of file annotation responses.
        """
        # Create or coerce a protobuf request object.
        request = image_annotator.BatchAnnotateFilesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.batch_annotate_files,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def async_batch_annotate_images(
        self,
        request: image_annotator.AsyncBatchAnnotateImagesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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

        Args:
            request (:class:`~.image_annotator.AsyncBatchAnnotateImagesRequest`):
                The request object. Request for async image annotation
                for a list of images.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.image_annotator.AsyncBatchAnnotateImagesResponse``:
                Response to an async batch image annotation request.

        """
        # Create or coerce a protobuf request object.
        request = image_annotator.AsyncBatchAnnotateImagesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.async_batch_annotate_images,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            image_annotator.AsyncBatchAnnotateImagesResponse,
            metadata_type=image_annotator.OperationMetadata,
        )

        # Done; return the response.
        return response

    def async_batch_annotate_files(
        self,
        request: image_annotator.AsyncBatchAnnotateFilesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Run asynchronous image detection and annotation for a list of
        generic files, such as PDF files, which may contain multiple
        pages and multiple images per page. Progress and results can be
        retrieved through the ``google.longrunning.Operations``
        interface. ``Operation.metadata`` contains ``OperationMetadata``
        (metadata). ``Operation.response`` contains
        ``AsyncBatchAnnotateFilesResponse`` (results).

        Args:
            request (:class:`~.image_annotator.AsyncBatchAnnotateFilesRequest`):
                The request object. Multiple async file annotation
                requests are batched into a single service call.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.image_annotator.AsyncBatchAnnotateFilesResponse``:
                Response to an async batch file annotation request.

        """
        # Create or coerce a protobuf request object.
        request = image_annotator.AsyncBatchAnnotateFilesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.async_batch_annotate_files,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            image_annotator.AsyncBatchAnnotateFilesResponse,
            metadata_type=image_annotator.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-vision").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("ImageAnnotator",)
