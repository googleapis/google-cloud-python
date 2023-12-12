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

from google.shopping.css_v1.types import css_products


class ListCssProductsPager:
    """A pager for iterating through ``list_css_products`` requests.

    This class thinly wraps an initial
    :class:`google.shopping.css_v1.types.ListCssProductsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``css_products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCssProducts`` requests and continue to iterate
    through the ``css_products`` field on the
    corresponding responses.

    All the usual :class:`google.shopping.css_v1.types.ListCssProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., css_products.ListCssProductsResponse],
        request: css_products.ListCssProductsRequest,
        response: css_products.ListCssProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.shopping.css_v1.types.ListCssProductsRequest):
                The initial request object.
            response (google.shopping.css_v1.types.ListCssProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = css_products.ListCssProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[css_products.ListCssProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[css_products.CssProduct]:
        for page in self.pages:
            yield from page.css_products

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCssProductsAsyncPager:
    """A pager for iterating through ``list_css_products`` requests.

    This class thinly wraps an initial
    :class:`google.shopping.css_v1.types.ListCssProductsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``css_products`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCssProducts`` requests and continue to iterate
    through the ``css_products`` field on the
    corresponding responses.

    All the usual :class:`google.shopping.css_v1.types.ListCssProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[css_products.ListCssProductsResponse]],
        request: css_products.ListCssProductsRequest,
        response: css_products.ListCssProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.shopping.css_v1.types.ListCssProductsRequest):
                The initial request object.
            response (google.shopping.css_v1.types.ListCssProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = css_products.ListCssProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[css_products.ListCssProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[css_products.CssProduct]:
        async def async_generator():
            async for page in self.pages:
                for response in page.css_products:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
