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

from google.cloud.recommendationengine_v1beta1.types import prediction_service


class PredictPager:
    """A pager for iterating through ``predict`` requests.

    This class thinly wraps an initial
    :class:`~.prediction_service.PredictResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``Predict`` requests and continue to iterate
    through the ``results`` field on the
    corresponding responses.

    All the usual :class:`~.prediction_service.PredictResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [prediction_service.PredictRequest], prediction_service.PredictResponse
        ],
        request: prediction_service.PredictRequest,
        response: prediction_service.PredictResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.prediction_service.PredictRequest`):
                The initial request object.
            response (:class:`~.prediction_service.PredictResponse`):
                The initial response object.
        """
        self._method = method
        self._request = prediction_service.PredictRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[prediction_service.PredictResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[prediction_service.PredictResponse.PredictionResult]:
        for page in self.pages:
            yield from page.results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
