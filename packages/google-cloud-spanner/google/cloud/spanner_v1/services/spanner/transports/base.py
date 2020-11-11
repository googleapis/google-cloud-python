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

from google.cloud.spanner_v1.types import result_set
from google.cloud.spanner_v1.types import spanner
from google.cloud.spanner_v1.types import transaction
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-spanner",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class SpannerTransport(abc.ABC):
    """Abstract transport class for Spanner."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spanner.data",
    )

    def __init__(
        self,
        *,
        host: str = "spanner.googleapis.com",
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
            self.create_session: gapic_v1.method.wrap_method(
                self.create_session,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.batch_create_sessions: gapic_v1.method.wrap_method(
                self.batch_create_sessions,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_session: gapic_v1.method.wrap_method(
                self.get_session,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_sessions: gapic_v1.method.wrap_method(
                self.list_sessions,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=3600.0,
                client_info=client_info,
            ),
            self.delete_session: gapic_v1.method.wrap_method(
                self.delete_session,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.execute_sql: gapic_v1.method.wrap_method(
                self.execute_sql,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.execute_streaming_sql: gapic_v1.method.wrap_method(
                self.execute_streaming_sql,
                default_timeout=3600.0,
                client_info=client_info,
            ),
            self.execute_batch_dml: gapic_v1.method.wrap_method(
                self.execute_batch_dml,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.read: gapic_v1.method.wrap_method(
                self.read,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.streaming_read: gapic_v1.method.wrap_method(
                self.streaming_read, default_timeout=3600.0, client_info=client_info,
            ),
            self.begin_transaction: gapic_v1.method.wrap_method(
                self.begin_transaction,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.commit: gapic_v1.method.wrap_method(
                self.commit,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=3600.0,
                client_info=client_info,
            ),
            self.rollback: gapic_v1.method.wrap_method(
                self.rollback,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.partition_query: gapic_v1.method.wrap_method(
                self.partition_query,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.partition_read: gapic_v1.method.wrap_method(
                self.partition_read,
                default_retry=retries.Retry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
        }

    @property
    def create_session(
        self,
    ) -> typing.Callable[
        [spanner.CreateSessionRequest],
        typing.Union[spanner.Session, typing.Awaitable[spanner.Session]],
    ]:
        raise NotImplementedError()

    @property
    def batch_create_sessions(
        self,
    ) -> typing.Callable[
        [spanner.BatchCreateSessionsRequest],
        typing.Union[
            spanner.BatchCreateSessionsResponse,
            typing.Awaitable[spanner.BatchCreateSessionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_session(
        self,
    ) -> typing.Callable[
        [spanner.GetSessionRequest],
        typing.Union[spanner.Session, typing.Awaitable[spanner.Session]],
    ]:
        raise NotImplementedError()

    @property
    def list_sessions(
        self,
    ) -> typing.Callable[
        [spanner.ListSessionsRequest],
        typing.Union[
            spanner.ListSessionsResponse, typing.Awaitable[spanner.ListSessionsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_session(
        self,
    ) -> typing.Callable[
        [spanner.DeleteSessionRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def execute_sql(
        self,
    ) -> typing.Callable[
        [spanner.ExecuteSqlRequest],
        typing.Union[result_set.ResultSet, typing.Awaitable[result_set.ResultSet]],
    ]:
        raise NotImplementedError()

    @property
    def execute_streaming_sql(
        self,
    ) -> typing.Callable[
        [spanner.ExecuteSqlRequest],
        typing.Union[
            result_set.PartialResultSet, typing.Awaitable[result_set.PartialResultSet]
        ],
    ]:
        raise NotImplementedError()

    @property
    def execute_batch_dml(
        self,
    ) -> typing.Callable[
        [spanner.ExecuteBatchDmlRequest],
        typing.Union[
            spanner.ExecuteBatchDmlResponse,
            typing.Awaitable[spanner.ExecuteBatchDmlResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def read(
        self,
    ) -> typing.Callable[
        [spanner.ReadRequest],
        typing.Union[result_set.ResultSet, typing.Awaitable[result_set.ResultSet]],
    ]:
        raise NotImplementedError()

    @property
    def streaming_read(
        self,
    ) -> typing.Callable[
        [spanner.ReadRequest],
        typing.Union[
            result_set.PartialResultSet, typing.Awaitable[result_set.PartialResultSet]
        ],
    ]:
        raise NotImplementedError()

    @property
    def begin_transaction(
        self,
    ) -> typing.Callable[
        [spanner.BeginTransactionRequest],
        typing.Union[
            transaction.Transaction, typing.Awaitable[transaction.Transaction]
        ],
    ]:
        raise NotImplementedError()

    @property
    def commit(
        self,
    ) -> typing.Callable[
        [spanner.CommitRequest],
        typing.Union[spanner.CommitResponse, typing.Awaitable[spanner.CommitResponse]],
    ]:
        raise NotImplementedError()

    @property
    def rollback(
        self,
    ) -> typing.Callable[
        [spanner.RollbackRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def partition_query(
        self,
    ) -> typing.Callable[
        [spanner.PartitionQueryRequest],
        typing.Union[
            spanner.PartitionResponse, typing.Awaitable[spanner.PartitionResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def partition_read(
        self,
    ) -> typing.Callable[
        [spanner.PartitionReadRequest],
        typing.Union[
            spanner.PartitionResponse, typing.Awaitable[spanner.PartitionResponse]
        ],
    ]:
        raise NotImplementedError()


__all__ = ("SpannerTransport",)
