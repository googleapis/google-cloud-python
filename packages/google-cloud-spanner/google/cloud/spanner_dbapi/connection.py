# Copyright 2020 Google LLC All rights reserved.
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

"""DB-API Connection for the Google Cloud Spanner."""

import warnings

from google.api_core.gapic_v1.client_info import ClientInfo
from google.cloud import spanner_v1 as spanner

from google.cloud.spanner_dbapi.cursor import Cursor
from google.cloud.spanner_dbapi.exceptions import InterfaceError
from google.cloud.spanner_dbapi.version import DEFAULT_USER_AGENT
from google.cloud.spanner_dbapi.version import PY_VERSION


AUTOCOMMIT_MODE_WARNING = "This method is non-operational in autocommit mode"


class Connection:
    """Representation of a DB-API connection to a Cloud Spanner database.

    You most likely don't need to instantiate `Connection` objects
    directly, use the `connect` module function instead.

    :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
    :param instance: Cloud Spanner instance to connect to.

    :type database: :class:`~google.cloud.spanner_v1.database.Database`
    :param database: The database to which the connection is linked.
    """

    def __init__(self, instance, database):
        self._instance = instance
        self._database = database
        self._ddl_statements = []

        self._transaction = None
        self._session = None

        self.is_closed = False
        self._autocommit = False

    @property
    def autocommit(self):
        """Autocommit mode flag for this connection.

        :rtype: bool
        :returns: Autocommit mode flag value.
        """
        return self._autocommit

    @autocommit.setter
    def autocommit(self, value):
        """Change this connection autocommit mode. Setting this value to True
        while a transaction is active will commit the current transaction.

        :type value: bool
        :param value: New autocommit mode state.
        """
        if value and not self._autocommit:
            self.commit()

        self._autocommit = value

    @property
    def database(self):
        """Database to which this connection relates.

        :rtype: :class:`~google.cloud.spanner_v1.database.Database`
        :returns: The related database object.
        """
        return self._database

    @property
    def instance(self):
        """Instance to which this connection relates.

        :rtype: :class:`~google.cloud.spanner_v1.instance.Instance`
        :returns: The related instance object.
        """
        return self._instance

    def _session_checkout(self):
        """Get a Cloud Spanner session from the pool.

        If there is already a session associated with
        this connection, it'll be used instead.

        :rtype: :class:`google.cloud.spanner_v1.session.Session`
        :returns: Cloud Spanner session object ready to use.
        """
        if not self._session:
            self._session = self.database._pool.get()

        return self._session

    def _release_session(self):
        """Release the currently used Spanner session.

        The session will be returned into the sessions pool.
        """
        self.database._pool.put(self._session)
        self._session = None

    def transaction_checkout(self):
        """Get a Cloud Spanner transaction.

        Begin a new transaction, if there is no transaction in
        this connection yet. Return the begun one otherwise.

        The method is non operational in autocommit mode.

        :rtype: :class:`google.cloud.spanner_v1.transaction.Transaction`
        :returns: A Cloud Spanner transaction object, ready to use.
        """
        if not self.autocommit:
            if (
                not self._transaction
                or self._transaction.committed
                or self._transaction.rolled_back
            ):
                self._transaction = self._session_checkout().transaction()
                self._transaction.begin()

            return self._transaction

    def _raise_if_closed(self):
        """Helper to check the connection state before running a query.
        Raises an exception if this connection is closed.

        :raises: :class:`InterfaceError`: if this connection is closed.
        """
        if self.is_closed:
            raise InterfaceError("connection is already closed")

    def close(self):
        """Closes this connection.

        The connection will be unusable from this point forward. If the
        connection has an active transaction, it will be rolled back.
        """
        if (
            self._transaction
            and not self._transaction.committed
            and not self._transaction.rolled_back
        ):
            self._transaction.rollback()

        self.is_closed = True

    def commit(self):
        """Commits any pending transaction to the database.

        This method is non-operational in autocommit mode.
        """
        if self._autocommit:
            warnings.warn(AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2)
        elif self._transaction:
            self._transaction.commit()
            self._release_session()

    def rollback(self):
        """Rolls back any pending transaction.

        This is a no-op if there is no active transaction or if the connection
        is in autocommit mode.
        """
        if self._autocommit:
            warnings.warn(AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2)
        elif self._transaction:
            self._transaction.rollback()
            self._release_session()

    def cursor(self):
        """Factory to create a DB-API Cursor."""
        self._raise_if_closed()

        return Cursor(self)

    def run_prior_DDL_statements(self):
        self._raise_if_closed()

        if self._ddl_statements:
            ddl_statements = self._ddl_statements
            self._ddl_statements = []

            return self.database.update_ddl(ddl_statements).result()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.commit()
        self.close()


def connect(
    instance_id, database_id, project=None, credentials=None, pool=None, user_agent=None
):
    """Creates a connection to a Google Cloud Spanner database.

    :type instance_id: str
    :param instance_id: The ID of the instance to connect to.

    :type database_id: str
    :param database_id: The ID of the database to connect to.

    :type project: str
    :param project: (Optional) The ID of the project which owns the
                    instances, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The authorization credentials to attach to
                        requests. These credentials identify this application
                        to the service. If none are specified, the client will
                        attempt to ascertain the credentials from the
                        environment.

    :type pool: Concrete subclass of
                :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`.
    :param pool: (Optional). Session pool to be used by database.

    :type user_agent: str
    :param user_agent: (Optional) User agent to be used with this connection's
                       requests.

    :rtype: :class:`google.cloud.spanner_dbapi.connection.Connection`
    :returns: Connection object associated with the given Google Cloud Spanner
              resource.

    :raises: :class:`ValueError` in case of given instance/database
             doesn't exist.
    """

    client_info = ClientInfo(
        user_agent=user_agent or DEFAULT_USER_AGENT, python_version=PY_VERSION
    )

    client = spanner.Client(
        project=project, credentials=credentials, client_info=client_info
    )

    instance = client.instance(instance_id)
    if not instance.exists():
        raise ValueError("instance '%s' does not exist." % instance_id)

    database = instance.database(database_id, pool=pool)
    if not database.exists():
        raise ValueError("database '%s' does not exist." % database_id)

    return Connection(instance, database)
