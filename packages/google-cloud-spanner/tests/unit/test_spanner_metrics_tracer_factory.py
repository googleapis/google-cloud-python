# -*- coding: utf-8 -*-
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

import pytest
import unittest
from unittest import mock

from google.cloud.spanner_v1.metrics.constants import GOOGLE_CLOUD_REGION_KEY
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from opentelemetry.sdk.resources import Resource

pytest.importorskip("opentelemetry")


class TestSpannerMetricsTracerFactory:
    def test_new_instance_creation(self):
        factory1 = SpannerMetricsTracerFactory(enabled=True)
        factory2 = SpannerMetricsTracerFactory(enabled=True)
        assert factory1 is factory2  # Should return the same instance

    def test_generate_client_uid_format(self):
        client_uid = SpannerMetricsTracerFactory._generate_client_uid()
        assert isinstance(client_uid, str)
        assert len(client_uid.split("@")) == 3  # Should contain uuid, pid, and hostname

    def test_generate_client_hash(self):
        client_uid = "123e4567-e89b-12d3-a456-426614174000@1234@hostname"
        client_hash = SpannerMetricsTracerFactory._generate_client_hash(client_uid)
        assert isinstance(client_hash, str)
        assert len(client_hash) == 6  # Should be a 6-digit hex string

    def test_get_instance_config(self):
        instance_config = SpannerMetricsTracerFactory._get_instance_config()
        assert instance_config == "unknown"  # As per the current implementation

    def test_get_client_name(self):
        client_name = SpannerMetricsTracerFactory._get_client_name()
        assert isinstance(client_name, str)
        assert "spanner-python" in client_name

    def test_get_location(self):
        location = SpannerMetricsTracerFactory._get_location()
        assert isinstance(location, str)
        assert location  # Simply asserting for non empty as this can change depending on the instance this test runs in.


class TestSpannerMetricsTracerFactoryGetLocation(unittest.TestCase):
    @mock.patch(
        "opentelemetry.resourcedetector.gcp_resource_detector.GoogleCloudResourceDetector.detect"
    )
    def test_get_location_with_region(self, mock_detect):
        """Test that _get_location returns the region when detected."""
        mock_resource = Resource.create({GOOGLE_CLOUD_REGION_KEY: "us-central1"})
        mock_detect.return_value = mock_resource

        location = SpannerMetricsTracerFactory._get_location()
        assert location == "us-central1"

    @mock.patch(
        "opentelemetry.resourcedetector.gcp_resource_detector.GoogleCloudResourceDetector.detect"
    )
    def test_get_location_without_region(self, mock_detect):
        """Test that _get_location returns 'global' when no region is detected."""
        mock_resource = Resource.create({})  # No region attribute
        mock_detect.return_value = mock_resource

        location = SpannerMetricsTracerFactory._get_location()
        assert location == "global"

    @mock.patch(
        "opentelemetry.resourcedetector.gcp_resource_detector.GoogleCloudResourceDetector.detect"
    )
    def test_get_location_with_exception(self, mock_detect):
        """Test that _get_location returns 'global' and logs a warning on exception."""
        mock_detect.side_effect = Exception("detector failed")

        with self.assertLogs(
            "google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory",
            level="WARNING",
        ) as log:
            location = SpannerMetricsTracerFactory._get_location()
            assert location == "global"
            self.assertIn("Failed to detect GCP resource location", log.output[0])
