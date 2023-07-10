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

from google.cloud.securitycenter_v1.types import (
    bigquery_export,
    effective_security_health_analytics_custom_module,
    mute_config,
    notification_config,
    security_health_analytics_custom_module,
    securitycenter_service,
    source,
)


class GroupAssetsPager:
    """A pager for iterating through ``group_assets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.GroupAssetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``group_by_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``GroupAssets`` requests and continue to iterate
    through the ``group_by_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.GroupAssetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.GroupAssetsResponse],
        request: securitycenter_service.GroupAssetsRequest,
        response: securitycenter_service.GroupAssetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.GroupAssetsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.GroupAssetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.GroupAssetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.GroupAssetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securitycenter_service.GroupResult]:
        for page in self.pages:
            yield from page.group_by_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class GroupAssetsAsyncPager:
    """A pager for iterating through ``group_assets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.GroupAssetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``group_by_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``GroupAssets`` requests and continue to iterate
    through the ``group_by_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.GroupAssetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[securitycenter_service.GroupAssetsResponse]],
        request: securitycenter_service.GroupAssetsRequest,
        response: securitycenter_service.GroupAssetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.GroupAssetsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.GroupAssetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.GroupAssetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securitycenter_service.GroupAssetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[securitycenter_service.GroupResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.group_by_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class GroupFindingsPager:
    """A pager for iterating through ``group_findings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.GroupFindingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``group_by_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``GroupFindings`` requests and continue to iterate
    through the ``group_by_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.GroupFindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.GroupFindingsResponse],
        request: securitycenter_service.GroupFindingsRequest,
        response: securitycenter_service.GroupFindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.GroupFindingsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.GroupFindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.GroupFindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.GroupFindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securitycenter_service.GroupResult]:
        for page in self.pages:
            yield from page.group_by_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class GroupFindingsAsyncPager:
    """A pager for iterating through ``group_findings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.GroupFindingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``group_by_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``GroupFindings`` requests and continue to iterate
    through the ``group_by_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.GroupFindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[securitycenter_service.GroupFindingsResponse]],
        request: securitycenter_service.GroupFindingsRequest,
        response: securitycenter_service.GroupFindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.GroupFindingsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.GroupFindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.GroupFindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[securitycenter_service.GroupFindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[securitycenter_service.GroupResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.group_by_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAssetsPager:
    """A pager for iterating through ``list_assets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListAssetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``list_assets_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAssets`` requests and continue to iterate
    through the ``list_assets_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListAssetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListAssetsResponse],
        request: securitycenter_service.ListAssetsRequest,
        response: securitycenter_service.ListAssetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListAssetsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListAssetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListAssetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListAssetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[securitycenter_service.ListAssetsResponse.ListAssetsResult]:
        for page in self.pages:
            yield from page.list_assets_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAssetsAsyncPager:
    """A pager for iterating through ``list_assets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListAssetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``list_assets_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAssets`` requests and continue to iterate
    through the ``list_assets_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListAssetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[securitycenter_service.ListAssetsResponse]],
        request: securitycenter_service.ListAssetsRequest,
        response: securitycenter_service.ListAssetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListAssetsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListAssetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListAssetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securitycenter_service.ListAssetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[securitycenter_service.ListAssetsResponse.ListAssetsResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.list_assets_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDescendantSecurityHealthAnalyticsCustomModulesPager:
    """A pager for iterating through ``list_descendant_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDescendantSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
        ],
        request: securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[
        securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[
        security_health_analytics_custom_module.SecurityHealthAnalyticsCustomModule
    ]:
        for page in self.pages:
            yield from page.security_health_analytics_custom_modules

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDescendantSecurityHealthAnalyticsCustomModulesAsyncPager:
    """A pager for iterating through ``list_descendant_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDescendantSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[
                securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse
            ],
        ],
        request: securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListDescendantSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
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
        securitycenter_service.ListDescendantSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[
        security_health_analytics_custom_module.SecurityHealthAnalyticsCustomModule
    ]:
        async def async_generator():
            async for page in self.pages:
                for response in page.security_health_analytics_custom_modules:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListFindingsPager:
    """A pager for iterating through ``list_findings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListFindingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``list_findings_results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListFindings`` requests and continue to iterate
    through the ``list_findings_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListFindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListFindingsResponse],
        request: securitycenter_service.ListFindingsRequest,
        response: securitycenter_service.ListFindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListFindingsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListFindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListFindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListFindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[securitycenter_service.ListFindingsResponse.ListFindingsResult]:
        for page in self.pages:
            yield from page.list_findings_results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListFindingsAsyncPager:
    """A pager for iterating through ``list_findings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListFindingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``list_findings_results`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListFindings`` requests and continue to iterate
    through the ``list_findings_results`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListFindingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[securitycenter_service.ListFindingsResponse]],
        request: securitycenter_service.ListFindingsRequest,
        response: securitycenter_service.ListFindingsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListFindingsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListFindingsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListFindingsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securitycenter_service.ListFindingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[securitycenter_service.ListFindingsResponse.ListFindingsResult]:
        async def async_generator():
            async for page in self.pages:
                for response in page.list_findings_results:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMuteConfigsPager:
    """A pager for iterating through ``list_mute_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListMuteConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``mute_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListMuteConfigs`` requests and continue to iterate
    through the ``mute_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListMuteConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListMuteConfigsResponse],
        request: securitycenter_service.ListMuteConfigsRequest,
        response: securitycenter_service.ListMuteConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListMuteConfigsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListMuteConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListMuteConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListMuteConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[mute_config.MuteConfig]:
        for page in self.pages:
            yield from page.mute_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListMuteConfigsAsyncPager:
    """A pager for iterating through ``list_mute_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListMuteConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``mute_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListMuteConfigs`` requests and continue to iterate
    through the ``mute_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListMuteConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[securitycenter_service.ListMuteConfigsResponse]
        ],
        request: securitycenter_service.ListMuteConfigsRequest,
        response: securitycenter_service.ListMuteConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListMuteConfigsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListMuteConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListMuteConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[securitycenter_service.ListMuteConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[mute_config.MuteConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.mute_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNotificationConfigsPager:
    """A pager for iterating through ``list_notification_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``notification_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNotificationConfigs`` requests and continue to iterate
    through the ``notification_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListNotificationConfigsResponse],
        request: securitycenter_service.ListNotificationConfigsRequest,
        response: securitycenter_service.ListNotificationConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListNotificationConfigsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListNotificationConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListNotificationConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[notification_config.NotificationConfig]:
        for page in self.pages:
            yield from page.notification_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNotificationConfigsAsyncPager:
    """A pager for iterating through ``list_notification_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``notification_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNotificationConfigs`` requests and continue to iterate
    through the ``notification_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[securitycenter_service.ListNotificationConfigsResponse]
        ],
        request: securitycenter_service.ListNotificationConfigsRequest,
        response: securitycenter_service.ListNotificationConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListNotificationConfigsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListNotificationConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListNotificationConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[securitycenter_service.ListNotificationConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[notification_config.NotificationConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.notification_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEffectiveSecurityHealthAnalyticsCustomModulesPager:
    """A pager for iterating through ``list_effective_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``effective_security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEffectiveSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``effective_security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
        ],
        request: securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
            request
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[
        securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[
        effective_security_health_analytics_custom_module.EffectiveSecurityHealthAnalyticsCustomModule
    ]:
        for page in self.pages:
            yield from page.effective_security_health_analytics_custom_modules

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEffectiveSecurityHealthAnalyticsCustomModulesAsyncPager:
    """A pager for iterating through ``list_effective_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``effective_security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEffectiveSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``effective_security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[
                securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse
            ],
        ],
        request: securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
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
        securitycenter_service.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[
        effective_security_health_analytics_custom_module.EffectiveSecurityHealthAnalyticsCustomModule
    ]:
        async def async_generator():
            async for page in self.pages:
                for response in page.effective_security_health_analytics_custom_modules:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSecurityHealthAnalyticsCustomModulesPager:
    """A pager for iterating through ``list_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse
        ],
        request: securitycenter_service.ListSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = (
            securitycenter_service.ListSecurityHealthAnalyticsCustomModulesRequest(
                request
            )
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[
        securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[
        security_health_analytics_custom_module.SecurityHealthAnalyticsCustomModule
    ]:
        for page in self.pages:
            yield from page.security_health_analytics_custom_modules

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSecurityHealthAnalyticsCustomModulesAsyncPager:
    """A pager for iterating through ``list_security_health_analytics_custom_modules`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``security_health_analytics_custom_modules`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSecurityHealthAnalyticsCustomModules`` requests and continue to iterate
    through the ``security_health_analytics_custom_modules`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ...,
            Awaitable[
                securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse
            ],
        ],
        request: securitycenter_service.ListSecurityHealthAnalyticsCustomModulesRequest,
        response: securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListSecurityHealthAnalyticsCustomModulesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = (
            securitycenter_service.ListSecurityHealthAnalyticsCustomModulesRequest(
                request
            )
        )
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[
        securitycenter_service.ListSecurityHealthAnalyticsCustomModulesResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[
        security_health_analytics_custom_module.SecurityHealthAnalyticsCustomModule
    ]:
        async def async_generator():
            async for page in self.pages:
                for response in page.security_health_analytics_custom_modules:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSourcesPager:
    """A pager for iterating through ``list_sources`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListSourcesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``sources`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSources`` requests and continue to iterate
    through the ``sources`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListSourcesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListSourcesResponse],
        request: securitycenter_service.ListSourcesRequest,
        response: securitycenter_service.ListSourcesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListSourcesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListSourcesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListSourcesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListSourcesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[source.Source]:
        for page in self.pages:
            yield from page.sources

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSourcesAsyncPager:
    """A pager for iterating through ``list_sources`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListSourcesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``sources`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSources`` requests and continue to iterate
    through the ``sources`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListSourcesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[securitycenter_service.ListSourcesResponse]],
        request: securitycenter_service.ListSourcesRequest,
        response: securitycenter_service.ListSourcesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListSourcesRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListSourcesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListSourcesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securitycenter_service.ListSourcesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[source.Source]:
        async def async_generator():
            async for page in self.pages:
                for response in page.sources:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBigQueryExportsPager:
    """A pager for iterating through ``list_big_query_exports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``big_query_exports`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListBigQueryExports`` requests and continue to iterate
    through the ``big_query_exports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., securitycenter_service.ListBigQueryExportsResponse],
        request: securitycenter_service.ListBigQueryExportsRequest,
        response: securitycenter_service.ListBigQueryExportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListBigQueryExportsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListBigQueryExportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securitycenter_service.ListBigQueryExportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[bigquery_export.BigQueryExport]:
        for page in self.pages:
            yield from page.big_query_exports

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListBigQueryExportsAsyncPager:
    """A pager for iterating through ``list_big_query_exports`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``big_query_exports`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListBigQueryExports`` requests and continue to iterate
    through the ``big_query_exports`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[securitycenter_service.ListBigQueryExportsResponse]
        ],
        request: securitycenter_service.ListBigQueryExportsRequest,
        response: securitycenter_service.ListBigQueryExportsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securitycenter_v1.types.ListBigQueryExportsRequest):
                The initial request object.
            response (google.cloud.securitycenter_v1.types.ListBigQueryExportsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securitycenter_service.ListBigQueryExportsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[securitycenter_service.ListBigQueryExportsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[bigquery_export.BigQueryExport]:
        async def async_generator():
            async for page in self.pages:
                for response in page.big_query_exports:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
