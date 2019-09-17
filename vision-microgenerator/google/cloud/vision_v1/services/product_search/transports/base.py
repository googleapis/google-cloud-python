# -*- coding: utf-8 -*-
import abc
import typing

from google import auth
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.vision_v1.types import product_search_service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


class ProductSearchTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for ProductSearch."""

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
    def create_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.CreateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        raise NotImplementedError

    @property
    def list_product_sets(
        self
    ) -> typing.Callable[
        [product_search_service.ListProductSetsRequest],
        product_search_service.ListProductSetsResponse,
    ]:
        raise NotImplementedError

    @property
    def get_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.GetProductSetRequest], product_search_service.ProductSet
    ]:
        raise NotImplementedError

    @property
    def update_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.UpdateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        raise NotImplementedError

    @property
    def delete_product_set(
        self
    ) -> typing.Callable[[product_search_service.DeleteProductSetRequest], empty.Empty]:
        raise NotImplementedError

    @property
    def create_product(
        self
    ) -> typing.Callable[
        [product_search_service.CreateProductRequest], product_search_service.Product
    ]:
        raise NotImplementedError

    @property
    def list_products(
        self
    ) -> typing.Callable[
        [product_search_service.ListProductsRequest],
        product_search_service.ListProductsResponse,
    ]:
        raise NotImplementedError

    @property
    def get_product(
        self
    ) -> typing.Callable[
        [product_search_service.GetProductRequest], product_search_service.Product
    ]:
        raise NotImplementedError

    @property
    def update_product(
        self
    ) -> typing.Callable[
        [product_search_service.UpdateProductRequest], product_search_service.Product
    ]:
        raise NotImplementedError

    @property
    def delete_product(
        self
    ) -> typing.Callable[[product_search_service.DeleteProductRequest], empty.Empty]:
        raise NotImplementedError

    @property
    def create_reference_image(
        self
    ) -> typing.Callable[
        [product_search_service.CreateReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        raise NotImplementedError

    @property
    def delete_reference_image(
        self
    ) -> typing.Callable[
        [product_search_service.DeleteReferenceImageRequest], empty.Empty
    ]:
        raise NotImplementedError

    @property
    def list_reference_images(
        self
    ) -> typing.Callable[
        [product_search_service.ListReferenceImagesRequest],
        product_search_service.ListReferenceImagesResponse,
    ]:
        raise NotImplementedError

    @property
    def get_reference_image(
        self
    ) -> typing.Callable[
        [product_search_service.GetReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        raise NotImplementedError

    @property
    def add_product_to_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.AddProductToProductSetRequest], empty.Empty
    ]:
        raise NotImplementedError

    @property
    def remove_product_from_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.RemoveProductFromProductSetRequest], empty.Empty
    ]:
        raise NotImplementedError

    @property
    def list_products_in_product_set(
        self
    ) -> typing.Callable[
        [product_search_service.ListProductsInProductSetRequest],
        product_search_service.ListProductsInProductSetResponse,
    ]:
        raise NotImplementedError

    @property
    def import_product_sets(
        self
    ) -> typing.Callable[
        [product_search_service.ImportProductSetsRequest], operations.Operation
    ]:
        raise NotImplementedError

    @property
    def purge_products(
        self
    ) -> typing.Callable[
        [product_search_service.PurgeProductsRequest], operations.Operation
    ]:
        raise NotImplementedError


__all__ = ("ProductSearchTransport",)
