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

from google.cloud.automl_v1.types import dataset
from google.cloud.automl_v1.types import model
from google.cloud.automl_v1.types import model_evaluation
from google.cloud.automl_v1.types import service


class ListDatasetsPager:
    """A pager for iterating through ``list_datasets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListDatasetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDatasets`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListDatasetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListDatasetsResponse],
        request: service.ListDatasetsRequest,
        response: service.ListDatasetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListDatasetsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListDatasetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListDatasetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListDatasetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[dataset.Dataset]:
        for page in self.pages:
            yield from page.datasets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDatasetsAsyncPager:
    """A pager for iterating through ``list_datasets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListDatasetsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``datasets`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDatasets`` requests and continue to iterate
    through the ``datasets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListDatasetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListDatasetsResponse]],
        request: service.ListDatasetsRequest,
        response: service.ListDatasetsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListDatasetsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListDatasetsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListDatasetsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[service.ListDatasetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[dataset.Dataset]:
        async def async_generator():
            async for page in self.pages:
                for response in page.datasets:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelsPager:
    """A pager for iterating through ``list_models`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListModelsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``model`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListModels`` requests and continue to iterate
    through the ``model`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListModelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListModelsResponse],
        request: service.ListModelsRequest,
        response: service.ListModelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListModelsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListModelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListModelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListModelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[model.Model]:
        for page in self.pages:
            yield from page.model

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelsAsyncPager:
    """A pager for iterating through ``list_models`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListModelsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``model`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListModels`` requests and continue to iterate
    through the ``model`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListModelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListModelsResponse]],
        request: service.ListModelsRequest,
        response: service.ListModelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListModelsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListModelsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListModelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[service.ListModelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[model.Model]:
        async def async_generator():
            async for page in self.pages:
                for response in page.model:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationsPager:
    """A pager for iterating through ``list_model_evaluations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListModelEvaluationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``model_evaluation`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListModelEvaluations`` requests and continue to iterate
    through the ``model_evaluation`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListModelEvaluationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListModelEvaluationsResponse],
        request: service.ListModelEvaluationsRequest,
        response: service.ListModelEvaluationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListModelEvaluationsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListModelEvaluationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListModelEvaluationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListModelEvaluationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[model_evaluation.ModelEvaluation]:
        for page in self.pages:
            yield from page.model_evaluation

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationsAsyncPager:
    """A pager for iterating through ``list_model_evaluations`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.automl_v1.types.ListModelEvaluationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``model_evaluation`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListModelEvaluations`` requests and continue to iterate
    through the ``model_evaluation`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.automl_v1.types.ListModelEvaluationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListModelEvaluationsResponse]],
        request: service.ListModelEvaluationsRequest,
        response: service.ListModelEvaluationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.automl_v1.types.ListModelEvaluationsRequest):
                The initial request object.
            response (google.cloud.automl_v1.types.ListModelEvaluationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListModelEvaluationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[service.ListModelEvaluationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[model_evaluation.ModelEvaluation]:
        async def async_generator():
            async for page in self.pages:
                for response in page.model_evaluation:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
