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

from google.cloud.resourcemanager_v3.types import tag_bindings


class ListTagBindingsPager:
    """A pager for iterating through ``list_tag_bindings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.resourcemanager_v3.types.ListTagBindingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``tag_bindings`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTagBindings`` requests and continue to iterate
    through the ``tag_bindings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.resourcemanager_v3.types.ListTagBindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., tag_bindings.ListTagBindingsResponse],
        request: tag_bindings.ListTagBindingsRequest,
        response: tag_bindings.ListTagBindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.resourcemanager_v3.types.ListTagBindingsRequest):
                The initial request object.
            response (google.cloud.resourcemanager_v3.types.ListTagBindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = tag_bindings.ListTagBindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[tag_bindings.ListTagBindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[tag_bindings.TagBinding]:
        for page in self.pages:
            yield from page.tag_bindings

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTagBindingsAsyncPager:
    """A pager for iterating through ``list_tag_bindings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.resourcemanager_v3.types.ListTagBindingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``tag_bindings`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTagBindings`` requests and continue to iterate
    through the ``tag_bindings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.resourcemanager_v3.types.ListTagBindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[tag_bindings.ListTagBindingsResponse]],
        request: tag_bindings.ListTagBindingsRequest,
        response: tag_bindings.ListTagBindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.resourcemanager_v3.types.ListTagBindingsRequest):
                The initial request object.
            response (google.cloud.resourcemanager_v3.types.ListTagBindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = tag_bindings.ListTagBindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[tag_bindings.ListTagBindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[tag_bindings.TagBinding]:
        async def async_generator():
            async for page in self.pages:
                for response in page.tag_bindings:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEffectiveTagsPager:
    """A pager for iterating through ``list_effective_tags`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``effective_tags`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEffectiveTags`` requests and continue to iterate
    through the ``effective_tags`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., tag_bindings.ListEffectiveTagsResponse],
        request: tag_bindings.ListEffectiveTagsRequest,
        response: tag_bindings.ListEffectiveTagsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.resourcemanager_v3.types.ListEffectiveTagsRequest):
                The initial request object.
            response (google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = tag_bindings.ListEffectiveTagsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[tag_bindings.ListEffectiveTagsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[tag_bindings.EffectiveTag]:
        for page in self.pages:
            yield from page.effective_tags

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEffectiveTagsAsyncPager:
    """A pager for iterating through ``list_effective_tags`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``effective_tags`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEffectiveTags`` requests and continue to iterate
    through the ``effective_tags`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[tag_bindings.ListEffectiveTagsResponse]],
        request: tag_bindings.ListEffectiveTagsRequest,
        response: tag_bindings.ListEffectiveTagsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.resourcemanager_v3.types.ListEffectiveTagsRequest):
                The initial request object.
            response (google.cloud.resourcemanager_v3.types.ListEffectiveTagsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = tag_bindings.ListEffectiveTagsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[tag_bindings.ListEffectiveTagsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[tag_bindings.EffectiveTag]:
        async def async_generator():
            async for page in self.pages:
                for response in page.effective_tags:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
