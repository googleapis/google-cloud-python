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

from google.cloud.securesourcemanager_v1.types import secure_source_manager


class ListInstancesPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListInstancesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., secure_source_manager.ListInstancesResponse],
        request: secure_source_manager.ListInstancesRequest,
        response: secure_source_manager.ListInstancesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListInstancesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListInstancesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[secure_source_manager.ListInstancesResponse]:
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

    def __iter__(self) -> Iterator[secure_source_manager.Instance]:
        for page in self.pages:
            yield from page.instances

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInstancesAsyncPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListInstancesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[secure_source_manager.ListInstancesResponse]],
        request: secure_source_manager.ListInstancesRequest,
        response: secure_source_manager.ListInstancesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListInstancesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListInstancesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[secure_source_manager.ListInstancesResponse]:
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

    def __aiter__(self) -> AsyncIterator[secure_source_manager.Instance]:
        async def async_generator():
            async for page in self.pages:
                for response in page.instances:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRepositoriesPager:
    """A pager for iterating through ``list_repositories`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``repositories`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRepositories`` requests and continue to iterate
    through the ``repositories`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., secure_source_manager.ListRepositoriesResponse],
        request: secure_source_manager.ListRepositoriesRequest,
        response: secure_source_manager.ListRepositoriesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListRepositoriesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListRepositoriesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[secure_source_manager.ListRepositoriesResponse]:
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

    def __iter__(self) -> Iterator[secure_source_manager.Repository]:
        for page in self.pages:
            yield from page.repositories

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRepositoriesAsyncPager:
    """A pager for iterating through ``list_repositories`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``repositories`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRepositories`` requests and continue to iterate
    through the ``repositories`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[secure_source_manager.ListRepositoriesResponse]
        ],
        request: secure_source_manager.ListRepositoriesRequest,
        response: secure_source_manager.ListRepositoriesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListRepositoriesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListRepositoriesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListRepositoriesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[secure_source_manager.ListRepositoriesResponse]:
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

    def __aiter__(self) -> AsyncIterator[secure_source_manager.Repository]:
        async def async_generator():
            async for page in self.pages:
                for response in page.repositories:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBranchRulesPager:
    """A pager for iterating through ``list_branch_rules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``branch_rules`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListBranchRules`` requests and continue to iterate
    through the ``branch_rules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., secure_source_manager.ListBranchRulesResponse],
        request: secure_source_manager.ListBranchRulesRequest,
        response: secure_source_manager.ListBranchRulesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListBranchRulesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListBranchRulesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[secure_source_manager.ListBranchRulesResponse]:
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

    def __iter__(self) -> Iterator[secure_source_manager.BranchRule]:
        for page in self.pages:
            yield from page.branch_rules

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBranchRulesAsyncPager:
    """A pager for iterating through ``list_branch_rules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``branch_rules`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListBranchRules`` requests and continue to iterate
    through the ``branch_rules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[secure_source_manager.ListBranchRulesResponse]],
        request: secure_source_manager.ListBranchRulesRequest,
        response: secure_source_manager.ListBranchRulesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securesourcemanager_v1.types.ListBranchRulesRequest):
                The initial request object.
            response (google.cloud.securesourcemanager_v1.types.ListBranchRulesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = secure_source_manager.ListBranchRulesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[secure_source_manager.ListBranchRulesResponse]:
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

    def __aiter__(self) -> AsyncIterator[secure_source_manager.BranchRule]:
        async def async_generator():
            async for page in self.pages:
                for response in page.branch_rules:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
