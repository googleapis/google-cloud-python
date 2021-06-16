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

from google.cloud.workflows_v1beta.types import workflows


class ListWorkflowsPager:
    """A pager for iterating through ``list_workflows`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.workflows_v1beta.types.ListWorkflowsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``workflows`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListWorkflows`` requests and continue to iterate
    through the ``workflows`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.workflows_v1beta.types.ListWorkflowsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., workflows.ListWorkflowsResponse],
        request: workflows.ListWorkflowsRequest,
        response: workflows.ListWorkflowsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.workflows_v1beta.types.ListWorkflowsRequest):
                The initial request object.
            response (google.cloud.workflows_v1beta.types.ListWorkflowsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workflows.ListWorkflowsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[workflows.ListWorkflowsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[workflows.Workflow]:
        for page in self.pages:
            yield from page.workflows

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListWorkflowsAsyncPager:
    """A pager for iterating through ``list_workflows`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.workflows_v1beta.types.ListWorkflowsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``workflows`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListWorkflows`` requests and continue to iterate
    through the ``workflows`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.workflows_v1beta.types.ListWorkflowsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[workflows.ListWorkflowsResponse]],
        request: workflows.ListWorkflowsRequest,
        response: workflows.ListWorkflowsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.workflows_v1beta.types.ListWorkflowsRequest):
                The initial request object.
            response (google.cloud.workflows_v1beta.types.ListWorkflowsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = workflows.ListWorkflowsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[workflows.ListWorkflowsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[workflows.Workflow]:
        async def async_generator():
            async for page in self.pages:
                for response in page.workflows:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
