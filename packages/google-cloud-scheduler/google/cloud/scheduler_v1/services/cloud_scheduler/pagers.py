# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, Sequence, Tuple

from google.cloud.scheduler_v1.types import cloudscheduler
from google.cloud.scheduler_v1.types import job


class ListJobsPager:
    """A pager for iterating through ``list_jobs`` requests.

    This class thinly wraps an initial
    :class:`~.cloudscheduler.ListJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListJobs`` requests and continue to iterate
    through the ``jobs`` field on the
    corresponding responses.

    All the usual :class:`~.cloudscheduler.ListJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., cloudscheduler.ListJobsResponse],
        request: cloudscheduler.ListJobsRequest,
        response: cloudscheduler.ListJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.cloudscheduler.ListJobsRequest`):
                The initial request object.
            response (:class:`~.cloudscheduler.ListJobsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudscheduler.ListJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[cloudscheduler.ListJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[job.Job]:
        for page in self.pages:
            yield from page.jobs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListJobsAsyncPager:
    """A pager for iterating through ``list_jobs`` requests.

    This class thinly wraps an initial
    :class:`~.cloudscheduler.ListJobsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``jobs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListJobs`` requests and continue to iterate
    through the ``jobs`` field on the
    corresponding responses.

    All the usual :class:`~.cloudscheduler.ListJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[cloudscheduler.ListJobsResponse]],
        request: cloudscheduler.ListJobsRequest,
        response: cloudscheduler.ListJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.cloudscheduler.ListJobsRequest`):
                The initial request object.
            response (:class:`~.cloudscheduler.ListJobsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudscheduler.ListJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[cloudscheduler.ListJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[job.Job]:
        async def async_generator():
            async for page in self.pages:
                for response in page.jobs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
