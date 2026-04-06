# Copyright 2026 Google LLC
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

import mock

from google.cloud import storage_control_v2
from samples.handwritten import storage_control_create_anywhere_cache
from samples.handwritten import storage_control_get_anywhere_cache
from samples.handwritten import storage_control_list_anywhere_caches
from samples.handwritten import storage_control_update_anywhere_cache
from samples.handwritten import storage_control_pause_anywhere_cache
from samples.handwritten import storage_control_resume_anywhere_cache
from samples.handwritten import storage_control_disable_anywhere_cache

BUCKET_NAME = "test-bucket"
ZONE = "us-central1-a"
ANYWHERE_CACHE_ID = "us-central1-a"
ANYWHERE_CACHE_NAME = f"projects/_/buckets/{BUCKET_NAME}/anywhereCaches/{ANYWHERE_CACHE_ID}"


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_create_anywhere_cache(mock_client):
    mock_operation = mock.Mock()
    mock_operation.result.return_value = storage_control_v2.AnywhereCache(name=ANYWHERE_CACHE_NAME)
    mock_operation.operation.name = "op-name"
    mock_client.return_value.create_anywhere_cache.return_value = mock_operation

    response = storage_control_create_anywhere_cache.create_anywhere_cache(BUCKET_NAME, ZONE)

    assert response.name == ANYWHERE_CACHE_NAME
    mock_client.return_value.create_anywhere_cache.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_get_anywhere_cache(mock_client):
    mock_client.return_value.get_anywhere_cache.return_value = storage_control_v2.AnywhereCache(
        name=ANYWHERE_CACHE_NAME, state="RUNNING"
    )

    response = storage_control_get_anywhere_cache.get_anywhere_cache(BUCKET_NAME, ANYWHERE_CACHE_ID)

    assert response.name == ANYWHERE_CACHE_NAME
    assert response.state == "RUNNING"
    mock_client.return_value.get_anywhere_cache.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_list_anywhere_caches(mock_client):
    mock_client.return_value.list_anywhere_caches.return_value = [
        storage_control_v2.AnywhereCache(name=ANYWHERE_CACHE_NAME)
    ]

    response = storage_control_list_anywhere_caches.list_anywhere_caches(BUCKET_NAME)

    assert len(list(response)) == 1
    mock_client.return_value.list_anywhere_caches.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_update_anywhere_cache(mock_client):
    mock_operation = mock.Mock()
    mock_operation.result.return_value = storage_control_v2.AnywhereCache(
        name=ANYWHERE_CACHE_NAME, admission_policy="admit-on-second-miss"
    )
    mock_operation.operation.name = "op-name"
    mock_client.return_value.update_anywhere_cache.return_value = mock_operation

    response = storage_control_update_anywhere_cache.update_anywhere_cache(
        BUCKET_NAME, ANYWHERE_CACHE_ID, "admit-on-second-miss"
    )

    assert response.name == ANYWHERE_CACHE_NAME
    assert response.admission_policy == "admit-on-second-miss"
    mock_client.return_value.update_anywhere_cache.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_pause_anywhere_cache(mock_client):
    mock_client.return_value.pause_anywhere_cache.return_value = storage_control_v2.AnywhereCache(
        name=ANYWHERE_CACHE_NAME, state="PAUSED"
    )

    response = storage_control_pause_anywhere_cache.pause_anywhere_cache(BUCKET_NAME, ANYWHERE_CACHE_ID)

    assert response.name == ANYWHERE_CACHE_NAME
    assert response.state == "PAUSED"
    mock_client.return_value.pause_anywhere_cache.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_resume_anywhere_cache(mock_client):
    mock_client.return_value.resume_anywhere_cache.return_value = storage_control_v2.AnywhereCache(
        name=ANYWHERE_CACHE_NAME, state="RUNNING"
    )

    response = storage_control_resume_anywhere_cache.resume_anywhere_cache(BUCKET_NAME, ANYWHERE_CACHE_ID)

    assert response.name == ANYWHERE_CACHE_NAME
    assert response.state == "RUNNING"
    mock_client.return_value.resume_anywhere_cache.assert_called_once()


@mock.patch("google.cloud.storage_control_v2.StorageControlClient")
def test_disable_anywhere_cache(mock_client):
    mock_client.return_value.disable_anywhere_cache.return_value = storage_control_v2.AnywhereCache(
        name=ANYWHERE_CACHE_NAME, state="DISABLED"
    )

    response = storage_control_disable_anywhere_cache.disable_anywhere_cache(BUCKET_NAME, ANYWHERE_CACHE_ID)

    assert response.name == ANYWHERE_CACHE_NAME
    assert response.state == "DISABLED"
    mock_client.return_value.disable_anywhere_cache.assert_called_once()
