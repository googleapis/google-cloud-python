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
from typing import Any, AsyncIterator, Awaitable, Callable, Sequence, Tuple, Optional, Iterator

from google.cloud.eventarc_v1.types import channel
from google.cloud.eventarc_v1.types import channel_connection
from google.cloud.eventarc_v1.types import discovery
from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import trigger


class ListTriggersPager:
    """A pager for iterating through ``list_triggers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListTriggersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``triggers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTriggers`` requests and continue to iterate
    through the ``triggers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListTriggersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., eventarc.ListTriggersResponse],
            request: eventarc.ListTriggersRequest,
            response: eventarc.ListTriggersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListTriggersRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListTriggersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListTriggersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[eventarc.ListTriggersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[trigger.Trigger]:
        for page in self.pages:
            yield from page.triggers

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListTriggersAsyncPager:
    """A pager for iterating through ``list_triggers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListTriggersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``triggers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTriggers`` requests and continue to iterate
    through the ``triggers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListTriggersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[eventarc.ListTriggersResponse]],
            request: eventarc.ListTriggersRequest,
            response: eventarc.ListTriggersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListTriggersRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListTriggersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListTriggersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[eventarc.ListTriggersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[trigger.Trigger]:
        async def async_generator():
            async for page in self.pages:
                for response in page.triggers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListChannelsPager:
    """A pager for iterating through ``list_channels`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListChannelsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``channels`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListChannels`` requests and continue to iterate
    through the ``channels`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListChannelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., eventarc.ListChannelsResponse],
            request: eventarc.ListChannelsRequest,
            response: eventarc.ListChannelsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListChannelsRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListChannelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListChannelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[eventarc.ListChannelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[channel.Channel]:
        for page in self.pages:
            yield from page.channels

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListChannelsAsyncPager:
    """A pager for iterating through ``list_channels`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListChannelsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``channels`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListChannels`` requests and continue to iterate
    through the ``channels`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListChannelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[eventarc.ListChannelsResponse]],
            request: eventarc.ListChannelsRequest,
            response: eventarc.ListChannelsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListChannelsRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListChannelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListChannelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[eventarc.ListChannelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[channel.Channel]:
        async def async_generator():
            async for page in self.pages:
                for response in page.channels:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListProvidersPager:
    """A pager for iterating through ``list_providers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListProvidersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``providers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProviders`` requests and continue to iterate
    through the ``providers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListProvidersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., eventarc.ListProvidersResponse],
            request: eventarc.ListProvidersRequest,
            response: eventarc.ListProvidersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListProvidersRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListProvidersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListProvidersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[eventarc.ListProvidersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[discovery.Provider]:
        for page in self.pages:
            yield from page.providers

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListProvidersAsyncPager:
    """A pager for iterating through ``list_providers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListProvidersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``providers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProviders`` requests and continue to iterate
    through the ``providers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListProvidersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[eventarc.ListProvidersResponse]],
            request: eventarc.ListProvidersRequest,
            response: eventarc.ListProvidersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListProvidersRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListProvidersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListProvidersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[eventarc.ListProvidersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[discovery.Provider]:
        async def async_generator():
            async for page in self.pages:
                for response in page.providers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListChannelConnectionsPager:
    """A pager for iterating through ``list_channel_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListChannelConnectionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``channel_connections`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListChannelConnections`` requests and continue to iterate
    through the ``channel_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListChannelConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., eventarc.ListChannelConnectionsResponse],
            request: eventarc.ListChannelConnectionsRequest,
            response: eventarc.ListChannelConnectionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListChannelConnectionsRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListChannelConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListChannelConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[eventarc.ListChannelConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[channel_connection.ChannelConnection]:
        for page in self.pages:
            yield from page.channel_connections

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListChannelConnectionsAsyncPager:
    """A pager for iterating through ``list_channel_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.eventarc_v1.types.ListChannelConnectionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``channel_connections`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListChannelConnections`` requests and continue to iterate
    through the ``channel_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.eventarc_v1.types.ListChannelConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[eventarc.ListChannelConnectionsResponse]],
            request: eventarc.ListChannelConnectionsRequest,
            response: eventarc.ListChannelConnectionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.eventarc_v1.types.ListChannelConnectionsRequest):
                The initial request object.
            response (google.cloud.eventarc_v1.types.ListChannelConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = eventarc.ListChannelConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[eventarc.ListChannelConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[channel_connection.ChannelConnection]:
        async def async_generator():
            async for page in self.pages:
                for response in page.channel_connections:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
