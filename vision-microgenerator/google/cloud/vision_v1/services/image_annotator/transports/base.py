# -*- coding: utf-8 -*-
import abc
import typing

from google import auth
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.vision_v1.types import image_annotator
from google.longrunning import operations_pb2 as operations  # type: ignore


class ImageAnnotatorTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for ImageAnnotator."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-vision",
    )

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError

    @property
    def batch_annotate_images(
        self
    ) -> typing.Callable[
        [image_annotator.BatchAnnotateImagesRequest],
        image_annotator.BatchAnnotateImagesResponse,
    ]:
        raise NotImplementedError

    @property
    def batch_annotate_files(
        self
    ) -> typing.Callable[
        [image_annotator.BatchAnnotateFilesRequest],
        image_annotator.BatchAnnotateFilesResponse,
    ]:
        raise NotImplementedError

    @property
    def async_batch_annotate_images(
        self
    ) -> typing.Callable[
        [image_annotator.AsyncBatchAnnotateImagesRequest], operations.Operation
    ]:
        raise NotImplementedError

    @property
    def async_batch_annotate_files(
        self
    ) -> typing.Callable[
        [image_annotator.AsyncBatchAnnotateFilesRequest], operations.Operation
    ]:
        raise NotImplementedError


__all__ = ("ImageAnnotatorTransport",)
