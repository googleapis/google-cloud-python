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

from google.cloud.managedkafka_v1.types import managed_kafka, resources


class ListClustersPager:
    """A pager for iterating through ``list_clusters`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListClustersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``clusters`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListClusters`` requests and continue to iterate
    through the ``clusters`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListClustersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., managed_kafka.ListClustersResponse],
        request: managed_kafka.ListClustersRequest,
        response: managed_kafka.ListClustersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListClustersRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListClustersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListClustersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[managed_kafka.ListClustersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Cluster]:
        for page in self.pages:
            yield from page.clusters

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListClustersAsyncPager:
    """A pager for iterating through ``list_clusters`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListClustersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``clusters`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListClusters`` requests and continue to iterate
    through the ``clusters`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListClustersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[managed_kafka.ListClustersResponse]],
        request: managed_kafka.ListClustersRequest,
        response: managed_kafka.ListClustersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListClustersRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListClustersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListClustersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[managed_kafka.ListClustersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Cluster]:
        async def async_generator():
            async for page in self.pages:
                for response in page.clusters:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTopicsPager:
    """A pager for iterating through ``list_topics`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListTopicsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``topics`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTopics`` requests and continue to iterate
    through the ``topics`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListTopicsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., managed_kafka.ListTopicsResponse],
        request: managed_kafka.ListTopicsRequest,
        response: managed_kafka.ListTopicsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListTopicsRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListTopicsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListTopicsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[managed_kafka.ListTopicsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.Topic]:
        for page in self.pages:
            yield from page.topics

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTopicsAsyncPager:
    """A pager for iterating through ``list_topics`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListTopicsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``topics`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTopics`` requests and continue to iterate
    through the ``topics`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListTopicsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[managed_kafka.ListTopicsResponse]],
        request: managed_kafka.ListTopicsRequest,
        response: managed_kafka.ListTopicsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListTopicsRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListTopicsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListTopicsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[managed_kafka.ListTopicsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.Topic]:
        async def async_generator():
            async for page in self.pages:
                for response in page.topics:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConsumerGroupsPager:
    """A pager for iterating through ``list_consumer_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``consumer_groups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListConsumerGroups`` requests and continue to iterate
    through the ``consumer_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., managed_kafka.ListConsumerGroupsResponse],
        request: managed_kafka.ListConsumerGroupsRequest,
        response: managed_kafka.ListConsumerGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListConsumerGroupsRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListConsumerGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[managed_kafka.ListConsumerGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.ConsumerGroup]:
        for page in self.pages:
            yield from page.consumer_groups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListConsumerGroupsAsyncPager:
    """A pager for iterating through ``list_consumer_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``consumer_groups`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListConsumerGroups`` requests and continue to iterate
    through the ``consumer_groups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[managed_kafka.ListConsumerGroupsResponse]],
        request: managed_kafka.ListConsumerGroupsRequest,
        response: managed_kafka.ListConsumerGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.managedkafka_v1.types.ListConsumerGroupsRequest):
                The initial request object.
            response (google.cloud.managedkafka_v1.types.ListConsumerGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = managed_kafka.ListConsumerGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[managed_kafka.ListConsumerGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.ConsumerGroup]:
        async def async_generator():
            async for page in self.pages:
                for response in page.consumer_groups:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
