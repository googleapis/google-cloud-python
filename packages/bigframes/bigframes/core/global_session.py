# Copyright 2023 Google LLC
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

"""Utilities for managing a default, globally available Session object."""

import threading
import traceback
from typing import Callable, Optional, TypeVar
import warnings

import google.auth.exceptions

import bigframes._config
import bigframes.exceptions as bfe
import bigframes.session

_global_session: Optional[bigframes.session.Session] = None
_global_session_lock = threading.Lock()
_global_session_state = threading.local()
_global_session_state.thread_local_session = None


def _try_close_session(session: bigframes.session.Session):
    """Try to close the session and warn if couldn't."""
    try:
        session.close()
    except google.auth.exceptions.RefreshError as e:
        session_id = session.session_id
        location = session._location
        project_id = session._project
        msg = bfe.format_message(
            f"Session cleanup failed for session with id: {session_id}, "
            f"location: {location}, project: {project_id}"
        )
        warnings.warn(msg, category=bfe.CleanupFailedWarning)
        traceback.print_tb(e.__traceback__)


def close_session() -> None:
    """Start a fresh session the next time a function requires a session.

    Closes the current session if it was already started, deleting any
    temporary tables that were created.

    Returns:
        None
    """
    global _global_session, _global_session_lock, _global_session_state

    if bigframes._config.options.is_bigquery_thread_local:
        if _global_session_state.thread_local_session is not None:
            _try_close_session(_global_session_state.thread_local_session)
            _global_session_state.thread_local_session = None

        # Currently using thread-local options, so no global lock needed.
        # Don't reset options.bigquery, as that's the responsibility
        # of the context manager that started it in the first place. The user
        # might have explicitly closed the session in the context manager and
        # the thread-locality property needs to be retained.
        bigframes._config.options.bigquery._session_started = False

        # Don't close the non-thread-local session.
        return

    with _global_session_lock:
        if _global_session is not None:
            _try_close_session(_global_session)
            _global_session = None

        # This should be global, not thread-local because of the if clause
        # above.
        bigframes._config.options.bigquery._session_started = False


def get_global_session():
    """Gets the global session.

    Creates the global session if it does not exist.
    """
    global _global_session, _global_session_lock, _global_session_state

    if bigframes._config.options.is_bigquery_thread_local:
        if _global_session_state.thread_local_session is None:
            _global_session_state.thread_local_session = bigframes.session.connect(
                bigframes._config.options.bigquery
            )

        return _global_session_state.thread_local_session

    with _global_session_lock:
        if _global_session is None:
            _global_session = bigframes.session.connect(
                bigframes._config.options.bigquery
            )

    return _global_session


_T = TypeVar("_T")


def with_default_session(func_: Callable[..., _T], *args, **kwargs) -> _T:
    return func_(get_global_session(), *args, **kwargs)


class _GlobalSessionContext:
    """
    Context manager for testing that sets global session.
    """

    def __init__(self, session: bigframes.session.Session):
        self._session = session

    def __enter__(self):
        global _global_session, _global_session_lock
        with _global_session_lock:
            self._previous_session = _global_session
            _global_session = self._session

    def __exit__(self, *exc_details):
        global _global_session, _global_session_lock
        with _global_session_lock:
            _global_session = self._previous_session
