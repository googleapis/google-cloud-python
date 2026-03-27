# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
    package="google.cloud.dataplex.v1",
    manifest={
        "DataDocumentationSpec",
        "DataDocumentationResult",
    },
)


class DataDocumentationSpec(proto.Message):
    r"""DataDocumentation scan related spec.

    Attributes:
        catalog_publishing_enabled (bool):
            Optional. Whether to publish result to
            Dataplex Catalog.
        generation_scopes (MutableSequence[google.cloud.dataplex_v1.types.DataDocumentationSpec.GenerationScope]):
            Optional. Specifies which components of the
            data documentation to generate. Any component
            that is required to generate the specified
            components will also be generated. If no
            generation scope is specified, all available
            documentation components will be generated.
    """

    class GenerationScope(proto.Enum):
        r"""The data documentation generation scope. This field contains
        the possible components of a data documentation scan which can
        be selectively generated.

        Values:
            GENERATION_SCOPE_UNSPECIFIED (0):
                Unspecified generation scope. If no
                generation scope is specified, all available
                documentation components will be generated.
            ALL (1):
                All the possible results will be generated.
            TABLE_AND_COLUMN_DESCRIPTIONS (2):
                Table and column descriptions will be
                generated.
            SQL_QUERIES (3):
                SQL queries will be generated.
        """

        GENERATION_SCOPE_UNSPECIFIED = 0
        ALL = 1
        TABLE_AND_COLUMN_DESCRIPTIONS = 2
        SQL_QUERIES = 3

    catalog_publishing_enabled: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    generation_scopes: MutableSequence[GenerationScope] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=GenerationScope,
    )


class DataDocumentationResult(proto.Message):
    r"""The output of a DataDocumentation scan.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        table_result (google.cloud.dataplex_v1.types.DataDocumentationResult.TableResult):
            Output only. Table result for insights.

            This field is a member of `oneof`_ ``result``.
    """

    class TableResult(proto.Message):
        r"""Generated metadata about the table.

        Attributes:
            name (str):
                Output only. The service-qualified full resource name of the
                cloud resource. Ex:
                //bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID
            overview (str):
                Output only. Generated description of the
                table.
            schema (google.cloud.dataplex_v1.types.DataDocumentationResult.Schema):
                Output only. Schema of the table with
                generated metadata of the columns in the schema.
            queries (MutableSequence[google.cloud.dataplex_v1.types.DataDocumentationResult.Query]):
                Output only. Sample SQL queries for the
                table.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        overview: str = proto.Field(
            proto.STRING,
            number=2,
        )
        schema: "DataDocumentationResult.Schema" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="DataDocumentationResult.Schema",
        )
        queries: MutableSequence["DataDocumentationResult.Query"] = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message="DataDocumentationResult.Query",
        )

    class Query(proto.Message):
        r"""A sample SQL query in data documentation.

        Attributes:
            sql (str):
                Output only. The SQL query string which can
                be executed.
            description (str):
                Output only. The description for the query.
        """

        sql: str = proto.Field(
            proto.STRING,
            number=1,
        )
        description: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class Schema(proto.Message):
        r"""Schema of the table with generated metadata of columns.

        Attributes:
            fields (MutableSequence[google.cloud.dataplex_v1.types.DataDocumentationResult.Field]):
                Output only. The list of columns.
        """

        fields: MutableSequence["DataDocumentationResult.Field"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="DataDocumentationResult.Field",
        )

    class Field(proto.Message):
        r"""Column of a table with generated metadata and nested fields.

        Attributes:
            name (str):
                Output only. The name of the column.
            description (str):
                Output only. Generated description for
                columns and fields.
            fields (MutableSequence[google.cloud.dataplex_v1.types.DataDocumentationResult.Field]):
                Output only. Nested fields.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        description: str = proto.Field(
            proto.STRING,
            number=2,
        )
        fields: MutableSequence["DataDocumentationResult.Field"] = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="DataDocumentationResult.Field",
        )

    table_result: TableResult = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="result",
        message=TableResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
