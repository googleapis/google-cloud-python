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

from google.cloud.monitoring_v3.types import alert
from google.cloud.monitoring_v3.types import alert_service


class ListAlertPoliciesPager:
    """A pager for iterating through ``list_alert_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListAlertPoliciesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``alert_policies`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAlertPolicies`` requests and continue to iterate
    through the ``alert_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListAlertPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., alert_service.ListAlertPoliciesResponse],
        request: alert_service.ListAlertPoliciesRequest,
        response: alert_service.ListAlertPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListAlertPoliciesRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListAlertPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = alert_service.ListAlertPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[alert_service.ListAlertPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[alert.AlertPolicy]:
        for page in self.pages:
            yield from page.alert_policies

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAlertPoliciesAsyncPager:
    """A pager for iterating through ``list_alert_policies`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.monitoring_v3.types.ListAlertPoliciesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``alert_policies`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAlertPolicies`` requests and continue to iterate
    through the ``alert_policies`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.monitoring_v3.types.ListAlertPoliciesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[alert_service.ListAlertPoliciesResponse]],
        request: alert_service.ListAlertPoliciesRequest,
        response: alert_service.ListAlertPoliciesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.monitoring_v3.types.ListAlertPoliciesRequest):
                The initial request object.
            response (google.cloud.monitoring_v3.types.ListAlertPoliciesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = alert_service.ListAlertPoliciesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[alert_service.ListAlertPoliciesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[alert.AlertPolicy]:
        async def async_generator():
            async for page in self.pages:
                for response in page.alert_policies:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
