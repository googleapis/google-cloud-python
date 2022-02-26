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
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.cloud.bigtable_admin_v2.types import bigtable_table_admin
from google.cloud.bigtable_admin_v2.types import table


class ListTablesPager:
    """A pager for iterating through ``list_tables`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListTablesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``tables`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTables`` requests and continue to iterate
    through the ``tables`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListTablesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., bigtable_table_admin.ListTablesResponse],
        request: bigtable_table_admin.ListTablesRequest,
        response: bigtable_table_admin.ListTablesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListTablesRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListTablesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListTablesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[bigtable_table_admin.ListTablesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[table.Table]:
        for page in self.pages:
            yield from page.tables

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTablesAsyncPager:
    """A pager for iterating through ``list_tables`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListTablesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``tables`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTables`` requests and continue to iterate
    through the ``tables`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListTablesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[bigtable_table_admin.ListTablesResponse]],
        request: bigtable_table_admin.ListTablesRequest,
        response: bigtable_table_admin.ListTablesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListTablesRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListTablesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListTablesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[bigtable_table_admin.ListTablesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[table.Table]:
        async def async_generator():
            async for page in self.pages:
                for response in page.tables:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSnapshotsPager:
    """A pager for iterating through ``list_snapshots`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``snapshots`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSnapshots`` requests and continue to iterate
    through the ``snapshots`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., bigtable_table_admin.ListSnapshotsResponse],
        request: bigtable_table_admin.ListSnapshotsRequest,
        response: bigtable_table_admin.ListSnapshotsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListSnapshotsRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListSnapshotsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[bigtable_table_admin.ListSnapshotsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[table.Snapshot]:
        for page in self.pages:
            yield from page.snapshots

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSnapshotsAsyncPager:
    """A pager for iterating through ``list_snapshots`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``snapshots`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSnapshots`` requests and continue to iterate
    through the ``snapshots`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[bigtable_table_admin.ListSnapshotsResponse]],
        request: bigtable_table_admin.ListSnapshotsRequest,
        response: bigtable_table_admin.ListSnapshotsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListSnapshotsRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListSnapshotsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListSnapshotsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[bigtable_table_admin.ListSnapshotsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[table.Snapshot]:
        async def async_generator():
            async for page in self.pages:
                for response in page.snapshots:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBackupsPager:
    """A pager for iterating through ``list_backups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListBackupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``backups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListBackups`` requests and continue to iterate
    through the ``backups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListBackupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., bigtable_table_admin.ListBackupsResponse],
        request: bigtable_table_admin.ListBackupsRequest,
        response: bigtable_table_admin.ListBackupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListBackupsRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListBackupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListBackupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[bigtable_table_admin.ListBackupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[table.Backup]:
        for page in self.pages:
            yield from page.backups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBackupsAsyncPager:
    """A pager for iterating through ``list_backups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigtable_admin_v2.types.ListBackupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``backups`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListBackups`` requests and continue to iterate
    through the ``backups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigtable_admin_v2.types.ListBackupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[bigtable_table_admin.ListBackupsResponse]],
        request: bigtable_table_admin.ListBackupsRequest,
        response: bigtable_table_admin.ListBackupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigtable_admin_v2.types.ListBackupsRequest):
                The initial request object.
            response (google.cloud.bigtable_admin_v2.types.ListBackupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = bigtable_table_admin.ListBackupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[bigtable_table_admin.ListBackupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[table.Backup]:
        async def async_generator():
            async for page in self.pages:
                for response in page.backups:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
