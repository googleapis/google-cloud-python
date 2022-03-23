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
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.cloud.bare_metal_solution_v2.types import baremetalsolution


class ListInstancesPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListInstancesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListInstancesResponse],
        request: baremetalsolution.ListInstancesRequest,
        response: baremetalsolution.ListInstancesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListInstancesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.Instance]:
        for page in self.pages:
            yield from page.instances

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListInstancesAsyncPager:
    """A pager for iterating through ``list_instances`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListInstancesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``instances`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListInstances`` requests and continue to iterate
    through the ``instances`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListInstancesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[baremetalsolution.ListInstancesResponse]],
        request: baremetalsolution.ListInstancesRequest,
        response: baremetalsolution.ListInstancesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListInstancesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListInstancesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[baremetalsolution.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.Instance]:
        async def async_generator():
            async for page in self.pages:
                for response in page.instances:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVolumesPager:
    """A pager for iterating through ``list_volumes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListVolumesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``volumes`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVolumes`` requests and continue to iterate
    through the ``volumes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListVolumesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListVolumesResponse],
        request: baremetalsolution.ListVolumesRequest,
        response: baremetalsolution.ListVolumesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListVolumesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListVolumesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListVolumesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListVolumesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.Volume]:
        for page in self.pages:
            yield from page.volumes

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVolumesAsyncPager:
    """A pager for iterating through ``list_volumes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListVolumesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``volumes`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVolumes`` requests and continue to iterate
    through the ``volumes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListVolumesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[baremetalsolution.ListVolumesResponse]],
        request: baremetalsolution.ListVolumesRequest,
        response: baremetalsolution.ListVolumesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListVolumesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListVolumesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListVolumesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[baremetalsolution.ListVolumesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.Volume]:
        async def async_generator():
            async for page in self.pages:
                for response in page.volumes:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNetworksPager:
    """A pager for iterating through ``list_networks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListNetworksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``networks`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNetworks`` requests and continue to iterate
    through the ``networks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListNetworksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListNetworksResponse],
        request: baremetalsolution.ListNetworksRequest,
        response: baremetalsolution.ListNetworksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListNetworksRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListNetworksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.Network]:
        for page in self.pages:
            yield from page.networks

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNetworksAsyncPager:
    """A pager for iterating through ``list_networks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListNetworksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``networks`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNetworks`` requests and continue to iterate
    through the ``networks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListNetworksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[baremetalsolution.ListNetworksResponse]],
        request: baremetalsolution.ListNetworksRequest,
        response: baremetalsolution.ListNetworksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListNetworksRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListNetworksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[baremetalsolution.ListNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.Network]:
        async def async_generator():
            async for page in self.pages:
                for response in page.networks:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSnapshotSchedulePoliciesPager:
    """A pager for iterating through ``list_snapshot_schedule_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``snapshot_schedule_policies`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSnapshotSchedulePolicies`` requests and continue to iterate
    through the ``snapshot_schedule_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListSnapshotSchedulePoliciesResponse],
        request: baremetalsolution.ListSnapshotSchedulePoliciesRequest,
        response: baremetalsolution.ListSnapshotSchedulePoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListSnapshotSchedulePoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListSnapshotSchedulePoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.SnapshotSchedulePolicy]:
        for page in self.pages:
            yield from page.snapshot_schedule_policies

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSnapshotSchedulePoliciesAsyncPager:
    """A pager for iterating through ``list_snapshot_schedule_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``snapshot_schedule_policies`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSnapshotSchedulePolicies`` requests and continue to iterate
    through the ``snapshot_schedule_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[baremetalsolution.ListSnapshotSchedulePoliciesResponse]
        ],
        request: baremetalsolution.ListSnapshotSchedulePoliciesRequest,
        response: baremetalsolution.ListSnapshotSchedulePoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListSnapshotSchedulePoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[baremetalsolution.ListSnapshotSchedulePoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.SnapshotSchedulePolicy]:
        async def async_generator():
            async for page in self.pages:
                for response in page.snapshot_schedule_policies:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVolumeSnapshotsPager:
    """A pager for iterating through ``list_volume_snapshots`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``volume_snapshots`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVolumeSnapshots`` requests and continue to iterate
    through the ``volume_snapshots`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListVolumeSnapshotsResponse],
        request: baremetalsolution.ListVolumeSnapshotsRequest,
        response: baremetalsolution.ListVolumeSnapshotsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListVolumeSnapshotsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListVolumeSnapshotsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.VolumeSnapshot]:
        for page in self.pages:
            yield from page.volume_snapshots

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVolumeSnapshotsAsyncPager:
    """A pager for iterating through ``list_volume_snapshots`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``volume_snapshots`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVolumeSnapshots`` requests and continue to iterate
    through the ``volume_snapshots`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[baremetalsolution.ListVolumeSnapshotsResponse]],
        request: baremetalsolution.ListVolumeSnapshotsRequest,
        response: baremetalsolution.ListVolumeSnapshotsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListVolumeSnapshotsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[baremetalsolution.ListVolumeSnapshotsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.VolumeSnapshot]:
        async def async_generator():
            async for page in self.pages:
                for response in page.volume_snapshots:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLunsPager:
    """A pager for iterating through ``list_luns`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListLunsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``luns`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListLuns`` requests and continue to iterate
    through the ``luns`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListLunsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., baremetalsolution.ListLunsResponse],
        request: baremetalsolution.ListLunsRequest,
        response: baremetalsolution.ListLunsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListLunsRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListLunsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListLunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[baremetalsolution.ListLunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[baremetalsolution.Lun]:
        for page in self.pages:
            yield from page.luns

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLunsAsyncPager:
    """A pager for iterating through ``list_luns`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListLunsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``luns`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListLuns`` requests and continue to iterate
    through the ``luns`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListLunsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[baremetalsolution.ListLunsResponse]],
        request: baremetalsolution.ListLunsRequest,
        response: baremetalsolution.ListLunsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListLunsRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListLunsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = baremetalsolution.ListLunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[baremetalsolution.ListLunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[baremetalsolution.Lun]:
        async def async_generator():
            async for page in self.pages:
                for response in page.luns:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
