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
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.vision_v1p4beta1.types import product_search_service


class ListProductSetsPager:
    """A pager for iterating through ``list_product_sets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductSetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``product_sets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProductSets`` requests and continue to iterate
    through the ``product_sets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductSetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., product_search_service.ListProductSetsResponse],
        request: product_search_service.ListProductSetsRequest,
        response: product_search_service.ListProductSetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductSetsRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductSetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductSetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[product_search_service.ListProductSetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[product_search_service.ProductSet]:
        for page in self.pages:
            yield from page.product_sets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductSetsAsyncPager:
    """A pager for iterating through ``list_product_sets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductSetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``product_sets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProductSets`` requests and continue to iterate
    through the ``product_sets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductSetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[product_search_service.ListProductSetsResponse]
        ],
        request: product_search_service.ListProductSetsRequest,
        response: product_search_service.ListProductSetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductSetsRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductSetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductSetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[product_search_service.ListProductSetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[product_search_service.ProductSet]:
        async def async_generator():
            async for page in self.pages:
                for response in page.product_sets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsPager:
    """A pager for iterating through ``list_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., product_search_service.ListProductsResponse],
        request: product_search_service.ListProductsRequest,
        response: product_search_service.ListProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductsRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[product_search_service.ListProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[product_search_service.Product]:
        for page in self.pages:
            yield from page.products

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsAsyncPager:
    """A pager for iterating through ``list_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[product_search_service.ListProductsResponse]],
        request: product_search_service.ListProductsRequest,
        response: product_search_service.ListProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductsRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[product_search_service.ListProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[product_search_service.Product]:
        async def async_generator():
            async for page in self.pages:
                for response in page.products:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReferenceImagesPager:
    """A pager for iterating through ``list_reference_images`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``reference_images`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListReferenceImages`` requests and continue to iterate
    through the ``reference_images`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., product_search_service.ListReferenceImagesResponse],
        request: product_search_service.ListReferenceImagesRequest,
        response: product_search_service.ListReferenceImagesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListReferenceImagesRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListReferenceImagesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[product_search_service.ListReferenceImagesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[product_search_service.ReferenceImage]:
        for page in self.pages:
            yield from page.reference_images

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReferenceImagesAsyncPager:
    """A pager for iterating through ``list_reference_images`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``reference_images`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListReferenceImages`` requests and continue to iterate
    through the ``reference_images`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[product_search_service.ListReferenceImagesResponse]
        ],
        request: product_search_service.ListReferenceImagesRequest,
        response: product_search_service.ListReferenceImagesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListReferenceImagesRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListReferenceImagesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListReferenceImagesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[product_search_service.ListReferenceImagesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[product_search_service.ReferenceImage]:
        async def async_generator():
            async for page in self.pages:
                for response in page.reference_images:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsInProductSetPager:
    """A pager for iterating through ``list_products_in_product_set`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProductsInProductSet`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., product_search_service.ListProductsInProductSetResponse],
        request: product_search_service.ListProductsInProductSetRequest,
        response: product_search_service.ListProductsInProductSetResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductsInProductSetRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductsInProductSetRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[product_search_service.ListProductsInProductSetResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[product_search_service.Product]:
        for page in self.pages:
            yield from page.products

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsInProductSetAsyncPager:
    """A pager for iterating through ``list_products_in_product_set`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProductsInProductSet`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[product_search_service.ListProductsInProductSetResponse]
        ],
        request: product_search_service.ListProductsInProductSetRequest,
        response: product_search_service.ListProductsInProductSetResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vision_v1p4beta1.types.ListProductsInProductSetRequest):
                The initial request object.
            response (google.cloud.vision_v1p4beta1.types.ListProductsInProductSetResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = product_search_service.ListProductsInProductSetRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[product_search_service.ListProductsInProductSetResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[product_search_service.Product]:
        async def async_generator():
            async for page in self.pages:
                for response in page.products:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
