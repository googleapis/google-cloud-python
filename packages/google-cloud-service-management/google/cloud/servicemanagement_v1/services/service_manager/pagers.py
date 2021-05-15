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

from google.api import service_pb2  # type: ignore
from google.cloud.servicemanagement_v1.types import resources
from google.cloud.servicemanagement_v1.types import servicemanager


class ListServicesPager:
    """A pager for iterating through ``list_services`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServicesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``services`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServices`` requests and continue to iterate
    through the ``services`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., servicemanager.ListServicesResponse],
        request: servicemanager.ListServicesRequest,
        response: servicemanager.ListServicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServicesRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[servicemanager.ListServicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.ManagedService]:
        for page in self.pages:
            yield from page.services

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServicesAsyncPager:
    """A pager for iterating through ``list_services`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServicesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``services`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListServices`` requests and continue to iterate
    through the ``services`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[servicemanager.ListServicesResponse]],
        request: servicemanager.ListServicesRequest,
        response: servicemanager.ListServicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServicesRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[servicemanager.ListServicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.ManagedService]:
        async def async_generator():
            async for page in self.pages:
                for response in page.services:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServiceConfigsPager:
    """A pager for iterating through ``list_service_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``service_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServiceConfigs`` requests and continue to iterate
    through the ``service_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., servicemanager.ListServiceConfigsResponse],
        request: servicemanager.ListServiceConfigsRequest,
        response: servicemanager.ListServiceConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServiceConfigsRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServiceConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[servicemanager.ListServiceConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[service_pb2.Service]:
        for page in self.pages:
            yield from page.service_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServiceConfigsAsyncPager:
    """A pager for iterating through ``list_service_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``service_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListServiceConfigs`` requests and continue to iterate
    through the ``service_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[servicemanager.ListServiceConfigsResponse]],
        request: servicemanager.ListServiceConfigsRequest,
        response: servicemanager.ListServiceConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServiceConfigsRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServiceConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServiceConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[servicemanager.ListServiceConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[service_pb2.Service]:
        async def async_generator():
            async for page in self.pages:
                for response in page.service_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServiceRolloutsPager:
    """A pager for iterating through ``list_service_rollouts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``rollouts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServiceRollouts`` requests and continue to iterate
    through the ``rollouts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., servicemanager.ListServiceRolloutsResponse],
        request: servicemanager.ListServiceRolloutsRequest,
        response: servicemanager.ListServiceRolloutsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServiceRolloutsRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServiceRolloutsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[servicemanager.ListServiceRolloutsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.Rollout]:
        for page in self.pages:
            yield from page.rollouts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServiceRolloutsAsyncPager:
    """A pager for iterating through ``list_service_rollouts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``rollouts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListServiceRollouts`` requests and continue to iterate
    through the ``rollouts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[servicemanager.ListServiceRolloutsResponse]],
        request: servicemanager.ListServiceRolloutsRequest,
        response: servicemanager.ListServiceRolloutsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.servicemanagement_v1.types.ListServiceRolloutsRequest):
                The initial request object.
            response (google.cloud.servicemanagement_v1.types.ListServiceRolloutsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = servicemanager.ListServiceRolloutsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[servicemanager.ListServiceRolloutsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.Rollout]:
        async def async_generator():
            async for page in self.pages:
                for response in page.rollouts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
