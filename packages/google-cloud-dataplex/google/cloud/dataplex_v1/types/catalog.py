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
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "EntryView",
        "TransferStatus",
        "AspectType",
        "EntryGroup",
        "EntryType",
        "Aspect",
        "AspectSource",
        "Entry",
        "EntrySource",
        "CreateEntryGroupRequest",
        "UpdateEntryGroupRequest",
        "DeleteEntryGroupRequest",
        "ListEntryGroupsRequest",
        "ListEntryGroupsResponse",
        "GetEntryGroupRequest",
        "CreateEntryTypeRequest",
        "UpdateEntryTypeRequest",
        "DeleteEntryTypeRequest",
        "ListEntryTypesRequest",
        "ListEntryTypesResponse",
        "GetEntryTypeRequest",
        "CreateAspectTypeRequest",
        "UpdateAspectTypeRequest",
        "DeleteAspectTypeRequest",
        "ListAspectTypesRequest",
        "ListAspectTypesResponse",
        "GetAspectTypeRequest",
        "CreateEntryRequest",
        "UpdateEntryRequest",
        "DeleteEntryRequest",
        "ListEntriesRequest",
        "ListEntriesResponse",
        "GetEntryRequest",
        "LookupEntryRequest",
        "SearchEntriesRequest",
        "SearchEntriesResult",
        "SearchEntriesResponse",
    },
)


class EntryView(proto.Enum):
    r"""View for controlling which parts of an entry are to be
    returned.

    Values:
        ENTRY_VIEW_UNSPECIFIED (0):
            Unspecified EntryView. Defaults to FULL.
        BASIC (1):
            Returns entry only, without aspects.
        FULL (2):
            Returns all required aspects as well as the
            keys of all non-required aspects.
        CUSTOM (3):
            Returns aspects matching custom fields in
            GetEntryRequest. If the number of aspects would
            exceed 100, the first 100 will be returned.
        ALL (4):
            Returns all aspects. If the number of aspects
            would exceed 100, the first 100 will be
            returned.
    """
    ENTRY_VIEW_UNSPECIFIED = 0
    BASIC = 1
    FULL = 2
    CUSTOM = 3
    ALL = 4


class TransferStatus(proto.Enum):
    r"""Denotes the transfer status of a resource. It is unspecified
    for resources created from Dataplex API.

    Values:
        TRANSFER_STATUS_UNSPECIFIED (0):
            The default value. It is set for resources
            that were not subject for migration from Data
            Catalog service.
        TRANSFER_STATUS_MIGRATED (1):
            Indicates that a resource was migrated from
            Data Catalog service but it hasn't been
            transferred yet. In particular the resource
            cannot be updated from Dataplex API.
        TRANSFER_STATUS_TRANSFERRED (2):
            Indicates that a resource was transferred
            from Data Catalog service. The resource can only
            be updated from Dataplex API.
    """
    TRANSFER_STATUS_UNSPECIFIED = 0
    TRANSFER_STATUS_MIGRATED = 1
    TRANSFER_STATUS_TRANSFERRED = 2


class AspectType(proto.Message):
    r"""Aspect Type is a template for creating Aspects, and
    represents the JSON-schema for a given Entry, e.g., BigQuery
    Table Schema.

    Attributes:
        name (str):
            Output only. The relative resource name of the AspectType,
            of the form:
            projects/{project_number}/locations/{location_id}/aspectTypes/{aspect_type_id}.
        uid (str):
            Output only. System generated globally unique
            ID for the AspectType. This ID will be different
            if the AspectType is deleted and re-created with
            the same name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the AspectType was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the AspectType was
            last updated.
        description (str):
            Optional. Description of the AspectType.
        display_name (str):
            Optional. User friendly display name.
        labels (MutableMapping[str, str]):
            Optional. User-defined labels for the
            AspectType.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
        authorization (google.cloud.dataplex_v1.types.AspectType.Authorization):
            Immutable. Authorization defined for this
            type.
        metadata_template (google.cloud.dataplex_v1.types.AspectType.MetadataTemplate):
            Required. MetadataTemplate of the aspect.
        transfer_status (google.cloud.dataplex_v1.types.TransferStatus):
            Output only. Denotes the transfer status of
            the Aspect Type. It is unspecified for Aspect
            Types created from Dataplex API.
    """

    class Authorization(proto.Message):
        r"""Autorization for an Aspect Type.

        Attributes:
            alternate_use_permission (str):
                Immutable. The IAM permission grantable on
                the Entry Group to allow access to instantiate
                Aspects of Dataplex owned Aspect Types, only
                settable for Dataplex owned Types.
        """

        alternate_use_permission: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class MetadataTemplate(proto.Message):
        r"""MetadataTemplate definition for AspectType

        Attributes:
            index (int):
                Optional. Index is used to encode Template
                messages. The value of index can range between 1
                and 2,147,483,647. Index must be unique within
                all fields in a Template. (Nested Templates can
                reuse indexes). Once a Template is defined, the
                index cannot be changed, because it identifies
                the field in the actual storage format. Index is
                a mandatory field, but it is optional for top
                level fields, and map/array "values"
                definitions.
            name (str):
                Required. The name of the field.
            type_ (str):
                Required. The datatype of this field. The
                following values are supported: Primitive types
                (string, integer, boolean, double, datetime);
                datetime must be of the format RFC3339 UTC
                "Zulu" (Examples:

                "2014-10-02T15:01:23Z" and
                "2014-10-02T15:01:23.045123456Z"). Complex types
                (enum, array, map, record).
            record_fields (MutableSequence[google.cloud.dataplex_v1.types.AspectType.MetadataTemplate]):
                Optional. Field definition, needs to be
                specified if the type is record. Defines the
                nested fields.
            enum_values (MutableSequence[google.cloud.dataplex_v1.types.AspectType.MetadataTemplate.EnumValue]):
                Optional. The list of values for an enum
                type. Needs to be defined if the type is enum.
            map_items (google.cloud.dataplex_v1.types.AspectType.MetadataTemplate):
                Optional. map_items needs to be set if the type is map.
                map_items can refer to a primitive field or a complex
                (record only) field. To specify a primitive field, just name
                and type needs to be set in the nested MetadataTemplate. The
                recommended value for the name field is item, as this is not
                used in the actual payload.
            array_items (google.cloud.dataplex_v1.types.AspectType.MetadataTemplate):
                Optional. array_items needs to be set if the type is array.
                array_items can refer to a primitive field or a complex
                (record only) field. To specify a primitive field, just name
                and type needs to be set in the nested MetadataTemplate. The
                recommended value for the name field is item, as this is not
                used in the actual payload.
            type_id (str):
                Optional. Id can be used if this definition
                of the field needs to be reused later. Id needs
                to be unique across the entire template. Id can
                only be specified if the field type is record.
            type_ref (str):
                Optional. A reference to another field
                definition (instead of an inline definition).
                The value must be equal to the value of an id
                field defined elsewhere in the MetadataTemplate.
                Only fields with type as record can refer to
                other fields.
            constraints (google.cloud.dataplex_v1.types.AspectType.MetadataTemplate.Constraints):
                Optional. Specifies the constraints on this
                field.
            annotations (google.cloud.dataplex_v1.types.AspectType.MetadataTemplate.Annotations):
                Optional. Specifies annotations on this
                field.
        """

        class EnumValue(proto.Message):
            r"""Definition of Enumvalue (to be used by enum fields)

            Attributes:
                index (int):
                    Required. Index for the enum. Cannot be
                    modified.
                name (str):
                    Required. Name of the enumvalue. This is the
                    actual value that the aspect will contain.
                deprecated (str):
                    Optional. Optional deprecation message to be
                    set if an enum value needs to be deprecated.
            """

            index: int = proto.Field(
                proto.INT32,
                number=1,
            )
            name: str = proto.Field(
                proto.STRING,
                number=2,
            )
            deprecated: str = proto.Field(
                proto.STRING,
                number=3,
            )

        class Constraints(proto.Message):
            r"""Definition of the constraints of a field

            Attributes:
                required (bool):
                    Optional. Marks this as an optional/required
                    field.
            """

            required: bool = proto.Field(
                proto.BOOL,
                number=1,
            )

        class Annotations(proto.Message):
            r"""Definition of the annotations of a field

            Attributes:
                deprecated (str):
                    Optional. Marks a field as deprecated, a
                    deprecation message can be included.
                display_name (str):
                    Optional. Specify a displayname for a field.
                description (str):
                    Optional. Specify a description for a field
                display_order (int):
                    Optional. Specify a display order for a
                    field. Display order can be used to reorder
                    where a field is rendered
                string_type (str):
                    Optional. String Type annotations can be used
                    to specify special meaning to string fields. The
                    following values are supported: richText:

                    The field must be interpreted as a rich text
                    field. url: A fully qualified url link.
                    resource: A service qualified resource
                    reference.
                string_values (MutableSequence[str]):
                    Optional. Suggested hints for string fields.
                    These can be used to suggest values to users,
                    through an UI for example.
            """

            deprecated: str = proto.Field(
                proto.STRING,
                number=1,
            )
            display_name: str = proto.Field(
                proto.STRING,
                number=2,
            )
            description: str = proto.Field(
                proto.STRING,
                number=3,
            )
            display_order: int = proto.Field(
                proto.INT32,
                number=4,
            )
            string_type: str = proto.Field(
                proto.STRING,
                number=6,
            )
            string_values: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=7,
            )

        index: int = proto.Field(
            proto.INT32,
            number=1,
        )
        name: str = proto.Field(
            proto.STRING,
            number=2,
        )
        type_: str = proto.Field(
            proto.STRING,
            number=5,
        )
        record_fields: MutableSequence[
            "AspectType.MetadataTemplate"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message="AspectType.MetadataTemplate",
        )
        enum_values: MutableSequence[
            "AspectType.MetadataTemplate.EnumValue"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=8,
            message="AspectType.MetadataTemplate.EnumValue",
        )
        map_items: "AspectType.MetadataTemplate" = proto.Field(
            proto.MESSAGE,
            number=10,
            message="AspectType.MetadataTemplate",
        )
        array_items: "AspectType.MetadataTemplate" = proto.Field(
            proto.MESSAGE,
            number=11,
            message="AspectType.MetadataTemplate",
        )
        type_id: str = proto.Field(
            proto.STRING,
            number=12,
        )
        type_ref: str = proto.Field(
            proto.STRING,
            number=13,
        )
        constraints: "AspectType.MetadataTemplate.Constraints" = proto.Field(
            proto.MESSAGE,
            number=50,
            message="AspectType.MetadataTemplate.Constraints",
        )
        annotations: "AspectType.MetadataTemplate.Annotations" = proto.Field(
            proto.MESSAGE,
            number=51,
            message="AspectType.MetadataTemplate.Annotations",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    authorization: Authorization = proto.Field(
        proto.MESSAGE,
        number=52,
        message=Authorization,
    )
    metadata_template: MetadataTemplate = proto.Field(
        proto.MESSAGE,
        number=53,
        message=MetadataTemplate,
    )
    transfer_status: "TransferStatus" = proto.Field(
        proto.ENUM,
        number=202,
        enum="TransferStatus",
    )


class EntryGroup(proto.Message):
    r"""An Entry Group represents a logical grouping of one or more
    Entries.

    Attributes:
        name (str):
            Output only. The relative resource name of the EntryGroup,
            of the form:
            projects/{project_number}/locations/{location_id}/entryGroups/{entry_group_id}.
        uid (str):
            Output only. System generated globally unique
            ID for the EntryGroup. This ID will be different
            if the EntryGroup is deleted and re-created with
            the same name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the EntryGroup was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the EntryGroup was
            last updated.
        description (str):
            Optional. Description of the EntryGroup.
        display_name (str):
            Optional. User friendly display name.
        labels (MutableMapping[str, str]):
            Optional. User-defined labels for the
            EntryGroup.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
        transfer_status (google.cloud.dataplex_v1.types.TransferStatus):
            Output only. Denotes the transfer status of
            the Entry Group. It is unspecified for Entry
            Group created from Dataplex API.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    transfer_status: "TransferStatus" = proto.Field(
        proto.ENUM,
        number=202,
        enum="TransferStatus",
    )


class EntryType(proto.Message):
    r"""Entry Type is a template for creating Entries.

    Attributes:
        name (str):
            Output only. The relative resource name of the EntryType, of
            the form:
            projects/{project_number}/locations/{location_id}/entryTypes/{entry_type_id}.
        uid (str):
            Output only. System generated globally unique
            ID for the EntryType. This ID will be different
            if the EntryType is deleted and re-created with
            the same name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the EntryType was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the EntryType was
            last updated.
        description (str):
            Optional. Description of the EntryType.
        display_name (str):
            Optional. User friendly display name.
        labels (MutableMapping[str, str]):
            Optional. User-defined labels for the
            EntryType.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        type_aliases (MutableSequence[str]):
            Optional. Indicates the class this Entry Type
            belongs to, for example, TABLE, DATABASE, MODEL.
        platform (str):
            Optional. The platform that Entries of this
            type belongs to.
        system (str):
            Optional. The system that Entries of this
            type belongs to. Examples include CloudSQL,
            MariaDB etc
        required_aspects (MutableSequence[google.cloud.dataplex_v1.types.EntryType.AspectInfo]):
            AspectInfo for the entry type.
        authorization (google.cloud.dataplex_v1.types.EntryType.Authorization):
            Immutable. Authorization defined for this
            type.
    """

    class AspectInfo(proto.Message):
        r"""

        Attributes:
            type_ (str):
                Required aspect type for the entry type.
        """

        type_: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class Authorization(proto.Message):
        r"""Authorization for an Entry Type.

        Attributes:
            alternate_use_permission (str):
                Immutable. The IAM permission grantable on
                the Entry Group to allow access to instantiate
                Entries of Dataplex owned Entry Types, only
                settable for Dataplex owned Types.
        """

        alternate_use_permission: str = proto.Field(
            proto.STRING,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    type_aliases: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    platform: str = proto.Field(
        proto.STRING,
        number=10,
    )
    system: str = proto.Field(
        proto.STRING,
        number=11,
    )
    required_aspects: MutableSequence[AspectInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=50,
        message=AspectInfo,
    )
    authorization: Authorization = proto.Field(
        proto.MESSAGE,
        number=51,
        message=Authorization,
    )


class Aspect(proto.Message):
    r"""An aspect is a single piece of metadata describing an entry.

    Attributes:
        aspect_type (str):
            Output only. The resource name of the type
            used to create this Aspect.
        path (str):
            Output only. The path in the entry under
            which the aspect is attached.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the Aspect was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the Aspect was
            last updated.
        data (google.protobuf.struct_pb2.Struct):
            Required. The content of the aspect, according to its aspect
            type schema. This will replace ``content``. The maximum size
            of the field is 120KB (encoded as UTF-8).
        aspect_source (google.cloud.dataplex_v1.types.AspectSource):

    """

    aspect_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    path: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    data: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=8,
        message=struct_pb2.Struct,
    )
    aspect_source: "AspectSource" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="AspectSource",
    )


class AspectSource(proto.Message):
    r"""AspectSource contains source system related information for
    the aspect.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The create time of the aspect in the source
            system.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The update time of the aspect in the source
            system.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )


class Entry(proto.Message):
    r"""An entry is a representation of a data asset which can be
    described by various metadata.

    Attributes:
        name (str):
            Identifier. The relative resource name of the Entry, of the
            form:
            projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}.
        entry_type (str):
            Required. Immutable. The resource name of the
            EntryType used to create this Entry.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the Entry was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the Entry was last
            updated.
        aspects (MutableMapping[str, google.cloud.dataplex_v1.types.Aspect]):
            Optional. The Aspects attached to the Entry.
            The format for the key can be one of the
            following:

            1. {projectId}.{locationId}.{aspectTypeId} (if
                the aspect is attached directly to the
                entry)
            2.
                {projectId}.{locationId}.{aspectTypeId}@{path}
                (if the aspect is attached to an entry's
                path)
        parent_entry (str):
            Optional. Immutable. The resource name of the
            parent entry.
        fully_qualified_name (str):
            Optional. A name for the entry that can
            reference it in an external system. The maximum
            size of the field is 4000 characters.
        entry_source (google.cloud.dataplex_v1.types.EntrySource):
            Optional. Source system related information
            for an entry.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_type: str = proto.Field(
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    aspects: MutableMapping[str, "Aspect"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=9,
        message="Aspect",
    )
    parent_entry: str = proto.Field(
        proto.STRING,
        number=10,
    )
    fully_qualified_name: str = proto.Field(
        proto.STRING,
        number=12,
    )
    entry_source: "EntrySource" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="EntrySource",
    )


class EntrySource(proto.Message):
    r"""EntrySource contains source system related information for
    the entry.

    Attributes:
        resource (str):
            The name of the resource in the source
            system. The maximum size of the field is 4000
            characters.
        system (str):
            The name of the source system.
            The maximum size of the field is 64 characters.
        platform (str):
            The platform containing the source system.
            The maximum size of the field is 64 characters.
        display_name (str):
            User friendly display name.
            The maximum size of the field is 500 characters.
        description (str):
            Description of the Entry.
            The maximum size of the field is 2000
            characters.
        labels (MutableMapping[str, str]):
            User-defined labels.
            The maximum size of keys and values is 128
            characters each.
        ancestors (MutableSequence[google.cloud.dataplex_v1.types.EntrySource.Ancestor]):
            Immutable. The ancestors of the Entry in the
            source system.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The create time of the resource in the source
            system.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The update time of the resource in the source
            system.
        location (str):
            Output only. Location of the resource in the
            source system. Entry will be searchable by this
            location. By default, this should match the
            location of the EntryGroup containing this
            entry. A different value allows capturing source
            location for data external to GCP.
    """

    class Ancestor(proto.Message):
        r"""Ancestor contains information about individual items in the
        hierarchy of an Entry.

        Attributes:
            name (str):
                Optional. The name of the ancestor resource.
            type_ (str):
                Optional. The type of the ancestor resource.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        type_: str = proto.Field(
            proto.STRING,
            number=2,
        )

    resource: str = proto.Field(
        proto.STRING,
        number=1,
    )
    system: str = proto.Field(
        proto.STRING,
        number=2,
    )
    platform: str = proto.Field(
        proto.STRING,
        number=3,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    ancestors: MutableSequence[Ancestor] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=Ancestor,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    location: str = proto.Field(
        proto.STRING,
        number=12,
    )


class CreateEntryGroupRequest(proto.Message):
    r"""Create EntryGroup Request

    Attributes:
        parent (str):
            Required. The resource name of the entryGroup, of the form:
            projects/{project_number}/locations/{location_id} where
            ``location_id`` refers to a GCP region.
        entry_group_id (str):
            Required. EntryGroup identifier.
        entry_group (google.cloud.dataplex_v1.types.EntryGroup):
            Required. EntryGroup Resource
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_group_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    entry_group: "EntryGroup" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="EntryGroup",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateEntryGroupRequest(proto.Message):
    r"""Update EntryGroup Request

    Attributes:
        entry_group (google.cloud.dataplex_v1.types.EntryGroup):
            Required. EntryGroup Resource
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    entry_group: "EntryGroup" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EntryGroup",
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


class DeleteEntryGroupRequest(proto.Message):
    r"""Delele EntryGroup Request

    Attributes:
        name (str):
            Required. The resource name of the EntryGroup:
            ``projects/{project_number}/locations/{location_id}/entryGroups/{entry_group_id}``.
        etag (str):
            Optional. If the client provided etag value
            does not match the current etag value, the
            DeleteEntryGroupRequest method returns an
            ABORTED error response
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEntryGroupsRequest(proto.Message):
    r"""List entryGroups request.

    Attributes:
        parent (str):
            Required. The resource name of the entryGroup location, of
            the form:
            ``projects/{project_number}/locations/{location_id}`` where
            ``location_id`` refers to a GCP region.
        page_size (int):
            Optional. Maximum number of EntryGroups to
            return. The service may return fewer than this
            value. If unspecified, at most 10 EntryGroups
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListEntryGroups`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListEntryGroups`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter request.
        order_by (str):
            Optional. Order by fields for the result.
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


class ListEntryGroupsResponse(proto.Message):
    r"""List ListEntryGroups response.

    Attributes:
        entry_groups (MutableSequence[google.cloud.dataplex_v1.types.EntryGroup]):
            ListEntryGroups under the given parent
            location.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable_locations (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    entry_groups: MutableSequence["EntryGroup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EntryGroup",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetEntryGroupRequest(proto.Message):
    r"""Get EntryGroup request.

    Attributes:
        name (str):
            Required. The resource name of the EntryGroup:
            ``projects/{project_number}/locations/{location_id}/entryGroups/{entry_group_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateEntryTypeRequest(proto.Message):
    r"""Create EntryType Request

    Attributes:
        parent (str):
            Required. The resource name of the EntryType, of the form:
            projects/{project_number}/locations/{location_id} where
            ``location_id`` refers to a GCP region.
        entry_type_id (str):
            Required. EntryType identifier.
        entry_type (google.cloud.dataplex_v1.types.EntryType):
            Required. EntryType Resource
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_type_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    entry_type: "EntryType" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="EntryType",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateEntryTypeRequest(proto.Message):
    r"""Update EntryType Request

    Attributes:
        entry_type (google.cloud.dataplex_v1.types.EntryType):
            Required. EntryType Resource
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    entry_type: "EntryType" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EntryType",
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


class DeleteEntryTypeRequest(proto.Message):
    r"""Delele EntryType Request

    Attributes:
        name (str):
            Required. The resource name of the EntryType:
            ``projects/{project_number}/locations/{location_id}/entryTypes/{entry_type_id}``.
        etag (str):
            Optional. If the client provided etag value
            does not match the current etag value, the
            DeleteEntryTypeRequest method returns an ABORTED
            error response
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListEntryTypesRequest(proto.Message):
    r"""List EntryTypes request

    Attributes:
        parent (str):
            Required. The resource name of the EntryType location, of
            the form:
            ``projects/{project_number}/locations/{location_id}`` where
            ``location_id`` refers to a GCP region.
        page_size (int):
            Optional. Maximum number of EntryTypes to
            return. The service may return fewer than this
            value. If unspecified, at most 10 EntryTypes
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListEntryTypes`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListEntryTypes`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter request. Filters are
            case-sensitive. The following formats are
            supported:

            labels.key1 = "value1"
            labels:key1
            name = "value"
            These restrictions can be coinjoined with AND,
            OR and NOT conjunctions.
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


class ListEntryTypesResponse(proto.Message):
    r"""List EntryTypes response

    Attributes:
        entry_types (MutableSequence[google.cloud.dataplex_v1.types.EntryType]):
            ListEntryTypes under the given parent
            location.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable_locations (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    entry_types: MutableSequence["EntryType"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EntryType",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetEntryTypeRequest(proto.Message):
    r"""Get EntryType request

    Attributes:
        name (str):
            Required. The resource name of the EntryType:
            ``projects/{project_number}/locations/{location_id}/entryTypes/{entry_type_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateAspectTypeRequest(proto.Message):
    r"""Create AspectType Request

    Attributes:
        parent (str):
            Required. The resource name of the AspectType, of the form:
            projects/{project_number}/locations/{location_id} where
            ``location_id`` refers to a GCP region.
        aspect_type_id (str):
            Required. AspectType identifier.
        aspect_type (google.cloud.dataplex_v1.types.AspectType):
            Required. AspectType Resource
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    aspect_type_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    aspect_type: "AspectType" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AspectType",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateAspectTypeRequest(proto.Message):
    r"""Update AspectType Request

    Attributes:
        aspect_type (google.cloud.dataplex_v1.types.AspectType):
            Required. AspectType Resource
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    aspect_type: "AspectType" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="AspectType",
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


class DeleteAspectTypeRequest(proto.Message):
    r"""Delele AspectType Request

    Attributes:
        name (str):
            Required. The resource name of the AspectType:
            ``projects/{project_number}/locations/{location_id}/aspectTypes/{aspect_type_id}``.
        etag (str):
            Optional. If the client provided etag value
            does not match the current etag value, the
            DeleteAspectTypeRequest method returns an
            ABORTED error response
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListAspectTypesRequest(proto.Message):
    r"""List AspectTypes request

    Attributes:
        parent (str):
            Required. The resource name of the AspectType location, of
            the form:
            ``projects/{project_number}/locations/{location_id}`` where
            ``location_id`` refers to a GCP region.
        page_size (int):
            Optional. Maximum number of AspectTypes to
            return. The service may return fewer than this
            value. If unspecified, at most 10 AspectTypes
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListAspectTypes`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListAspectTypes`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter request. Filters are
            case-sensitive. The following formats are
            supported:

            labels.key1 = "value1"
            labels:key1
            name = "value"
            These restrictions can be coinjoined with AND,
            OR and NOT conjunctions.
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


class ListAspectTypesResponse(proto.Message):
    r"""List AspectTypes response

    Attributes:
        aspect_types (MutableSequence[google.cloud.dataplex_v1.types.AspectType]):
            ListAspectTypes under the given parent
            location.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable_locations (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    aspect_types: MutableSequence["AspectType"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AspectType",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetAspectTypeRequest(proto.Message):
    r"""Get AspectType request

    Attributes:
        name (str):
            Required. The resource name of the AspectType:
            ``projects/{project_number}/locations/{location_id}/aspectTypes/{aspect_type_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateEntryRequest(proto.Message):
    r"""

    Attributes:
        parent (str):
            Required. The resource name of the parent Entry Group:
            ``projects/{project}/locations/{location}/entryGroups/{entry_group}``.
        entry_id (str):
            Required. Entry identifier. It has to be unique within an
            Entry Group.

            Entries corresponding to Google Cloud resources use Entry ID
            format based on Full Resource Names
            (https://cloud.google.com/apis/design/resource_names#full_resource_name).
            The format is a Full Resource Name of the resource without
            the prefix double slashes in the API Service Name part of
            Full Resource Name. This allows retrieval of entries using
            their associated resource name.

            For example if the Full Resource Name of a resource is
            ``//library.googleapis.com/shelves/shelf1/books/book2``,
            then the suggested entry_id is
            ``library.googleapis.com/shelves/shelf1/books/book2``.

            It is also suggested to follow the same convention for
            entries corresponding to resources from other providers or
            systems than Google Cloud.

            The maximum size of the field is 4000 characters.
        entry (google.cloud.dataplex_v1.types.Entry):
            Required. Entry resource.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    entry_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    entry: "Entry" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Entry",
    )


class UpdateEntryRequest(proto.Message):
    r"""

    Attributes:
        entry (google.cloud.dataplex_v1.types.Entry):
            Required. Entry resource.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Mask of fields to update. To update Aspects, the
            update_mask must contain the value "aspects".

            If the update_mask is empty, all modifiable fields present
            in the request will be updated.
        allow_missing (bool):
            Optional. If set to true and the entry does
            not exist, it will be created.
        delete_missing_aspects (bool):
            Optional. If set to true and the aspect_keys specify aspect
            ranges, any existing aspects from that range not provided in
            the request will be deleted.
        aspect_keys (MutableSequence[str]):
            Optional. The map keys of the Aspects which should be
            modified. Supports the following syntaxes:

            -  <aspect_type_reference> - matches aspect on given type
               and empty path
            -  <aspect_type_reference>@path - matches aspect on given
               type and specified path
            -  <aspect_type_reference>\* - matches aspects on given type
               for all paths
            -  \*@path - matches aspects of all types on the given path

            Existing aspects matching the syntax will not be removed
            unless ``delete_missing_aspects`` is set to true.

            If this field is left empty, it will be treated as
            specifying exactly those Aspects present in the request.
    """

    entry: "Entry" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Entry",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    delete_missing_aspects: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    aspect_keys: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class DeleteEntryRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The resource name of the Entry:
            ``projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListEntriesRequest(proto.Message):
    r"""

    Attributes:
        parent (str):
            Required. The resource name of the parent Entry Group:
            ``projects/{project}/locations/{location}/entryGroups/{entry_group}``.
        page_size (int):

        page_token (str):
            Optional. The pagination token returned by a
            previous request.
        filter (str):
            Optional. A filter on the entries to return. Filters are
            case-sensitive. The request can be filtered by the following
            fields: entry_type, entry_source.display_name. The
            comparison operators are =, !=, <, >, <=, >= (strings are
            compared according to lexical order) The logical operators
            AND, OR, NOT can be used in the filter. Wildcard "*" can be
            used, but for entry_type the full project id or number needs
            to be provided. Example filter expressions:
            "entry_source.display_name=AnExampleDisplayName"
            "entry_type=projects/example-project/locations/global/entryTypes/example-entry_type"
            `entry_type=projects/example-project/locations/us/entryTypes/a*
            OR entry_type=projects/another-project/locations/*` "NOT
            entry_source.display_name=AnotherExampleDisplayName".
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


class ListEntriesResponse(proto.Message):
    r"""

    Attributes:
        entries (MutableSequence[google.cloud.dataplex_v1.types.Entry]):
            The list of entries.
        next_page_token (str):
            Pagination token.
    """

    @property
    def raw_page(self):
        return self

    entries: MutableSequence["Entry"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Entry",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEntryRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The resource name of the Entry:
            ``projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}``.
        view (google.cloud.dataplex_v1.types.EntryView):
            Optional. View for controlling which parts of
            an entry are to be returned.
        aspect_types (MutableSequence[str]):
            Optional. Limits the aspects returned to the
            provided aspect types. Only works if the CUSTOM
            view is selected.
        paths (MutableSequence[str]):
            Optional. Limits the aspects returned to
            those associated with the provided paths within
            the Entry. Only works if the CUSTOM view is
            selected.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "EntryView" = proto.Field(
        proto.ENUM,
        number=2,
        enum="EntryView",
    )
    aspect_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    paths: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class LookupEntryRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The project to which the request should be
            attributed in the following form:
            ``projects/{project}/locations/{location}``.
        view (google.cloud.dataplex_v1.types.EntryView):
            Optional. View for controlling which parts of
            an entry are to be returned.
        aspect_types (MutableSequence[str]):
            Optional. Limits the aspects returned to the
            provided aspect types. Only works if the CUSTOM
            view is selected.
        paths (MutableSequence[str]):
            Optional. Limits the aspects returned to
            those associated with the provided paths within
            the Entry. Only works if the CUSTOM view is
            selected.
        entry (str):
            Required. The resource name of the Entry:
            ``projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "EntryView" = proto.Field(
        proto.ENUM,
        number=2,
        enum="EntryView",
    )
    aspect_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    paths: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    entry: str = proto.Field(
        proto.STRING,
        number=5,
    )


class SearchEntriesRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The project to which the request should be
            attributed in the following form:
            ``projects/{project}/locations/{location}``.
        query (str):
            Required. The query against which entries in
            scope should be matched.
        page_size (int):
            Optional. Pagination.
        page_token (str):

        order_by (str):
            Optional. Ordering of the results. Supported
            options to be added later.
        scope (str):
            Optional. The scope under which the search should be
            operating. Should either be organizations/<org_id> or
            projects/<project_ref>. If left unspecified, it will default
            to the organization where the project provided in ``name``
            is located.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    scope: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SearchEntriesResult(proto.Message):
    r"""A single result of a SearchEntries request.

    Attributes:
        linked_resource (str):
            Linked resource name.
        dataplex_entry (google.cloud.dataplex_v1.types.Entry):

        snippets (google.cloud.dataplex_v1.types.SearchEntriesResult.Snippets):
            Snippets.
    """

    class Snippets(proto.Message):
        r"""Snippets for the entry, contains HTML-style highlighting for
        matched tokens, will be used in UI.

        Attributes:
            dataplex_entry (google.cloud.dataplex_v1.types.Entry):
                Entry
        """

        dataplex_entry: "Entry" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Entry",
        )

    linked_resource: str = proto.Field(
        proto.STRING,
        number=8,
    )
    dataplex_entry: "Entry" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="Entry",
    )
    snippets: Snippets = proto.Field(
        proto.MESSAGE,
        number=12,
        message=Snippets,
    )


class SearchEntriesResponse(proto.Message):
    r"""

    Attributes:
        results (MutableSequence[google.cloud.dataplex_v1.types.SearchEntriesResult]):
            The results matching the search query.
        total_size (int):
            The estimated total number of matching
            entries. Not guaranteed to be accurate.
        next_page_token (str):
            Pagination token.
        unreachable (MutableSequence[str]):
            Unreachable locations. Search results don't
            include data from those locations.
    """

    @property
    def raw_page(self):
        return self

    results: MutableSequence["SearchEntriesResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SearchEntriesResult",
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
