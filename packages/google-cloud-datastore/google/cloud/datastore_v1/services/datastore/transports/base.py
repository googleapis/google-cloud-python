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

from google.cloud.datastore_v1.types import datastore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-datastore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DatastoreTransport(abc.ABC):
    """Abstract transport class for Datastore."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/datastore",
    )

    def __init__(
        self,
        *,
        host: str = "datastore.googleapis.com",
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
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.lookup: gapic_v1.method.wrap_method(
                self.lookup,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.run_query: gapic_v1.method.wrap_method(
                self.run_query,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.begin_transaction: gapic_v1.method.wrap_method(
                self.begin_transaction, default_timeout=60.0, client_info=client_info,
            ),
            self.commit: gapic_v1.method.wrap_method(
                self.commit, default_timeout=60.0, client_info=client_info,
            ),
            self.rollback: gapic_v1.method.wrap_method(
                self.rollback, default_timeout=60.0, client_info=client_info,
            ),
            self.allocate_ids: gapic_v1.method.wrap_method(
                self.allocate_ids, default_timeout=60.0, client_info=client_info,
            ),
            self.reserve_ids: gapic_v1.method.wrap_method(
                self.reserve_ids,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def lookup(
        self,
    ) -> typing.Callable[
        [datastore.LookupRequest],
        typing.Union[
            datastore.LookupResponse, typing.Awaitable[datastore.LookupResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def run_query(
        self,
    ) -> typing.Callable[
        [datastore.RunQueryRequest],
        typing.Union[
            datastore.RunQueryResponse, typing.Awaitable[datastore.RunQueryResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def begin_transaction(
        self,
    ) -> typing.Callable[
        [datastore.BeginTransactionRequest],
        typing.Union[
            datastore.BeginTransactionResponse,
            typing.Awaitable[datastore.BeginTransactionResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def commit(
        self,
    ) -> typing.Callable[
        [datastore.CommitRequest],
        typing.Union[
            datastore.CommitResponse, typing.Awaitable[datastore.CommitResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def rollback(
        self,
    ) -> typing.Callable[
        [datastore.RollbackRequest],
        typing.Union[
            datastore.RollbackResponse, typing.Awaitable[datastore.RollbackResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def allocate_ids(
        self,
    ) -> typing.Callable[
        [datastore.AllocateIdsRequest],
        typing.Union[
            datastore.AllocateIdsResponse,
            typing.Awaitable[datastore.AllocateIdsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def reserve_ids(
        self,
    ) -> typing.Callable[
        [datastore.ReserveIdsRequest],
        typing.Union[
            datastore.ReserveIdsResponse, typing.Awaitable[datastore.ReserveIdsResponse]
        ],
    ]:
        raise NotImplementedError()


__all__ = ("DatastoreTransport",)
