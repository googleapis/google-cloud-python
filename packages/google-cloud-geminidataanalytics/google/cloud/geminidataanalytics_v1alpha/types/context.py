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

from google.cloud.geminidataanalytics_v1alpha.types import datasource

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1alpha",
    manifest={
        "Context",
        "ExampleQuery",
        "GlossaryTerm",
        "ConversationOptions",
        "ChartOptions",
        "AnalysisOptions",
    },
)


class Context(proto.Message):
    r"""A collection of context to apply to this conversation

    Attributes:
        system_instruction (str):
            Optional. The basic entry point for data
            owners creating domain knowledge for Agent.

            Why: Business jargon (e.g., YTD revenue is
            calculated as…, Retirement Age is 65 in the USA,
            etc) and system instructions (e.g., answer like
            a Pirate) can help the model understand the
            business context around a user question.
        datasource_references (google.cloud.geminidataanalytics_v1alpha.types.DatasourceReferences):
            Required. Data sources that are available for
            answering the question.
        options (google.cloud.geminidataanalytics_v1alpha.types.ConversationOptions):
            Optional. Additional options for the
            conversation.
        example_queries (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.ExampleQuery]):
            Optional. A list of example queries,
            providing examples of relevant and commonly used
            SQL queries and their corresponding natural
            language queries optionally present. Currently
            only used for BigQuery data sources.
        glossary_terms (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.GlossaryTerm]):
            Optional. Term definitions (currently, only
            user authored)
        schema_relationships (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Context.SchemaRelationship]):
            Optional. Relationships between table schema,
            including referencing and referenced columns.
    """

    class SchemaRelationship(proto.Message):
        r"""The relationship between two tables, including referencing
        and referenced columns. This is a derived context retrieved from
        Dataplex Dataset Insights.

        Attributes:
            left_schema_paths (google.cloud.geminidataanalytics_v1alpha.types.Context.SchemaRelationship.SchemaPaths):
                An ordered list of fields for the join from the first table.
                The size of this list must be the same as
                ``right_schema_paths``. Each field at index i in this list
                must correspond to a field at the same index in the
                ``right_schema_paths`` list.
            right_schema_paths (google.cloud.geminidataanalytics_v1alpha.types.Context.SchemaRelationship.SchemaPaths):
                An ordered list of fields for the join from the second
                table. The size of this list must be the same as
                ``left_schema_paths``. Each field at index i in this list
                must correspond to a field at the same index in the
                ``left_schema_paths`` list.
            sources (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Context.SchemaRelationship.Source]):
                Sources which generated the schema relation
                edge.
            confidence_score (float):
                A confidence score for the suggested
                relationship. Manually added edges have the
                highest confidence score.
        """

        class Source(proto.Enum):
            r"""Source which generated the schema relation edge.

            Values:
                SOURCE_UNSPECIFIED (0):
                    The source of the schema relationship is
                    unspecified.
                BIGQUERY_JOB_HISTORY (1):
                    The source of the schema relationship is
                    BigQuery job history.
                LLM_SUGGESTED (2):
                    The source of the schema relationship is LLM
                    suggested.
                BIGQUERY_TABLE_CONSTRAINTS (3):
                    The source of the schema relationship is
                    BigQuery table constraints.
            """
            SOURCE_UNSPECIFIED = 0
            BIGQUERY_JOB_HISTORY = 1
            LLM_SUGGESTED = 2
            BIGQUERY_TABLE_CONSTRAINTS = 3

        class SchemaPaths(proto.Message):
            r"""Represents an ordered set of paths within the table schema.

            Attributes:
                table_fqn (str):
                    The service-qualified full resource name of the table Ex:
                    bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID
                paths (MutableSequence[str]):
                    The ordered list of paths within the table
                    schema.
            """

            table_fqn: str = proto.Field(
                proto.STRING,
                number=1,
            )
            paths: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=2,
            )

        left_schema_paths: "Context.SchemaRelationship.SchemaPaths" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Context.SchemaRelationship.SchemaPaths",
        )
        right_schema_paths: "Context.SchemaRelationship.SchemaPaths" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Context.SchemaRelationship.SchemaPaths",
        )
        sources: MutableSequence[
            "Context.SchemaRelationship.Source"
        ] = proto.RepeatedField(
            proto.ENUM,
            number=3,
            enum="Context.SchemaRelationship.Source",
        )
        confidence_score: float = proto.Field(
            proto.FLOAT,
            number=4,
        )

    system_instruction: str = proto.Field(
        proto.STRING,
        number=1,
    )
    datasource_references: datasource.DatasourceReferences = proto.Field(
        proto.MESSAGE,
        number=7,
        message=datasource.DatasourceReferences,
    )
    options: "ConversationOptions" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ConversationOptions",
    )
    example_queries: MutableSequence["ExampleQuery"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="ExampleQuery",
    )
    glossary_terms: MutableSequence["GlossaryTerm"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="GlossaryTerm",
    )
    schema_relationships: MutableSequence[SchemaRelationship] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=SchemaRelationship,
    )


class ExampleQuery(proto.Message):
    r"""Example of relevant and commonly used SQL query and its
    corresponding natural language queries optionally present.
    Currently only used for BigQuery data sources.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        sql_query (str):
            Optional. The SQL query that should be generated to answer
            the natural language question. For example: "SELECT
            COUNT(\*) FROM orders WHERE order_date BETWEEN '2024-01-01'
            AND '2024-01-31'".

            This field is a member of `oneof`_ ``query``.
        natural_language_question (str):
            Optional. A natural language question that a
            user might ask. For example: "How many orders
            were placed last month?".
    """

    sql_query: str = proto.Field(
        proto.STRING,
        number=101,
        oneof="query",
    )
    natural_language_question: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GlossaryTerm(proto.Message):
    r"""Definition of a term within a specific domain.

    Attributes:
        display_name (str):
            Required. User friendly display name of the
            glossary term being defined. For example: "CTR",
            "conversion rate", "pending".
        description (str):
            Required. The description or meaning of the
            term. For example: "Click-through rate", "The
            percentage of users who complete a desired
            action", "An order that is waiting to be
            processed.".
        labels (MutableSequence[str]):
            Optional. A list of general purpose labels associated to
            this term. For example: ["click rate", "clickthrough",
            "waiting"]
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ConversationOptions(proto.Message):
    r"""Options for the conversation.

    Attributes:
        chart (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions):
            Optional. Options for chart generation.
        analysis (google.cloud.geminidataanalytics_v1alpha.types.AnalysisOptions):
            Optional. Options for analysis.
    """

    chart: "ChartOptions" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ChartOptions",
    )
    analysis: "AnalysisOptions" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AnalysisOptions",
    )


class ChartOptions(proto.Message):
    r"""Options for chart generation.

    Attributes:
        image (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions):
            Optional. When specified, the agent will
            render generated charts using the provided
            format. Defaults to no image.
    """

    class ImageOptions(proto.Message):
        r"""Options for rendering images of generated charts.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            no_image (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions.NoImage):
                No image.

                This field is a member of `oneof`_ ``kind``.
            svg (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions.SvgOptions):
                SVG format.

                This field is a member of `oneof`_ ``kind``.
        """

        class NoImage(proto.Message):
            r"""No image."""

        class SvgOptions(proto.Message):
            r"""SVG options."""

        no_image: "ChartOptions.ImageOptions.NoImage" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="kind",
            message="ChartOptions.ImageOptions.NoImage",
        )
        svg: "ChartOptions.ImageOptions.SvgOptions" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="kind",
            message="ChartOptions.ImageOptions.SvgOptions",
        )

    image: ImageOptions = proto.Field(
        proto.MESSAGE,
        number=1,
        message=ImageOptions,
    )


class AnalysisOptions(proto.Message):
    r"""Options for analysis.

    Attributes:
        python (google.cloud.geminidataanalytics_v1alpha.types.AnalysisOptions.Python):
            Optional. Options for Python analysis.
    """

    class Python(proto.Message):
        r"""Options for Python analysis.

        Attributes:
            enabled (bool):
                Optional. Whether to enable Python analysis.
                Defaults to false.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    python: Python = proto.Field(
        proto.MESSAGE,
        number=1,
        message=Python,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
