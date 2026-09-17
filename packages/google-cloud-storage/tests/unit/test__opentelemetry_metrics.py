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

import pytest

from google.cloud.storage import _opentelemetry_metrics
from google.cloud.storage.version import __version__


@pytest.mark.parametrize(
    "env_val,default,expected",
    [
        ("1", False, True),
        ("true", False, True),
        ("True", False, True),
        ("yes", False, True),
        ("on", False, True),
        ("0", True, False),
        ("false", True, False),
        ("no", True, False),
        ("off", True, False),
        ("invalid", False, False),
    ],
)
def test_parse_bool_env(monkeypatch, env_val, default, expected):
    monkeypatch.setenv("TEST_BOOL_ENV", env_val)
    assert _opentelemetry_metrics._parse_bool_env("TEST_BOOL_ENV", default) == expected


def test_parse_bool_env_default(monkeypatch):
    monkeypatch.delenv("TEST_BOOL_ENV_MISSING", raising=False)
    assert _opentelemetry_metrics._parse_bool_env("TEST_BOOL_ENV_MISSING", True) is True
    assert (
        _opentelemetry_metrics._parse_bool_env("TEST_BOOL_ENV_MISSING", False) is False
    )


def test_dev_gate_locked_disables_metrics(monkeypatch):
    """When _ENABLE_METRICS_DEV_GATE is False, metrics must remain disabled."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", False)
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")

    assert _opentelemetry_metrics.is_metrics_enabled() is False
    assert _opentelemetry_metrics.is_metrics_enabled(client_setting=True) is False


def test_dev_gate_unlocked_respects_env_var(monkeypatch):
    """When dev gate is open, environment variable enables metrics."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)

    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")
    assert _opentelemetry_metrics.is_metrics_enabled() is True

    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "false")
    assert _opentelemetry_metrics.is_metrics_enabled() is False


def test_metrics_default_is_disabled_when_env_unset(monkeypatch):
    """When env var is unset, default value is False."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.delenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", raising=False)

    assert _opentelemetry_metrics.is_metrics_enabled() is False


def test_client_setting_overrides_env_var(monkeypatch):
    """Client constructor parameter must take precedence over env var."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)

    # Client disables while env var is True
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")
    assert _opentelemetry_metrics.is_metrics_enabled(client_setting=False) is False

    # Client enables while env var is False
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "false")
    assert _opentelemetry_metrics.is_metrics_enabled(client_setting=True) is True


def test_advanced_metrics_requires_base_metrics(monkeypatch):
    """Advanced metrics cannot be active if base metrics are disabled."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "false")
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_DEBUG_METRICS", "true")

    assert _opentelemetry_metrics.is_advanced_metrics_enabled() is False


def test_advanced_metrics_enabled(monkeypatch):
    """Advanced metrics is enabled when both base and debug flags are True."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_DEBUG_METRICS", "true")

    assert _opentelemetry_metrics.is_advanced_metrics_enabled() is True


def test_advanced_metrics_client_setting_overrides_env_var(monkeypatch):
    """Client setting overrides advanced metrics env var."""
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_DEBUG_METRICS", "false")

    assert (
        _opentelemetry_metrics.is_advanced_metrics_enabled(client_setting=True) is True
    )


def test_otel_missing_disables_metrics(monkeypatch):
    """If opentelemetry-api is not installed, metrics must gracefully disable."""
    monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", False)
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.setenv("GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS", "true")

    assert _opentelemetry_metrics.is_metrics_enabled() is False
    assert _opentelemetry_metrics.get_meter() is None


def test_get_common_attributes():
    """Verify common attributes conform to GCS OTel specification."""
    attrs = _opentelemetry_metrics.get_common_attributes()
    assert attrs["gcp.client.service"] == "storage"
    assert attrs["gcp.client.version"] == __version__
    assert attrs["gcp.client.repo"] == "googleapis/google-cloud-python"
    assert attrs["gcp.client.artifact"] == "google-cloud-storage"


def test_get_meter():
    """Verify get_meter returns a meter or None."""
    meter = _opentelemetry_metrics.get_meter()
    if _opentelemetry_metrics.HAS_OPENTELEMETRY_METRICS:
        assert meter is not None
    else:
        assert meter is None
