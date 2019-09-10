# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.spanner.v1 Spanner API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.spanner_v1.gapic import enums
from google.cloud.spanner_v1.gapic import spanner_client_config
from google.cloud.spanner_v1.gapic.transports import spanner_grpc_transport
from google.cloud.spanner_v1.proto import keys_pb2
from google.cloud.spanner_v1.proto import mutation_pb2
from google.cloud.spanner_v1.proto import result_set_pb2
from google.cloud.spanner_v1.proto import spanner_pb2
from google.cloud.spanner_v1.proto import spanner_pb2_grpc
from google.cloud.spanner_v1.proto import transaction_pb2
from google.protobuf import empty_pb2
from google.protobuf import struct_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-spanner").version


class SpannerClient(object):
    """
    Cloud Spanner API

    The Cloud Spanner API can be used to manage sessions and execute
    transactions on data stored in Cloud Spanner databases.
    """

    SERVICE_ADDRESS = "spanner.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.spanner.v1.Spanner"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SpannerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def database_path(cls, project, instance, database):
        """Return a fully-qualified database string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/databases/{database}",
            project=project,
            instance=instance,
            database=database,
        )

    @classmethod
    def session_path(cls, project, instance, database, session):
        """Return a fully-qualified session string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/databases/{database}/sessions/{session}",
            project=project,
            instance=instance,
            database=database,
            session=session,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.SpannerGrpcTransport,
                    Callable[[~.Credentials, type], ~.SpannerGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = spanner_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=spanner_grpc_transport.SpannerGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = spanner_grpc_transport.SpannerGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_session(
        self,
        database,
        session=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new session. A session can be used to perform transactions
        that read and/or modify data in a Cloud Spanner database. Sessions are
        meant to be reused for many consecutive transactions.

        Sessions can only execute one transaction at a time. To execute multiple
        concurrent read-write/write-only transactions, create multiple sessions.
        Note that standalone reads and queries use a transaction internally, and
        count toward the one transaction limit.

        Cloud Spanner limits the number of sessions that can exist at any given
        time; thus, it is a good idea to delete idle and/or unneeded sessions.
        Aside from explicit deletes, Cloud Spanner can delete sessions for which
        no operations are sent for more than an hour. If a session is deleted,
        requests to it return ``NOT_FOUND``.

        Idle sessions can be kept alive by sending a trivial SQL query
        periodically, e.g., ``"SELECT 1"``.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> response = client.create_session(database)

        Args:
            database (str): Required. The database in which the new session is created.
            session (Union[dict, ~google.cloud.spanner_v1.types.Session]): The session to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Session`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Session` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_session" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_session"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_session,
                default_retry=self._method_configs["CreateSession"].retry,
                default_timeout=self._method_configs["CreateSession"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.CreateSessionRequest(database=database, session=session)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_session"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_create_sessions(
        self,
        database,
        session_template=None,
        session_count=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates multiple new sessions.

        This API can be used to initialize a session cache on the clients.
        See https://goo.gl/TgSFN2 for best practices on session cache management.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> response = client.batch_create_sessions(database)

        Args:
            database (str): Required. The database in which the new sessions are created.
            session_template (Union[dict, ~google.cloud.spanner_v1.types.Session]): Parameters to be applied to each created session.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Session`
            session_count (int): Required. The number of sessions to be created in this batch call. The
                API may return fewer than the requested number of sessions. If a
                specific number of sessions are desired, the client can make additional
                calls to BatchCreateSessions (adjusting ``session_count`` as necessary).
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.BatchCreateSessionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_sessions" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_sessions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_sessions,
                default_retry=self._method_configs["BatchCreateSessions"].retry,
                default_timeout=self._method_configs["BatchCreateSessions"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.BatchCreateSessionsRequest(
            database=database,
            session_template=session_template,
            session_count=session_count,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["batch_create_sessions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_session(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a session. Returns ``NOT_FOUND`` if the session does not exist.
        This is mainly useful for determining whether a session is still alive.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> response = client.get_session(name)

        Args:
            name (str): Required. The name of the session to retrieve.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Session` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_session" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_session"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_session,
                default_retry=self._method_configs["GetSession"].retry,
                default_timeout=self._method_configs["GetSession"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.GetSessionRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_session"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_sessions(
        self,
        database,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all sessions in a given database.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_sessions(database):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_sessions(database).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            database (str): Required. The database in which to list sessions.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): An expression for filtering the results of the request. Filter rules are
                case insensitive. The fields eligible for filtering are:

                -  ``labels.key`` where key is the name of a label

                Some examples of using filters are:

                -  ``labels.env:*`` --> The session has the label "env".
                -  ``labels.env:dev`` --> The session has the label "env" and the value
                   of the label contains the string "dev".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.spanner_v1.types.Session` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_sessions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_sessions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_sessions,
                default_retry=self._method_configs["ListSessions"].retry,
                default_timeout=self._method_configs["ListSessions"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ListSessionsRequest(
            database=database, page_size=page_size, filter=filter_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_sessions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="sessions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_session(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Ends a session, releasing server resources associated with it. This will
        asynchronously trigger cancellation of any operations that are running with
        this session.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> name = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> client.delete_session(name)

        Args:
            name (str): Required. The name of the session to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_session" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_session"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_session,
                default_retry=self._method_configs["DeleteSession"].retry,
                default_timeout=self._method_configs["DeleteSession"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.DeleteSessionRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_session"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def execute_sql(
        self,
        session,
        sql,
        transaction=None,
        params=None,
        param_types=None,
        resume_token=None,
        query_mode=None,
        partition_token=None,
        seqno=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Executes an SQL statement, returning all results in a single reply. This
        method cannot be used to return a result set larger than 10 MiB; if the
        query yields more data than that, the query fails with a
        ``FAILED_PRECONDITION`` error.

        Operations inside read-write transactions might return ``ABORTED``. If
        this occurs, the application should restart the transaction from the
        beginning. See ``Transaction`` for more details.

        Larger result sets can be fetched in streaming fashion by calling
        ``ExecuteStreamingSql`` instead.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `sql`:
            >>> sql = ''
            >>>
            >>> response = client.execute_sql(session, sql)

        Args:
            session (str): Required. The session in which the SQL query should be performed.
            sql (str): Required. The SQL string.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use.

                For queries, if none is provided, the default is a temporary read-only
                transaction with strong concurrency.

                Standard DML statements require a ReadWrite transaction. Single-use
                transactions are not supported (to avoid replay).  The caller must
                either supply an existing transaction ID or begin a new transaction.

                Partitioned DML requires an existing PartitionedDml transaction ID.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            params (Union[dict, ~google.cloud.spanner_v1.types.Struct]): The SQL string can contain parameter placeholders. A parameter
                placeholder consists of ``'@'`` followed by the parameter name.
                Parameter names consist of any combination of letters, numbers, and
                underscores.

                Parameters can appear anywhere that a literal value is expected. The
                same parameter name can be used more than once, for example:
                ``"WHERE id > @msg_id AND id < @msg_id + 100"``

                It is an error to execute an SQL statement with unbound parameters.

                Parameter values are specified using ``params``, which is a JSON object
                whose keys are parameter names, and whose values are the corresponding
                parameter values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Struct`
            param_types (dict[str -> Union[dict, ~google.cloud.spanner_v1.types.Type]]): It is not always possible for Cloud Spanner to infer the right SQL type
                from a JSON value. For example, values of type ``BYTES`` and values of
                type ``STRING`` both appear in ``params`` as JSON strings.

                In these cases, ``param_types`` can be used to specify the exact SQL
                type for some or all of the SQL statement parameters. See the definition
                of ``Type`` for more information about SQL types.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Type`
            resume_token (bytes): If this request is resuming a previously interrupted SQL statement
                execution, ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this enables
                the new SQL statement execution to resume where the last one left off.
                The rest of the request parameters must exactly match the request that
                yielded this token.
            query_mode (~google.cloud.spanner_v1.types.QueryMode): Used to control the amount of debugging information returned in
                ``ResultSetStats``. If ``partition_token`` is set, ``query_mode`` can
                only be set to ``QueryMode.NORMAL``.
            partition_token (bytes): If present, results will be restricted to the specified partition
                previously created using PartitionQuery(). There must be an exact match
                for the values of fields common to this message and the
                PartitionQueryRequest message used to create this partition\_token.
            seqno (long): A per-transaction sequence number used to identify this request. This
                makes each request idempotent such that if the request is received multiple
                times, at most one will succeed.

                The sequence number must be monotonically increasing within the
                transaction. If a request arrives for the first time with an out-of-order
                sequence number, the transaction may be aborted. Replays of previously
                handled requests will yield the same response as the first execution.

                Required for DML statements. Ignored for queries.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.ResultSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "execute_sql" not in self._inner_api_calls:
            self._inner_api_calls[
                "execute_sql"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.execute_sql,
                default_retry=self._method_configs["ExecuteSql"].retry,
                default_timeout=self._method_configs["ExecuteSql"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ExecuteSqlRequest(
            session=session,
            sql=sql,
            transaction=transaction,
            params=params,
            param_types=param_types,
            resume_token=resume_token,
            query_mode=query_mode,
            partition_token=partition_token,
            seqno=seqno,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["execute_sql"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def execute_streaming_sql(
        self,
        session,
        sql,
        transaction=None,
        params=None,
        param_types=None,
        resume_token=None,
        query_mode=None,
        partition_token=None,
        seqno=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Like ``ExecuteSql``, except returns the result set as a stream. Unlike
        ``ExecuteSql``, there is no limit on the size of the returned result
        set. However, no individual row in the result set can exceed 100 MiB,
        and no column value can exceed 10 MiB.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `sql`:
            >>> sql = ''
            >>>
            >>> for element in client.execute_streaming_sql(session, sql):
            ...     # process element
            ...     pass

        Args:
            session (str): Required. The session in which the SQL query should be performed.
            sql (str): Required. The SQL string.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use.

                For queries, if none is provided, the default is a temporary read-only
                transaction with strong concurrency.

                Standard DML statements require a ReadWrite transaction. Single-use
                transactions are not supported (to avoid replay).  The caller must
                either supply an existing transaction ID or begin a new transaction.

                Partitioned DML requires an existing PartitionedDml transaction ID.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            params (Union[dict, ~google.cloud.spanner_v1.types.Struct]): The SQL string can contain parameter placeholders. A parameter
                placeholder consists of ``'@'`` followed by the parameter name.
                Parameter names consist of any combination of letters, numbers, and
                underscores.

                Parameters can appear anywhere that a literal value is expected. The
                same parameter name can be used more than once, for example:
                ``"WHERE id > @msg_id AND id < @msg_id + 100"``

                It is an error to execute an SQL statement with unbound parameters.

                Parameter values are specified using ``params``, which is a JSON object
                whose keys are parameter names, and whose values are the corresponding
                parameter values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Struct`
            param_types (dict[str -> Union[dict, ~google.cloud.spanner_v1.types.Type]]): It is not always possible for Cloud Spanner to infer the right SQL type
                from a JSON value. For example, values of type ``BYTES`` and values of
                type ``STRING`` both appear in ``params`` as JSON strings.

                In these cases, ``param_types`` can be used to specify the exact SQL
                type for some or all of the SQL statement parameters. See the definition
                of ``Type`` for more information about SQL types.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Type`
            resume_token (bytes): If this request is resuming a previously interrupted SQL statement
                execution, ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this enables
                the new SQL statement execution to resume where the last one left off.
                The rest of the request parameters must exactly match the request that
                yielded this token.
            query_mode (~google.cloud.spanner_v1.types.QueryMode): Used to control the amount of debugging information returned in
                ``ResultSetStats``. If ``partition_token`` is set, ``query_mode`` can
                only be set to ``QueryMode.NORMAL``.
            partition_token (bytes): If present, results will be restricted to the specified partition
                previously created using PartitionQuery(). There must be an exact match
                for the values of fields common to this message and the
                PartitionQueryRequest message used to create this partition\_token.
            seqno (long): A per-transaction sequence number used to identify this request. This
                makes each request idempotent such that if the request is received multiple
                times, at most one will succeed.

                The sequence number must be monotonically increasing within the
                transaction. If a request arrives for the first time with an out-of-order
                sequence number, the transaction may be aborted. Replays of previously
                handled requests will yield the same response as the first execution.

                Required for DML statements. Ignored for queries.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.spanner_v1.types.PartialResultSet].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "execute_streaming_sql" not in self._inner_api_calls:
            self._inner_api_calls[
                "execute_streaming_sql"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.execute_streaming_sql,
                default_retry=self._method_configs["ExecuteStreamingSql"].retry,
                default_timeout=self._method_configs["ExecuteStreamingSql"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ExecuteSqlRequest(
            session=session,
            sql=sql,
            transaction=transaction,
            params=params,
            param_types=param_types,
            resume_token=resume_token,
            query_mode=query_mode,
            partition_token=partition_token,
            seqno=seqno,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["execute_streaming_sql"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def execute_batch_dml(
        self,
        session,
        transaction,
        statements,
        seqno,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Executes a batch of SQL DML statements. This method allows many
        statements to be run with lower latency than submitting them
        sequentially with ``ExecuteSql``.

        Statements are executed in order, sequentially.
        ``ExecuteBatchDmlResponse`` will contain a ``ResultSet`` for each DML
        statement that has successfully executed. If a statement fails, its
        error status will be returned as part of the
        ``ExecuteBatchDmlResponse``. Execution will stop at the first failed
        statement; the remaining statements will not run.

        ExecuteBatchDml is expected to return an OK status with a response even
        if there was an error while processing one of the DML statements.
        Clients must inspect response.status to determine if there were any
        errors while processing the request.

        See more details in ``ExecuteBatchDmlRequest`` and
        ``ExecuteBatchDmlResponse``.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `transaction`:
            >>> transaction = {}
            >>>
            >>> # TODO: Initialize `statements`:
            >>> statements = []
            >>>
            >>> # TODO: Initialize `seqno`:
            >>> seqno = 0
            >>>
            >>> response = client.execute_batch_dml(session, transaction, statements, seqno)

        Args:
            session (str): Required. The session in which the DML statements should be performed.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. A ReadWrite transaction is required. Single-use
                transactions are not supported (to avoid replay).  The caller must either
                supply an existing transaction ID or begin a new transaction.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            statements (list[Union[dict, ~google.cloud.spanner_v1.types.Statement]]): The list of statements to execute in this batch. Statements are executed
                serially, such that the effects of statement i are visible to statement
                i+1. Each statement must be a DML statement. Execution will stop at the
                first failed statement; the remaining statements will not run.

                REQUIRES: statements\_size() > 0.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Statement`
            seqno (long): A per-transaction sequence number used to identify this request. This is
                used in the same space as the seqno in ``ExecuteSqlRequest``. See more
                details in ``ExecuteSqlRequest``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.ExecuteBatchDmlResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "execute_batch_dml" not in self._inner_api_calls:
            self._inner_api_calls[
                "execute_batch_dml"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.execute_batch_dml,
                default_retry=self._method_configs["ExecuteBatchDml"].retry,
                default_timeout=self._method_configs["ExecuteBatchDml"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ExecuteBatchDmlRequest(
            session=session, transaction=transaction, statements=statements, seqno=seqno
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["execute_batch_dml"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def read(
        self,
        session,
        table,
        columns,
        key_set,
        transaction=None,
        index=None,
        limit=None,
        resume_token=None,
        partition_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Reads rows from the database using key lookups and scans, as a simple
        key/value style alternative to ``ExecuteSql``. This method cannot be
        used to return a result set larger than 10 MiB; if the read matches more
        data than that, the read fails with a ``FAILED_PRECONDITION`` error.

        Reads inside read-write transactions might return ``ABORTED``. If this
        occurs, the application should restart the transaction from the
        beginning. See ``Transaction`` for more details.

        Larger result sets can be yielded in streaming fashion by calling
        ``StreamingRead`` instead.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `table`:
            >>> table = ''
            >>>
            >>> # TODO: Initialize `columns`:
            >>> columns = []
            >>>
            >>> # TODO: Initialize `key_set`:
            >>> key_set = {}
            >>>
            >>> response = client.read(session, table, columns, key_set)

        Args:
            session (str): Required. The session in which the read should be performed.
            table (str): Required. The name of the table in the database to be read.
            columns (list[str]): The columns of ``table`` to be returned for each row matching this
                request.
            key_set (Union[dict, ~google.cloud.spanner_v1.types.KeySet]): Required. ``key_set`` identifies the rows to be yielded. ``key_set``
                names the primary keys of the rows in ``table`` to be yielded, unless
                ``index`` is present. If ``index`` is present, then ``key_set`` instead
                names index keys in ``index``.

                If the ``partition_token`` field is empty, rows are yielded in table
                primary key order (if ``index`` is empty) or index key order (if
                ``index`` is non-empty). If the ``partition_token`` field is not empty,
                rows will be yielded in an unspecified order.

                It is not an error for the ``key_set`` to name rows that do not exist in
                the database. Read yields nothing for nonexistent rows.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.KeySet`
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            index (str): If non-empty, the name of an index on ``table``. This index is used
                instead of the table primary key when interpreting ``key_set`` and
                sorting result rows. See ``key_set`` for further information.
            limit (long): If greater than zero, only the first ``limit`` rows are yielded. If
                ``limit`` is zero, the default is no limit. A limit cannot be specified
                if ``partition_token`` is set.
            resume_token (bytes): If this request is resuming a previously interrupted read,
                ``resume_token`` should be copied from the last ``PartialResultSet``
                yielded before the interruption. Doing this enables the new read to
                resume where the last read left off. The rest of the request parameters
                must exactly match the request that yielded this token.
            partition_token (bytes): If present, results will be restricted to the specified partition
                previously created using PartitionRead(). There must be an exact match
                for the values of fields common to this message and the
                PartitionReadRequest message used to create this partition\_token.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.ResultSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "read" not in self._inner_api_calls:
            self._inner_api_calls["read"] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.read,
                default_retry=self._method_configs["Read"].retry,
                default_timeout=self._method_configs["Read"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ReadRequest(
            session=session,
            table=table,
            columns=columns,
            key_set=key_set,
            transaction=transaction,
            index=index,
            limit=limit,
            resume_token=resume_token,
            partition_token=partition_token,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["read"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def streaming_read(
        self,
        session,
        table,
        columns,
        key_set,
        transaction=None,
        index=None,
        limit=None,
        resume_token=None,
        partition_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Like ``Read``, except returns the result set as a stream. Unlike
        ``Read``, there is no limit on the size of the returned result set.
        However, no individual row in the result set can exceed 100 MiB, and no
        column value can exceed 10 MiB.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `table`:
            >>> table = ''
            >>>
            >>> # TODO: Initialize `columns`:
            >>> columns = []
            >>>
            >>> # TODO: Initialize `key_set`:
            >>> key_set = {}
            >>>
            >>> for element in client.streaming_read(session, table, columns, key_set):
            ...     # process element
            ...     pass

        Args:
            session (str): Required. The session in which the read should be performed.
            table (str): Required. The name of the table in the database to be read.
            columns (list[str]): The columns of ``table`` to be returned for each row matching this
                request.
            key_set (Union[dict, ~google.cloud.spanner_v1.types.KeySet]): Required. ``key_set`` identifies the rows to be yielded. ``key_set``
                names the primary keys of the rows in ``table`` to be yielded, unless
                ``index`` is present. If ``index`` is present, then ``key_set`` instead
                names index keys in ``index``.

                If the ``partition_token`` field is empty, rows are yielded in table
                primary key order (if ``index`` is empty) or index key order (if
                ``index`` is non-empty). If the ``partition_token`` field is not empty,
                rows will be yielded in an unspecified order.

                It is not an error for the ``key_set`` to name rows that do not exist in
                the database. Read yields nothing for nonexistent rows.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.KeySet`
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            index (str): If non-empty, the name of an index on ``table``. This index is used
                instead of the table primary key when interpreting ``key_set`` and
                sorting result rows. See ``key_set`` for further information.
            limit (long): If greater than zero, only the first ``limit`` rows are yielded. If
                ``limit`` is zero, the default is no limit. A limit cannot be specified
                if ``partition_token`` is set.
            resume_token (bytes): If this request is resuming a previously interrupted read,
                ``resume_token`` should be copied from the last ``PartialResultSet``
                yielded before the interruption. Doing this enables the new read to
                resume where the last read left off. The rest of the request parameters
                must exactly match the request that yielded this token.
            partition_token (bytes): If present, results will be restricted to the specified partition
                previously created using PartitionRead(). There must be an exact match
                for the values of fields common to this message and the
                PartitionReadRequest message used to create this partition\_token.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.spanner_v1.types.PartialResultSet].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "streaming_read" not in self._inner_api_calls:
            self._inner_api_calls[
                "streaming_read"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.streaming_read,
                default_retry=self._method_configs["StreamingRead"].retry,
                default_timeout=self._method_configs["StreamingRead"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.ReadRequest(
            session=session,
            table=table,
            columns=columns,
            key_set=key_set,
            transaction=transaction,
            index=index,
            limit=limit,
            resume_token=resume_token,
            partition_token=partition_token,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["streaming_read"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def begin_transaction(
        self,
        session,
        options_,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Begins a new transaction. This step can often be skipped: ``Read``,
        ``ExecuteSql`` and ``Commit`` can begin a new transaction as a
        side-effect.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `options_`:
            >>> options_ = {}
            >>>
            >>> response = client.begin_transaction(session, options_)

        Args:
            session (str): Required. The session in which the transaction runs.
            options_ (Union[dict, ~google.cloud.spanner_v1.types.TransactionOptions]): Required. Options for the new transaction.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Transaction` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "begin_transaction" not in self._inner_api_calls:
            self._inner_api_calls[
                "begin_transaction"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.begin_transaction,
                default_retry=self._method_configs["BeginTransaction"].retry,
                default_timeout=self._method_configs["BeginTransaction"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.BeginTransactionRequest(session=session, options=options_)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["begin_transaction"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def commit(
        self,
        session,
        mutations,
        transaction_id=None,
        single_use_transaction=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Commits a transaction. The request includes the mutations to be applied
        to rows in the database.

        ``Commit`` might return an ``ABORTED`` error. This can occur at any
        time; commonly, the cause is conflicts with concurrent transactions.
        However, it can also happen for a variety of other reasons. If
        ``Commit`` returns ``ABORTED``, the caller should re-attempt the
        transaction from the beginning, re-using the same session.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `mutations`:
            >>> mutations = []
            >>>
            >>> response = client.commit(session, mutations)

        Args:
            session (str): Required. The session in which the transaction to be committed is running.
            mutations (list[Union[dict, ~google.cloud.spanner_v1.types.Mutation]]): The mutations to be executed when this transaction commits. All
                mutations are applied atomically, in the order they appear in
                this list.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Mutation`
            transaction_id (bytes): Commit a previously-started transaction.
            single_use_transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionOptions]): Execute mutations in a temporary transaction. Note that unlike commit of
                a previously-started transaction, commit with a temporary transaction is
                non-idempotent. That is, if the ``CommitRequest`` is sent to Cloud
                Spanner more than once (for instance, due to retries in the application,
                or in the transport library), it is possible that the mutations are
                executed more than once. If this is undesirable, use
                ``BeginTransaction`` and ``Commit`` instead.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.CommitResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "commit" not in self._inner_api_calls:
            self._inner_api_calls[
                "commit"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.commit,
                default_retry=self._method_configs["Commit"].retry,
                default_timeout=self._method_configs["Commit"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            transaction_id=transaction_id, single_use_transaction=single_use_transaction
        )

        request = spanner_pb2.CommitRequest(
            session=session,
            mutations=mutations,
            transaction_id=transaction_id,
            single_use_transaction=single_use_transaction,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["commit"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def rollback(
        self,
        session,
        transaction_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Rolls back a transaction, releasing any locks it holds. It is a good
        idea to call this for any transaction that includes one or more ``Read``
        or ``ExecuteSql`` requests and ultimately decides not to commit.

        ``Rollback`` returns ``OK`` if it successfully aborts the transaction,
        the transaction was already aborted, or the transaction is not found.
        ``Rollback`` never returns ``ABORTED``.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `transaction_id`:
            >>> transaction_id = b''
            >>>
            >>> client.rollback(session, transaction_id)

        Args:
            session (str): Required. The session in which the transaction to roll back is running.
            transaction_id (bytes): Required. The transaction to roll back.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "rollback" not in self._inner_api_calls:
            self._inner_api_calls[
                "rollback"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.rollback,
                default_retry=self._method_configs["Rollback"].retry,
                default_timeout=self._method_configs["Rollback"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.RollbackRequest(
            session=session, transaction_id=transaction_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["rollback"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def partition_query(
        self,
        session,
        sql,
        transaction=None,
        params=None,
        param_types=None,
        partition_options=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a set of partition tokens that can be used to execute a query
        operation in parallel. Each of the returned partition tokens can be used
        by ``ExecuteStreamingSql`` to specify a subset of the query result to
        read. The same session and read-only transaction must be used by the
        PartitionQueryRequest used to create the partition tokens and the
        ExecuteSqlRequests that use the partition tokens.

        Partition tokens become invalid when the session used to create them is
        deleted, is idle for too long, begins a new transaction, or becomes too
        old. When any of these happen, it is not possible to resume the query,
        and the whole operation must be restarted from the beginning.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `sql`:
            >>> sql = ''
            >>>
            >>> response = client.partition_query(session, sql)

        Args:
            session (str): Required. The session used to create the partitions.
            sql (str): The query request to generate partitions for. The request will fail if
                the query is not root partitionable. The query plan of a root
                partitionable query has a single distributed union operator. A
                distributed union operator conceptually divides one or more tables into
                multiple splits, remotely evaluates a subquery independently on each
                split, and then unions all results.

                This must not contain DML commands, such as INSERT, UPDATE, or DELETE.
                Use ``ExecuteStreamingSql`` with a PartitionedDml transaction for large,
                partition-friendly DML operations.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): Read only snapshot transactions are supported, read/write and single use
                transactions are not.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            params (Union[dict, ~google.cloud.spanner_v1.types.Struct]): The SQL query string can contain parameter placeholders. A parameter
                placeholder consists of ``'@'`` followed by the parameter name.
                Parameter names consist of any combination of letters, numbers, and
                underscores.

                Parameters can appear anywhere that a literal value is expected. The
                same parameter name can be used more than once, for example:
                ``"WHERE id > @msg_id AND id < @msg_id + 100"``

                It is an error to execute an SQL query with unbound parameters.

                Parameter values are specified using ``params``, which is a JSON object
                whose keys are parameter names, and whose values are the corresponding
                parameter values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Struct`
            param_types (dict[str -> Union[dict, ~google.cloud.spanner_v1.types.Type]]): It is not always possible for Cloud Spanner to infer the right SQL type
                from a JSON value. For example, values of type ``BYTES`` and values of
                type ``STRING`` both appear in ``params`` as JSON strings.

                In these cases, ``param_types`` can be used to specify the exact SQL
                type for some or all of the SQL query parameters. See the definition of
                ``Type`` for more information about SQL types.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Type`
            partition_options (Union[dict, ~google.cloud.spanner_v1.types.PartitionOptions]): Additional options that affect how many partitions are created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.PartitionOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.PartitionResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "partition_query" not in self._inner_api_calls:
            self._inner_api_calls[
                "partition_query"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.partition_query,
                default_retry=self._method_configs["PartitionQuery"].retry,
                default_timeout=self._method_configs["PartitionQuery"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.PartitionQueryRequest(
            session=session,
            sql=sql,
            transaction=transaction,
            params=params,
            param_types=param_types,
            partition_options=partition_options,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["partition_query"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def partition_read(
        self,
        session,
        table,
        key_set,
        transaction=None,
        index=None,
        columns=None,
        partition_options=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a set of partition tokens that can be used to execute a read
        operation in parallel. Each of the returned partition tokens can be used
        by ``StreamingRead`` to specify a subset of the read result to read. The
        same session and read-only transaction must be used by the
        PartitionReadRequest used to create the partition tokens and the
        ReadRequests that use the partition tokens. There are no ordering
        guarantees on rows returned among the returned partition tokens, or even
        within each individual StreamingRead call issued with a
        partition\_token.

        Partition tokens become invalid when the session used to create them is
        deleted, is idle for too long, begins a new transaction, or becomes too
        old. When any of these happen, it is not possible to resume the read,
        and the whole operation must be restarted from the beginning.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `table`:
            >>> table = ''
            >>>
            >>> # TODO: Initialize `key_set`:
            >>> key_set = {}
            >>>
            >>> response = client.partition_read(session, table, key_set)

        Args:
            session (str): Required. The session used to create the partitions.
            table (str): Required. The name of the table in the database to be read.
            key_set (Union[dict, ~google.cloud.spanner_v1.types.KeySet]): Required. ``key_set`` identifies the rows to be yielded. ``key_set``
                names the primary keys of the rows in ``table`` to be yielded, unless
                ``index`` is present. If ``index`` is present, then ``key_set`` instead
                names index keys in ``index``.

                It is not an error for the ``key_set`` to name rows that do not exist in
                the database. Read yields nothing for nonexistent rows.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.KeySet`
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): Read only snapshot transactions are supported, read/write and single use
                transactions are not.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            index (str): If non-empty, the name of an index on ``table``. This index is used
                instead of the table primary key when interpreting ``key_set`` and
                sorting result rows. See ``key_set`` for further information.
            columns (list[str]): The columns of ``table`` to be returned for each row matching this
                request.
            partition_options (Union[dict, ~google.cloud.spanner_v1.types.PartitionOptions]): Additional options that affect how many partitions are created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.PartitionOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.PartitionResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "partition_read" not in self._inner_api_calls:
            self._inner_api_calls[
                "partition_read"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.partition_read,
                default_retry=self._method_configs["PartitionRead"].retry,
                default_timeout=self._method_configs["PartitionRead"].timeout,
                client_info=self._client_info,
            )

        request = spanner_pb2.PartitionReadRequest(
            session=session,
            table=table,
            key_set=key_set,
            transaction=transaction,
            index=index,
            columns=columns,
            partition_options=partition_options,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["partition_read"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
