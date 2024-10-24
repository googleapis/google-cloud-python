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

from google.cloud.dialogflowcx_v3beta1.types import test_case


class ListTestCasesPager:
    """A pager for iterating through ``list_test_cases`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``test_cases`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTestCases`` requests and continue to iterate
    through the ``test_cases`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., test_case.ListTestCasesResponse],
        request: test_case.ListTestCasesRequest,
        response: test_case.ListTestCasesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListTestCasesRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = test_case.ListTestCasesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[test_case.ListTestCasesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[test_case.TestCase]:
        for page in self.pages:
            yield from page.test_cases

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTestCasesAsyncPager:
    """A pager for iterating through ``list_test_cases`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``test_cases`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTestCases`` requests and continue to iterate
    through the ``test_cases`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[test_case.ListTestCasesResponse]],
        request: test_case.ListTestCasesRequest,
        response: test_case.ListTestCasesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListTestCasesRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListTestCasesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = test_case.ListTestCasesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[test_case.ListTestCasesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[test_case.TestCase]:
        async def async_generator():
            async for page in self.pages:
                for response in page.test_cases:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTestCaseResultsPager:
    """A pager for iterating through ``list_test_case_results`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``test_case_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTestCaseResults`` requests and continue to iterate
    through the ``test_case_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., test_case.ListTestCaseResultsResponse],
        request: test_case.ListTestCaseResultsRequest,
        response: test_case.ListTestCaseResultsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = test_case.ListTestCaseResultsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[test_case.ListTestCaseResultsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[test_case.TestCaseResult]:
        for page in self.pages:
            yield from page.test_case_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTestCaseResultsAsyncPager:
    """A pager for iterating through ``list_test_case_results`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``test_case_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTestCaseResults`` requests and continue to iterate
    through the ``test_case_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[test_case.ListTestCaseResultsResponse]],
        request: test_case.ListTestCaseResultsRequest,
        response: test_case.ListTestCaseResultsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListTestCaseResultsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = test_case.ListTestCaseResultsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[test_case.ListTestCaseResultsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[test_case.TestCaseResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.test_case_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
