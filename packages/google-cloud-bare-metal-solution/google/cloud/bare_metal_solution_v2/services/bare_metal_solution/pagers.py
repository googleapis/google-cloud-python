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

from google.cloud.bare_metal_solution_v2.types import instance
from google.cloud.bare_metal_solution_v2.types import lun
from google.cloud.bare_metal_solution_v2.types import network
from google.cloud.bare_metal_solution_v2.types import nfs_share
from google.cloud.bare_metal_solution_v2.types import volume


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
        method: Callable[..., instance.ListInstancesResponse],
        request: instance.ListInstancesRequest,
        response: instance.ListInstancesResponse,
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
        self._request = instance.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[instance.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[instance.Instance]:
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
        method: Callable[..., Awaitable[instance.ListInstancesResponse]],
        request: instance.ListInstancesRequest,
        response: instance.ListInstancesResponse,
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
        self._request = instance.ListInstancesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[instance.ListInstancesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[instance.Instance]:
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
        method: Callable[..., volume.ListVolumesResponse],
        request: volume.ListVolumesRequest,
        response: volume.ListVolumesResponse,
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
        self._request = volume.ListVolumesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[volume.ListVolumesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[volume.Volume]:
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
        method: Callable[..., Awaitable[volume.ListVolumesResponse]],
        request: volume.ListVolumesRequest,
        response: volume.ListVolumesResponse,
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
        self._request = volume.ListVolumesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[volume.ListVolumesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[volume.Volume]:
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
        method: Callable[..., network.ListNetworksResponse],
        request: network.ListNetworksRequest,
        response: network.ListNetworksResponse,
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
        self._request = network.ListNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[network.ListNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[network.Network]:
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
        method: Callable[..., Awaitable[network.ListNetworksResponse]],
        request: network.ListNetworksRequest,
        response: network.ListNetworksResponse,
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
        self._request = network.ListNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[network.ListNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[network.Network]:
        async def async_generator():
            async for page in self.pages:
                for response in page.networks:
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
        method: Callable[..., lun.ListLunsResponse],
        request: lun.ListLunsRequest,
        response: lun.ListLunsResponse,
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
        self._request = lun.ListLunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[lun.ListLunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[lun.Lun]:
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
        method: Callable[..., Awaitable[lun.ListLunsResponse]],
        request: lun.ListLunsRequest,
        response: lun.ListLunsResponse,
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
        self._request = lun.ListLunsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[lun.ListLunsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[lun.Lun]:
        async def async_generator():
            async for page in self.pages:
                for response in page.luns:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNfsSharesPager:
    """A pager for iterating through ``list_nfs_shares`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``nfs_shares`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNfsShares`` requests and continue to iterate
    through the ``nfs_shares`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., nfs_share.ListNfsSharesResponse],
        request: nfs_share.ListNfsSharesRequest,
        response: nfs_share.ListNfsSharesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListNfsSharesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = nfs_share.ListNfsSharesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[nfs_share.ListNfsSharesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[nfs_share.NfsShare]:
        for page in self.pages:
            yield from page.nfs_shares

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNfsSharesAsyncPager:
    """A pager for iterating through ``list_nfs_shares`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``nfs_shares`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNfsShares`` requests and continue to iterate
    through the ``nfs_shares`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[nfs_share.ListNfsSharesResponse]],
        request: nfs_share.ListNfsSharesRequest,
        response: nfs_share.ListNfsSharesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.bare_metal_solution_v2.types.ListNfsSharesRequest):
                The initial request object.
            response (google.cloud.bare_metal_solution_v2.types.ListNfsSharesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = nfs_share.ListNfsSharesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[nfs_share.ListNfsSharesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[nfs_share.NfsShare]:
        async def async_generator():
            async for page in self.pages:
                for response in page.nfs_shares:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
