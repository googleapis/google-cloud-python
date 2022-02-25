# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import proto  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.logging.v2',
    manifest={
        'LifecycleState',
        'LogBucket',
        'LogView',
        'LogSink',
        'BigQueryOptions',
        'ListBucketsRequest',
        'ListBucketsResponse',
        'CreateBucketRequest',
        'UpdateBucketRequest',
        'GetBucketRequest',
        'DeleteBucketRequest',
        'UndeleteBucketRequest',
        'ListViewsRequest',
        'ListViewsResponse',
        'CreateViewRequest',
        'UpdateViewRequest',
        'GetViewRequest',
        'DeleteViewRequest',
        'ListSinksRequest',
        'ListSinksResponse',
        'GetSinkRequest',
        'CreateSinkRequest',
        'UpdateSinkRequest',
        'DeleteSinkRequest',
        'LogExclusion',
        'ListExclusionsRequest',
        'ListExclusionsResponse',
        'GetExclusionRequest',
        'CreateExclusionRequest',
        'UpdateExclusionRequest',
        'DeleteExclusionRequest',
        'GetCmekSettingsRequest',
        'UpdateCmekSettingsRequest',
        'CmekSettings',
    },
)


class LifecycleState(proto.Enum):
    r"""LogBucket lifecycle states."""
    LIFECYCLE_STATE_UNSPECIFIED = 0
    ACTIVE = 1
    DELETE_REQUESTED = 2


class LogBucket(proto.Message):
    r"""Describes a repository of logs.

    Attributes:
        name (str):
            The resource name of the bucket. For example:
            "projects/my-project-id/locations/my-location/buckets/my-bucket-id
            The supported locations are: "global"

            For the location of ``global`` it is unspecified where logs
            are actually stored. Once a bucket has been created, the
            location can not be changed.
        description (str):
            Describes this bucket.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of the
            bucket. This is not set for any of the default
            buckets.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of the
            bucket.
        retention_days (int):
            Logs will be retained by default for this
            amount of time, after which they will
            automatically be deleted. The minimum retention
            period is 1 day. If this value is set to zero at
            bucket creation time, the default time of 30
            days will be used.
        locked (bool):
            Whether the bucket has been locked.
            The retention period on a locked bucket may not
            be changed. Locked buckets may only be deleted
            if they are empty.
        lifecycle_state (google.cloud.logging_v2.types.LifecycleState):
            Output only. The bucket lifecycle state.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    retention_days = proto.Field(
        proto.INT32,
        number=11,
    )
    locked = proto.Field(
        proto.BOOL,
        number=9,
    )
    lifecycle_state = proto.Field(
        proto.ENUM,
        number=12,
        enum='LifecycleState',
    )


class LogView(proto.Message):
    r"""Describes a view over logs in a bucket.

    Attributes:
        name (str):
            The resource name of the view.
            For example
            "projects/my-project-id/locations/my-location/buckets/my-bucket-id/views/my-view
        description (str):
            Describes this view.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of the
            view.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of the
            view.
        filter (str):
            Filter that restricts which log entries in a bucket are
            visible in this view. Filters are restricted to be a logical
            AND of ==/!= of any of the following: originating
            project/folder/organization/billing account. resource type
            log id Example: SOURCE("projects/myproject") AND
            resource.type = "gce_instance" AND LOG_ID("stdout")
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    filter = proto.Field(
        proto.STRING,
        number=7,
    )


class LogSink(proto.Message):
    r"""Describes a sink used to export log entries to one of the
    following destinations in any project: a Cloud Storage bucket, a
    BigQuery dataset, or a Cloud Pub/Sub topic. A logs filter
    controls which log entries are exported. The sink must be
    created within a project, organization, billing account, or
    folder.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The client-assigned sink identifier, unique within
            the project. Example: ``"my-syslog-errors-to-pubsub"``. Sink
            identifiers are limited to 100 characters and can include
            only the following characters: upper and lower-case
            alphanumeric characters, underscores, hyphens, and periods.
            First character has to be alphanumeric.
        destination (str):
            Required. The export destination:

            ::

                "storage.googleapis.com/[GCS_BUCKET]"
                "bigquery.googleapis.com/projects/[PROJECT_ID]/datasets/[DATASET]"
                "pubsub.googleapis.com/projects/[PROJECT_ID]/topics/[TOPIC_ID]"

            The sink's ``writer_identity``, set when the sink is
            created, must have permission to write to the destination or
            else the log entries are not exported. For more information,
            see `Exporting Logs with
            Sinks <https://cloud.google.com/logging/docs/api/tasks/exporting-logs>`__.
        filter (str):
            Optional. An `advanced logs
            filter <https://cloud.google.com/logging/docs/view/advanced-queries>`__.
            The only exported log entries are those that are in the
            resource owning the sink and that match the filter. For
            example:

            ::

                logName="projects/[PROJECT_ID]/logs/[LOG_ID]" AND severity>=ERROR
        description (str):
            Optional. A description of this sink.
            The maximum length of the description is 8000
            characters.
        disabled (bool):
            Optional. If set to True, then this sink is
            disabled and it does not export any log entries.
        exclusions (Sequence[google.cloud.logging_v2.types.LogExclusion]):
            Optional. Log entries that match any of the exclusion
            filters will not be exported. If a log entry is matched by
            both ``filter`` and one of ``exclusion_filters`` it will not
            be exported.
        output_version_format (google.cloud.logging_v2.types.LogSink.VersionFormat):
            Deprecated. This field is unused.
        writer_identity (str):
            Output only. An IAM identity—a service account or
            group—under which Logging writes the exported log entries to
            the sink's destination. This field is set by
            [sinks.create][google.logging.v2.ConfigServiceV2.CreateSink]
            and
            [sinks.update][google.logging.v2.ConfigServiceV2.UpdateSink]
            based on the value of ``unique_writer_identity`` in those
            methods.

            Until you grant this identity write-access to the
            destination, log entry exports from this sink will fail. For
            more information, see `Granting Access for a
            Resource <https://cloud.google.com/iam/docs/granting-roles-to-service-accounts#granting_access_to_a_service_account_for_a_resource>`__.
            Consult the destination service's documentation to determine
            the appropriate IAM roles to assign to the identity.
        include_children (bool):
            Optional. This field applies only to sinks owned by
            organizations and folders. If the field is false, the
            default, only the logs owned by the sink's parent resource
            are available for export. If the field is true, then logs
            from all the projects, folders, and billing accounts
            contained in the sink's parent resource are also available
            for export. Whether a particular log entry from the children
            is exported depends on the sink's filter expression. For
            example, if this field is true, then the filter
            ``resource.type=gce_instance`` would export all Compute
            Engine VM instance log entries from all projects in the
            sink's parent. To only export entries from certain child
            projects, filter on the project part of the log name:

            ::

                logName:("projects/test-project1/" OR "projects/test-project2/") AND
                resource.type=gce_instance
        bigquery_options (google.cloud.logging_v2.types.BigQueryOptions):
            Optional. Options that affect sinks exporting
            data to BigQuery.

            This field is a member of `oneof`_ ``options``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of the
            sink.
            This field may not be present for older sinks.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of the
            sink.
            This field may not be present for older sinks.
    """
    class VersionFormat(proto.Enum):
        r"""Deprecated. This is unused."""
        VERSION_FORMAT_UNSPECIFIED = 0
        V2 = 1
        V1 = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    destination = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=5,
    )
    description = proto.Field(
        proto.STRING,
        number=18,
    )
    disabled = proto.Field(
        proto.BOOL,
        number=19,
    )
    exclusions = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message='LogExclusion',
    )
    output_version_format = proto.Field(
        proto.ENUM,
        number=6,
        enum=VersionFormat,
    )
    writer_identity = proto.Field(
        proto.STRING,
        number=8,
    )
    include_children = proto.Field(
        proto.BOOL,
        number=9,
    )
    bigquery_options = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof='options',
        message='BigQueryOptions',
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=14,
        message=timestamp_pb2.Timestamp,
    )


class BigQueryOptions(proto.Message):
    r"""Options that change functionality of a sink exporting data to
    BigQuery.

    Attributes:
        use_partitioned_tables (bool):
            Optional. Whether to use `BigQuery's partition
            tables <https://cloud.google.com/bigquery/docs/partitioned-tables>`__.
            By default, Logging creates dated tables based on the log
            entries' timestamps, e.g. syslog_20170523. With partitioned
            tables the date suffix is no longer present and `special
            query
            syntax <https://cloud.google.com/bigquery/docs/querying-partitioned-tables>`__
            has to be used instead. In both cases, tables are sharded
            based on UTC timezone.
        uses_timestamp_column_partitioning (bool):
            Output only. True if new timestamp column based partitioning
            is in use, false if legacy ingestion-time partitioning is in
            use. All new sinks will have this field set true and will
            use timestamp column based partitioning. If
            use_partitioned_tables is false, this value has no meaning
            and will be false. Legacy sinks using partitioned tables
            will have this field set to false.
    """

    use_partitioned_tables = proto.Field(
        proto.BOOL,
        number=1,
    )
    uses_timestamp_column_partitioning = proto.Field(
        proto.BOOL,
        number=3,
    )


class ListBucketsRequest(proto.Message):
    r"""The parameters to ``ListBuckets``.

    Attributes:
        parent (str):
            Required. The parent resource whose buckets are to be
            listed:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]"
                "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]"
                "folders/[FOLDER_ID]/locations/[LOCATION_ID]"

            Note: The locations portion of the resource must be
            specified, but supplying the character ``-`` in place of
            [LOCATION_ID] will return all buckets.
        page_token (str):
            Optional. If present, then retrieve the next batch of
            results from the preceding call to this method.
            ``pageToken`` must be the value of ``nextPageToken`` from
            the previous response. The values of other method parameters
            should be identical to those in the previous call.
        page_size (int):
            Optional. The maximum number of results to return from this
            request. Non-positive values are ignored. The presence of
            ``nextPageToken`` in the response indicates that more
            results might be available.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )


class ListBucketsResponse(proto.Message):
    r"""The response from ListBuckets.

    Attributes:
        buckets (Sequence[google.cloud.logging_v2.types.LogBucket]):
            A list of buckets.
        next_page_token (str):
            If there might be more results than appear in this response,
            then ``nextPageToken`` is included. To get the next set of
            results, call the same method again using the value of
            ``nextPageToken`` as ``pageToken``.
    """

    @property
    def raw_page(self):
        return self

    buckets = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='LogBucket',
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateBucketRequest(proto.Message):
    r"""The parameters to ``CreateBucket``.

    Attributes:
        parent (str):
            Required. The resource in which to create the bucket:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]"

            Example: ``"projects/my-logging-project/locations/global"``
        bucket_id (str):
            Required. A client-assigned identifier such as
            ``"my-bucket"``. Identifiers are limited to 100 characters
            and can include only letters, digits, underscores, hyphens,
            and periods.
        bucket (google.cloud.logging_v2.types.LogBucket):
            Required. The new bucket. The region
            specified in the new bucket must be compliant
            with any Location Restriction Org Policy. The
            name field in the bucket is ignored.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    bucket_id = proto.Field(
        proto.STRING,
        number=2,
    )
    bucket = proto.Field(
        proto.MESSAGE,
        number=3,
        message='LogBucket',
    )


class UpdateBucketRequest(proto.Message):
    r"""The parameters to ``UpdateBucket``.

    Attributes:
        name (str):
            Required. The full resource name of the bucket to update.

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id"``.
            Also requires permission
            "resourcemanager.projects.updateLiens" to set the locked
            property
        bucket (google.cloud.logging_v2.types.LogBucket):
            Required. The updated bucket.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask that specifies the fields in ``bucket``
            that need an update. A bucket field will be overwritten if,
            and only if, it is in the update mask. ``name`` and output
            only fields cannot be updated.

            For a detailed ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.FieldMask

            Example: ``updateMask=retention_days``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    bucket = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogBucket',
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )


class GetBucketRequest(proto.Message):
    r"""The parameters to ``GetBucket``.

    Attributes:
        name (str):
            Required. The resource name of the bucket:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteBucketRequest(proto.Message):
    r"""The parameters to ``DeleteBucket``.

    Attributes:
        name (str):
            Required. The full resource name of the bucket to delete.

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeleteBucketRequest(proto.Message):
    r"""The parameters to ``UndeleteBucket``.

    Attributes:
        name (str):
            Required. The full resource name of the bucket to undelete.

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
                "folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListViewsRequest(proto.Message):
    r"""The parameters to ``ListViews``.

    Attributes:
        parent (str):
            Required. The bucket whose views are to be listed:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]".
        page_token (str):
            Optional. If present, then retrieve the next batch of
            results from the preceding call to this method.
            ``pageToken`` must be the value of ``nextPageToken`` from
            the previous response. The values of other method parameters
            should be identical to those in the previous call.
        page_size (int):
            Optional. The maximum number of results to return from this
            request. Non-positive values are ignored. The presence of
            ``nextPageToken`` in the response indicates that more
            results might be available.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )


class ListViewsResponse(proto.Message):
    r"""The response from ListViews.

    Attributes:
        views (Sequence[google.cloud.logging_v2.types.LogView]):
            A list of views.
        next_page_token (str):
            If there might be more results than appear in this response,
            then ``nextPageToken`` is included. To get the next set of
            results, call the same method again using the value of
            ``nextPageToken`` as ``pageToken``.
    """

    @property
    def raw_page(self):
        return self

    views = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='LogView',
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateViewRequest(proto.Message):
    r"""The parameters to ``CreateView``.

    Attributes:
        parent (str):
            Required. The bucket in which to create the view

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

            Example:
            ``"projects/my-logging-project/locations/my-location/buckets/my-bucket"``
        view_id (str):
            Required. The id to use for this view.
        view (google.cloud.logging_v2.types.LogView):
            Required. The new view.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    view_id = proto.Field(
        proto.STRING,
        number=2,
    )
    view = proto.Field(
        proto.MESSAGE,
        number=3,
        message='LogView',
    )


class UpdateViewRequest(proto.Message):
    r"""The parameters to ``UpdateView``.

    Attributes:
        name (str):
            Required. The full resource name of the view to update

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id/views/my-view-id"``.
        view (google.cloud.logging_v2.types.LogView):
            Required. The updated view.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask that specifies the fields in ``view``
            that need an update. A field will be overwritten if, and
            only if, it is in the update mask. ``name`` and output only
            fields cannot be updated.

            For a detailed ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.FieldMask

            Example: ``updateMask=filter``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    view = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogView',
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )


class GetViewRequest(proto.Message):
    r"""The parameters to ``GetView``.

    Attributes:
        name (str):
            Required. The resource name of the policy:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id/views/my-view-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteViewRequest(proto.Message):
    r"""The parameters to ``DeleteView``.

    Attributes:
        name (str):
            Required. The full resource name of the view to delete:

            ::

                "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]"

            Example:
            ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id/views/my-view-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSinksRequest(proto.Message):
    r"""The parameters to ``ListSinks``.

    Attributes:
        parent (str):
            Required. The parent resource whose sinks are to be listed:

            ::

                "projects/[PROJECT_ID]"
                "organizations/[ORGANIZATION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]"
                "folders/[FOLDER_ID]".
        page_token (str):
            Optional. If present, then retrieve the next batch of
            results from the preceding call to this method.
            ``pageToken`` must be the value of ``nextPageToken`` from
            the previous response. The values of other method parameters
            should be identical to those in the previous call.
        page_size (int):
            Optional. The maximum number of results to return from this
            request. Non-positive values are ignored. The presence of
            ``nextPageToken`` in the response indicates that more
            results might be available.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )


class ListSinksResponse(proto.Message):
    r"""Result returned from ``ListSinks``.

    Attributes:
        sinks (Sequence[google.cloud.logging_v2.types.LogSink]):
            A list of sinks.
        next_page_token (str):
            If there might be more results than appear in this response,
            then ``nextPageToken`` is included. To get the next set of
            results, call the same method again using the value of
            ``nextPageToken`` as ``pageToken``.
    """

    @property
    def raw_page(self):
        return self

    sinks = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='LogSink',
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetSinkRequest(proto.Message):
    r"""The parameters to ``GetSink``.

    Attributes:
        sink_name (str):
            Required. The resource name of the sink:

            ::

                "projects/[PROJECT_ID]/sinks/[SINK_ID]"
                "organizations/[ORGANIZATION_ID]/sinks/[SINK_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/sinks/[SINK_ID]"
                "folders/[FOLDER_ID]/sinks/[SINK_ID]"

            Example: ``"projects/my-project-id/sinks/my-sink-id"``.
    """

    sink_name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateSinkRequest(proto.Message):
    r"""The parameters to ``CreateSink``.

    Attributes:
        parent (str):
            Required. The resource in which to create the sink:

            ::

                "projects/[PROJECT_ID]"
                "organizations/[ORGANIZATION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]"
                "folders/[FOLDER_ID]"

            Examples: ``"projects/my-logging-project"``,
            ``"organizations/123456789"``.
        sink (google.cloud.logging_v2.types.LogSink):
            Required. The new sink, whose ``name`` parameter is a sink
            identifier that is not already in use.
        unique_writer_identity (bool):
            Optional. Determines the kind of IAM identity returned as
            ``writer_identity`` in the new sink. If this value is
            omitted or set to false, and if the sink's parent is a
            project, then the value returned as ``writer_identity`` is
            the same group or service account used by Logging before the
            addition of writer identities to this API. The sink's
            destination must be in the same project as the sink itself.

            If this field is set to true, or if the sink is owned by a
            non-project resource such as an organization, then the value
            of ``writer_identity`` will be a unique service account used
            only for exports from the new sink. For more information,
            see ``writer_identity`` in
            [LogSink][google.logging.v2.LogSink].
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    sink = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogSink',
    )
    unique_writer_identity = proto.Field(
        proto.BOOL,
        number=3,
    )


class UpdateSinkRequest(proto.Message):
    r"""The parameters to ``UpdateSink``.

    Attributes:
        sink_name (str):
            Required. The full resource name of the sink to update,
            including the parent resource and the sink identifier:

            ::

                "projects/[PROJECT_ID]/sinks/[SINK_ID]"
                "organizations/[ORGANIZATION_ID]/sinks/[SINK_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/sinks/[SINK_ID]"
                "folders/[FOLDER_ID]/sinks/[SINK_ID]"

            Example: ``"projects/my-project-id/sinks/my-sink-id"``.
        sink (google.cloud.logging_v2.types.LogSink):
            Required. The updated sink, whose name is the same
            identifier that appears as part of ``sink_name``.
        unique_writer_identity (bool):
            Optional. See
            [sinks.create][google.logging.v2.ConfigServiceV2.CreateSink]
            for a description of this field. When updating a sink, the
            effect of this field on the value of ``writer_identity`` in
            the updated sink depends on both the old and new values of
            this field:

            -  If the old and new values of this field are both false or
               both true, then there is no change to the sink's
               ``writer_identity``.
            -  If the old value is false and the new value is true, then
               ``writer_identity`` is changed to a unique service
               account.
            -  It is an error if the old value is true and the new value
               is set to false or defaulted to false.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask that specifies the fields in ``sink``
            that need an update. A sink field will be overwritten if,
            and only if, it is in the update mask. ``name`` and output
            only fields cannot be updated.

            An empty updateMask is temporarily treated as using the
            following mask for backwards compatibility purposes:
            destination,filter,includeChildren At some point in the
            future, behavior will be removed and specifying an empty
            updateMask will be an error.

            For a detailed ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.FieldMask

            Example: ``updateMask=filter``.
    """

    sink_name = proto.Field(
        proto.STRING,
        number=1,
    )
    sink = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogSink',
    )
    unique_writer_identity = proto.Field(
        proto.BOOL,
        number=3,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )


class DeleteSinkRequest(proto.Message):
    r"""The parameters to ``DeleteSink``.

    Attributes:
        sink_name (str):
            Required. The full resource name of the sink to delete,
            including the parent resource and the sink identifier:

            ::

                "projects/[PROJECT_ID]/sinks/[SINK_ID]"
                "organizations/[ORGANIZATION_ID]/sinks/[SINK_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/sinks/[SINK_ID]"
                "folders/[FOLDER_ID]/sinks/[SINK_ID]"

            Example: ``"projects/my-project-id/sinks/my-sink-id"``.
    """

    sink_name = proto.Field(
        proto.STRING,
        number=1,
    )


class LogExclusion(proto.Message):
    r"""Specifies a set of log entries that are not to be stored in
    Logging. If your GCP resource receives a large volume of logs,
    you can use exclusions to reduce your chargeable logs.
    Exclusions are processed after log sinks, so you can export log
    entries before they are excluded. Note that organization-level
    and folder-level exclusions don't apply to child resources, and
    that you can't exclude audit log entries.

    Attributes:
        name (str):
            Required. A client-assigned identifier, such as
            ``"load-balancer-exclusion"``. Identifiers are limited to
            100 characters and can include only letters, digits,
            underscores, hyphens, and periods. First character has to be
            alphanumeric.
        description (str):
            Optional. A description of this exclusion.
        filter (str):
            Required. An `advanced logs
            filter <https://cloud.google.com/logging/docs/view/advanced-queries>`__
            that matches the log entries to be excluded. By using the
            `sample
            function <https://cloud.google.com/logging/docs/view/advanced-queries#sample>`__,
            you can exclude less than 100% of the matching log entries.
            For example, the following query matches 99% of low-severity
            log entries from Google Cloud Storage buckets:

            ``"resource.type=gcs_bucket severity<ERROR sample(insertId, 0.99)"``
        disabled (bool):
            Optional. If set to True, then this exclusion is disabled
            and it does not exclude any log entries. You can [update an
            exclusion][google.logging.v2.ConfigServiceV2.UpdateExclusion]
            to change the value of this field.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of the
            exclusion.
            This field may not be present for older
            exclusions.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of the
            exclusion.
            This field may not be present for older
            exclusions.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=2,
    )
    filter = proto.Field(
        proto.STRING,
        number=3,
    )
    disabled = proto.Field(
        proto.BOOL,
        number=4,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class ListExclusionsRequest(proto.Message):
    r"""The parameters to ``ListExclusions``.

    Attributes:
        parent (str):
            Required. The parent resource whose exclusions are to be
            listed.

            ::

                "projects/[PROJECT_ID]"
                "organizations/[ORGANIZATION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]"
                "folders/[FOLDER_ID]".
        page_token (str):
            Optional. If present, then retrieve the next batch of
            results from the preceding call to this method.
            ``pageToken`` must be the value of ``nextPageToken`` from
            the previous response. The values of other method parameters
            should be identical to those in the previous call.
        page_size (int):
            Optional. The maximum number of results to return from this
            request. Non-positive values are ignored. The presence of
            ``nextPageToken`` in the response indicates that more
            results might be available.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )


class ListExclusionsResponse(proto.Message):
    r"""Result returned from ``ListExclusions``.

    Attributes:
        exclusions (Sequence[google.cloud.logging_v2.types.LogExclusion]):
            A list of exclusions.
        next_page_token (str):
            If there might be more results than appear in this response,
            then ``nextPageToken`` is included. To get the next set of
            results, call the same method again using the value of
            ``nextPageToken`` as ``pageToken``.
    """

    @property
    def raw_page(self):
        return self

    exclusions = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='LogExclusion',
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetExclusionRequest(proto.Message):
    r"""The parameters to ``GetExclusion``.

    Attributes:
        name (str):
            Required. The resource name of an existing exclusion:

            ::

                "projects/[PROJECT_ID]/exclusions/[EXCLUSION_ID]"
                "organizations/[ORGANIZATION_ID]/exclusions/[EXCLUSION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/exclusions/[EXCLUSION_ID]"
                "folders/[FOLDER_ID]/exclusions/[EXCLUSION_ID]"

            Example:
            ``"projects/my-project-id/exclusions/my-exclusion-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateExclusionRequest(proto.Message):
    r"""The parameters to ``CreateExclusion``.

    Attributes:
        parent (str):
            Required. The parent resource in which to create the
            exclusion:

            ::

                "projects/[PROJECT_ID]"
                "organizations/[ORGANIZATION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]"
                "folders/[FOLDER_ID]"

            Examples: ``"projects/my-logging-project"``,
            ``"organizations/123456789"``.
        exclusion (google.cloud.logging_v2.types.LogExclusion):
            Required. The new exclusion, whose ``name`` parameter is an
            exclusion name that is not already used in the parent
            resource.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    exclusion = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogExclusion',
    )


class UpdateExclusionRequest(proto.Message):
    r"""The parameters to ``UpdateExclusion``.

    Attributes:
        name (str):
            Required. The resource name of the exclusion to update:

            ::

                "projects/[PROJECT_ID]/exclusions/[EXCLUSION_ID]"
                "organizations/[ORGANIZATION_ID]/exclusions/[EXCLUSION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/exclusions/[EXCLUSION_ID]"
                "folders/[FOLDER_ID]/exclusions/[EXCLUSION_ID]"

            Example:
            ``"projects/my-project-id/exclusions/my-exclusion-id"``.
        exclusion (google.cloud.logging_v2.types.LogExclusion):
            Required. New values for the existing exclusion. Only the
            fields specified in ``update_mask`` are relevant.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. A non-empty list of fields to change in the
            existing exclusion. New values for the fields are taken from
            the corresponding fields in the
            [LogExclusion][google.logging.v2.LogExclusion] included in
            this request. Fields not mentioned in ``update_mask`` are
            not changed and are ignored in the request.

            For example, to change the filter and description of an
            exclusion, specify an ``update_mask`` of
            ``"filter,description"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    exclusion = proto.Field(
        proto.MESSAGE,
        number=2,
        message='LogExclusion',
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


class DeleteExclusionRequest(proto.Message):
    r"""The parameters to ``DeleteExclusion``.

    Attributes:
        name (str):
            Required. The resource name of an existing exclusion to
            delete:

            ::

                "projects/[PROJECT_ID]/exclusions/[EXCLUSION_ID]"
                "organizations/[ORGANIZATION_ID]/exclusions/[EXCLUSION_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/exclusions/[EXCLUSION_ID]"
                "folders/[FOLDER_ID]/exclusions/[EXCLUSION_ID]"

            Example:
            ``"projects/my-project-id/exclusions/my-exclusion-id"``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetCmekSettingsRequest(proto.Message):
    r"""The parameters to
    [GetCmekSettings][google.logging.v2.ConfigServiceV2.GetCmekSettings].

    See `Enabling CMEK for Logs
    Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
    for more information.

    Attributes:
        name (str):
            Required. The resource for which to retrieve CMEK settings.

            ::

                "projects/[PROJECT_ID]/cmekSettings"
                "organizations/[ORGANIZATION_ID]/cmekSettings"
                "billingAccounts/[BILLING_ACCOUNT_ID]/cmekSettings"
                "folders/[FOLDER_ID]/cmekSettings"

            Example: ``"organizations/12345/cmekSettings"``.

            Note: CMEK for the Logs Router can currently only be
            configured for GCP organizations. Once configured, it
            applies to all projects and folders in the GCP organization.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateCmekSettingsRequest(proto.Message):
    r"""The parameters to
    [UpdateCmekSettings][google.logging.v2.ConfigServiceV2.UpdateCmekSettings].

    See `Enabling CMEK for Logs
    Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
    for more information.

    Attributes:
        name (str):
            Required. The resource name for the CMEK settings to update.

            ::

                "projects/[PROJECT_ID]/cmekSettings"
                "organizations/[ORGANIZATION_ID]/cmekSettings"
                "billingAccounts/[BILLING_ACCOUNT_ID]/cmekSettings"
                "folders/[FOLDER_ID]/cmekSettings"

            Example: ``"organizations/12345/cmekSettings"``.

            Note: CMEK for the Logs Router can currently only be
            configured for GCP organizations. Once configured, it
            applies to all projects and folders in the GCP organization.
        cmek_settings (google.cloud.logging_v2.types.CmekSettings):
            Required. The CMEK settings to update.

            See `Enabling CMEK for Logs
            Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
            for more information.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask identifying which fields from
            ``cmek_settings`` should be updated. A field will be
            overwritten if and only if it is in the update mask. Output
            only fields cannot be updated.

            See [FieldMask][google.protobuf.FieldMask] for more
            information.

            Example: ``"updateMask=kmsKeyName"``
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    cmek_settings = proto.Field(
        proto.MESSAGE,
        number=2,
        message='CmekSettings',
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


class CmekSettings(proto.Message):
    r"""Describes the customer-managed encryption key (CMEK) settings
    associated with a project, folder, organization, billing account, or
    flexible resource.

    Note: CMEK for the Logs Router can currently only be configured for
    GCP organizations. Once configured, it applies to all projects and
    folders in the GCP organization.

    See `Enabling CMEK for Logs
    Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
    for more information.

    Attributes:
        name (str):
            Output only. The resource name of the CMEK
            settings.
        kms_key_name (str):
            The resource name for the configured Cloud KMS key.

            KMS key name format:
            "projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEYRING]/cryptoKeys/[KEY]"

            For example:
            ``"projects/my-project-id/locations/my-region/keyRings/key-ring-name/cryptoKeys/key-name"``

            To enable CMEK for the Logs Router, set this field to a
            valid ``kms_key_name`` for which the associated service
            account has the required
            ``roles/cloudkms.cryptoKeyEncrypterDecrypter`` role assigned
            for the key.

            The Cloud KMS key used by the Log Router can be updated by
            changing the ``kms_key_name`` to a new valid key name.
            Encryption operations that are in progress will be completed
            with the key that was in use when they started. Decryption
            operations will be completed using the key that was used at
            the time of encryption unless access to that key has been
            revoked.

            To disable CMEK for the Logs Router, set this field to an
            empty string.

            See `Enabling CMEK for Logs
            Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
            for more information.
        service_account_id (str):
            Output only. The service account that will be used by the
            Logs Router to access your Cloud KMS key.

            Before enabling CMEK for Logs Router, you must first assign
            the role ``roles/cloudkms.cryptoKeyEncrypterDecrypter`` to
            the service account that the Logs Router will use to access
            your Cloud KMS key. Use
            [GetCmekSettings][google.logging.v2.ConfigServiceV2.GetCmekSettings]
            to obtain the service account ID.

            See `Enabling CMEK for Logs
            Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
            for more information.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    kms_key_name = proto.Field(
        proto.STRING,
        number=2,
    )
    service_account_id = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
