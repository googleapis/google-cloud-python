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

from google.cloud.managedidentities_v1.types import managed_identities_service, resource


class ListDomainsPager:
    """A pager for iterating through ``list_domains`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedidentities_v1.types.ListDomainsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``domains`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDomains`` requests and continue to iterate
    through the ``domains`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedidentities_v1.types.ListDomainsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., managed_identities_service.ListDomainsResponse],
        request: managed_identities_service.ListDomainsRequest,
        response: managed_identities_service.ListDomainsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedidentities_v1.types.ListDomainsRequest):
                The initial request object.
            response (google.cloud.managedidentities_v1.types.ListDomainsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_identities_service.ListDomainsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[managed_identities_service.ListDomainsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resource.Domain]:
        for page in self.pages:
            yield from page.domains

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDomainsAsyncPager:
    """A pager for iterating through ``list_domains`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedidentities_v1.types.ListDomainsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``domains`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDomains`` requests and continue to iterate
    through the ``domains`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedidentities_v1.types.ListDomainsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[managed_identities_service.ListDomainsResponse]
        ],
        request: managed_identities_service.ListDomainsRequest,
        response: managed_identities_service.ListDomainsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedidentities_v1.types.ListDomainsRequest):
                The initial request object.
            response (google.cloud.managedidentities_v1.types.ListDomainsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_identities_service.ListDomainsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[managed_identities_service.ListDomainsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resource.Domain]:
        async def async_generator():
            async for page in self.pages:
                for response in page.domains:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
