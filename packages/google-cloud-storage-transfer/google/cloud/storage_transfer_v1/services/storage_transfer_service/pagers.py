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
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.storage_transfer_v1.types import transfer, transfer_types


class ListTransferJobsPager:
    """A pager for iterating through ``list_transfer_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storage_transfer_v1.types.ListTransferJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transfer_jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferJobs`` requests and continue to iterate
    through the ``transfer_jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storage_transfer_v1.types.ListTransferJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., transfer.ListTransferJobsResponse],
        request: transfer.ListTransferJobsRequest,
        response: transfer.ListTransferJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storage_transfer_v1.types.ListTransferJobsRequest):
                The initial request object.
            response (google.cloud.storage_transfer_v1.types.ListTransferJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = transfer.ListTransferJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[transfer.ListTransferJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[transfer_types.TransferJob]:
        for page in self.pages:
            yield from page.transfer_jobs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferJobsAsyncPager:
    """A pager for iterating through ``list_transfer_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storage_transfer_v1.types.ListTransferJobsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transfer_jobs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferJobs`` requests and continue to iterate
    through the ``transfer_jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storage_transfer_v1.types.ListTransferJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[transfer.ListTransferJobsResponse]],
        request: transfer.ListTransferJobsRequest,
        response: transfer.ListTransferJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storage_transfer_v1.types.ListTransferJobsRequest):
                The initial request object.
            response (google.cloud.storage_transfer_v1.types.ListTransferJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = transfer.ListTransferJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[transfer.ListTransferJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[transfer_types.TransferJob]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transfer_jobs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAgentPoolsPager:
    """A pager for iterating through ``list_agent_pools`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``agent_pools`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAgentPools`` requests and continue to iterate
    through the ``agent_pools`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., transfer.ListAgentPoolsResponse],
        request: transfer.ListAgentPoolsRequest,
        response: transfer.ListAgentPoolsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storage_transfer_v1.types.ListAgentPoolsRequest):
                The initial request object.
            response (google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = transfer.ListAgentPoolsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[transfer.ListAgentPoolsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[transfer_types.AgentPool]:
        for page in self.pages:
            yield from page.agent_pools

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAgentPoolsAsyncPager:
    """A pager for iterating through ``list_agent_pools`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``agent_pools`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAgentPools`` requests and continue to iterate
    through the ``agent_pools`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[transfer.ListAgentPoolsResponse]],
        request: transfer.ListAgentPoolsRequest,
        response: transfer.ListAgentPoolsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storage_transfer_v1.types.ListAgentPoolsRequest):
                The initial request object.
            response (google.cloud.storage_transfer_v1.types.ListAgentPoolsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = transfer.ListAgentPoolsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[transfer.ListAgentPoolsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[transfer_types.AgentPool]:
        async def async_generator():
            async for page in self.pages:
                for response in page.agent_pools:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
