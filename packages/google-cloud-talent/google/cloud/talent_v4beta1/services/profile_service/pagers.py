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

from google.cloud.talent_v4beta1.types import histogram
from google.cloud.talent_v4beta1.types import profile
from google.cloud.talent_v4beta1.types import profile_service


class ListProfilesPager:
    """A pager for iterating through ``list_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.ListProfilesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``profiles`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProfiles`` requests and continue to iterate
    through the ``profiles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.ListProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., profile_service.ListProfilesResponse],
        request: profile_service.ListProfilesRequest,
        response: profile_service.ListProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.ListProfilesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.ListProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = profile_service.ListProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[profile_service.ListProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[profile.Profile]:
        for page in self.pages:
            yield from page.profiles

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProfilesAsyncPager:
    """A pager for iterating through ``list_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.ListProfilesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``profiles`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProfiles`` requests and continue to iterate
    through the ``profiles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.ListProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[profile_service.ListProfilesResponse]],
        request: profile_service.ListProfilesRequest,
        response: profile_service.ListProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.ListProfilesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.ListProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = profile_service.ListProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[profile_service.ListProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[profile.Profile]:
        async def async_generator():
            async for page in self.pages:
                for response in page.profiles:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchProfilesPager:
    """A pager for iterating through ``search_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.SearchProfilesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``histogram_query_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchProfiles`` requests and continue to iterate
    through the ``histogram_query_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.SearchProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., profile_service.SearchProfilesResponse],
        request: profile_service.SearchProfilesRequest,
        response: profile_service.SearchProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.SearchProfilesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.SearchProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = profile_service.SearchProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[profile_service.SearchProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[histogram.HistogramQueryResult]:
        for page in self.pages:
            yield from page.histogram_query_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchProfilesAsyncPager:
    """A pager for iterating through ``search_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.SearchProfilesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``histogram_query_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchProfiles`` requests and continue to iterate
    through the ``histogram_query_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.SearchProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[profile_service.SearchProfilesResponse]],
        request: profile_service.SearchProfilesRequest,
        response: profile_service.SearchProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.SearchProfilesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.SearchProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = profile_service.SearchProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[profile_service.SearchProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[histogram.HistogramQueryResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.histogram_query_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
