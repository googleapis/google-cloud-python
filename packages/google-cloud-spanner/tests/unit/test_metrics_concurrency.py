# Copyright 2025 Google LLC
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

import threading
import time
import unittest
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from google.cloud.spanner_v1.metrics.metrics_capture import MetricsCapture


class TestMetricsConcurrency(unittest.TestCase):
    def setUp(self):
        # Reset factory singleton
        SpannerMetricsTracerFactory._metrics_tracer_factory = None

    def test_concurrent_tracers(self):
        """Verify that concurrent threads have isolated tracers."""
        factory = SpannerMetricsTracerFactory(enabled=True)
        # Ensure enabled
        factory.enabled = True

        errors = []

        def worker(idx):
            try:
                # Simulate a request workflow
                with MetricsCapture():
                    # Capture should have set a tracer
                    tracer = SpannerMetricsTracerFactory.get_current_tracer()
                    if tracer is None:
                        errors.append(f"Thread {idx}: Tracer is None inside Capture")
                        return

                    # Set a unique attribute for this thread
                    project_name = f"project-{idx}"
                    tracer.set_project(project_name)

                    # Simulate some work
                    time.sleep(0.01)

                    # Verify verify we still have OUR tracer
                    current_tracer = SpannerMetricsTracerFactory.get_current_tracer()
                    if current_tracer.client_attributes["project_id"] != project_name:
                        errors.append(
                            f"Thread {idx}: Tracer project mismatch. Expected {project_name}, got {current_tracer.client_attributes.get('project_id')}"
                        )

                    # Check interceptor logic (simulated)
                    # Interceptor reads from factory.current_metrics_tracer
                    interceptor_tracer = (
                        SpannerMetricsTracerFactory.get_current_tracer()
                    )
                    if interceptor_tracer is not tracer:
                        errors.append(f"Thread {idx}: Interceptor tracer mismatch")

            except Exception as e:
                errors.append(f"Thread {idx}: Exception {e}")

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(errors, [], f"Concurrency errors found: {errors}")

    def test_context_var_cleanup(self):
        """Verify tracer is cleaned up after ContextVar reset."""
        SpannerMetricsTracerFactory(enabled=True)

        with MetricsCapture():
            self.assertIsNotNone(SpannerMetricsTracerFactory.get_current_tracer())

        self.assertIsNone(SpannerMetricsTracerFactory.get_current_tracer())


if __name__ == "__main__":
    unittest.main()
