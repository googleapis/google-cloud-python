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

from google.cloud.metastore_v1beta.types import metastore


class ListServicesPager:
    """A pager for iterating through ``list_services`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListServicesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``services`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServices`` requests and continue to iterate
    through the ``services`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListServicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., metastore.ListServicesResponse],
        request: metastore.ListServicesRequest,
        response: metastore.ListServicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListServicesRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListServicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListServicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[metastore.ListServicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[metastore.Service]:
        for page in self.pages:
            yield from page.services

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServicesAsyncPager:
    """A pager for iterating through ``list_services`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListServicesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``services`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListServices`` requests and continue to iterate
    through the ``services`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListServicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[metastore.ListServicesResponse]],
        request: metastore.ListServicesRequest,
        response: metastore.ListServicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListServicesRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListServicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListServicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[metastore.ListServicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[metastore.Service]:
        async def async_generator():
            async for page in self.pages:
                for response in page.services:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMetadataImportsPager:
    """A pager for iterating through ``list_metadata_imports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListMetadataImportsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``metadata_imports`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMetadataImports`` requests and continue to iterate
    through the ``metadata_imports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListMetadataImportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., metastore.ListMetadataImportsResponse],
        request: metastore.ListMetadataImportsRequest,
        response: metastore.ListMetadataImportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListMetadataImportsRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListMetadataImportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListMetadataImportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[metastore.ListMetadataImportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[metastore.MetadataImport]:
        for page in self.pages:
            yield from page.metadata_imports

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMetadataImportsAsyncPager:
    """A pager for iterating through ``list_metadata_imports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListMetadataImportsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``metadata_imports`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMetadataImports`` requests and continue to iterate
    through the ``metadata_imports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListMetadataImportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[metastore.ListMetadataImportsResponse]],
        request: metastore.ListMetadataImportsRequest,
        response: metastore.ListMetadataImportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListMetadataImportsRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListMetadataImportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListMetadataImportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[metastore.ListMetadataImportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[metastore.MetadataImport]:
        async def async_generator():
            async for page in self.pages:
                for response in page.metadata_imports:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBackupsPager:
    """A pager for iterating through ``list_backups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListBackupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``backups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListBackups`` requests and continue to iterate
    through the ``backups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListBackupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., metastore.ListBackupsResponse],
        request: metastore.ListBackupsRequest,
        response: metastore.ListBackupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListBackupsRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListBackupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListBackupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[metastore.ListBackupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[metastore.Backup]:
        for page in self.pages:
            yield from page.backups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBackupsAsyncPager:
    """A pager for iterating through ``list_backups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.metastore_v1beta.types.ListBackupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``backups`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListBackups`` requests and continue to iterate
    through the ``backups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.metastore_v1beta.types.ListBackupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[metastore.ListBackupsResponse]],
        request: metastore.ListBackupsRequest,
        response: metastore.ListBackupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.metastore_v1beta.types.ListBackupsRequest):
                The initial request object.
            response (google.cloud.metastore_v1beta.types.ListBackupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = metastore.ListBackupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[metastore.ListBackupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[metastore.Backup]:
        async def async_generator():
            async for page in self.pages:
                for response in page.backups:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
