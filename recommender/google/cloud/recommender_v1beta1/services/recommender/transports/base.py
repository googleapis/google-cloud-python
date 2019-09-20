# -*- coding: utf-8 -*-
import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_service


class RecommenderTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for Recommender."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "recommender.googleapis.com",
        credentials: credentials.Credentials = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def list_recommendations(
        self
    ) -> typing.Callable[
        [recommender_service.ListRecommendationsRequest],
        recommender_service.ListRecommendationsResponse,
    ]:
        raise NotImplementedError

    @property
    def get_recommendation(
        self
    ) -> typing.Callable[
        [recommender_service.GetRecommendationRequest], recommendation.Recommendation
    ]:
        raise NotImplementedError

    @property
    def mark_recommendation_claimed(
        self
    ) -> typing.Callable[
        [recommender_service.MarkRecommendationClaimedRequest],
        recommendation.Recommendation,
    ]:
        raise NotImplementedError

    @property
    def mark_recommendation_succeeded(
        self
    ) -> typing.Callable[
        [recommender_service.MarkRecommendationSucceededRequest],
        recommendation.Recommendation,
    ]:
        raise NotImplementedError

    @property
    def mark_recommendation_failed(
        self
    ) -> typing.Callable[
        [recommender_service.MarkRecommendationFailedRequest],
        recommendation.Recommendation,
    ]:
        raise NotImplementedError


__all__ = ("RecommenderTransport",)
