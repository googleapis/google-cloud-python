# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/spanner/v1/spanner.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.spanner.v1 Spanner API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
from google.gax.utils import oneof
import google.gax

from google.cloud.spanner_v1.gapic import enums
from google.cloud.spanner_v1.gapic import spanner_client_config
from google.cloud.spanner_v1.proto import keys_pb2
from google.cloud.spanner_v1.proto import mutation_pb2
from google.cloud.spanner_v1.proto import spanner_pb2
from google.cloud.spanner_v1.proto import transaction_pb2
from google.protobuf import struct_pb2


class SpannerClient(object):
    """
    Cloud Spanner API

    The Cloud Spanner API can be used to manage sessions and execute
    transactions on data stored in Cloud Spanner databases.
    """

    SERVICE_ADDRESS = 'spanner.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/spanner.data', )

    _DATABASE_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/instances/{instance}/databases/{database}')
    _SESSION_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/instances/{instance}/databases/{database}/sessions/{session}'
    )

    @classmethod
    def database_path(cls, project, instance, database):
        """Returns a fully-qualified database resource name string."""
        return cls._DATABASE_PATH_TEMPLATE.render({
            'project': project,
            'instance': instance,
            'database': database,
        })

    @classmethod
    def session_path(cls, project, instance, database, session):
        """Returns a fully-qualified session resource name string."""
        return cls._SESSION_PATH_TEMPLATE.render({
            'project': project,
            'instance': instance,
            'database': database,
            'session': session,
        })

    @classmethod
    def match_project_from_database_name(cls, database_name):
        """Parses the project from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the project.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('project')

    @classmethod
    def match_instance_from_database_name(cls, database_name):
        """Parses the instance from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the instance.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('instance')

    @classmethod
    def match_database_from_database_name(cls, database_name):
        """Parses the database from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the database.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('database')

    @classmethod
    def match_project_from_session_name(cls, session_name):
        """Parses the project from a session resource.

        Args:
            session_name (str): A fully-qualified path representing a session
                resource.

        Returns:
            A string representing the project.
        """
        return cls._SESSION_PATH_TEMPLATE.match(session_name).get('project')

    @classmethod
    def match_instance_from_session_name(cls, session_name):
        """Parses the instance from a session resource.

        Args:
            session_name (str): A fully-qualified path representing a session
                resource.

        Returns:
            A string representing the instance.
        """
        return cls._SESSION_PATH_TEMPLATE.match(session_name).get('instance')

    @classmethod
    def match_database_from_session_name(cls, session_name):
        """Parses the database from a session resource.

        Args:
            session_name (str): A fully-qualified path representing a session
                resource.

        Returns:
            A string representing the database.
        """
        return cls._SESSION_PATH_TEMPLATE.match(session_name).get('database')

    @classmethod
    def match_session_from_session_name(cls, session_name):
        """Parses the session from a session resource.

        Args:
            session_name (str): A fully-qualified path representing a session
                resource.

        Returns:
            A string representing the session.
        """
        return cls._SESSION_PATH_TEMPLATE.match(session_name).get('session')

    def __init__(self,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
            channel (~grpc.Channel): A ``Channel`` instance through
                which to make calls.
            credentials (~google.auth.credentials.Credentials): The authorization
                credentials to attach to requests. These credentials identify this
                application to the service.
            ssl_credentials (~grpc.ChannelCredentials): A
                ``ChannelCredentials`` instance for use with an SSL-enabled
                channel.
            scopes (Sequence[str]): A list of OAuth2 scopes to attach to requests.
            client_config (dict):
                A dictionary for call options for each method. See
                :func:`google.gax.construct_settings` for the structure of
                this data. Falls back to the default config if not specified
                or the specified config is missing data points.
            lib_name (str): The API library software used for calling
                the service. (Unless you are writing an API client itself,
                leave this as default.)
            lib_version (str): The API library software version used
                for calling the service. (Unless you are writing an API client
                itself, leave this as default.)
            metrics_headers (dict): A dictionary of values for tracking
                client library metrics. Ultimately serializes to a string
                (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
                considered private.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'google-cloud-spanner', ).version

        # Load the configuration defaults.
        defaults = api_callable.construct_settings(
            'google.spanner.v1.Spanner',
            spanner_client_config.config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers, )
        self.spanner_stub = config.create_stub(
            spanner_pb2.SpannerStub,
            channel=channel,
            service_path=self.SERVICE_ADDRESS,
            service_port=self.DEFAULT_SERVICE_PORT,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self._create_session = api_callable.create_api_call(
            self.spanner_stub.CreateSession,
            settings=defaults['create_session'])
        self._get_session = api_callable.create_api_call(
            self.spanner_stub.GetSession, settings=defaults['get_session'])
        self._delete_session = api_callable.create_api_call(
            self.spanner_stub.DeleteSession,
            settings=defaults['delete_session'])
        self._execute_sql = api_callable.create_api_call(
            self.spanner_stub.ExecuteSql, settings=defaults['execute_sql'])
        self._execute_streaming_sql = api_callable.create_api_call(
            self.spanner_stub.ExecuteStreamingSql,
            settings=defaults['execute_streaming_sql'])
        self._read = api_callable.create_api_call(
            self.spanner_stub.Read, settings=defaults['read'])
        self._streaming_read = api_callable.create_api_call(
            self.spanner_stub.StreamingRead,
            settings=defaults['streaming_read'])
        self._begin_transaction = api_callable.create_api_call(
            self.spanner_stub.BeginTransaction,
            settings=defaults['begin_transaction'])
        self._commit = api_callable.create_api_call(
            self.spanner_stub.Commit, settings=defaults['commit'])
        self._rollback = api_callable.create_api_call(
            self.spanner_stub.Rollback, settings=defaults['rollback'])

    # Service calls
    def create_session(self, database, options=None):
        """
        Creates a new session. A session can be used to perform
        transactions that read and/or modify data in a Cloud Spanner database.
        Sessions are meant to be reused for many consecutive
        transactions.

        Sessions can only execute one transaction at a time. To execute
        multiple concurrent read-write/write-only transactions, create
        multiple sessions. Note that standalone reads and queries use a
        transaction internally, and count toward the one transaction
        limit.

        Cloud Spanner limits the number of sessions that can exist at any given
        time; thus, it is a good idea to delete idle and/or unneeded sessions.
        Aside from explicit deletes, Cloud Spanner can delete sessions for which no
        operations are sent for more than an hour. If a session is deleted,
        requests to it return ``NOT_FOUND``.

        Idle sessions can be kept alive by sending a trivial SQL query
        periodically, e.g., ``\"SELECT 1\"``.

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
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Session` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.CreateSessionRequest(database=database)
        return self._create_session(request, options)

    def get_session(self, name, options=None):
        """
        Gets a session. Returns ``NOT_FOUND`` if the session does not exist.
        This is mainly useful for determining whether a session is still
        alive.

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
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Session` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.GetSessionRequest(name=name)
        return self._get_session(request, options)

    def delete_session(self, name, options=None):
        """
        Ends a session, releasing server resources associated with it.

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
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.DeleteSessionRequest(name=name)
        self._delete_session(request, options)

    def execute_sql(self,
                    session,
                    sql,
                    transaction=None,
                    params=None,
                    param_types=None,
                    resume_token=None,
                    query_mode=None,
                    options=None):
        """
        Executes an SQL query, returning all rows in a single reply. This
        method cannot be used to return a result set larger than 10 MiB;
        if the query yields more data than that, the query fails with
        a ``FAILED_PRECONDITION`` error.

        Queries inside read-write transactions might return ``ABORTED``. If
        this occurs, the application should restart the transaction from
        the beginning. See ``Transaction`` for more details.

        Larger result sets can be fetched in streaming fashion by calling
        ``ExecuteStreamingSql`` instead.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> sql = ''
            >>>
            >>> response = client.execute_sql(session, sql)

        Args:
            session (str): Required. The session in which the SQL query should be performed.
            sql (str): Required. The SQL query string.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            params (Union[dict, ~google.cloud.spanner_v1.types.Struct]): The SQL query string can contain parameter placeholders. A parameter
                placeholder consists of ``'@'`` followed by the parameter
                name. Parameter names consist of any combination of letters,
                numbers, and underscores.

                Parameters can appear anywhere that a literal value is expected.  The same
                parameter name can be used more than once, for example:
                ``\"WHERE id > @msg_id AND id < @msg_id + 100\"``

                It is an error to execute an SQL query with unbound parameters.

                Parameter values are specified using ``params``, which is a JSON
                object whose keys are parameter names, and whose values are the
                corresponding parameter values.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Struct`
            param_types (dict[str -> Union[dict, ~google.cloud.spanner_v1.types.Type]]): It is not always possible for Cloud Spanner to infer the right SQL type
                from a JSON value.  For example, values of type ``BYTES`` and values
                of type ``STRING`` both appear in ``params`` as JSON strings.

                In these cases, ``param_types`` can be used to specify the exact
                SQL type for some or all of the SQL query parameters. See the
                definition of ``Type`` for more information
                about SQL types.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Type`
            resume_token (bytes): If this request is resuming a previously interrupted SQL query
                execution, ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this
                enables the new SQL query execution to resume where the last one left
                off. The rest of the request parameters must exactly match the
                request that yielded this token.
            query_mode (~google.cloud.spanner_v1.types.QueryMode): Used to control the amount of debugging information returned in
                ``ResultSetStats``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.ResultSet` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.ExecuteSqlRequest(
            session=session,
            sql=sql,
            transaction=transaction,
            params=params,
            param_types=param_types,
            resume_token=resume_token,
            query_mode=query_mode)
        return self._execute_sql(request, options)

    def execute_streaming_sql(self,
                              session,
                              sql,
                              transaction=None,
                              params=None,
                              param_types=None,
                              resume_token=None,
                              query_mode=None,
                              options=None):
        """
        Like ``ExecuteSql``, except returns the result
        set as a stream. Unlike ``ExecuteSql``, there
        is no limit on the size of the returned result set. However, no
        individual row in the result set can exceed 100 MiB, and no
        column value can exceed 10 MiB.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> sql = ''
            >>>
            >>> for element in client.execute_streaming_sql(session, sql):
            ...     # process element
            ...     pass

        Args:
            session (str): Required. The session in which the SQL query should be performed.
            sql (str): Required. The SQL query string.
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            params (Union[dict, ~google.cloud.spanner_v1.types.Struct]): The SQL query string can contain parameter placeholders. A parameter
                placeholder consists of ``'@'`` followed by the parameter
                name. Parameter names consist of any combination of letters,
                numbers, and underscores.

                Parameters can appear anywhere that a literal value is expected.  The same
                parameter name can be used more than once, for example:
                ``\"WHERE id > @msg_id AND id < @msg_id + 100\"``

                It is an error to execute an SQL query with unbound parameters.

                Parameter values are specified using ``params``, which is a JSON
                object whose keys are parameter names, and whose values are the
                corresponding parameter values.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Struct`
            param_types (dict[str -> Union[dict, ~google.cloud.spanner_v1.types.Type]]): It is not always possible for Cloud Spanner to infer the right SQL type
                from a JSON value.  For example, values of type ``BYTES`` and values
                of type ``STRING`` both appear in ``params`` as JSON strings.

                In these cases, ``param_types`` can be used to specify the exact
                SQL type for some or all of the SQL query parameters. See the
                definition of ``Type`` for more information
                about SQL types.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.Type`
            resume_token (bytes): If this request is resuming a previously interrupted SQL query
                execution, ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this
                enables the new SQL query execution to resume where the last one left
                off. The rest of the request parameters must exactly match the
                request that yielded this token.
            query_mode (~google.cloud.spanner_v1.types.QueryMode): Used to control the amount of debugging information returned in
                ``ResultSetStats``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.spanner_v1.types.PartialResultSet].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.ExecuteSqlRequest(
            session=session,
            sql=sql,
            transaction=transaction,
            params=params,
            param_types=param_types,
            resume_token=resume_token,
            query_mode=query_mode)
        return self._execute_streaming_sql(request, options)

    def read(self,
             session,
             table,
             columns,
             key_set,
             transaction=None,
             index=None,
             limit=None,
             resume_token=None,
             options=None):
        """
        Reads rows from the database using key lookups and scans, as a
        simple key/value style alternative to
        ``ExecuteSql``.  This method cannot be used to
        return a result set larger than 10 MiB; if the read matches more
        data than that, the read fails with a ``FAILED_PRECONDITION``
        error.

        Reads inside read-write transactions might return ``ABORTED``. If
        this occurs, the application should restart the transaction from
        the beginning. See ``Transaction`` for more details.

        Larger result sets can be yielded in streaming fashion by calling
        ``StreamingRead`` instead.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> table = ''
            >>> columns = []
            >>> key_set = {}
            >>>
            >>> response = client.read(session, table, columns, key_set)

        Args:
            session (str): Required. The session in which the read should be performed.
            table (str): Required. The name of the table in the database to be read.
            columns (list[str]): The columns of ``table`` to be returned for each row matching
                this request.
            key_set (Union[dict, ~google.cloud.spanner_v1.types.KeySet]): Required. ``key_set`` identifies the rows to be yielded. ``key_set`` names the
                primary keys of the rows in ``table`` to be yielded, unless ``index``
                is present. If ``index`` is present, then ``key_set`` instead names
                index keys in ``index``.

                Rows are yielded in table primary key order (if ``index`` is empty)
                or index key order (if ``index`` is non-empty).

                It is not an error for the ``key_set`` to name rows that do not
                exist in the database. Read yields nothing for nonexistent rows.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.KeySet`
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            index (str): If non-empty, the name of an index on ``table``. This index is
                used instead of the table primary key when interpreting ``key_set``
                and sorting result rows. See ``key_set`` for further information.
            limit (long): If greater than zero, only the first ``limit`` rows are yielded. If ``limit``
                is zero, the default is no limit.
            resume_token (bytes): If this request is resuming a previously interrupted read,
                ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this
                enables the new read to resume where the last read left off. The
                rest of the request parameters must exactly match the request
                that yielded this token.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.ResultSet` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.ReadRequest(
            session=session,
            table=table,
            columns=columns,
            key_set=key_set,
            transaction=transaction,
            index=index,
            limit=limit,
            resume_token=resume_token)
        return self._read(request, options)

    def streaming_read(self,
                       session,
                       table,
                       columns,
                       key_set,
                       transaction=None,
                       index=None,
                       limit=None,
                       resume_token=None,
                       options=None):
        """
        Like ``Read``, except returns the result set as a
        stream. Unlike ``Read``, there is no limit on the
        size of the returned result set. However, no individual row in
        the result set can exceed 100 MiB, and no column value can exceed
        10 MiB.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> table = ''
            >>> columns = []
            >>> key_set = {}
            >>>
            >>> for element in client.streaming_read(session, table, columns, key_set):
            ...     # process element
            ...     pass

        Args:
            session (str): Required. The session in which the read should be performed.
            table (str): Required. The name of the table in the database to be read.
            columns (list[str]): The columns of ``table`` to be returned for each row matching
                this request.
            key_set (Union[dict, ~google.cloud.spanner_v1.types.KeySet]): Required. ``key_set`` identifies the rows to be yielded. ``key_set`` names the
                primary keys of the rows in ``table`` to be yielded, unless ``index``
                is present. If ``index`` is present, then ``key_set`` instead names
                index keys in ``index``.

                Rows are yielded in table primary key order (if ``index`` is empty)
                or index key order (if ``index`` is non-empty).

                It is not an error for the ``key_set`` to name rows that do not
                exist in the database. Read yields nothing for nonexistent rows.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.KeySet`
            transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionSelector]): The transaction to use. If none is provided, the default is a
                temporary read-only transaction with strong concurrency.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionSelector`
            index (str): If non-empty, the name of an index on ``table``. This index is
                used instead of the table primary key when interpreting ``key_set``
                and sorting result rows. See ``key_set`` for further information.
            limit (long): If greater than zero, only the first ``limit`` rows are yielded. If ``limit``
                is zero, the default is no limit.
            resume_token (bytes): If this request is resuming a previously interrupted read,
                ``resume_token`` should be copied from the last
                ``PartialResultSet`` yielded before the interruption. Doing this
                enables the new read to resume where the last read left off. The
                rest of the request parameters must exactly match the request
                that yielded this token.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.spanner_v1.types.PartialResultSet].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.ReadRequest(
            session=session,
            table=table,
            columns=columns,
            key_set=key_set,
            transaction=transaction,
            index=index,
            limit=limit,
            resume_token=resume_token)
        return self._streaming_read(request, options)

    def begin_transaction(self, session, options_, options=None):
        """
        Begins a new transaction. This step can often be skipped:
        ``Read``, ``ExecuteSql`` and
        ``Commit`` can begin a new transaction as a
        side-effect.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> options_ = {}
            >>>
            >>> response = client.begin_transaction(session, options_)

        Args:
            session (str): Required. The session in which the transaction runs.
            options_ (Union[dict, ~google.cloud.spanner_v1.types.TransactionOptions]): Required. Options for the new transaction.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionOptions`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.Transaction` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.BeginTransactionRequest(
            session=session, options=options_)
        return self._begin_transaction(request, options)

    def commit(self,
               session,
               mutations,
               transaction_id=None,
               single_use_transaction=None,
               options=None):
        """
        Commits a transaction. The request includes the mutations to be
        applied to rows in the database.

        ``Commit`` might return an ``ABORTED`` error. This can occur at any time;
        commonly, the cause is conflicts with concurrent
        transactions. However, it can also happen for a variety of other
        reasons. If ``Commit`` returns ``ABORTED``, the caller should re-attempt
        the transaction from the beginning, re-using the same session.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
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
            single_use_transaction (Union[dict, ~google.cloud.spanner_v1.types.TransactionOptions]): Execute mutations in a temporary transaction. Note that unlike
                commit of a previously-started transaction, commit with a
                temporary transaction is non-idempotent. That is, if the
                ``CommitRequest`` is sent to Cloud Spanner more than once (for
                instance, due to retries in the application, or in the
                transport library), it is possible that the mutations are
                executed more than once. If this is undesirable, use
                ``BeginTransaction`` and
                ``Commit`` instead.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.TransactionOptions`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_v1.types.CommitResponse` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(
            transaction_id=transaction_id,
            single_use_transaction=single_use_transaction, )

        request = spanner_pb2.CommitRequest(
            session=session,
            mutations=mutations,
            transaction_id=transaction_id,
            single_use_transaction=single_use_transaction)
        return self._commit(request, options)

    def rollback(self, session, transaction_id, options=None):
        """
        Rolls back a transaction, releasing any locks it holds. It is a good
        idea to call this for any transaction that includes one or more
        ``Read`` or ``ExecuteSql`` requests and
        ultimately decides not to commit.

        ``Rollback`` returns ``OK`` if it successfully aborts the transaction, the
        transaction was already aborted, or the transaction is not
        found. ``Rollback`` never returns ``ABORTED``.

        Example:
            >>> from google.cloud import spanner_v1
            >>>
            >>> client = spanner_v1.SpannerClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[INSTANCE]', '[DATABASE]', '[SESSION]')
            >>> transaction_id = b''
            >>>
            >>> client.rollback(session, transaction_id)

        Args:
            session (str): Required. The session in which the transaction to roll back is running.
            transaction_id (bytes): Required. The transaction to roll back.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_pb2.RollbackRequest(
            session=session, transaction_id=transaction_id)
        self._rollback(request, options)
