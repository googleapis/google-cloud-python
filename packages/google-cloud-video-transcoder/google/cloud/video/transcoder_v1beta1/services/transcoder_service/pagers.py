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
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    Sequence,
    Tuple,
    Optional,
)

from google.cloud.video.transcoder_v1beta1.types import resources
from google.cloud.video.transcoder_v1beta1.types import services


class ListJobsPager:
    """A pager for iterating through ``list_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.transcoder_v1beta1.types.ListJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListJobs`` requests and continue to iterate
    through the ``jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.transcoder_v1beta1.types.ListJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., services.ListJobsResponse],
        request: services.ListJobsRequest,
        response: services.ListJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.transcoder_v1beta1.types.ListJobsRequest):
                The initial request object.
            response (google.cloud.video.transcoder_v1beta1.types.ListJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = services.ListJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[services.ListJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.Job]:
        for page in self.pages:
            yield from page.jobs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListJobsAsyncPager:
    """A pager for iterating through ``list_jobs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.transcoder_v1beta1.types.ListJobsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``jobs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListJobs`` requests and continue to iterate
    through the ``jobs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.transcoder_v1beta1.types.ListJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[services.ListJobsResponse]],
        request: services.ListJobsRequest,
        response: services.ListJobsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.transcoder_v1beta1.types.ListJobsRequest):
                The initial request object.
            response (google.cloud.video.transcoder_v1beta1.types.ListJobsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = services.ListJobsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[services.ListJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.Job]:
        async def async_generator():
            async for page in self.pages:
                for response in page.jobs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListJobTemplatesPager:
    """A pager for iterating through ``list_job_templates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``job_templates`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListJobTemplates`` requests and continue to iterate
    through the ``job_templates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., services.ListJobTemplatesResponse],
        request: services.ListJobTemplatesRequest,
        response: services.ListJobTemplatesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesRequest):
                The initial request object.
            response (google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = services.ListJobTemplatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[services.ListJobTemplatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.JobTemplate]:
        for page in self.pages:
            yield from page.job_templates

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListJobTemplatesAsyncPager:
    """A pager for iterating through ``list_job_templates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``job_templates`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListJobTemplates`` requests and continue to iterate
    through the ``job_templates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[services.ListJobTemplatesResponse]],
        request: services.ListJobTemplatesRequest,
        response: services.ListJobTemplatesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesRequest):
                The initial request object.
            response (google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = services.ListJobTemplatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[services.ListJobTemplatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.JobTemplate]:
        async def async_generator():
            async for page in self.pages:
                for response in page.job_templates:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
