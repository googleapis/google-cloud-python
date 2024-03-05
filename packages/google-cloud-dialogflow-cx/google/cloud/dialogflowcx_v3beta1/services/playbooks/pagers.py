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

from google.cloud.dialogflowcx_v3beta1.types import playbook


class ListPlaybooksPager:
    """A pager for iterating through ``list_playbooks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``playbooks`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPlaybooks`` requests and continue to iterate
    through the ``playbooks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., playbook.ListPlaybooksResponse],
        request: playbook.ListPlaybooksRequest,
        response: playbook.ListPlaybooksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = playbook.ListPlaybooksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[playbook.ListPlaybooksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[playbook.Playbook]:
        for page in self.pages:
            yield from page.playbooks

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPlaybooksAsyncPager:
    """A pager for iterating through ``list_playbooks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``playbooks`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPlaybooks`` requests and continue to iterate
    through the ``playbooks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[playbook.ListPlaybooksResponse]],
        request: playbook.ListPlaybooksRequest,
        response: playbook.ListPlaybooksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListPlaybooksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = playbook.ListPlaybooksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[playbook.ListPlaybooksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[playbook.Playbook]:
        async def async_generator():
            async for page in self.pages:
                for response in page.playbooks:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPlaybookVersionsPager:
    """A pager for iterating through ``list_playbook_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``playbook_versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPlaybookVersions`` requests and continue to iterate
    through the ``playbook_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., playbook.ListPlaybookVersionsResponse],
        request: playbook.ListPlaybookVersionsRequest,
        response: playbook.ListPlaybookVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = playbook.ListPlaybookVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[playbook.ListPlaybookVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[playbook.PlaybookVersion]:
        for page in self.pages:
            yield from page.playbook_versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPlaybookVersionsAsyncPager:
    """A pager for iterating through ``list_playbook_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``playbook_versions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPlaybookVersions`` requests and continue to iterate
    through the ``playbook_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[playbook.ListPlaybookVersionsResponse]],
        request: playbook.ListPlaybookVersionsRequest,
        response: playbook.ListPlaybookVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListPlaybookVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = playbook.ListPlaybookVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[playbook.ListPlaybookVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[playbook.PlaybookVersion]:
        async def async_generator():
            async for page in self.pages:
                for response in page.playbook_versions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
