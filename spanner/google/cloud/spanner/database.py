# Copyright 2016 Google Inc. All rights reserved.
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

"""User friendly container for Cloud Spanner Database."""

import functools
import re

from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.gax import _OperationFuture
from google.cloud.proto.spanner.admin.database.v1 import (
    spanner_database_admin_pb2 as admin_v1_pb2)
from google.cloud.gapic.spanner.v1.spanner_client import SpannerClient
from grpc import StatusCode
import six

# pylint: disable=ungrouped-imports
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.operation import register_type
from google.cloud.spanner import __version__
from google.cloud.spanner._helpers import _options_with_prefix
from google.cloud.spanner.batch import Batch
from google.cloud.spanner.session import Session
from google.cloud.spanner.pool import BurstyPool
from google.cloud.spanner.snapshot import Snapshot
from google.cloud.spanner.pool import SessionCheckout
# pylint: enable=ungrouped-imports


_DATABASE_NAME_RE = re.compile(
    r'^projects/(?P<project>[^/]+)/'
    r'instances/(?P<instance_id>[a-z][-a-z0-9]*)/'
    r'databases/(?P<database_id>[a-z][a-z0-9_\-]*[a-z0-9])$'
    )

register_type(admin_v1_pb2.Database)
register_type(admin_v1_pb2.CreateDatabaseMetadata)
register_type(admin_v1_pb2.UpdateDatabaseDdlMetadata)


class _BrokenResultFuture(_OperationFuture):
    """An _OperationFuture subclass that is permissive about type mismatches
    in results, and simply returns an empty-ish object if they happen.

    This class exists to get past a contra-spec result on
    `update_database_ddl`; since the result is empty there is no
    critical loss.
    """
    @functools.wraps(_OperationFuture.result)
    def result(self, *args, **kwargs):
        try:
            return super(_BrokenResultFuture, self).result(*args, **kwargs)
        except TypeError:
            return self._result_type()


class Database(object):
    """Representation of a Cloud Spanner Database.

    We can use a :class:`Database` to:

    * :meth:`create` the database
    * :meth:`reload` the database
    * :meth:`update` the database
    * :meth:`drop` the database

    :type database_id: str
    :param database_id: The ID of the database.

    :type instance: :class:`~google.cloud.spanner.instance.Instance`
    :param instance: The instance that owns the database.

    :type ddl_statements: list of string
    :param ddl_statements: (Optional) DDL statements, excluding the
                           CREATE DATABASE statement.

    :type pool: concrete subclass of
                :class:`~google.cloud.spanner.pool.AbstractSessionPool`.
    :param pool: (Optional) session pool to be used by database.  If not
                 passed, the database will construct an instance of
                 :class:`~google.cloud.spanner.pool.BurstyPool`.
    """

    _spanner_api = None

    def __init__(self, database_id, instance, ddl_statements=(), pool=None):
        self.database_id = database_id
        self._instance = instance
        self._ddl_statements = _check_ddl_statements(ddl_statements)

        if pool is None:
            pool = BurstyPool()

        self._pool = pool
        pool.bind(self)

    @classmethod
    def from_pb(cls, database_pb, instance, pool=None):
        """Creates an instance of this class from a protobuf.

        :type database_pb:
            :class:`google.spanner.v2.spanner_instance_admin_pb2.Instance`
        :param database_pb: A instance protobuf object.

        :type instance: :class:`~google.cloud.spanner.instance.Instance`
        :param instance: The instance that owns the database.

        :type pool: concrete subclass of
                    :class:`~google.cloud.spanner.pool.AbstractSessionPool`.
        :param pool: (Optional) session pool to be used by database.

        :rtype: :class:`Database`
        :returns: The database parsed from the protobuf response.
        :raises:
            :class:`ValueError <exceptions.ValueError>` if the instance
            name does not match the expected format
            or if the parsed project ID does not match the project ID
            on the instance's client, or if the parsed instance ID does
            not match the instance's ID.
        """
        match = _DATABASE_NAME_RE.match(database_pb.name)
        if match is None:
            raise ValueError('Database protobuf name was not in the '
                             'expected format.', database_pb.name)
        if match.group('project') != instance._client.project:
            raise ValueError('Project ID on database does not match the '
                             'project ID on the instance\'s client')
        instance_id = match.group('instance_id')
        if instance_id != instance.instance_id:
            raise ValueError('Instance ID on database does not match the '
                             'Instance ID on the instance')
        database_id = match.group('database_id')

        return cls(database_id, instance, pool=pool)

    @property
    def name(self):
        """Database name used in requests.

        .. note::

          This property will not change if ``database_id`` does not, but the
          return value is not cached.

        The database name is of the form

            ``"projects/../instances/../databases/{database_id}"``

        :rtype: str
        :returns: The database name.
        """
        return self._instance.name + '/databases/' + self.database_id

    @property
    def ddl_statements(self):
        """DDL Statements used to define database schema.

        See:
        cloud.google.com/spanner/docs/data-definition-language

        :rtype: sequence of string
        :returns: the statements
        """
        return self._ddl_statements

    @property
    def spanner_api(self):
        """Helper for session-related API calls."""
        if self._spanner_api is None:
            self._spanner_api = SpannerClient(
                lib_name='gccl', lib_version=__version__)
        return self._spanner_api

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.database_id == self.database_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self.__eq__(other)

    def create(self):
        """Create this database within its instance

        Inclues any configured schema assigned to :attr:`ddl_statements`.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.CreateDatabase
        """
        api = self._instance._client.database_admin_api
        options = _options_with_prefix(self.name)
        db_name = self.database_id
        if '-' in db_name:
            db_name = '`%s`' % (db_name,)

        try:
            future = api.create_database(
                parent=self._instance.name,
                create_statement='CREATE DATABASE %s' % (db_name,),
                extra_statements=list(self._ddl_statements),
                options=options,
            )
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.ALREADY_EXISTS:
                raise Conflict(self.name)
            elif exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound('Instance not found: {name}'.format(
                    name=self._instance.name,
                ))
            raise

        future.caller_metadata = {'request_type': 'CreateDatabase'}
        return future

    def exists(self):
        """Test whether this database exists.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDDL
        """
        api = self._instance._client.database_admin_api
        options = _options_with_prefix(self.name)

        try:
            api.get_database_ddl(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                return False
            raise
        return True

    def reload(self):
        """Reload this database.

        Refresh any configured schema into :attr:`ddl_statements`.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDDL
        """
        api = self._instance._client.database_admin_api
        options = _options_with_prefix(self.name)

        try:
            response = api.get_database_ddl(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise
        self._ddl_statements = tuple(response.statements)

    def update_ddl(self, ddl_statements):
        """Update DDL for this database.

        Apply any configured schema from :attr:`ddl_statements`.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.UpdateDatabase

        :rtype: :class:`google.cloud.operation.Operation`
        :returns: an operation instance
        """
        client = self._instance._client
        api = client.database_admin_api
        options = _options_with_prefix(self.name)

        try:
            future = api.update_database_ddl(
                self.name, ddl_statements, '', options=options)
            future.__class__ = _BrokenResultFuture
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

        future.caller_metadata = {'request_type': 'UpdateDatabaseDdl'}
        return future

    def drop(self):
        """Drop this database.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.DropDatabase
        """
        api = self._instance._client.database_admin_api
        options = _options_with_prefix(self.name)

        try:
            api.drop_database(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

    def session(self):
        """Factory to create a session for this database.

        :rtype: :class:`~google.cloud.spanner.session.Session`
        :returns: a session bound to this database.
        """
        return Session(self)

    def read(self, table, columns, keyset, index='', limit=0,
             resume_token=b''):
        """Perform a ``StreamingRead`` API request for rows in a table.

        :type table: str
        :param table: name of the table from which to fetch data

        :type columns: list of str
        :param columns: names of columns to be retrieved

        :type keyset: :class:`~google.cloud.spanner.keyset.KeySet`
        :param keyset: keys / ranges identifying rows to be retrieved

        :type index: str
        :param index: (Optional) name of index to use, rather than the
                      table's primary key

        :type limit: int
        :param limit: (Optional) maxiumn number of rows to return

        :type resume_token: bytes
        :param resume_token: token for resuming previously-interrupted read

        :rtype: :class:`~google.cloud.spanner.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        with SessionCheckout(self._pool) as session:
            return session.read(
                table, columns, keyset, index, limit, resume_token)

    def execute_sql(self, sql, params=None, param_types=None, query_mode=None,
                    resume_token=b''):
        """Perform an ``ExecuteStreamingSql`` API request.

        :type sql: str
        :param sql: SQL query statement

        :type params: dict, {str -> column value}
        :param params: values for parameter replacement.  Keys must match
                       the names used in ``sql``.

        :type param_types:
            dict, {str -> :class:`google.spanner.v1.type_pb2.TypeCode`}
        :param param_types: (Optional) explicit types for one or more param
                            values;  overrides default type detection on the
                            back-end.

        :type query_mode:
            :class:`google.spanner.v1.spanner_pb2.ExecuteSqlRequest.QueryMode`
        :param query_mode: Mode governing return of results / query plan. See:
            https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.ExecuteSqlRequest.QueryMode1

        :type resume_token: bytes
        :param resume_token: token for resuming previously-interrupted query

        :rtype: :class:`~google.cloud.spanner.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        with SessionCheckout(self._pool) as session:
            return session.execute_sql(
                sql, params, param_types, query_mode, resume_token)

    def run_in_transaction(self, func, *args, **kw):
        """Perform a unit of work in a transaction, retrying on abort.

        :type func: callable
        :param func: takes a required positional argument, the transaction,
                     and additional positional / keyword arguments as supplied
                     by the caller.

        :type args: tuple
        :param args: additional positional arguments to be passed to ``func``.

        :type kw: dict
        :param kw: optional keyword arguments to be passed to ``func``.
                   If passed, "timeout_secs" will be removed and used to
                   override the default timeout.

        :rtype: :class:`datetime.datetime`
        :returns: timestamp of committed transaction
        """
        with SessionCheckout(self._pool) as session:
            return session.run_in_transaction(func, *args, **kw)

    def batch(self):
        """Return an object which wraps a batch.

        The wrapper *must* be used as a context manager, with the batch
        as the value returned by the wrapper.

        :rtype: :class:`~google.cloud.spanner.database.BatchCheckout`
        :returns: new wrapper
        """
        return BatchCheckout(self)

    def snapshot(self, read_timestamp=None, min_read_timestamp=None,
                 max_staleness=None, exact_staleness=None):
        """Return an object which wraps a snapshot.

        The wrapper *must* be used as a context manager, with the snapshot
        as the value returned by the wrapper.

        See:
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.TransactionOptions.ReadOnly

        If no options are passed, reads will use the ``strong`` model, reading
        at a timestamp where all previously committed transactions are visible.

        :type read_timestamp: :class:`datetime.datetime`
        :param read_timestamp: Execute all reads at the given timestamp.

        :type min_read_timestamp: :class:`datetime.datetime`
        :param min_read_timestamp: Execute all reads at a
                                   timestamp >= ``min_read_timestamp``.

        :type max_staleness: :class:`datetime.timedelta`
        :param max_staleness: Read data at a
                              timestamp >= NOW - ``max_staleness`` seconds.

        :type exact_staleness: :class:`datetime.timedelta`
        :param exact_staleness: Execute all reads at a timestamp that is
                                ``exact_staleness`` old.

        :rtype: :class:`~google.cloud.spanner.snapshot.Snapshot`
        :returns: a snapshot bound to this session
        :raises: :exc:`ValueError` if the session has not yet been created.

        :rtype: :class:`~google.cloud.spanner.database.SnapshotCheckout`
        :returns: new wrapper
        """
        return SnapshotCheckout(
            self,
            read_timestamp=read_timestamp,
            min_read_timestamp=min_read_timestamp,
            max_staleness=max_staleness,
            exact_staleness=exact_staleness,
        )


class BatchCheckout(object):
    """Context manager for using a batch from a database.

    Inside the context manager, checks out a session from the database,
    creates a batch from it, making the batch available.

    Caller must *not* use the batch to perform API requests outside the scope
    of the context manager.

    :type database: :class:`~google.cloud.spannder.database.Database`
    :param database: database to use
    """
    def __init__(self, database):
        self._database = database
        self._session = self._batch = None

    def __enter__(self):
        """Begin ``with`` block."""
        session = self._session = self._database._pool.get()
        batch = self._batch = Batch(session)
        return batch

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End ``with`` block."""
        try:
            if exc_type is None:
                self._batch.commit()
        finally:
            self._database._pool.put(self._session)


class SnapshotCheckout(object):
    """Context manager for using a snapshot from a database.

    Inside the context manager, checks out a session from the database,
    creates a snapshot from it, making the snapshot available.

    Caller must *not* use the snapshot to perform API requests outside the
    scope of the context manager.

    :type database: :class:`~google.cloud.spannder.database.Database`
    :param database: database to use

    :type read_timestamp: :class:`datetime.datetime`
    :param read_timestamp: Execute all reads at the given timestamp.

    :type min_read_timestamp: :class:`datetime.datetime`
    :param min_read_timestamp: Execute all reads at a
                               timestamp >= ``min_read_timestamp``.

    :type max_staleness: :class:`datetime.timedelta`
    :param max_staleness: Read data at a
                          timestamp >= NOW - ``max_staleness`` seconds.

    :type exact_staleness: :class:`datetime.timedelta`
    :param exact_staleness: Execute all reads at a timestamp that is
                            ``exact_staleness`` old.
    """
    def __init__(self, database, read_timestamp=None, min_read_timestamp=None,
                 max_staleness=None, exact_staleness=None):
        self._database = database
        self._session = None
        self._read_timestamp = read_timestamp
        self._min_read_timestamp = min_read_timestamp
        self._max_staleness = max_staleness
        self._exact_staleness = exact_staleness

    def __enter__(self):
        """Begin ``with`` block."""
        session = self._session = self._database._pool.get()
        return Snapshot(
            session,
            read_timestamp=self._read_timestamp,
            min_read_timestamp=self._min_read_timestamp,
            max_staleness=self._max_staleness,
            exact_staleness=self._exact_staleness,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End ``with`` block."""
        self._database._pool.put(self._session)


def _check_ddl_statements(value):
    """Validate DDL Statements used to define database schema.

    See:
    https://cloud.google.com/spanner/docs/data-definition-language

    :type value: list of string
    :param value: DDL statements, excluding the 'CREATE DATABSE' statement

    :rtype: tuple
    :returns: tuple of validated DDL statement strings.
    """
    if not all(isinstance(line, six.string_types) for line in value):
        raise ValueError("Pass a list of strings")

    if any('create database' in line.lower() for line in value):
        raise ValueError("Do not pass a 'CREATE DATABASE' statement")

    return tuple(value)
