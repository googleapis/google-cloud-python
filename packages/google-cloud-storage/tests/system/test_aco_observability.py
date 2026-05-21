# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import concurrent.futures
import threading
import time

import pytest
from google.api_core import exceptions

from . import _helpers


def test_sequential_cache_priming(storage_client, exporter, buckets_to_delete):
    """Verifies that a cache miss returns immediately and warms the cache, and the subsequent request successfully contains the ACO destination annotations."""
    bucket_name = _helpers.unique_name("aco-priming")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    buckets_to_delete.append(bucket)

    # Clear cache to force a cache miss
    storage_client._bucket_metadata_cache.clear()

    blob_name = "test_blob.txt"
    blob = bucket.blob(blob_name)
    blob.upload_from_string("hello")

    # Clear cache and OTel exporter logs
    storage_client._bucket_metadata_cache.clear()
    exporter.clear()

    # 1. First download (must be a cache miss)
    blob.download_as_bytes()

    spans = exporter.get_finished_spans()
    dl_spans = [s for s in spans if s.name == "Storage.Blob.downloadAsBytes"]
    assert len(dl_spans) == 1
    attrs = dl_spans[0].attributes
    assert "gcp.resource.destination.id" not in attrs
    assert "gcp.resource.destination.location" not in attrs

    # Wait for background fetch thread to populate cache
    time.sleep(1.5)

    # 2. Second download (must be a cache hit)
    exporter.clear()
    blob.download_as_bytes()

    spans = exporter.get_finished_spans()
    dl_spans = [s for s in spans if s.name == "Storage.Blob.downloadAsBytes"]
    assert len(dl_spans) == 1
    attrs = dl_spans[0].attributes
    assert "gcp.resource.destination.id" in attrs
    assert "gcp.resource.destination.location" in attrs
    assert bucket_name in attrs["gcp.resource.destination.id"]


def test_403_permission_cache_fallback(storage_client, buckets_to_delete):
    """Verifies that if the client does not have permission to reload the bucket (403 Forbidden), the cache safely stores fallback annotations to prevent subsequent API call retry storms."""
    bucket_name = _helpers.unique_name("aco-403")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    buckets_to_delete.append(bucket)

    storage_client._bucket_metadata_cache.clear()

    original_get_bucket = storage_client.get_bucket
    forbidden_triggered = threading.Event()

    def mock_get_bucket(*args, **kwargs):
        from google.api_core.exceptions import Forbidden

        forbidden_triggered.set()
        raise Forbidden("403 Forbidden simulated for system test")

    storage_client.get_bucket = mock_get_bucket

    try:
        # Trigger background fetch
        storage_client._bucket_metadata_cache.get_or_queue_fetch(bucket_name)

        # Wait for background fetch to execute and catch the Forbidden error
        assert forbidden_triggered.wait(timeout=3.0)
        time.sleep(0.5)  # allow time to store fallback

        # Retrieve from cache
        cached = storage_client._bucket_metadata_cache.get(bucket_name)
        assert cached is not None
        dest_id, loc = cached
        assert dest_id == f"projects/_/buckets/{bucket_name}"
        assert loc == "global"
    finally:
        storage_client.get_bucket = original_get_bucket


def test_cache_stampede_protection(storage_client, buckets_to_delete):
    """Verifies that under highly concurrent cache miss conditions, exactly one background metadata API fetch is executed, and all caller threads safely complete without stampeding the GCS server."""
    bucket_name = _helpers.unique_name("aco-stampede")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    buckets_to_delete.append(bucket)

    blob = bucket.blob("test.txt")
    blob.upload_from_string("data")

    storage_client._bucket_metadata_cache.clear()

    fetch_count = 0
    count_lock = threading.Lock()
    original_get_bucket = storage_client.get_bucket

    def monitored_get_bucket(*args, **kwargs):
        nonlocal fetch_count
        with count_lock:
            fetch_count += 1
        time.sleep(0.5)  # simulate some GCS network latency
        return original_get_bucket(*args, **kwargs)

    storage_client.get_bucket = monitored_get_bucket

    try:
        num_threads = 15
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(blob.download_as_bytes) for _ in range(num_threads)
            ]
            concurrent.futures.wait(futures)

        # Wait for background fetch thread to update cache
        time.sleep(1.0)

        # Exactly 1 background GCS get_bucket fetch call must have been triggered
        assert fetch_count == 1
    finally:
        storage_client.get_bucket = original_get_bucket


def test_cache_eviction_scenarios(storage_client, buckets_to_delete):
    """Verifies that if a GCS bucket is deleted out-of-band, any operations triggering a 404 NotFound will asynchronously verify the deletion and evict the bucket from the cache; and direct Bucket.delete() calls synchronously evict the cache."""
    bucket_name = _helpers.unique_name("aco-eviction")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    buckets_to_delete.append(bucket)

    blob = bucket.blob("test.txt")
    blob.upload_from_string("data")

    # Clear and warm cache
    storage_client._bucket_metadata_cache.clear()
    storage_client._bucket_metadata_cache.get_or_queue_fetch(bucket_name)
    time.sleep(1.0)

    assert storage_client._bucket_metadata_cache.get(bucket_name) is not None

    # --- 4a. 404 on Bucket (Asynchronous Eviction) ---
    # Delete GCS bucket directly via HTTP connection to bypass client.delete synchronous eviction
    query_params = {}
    if bucket.user_project is not None:
        query_params["userProject"] = bucket.user_project
    blob.delete()
    storage_client._delete_resource(bucket.path, query_params=query_params)
    buckets_to_delete.remove(bucket)

    # Attempt to load blob (raises 404 NotFound bucket error)
    with pytest.raises(exceptions.NotFound):
        blob.download_as_bytes()

    # Wait for background check_and_evict thread
    time.sleep(1.5)

    # Cache must be evicted
    assert storage_client._bucket_metadata_cache.get(bucket_name) is None

    # --- 4b. Synchronous Delete Eviction ---
    # Re-create bucket, warm cache
    storage_client.create_bucket(bucket)
    storage_client._bucket_metadata_cache.get_or_queue_fetch(bucket_name)
    time.sleep(1.0)
    assert storage_client._bucket_metadata_cache.get(bucket_name) is not None

    # Synchronously delete bucket via SDK client
    bucket.delete()
    # Cache MUST be evicted immediately without waiting
    assert storage_client._bucket_metadata_cache.get(bucket_name) is None


def test_404_on_blob_bucket_exists(storage_client, buckets_to_delete):
    """Verifies that a 404 NotFound on a missing blob inside an existing bucket triggers background check_and_evict which retains the bucket in the cache."""
    bucket_name = _helpers.unique_name("aco-blob-404")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    buckets_to_delete.append(bucket)

    # Warm cache
    storage_client._bucket_metadata_cache.clear()
    storage_client._bucket_metadata_cache.get_or_queue_fetch(bucket_name)
    time.sleep(1.0)
    assert storage_client._bucket_metadata_cache.get(bucket_name) is not None

    # Make a 404 request to a non-existent blob inside this bucket
    non_existent_blob = bucket.blob("non_existent.txt")
    with pytest.raises(exceptions.NotFound):
        non_existent_blob.download_as_bytes()

    # Wait for background check_and_evict thread
    time.sleep(1.5)

    # Bucket must STILL be retained in the cache!
    assert storage_client._bucket_metadata_cache.get(bucket_name) is not None


def test_404_on_blob_bucket_deleted(storage_client):
    """Verifies that a 404 NotFound on a missing blob when the bucket is deleted triggers background check_and_evict which evicts the bucket from the cache."""
    bucket_name = _helpers.unique_name("aco-blob-bucket-404")
    bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)

    # Warm cache
    storage_client._bucket_metadata_cache.clear()
    storage_client._bucket_metadata_cache.get_or_queue_fetch(bucket_name)
    time.sleep(1.0)
    assert storage_client._bucket_metadata_cache.get(bucket_name) is not None

    # Delete bucket directly via GCS connection (bypassing client synchronous eviction)
    query_params = {}
    if bucket.user_project is not None:
        query_params["userProject"] = bucket.user_project
    storage_client._delete_resource(bucket.path, query_params=query_params)

    # Make 404 request to a blob (raises 404 NotFound because bucket is deleted)
    non_existent_blob = bucket.blob("non_existent.txt")
    with pytest.raises(exceptions.NotFound):
        non_existent_blob.download_as_bytes()

    # Wait for background check_and_evict thread
    time.sleep(1.5)

    # Bucket must be evicted from the cache!
    assert storage_client._bucket_metadata_cache.get(bucket_name) is None


def test_lru_bounded_capacity_eviction(storage_client):
    """Verifies that the cache respects the configured size bounds and correctly evicts the least-recently-used elements to avoid memory leaks."""
    from google.cloud.storage._bucket_metadata_cache import BucketMetadataCache

    cache = BucketMetadataCache(storage_client, max_size=5)

    # Populate with 5 buckets
    cache.update_cache("b1", "dest1", "loc1")
    cache.update_cache("b2", "dest2", "loc2")
    cache.update_cache("b3", "dest3", "loc3")
    cache.update_cache("b4", "dest4", "loc4")
    cache.update_cache("b5", "dest5", "loc5")

    # Access b1 (make it most recently used)
    cache.get("b1")

    # Add b6 (which evicts b2, the LRU item)
    cache.update_cache("b6", "dest6", "loc6")

    # Assert b2 is evicted
    assert cache.get("b2") is None
    # Assert b1 is retained
    assert cache.get("b1") == ("dest1", "loc1")
    # Assert b6 is present
    assert cache.get("b6") == ("dest6", "loc6")
