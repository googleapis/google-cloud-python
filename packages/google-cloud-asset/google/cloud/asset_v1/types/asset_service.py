# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.asset_v1.types import assets as gca_assets
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1",
    manifest={
        "ContentType",
        "ExportAssetsRequest",
        "ExportAssetsResponse",
        "ListAssetsRequest",
        "ListAssetsResponse",
        "BatchGetAssetsHistoryRequest",
        "BatchGetAssetsHistoryResponse",
        "CreateFeedRequest",
        "GetFeedRequest",
        "ListFeedsRequest",
        "ListFeedsResponse",
        "UpdateFeedRequest",
        "DeleteFeedRequest",
        "OutputConfig",
        "OutputResult",
        "GcsOutputResult",
        "GcsDestination",
        "BigQueryDestination",
        "PartitionSpec",
        "PubsubDestination",
        "FeedOutputConfig",
        "Feed",
        "SearchAllResourcesRequest",
        "SearchAllResourcesResponse",
        "SearchAllIamPoliciesRequest",
        "SearchAllIamPoliciesResponse",
        "IamPolicyAnalysisQuery",
        "AnalyzeIamPolicyRequest",
        "AnalyzeIamPolicyResponse",
        "IamPolicyAnalysisOutputConfig",
        "AnalyzeIamPolicyLongrunningRequest",
        "AnalyzeIamPolicyLongrunningResponse",
    },
)


class ContentType(proto.Enum):
    r"""Asset content type."""
    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2
    ORG_POLICY = 4
    ACCESS_POLICY = 5
    OS_INVENTORY = 6


class ExportAssetsRequest(proto.Message):
    r"""Export asset request.
    Attributes:
        parent (str):
            Required. The relative name of the root
            asset. This can only be an organization number
            (such as "organizations/123"), a project ID
            (such as "projects/my-project-id"), or a project
            number (such as "projects/12345"), or a folder
            number (such as "folders/123").
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp to take an asset snapshot. This can
            only be set to a timestamp between the current
            time and the current time minus 35 days
            (inclusive). If not specified, the current time
            will be used. Due to delays in resource data
            collection and indexing, there is a volatile
            window during which running the same query may
            get different results.
        asset_types (Sequence[str]):
            A list of asset types to take a snapshot for. For example:
            "compute.googleapis.com/Disk".

            Regular expressions are also supported. For example:

            -  "compute.googleapis.com.*" snapshots resources whose
               asset type starts with "compute.googleapis.com".
            -  ".*Instance" snapshots resources whose asset type ends
               with "Instance".
            -  ".*Instance.*" snapshots resources whose asset type
               contains "Instance".

            See `RE2 <https://github.com/google/re2/wiki/Syntax>`__ for
            all supported regular expression syntax. If the regular
            expression does not match any supported asset type, an
            INVALID_ARGUMENT error will be returned.

            If specified, only matching assets will be returned,
            otherwise, it will snapshot all asset types. See
            `Introduction to Cloud Asset
            Inventory <https://cloud.google.com/asset-inventory/docs/overview>`__
            for all supported asset types.
        content_type (google.cloud.asset_v1.types.ContentType):
            Asset content type. If not specified, no
            content but the asset name will be returned.
        output_config (google.cloud.asset_v1.types.OutputConfig):
            Required. Output configuration indicating
            where the results will be output to.
    """

    parent = proto.Field(proto.STRING, number=1,)
    read_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    asset_types = proto.RepeatedField(proto.STRING, number=3,)
    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)
    output_config = proto.Field(proto.MESSAGE, number=5, message="OutputConfig",)


class ExportAssetsResponse(proto.Message):
    r"""The export asset response. This message is returned by the
    [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
    method in the returned
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field.

    Attributes:
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Time the snapshot was taken.
        output_config (google.cloud.asset_v1.types.OutputConfig):
            Output configuration indicating where the
            results were output to.
        output_result (google.cloud.asset_v1.types.OutputResult):
            Output result indicating where the assets were exported to.
            For example, a set of actual Google Cloud Storage object
            uris where the assets are exported to. The uris can be
            different from what [output_config] has specified, as the
            service will split the output object into multiple ones once
            it exceeds a single Google Cloud Storage object limit.
    """

    read_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    output_config = proto.Field(proto.MESSAGE, number=2, message="OutputConfig",)
    output_result = proto.Field(proto.MESSAGE, number=3, message="OutputResult",)


class ListAssetsRequest(proto.Message):
    r"""ListAssets request.
    Attributes:
        parent (str):
            Required. Name of the organization or project the assets
            belong to. Format: "organizations/[organization-number]"
            (such as "organizations/123"), "projects/[project-id]" (such
            as "projects/my-project-id"), or "projects/[project-number]"
            (such as "projects/12345").
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp to take an asset snapshot. This can
            only be set to a timestamp between the current
            time and the current time minus 35 days
            (inclusive). If not specified, the current time
            will be used. Due to delays in resource data
            collection and indexing, there is a volatile
            window during which running the same query may
            get different results.
        asset_types (Sequence[str]):
            A list of asset types to take a snapshot for. For example:
            "compute.googleapis.com/Disk".

            Regular expression is also supported. For example:

            -  "compute.googleapis.com.*" snapshots resources whose
               asset type starts with "compute.googleapis.com".
            -  ".*Instance" snapshots resources whose asset type ends
               with "Instance".
            -  ".*Instance.*" snapshots resources whose asset type
               contains "Instance".

            See `RE2 <https://github.com/google/re2/wiki/Syntax>`__ for
            all supported regular expression syntax. If the regular
            expression does not match any supported asset type, an
            INVALID_ARGUMENT error will be returned.

            If specified, only matching assets will be returned,
            otherwise, it will snapshot all asset types. See
            `Introduction to Cloud Asset
            Inventory <https://cloud.google.com/asset-inventory/docs/overview>`__
            for all supported asset types.
        content_type (google.cloud.asset_v1.types.ContentType):
            Asset content type. If not specified, no
            content but the asset name will be returned.
        page_size (int):
            The maximum number of assets to be returned
            in a single response. Default is 100, minimum is
            1, and maximum is 1000.
        page_token (str):
            The ``next_page_token`` returned from the previous
            ``ListAssetsResponse``, or unspecified for the first
            ``ListAssetsRequest``. It is a continuation of a prior
            ``ListAssets`` call, and the API should return the next page
            of assets.
    """

    parent = proto.Field(proto.STRING, number=1,)
    read_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    asset_types = proto.RepeatedField(proto.STRING, number=3,)
    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)
    page_size = proto.Field(proto.INT32, number=5,)
    page_token = proto.Field(proto.STRING, number=6,)


class ListAssetsResponse(proto.Message):
    r"""ListAssets response.
    Attributes:
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Time the snapshot was taken.
        assets (Sequence[google.cloud.asset_v1.types.Asset]):
            Assets.
        next_page_token (str):
            Token to retrieve the next page of results.
            It expires 72 hours after the page token for the
            first page is generated. Set to empty if there
            are no remaining results.
    """

    @property
    def raw_page(self):
        return self

    read_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    assets = proto.RepeatedField(proto.MESSAGE, number=2, message=gca_assets.Asset,)
    next_page_token = proto.Field(proto.STRING, number=3,)


class BatchGetAssetsHistoryRequest(proto.Message):
    r"""Batch get assets history request.
    Attributes:
        parent (str):
            Required. The relative name of the root
            asset. It can only be an organization number
            (such as "organizations/123"), a project ID
            (such as "projects/my-project-id")", or a
            project number (such as "projects/12345").
        asset_names (Sequence[str]):
            A list of the full names of the assets. See:
            https://cloud.google.com/asset-inventory/docs/resource-name-format
            Example:

            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.

            The request becomes a no-op if the asset name list is empty,
            and the max size of the asset name list is 100 in one
            request.
        content_type (google.cloud.asset_v1.types.ContentType):
            Optional. The content type.
        read_time_window (google.cloud.asset_v1.types.TimeWindow):
            Optional. The time window for the asset history. Both
            start_time and end_time are optional and if set, it must be
            after the current time minus 35 days. If end_time is not
            set, it is default to current timestamp. If start_time is
            not set, the snapshot of the assets at end_time will be
            returned. The returned results contain all temporal assets
            whose time window overlap with read_time_window.
    """

    parent = proto.Field(proto.STRING, number=1,)
    asset_names = proto.RepeatedField(proto.STRING, number=2,)
    content_type = proto.Field(proto.ENUM, number=3, enum="ContentType",)
    read_time_window = proto.Field(
        proto.MESSAGE, number=4, message=gca_assets.TimeWindow,
    )


class BatchGetAssetsHistoryResponse(proto.Message):
    r"""Batch get assets history response.
    Attributes:
        assets (Sequence[google.cloud.asset_v1.types.TemporalAsset]):
            A list of assets with valid time windows.
    """

    assets = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gca_assets.TemporalAsset,
    )


class CreateFeedRequest(proto.Message):
    r"""Create asset feed request.
    Attributes:
        parent (str):
            Required. The name of the
            project/folder/organization where this feed
            should be created in. It can only be an
            organization number (such as
            "organizations/123"), a folder number (such as
            "folders/123"), a project ID (such as
            "projects/my-project-id")", or a project number
            (such as "projects/12345").
        feed_id (str):
            Required. This is the client-assigned asset
            feed identifier and it needs to be unique under
            a specific parent project/folder/organization.
        feed (google.cloud.asset_v1.types.Feed):
            Required. The feed details. The field ``name`` must be empty
            and it will be generated in the format of:
            projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    parent = proto.Field(proto.STRING, number=1,)
    feed_id = proto.Field(proto.STRING, number=2,)
    feed = proto.Field(proto.MESSAGE, number=3, message="Feed",)


class GetFeedRequest(proto.Message):
    r"""Get asset feed request.
    Attributes:
        name (str):
            Required. The name of the Feed and it must be in the format
            of: projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    name = proto.Field(proto.STRING, number=1,)


class ListFeedsRequest(proto.Message):
    r"""List asset feeds request.
    Attributes:
        parent (str):
            Required. The parent
            project/folder/organization whose feeds are to
            be listed. It can only be using
            project/folder/organization number (such as
            "folders/12345")", or a project ID (such as
            "projects/my-project-id").
    """

    parent = proto.Field(proto.STRING, number=1,)


class ListFeedsResponse(proto.Message):
    r"""
    Attributes:
        feeds (Sequence[google.cloud.asset_v1.types.Feed]):
            A list of feeds.
    """

    feeds = proto.RepeatedField(proto.MESSAGE, number=1, message="Feed",)


class UpdateFeedRequest(proto.Message):
    r"""Update asset feed request.
    Attributes:
        feed (google.cloud.asset_v1.types.Feed):
            Required. The new values of feed details. It must match an
            existing feed and the field ``name`` must be in the format
            of: projects/project_number/feeds/feed_id or
            folders/folder_number/feeds/feed_id or
            organizations/organization_number/feeds/feed_id.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Only updates the ``feed`` fields indicated by this
            mask. The field mask must not be empty, and it must not
            contain fields that are immutable or only set by the server.
    """

    feed = proto.Field(proto.MESSAGE, number=1, message="Feed",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteFeedRequest(proto.Message):
    r"""
    Attributes:
        name (str):
            Required. The name of the feed and it must be in the format
            of: projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    name = proto.Field(proto.STRING, number=1,)


class OutputConfig(proto.Message):
    r"""Output configuration for export assets destination.
    Attributes:
        gcs_destination (google.cloud.asset_v1.types.GcsDestination):
            Destination on Cloud Storage.
        bigquery_destination (google.cloud.asset_v1.types.BigQueryDestination):
            Destination on BigQuery. The output table
            stores the fields in asset proto as columns in
            BigQuery.
    """

    gcs_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message="GcsDestination",
    )
    bigquery_destination = proto.Field(
        proto.MESSAGE, number=2, oneof="destination", message="BigQueryDestination",
    )


class OutputResult(proto.Message):
    r"""Output result of export assets.
    Attributes:
        gcs_result (google.cloud.asset_v1.types.GcsOutputResult):
            Export result on Cloud Storage.
    """

    gcs_result = proto.Field(
        proto.MESSAGE, number=1, oneof="result", message="GcsOutputResult",
    )


class GcsOutputResult(proto.Message):
    r"""A Cloud Storage output result.
    Attributes:
        uris (Sequence[str]):
            List of uris of the Cloud Storage objects. Example:
            "gs://bucket_name/object_name".
    """

    uris = proto.RepeatedField(proto.STRING, number=1,)


class GcsDestination(proto.Message):
    r"""A Cloud Storage location.
    Attributes:
        uri (str):
            The uri of the Cloud Storage object. It's the same uri that
            is used by gsutil. Example: "gs://bucket_name/object_name".
            See `Viewing and Editing Object
            Metadata <https://cloud.google.com/storage/docs/viewing-editing-metadata>`__
            for more information.

            If the specified Cloud Storage object already exists and
            there is no
            `hold <https://cloud.google.com/storage/docs/object-holds>`__,
            it will be overwritten with the exported result.
        uri_prefix (str):
            The uri prefix of all generated Cloud Storage objects.
            Example: "gs://bucket_name/object_name_prefix". Each object
            uri is in format: "gs://bucket_name/object_name_prefix// and
            only contains assets for that type. starts from 0. Example:
            "gs://bucket_name/object_name_prefix/compute.googleapis.com/Disk/0"
            is the first shard of output objects containing all
            compute.googleapis.com/Disk assets. An INVALID_ARGUMENT
            error will be returned if file with the same name
            "gs://bucket_name/object_name_prefix" already exists.
    """

    uri = proto.Field(proto.STRING, number=1, oneof="object_uri",)
    uri_prefix = proto.Field(proto.STRING, number=2, oneof="object_uri",)


class BigQueryDestination(proto.Message):
    r"""A BigQuery destination for exporting assets to.
    Attributes:
        dataset (str):
            Required. The BigQuery dataset in format
            "projects/projectId/datasets/datasetId", to which the
            snapshot result should be exported. If this dataset does not
            exist, the export call returns an INVALID_ARGUMENT error.
        table (str):
            Required. The BigQuery table to which the
            snapshot result should be written. If this table
            does not exist, a new table with the given name
            will be created.
        force (bool):
            If the destination table already exists and this flag is
            ``TRUE``, the table will be overwritten by the contents of
            assets snapshot. If the flag is ``FALSE`` or unset and the
            destination table already exists, the export call returns an
            INVALID_ARGUMEMT error.
        partition_spec (google.cloud.asset_v1.types.PartitionSpec):
            [partition_spec] determines whether to export to partitioned
            table(s) and how to partition the data.

            If [partition_spec] is unset or
            [partition_spec.partition_key] is unset or
            ``PARTITION_KEY_UNSPECIFIED``, the snapshot results will be
            exported to non-partitioned table(s). [force] will decide
            whether to overwrite existing table(s).

            If [partition_spec] is specified. First, the snapshot
            results will be written to partitioned table(s) with two
            additional timestamp columns, readTime and requestTime, one
            of which will be the partition key. Secondly, in the case
            when any destination table already exists, it will first try
            to update existing table's schema as necessary by appending
            additional columns. Then, if [force] is ``TRUE``, the
            corresponding partition will be overwritten by the snapshot
            results (data in different partitions will remain intact);
            if [force] is unset or ``FALSE``, it will append the data.
            An error will be returned if the schema update or data
            appension fails.
        separate_tables_per_asset_type (bool):
            If this flag is ``TRUE``, the snapshot results will be
            written to one or multiple tables, each of which contains
            results of one asset type. The [force] and [partition_spec]
            fields will apply to each of them.

            Field [table] will be concatenated with "*" and the asset
            type names (see
            https://cloud.google.com/asset-inventory/docs/supported-asset-types
            for supported asset types) to construct per-asset-type table
            names, in which all non-alphanumeric characters like "." and
            "/" will be substituted by "*". Example: if field [table] is
            "mytable" and snapshot results contain
            "storage.googleapis.com/Bucket" assets, the corresponding
            table name will be "mytable_storage_googleapis_com_Bucket".
            If any of these tables does not exist, a new table with the
            concatenated name will be created.

            When [content_type] in the ExportAssetsRequest is
            ``RESOURCE``, the schema of each table will include
            RECORD-type columns mapped to the nested fields in the
            Asset.resource.data field of that asset type (up to the 15
            nested level BigQuery supports
            (https://cloud.google.com/bigquery/docs/nested-repeated#limitations)).
            The fields in >15 nested levels will be stored in JSON
            format string as a child column of its parent RECORD column.

            If error occurs when exporting to any table, the whole
            export call will return an error but the export results that
            already succeed will persist. Example: if exporting to
            table_type_A succeeds when exporting to table_type_B fails
            during one export call, the results in table_type_A will
            persist and there will not be partial results persisting in
            a table.
    """

    dataset = proto.Field(proto.STRING, number=1,)
    table = proto.Field(proto.STRING, number=2,)
    force = proto.Field(proto.BOOL, number=3,)
    partition_spec = proto.Field(proto.MESSAGE, number=4, message="PartitionSpec",)
    separate_tables_per_asset_type = proto.Field(proto.BOOL, number=5,)


class PartitionSpec(proto.Message):
    r"""Specifications of BigQuery partitioned table as export
    destination.

    Attributes:
        partition_key (google.cloud.asset_v1.types.PartitionSpec.PartitionKey):
            The partition key for BigQuery partitioned
            table.
    """

    class PartitionKey(proto.Enum):
        r"""This enum is used to determine the partition key column when
        exporting assets to BigQuery partitioned table(s). Note that, if the
        partition key is a timestamp column, the actual partition is based
        on its date value (expressed in UTC. see details in
        https://cloud.google.com/bigquery/docs/partitioned-tables#date_timestamp_partitioned_tables).
        """
        PARTITION_KEY_UNSPECIFIED = 0
        READ_TIME = 1
        REQUEST_TIME = 2

    partition_key = proto.Field(proto.ENUM, number=1, enum=PartitionKey,)


class PubsubDestination(proto.Message):
    r"""A Pub/Sub destination.
    Attributes:
        topic (str):
            The name of the Pub/Sub topic to publish to. Example:
            ``projects/PROJECT_ID/topics/TOPIC_ID``.
    """

    topic = proto.Field(proto.STRING, number=1,)


class FeedOutputConfig(proto.Message):
    r"""Output configuration for asset feed destination.
    Attributes:
        pubsub_destination (google.cloud.asset_v1.types.PubsubDestination):
            Destination on Pub/Sub.
    """

    pubsub_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message="PubsubDestination",
    )


class Feed(proto.Message):
    r"""An asset feed used to export asset updates to a destinations.
    An asset feed filter controls what updates are exported. The
    asset feed must be created within a project, organization, or
    folder. Supported destinations are:
    Pub/Sub topics.

    Attributes:
        name (str):
            Required. The format will be
            projects/{project_number}/feeds/{client-assigned_feed_identifier}
            or
            folders/{folder_number}/feeds/{client-assigned_feed_identifier}
            or
            organizations/{organization_number}/feeds/{client-assigned_feed_identifier}

            The client-assigned feed identifier must be unique within
            the parent project/folder/organization.
        asset_names (Sequence[str]):
            A list of the full names of the assets to receive updates.
            You must specify either or both of asset_names and
            asset_types. Only asset updates matching specified
            asset_names or asset_types are exported to the feed.
            Example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more info.
        asset_types (Sequence[str]):
            A list of types of the assets to receive updates. You must
            specify either or both of asset_names and asset_types. Only
            asset updates matching specified asset_names or asset_types
            are exported to the feed. Example:
            ``"compute.googleapis.com/Disk"``

            See `this
            topic <https://cloud.google.com/asset-inventory/docs/supported-asset-types>`__
            for a list of all supported asset types.
        content_type (google.cloud.asset_v1.types.ContentType):
            Asset content type. If not specified, no
            content but the asset name and type will be
            returned.
        feed_output_config (google.cloud.asset_v1.types.FeedOutputConfig):
            Required. Feed output configuration defining
            where the asset updates are published to.
        condition (google.type.expr_pb2.Expr):
            A condition which determines whether an asset update should
            be published. If specified, an asset will be returned only
            when the expression evaluates to true. When set,
            ``expression`` field in the ``Expr`` must be a valid [CEL
            expression] (https://github.com/google/cel-spec) on a
            TemporalAsset with name ``temporal_asset``. Example: a Feed
            with expression ("temporal_asset.deleted == true") will only
            publish Asset deletions. Other fields of ``Expr`` are
            optional.

            See our `user
            guide <https://cloud.google.com/asset-inventory/docs/monitoring-asset-changes#feed_with_condition>`__
            for detailed instructions.
    """

    name = proto.Field(proto.STRING, number=1,)
    asset_names = proto.RepeatedField(proto.STRING, number=2,)
    asset_types = proto.RepeatedField(proto.STRING, number=3,)
    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)
    feed_output_config = proto.Field(
        proto.MESSAGE, number=5, message="FeedOutputConfig",
    )
    condition = proto.Field(proto.MESSAGE, number=6, message=expr_pb2.Expr,)


class SearchAllResourcesRequest(proto.Message):
    r"""Search all resources request.
    Attributes:
        scope (str):
            Required. A scope can be a project, a folder, or an
            organization. The search is limited to the resources within
            the ``scope``. The caller must be granted the
            ```cloudasset.assets.searchAllResources`` <https://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
            permission on the desired scope.

            The allowed values are:

            -  projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            -  projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            -  folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            -  organizations/{ORGANIZATION_NUMBER} (e.g.,
               "organizations/123456")
        query (str):
            Optional. The query statement. See `how to construct a
            query <https://cloud.google.com/asset-inventory/docs/searching-resources#how_to_construct_a_query>`__
            for more information. If not specified or empty, it will
            search all the resources within the specified ``scope``.

            Examples:

            -  ``name:Important`` to find Cloud resources whose name
               contains "Important" as a word.
            -  ``name=Important`` to find the Cloud resource whose name
               is exactly "Important".
            -  ``displayName:Impor*`` to find Cloud resources whose
               display name contains "Impor" as a prefix of any word in
               the field.
            -  ``location:us-west*`` to find Cloud resources whose
               location contains both "us" and "west" as prefixes.
            -  ``labels:prod`` to find Cloud resources whose labels
               contain "prod" as a key or value.
            -  ``labels.env:prod`` to find Cloud resources that have a
               label "env" and its value is "prod".
            -  ``labels.env:*`` to find Cloud resources that have a
               label "env".
            -  ``kmsKey:key`` to find Cloud resources encrypted with a
               customer-managed encryption key whose name contains the
               word "key".
            -  ``state:ACTIVE`` to find Cloud resources whose state
               contains "ACTIVE" as a word.
            -  ``NOT state:ACTIVE`` to find {{gcp_name}} resources whose
               state doesn't contain "ACTIVE" as a word.
            -  ``createTime<1609459200`` to find Cloud resources that
               were created before "2021-01-01 00:00:00 UTC". 1609459200
               is the epoch timestamp of "2021-01-01 00:00:00 UTC" in
               seconds.
            -  ``updateTime>1609459200`` to find Cloud resources that
               were updated after "2021-01-01 00:00:00 UTC". 1609459200
               is the epoch timestamp of "2021-01-01 00:00:00 UTC" in
               seconds.
            -  ``Important`` to find Cloud resources that contain
               "Important" as a word in any of the searchable fields.
            -  ``Impor*`` to find Cloud resources that contain "Impor"
               as a prefix of any word in any of the searchable fields.
            -  ``Important location:(us-west1 OR global)`` to find Cloud
               resources that contain "Important" as a word in any of
               the searchable fields and are also located in the
               "us-west1" region or the "global" location.
        asset_types (Sequence[str]):
            Optional. A list of asset types that this request searches
            for. If empty, it will search all the `searchable asset
            types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__.

            Regular expressions are also supported. For example:

            -  "compute.googleapis.com.*" snapshots resources whose
               asset type starts with "compute.googleapis.com".
            -  ".*Instance" snapshots resources whose asset type ends
               with "Instance".
            -  ".*Instance.*" snapshots resources whose asset type
               contains "Instance".

            See `RE2 <https://github.com/google/re2/wiki/Syntax>`__ for
            all supported regular expression syntax. If the regular
            expression does not match any supported asset type, an
            INVALID_ARGUMENT error will be returned.
        page_size (int):
            Optional. The page size for search result pagination. Page
            size is capped at 500 even if a larger value is given. If
            set to zero, server will pick an appropriate default.
            Returned results may be fewer than requested. When this
            happens, there could be more results as long as
            ``next_page_token`` is returned.
        page_token (str):
            Optional. If present, then retrieve the next batch of
            results from the preceding call to this method.
            ``page_token`` must be the value of ``next_page_token`` from
            the previous response. The values of all other method
            parameters, must be identical to those in the previous call.
        order_by (str):
            Optional. A comma-separated list of fields specifying the
            sorting order of the results. The default order is
            ascending. Add " DESC" after the field name to indicate
            descending order. Redundant space characters are ignored.
            Example: "location DESC, name". Only singular primitive
            fields in the response are sortable:

            -  name
            -  assetType
            -  project
            -  displayName
            -  description
            -  location
            -  kmsKey
            -  createTime
            -  updateTime
            -  state
            -  parentFullResourceName
            -  parentAssetType All the other fields such as repeated
               fields (e.g., ``networkTags``), map fields (e.g.,
               ``labels``) and struct fields (e.g.,
               ``additionalAttributes``) are not supported.
    """

    scope = proto.Field(proto.STRING, number=1,)
    query = proto.Field(proto.STRING, number=2,)
    asset_types = proto.RepeatedField(proto.STRING, number=3,)
    page_size = proto.Field(proto.INT32, number=4,)
    page_token = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class SearchAllResourcesResponse(proto.Message):
    r"""Search all resources response.
    Attributes:
        results (Sequence[google.cloud.asset_v1.types.ResourceSearchResult]):
            A list of Resources that match the search
            query. It contains the resource standard
            metadata information.
        next_page_token (str):
            If there are more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gca_assets.ResourceSearchResult,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class SearchAllIamPoliciesRequest(proto.Message):
    r"""Search all IAM policies request.
    Attributes:
        scope (str):
            Required. A scope can be a project, a folder, or an
            organization. The search is limited to the IAM policies
            within the ``scope``. The caller must be granted the
            ```cloudasset.assets.searchAllIamPolicies`` <https://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
            permission on the desired scope.

            The allowed values are:

            -  projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            -  projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            -  folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            -  organizations/{ORGANIZATION_NUMBER} (e.g.,
               "organizations/123456")
        query (str):
            Optional. The query statement. See `how to construct a
            query <https://cloud.google.com/asset-inventory/docs/searching-iam-policies#how_to_construct_a_query>`__
            for more information. If not specified or empty, it will
            search all the IAM policies within the specified ``scope``.
            Note that the query string is compared against each Cloud
            IAM policy binding, including its members, roles, and Cloud
            IAM conditions. The returned Cloud IAM policies will only
            contain the bindings that match your query. To learn more
            about the IAM policy structure, see `IAM policy
            doc <https://cloud.google.com/iam/docs/policies#structure>`__.

            Examples:

            -  ``policy:amy@gmail.com`` to find IAM policy bindings that
               specify user "amy@gmail.com".
            -  ``policy:roles/compute.admin`` to find IAM policy
               bindings that specify the Compute Admin role.
            -  ``policy:comp*`` to find IAM policy bindings that contain
               "comp" as a prefix of any word in the binding.
            -  ``policy.role.permissions:storage.buckets.update`` to
               find IAM policy bindings that specify a role containing
               "storage.buckets.update" permission. Note that if callers
               don't have ``iam.roles.get`` access to a role's included
               permissions, policy bindings that specify this role will
               be dropped from the search results.
            -  ``policy.role.permissions:upd*`` to find IAM policy
               bindings that specify a role containing "upd" as a prefix
               of any word in the role permission. Note that if callers
               don't have ``iam.roles.get`` access to a role's included
               permissions, policy bindings that specify this role will
               be dropped from the search results.
            -  ``resource:organizations/123456`` to find IAM policy
               bindings that are set on "organizations/123456".
            -  ``resource=//cloudresourcemanager.googleapis.com/projects/myproject``
               to find IAM policy bindings that are set on the project
               named "myproject".
            -  ``Important`` to find IAM policy bindings that contain
               "Important" as a word in any of the searchable fields
               (except for the included permissions).
            -  ``resource:(instance1 OR instance2) policy:amy`` to find
               IAM policy bindings that are set on resources "instance1"
               or "instance2" and also specify user "amy".
            -  ``roles:roles/compute.admin`` to find IAM policy bindings
               that specify the Compute Admin role.
            -  ``memberTypes:user`` to find IAM policy bindings that
               contain the "user" member type.
        page_size (int):
            Optional. The page size for search result pagination. Page
            size is capped at 500 even if a larger value is given. If
            set to zero, server will pick an appropriate default.
            Returned results may be fewer than requested. When this
            happens, there could be more results as long as
            ``next_page_token`` is returned.
        page_token (str):
            Optional. If present, retrieve the next batch of results
            from the preceding call to this method. ``page_token`` must
            be the value of ``next_page_token`` from the previous
            response. The values of all other method parameters must be
            identical to those in the previous call.
        asset_types (Sequence[str]):
            Optional. A list of asset types that the IAM policies are
            attached to. If empty, it will search the IAM policies that
            are attached to all the `searchable asset
            types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__.

            Regular expressions are also supported. For example:

            -  "compute.googleapis.com.*" snapshots IAM policies
               attached to asset type starts with
               "compute.googleapis.com".
            -  ".*Instance" snapshots IAM policies attached to asset
               type ends with "Instance".
            -  ".*Instance.*" snapshots IAM policies attached to asset
               type contains "Instance".

            See `RE2 <https://github.com/google/re2/wiki/Syntax>`__ for
            all supported regular expression syntax. If the regular
            expression does not match any supported asset type, an
            INVALID_ARGUMENT error will be returned.
        order_by (str):
            Optional. A comma-separated list of fields specifying the
            sorting order of the results. The default order is
            ascending. Add " DESC" after the field name to indicate
            descending order. Redundant space characters are ignored.
            Example: "assetType DESC, resource". Only singular primitive
            fields in the response are sortable:

            -  resource
            -  assetType
            -  project All the other fields such as repeated fields
               (e.g., ``folders``) and non-primitive fields (e.g.,
               ``policy``) are not supported.
    """

    scope = proto.Field(proto.STRING, number=1,)
    query = proto.Field(proto.STRING, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)
    asset_types = proto.RepeatedField(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=7,)


class SearchAllIamPoliciesResponse(proto.Message):
    r"""Search all IAM policies response.
    Attributes:
        results (Sequence[google.cloud.asset_v1.types.IamPolicySearchResult]):
            A list of IamPolicy that match the search
            query. Related information such as the
            associated resource is returned along with the
            policy.
        next_page_token (str):
            Set if there are more results than those appearing in this
            response; to get the next set of results, call this method
            again, using this value as the ``page_token``.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gca_assets.IamPolicySearchResult,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class IamPolicyAnalysisQuery(proto.Message):
    r"""## IAM policy analysis query message.
    Attributes:
        scope (str):
            Required. The relative name of the root asset. Only
            resources and IAM policies within the scope will be
            analyzed.

            This can only be an organization number (such as
            "organizations/123"), a folder number (such as
            "folders/123"), a project ID (such as
            "projects/my-project-id"), or a project number (such as
            "projects/12345").

            To know how to get organization id, visit
            `here <https://cloud.google.com/resource-manager/docs/creating-managing-organization#retrieving_your_organization_id>`__.

            To know how to get folder or project id, visit
            `here <https://cloud.google.com/resource-manager/docs/creating-managing-folders#viewing_or_listing_folders_and_projects>`__.
        resource_selector (google.cloud.asset_v1.types.IamPolicyAnalysisQuery.ResourceSelector):
            Optional. Specifies a resource for analysis.
        identity_selector (google.cloud.asset_v1.types.IamPolicyAnalysisQuery.IdentitySelector):
            Optional. Specifies an identity for analysis.
        access_selector (google.cloud.asset_v1.types.IamPolicyAnalysisQuery.AccessSelector):
            Optional. Specifies roles or permissions for
            analysis. This is optional.
        options (google.cloud.asset_v1.types.IamPolicyAnalysisQuery.Options):
            Optional. The query options.
        condition_context (google.cloud.asset_v1.types.IamPolicyAnalysisQuery.ConditionContext):
            Optional. The hypothetical context for IAM
            conditions evaluation.
    """

    class ResourceSelector(proto.Message):
        r"""Specifies the resource to analyze for access policies, which
        may be set directly on the resource, or on ancestors such as
        organizations, folders or projects.

        Attributes:
            full_resource_name (str):
                Required. The [full resource name]
                (https://cloud.google.com/asset-inventory/docs/resource-name-format)
                of a resource of `supported resource
                types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#analyzable_asset_types>`__.
        """

        full_resource_name = proto.Field(proto.STRING, number=1,)

    class IdentitySelector(proto.Message):
        r"""Specifies an identity for which to determine resource access,
        based on roles assigned either directly to them or to the groups
        they belong to, directly or indirectly.

        Attributes:
            identity (str):
                Required. The identity appear in the form of members in `IAM
                policy
                binding <https://cloud.google.com/iam/reference/rest/v1/Binding>`__.

                The examples of supported forms are:
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com".

                Notice that wildcard characters (such as \* and ?) are not
                supported. You must give a specific identity.
        """

        identity = proto.Field(proto.STRING, number=1,)

    class AccessSelector(proto.Message):
        r"""Specifies roles and/or permissions to analyze, to determine
        both the identities possessing them and the resources they
        control. If multiple values are specified, results will include
        roles or permissions matching any of them. The total number of
        roles and permissions should be equal or less than 10.

        Attributes:
            roles (Sequence[str]):
                Optional. The roles to appear in result.
            permissions (Sequence[str]):
                Optional. The permissions to appear in
                result.
        """

        roles = proto.RepeatedField(proto.STRING, number=1,)
        permissions = proto.RepeatedField(proto.STRING, number=2,)

    class Options(proto.Message):
        r"""Contains query options.
        Attributes:
            expand_groups (bool):
                Optional. If true, the identities section of the result will
                expand any Google groups appearing in an IAM policy binding.

                If
                [IamPolicyAnalysisQuery.identity_selector][google.cloud.asset.v1.IamPolicyAnalysisQuery.identity_selector]
                is specified, the identity in the result will be determined
                by the selector, and this flag is not allowed to set.

                Default is false.
            expand_roles (bool):
                Optional. If true, the access section of result will expand
                any roles appearing in IAM policy bindings to include their
                permissions.

                If
                [IamPolicyAnalysisQuery.access_selector][google.cloud.asset.v1.IamPolicyAnalysisQuery.access_selector]
                is specified, the access section of the result will be
                determined by the selector, and this flag is not allowed to
                set.

                Default is false.
            expand_resources (bool):
                Optional. If true and
                [IamPolicyAnalysisQuery.resource_selector][google.cloud.asset.v1.IamPolicyAnalysisQuery.resource_selector]
                is not specified, the resource section of the result will
                expand any resource attached to an IAM policy to include
                resources lower in the resource hierarchy.

                For example, if the request analyzes for which resources
                user A has permission P, and the results include an IAM
                policy with P on a GCP folder, the results will also include
                resources in that folder with permission P.

                If true and
                [IamPolicyAnalysisQuery.resource_selector][google.cloud.asset.v1.IamPolicyAnalysisQuery.resource_selector]
                is specified, the resource section of the result will expand
                the specified resource to include resources lower in the
                resource hierarchy. Only project or lower resources are
                supported. Folder and organization resource cannot be used
                together with this option.

                For example, if the request analyzes for which users have
                permission P on a GCP project with this option enabled, the
                results will include all users who have permission P on that
                project or any lower resource.

                Default is false.
            output_resource_edges (bool):
                Optional. If true, the result will output
                resource edges, starting from the policy
                attached resource, to any expanded resources.
                Default is false.
            output_group_edges (bool):
                Optional. If true, the result will output
                group identity edges, starting from the
                binding's group members, to any expanded
                identities. Default is false.
            analyze_service_account_impersonation (bool):
                Optional. If true, the response will include access analysis
                from identities to resources via service account
                impersonation. This is a very expensive operation, because
                many derived queries will be executed. We highly recommend
                you use
                [AssetService.AnalyzeIamPolicyLongrunning][google.cloud.asset.v1.AssetService.AnalyzeIamPolicyLongrunning]
                rpc instead.

                For example, if the request analyzes for which resources
                user A has permission P, and there's an IAM policy states
                user A has iam.serviceAccounts.getAccessToken permission to
                a service account SA, and there's another IAM policy states
                service account SA has permission P to a GCP folder F, then
                user A potentially has access to the GCP folder F. And those
                advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Another example, if the request analyzes for who has
                permission P to a GCP folder F, and there's an IAM policy
                states user A has iam.serviceAccounts.actAs permission to a
                service account SA, and there's another IAM policy states
                service account SA has permission P to the GCP folder F,
                then user A potentially has access to the GCP folder F. And
                those advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Default is false.
        """

        expand_groups = proto.Field(proto.BOOL, number=1,)
        expand_roles = proto.Field(proto.BOOL, number=2,)
        expand_resources = proto.Field(proto.BOOL, number=3,)
        output_resource_edges = proto.Field(proto.BOOL, number=4,)
        output_group_edges = proto.Field(proto.BOOL, number=5,)
        analyze_service_account_impersonation = proto.Field(proto.BOOL, number=6,)

    class ConditionContext(proto.Message):
        r"""The IAM conditions context.
        Attributes:
            access_time (google.protobuf.timestamp_pb2.Timestamp):
                The hypothetical access timestamp to evaluate IAM
                conditions. Note that this value must not be earlier than
                the current time; otherwise, an INVALID_ARGUMENT error will
                be returned.
        """

        access_time = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="TimeContext",
            message=timestamp_pb2.Timestamp,
        )

    scope = proto.Field(proto.STRING, number=1,)
    resource_selector = proto.Field(proto.MESSAGE, number=2, message=ResourceSelector,)
    identity_selector = proto.Field(proto.MESSAGE, number=3, message=IdentitySelector,)
    access_selector = proto.Field(proto.MESSAGE, number=4, message=AccessSelector,)
    options = proto.Field(proto.MESSAGE, number=5, message=Options,)
    condition_context = proto.Field(proto.MESSAGE, number=6, message=ConditionContext,)


class AnalyzeIamPolicyRequest(proto.Message):
    r"""A request message for
    [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1.AssetService.AnalyzeIamPolicy].

    Attributes:
        analysis_query (google.cloud.asset_v1.types.IamPolicyAnalysisQuery):
            Required. The request query.
        execution_timeout (google.protobuf.duration_pb2.Duration):
            Optional. Amount of time executable has to complete. See
            JSON representation of
            `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`__.

            If this field is set with a value less than the RPC
            deadline, and the execution of your query hasn't finished in
            the specified execution timeout, you will get a response
            with partial result. Otherwise, your query's execution will
            continue until the RPC deadline. If it's not finished until
            then, you will get a DEADLINE_EXCEEDED error.

            Default is empty.
    """

    analysis_query = proto.Field(
        proto.MESSAGE, number=1, message="IamPolicyAnalysisQuery",
    )
    execution_timeout = proto.Field(
        proto.MESSAGE, number=2, message=duration_pb2.Duration,
    )


class AnalyzeIamPolicyResponse(proto.Message):
    r"""A response message for
    [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1.AssetService.AnalyzeIamPolicy].

    Attributes:
        main_analysis (google.cloud.asset_v1.types.AnalyzeIamPolicyResponse.IamPolicyAnalysis):
            The main analysis that matches the original
            request.
        service_account_impersonation_analysis (Sequence[google.cloud.asset_v1.types.AnalyzeIamPolicyResponse.IamPolicyAnalysis]):
            The service account impersonation analysis if
            [AnalyzeIamPolicyRequest.analyze_service_account_impersonation][]
            is enabled.
        fully_explored (bool):
            Represents whether all entries in the
            [main_analysis][google.cloud.asset.v1.AnalyzeIamPolicyResponse.main_analysis]
            and
            [service_account_impersonation_analysis][google.cloud.asset.v1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis]
            have been fully explored to answer the query in the request.
    """

    class IamPolicyAnalysis(proto.Message):
        r"""An analysis message to group the query and results.
        Attributes:
            analysis_query (google.cloud.asset_v1.types.IamPolicyAnalysisQuery):
                The analysis query.
            analysis_results (Sequence[google.cloud.asset_v1.types.IamPolicyAnalysisResult]):
                A list of
                [IamPolicyAnalysisResult][google.cloud.asset.v1.IamPolicyAnalysisResult]
                that matches the analysis query, or empty if no result is
                found.
            fully_explored (bool):
                Represents whether all entries in the
                [analysis_results][google.cloud.asset.v1.AnalyzeIamPolicyResponse.IamPolicyAnalysis.analysis_results]
                have been fully explored to answer the query.
            non_critical_errors (Sequence[google.cloud.asset_v1.types.IamPolicyAnalysisState]):
                A list of non-critical errors happened during
                the query handling.
        """

        analysis_query = proto.Field(
            proto.MESSAGE, number=1, message="IamPolicyAnalysisQuery",
        )
        analysis_results = proto.RepeatedField(
            proto.MESSAGE, number=2, message=gca_assets.IamPolicyAnalysisResult,
        )
        fully_explored = proto.Field(proto.BOOL, number=3,)
        non_critical_errors = proto.RepeatedField(
            proto.MESSAGE, number=5, message=gca_assets.IamPolicyAnalysisState,
        )

    main_analysis = proto.Field(proto.MESSAGE, number=1, message=IamPolicyAnalysis,)
    service_account_impersonation_analysis = proto.RepeatedField(
        proto.MESSAGE, number=2, message=IamPolicyAnalysis,
    )
    fully_explored = proto.Field(proto.BOOL, number=3,)


class IamPolicyAnalysisOutputConfig(proto.Message):
    r"""Output configuration for export IAM policy analysis
    destination.

    Attributes:
        gcs_destination (google.cloud.asset_v1.types.IamPolicyAnalysisOutputConfig.GcsDestination):
            Destination on Cloud Storage.
        bigquery_destination (google.cloud.asset_v1.types.IamPolicyAnalysisOutputConfig.BigQueryDestination):
            Destination on BigQuery.
    """

    class GcsDestination(proto.Message):
        r"""A Cloud Storage location.
        Attributes:
            uri (str):
                Required. The uri of the Cloud Storage object. It's the same
                uri that is used by gsutil. Example:
                "gs://bucket_name/object_name". See `Viewing and Editing
                Object
                Metadata <https://cloud.google.com/storage/docs/viewing-editing-metadata>`__
                for more information.

                If the specified Cloud Storage object already exists and
                there is no
                `hold <https://cloud.google.com/storage/docs/object-holds>`__,
                it will be overwritten with the analysis result.
        """

        uri = proto.Field(proto.STRING, number=1,)

    class BigQueryDestination(proto.Message):
        r"""A BigQuery destination.
        Attributes:
            dataset (str):
                Required. The BigQuery dataset in format
                "projects/projectId/datasets/datasetId", to which the
                analysis results should be exported. If this dataset does
                not exist, the export call will return an INVALID_ARGUMENT
                error.
            table_prefix (str):
                Required. The prefix of the BigQuery tables to which the
                analysis results will be written. Tables will be created
                based on this table_prefix if not exist:

                -  <table_prefix>_analysis table will contain export
                   operation's metadata.
                -  <table_prefix>_analysis_result will contain all the
                   [IamPolicyAnalysisResult][google.cloud.asset.v1.IamPolicyAnalysisResult].
                   When [partition_key] is specified, both tables will be
                   partitioned based on the [partition_key].
            partition_key (google.cloud.asset_v1.types.IamPolicyAnalysisOutputConfig.BigQueryDestination.PartitionKey):
                The partition key for BigQuery partitioned
                table.
            write_disposition (str):
                Optional. Specifies the action that occurs if the
                destination table or partition already exists. The following
                values are supported:

                -  WRITE_TRUNCATE: If the table or partition already exists,
                   BigQuery overwrites the entire table or all the
                   partitions data.
                -  WRITE_APPEND: If the table or partition already exists,
                   BigQuery appends the data to the table or the latest
                   partition.
                -  WRITE_EMPTY: If the table already exists and contains
                   data, an error is returned.

                The default value is WRITE_APPEND. Each action is atomic and
                only occurs if BigQuery is able to complete the job
                successfully. Details are at
                https://cloud.google.com/bigquery/docs/loading-data-local#appending_to_or_overwriting_a_table_using_a_local_file.
        """

        class PartitionKey(proto.Enum):
            r"""This enum determines the partition key column for the
            bigquery tables. Partitioning can improve query performance and
            reduce query cost by filtering partitions. Refer to
            https://cloud.google.com/bigquery/docs/partitioned-tables for
            details.
            """
            PARTITION_KEY_UNSPECIFIED = 0
            REQUEST_TIME = 1

        dataset = proto.Field(proto.STRING, number=1,)
        table_prefix = proto.Field(proto.STRING, number=2,)
        partition_key = proto.Field(
            proto.ENUM,
            number=3,
            enum="IamPolicyAnalysisOutputConfig.BigQueryDestination.PartitionKey",
        )
        write_disposition = proto.Field(proto.STRING, number=4,)

    gcs_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message=GcsDestination,
    )
    bigquery_destination = proto.Field(
        proto.MESSAGE, number=2, oneof="destination", message=BigQueryDestination,
    )


class AnalyzeIamPolicyLongrunningRequest(proto.Message):
    r"""A request message for
    [AssetService.AnalyzeIamPolicyLongrunning][google.cloud.asset.v1.AssetService.AnalyzeIamPolicyLongrunning].

    Attributes:
        analysis_query (google.cloud.asset_v1.types.IamPolicyAnalysisQuery):
            Required. The request query.
        output_config (google.cloud.asset_v1.types.IamPolicyAnalysisOutputConfig):
            Required. Output configuration indicating
            where the results will be output to.
    """

    analysis_query = proto.Field(
        proto.MESSAGE, number=1, message="IamPolicyAnalysisQuery",
    )
    output_config = proto.Field(
        proto.MESSAGE, number=2, message="IamPolicyAnalysisOutputConfig",
    )


class AnalyzeIamPolicyLongrunningResponse(proto.Message):
    r"""A response message for
    [AssetService.AnalyzeIamPolicyLongrunning][google.cloud.asset.v1.AssetService.AnalyzeIamPolicyLongrunning].
        """


__all__ = tuple(sorted(__protobuf__.manifest))
