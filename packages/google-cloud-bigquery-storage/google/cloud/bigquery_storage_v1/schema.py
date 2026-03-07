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

"""Utilities for converting BigQuery schemas to Protocol Buffer descriptors.

This module provides functionality to dynamically generate Protocol Buffer
descriptors from BigQuery table schemas, eliminating the need to manually
create and compile .proto files when using the BigQuery Storage Write API.
"""

import re
from typing import Dict, List, Tuple

from google.cloud.bigquery_storage_v1 import types
from google.protobuf import descriptor_pb2


# Mapping from BigQuery types to Protocol Buffer field types
_BQ_TO_PROTO_TYPE_MAP: Dict[types.TableFieldSchema.Type, int] = {
    types.TableFieldSchema.Type.STRING: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    types.TableFieldSchema.Type.INT64: descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
    types.TableFieldSchema.Type.BOOL: descriptor_pb2.FieldDescriptorProto.TYPE_BOOL,
    types.TableFieldSchema.Type.BYTES: descriptor_pb2.FieldDescriptorProto.TYPE_BYTES,
    types.TableFieldSchema.Type.DOUBLE: descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE,
    # DATE is represented as days since epoch
    types.TableFieldSchema.Type.DATE: descriptor_pb2.FieldDescriptorProto.TYPE_INT32,
    # DATETIME is represented as a formatted string
    types.TableFieldSchema.Type.DATETIME: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    # TIME is represented as a formatted string
    types.TableFieldSchema.Type.TIME: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    # TIMESTAMP is represented as microseconds since epoch
    types.TableFieldSchema.Type.TIMESTAMP: descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
    # NUMERIC and BIGNUMERIC are represented as strings
    types.TableFieldSchema.Type.NUMERIC: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    types.TableFieldSchema.Type.BIGNUMERIC: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    # GEOGRAPHY is represented as WKT string
    types.TableFieldSchema.Type.GEOGRAPHY: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    # JSON is represented as a string
    types.TableFieldSchema.Type.JSON: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
    # INTERVAL is represented as a string
    types.TableFieldSchema.Type.INTERVAL: descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
}


def _sanitize_field_name(field_name: str) -> str:
    """Sanitize a field name to make it proto-compatible.

    Args:
        field_name: The original field name.

    Returns:
        The sanitized field name.
    """
    # Replace invalid characters with underscores.
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', field_name)
    # If the first character is a digit, prepend an underscore.
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized
    # As a convention, field names are lowercased.
    return sanitized.lower()


def _get_field_label(mode: types.TableFieldSchema.Mode) -> int:
    """Convert BigQuery field mode to Protocol Buffer field label.

    Args:
        mode: The BigQuery field mode (NULLABLE, REQUIRED, or REPEATED).

    Returns:
        The corresponding Protocol Buffer field label constant.
    """
    if mode == types.TableFieldSchema.Mode.REQUIRED:
        return descriptor_pb2.FieldDescriptorProto.LABEL_REQUIRED
    elif mode == types.TableFieldSchema.Mode.REPEATED:
        return descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
    else:  # NULLABLE or MODE_UNSPECIFIED
        return descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL


def _convert_bq_field_to_proto_field(
    bq_field: types.TableFieldSchema,
    field_number: int,
    scope: str,
) -> descriptor_pb2.FieldDescriptorProto:
    """Convert a BigQuery field to a Protocol Buffer field descriptor.

    Args:
        bq_field: The BigQuery field schema.
        field_number: The field number (position) in the message.
        scope: The scope/type name for nested messages (STRUCT/RANGE).

    Returns:
        A FieldDescriptorProto for the field.
    """
    field_name = _sanitize_field_name(bq_field.name)
    mode = bq_field.mode or types.TableFieldSchema.Mode.NULLABLE

    field_descriptor = descriptor_pb2.FieldDescriptorProto()
    field_descriptor.name = field_name
    field_descriptor.number = field_number
    field_descriptor.label = _get_field_label(mode)

    if bq_field.type_ == types.TableFieldSchema.Type.STRUCT:
        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
        field_descriptor.type_name = scope
    elif bq_field.type_ == types.TableFieldSchema.Type.RANGE:
        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
        field_descriptor.type_name = scope
    else:
        proto_type = _BQ_TO_PROTO_TYPE_MAP.get(bq_field.type_)
        if proto_type is None:
            raise ValueError(
                f"Unsupported BigQuery type: {bq_field.type_} for field {bq_field.name}"
            )
        field_descriptor.type = proto_type

    return field_descriptor


def _convert_bq_table_schema_to_proto_descriptor_impl(
    table_schema: types.TableSchema,
    scope: str,
) -> Tuple[descriptor_pb2.DescriptorProto, List[descriptor_pb2.DescriptorProto]]:
    """Recursively convert BigQuery table schema to proto descriptor.

    Args:
        table_schema: The BigQuery table schema.
        scope: The current scope for naming nested messages.

    Returns:
        A tuple of (descriptor, nested_descriptors):
        - descriptor: The DescriptorProto for this level
        - nested_descriptors: List of all nested DescriptorProto objects

    Raises:
        ValueError: If the schema contains unsupported field types or invalid RANGE fields.
    """
    fields = []
    all_nested_descriptors = []
    field_number = 1

    for bq_field in table_schema.fields:
        if bq_field.type_ == types.TableFieldSchema.Type.STRUCT:
            # Sanitize the field name for use in scope
            scope_name = _sanitize_field_name(bq_field.name)
            current_scope = f"{scope}__{scope_name}"

            # Recursively convert nested struct
            nested_schema = types.TableSchema(fields=list(bq_field.fields))
            nested_descriptor, deeply_nested = _convert_bq_table_schema_to_proto_descriptor_impl(
                nested_schema, current_scope
            )
            all_nested_descriptors.append(nested_descriptor)
            all_nested_descriptors.extend(deeply_nested)

            # Create field pointing to the nested message
            field = _convert_bq_field_to_proto_field(bq_field, field_number, current_scope)
            fields.append(field)

        elif bq_field.type_ == types.TableFieldSchema.Type.RANGE:
            # Sanitize the field name for use in scope
            scope_name = _sanitize_field_name(bq_field.name)
            current_scope = f"{scope}__{scope_name}"

            # Validate RANGE element type
            if not bq_field.range_element_type or not bq_field.range_element_type.type_:
                raise ValueError(
                    f"RANGE field '{bq_field.name}' is missing range_element_type. "
                    f"RANGE fields must specify an element type (DATE, DATETIME, or TIMESTAMP)."
                )

            element_type = bq_field.range_element_type.type_

            # Validate the element type is supported
            if element_type not in (
                types.TableFieldSchema.Type.DATE,
                types.TableFieldSchema.Type.DATETIME,
                types.TableFieldSchema.Type.TIMESTAMP,
            ):
                raise ValueError(
                    f"Unsupported element type '{element_type}' for RANGE field '{bq_field.name}'. "
                    f"Supported types are DATE, DATETIME, and TIMESTAMP."
                )

            # Create RANGE nested message with start and end fields
            range_fields = [
                types.TableFieldSchema(
                    name="start",
                    type_=element_type,
                    mode=types.TableFieldSchema.Mode.NULLABLE,
                ),
                types.TableFieldSchema(
                    name="end",
                    type_=element_type,
                    mode=types.TableFieldSchema.Mode.NULLABLE,
                ),
            ]
            range_schema = types.TableSchema(fields=range_fields)
            range_descriptor, _ = _convert_bq_table_schema_to_proto_descriptor_impl(
                range_schema, current_scope
            )
            all_nested_descriptors.append(range_descriptor)

            # Create field pointing to the RANGE message
            field = _convert_bq_field_to_proto_field(bq_field, field_number, current_scope)
            fields.append(field)

        else:
            # Primitive field
            field = _convert_bq_field_to_proto_field(bq_field, field_number, "")
            fields.append(field)

        field_number += 1

    # Create the descriptor for this level
    descriptor = descriptor_pb2.DescriptorProto()
    descriptor.name = scope
    descriptor.field.extend(fields)

    return descriptor, all_nested_descriptors


def table_schema_to_proto_descriptor(
    table_schema: types.TableSchema,
    message_name: str = "root",
) -> descriptor_pb2.DescriptorProto:
    """Convert a BigQuery TableSchema to a Protocol Buffer DescriptorProto.

    This function generates a Protocol Buffer descriptor that can be used with
    the BigQuery Storage Write API without needing to create and compile .proto
    files. The generated descriptor uses proto2 wire format, which is required
    by the Write API.

    Args:
        table_schema: The BigQuery table schema to convert.
        message_name: Optional name for the root message type. Defaults to "root".

    Returns:
        A DescriptorProto that can be used with ProtoSchema in the Write API.

    Raises:
        ValueError: If the schema contains unsupported field types or invalid RANGE fields.

    Example:
        >>> from google.cloud.bigquery_storage_v1 import schema, types
        >>>
        >>> # Define a BigQuery schema
        >>> table_schema = types.TableSchema(fields=[
        ...     types.TableFieldSchema(
        ...         name="id",
        ...         type_=types.TableFieldSchema.Type.INT64,
        ...         mode=types.TableFieldSchema.Mode.REQUIRED
        ...     ),
        ...     types.TableFieldSchema(
        ...         name="name",
        ...         type_=types.TableFieldSchema.Type.STRING
        ...     ),
        ... ])
        >>>
        >>> # Convert to proto descriptor
        >>> proto_descriptor = schema.table_schema_to_proto_descriptor(table_schema)
        >>>
        >>> # Use with Write API
        >>> proto_schema = types.ProtoSchema()
        >>> proto_schema.proto_descriptor = proto_descriptor

    Note:
        For detailed information about BigQuery to Protocol Buffer type mappings,
        see: https://cloud.google.com/bigquery/docs/write-api#data_type_conversions
    """
    # Convert using scope-based naming
    root_descriptor, nested_descriptors = _convert_bq_table_schema_to_proto_descriptor_impl(
        table_schema, message_name
    )

    root_descriptor.nested_type.extend(nested_descriptors)

    return root_descriptor


__all__ = ("table_schema_to_proto_descriptor",)
