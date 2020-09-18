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
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1",
    manifest={
        "ContentType",
        "ExportAssetsRequest",
        "ExportAssetsResponse",
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
    },
)


class ContentType(proto.Enum):
    r"""Asset content type."""
    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2
    ORG_POLICY = 4
    ACCESS_POLICY = 5


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
        read_time (~.timestamp.Timestamp):
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
        content_type (~.asset_service.ContentType):
            Asset content type. If not specified, no
            content but the asset name will be returned.
        output_config (~.asset_service.OutputConfig):
            Required. Output configuration indicating
            where the results will be output to.
    """

    parent = proto.Field(proto.STRING, number=1)

    read_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    asset_types = proto.RepeatedField(proto.STRING, number=3)

    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)

    output_config = proto.Field(proto.MESSAGE, number=5, message="OutputConfig",)


class ExportAssetsResponse(proto.Message):
    r"""The export asset response. This message is returned by the
    [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
    method in the returned
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field.

    Attributes:
        read_time (~.timestamp.Timestamp):
            Time the snapshot was taken.
        output_config (~.asset_service.OutputConfig):
            Output configuration indicating where the
            results were output to.
        output_result (~.asset_service.OutputResult):
            Output result indicating where the assets were exported to.
            For example, a set of actual Google Cloud Storage object
            uris where the assets are exported to. The uris can be
            different from what [output_config] has specified, as the
            service will split the output object into multiple ones once
            it exceeds a single Google Cloud Storage object limit.
    """

    read_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    output_config = proto.Field(proto.MESSAGE, number=2, message="OutputConfig",)

    output_result = proto.Field(proto.MESSAGE, number=3, message="OutputResult",)


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
        content_type (~.asset_service.ContentType):
            Optional. The content type.
        read_time_window (~.gca_assets.TimeWindow):
            Optional. The time window for the asset history. Both
            start_time and end_time are optional and if set, it must be
            after the current time minus 35 days. If end_time is not
            set, it is default to current timestamp. If start_time is
            not set, the snapshot of the assets at end_time will be
            returned. The returned results contain all temporal assets
            whose time window overlap with read_time_window.
    """

    parent = proto.Field(proto.STRING, number=1)

    asset_names = proto.RepeatedField(proto.STRING, number=2)

    content_type = proto.Field(proto.ENUM, number=3, enum="ContentType",)

    read_time_window = proto.Field(
        proto.MESSAGE, number=4, message=gca_assets.TimeWindow,
    )


class BatchGetAssetsHistoryResponse(proto.Message):
    r"""Batch get assets history response.

    Attributes:
        assets (Sequence[~.gca_assets.TemporalAsset]):
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
        feed (~.asset_service.Feed):
            Required. The feed details. The field ``name`` must be empty
            and it will be generated in the format of:
            projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    parent = proto.Field(proto.STRING, number=1)

    feed_id = proto.Field(proto.STRING, number=2)

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

    name = proto.Field(proto.STRING, number=1)


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

    parent = proto.Field(proto.STRING, number=1)


class ListFeedsResponse(proto.Message):
    r"""

    Attributes:
        feeds (Sequence[~.asset_service.Feed]):
            A list of feeds.
    """

    feeds = proto.RepeatedField(proto.MESSAGE, number=1, message="Feed",)


class UpdateFeedRequest(proto.Message):
    r"""Update asset feed request.

    Attributes:
        feed (~.asset_service.Feed):
            Required. The new values of feed details. It must match an
            existing feed and the field ``name`` must be in the format
            of: projects/project_number/feeds/feed_id or
            folders/folder_number/feeds/feed_id or
            organizations/organization_number/feeds/feed_id.
        update_mask (~.field_mask.FieldMask):
            Required. Only updates the ``feed`` fields indicated by this
            mask. The field mask must not be empty, and it must not
            contain fields that are immutable or only set by the server.
    """

    feed = proto.Field(proto.MESSAGE, number=1, message="Feed",)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteFeedRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The name of the feed and it must be in the format
            of: projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    name = proto.Field(proto.STRING, number=1)


class OutputConfig(proto.Message):
    r"""Output configuration for export assets destination.

    Attributes:
        gcs_destination (~.asset_service.GcsDestination):
            Destination on Cloud Storage.
        bigquery_destination (~.asset_service.BigQueryDestination):
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
        gcs_result (~.asset_service.GcsOutputResult):
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

    uris = proto.RepeatedField(proto.STRING, number=1)


class GcsDestination(proto.Message):
    r"""A Cloud Storage location.

    Attributes:
        uri (str):
            The uri of the Cloud Storage object. It's the same uri that
            is used by gsutil. Example: "gs://bucket_name/object_name".
            See `Viewing and Editing Object
            Metadata <https://cloud.google.com/storage/docs/viewing-editing-metadata>`__
            for more information.
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

    uri = proto.Field(proto.STRING, number=1, oneof="object_uri")

    uri_prefix = proto.Field(proto.STRING, number=2, oneof="object_uri")


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
        partition_spec (~.asset_service.PartitionSpec):
            [partition_spec] determines whether to export to partitioned
            table(s) and how to partition the data.

            If [partition_spec] is unset or [partition_spec.partion_key]
            is unset or ``PARTITION_KEY_UNSPECIFIED``, the snapshot
            results will be exported to non-partitioned table(s).
            [force] will decide whether to overwrite existing table(s).

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

    dataset = proto.Field(proto.STRING, number=1)

    table = proto.Field(proto.STRING, number=2)

    force = proto.Field(proto.BOOL, number=3)

    partition_spec = proto.Field(proto.MESSAGE, number=4, message="PartitionSpec",)

    separate_tables_per_asset_type = proto.Field(proto.BOOL, number=5)


class PartitionSpec(proto.Message):
    r"""Specifications of BigQuery partitioned table as export
    destination.

    Attributes:
        partition_key (~.asset_service.PartitionSpec.PartitionKey):
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

    topic = proto.Field(proto.STRING, number=1)


class FeedOutputConfig(proto.Message):
    r"""Output configuration for asset feed destination.

    Attributes:
        pubsub_destination (~.asset_service.PubsubDestination):
            Destination on Pub/Sub.
    """

    pubsub_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message=PubsubDestination,
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
        content_type (~.asset_service.ContentType):
            Asset content type. If not specified, no
            content but the asset name and type will be
            returned.
        feed_output_config (~.asset_service.FeedOutputConfig):
            Required. Feed output configuration defining
            where the asset updates are published to.
        condition (~.expr.Expr):
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

    name = proto.Field(proto.STRING, number=1)

    asset_names = proto.RepeatedField(proto.STRING, number=2)

    asset_types = proto.RepeatedField(proto.STRING, number=3)

    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)

    feed_output_config = proto.Field(proto.MESSAGE, number=5, message=FeedOutputConfig,)

    condition = proto.Field(proto.MESSAGE, number=6, message=expr.Expr,)


class SearchAllResourcesRequest(proto.Message):
    r"""Search all resources request.

    Attributes:
        scope (str):
            Required. A scope can be a project, a folder, or an
            organization. The search is limited to the resources within
            the ``scope``. The caller must be granted the
            ```cloudasset.assets.searchAllResources`` <http://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
            permission on the desired scope.

            The allowed values are:

            -  projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            -  projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            -  folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            -  organizations/{ORGANIZATION_NUMBER} (e.g.,
               "organizations/123456")
        query (str):
            Optional. The query statement. See `how to construct a
            query <http://cloud.google.com/asset-inventory/docs/searching-resources#how_to_construct_a_query>`__
            for more information. If not specified or empty, it will
            search all the resources within the specified ``scope``.
            Note that the query string is compared against each Cloud
            IAM policy binding, including its members, roles, and Cloud
            IAM conditions. The returned Cloud IAM policies will only
            contain the bindings that match your query. To learn more
            about the IAM policy structure, see `IAM policy
            doc <https://cloud.google.com/iam/docs/policies#structure>`__.

            Examples:

            -  ``name:Important`` to find Cloud resources whose name
               contains "Important" as a word.
            -  ``displayName:Impor*`` to find Cloud resources whose
               display name contains "Impor" as a prefix.
            -  ``description:*por*`` to find Cloud resources whose
               description contains "por" as a substring.
            -  ``location:us-west*`` to find Cloud resources whose
               location is prefixed with "us-west".
            -  ``labels:prod`` to find Cloud resources whose labels
               contain "prod" as a key or value.
            -  ``labels.env:prod`` to find Cloud resources that have a
               label "env" and its value is "prod".
            -  ``labels.env:*`` to find Cloud resources that have a
               label "env".
            -  ``Important`` to find Cloud resources that contain
               "Important" as a word in any of the searchable fields.
            -  ``Impor*`` to find Cloud resources that contain "Impor"
               as a prefix in any of the searchable fields.
            -  ``*por*`` to find Cloud resources that contain "por" as a
               substring in any of the searchable fields.
            -  ``Important location:(us-west1 OR global)`` to find Cloud
               resources that contain "Important" as a word in any of
               the searchable fields and are also located in the
               "us-west1" region or the "global" location.
        asset_types (Sequence[str]):
            Optional. A list of asset types that this request searches
            for. If empty, it will search all the `searchable asset
            types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__.
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
            Optional. A comma separated list of fields specifying the
            sorting order of the results. The default order is
            ascending. Add " DESC" after the field name to indicate
            descending order. Redundant space characters are ignored.
            Example: "location DESC, name". Only string fields in the
            response are sortable, including ``name``, ``displayName``,
            ``description``, ``location``. All the other fields such as
            repeated fields (e.g., ``networkTags``), map fields (e.g.,
            ``labels``) and struct fields (e.g.,
            ``additionalAttributes``) are not supported.
    """

    scope = proto.Field(proto.STRING, number=1)

    query = proto.Field(proto.STRING, number=2)

    asset_types = proto.RepeatedField(proto.STRING, number=3)

    page_size = proto.Field(proto.INT32, number=4)

    page_token = proto.Field(proto.STRING, number=5)

    order_by = proto.Field(proto.STRING, number=6)


class SearchAllResourcesResponse(proto.Message):
    r"""Search all resources response.

    Attributes:
        results (Sequence[~.gca_assets.ResourceSearchResult]):
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

    next_page_token = proto.Field(proto.STRING, number=2)


class SearchAllIamPoliciesRequest(proto.Message):
    r"""Search all IAM policies request.

    Attributes:
        scope (str):
            Required. A scope can be a project, a folder, or an
            organization. The search is limited to the IAM policies
            within the ``scope``. The caller must be granted the
            ```cloudasset.assets.searchAllIamPolicies`` <http://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
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

            Examples:

            -  ``policy:amy@gmail.com`` to find IAM policy bindings that
               specify user "amy@gmail.com".
            -  ``policy:roles/compute.admin`` to find IAM policy
               bindings that specify the Compute Admin role.
            -  ``policy.role.permissions:storage.buckets.update`` to
               find IAM policy bindings that specify a role containing
               "storage.buckets.update" permission. Note that if callers
               don't have ``iam.roles.get`` access to a role's included
               permissions, policy bindings that specify this role will
               be dropped from the search results.
            -  ``resource:organizations/123456`` to find IAM policy
               bindings that are set on "organizations/123456".
            -  ``Important`` to find IAM policy bindings that contain
               "Important" as a word in any of the searchable fields
               (except for the included permissions).
            -  ``*por*`` to find IAM policy bindings that contain "por"
               as a substring in any of the searchable fields (except
               for the included permissions).
            -  ``resource:(instance1 OR instance2) policy:amy`` to find
               IAM policy bindings that are set on resources "instance1"
               or "instance2" and also specify user "amy".
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
    """

    scope = proto.Field(proto.STRING, number=1)

    query = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class SearchAllIamPoliciesResponse(proto.Message):
    r"""Search all IAM policies response.

    Attributes:
        results (Sequence[~.gca_assets.IamPolicySearchResult]):
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

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
