# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.cloud.contact_center_insights_v1.types import (
    contact_center_insights,
    resources,
)


class ListConversationsPager:
    """A pager for iterating through ``list_conversations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListConversationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``conversations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConversations`` requests and continue to iterate
    through the ``conversations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListConversationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., contact_center_insights.ListConversationsResponse],
        request: contact_center_insights.ListConversationsRequest,
        response: contact_center_insights.ListConversationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListConversationsRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListConversationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListConversationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[contact_center_insights.ListConversationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Conversation]:
        for page in self.pages:
            yield from page.conversations

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConversationsAsyncPager:
    """A pager for iterating through ``list_conversations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListConversationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``conversations`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConversations`` requests and continue to iterate
    through the ``conversations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListConversationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[contact_center_insights.ListConversationsResponse]
        ],
        request: contact_center_insights.ListConversationsRequest,
        response: contact_center_insights.ListConversationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListConversationsRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListConversationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListConversationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[contact_center_insights.ListConversationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Conversation]:
        async def async_generator():
            async for page in self.pages:
                for response in page.conversations:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAnalysesPager:
    """A pager for iterating through ``list_analyses`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListAnalysesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``analyses`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAnalyses`` requests and continue to iterate
    through the ``analyses`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListAnalysesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., contact_center_insights.ListAnalysesResponse],
        request: contact_center_insights.ListAnalysesRequest,
        response: contact_center_insights.ListAnalysesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListAnalysesRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListAnalysesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListAnalysesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[contact_center_insights.ListAnalysesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Analysis]:
        for page in self.pages:
            yield from page.analyses

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAnalysesAsyncPager:
    """A pager for iterating through ``list_analyses`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListAnalysesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``analyses`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAnalyses`` requests and continue to iterate
    through the ``analyses`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListAnalysesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[contact_center_insights.ListAnalysesResponse]],
        request: contact_center_insights.ListAnalysesRequest,
        response: contact_center_insights.ListAnalysesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListAnalysesRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListAnalysesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListAnalysesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[contact_center_insights.ListAnalysesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Analysis]:
        async def async_generator():
            async for page in self.pages:
                for response in page.analyses:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPhraseMatchersPager:
    """A pager for iterating through ``list_phrase_matchers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``phrase_matchers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPhraseMatchers`` requests and continue to iterate
    through the ``phrase_matchers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., contact_center_insights.ListPhraseMatchersResponse],
        request: contact_center_insights.ListPhraseMatchersRequest,
        response: contact_center_insights.ListPhraseMatchersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListPhraseMatchersRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListPhraseMatchersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[contact_center_insights.ListPhraseMatchersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.PhraseMatcher]:
        for page in self.pages:
            yield from page.phrase_matchers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPhraseMatchersAsyncPager:
    """A pager for iterating through ``list_phrase_matchers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``phrase_matchers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPhraseMatchers`` requests and continue to iterate
    through the ``phrase_matchers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[contact_center_insights.ListPhraseMatchersResponse]
        ],
        request: contact_center_insights.ListPhraseMatchersRequest,
        response: contact_center_insights.ListPhraseMatchersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListPhraseMatchersRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListPhraseMatchersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListPhraseMatchersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[contact_center_insights.ListPhraseMatchersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.PhraseMatcher]:
        async def async_generator():
            async for page in self.pages:
                for response in page.phrase_matchers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListViewsPager:
    """A pager for iterating through ``list_views`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListViewsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``views`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListViews`` requests and continue to iterate
    through the ``views`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListViewsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., contact_center_insights.ListViewsResponse],
        request: contact_center_insights.ListViewsRequest,
        response: contact_center_insights.ListViewsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListViewsRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListViewsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListViewsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[contact_center_insights.ListViewsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.View]:
        for page in self.pages:
            yield from page.views

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListViewsAsyncPager:
    """A pager for iterating through ``list_views`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.contact_center_insights_v1.types.ListViewsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``views`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListViews`` requests and continue to iterate
    through the ``views`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.contact_center_insights_v1.types.ListViewsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[contact_center_insights.ListViewsResponse]],
        request: contact_center_insights.ListViewsRequest,
        response: contact_center_insights.ListViewsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.contact_center_insights_v1.types.ListViewsRequest):
                The initial request object.
            response (google.cloud.contact_center_insights_v1.types.ListViewsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = contact_center_insights.ListViewsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[contact_center_insights.ListViewsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.View]:
        async def async_generator():
            async for page in self.pages:
                for response in page.views:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
