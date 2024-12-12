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
    Union,
)

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import retry_async as retries_async

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
    OptionalAsyncRetry = Union[
        retries_async.AsyncRetry, gapic_v1.method._MethodDefault, None
    ]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore
    OptionalAsyncRetry = Union[retries_async.AsyncRetry, object, None]  # type: ignore

from google.cloud.assuredworkloads_v1.types import assuredworkloads


class ListWorkloadsPager:
    """A pager for iterating through ``list_workloads`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``workloads`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListWorkloads`` requests and continue to iterate
    through the ``workloads`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., assuredworkloads.ListWorkloadsResponse],
        request: assuredworkloads.ListWorkloadsRequest,
        response: assuredworkloads.ListWorkloadsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.assuredworkloads_v1.types.ListWorkloadsRequest):
                The initial request object.
            response (google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = assuredworkloads.ListWorkloadsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[assuredworkloads.ListWorkloadsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[assuredworkloads.Workload]:
        for page in self.pages:
            yield from page.workloads

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListWorkloadsAsyncPager:
    """A pager for iterating through ``list_workloads`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``workloads`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListWorkloads`` requests and continue to iterate
    through the ``workloads`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[assuredworkloads.ListWorkloadsResponse]],
        request: assuredworkloads.ListWorkloadsRequest,
        response: assuredworkloads.ListWorkloadsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.assuredworkloads_v1.types.ListWorkloadsRequest):
                The initial request object.
            response (google.cloud.assuredworkloads_v1.types.ListWorkloadsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = assuredworkloads.ListWorkloadsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[assuredworkloads.ListWorkloadsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __aiter__(self) -> AsyncIterator[assuredworkloads.Workload]:
        async def async_generator():
            async for page in self.pages:
                for response in page.workloads:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListViolationsPager:
    """A pager for iterating through ``list_violations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.assuredworkloads_v1.types.ListViolationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``violations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListViolations`` requests and continue to iterate
    through the ``violations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.assuredworkloads_v1.types.ListViolationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., assuredworkloads.ListViolationsResponse],
        request: assuredworkloads.ListViolationsRequest,
        response: assuredworkloads.ListViolationsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.assuredworkloads_v1.types.ListViolationsRequest):
                The initial request object.
            response (google.cloud.assuredworkloads_v1.types.ListViolationsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = assuredworkloads.ListViolationsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[assuredworkloads.ListViolationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[assuredworkloads.Violation]:
        for page in self.pages:
            yield from page.violations

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListViolationsAsyncPager:
    """A pager for iterating through ``list_violations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.assuredworkloads_v1.types.ListViolationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``violations`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListViolations`` requests and continue to iterate
    through the ``violations`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.assuredworkloads_v1.types.ListViolationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[assuredworkloads.ListViolationsResponse]],
        request: assuredworkloads.ListViolationsRequest,
        response: assuredworkloads.ListViolationsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.assuredworkloads_v1.types.ListViolationsRequest):
                The initial request object.
            response (google.cloud.assuredworkloads_v1.types.ListViolationsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = assuredworkloads.ListViolationsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[assuredworkloads.ListViolationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __aiter__(self) -> AsyncIterator[assuredworkloads.Violation]:
        async def async_generator():
            async for page in self.pages:
                for response in page.violations:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
