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

"""Script to test and verify GCS ACO Cache Stampede (Thundering Herd) Protection during blob downloads."""

import argparse
import concurrent.futures
import logging
import threading
import time
from unittest import mock

from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s: %(message)s",
)
logger = logging.getLogger(__name__)


def test_with_mock(num_threads=20):
    logger.info(
        f"--- Testing Cache Stampede Protection with Mock Client ({num_threads} threads) ---"
    )
    client = mock.Mock(spec=storage.Client)

    # Initialize cache on client
    from google.cloud.storage._bucket_metadata_cache import BucketMetadataCache

    client._bucket_metadata_cache = BucketMetadataCache(client)

    fetch_count = 0
    count_lock = threading.Lock()

    def simulated_get_bucket(*args, **kwargs):
        nonlocal fetch_count
        with count_lock:
            fetch_count += 1
        logger.info(
            "Background thread executing client.get_bucket()... (simulating 0.5s network latency)"
        )
        time.sleep(0.5)
        b = mock.Mock()
        b.name = "test-bucket"
        b.project_number = 12345
        b.location = "us-east1"
        b.location_type = "region"
        return b

    client.get_bucket.side_effect = simulated_get_bucket

    # Wrap download_as_bytes to invoke span creation (which triggers cache lookup)
    from google.cloud.storage.blob import Blob

    class DummyBlob(Blob):
        def __init__(self, client):
            bkt = mock.Mock()
            bkt.name = "test-bucket"
            bkt.client = client
            super().__init__(name="dummy-blob", bucket=bkt)

        def download_as_bytes(self):
            with self._create_trace_span(name="Storage.Blob.downloadAsBytes"):
                time.sleep(0.05)  # Simulate quick download
                return b"data"

    dummy_blob = DummyBlob(client)

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(dummy_blob.download_as_bytes) for _ in range(num_threads)
        ]
        concurrent.futures.wait(futures)
    end_time = time.time()

    # Wait briefly for background thread to finish updating cache
    time.sleep(0.6)

    logger.info(f"Execution completed in {end_time - start_time:.2f}s.")
    logger.info(f"Total threads launched: {num_threads}")
    logger.info(f"Total background metadata fetches executed: {fetch_count}")

    if fetch_count == 1:
        logger.info(
            "SUCCESS: Cache stampede protection successfully suppressed thundering herd! Only 1 background fetch occurred."
        )
    else:
        logger.error(
            f"FAILURE: Expected exactly 1 background fetch, but got {fetch_count}!"
        )


def test_with_real_gcs(bucket_name, blob_name, num_threads=20):
    logger.info(
        f"--- Testing Cache Stampede Protection with Real GCS Bucket '{bucket_name}' ({num_threads} threads) ---"
    )
    client = storage.Client()

    if (
        not hasattr(client, "_bucket_metadata_cache")
        or not client._bucket_metadata_cache
    ):
        logger.error("GCS Client does not have _bucket_metadata_cache initialized!")
        return

    # Clear any existing cache
    client._bucket_metadata_cache.clear()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Ensure blob exists or create dummy data
    # if not blob.exists():
    #     logger.info(
    #         f"Blob '{blob_name}' does not exist. Creating dummy blob..."
    #     )
    #     blob.upload_from_string("cache stampede test data")

    fetch_count = 0
    count_lock = threading.Lock()
    original_get_bucket = client.get_bucket

    def monitored_get_bucket(*args, **kwargs):
        nonlocal fetch_count
        with count_lock:
            fetch_count += 1
        logger.info(
            f"Background thread executing get_bucket({args[0] if args else kwargs.get('bucket_or_name')})..."
        )
        return original_get_bucket(*args, **kwargs)

    client.get_bucket = monitored_get_bucket

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(blob.download_as_bytes) for _ in range(num_threads)]
        concurrent.futures.wait(futures)
    end_time = time.time()

    # Wait briefly for background thread to finish
    time.sleep(1.0)

    logger.info(f"Execution completed in {end_time - start_time:.2f}s.")
    logger.info(f"Total threads launched: {num_threads}")
    logger.info(f"Total background metadata fetches executed: {fetch_count}")

    if fetch_count == 1:
        logger.info(
            "SUCCESS: Real GCS cache stampede protection successfully suppressed thundering herd!"
        )
    else:
        logger.warning(f"Result: {fetch_count} background fetches executed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test GCS ACO Cache Stampede Protection."
    )
    parser.add_argument("--bucket", type=str, help="Real GCS bucket name to test.")
    parser.add_argument(
        "--blob",
        type=str,
        default="stampede_test.txt",
        help="Blob name to test (default: stampede_test.txt).",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=20,
        help="Number of concurrent download threads (default: 20).",
    )
    args = parser.parse_args()

    if args.bucket:
        test_with_real_gcs(args.bucket, args.blob, args.threads)
    else:
        test_with_mock(args.threads)
