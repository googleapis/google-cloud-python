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
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.api import monitored_resource_pb2  # type: ignore
from google.cloud.monitoring_v3.types import group
from google.cloud.monitoring_v3.types import group_service


class ListGroupsPager:
    """A pager for iterating through ``list_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListGroupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``group`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGroups`` requests and continue to iterate
    through the ``group`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., group_service.ListGroupsResponse],
        request: group_service.ListGroupsRequest,
        response: group_service.ListGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListGroupsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = group_service.ListGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[group_service.ListGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[group.Group]:
        for page in self.pages:
            yield from page.group

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGroupsAsyncPager:
    """A pager for iterating through ``list_groups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListGroupsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``group`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListGroups`` requests and continue to iterate
    through the ``group`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListGroupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[group_service.ListGroupsResponse]],
        request: group_service.ListGroupsRequest,
        response: group_service.ListGroupsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListGroupsRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListGroupsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = group_service.ListGroupsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[group_service.ListGroupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[group.Group]:
        async def async_generator():
            async for page in self.pages:
                for response in page.group:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGroupMembersPager:
    """A pager for iterating through ``list_group_members`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListGroupMembersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``members`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGroupMembers`` requests and continue to iterate
    through the ``members`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListGroupMembersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., group_service.ListGroupMembersResponse],
        request: group_service.ListGroupMembersRequest,
        response: group_service.ListGroupMembersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListGroupMembersRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListGroupMembersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = group_service.ListGroupMembersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[group_service.ListGroupMembersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[monitored_resource_pb2.MonitoredResource]:
        for page in self.pages:
            yield from page.members

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGroupMembersAsyncPager:
    """A pager for iterating through ``list_group_members`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListGroupMembersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``members`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListGroupMembers`` requests and continue to iterate
    through the ``members`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListGroupMembersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[group_service.ListGroupMembersResponse]],
        request: group_service.ListGroupMembersRequest,
        response: group_service.ListGroupMembersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListGroupMembersRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListGroupMembersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = group_service.ListGroupMembersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[group_service.ListGroupMembersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[monitored_resource_pb2.MonitoredResource]:
        async def async_generator():
            async for page in self.pages:
                for response in page.members:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
