# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterable

from google.cloud.vision_v1.types import product_search_service


class ListProductSetsPager:
    """A pager for iterating through ``list_product_sets`` requests.

    This class thinly wraps an initial
    :class:`~.product_search_service.ListProductSetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``product_sets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProductSets`` requests and continue to iterate
    through the ``product_sets`` field on the
    corresponding responses.

    All the usual :class:`~.product_search_service.ListProductSetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [product_search_service.ListProductSetsRequest],
            product_search_service.ListProductSetsResponse,
        ],
        request: product_search_service.ListProductSetsRequest,
        response: product_search_service.ListProductSetsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.product_search_service.ListProductSetsRequest`):
                The initial request object.
            response (:class:`~.product_search_service.ListProductSetsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = product_search_service.ListProductSetsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def __iter__(self) -> Iterable[product_search_service.ProductSet]:
        while True:
            # Iterate through the results on this response.
            for result in self._response.product_sets:
                yield result

            # Sanity check: Is this the last page? If so, we are done.
            if not self._response.next_page_token:
                break

            # Get the next page.
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsPager:
    """A pager for iterating through ``list_products`` requests.

    This class thinly wraps an initial
    :class:`~.product_search_service.ListProductsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`~.product_search_service.ListProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [product_search_service.ListProductsRequest],
            product_search_service.ListProductsResponse,
        ],
        request: product_search_service.ListProductsRequest,
        response: product_search_service.ListProductsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.product_search_service.ListProductsRequest`):
                The initial request object.
            response (:class:`~.product_search_service.ListProductsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = product_search_service.ListProductsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def __iter__(self) -> Iterable[product_search_service.Product]:
        while True:
            # Iterate through the results on this response.
            for result in self._response.products:
                yield result

            # Sanity check: Is this the last page? If so, we are done.
            if not self._response.next_page_token:
                break

            # Get the next page.
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReferenceImagesPager:
    """A pager for iterating through ``list_reference_images`` requests.

    This class thinly wraps an initial
    :class:`~.product_search_service.ListReferenceImagesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``reference_images`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListReferenceImages`` requests and continue to iterate
    through the ``reference_images`` field on the
    corresponding responses.

    All the usual :class:`~.product_search_service.ListReferenceImagesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [product_search_service.ListReferenceImagesRequest],
            product_search_service.ListReferenceImagesResponse,
        ],
        request: product_search_service.ListReferenceImagesRequest,
        response: product_search_service.ListReferenceImagesResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.product_search_service.ListReferenceImagesRequest`):
                The initial request object.
            response (:class:`~.product_search_service.ListReferenceImagesResponse`):
                The initial response object.
        """
        self._method = method
        self._request = product_search_service.ListReferenceImagesRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def __iter__(self) -> Iterable[product_search_service.ReferenceImage]:
        while True:
            # Iterate through the results on this response.
            for result in self._response.reference_images:
                yield result

            # Sanity check: Is this the last page? If so, we are done.
            if not self._response.next_page_token:
                break

            # Get the next page.
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsInProductSetPager:
    """A pager for iterating through ``list_products_in_product_set`` requests.

    This class thinly wraps an initial
    :class:`~.product_search_service.ListProductsInProductSetResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProductsInProductSet`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`~.product_search_service.ListProductsInProductSetResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [product_search_service.ListProductsInProductSetRequest],
            product_search_service.ListProductsInProductSetResponse,
        ],
        request: product_search_service.ListProductsInProductSetRequest,
        response: product_search_service.ListProductsInProductSetResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.product_search_service.ListProductsInProductSetRequest`):
                The initial request object.
            response (:class:`~.product_search_service.ListProductsInProductSetResponse`):
                The initial response object.
        """
        self._method = method
        self._request = product_search_service.ListProductsInProductSetRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def __iter__(self) -> Iterable[product_search_service.Product]:
        while True:
            # Iterate through the results on this response.
            for result in self._response.products:
                yield result

            # Sanity check: Is this the last page? If so, we are done.
            if not self._response.next_page_token:
                break

            # Get the next page.
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
