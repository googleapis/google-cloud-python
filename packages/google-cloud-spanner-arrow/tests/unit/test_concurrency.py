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
import unittest

import google_cloud_spanner_arrow as sa


class TestSpannerArrowConcurrency(unittest.TestCase):
    def test_multi_threaded_batch_creation(self):
        fields = [("id", 2), ("name", 6), ("score", 3)]
        num_threads = 8
        rows_per_thread = 5000

        def worker(thread_id: int):
            rows = [
                [f"{thread_id * 100000 + i}", f"user_{thread_id}_{i}", float(i)]
                for i in range(rows_per_thread)
            ]
            batch = sa.rows_to_arrow_batch(fields, rows)
            self.assertEqual(batch.num_rows, rows_per_thread)
            self.assertEqual(batch.column("id").to_pylist()[0], thread_id * 100000)
            self.assertEqual(
                batch.column("id").to_pylist()[-1],
                thread_id * 100000 + rows_per_thread - 1,
            )
            return batch.num_rows

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, tid) for tid in range(num_threads)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        self.assertEqual(sum(results), num_threads * rows_per_thread)


if __name__ == "__main__":
    unittest.main()
