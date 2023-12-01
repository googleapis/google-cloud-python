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

from google.analytics.data_v1alpha.types import analytics_data_api


class ListAudienceListsPager:
    """A pager for iterating through ``list_audience_lists`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.data_v1alpha.types.ListAudienceListsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``audience_lists`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAudienceLists`` requests and continue to iterate
    through the ``audience_lists`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.data_v1alpha.types.ListAudienceListsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_data_api.ListAudienceListsResponse],
        request: analytics_data_api.ListAudienceListsRequest,
        response: analytics_data_api.ListAudienceListsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.data_v1alpha.types.ListAudienceListsRequest):
                The initial request object.
            response (google.analytics.data_v1alpha.types.ListAudienceListsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_data_api.ListAudienceListsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analytics_data_api.ListAudienceListsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[analytics_data_api.AudienceList]:
        for page in self.pages:
            yield from page.audience_lists

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAudienceListsAsyncPager:
    """A pager for iterating through ``list_audience_lists`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.data_v1alpha.types.ListAudienceListsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``audience_lists`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAudienceLists`` requests and continue to iterate
    through the ``audience_lists`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.data_v1alpha.types.ListAudienceListsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_data_api.ListAudienceListsResponse]],
        request: analytics_data_api.ListAudienceListsRequest,
        response: analytics_data_api.ListAudienceListsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.data_v1alpha.types.ListAudienceListsRequest):
                The initial request object.
            response (google.analytics.data_v1alpha.types.ListAudienceListsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_data_api.ListAudienceListsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[analytics_data_api.ListAudienceListsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[analytics_data_api.AudienceList]:
        async def async_generator():
            async for page in self.pages:
                for response in page.audience_lists:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRecurringAudienceListsPager:
    """A pager for iterating through ``list_recurring_audience_lists`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``recurring_audience_lists`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRecurringAudienceLists`` requests and continue to iterate
    through the ``recurring_audience_lists`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_data_api.ListRecurringAudienceListsResponse],
        request: analytics_data_api.ListRecurringAudienceListsRequest,
        response: analytics_data_api.ListRecurringAudienceListsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.data_v1alpha.types.ListRecurringAudienceListsRequest):
                The initial request object.
            response (google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_data_api.ListRecurringAudienceListsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analytics_data_api.ListRecurringAudienceListsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[analytics_data_api.RecurringAudienceList]:
        for page in self.pages:
            yield from page.recurring_audience_lists

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRecurringAudienceListsAsyncPager:
    """A pager for iterating through ``list_recurring_audience_lists`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``recurring_audience_lists`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRecurringAudienceLists`` requests and continue to iterate
    through the ``recurring_audience_lists`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[analytics_data_api.ListRecurringAudienceListsResponse]
        ],
        request: analytics_data_api.ListRecurringAudienceListsRequest,
        response: analytics_data_api.ListRecurringAudienceListsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.data_v1alpha.types.ListRecurringAudienceListsRequest):
                The initial request object.
            response (google.analytics.data_v1alpha.types.ListRecurringAudienceListsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_data_api.ListRecurringAudienceListsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[analytics_data_api.ListRecurringAudienceListsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[analytics_data_api.RecurringAudienceList]:
        async def async_generator():
            async for page in self.pages:
                for response in page.recurring_audience_lists:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
