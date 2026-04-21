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
import mock

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    NumberDataPoint,
    HistogramDataPoint,
    MetricExportResult,
    MetricsData,
    ResourceMetrics,
    ScopeMetrics,
    Metric,
    Sum,
    AggregationTemporality,
)
from google.cloud.monitoring_v3 import (
    Point,
    TimeSeries,
)
from google.api.distribution_pb2 import Distribution


from google.cloud.bigtable.data._metrics.handlers.gcp_exporter import (
    BigtableMetricsExporter,
)
from google.cloud.bigtable.data._metrics.handlers.gcp_exporter import (
    GoogleCloudMetricsHandler,
)
from google.cloud.bigtable.data._metrics.handlers.opentelemetry import (
    _OpenTelemetryInstruments,
)


class TestGoogleCloudMetricsHandler:
    def _make_one(self, *args, **kwargs):
        return GoogleCloudMetricsHandler(*args, **kwargs)

    def test_ctor_defaults(self):
        from google.cloud.bigtable import __version__ as CLIENT_VERSION

        expected_instance = "my_instance"
        expected_table = "my_table"
        expected_exporter = BigtableMetricsExporter("project")
        with mock.patch.object(
            GoogleCloudMetricsHandler, "_generate_client_uid"
        ) as uid_mock:
            handler = self._make_one(
                expected_exporter,
                instance_id=expected_instance,
                table_id=expected_table,
            )
        assert isinstance(handler.meter_provider, MeterProvider)
        assert isinstance(handler.otel, _OpenTelemetryInstruments)
        assert handler.shared_labels["resource_instance"] == expected_instance
        assert handler.shared_labels["resource_table"] == expected_table
        assert handler.shared_labels["app_profile"] == "default"
        assert (
            handler.shared_labels["client_name"] == f"python-bigtable/{CLIENT_VERSION}"
        )
        assert handler.shared_labels["client_uid"] == uid_mock()

    def test_ctor_explicit(self):
        expected_instance = "my_instance"
        expected_table = "my_table"
        expected_version = "my_version"
        expected_uid = "my_uid"
        expected_app_profile = "my_profile"
        expected_exporter = BigtableMetricsExporter("project")
        handler = self._make_one(
            expected_exporter,
            instance_id=expected_instance,
            table_id=expected_table,
            app_profile_id=expected_app_profile,
            client_uid=expected_uid,
            client_version=expected_version,
        )
        assert handler.shared_labels["resource_instance"] == expected_instance
        assert handler.shared_labels["resource_table"] == expected_table
        assert handler.shared_labels["app_profile"] == expected_app_profile
        assert (
            handler.shared_labels["client_name"]
            == f"python-bigtable/{expected_version}"
        )
        assert handler.shared_labels["client_uid"] == expected_uid

    @mock.patch(
        "google.cloud.bigtable.data._metrics.handlers.gcp_exporter.PeriodicExportingMetricReader"
    )
    @mock.patch(
        "google.cloud.bigtable.data._metrics.handlers.gcp_exporter.MeterProvider"
    )
    @mock.patch(
        "google.cloud.bigtable.data._metrics.handlers.gcp_exporter._OpenTelemetryInstruments"
    )
    @mock.patch(
        "google.cloud.bigtable.data._metrics.handlers.gcp_exporter.OpenTelemetryMetricsHandler.__init__"
    )
    def test_ctor_with_mocks(
        self, mock_super_init, mock_otel_instruments, mock_meter_provider, mock_reader
    ):
        from google.cloud.bigtable.data._metrics.handlers.gcp_exporter import (
            VIEW_LIST,
        )

        exporter = mock.Mock()
        export_interval = 90
        kwargs = {"instance_id": "test_instance", "table_id": "test_table"}
        handler = self._make_one(exporter, export_interval=export_interval, **kwargs)
        # check PeriodicExportingMetricReader
        mock_reader.assert_called_once_with(
            exporter, export_interval_millis=export_interval * 1000
        )
        # check MeterProvider
        mock_meter_provider.assert_called_once_with(
            metric_readers=[mock_reader.return_value], views=VIEW_LIST
        )
        # check _OpenTelemetryInstruments
        mock_otel_instruments.assert_called_once_with(
            meter_provider=mock_meter_provider.return_value
        )
        # check super().__init__ call
        mock_super_init.assert_called_once_with(
            instruments=mock_otel_instruments.return_value, **kwargs
        )
        assert handler.meter_provider == mock_meter_provider.return_value

    def test_close(self):
        mock_instance = mock.Mock()
        assert mock_instance.meter_provider.shutdown.call_count == 0
        GoogleCloudMetricsHandler.close(mock_instance)
        assert mock_instance.meter_provider.shutdown.call_count == 1


class TestBigtableMetricsExporter:
    def _make_one(self, *args, **kwargs):
        return BigtableMetricsExporter(*args, **kwargs)

    def test_ctor_defaults(self):
        from google.cloud.monitoring_v3 import MetricServiceClient

        expected_project = "custom"
        instance = self._make_one(expected_project)
        assert instance.project_id == expected_project
        assert instance.prefix == "bigtable.googleapis.com/internal/client"
        assert isinstance(instance.client, MetricServiceClient)

    def test_ctor_mocks(self):
        expected_project = "custom"
        with mock.patch(
            "google.cloud.monitoring_v3.MetricServiceClient.__init__",
            return_value=None,
        ) as mock_client:
            args = [mock.Mock(), object()]
            kwargs = {"a": "b"}
            instance = self._make_one(expected_project, *args, **kwargs)
            assert instance.project_id == expected_project
            assert instance.prefix == "bigtable.googleapis.com/internal/client"
            mock_client.assert_called_once_with(*args, **kwargs)

    @pytest.mark.parametrize(
        "value,expected_field",
        [
            (123, "int64_value"),
            (123.456, "double_value"),
        ],
    )
    def test__to_point_w_number(self, value, expected_field):
        """Test that NumberDataPoint is converted to a Point correctly."""
        instance = self._make_one("project")
        expected_start_time_nanos = 100
        expected_end_time_nanos = 200
        dp = NumberDataPoint(
            attributes={},
            start_time_unix_nano=expected_start_time_nanos,
            time_unix_nano=expected_end_time_nanos,
            value=value,
        )
        point = instance._to_point(dp)
        assert isinstance(point, Point)
        assert getattr(point.value, expected_field) == value
        assert (
            point.interval.start_time.second * 10**9
        ) + point.interval.start_time.nanosecond == expected_start_time_nanos
        assert (
            point.interval.end_time.second * 10**9
        ) + point.interval.end_time.nanosecond == expected_end_time_nanos

    def test__to_point_w_histogram(self):
        """Test that HistogramDataPoint is converted to a Point correctly."""
        instance = self._make_one("project")
        expected_start_time_nanos = 100
        expected_end_time_nanos = 200
        expected_count = 10
        expected_sum = 100.0
        expected_bucket_counts = [1, 2, 7]
        expected_explicit_bounds = [10, 20]
        dp = HistogramDataPoint(
            attributes={},
            start_time_unix_nano=expected_start_time_nanos,
            time_unix_nano=expected_end_time_nanos,
            count=expected_count,
            sum=expected_sum,
            bucket_counts=expected_bucket_counts,
            explicit_bounds=expected_explicit_bounds,
            min=0,
            max=50,
        )
        point = instance._to_point(dp)
        assert isinstance(point, Point)
        dist = point.value.distribution_value
        assert isinstance(dist, Distribution)
        assert dist.count == expected_count
        assert dist.mean == expected_sum / expected_count
        assert list(dist.bucket_counts) == expected_bucket_counts
        assert (
            list(dist.bucket_options.explicit_buckets.bounds)
            == expected_explicit_bounds
        )
        assert (
            point.interval.start_time.second * 10**9
        ) + point.interval.start_time.nanosecond == expected_start_time_nanos
        assert (
            point.interval.end_time.second * 10**9
        ) + point.interval.end_time.nanosecond == expected_end_time_nanos

    def test__to_point_w_histogram_zero_count(self):
        """Test that HistogramDataPoint with zero count is converted to a Point correctly."""
        instance = self._make_one("project")
        dp = HistogramDataPoint(
            attributes={},
            start_time_unix_nano=100,
            time_unix_nano=200,
            count=0,
            sum=0,
            bucket_counts=[],
            explicit_bounds=[],
            min=0,
            max=0,
        )
        point = instance._to_point(dp)
        assert isinstance(point, Point)
        dist = point.value.distribution_value
        assert isinstance(dist, Distribution)
        assert dist.count == 0
        assert dist.mean == 0.0

    @pytest.mark.parametrize(
        "num_series, batch_size, expected_calls, expected_batch_sizes",
        [
            (10, 200, 1, [10]),
            (200, 200, 1, [200]),
            (500, 200, 3, [200, 200, 100]),
            (0, 200, 0, []),
        ],
    )
    def test__batch_write(
        self, num_series, batch_size, expected_calls, expected_batch_sizes
    ):
        """Test that _batch_write splits series into batches correctly."""
        instance = self._make_one("project")
        instance.client = mock.Mock()
        series = [TimeSeries() for _ in range(num_series)]
        instance._batch_write(series, max_batch_size=batch_size)
        assert instance.client.create_service_time_series.call_count == expected_calls
        for i, call in enumerate(
            instance.client.create_service_time_series.call_args_list
        ):
            call_args, _ = call
            assert len(call_args[0].time_series) == expected_batch_sizes[i]

    def test__batch_write_with_deadline(self):
        """Test that _batch_write passes deadlines to gapic correctly."""
        import time
        from google.api_core import gapic_v1

        instance = self._make_one("project")
        instance.client = mock.Mock()
        series = [TimeSeries() for _ in range(10)]
        # test with deadline
        deadline = time.time() + 10
        instance._batch_write(series, deadline=deadline)
        (
            call_args,
            call_kwargs,
        ) = instance.client.create_service_time_series.call_args_list[0]
        assert "timeout" in call_kwargs
        assert 9 < call_kwargs["timeout"] < 10
        # test without deadline
        instance.client.create_service_time_series.reset_mock()
        instance._batch_write(series, deadline=None)
        (
            call_args,
            call_kwargs,
        ) = instance.client.create_service_time_series.call_args_list[0]
        assert "timeout" in call_kwargs
        assert call_kwargs["timeout"] == gapic_v1.method.DEFAULT

    def test_export(self):
        """Test that export correctly converts metrics and calls _batch_write."""
        project_id = "project"
        instance = self._make_one(project_id)
        instance._batch_write = mock.Mock()
        # create mock metrics data
        expected_value = 123
        attributes = {
            "resource_instance": "instance1",
            "resource_cluster": "cluster1",
            "resource_table": "table1",
            "resource_zone": "zone1",
            "method": "ReadRows",
        }
        data_point = NumberDataPoint(
            attributes=attributes,
            start_time_unix_nano=100,
            time_unix_nano=200,
            value=expected_value,
        )
        metric = Metric(
            name="operation_latencies",
            description="",
            unit="ms",
            data=Sum(
                data_points=[data_point],
                aggregation_temporality=AggregationTemporality.CUMULATIVE,
                is_monotonic=False,
            ),
        )
        scope_metric = ScopeMetrics(
            scope=mock.Mock(), metrics=[metric], schema_url=None
        )
        resource_metric = ResourceMetrics(
            resource=mock.Mock(), scope_metrics=[scope_metric], schema_url=None
        )
        metrics_data = MetricsData(resource_metrics=[resource_metric])
        result = instance.export(metrics_data)
        assert result == MetricExportResult.SUCCESS
        instance._batch_write.assert_called_once()
        # check the TimeSeries passed to _batch_write
        call_args, call_kwargs = instance._batch_write.call_args_list[0]
        series_list = call_args[0]
        assert len(series_list) == 1
        series = series_list[0]
        assert series.metric.type == f"{instance.prefix}/operation_latencies"
        assert series.metric.labels["method"] == "ReadRows"
        assert "resource_instance" not in series.metric.labels
        assert series.resource.type == "bigtable_client_raw"
        assert series.resource.labels["project_id"] == project_id
        assert series.resource.labels["instance"] == "instance1"
        assert series.resource.labels["cluster"] == "cluster1"
        assert series.resource.labels["table"] == "table1"
        assert series.resource.labels["zone"] == "zone1"
        assert len(series.points) == 1
        point = series.points[0]
        assert point.value.int64_value == expected_value

    def test_export_no_attributes(self):
        """Test that export skips data points with no attributes."""
        instance = self._make_one("project")
        instance._batch_write = mock.Mock()
        data_point = NumberDataPoint(
            attributes={}, start_time_unix_nano=100, time_unix_nano=200, value=123
        )
        metric = Metric(
            name="operation_latencies",
            description="",
            unit="ms",
            data=Sum(
                data_points=[data_point],
                aggregation_temporality=AggregationTemporality.CUMULATIVE,
                is_monotonic=False,
            ),
        )
        scope_metric = ScopeMetrics(
            scope=mock.Mock(), metrics=[metric], schema_url=None
        )
        resource_metric = ResourceMetrics(
            resource=mock.Mock(), scope_metrics=[scope_metric], schema_url=None
        )
        metrics_data = MetricsData(resource_metrics=[resource_metric])
        result = instance.export(metrics_data)
        assert result == MetricExportResult.SUCCESS
        instance._batch_write.assert_called_once()
        series_list = instance._batch_write.call_args[0][0]
        assert len(series_list) == 0

    def test_exception_in_export(self):
        """
        make sure exceptions don't raise
        """
        instance = self._make_one("project")
        instance._batch_write = mock.Mock(side_effect=Exception("test"))
        # create mock metrics data with one valid data point
        attributes = {
            "resource_instance": "instance1",
            "resource_cluster": "cluster1",
            "resource_table": "table1",
            "resource_zone": "zone1",
        }
        data_point = NumberDataPoint(
            attributes=attributes,
            start_time_unix_nano=100,
            time_unix_nano=200,
            value=123,
        )
        metric = Metric(
            name="operation_latencies",
            description="",
            unit="ms",
            data=Sum(
                data_points=[data_point],
                aggregation_temporality=AggregationTemporality.CUMULATIVE,
                is_monotonic=False,
            ),
        )
        scope_metric = ScopeMetrics(
            scope=mock.Mock(), metrics=[metric], schema_url=None
        )
        resource_metric = ResourceMetrics(
            resource=mock.Mock(), scope_metrics=[scope_metric], schema_url=None
        )
        metrics_data = MetricsData(resource_metrics=[resource_metric])
        result = instance.export(metrics_data)
        assert result == MetricExportResult.FAILURE
