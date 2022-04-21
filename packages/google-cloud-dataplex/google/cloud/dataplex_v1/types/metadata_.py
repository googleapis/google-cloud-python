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
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "StorageSystem",
        "CreateEntityRequest",
        "UpdateEntityRequest",
        "DeleteEntityRequest",
        "ListEntitiesRequest",
        "ListEntitiesResponse",
        "GetEntityRequest",
        "ListPartitionsRequest",
        "CreatePartitionRequest",
        "DeletePartitionRequest",
        "ListPartitionsResponse",
        "GetPartitionRequest",
        "Entity",
        "Partition",
        "Schema",
        "StorageFormat",
    },
)


class StorageSystem(proto.Enum):
    r"""Identifies the cloud system that manages the data storage."""
    STORAGE_SYSTEM_UNSPECIFIED = 0
    CLOUD_STORAGE = 1
    BIGQUERY = 2


class CreateEntityRequest(proto.Message):
    r"""Create a metadata entity request.

    Attributes:
        parent (str):
            Required. The resource name of the parent zone:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}``.
        entity (google.cloud.dataplex_v1.types.Entity):
            Required. Entity resource.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    entity = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Entity",
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateEntityRequest(proto.Message):
    r"""Update a metadata entity request.
    The exiting entity will be fully replaced by the entity in the
    request. The entity ID is mutable. To modify the ID, use the
    current entity ID in the request URL and specify the new ID in
    the request body.

    Attributes:
        entity (google.cloud.dataplex_v1.types.Entity):
            Required. Update description.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    entity = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Entity",
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteEntityRequest(proto.Message):
    r"""Delete a metadata entity request.

    Attributes:
        name (str):
            Required. The resource name of the entity:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.
        etag (str):
            Required. The etag associated with the
            partition if it was previously retrieved.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    etag = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEntitiesRequest(proto.Message):
    r"""List metadata entities request.

    Attributes:
        parent (str):
            Required. The resource name of the parent zone:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}``.
        view (google.cloud.dataplex_v1.types.ListEntitiesRequest.EntityView):
            Required. Specify the entity view to make a
            partial list request.
        page_size (int):
            Optional. Maximum number of entities to
            return. The service may return fewer than this
            value. If unspecified, 100 entities will be
            returned by default. The maximum value is 500;
            larger values will will be truncated to 500.
        page_token (str):
            Optional. Page token received from a previous
            ``ListEntities`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListEntities`` must match the call that
            provided the page token.
        filter (str):
            Optional. The following filter parameters can be added to
            the URL to limit the entities returned by the API:

            -  Entity ID: ?filter="id=entityID"
            -  Asset ID: ?filter="asset=assetID"
            -  Data path ?filter="data_path=gs://my-bucket"
            -  Is HIVE compatible: ?filter=”hive_compatible=true”
            -  Is BigQuery compatible:
               ?filter=”bigquery_compatible=true”
    """

    class EntityView(proto.Enum):
        r"""Entity views."""
        ENTITY_VIEW_UNSPECIFIED = 0
        TABLES = 1
        FILESETS = 2

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    view = proto.Field(
        proto.ENUM,
        number=2,
        enum=EntityView,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token = proto.Field(
        proto.STRING,
        number=4,
    )
    filter = proto.Field(
        proto.STRING,
        number=5,
    )


class ListEntitiesResponse(proto.Message):
    r"""List metadata entities response.

    Attributes:
        entities (Sequence[google.cloud.dataplex_v1.types.Entity]):
            Entities in the specified parent zone.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no remaining results in
            the list.
    """

    @property
    def raw_page(self):
        return self

    entities = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Entity",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEntityRequest(proto.Message):
    r"""Get metadata entity request.

    Attributes:
        name (str):
            Required. The resource name of the entity:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}.``
        view (google.cloud.dataplex_v1.types.GetEntityRequest.EntityView):
            Optional. Used to select the subset of entity information to
            return. Defaults to ``BASIC``.
    """

    class EntityView(proto.Enum):
        r"""Entity views for get entity partial result."""
        ENTITY_VIEW_UNSPECIFIED = 0
        BASIC = 1
        SCHEMA = 2
        FULL = 4

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    view = proto.Field(
        proto.ENUM,
        number=2,
        enum=EntityView,
    )


class ListPartitionsRequest(proto.Message):
    r"""List metadata partitions request.

    Attributes:
        parent (str):
            Required. The resource name of the parent entity:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.
        page_size (int):
            Optional. Maximum number of partitions to
            return. The service may return fewer than this
            value. If unspecified, 100 partitions will be
            returned by default. The maximum page size is
            500; larger values will will be truncated to
            500.
        page_token (str):
            Optional. Page token received from a previous
            ``ListPartitions`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListPartitions`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter the partitions returned to the caller using
            a key vslue pair expression. The filter expression supports:

            -  logical operators: AND, OR
            -  comparison operators: <, >, >=, <= ,=, !=
            -  LIKE operators:

               -  The right hand of a LIKE operator supports “.” and “*”
                  for wildcard searches, for example "value1 LIKE
                  ".*oo.*"

            -  parenthetical grouping: ( )

            Sample filter expression: \`?filter="key1 < value1 OR key2 >
            value2"

            **Notes:**

            -  Keys to the left of operators are case insensitive.
            -  Partition results are sorted first by creation time, then
               by lexicographic order.
            -  Up to 20 key value filter pairs are allowed, but due to
               performance considerations, only the first 10 will be
               used as a filter.
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
    filter = proto.Field(
        proto.STRING,
        number=4,
    )


class CreatePartitionRequest(proto.Message):
    r"""Create metadata partition request.

    Attributes:
        parent (str):
            Required. The resource name of the parent zone:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.
        partition (google.cloud.dataplex_v1.types.Partition):
            Required. Partition resource.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    partition = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Partition",
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeletePartitionRequest(proto.Message):
    r"""Delete metadata partition request.

    Attributes:
        name (str):
            Required. The resource name of the partition. format:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}/partitions/{partition_value_path}``.
            The {partition_value_path} segment consists of an ordered
            sequence of partition values separated by "/". All values
            must be provided.
        etag (str):
            Optional. The etag associated with the
            partition if it was previously retrieved.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    etag = proto.Field(
        proto.STRING,
        number=2,
    )


class ListPartitionsResponse(proto.Message):
    r"""List metadata partitions response.

    Attributes:
        partitions (Sequence[google.cloud.dataplex_v1.types.Partition]):
            Partitions under the specified parent entity.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no remaining results in
            the list.
    """

    @property
    def raw_page(self):
        return self

    partitions = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Partition",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPartitionRequest(proto.Message):
    r"""Get metadata partition request.

    Attributes:
        name (str):
            Required. The resource name of the partition:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}/partitions/{partition_value_path}``.
            The {partition_value_path} segment consists of an ordered
            sequence of partition values separated by "/". All values
            must be provided.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class Entity(proto.Message):
    r"""Represents tables and fileset metadata contained within a
    zone.

    Attributes:
        name (str):
            Output only. The resource name of the entity, of the form:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{id}``.
        display_name (str):
            Optional. Display name must be shorter than
            or equal to 63 characters.
        description (str):
            Optional. User friendly longer description
            text. Must be shorter than or equal to 1024
            characters.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the entity was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the entity was
            last updated.
        id (str):
            Required. A user-provided entity ID. It is
            mutable, and will be used as the published table
            name. Specifying a new ID in an update entity
            request will override the existing value.
            The ID must contain only letters (a-z, A-Z),
            numbers (0-9), and underscores. Must begin with
            a letter.
        etag (str):
            Optional. The etag for this entity. Required
            for update and delete requests. Must match the
            server's etag.
        type_ (google.cloud.dataplex_v1.types.Entity.Type):
            Required. Immutable. The type of entity.
        asset (str):
            Required. Immutable. The ID of the asset
            associated with the storage location containing
            the entity data. The entity must be with in the
            same zone with the asset.
        data_path (str):
            Required. Immutable. The storage path of the entity data.
            For Cloud Storage data, this is the fully-qualified path to
            the entity, such as ``gs://bucket/path/to/data``. For
            BigQuery data, this is the name of the table resource, such
            as
            ``projects/project_id/datasets/dataset_id/tables/table_id``.
        data_path_pattern (str):
            Optional. The set of items within the data path constituting
            the data in the entity, represented as a glob path. Example:
            ``gs://bucket/path/to/data/**/*.csv``.
        catalog_entry (str):
            Output only. The name of the associated Data
            Catalog entry.
        system (google.cloud.dataplex_v1.types.StorageSystem):
            Required. Immutable. Identifies the storage
            system of the entity data.
        format_ (google.cloud.dataplex_v1.types.StorageFormat):
            Required. Identifies the storage format of
            the entity data. It does not apply to entities
            with data stored in BigQuery.
        compatibility (google.cloud.dataplex_v1.types.Entity.CompatibilityStatus):
            Output only. Metadata stores that the entity
            is compatible with.
        schema (google.cloud.dataplex_v1.types.Schema):
            Required. The description of the data structure and layout.
            The schema is not included in list responses. It is only
            included in ``SCHEMA`` and ``FULL`` entity views of a
            ``GetEntity`` response.
    """

    class Type(proto.Enum):
        r"""The type of entity."""
        TYPE_UNSPECIFIED = 0
        TABLE = 1
        FILESET = 2

    class CompatibilityStatus(proto.Message):
        r"""Provides compatibility information for various metadata
        stores.

        Attributes:
            hive_metastore (google.cloud.dataplex_v1.types.Entity.CompatibilityStatus.Compatibility):
                Output only. Whether this entity is
                compatible with Hive Metastore.
            bigquery (google.cloud.dataplex_v1.types.Entity.CompatibilityStatus.Compatibility):
                Output only. Whether this entity is
                compatible with BigQuery.
        """

        class Compatibility(proto.Message):
            r"""Provides compatibility information for a specific metadata
            store.

            Attributes:
                compatible (bool):
                    Output only. Whether the entity is compatible
                    and can be represented in the metadata store.
                reason (str):
                    Output only. Provides additional detail if
                    the entity is incompatible with the metadata
                    store.
            """

            compatible = proto.Field(
                proto.BOOL,
                number=1,
            )
            reason = proto.Field(
                proto.STRING,
                number=2,
            )

        hive_metastore = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Entity.CompatibilityStatus.Compatibility",
        )
        bigquery = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Entity.CompatibilityStatus.Compatibility",
        )

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
    id = proto.Field(
        proto.STRING,
        number=7,
    )
    etag = proto.Field(
        proto.STRING,
        number=8,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=10,
        enum=Type,
    )
    asset = proto.Field(
        proto.STRING,
        number=11,
    )
    data_path = proto.Field(
        proto.STRING,
        number=12,
    )
    data_path_pattern = proto.Field(
        proto.STRING,
        number=13,
    )
    catalog_entry = proto.Field(
        proto.STRING,
        number=14,
    )
    system = proto.Field(
        proto.ENUM,
        number=15,
        enum="StorageSystem",
    )
    format_ = proto.Field(
        proto.MESSAGE,
        number=16,
        message="StorageFormat",
    )
    compatibility = proto.Field(
        proto.MESSAGE,
        number=19,
        message=CompatibilityStatus,
    )
    schema = proto.Field(
        proto.MESSAGE,
        number=50,
        message="Schema",
    )


class Partition(proto.Message):
    r"""Represents partition metadata contained within entity
    instances.

    Attributes:
        name (str):
            Output only. The values must be HTML URL
            encoded two times before constructing the path.
            For example, if you have a value of "US:CA",
            encoded it two times and you get "US%253ACA".
            Then if you have the 2nd value is
            "CA#Sunnyvale", encoded two times and you get
            "CA%2523Sunnyvale". The partition values path is
            "US%253ACA/CA%2523Sunnyvale". The final URL will
            be
            "https://.../partitions/US%253ACA/CA%2523Sunnyvale".
            The name field in the responses will always have
            the encoded format.
        values (Sequence[str]):
            Required. Immutable. The set of values
            representing the partition, which correspond to
            the partition schema defined in the parent
            entity.
        location (str):
            Required. Immutable. The location of the entity data within
            the partition, for example,
            ``gs://bucket/path/to/entity/key1=value1/key2=value2``. Or
            ``projects/<project_id>/datasets/<dataset_id>/tables/<table_id>``
        etag (str):
            Optional. The etag for this partition.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    values = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    location = proto.Field(
        proto.STRING,
        number=3,
    )
    etag = proto.Field(
        proto.STRING,
        number=4,
    )


class Schema(proto.Message):
    r"""Schema information describing the structure and layout of the
    data.

    Attributes:
        user_managed (bool):
            Required. Whether the schema is user-managed or managed by
            the service.

            -  Set user_manage to false if you would like Dataplex to
               help you manage the schema. You will get the full service
               provided by Dataplex discovery, including new data
               discovery, schema inference and schema evolution. You can
               still provide input the schema of the entities, for
               example renaming a schema field, changing CSV or Json
               options if you think the discovered values are not as
               accurate. Dataplex will consider your input as the
               initial schema (as if they were produced by the previous
               discovery run), and will evolve schema or flag actions
               based on that.
            -  Set user_manage to true if you would like to fully manage
               the entity schema by yourself. This is useful when you
               would like to manually specify the schema for a table. In
               this case, the schema defined by the user is guaranteed
               to be kept unchanged and would not be overwritten. But
               this also means Dataplex will not provide schema
               evolution management for you. Dataplex will still be able
               to manage partition registration (i.e., keeping the list
               of partitions up to date) when Dataplex discovery is
               turned on and user_managed is set to true.
        fields (Sequence[google.cloud.dataplex_v1.types.Schema.SchemaField]):
            Optional. The sequence of fields describing
            data in table entities.
        partition_fields (Sequence[google.cloud.dataplex_v1.types.Schema.PartitionField]):
            Optional. The sequence of fields describing
            the partition structure in entities. If this
            field is empty, there are no partitions within
            the data.
        partition_style (google.cloud.dataplex_v1.types.Schema.PartitionStyle):
            Optional. The structure of paths containing
            partition data within the entity.
    """

    class Type(proto.Enum):
        r"""Type information for fields in schemas and partition schemas."""
        TYPE_UNSPECIFIED = 0
        BOOLEAN = 1
        BYTE = 2
        INT16 = 3
        INT32 = 4
        INT64 = 5
        FLOAT = 6
        DOUBLE = 7
        DECIMAL = 8
        STRING = 9
        BINARY = 10
        TIMESTAMP = 11
        DATE = 12
        TIME = 13
        RECORD = 14
        NULL = 100

    class Mode(proto.Enum):
        r"""Additional qualifiers to define field semantics."""
        MODE_UNSPECIFIED = 0
        REQUIRED = 1
        NULLABLE = 2
        REPEATED = 3

    class PartitionStyle(proto.Enum):
        r"""The structure of paths within the entity, which represent
        partitions.
        """
        PARTITION_STYLE_UNSPECIFIED = 0
        HIVE_COMPATIBLE = 1

    class SchemaField(proto.Message):
        r"""Represents a column field within a table schema.

        Attributes:
            name (str):
                Required. The name of the field. The maximum length is 767
                characters. The name must begins with a letter and not
                contains ``:`` and ``.``.
            description (str):
                Optional. User friendly field description.
                Must be less than or equal to 1024 characters.
            type_ (google.cloud.dataplex_v1.types.Schema.Type):
                Required. The type of field.
            mode (google.cloud.dataplex_v1.types.Schema.Mode):
                Required. Additional field semantics.
            fields (Sequence[google.cloud.dataplex_v1.types.Schema.SchemaField]):
                Optional. Any nested field for complex types.
        """

        name = proto.Field(
            proto.STRING,
            number=1,
        )
        description = proto.Field(
            proto.STRING,
            number=2,
        )
        type_ = proto.Field(
            proto.ENUM,
            number=3,
            enum="Schema.Type",
        )
        mode = proto.Field(
            proto.ENUM,
            number=4,
            enum="Schema.Mode",
        )
        fields = proto.RepeatedField(
            proto.MESSAGE,
            number=10,
            message="Schema.SchemaField",
        )

    class PartitionField(proto.Message):
        r"""Represents a key field within the entity's partition
        structure. You could have up to 20 partition fields, but only
        the first 10 partitions have the filtering ability due to
        performance consideration.

        Attributes:
            name (str):
                Required. Partition name is editable if only
                the partition style is not HIVE compatible. The
                maximum length allowed is 767 characters.
            type_ (google.cloud.dataplex_v1.types.Schema.Type):
                Required. Immutable. The type of field.
        """

        name = proto.Field(
            proto.STRING,
            number=1,
        )
        type_ = proto.Field(
            proto.ENUM,
            number=2,
            enum="Schema.Type",
        )

    user_managed = proto.Field(
        proto.BOOL,
        number=1,
    )
    fields = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=SchemaField,
    )
    partition_fields = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=PartitionField,
    )
    partition_style = proto.Field(
        proto.ENUM,
        number=4,
        enum=PartitionStyle,
    )


class StorageFormat(proto.Message):
    r"""Describes the format of the data within its storage location.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        format_ (google.cloud.dataplex_v1.types.StorageFormat.Format):
            Output only. The data format associated with
            the stored data, which represents content type
            values. The value is inferred from mime type.
        compression_format (google.cloud.dataplex_v1.types.StorageFormat.CompressionFormat):
            Optional. The compression type associated
            with the stored data. If unspecified, the data
            is uncompressed.
        mime_type (str):
            Required. The mime type descriptor for the
            data. Must match the pattern {type}/{subtype}.
            Supported values: - application/x-parquet
            - application/x-avro
            - application/x-orc
            - application/x-tfrecord
            - application/json
            - application/{subtypes}
            - text/csv
            - text/<subtypes>
            - image/{image subtype}
            - video/{video subtype}
            - audio/{audio subtype}
        csv (google.cloud.dataplex_v1.types.StorageFormat.CsvOptions):
            Optional. Additional information about CSV
            formatted data.

            This field is a member of `oneof`_ ``options``.
        json (google.cloud.dataplex_v1.types.StorageFormat.JsonOptions):
            Optional. Additional information about CSV
            formatted data.

            This field is a member of `oneof`_ ``options``.
    """

    class Format(proto.Enum):
        r"""The specific file format of the data."""
        FORMAT_UNSPECIFIED = 0
        PARQUET = 1
        AVRO = 2
        ORC = 3
        CSV = 100
        JSON = 101
        IMAGE = 200
        AUDIO = 201
        VIDEO = 202
        TEXT = 203
        TFRECORD = 204
        OTHER = 1000
        UNKNOWN = 1001

    class CompressionFormat(proto.Enum):
        r"""The specific compressed file format of the data."""
        COMPRESSION_FORMAT_UNSPECIFIED = 0
        GZIP = 2
        BZIP2 = 3

    class CsvOptions(proto.Message):
        r"""Describes CSV and similar semi-structured data formats.

        Attributes:
            encoding (str):
                Optional. The character encoding of the data.
                Accepts "US-ASCII", "UTF-8", and "ISO-8859-1".
                Defaults to UTF-8 if unspecified.
            header_rows (int):
                Optional. The number of rows to interpret as
                header rows that should be skipped when reading
                data rows. Defaults to 0.
            delimiter (str):
                Optional. The delimiter used to separate
                values. Defaults to ','.
            quote (str):
                Optional. The character used to quote column
                values. Accepts '"' and '''. Defaults to '"' if
                unspecified.
        """

        encoding = proto.Field(
            proto.STRING,
            number=1,
        )
        header_rows = proto.Field(
            proto.INT32,
            number=2,
        )
        delimiter = proto.Field(
            proto.STRING,
            number=3,
        )
        quote = proto.Field(
            proto.STRING,
            number=4,
        )

    class JsonOptions(proto.Message):
        r"""Describes JSON data format.

        Attributes:
            encoding (str):
                Optional. The character encoding of the data.
                Accepts "US-ASCII", "UTF-8" and "ISO-8859-1".
                Defaults to UTF-8 if not specified.
        """

        encoding = proto.Field(
            proto.STRING,
            number=1,
        )

    format_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=Format,
    )
    compression_format = proto.Field(
        proto.ENUM,
        number=2,
        enum=CompressionFormat,
    )
    mime_type = proto.Field(
        proto.STRING,
        number=3,
    )
    csv = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="options",
        message=CsvOptions,
    )
    json = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="options",
        message=JsonOptions,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
