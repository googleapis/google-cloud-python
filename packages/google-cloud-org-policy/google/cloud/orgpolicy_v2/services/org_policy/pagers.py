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

from google.cloud.orgpolicy_v2.types import constraint
from google.cloud.orgpolicy_v2.types import orgpolicy


class ListConstraintsPager:
    """A pager for iterating through ``list_constraints`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.orgpolicy_v2.types.ListConstraintsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``constraints`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConstraints`` requests and continue to iterate
    through the ``constraints`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.orgpolicy_v2.types.ListConstraintsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., orgpolicy.ListConstraintsResponse],
        request: orgpolicy.ListConstraintsRequest,
        response: orgpolicy.ListConstraintsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.orgpolicy_v2.types.ListConstraintsRequest):
                The initial request object.
            response (google.cloud.orgpolicy_v2.types.ListConstraintsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = orgpolicy.ListConstraintsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[orgpolicy.ListConstraintsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[constraint.Constraint]:
        for page in self.pages:
            yield from page.constraints

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConstraintsAsyncPager:
    """A pager for iterating through ``list_constraints`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.orgpolicy_v2.types.ListConstraintsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``constraints`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConstraints`` requests and continue to iterate
    through the ``constraints`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.orgpolicy_v2.types.ListConstraintsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[orgpolicy.ListConstraintsResponse]],
        request: orgpolicy.ListConstraintsRequest,
        response: orgpolicy.ListConstraintsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.orgpolicy_v2.types.ListConstraintsRequest):
                The initial request object.
            response (google.cloud.orgpolicy_v2.types.ListConstraintsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = orgpolicy.ListConstraintsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[orgpolicy.ListConstraintsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[constraint.Constraint]:
        async def async_generator():
            async for page in self.pages:
                for response in page.constraints:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPoliciesPager:
    """A pager for iterating through ``list_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.orgpolicy_v2.types.ListPoliciesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``policies`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPolicies`` requests and continue to iterate
    through the ``policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.orgpolicy_v2.types.ListPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., orgpolicy.ListPoliciesResponse],
        request: orgpolicy.ListPoliciesRequest,
        response: orgpolicy.ListPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.orgpolicy_v2.types.ListPoliciesRequest):
                The initial request object.
            response (google.cloud.orgpolicy_v2.types.ListPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = orgpolicy.ListPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[orgpolicy.ListPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[orgpolicy.Policy]:
        for page in self.pages:
            yield from page.policies

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPoliciesAsyncPager:
    """A pager for iterating through ``list_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.orgpolicy_v2.types.ListPoliciesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``policies`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPolicies`` requests and continue to iterate
    through the ``policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.orgpolicy_v2.types.ListPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[orgpolicy.ListPoliciesResponse]],
        request: orgpolicy.ListPoliciesRequest,
        response: orgpolicy.ListPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.orgpolicy_v2.types.ListPoliciesRequest):
                The initial request object.
            response (google.cloud.orgpolicy_v2.types.ListPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = orgpolicy.ListPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[orgpolicy.ListPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[orgpolicy.Policy]:
        async def async_generator():
            async for page in self.pages:
                for response in page.policies:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
