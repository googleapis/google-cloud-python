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

from google.cloud.datacatalog_v1.types import common
from google.cloud.datacatalog_v1.types import data_source as gcd_data_source
from google.cloud.datacatalog_v1.types import gcs_fileset_spec as gcd_gcs_fileset_spec
from google.cloud.datacatalog_v1.types import schema as gcd_schema
from google.cloud.datacatalog_v1.types import search
from google.cloud.datacatalog_v1.types import table_spec
from google.cloud.datacatalog_v1.types import tags as gcd_tags
from google.cloud.datacatalog_v1.types import timestamps
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1",
    manifest={
        "EntryType",
        "SearchCatalogRequest",
        "SearchCatalogResponse",
        "CreateEntryGroupRequest",
        "UpdateEntryGroupRequest",
        "GetEntryGroupRequest",
        "DeleteEntryGroupRequest",
        "ListEntryGroupsRequest",
        "ListEntryGroupsResponse",
        "CreateEntryRequest",
        "UpdateEntryRequest",
        "DeleteEntryRequest",
        "GetEntryRequest",
        "LookupEntryRequest",
        "Entry",
        "DatabaseTableSpec",
        "EntryGroup",
        "CreateTagTemplateRequest",
        "GetTagTemplateRequest",
        "UpdateTagTemplateRequest",
        "DeleteTagTemplateRequest",
        "CreateTagRequest",
        "UpdateTagRequest",
        "DeleteTagRequest",
        "CreateTagTemplateFieldRequest",
        "UpdateTagTemplateFieldRequest",
        "RenameTagTemplateFieldRequest",
        "RenameTagTemplateFieldEnumValueRequest",
        "DeleteTagTemplateFieldRequest",
        "ListTagsRequest",
        "ListTagsResponse",
        "ListEntriesRequest",
        "ListEntriesResponse",
    },
)


class EntryType(proto.Enum):
    r"""Entry resources in Data Catalog can be of different types e.g. a
    BigQuery Table entry is of type ``TABLE``. This enum describes all
    the possible types Data Catalog contains.
    """
    ENTRY_TYPE_UNSPECIFIED = 0
    TABLE = 2
    MODEL = 5
    DATA_STREAM = 3
    FILESET = 4
    DATABASE = 7
    SERVICE = 14


class SearchCatalogRequest(proto.Message):
    r"""Request message for
    [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

    Attributes:
        scope (google.cloud.datacatalog_v1.types.SearchCatalogRequest.Scope):
            Required. The scope of this search request. A ``scope`` that
            has empty ``include_org_ids``, ``include_project_ids`` AND
            false ``include_gcp_public_datasets`` is considered invalid.
            Data Catalog will return an error in such a case.
        query (str):
            Optional. The query string in search query syntax. An empty
            query string will result in all data assets (in the
            specified scope) that the user has access to.

            Query strings can be simple as "x" or more qualified as:

            -  name:x
            -  column:x
            -  description:y

            Note: Query tokens need to have a minimum of 3 characters
            for substring matching to work correctly. See `Data Catalog
            Search
            Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
            for more information.
        page_size (int):
            Number of results in the search page. If <=0 then defaults
            to 10. Max limit for page_size is 1000. Throws an invalid
            argument for page_size > 1000.
        page_token (str):
            Optional. Pagination token returned in an earlier
            [SearchCatalogResponse.next_page_token][google.cloud.datacatalog.v1.SearchCatalogResponse.next_page_token],
            which indicates that this is a continuation of a prior
            [SearchCatalogRequest][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog]
            call, and that the system should return the next page of
            data. If empty, the first page is returned.
        order_by (str):
            Specifies the ordering of results, currently supported
            case-sensitive choices are:

            -  ``relevance``, only supports descending
            -  ``last_modified_timestamp [asc|desc]``, defaults to
               descending if not specified

            If not specified, defaults to ``relevance`` descending.
    """

    class Scope(proto.Message):
        r"""The criteria that select the subspace used for query
        matching.

        Attributes:
            include_org_ids (Sequence[str]):
                The list of organization IDs to search
                within. To find your organization ID, follow
                instructions in
                https://cloud.google.com/resource-
                manager/docs/creating-managing-organization.
            include_project_ids (Sequence[str]):
                The list of project IDs to search within. To
                learn more about the distinction between project
                names/IDs/numbers, go to
                https://cloud.google.com/docs/overview/#projects.
            include_gcp_public_datasets (bool):
                If ``true``, include Google Cloud Platform (GCP) public
                datasets in the search results. Info on GCP public datasets
                is available at https://cloud.google.com/public-datasets/.
                By default, GCP public datasets are excluded.
            restricted_locations (Sequence[str]):
                Optional. The list of locations to search within.

                1. If empty, search will be performed in all locations;
                2. If any of the locations are NOT `supported
                   regions <https://cloud.google.com/data-catalog/docs/concepts/regions#supported_regions>`__,
                   error will be returned;
                3. Otherwise, search only the given locations for matching
                   results. Typical usage is to leave this field empty. When
                   a location is unreachable as returned in the
                   ``SearchCatalogResponse.unreachable`` field, users can
                   repeat the search request with this parameter set to get
                   additional information on the error.
        """

        include_org_ids = proto.RepeatedField(proto.STRING, number=2,)
        include_project_ids = proto.RepeatedField(proto.STRING, number=3,)
        include_gcp_public_datasets = proto.Field(proto.BOOL, number=7,)
        restricted_locations = proto.RepeatedField(proto.STRING, number=16,)

    scope = proto.Field(proto.MESSAGE, number=6, message=Scope,)
    query = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    order_by = proto.Field(proto.STRING, number=5,)


class SearchCatalogResponse(proto.Message):
    r"""Response message for
    [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

    Attributes:
        results (Sequence[google.cloud.datacatalog_v1.types.SearchCatalogResult]):
            Search results.
        next_page_token (str):
            The token that can be used to retrieve the
            next page of results.
        unreachable (Sequence[str]):
            Unreachable locations. Search result does not include data
            from those locations. Users can get additional information
            on the error by repeating the search request with a more
            restrictive parameter -- setting the value for
            ``SearchDataCatalogRequest.scope.restricted_locations``.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message=search.SearchCatalogResult,
    )
    next_page_token = proto.Field(proto.STRING, number=3,)
    unreachable = proto.RepeatedField(proto.STRING, number=6,)


class CreateEntryGroupRequest(proto.Message):
    r"""Request message for
    [CreateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.CreateEntryGroup].

    Attributes:
        parent (str):
            Required. The name of the project this entry group belongs
            to. Example:

            ``projects/{project_id}/locations/{location}``

            Note: The entry group itself and its child resources might
            not be stored in the location specified in its name.
        entry_group_id (str):
            Required. The ID of the entry group to create.

            The ID must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and must start with a letter or underscore.
            The maximum size is 64 bytes when encoded in UTF-8.
        entry_group (google.cloud.datacatalog_v1.types.EntryGroup):
            The entry group to create. Defaults to an
            empty entry group.
    """

    parent = proto.Field(proto.STRING, number=1,)
    entry_group_id = proto.Field(proto.STRING, number=3,)
    entry_group = proto.Field(proto.MESSAGE, number=2, message="EntryGroup",)


class UpdateEntryGroupRequest(proto.Message):
    r"""Request message for
    [UpdateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.UpdateEntryGroup].

    Attributes:
        entry_group (google.cloud.datacatalog_v1.types.EntryGroup):
            Required. The updated entry group. "name"
            field must be set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on
            an entry group.
            If this parameter is absent or empty, all
            modifiable fields are overwritten. If such
            fields are non-required and omitted in the
            request body, their values are emptied.
    """

    entry_group = proto.Field(proto.MESSAGE, number=1, message="EntryGroup",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class GetEntryGroupRequest(proto.Message):
    r"""Request message for
    [GetEntryGroup][google.cloud.datacatalog.v1.DataCatalog.GetEntryGroup].

    Attributes:
        name (str):
            Required. The name of the entry group. For example,
            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}``.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to return. If not set or empty,
            all fields are returned.
    """

    name = proto.Field(proto.STRING, number=1,)
    read_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,)


class DeleteEntryGroupRequest(proto.Message):
    r"""Request message for
    [DeleteEntryGroup][google.cloud.datacatalog.v1.DataCatalog.DeleteEntryGroup].

    Attributes:
        name (str):
            Required. The name of the entry group. For example,
            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}``.
        force (bool):
            Optional. If true, deletes all entries in the
            entry group.
    """

    name = proto.Field(proto.STRING, number=1,)
    force = proto.Field(proto.BOOL, number=2,)


class ListEntryGroupsRequest(proto.Message):
    r"""Request message for
    [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].

    Attributes:
        parent (str):
            Required. The name of the location that contains the entry
            groups, which can be provided in URL format. Example:

            -  projects/{project_id}/locations/{location}
        page_size (int):
            Optional. The maximum number of items to return. Default is
            10. Max limit is 1000. Throws an invalid argument for
            ``page_size > 1000``.
        page_token (str):
            Optional. Token that specifies which page is
            requested. If empty, the first page is returned.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListEntryGroupsResponse(proto.Message):
    r"""Response message for
    [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].

    Attributes:
        entry_groups (Sequence[google.cloud.datacatalog_v1.types.EntryGroup]):
            EntryGroup details.
        next_page_token (str):
            Token to retrieve the next page of results.
            It is set to empty if no items remain in
            results.
    """

    @property
    def raw_page(self):
        return self

    entry_groups = proto.RepeatedField(proto.MESSAGE, number=1, message="EntryGroup",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateEntryRequest(proto.Message):
    r"""Request message for
    [CreateEntry][google.cloud.datacatalog.v1.DataCatalog.CreateEntry].

    Attributes:
        parent (str):
            Required. The name of the entry group this entry belongs to.
            Example:

            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}``

            Note: The entry itself and its child resources might not be
            stored in the location specified in its name.
        entry_id (str):
            Required. The ID of the entry to create.

            The ID must contain only letters (a-z, A-Z), numbers (0-9),
            and underscores (_). The maximum size is 64 bytes when
            encoded in UTF-8.
        entry (google.cloud.datacatalog_v1.types.Entry):
            Required. The entry to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    entry_id = proto.Field(proto.STRING, number=3,)
    entry = proto.Field(proto.MESSAGE, number=2, message="Entry",)


class UpdateEntryRequest(proto.Message):
    r"""Request message for
    [UpdateEntry][google.cloud.datacatalog.v1.DataCatalog.UpdateEntry].

    Attributes:
        entry (google.cloud.datacatalog_v1.types.Entry):
            Required. The updated entry. The "name" field
            must be set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on an entry.

            If this parameter is absent or empty, all modifiable fields
            are overwritten. If such fields are non-required and omitted
            in the request body, their values are emptied.

            The following fields are modifiable:

            -  For entries with type ``DATA_STREAM``:

               -  ``schema``

            -  For entries with type ``FILESET``:

               -  ``schema``
               -  ``display_name``
               -  ``description``
               -  ``gcs_fileset_spec``
               -  ``gcs_fileset_spec.file_patterns``

            -  For entries with ``user_specified_type``:

               -  ``schema``
               -  ``display_name``
               -  ``description``
               -  ``user_specified_type``
               -  ``user_specified_system``
               -  ``linked_resource``
               -  ``source_system_timestamps``
    """

    entry = proto.Field(proto.MESSAGE, number=1, message="Entry",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteEntryRequest(proto.Message):
    r"""Request message for
    [DeleteEntry][google.cloud.datacatalog.v1.DataCatalog.DeleteEntry].

    Attributes:
        name (str):
            Required. The name of the entry. Example:

            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}
    """

    name = proto.Field(proto.STRING, number=1,)


class GetEntryRequest(proto.Message):
    r"""Request message for
    [GetEntry][google.cloud.datacatalog.v1.DataCatalog.GetEntry].

    Attributes:
        name (str):
            Required. The name of the entry. Example:

            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}
    """

    name = proto.Field(proto.STRING, number=1,)


class LookupEntryRequest(proto.Message):
    r"""Request message for
    [LookupEntry][google.cloud.datacatalog.v1.DataCatalog.LookupEntry].

    Attributes:
        linked_resource (str):
            The full name of the Google Cloud Platform resource the Data
            Catalog entry represents. See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name.
            Full names are case-sensitive.

            Examples:

            -  //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId
            -  //pubsub.googleapis.com/projects/projectId/topics/topicId
        sql_resource (str):
            The SQL name of the entry. SQL names are case-sensitive.

            Examples:

            -  ``pubsub.project_id.topic_id``
            -  :literal:`pubsub.project_id.`topic.id.with.dots\``
            -  ``bigquery.table.project_id.dataset_id.table_id``
            -  ``bigquery.dataset.project_id.dataset_id``
            -  ``datacatalog.entry.project_id.location_id.entry_group_id.entry_id``

            ``*_id``\ s should satisfy the standard SQL rules for
            identifiers.
            https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical.
        fully_qualified_name (str):
            Fully qualified name (FQN) of the resource.

            FQNs take two forms:

            -  For non-regionalized resources:

               ``{SYSTEM}:{PROJECT}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            -  For regionalized resources:

               ``{SYSTEM}:{PROJECT}.{LOCATION_ID}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            Example for a DPMS table:

            ``dataproc_metastore:project_id.location_id.instance_id.database_id.table_id``
    """

    linked_resource = proto.Field(proto.STRING, number=1, oneof="target_name",)
    sql_resource = proto.Field(proto.STRING, number=3, oneof="target_name",)
    fully_qualified_name = proto.Field(proto.STRING, number=5, oneof="target_name",)


class Entry(proto.Message):
    r"""Entry Metadata. A Data Catalog Entry resource represents another
    resource in Google Cloud Platform (such as a BigQuery dataset or a
    Pub/Sub topic) or outside of Google Cloud Platform. Clients can use
    the ``linked_resource`` field in the Entry resource to refer to the
    original resource ID of the source system.

    An Entry resource contains resource details, such as its schema. An
    Entry can also be used to attach flexible metadata, such as a
    [Tag][google.cloud.datacatalog.v1.Tag].

    Attributes:
        name (str):
            Output only. The resource name of an entry in URL format.
            Example:

            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}``

            Note: The entry itself and its child resources might not be
            stored in the location specified in its name.
        linked_resource (str):
            The resource this metadata entry refers to.

            For Google Cloud Platform resources, ``linked_resource`` is
            the `full name of the
            resource <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__.
            For example, the ``linked_resource`` for a table resource
            from BigQuery is:

            ``//bigquery.googleapis.com/projects/{projectId}/datasets/{datasetId}/tables/{tableId}``

            Output only when entry is one of the types in the
            ``EntryType`` enum.

            For entries with a ``user_specified_type``, this field is
            optional and defaults to an empty string.

            The resource string must contain only letters (a-z, A-Z),
            numbers (0-9), underscores (_), periods (.), colons (:),
            slashes (/), dashes (-), and hashes (#). The maximum size is
            200 bytes when encoded in UTF-8.
        fully_qualified_name (str):
            Fully qualified name (FQN) of the resource. Set
            automatically for entries representing resources from synced
            systems. Settable only during creation and read-only
            afterwards. Can be used for search and lookup of the
            entries.

            FQNs take two forms:

            -  For non-regionalized resources:

               ``{SYSTEM}:{PROJECT}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            -  For regionalized resources:

               ``{SYSTEM}:{PROJECT}.{LOCATION_ID}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            Example for a DPMS table:

            ``dataproc_metastore:project_id.location_id.instance_id.database_id.table_id``
        type_ (google.cloud.datacatalog_v1.types.EntryType):
            The type of the entry.
            Only used for Entries with types in the
            EntryType enum.
        user_specified_type (str):
            Entry type if it does not fit any of the input-allowed
            values listed in ``EntryType`` enum above. When creating an
            entry, users should check the enum values first, if nothing
            matches the entry to be created, then provide a custom
            value, for example "my_special_type".
            ``user_specified_type`` strings must begin with a letter or
            underscore and can only contain letters, numbers, and
            underscores; are case insensitive; must be at least 1
            character and at most 64 characters long.

            Currently, only FILESET enum value is allowed. All other
            entries created through Data Catalog must use
            ``user_specified_type``.
        integrated_system (google.cloud.datacatalog_v1.types.IntegratedSystem):
            Output only. This field indicates the entry's
            source system that Data Catalog integrates with,
            such as BigQuery or Pub/Sub.
        user_specified_system (str):
            This field indicates the entry's source system that Data
            Catalog does not integrate with. ``user_specified_system``
            strings must begin with a letter or underscore and can only
            contain letters, numbers, and underscores; are case
            insensitive; must be at least 1 character and at most 64
            characters long.
        gcs_fileset_spec (google.cloud.datacatalog_v1.types.GcsFilesetSpec):
            Specification that applies to a Cloud Storage
            fileset. This is only valid on entries of type
            FILESET.
        bigquery_table_spec (google.cloud.datacatalog_v1.types.BigQueryTableSpec):
            Specification that applies to a BigQuery table. This is only
            valid on entries of type ``TABLE``.
        bigquery_date_sharded_spec (google.cloud.datacatalog_v1.types.BigQueryDateShardedSpec):
            Specification for a group of BigQuery tables with name
            pattern ``[prefix]YYYYMMDD``. Context:
            https://cloud.google.com/bigquery/docs/partitioned-tables#partitioning_versus_sharding.
        database_table_spec (google.cloud.datacatalog_v1.types.DatabaseTableSpec):
            Specification that applies to a table resource. Only valid
            for entries of ``TABLE`` type.
        display_name (str):
            Display name of an entry.

            The name must contain only Unicode letters, numbers (0-9),
            underscores (_), dashes (-), spaces ( ), and can't start or
            end with spaces. The maximum size is 200 bytes when encoded
            in UTF-8. Default value is an empty string.
        description (str):
            Entry description that can consist of several
            sentences or paragraphs that describe entry
            contents.
            The description must not contain Unicode non-
            characters as well as C0 and C1 control codes
            except tabs (HT), new lines (LF), carriage
            returns (CR), and page breaks (FF).
            The maximum size is 2000 bytes when encoded in
            UTF-8. Default value is an empty string.
        schema (google.cloud.datacatalog_v1.types.Schema):
            Schema of the entry. An entry might not have
            any schema attached to it.
        source_system_timestamps (google.cloud.datacatalog_v1.types.SystemTimestamps):
            Timestamps about the underlying resource, not about this
            Data Catalog entry. Output only when Entry is of type in the
            EntryType enum. For entries with user_specified_type, this
            field is optional and defaults to an empty timestamp.
        data_source (google.cloud.datacatalog_v1.types.DataSource):
            Output only. Physical location of the entry.
    """

    name = proto.Field(proto.STRING, number=1,)
    linked_resource = proto.Field(proto.STRING, number=9,)
    fully_qualified_name = proto.Field(proto.STRING, number=29,)
    type_ = proto.Field(proto.ENUM, number=2, oneof="entry_type", enum="EntryType",)
    user_specified_type = proto.Field(proto.STRING, number=16, oneof="entry_type",)
    integrated_system = proto.Field(
        proto.ENUM, number=17, oneof="system", enum=common.IntegratedSystem,
    )
    user_specified_system = proto.Field(proto.STRING, number=18, oneof="system",)
    gcs_fileset_spec = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="type_spec",
        message=gcd_gcs_fileset_spec.GcsFilesetSpec,
    )
    bigquery_table_spec = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="type_spec",
        message=table_spec.BigQueryTableSpec,
    )
    bigquery_date_sharded_spec = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="type_spec",
        message=table_spec.BigQueryDateShardedSpec,
    )
    database_table_spec = proto.Field(
        proto.MESSAGE, number=24, oneof="spec", message="DatabaseTableSpec",
    )
    display_name = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    schema = proto.Field(proto.MESSAGE, number=5, message=gcd_schema.Schema,)
    source_system_timestamps = proto.Field(
        proto.MESSAGE, number=7, message=timestamps.SystemTimestamps,
    )
    data_source = proto.Field(
        proto.MESSAGE, number=20, message=gcd_data_source.DataSource,
    )


class DatabaseTableSpec(proto.Message):
    r"""Specification that applies to a table resource. Only valid for
    entries of ``TABLE`` type.

    Attributes:
        type_ (google.cloud.datacatalog_v1.types.DatabaseTableSpec.TableType):
            Type of this table.
    """

    class TableType(proto.Enum):
        r"""Type of the table."""
        TABLE_TYPE_UNSPECIFIED = 0
        NATIVE = 1
        EXTERNAL = 2

    type_ = proto.Field(proto.ENUM, number=1, enum=TableType,)


class EntryGroup(proto.Message):
    r"""EntryGroup Metadata. An EntryGroup resource represents a logical
    grouping of zero or more Data Catalog
    [Entry][google.cloud.datacatalog.v1.Entry] resources.

    Attributes:
        name (str):
            The resource name of the entry group in URL format. Example:

            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}``

            Note: The entry group itself and its child resources might
            not be stored in the location specified in its name.
        display_name (str):
            A short name to identify the entry group, for
            example, "analytics data - jan 2011". Default
            value is an empty string.
        description (str):
            Entry group description, which can consist of
            several sentences or paragraphs that describe
            entry group contents. Default value is an empty
            string.
        data_catalog_timestamps (google.cloud.datacatalog_v1.types.SystemTimestamps):
            Output only. Timestamps about this
            EntryGroup. Default value is empty timestamps.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    data_catalog_timestamps = proto.Field(
        proto.MESSAGE, number=4, message=timestamps.SystemTimestamps,
    )


class CreateTagTemplateRequest(proto.Message):
    r"""Request message for
    [CreateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplate].

    Attributes:
        parent (str):
            Required. The name of the project and the template location
            `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.

            Example:

            -  projects/{project_id}/locations/us-central1
        tag_template_id (str):
            Required. The ID of the tag template to create.

            The ID must contain only lowercase letters (a-z), numbers
            (0-9), or underscores (_), and must start with a letter or
            underscore. The maximum size is 64 bytes when encoded in
            UTF-8.
        tag_template (google.cloud.datacatalog_v1.types.TagTemplate):
            Required. The tag template to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    tag_template_id = proto.Field(proto.STRING, number=3,)
    tag_template = proto.Field(proto.MESSAGE, number=2, message=gcd_tags.TagTemplate,)


class GetTagTemplateRequest(proto.Message):
    r"""Request message for
    [GetTagTemplate][google.cloud.datacatalog.v1.DataCatalog.GetTagTemplate].

    Attributes:
        name (str):
            Required. The name of the tag template. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateTagTemplateRequest(proto.Message):
    r"""Request message for
    [UpdateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplate].

    Attributes:
        tag_template (google.cloud.datacatalog_v1.types.TagTemplate):
            Required. The template to update. The "name"
            field must be set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on a tag template.
            Currently, only ``display_name`` can be overwritten.

            In general, if this parameter is absent or empty, all
            modifiable fields are overwritten. If such fields are
            non-required and omitted in the request body, their values
            are emptied.
    """

    tag_template = proto.Field(proto.MESSAGE, number=1, message=gcd_tags.TagTemplate,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteTagTemplateRequest(proto.Message):
    r"""Request message for
    [DeleteTagTemplate][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplate].

    Attributes:
        name (str):
            Required. The name of the tag template to delete. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}
        force (bool):
            Required. Currently, this field must always be set to
            ``true``. This confirms the deletion of any possible tags
            using this template. ``force = false`` will be supported in
            the future.
    """

    name = proto.Field(proto.STRING, number=1,)
    force = proto.Field(proto.BOOL, number=2,)


class CreateTagRequest(proto.Message):
    r"""Request message for
    [CreateTag][google.cloud.datacatalog.v1.DataCatalog.CreateTag].

    Attributes:
        parent (str):
            Required. The name of the resource to attach this tag to.
            Tags can be attached to entries. An entry can have up to
            1000 attached tags. Example:

            ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}``

            Note: The tag and its child resources might not be stored in
            the location specified in its name.
        tag (google.cloud.datacatalog_v1.types.Tag):
            Required. The tag to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    tag = proto.Field(proto.MESSAGE, number=2, message=gcd_tags.Tag,)


class UpdateTagRequest(proto.Message):
    r"""Request message for
    [UpdateTag][google.cloud.datacatalog.v1.DataCatalog.UpdateTag].

    Attributes:
        tag (google.cloud.datacatalog_v1.types.Tag):
            Required. The updated tag. The "name" field
            must be set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on a tag.
            Currently, a tag has the only modifiable field with the name
            ``fields``.

            In general, if this parameter is absent or empty, all
            modifiable fields are overwritten. If such fields are
            non-required and omitted in the request body, their values
            are emptied.
    """

    tag = proto.Field(proto.MESSAGE, number=1, message=gcd_tags.Tag,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteTagRequest(proto.Message):
    r"""Request message for
    [DeleteTag][google.cloud.datacatalog.v1.DataCatalog.DeleteTag].

    Attributes:
        name (str):
            Required. The name of the tag to delete. Example:

            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}/tags/{tag_id}
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [CreateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplateField].

    Attributes:
        parent (str):
            Required. The name of the project and the template location
            `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.

            Example:

            -  projects/{project_id}/locations/us-central1/tagTemplates/{tag_template_id}
        tag_template_field_id (str):
            Required. The ID of the tag template field to create.

            Note: Adding a required field to an existing template is
            *not* allowed.

            Field IDs can contain letters (both uppercase and
            lowercase), numbers (0-9), underscores (_) and dashes (-).
            Field IDs must be at least 1 character long and at most 128
            characters long. Field IDs must also be unique within their
            template.
        tag_template_field (google.cloud.datacatalog_v1.types.TagTemplateField):
            Required. The tag template field to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    tag_template_field_id = proto.Field(proto.STRING, number=2,)
    tag_template_field = proto.Field(
        proto.MESSAGE, number=3, message=gcd_tags.TagTemplateField,
    )


class UpdateTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [UpdateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template field. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}
        tag_template_field (google.cloud.datacatalog_v1.types.TagTemplateField):
            Required. The template to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Names of fields whose values to overwrite on an
            individual field of a tag template. The following fields are
            modifiable:

            -  ``display_name``
            -  ``type.enum_type``
            -  ``is_required``

            If this parameter is absent or empty, all modifiable fields
            are overwritten. If such fields are non-required and omitted
            in the request body, their values are emptied with one
            exception: when updating an enum type, the provided values
            are merged with the existing values. Therefore, enum values
            can only be added, existing enum values cannot be deleted or
            renamed.

            Additionally, updating a template field from optional to
            required is *not* allowed.
    """

    name = proto.Field(proto.STRING, number=1,)
    tag_template_field = proto.Field(
        proto.MESSAGE, number=2, message=gcd_tags.TagTemplateField,
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


class RenameTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [RenameTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}
        new_tag_template_field_id (str):
            Required. The new ID of this tag template field. For
            example, ``my_new_field``.
    """

    name = proto.Field(proto.STRING, number=1,)
    new_tag_template_field_id = proto.Field(proto.STRING, number=2,)


class RenameTagTemplateFieldEnumValueRequest(proto.Message):
    r"""Request message for
    [RenameTagTemplateFieldEnumValue][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateFieldEnumValue].

    Attributes:
        name (str):
            Required. The name of the enum field value. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}/enumValues/{enum_value_display_name}
        new_enum_value_display_name (str):
            Required. The new display name of the enum value. For
            example, ``my_new_enum_value``.
    """

    name = proto.Field(proto.STRING, number=1,)
    new_enum_value_display_name = proto.Field(proto.STRING, number=2,)


class DeleteTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [DeleteTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template field to delete.
            Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}
        force (bool):
            Required. Currently, this field must always be set to
            ``true``. This confirms the deletion of this field from any
            tags using this field. ``force = false`` will be supported
            in the future.
    """

    name = proto.Field(proto.STRING, number=1,)
    force = proto.Field(proto.BOOL, number=2,)


class ListTagsRequest(proto.Message):
    r"""Request message for
    [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].

    Attributes:
        parent (str):
            Required. The name of the Data Catalog resource to list the
            tags of. The resource could be an
            [Entry][google.cloud.datacatalog.v1.Entry] or an
            [EntryGroup][google.cloud.datacatalog.v1.EntryGroup].

            Examples:

            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}
            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}
        page_size (int):
            The maximum number of tags to return. Default
            is 10. Max limit is 1000.
        page_token (str):
            Token that specifies which page is requested.
            If empty, the first page is returned.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListTagsResponse(proto.Message):
    r"""Response message for
    [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].

    Attributes:
        tags (Sequence[google.cloud.datacatalog_v1.types.Tag]):
            [Tag][google.cloud.datacatalog.v1.Tag] details.
        next_page_token (str):
            Token to retrieve the next page of results.
            It is set to empty if no items remain in
            results.
    """

    @property
    def raw_page(self):
        return self

    tags = proto.RepeatedField(proto.MESSAGE, number=1, message=gcd_tags.Tag,)
    next_page_token = proto.Field(proto.STRING, number=2,)


class ListEntriesRequest(proto.Message):
    r"""Request message for
    [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].

    Attributes:
        parent (str):
            Required. The name of the entry group that contains the
            entries, which can be provided in URL format. Example:

            -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}
        page_size (int):
            The maximum number of items to return. Default is 10. Max
            limit is 1000. Throws an invalid argument for
            ``page_size > 1000``.
        page_token (str):
            Token that specifies which page is requested.
            If empty, the first page is returned.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to return for each Entry. If not set or empty,
            all fields are returned. For example, setting read_mask to
            contain only one path "name" will cause ListEntries to
            return a list of Entries with only "name" field.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    read_mask = proto.Field(proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,)


class ListEntriesResponse(proto.Message):
    r"""Response message for
    [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].

    Attributes:
        entries (Sequence[google.cloud.datacatalog_v1.types.Entry]):
            Entry details.
        next_page_token (str):
            Token to retrieve the next page of results.
            It is set to empty if no items remain in
            results.
    """

    @property
    def raw_page(self):
        return self

    entries = proto.RepeatedField(proto.MESSAGE, number=1, message="Entry",)
    next_page_token = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
