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

from google.cloud.bigquery_analyticshub_v1.types import analyticshub


class ListDataExchangesPager:
    """A pager for iterating through ``list_data_exchanges`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``data_exchanges`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDataExchanges`` requests and continue to iterate
    through the ``data_exchanges`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analyticshub.ListDataExchangesResponse],
        request: analyticshub.ListDataExchangesRequest,
        response: analyticshub.ListDataExchangesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse):
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
        self._request = analyticshub.ListDataExchangesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analyticshub.ListDataExchangesResponse]:
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

    def __iter__(self) -> Iterator[analyticshub.DataExchange]:
        for page in self.pages:
            yield from page.data_exchanges

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDataExchangesAsyncPager:
    """A pager for iterating through ``list_data_exchanges`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``data_exchanges`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDataExchanges`` requests and continue to iterate
    through the ``data_exchanges`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analyticshub.ListDataExchangesResponse]],
        request: analyticshub.ListDataExchangesRequest,
        response: analyticshub.ListDataExchangesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListDataExchangesResponse):
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
        self._request = analyticshub.ListDataExchangesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[analyticshub.ListDataExchangesResponse]:
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

    def __aiter__(self) -> AsyncIterator[analyticshub.DataExchange]:
        async def async_generator():
            async for page in self.pages:
                for response in page.data_exchanges:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListOrgDataExchangesPager:
    """A pager for iterating through ``list_org_data_exchanges`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``data_exchanges`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListOrgDataExchanges`` requests and continue to iterate
    through the ``data_exchanges`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analyticshub.ListOrgDataExchangesResponse],
        request: analyticshub.ListOrgDataExchangesRequest,
        response: analyticshub.ListOrgDataExchangesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse):
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
        self._request = analyticshub.ListOrgDataExchangesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analyticshub.ListOrgDataExchangesResponse]:
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

    def __iter__(self) -> Iterator[analyticshub.DataExchange]:
        for page in self.pages:
            yield from page.data_exchanges

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListOrgDataExchangesAsyncPager:
    """A pager for iterating through ``list_org_data_exchanges`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``data_exchanges`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListOrgDataExchanges`` requests and continue to iterate
    through the ``data_exchanges`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analyticshub.ListOrgDataExchangesResponse]],
        request: analyticshub.ListOrgDataExchangesRequest,
        response: analyticshub.ListOrgDataExchangesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListOrgDataExchangesResponse):
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
        self._request = analyticshub.ListOrgDataExchangesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[analyticshub.ListOrgDataExchangesResponse]:
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

    def __aiter__(self) -> AsyncIterator[analyticshub.DataExchange]:
        async def async_generator():
            async for page in self.pages:
                for response in page.data_exchanges:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListListingsPager:
    """A pager for iterating through ``list_listings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``listings`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListListings`` requests and continue to iterate
    through the ``listings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analyticshub.ListListingsResponse],
        request: analyticshub.ListListingsRequest,
        response: analyticshub.ListListingsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListListingsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse):
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
        self._request = analyticshub.ListListingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analyticshub.ListListingsResponse]:
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

    def __iter__(self) -> Iterator[analyticshub.Listing]:
        for page in self.pages:
            yield from page.listings

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListListingsAsyncPager:
    """A pager for iterating through ``list_listings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``listings`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListListings`` requests and continue to iterate
    through the ``listings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analyticshub.ListListingsResponse]],
        request: analyticshub.ListListingsRequest,
        response: analyticshub.ListListingsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListListingsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListListingsResponse):
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
        self._request = analyticshub.ListListingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[analyticshub.ListListingsResponse]:
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

    def __aiter__(self) -> AsyncIterator[analyticshub.Listing]:
        async def async_generator():
            async for page in self.pages:
                for response in page.listings:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubscriptionsPager:
    """A pager for iterating through ``list_subscriptions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``subscriptions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSubscriptions`` requests and continue to iterate
    through the ``subscriptions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analyticshub.ListSubscriptionsResponse],
        request: analyticshub.ListSubscriptionsRequest,
        response: analyticshub.ListSubscriptionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse):
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
        self._request = analyticshub.ListSubscriptionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analyticshub.ListSubscriptionsResponse]:
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

    def __iter__(self) -> Iterator[analyticshub.Subscription]:
        for page in self.pages:
            yield from page.subscriptions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubscriptionsAsyncPager:
    """A pager for iterating through ``list_subscriptions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``subscriptions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSubscriptions`` requests and continue to iterate
    through the ``subscriptions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analyticshub.ListSubscriptionsResponse]],
        request: analyticshub.ListSubscriptionsRequest,
        response: analyticshub.ListSubscriptionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListSubscriptionsResponse):
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
        self._request = analyticshub.ListSubscriptionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[analyticshub.ListSubscriptionsResponse]:
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

    def __aiter__(self) -> AsyncIterator[analyticshub.Subscription]:
        async def async_generator():
            async for page in self.pages:
                for response in page.subscriptions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSharedResourceSubscriptionsPager:
    """A pager for iterating through ``list_shared_resource_subscriptions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``shared_resource_subscriptions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSharedResourceSubscriptions`` requests and continue to iterate
    through the ``shared_resource_subscriptions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analyticshub.ListSharedResourceSubscriptionsResponse],
        request: analyticshub.ListSharedResourceSubscriptionsRequest,
        response: analyticshub.ListSharedResourceSubscriptionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse):
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
        self._request = analyticshub.ListSharedResourceSubscriptionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[analyticshub.ListSharedResourceSubscriptionsResponse]:
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

    def __iter__(self) -> Iterator[analyticshub.Subscription]:
        for page in self.pages:
            yield from page.shared_resource_subscriptions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSharedResourceSubscriptionsAsyncPager:
    """A pager for iterating through ``list_shared_resource_subscriptions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``shared_resource_subscriptions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSharedResourceSubscriptions`` requests and continue to iterate
    through the ``shared_resource_subscriptions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[analyticshub.ListSharedResourceSubscriptionsResponse]
        ],
        request: analyticshub.ListSharedResourceSubscriptionsRequest,
        response: analyticshub.ListSharedResourceSubscriptionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsRequest):
                The initial request object.
            response (google.cloud.bigquery_analyticshub_v1.types.ListSharedResourceSubscriptionsResponse):
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
        self._request = analyticshub.ListSharedResourceSubscriptionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[analyticshub.ListSharedResourceSubscriptionsResponse]:
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

    def __aiter__(self) -> AsyncIterator[analyticshub.Subscription]:
        async def async_generator():
            async for page in self.pages:
                for response in page.shared_resource_subscriptions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
