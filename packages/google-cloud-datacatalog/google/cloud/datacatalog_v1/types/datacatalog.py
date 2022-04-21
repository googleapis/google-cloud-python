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
from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.datacatalog_v1.types import gcs_fileset_spec as gcd_gcs_fileset_spec
from google.cloud.datacatalog_v1.types import bigquery, common
from google.cloud.datacatalog_v1.types import data_source as gcd_data_source
from google.cloud.datacatalog_v1.types import dataplex_spec
from google.cloud.datacatalog_v1.types import schema as gcd_schema
from google.cloud.datacatalog_v1.types import search, table_spec
from google.cloud.datacatalog_v1.types import tags as gcd_tags
from google.cloud.datacatalog_v1.types import timestamps, usage

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
        "FilesetSpec",
        "DataSourceConnectionSpec",
        "RoutineSpec",
        "BusinessContext",
        "EntryOverview",
        "Contacts",
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
        "StarEntryRequest",
        "StarEntryResponse",
        "UnstarEntryRequest",
        "UnstarEntryResponse",
        "ModifyEntryOverviewRequest",
        "ModifyEntryContactsRequest",
    },
)


class EntryType(proto.Enum):
    r"""The enum field that lists all the types of entry resources in Data
    Catalog. For example, a BigQuery table entry has the ``TABLE`` type.
    """
    ENTRY_TYPE_UNSPECIFIED = 0
    TABLE = 2
    MODEL = 5
    DATA_STREAM = 3
    FILESET = 4
    CLUSTER = 6
    DATABASE = 7
    DATA_SOURCE_CONNECTION = 8
    ROUTINE = 9
    LAKE = 10
    ZONE = 11
    SERVICE = 14


class SearchCatalogRequest(proto.Message):
    r"""Request message for
    [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

    Attributes:
        scope (google.cloud.datacatalog_v1.types.SearchCatalogRequest.Scope):
            Required. The scope of this search request.

            The ``scope`` is invalid if ``include_org_ids``,
            ``include_project_ids`` are empty AND
            ``include_gcp_public_datasets`` is set to ``false``. In this
            case, the request returns an error.
        query (str):
            Optional. The query string with a minimum of 3 characters
            and specific syntax. For more information, see `Data Catalog
            search
            syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__.

            An empty query string returns all data assets (in the
            specified scope) that you have access to.

            A query string can be a simple ``xyz`` or qualified by
            predicates:

            -  ``name:x``
            -  ``column:y``
            -  ``description:z``
        page_size (int):
            Number of results to return in a single
            search page.
            Can't be negative or 0, defaults to 10 in this
            case. The maximum number is 1000. If exceeded,
            throws an "invalid argument" exception.
        page_token (str):
            Optional. Pagination token that, if specified, returns the
            next page of search results. If empty, returns the first
            page.

            This token is returned in the
            [SearchCatalogResponse.next_page_token][google.cloud.datacatalog.v1.SearchCatalogResponse.next_page_token]
            field of the response to a previous
            [SearchCatalogRequest][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog]
            call.
        order_by (str):
            Specifies the order of results.

            Currently supported case-sensitive values are:

            -  ``relevance`` that can only be descending
            -  ``last_modified_timestamp [asc|desc]`` with descending
               (``desc``) as default
            -  ``default`` that can only be descending

            If this parameter is omitted, it defaults to the descending
            ``relevance``.
    """

    class Scope(proto.Message):
        r"""The criteria that select the subspace used for query
        matching.

        Attributes:
            include_org_ids (Sequence[str]):
                The list of organization IDs to search within.

                To find your organization ID, follow the steps from
                [Creating and managing organizations]
                (/resource-manager/docs/creating-managing-organization).
            include_project_ids (Sequence[str]):
                The list of project IDs to search within.

                For more information on the distinction between project
                names, IDs, and numbers, see
                `Projects </docs/overview/#projects>`__.
            include_gcp_public_datasets (bool):
                If ``true``, include Google Cloud Platform (GCP) public
                datasets in search results. By default, they are excluded.

                See `Google Cloud Public Datasets </public-datasets>`__ for
                more information.
            restricted_locations (Sequence[str]):
                Optional. The list of locations to search within. If empty,
                all locations are searched.

                Returns an error if any location in the list isn't one of
                the `Supported
                regions <https://cloud.google.com/data-catalog/docs/concepts/regions#supported_regions>`__.

                If a location is unreachable, its name is returned in the
                ``SearchCatalogResponse.unreachable`` field. To get
                additional information on the error, repeat the search
                request and set the location name as the value of this
                parameter.
            starred_only (bool):
                Optional. If ``true``, search only among starred entries.

                By default, all results are returned, starred or not.
            include_public_tag_templates (bool):
                Optional. This field is deprecated. The
                search mechanism for public and private tag
                templates is the same.
        """

        include_org_ids = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        include_project_ids = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        include_gcp_public_datasets = proto.Field(
            proto.BOOL,
            number=7,
        )
        restricted_locations = proto.RepeatedField(
            proto.STRING,
            number=16,
        )
        starred_only = proto.Field(
            proto.BOOL,
            number=18,
        )
        include_public_tag_templates = proto.Field(
            proto.BOOL,
            number=19,
        )

    scope = proto.Field(
        proto.MESSAGE,
        number=6,
        message=Scope,
    )
    query = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class SearchCatalogResponse(proto.Message):
    r"""Response message for
    [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

    Attributes:
        results (Sequence[google.cloud.datacatalog_v1.types.SearchCatalogResult]):
            Search results.
        next_page_token (str):
            Pagination token that can be used in
            subsequent calls to retrieve the next page of
            results.
        unreachable (Sequence[str]):
            Unreachable locations. Search results don't include data
            from those locations.

            To get additional information on an error, repeat the search
            request and restrict it to specific locations by setting the
            ``SearchCatalogRequest.scope.restricted_locations``
            parameter.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=search.SearchCatalogResult,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=6,
    )


class CreateEntryGroupRequest(proto.Message):
    r"""Request message for
    [CreateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.CreateEntryGroup].

    Attributes:
        parent (str):
            Required. The names of the project and
            location that the new entry group belongs to.
            Note: The entry group itself and its child
            resources might not be stored in the location
            specified in its name.
        entry_group_id (str):
            Required. The ID of the entry group to create.

            The ID must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and must start with a letter or underscore.
            The maximum size is 64 bytes when encoded in UTF-8.
        entry_group (google.cloud.datacatalog_v1.types.EntryGroup):
            The entry group to create. Defaults to empty.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_group_id = proto.Field(
        proto.STRING,
        number=3,
    )
    entry_group = proto.Field(
        proto.MESSAGE,
        number=2,
        message="EntryGroup",
    )


class UpdateEntryGroupRequest(proto.Message):
    r"""Request message for
    [UpdateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.UpdateEntryGroup].

    Attributes:
        entry_group (google.cloud.datacatalog_v1.types.EntryGroup):
            Required. Updates for the entry group. The ``name`` field
            must be set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on
            an entry group.
            If this parameter is absent or empty, all
            modifiable fields are overwritten. If such
            fields are non-required and omitted in the
            request body, their values are emptied.
    """

    entry_group = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EntryGroup",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetEntryGroupRequest(proto.Message):
    r"""Request message for
    [GetEntryGroup][google.cloud.datacatalog.v1.DataCatalog.GetEntryGroup].

    Attributes:
        name (str):
            Required. The name of the entry group to get.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to return. If empty or omitted,
            all fields are returned.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    read_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteEntryGroupRequest(proto.Message):
    r"""Request message for
    [DeleteEntryGroup][google.cloud.datacatalog.v1.DataCatalog.DeleteEntryGroup].

    Attributes:
        name (str):
            Required. The name of the entry group to
            delete.
        force (bool):
            Optional. If true, deletes all entries in the
            entry group.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    force = proto.Field(
        proto.BOOL,
        number=2,
    )


class ListEntryGroupsRequest(proto.Message):
    r"""Request message for
    [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].

    Attributes:
        parent (str):
            Required. The name of the location that
            contains the entry groups to list.
            Can be provided as a URL.
        page_size (int):
            Optional. The maximum number of items to return.

            Default is 10. Maximum limit is 1000. Throws an invalid
            argument if ``page_size`` is greater than 1000.
        page_token (str):
            Optional. Pagination token that specifies the
            next page to return. If empty, returns the first
            page.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListEntryGroupsResponse(proto.Message):
    r"""Response message for
    [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].

    Attributes:
        entry_groups (Sequence[google.cloud.datacatalog_v1.types.EntryGroup]):
            Entry group details.
        next_page_token (str):
            Pagination token to specify in the next call
            to retrieve the next page of results. Empty if
            there are no more items.
    """

    @property
    def raw_page(self):
        return self

    entry_groups = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EntryGroup",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateEntryRequest(proto.Message):
    r"""Request message for
    [CreateEntry][google.cloud.datacatalog.v1.DataCatalog.CreateEntry].

    Attributes:
        parent (str):
            Required. The name of the entry group this
            entry belongs to.
            Note: The entry itself and its child resources
            might not be stored in the location specified in
            its name.
        entry_id (str):
            Required. The ID of the entry to create.

            The ID must contain only letters (a-z, A-Z), numbers (0-9),
            and underscores (_). The maximum size is 64 bytes when
            encoded in UTF-8.
        entry (google.cloud.datacatalog_v1.types.Entry):
            Required. The entry to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_id = proto.Field(
        proto.STRING,
        number=3,
    )
    entry = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Entry",
    )


class UpdateEntryRequest(proto.Message):
    r"""Request message for
    [UpdateEntry][google.cloud.datacatalog.v1.DataCatalog.UpdateEntry].

    Attributes:
        entry (google.cloud.datacatalog_v1.types.Entry):
            Required. Updates for the entry. The ``name`` field must be
            set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on an entry.

            If this parameter is absent or empty, all modifiable fields
            are overwritten. If such fields are non-required and omitted
            in the request body, their values are emptied.

            You can modify only the fields listed below.

            For entries with type ``DATA_STREAM``:

            -  ``schema``

            For entries with type ``FILESET``:

            -  ``schema``
            -  ``display_name``
            -  ``description``
            -  ``gcs_fileset_spec``
            -  ``gcs_fileset_spec.file_patterns``

            For entries with ``user_specified_type``:

            -  ``schema``
            -  ``display_name``
            -  ``description``
            -  ``user_specified_type``
            -  ``user_specified_system``
            -  ``linked_resource``
            -  ``source_system_timestamps``
    """

    entry = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Entry",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteEntryRequest(proto.Message):
    r"""Request message for
    [DeleteEntry][google.cloud.datacatalog.v1.DataCatalog.DeleteEntry].

    Attributes:
        name (str):
            Required. The name of the entry to delete.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetEntryRequest(proto.Message):
    r"""Request message for
    [GetEntry][google.cloud.datacatalog.v1.DataCatalog.GetEntry].

    Attributes:
        name (str):
            Required. The name of the entry to get.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class LookupEntryRequest(proto.Message):
    r"""Request message for
    [LookupEntry][google.cloud.datacatalog.v1.DataCatalog.LookupEntry].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        linked_resource (str):
            The full name of the Google Cloud Platform resource the Data
            Catalog entry represents. For more information, see [Full
            Resource Name]
            (https://cloud.google.com/apis/design/resource_names#full_resource_name).

            Full names are case-sensitive. For example:

            -  ``//bigquery.googleapis.com/projects/{PROJECT_ID}/datasets/{DATASET_ID}/tables/{TABLE_ID}``
            -  ``//pubsub.googleapis.com/projects/{PROJECT_ID}/topics/{TOPIC_ID}``

            This field is a member of `oneof`_ ``target_name``.
        sql_resource (str):
            The SQL name of the entry. SQL names are case-sensitive.

            Examples:

            -  ``pubsub.topic.{PROJECT_ID}.{TOPIC_ID}``
            -  ``pubsub.topic.{PROJECT_ID}.``\ \`\ ``{TOPIC.ID.SEPARATED.WITH.DOTS}``\ \`
            -  ``bigquery.table.{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}``
            -  ``bigquery.dataset.{PROJECT_ID}.{DATASET_ID}``
            -  ``datacatalog.entry.{PROJECT_ID}.{LOCATION_ID}.{ENTRY_GROUP_ID}.{ENTRY_ID}``

            Identifiers (``*_ID``) should comply with the [Lexical
            structure in Standard SQL]
            (https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical).

            This field is a member of `oneof`_ ``target_name``.
        fully_qualified_name (str):
            Fully qualified name (FQN) of the resource.

            FQNs take two forms:

            -  For non-regionalized resources:

               ``{SYSTEM}:{PROJECT}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            -  For regionalized resources:

               ``{SYSTEM}:{PROJECT}.{LOCATION_ID}.{PATH_TO_RESOURCE_SEPARATED_WITH_DOTS}``

            Example for a DPMS table:

            ``dataproc_metastore:{PROJECT_ID}.{LOCATION_ID}.{INSTANCE_ID}.{DATABASE_ID}.{TABLE_ID}``

            This field is a member of `oneof`_ ``target_name``.
    """

    linked_resource = proto.Field(
        proto.STRING,
        number=1,
        oneof="target_name",
    )
    sql_resource = proto.Field(
        proto.STRING,
        number=3,
        oneof="target_name",
    )
    fully_qualified_name = proto.Field(
        proto.STRING,
        number=5,
        oneof="target_name",
    )


class Entry(proto.Message):
    r"""Entry metadata. A Data Catalog entry represents another resource in
    Google Cloud Platform (such as a BigQuery dataset or a Pub/Sub
    topic) or outside of it. You can use the ``linked_resource`` field
    in the entry resource to refer to the original resource ID of the
    source system.

    An entry resource contains resource details, for example, its
    schema. Additionally, you can attach flexible metadata to an entry
    in the form of a [Tag][google.cloud.datacatalog.v1.Tag].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The resource name of an entry in
            URL format.
            Note: The entry itself and its child resources
            might not be stored in the location specified in
            its name.
        linked_resource (str):
            The resource this metadata entry refers to.

            For Google Cloud Platform resources, ``linked_resource`` is
            the [Full Resource Name]
            (https://cloud.google.com/apis/design/resource_names#full_resource_name).
            For example, the ``linked_resource`` for a table resource
            from BigQuery is:

            ``//bigquery.googleapis.com/projects/{PROJECT_ID}/datasets/{DATASET_ID}/tables/{TABLE_ID}``

            Output only when the entry is one of the types in the
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

            ``dataproc_metastore:{PROJECT_ID}.{LOCATION_ID}.{INSTANCE_ID}.{DATABASE_ID}.{TABLE_ID}``
        type_ (google.cloud.datacatalog_v1.types.EntryType):
            The type of the entry. Only used for entries with types
            listed in the ``EntryType`` enum.

            Currently, only ``FILESET`` enum value is allowed. All other
            entries created in Data Catalog must use the
            ``user_specified_type``.

            This field is a member of `oneof`_ ``entry_type``.
        user_specified_type (str):
            Custom entry type that doesn't match any of the values
            allowed for input and listed in the ``EntryType`` enum.

            When creating an entry, first check the type values in the
            enum. If there are no appropriate types for the new entry,
            provide a custom value, for example, ``my_special_type``.

            The ``user_specified_type`` string has the following
            limitations:

            -  Is case insensitive.
            -  Must begin with a letter or underscore.
            -  Can only contain letters, numbers, and underscores.
            -  Must be at least 1 character and at most 64 characters
               long.

            This field is a member of `oneof`_ ``entry_type``.
        integrated_system (google.cloud.datacatalog_v1.types.IntegratedSystem):
            Output only. Indicates the entry's source
            system that Data Catalog integrates with, such
            as BigQuery, Pub/Sub, or Dataproc Metastore.

            This field is a member of `oneof`_ ``system``.
        user_specified_system (str):
            Indicates the entry's source system that Data Catalog
            doesn't automatically integrate with.

            The ``user_specified_system`` string has the following
            limitations:

            -  Is case insensitive.
            -  Must begin with a letter or underscore.
            -  Can only contain letters, numbers, and underscores.
            -  Must be at least 1 character and at most 64 characters
               long.

            This field is a member of `oneof`_ ``system``.
        gcs_fileset_spec (google.cloud.datacatalog_v1.types.GcsFilesetSpec):
            Specification that applies to a Cloud Storage fileset. Valid
            only for entries with the ``FILESET`` type.

            This field is a member of `oneof`_ ``type_spec``.
        bigquery_table_spec (google.cloud.datacatalog_v1.types.BigQueryTableSpec):
            Specification that applies to a BigQuery table. Valid only
            for entries with the ``TABLE`` type.

            This field is a member of `oneof`_ ``type_spec``.
        bigquery_date_sharded_spec (google.cloud.datacatalog_v1.types.BigQueryDateShardedSpec):
            Specification for a group of BigQuery tables with the
            ``[prefix]YYYYMMDD`` name pattern.

            For more information, see [Introduction to partitioned
            tables]
            (https://cloud.google.com/bigquery/docs/partitioned-tables#partitioning_versus_sharding).

            This field is a member of `oneof`_ ``type_spec``.
        database_table_spec (google.cloud.datacatalog_v1.types.DatabaseTableSpec):
            Specification that applies to a table resource. Valid only
            for entries with the ``TABLE`` type.

            This field is a member of `oneof`_ ``spec``.
        data_source_connection_spec (google.cloud.datacatalog_v1.types.DataSourceConnectionSpec):
            Specification that applies to a data source connection.
            Valid only for entries with the ``DATA_SOURCE_CONNECTION``
            type.

            This field is a member of `oneof`_ ``spec``.
        routine_spec (google.cloud.datacatalog_v1.types.RoutineSpec):
            Specification that applies to a user-defined function or
            procedure. Valid only for entries with the ``ROUTINE`` type.

            This field is a member of `oneof`_ ``spec``.
        fileset_spec (google.cloud.datacatalog_v1.types.FilesetSpec):
            Specification that applies to a fileset resource. Valid only
            for entries with the ``FILESET`` type.

            This field is a member of `oneof`_ ``spec``.
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
            The description must not contain Unicode
            non-characters as well as C0 and C1 control
            codes except tabs (HT), new lines (LF), carriage
            returns (CR), and page breaks (FF).
            The maximum size is 2000 bytes when encoded in
            UTF-8. Default value is an empty string.
        business_context (google.cloud.datacatalog_v1.types.BusinessContext):
            Business Context of the entry. Not supported
            for BigQuery datasets
        schema (google.cloud.datacatalog_v1.types.Schema):
            Schema of the entry. An entry might not have
            any schema attached to it.
        source_system_timestamps (google.cloud.datacatalog_v1.types.SystemTimestamps):
            Timestamps from the underlying resource, not from the Data
            Catalog entry.

            Output only when the entry has a type listed in the
            ``EntryType`` enum. For entries with
            ``user_specified_type``, this field is optional and defaults
            to an empty timestamp.
        usage_signal (google.cloud.datacatalog_v1.types.UsageSignal):
            Output only. Resource usage statistics.
        labels (Mapping[str, str]):
            Cloud labels attached to the entry.
            In Data Catalog, you can create and modify
            labels attached only to custom entries. Synced
            entries have unmodifiable labels that come from
            the source system.
        data_source (google.cloud.datacatalog_v1.types.DataSource):
            Output only. Physical location of the entry.
        personal_details (google.cloud.datacatalog_v1.types.PersonalDetails):
            Output only. Additional information related
            to the entry. Private to the current user.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    linked_resource = proto.Field(
        proto.STRING,
        number=9,
    )
    fully_qualified_name = proto.Field(
        proto.STRING,
        number=29,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=2,
        oneof="entry_type",
        enum="EntryType",
    )
    user_specified_type = proto.Field(
        proto.STRING,
        number=16,
        oneof="entry_type",
    )
    integrated_system = proto.Field(
        proto.ENUM,
        number=17,
        oneof="system",
        enum=common.IntegratedSystem,
    )
    user_specified_system = proto.Field(
        proto.STRING,
        number=18,
        oneof="system",
    )
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
        proto.MESSAGE,
        number=24,
        oneof="spec",
        message="DatabaseTableSpec",
    )
    data_source_connection_spec = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof="spec",
        message="DataSourceConnectionSpec",
    )
    routine_spec = proto.Field(
        proto.MESSAGE,
        number=28,
        oneof="spec",
        message="RoutineSpec",
    )
    fileset_spec = proto.Field(
        proto.MESSAGE,
        number=33,
        oneof="spec",
        message="FilesetSpec",
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    description = proto.Field(
        proto.STRING,
        number=4,
    )
    business_context = proto.Field(
        proto.MESSAGE,
        number=37,
        message="BusinessContext",
    )
    schema = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcd_schema.Schema,
    )
    source_system_timestamps = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamps.SystemTimestamps,
    )
    usage_signal = proto.Field(
        proto.MESSAGE,
        number=13,
        message=usage.UsageSignal,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=14,
    )
    data_source = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gcd_data_source.DataSource,
    )
    personal_details = proto.Field(
        proto.MESSAGE,
        number=26,
        message=common.PersonalDetails,
    )


class DatabaseTableSpec(proto.Message):
    r"""Specification that applies to a table resource. Valid only for
    entries with the ``TABLE`` type.

    Attributes:
        type_ (google.cloud.datacatalog_v1.types.DatabaseTableSpec.TableType):
            Type of this table.
        dataplex_table (google.cloud.datacatalog_v1.types.DataplexTableSpec):
            Fields specific to a Dataplex table and
            present only in the Dataplex table entries.
    """

    class TableType(proto.Enum):
        r"""Type of the table."""
        TABLE_TYPE_UNSPECIFIED = 0
        NATIVE = 1
        EXTERNAL = 2

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=TableType,
    )
    dataplex_table = proto.Field(
        proto.MESSAGE,
        number=2,
        message=dataplex_spec.DataplexTableSpec,
    )


class FilesetSpec(proto.Message):
    r"""Specification that applies to a fileset. Valid only for
    entries with the 'FILESET' type.

    Attributes:
        dataplex_fileset (google.cloud.datacatalog_v1.types.DataplexFilesetSpec):
            Fields specific to a Dataplex fileset and
            present only in the Dataplex fileset entries.
    """

    dataplex_fileset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=dataplex_spec.DataplexFilesetSpec,
    )


class DataSourceConnectionSpec(proto.Message):
    r"""Specification that applies to a data source connection. Valid only
    for entries with the ``DATA_SOURCE_CONNECTION`` type.

    Attributes:
        bigquery_connection_spec (google.cloud.datacatalog_v1.types.BigQueryConnectionSpec):
            Fields specific to BigQuery connections.
    """

    bigquery_connection_spec = proto.Field(
        proto.MESSAGE,
        number=1,
        message=bigquery.BigQueryConnectionSpec,
    )


class RoutineSpec(proto.Message):
    r"""Specification that applies to a routine. Valid only for entries with
    the ``ROUTINE`` type.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        routine_type (google.cloud.datacatalog_v1.types.RoutineSpec.RoutineType):
            The type of the routine.
        language (str):
            The language the routine is written in. The exact value
            depends on the source system. For BigQuery routines,
            possible values are:

            -  ``SQL``
            -  ``JAVASCRIPT``
        routine_arguments (Sequence[google.cloud.datacatalog_v1.types.RoutineSpec.Argument]):
            Arguments of the routine.
        return_type (str):
            Return type of the argument. The exact value
            depends on the source system and the language.
        definition_body (str):
            The body of the routine.
        bigquery_routine_spec (google.cloud.datacatalog_v1.types.BigQueryRoutineSpec):
            Fields specific for BigQuery routines.

            This field is a member of `oneof`_ ``system_spec``.
    """

    class RoutineType(proto.Enum):
        r"""The fine-grained type of the routine."""
        ROUTINE_TYPE_UNSPECIFIED = 0
        SCALAR_FUNCTION = 1
        PROCEDURE = 2

    class Argument(proto.Message):
        r"""Input or output argument of a function or stored procedure.

        Attributes:
            name (str):
                The name of the argument. A return argument
                of a function might not have a name.
            mode (google.cloud.datacatalog_v1.types.RoutineSpec.Argument.Mode):
                Specifies whether the argument is input or
                output.
            type_ (str):
                Type of the argument. The exact value depends
                on the source system and the language.
        """

        class Mode(proto.Enum):
            r"""The input or output mode of the argument."""
            MODE_UNSPECIFIED = 0
            IN = 1
            OUT = 2
            INOUT = 3

        name = proto.Field(
            proto.STRING,
            number=1,
        )
        mode = proto.Field(
            proto.ENUM,
            number=2,
            enum="RoutineSpec.Argument.Mode",
        )
        type_ = proto.Field(
            proto.STRING,
            number=3,
        )

    routine_type = proto.Field(
        proto.ENUM,
        number=1,
        enum=RoutineType,
    )
    language = proto.Field(
        proto.STRING,
        number=2,
    )
    routine_arguments = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=Argument,
    )
    return_type = proto.Field(
        proto.STRING,
        number=4,
    )
    definition_body = proto.Field(
        proto.STRING,
        number=5,
    )
    bigquery_routine_spec = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="system_spec",
        message=bigquery.BigQueryRoutineSpec,
    )


class BusinessContext(proto.Message):
    r"""Business Context of the entry.

    Attributes:
        entry_overview (google.cloud.datacatalog_v1.types.EntryOverview):
            Entry overview fields for rich text
            descriptions of entries.
        contacts (google.cloud.datacatalog_v1.types.Contacts):
            Contact people for the entry.
    """

    entry_overview = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EntryOverview",
    )
    contacts = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Contacts",
    )


class EntryOverview(proto.Message):
    r"""Entry overview fields for rich text descriptions of entries.

    Attributes:
        overview (str):
            Entry overview with support for rich text.
            The overview must only contain Unicode
            characters, and should be formatted using HTML.
            The maximum length is 10 MiB as this value holds
            HTML descriptions including encoded images. The
            maximum length of the text without images is 100
            KiB.
    """

    overview = proto.Field(
        proto.STRING,
        number=1,
    )


class Contacts(proto.Message):
    r"""Contact people for the entry.

    Attributes:
        people (Sequence[google.cloud.datacatalog_v1.types.Contacts.Person]):
            The list of contact people for the entry.
    """

    class Person(proto.Message):
        r"""A contact person for the entry.

        Attributes:
            designation (str):
                Designation of the person, for example, Data
                Steward.
            email (str):
                Email of the person in the format of ``john.doe@xyz``,
                ``<john.doe@xyz>``, or ``John Doe<john.doe@xyz>``.
        """

        designation = proto.Field(
            proto.STRING,
            number=1,
        )
        email = proto.Field(
            proto.STRING,
            number=2,
        )

    people = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Person,
    )


class EntryGroup(proto.Message):
    r"""Entry group metadata.

    An ``EntryGroup`` resource represents a logical grouping of zero or
    more Data Catalog [Entry][google.cloud.datacatalog.v1.Entry]
    resources.

    Attributes:
        name (str):
            The resource name of the entry group in URL
            format.
            Note: The entry group itself and its child
            resources might not be stored in the location
            specified in its name.
        display_name (str):
            A short name to identify the entry group, for
            example, "analytics data - jan 2011". Default
            value is an empty string.
        description (str):
            Entry group description. Can consist of
            several sentences or paragraphs that describe
            the entry group contents. Default value is an
            empty string.
        data_catalog_timestamps (google.cloud.datacatalog_v1.types.SystemTimestamps):
            Output only. Timestamps of the entry group.
            Default value is empty.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    data_catalog_timestamps = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamps.SystemTimestamps,
    )


class CreateTagTemplateRequest(proto.Message):
    r"""Request message for
    [CreateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplate].

    Attributes:
        parent (str):
            Required. The name of the project and the template location
            `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.
        tag_template_id (str):
            Required. The ID of the tag template to create.

            The ID must contain only lowercase letters (a-z), numbers
            (0-9), or underscores (_), and must start with a letter or
            underscore. The maximum size is 64 bytes when encoded in
            UTF-8.
        tag_template (google.cloud.datacatalog_v1.types.TagTemplate):
            Required. The tag template to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    tag_template_id = proto.Field(
        proto.STRING,
        number=3,
    )
    tag_template = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_tags.TagTemplate,
    )


class GetTagTemplateRequest(proto.Message):
    r"""Request message for
    [GetTagTemplate][google.cloud.datacatalog.v1.DataCatalog.GetTagTemplate].

    Attributes:
        name (str):
            Required. The name of the tag template to
            get.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateTagTemplateRequest(proto.Message):
    r"""Request message for
    [UpdateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplate].

    Attributes:
        tag_template (google.cloud.datacatalog_v1.types.TagTemplate):
            Required. The template to update. The ``name`` field must be
            set.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Names of fields whose values to overwrite on a tag template.
            Currently, only ``display_name`` and
            ``is_publicly_readable`` can be overwritten.

            If this parameter is absent or empty, all modifiable fields
            are overwritten. If such fields are non-required and omitted
            in the request body, their values are emptied.

            Note: Updating the ``is_publicly_readable`` field may
            require up to 12 hours to take effect in search results.
    """

    tag_template = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_tags.TagTemplate,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteTagTemplateRequest(proto.Message):
    r"""Request message for
    [DeleteTagTemplate][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplate].

    Attributes:
        name (str):
            Required. The name of the tag template to
            delete.
        force (bool):
            Required. If true, deletes all tags that use this template.

            Currently, ``true`` is the only supported value.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    force = proto.Field(
        proto.BOOL,
        number=2,
    )


class CreateTagRequest(proto.Message):
    r"""Request message for
    [CreateTag][google.cloud.datacatalog.v1.DataCatalog.CreateTag].

    Attributes:
        parent (str):
            Required. The name of the resource to attach
            this tag to.
            Tags can be attached to entries or entry groups.
            An entry can have up to 1000 attached tags.

            Note: The tag and its child resources might not
            be stored in the location specified in its name.
        tag (google.cloud.datacatalog_v1.types.Tag):
            Required. The tag to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    tag = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_tags.Tag,
    )


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

    tag = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_tags.Tag,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteTagRequest(proto.Message):
    r"""Request message for
    [DeleteTag][google.cloud.datacatalog.v1.DataCatalog.DeleteTag].

    Attributes:
        name (str):
            Required. The name of the tag to delete.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [CreateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplateField].

    Attributes:
        parent (str):
            Required. The name of the project and the template location
            `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.
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

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    tag_template_field_id = proto.Field(
        proto.STRING,
        number=2,
    )
    tag_template_field = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcd_tags.TagTemplateField,
    )


class UpdateTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [UpdateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template field.
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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    tag_template_field = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_tags.TagTemplateField,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


class RenameTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [RenameTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template field.
        new_tag_template_field_id (str):
            Required. The new ID of this tag template field. For
            example, ``my_new_field``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    new_tag_template_field_id = proto.Field(
        proto.STRING,
        number=2,
    )


class RenameTagTemplateFieldEnumValueRequest(proto.Message):
    r"""Request message for
    [RenameTagTemplateFieldEnumValue][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateFieldEnumValue].

    Attributes:
        name (str):
            Required. The name of the enum field value.
        new_enum_value_display_name (str):
            Required. The new display name of the enum value. For
            example, ``my_new_enum_value``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    new_enum_value_display_name = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteTagTemplateFieldRequest(proto.Message):
    r"""Request message for
    [DeleteTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplateField].

    Attributes:
        name (str):
            Required. The name of the tag template field
            to delete.
        force (bool):
            Required. If true, deletes this field from any tags that use
            it.

            Currently, ``true`` is the only supported value.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    force = proto.Field(
        proto.BOOL,
        number=2,
    )


class ListTagsRequest(proto.Message):
    r"""Request message for
    [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].

    Attributes:
        parent (str):
            Required. The name of the Data Catalog resource to list the
            tags of.

            The resource can be an
            [Entry][google.cloud.datacatalog.v1.Entry] or an
            [EntryGroup][google.cloud.datacatalog.v1.EntryGroup]
            (without ``/entries/{entries}`` at the end).
        page_size (int):
            The maximum number of tags to return. Default
            is 10. Maximum limit is 1000.
        page_token (str):
            Pagination token that specifies the next page
            to return. If empty, the first page is returned.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTagsResponse(proto.Message):
    r"""Response message for
    [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].

    Attributes:
        tags (Sequence[google.cloud.datacatalog_v1.types.Tag]):
            [Tag][google.cloud.datacatalog.v1.Tag] details.
        next_page_token (str):
            Pagination token of the next results page.
            Empty if there are no more items in results.
    """

    @property
    def raw_page(self):
        return self

    tags = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_tags.Tag,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEntriesRequest(proto.Message):
    r"""Request message for
    [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].

    Attributes:
        parent (str):
            Required. The name of the entry group that
            contains the entries to list.
            Can be provided in URL format.
        page_size (int):
            The maximum number of items to return. Default is 10.
            Maximum limit is 1000. Throws an invalid argument if
            ``page_size`` is more than 1000.
        page_token (str):
            Pagination token that specifies the next page
            to return. If empty, the first page is returned.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to return for each entry. If empty or omitted,
            all fields are returned.

            For example, to return a list of entries with only the
            ``name`` field, set ``read_mask`` to only one path with the
            ``name`` value.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    read_mask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )


class ListEntriesResponse(proto.Message):
    r"""Response message for
    [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].

    Attributes:
        entries (Sequence[google.cloud.datacatalog_v1.types.Entry]):
            Entry details.
        next_page_token (str):
            Pagination token of the next results page.
            Empty if there are no more items in results.
    """

    @property
    def raw_page(self):
        return self

    entries = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Entry",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class StarEntryRequest(proto.Message):
    r"""Request message for
    [StarEntry][google.cloud.datacatalog.v1.DataCatalog.StarEntry].

    Attributes:
        name (str):
            Required. The name of the entry to mark as
            starred.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class StarEntryResponse(proto.Message):
    r"""Response message for
    [StarEntry][google.cloud.datacatalog.v1.DataCatalog.StarEntry].
    Empty for now

    """


class UnstarEntryRequest(proto.Message):
    r"""Request message for
    [UnstarEntry][google.cloud.datacatalog.v1.DataCatalog.UnstarEntry].

    Attributes:
        name (str):
            Required. The name of the entry to mark as **not** starred.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UnstarEntryResponse(proto.Message):
    r"""Response message for
    [UnstarEntry][google.cloud.datacatalog.v1.DataCatalog.UnstarEntry].
    Empty for now

    """


class ModifyEntryOverviewRequest(proto.Message):
    r"""Request message for
    [ModifyEntryOverview][google.cloud.datacatalog.v1.DataCatalog.ModifyEntryOverview].

    Attributes:
        name (str):
            Required. The full resource name of the
            entry.
        entry_overview (google.cloud.datacatalog_v1.types.EntryOverview):
            Required. The new value for the Entry
            Overview.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_overview = proto.Field(
        proto.MESSAGE,
        number=2,
        message="EntryOverview",
    )


class ModifyEntryContactsRequest(proto.Message):
    r"""Request message for
    [ModifyEntryContacts][google.cloud.datacatalog.v1.DataCatalog.ModifyEntryContacts].

    Attributes:
        name (str):
            Required. The full resource name of the
            entry.
        contacts (google.cloud.datacatalog_v1.types.Contacts):
            Required. The new value for the Contacts.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    contacts = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Contacts",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
