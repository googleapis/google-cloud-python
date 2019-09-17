# -*- coding: utf-8 -*-
from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.vision_v1.types import image_annotator
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import ImageAnnotatorTransport


class ImageAnnotatorGrpcTransport(ImageAnnotatorTransport):
    """gRPC backend transport for ImageAnnotator.

    Service that performs Google Cloud Vision API detection tasks
    over client images, such as face, landmark, logo, label, and
    text detection. The ImageAnnotator service returns detected
    entities from the images.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
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
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = grpc_helpers.create_channel(
                self._host, credentials=self._credentials, scopes=self.AUTH_SCOPES
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def batch_annotate_images(
        self
    ) -> Callable[
        [image_annotator.BatchAnnotateImagesRequest],
        image_annotator.BatchAnnotateImagesResponse,
    ]:
        r"""Return a callable for the batch annotate images method over gRPC.

        Run image detection and annotation for a batch of
        images.

        Returns:
            Callable[[~.BatchAnnotateImagesRequest],
                    ~.BatchAnnotateImagesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_annotate_images" not in self._stubs:
            self._stubs["batch_annotate_images"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1.ImageAnnotator/BatchAnnotateImages",
                request_serializer=image_annotator.BatchAnnotateImagesRequest.serialize,
                response_deserializer=image_annotator.BatchAnnotateImagesResponse.deserialize,
            )
        return self._stubs["batch_annotate_images"]

    @property
    def batch_annotate_files(
        self
    ) -> Callable[
        [image_annotator.BatchAnnotateFilesRequest],
        image_annotator.BatchAnnotateFilesResponse,
    ]:
        r"""Return a callable for the batch annotate files method over gRPC.

        Service that performs image detection and annotation
        for a batch of files. Now only "application/pdf",
        "image/tiff" and "image/gif" are supported.
        This service will extract at most 5 (customers can
        specify which 5 in AnnotateFileRequest.pages) frames
        (gif) or pages (pdf or tiff) from each file provided and
        perform detection and annotation for each image
        extracted.

        Returns:
            Callable[[~.BatchAnnotateFilesRequest],
                    ~.BatchAnnotateFilesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_annotate_files" not in self._stubs:
            self._stubs["batch_annotate_files"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1.ImageAnnotator/BatchAnnotateFiles",
                request_serializer=image_annotator.BatchAnnotateFilesRequest.serialize,
                response_deserializer=image_annotator.BatchAnnotateFilesResponse.deserialize,
            )
        return self._stubs["batch_annotate_files"]

    @property
    def async_batch_annotate_images(
        self
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateImagesRequest], operations.Operation
    ]:
        r"""Return a callable for the async batch annotate images method over gRPC.

        Run asynchronous image detection and annotation for a list of
        images.

        Progress and results can be retrieved through the
        ``google.longrunning.Operations`` interface.
        ``Operation.metadata`` contains ``OperationMetadata``
        (metadata). ``Operation.response`` contains
        ``AsyncBatchAnnotateImagesResponse`` (results).

        This service will write image annotation outputs to json files
        in customer GCS bucket, each json file containing
        BatchAnnotateImagesResponse proto.

        Returns:
            Callable[[~.AsyncBatchAnnotateImagesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "async_batch_annotate_images" not in self._stubs:
            self._stubs["async_batch_annotate_images"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1.ImageAnnotator/AsyncBatchAnnotateImages",
                request_serializer=image_annotator.AsyncBatchAnnotateImagesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["async_batch_annotate_images"]

    @property
    def async_batch_annotate_files(
        self
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateFilesRequest], operations.Operation
    ]:
        r"""Return a callable for the async batch annotate files method over gRPC.

        Run asynchronous image detection and annotation for a list of
        generic files, such as PDF files, which may contain multiple
        pages and multiple images per page. Progress and results can be
        retrieved through the ``google.longrunning.Operations``
        interface. ``Operation.metadata`` contains ``OperationMetadata``
        (metadata). ``Operation.response`` contains
        ``AsyncBatchAnnotateFilesResponse`` (results).

        Returns:
            Callable[[~.AsyncBatchAnnotateFilesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "async_batch_annotate_files" not in self._stubs:
            self._stubs["async_batch_annotate_files"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1.ImageAnnotator/AsyncBatchAnnotateFiles",
                request_serializer=image_annotator.AsyncBatchAnnotateFilesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["async_batch_annotate_files"]


__all__ = ("ImageAnnotatorGrpcTransport",)
