# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.api_core import operation
from google.cloud.vision_v1.services.product_search import pagers
from google.cloud.vision_v1.types import product_search_service
from google.protobuf import empty_pb2 as empty  # type: ignore

from .transports.base import ProductSearchTransport
from .transports.grpc import ProductSearchGrpcTransport


class ProductSearchMeta(type):
    """Metaclass for the ProductSearch client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[ProductSearchTransport]]
    _transport_registry["grpc"] = ProductSearchGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[ProductSearchTransport]:
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


class ProductSearch(metaclass=ProductSearchMeta):
    """Manages Products and ProductSets of reference images for use in
    product search. It uses the following resource model:

    -  The API has a collection of
       [ProductSet][google.cloud.vision.v1.ProductSet] resources, named
       ``projects/*/locations/*/productSets/*``, which acts as a way to
       put different products into groups to limit identification.

    In parallel,

    -  The API has a collection of
       [Product][google.cloud.vision.v1.Product] resources, named
       ``projects/*/locations/*/products/*``

    -  Each [Product][google.cloud.vision.v1.Product] has a collection
       of [ReferenceImage][google.cloud.vision.v1.ReferenceImage]
       resources, named
       ``projects/*/locations/*/products/*/referenceImages/*``
    """

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        transport: Union[str, ProductSearchTransport] = None,
    ) -> None:
        """Instantiate the product search.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ProductSearchTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
        """
        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ProductSearchTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(credentials=credentials, host=host)

    def create_product_set(
        self,
        request: product_search_service.CreateProductSetRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ProductSet:
        r"""Creates and returns a new ProductSet resource.

        Possible errors:

        -  Returns INVALID_ARGUMENT if display_name is missing, or is
           longer than 4096 characters.

        Args:
            request (:class:`~.product_search_service.CreateProductSetRequest`):
                The request object. Request message for the
                `CreateProductSet` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.ProductSet:
                A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

        """
        # Create or coerce a protobuf request object.
        request = product_search_service.CreateProductSetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_product_set,
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

    def list_product_sets(
        self,
        request: product_search_service.ListProductSetsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductSetsPager:
        r"""Lists ProductSets in an unspecified order.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100, or
           less than 1.

        Args:
            request (:class:`~.product_search_service.ListProductSetsRequest`):
                The request object. Request message for the
                `ListProductSets` method.
            parent (:class:`str`):
                Required. The project from which ProductSets should be
                listed.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListProductSetsPager:
                Response message for the ``ListProductSets`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.ListProductSetsRequest(request)
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_product_sets,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListProductSetsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_product_set(
        self,
        request: product_search_service.GetProductSetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ProductSet:
        r"""Gets information associated with a ProductSet.

        Possible errors:

        -  Returns NOT_FOUND if the ProductSet does not exist.

        Args:
            request (:class:`~.product_search_service.GetProductSetRequest`):
                The request object. Request message for the
                `GetProductSet` method.
            name (:class:`str`):
                Required. Resource name of the ProductSet to get.

                Format is:
                ``projects/PROJECT_ID/locations/LOG_ID/productSets/PRODUCT_SET_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.ProductSet:
                A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.GetProductSetRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_product_set,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_product_set(
        self,
        request: product_search_service.UpdateProductSetRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ProductSet:
        r"""Makes changes to a ProductSet resource. Only display_name can be
        updated currently.

        Possible errors:

        -  Returns NOT_FOUND if the ProductSet does not exist.
        -  Returns INVALID_ARGUMENT if display_name is present in
           update_mask but missing from the request or longer than 4096
           characters.

        Args:
            request (:class:`~.product_search_service.UpdateProductSetRequest`):
                The request object. Request message for the
                `UpdateProductSet` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.ProductSet:
                A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

        """
        # Create or coerce a protobuf request object.
        request = product_search_service.UpdateProductSetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_product_set,
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

    def delete_product_set(
        self,
        request: product_search_service.DeleteProductSetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes a ProductSet. Products and
        ReferenceImages in the ProductSet are not deleted.
        The actual image files are not deleted from Google Cloud
        Storage.

        Args:
            request (:class:`~.product_search_service.DeleteProductSetRequest`):
                The request object. Request message for the
                `DeleteProductSet` method.
            name (:class:`str`):
                Required. Resource name of the ProductSet to delete.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.DeleteProductSetRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_product_set,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def create_product(
        self,
        request: product_search_service.CreateProductRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.Product:
        r"""Creates and returns a new product resource.

        Possible errors:

        -  Returns INVALID_ARGUMENT if display_name is missing or longer
           than 4096 characters.
        -  Returns INVALID_ARGUMENT if description is longer than 4096
           characters.
        -  Returns INVALID_ARGUMENT if product_category is missing or
           invalid.

        Args:
            request (:class:`~.product_search_service.CreateProductRequest`):
                The request object. Request message for the
                `CreateProduct` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.Product:
                A Product contains ReferenceImages.
        """
        # Create or coerce a protobuf request object.
        request = product_search_service.CreateProductRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_product,
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

    def list_products(
        self,
        request: product_search_service.ListProductsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductsPager:
        r"""Lists products in an unspecified order.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100 or
           less than 1.

        Args:
            request (:class:`~.product_search_service.ListProductsRequest`):
                The request object. Request message for the
                `ListProducts` method.
            parent (:class:`str`):
                Required. The project OR ProductSet from which Products
                should be listed.

                Format: ``projects/PROJECT_ID/locations/LOC_ID``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListProductsPager:
                Response message for the ``ListProducts`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.ListProductsRequest(request)
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_products,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListProductsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_product(
        self,
        request: product_search_service.GetProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.Product:
        r"""Gets information associated with a Product.

        Possible errors:

        -  Returns NOT_FOUND if the Product does not exist.

        Args:
            request (:class:`~.product_search_service.GetProductRequest`):
                The request object. Request message for the `GetProduct`
                method.
            name (:class:`str`):
                Required. Resource name of the Product to get.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.Product:
                A Product contains ReferenceImages.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.GetProductRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_product,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_product(
        self,
        request: product_search_service.UpdateProductRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.Product:
        r"""Makes changes to a Product resource. Only the ``display_name``,
        ``description``, and ``labels`` fields can be updated right now.

        If labels are updated, the change will not be reflected in
        queries until the next index time.

        Possible errors:

        -  Returns NOT_FOUND if the Product does not exist.
        -  Returns INVALID_ARGUMENT if display_name is present in
           update_mask but is missing from the request or longer than
           4096 characters.
        -  Returns INVALID_ARGUMENT if description is present in
           update_mask but is longer than 4096 characters.
        -  Returns INVALID_ARGUMENT if product_category is present in
           update_mask.

        Args:
            request (:class:`~.product_search_service.UpdateProductRequest`):
                The request object. Request message for the
                `UpdateProduct` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.Product:
                A Product contains ReferenceImages.
        """
        # Create or coerce a protobuf request object.
        request = product_search_service.UpdateProductRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_product,
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

    def delete_product(
        self,
        request: product_search_service.DeleteProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes a product and its reference
        images.
        Metadata of the product and all its images will be
        deleted right away, but search queries against
        ProductSets containing the product may still work until
        all related caches are refreshed.

        Args:
            request (:class:`~.product_search_service.DeleteProductRequest`):
                The request object. Request message for the
                `DeleteProduct` method.
            name (:class:`str`):
                Required. Resource name of product to delete.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.DeleteProductRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_product,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def create_reference_image(
        self,
        request: product_search_service.CreateReferenceImageRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ReferenceImage:
        r"""Creates and returns a new ReferenceImage resource.

        The ``bounding_poly`` field is optional. If ``bounding_poly`` is
        not specified, the system will try to detect regions of interest
        in the image that are compatible with the product_category on
        the parent product. If it is specified, detection is ALWAYS
        skipped. The system converts polygons into non-rotated
        rectangles.

        Note that the pipeline will resize the image if the image
        resolution is too large to process (above 50MP).

        Possible errors:

        -  Returns INVALID_ARGUMENT if the image_uri is missing or
           longer than 4096 characters.
        -  Returns INVALID_ARGUMENT if the product does not exist.
        -  Returns INVALID_ARGUMENT if bounding_poly is not provided,
           and nothing compatible with the parent product's
           product_category is detected.
        -  Returns INVALID_ARGUMENT if bounding_poly contains more than
           10 polygons.

        Args:
            request (:class:`~.product_search_service.CreateReferenceImageRequest`):
                The request object. Request message for the
                `CreateReferenceImage` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.ReferenceImage:
                A ``ReferenceImage`` represents a product image and its
                associated metadata, such as bounding boxes.

        """
        # Create or coerce a protobuf request object.
        request = product_search_service.CreateReferenceImageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_reference_image,
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

    def delete_reference_image(
        self,
        request: product_search_service.DeleteReferenceImageRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes a reference image.
        The image metadata will be deleted right away, but
        search queries against ProductSets containing the image
        may still work until all related caches are refreshed.

        The actual image files are not deleted from Google Cloud
        Storage.

        Args:
            request (:class:`~.product_search_service.DeleteReferenceImageRequest`):
                The request object. Request message for the
                `DeleteReferenceImage` method.
            name (:class:`str`):
                Required. The resource name of the reference image to
                delete.

                Format is:

                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.DeleteReferenceImageRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_reference_image,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def list_reference_images(
        self,
        request: product_search_service.ListReferenceImagesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReferenceImagesPager:
        r"""Lists reference images.

        Possible errors:

        -  Returns NOT_FOUND if the parent product does not exist.
        -  Returns INVALID_ARGUMENT if the page_size is greater than
           100, or less than 1.

        Args:
            request (:class:`~.product_search_service.ListReferenceImagesRequest`):
                The request object. Request message for the
                `ListReferenceImages` method.
            parent (:class:`str`):
                Required. Resource name of the product containing the
                reference images.

                Format is
                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListReferenceImagesPager:
                Response message for the ``ListReferenceImages`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.ListReferenceImagesRequest(request)
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_reference_images,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListReferenceImagesPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_reference_image(
        self,
        request: product_search_service.GetReferenceImageRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ReferenceImage:
        r"""Gets information associated with a ReferenceImage.

        Possible errors:

        -  Returns NOT_FOUND if the specified image does not exist.

        Args:
            request (:class:`~.product_search_service.GetReferenceImageRequest`):
                The request object. Request message for the
                `GetReferenceImage` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.product_search_service.ReferenceImage:
                A ``ReferenceImage`` represents a product image and its
                associated metadata, such as bounding boxes.

        """
        # Create or coerce a protobuf request object.
        request = product_search_service.GetReferenceImageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_reference_image,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def add_product_to_product_set(
        self,
        request: product_search_service.AddProductToProductSetRequest = None,
        *,
        name: str = None,
        product: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Adds a Product to the specified ProductSet. If the Product is
        already present, no change is made.

        One Product can be added to at most 100 ProductSets.

        Possible errors:

        -  Returns NOT_FOUND if the Product or the ProductSet doesn't
           exist.

        Args:
            request (:class:`~.product_search_service.AddProductToProductSetRequest`):
                The request object. Request message for the
                `AddProductToProductSet` method.
            name (:class:`str`):
                Required. The resource name for the ProductSet to
                modify.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product (:class:`str`):
                Required. The resource name for the Product to be added
                to this ProductSet.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, product]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.AddProductToProductSetRequest(request)
        if name is not None:
            request.name = name
        if product is not None:
            request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.add_product_to_product_set,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def remove_product_from_product_set(
        self,
        request: product_search_service.RemoveProductFromProductSetRequest = None,
        *,
        name: str = None,
        product: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a Product from the specified ProductSet.

        Args:
            request (:class:`~.product_search_service.RemoveProductFromProductSetRequest`):
                The request object. Request message for the
                `RemoveProductFromProductSet` method.
            name (:class:`str`):
                Required. The resource name for the ProductSet to
                modify.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product (:class:`str`):
                Required. The resource name for the Product to be
                removed from this ProductSet.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, product]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.RemoveProductFromProductSetRequest(request)
        if name is not None:
            request.name = name
        if product is not None:
            request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.remove_product_from_product_set,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def list_products_in_product_set(
        self,
        request: product_search_service.ListProductsInProductSetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductsInProductSetPager:
        r"""Lists the Products in a ProductSet, in an unspecified order. If
        the ProductSet does not exist, the products field of the
        response will be empty.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100 or
           less than 1.

        Args:
            request (:class:`~.product_search_service.ListProductsInProductSetRequest`):
                The request object. Request message for the
                `ListProductsInProductSet` method.
            name (:class:`str`):
                Required. The ProductSet resource for which to retrieve
                Products.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListProductsInProductSetPager:
                Response message for the ``ListProductsInProductSet``
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.ListProductsInProductSetRequest(request)
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_products_in_product_set,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListProductsInProductSetPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def import_product_sets(
        self,
        request: product_search_service.ImportProductSetsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Asynchronous API that imports a list of reference images to
        specified product sets based on a list of image information.

        The [google.longrunning.Operation][google.longrunning.Operation]
        API can be used to keep track of the progress and results of the
        request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress) ``Operation.response``
        contains ``ImportProductSetsResponse``. (results)

        The input source of this method is a csv file on Google Cloud
        Storage. For the format of the csv file please see
        [ImportProductSetsGcsSource.csv_file_uri][google.cloud.vision.v1.ImportProductSetsGcsSource.csv_file_uri].

        Args:
            request (:class:`~.product_search_service.ImportProductSetsRequest`):
                The request object. Request message for the
                `ImportProductSets` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.product_search_service.ImportProductSetsResponse``:
                Response message for the ``ImportProductSets`` method.

                This message is returned by the
                [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
                method in the returned
                [google.longrunning.Operation.response][google.longrunning.Operation.response]
                field.

        """
        # Create or coerce a protobuf request object.
        request = product_search_service.ImportProductSetsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.import_product_sets,
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
            product_search_service.ImportProductSetsResponse,
            metadata_type=product_search_service.BatchOperationMetadata,
        )

        # Done; return the response.
        return response

    def purge_products(
        self,
        request: product_search_service.PurgeProductsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Asynchronous API to delete all Products in a ProductSet or all
        Products that are in no ProductSet.

        If a Product is a member of the specified ProductSet in addition
        to other ProductSets, the Product will still be deleted.

        It is recommended to not delete the specified ProductSet until
        after this operation has completed. It is also recommended to
        not add any of the Products involved in the batch delete to a
        new ProductSet while this operation is running because those
        Products may still end up deleted.

        It's not possible to undo the PurgeProducts operation.
        Therefore, it is recommended to keep the csv files used in
        ImportProductSets (if that was how you originally built the
        Product Set) before starting PurgeProducts, in case you need to
        re-import the data after deletion.

        If the plan is to purge all of the Products from a ProductSet
        and then re-use the empty ProductSet to re-import new Products
        into the empty ProductSet, you must wait until the PurgeProducts
        operation has finished for that ProductSet.

        The [google.longrunning.Operation][google.longrunning.Operation]
        API can be used to keep track of the progress and results of the
        request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress)

        Args:
            request (:class:`~.product_search_service.PurgeProductsRequest`):
                The request object. Request message for the
                `PurgeProducts` method.
            parent (:class:`str`):
                Required. The project and location in which the Products
                should be deleted.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Create or coerce a protobuf request object.
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        request = product_search_service.PurgeProductsRequest(request)
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.purge_products,
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
            empty.Empty,
            metadata_type=product_search_service.BatchOperationMetadata,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-vision").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("ProductSearch",)
