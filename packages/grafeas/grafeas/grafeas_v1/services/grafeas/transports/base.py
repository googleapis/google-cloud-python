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

from google import auth
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.protobuf import empty_pb2 as empty  # type: ignore
from grafeas.grafeas_v1.types import grafeas


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("grafeas",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


class GrafeasTransport(abc.ABC):
    """Abstract transport class for Grafeas."""

    AUTH_SCOPES = ()

    def __init__(
        self,
        *,
        host: str = "",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
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
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages()

    def _prep_wrapped_messages(self):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.get_occurrence: gapic_v1.method.wrap_method(
                self.get_occurrence,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.list_occurrences: gapic_v1.method.wrap_method(
                self.list_occurrences,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.delete_occurrence: gapic_v1.method.wrap_method(
                self.delete_occurrence,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.create_occurrence: gapic_v1.method.wrap_method(
                self.create_occurrence, default_timeout=30.0, client_info=_client_info,
            ),
            self.batch_create_occurrences: gapic_v1.method.wrap_method(
                self.batch_create_occurrences,
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.update_occurrence: gapic_v1.method.wrap_method(
                self.update_occurrence, default_timeout=30.0, client_info=_client_info,
            ),
            self.get_occurrence_note: gapic_v1.method.wrap_method(
                self.get_occurrence_note,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.get_note: gapic_v1.method.wrap_method(
                self.get_note,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.list_notes: gapic_v1.method.wrap_method(
                self.list_notes,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.delete_note: gapic_v1.method.wrap_method(
                self.delete_note,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
            self.create_note: gapic_v1.method.wrap_method(
                self.create_note, default_timeout=30.0, client_info=_client_info,
            ),
            self.batch_create_notes: gapic_v1.method.wrap_method(
                self.batch_create_notes, default_timeout=30.0, client_info=_client_info,
            ),
            self.update_note: gapic_v1.method.wrap_method(
                self.update_note, default_timeout=30.0, client_info=_client_info,
            ),
            self.list_note_occurrences: gapic_v1.method.wrap_method(
                self.list_note_occurrences,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=30.0,
                client_info=_client_info,
            ),
        }

    @property
    def get_occurrence(
        self,
    ) -> typing.Callable[
        [grafeas.GetOccurrenceRequest],
        typing.Union[grafeas.Occurrence, typing.Awaitable[grafeas.Occurrence]],
    ]:
        raise NotImplementedError()

    @property
    def list_occurrences(
        self,
    ) -> typing.Callable[
        [grafeas.ListOccurrencesRequest],
        typing.Union[
            grafeas.ListOccurrencesResponse,
            typing.Awaitable[grafeas.ListOccurrencesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_occurrence(
        self,
    ) -> typing.Callable[
        [grafeas.DeleteOccurrenceRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_occurrence(
        self,
    ) -> typing.Callable[
        [grafeas.CreateOccurrenceRequest],
        typing.Union[grafeas.Occurrence, typing.Awaitable[grafeas.Occurrence]],
    ]:
        raise NotImplementedError()

    @property
    def batch_create_occurrences(
        self,
    ) -> typing.Callable[
        [grafeas.BatchCreateOccurrencesRequest],
        typing.Union[
            grafeas.BatchCreateOccurrencesResponse,
            typing.Awaitable[grafeas.BatchCreateOccurrencesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_occurrence(
        self,
    ) -> typing.Callable[
        [grafeas.UpdateOccurrenceRequest],
        typing.Union[grafeas.Occurrence, typing.Awaitable[grafeas.Occurrence]],
    ]:
        raise NotImplementedError()

    @property
    def get_occurrence_note(
        self,
    ) -> typing.Callable[
        [grafeas.GetOccurrenceNoteRequest],
        typing.Union[grafeas.Note, typing.Awaitable[grafeas.Note]],
    ]:
        raise NotImplementedError()

    @property
    def get_note(
        self,
    ) -> typing.Callable[
        [grafeas.GetNoteRequest],
        typing.Union[grafeas.Note, typing.Awaitable[grafeas.Note]],
    ]:
        raise NotImplementedError()

    @property
    def list_notes(
        self,
    ) -> typing.Callable[
        [grafeas.ListNotesRequest],
        typing.Union[
            grafeas.ListNotesResponse, typing.Awaitable[grafeas.ListNotesResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_note(
        self,
    ) -> typing.Callable[
        [grafeas.DeleteNoteRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_note(
        self,
    ) -> typing.Callable[
        [grafeas.CreateNoteRequest],
        typing.Union[grafeas.Note, typing.Awaitable[grafeas.Note]],
    ]:
        raise NotImplementedError()

    @property
    def batch_create_notes(
        self,
    ) -> typing.Callable[
        [grafeas.BatchCreateNotesRequest],
        typing.Union[
            grafeas.BatchCreateNotesResponse,
            typing.Awaitable[grafeas.BatchCreateNotesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_note(
        self,
    ) -> typing.Callable[
        [grafeas.UpdateNoteRequest],
        typing.Union[grafeas.Note, typing.Awaitable[grafeas.Note]],
    ]:
        raise NotImplementedError()

    @property
    def list_note_occurrences(
        self,
    ) -> typing.Callable[
        [grafeas.ListNoteOccurrencesRequest],
        typing.Union[
            grafeas.ListNoteOccurrencesResponse,
            typing.Awaitable[grafeas.ListNoteOccurrencesResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("GrafeasTransport",)
