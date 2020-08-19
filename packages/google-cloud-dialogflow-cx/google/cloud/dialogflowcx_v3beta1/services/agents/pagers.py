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

from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, Sequence, Tuple

from google.cloud.dialogflowcx_v3beta1.types import agent


class ListAgentsPager:
    """A pager for iterating through ``list_agents`` requests.

    This class thinly wraps an initial
    :class:`~.agent.ListAgentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``agents`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAgents`` requests and continue to iterate
    through the ``agents`` field on the
    corresponding responses.

    All the usual :class:`~.agent.ListAgentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., agent.ListAgentsResponse],
        request: agent.ListAgentsRequest,
        response: agent.ListAgentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.agent.ListAgentsRequest`):
                The initial request object.
            response (:class:`~.agent.ListAgentsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = agent.ListAgentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[agent.ListAgentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[agent.Agent]:
        for page in self.pages:
            yield from page.agents

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAgentsAsyncPager:
    """A pager for iterating through ``list_agents`` requests.

    This class thinly wraps an initial
    :class:`~.agent.ListAgentsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``agents`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAgents`` requests and continue to iterate
    through the ``agents`` field on the
    corresponding responses.

    All the usual :class:`~.agent.ListAgentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[agent.ListAgentsResponse]],
        request: agent.ListAgentsRequest,
        response: agent.ListAgentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.agent.ListAgentsRequest`):
                The initial request object.
            response (:class:`~.agent.ListAgentsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = agent.ListAgentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[agent.ListAgentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[agent.Agent]:
        async def async_generator():
            async for page in self.pages:
                for response in page.agents:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
