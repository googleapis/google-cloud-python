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

from google.cloud.bigquery_datatransfer_v1.types import datatransfer
from google.cloud.bigquery_datatransfer_v1.types import transfer


class ListDataSourcesPager:
    """A pager for iterating through ``list_data_sources`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``data_sources`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDataSources`` requests and continue to iterate
    through the ``data_sources`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datatransfer.ListDataSourcesResponse],
        request: datatransfer.ListDataSourcesRequest,
        response: datatransfer.ListDataSourcesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListDataSourcesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datatransfer.ListDataSourcesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[datatransfer.DataSource]:
        for page in self.pages:
            yield from page.data_sources

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDataSourcesAsyncPager:
    """A pager for iterating through ``list_data_sources`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``data_sources`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDataSources`` requests and continue to iterate
    through the ``data_sources`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datatransfer.ListDataSourcesResponse]],
        request: datatransfer.ListDataSourcesRequest,
        response: datatransfer.ListDataSourcesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListDataSourcesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListDataSourcesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datatransfer.ListDataSourcesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[datatransfer.DataSource]:
        async def async_generator():
            async for page in self.pages:
                for response in page.data_sources:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferConfigsPager:
    """A pager for iterating through ``list_transfer_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transfer_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferConfigs`` requests and continue to iterate
    through the ``transfer_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datatransfer.ListTransferConfigsResponse],
        request: datatransfer.ListTransferConfigsRequest,
        response: datatransfer.ListTransferConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datatransfer.ListTransferConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[transfer.TransferConfig]:
        for page in self.pages:
            yield from page.transfer_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferConfigsAsyncPager:
    """A pager for iterating through ``list_transfer_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transfer_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferConfigs`` requests and continue to iterate
    through the ``transfer_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datatransfer.ListTransferConfigsResponse]],
        request: datatransfer.ListTransferConfigsRequest,
        response: datatransfer.ListTransferConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datatransfer.ListTransferConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[transfer.TransferConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transfer_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferRunsPager:
    """A pager for iterating through ``list_transfer_runs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transfer_runs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferRuns`` requests and continue to iterate
    through the ``transfer_runs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datatransfer.ListTransferRunsResponse],
        request: datatransfer.ListTransferRunsRequest,
        response: datatransfer.ListTransferRunsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferRunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datatransfer.ListTransferRunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[transfer.TransferRun]:
        for page in self.pages:
            yield from page.transfer_runs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferRunsAsyncPager:
    """A pager for iterating through ``list_transfer_runs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transfer_runs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferRuns`` requests and continue to iterate
    through the ``transfer_runs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datatransfer.ListTransferRunsResponse]],
        request: datatransfer.ListTransferRunsRequest,
        response: datatransfer.ListTransferRunsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferRunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datatransfer.ListTransferRunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[transfer.TransferRun]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transfer_runs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferLogsPager:
    """A pager for iterating through ``list_transfer_logs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transfer_messages`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferLogs`` requests and continue to iterate
    through the ``transfer_messages`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., datatransfer.ListTransferLogsResponse],
        request: datatransfer.ListTransferLogsRequest,
        response: datatransfer.ListTransferLogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferLogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[datatransfer.ListTransferLogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[transfer.TransferMessage]:
        for page in self.pages:
            yield from page.transfer_messages

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferLogsAsyncPager:
    """A pager for iterating through ``list_transfer_logs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transfer_messages`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferLogs`` requests and continue to iterate
    through the ``transfer_messages`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[datatransfer.ListTransferLogsResponse]],
        request: datatransfer.ListTransferLogsRequest,
        response: datatransfer.ListTransferLogsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsRequest):
                The initial request object.
            response (google.cloud.bigquery_datatransfer_v1.types.ListTransferLogsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = datatransfer.ListTransferLogsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[datatransfer.ListTransferLogsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[transfer.TransferMessage]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transfer_messages:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
