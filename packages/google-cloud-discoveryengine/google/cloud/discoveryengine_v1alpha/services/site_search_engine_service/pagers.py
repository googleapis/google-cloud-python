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

from google.cloud.discoveryengine_v1alpha.types import (
    site_search_engine,
    site_search_engine_service,
)


class ListTargetSitesPager:
    """A pager for iterating through ``list_target_sites`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``target_sites`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTargetSites`` requests and continue to iterate
    through the ``target_sites`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., site_search_engine_service.ListTargetSitesResponse],
        request: site_search_engine_service.ListTargetSitesRequest,
        response: site_search_engine_service.ListTargetSitesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1alpha.types.ListTargetSitesRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = site_search_engine_service.ListTargetSitesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[site_search_engine_service.ListTargetSitesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[site_search_engine.TargetSite]:
        for page in self.pages:
            yield from page.target_sites

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTargetSitesAsyncPager:
    """A pager for iterating through ``list_target_sites`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``target_sites`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTargetSites`` requests and continue to iterate
    through the ``target_sites`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[site_search_engine_service.ListTargetSitesResponse]
        ],
        request: site_search_engine_service.ListTargetSitesRequest,
        response: site_search_engine_service.ListTargetSitesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1alpha.types.ListTargetSitesRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1alpha.types.ListTargetSitesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = site_search_engine_service.ListTargetSitesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[site_search_engine_service.ListTargetSitesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[site_search_engine.TargetSite]:
        async def async_generator():
            async for page in self.pages:
                for response in page.target_sites:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class FetchDomainVerificationStatusPager:
    """A pager for iterating through ``fetch_domain_verification_status`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``target_sites`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``FetchDomainVerificationStatus`` requests and continue to iterate
    through the ``target_sites`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., site_search_engine_service.FetchDomainVerificationStatusResponse
        ],
        request: site_search_engine_service.FetchDomainVerificationStatusRequest,
        response: site_search_engine_service.FetchDomainVerificationStatusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = site_search_engine_service.FetchDomainVerificationStatusRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[site_search_engine_service.FetchDomainVerificationStatusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[site_search_engine.TargetSite]:
        for page in self.pages:
            yield from page.target_sites

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class FetchDomainVerificationStatusAsyncPager:
    """A pager for iterating through ``fetch_domain_verification_status`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``target_sites`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``FetchDomainVerificationStatus`` requests and continue to iterate
    through the ``target_sites`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[site_search_engine_service.FetchDomainVerificationStatusResponse],
        ],
        request: site_search_engine_service.FetchDomainVerificationStatusRequest,
        response: site_search_engine_service.FetchDomainVerificationStatusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusRequest):
                The initial request object.
            response (google.cloud.discoveryengine_v1alpha.types.FetchDomainVerificationStatusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = site_search_engine_service.FetchDomainVerificationStatusRequest(
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
        site_search_engine_service.FetchDomainVerificationStatusResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[site_search_engine.TargetSite]:
        async def async_generator():
            async for page in self.pages:
                for response in page.target_sites:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
