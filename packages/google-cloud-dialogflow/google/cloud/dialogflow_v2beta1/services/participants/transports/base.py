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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.dialogflow_v2beta1.types import participant
from google.cloud.dialogflow_v2beta1.types import participant as gcd_participant


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ParticipantsTransport(abc.ABC):
    """Abstract transport class for Participants."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/dialogflow",
    )

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_participant: gapic_v1.method.wrap_method(
                self.create_participant, default_timeout=None, client_info=client_info,
            ),
            self.get_participant: gapic_v1.method.wrap_method(
                self.get_participant, default_timeout=None, client_info=client_info,
            ),
            self.list_participants: gapic_v1.method.wrap_method(
                self.list_participants, default_timeout=None, client_info=client_info,
            ),
            self.update_participant: gapic_v1.method.wrap_method(
                self.update_participant, default_timeout=None, client_info=client_info,
            ),
            self.analyze_content: gapic_v1.method.wrap_method(
                self.analyze_content,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                    deadline=220.0,
                ),
                default_timeout=220.0,
                client_info=client_info,
            ),
            self.suggest_articles: gapic_v1.method.wrap_method(
                self.suggest_articles, default_timeout=None, client_info=client_info,
            ),
            self.suggest_faq_answers: gapic_v1.method.wrap_method(
                self.suggest_faq_answers, default_timeout=None, client_info=client_info,
            ),
            self.suggest_smart_replies: gapic_v1.method.wrap_method(
                self.suggest_smart_replies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_suggestions: gapic_v1.method.wrap_method(
                self.list_suggestions, default_timeout=None, client_info=client_info,
            ),
            self.compile_suggestion: gapic_v1.method.wrap_method(
                self.compile_suggestion, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def create_participant(
        self,
    ) -> typing.Callable[
        [gcd_participant.CreateParticipantRequest],
        typing.Union[
            gcd_participant.Participant, typing.Awaitable[gcd_participant.Participant]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_participant(
        self,
    ) -> typing.Callable[
        [participant.GetParticipantRequest],
        typing.Union[
            participant.Participant, typing.Awaitable[participant.Participant]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_participants(
        self,
    ) -> typing.Callable[
        [participant.ListParticipantsRequest],
        typing.Union[
            participant.ListParticipantsResponse,
            typing.Awaitable[participant.ListParticipantsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_participant(
        self,
    ) -> typing.Callable[
        [gcd_participant.UpdateParticipantRequest],
        typing.Union[
            gcd_participant.Participant, typing.Awaitable[gcd_participant.Participant]
        ],
    ]:
        raise NotImplementedError()

    @property
    def analyze_content(
        self,
    ) -> typing.Callable[
        [gcd_participant.AnalyzeContentRequest],
        typing.Union[
            gcd_participant.AnalyzeContentResponse,
            typing.Awaitable[gcd_participant.AnalyzeContentResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def suggest_articles(
        self,
    ) -> typing.Callable[
        [participant.SuggestArticlesRequest],
        typing.Union[
            participant.SuggestArticlesResponse,
            typing.Awaitable[participant.SuggestArticlesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def suggest_faq_answers(
        self,
    ) -> typing.Callable[
        [participant.SuggestFaqAnswersRequest],
        typing.Union[
            participant.SuggestFaqAnswersResponse,
            typing.Awaitable[participant.SuggestFaqAnswersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def suggest_smart_replies(
        self,
    ) -> typing.Callable[
        [participant.SuggestSmartRepliesRequest],
        typing.Union[
            participant.SuggestSmartRepliesResponse,
            typing.Awaitable[participant.SuggestSmartRepliesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_suggestions(
        self,
    ) -> typing.Callable[
        [participant.ListSuggestionsRequest],
        typing.Union[
            participant.ListSuggestionsResponse,
            typing.Awaitable[participant.ListSuggestionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def compile_suggestion(
        self,
    ) -> typing.Callable[
        [participant.CompileSuggestionRequest],
        typing.Union[
            participant.CompileSuggestionResponse,
            typing.Awaitable[participant.CompileSuggestionResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ParticipantsTransport",)
