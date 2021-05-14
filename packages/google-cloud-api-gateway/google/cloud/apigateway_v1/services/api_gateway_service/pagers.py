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

from google.cloud.apigateway_v1.types import apigateway


class ListGatewaysPager:
    """A pager for iterating through ``list_gateways`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListGatewaysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``gateways`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGateways`` requests and continue to iterate
    through the ``gateways`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListGatewaysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., apigateway.ListGatewaysResponse],
        request: apigateway.ListGatewaysRequest,
        response: apigateway.ListGatewaysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListGatewaysRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListGatewaysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListGatewaysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[apigateway.ListGatewaysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[apigateway.Gateway]:
        for page in self.pages:
            yield from page.gateways

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGatewaysAsyncPager:
    """A pager for iterating through ``list_gateways`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListGatewaysResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``gateways`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListGateways`` requests and continue to iterate
    through the ``gateways`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListGatewaysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[apigateway.ListGatewaysResponse]],
        request: apigateway.ListGatewaysRequest,
        response: apigateway.ListGatewaysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListGatewaysRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListGatewaysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListGatewaysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[apigateway.ListGatewaysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[apigateway.Gateway]:
        async def async_generator():
            async for page in self.pages:
                for response in page.gateways:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApisPager:
    """A pager for iterating through ``list_apis`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListApisResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``apis`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApis`` requests and continue to iterate
    through the ``apis`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListApisResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., apigateway.ListApisResponse],
        request: apigateway.ListApisRequest,
        response: apigateway.ListApisResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListApisRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListApisResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListApisRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[apigateway.ListApisResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[apigateway.Api]:
        for page in self.pages:
            yield from page.apis

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApisAsyncPager:
    """A pager for iterating through ``list_apis`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListApisResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``apis`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApis`` requests and continue to iterate
    through the ``apis`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListApisResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[apigateway.ListApisResponse]],
        request: apigateway.ListApisRequest,
        response: apigateway.ListApisResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListApisRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListApisResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListApisRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[apigateway.ListApisResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[apigateway.Api]:
        async def async_generator():
            async for page in self.pages:
                for response in page.apis:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiConfigsPager:
    """A pager for iterating through ``list_api_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListApiConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiConfigs`` requests and continue to iterate
    through the ``api_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListApiConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., apigateway.ListApiConfigsResponse],
        request: apigateway.ListApiConfigsRequest,
        response: apigateway.ListApiConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListApiConfigsRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListApiConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListApiConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[apigateway.ListApiConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[apigateway.ApiConfig]:
        for page in self.pages:
            yield from page.api_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiConfigsAsyncPager:
    """A pager for iterating through ``list_api_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigateway_v1.types.ListApiConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiConfigs`` requests and continue to iterate
    through the ``api_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigateway_v1.types.ListApiConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[apigateway.ListApiConfigsResponse]],
        request: apigateway.ListApiConfigsRequest,
        response: apigateway.ListApiConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigateway_v1.types.ListApiConfigsRequest):
                The initial request object.
            response (google.cloud.apigateway_v1.types.ListApiConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = apigateway.ListApiConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[apigateway.ListApiConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[apigateway.ApiConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
