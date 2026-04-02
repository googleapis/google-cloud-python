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

import datetime
import os
import unittest.mock

import google.cloud.bigquery as bigquery
import pytest

import bigframes.session.metrics as metrics

NOW = datetime.datetime.now(datetime.timezone.utc)


def test_count_job_stats_with_row_iterator():
    row_iterator = unittest.mock.create_autospec(
        bigquery.table.RowIterator, instance=True
    )
    row_iterator.total_bytes_processed = 1024
    row_iterator.query = "SELECT * FROM table"
    row_iterator.slot_millis = 1234
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(row_iterator=row_iterator)

    assert execution_metrics.execution_count == 1
    assert execution_metrics.bytes_processed == 1024
    assert execution_metrics.query_char_count == 19
    assert execution_metrics.slot_millis == 1234


def test_count_job_stats_with_row_iterator_missing_stats():
    row_iterator = unittest.mock.create_autospec(
        bigquery.table.RowIterator, instance=True
    )
    # Simulate properties not being present on the object
    del row_iterator.total_bytes_processed
    del row_iterator.query
    del row_iterator.slot_millis
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(row_iterator=row_iterator)

    assert execution_metrics.execution_count == 1
    assert execution_metrics.bytes_processed == 0
    assert execution_metrics.query_char_count == 0
    assert execution_metrics.slot_millis == 0


def test_count_job_stats_with_row_iterator_none_stats():
    row_iterator = unittest.mock.create_autospec(
        bigquery.table.RowIterator, instance=True
    )
    row_iterator.total_bytes_processed = None
    row_iterator.query = None
    row_iterator.slot_millis = None
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(row_iterator=row_iterator)

    assert execution_metrics.execution_count == 1
    assert execution_metrics.bytes_processed == 0
    assert execution_metrics.query_char_count == 0
    assert execution_metrics.slot_millis == 0


def test_count_job_stats_with_dry_run():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = True
    query_job.query = "SELECT * FROM table"
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(query_job=query_job)

    # Dry run jobs shouldn't count as "executed"
    assert execution_metrics.execution_count == 0
    assert execution_metrics.bytes_processed == 0
    assert execution_metrics.query_char_count == 0
    assert execution_metrics.slot_millis == 0


def test_count_job_stats_with_valid_job():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.query = "SELECT * FROM table"
    query_job.total_bytes_processed = 2048
    query_job.slot_millis = 5678
    query_job.created = NOW
    query_job.ended = NOW + datetime.timedelta(seconds=2)
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(query_job=query_job)

    assert execution_metrics.execution_count == 1
    assert execution_metrics.bytes_processed == 2048
    assert execution_metrics.query_char_count == 19
    assert execution_metrics.slot_millis == 5678
    assert execution_metrics.execution_secs == pytest.approx(2.0)


def test_count_job_stats_with_cached_job():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.query = "SELECT * FROM table"
    # Cache hit jobs don't have total_bytes_processed or slot_millis
    query_job.total_bytes_processed = None
    query_job.slot_millis = None
    query_job.created = NOW
    query_job.ended = NOW + datetime.timedelta(seconds=1)
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(query_job=query_job)

    assert execution_metrics.execution_count == 1
    assert execution_metrics.bytes_processed == 0
    assert execution_metrics.query_char_count == 19
    assert execution_metrics.slot_millis == 0
    assert execution_metrics.execution_secs == pytest.approx(1.0)


def test_count_job_stats_with_unsupported_job():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.query = "SELECT * FROM table"
    # Some jobs, such as scripts, don't have these properties.
    query_job.total_bytes_processed = None
    query_job.slot_millis = None
    query_job.created = None
    query_job.ended = None
    execution_metrics = metrics.ExecutionMetrics()
    execution_metrics.count_job_stats(query_job=query_job)

    # Don't count jobs if we can't get performance stats.
    assert execution_metrics.execution_count == 0
    assert execution_metrics.bytes_processed == 0
    assert execution_metrics.query_char_count == 0
    assert execution_metrics.slot_millis == 0
    assert execution_metrics.execution_secs == pytest.approx(0.0)


def test_get_performance_stats_with_valid_job():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.query = "SELECT * FROM table"
    query_job.total_bytes_processed = 2048
    query_job.slot_millis = 5678
    query_job.created = NOW
    query_job.ended = NOW + datetime.timedelta(seconds=2)
    stats = metrics.get_performance_stats(query_job)
    assert stats is not None
    query_char_count, bytes_processed, slot_millis, exec_seconds = stats
    assert query_char_count == 19
    assert bytes_processed == 2048
    assert slot_millis == 5678
    assert exec_seconds == pytest.approx(2.0)


def test_get_performance_stats_with_dry_run():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = True
    stats = metrics.get_performance_stats(query_job)
    assert stats is None


def test_get_performance_stats_with_missing_timestamps():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.created = None
    query_job.ended = NOW
    stats = metrics.get_performance_stats(query_job)
    assert stats is None

    query_job.created = NOW
    query_job.ended = None
    stats = metrics.get_performance_stats(query_job)
    assert stats is None


def test_get_performance_stats_with_mocked_types():
    query_job = unittest.mock.create_autospec(bigquery.QueryJob, instance=True)
    query_job.configuration.dry_run = False
    query_job.created = NOW
    query_job.ended = NOW
    query_job.total_bytes_processed = unittest.mock.Mock()
    query_job.slot_millis = 123
    stats = metrics.get_performance_stats(query_job)
    assert stats is None

    query_job.total_bytes_processed = 123
    query_job.slot_millis = unittest.mock.Mock()
    stats = metrics.get_performance_stats(query_job)
    assert stats is None


@pytest.fixture
def mock_environ(monkeypatch):
    """Fixture to mock os.environ."""
    monkeypatch.setenv(metrics.LOGGING_NAME_ENV_VAR, "my_test_case")


def test_write_stats_to_disk_writes_files(tmp_path, mock_environ):
    os.chdir(tmp_path)
    test_name = os.environ[metrics.LOGGING_NAME_ENV_VAR]
    metrics.write_stats_to_disk(
        query_char_count=100,
        bytes_processed=200,
        slot_millis=300,
        exec_seconds=1.23,
    )

    slot_file = tmp_path / (test_name + ".slotmillis")
    assert slot_file.exists()
    with open(slot_file) as f:
        assert f.read() == "300\n"

    exec_time_file = tmp_path / (test_name + ".bq_exec_time_seconds")
    assert exec_time_file.exists()
    with open(exec_time_file) as f:
        assert f.read() == "1.23\n"

    query_char_count_file = tmp_path / (test_name + ".query_char_count")
    assert query_char_count_file.exists()
    with open(query_char_count_file) as f:
        assert f.read() == "100\n"

    bytes_file = tmp_path / (test_name + ".bytesprocessed")
    assert bytes_file.exists()
    with open(bytes_file) as f:
        assert f.read() == "200\n"


def test_write_stats_to_disk_no_env_var(tmp_path, monkeypatch):
    monkeypatch.delenv(metrics.LOGGING_NAME_ENV_VAR, raising=False)
    os.chdir(tmp_path)
    metrics.write_stats_to_disk(
        query_char_count=100,
        bytes_processed=200,
        slot_millis=300,
        exec_seconds=1.23,
    )
    assert len(list(tmp_path.iterdir())) == 0
