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

from google.cloud.errorreporting_v1beta1.types import common
from google.cloud.errorreporting_v1beta1.types import error_stats_service


class ListGroupStatsPager:
    """A pager for iterating through ``list_group_stats`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``error_group_stats`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGroupStats`` requests and continue to iterate
    through the ``error_group_stats`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., error_stats_service.ListGroupStatsResponse],
        request: error_stats_service.ListGroupStatsRequest,
        response: error_stats_service.ListGroupStatsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.errorreporting_v1beta1.types.ListGroupStatsRequest):
                The initial request object.
            response (google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = error_stats_service.ListGroupStatsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[error_stats_service.ListGroupStatsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[error_stats_service.ErrorGroupStats]:
        for page in self.pages:
            yield from page.error_group_stats

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGroupStatsAsyncPager:
    """A pager for iterating through ``list_group_stats`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``error_group_stats`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListGroupStats`` requests and continue to iterate
    through the ``error_group_stats`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[error_stats_service.ListGroupStatsResponse]],
        request: error_stats_service.ListGroupStatsRequest,
        response: error_stats_service.ListGroupStatsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.errorreporting_v1beta1.types.ListGroupStatsRequest):
                The initial request object.
            response (google.cloud.errorreporting_v1beta1.types.ListGroupStatsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = error_stats_service.ListGroupStatsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[error_stats_service.ListGroupStatsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[error_stats_service.ErrorGroupStats]:
        async def async_generator():
            async for page in self.pages:
                for response in page.error_group_stats:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEventsPager:
    """A pager for iterating through ``list_events`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.errorreporting_v1beta1.types.ListEventsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``error_events`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEvents`` requests and continue to iterate
    through the ``error_events`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.errorreporting_v1beta1.types.ListEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., error_stats_service.ListEventsResponse],
        request: error_stats_service.ListEventsRequest,
        response: error_stats_service.ListEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.errorreporting_v1beta1.types.ListEventsRequest):
                The initial request object.
            response (google.cloud.errorreporting_v1beta1.types.ListEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = error_stats_service.ListEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[error_stats_service.ListEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[common.ErrorEvent]:
        for page in self.pages:
            yield from page.error_events

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEventsAsyncPager:
    """A pager for iterating through ``list_events`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.errorreporting_v1beta1.types.ListEventsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``error_events`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEvents`` requests and continue to iterate
    through the ``error_events`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.errorreporting_v1beta1.types.ListEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[error_stats_service.ListEventsResponse]],
        request: error_stats_service.ListEventsRequest,
        response: error_stats_service.ListEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.errorreporting_v1beta1.types.ListEventsRequest):
                The initial request object.
            response (google.cloud.errorreporting_v1beta1.types.ListEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = error_stats_service.ListEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[error_stats_service.ListEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[common.ErrorEvent]:
        async def async_generator():
            async for page in self.pages:
                for response in page.error_events:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
