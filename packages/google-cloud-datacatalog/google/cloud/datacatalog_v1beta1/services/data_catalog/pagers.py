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
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    Sequence,
    Tuple,
    Optional,
)

from google.cloud.datacatalog_v1beta1.types import datacatalog
from google.cloud.datacatalog_v1beta1.types import search
from google.cloud.datacatalog_v1beta1.types import tags


class SearchCatalogPager:
    """A pager for iterating through ``search_catalog`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchCatalog`` requests and continue to iterate
    through the ``results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datacatalog.SearchCatalogResponse],
        request: datacatalog.SearchCatalogRequest,
        response: datacatalog.SearchCatalogResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.SearchCatalogRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.SearchCatalogRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datacatalog.SearchCatalogResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[search.SearchCatalogResult]:
        for page in self.pages:
            yield from page.results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchCatalogAsyncPager:
    """A pager for iterating through ``search_catalog`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchCatalog`` requests and continue to iterate
    through the ``results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datacatalog.SearchCatalogResponse]],
        request: datacatalog.SearchCatalogRequest,
        response: datacatalog.SearchCatalogResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.SearchCatalogRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.SearchCatalogResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.SearchCatalogRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datacatalog.SearchCatalogResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[search.SearchCatalogResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntryGroupsPager:
    """A pager for iterating through ``list_entry_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``entry_groups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEntryGroups`` requests and continue to iterate
    through the ``entry_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datacatalog.ListEntryGroupsResponse],
        request: datacatalog.ListEntryGroupsRequest,
        response: datacatalog.ListEntryGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListEntryGroupsRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListEntryGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datacatalog.ListEntryGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[datacatalog.EntryGroup]:
        for page in self.pages:
            yield from page.entry_groups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntryGroupsAsyncPager:
    """A pager for iterating through ``list_entry_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``entry_groups`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEntryGroups`` requests and continue to iterate
    through the ``entry_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datacatalog.ListEntryGroupsResponse]],
        request: datacatalog.ListEntryGroupsRequest,
        response: datacatalog.ListEntryGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListEntryGroupsRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListEntryGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datacatalog.ListEntryGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[datacatalog.EntryGroup]:
        async def async_generator():
            async for page in self.pages:
                for response in page.entry_groups:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntriesPager:
    """A pager for iterating through ``list_entries`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListEntriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEntries`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datacatalog.ListEntriesResponse],
        request: datacatalog.ListEntriesRequest,
        response: datacatalog.ListEntriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListEntriesRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListEntriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListEntriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datacatalog.ListEntriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[datacatalog.Entry]:
        for page in self.pages:
            yield from page.entries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntriesAsyncPager:
    """A pager for iterating through ``list_entries`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListEntriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEntries`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datacatalog.ListEntriesResponse]],
        request: datacatalog.ListEntriesRequest,
        response: datacatalog.ListEntriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListEntriesRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListEntriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListEntriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datacatalog.ListEntriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[datacatalog.Entry]:
        async def async_generator():
            async for page in self.pages:
                for response in page.entries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTagsPager:
    """A pager for iterating through ``list_tags`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListTagsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``tags`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTags`` requests and continue to iterate
    through the ``tags`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListTagsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datacatalog.ListTagsResponse],
        request: datacatalog.ListTagsRequest,
        response: datacatalog.ListTagsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListTagsRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListTagsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListTagsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datacatalog.ListTagsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[tags.Tag]:
        for page in self.pages:
            yield from page.tags

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTagsAsyncPager:
    """A pager for iterating through ``list_tags`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.datacatalog_v1beta1.types.ListTagsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``tags`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTags`` requests and continue to iterate
    through the ``tags`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.datacatalog_v1beta1.types.ListTagsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datacatalog.ListTagsResponse]],
        request: datacatalog.ListTagsRequest,
        response: datacatalog.ListTagsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.datacatalog_v1beta1.types.ListTagsRequest):
                The initial request object.
            response (google.cloud.datacatalog_v1beta1.types.ListTagsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datacatalog.ListTagsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datacatalog.ListTagsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[tags.Tag]:
        async def async_generator():
            async for page in self.pages:
                for response in page.tags:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
