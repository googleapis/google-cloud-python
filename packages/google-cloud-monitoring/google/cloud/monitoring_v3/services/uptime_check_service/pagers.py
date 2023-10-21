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

from google.cloud.monitoring_v3.types import uptime
from google.cloud.monitoring_v3.types import uptime_service


class ListUptimeCheckConfigsPager:
    """A pager for iterating through ``list_uptime_check_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``uptime_check_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListUptimeCheckConfigs`` requests and continue to iterate
    through the ``uptime_check_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., uptime_service.ListUptimeCheckConfigsResponse],
        request: uptime_service.ListUptimeCheckConfigsRequest,
        response: uptime_service.ListUptimeCheckConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListUptimeCheckConfigsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = uptime_service.ListUptimeCheckConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[uptime_service.ListUptimeCheckConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[uptime.UptimeCheckConfig]:
        for page in self.pages:
            yield from page.uptime_check_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListUptimeCheckConfigsAsyncPager:
    """A pager for iterating through ``list_uptime_check_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``uptime_check_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListUptimeCheckConfigs`` requests and continue to iterate
    through the ``uptime_check_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[uptime_service.ListUptimeCheckConfigsResponse]],
        request: uptime_service.ListUptimeCheckConfigsRequest,
        response: uptime_service.ListUptimeCheckConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListUptimeCheckConfigsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListUptimeCheckConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = uptime_service.ListUptimeCheckConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[uptime_service.ListUptimeCheckConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[uptime.UptimeCheckConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.uptime_check_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListUptimeCheckIpsPager:
    """A pager for iterating through ``list_uptime_check_ips`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``uptime_check_ips`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListUptimeCheckIps`` requests and continue to iterate
    through the ``uptime_check_ips`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., uptime_service.ListUptimeCheckIpsResponse],
        request: uptime_service.ListUptimeCheckIpsRequest,
        response: uptime_service.ListUptimeCheckIpsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListUptimeCheckIpsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = uptime_service.ListUptimeCheckIpsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[uptime_service.ListUptimeCheckIpsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[uptime.UptimeCheckIp]:
        for page in self.pages:
            yield from page.uptime_check_ips

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListUptimeCheckIpsAsyncPager:
    """A pager for iterating through ``list_uptime_check_ips`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``uptime_check_ips`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListUptimeCheckIps`` requests and continue to iterate
    through the ``uptime_check_ips`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[uptime_service.ListUptimeCheckIpsResponse]],
        request: uptime_service.ListUptimeCheckIpsRequest,
        response: uptime_service.ListUptimeCheckIpsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListUptimeCheckIpsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListUptimeCheckIpsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = uptime_service.ListUptimeCheckIpsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[uptime_service.ListUptimeCheckIpsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[uptime.UptimeCheckIp]:
        async def async_generator():
            async for page in self.pages:
                for response in page.uptime_check_ips:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
