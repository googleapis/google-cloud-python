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

from google.cloud.vmwareengine_v1.types import vmwareengine, vmwareengine_resources


class ListPrivateCloudsPager:
    """A pager for iterating through ``list_private_clouds`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``private_clouds`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPrivateClouds`` requests and continue to iterate
    through the ``private_clouds`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListPrivateCloudsResponse],
        request: vmwareengine.ListPrivateCloudsRequest,
        response: vmwareengine.ListPrivateCloudsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateCloudsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateCloudsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListPrivateCloudsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.PrivateCloud]:
        for page in self.pages:
            yield from page.private_clouds

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPrivateCloudsAsyncPager:
    """A pager for iterating through ``list_private_clouds`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``private_clouds`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPrivateClouds`` requests and continue to iterate
    through the ``private_clouds`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListPrivateCloudsResponse]],
        request: vmwareengine.ListPrivateCloudsRequest,
        response: vmwareengine.ListPrivateCloudsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateCloudsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateCloudsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateCloudsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListPrivateCloudsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.PrivateCloud]:
        async def async_generator():
            async for page in self.pages:
                for response in page.private_clouds:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListClustersPager:
    """A pager for iterating through ``list_clusters`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListClustersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``clusters`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListClusters`` requests and continue to iterate
    through the ``clusters`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListClustersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListClustersResponse],
        request: vmwareengine.ListClustersRequest,
        response: vmwareengine.ListClustersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListClustersRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListClustersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListClustersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListClustersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.Cluster]:
        for page in self.pages:
            yield from page.clusters

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListClustersAsyncPager:
    """A pager for iterating through ``list_clusters`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListClustersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``clusters`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListClusters`` requests and continue to iterate
    through the ``clusters`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListClustersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListClustersResponse]],
        request: vmwareengine.ListClustersRequest,
        response: vmwareengine.ListClustersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListClustersRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListClustersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListClustersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListClustersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.Cluster]:
        async def async_generator():
            async for page in self.pages:
                for response in page.clusters:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubnetsPager:
    """A pager for iterating through ``list_subnets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListSubnetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``subnets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSubnets`` requests and continue to iterate
    through the ``subnets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListSubnetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListSubnetsResponse],
        request: vmwareengine.ListSubnetsRequest,
        response: vmwareengine.ListSubnetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListSubnetsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListSubnetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListSubnetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListSubnetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.Subnet]:
        for page in self.pages:
            yield from page.subnets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubnetsAsyncPager:
    """A pager for iterating through ``list_subnets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListSubnetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``subnets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSubnets`` requests and continue to iterate
    through the ``subnets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListSubnetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListSubnetsResponse]],
        request: vmwareengine.ListSubnetsRequest,
        response: vmwareengine.ListSubnetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListSubnetsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListSubnetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListSubnetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListSubnetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.Subnet]:
        async def async_generator():
            async for page in self.pages:
                for response in page.subnets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNodeTypesPager:
    """A pager for iterating through ``list_node_types`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListNodeTypesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``node_types`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNodeTypes`` requests and continue to iterate
    through the ``node_types`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListNodeTypesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListNodeTypesResponse],
        request: vmwareengine.ListNodeTypesRequest,
        response: vmwareengine.ListNodeTypesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListNodeTypesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListNodeTypesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListNodeTypesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListNodeTypesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.NodeType]:
        for page in self.pages:
            yield from page.node_types

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNodeTypesAsyncPager:
    """A pager for iterating through ``list_node_types`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListNodeTypesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``node_types`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNodeTypes`` requests and continue to iterate
    through the ``node_types`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListNodeTypesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListNodeTypesResponse]],
        request: vmwareengine.ListNodeTypesRequest,
        response: vmwareengine.ListNodeTypesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListNodeTypesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListNodeTypesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListNodeTypesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListNodeTypesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.NodeType]:
        async def async_generator():
            async for page in self.pages:
                for response in page.node_types:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListHcxActivationKeysPager:
    """A pager for iterating through ``list_hcx_activation_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``hcx_activation_keys`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListHcxActivationKeys`` requests and continue to iterate
    through the ``hcx_activation_keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListHcxActivationKeysResponse],
        request: vmwareengine.ListHcxActivationKeysRequest,
        response: vmwareengine.ListHcxActivationKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListHcxActivationKeysRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListHcxActivationKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListHcxActivationKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.HcxActivationKey]:
        for page in self.pages:
            yield from page.hcx_activation_keys

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListHcxActivationKeysAsyncPager:
    """A pager for iterating through ``list_hcx_activation_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``hcx_activation_keys`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListHcxActivationKeys`` requests and continue to iterate
    through the ``hcx_activation_keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListHcxActivationKeysResponse]],
        request: vmwareengine.ListHcxActivationKeysRequest,
        response: vmwareengine.ListHcxActivationKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListHcxActivationKeysRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListHcxActivationKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListHcxActivationKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListHcxActivationKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.HcxActivationKey]:
        async def async_generator():
            async for page in self.pages:
                for response in page.hcx_activation_keys:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNetworkPoliciesPager:
    """A pager for iterating through ``list_network_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``network_policies`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNetworkPolicies`` requests and continue to iterate
    through the ``network_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListNetworkPoliciesResponse],
        request: vmwareengine.ListNetworkPoliciesRequest,
        response: vmwareengine.ListNetworkPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListNetworkPoliciesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListNetworkPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListNetworkPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.NetworkPolicy]:
        for page in self.pages:
            yield from page.network_policies

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListNetworkPoliciesAsyncPager:
    """A pager for iterating through ``list_network_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``network_policies`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListNetworkPolicies`` requests and continue to iterate
    through the ``network_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListNetworkPoliciesResponse]],
        request: vmwareengine.ListNetworkPoliciesRequest,
        response: vmwareengine.ListNetworkPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListNetworkPoliciesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListNetworkPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListNetworkPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListNetworkPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.NetworkPolicy]:
        async def async_generator():
            async for page in self.pages:
                for response in page.network_policies:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVmwareEngineNetworksPager:
    """A pager for iterating through ``list_vmware_engine_networks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``vmware_engine_networks`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVmwareEngineNetworks`` requests and continue to iterate
    through the ``vmware_engine_networks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListVmwareEngineNetworksResponse],
        request: vmwareengine.ListVmwareEngineNetworksRequest,
        response: vmwareengine.ListVmwareEngineNetworksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListVmwareEngineNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListVmwareEngineNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.VmwareEngineNetwork]:
        for page in self.pages:
            yield from page.vmware_engine_networks

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVmwareEngineNetworksAsyncPager:
    """A pager for iterating through ``list_vmware_engine_networks`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``vmware_engine_networks`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVmwareEngineNetworks`` requests and continue to iterate
    through the ``vmware_engine_networks`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListVmwareEngineNetworksResponse]],
        request: vmwareengine.ListVmwareEngineNetworksRequest,
        response: vmwareengine.ListVmwareEngineNetworksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListVmwareEngineNetworksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListVmwareEngineNetworksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[vmwareengine.ListVmwareEngineNetworksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.VmwareEngineNetwork]:
        async def async_generator():
            async for page in self.pages:
                for response in page.vmware_engine_networks:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPrivateConnectionsPager:
    """A pager for iterating through ``list_private_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``private_connections`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPrivateConnections`` requests and continue to iterate
    through the ``private_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListPrivateConnectionsResponse],
        request: vmwareengine.ListPrivateConnectionsRequest,
        response: vmwareengine.ListPrivateConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateConnectionsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[vmwareengine.ListPrivateConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.PrivateConnection]:
        for page in self.pages:
            yield from page.private_connections

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPrivateConnectionsAsyncPager:
    """A pager for iterating through ``list_private_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``private_connections`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPrivateConnections`` requests and continue to iterate
    through the ``private_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[vmwareengine.ListPrivateConnectionsResponse]],
        request: vmwareengine.ListPrivateConnectionsRequest,
        response: vmwareengine.ListPrivateConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateConnectionsRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[vmwareengine.ListPrivateConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.PrivateConnection]:
        async def async_generator():
            async for page in self.pages:
                for response in page.private_connections:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPrivateConnectionPeeringRoutesPager:
    """A pager for iterating through ``list_private_connection_peering_routes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``peering_routes`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPrivateConnectionPeeringRoutes`` requests and continue to iterate
    through the ``peering_routes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., vmwareengine.ListPrivateConnectionPeeringRoutesResponse],
        request: vmwareengine.ListPrivateConnectionPeeringRoutesRequest,
        response: vmwareengine.ListPrivateConnectionPeeringRoutesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateConnectionPeeringRoutesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[vmwareengine.ListPrivateConnectionPeeringRoutesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[vmwareengine_resources.PeeringRoute]:
        for page in self.pages:
            yield from page.peering_routes

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPrivateConnectionPeeringRoutesAsyncPager:
    """A pager for iterating through ``list_private_connection_peering_routes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``peering_routes`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPrivateConnectionPeeringRoutes`` requests and continue to iterate
    through the ``peering_routes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[vmwareengine.ListPrivateConnectionPeeringRoutesResponse]
        ],
        request: vmwareengine.ListPrivateConnectionPeeringRoutesRequest,
        response: vmwareengine.ListPrivateConnectionPeeringRoutesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesRequest):
                The initial request object.
            response (google.cloud.vmwareengine_v1.types.ListPrivateConnectionPeeringRoutesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = vmwareengine.ListPrivateConnectionPeeringRoutesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[vmwareengine.ListPrivateConnectionPeeringRoutesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[vmwareengine_resources.PeeringRoute]:
        async def async_generator():
            async for page in self.pages:
                for response in page.peering_routes:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
