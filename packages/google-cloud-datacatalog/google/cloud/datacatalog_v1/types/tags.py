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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1",
    manifest={"Tag", "TagField", "TagTemplate", "TagTemplateField", "FieldType",},
)


class Tag(proto.Message):
    r"""Tags are used to attach custom metadata to Data Catalog resources.
    Tags conform to the specifications within their tag template.

    See `Data Catalog
    IAM <https://cloud.google.com/data-catalog/docs/concepts/iam>`__ for
    information on the permissions needed to create or view tags.

    Attributes:
        name (str):
            The resource name of the tag in URL format. Example:

            -  projects/{project_id}/locations/{location}/entrygroups/{entry_group_id}/entries/{entry_id}/tags/{tag_id}

            where ``tag_id`` is a system-generated identifier. Note that
            this Tag may not actually be stored in the location in this
            name.
        template (str):
            Required. The resource name of the tag template that this
            tag uses. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}

            This field cannot be modified after creation.
        template_display_name (str):
            Output only. The display name of the tag
            template.
        column (str):
            Resources like Entry can have schemas associated with them.
            This scope allows users to attach tags to an individual
            column based on that schema.

            For attaching a tag to a nested column, use ``.`` to
            separate the column names. Example:

            -  ``outer_column.inner_column``
        fields (Sequence[~.tags.Tag.FieldsEntry]):
            Required. This maps the ID of a tag field to
            the value of and additional information about
            that field. Valid field IDs are defined by the
            tag's template. A tag must have at least 1 field
            and at most 500 fields.
    """

    name = proto.Field(proto.STRING, number=1)

    template = proto.Field(proto.STRING, number=2)

    template_display_name = proto.Field(proto.STRING, number=5)

    column = proto.Field(proto.STRING, number=4, oneof="scope")

    fields = proto.MapField(proto.STRING, proto.MESSAGE, number=3, message="TagField",)


class TagField(proto.Message):
    r"""Contains the value and supporting information for a field within a
    [Tag][google.cloud.datacatalog.v1.Tag].

    Attributes:
        display_name (str):
            Output only. The display name of this field.
        double_value (float):
            Holds the value for a tag field with double
            type.
        string_value (str):
            Holds the value for a tag field with string
            type.
        bool_value (bool):
            Holds the value for a tag field with boolean
            type.
        timestamp_value (~.timestamp.Timestamp):
            Holds the value for a tag field with
            timestamp type.
        enum_value (~.tags.TagField.EnumValue):
            Holds the value for a tag field with enum
            type. This value must be one of the allowed
            values in the definition of this enum.
        order (int):
            Output only. The order of this field with respect to other
            fields in this tag. It can be set in
            [Tag][google.cloud.datacatalog.v1.TagTemplateField.order].
            For example, a higher value can indicate a more important
            field. The value can be negative. Multiple fields can have
            the same order, and field orders within a tag do not have to
            be sequential.
    """

    class EnumValue(proto.Message):
        r"""Holds an enum value.

        Attributes:
            display_name (str):
                The display name of the enum value.
        """

        display_name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=1)

    double_value = proto.Field(proto.DOUBLE, number=2, oneof="kind")

    string_value = proto.Field(proto.STRING, number=3, oneof="kind")

    bool_value = proto.Field(proto.BOOL, number=4, oneof="kind")

    timestamp_value = proto.Field(
        proto.MESSAGE, number=5, oneof="kind", message=timestamp.Timestamp,
    )

    enum_value = proto.Field(proto.MESSAGE, number=6, oneof="kind", message=EnumValue,)

    order = proto.Field(proto.INT32, number=7)


class TagTemplate(proto.Message):
    r"""A tag template defines a tag, which can have one or more typed
    fields. The template is used to create and attach the tag to GCP
    resources. `Tag template
    roles <https://cloud.google.com/iam/docs/understanding-roles#data-catalog-roles>`__
    provide permissions to create, edit, and use the template. See, for
    example, the `TagTemplate
    User <https://cloud.google.com/data-catalog/docs/how-to/template-user>`__
    role, which includes permission to use the tag template to tag
    resources.

    Attributes:
        name (str):
            The resource name of the tag template in URL format.
            Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}

            Note that this TagTemplate and its child resources may not
            actually be stored in the location in this name.
        display_name (str):
            The display name for this template. Defaults
            to an empty string.
        fields (Sequence[~.tags.TagTemplate.FieldsEntry]):
            Required. Map of tag template field IDs to the settings for
            the field. This map is an exhaustive list of the allowed
            fields. This map must contain at least one field and at most
            500 fields.

            The keys to this map are tag template field IDs. Field IDs
            can contain letters (both uppercase and lowercase), numbers
            (0-9) and underscores (_). Field IDs must be at least 1
            character long and at most 64 characters long. Field IDs
            must start with a letter or underscore.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    fields = proto.MapField(
        proto.STRING, proto.MESSAGE, number=3, message="TagTemplateField",
    )


class TagTemplateField(proto.Message):
    r"""The template for an individual field within a tag template.

    Attributes:
        name (str):
            Output only. The resource name of the tag template field in
            URL format. Example:

            -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template}/fields/{field}

            Note that this TagTemplateField may not actually be stored
            in the location in this name.
        display_name (str):
            The display name for this field. Defaults to
            an empty string.
        type_ (~.tags.FieldType):
            Required. The type of value this tag field
            can contain.
        is_required (bool):
            Whether this is a required field. Defaults to
            false.
        order (int):
            The order of this field with respect to other
            fields in this tag template. For example, a
            higher value can indicate a more important
            field. The value can be negative. Multiple
            fields can have the same order, and field orders
            within a tag do not have to be sequential.
    """

    name = proto.Field(proto.STRING, number=6)

    display_name = proto.Field(proto.STRING, number=1)

    type_ = proto.Field(proto.MESSAGE, number=2, message="FieldType",)

    is_required = proto.Field(proto.BOOL, number=3)

    order = proto.Field(proto.INT32, number=5)


class FieldType(proto.Message):
    r"""

    Attributes:
        primitive_type (~.tags.FieldType.PrimitiveType):
            Represents primitive types - string, bool
            etc.
        enum_type (~.tags.FieldType.EnumType):
            Represents an enum type.
    """

    class PrimitiveType(proto.Enum):
        r""""""
        PRIMITIVE_TYPE_UNSPECIFIED = 0
        DOUBLE = 1
        STRING = 2
        BOOL = 3
        TIMESTAMP = 4

    class EnumType(proto.Message):
        r"""

        Attributes:
            allowed_values (Sequence[~.tags.FieldType.EnumType.EnumValue]):
                Required on create; optional on update. The
                set of allowed values for this enum. This set
                must not be empty, the display names of the
                values in this set must not be empty and the
                display names of the values must be case-
                insensitively unique within this set. Currently,
                enum values can only be added to the list of
                allowed values. Deletion and renaming of enum
                values are not supported. Can have up to 500
                allowed values.
        """

        class EnumValue(proto.Message):
            r"""

            Attributes:
                display_name (str):
                    Required. The display name of the enum value.
                    Must not be an empty string.
            """

            display_name = proto.Field(proto.STRING, number=1)

        allowed_values = proto.RepeatedField(
            proto.MESSAGE, number=1, message="FieldType.EnumType.EnumValue",
        )

    primitive_type = proto.Field(
        proto.ENUM, number=1, oneof="type_decl", enum=PrimitiveType,
    )

    enum_type = proto.Field(
        proto.MESSAGE, number=2, oneof="type_decl", message=EnumType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
