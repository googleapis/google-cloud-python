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

from google.cloud.privatecatalog_v1beta1.types import private_catalog


class SearchCatalogsPager:
    """A pager for iterating through ``search_catalogs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``catalogs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchCatalogs`` requests and continue to iterate
    through the ``catalogs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., private_catalog.SearchCatalogsResponse],
        request: private_catalog.SearchCatalogsRequest,
        response: private_catalog.SearchCatalogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchCatalogsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchCatalogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[private_catalog.SearchCatalogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[private_catalog.Catalog]:
        for page in self.pages:
            yield from page.catalogs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchCatalogsAsyncPager:
    """A pager for iterating through ``search_catalogs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``catalogs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchCatalogs`` requests and continue to iterate
    through the ``catalogs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[private_catalog.SearchCatalogsResponse]],
        request: private_catalog.SearchCatalogsRequest,
        response: private_catalog.SearchCatalogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchCatalogsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchCatalogsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchCatalogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[private_catalog.SearchCatalogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[private_catalog.Catalog]:
        async def async_generator():
            async for page in self.pages:
                for response in page.catalogs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchProductsPager:
    """A pager for iterating through ``search_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., private_catalog.SearchProductsResponse],
        request: private_catalog.SearchProductsRequest,
        response: private_catalog.SearchProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchProductsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[private_catalog.SearchProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[private_catalog.Product]:
        for page in self.pages:
            yield from page.products

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchProductsAsyncPager:
    """A pager for iterating through ``search_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[private_catalog.SearchProductsResponse]],
        request: private_catalog.SearchProductsRequest,
        response: private_catalog.SearchProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchProductsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[private_catalog.SearchProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[private_catalog.Product]:
        async def async_generator():
            async for page in self.pages:
                for response in page.products:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchVersionsPager:
    """A pager for iterating through ``search_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchVersions`` requests and continue to iterate
    through the ``versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., private_catalog.SearchVersionsResponse],
        request: private_catalog.SearchVersionsRequest,
        response: private_catalog.SearchVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchVersionsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[private_catalog.SearchVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[private_catalog.Version]:
        for page in self.pages:
            yield from page.versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchVersionsAsyncPager:
    """A pager for iterating through ``search_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``versions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchVersions`` requests and continue to iterate
    through the ``versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[private_catalog.SearchVersionsResponse]],
        request: private_catalog.SearchVersionsRequest,
        response: private_catalog.SearchVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.privatecatalog_v1beta1.types.SearchVersionsRequest):
                The initial request object.
            response (google.cloud.privatecatalog_v1beta1.types.SearchVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = private_catalog.SearchVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[private_catalog.SearchVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[private_catalog.Version]:
        async def async_generator():
            async for page in self.pages:
                for response in page.versions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
