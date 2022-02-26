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

from google.cloud.clouddms_v1.types import clouddms
from google.cloud.clouddms_v1.types import clouddms_resources


class ListMigrationJobsPager:
    """A pager for iterating through ``list_migration_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.clouddms_v1.types.ListMigrationJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``migration_jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMigrationJobs`` requests and continue to iterate
    through the ``migration_jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.clouddms_v1.types.ListMigrationJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., clouddms.ListMigrationJobsResponse],
        request: clouddms.ListMigrationJobsRequest,
        response: clouddms.ListMigrationJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.clouddms_v1.types.ListMigrationJobsRequest):
                The initial request object.
            response (google.cloud.clouddms_v1.types.ListMigrationJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = clouddms.ListMigrationJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[clouddms.ListMigrationJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[clouddms_resources.MigrationJob]:
        for page in self.pages:
            yield from page.migration_jobs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMigrationJobsAsyncPager:
    """A pager for iterating through ``list_migration_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.clouddms_v1.types.ListMigrationJobsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``migration_jobs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMigrationJobs`` requests and continue to iterate
    through the ``migration_jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.clouddms_v1.types.ListMigrationJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[clouddms.ListMigrationJobsResponse]],
        request: clouddms.ListMigrationJobsRequest,
        response: clouddms.ListMigrationJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.clouddms_v1.types.ListMigrationJobsRequest):
                The initial request object.
            response (google.cloud.clouddms_v1.types.ListMigrationJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = clouddms.ListMigrationJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[clouddms.ListMigrationJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[clouddms_resources.MigrationJob]:
        async def async_generator():
            async for page in self.pages:
                for response in page.migration_jobs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConnectionProfilesPager:
    """A pager for iterating through ``list_connection_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.clouddms_v1.types.ListConnectionProfilesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``connection_profiles`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConnectionProfiles`` requests and continue to iterate
    through the ``connection_profiles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.clouddms_v1.types.ListConnectionProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., clouddms.ListConnectionProfilesResponse],
        request: clouddms.ListConnectionProfilesRequest,
        response: clouddms.ListConnectionProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.clouddms_v1.types.ListConnectionProfilesRequest):
                The initial request object.
            response (google.cloud.clouddms_v1.types.ListConnectionProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = clouddms.ListConnectionProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[clouddms.ListConnectionProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[clouddms_resources.ConnectionProfile]:
        for page in self.pages:
            yield from page.connection_profiles

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConnectionProfilesAsyncPager:
    """A pager for iterating through ``list_connection_profiles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.clouddms_v1.types.ListConnectionProfilesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``connection_profiles`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConnectionProfiles`` requests and continue to iterate
    through the ``connection_profiles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.clouddms_v1.types.ListConnectionProfilesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[clouddms.ListConnectionProfilesResponse]],
        request: clouddms.ListConnectionProfilesRequest,
        response: clouddms.ListConnectionProfilesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.clouddms_v1.types.ListConnectionProfilesRequest):
                The initial request object.
            response (google.cloud.clouddms_v1.types.ListConnectionProfilesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = clouddms.ListConnectionProfilesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[clouddms.ListConnectionProfilesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[clouddms_resources.ConnectionProfile]:
        async def async_generator():
            async for page in self.pages:
                for response in page.connection_profiles:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
