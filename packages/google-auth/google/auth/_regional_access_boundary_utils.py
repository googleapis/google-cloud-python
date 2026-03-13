# Copyright 2026 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for Regional Access Boundary management."""

import datetime
import functools
import logging
import os
import threading
from typing import NamedTuple, Optional

from google.auth import _helpers
from google.auth import environment_vars

_LOGGER = logging.getLogger(__name__)


@functools.lru_cache()
def is_regional_access_boundary_enabled():
    """Checks if Regional Access Boundary is enabled via environment variable.

    The environment variable is interpreted as a boolean with the following
    (case-insensitive) rules:
    - "true", "1" are considered true.
    - Any other value (or unset) is considered false.

    Returns:
        bool: True if Regional Access Boundary is enabled, False otherwise.
    """
    value = os.environ.get(environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED)
    if value is None:
        return False

    return value.lower() in ("true", "1")


# The default lifetime for a cached Regional Access Boundary.
DEFAULT_REGIONAL_ACCESS_BOUNDARY_TTL = datetime.timedelta(hours=6)

# The period of time prior to the boundary's expiration when a background refresh
# is proactively triggered.
REGIONAL_ACCESS_BOUNDARY_REFRESH_THRESHOLD = datetime.timedelta(hours=1)

# The initial cooldown period for a failed Regional Access Boundary lookup.
DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN = datetime.timedelta(minutes=15)

# The maximum cooldown period for a failed Regional Access Boundary lookup.
MAX_REGIONAL_ACCESS_BOUNDARY_COOLDOWN = datetime.timedelta(hours=6)


# The header key used for Regional Access Boundaries.
_REGIONAL_ACCESS_BOUNDARY_HEADER = "x-allowed-locations"


class _RegionalAccessBoundaryData(NamedTuple):
    """Data container for a Regional Access Boundary snapshot.

    Attributes:
        encoded_locations (Optional[str]): The encoded Regional Access Boundary string.
        expiry (Optional[datetime.datetime]): The hard expiration time of the boundary data.
        cooldown_expiry (Optional[datetime.datetime]): The time until which further lookups are skipped.
        cooldown_duration (datetime.timedelta): The current duration for the exponential cooldown.
    """

    encoded_locations: Optional[str]
    expiry: Optional[datetime.datetime]
    cooldown_expiry: Optional[datetime.datetime]
    cooldown_duration: datetime.timedelta


class _RegionalAccessBoundaryManager(object):
    """Manages the Regional Access Boundary state and its background refresh.

    This class provides a stable container for the Regional Access Boundary state,
    allowing cloned credentials to share the same underlying state and refresh mechanism.
    The actual data is held in an immutable `_RegionalAccessBoundaryData` object
    and is swapped atomically to ensure thread-safe, lock-free reads.
    """

    def __init__(self):
        self._data = _RegionalAccessBoundaryData(
            encoded_locations=None,
            expiry=None,
            cooldown_expiry=None,
            cooldown_duration=DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        self.refresh_manager = _RegionalAccessBoundaryRefreshManager()
        self._update_lock = threading.Lock()

    def apply_headers(self, headers):
        """Applies the Regional Access Boundary header to the provided dictionary.

        If the boundary is valid, the 'x-allowed-locations' header is added
        or updated. Otherwise, the header is removed to ensure no stale
        data is sent.

        Args:
            headers (MutableMapping[str, str]): The headers dictionary to update.
        """
        rab_data = self._data

        if rab_data.encoded_locations is not None and (
            rab_data.expiry is not None and _helpers.utcnow() < rab_data.expiry
        ):
            headers[_REGIONAL_ACCESS_BOUNDARY_HEADER] = rab_data.encoded_locations
        else:
            headers.pop(_REGIONAL_ACCESS_BOUNDARY_HEADER, None)

    def maybe_start_refresh(self, credentials, request):
        """Starts a background thread to refresh the Regional Access Boundary if needed.

        Args:
            credentials (google.auth.credentials.Credentials): The credentials to refresh.
            request (google.auth.transport.Request): The object used to make HTTP requests.
        """
        rab_data = self._data

        # Don't start a new refresh if the Regional Access Boundary info is still fresh.
        if (
            rab_data.encoded_locations
            and rab_data.expiry
            and _helpers.utcnow()
            < (rab_data.expiry - REGIONAL_ACCESS_BOUNDARY_REFRESH_THRESHOLD)
        ):
            return

        # Don't start a new refresh if the cooldown is still in effect.
        if rab_data.cooldown_expiry and _helpers.utcnow() < rab_data.cooldown_expiry:
            return

        # If all checks pass, start the background refresh.
        self.refresh_manager.start_refresh(credentials, request, self)


class _RegionalAccessBoundaryRefreshThread(threading.Thread):
    """Thread for background refreshing of the Regional Access Boundary."""

    def __init__(self, credentials, request, rab_manager):
        super(_RegionalAccessBoundaryRefreshThread, self).__init__()
        self.daemon = True
        self._credentials = credentials
        self._request = request
        self._rab_manager = rab_manager

    def run(self):
        """
        Performs the Regional Access Boundary lookup and updates the state.

        This method is run in a separate thread. It delegates the actual lookup
        to the credentials object's `_lookup_regional_access_boundary` method.
        Based on the lookup's outcome (success or complete failure after retries),
        it updates the cached Regional Access Boundary information,
        its expiry, its cooldown expiry, and its exponential cooldown duration.
        """
        # Catch exceptions (e.g., from the underlying transport) to prevent the
        # background thread from crashing. This ensures we can gracefully enter
        # an exponential cooldown state on failure.
        try:
            regional_access_boundary_info = (
                self._credentials._lookup_regional_access_boundary(self._request)
            )
        except Exception as e:
            if _helpers.is_logging_enabled(_LOGGER):
                _LOGGER.warning(
                    "Asynchronous Regional Access Boundary lookup raised an exception: %s",
                    e,
                    exc_info=True,
                )
            regional_access_boundary_info = None

        with self._rab_manager._update_lock:
            # Capture the current state before calculating updates.
            current_data = self._rab_manager._data

            if regional_access_boundary_info:
                # On success, update the boundary and its expiry, and clear any cooldown.
                encoded_locations = regional_access_boundary_info.get(
                    "encodedLocations"
                )
                updated_data = _RegionalAccessBoundaryData(
                    encoded_locations=encoded_locations,
                    expiry=_helpers.utcnow() + DEFAULT_REGIONAL_ACCESS_BOUNDARY_TTL,
                    cooldown_expiry=None,
                    cooldown_duration=DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
                )
                if _helpers.is_logging_enabled(_LOGGER):
                    _LOGGER.debug(
                        "Asynchronous Regional Access Boundary lookup successful."
                    )
            else:
                # On failure, calculate cooldown and update state.
                if _helpers.is_logging_enabled(_LOGGER):
                    _LOGGER.warning(
                        "Asynchronous Regional Access Boundary lookup failed. Entering cooldown."
                    )

                next_cooldown_expiry = (
                    _helpers.utcnow() + current_data.cooldown_duration
                )
                next_cooldown_duration = min(
                    current_data.cooldown_duration * 2,
                    MAX_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
                )

                # If the refresh failed, we keep reusing the existing data unless
                # it has reached its hard expiration time.
                if current_data.expiry and _helpers.utcnow() > current_data.expiry:
                    next_encoded_locations = None
                    next_expiry = None
                else:
                    next_encoded_locations = current_data.encoded_locations
                    next_expiry = current_data.expiry

                updated_data = _RegionalAccessBoundaryData(
                    encoded_locations=next_encoded_locations,
                    expiry=next_expiry,
                    cooldown_expiry=next_cooldown_expiry,
                    cooldown_duration=next_cooldown_duration,
                )

            # Perform the atomic swap of the state object.
            self._rab_manager._data = updated_data


class _RegionalAccessBoundaryRefreshManager(object):
    """Manages a thread for background refreshing of the Regional Access Boundary."""

    def __init__(self):
        self._lock = threading.Lock()
        self._worker = None

    def start_refresh(self, credentials, request, rab_manager):
        """
        Starts a background thread to refresh the Regional Access Boundary if one is not already running.

        Args:
            credentials (CredentialsWithRegionalAccessBoundary): The credentials
                to refresh.
            request (google.auth.transport.Request): The object used to make
                HTTP requests.
            rab_manager (_RegionalAccessBoundaryManager): The manager container to update.
        """
        with self._lock:
            if self._worker and self._worker.is_alive():
                # A refresh is already in progress.
                return

            self._worker = _RegionalAccessBoundaryRefreshThread(
                credentials, request, rab_manager
            )
            self._worker.start()
