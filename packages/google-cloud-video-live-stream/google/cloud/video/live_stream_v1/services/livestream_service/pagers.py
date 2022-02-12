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
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.cloud.video.live_stream_v1.types import resources
from google.cloud.video.live_stream_v1.types import service


class ListChannelsPager:
    """A pager for iterating through ``list_channels`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListChannelsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``channels`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListChannels`` requests and continue to iterate
    through the ``channels`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListChannelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListChannelsResponse],
        request: service.ListChannelsRequest,
        response: service.ListChannelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListChannelsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListChannelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListChannelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListChannelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Channel]:
        for page in self.pages:
            yield from page.channels

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListChannelsAsyncPager:
    """A pager for iterating through ``list_channels`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListChannelsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``channels`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListChannels`` requests and continue to iterate
    through the ``channels`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListChannelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListChannelsResponse]],
        request: service.ListChannelsRequest,
        response: service.ListChannelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListChannelsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListChannelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListChannelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListChannelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Channel]:
        async def async_generator():
            async for page in self.pages:
                for response in page.channels:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInputsPager:
    """A pager for iterating through ``list_inputs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListInputsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``inputs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListInputs`` requests and continue to iterate
    through the ``inputs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListInputsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListInputsResponse],
        request: service.ListInputsRequest,
        response: service.ListInputsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListInputsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListInputsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListInputsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListInputsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Input]:
        for page in self.pages:
            yield from page.inputs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInputsAsyncPager:
    """A pager for iterating through ``list_inputs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListInputsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``inputs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListInputs`` requests and continue to iterate
    through the ``inputs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListInputsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListInputsResponse]],
        request: service.ListInputsRequest,
        response: service.ListInputsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListInputsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListInputsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListInputsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListInputsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Input]:
        async def async_generator():
            async for page in self.pages:
                for response in page.inputs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEventsPager:
    """A pager for iterating through ``list_events`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListEventsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``events`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEvents`` requests and continue to iterate
    through the ``events`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListEventsResponse],
        request: service.ListEventsRequest,
        response: service.ListEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListEventsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Event]:
        for page in self.pages:
            yield from page.events

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEventsAsyncPager:
    """A pager for iterating through ``list_events`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.live_stream_v1.types.ListEventsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``events`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEvents`` requests and continue to iterate
    through the ``events`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.live_stream_v1.types.ListEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListEventsResponse]],
        request: service.ListEventsRequest,
        response: service.ListEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.live_stream_v1.types.ListEventsRequest):
                The initial request object.
            response (google.cloud.video.live_stream_v1.types.ListEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Event]:
        async def async_generator():
            async for page in self.pages:
                for response in page.events:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
