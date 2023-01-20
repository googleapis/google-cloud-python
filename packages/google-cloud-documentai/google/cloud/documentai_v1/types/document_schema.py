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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1",
    manifest={
        "DocumentSchema",
    },
)


class DocumentSchema(proto.Message):
    r"""The schema defines the output of the processed document by a
    processor.

    Attributes:
        display_name (str):
            Display name to show to users.
        description (str):
            Description of the schema.
        entity_types (MutableSequence[google.cloud.documentai_v1.types.DocumentSchema.EntityType]):
            Entity types of the schema.
        metadata (google.cloud.documentai_v1.types.DocumentSchema.Metadata):
            Metadata of the schema.
    """

    class EntityType(proto.Message):
        r"""EntityType is the wrapper of a label of the corresponding
        model with detailed attributes and limitations for entity-based
        processors. Multiple types can also compose a dependency tree to
        represent nested types.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            enum_values (google.cloud.documentai_v1.types.DocumentSchema.EntityType.EnumValues):
                If specified, lists all the possible values for this entity.
                This should not be more than a handful of values. If the
                number of values is >10 or could change frequently use the
                ``EntityType.value_ontology`` field and specify a list of
                all possible values in a value ontology file.

                This field is a member of `oneof`_ ``value_source``.
            display_name (str):
                User defined name for the type.
            name (str):
                Name of the type. It must be unique within the schema file
                and cannot be a 'Common Type'. Besides that we use the
                following naming conventions:

                -  *use ``snake_casing``*
                -  name matching is case-sensitive
                -  Maximum 64 characters.
                -  Must start with a letter.
                -  Allowed characters: ASCII letters ``[a-z0-9_-]``. (For
                   backward compatibility internal infrastructure and
                   tooling can handle any ascii character)
                -  The ``/`` is sometimes used to denote a property of a
                   type. For example ``line_item/amount``. This convention
                   is deprecated, but will still be honored for backward
                   compatibility.
            base_types (MutableSequence[str]):
                The entity type that this type is derived
                from.  For now, one and only one should be set.
            properties (MutableSequence[google.cloud.documentai_v1.types.DocumentSchema.EntityType.Property]):
                Describing the nested structure, or
                composition of an entity.
        """

        class EnumValues(proto.Message):
            r"""Defines the a list of enum values.

            Attributes:
                values (MutableSequence[str]):
                    The individual values that this enum values
                    type can include.
            """

            values: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )

        class Property(proto.Message):
            r"""Defines properties that can be part of the entity type.

            Attributes:
                name (str):
                    The name of the property.  Follows the same
                    guidelines as the EntityType name.
                value_type (str):
                    A reference to the value type of the property. This type is
                    subject to the same conventions as the ``Entity.base_types``
                    field.
                occurrence_type (google.cloud.documentai_v1.types.DocumentSchema.EntityType.Property.OccurrenceType):
                    Occurrence type limits the number of
                    instances an entity type appears in the
                    document.
            """

            class OccurrenceType(proto.Enum):
                r"""Types of occurrences of the entity type in the document.
                Note: this represents the number of instances of an entity
                types, not number of mentions of a given entity instance.

                Values:
                    OCCURRENCE_TYPE_UNSPECIFIED (0):
                        Unspecified occurrence type.
                    OPTIONAL_ONCE (1):
                        There will be zero or one instance of this
                        entity type.
                    OPTIONAL_MULTIPLE (2):
                        The entity type will appear zero or multiple
                        times.
                    REQUIRED_ONCE (3):
                        The entity type will only appear exactly
                        once.
                    REQUIRED_MULTIPLE (4):
                        The entity type will appear once or more
                        times.
                """
                OCCURRENCE_TYPE_UNSPECIFIED = 0
                OPTIONAL_ONCE = 1
                OPTIONAL_MULTIPLE = 2
                REQUIRED_ONCE = 3
                REQUIRED_MULTIPLE = 4

            name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            value_type: str = proto.Field(
                proto.STRING,
                number=2,
            )
            occurrence_type: "DocumentSchema.EntityType.Property.OccurrenceType" = (
                proto.Field(
                    proto.ENUM,
                    number=3,
                    enum="DocumentSchema.EntityType.Property.OccurrenceType",
                )
            )

        enum_values: "DocumentSchema.EntityType.EnumValues" = proto.Field(
            proto.MESSAGE,
            number=14,
            oneof="value_source",
            message="DocumentSchema.EntityType.EnumValues",
        )
        display_name: str = proto.Field(
            proto.STRING,
            number=13,
        )
        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        base_types: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        properties: MutableSequence[
            "DocumentSchema.EntityType.Property"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message="DocumentSchema.EntityType.Property",
        )

    class Metadata(proto.Message):
        r"""Metadata for global schema behavior.

        Attributes:
            document_splitter (bool):
                If true, a ``document`` entity type can be applied to
                subdocument ( splitting). Otherwise, it can only be applied
                to the entire document (classification).
            document_allow_multiple_labels (bool):
                If true, on a given page, there can be multiple ``document``
                annotations covering it.
            prefixed_naming_on_properties (bool):
                If set, all the nested entities must be
                prefixed with the parents.
            skip_naming_validation (bool):
                If set, we will skip the naming format validation in the
                schema. So the string values in
                ``DocumentSchema.EntityType.name`` and
                ``DocumentSchema.EntityType.Property.name`` will not be
                checked.
        """

        document_splitter: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        document_allow_multiple_labels: bool = proto.Field(
            proto.BOOL,
            number=2,
        )
        prefixed_naming_on_properties: bool = proto.Field(
            proto.BOOL,
            number=6,
        )
        skip_naming_validation: bool = proto.Field(
            proto.BOOL,
            number=7,
        )

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    entity_types: MutableSequence[EntityType] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=EntityType,
    )
    metadata: Metadata = proto.Field(
        proto.MESSAGE,
        number=4,
        message=Metadata,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
