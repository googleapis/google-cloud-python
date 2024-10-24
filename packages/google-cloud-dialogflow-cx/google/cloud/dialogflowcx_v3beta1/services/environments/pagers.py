# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.dialogflowcx_v3beta1.types import environment


class ListEnvironmentsPager:
    """A pager for iterating through ``list_environments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEnvironments`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., environment.ListEnvironmentsResponse],
        request: environment.ListEnvironmentsRequest,
        response: environment.ListEnvironmentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.ListEnvironmentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[environment.ListEnvironmentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[environment.Environment]:
        for page in self.pages:
            yield from page.environments

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEnvironmentsAsyncPager:
    """A pager for iterating through ``list_environments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEnvironments`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[environment.ListEnvironmentsResponse]],
        request: environment.ListEnvironmentsRequest,
        response: environment.ListEnvironmentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListEnvironmentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.ListEnvironmentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[environment.ListEnvironmentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[environment.Environment]:
        async def async_generator():
            async for page in self.pages:
                for response in page.environments:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupEnvironmentHistoryPager:
    """A pager for iterating through ``lookup_environment_history`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``LookupEnvironmentHistory`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., environment.LookupEnvironmentHistoryResponse],
        request: environment.LookupEnvironmentHistoryRequest,
        response: environment.LookupEnvironmentHistoryResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.LookupEnvironmentHistoryRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[environment.LookupEnvironmentHistoryResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[environment.Environment]:
        for page in self.pages:
            yield from page.environments

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupEnvironmentHistoryAsyncPager:
    """A pager for iterating through ``lookup_environment_history`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``LookupEnvironmentHistory`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[environment.LookupEnvironmentHistoryResponse]],
        request: environment.LookupEnvironmentHistoryRequest,
        response: environment.LookupEnvironmentHistoryResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.LookupEnvironmentHistoryResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.LookupEnvironmentHistoryRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[environment.LookupEnvironmentHistoryResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[environment.Environment]:
        async def async_generator():
            async for page in self.pages:
                for response in page.environments:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListContinuousTestResultsPager:
    """A pager for iterating through ``list_continuous_test_results`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``continuous_test_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListContinuousTestResults`` requests and continue to iterate
    through the ``continuous_test_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., environment.ListContinuousTestResultsResponse],
        request: environment.ListContinuousTestResultsRequest,
        response: environment.ListContinuousTestResultsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.ListContinuousTestResultsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[environment.ListContinuousTestResultsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[environment.ContinuousTestResult]:
        for page in self.pages:
            yield from page.continuous_test_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListContinuousTestResultsAsyncPager:
    """A pager for iterating through ``list_continuous_test_results`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``continuous_test_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListContinuousTestResults`` requests and continue to iterate
    through the ``continuous_test_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[environment.ListContinuousTestResultsResponse]],
        request: environment.ListContinuousTestResultsRequest,
        response: environment.ListContinuousTestResultsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListContinuousTestResultsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.ListContinuousTestResultsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[environment.ListContinuousTestResultsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[environment.ContinuousTestResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.continuous_test_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
