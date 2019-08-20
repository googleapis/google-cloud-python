# -*- coding: utf-8 -*-
import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.language_v1.types import language_service


class LanguageServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for LanguageService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-language",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        *,
        host: str = "language.googleapis.com",
        credentials: credentials.Credentials = None,
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
    def analyze_sentiment(
        self
    ) -> typing.Callable[
        [language_service.AnalyzeSentimentRequest],
        language_service.AnalyzeSentimentResponse,
    ]:
        raise NotImplementedError

    @property
    def analyze_entities(
        self
    ) -> typing.Callable[
        [language_service.AnalyzeEntitiesRequest],
        language_service.AnalyzeEntitiesResponse,
    ]:
        raise NotImplementedError

    @property
    def analyze_entity_sentiment(
        self
    ) -> typing.Callable[
        [language_service.AnalyzeEntitySentimentRequest],
        language_service.AnalyzeEntitySentimentResponse,
    ]:
        raise NotImplementedError

    @property
    def analyze_syntax(
        self
    ) -> typing.Callable[
        [language_service.AnalyzeSyntaxRequest], language_service.AnalyzeSyntaxResponse
    ]:
        raise NotImplementedError

    @property
    def classify_text(
        self
    ) -> typing.Callable[
        [language_service.ClassifyTextRequest], language_service.ClassifyTextResponse
    ]:
        raise NotImplementedError

    @property
    def annotate_text(
        self
    ) -> typing.Callable[
        [language_service.AnnotateTextRequest], language_service.AnnotateTextResponse
    ]:
        raise NotImplementedError


__all__ = ("LanguageServiceTransport",)
