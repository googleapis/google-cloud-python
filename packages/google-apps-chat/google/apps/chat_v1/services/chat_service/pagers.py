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

from google.apps.chat_v1.types import membership, message, reaction, space, space_event


class ListMessagesPager:
    """A pager for iterating through ``list_messages`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListMessagesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``messages`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMessages`` requests and continue to iterate
    through the ``messages`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListMessagesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., message.ListMessagesResponse],
        request: message.ListMessagesRequest,
        response: message.ListMessagesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListMessagesRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListMessagesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = message.ListMessagesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[message.ListMessagesResponse]:
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

    def __iter__(self) -> Iterator[message.Message]:
        for page in self.pages:
            yield from page.messages

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMessagesAsyncPager:
    """A pager for iterating through ``list_messages`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListMessagesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``messages`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMessages`` requests and continue to iterate
    through the ``messages`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListMessagesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[message.ListMessagesResponse]],
        request: message.ListMessagesRequest,
        response: message.ListMessagesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListMessagesRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListMessagesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = message.ListMessagesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[message.ListMessagesResponse]:
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

    def __aiter__(self) -> AsyncIterator[message.Message]:
        async def async_generator():
            async for page in self.pages:
                for response in page.messages:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMembershipsPager:
    """A pager for iterating through ``list_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListMembershipsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``memberships`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMemberships`` requests and continue to iterate
    through the ``memberships`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., membership.ListMembershipsResponse],
        request: membership.ListMembershipsRequest,
        response: membership.ListMembershipsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListMembershipsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListMembershipsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = membership.ListMembershipsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[membership.ListMembershipsResponse]:
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

    def __iter__(self) -> Iterator[membership.Membership]:
        for page in self.pages:
            yield from page.memberships

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMembershipsAsyncPager:
    """A pager for iterating through ``list_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListMembershipsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``memberships`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMemberships`` requests and continue to iterate
    through the ``memberships`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[membership.ListMembershipsResponse]],
        request: membership.ListMembershipsRequest,
        response: membership.ListMembershipsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListMembershipsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListMembershipsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = membership.ListMembershipsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[membership.ListMembershipsResponse]:
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

    def __aiter__(self) -> AsyncIterator[membership.Membership]:
        async def async_generator():
            async for page in self.pages:
                for response in page.memberships:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSpacesPager:
    """A pager for iterating through ``list_spaces`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListSpacesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``spaces`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSpaces`` requests and continue to iterate
    through the ``spaces`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListSpacesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., space.ListSpacesResponse],
        request: space.ListSpacesRequest,
        response: space.ListSpacesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListSpacesRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListSpacesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = space.ListSpacesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[space.ListSpacesResponse]:
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

    def __iter__(self) -> Iterator[space.Space]:
        for page in self.pages:
            yield from page.spaces

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSpacesAsyncPager:
    """A pager for iterating through ``list_spaces`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListSpacesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``spaces`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSpaces`` requests and continue to iterate
    through the ``spaces`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListSpacesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[space.ListSpacesResponse]],
        request: space.ListSpacesRequest,
        response: space.ListSpacesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListSpacesRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListSpacesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = space.ListSpacesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[space.ListSpacesResponse]:
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

    def __aiter__(self) -> AsyncIterator[space.Space]:
        async def async_generator():
            async for page in self.pages:
                for response in page.spaces:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReactionsPager:
    """A pager for iterating through ``list_reactions`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListReactionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``reactions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListReactions`` requests and continue to iterate
    through the ``reactions`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListReactionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., reaction.ListReactionsResponse],
        request: reaction.ListReactionsRequest,
        response: reaction.ListReactionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListReactionsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListReactionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = reaction.ListReactionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[reaction.ListReactionsResponse]:
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

    def __iter__(self) -> Iterator[reaction.Reaction]:
        for page in self.pages:
            yield from page.reactions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReactionsAsyncPager:
    """A pager for iterating through ``list_reactions`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListReactionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``reactions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListReactions`` requests and continue to iterate
    through the ``reactions`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListReactionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[reaction.ListReactionsResponse]],
        request: reaction.ListReactionsRequest,
        response: reaction.ListReactionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListReactionsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListReactionsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = reaction.ListReactionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[reaction.ListReactionsResponse]:
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

    def __aiter__(self) -> AsyncIterator[reaction.Reaction]:
        async def async_generator():
            async for page in self.pages:
                for response in page.reactions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSpaceEventsPager:
    """A pager for iterating through ``list_space_events`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListSpaceEventsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``space_events`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSpaceEvents`` requests and continue to iterate
    through the ``space_events`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListSpaceEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., space_event.ListSpaceEventsResponse],
        request: space_event.ListSpaceEventsRequest,
        response: space_event.ListSpaceEventsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListSpaceEventsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListSpaceEventsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = space_event.ListSpaceEventsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[space_event.ListSpaceEventsResponse]:
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

    def __iter__(self) -> Iterator[space_event.SpaceEvent]:
        for page in self.pages:
            yield from page.space_events

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSpaceEventsAsyncPager:
    """A pager for iterating through ``list_space_events`` requests.

    This class thinly wraps an initial
    :class:`google.apps.chat_v1.types.ListSpaceEventsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``space_events`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSpaceEvents`` requests and continue to iterate
    through the ``space_events`` field on the
    corresponding responses.

    All the usual :class:`google.apps.chat_v1.types.ListSpaceEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[space_event.ListSpaceEventsResponse]],
        request: space_event.ListSpaceEventsRequest,
        response: space_event.ListSpaceEventsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.chat_v1.types.ListSpaceEventsRequest):
                The initial request object.
            response (google.apps.chat_v1.types.ListSpaceEventsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = space_event.ListSpaceEventsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[space_event.ListSpaceEventsResponse]:
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

    def __aiter__(self) -> AsyncIterator[space_event.SpaceEvent]:
        async def async_generator():
            async for page in self.pages:
                for response in page.space_events:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
