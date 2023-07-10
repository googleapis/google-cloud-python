# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import proto  # type: ignore

from google.cloud.dataplex_v1.types import (
    data_profile,
    data_quality,
    processing,
    resources,
)

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "DataScanType",
        "CreateDataScanRequest",
        "UpdateDataScanRequest",
        "DeleteDataScanRequest",
        "GetDataScanRequest",
        "ListDataScansRequest",
        "ListDataScansResponse",
        "RunDataScanRequest",
        "RunDataScanResponse",
        "GetDataScanJobRequest",
        "ListDataScanJobsRequest",
        "ListDataScanJobsResponse",
        "DataScan",
        "DataScanJob",
    },
)


class DataScanType(proto.Enum):
    r"""The type of DataScan.

    Values:
        DATA_SCAN_TYPE_UNSPECIFIED (0):
            The DataScan type is unspecified.
        DATA_QUALITY (1):
            Data Quality scan.
        DATA_PROFILE (2):
            Data Profile scan.
    """
    DATA_SCAN_TYPE_UNSPECIFIED = 0
    DATA_QUALITY = 1
    DATA_PROFILE = 2


class CreateDataScanRequest(proto.Message):
    r"""Create dataScan request.

    Attributes:
        parent (str):
            Required. The resource name of the parent location:
            ``projects/{project}/locations/{location_id}`` where
            ``project`` refers to a *project_id* or *project_number* and
            ``location_id`` refers to a GCP region.
        data_scan (google.cloud.dataplex_v1.types.DataScan):
            Required. DataScan resource.
        data_scan_id (str):
            Required. DataScan identifier.

            -  Must contain only lowercase letters, numbers and hyphens.
            -  Must start with a letter.
            -  Must end with a number or a letter.
            -  Must be between 1-63 characters.
            -  Must be unique within the customer project / location.
        validate_only (bool):
            Optional. Only validate the request, but do not perform
            mutations. The default is ``false``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_scan: "DataScan" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DataScan",
    )
    data_scan_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateDataScanRequest(proto.Message):
    r"""Update dataScan request.

    Attributes:
        data_scan (google.cloud.dataplex_v1.types.DataScan):
            Required. DataScan resource to be updated.

            Only fields specified in ``update_mask`` are updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        validate_only (bool):
            Optional. Only validate the request, but do not perform
            mutations. The default is ``false``.
    """

    data_scan: "DataScan" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DataScan",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteDataScanRequest(proto.Message):
    r"""Delete dataScan request.

    Attributes:
        name (str):
            Required. The resource name of the dataScan:
            ``projects/{project}/locations/{location_id}/dataScans/{data_scan_id}``
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetDataScanRequest(proto.Message):
    r"""Get dataScan request.

    Attributes:
        name (str):
            Required. The resource name of the dataScan:
            ``projects/{project}/locations/{location_id}/dataScans/{data_scan_id}``
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
        view (google.cloud.dataplex_v1.types.GetDataScanRequest.DataScanView):
            Optional. Select the DataScan view to return. Defaults to
            ``BASIC``.
    """

    class DataScanView(proto.Enum):
        r"""DataScan view options.

        Values:
            DATA_SCAN_VIEW_UNSPECIFIED (0):
                The API will default to the ``BASIC`` view.
            BASIC (1):
                Basic view that does not include *spec* and *result*.
            FULL (10):
                Include everything.
        """
        DATA_SCAN_VIEW_UNSPECIFIED = 0
        BASIC = 1
        FULL = 10

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: DataScanView = proto.Field(
        proto.ENUM,
        number=2,
        enum=DataScanView,
    )


class ListDataScansRequest(proto.Message):
    r"""List dataScans request.

    Attributes:
        parent (str):
            Required. The resource name of the parent location:
            ``projects/{project}/locations/{location_id}`` where
            ``project`` refers to a *project_id* or *project_number* and
            ``location_id`` refers to a GCP region.
        page_size (int):
            Optional. Maximum number of dataScans to
            return. The service may return fewer than this
            value. If unspecified, at most 500 scans will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListDataScans`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListDataScans`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter request.
        order_by (str):
            Optional. Order by fields (``name`` or ``create_time``) for
            the result. If not specified, the ordering is undefined.
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


class ListDataScansResponse(proto.Message):
    r"""List dataScans response.

    Attributes:
        data_scans (MutableSequence[google.cloud.dataplex_v1.types.DataScan]):
            DataScans (``BASIC`` view only) under the given parent
            location.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    data_scans: MutableSequence["DataScan"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataScan",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class RunDataScanRequest(proto.Message):
    r"""Run DataScan Request

    Attributes:
        name (str):
            Required. The resource name of the DataScan:
            ``projects/{project}/locations/{location_id}/dataScans/{data_scan_id}``.
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.

            Only **OnDemand** data scans are allowed.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RunDataScanResponse(proto.Message):
    r"""Run DataScan Response.

    Attributes:
        job (google.cloud.dataplex_v1.types.DataScanJob):
            DataScanJob created by RunDataScan request.
    """

    job: "DataScanJob" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DataScanJob",
    )


class GetDataScanJobRequest(proto.Message):
    r"""Get DataScanJob request.

    Attributes:
        name (str):
            Required. The resource name of the DataScanJob:
            ``projects/{project}/locations/{location_id}/dataScans/{data_scan_id}/jobs/{data_scan_job_id}``
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
        view (google.cloud.dataplex_v1.types.GetDataScanJobRequest.DataScanJobView):
            Optional. Select the DataScanJob view to return. Defaults to
            ``BASIC``.
    """

    class DataScanJobView(proto.Enum):
        r"""DataScanJob view options.

        Values:
            DATA_SCAN_JOB_VIEW_UNSPECIFIED (0):
                The API will default to the ``BASIC`` view.
            BASIC (1):
                Basic view that does not include *spec* and *result*.
            FULL (10):
                Include everything.
        """
        DATA_SCAN_JOB_VIEW_UNSPECIFIED = 0
        BASIC = 1
        FULL = 10

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: DataScanJobView = proto.Field(
        proto.ENUM,
        number=2,
        enum=DataScanJobView,
    )


class ListDataScanJobsRequest(proto.Message):
    r"""List DataScanJobs request.

    Attributes:
        parent (str):
            Required. The resource name of the parent environment:
            ``projects/{project}/locations/{location_id}/dataScans/{data_scan_id}``
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
        page_size (int):
            Optional. Maximum number of DataScanJobs to
            return. The service may return fewer than this
            value. If unspecified, at most 10 DataScanJobs
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListDataScanJobs`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListDataScanJobs`` must match the call that
            provided the page token.
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


class ListDataScanJobsResponse(proto.Message):
    r"""List DataScanJobs response.

    Attributes:
        data_scan_jobs (MutableSequence[google.cloud.dataplex_v1.types.DataScanJob]):
            DataScanJobs (``BASIC`` view only) under a given dataScan.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    data_scan_jobs: MutableSequence["DataScanJob"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataScanJob",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DataScan(proto.Message):
    r"""Represents a user-visible job which provides the insights for the
    related data source.

    For example:

    -  Data Quality: generates queries based on the rules and runs
       against the data to get data quality check results.
    -  Data Profile: analyzes the data in table(s) and generates
       insights about the structure, content and relationships (such as
       null percent, cardinality, min/max/mean, etc).

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The relative resource name of the scan, of the
            form:
            ``projects/{project}/locations/{location_id}/dataScans/{datascan_id}``,
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
        uid (str):
            Output only. System generated globally unique
            ID for the scan. This ID will be different if
            the scan is deleted and re-created with the same
            name.
        description (str):
            Optional. Description of the scan.

            -  Must be between 1-1024 characters.
        display_name (str):
            Optional. User friendly display name.

            -  Must be between 1-256 characters.
        labels (MutableMapping[str, str]):
            Optional. User-defined labels for the scan.
        state (google.cloud.dataplex_v1.types.State):
            Output only. Current state of the DataScan.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the scan was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the scan was last
            updated.
        data (google.cloud.dataplex_v1.types.DataSource):
            Required. The data source for DataScan.
        execution_spec (google.cloud.dataplex_v1.types.DataScan.ExecutionSpec):
            Optional. DataScan execution settings.
            If not specified, the fields in it will use
            their default values.
        execution_status (google.cloud.dataplex_v1.types.DataScan.ExecutionStatus):
            Output only. Status of the data scan
            execution.
        type_ (google.cloud.dataplex_v1.types.DataScanType):
            Output only. The type of DataScan.
        data_quality_spec (google.cloud.dataplex_v1.types.DataQualitySpec):
            DataQualityScan related setting.

            This field is a member of `oneof`_ ``spec``.
        data_profile_spec (google.cloud.dataplex_v1.types.DataProfileSpec):
            DataProfileScan related setting.

            This field is a member of `oneof`_ ``spec``.
        data_quality_result (google.cloud.dataplex_v1.types.DataQualityResult):
            Output only. The result of the data quality
            scan.

            This field is a member of `oneof`_ ``result``.
        data_profile_result (google.cloud.dataplex_v1.types.DataProfileResult):
            Output only. The result of the data profile
            scan.

            This field is a member of `oneof`_ ``result``.
    """

    class ExecutionSpec(proto.Message):
        r"""DataScan execution settings.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            trigger (google.cloud.dataplex_v1.types.Trigger):
                Optional. Spec related to how often and when a scan should
                be triggered.

                If not specified, the default is ``OnDemand``, which means
                the scan will not run until the user calls ``RunDataScan``
                API.
            field (str):
                Immutable. The unnested field (of type *Date* or
                *Timestamp*) that contains values which monotonically
                increase over time.

                If not specified, a data scan will run for all data in the
                table.

                This field is a member of `oneof`_ ``incremental``.
        """

        trigger: processing.Trigger = proto.Field(
            proto.MESSAGE,
            number=1,
            message=processing.Trigger,
        )
        field: str = proto.Field(
            proto.STRING,
            number=100,
            oneof="incremental",
        )

    class ExecutionStatus(proto.Message):
        r"""Status of the data scan execution.

        Attributes:
            latest_job_start_time (google.protobuf.timestamp_pb2.Timestamp):
                The time when the latest DataScanJob started.
            latest_job_end_time (google.protobuf.timestamp_pb2.Timestamp):
                The time when the latest DataScanJob ended.
        """

        latest_job_start_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=4,
            message=timestamp_pb2.Timestamp,
        )
        latest_job_end_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=5,
            message=timestamp_pb2.Timestamp,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    state: resources.State = proto.Field(
        proto.ENUM,
        number=6,
        enum=resources.State,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    data: processing.DataSource = proto.Field(
        proto.MESSAGE,
        number=9,
        message=processing.DataSource,
    )
    execution_spec: ExecutionSpec = proto.Field(
        proto.MESSAGE,
        number=10,
        message=ExecutionSpec,
    )
    execution_status: ExecutionStatus = proto.Field(
        proto.MESSAGE,
        number=11,
        message=ExecutionStatus,
    )
    type_: "DataScanType" = proto.Field(
        proto.ENUM,
        number=12,
        enum="DataScanType",
    )
    data_quality_spec: data_quality.DataQualitySpec = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="spec",
        message=data_quality.DataQualitySpec,
    )
    data_profile_spec: data_profile.DataProfileSpec = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="spec",
        message=data_profile.DataProfileSpec,
    )
    data_quality_result: data_quality.DataQualityResult = proto.Field(
        proto.MESSAGE,
        number=200,
        oneof="result",
        message=data_quality.DataQualityResult,
    )
    data_profile_result: data_profile.DataProfileResult = proto.Field(
        proto.MESSAGE,
        number=201,
        oneof="result",
        message=data_profile.DataProfileResult,
    )


class DataScanJob(proto.Message):
    r"""A DataScanJob represents an instance of DataScan execution.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The relative resource name of the DataScanJob,
            of the form:
            ``projects/{project}/locations/{location_id}/dataScans/{datascan_id}/jobs/{job_id}``,
            where ``project`` refers to a *project_id* or
            *project_number* and ``location_id`` refers to a GCP region.
        uid (str):
            Output only. System generated globally unique
            ID for the DataScanJob.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the DataScanJob
            was started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the DataScanJob
            ended.
        state (google.cloud.dataplex_v1.types.DataScanJob.State):
            Output only. Execution state for the
            DataScanJob.
        message (str):
            Output only. Additional information about the
            current state.
        type_ (google.cloud.dataplex_v1.types.DataScanType):
            Output only. The type of the parent DataScan.
        data_quality_spec (google.cloud.dataplex_v1.types.DataQualitySpec):
            Output only. DataQualityScan related setting.

            This field is a member of `oneof`_ ``spec``.
        data_profile_spec (google.cloud.dataplex_v1.types.DataProfileSpec):
            Output only. DataProfileScan related setting.

            This field is a member of `oneof`_ ``spec``.
        data_quality_result (google.cloud.dataplex_v1.types.DataQualityResult):
            Output only. The result of the data quality
            scan.

            This field is a member of `oneof`_ ``result``.
        data_profile_result (google.cloud.dataplex_v1.types.DataProfileResult):
            Output only. The result of the data profile
            scan.

            This field is a member of `oneof`_ ``result``.
    """

    class State(proto.Enum):
        r"""Execution state for the DataScanJob.

        Values:
            STATE_UNSPECIFIED (0):
                The DataScanJob state is unspecified.
            RUNNING (1):
                The DataScanJob is running.
            CANCELING (2):
                The DataScanJob is canceling.
            CANCELLED (3):
                The DataScanJob cancellation was successful.
            SUCCEEDED (4):
                The DataScanJob completed successfully.
            FAILED (5):
                The DataScanJob is no longer running due to
                an error.
            PENDING (7):
                The DataScanJob has been created but not
                started to run yet.
        """
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        CANCELING = 2
        CANCELLED = 3
        SUCCEEDED = 4
        FAILED = 5
        PENDING = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    message: str = proto.Field(
        proto.STRING,
        number=6,
    )
    type_: "DataScanType" = proto.Field(
        proto.ENUM,
        number=7,
        enum="DataScanType",
    )
    data_quality_spec: data_quality.DataQualitySpec = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="spec",
        message=data_quality.DataQualitySpec,
    )
    data_profile_spec: data_profile.DataProfileSpec = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="spec",
        message=data_profile.DataProfileSpec,
    )
    data_quality_result: data_quality.DataQualityResult = proto.Field(
        proto.MESSAGE,
        number=200,
        oneof="result",
        message=data_quality.DataQualityResult,
    )
    data_profile_result: data_profile.DataProfileResult = proto.Field(
        proto.MESSAGE,
        number=201,
        oneof="result",
        message=data_profile.DataProfileResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
