# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterable

from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_service


class ListRecommendationsPager:
    """A pager for iterating through ``list_recommendations`` requests.

    This class thinly wraps an initial
    :class:`~.recommender_service.ListRecommendationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``recommendations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRecommendations`` requests and continue to iterate
    through the ``recommendations`` field on the
    corresponding responses.

    All the usual :class:`~.recommender_service.ListRecommendationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [recommender_service.ListRecommendationsRequest],
            recommender_service.ListRecommendationsResponse,
        ],
        request: recommender_service.ListRecommendationsRequest,
        response: recommender_service.ListRecommendationsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.recommender_service.ListRecommendationsRequest`):
                The initial request object.
            response (:class:`~.recommender_service.ListRecommendationsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = recommender_service.ListRecommendationsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def __iter__(self) -> Iterable[recommendation.Recommendation]:
        while True:
            # Iterate through the results on this response.
            for result in self._response.recommendations:
                yield result

            # Sanity check: Is this the last page? If so, we are done.
            if not self._response.next_page_token:
                break

            # Get the next page.
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
