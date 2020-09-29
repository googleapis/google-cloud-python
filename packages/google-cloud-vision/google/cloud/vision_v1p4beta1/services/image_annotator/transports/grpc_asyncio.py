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
from google.api_core import operations_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.vision_v1p4beta1.types import image_annotator
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import ImageAnnotatorTransport, DEFAULT_CLIENT_INFO
from .grpc import ImageAnnotatorGrpcTransport


class ImageAnnotatorGrpcAsyncIOTransport(ImageAnnotatorTransport):
    """gRPC AsyncIO backend transport for ImageAnnotator.

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

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
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
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
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
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def batch_annotate_images(
        self,
    ) -> Callable[
        [image_annotator.BatchAnnotateImagesRequest],
        Awaitable[image_annotator.BatchAnnotateImagesResponse],
    ]:
        r"""Return a callable for the batch annotate images method over gRPC.

        Run image detection and annotation for a batch of
        images.

        Returns:
            Callable[[~.BatchAnnotateImagesRequest],
                    Awaitable[~.BatchAnnotateImagesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_annotate_images" not in self._stubs:
            self._stubs["batch_annotate_images"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1p4beta1.ImageAnnotator/BatchAnnotateImages",
                request_serializer=image_annotator.BatchAnnotateImagesRequest.serialize,
                response_deserializer=image_annotator.BatchAnnotateImagesResponse.deserialize,
            )
        return self._stubs["batch_annotate_images"]

    @property
    def batch_annotate_files(
        self,
    ) -> Callable[
        [image_annotator.BatchAnnotateFilesRequest],
        Awaitable[image_annotator.BatchAnnotateFilesResponse],
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
                    Awaitable[~.BatchAnnotateFilesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_annotate_files" not in self._stubs:
            self._stubs["batch_annotate_files"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1p4beta1.ImageAnnotator/BatchAnnotateFiles",
                request_serializer=image_annotator.BatchAnnotateFilesRequest.serialize,
                response_deserializer=image_annotator.BatchAnnotateFilesResponse.deserialize,
            )
        return self._stubs["batch_annotate_files"]

    @property
    def async_batch_annotate_images(
        self,
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateImagesRequest],
        Awaitable[operations.Operation],
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
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "async_batch_annotate_images" not in self._stubs:
            self._stubs["async_batch_annotate_images"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1p4beta1.ImageAnnotator/AsyncBatchAnnotateImages",
                request_serializer=image_annotator.AsyncBatchAnnotateImagesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["async_batch_annotate_images"]

    @property
    def async_batch_annotate_files(
        self,
    ) -> Callable[
        [image_annotator.AsyncBatchAnnotateFilesRequest],
        Awaitable[operations.Operation],
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
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "async_batch_annotate_files" not in self._stubs:
            self._stubs["async_batch_annotate_files"] = self.grpc_channel.unary_unary(
                "/google.cloud.vision.v1p4beta1.ImageAnnotator/AsyncBatchAnnotateFiles",
                request_serializer=image_annotator.AsyncBatchAnnotateFilesRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["async_batch_annotate_files"]


__all__ = ("ImageAnnotatorGrpcAsyncIOTransport",)
