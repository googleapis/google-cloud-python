# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from google.cloud.bigquery_storage_v1 import schema, types
from google.protobuf import descriptor_pb2


class TestTableSchemaToProtoDescriptor:
    """Tests for table_schema_to_proto_descriptor function."""

    def test_basic_types(self):
        """Test conversion of basic BigQuery types to proto types."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="string_col", type_=types.TableFieldSchema.Type.STRING
                ),
                types.TableFieldSchema(
                    name="int64_col", type_=types.TableFieldSchema.Type.INT64
                ),
                types.TableFieldSchema(
                    name="bool_col", type_=types.TableFieldSchema.Type.BOOL
                ),
                types.TableFieldSchema(
                    name="bytes_col", type_=types.TableFieldSchema.Type.BYTES
                ),
                types.TableFieldSchema(
                    name="double_col", type_=types.TableFieldSchema.Type.DOUBLE
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        assert proto_descriptor.name == "root"
        assert len(proto_descriptor.field) == 5

        # Check string field (field names are lowercased)
        string_field = proto_descriptor.field[0]
        assert string_field.name == "string_col"
        assert string_field.number == 1
        assert string_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING
        assert string_field.label == descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL

        # Check int64 field
        int64_field = proto_descriptor.field[1]
        assert int64_field.name == "int64_col"
        assert int64_field.number == 2
        assert int64_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64

        # Check bool field
        bool_field = proto_descriptor.field[2]
        assert bool_field.name == "bool_col"
        assert bool_field.number == 3
        assert bool_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

        # Check bytes field
        bytes_field = proto_descriptor.field[3]
        assert bytes_field.name == "bytes_col"
        assert bytes_field.number == 4
        assert bytes_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_BYTES

        # Check double field
        double_field = proto_descriptor.field[4]
        assert double_field.name == "double_col"
        assert double_field.number == 5
        assert double_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE

    def test_special_types(self):
        """Test conversion of special BigQuery types (DATE, TIMESTAMP, NUMERIC, etc.)."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="date_col", type_=types.TableFieldSchema.Type.DATE
                ),
                types.TableFieldSchema(
                    name="datetime_col", type_=types.TableFieldSchema.Type.DATETIME
                ),
                types.TableFieldSchema(
                    name="time_col", type_=types.TableFieldSchema.Type.TIME
                ),
                types.TableFieldSchema(
                    name="timestamp_col", type_=types.TableFieldSchema.Type.TIMESTAMP
                ),
                types.TableFieldSchema(
                    name="numeric_col", type_=types.TableFieldSchema.Type.NUMERIC
                ),
                types.TableFieldSchema(
                    name="bignumeric_col", type_=types.TableFieldSchema.Type.BIGNUMERIC
                ),
                types.TableFieldSchema(
                    name="geography_col", type_=types.TableFieldSchema.Type.GEOGRAPHY
                ),
                types.TableFieldSchema(
                    name="json_col", type_=types.TableFieldSchema.Type.JSON
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # DATE -> INT32
        assert proto_descriptor.field[0].type == descriptor_pb2.FieldDescriptorProto.TYPE_INT32

        # DATETIME -> STRING
        assert proto_descriptor.field[1].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # TIME -> STRING
        assert proto_descriptor.field[2].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # TIMESTAMP -> INT64
        assert proto_descriptor.field[3].type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64

        # NUMERIC -> STRING
        assert proto_descriptor.field[4].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # BIGNUMERIC -> STRING
        assert proto_descriptor.field[5].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # GEOGRAPHY -> STRING
        assert proto_descriptor.field[6].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # JSON -> STRING
        assert proto_descriptor.field[7].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    def test_field_modes(self):
        """Test conversion of BigQuery field modes to proto labels."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="nullable_col",
                    type_=types.TableFieldSchema.Type.STRING,
                    mode=types.TableFieldSchema.Mode.NULLABLE,
                ),
                types.TableFieldSchema(
                    name="required_col",
                    type_=types.TableFieldSchema.Type.STRING,
                    mode=types.TableFieldSchema.Mode.REQUIRED,
                ),
                types.TableFieldSchema(
                    name="repeated_col",
                    type_=types.TableFieldSchema.Type.STRING,
                    mode=types.TableFieldSchema.Mode.REPEATED,
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # NULLABLE -> LABEL_OPTIONAL
        assert (
            proto_descriptor.field[0].label
            == descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
        )

        # REQUIRED -> LABEL_REQUIRED
        assert (
            proto_descriptor.field[1].label
            == descriptor_pb2.FieldDescriptorProto.LABEL_REQUIRED
        )

        # REPEATED -> LABEL_REPEATED
        assert (
            proto_descriptor.field[2].label
            == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
        )

    def test_struct_field(self):
        """Test conversion of STRUCT (nested message) fields with scope-based naming."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="struct_col",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    fields=[
                        types.TableFieldSchema(
                            name="sub_string",
                            type_=types.TableFieldSchema.Type.STRING,
                        ),
                        types.TableFieldSchema(
                            name="sub_int",
                            type_=types.TableFieldSchema.Type.INT64,
                        ),
                    ],
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Check main field (uses scope-based naming)
        struct_field = proto_descriptor.field[0]
        assert struct_field.name == "struct_col"
        assert struct_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
        assert struct_field.type_name == "root__struct_col"

        # Check nested type
        assert len(proto_descriptor.nested_type) == 1
        nested_type = proto_descriptor.nested_type[0]
        assert nested_type.name == "root__struct_col"
        assert len(nested_type.field) == 2

        # Check nested fields
        assert nested_type.field[0].name == "sub_string"
        assert nested_type.field[0].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING
        assert nested_type.field[1].name == "sub_int"
        assert nested_type.field[1].type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64

    def test_repeated_struct(self):
        """Test conversion of repeated STRUCT fields (arrays of structs)."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="struct_list",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    mode=types.TableFieldSchema.Mode.REPEATED,
                    fields=[
                        types.TableFieldSchema(
                            name="item_id",
                            type_=types.TableFieldSchema.Type.INT64,
                        ),
                    ],
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        struct_field = proto_descriptor.field[0]
        assert struct_field.label == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
        assert struct_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE

    def test_range_field(self):
        """Test conversion of RANGE fields with scope-based naming."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="date_range",
                    type_=types.TableFieldSchema.Type.RANGE,
                    range_element_type=types.TableFieldSchema.FieldElementType(
                        type_=types.TableFieldSchema.Type.DATE
                    ),
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Check main field (uses scope-based naming)
        range_field = proto_descriptor.field[0]
        assert range_field.name == "date_range"
        assert range_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
        assert range_field.type_name == "root__date_range"

        # Check nested Range message
        assert len(proto_descriptor.nested_type) == 1
        range_type = proto_descriptor.nested_type[0]
        assert range_type.name == "root__date_range"
        assert len(range_type.field) == 2

        # Check start field
        start_field = range_type.field[0]
        assert start_field.name == "start"
        assert start_field.number == 1
        assert start_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_INT32  # DATE -> INT32

        # Check end field
        end_field = range_type.field[1]
        assert end_field.name == "end"
        assert end_field.number == 2
        assert end_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_INT32

    def test_deeply_nested_struct(self):
        """Test conversion of deeply nested STRUCT fields with hierarchical scope naming."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="outer",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    fields=[
                        types.TableFieldSchema(
                            name="inner",
                            type_=types.TableFieldSchema.Type.STRUCT,
                            fields=[
                                types.TableFieldSchema(
                                    name="value",
                                    type_=types.TableFieldSchema.Type.STRING,
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Check outer struct
        assert len(proto_descriptor.nested_type) >= 1
        # Find the outer nested type
        outer_type = next(nt for nt in proto_descriptor.nested_type if nt.name == "root__outer")
        assert outer_type.name == "root__outer"

        # Find the inner nested type (should be in root's nested types due to flattening)
        inner_type = next(nt for nt in proto_descriptor.nested_type if nt.name == "root__outer__inner")
        assert inner_type.name == "root__outer__inner"
        assert len(inner_type.field) == 1
        assert inner_type.field[0].name == "value"

    def test_custom_message_name(self):
        """Test specifying a custom message name."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="id", type_=types.TableFieldSchema.Type.INT64
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(
            table_schema, message_name="CustomRow"
        )

        assert proto_descriptor.name == "CustomRow"

    def test_field_numbering(self):
        """Test that field numbers are assigned sequentially starting from 1."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="first", type_=types.TableFieldSchema.Type.STRING
                ),
                types.TableFieldSchema(
                    name="second", type_=types.TableFieldSchema.Type.INT64
                ),
                types.TableFieldSchema(
                    name="third", type_=types.TableFieldSchema.Type.BOOL
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        assert proto_descriptor.field[0].number == 1
        assert proto_descriptor.field[1].number == 2
        assert proto_descriptor.field[2].number == 3

    def test_empty_schema(self):
        """Test conversion of an empty schema."""
        table_schema = types.TableSchema(fields=[])

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        assert proto_descriptor.name == "root"
        assert len(proto_descriptor.field) == 0

    def test_complex_schema(self):
        """Test a complex schema with multiple field types and nesting."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="id",
                    type_=types.TableFieldSchema.Type.INT64,
                    mode=types.TableFieldSchema.Mode.REQUIRED,
                ),
                types.TableFieldSchema(
                    name="name",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
                types.TableFieldSchema(
                    name="tags",
                    type_=types.TableFieldSchema.Type.STRING,
                    mode=types.TableFieldSchema.Mode.REPEATED,
                ),
                types.TableFieldSchema(
                    name="metadata",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    fields=[
                        types.TableFieldSchema(
                            name="created_at",
                            type_=types.TableFieldSchema.Type.TIMESTAMP,
                        ),
                        types.TableFieldSchema(
                            name="attributes",
                            type_=types.TableFieldSchema.Type.JSON,
                        ),
                    ],
                ),
                types.TableFieldSchema(
                    name="active_period",
                    type_=types.TableFieldSchema.Type.RANGE,
                    range_element_type=types.TableFieldSchema.FieldElementType(
                        type_=types.TableFieldSchema.Type.TIMESTAMP
                    ),
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Verify overall structure
        assert len(proto_descriptor.field) == 5
        assert len(proto_descriptor.nested_type) == 2  # metadata and active_period

        # Verify required field
        assert (
            proto_descriptor.field[0].label
            == descriptor_pb2.FieldDescriptorProto.LABEL_REQUIRED
        )

        # Verify repeated field
        assert (
            proto_descriptor.field[2].label
            == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
        )

        # Verify struct field
        metadata_field = proto_descriptor.field[3]
        assert metadata_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE

        # Verify range field
        range_field = proto_descriptor.field[4]
        assert range_field.type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE

    def test_range_without_element_type_raises_error(self):
        """Test that RANGE fields without element type raise ValueError."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="incomplete_range",
                    type_=types.TableFieldSchema.Type.RANGE,
                    # Missing range_element_type - should raise error
                ),
            ]
        )

        with pytest.raises(ValueError) as exc_info:
            schema.table_schema_to_proto_descriptor(table_schema)

        assert "RANGE field 'incomplete_range' is missing range_element_type" in str(
            exc_info.value
        )

    def test_scope_based_naming_avoids_collisions(self):
        """Test that scope-based naming naturally avoids collisions."""
        # Even if field names might collide with generated names, scope-based naming prevents issues
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="my_record",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    fields=[
                        types.TableFieldSchema(
                            name="value",
                            type_=types.TableFieldSchema.Type.STRING,
                        ),
                    ],
                ),
                types.TableFieldSchema(
                    name="my_record_struct",  # Would collide with suffix-based naming
                    type_=types.TableFieldSchema.Type.STRING,
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Verify fields are created correctly
        assert len(proto_descriptor.field) == 2
        assert proto_descriptor.field[0].name == "my_record"
        assert proto_descriptor.field[0].type_name == "root__my_record"
        assert proto_descriptor.field[1].name == "my_record_struct"

        # Verify nested type uses scope-based name
        assert len(proto_descriptor.nested_type) == 1
        assert proto_descriptor.nested_type[0].name == "root__my_record"

    def test_field_name_sanitization(self):
        """Test that field names are sanitized to be proto-compatible."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="field-with-hyphens",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
                types.TableFieldSchema(
                    name="field with spaces",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
                types.TableFieldSchema(
                    name="123field",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
                types.TableFieldSchema(
                    name="field@special#chars",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
                types.TableFieldSchema(
                    name="ValidField",
                    type_=types.TableFieldSchema.Type.STRING,
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Hyphens replaced with underscores
        assert proto_descriptor.field[0].name == "field_with_hyphens"

        # Spaces replaced with underscores
        assert proto_descriptor.field[1].name == "field_with_spaces"

        # Field starting with digit gets prepended underscore
        assert proto_descriptor.field[2].name == "_123field"

        # Special characters replaced with underscores
        assert proto_descriptor.field[3].name == "field_special_chars"

        # Valid field names are lowercased
        assert proto_descriptor.field[4].name == "validfield"

    def test_field_name_sanitization_in_nested_structs(self):
        """Test that field name sanitization works in nested STRUCT fields."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="outer-struct",
                    type_=types.TableFieldSchema.Type.STRUCT,
                    fields=[
                        types.TableFieldSchema(
                            name="inner-field",
                            type_=types.TableFieldSchema.Type.STRING,
                        ),
                        types.TableFieldSchema(
                            name="123inner",
                            type_=types.TableFieldSchema.Type.INT64,
                        ),
                    ],
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Outer struct field name sanitized
        outer_field = proto_descriptor.field[0]
        assert outer_field.name == "outer_struct"
        assert outer_field.type_name == "root__outer_struct"

        # Nested type name sanitized
        nested_type = proto_descriptor.nested_type[0]
        assert nested_type.name == "root__outer_struct"

        # Inner fields sanitized
        assert nested_type.field[0].name == "inner_field"
        assert nested_type.field[1].name == "_123inner"

    def test_field_name_sanitization_in_range_fields(self):
        """Test that field name sanitization works for RANGE fields."""
        table_schema = types.TableSchema(
            fields=[
                types.TableFieldSchema(
                    name="date-range",
                    type_=types.TableFieldSchema.Type.RANGE,
                    range_element_type=types.TableFieldSchema.FieldElementType(
                        type_=types.TableFieldSchema.Type.DATE
                    ),
                ),
            ]
        )

        proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)

        # Range field name sanitized
        range_field = proto_descriptor.field[0]
        assert range_field.name == "date_range"
        assert range_field.type_name == "root__date_range"

        # Range type name sanitized
        range_type = proto_descriptor.nested_type[0]
        assert range_type.name == "root__date_range"


if __name__ == "__main__":
    pytest.main([__file__])
