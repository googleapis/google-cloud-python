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

from google.cloud.talent_v4beta1.types import company, company_service


class ListCompaniesPager:
    """A pager for iterating through ``list_companies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.ListCompaniesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``companies`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCompanies`` requests and continue to iterate
    through the ``companies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.ListCompaniesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., company_service.ListCompaniesResponse],
        request: company_service.ListCompaniesRequest,
        response: company_service.ListCompaniesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.ListCompaniesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.ListCompaniesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = company_service.ListCompaniesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[company_service.ListCompaniesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[company.Company]:
        for page in self.pages:
            yield from page.companies

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCompaniesAsyncPager:
    """A pager for iterating through ``list_companies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.talent_v4beta1.types.ListCompaniesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``companies`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCompanies`` requests and continue to iterate
    through the ``companies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.talent_v4beta1.types.ListCompaniesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[company_service.ListCompaniesResponse]],
        request: company_service.ListCompaniesRequest,
        response: company_service.ListCompaniesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.talent_v4beta1.types.ListCompaniesRequest):
                The initial request object.
            response (google.cloud.talent_v4beta1.types.ListCompaniesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = company_service.ListCompaniesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[company_service.ListCompaniesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[company.Company]:
        async def async_generator():
            async for page in self.pages:
                for response in page.companies:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
