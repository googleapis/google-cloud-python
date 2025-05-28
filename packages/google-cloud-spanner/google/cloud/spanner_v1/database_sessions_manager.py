# Copyright 2025 Google LLC All rights reserved.
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
import datetime
import threading
import time
import weakref

from google.api_core.exceptions import MethodNotImplemented

from google.cloud.spanner_v1._opentelemetry_tracing import (
    get_current_span,
    add_span_event,
)
from google.cloud.spanner_v1.session import Session
from google.cloud.spanner_v1.session_options import TransactionType


class DatabaseSessionsManager(object):
    """Manages sessions for a Cloud Spanner database.
    Sessions can be checked out from the database session manager for a specific
    transaction type using :meth:`get_session`, and returned to the session manager
    using :meth:`put_session`.
    The sessions returned by the session manager depend on the client's session options (see
    :class:`~google.cloud.spanner_v1.session_options.SessionOptions`) and the provided session
    pool (see :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`).
    :type database: :class:`~google.cloud.spanner_v1.database.Database`
    :param database: The database to manage sessions for.
    :type pool: :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`
    :param pool: The pool to get non-multiplexed sessions from.
    """

    # Intervals for the maintenance thread to check and refresh the multiplexed session.
    _MAINTENANCE_THREAD_POLLING_INTERVAL = datetime.timedelta(minutes=10)
    _MAINTENANCE_THREAD_REFRESH_INTERVAL = datetime.timedelta(days=7)

    def __init__(self, database, pool):
        self._database = database
        self._pool = pool

        # Declare multiplexed session attributes. When a multiplexed session for the
        # database session manager is created, a maintenance thread is initialized to
        # periodically delete and recreate the multiplexed session so that it remains
        # valid. Because of this concurrency, we need to use a lock whenever we access
        # the multiplexed session to avoid any race conditions. We also create an event
        # so that the thread can terminate if the use of multiplexed session has been
        # disabled for all transactions.
        self._multiplexed_session = None
        self._multiplexed_session_maintenance_thread = None
        self._multiplexed_session_lock = threading.Lock()
        self._is_multiplexed_sessions_disabled_event = threading.Event()

    @property
    def _logger(self):
        """The logger used by this database session manager.

        :rtype: :class:`logging.Logger`
        :returns: The logger.
        """
        return self._database.logger

    def get_session(self, transaction_type: TransactionType) -> Session:
        """Returns a session for the given transaction type from the database session manager.
        :rtype: :class:`~google.cloud.spanner_v1.session.Session`
        :returns: a session for the given transaction type.
        """

        session_options = self._database.session_options
        use_multiplexed = session_options.use_multiplexed(transaction_type)

        if use_multiplexed and transaction_type == TransactionType.READ_WRITE:
            raise NotImplementedError(
                f"Multiplexed sessions are not yet supported for {transaction_type} transactions."
            )

        if use_multiplexed:
            try:
                session = self._get_multiplexed_session()

            # If multiplexed sessions are not supported, disable
            # them for all transactions and return a non-multiplexed session.
            except MethodNotImplemented:
                self._disable_multiplexed_sessions()
                session = self._pool.get()

        else:
            session = self._pool.get()

        add_span_event(
            get_current_span(),
            "Using session",
            {"id": session.session_id, "multiplexed": session.is_multiplexed},
        )

        return session

    def put_session(self, session: Session) -> None:
        """Returns the session to the database session manager.
        :type session: :class:`~google.cloud.spanner_v1.session.Session`
        :param session: The session to return to the database session manager.
        """

        add_span_event(
            get_current_span(),
            "Returning session",
            {"id": session.session_id, "multiplexed": session.is_multiplexed},
        )

        # No action is needed for multiplexed sessions: the session
        # pool is only used for managing non-multiplexed sessions,
        # since they can only process one transaction at a time.
        if not session.is_multiplexed:
            self._pool.put(session)

    def _get_multiplexed_session(self) -> Session:
        """Returns a multiplexed session from the database session manager.
        If the multiplexed session is not defined, creates a new multiplexed
        session and starts a maintenance thread to periodically delete and
        recreate it so that it remains valid. Otherwise, simply returns the
        current multiplexed session.
        :raises MethodNotImplemented:
            if multiplexed sessions are not supported.
        :rtype: :class:`~google.cloud.spanner_v1.session.Session`
        :returns: a multiplexed session.
        """

        with self._multiplexed_session_lock:
            if self._multiplexed_session is None:
                self._multiplexed_session = self._build_multiplexed_session()

                # Build and start a thread to maintain the multiplexed session.
                self._multiplexed_session_maintenance_thread = (
                    self._build_maintenance_thread()
                )
                self._multiplexed_session_maintenance_thread.start()

            return self._multiplexed_session

    def _build_multiplexed_session(self) -> Session:
        """Builds and returns a new multiplexed session for the database session manager.
        :raises MethodNotImplemented:
            if multiplexed sessions are not supported.
        :rtype: :class:`~google.cloud.spanner_v1.session.Session`
        :returns: a new multiplexed session.
        """

        session = Session(
            database=self._database,
            database_role=self._database.database_role,
            is_multiplexed=True,
        )

        session.create()

        self._logger.info("Created multiplexed session.")

        return session

    def _disable_multiplexed_sessions(self) -> None:
        """Disables multiplexed sessions for all transactions."""

        self._multiplexed_session = None
        self._is_multiplexed_sessions_disabled_event.set()
        self._database.session_options.disable_multiplexed(self._logger)

    def _build_maintenance_thread(self) -> threading.Thread:
        """Builds and returns a multiplexed session maintenance thread for
        the database session manager. This thread will periodically delete
        and recreate the multiplexed session to ensure that it is always valid.
        :rtype: :class:`threading.Thread`
        :returns: a multiplexed session maintenance thread.
        """

        # Use a weak reference to the database session manager to avoid
        # creating a circular reference that would prevent the database
        # session manager from being garbage collected.
        session_manager_ref = weakref.ref(self)

        return threading.Thread(
            target=self._maintain_multiplexed_session,
            name=f"maintenance-multiplexed-session-{self._multiplexed_session.name}",
            args=[session_manager_ref],
            daemon=True,
        )

    @staticmethod
    def _maintain_multiplexed_session(session_manager_ref) -> None:
        """Maintains the multiplexed session for the database session manager.
        This method will delete and recreate the referenced database session manager's
        multiplexed session to ensure that it is always valid. The method will run until
        the database session manager is deleted, the multiplexed session is deleted, or
        building a multiplexed session fails.
        :type session_manager_ref: :class:`_weakref.ReferenceType`
        :param session_manager_ref: A weak reference to the database session manager.
        """

        session_manager = session_manager_ref()
        if session_manager is None:
            return

        polling_interval_seconds = (
            session_manager._MAINTENANCE_THREAD_POLLING_INTERVAL.total_seconds()
        )
        refresh_interval_seconds = (
            session_manager._MAINTENANCE_THREAD_REFRESH_INTERVAL.total_seconds()
        )

        session_created_time = time.time()

        while True:
            # Terminate the thread is the database session manager has been deleted.
            session_manager = session_manager_ref()
            if session_manager is None:
                return

            # Terminate the thread if the use of multiplexed sessions has been disabled.
            if session_manager._is_multiplexed_sessions_disabled_event.is_set():
                return

            # Wait for until the refresh interval has elapsed.
            if time.time() - session_created_time < refresh_interval_seconds:
                time.sleep(polling_interval_seconds)
                continue

            with session_manager._multiplexed_session_lock:
                session_manager._multiplexed_session.delete()

                try:
                    session_manager._multiplexed_session = (
                        session_manager._build_multiplexed_session()
                    )

                # Disable multiplexed sessions for all transactions and terminate
                # the thread if building a multiplexed session fails.
                except MethodNotImplemented:
                    session_manager._disable_multiplexed_sessions()
                    return

            session_created_time = time.time()
