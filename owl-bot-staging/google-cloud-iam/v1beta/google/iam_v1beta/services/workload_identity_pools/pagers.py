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

from google.iam_v1beta.types import workload_identity_pool


class ListWorkloadIdentityPoolsPager:
    """A pager for iterating through ``list_workload_identity_pools`` requests.

    This class thinly wraps an initial
    :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``workload_identity_pools`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListWorkloadIdentityPools`` requests and continue to iterate
    through the ``workload_identity_pools`` field on the
    corresponding responses.

    All the usual :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., workload_identity_pool.ListWorkloadIdentityPoolsResponse],
            request: workload_identity_pool.ListWorkloadIdentityPoolsRequest,
            response: workload_identity_pool.ListWorkloadIdentityPoolsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.iam_v1beta.types.ListWorkloadIdentityPoolsRequest):
                The initial request object.
            response (google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workload_identity_pool.ListWorkloadIdentityPoolsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[workload_identity_pool.ListWorkloadIdentityPoolsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[workload_identity_pool.WorkloadIdentityPool]:
        for page in self.pages:
            yield from page.workload_identity_pools

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListWorkloadIdentityPoolsAsyncPager:
    """A pager for iterating through ``list_workload_identity_pools`` requests.

    This class thinly wraps an initial
    :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``workload_identity_pools`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListWorkloadIdentityPools`` requests and continue to iterate
    through the ``workload_identity_pools`` field on the
    corresponding responses.

    All the usual :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[workload_identity_pool.ListWorkloadIdentityPoolsResponse]],
            request: workload_identity_pool.ListWorkloadIdentityPoolsRequest,
            response: workload_identity_pool.ListWorkloadIdentityPoolsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.iam_v1beta.types.ListWorkloadIdentityPoolsRequest):
                The initial request object.
            response (google.iam_v1beta.types.ListWorkloadIdentityPoolsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workload_identity_pool.ListWorkloadIdentityPoolsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[workload_identity_pool.ListWorkloadIdentityPoolsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[workload_identity_pool.WorkloadIdentityPool]:
        async def async_generator():
            async for page in self.pages:
                for response in page.workload_identity_pools:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListWorkloadIdentityPoolProvidersPager:
    """A pager for iterating through ``list_workload_identity_pool_providers`` requests.

    This class thinly wraps an initial
    :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``workload_identity_pool_providers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListWorkloadIdentityPoolProviders`` requests and continue to iterate
    through the ``workload_identity_pool_providers`` field on the
    corresponding responses.

    All the usual :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse],
            request: workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest,
            response: workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersRequest):
                The initial request object.
            response (google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[workload_identity_pool.WorkloadIdentityPoolProvider]:
        for page in self.pages:
            yield from page.workload_identity_pool_providers

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListWorkloadIdentityPoolProvidersAsyncPager:
    """A pager for iterating through ``list_workload_identity_pool_providers`` requests.

    This class thinly wraps an initial
    :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``workload_identity_pool_providers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListWorkloadIdentityPoolProviders`` requests and continue to iterate
    through the ``workload_identity_pool_providers`` field on the
    corresponding responses.

    All the usual :class:`google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse]],
            request: workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest,
            response: workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersRequest):
                The initial request object.
            response (google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[workload_identity_pool.WorkloadIdentityPoolProvider]:
        async def async_generator():
            async for page in self.pages:
                for response in page.workload_identity_pool_providers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
