# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from typing import Any, Callable, Iterable

from google.cloud.recommendationengine_v1beta1.types import (
    prediction_apikey_registry_service,
)


class ListPredictionApiKeyRegistrationsPager:
    """A pager for iterating through ``list_prediction_api_key_registrations`` requests.

    This class thinly wraps an initial
    :class:`~.prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``prediction_api_key_registrations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPredictionApiKeyRegistrations`` requests and continue to iterate
    through the ``prediction_api_key_registrations`` field on the
    corresponding responses.

    All the usual :class:`~.prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [
                prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest
            ],
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse,
        ],
        request: prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest,
        response: prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest`):
                The initial request object.
            response (:class:`~.prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest(
            request
        )
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self
    ) -> Iterable[
        prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse
    ]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(
        self
    ) -> Iterable[prediction_apikey_registry_service.PredictionApiKeyRegistration]:
        for page in self.pages:
            yield from page.prediction_api_key_registrations

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
