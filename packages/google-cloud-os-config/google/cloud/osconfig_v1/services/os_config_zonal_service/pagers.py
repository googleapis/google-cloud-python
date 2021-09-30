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

from google.cloud.osconfig_v1.types import inventory
from google.cloud.osconfig_v1.types import vulnerability


class ListInventoriesPager:
    """A pager for iterating through ``list_inventories`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.osconfig_v1.types.ListInventoriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``inventories`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListInventories`` requests and continue to iterate
    through the ``inventories`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.osconfig_v1.types.ListInventoriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., inventory.ListInventoriesResponse],
        request: inventory.ListInventoriesRequest,
        response: inventory.ListInventoriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.osconfig_v1.types.ListInventoriesRequest):
                The initial request object.
            response (google.cloud.osconfig_v1.types.ListInventoriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = inventory.ListInventoriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[inventory.ListInventoriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[inventory.Inventory]:
        for page in self.pages:
            yield from page.inventories

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInventoriesAsyncPager:
    """A pager for iterating through ``list_inventories`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.osconfig_v1.types.ListInventoriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``inventories`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListInventories`` requests and continue to iterate
    through the ``inventories`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.osconfig_v1.types.ListInventoriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[inventory.ListInventoriesResponse]],
        request: inventory.ListInventoriesRequest,
        response: inventory.ListInventoriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.osconfig_v1.types.ListInventoriesRequest):
                The initial request object.
            response (google.cloud.osconfig_v1.types.ListInventoriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = inventory.ListInventoriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[inventory.ListInventoriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[inventory.Inventory]:
        async def async_generator():
            async for page in self.pages:
                for response in page.inventories:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVulnerabilityReportsPager:
    """A pager for iterating through ``list_vulnerability_reports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``vulnerability_reports`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVulnerabilityReports`` requests and continue to iterate
    through the ``vulnerability_reports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vulnerability.ListVulnerabilityReportsResponse],
        request: vulnerability.ListVulnerabilityReportsRequest,
        response: vulnerability.ListVulnerabilityReportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.osconfig_v1.types.ListVulnerabilityReportsRequest):
                The initial request object.
            response (google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vulnerability.ListVulnerabilityReportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vulnerability.ListVulnerabilityReportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vulnerability.VulnerabilityReport]:
        for page in self.pages:
            yield from page.vulnerability_reports

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVulnerabilityReportsAsyncPager:
    """A pager for iterating through ``list_vulnerability_reports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``vulnerability_reports`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVulnerabilityReports`` requests and continue to iterate
    through the ``vulnerability_reports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[vulnerability.ListVulnerabilityReportsResponse]
        ],
        request: vulnerability.ListVulnerabilityReportsRequest,
        response: vulnerability.ListVulnerabilityReportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.osconfig_v1.types.ListVulnerabilityReportsRequest):
                The initial request object.
            response (google.cloud.osconfig_v1.types.ListVulnerabilityReportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vulnerability.ListVulnerabilityReportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[vulnerability.ListVulnerabilityReportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vulnerability.VulnerabilityReport]:
        async def async_generator():
            async for page in self.pages:
                for response in page.vulnerability_reports:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
