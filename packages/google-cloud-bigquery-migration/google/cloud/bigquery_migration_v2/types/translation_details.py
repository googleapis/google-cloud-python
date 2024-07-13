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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.bigquery.migration.v2",
    manifest={
        "TranslationDetails",
        "SourceTargetMapping",
        "SourceSpec",
        "TargetSpec",
        "Literal",
        "SourceEnvironment",
    },
)


class TranslationDetails(proto.Message):
    r"""The translation details to capture the necessary settings for
    a translation job.

    Attributes:
        source_target_mapping (MutableSequence[google.cloud.bigquery_migration_v2.types.SourceTargetMapping]):
            The mapping from source to target SQL.
        target_base_uri (str):
            The base URI for all writes to persistent
            storage.
        source_environment (google.cloud.bigquery_migration_v2.types.SourceEnvironment):
            The default source environment values for the
            translation.
        target_return_literals (MutableSequence[str]):
            The list of literal targets that will be directly returned
            to the response. Each entry consists of the constructed
            path, EXCLUDING the base path. Not providing a
            target_base_uri will prevent writing to persistent storage.
        target_types (MutableSequence[str]):
            The types of output to generate, e.g. sql, metadata,
            lineage_from_sql_scripts, etc. If not specified, a default
            set of targets will be generated. Some additional target
            types may be slower to generate. See the documentation for
            the set of available target types.
    """

    source_target_mapping: MutableSequence["SourceTargetMapping"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SourceTargetMapping",
    )
    target_base_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_environment: "SourceEnvironment" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="SourceEnvironment",
    )
    target_return_literals: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    target_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class SourceTargetMapping(proto.Message):
    r"""Represents one mapping from a source SQL to a target SQL.

    Attributes:
        source_spec (google.cloud.bigquery_migration_v2.types.SourceSpec):
            The source SQL or the path to it.
        target_spec (google.cloud.bigquery_migration_v2.types.TargetSpec):
            The target SQL or the path for it.
    """

    source_spec: "SourceSpec" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SourceSpec",
    )
    target_spec: "TargetSpec" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TargetSpec",
    )


class SourceSpec(proto.Message):
    r"""Represents one path to the location that holds source data.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        base_uri (str):
            The base URI for all files to be read in as
            sources for translation.

            This field is a member of `oneof`_ ``source``.
        literal (google.cloud.bigquery_migration_v2.types.Literal):
            Source literal.

            This field is a member of `oneof`_ ``source``.
        encoding (str):
            Optional. The optional field to specify the
            encoding of the sql bytes.
    """

    base_uri: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="source",
    )
    literal: "Literal" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message="Literal",
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TargetSpec(proto.Message):
    r"""Represents one path to the location that holds target data.

    Attributes:
        relative_path (str):
            The relative path for the target data. Given source file
            ``base_uri/input/sql``, the output would be
            ``target_base_uri/sql/relative_path/input.sql``.
    """

    relative_path: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Literal(proto.Message):
    r"""Literal data.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        literal_string (str):
            Literal string data.

            This field is a member of `oneof`_ ``literal_data``.
        literal_bytes (bytes):
            Literal byte data.

            This field is a member of `oneof`_ ``literal_data``.
        relative_path (str):
            Required. The identifier of the literal
            entry.
    """

    literal_string: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="literal_data",
    )
    literal_bytes: bytes = proto.Field(
        proto.BYTES,
        number=3,
        oneof="literal_data",
    )
    relative_path: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SourceEnvironment(proto.Message):
    r"""Represents the default source environment values for the
    translation.

    Attributes:
        default_database (str):
            The default database name to fully qualify
            SQL objects when their database name is missing.
        schema_search_path (MutableSequence[str]):
            The schema search path. When SQL objects are
            missing schema name, translation engine will
            search through this list to find the value.
        metadata_store_dataset (str):
            Optional. Expects a validQ BigQuery dataset ID that exists,
            e.g., project-123.metadata_store_123. If specified,
            translation will search and read the required schema
            information from a metadata store in this dataset. If
            metadata store doesn't exist, translation will parse the
            metadata file and upload the schema info to a temp table in
            the dataset to speed up future translation jobs.
    """

    default_database: str = proto.Field(
        proto.STRING,
        number=1,
    )
    schema_search_path: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    metadata_store_dataset: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
