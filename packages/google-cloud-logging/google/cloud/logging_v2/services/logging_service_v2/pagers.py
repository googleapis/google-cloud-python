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

from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, Sequence, Tuple

from google.api import monitored_resource_pb2 as monitored_resource  # type: ignore
from google.cloud.logging_v2.types import log_entry
from google.cloud.logging_v2.types import logging


class ListLogEntriesPager:
    """A pager for iterating through ``list_log_entries`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListLogEntriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListLogEntries`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListLogEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., logging.ListLogEntriesResponse],
        request: logging.ListLogEntriesRequest,
        response: logging.ListLogEntriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListLogEntriesRequest`):
                The initial request object.
            response (:class:`~.logging.ListLogEntriesResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListLogEntriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[logging.ListLogEntriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[log_entry.LogEntry]:
        for page in self.pages:
            yield from page.entries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLogEntriesAsyncPager:
    """A pager for iterating through ``list_log_entries`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListLogEntriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListLogEntries`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListLogEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[logging.ListLogEntriesResponse]],
        request: logging.ListLogEntriesRequest,
        response: logging.ListLogEntriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListLogEntriesRequest`):
                The initial request object.
            response (:class:`~.logging.ListLogEntriesResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListLogEntriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[logging.ListLogEntriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[log_entry.LogEntry]:
        async def async_generator():
            async for page in self.pages:
                for response in page.entries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMonitoredResourceDescriptorsPager:
    """A pager for iterating through ``list_monitored_resource_descriptors`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListMonitoredResourceDescriptorsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``resource_descriptors`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMonitoredResourceDescriptors`` requests and continue to iterate
    through the ``resource_descriptors`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListMonitoredResourceDescriptorsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., logging.ListMonitoredResourceDescriptorsResponse],
        request: logging.ListMonitoredResourceDescriptorsRequest,
        response: logging.ListMonitoredResourceDescriptorsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListMonitoredResourceDescriptorsRequest`):
                The initial request object.
            response (:class:`~.logging.ListMonitoredResourceDescriptorsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListMonitoredResourceDescriptorsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[logging.ListMonitoredResourceDescriptorsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[monitored_resource.MonitoredResourceDescriptor]:
        for page in self.pages:
            yield from page.resource_descriptors

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMonitoredResourceDescriptorsAsyncPager:
    """A pager for iterating through ``list_monitored_resource_descriptors`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListMonitoredResourceDescriptorsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``resource_descriptors`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMonitoredResourceDescriptors`` requests and continue to iterate
    through the ``resource_descriptors`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListMonitoredResourceDescriptorsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[logging.ListMonitoredResourceDescriptorsResponse]
        ],
        request: logging.ListMonitoredResourceDescriptorsRequest,
        response: logging.ListMonitoredResourceDescriptorsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListMonitoredResourceDescriptorsRequest`):
                The initial request object.
            response (:class:`~.logging.ListMonitoredResourceDescriptorsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListMonitoredResourceDescriptorsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[logging.ListMonitoredResourceDescriptorsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterable[monitored_resource.MonitoredResourceDescriptor]:
        async def async_generator():
            async for page in self.pages:
                for response in page.resource_descriptors:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLogsPager:
    """A pager for iterating through ``list_logs`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListLogsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``log_names`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListLogs`` requests and continue to iterate
    through the ``log_names`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListLogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., logging.ListLogsResponse],
        request: logging.ListLogsRequest,
        response: logging.ListLogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListLogsRequest`):
                The initial request object.
            response (:class:`~.logging.ListLogsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListLogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[logging.ListLogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[str]:
        for page in self.pages:
            yield from page.log_names

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLogsAsyncPager:
    """A pager for iterating through ``list_logs`` requests.

    This class thinly wraps an initial
    :class:`~.logging.ListLogsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``log_names`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListLogs`` requests and continue to iterate
    through the ``log_names`` field on the
    corresponding responses.

    All the usual :class:`~.logging.ListLogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[logging.ListLogsResponse]],
        request: logging.ListLogsRequest,
        response: logging.ListLogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.logging.ListLogsRequest`):
                The initial request object.
            response (:class:`~.logging.ListLogsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = logging.ListLogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[logging.ListLogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[str]:
        async def async_generator():
            async for page in self.pages:
                for response in page.log_names:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
