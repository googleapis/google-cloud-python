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
from typing import Any, AsyncIterator, Awaitable, Callable, Sequence, Tuple, Optional, Iterator

from google.cloud.securityposture_v1.types import securityposture


class ListPosturesPager:
    """A pager for iterating through ``list_postures`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPosturesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``postures`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPostures`` requests and continue to iterate
    through the ``postures`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPosturesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., securityposture.ListPosturesResponse],
            request: securityposture.ListPosturesRequest,
            response: securityposture.ListPosturesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPosturesRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPosturesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPosturesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securityposture.ListPosturesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securityposture.Posture]:
        for page in self.pages:
            yield from page.postures

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPosturesAsyncPager:
    """A pager for iterating through ``list_postures`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPosturesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``postures`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPostures`` requests and continue to iterate
    through the ``postures`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPosturesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[securityposture.ListPosturesResponse]],
            request: securityposture.ListPosturesRequest,
            response: securityposture.ListPosturesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPosturesRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPosturesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPosturesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securityposture.ListPosturesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[securityposture.Posture]:
        async def async_generator():
            async for page in self.pages:
                for response in page.postures:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureRevisionsPager:
    """A pager for iterating through ``list_posture_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureRevisionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``revisions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPostureRevisions`` requests and continue to iterate
    through the ``revisions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., securityposture.ListPostureRevisionsResponse],
            request: securityposture.ListPostureRevisionsRequest,
            response: securityposture.ListPostureRevisionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureRevisionsRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securityposture.ListPostureRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securityposture.Posture]:
        for page in self.pages:
            yield from page.revisions

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureRevisionsAsyncPager:
    """A pager for iterating through ``list_posture_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureRevisionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``revisions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPostureRevisions`` requests and continue to iterate
    through the ``revisions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[securityposture.ListPostureRevisionsResponse]],
            request: securityposture.ListPostureRevisionsRequest,
            response: securityposture.ListPostureRevisionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureRevisionsRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securityposture.ListPostureRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[securityposture.Posture]:
        async def async_generator():
            async for page in self.pages:
                for response in page.revisions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureDeploymentsPager:
    """A pager for iterating through ``list_posture_deployments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``posture_deployments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPostureDeployments`` requests and continue to iterate
    through the ``posture_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., securityposture.ListPostureDeploymentsResponse],
            request: securityposture.ListPostureDeploymentsRequest,
            response: securityposture.ListPostureDeploymentsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureDeploymentsRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureDeploymentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securityposture.ListPostureDeploymentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securityposture.PostureDeployment]:
        for page in self.pages:
            yield from page.posture_deployments

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureDeploymentsAsyncPager:
    """A pager for iterating through ``list_posture_deployments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``posture_deployments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPostureDeployments`` requests and continue to iterate
    through the ``posture_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[securityposture.ListPostureDeploymentsResponse]],
            request: securityposture.ListPostureDeploymentsRequest,
            response: securityposture.ListPostureDeploymentsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureDeploymentsRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureDeploymentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureDeploymentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securityposture.ListPostureDeploymentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[securityposture.PostureDeployment]:
        async def async_generator():
            async for page in self.pages:
                for response in page.posture_deployments:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureTemplatesPager:
    """A pager for iterating through ``list_posture_templates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureTemplatesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``posture_templates`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPostureTemplates`` requests and continue to iterate
    through the ``posture_templates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureTemplatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., securityposture.ListPostureTemplatesResponse],
            request: securityposture.ListPostureTemplatesRequest,
            response: securityposture.ListPostureTemplatesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureTemplatesRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureTemplatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureTemplatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[securityposture.ListPostureTemplatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[securityposture.PostureTemplate]:
        for page in self.pages:
            yield from page.posture_templates

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListPostureTemplatesAsyncPager:
    """A pager for iterating through ``list_posture_templates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.securityposture_v1.types.ListPostureTemplatesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``posture_templates`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPostureTemplates`` requests and continue to iterate
    through the ``posture_templates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.securityposture_v1.types.ListPostureTemplatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[securityposture.ListPostureTemplatesResponse]],
            request: securityposture.ListPostureTemplatesRequest,
            response: securityposture.ListPostureTemplatesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.securityposture_v1.types.ListPostureTemplatesRequest):
                The initial request object.
            response (google.cloud.securityposture_v1.types.ListPostureTemplatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = securityposture.ListPostureTemplatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[securityposture.ListPostureTemplatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[securityposture.PostureTemplate]:
        async def async_generator():
            async for page in self.pages:
                for response in page.posture_templates:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
