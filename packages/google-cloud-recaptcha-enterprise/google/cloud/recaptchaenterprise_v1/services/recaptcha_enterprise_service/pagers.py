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

from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise


class ListKeysPager:
    """A pager for iterating through ``list_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListKeysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``keys`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListKeys`` requests and continue to iterate
    through the ``keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., recaptchaenterprise.ListKeysResponse],
        request: recaptchaenterprise.ListKeysRequest,
        response: recaptchaenterprise.ListKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListKeysRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[recaptchaenterprise.ListKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[recaptchaenterprise.Key]:
        for page in self.pages:
            yield from page.keys

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListKeysAsyncPager:
    """A pager for iterating through ``list_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListKeysResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``keys`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListKeys`` requests and continue to iterate
    through the ``keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[recaptchaenterprise.ListKeysResponse]],
        request: recaptchaenterprise.ListKeysRequest,
        response: recaptchaenterprise.ListKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListKeysRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[recaptchaenterprise.ListKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[recaptchaenterprise.Key]:
        async def async_generator():
            async for page in self.pages:
                for response in page.keys:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRelatedAccountGroupsPager:
    """A pager for iterating through ``list_related_account_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``related_account_groups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRelatedAccountGroups`` requests and continue to iterate
    through the ``related_account_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., recaptchaenterprise.ListRelatedAccountGroupsResponse],
        request: recaptchaenterprise.ListRelatedAccountGroupsRequest,
        response: recaptchaenterprise.ListRelatedAccountGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListRelatedAccountGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[recaptchaenterprise.ListRelatedAccountGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[recaptchaenterprise.RelatedAccountGroup]:
        for page in self.pages:
            yield from page.related_account_groups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRelatedAccountGroupsAsyncPager:
    """A pager for iterating through ``list_related_account_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``related_account_groups`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRelatedAccountGroups`` requests and continue to iterate
    through the ``related_account_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[recaptchaenterprise.ListRelatedAccountGroupsResponse]
        ],
        request: recaptchaenterprise.ListRelatedAccountGroupsRequest,
        response: recaptchaenterprise.ListRelatedAccountGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListRelatedAccountGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[recaptchaenterprise.ListRelatedAccountGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[recaptchaenterprise.RelatedAccountGroup]:
        async def async_generator():
            async for page in self.pages:
                for response in page.related_account_groups:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRelatedAccountGroupMembershipsPager:
    """A pager for iterating through ``list_related_account_group_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``related_account_group_memberships`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRelatedAccountGroupMemberships`` requests and continue to iterate
    through the ``related_account_group_memberships`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse
        ],
        request: recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest,
        response: recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[recaptchaenterprise.RelatedAccountGroupMembership]:
        for page in self.pages:
            yield from page.related_account_group_memberships

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRelatedAccountGroupMembershipsAsyncPager:
    """A pager for iterating through ``list_related_account_group_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``related_account_group_memberships`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRelatedAccountGroupMemberships`` requests and continue to iterate
    through the ``related_account_group_memberships`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse],
        ],
        request: recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest,
        response: recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[recaptchaenterprise.RelatedAccountGroupMembership]:
        async def async_generator():
            async for page in self.pages:
                for response in page.related_account_group_memberships:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchRelatedAccountGroupMembershipsPager:
    """A pager for iterating through ``search_related_account_group_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``related_account_group_memberships`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``SearchRelatedAccountGroupMemberships`` requests and continue to iterate
    through the ``related_account_group_memberships`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse
        ],
        request: recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest,
        response: recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[recaptchaenterprise.RelatedAccountGroupMembership]:
        for page in self.pages:
            yield from page.related_account_group_memberships

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class SearchRelatedAccountGroupMembershipsAsyncPager:
    """A pager for iterating through ``search_related_account_group_memberships`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``related_account_group_memberships`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``SearchRelatedAccountGroupMemberships`` requests and continue to iterate
    through the ``related_account_group_memberships`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse],
        ],
        request: recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest,
        response: recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsRequest):
                The initial request object.
            response (google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[
        recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[recaptchaenterprise.RelatedAccountGroupMembership]:
        async def async_generator():
            async for page in self.pages:
                for response in page.related_account_group_memberships:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
