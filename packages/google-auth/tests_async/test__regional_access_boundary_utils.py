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

import asyncio
from unittest import mock

import pytest  # type: ignore

from google.auth import _regional_access_boundary_utils


@pytest.mark.asyncio
async def test_async_refresh_manager_start_refresh():
    credentials = mock.AsyncMock()
    credentials._lookup_regional_access_boundary.return_value = {
        "encodedLocations": "0xA30"
    }

    request = mock.Mock()
    rab_manager = mock.Mock()

    manager = (
        _regional_access_boundary_utils._AsyncRegionalAccessBoundaryRefreshManager()
    )

    manager.start_refresh(credentials, request, rab_manager)

    # Wait for the background task to finish
    await manager._worker_task

    credentials._lookup_regional_access_boundary.assert_called_once_with(request)
    rab_manager.process_regional_access_boundary_info.assert_called_once_with(
        {"encodedLocations": "0xA30"}
    )


@pytest.mark.asyncio
async def test_async_refresh_manager_duplicate_refresh_prevented():
    credentials = mock.AsyncMock()

    # Use events to control the concurrency timing
    lookup_started = asyncio.Event()
    lookup_finish = asyncio.Event()

    async def controlled_lookup(*args, **kwargs):
        lookup_started.set()  # Signal that the background lookup has started.
        await lookup_finish.wait()  # Block until the test allows the lookup to complete.
        return {"encodedLocations": "0xA30"}

    credentials._lookup_regional_access_boundary.side_effect = controlled_lookup

    request = mock.Mock()
    rab_manager = mock.Mock()

    manager = (
        _regional_access_boundary_utils._AsyncRegionalAccessBoundaryRefreshManager()
    )

    # Start the initial refresh task in the background.
    manager.start_refresh(credentials, request, rab_manager)

    # Wait until the background task has begun executing the lookup.
    await lookup_started.wait()

    # Attempt a second refresh while the initial task is still in progress.
    manager.start_refresh(credentials, request, rab_manager)

    # Unblock the initial task and wait for it to complete.
    lookup_finish.set()
    await manager._worker_task

    # Verify that the second refresh request was ignored and only one lookup occurred.
    assert credentials._lookup_regional_access_boundary.call_count == 1
