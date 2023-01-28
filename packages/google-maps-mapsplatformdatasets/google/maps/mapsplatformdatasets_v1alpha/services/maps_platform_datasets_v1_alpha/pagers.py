# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.maps.mapsplatformdatasets_v1alpha.types import (
    dataset,
    maps_platform_datasets,
)


class ListDatasetVersionsPager:
    """A pager for iterating through ``list_dataset_versions`` requests.

    This class thinly wraps an initial
    :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDatasetVersions`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., maps_platform_datasets.ListDatasetVersionsResponse],
        request: maps_platform_datasets.ListDatasetVersionsRequest,
        response: maps_platform_datasets.ListDatasetVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsRequest):
                The initial request object.
            response (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = maps_platform_datasets.ListDatasetVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[maps_platform_datasets.ListDatasetVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[dataset.Dataset]:
        for page in self.pages:
            yield from page.datasets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDatasetVersionsAsyncPager:
    """A pager for iterating through ``list_dataset_versions`` requests.

    This class thinly wraps an initial
    :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDatasetVersions`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[maps_platform_datasets.ListDatasetVersionsResponse]
        ],
        request: maps_platform_datasets.ListDatasetVersionsRequest,
        response: maps_platform_datasets.ListDatasetVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsRequest):
                The initial request object.
            response (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = maps_platform_datasets.ListDatasetVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[maps_platform_datasets.ListDatasetVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[dataset.Dataset]:
        async def async_generator():
            async for page in self.pages:
                for response in page.datasets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDatasetsPager:
    """A pager for iterating through ``list_datasets`` requests.

    This class thinly wraps an initial
    :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDatasets`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., maps_platform_datasets.ListDatasetsResponse],
        request: maps_platform_datasets.ListDatasetsRequest,
        response: maps_platform_datasets.ListDatasetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsRequest):
                The initial request object.
            response (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = maps_platform_datasets.ListDatasetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[maps_platform_datasets.ListDatasetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[dataset.Dataset]:
        for page in self.pages:
            yield from page.datasets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDatasetsAsyncPager:
    """A pager for iterating through ``list_datasets`` requests.

    This class thinly wraps an initial
    :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDatasets`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[maps_platform_datasets.ListDatasetsResponse]],
        request: maps_platform_datasets.ListDatasetsRequest,
        response: maps_platform_datasets.ListDatasetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsRequest):
                The initial request object.
            response (google.maps.mapsplatformdatasets_v1alpha.types.ListDatasetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = maps_platform_datasets.ListDatasetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[maps_platform_datasets.ListDatasetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[dataset.Dataset]:
        async def async_generator():
            async for page in self.pages:
                for response in page.datasets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
