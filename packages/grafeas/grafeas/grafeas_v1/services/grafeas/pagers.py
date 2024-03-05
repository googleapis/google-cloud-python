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

from grafeas.grafeas_v1.types import grafeas


class ListOccurrencesPager:
    """A pager for iterating through ``list_occurrences`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListOccurrencesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``occurrences`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListOccurrences`` requests and continue to iterate
    through the ``occurrences`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListOccurrencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., grafeas.ListOccurrencesResponse],
        request: grafeas.ListOccurrencesRequest,
        response: grafeas.ListOccurrencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListOccurrencesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListOccurrencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListOccurrencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[grafeas.ListOccurrencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[grafeas.Occurrence]:
        for page in self.pages:
            yield from page.occurrences

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListOccurrencesAsyncPager:
    """A pager for iterating through ``list_occurrences`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListOccurrencesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``occurrences`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListOccurrences`` requests and continue to iterate
    through the ``occurrences`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListOccurrencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[grafeas.ListOccurrencesResponse]],
        request: grafeas.ListOccurrencesRequest,
        response: grafeas.ListOccurrencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListOccurrencesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListOccurrencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListOccurrencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[grafeas.ListOccurrencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[grafeas.Occurrence]:
        async def async_generator():
            async for page in self.pages:
                for response in page.occurrences:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNotesPager:
    """A pager for iterating through ``list_notes`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListNotesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``notes`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNotes`` requests and continue to iterate
    through the ``notes`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListNotesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., grafeas.ListNotesResponse],
        request: grafeas.ListNotesRequest,
        response: grafeas.ListNotesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListNotesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListNotesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListNotesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[grafeas.ListNotesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[grafeas.Note]:
        for page in self.pages:
            yield from page.notes

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNotesAsyncPager:
    """A pager for iterating through ``list_notes`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListNotesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``notes`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNotes`` requests and continue to iterate
    through the ``notes`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListNotesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[grafeas.ListNotesResponse]],
        request: grafeas.ListNotesRequest,
        response: grafeas.ListNotesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListNotesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListNotesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListNotesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[grafeas.ListNotesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[grafeas.Note]:
        async def async_generator():
            async for page in self.pages:
                for response in page.notes:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNoteOccurrencesPager:
    """A pager for iterating through ``list_note_occurrences`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListNoteOccurrencesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``occurrences`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNoteOccurrences`` requests and continue to iterate
    through the ``occurrences`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListNoteOccurrencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., grafeas.ListNoteOccurrencesResponse],
        request: grafeas.ListNoteOccurrencesRequest,
        response: grafeas.ListNoteOccurrencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListNoteOccurrencesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListNoteOccurrencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListNoteOccurrencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[grafeas.ListNoteOccurrencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[grafeas.Occurrence]:
        for page in self.pages:
            yield from page.occurrences

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNoteOccurrencesAsyncPager:
    """A pager for iterating through ``list_note_occurrences`` requests.

    This class thinly wraps an initial
    :class:`grafeas.grafeas_v1.types.ListNoteOccurrencesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``occurrences`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNoteOccurrences`` requests and continue to iterate
    through the ``occurrences`` field on the
    corresponding responses.

    All the usual :class:`grafeas.grafeas_v1.types.ListNoteOccurrencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[grafeas.ListNoteOccurrencesResponse]],
        request: grafeas.ListNoteOccurrencesRequest,
        response: grafeas.ListNoteOccurrencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (grafeas.grafeas_v1.types.ListNoteOccurrencesRequest):
                The initial request object.
            response (grafeas.grafeas_v1.types.ListNoteOccurrencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = grafeas.ListNoteOccurrencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[grafeas.ListNoteOccurrencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[grafeas.Occurrence]:
        async def async_generator():
            async for page in self.pages:
                for response in page.occurrences:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
