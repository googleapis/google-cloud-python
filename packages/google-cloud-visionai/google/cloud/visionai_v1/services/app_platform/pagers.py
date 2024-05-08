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

from google.cloud.visionai_v1.types import platform


class ListApplicationsPager:
    """A pager for iterating through ``list_applications`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListApplicationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``applications`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApplications`` requests and continue to iterate
    through the ``applications`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListApplicationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., platform.ListApplicationsResponse],
        request: platform.ListApplicationsRequest,
        response: platform.ListApplicationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListApplicationsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListApplicationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListApplicationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[platform.ListApplicationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[platform.Application]:
        for page in self.pages:
            yield from page.applications

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApplicationsAsyncPager:
    """A pager for iterating through ``list_applications`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListApplicationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``applications`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApplications`` requests and continue to iterate
    through the ``applications`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListApplicationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[platform.ListApplicationsResponse]],
        request: platform.ListApplicationsRequest,
        response: platform.ListApplicationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListApplicationsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListApplicationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListApplicationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[platform.ListApplicationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[platform.Application]:
        async def async_generator():
            async for page in self.pages:
                for response in page.applications:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInstancesPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListInstancesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., platform.ListInstancesResponse],
        request: platform.ListInstancesRequest,
        response: platform.ListInstancesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListInstancesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[platform.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[platform.Instance]:
        for page in self.pages:
            yield from page.instances

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInstancesAsyncPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListInstancesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[platform.ListInstancesResponse]],
        request: platform.ListInstancesRequest,
        response: platform.ListInstancesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListInstancesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[platform.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[platform.Instance]:
        async def async_generator():
            async for page in self.pages:
                for response in page.instances:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDraftsPager:
    """A pager for iterating through ``list_drafts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListDraftsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``drafts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDrafts`` requests and continue to iterate
    through the ``drafts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListDraftsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., platform.ListDraftsResponse],
        request: platform.ListDraftsRequest,
        response: platform.ListDraftsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListDraftsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListDraftsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListDraftsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[platform.ListDraftsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[platform.Draft]:
        for page in self.pages:
            yield from page.drafts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDraftsAsyncPager:
    """A pager for iterating through ``list_drafts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListDraftsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``drafts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDrafts`` requests and continue to iterate
    through the ``drafts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListDraftsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[platform.ListDraftsResponse]],
        request: platform.ListDraftsRequest,
        response: platform.ListDraftsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListDraftsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListDraftsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListDraftsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[platform.ListDraftsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[platform.Draft]:
        async def async_generator():
            async for page in self.pages:
                for response in page.drafts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProcessorsPager:
    """A pager for iterating through ``list_processors`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListProcessorsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``processors`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProcessors`` requests and continue to iterate
    through the ``processors`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListProcessorsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., platform.ListProcessorsResponse],
        request: platform.ListProcessorsRequest,
        response: platform.ListProcessorsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListProcessorsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListProcessorsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListProcessorsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[platform.ListProcessorsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[platform.Processor]:
        for page in self.pages:
            yield from page.processors

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProcessorsAsyncPager:
    """A pager for iterating through ``list_processors`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.visionai_v1.types.ListProcessorsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``processors`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProcessors`` requests and continue to iterate
    through the ``processors`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.visionai_v1.types.ListProcessorsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[platform.ListProcessorsResponse]],
        request: platform.ListProcessorsRequest,
        response: platform.ListProcessorsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.visionai_v1.types.ListProcessorsRequest):
                The initial request object.
            response (google.cloud.visionai_v1.types.ListProcessorsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = platform.ListProcessorsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[platform.ListProcessorsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[platform.Processor]:
        async def async_generator():
            async for page in self.pages:
                for response in page.processors:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
