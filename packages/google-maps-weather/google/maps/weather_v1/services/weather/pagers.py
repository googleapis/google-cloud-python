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

from google.maps.weather_v1.types import (
    forecast_day,
    forecast_hour,
    history_hour,
    weather_service,
)


class LookupForecastHoursPager:
    """A pager for iterating through ``lookup_forecast_hours`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupForecastHoursResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``forecast_hours`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``LookupForecastHours`` requests and continue to iterate
    through the ``forecast_hours`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupForecastHoursResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., weather_service.LookupForecastHoursResponse],
        request: weather_service.LookupForecastHoursRequest,
        response: weather_service.LookupForecastHoursResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupForecastHoursRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupForecastHoursResponse):
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
        self._request = weather_service.LookupForecastHoursRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[weather_service.LookupForecastHoursResponse]:
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

    def __iter__(self) -> Iterator[forecast_hour.ForecastHour]:
        for page in self.pages:
            yield from page.forecast_hours

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupForecastHoursAsyncPager:
    """A pager for iterating through ``lookup_forecast_hours`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupForecastHoursResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``forecast_hours`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``LookupForecastHours`` requests and continue to iterate
    through the ``forecast_hours`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupForecastHoursResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[weather_service.LookupForecastHoursResponse]],
        request: weather_service.LookupForecastHoursRequest,
        response: weather_service.LookupForecastHoursResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupForecastHoursRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupForecastHoursResponse):
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
        self._request = weather_service.LookupForecastHoursRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[weather_service.LookupForecastHoursResponse]:
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

    def __aiter__(self) -> AsyncIterator[forecast_hour.ForecastHour]:
        async def async_generator():
            async for page in self.pages:
                for response in page.forecast_hours:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupForecastDaysPager:
    """A pager for iterating through ``lookup_forecast_days`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupForecastDaysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``forecast_days`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``LookupForecastDays`` requests and continue to iterate
    through the ``forecast_days`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupForecastDaysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., weather_service.LookupForecastDaysResponse],
        request: weather_service.LookupForecastDaysRequest,
        response: weather_service.LookupForecastDaysResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupForecastDaysRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupForecastDaysResponse):
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
        self._request = weather_service.LookupForecastDaysRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[weather_service.LookupForecastDaysResponse]:
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

    def __iter__(self) -> Iterator[forecast_day.ForecastDay]:
        for page in self.pages:
            yield from page.forecast_days

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupForecastDaysAsyncPager:
    """A pager for iterating through ``lookup_forecast_days`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupForecastDaysResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``forecast_days`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``LookupForecastDays`` requests and continue to iterate
    through the ``forecast_days`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupForecastDaysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[weather_service.LookupForecastDaysResponse]],
        request: weather_service.LookupForecastDaysRequest,
        response: weather_service.LookupForecastDaysResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupForecastDaysRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupForecastDaysResponse):
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
        self._request = weather_service.LookupForecastDaysRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[weather_service.LookupForecastDaysResponse]:
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

    def __aiter__(self) -> AsyncIterator[forecast_day.ForecastDay]:
        async def async_generator():
            async for page in self.pages:
                for response in page.forecast_days:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupHistoryHoursPager:
    """A pager for iterating through ``lookup_history_hours`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupHistoryHoursResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``history_hours`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``LookupHistoryHours`` requests and continue to iterate
    through the ``history_hours`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupHistoryHoursResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., weather_service.LookupHistoryHoursResponse],
        request: weather_service.LookupHistoryHoursRequest,
        response: weather_service.LookupHistoryHoursResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupHistoryHoursRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupHistoryHoursResponse):
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
        self._request = weather_service.LookupHistoryHoursRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[weather_service.LookupHistoryHoursResponse]:
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

    def __iter__(self) -> Iterator[history_hour.HistoryHour]:
        for page in self.pages:
            yield from page.history_hours

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class LookupHistoryHoursAsyncPager:
    """A pager for iterating through ``lookup_history_hours`` requests.

    This class thinly wraps an initial
    :class:`google.maps.weather_v1.types.LookupHistoryHoursResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``history_hours`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``LookupHistoryHours`` requests and continue to iterate
    through the ``history_hours`` field on the
    corresponding responses.

    All the usual :class:`google.maps.weather_v1.types.LookupHistoryHoursResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[weather_service.LookupHistoryHoursResponse]],
        request: weather_service.LookupHistoryHoursRequest,
        response: weather_service.LookupHistoryHoursResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.weather_v1.types.LookupHistoryHoursRequest):
                The initial request object.
            response (google.maps.weather_v1.types.LookupHistoryHoursResponse):
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
        self._request = weather_service.LookupHistoryHoursRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[weather_service.LookupHistoryHoursResponse]:
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

    def __aiter__(self) -> AsyncIterator[history_hour.HistoryHour]:
        async def async_generator():
            async for page in self.pages:
                for response in page.history_hours:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
