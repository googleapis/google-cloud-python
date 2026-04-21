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

from __future__ import annotations

import time

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics import view
from opentelemetry.sdk.metrics.export import (
    HistogramDataPoint,
    MetricExporter,
    MetricExportResult,
    MetricsData,
    NumberDataPoint,
    PeriodicExportingMetricReader,
)
from google.protobuf.timestamp_pb2 import Timestamp
from google.api.distribution_pb2 import Distribution
from google.api.metric_pb2 import Metric as GMetric
from google.api.monitored_resource_pb2 import MonitoredResource
from google.api.metric_pb2 import MetricDescriptor
from google.api_core import gapic_v1
from google.cloud.monitoring_v3 import (
    CreateTimeSeriesRequest,
    MetricServiceClient,
    Point,
    TimeInterval,
    TimeSeries,
    TypedValue,
)

from google.cloud.bigtable.data._metrics.handlers.opentelemetry import (
    OpenTelemetryMetricsHandler,
)
from google.cloud.bigtable.data._metrics.handlers.opentelemetry import (
    _OpenTelemetryInstruments,
)


# create OpenTelemetry views for Bigtable metrics
# avoid reformatting into individual lines
# fmt: off
MILLIS_AGGREGATION = view.ExplicitBucketHistogramAggregation(
    [
        0, 1, 2, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 30, 40,
        50, 65, 80, 100, 130, 160, 200, 250, 300, 400, 500, 650,
        800, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000,
        200_000, 400_000, 800_000, 1_600_000, 3_200_000
    ]
)
# fmt: on
COUNT_AGGREGATION = view.SumAggregation()
INSTRUMENT_NAMES = (
    "operation_latencies",
    "first_response_latencies",
    "attempt_latencies",
    "retry_count",
    "server_latencies",
    "connectivity_error_count",
    "application_latencies",
    "throttling_latencies",
)
VIEW_LIST = [
    view.View(
        instrument_name=n,
        name=n,
        aggregation=MILLIS_AGGREGATION
        if n.endswith("latencies")
        else COUNT_AGGREGATION,
    )
    for n in INSTRUMENT_NAMES
]


class GoogleCloudMetricsHandler(OpenTelemetryMetricsHandler):
    """
    Maintains an internal set of OpenTelemetry metrics for the Bigtable client library,
    and periodically exports them to Google Cloud Monitoring.

    The OpenTelemetry metrics that are tracked are as follows:
      - operation_latencies: latency of each client method call, over all of it's attempts.
      - first_response_latencies: latency of receiving the first row in a ReadRows operation.
      - attempt_latencies: latency of each client attempt RPC.
      - retry_count: Number of additional RPCs sent after the initial attempt.
      - server_latencies: latency recorded on the server side for each attempt.
      - connectivity_error_count: number of attempts that failed to reach Google's network.
      - application_latencies: the time spent waiting for the application to process the next response.
      - throttling_latencies: latency introduced by waiting when there are too many outstanding requests in a bulk operation.

    Args:
        exporter: The exporter object used to write metrics to Cloud Montitoring.
            Should correspond 1:1 with a bigtable client, and share auth configuration
        export_interval: The interval (in seconds) at which to export metrics to Cloud Monitoring.
        *args: configuration positional arguments passed down to super class
        *kwargs: configuration keyword arguments passed down to super class
    """

    def __init__(self, exporter, *args, export_interval=60, **kwargs):
        # periodically executes exporter
        gcp_reader = PeriodicExportingMetricReader(
            exporter, export_interval_millis=export_interval * 1000
        )
        # use private meter provider to store instruments and views
        self.meter_provider = MeterProvider(
            metric_readers=[gcp_reader], views=VIEW_LIST
        )
        otel = _OpenTelemetryInstruments(meter_provider=self.meter_provider)
        super().__init__(*args, instruments=otel, **kwargs)

    def close(self):
        self.meter_provider.shutdown()


class BigtableMetricsExporter(MetricExporter):
    """
    OpenTelemetry Exporter implementation for sending metrics to Google Cloud Monitoring.

    We must use a custom exporter because the public one doesn't support writing to internal
    metrics like `bigtable.googleapis.com/internal/client/`

    Each GoogleCloudMetricsHandler will maintain its own exporter instance associated with the
    project_id it is configured with.

    Args:
        project_id: GCP project id to associate metrics with
    """

    def __init__(self, project_id: str, *client_args, **client_kwargs):
        super().__init__()
        self.client = MetricServiceClient(*client_args, **client_kwargs)
        self.prefix = "bigtable.googleapis.com/internal/client"
        self.project_id = project_id

    def export(
        self, metrics_data: MetricsData, timeout_millis: float = 10_000, **kwargs
    ) -> MetricExportResult:
        """
        Write a set of metrics to Cloud Monitoring.
        This method is called by the OpenTelemetry SDK
        """
        deadline = time.time() + (timeout_millis / 1000)
        metric_kind = MetricDescriptor.MetricKind.CUMULATIVE
        all_series: list[TimeSeries] = []
        # process each metric from OTel format into Cloud Monitoring format
        for resource_metric in metrics_data.resource_metrics:
            for scope_metric in resource_metric.scope_metrics:
                for metric in scope_metric.metrics:
                    for data_point in [
                        pt for pt in metric.data.data_points if pt.attributes
                    ]:
                        if data_point.attributes:
                            monitored_resource = MonitoredResource(
                                type="bigtable_client_raw",
                                labels={
                                    "project_id": self.project_id,
                                    "instance": data_point.attributes[
                                        "resource_instance"
                                    ],
                                    "cluster": data_point.attributes[
                                        "resource_cluster"
                                    ],
                                    "table": data_point.attributes["resource_table"],
                                    "zone": data_point.attributes["resource_zone"],
                                },
                            )
                            point = self._to_point(data_point)
                            series = TimeSeries(
                                resource=monitored_resource,
                                metric_kind=metric_kind,
                                points=[point],
                                metric=GMetric(
                                    type=f"{self.prefix}/{metric.name}",
                                    labels={
                                        k: v
                                        for k, v in data_point.attributes.items()
                                        if not k.startswith("resource_")
                                    },
                                ),
                                unit=metric.unit,
                            )
                            all_series.append(series)
        # send all metrics to Cloud Monitoring
        try:
            self._batch_write(all_series, deadline)
            return MetricExportResult.SUCCESS
        except Exception:
            return MetricExportResult.FAILURE

    def _batch_write(
        self, series: list[TimeSeries], deadline=None, max_batch_size=200
    ) -> None:
        """
        Adapted from CloudMonitoringMetricsExporter
        https://github.com/GoogleCloudPlatform/opentelemetry-operations-python/blob/3668dfe7ce3b80dd01f42af72428de957b58b316/opentelemetry-exporter-gcp-monitoring/src/opentelemetry/exporter/cloud_monitoring/__init__.py#L82

        Args:
            series: list of TimeSeries to write. Will be split into batches if necessary
            deadline: designates the time.time() at which to stop writing. If None, uses API default
            max_batch_size: maximum number of time series to write at once.
                Cloud Monitoring allows up to 200 per request
        """
        write_ind = 0
        while write_ind < len(series):
            # find time left for next batch
            timeout = deadline - time.time() if deadline else gapic_v1.method.DEFAULT
            # write next batch
            self.client.create_service_time_series(
                CreateTimeSeriesRequest(
                    name=f"projects/{self.project_id}",
                    time_series=series[write_ind : write_ind + max_batch_size],
                ),
                timeout=timeout,
            )
            write_ind += max_batch_size

    @staticmethod
    def _to_point(data_point: NumberDataPoint | HistogramDataPoint) -> Point:
        """
        Adapted from CloudMonitoringMetricsExporter
        https://github.com/GoogleCloudPlatform/opentelemetry-operations-python/blob/3668dfe7ce3b80dd01f42af72428de957b58b316/opentelemetry-exporter-gcp-monitoring/src/opentelemetry/exporter/cloud_monitoring/__init__.py#L82
        """
        if isinstance(data_point, HistogramDataPoint):
            mean = data_point.sum / data_point.count if data_point.count else 0.0
            point_value = TypedValue(
                distribution_value=Distribution(
                    count=data_point.count,
                    mean=mean,
                    bucket_counts=data_point.bucket_counts,
                    bucket_options=Distribution.BucketOptions(
                        explicit_buckets=Distribution.BucketOptions.Explicit(
                            bounds=data_point.explicit_bounds,
                        )
                    ),
                )
            )
        else:
            if isinstance(data_point.value, int):
                point_value = TypedValue(int64_value=data_point.value)
            else:
                point_value = TypedValue(double_value=data_point.value)
        start_time = Timestamp()
        start_time.FromNanoseconds(data_point.start_time_unix_nano)
        end_time = Timestamp()
        end_time.FromNanoseconds(data_point.time_unix_nano)
        interval = TimeInterval(start_time=start_time, end_time=end_time)
        return Point(interval=interval, value=point_value)

    def shutdown(self, timeout_millis: float = 30_000, **kwargs):
        """
        Adapted from CloudMonitoringMetricsExporter
        https://github.com/GoogleCloudPlatform/opentelemetry-operations-python/blob/3668dfe7ce3b80dd01f42af72428de957b58b316/opentelemetry-exporter-gcp-monitoring/src/opentelemetry/exporter/cloud_monitoring/__init__.py#L82
        """
        pass

    def force_flush(self, timeout_millis: float = 10_000):
        """
        Adapted from CloudMonitoringMetricsExporter
        https://github.com/GoogleCloudPlatform/opentelemetry-operations-python/blob/3668dfe7ce3b80dd01f42af72428de957b58b316/opentelemetry-exporter-gcp-monitoring/src/opentelemetry/exporter/cloud_monitoring/__init__.py#L82
        """
        return True
