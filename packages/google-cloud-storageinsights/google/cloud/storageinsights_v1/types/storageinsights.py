# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.storageinsights.v1",
    manifest={
        "ListReportConfigsRequest",
        "ListReportConfigsResponse",
        "GetReportConfigRequest",
        "CreateReportConfigRequest",
        "UpdateReportConfigRequest",
        "DeleteReportConfigRequest",
        "ReportDetail",
        "ListReportDetailsRequest",
        "ListReportDetailsResponse",
        "GetReportDetailRequest",
        "OperationMetadata",
        "FrequencyOptions",
        "CSVOptions",
        "ParquetOptions",
        "CloudStorageFilters",
        "CloudStorageDestinationOptions",
        "ObjectMetadataReportOptions",
        "ReportConfig",
    },
)


class ListReportConfigsRequest(proto.Message):
    r"""Message for requesting list of ReportConfigs

    Attributes:
        parent (str):
            Required. Parent value for
            ListReportConfigsRequest
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results the
            server should return.
        filter (str):
            Filtering results
        order_by (str):
            Hint for how to order the results
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListReportConfigsResponse(proto.Message):
    r"""Message for response to listing ReportConfigs

    Attributes:
        report_configs (MutableSequence[google.cloud.storageinsights_v1.types.ReportConfig]):
            The list of ReportConfig
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    report_configs: MutableSequence["ReportConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ReportConfig",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetReportConfigRequest(proto.Message):
    r"""Message for getting a ReportConfig

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateReportConfigRequest(proto.Message):
    r"""Message for creating a ReportConfig

    Attributes:
        parent (str):
            Required. Value for parent.
        report_config (google.cloud.storageinsights_v1.types.ReportConfig):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    report_config: "ReportConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ReportConfig",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateReportConfigRequest(proto.Message):
    r"""Message for updating a ReportConfig

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ReportConfig resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        report_config (google.cloud.storageinsights_v1.types.ReportConfig):
            Required. The resource being updated
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    report_config: "ReportConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ReportConfig",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteReportConfigRequest(proto.Message):
    r"""Message for deleting a ReportConfig

    Attributes:
        name (str):
            Required. Name of the resource
        force (bool):
            Optional. If set, all ReportDetails for this
            ReportConfig will be deleted.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ReportDetail(proto.Message):
    r"""Message describing ReportDetail object. ReportDetail
    represents metadata of generated reports for a ReportConfig.
    Next ID: 10

    Attributes:
        name (str):
            Name of resource. It will be of form
            projects/<project>/locations/<location>/reportConfigs/<report-config-id>/reportDetails/<report-detail-id>.
        snapshot_time (google.protobuf.timestamp_pb2.Timestamp):
            The snapshot time.
            All the report data is referenced at this point
            of time.
        report_path_prefix (str):
            Prefix of the object name of each report's shard. This will
            have full prefix except the "extension" and "shard_id". For
            example, if the ``destination_path`` is
            ``{{report-config-id}}/dt={{datetime}}``, the shard object
            name would be
            ``gs://my-insights/1A34-F2E456-12B456-1C3D/dt=2022-05-20T06:35/1A34-F2E456-12B456-1C3D_2022-05-20T06:35_5.csv``
            and the value of ``report_path_prefix`` field would be
            ``gs://my-insights/1A34-F2E456-12B456-1C3D/dt=2022-05-20T06:35/1A34-F2E456-12B456-1C3D_2022-05-20T06:35_``.
        shards_count (int):
            Total shards generated for the report.
        status (google.rpc.status_pb2.Status):
            Status of the ReportDetail.
        labels (MutableMapping[str, str]):
            Labels as key value pairs
        target_datetime (google.type.datetime_pb2.DateTime):
            The date for which report is generated. The time part of
            target_datetime will be zero till we support multiple
            reports per day.
        report_metrics (google.cloud.storageinsights_v1.types.ReportDetail.Metrics):
            Metrics of the report.
    """

    class Metrics(proto.Message):
        r"""Different metrics associated with the generated report.

        Attributes:
            processed_records_count (int):
                Count of Cloud Storage objects which are part
                of the report.
        """

        processed_records_count: int = proto.Field(
            proto.INT64,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    snapshot_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    report_path_prefix: str = proto.Field(
        proto.STRING,
        number=8,
    )
    shards_count: int = proto.Field(
        proto.INT64,
        number=9,
    )
    status: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    target_datetime: datetime_pb2.DateTime = proto.Field(
        proto.MESSAGE,
        number=6,
        message=datetime_pb2.DateTime,
    )
    report_metrics: Metrics = proto.Field(
        proto.MESSAGE,
        number=7,
        message=Metrics,
    )


class ListReportDetailsRequest(proto.Message):
    r"""Message for requesting list of ReportDetails

    Attributes:
        parent (str):
            Required. Parent value for
            ListReportDetailsRequest
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results the
            server should return.
        filter (str):
            Filtering results
        order_by (str):
            Hint for how to order the results
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListReportDetailsResponse(proto.Message):
    r"""Message for response to listing ReportDetails

    Attributes:
        report_details (MutableSequence[google.cloud.storageinsights_v1.types.ReportDetail]):
            The list of ReportDetail
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    report_details: MutableSequence["ReportDetail"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ReportDetail",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetReportDetailRequest(proto.Message):
    r"""Message for getting a ReportDetail

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class FrequencyOptions(proto.Message):
    r"""ReportConfig Resource:

    Options to setup frequency of report generation.

    Attributes:
        frequency (google.cloud.storageinsights_v1.types.FrequencyOptions.Frequency):
            Frequency of report generation.
        start_date (google.type.date_pb2.Date):
            The date from which report generation should
            start. UTC time zone.
        end_date (google.type.date_pb2.Date):
            The date on which report generation should
            stop (Inclusive). UTC time zone.
    """

    class Frequency(proto.Enum):
        r"""This ENUM specifies possible frequencies of report
        generation.

        Values:
            FREQUENCY_UNSPECIFIED (0):
                Unspecified.
            DAILY (1):
                Report will be generated daily.
            WEEKLY (2):
                Report will be generated weekly.
        """
        FREQUENCY_UNSPECIFIED = 0
        DAILY = 1
        WEEKLY = 2

    frequency: Frequency = proto.Field(
        proto.ENUM,
        number=1,
        enum=Frequency,
    )
    start_date: date_pb2.Date = proto.Field(
        proto.MESSAGE,
        number=2,
        message=date_pb2.Date,
    )
    end_date: date_pb2.Date = proto.Field(
        proto.MESSAGE,
        number=3,
        message=date_pb2.Date,
    )


class CSVOptions(proto.Message):
    r"""Options to configure CSV formatted reports.

    Attributes:
        record_separator (str):
            Record separator characters in CSV.
        delimiter (str):
            Delimiter characters in CSV.
        header_required (bool):
            If set, will include a header row in the CSV
            report.
    """

    record_separator: str = proto.Field(
        proto.STRING,
        number=1,
    )
    delimiter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    header_required: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class ParquetOptions(proto.Message):
    r"""Options to configure Parquet formatted reports."""


class CloudStorageFilters(proto.Message):
    r"""Options to filter data on storage systems.
    Next ID: 2

    Attributes:
        bucket (str):
            Bucket for which the report will be
            generated.
    """

    bucket: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CloudStorageDestinationOptions(proto.Message):
    r"""Options to store reports in storage systems.
    Next ID: 3

    Attributes:
        bucket (str):
            Destination bucket.
        destination_path (str):
            Destination path is the path in the bucket
            where the report should be generated.
    """

    bucket: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destination_path: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ObjectMetadataReportOptions(proto.Message):
    r"""Report specification for exporting object metadata.
    Next ID: 4


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        metadata_fields (MutableSequence[str]):
            Metadata fields to be included in the report.
        storage_filters (google.cloud.storageinsights_v1.types.CloudStorageFilters):
            Cloud Storage as the storage system.

            This field is a member of `oneof`_ ``filter``.
        storage_destination_options (google.cloud.storageinsights_v1.types.CloudStorageDestinationOptions):
            Cloud Storage as the storage system.

            This field is a member of `oneof`_ ``destination_options``.
    """

    metadata_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    storage_filters: "CloudStorageFilters" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="filter",
        message="CloudStorageFilters",
    )
    storage_destination_options: "CloudStorageDestinationOptions" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="destination_options",
        message="CloudStorageDestinationOptions",
    )


class ReportConfig(proto.Message):
    r"""Message describing ReportConfig object. ReportConfig is the
    configuration to generate reports.
    See
    https://cloud.google.com/storage/docs/insights/using-inventory-reports#create-config-rest
    for more details on how to set various fields.
    Next ID: 12

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            name of resource. It will be of form
            projects/<project>/locations/<location>/reportConfigs/<report-config-id>.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update time stamp
        frequency_options (google.cloud.storageinsights_v1.types.FrequencyOptions):
            The frequency of report generation.
        csv_options (google.cloud.storageinsights_v1.types.CSVOptions):
            Options for CSV formatted reports.

            This field is a member of `oneof`_ ``report_format``.
        parquet_options (google.cloud.storageinsights_v1.types.ParquetOptions):
            Options for Parquet formatted reports.

            This field is a member of `oneof`_ ``report_format``.
        object_metadata_report_options (google.cloud.storageinsights_v1.types.ObjectMetadataReportOptions):
            Report for exporting object metadata.

            This field is a member of `oneof`_ ``report_kind``.
        labels (MutableMapping[str, str]):
            Labels as key value pairs
        display_name (str):
            User provided display name which can be empty
            and limited to 256 characters that is editable.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    frequency_options: "FrequencyOptions" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="FrequencyOptions",
    )
    csv_options: "CSVOptions" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="report_format",
        message="CSVOptions",
    )
    parquet_options: "ParquetOptions" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="report_format",
        message="ParquetOptions",
    )
    object_metadata_report_options: "ObjectMetadataReportOptions" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="report_kind",
        message="ObjectMetadataReportOptions",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=11,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
