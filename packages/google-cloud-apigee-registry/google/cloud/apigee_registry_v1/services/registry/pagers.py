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

from google.cloud.apigee_registry_v1.types import registry_models, registry_service


class ListApisPager:
    """A pager for iterating through ``list_apis`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApisResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``apis`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApis`` requests and continue to iterate
    through the ``apis`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApisResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApisResponse],
        request: registry_service.ListApisRequest,
        response: registry_service.ListApisResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApisRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApisResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApisRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApisResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.Api]:
        for page in self.pages:
            yield from page.apis

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApisAsyncPager:
    """A pager for iterating through ``list_apis`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApisResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``apis`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApis`` requests and continue to iterate
    through the ``apis`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApisResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListApisResponse]],
        request: registry_service.ListApisRequest,
        response: registry_service.ListApisResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApisRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApisResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApisRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[registry_service.ListApisResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.Api]:
        async def async_generator():
            async for page in self.pages:
                for response in page.apis:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiVersionsPager:
    """A pager for iterating through ``list_api_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiVersions`` requests and continue to iterate
    through the ``api_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApiVersionsResponse],
        request: registry_service.ListApiVersionsRequest,
        response: registry_service.ListApiVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiVersionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApiVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.ApiVersion]:
        for page in self.pages:
            yield from page.api_versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiVersionsAsyncPager:
    """A pager for iterating through ``list_api_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiVersionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_versions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiVersions`` requests and continue to iterate
    through the ``api_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListApiVersionsResponse]],
        request: registry_service.ListApiVersionsRequest,
        response: registry_service.ListApiVersionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiVersionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiVersionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiVersionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[registry_service.ListApiVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.ApiVersion]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_versions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiSpecsPager:
    """A pager for iterating through ``list_api_specs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiSpecsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_specs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiSpecs`` requests and continue to iterate
    through the ``api_specs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiSpecsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApiSpecsResponse],
        request: registry_service.ListApiSpecsRequest,
        response: registry_service.ListApiSpecsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiSpecsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiSpecsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiSpecsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApiSpecsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.ApiSpec]:
        for page in self.pages:
            yield from page.api_specs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiSpecsAsyncPager:
    """A pager for iterating through ``list_api_specs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiSpecsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_specs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiSpecs`` requests and continue to iterate
    through the ``api_specs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiSpecsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListApiSpecsResponse]],
        request: registry_service.ListApiSpecsRequest,
        response: registry_service.ListApiSpecsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiSpecsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiSpecsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiSpecsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[registry_service.ListApiSpecsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.ApiSpec]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_specs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiSpecRevisionsPager:
    """A pager for iterating through ``list_api_spec_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_specs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiSpecRevisions`` requests and continue to iterate
    through the ``api_specs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApiSpecRevisionsResponse],
        request: registry_service.ListApiSpecRevisionsRequest,
        response: registry_service.ListApiSpecRevisionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiSpecRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApiSpecRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.ApiSpec]:
        for page in self.pages:
            yield from page.api_specs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiSpecRevisionsAsyncPager:
    """A pager for iterating through ``list_api_spec_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_specs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiSpecRevisions`` requests and continue to iterate
    through the ``api_specs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListApiSpecRevisionsResponse]],
        request: registry_service.ListApiSpecRevisionsRequest,
        response: registry_service.ListApiSpecRevisionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiSpecRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[registry_service.ListApiSpecRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.ApiSpec]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_specs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiDeploymentsPager:
    """A pager for iterating through ``list_api_deployments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_deployments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiDeployments`` requests and continue to iterate
    through the ``api_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApiDeploymentsResponse],
        request: registry_service.ListApiDeploymentsRequest,
        response: registry_service.ListApiDeploymentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiDeploymentsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiDeploymentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApiDeploymentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.ApiDeployment]:
        for page in self.pages:
            yield from page.api_deployments

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiDeploymentsAsyncPager:
    """A pager for iterating through ``list_api_deployments`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_deployments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiDeployments`` requests and continue to iterate
    through the ``api_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListApiDeploymentsResponse]],
        request: registry_service.ListApiDeploymentsRequest,
        response: registry_service.ListApiDeploymentsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiDeploymentsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiDeploymentsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiDeploymentsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[registry_service.ListApiDeploymentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.ApiDeployment]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_deployments:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiDeploymentRevisionsPager:
    """A pager for iterating through ``list_api_deployment_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``api_deployments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListApiDeploymentRevisions`` requests and continue to iterate
    through the ``api_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListApiDeploymentRevisionsResponse],
        request: registry_service.ListApiDeploymentRevisionsRequest,
        response: registry_service.ListApiDeploymentRevisionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiDeploymentRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListApiDeploymentRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.ApiDeployment]:
        for page in self.pages:
            yield from page.api_deployments

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListApiDeploymentRevisionsAsyncPager:
    """A pager for iterating through ``list_api_deployment_revisions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``api_deployments`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListApiDeploymentRevisions`` requests and continue to iterate
    through the ``api_deployments`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[registry_service.ListApiDeploymentRevisionsResponse]
        ],
        request: registry_service.ListApiDeploymentRevisionsRequest,
        response: registry_service.ListApiDeploymentRevisionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListApiDeploymentRevisionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[registry_service.ListApiDeploymentRevisionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.ApiDeployment]:
        async def async_generator():
            async for page in self.pages:
                for response in page.api_deployments:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListArtifactsPager:
    """A pager for iterating through ``list_artifacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListArtifactsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``artifacts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListArtifacts`` requests and continue to iterate
    through the ``artifacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListArtifactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., registry_service.ListArtifactsResponse],
        request: registry_service.ListArtifactsRequest,
        response: registry_service.ListArtifactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListArtifactsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListArtifactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListArtifactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[registry_service.ListArtifactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[registry_models.Artifact]:
        for page in self.pages:
            yield from page.artifacts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListArtifactsAsyncPager:
    """A pager for iterating through ``list_artifacts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.apigee_registry_v1.types.ListArtifactsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``artifacts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListArtifacts`` requests and continue to iterate
    through the ``artifacts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.apigee_registry_v1.types.ListArtifactsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[registry_service.ListArtifactsResponse]],
        request: registry_service.ListArtifactsRequest,
        response: registry_service.ListArtifactsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.apigee_registry_v1.types.ListArtifactsRequest):
                The initial request object.
            response (google.cloud.apigee_registry_v1.types.ListArtifactsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = registry_service.ListArtifactsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[registry_service.ListArtifactsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[registry_models.Artifact]:
        async def async_generator():
            async for page in self.pages:
                for response in page.artifacts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
