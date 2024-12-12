# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    Union,
)

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import retry_async as retries_async

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
    OptionalAsyncRetry = Union[
        retries_async.AsyncRetry, gapic_v1.method._MethodDefault, None
    ]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore
    OptionalAsyncRetry = Union[retries_async.AsyncRetry, object, None]  # type: ignore

from google.cloud.discoveryengine_v1beta.types import (
    conversation,
    conversational_search_service,
    session,
)


class ListConversationsPager:
    """A pager for iterating through ``list_conversations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1beta.types.ListConversationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``conversations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConversations`` requests and continue to iterate
    through the ``conversations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1beta.types.ListConversationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., conversational_search_service.ListConversationsResponse],
        request: conversational_search_service.ListConversationsRequest,
        response: conversational_search_service.ListConversationsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1beta.types.ListConversationsRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1beta.types.ListConversationsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = conversational_search_service.ListConversationsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[conversational_search_service.ListConversationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[conversation.Conversation]:
        for page in self.pages:
            yield from page.conversations

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConversationsAsyncPager:
    """A pager for iterating through ``list_conversations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1beta.types.ListConversationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``conversations`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConversations`` requests and continue to iterate
    through the ``conversations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1beta.types.ListConversationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[conversational_search_service.ListConversationsResponse]
        ],
        request: conversational_search_service.ListConversationsRequest,
        response: conversational_search_service.ListConversationsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1beta.types.ListConversationsRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1beta.types.ListConversationsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = conversational_search_service.ListConversationsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[conversational_search_service.ListConversationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __aiter__(self) -> AsyncIterator[conversation.Conversation]:
        async def async_generator():
            async for page in self.pages:
                for response in page.conversations:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSessionsPager:
    """A pager for iterating through ``list_sessions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1beta.types.ListSessionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``sessions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSessions`` requests and continue to iterate
    through the ``sessions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1beta.types.ListSessionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., conversational_search_service.ListSessionsResponse],
        request: conversational_search_service.ListSessionsRequest,
        response: conversational_search_service.ListSessionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1beta.types.ListSessionsRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1beta.types.ListSessionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = conversational_search_service.ListSessionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[conversational_search_service.ListSessionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[session.Session]:
        for page in self.pages:
            yield from page.sessions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSessionsAsyncPager:
    """A pager for iterating through ``list_sessions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1beta.types.ListSessionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``sessions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSessions`` requests and continue to iterate
    through the ``sessions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1beta.types.ListSessionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[conversational_search_service.ListSessionsResponse]
        ],
        request: conversational_search_service.ListSessionsRequest,
        response: conversational_search_service.ListSessionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1beta.types.ListSessionsRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1beta.types.ListSessionsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = conversational_search_service.ListSessionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[conversational_search_service.ListSessionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __aiter__(self) -> AsyncIterator[session.Session]:
        async def async_generator():
            async for page in self.pages:
                for response in page.sessions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
