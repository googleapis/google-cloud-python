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
import bigframes.session

_global_session: Optional[bigframes.session.Session] = None
_global_session_lock = threading.Lock()


def close_session() -> None:
    """Start a fresh session the next time a function requires a session.

    Closes the current session if it was already started, deleting any
    temporary tables that were created.

    Returns:
        None
    """
    global _global_session

    with _global_session_lock:
        if _global_session is not None:
            try:
                _global_session.close()
            except google.auth.exceptions.RefreshError as e:
                session_id = _global_session.session_id
                location = _global_session._location
                project_id = _global_session._project
                warnings.warn(
                    f"Session cleanup failed for session with id: {session_id}, "
                    f"location: {location}, project: {project_id}",
                    category=bigframes.exceptions.CleanupFailedWarning,
                )
                traceback.print_tb(e.__traceback__)
            _global_session = None

        bigframes._config.options.bigquery._session_started = False


def get_global_session():
    """Gets the global session.

    Creates the global session if it does not exist.
    """
    global _global_session, _global_session_lock

    with _global_session_lock:
        if _global_session is None:
            _global_session = bigframes.session.connect(
                bigframes._config.options.bigquery
            )

    return _global_session


_T = TypeVar("_T")


def with_default_session(func: Callable[..., _T], *args, **kwargs) -> _T:
    return func(get_global_session(), *args, **kwargs)
