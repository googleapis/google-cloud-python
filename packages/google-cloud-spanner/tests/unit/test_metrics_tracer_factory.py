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

from google.cloud.spanner_v1.metrics.metrics_tracer_factory import MetricsTracerFactory
from google.cloud.spanner_v1.metrics.metrics_tracer import MetricsTracer

pytest.importorskip("opentelemetry")


@pytest.fixture
def metrics_tracer_factory():
    factory = MetricsTracerFactory(
        enabled=True,
        service_name="test_service",
    )
    factory.set_project("test_project").set_instance(
        "test_instance"
    ).set_instance_config("test_config").set_location("test_location").set_client_hash(
        "test_hash"
    ).set_client_uid(
        "test_uid"
    ).set_client_name(
        "test_name"
    ).set_database(
        "test_db"
    ).enable_direct_path(
        False
    )
    return factory


def test_initialization(metrics_tracer_factory):
    assert metrics_tracer_factory.enabled is True
    assert metrics_tracer_factory.client_attributes["project_id"] == "test_project"


def test_create_metrics_tracer(metrics_tracer_factory):
    tracer = metrics_tracer_factory.create_metrics_tracer()
    assert isinstance(tracer, MetricsTracer)


def test_client_attributes(metrics_tracer_factory):
    attributes = metrics_tracer_factory.client_attributes
    assert attributes["project_id"] == "test_project"
    assert attributes["instance_id"] == "test_instance"
