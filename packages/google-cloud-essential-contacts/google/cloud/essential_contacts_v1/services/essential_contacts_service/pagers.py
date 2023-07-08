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

from google.cloud.essential_contacts_v1.types import service


class ListContactsPager:
    """A pager for iterating through ``list_contacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.essential_contacts_v1.types.ListContactsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``contacts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListContacts`` requests and continue to iterate
    through the ``contacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.essential_contacts_v1.types.ListContactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListContactsResponse],
        request: service.ListContactsRequest,
        response: service.ListContactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.essential_contacts_v1.types.ListContactsRequest):
                The initial request object.
            response (google.cloud.essential_contacts_v1.types.ListContactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListContactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListContactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[service.Contact]:
        for page in self.pages:
            yield from page.contacts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListContactsAsyncPager:
    """A pager for iterating through ``list_contacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.essential_contacts_v1.types.ListContactsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``contacts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListContacts`` requests and continue to iterate
    through the ``contacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.essential_contacts_v1.types.ListContactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListContactsResponse]],
        request: service.ListContactsRequest,
        response: service.ListContactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.essential_contacts_v1.types.ListContactsRequest):
                The initial request object.
            response (google.cloud.essential_contacts_v1.types.ListContactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListContactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListContactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[service.Contact]:
        async def async_generator():
            async for page in self.pages:
                for response in page.contacts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ComputeContactsPager:
    """A pager for iterating through ``compute_contacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.essential_contacts_v1.types.ComputeContactsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``contacts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ComputeContacts`` requests and continue to iterate
    through the ``contacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.essential_contacts_v1.types.ComputeContactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ComputeContactsResponse],
        request: service.ComputeContactsRequest,
        response: service.ComputeContactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.essential_contacts_v1.types.ComputeContactsRequest):
                The initial request object.
            response (google.cloud.essential_contacts_v1.types.ComputeContactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ComputeContactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ComputeContactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[service.Contact]:
        for page in self.pages:
            yield from page.contacts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ComputeContactsAsyncPager:
    """A pager for iterating through ``compute_contacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.essential_contacts_v1.types.ComputeContactsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``contacts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ComputeContacts`` requests and continue to iterate
    through the ``contacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.essential_contacts_v1.types.ComputeContactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ComputeContactsResponse]],
        request: service.ComputeContactsRequest,
        response: service.ComputeContactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.essential_contacts_v1.types.ComputeContactsRequest):
                The initial request object.
            response (google.cloud.essential_contacts_v1.types.ComputeContactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ComputeContactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ComputeContactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[service.Contact]:
        async def async_generator():
            async for page in self.pages:
                for response in page.contacts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
