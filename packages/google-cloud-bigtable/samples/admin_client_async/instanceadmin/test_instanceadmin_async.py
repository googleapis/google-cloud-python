# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

import backoff
import pytest
from google.api_core import exceptions

from .instanceadmin_async import (
    add_cluster,
    delete_cluster,
    delete_instance,
    run_instance_operations,
)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
INSTANCE_ID = f"instance-admin-async-{str(uuid.uuid4())[:8]}"
CLUSTER_ID = f"cluster-admin-async-{str(uuid.uuid4())[:8]}"
NEW_CLUSTER_ID = f"cluster-add-async-{str(uuid.uuid4())[:8]}"
FALLBACK_ZONES = (
    "us-central1-f",
    "us-central1-b",
    "us-central1-c",
    "us-east1-b",
    "us-west1-b",
)


def _is_zone_stockout(exc):
    message = str(exc).lower()
    return "sold out" in message or "not enough servers" in message


async def _run_with_zone_fallback(fn, zones, capsys, *args):
    last_exc = None
    for zone in zones:
        capsys.readouterr()
        try:
            await fn(*args, location_id=zone)
            return zone
        except exceptions.GoogleAPICallError as exc:
            if not _is_zone_stockout(exc):
                raise
            last_exc = exc
    raise last_exc


@pytest.mark.asyncio
async def test_instance_operations(capsys):
    try:
        primary_zone = await _run_with_zone_fallback(
            run_instance_operations,
            FALLBACK_ZONES,
            capsys,
            PROJECT,
            INSTANCE_ID,
            CLUSTER_ID,
        )
        out, _ = capsys.readouterr()
        assert f"Created instance: {INSTANCE_ID}" in out
        assert "Listing instances:" in out
        assert "Listing clusters..." in out

        backoff_503 = backoff.on_exception(backoff.expo, exceptions.ServiceUnavailable)
        secondary_zones = tuple(z for z in FALLBACK_ZONES if z != primary_zone)
        await _run_with_zone_fallback(
            backoff_503(add_cluster),
            secondary_zones,
            capsys,
            PROJECT,
            INSTANCE_ID,
            NEW_CLUSTER_ID,
        )
        out, _ = capsys.readouterr()
        assert f"Cluster created: {NEW_CLUSTER_ID}" in out

        await delete_cluster(PROJECT, INSTANCE_ID, NEW_CLUSTER_ID)
        out, _ = capsys.readouterr()
        assert f"Cluster deleted: {NEW_CLUSTER_ID}" in out

        await delete_instance(PROJECT, INSTANCE_ID)
        out, _ = capsys.readouterr()
        assert f"Deleted instance: {INSTANCE_ID}" in out
    finally:
        await delete_instance(PROJECT, INSTANCE_ID)
