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
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    Sequence,
    Tuple,
    Optional,
)

from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import resources


class ListAccountsPager:
    """A pager for iterating through ``list_accounts`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAccountsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``accounts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAccounts`` requests and continue to iterate
    through the ``accounts`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAccountsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListAccountsResponse],
        request: analytics_admin.ListAccountsRequest,
        response: analytics_admin.ListAccountsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAccountsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAccountsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAccountsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListAccountsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.Account]:
        for page in self.pages:
            yield from page.accounts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAccountsAsyncPager:
    """A pager for iterating through ``list_accounts`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAccountsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``accounts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAccounts`` requests and continue to iterate
    through the ``accounts`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAccountsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListAccountsResponse]],
        request: analytics_admin.ListAccountsRequest,
        response: analytics_admin.ListAccountsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAccountsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAccountsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAccountsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListAccountsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.Account]:
        async def async_generator():
            async for page in self.pages:
                for response in page.accounts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAccountSummariesPager:
    """A pager for iterating through ``list_account_summaries`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAccountSummariesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``account_summaries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAccountSummaries`` requests and continue to iterate
    through the ``account_summaries`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAccountSummariesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListAccountSummariesResponse],
        request: analytics_admin.ListAccountSummariesRequest,
        response: analytics_admin.ListAccountSummariesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAccountSummariesRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAccountSummariesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAccountSummariesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListAccountSummariesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.AccountSummary]:
        for page in self.pages:
            yield from page.account_summaries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAccountSummariesAsyncPager:
    """A pager for iterating through ``list_account_summaries`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAccountSummariesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``account_summaries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAccountSummaries`` requests and continue to iterate
    through the ``account_summaries`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAccountSummariesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListAccountSummariesResponse]],
        request: analytics_admin.ListAccountSummariesRequest,
        response: analytics_admin.ListAccountSummariesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAccountSummariesRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAccountSummariesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAccountSummariesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListAccountSummariesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.AccountSummary]:
        async def async_generator():
            async for page in self.pages:
                for response in page.account_summaries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPropertiesPager:
    """A pager for iterating through ``list_properties`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListPropertiesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``properties`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProperties`` requests and continue to iterate
    through the ``properties`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListPropertiesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListPropertiesResponse],
        request: analytics_admin.ListPropertiesRequest,
        response: analytics_admin.ListPropertiesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListPropertiesRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListPropertiesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListPropertiesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListPropertiesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.Property]:
        for page in self.pages:
            yield from page.properties

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPropertiesAsyncPager:
    """A pager for iterating through ``list_properties`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListPropertiesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``properties`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProperties`` requests and continue to iterate
    through the ``properties`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListPropertiesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListPropertiesResponse]],
        request: analytics_admin.ListPropertiesRequest,
        response: analytics_admin.ListPropertiesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListPropertiesRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListPropertiesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListPropertiesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListPropertiesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.Property]:
        async def async_generator():
            async for page in self.pages:
                for response in page.properties:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListUserLinksPager:
    """A pager for iterating through ``list_user_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListUserLinksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``user_links`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListUserLinks`` requests and continue to iterate
    through the ``user_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListUserLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListUserLinksResponse],
        request: analytics_admin.ListUserLinksRequest,
        response: analytics_admin.ListUserLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListUserLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListUserLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListUserLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListUserLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.UserLink]:
        for page in self.pages:
            yield from page.user_links

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListUserLinksAsyncPager:
    """A pager for iterating through ``list_user_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListUserLinksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``user_links`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListUserLinks`` requests and continue to iterate
    through the ``user_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListUserLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListUserLinksResponse]],
        request: analytics_admin.ListUserLinksRequest,
        response: analytics_admin.ListUserLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListUserLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListUserLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListUserLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListUserLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.UserLink]:
        async def async_generator():
            async for page in self.pages:
                for response in page.user_links:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class AuditUserLinksPager:
    """A pager for iterating through ``audit_user_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.AuditUserLinksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``user_links`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``AuditUserLinks`` requests and continue to iterate
    through the ``user_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.AuditUserLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.AuditUserLinksResponse],
        request: analytics_admin.AuditUserLinksRequest,
        response: analytics_admin.AuditUserLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.AuditUserLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.AuditUserLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.AuditUserLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.AuditUserLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.AuditUserLink]:
        for page in self.pages:
            yield from page.user_links

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class AuditUserLinksAsyncPager:
    """A pager for iterating through ``audit_user_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.AuditUserLinksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``user_links`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``AuditUserLinks`` requests and continue to iterate
    through the ``user_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.AuditUserLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.AuditUserLinksResponse]],
        request: analytics_admin.AuditUserLinksRequest,
        response: analytics_admin.AuditUserLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.AuditUserLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.AuditUserLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.AuditUserLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.AuditUserLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.AuditUserLink]:
        async def async_generator():
            async for page in self.pages:
                for response in page.user_links:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListWebDataStreamsPager:
    """A pager for iterating through ``list_web_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``web_data_streams`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListWebDataStreams`` requests and continue to iterate
    through the ``web_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListWebDataStreamsResponse],
        request: analytics_admin.ListWebDataStreamsRequest,
        response: analytics_admin.ListWebDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListWebDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListWebDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListWebDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.WebDataStream]:
        for page in self.pages:
            yield from page.web_data_streams

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListWebDataStreamsAsyncPager:
    """A pager for iterating through ``list_web_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``web_data_streams`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListWebDataStreams`` requests and continue to iterate
    through the ``web_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListWebDataStreamsResponse]],
        request: analytics_admin.ListWebDataStreamsRequest,
        response: analytics_admin.ListWebDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListWebDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListWebDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListWebDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListWebDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.WebDataStream]:
        async def async_generator():
            async for page in self.pages:
                for response in page.web_data_streams:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListIosAppDataStreamsPager:
    """A pager for iterating through ``list_ios_app_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``ios_app_data_streams`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListIosAppDataStreams`` requests and continue to iterate
    through the ``ios_app_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListIosAppDataStreamsResponse],
        request: analytics_admin.ListIosAppDataStreamsRequest,
        response: analytics_admin.ListIosAppDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListIosAppDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListIosAppDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListIosAppDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.IosAppDataStream]:
        for page in self.pages:
            yield from page.ios_app_data_streams

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListIosAppDataStreamsAsyncPager:
    """A pager for iterating through ``list_ios_app_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``ios_app_data_streams`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListIosAppDataStreams`` requests and continue to iterate
    through the ``ios_app_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListIosAppDataStreamsResponse]],
        request: analytics_admin.ListIosAppDataStreamsRequest,
        response: analytics_admin.ListIosAppDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListIosAppDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListIosAppDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListIosAppDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListIosAppDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.IosAppDataStream]:
        async def async_generator():
            async for page in self.pages:
                for response in page.ios_app_data_streams:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAndroidAppDataStreamsPager:
    """A pager for iterating through ``list_android_app_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``android_app_data_streams`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAndroidAppDataStreams`` requests and continue to iterate
    through the ``android_app_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListAndroidAppDataStreamsResponse],
        request: analytics_admin.ListAndroidAppDataStreamsRequest,
        response: analytics_admin.ListAndroidAppDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAndroidAppDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListAndroidAppDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.AndroidAppDataStream]:
        for page in self.pages:
            yield from page.android_app_data_streams

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAndroidAppDataStreamsAsyncPager:
    """A pager for iterating through ``list_android_app_data_streams`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``android_app_data_streams`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAndroidAppDataStreams`` requests and continue to iterate
    through the ``android_app_data_streams`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[analytics_admin.ListAndroidAppDataStreamsResponse]
        ],
        request: analytics_admin.ListAndroidAppDataStreamsRequest,
        response: analytics_admin.ListAndroidAppDataStreamsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListAndroidAppDataStreamsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListAndroidAppDataStreamsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListAndroidAppDataStreamsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.AndroidAppDataStream]:
        async def async_generator():
            async for page in self.pages:
                for response in page.android_app_data_streams:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListFirebaseLinksPager:
    """A pager for iterating through ``list_firebase_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``firebase_links`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListFirebaseLinks`` requests and continue to iterate
    through the ``firebase_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListFirebaseLinksResponse],
        request: analytics_admin.ListFirebaseLinksRequest,
        response: analytics_admin.ListFirebaseLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListFirebaseLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListFirebaseLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListFirebaseLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.FirebaseLink]:
        for page in self.pages:
            yield from page.firebase_links

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListFirebaseLinksAsyncPager:
    """A pager for iterating through ``list_firebase_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``firebase_links`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListFirebaseLinks`` requests and continue to iterate
    through the ``firebase_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListFirebaseLinksResponse]],
        request: analytics_admin.ListFirebaseLinksRequest,
        response: analytics_admin.ListFirebaseLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListFirebaseLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListFirebaseLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListFirebaseLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListFirebaseLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.FirebaseLink]:
        async def async_generator():
            async for page in self.pages:
                for response in page.firebase_links:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGoogleAdsLinksPager:
    """A pager for iterating through ``list_google_ads_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``google_ads_links`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGoogleAdsLinks`` requests and continue to iterate
    through the ``google_ads_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListGoogleAdsLinksResponse],
        request: analytics_admin.ListGoogleAdsLinksRequest,
        response: analytics_admin.ListGoogleAdsLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListGoogleAdsLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListGoogleAdsLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListGoogleAdsLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.GoogleAdsLink]:
        for page in self.pages:
            yield from page.google_ads_links

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGoogleAdsLinksAsyncPager:
    """A pager for iterating through ``list_google_ads_links`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``google_ads_links`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListGoogleAdsLinks`` requests and continue to iterate
    through the ``google_ads_links`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListGoogleAdsLinksResponse]],
        request: analytics_admin.ListGoogleAdsLinksRequest,
        response: analytics_admin.ListGoogleAdsLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListGoogleAdsLinksRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListGoogleAdsLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListGoogleAdsLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListGoogleAdsLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.GoogleAdsLink]:
        async def async_generator():
            async for page in self.pages:
                for response in page.google_ads_links:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMeasurementProtocolSecretsPager:
    """A pager for iterating through ``list_measurement_protocol_secrets`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``measurement_protocol_secrets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMeasurementProtocolSecrets`` requests and continue to iterate
    through the ``measurement_protocol_secrets`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListMeasurementProtocolSecretsResponse],
        request: analytics_admin.ListMeasurementProtocolSecretsRequest,
        response: analytics_admin.ListMeasurementProtocolSecretsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListMeasurementProtocolSecretsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListMeasurementProtocolSecretsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.MeasurementProtocolSecret]:
        for page in self.pages:
            yield from page.measurement_protocol_secrets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMeasurementProtocolSecretsAsyncPager:
    """A pager for iterating through ``list_measurement_protocol_secrets`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``measurement_protocol_secrets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMeasurementProtocolSecrets`` requests and continue to iterate
    through the ``measurement_protocol_secrets`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[analytics_admin.ListMeasurementProtocolSecretsResponse]
        ],
        request: analytics_admin.ListMeasurementProtocolSecretsRequest,
        response: analytics_admin.ListMeasurementProtocolSecretsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListMeasurementProtocolSecretsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListMeasurementProtocolSecretsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.MeasurementProtocolSecret]:
        async def async_generator():
            async for page in self.pages:
                for response in page.measurement_protocol_secrets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchChangeHistoryEventsPager:
    """A pager for iterating through ``search_change_history_events`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``change_history_events`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchChangeHistoryEvents`` requests and continue to iterate
    through the ``change_history_events`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.SearchChangeHistoryEventsResponse],
        request: analytics_admin.SearchChangeHistoryEventsRequest,
        response: analytics_admin.SearchChangeHistoryEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.SearchChangeHistoryEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.SearchChangeHistoryEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.ChangeHistoryEvent]:
        for page in self.pages:
            yield from page.change_history_events

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchChangeHistoryEventsAsyncPager:
    """A pager for iterating through ``search_change_history_events`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``change_history_events`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchChangeHistoryEvents`` requests and continue to iterate
    through the ``change_history_events`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[analytics_admin.SearchChangeHistoryEventsResponse]
        ],
        request: analytics_admin.SearchChangeHistoryEventsRequest,
        response: analytics_admin.SearchChangeHistoryEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.SearchChangeHistoryEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.SearchChangeHistoryEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.ChangeHistoryEvent]:
        async def async_generator():
            async for page in self.pages:
                for response in page.change_history_events:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConversionEventsPager:
    """A pager for iterating through ``list_conversion_events`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListConversionEventsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``conversion_events`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConversionEvents`` requests and continue to iterate
    through the ``conversion_events`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListConversionEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListConversionEventsResponse],
        request: analytics_admin.ListConversionEventsRequest,
        response: analytics_admin.ListConversionEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListConversionEventsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListConversionEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListConversionEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListConversionEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.ConversionEvent]:
        for page in self.pages:
            yield from page.conversion_events

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConversionEventsAsyncPager:
    """A pager for iterating through ``list_conversion_events`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListConversionEventsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``conversion_events`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConversionEvents`` requests and continue to iterate
    through the ``conversion_events`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListConversionEventsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListConversionEventsResponse]],
        request: analytics_admin.ListConversionEventsRequest,
        response: analytics_admin.ListConversionEventsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListConversionEventsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListConversionEventsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListConversionEventsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListConversionEventsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.ConversionEvent]:
        async def async_generator():
            async for page in self.pages:
                for response in page.conversion_events:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCustomDimensionsPager:
    """A pager for iterating through ``list_custom_dimensions`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``custom_dimensions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCustomDimensions`` requests and continue to iterate
    through the ``custom_dimensions`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListCustomDimensionsResponse],
        request: analytics_admin.ListCustomDimensionsRequest,
        response: analytics_admin.ListCustomDimensionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListCustomDimensionsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListCustomDimensionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListCustomDimensionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.CustomDimension]:
        for page in self.pages:
            yield from page.custom_dimensions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCustomDimensionsAsyncPager:
    """A pager for iterating through ``list_custom_dimensions`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``custom_dimensions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCustomDimensions`` requests and continue to iterate
    through the ``custom_dimensions`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListCustomDimensionsResponse]],
        request: analytics_admin.ListCustomDimensionsRequest,
        response: analytics_admin.ListCustomDimensionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListCustomDimensionsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListCustomDimensionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListCustomDimensionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[analytics_admin.ListCustomDimensionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.CustomDimension]:
        async def async_generator():
            async for page in self.pages:
                for response in page.custom_dimensions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCustomMetricsPager:
    """A pager for iterating through ``list_custom_metrics`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListCustomMetricsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``custom_metrics`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCustomMetrics`` requests and continue to iterate
    through the ``custom_metrics`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListCustomMetricsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., analytics_admin.ListCustomMetricsResponse],
        request: analytics_admin.ListCustomMetricsRequest,
        response: analytics_admin.ListCustomMetricsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListCustomMetricsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListCustomMetricsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListCustomMetricsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[analytics_admin.ListCustomMetricsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.CustomMetric]:
        for page in self.pages:
            yield from page.custom_metrics

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCustomMetricsAsyncPager:
    """A pager for iterating through ``list_custom_metrics`` requests.

    This class thinly wraps an initial
    :class:`google.analytics.admin_v1alpha.types.ListCustomMetricsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``custom_metrics`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCustomMetrics`` requests and continue to iterate
    through the ``custom_metrics`` field on the
    corresponding responses.

    All the usual :class:`google.analytics.admin_v1alpha.types.ListCustomMetricsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[analytics_admin.ListCustomMetricsResponse]],
        request: analytics_admin.ListCustomMetricsRequest,
        response: analytics_admin.ListCustomMetricsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.analytics.admin_v1alpha.types.ListCustomMetricsRequest):
                The initial request object.
            response (google.analytics.admin_v1alpha.types.ListCustomMetricsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = analytics_admin.ListCustomMetricsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[analytics_admin.ListCustomMetricsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.CustomMetric]:
        async def async_generator():
            async for page in self.pages:
                for response in page.custom_metrics:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
