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

from google.cloud.dialogflowcx_v3beta1.types import version


class ListVersionsPager:
    """A pager for iterating through ``list_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVersions`` requests and continue to iterate
    through the ``versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., version.ListVersionsResponse],
        request: version.ListVersionsRequest,
        response: version.ListVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListVersionsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = version.ListVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[version.ListVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[version.Version]:
        for page in self.pages:
            yield from page.versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVersionsAsyncPager:
    """A pager for iterating through ``list_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``versions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVersions`` requests and continue to iterate
    through the ``versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[version.ListVersionsResponse]],
        request: version.ListVersionsRequest,
        response: version.ListVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.dialogflowcx_v3beta1.types.ListVersionsRequest):
                The initial request object.
            response (google.cloud.dialogflowcx_v3beta1.types.ListVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = version.ListVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[version.ListVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[version.Version]:
        async def async_generator():
            async for page in self.pages:
                for response in page.versions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
