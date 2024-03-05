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

from google.cloud.dialogflow_v2.types import environment


class ListEnvironmentsPager:
    """A pager for iterating through ``list_environments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflow_v2.types.ListEnvironmentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEnvironments`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflow_v2.types.ListEnvironmentsResponse`
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
            request (google.cloud.dialogflow_v2.types.ListEnvironmentsRequest):
                The initial request object.
            response (google.cloud.dialogflow_v2.types.ListEnvironmentsResponse):
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
    :class:`google.cloud.dialogflow_v2.types.ListEnvironmentsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``environments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEnvironments`` requests and continue to iterate
    through the ``environments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflow_v2.types.ListEnvironmentsResponse`
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
            request (google.cloud.dialogflow_v2.types.ListEnvironmentsRequest):
                The initial request object.
            response (google.cloud.dialogflow_v2.types.ListEnvironmentsResponse):
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


class GetEnvironmentHistoryPager:
    """A pager for iterating through ``get_environment_history`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflow_v2.types.EnvironmentHistory` object, and
    provides an ``__iter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``GetEnvironmentHistory`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflow_v2.types.EnvironmentHistory`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., environment.EnvironmentHistory],
        request: environment.GetEnvironmentHistoryRequest,
        response: environment.EnvironmentHistory,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflow_v2.types.GetEnvironmentHistoryRequest):
                The initial request object.
            response (google.cloud.dialogflow_v2.types.EnvironmentHistory):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.GetEnvironmentHistoryRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[environment.EnvironmentHistory]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[environment.EnvironmentHistory.Entry]:
        for page in self.pages:
            yield from page.entries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class GetEnvironmentHistoryAsyncPager:
    """A pager for iterating through ``get_environment_history`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflow_v2.types.EnvironmentHistory` object, and
    provides an ``__aiter__`` method to iterate through its
    ``entries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``GetEnvironmentHistory`` requests and continue to iterate
    through the ``entries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflow_v2.types.EnvironmentHistory`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[environment.EnvironmentHistory]],
        request: environment.GetEnvironmentHistoryRequest,
        response: environment.EnvironmentHistory,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflow_v2.types.GetEnvironmentHistoryRequest):
                The initial request object.
            response (google.cloud.dialogflow_v2.types.EnvironmentHistory):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = environment.GetEnvironmentHistoryRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[environment.EnvironmentHistory]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[environment.EnvironmentHistory.Entry]:
        async def async_generator():
            async for page in self.pages:
                for response in page.entries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
