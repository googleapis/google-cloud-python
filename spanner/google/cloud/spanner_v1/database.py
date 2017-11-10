# Copyright 2016 Google LLC All rights reserved.
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

import re
import threading

import google.auth.credentials
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.cloud.spanner_v1.gapic.spanner_client import SpannerClient
from grpc import StatusCode
import six

# pylint: disable=ungrouped-imports
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.spanner_v1 import __version__
from google.cloud.spanner_v1._helpers import _options_with_prefix
from google.cloud.spanner_v1.batch import Batch
from google.cloud.spanner_v1.pool import BurstyPool
from google.cloud.spanner_v1.pool import SessionCheckout
from google.cloud.spanner_v1.session import Session
from google.cloud.spanner_v1.snapshot import Snapshot
# pylint: enable=ungrouped-imports


SPANNER_DATA_SCOPE = 'https://www.googleapis.com/auth/spanner.data'


_DATABASE_NAME_RE = re.compile(
    r'^projects/(?P<project>[^/]+)/'
    r'instances/(?P<instance_id>[a-z][-a-z0-9]*)/'
    r'databases/(?P<database_id>[a-z][a-z0-9_\-]*[a-z0-9])$'
    )


class Database(object):
    """Representation of a Cloud Spanner Database.

    We can use a :class:`Database` to:

    * :meth:`create` the database
    * :meth:`reload` the database
    * :meth:`update` the database
    * :meth:`drop` the database

    :type database_id: str
    :param database_id: The ID of the database.

    :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
    :param instance: The instance that owns the database.

    :type ddl_statements: list of string
    :param ddl_statements: (Optional) DDL statements, excluding the
                           CREATE DATABASE statement.

    :type pool: concrete subclass of
                :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`.
    :param pool: (Optional) session pool to be used by database.  If not
                 passed, the database will construct an instance of
                 :class:`~google.cloud.spanner_v1.pool.BurstyPool`.
    """

    _spanner_api = None

    def __init__(self, database_id, instance, ddl_statements=(), pool=None):
        self.database_id = database_id
        self._instance = instance
        self._ddl_statements = _check_ddl_statements(ddl_statements)
        self._local = threading.local()

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

        :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
        :param instance: The instance that owns the database.

        :type pool: concrete subclass of
                    :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`.
        :param pool: (Optional) session pool to be used by database.

        :rtype: :class:`Database`
        :returns: The database parsed from the protobuf response.
        :raises ValueError:
            if the instance name does not match the expected format
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

        See
        cloud.google.com/spanner/docs/data-definition-language

        :rtype: sequence of string
        :returns: the statements
        """
        return self._ddl_statements

    @property
    def spanner_api(self):
        """Helper for session-related API calls."""
        if self._spanner_api is None:
            credentials = self._instance._client.credentials
            if isinstance(credentials, google.auth.credentials.Scoped):
                credentials = credentials.with_scopes((SPANNER_DATA_SCOPE,))
            self._spanner_api = SpannerClient(
                lib_name='gccl',
                lib_version=__version__,
                credentials=credentials,
            )
        return self._spanner_api

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (other.database_id == self.database_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self == other

    def create(self):
        """Create this database within its instance

        Inclues any configured schema assigned to :attr:`ddl_statements`.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.CreateDatabase

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: a future used to poll the status of the create request
        :raises Conflict: if the database already exists
        :raises NotFound: if the instance owning the database does not exist
        :raises GaxError:
            for errors other than ``ALREADY_EXISTS`` returned from the call
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

        return future

    def exists(self):
        """Test whether this database exists.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDDL

        :rtype: bool
        :returns: True if the database exists, else false.
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
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

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDDL

        :raises NotFound: if the database does not exist
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
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

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.UpdateDatabase

        :rtype: :class:`google.api_core.operation.Operation`
        :returns: an operation instance
        :raises NotFound: if the database does not exist
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
        """
        client = self._instance._client
        api = client.database_admin_api
        options = _options_with_prefix(self.name)

        try:
            future = api.update_database_ddl(
                self.name, ddl_statements, '', options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

        return future

    def drop(self):
        """Drop this database.

        See
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

        :rtype: :class:`~google.cloud.spanner_v1.session.Session`
        :returns: a session bound to this database.
        """
        return Session(self)

    def snapshot(self, **kw):
        """Return an object which wraps a snapshot.

        The wrapper *must* be used as a context manager, with the snapshot
        as the value returned by the wrapper.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.TransactionOptions.ReadOnly

        :type kw: dict
        :param kw:
            Passed through to
            :class:`~google.cloud.spanner_v1.snapshot.Snapshot` constructor.

        :rtype: :class:`~google.cloud.spanner_v1.database.SnapshotCheckout`
        :returns: new wrapper
        """
        return SnapshotCheckout(self, **kw)

    def batch(self):
        """Return an object which wraps a batch.

        The wrapper *must* be used as a context manager, with the batch
        as the value returned by the wrapper.

        :rtype: :class:`~google.cloud.spanner_v1.database.BatchCheckout`
        :returns: new wrapper
        """
        return BatchCheckout(self)

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
        # Sanity check: Is there a transaction already running?
        # If there is, then raise a red flag. Otherwise, mark that this one
        # is running.
        if getattr(self._local, 'transaction_running', False):
            raise RuntimeError('Spanner does not support nested transactions.')
        self._local.transaction_running = True

        # Check out a session and run the function in a transaction; once
        # done, flip the sanity check bit back.
        try:
            with SessionCheckout(self._pool) as session:
                return session.run_in_transaction(func, *args, **kw)
        finally:
            self._local.transaction_running = False


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

    :type kw: dict
    :param kw:
        Passed through to
        :class:`~google.cloud.spanner_v1.snapshot.Snapshot` constructor.
    """
    def __init__(self, database, **kw):
        self._database = database
        self._session = None
        self._kw = kw

    def __enter__(self):
        """Begin ``with`` block."""
        session = self._session = self._database._pool.get()
        return Snapshot(session, **self._kw)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End ``with`` block."""
        self._database._pool.put(self._session)


def _check_ddl_statements(value):
    """Validate DDL Statements used to define database schema.

    See
    https://cloud.google.com/spanner/docs/data-definition-language

    :type value: list of string
    :param value: DDL statements, excluding the 'CREATE DATABSE' statement

    :rtype: tuple
    :returns: tuple of validated DDL statement strings.
    :raises ValueError:
        if elements in ``value`` are not strings, or if ``value`` contains
        a ``CREATE DATABASE`` statement.
    """
    if not all(isinstance(line, six.string_types) for line in value):
        raise ValueError("Pass a list of strings")

    if any('create database' in line.lower() for line in value):
        raise ValueError("Do not pass a 'CREATE DATABASE' statement")

    return tuple(value)
