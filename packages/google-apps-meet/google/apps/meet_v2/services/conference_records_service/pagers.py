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

from google.apps.meet_v2.types import resource, service


class ListConferenceRecordsPager:
    """A pager for iterating through ``list_conference_records`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListConferenceRecordsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``conference_records`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConferenceRecords`` requests and continue to iterate
    through the ``conference_records`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListConferenceRecordsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListConferenceRecordsResponse],
        request: service.ListConferenceRecordsRequest,
        response: service.ListConferenceRecordsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListConferenceRecordsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListConferenceRecordsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListConferenceRecordsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListConferenceRecordsResponse]:
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

    def __iter__(self) -> Iterator[resource.ConferenceRecord]:
        for page in self.pages:
            yield from page.conference_records

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConferenceRecordsAsyncPager:
    """A pager for iterating through ``list_conference_records`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListConferenceRecordsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``conference_records`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConferenceRecords`` requests and continue to iterate
    through the ``conference_records`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListConferenceRecordsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListConferenceRecordsResponse]],
        request: service.ListConferenceRecordsRequest,
        response: service.ListConferenceRecordsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListConferenceRecordsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListConferenceRecordsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListConferenceRecordsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListConferenceRecordsResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.ConferenceRecord]:
        async def async_generator():
            async for page in self.pages:
                for response in page.conference_records:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListParticipantsPager:
    """A pager for iterating through ``list_participants`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListParticipantsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``participants`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListParticipants`` requests and continue to iterate
    through the ``participants`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListParticipantsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListParticipantsResponse],
        request: service.ListParticipantsRequest,
        response: service.ListParticipantsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListParticipantsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListParticipantsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListParticipantsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListParticipantsResponse]:
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

    def __iter__(self) -> Iterator[resource.Participant]:
        for page in self.pages:
            yield from page.participants

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListParticipantsAsyncPager:
    """A pager for iterating through ``list_participants`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListParticipantsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``participants`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListParticipants`` requests and continue to iterate
    through the ``participants`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListParticipantsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListParticipantsResponse]],
        request: service.ListParticipantsRequest,
        response: service.ListParticipantsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListParticipantsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListParticipantsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListParticipantsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListParticipantsResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.Participant]:
        async def async_generator():
            async for page in self.pages:
                for response in page.participants:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListParticipantSessionsPager:
    """A pager for iterating through ``list_participant_sessions`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListParticipantSessionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``participant_sessions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListParticipantSessions`` requests and continue to iterate
    through the ``participant_sessions`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListParticipantSessionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListParticipantSessionsResponse],
        request: service.ListParticipantSessionsRequest,
        response: service.ListParticipantSessionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListParticipantSessionsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListParticipantSessionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListParticipantSessionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListParticipantSessionsResponse]:
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

    def __iter__(self) -> Iterator[resource.ParticipantSession]:
        for page in self.pages:
            yield from page.participant_sessions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListParticipantSessionsAsyncPager:
    """A pager for iterating through ``list_participant_sessions`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListParticipantSessionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``participant_sessions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListParticipantSessions`` requests and continue to iterate
    through the ``participant_sessions`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListParticipantSessionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListParticipantSessionsResponse]],
        request: service.ListParticipantSessionsRequest,
        response: service.ListParticipantSessionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListParticipantSessionsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListParticipantSessionsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListParticipantSessionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListParticipantSessionsResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.ParticipantSession]:
        async def async_generator():
            async for page in self.pages:
                for response in page.participant_sessions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRecordingsPager:
    """A pager for iterating through ``list_recordings`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListRecordingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``recordings`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRecordings`` requests and continue to iterate
    through the ``recordings`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListRecordingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListRecordingsResponse],
        request: service.ListRecordingsRequest,
        response: service.ListRecordingsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListRecordingsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListRecordingsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListRecordingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListRecordingsResponse]:
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

    def __iter__(self) -> Iterator[resource.Recording]:
        for page in self.pages:
            yield from page.recordings

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRecordingsAsyncPager:
    """A pager for iterating through ``list_recordings`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListRecordingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``recordings`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRecordings`` requests and continue to iterate
    through the ``recordings`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListRecordingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListRecordingsResponse]],
        request: service.ListRecordingsRequest,
        response: service.ListRecordingsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListRecordingsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListRecordingsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListRecordingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListRecordingsResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.Recording]:
        async def async_generator():
            async for page in self.pages:
                for response in page.recordings:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTranscriptsPager:
    """A pager for iterating through ``list_transcripts`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListTranscriptsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transcripts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTranscripts`` requests and continue to iterate
    through the ``transcripts`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListTranscriptsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListTranscriptsResponse],
        request: service.ListTranscriptsRequest,
        response: service.ListTranscriptsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListTranscriptsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListTranscriptsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListTranscriptsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListTranscriptsResponse]:
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

    def __iter__(self) -> Iterator[resource.Transcript]:
        for page in self.pages:
            yield from page.transcripts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTranscriptsAsyncPager:
    """A pager for iterating through ``list_transcripts`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListTranscriptsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transcripts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTranscripts`` requests and continue to iterate
    through the ``transcripts`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListTranscriptsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListTranscriptsResponse]],
        request: service.ListTranscriptsRequest,
        response: service.ListTranscriptsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListTranscriptsRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListTranscriptsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListTranscriptsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListTranscriptsResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.Transcript]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transcripts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTranscriptEntriesPager:
    """A pager for iterating through ``list_transcript_entries`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListTranscriptEntriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transcript_entries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTranscriptEntries`` requests and continue to iterate
    through the ``transcript_entries`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListTranscriptEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListTranscriptEntriesResponse],
        request: service.ListTranscriptEntriesRequest,
        response: service.ListTranscriptEntriesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListTranscriptEntriesRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListTranscriptEntriesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListTranscriptEntriesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListTranscriptEntriesResponse]:
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

    def __iter__(self) -> Iterator[resource.TranscriptEntry]:
        for page in self.pages:
            yield from page.transcript_entries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTranscriptEntriesAsyncPager:
    """A pager for iterating through ``list_transcript_entries`` requests.

    This class thinly wraps an initial
    :class:`google.apps.meet_v2.types.ListTranscriptEntriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transcript_entries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTranscriptEntries`` requests and continue to iterate
    through the ``transcript_entries`` field on the
    corresponding responses.

    All the usual :class:`google.apps.meet_v2.types.ListTranscriptEntriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListTranscriptEntriesResponse]],
        request: service.ListTranscriptEntriesRequest,
        response: service.ListTranscriptEntriesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.apps.meet_v2.types.ListTranscriptEntriesRequest):
                The initial request object.
            response (google.apps.meet_v2.types.ListTranscriptEntriesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        self._method = method
        self._request = service.ListTranscriptEntriesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListTranscriptEntriesResponse]:
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

    def __aiter__(self) -> AsyncIterator[resource.TranscriptEntry]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transcript_entries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
