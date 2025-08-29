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
        "RetrieveBigQueryTableContextsRequest",
        "RetrieveBigQueryTableContextsResponse",
        "RetrieveBigQueryTableContextsFromRecentTablesRequest",
        "RetrieveBigQueryTableContextsFromRecentTablesResponse",
        "RetrieveBigQueryTableSuggestedDescriptionsRequest",
        "RetrieveBigQueryTableSuggestedDescriptionsResponse",
        "RetrieveBigQueryTableSuggestedExamplesRequest",
        "RetrieveBigQueryTableSuggestedExamplesResponse",
        "RetrieveBigQueryRecentRelevantTablesRequest",
        "RetrieveBigQueryRecentRelevantTablesResponse",
        "DirectLookup",
        "TableCandidate",
    },
)


class RetrieveBigQueryTableContextsRequest(proto.Message):
    r"""Request for retrieving BigQuery table contextual data via
    direct lookup.

    Attributes:
        parent (str):
            Required. Parent value for
            RetrieveBigQueryTableContextRequest. Pattern:
            ``projects/{project}/locations/{location}`` For location,
            use "global" for now. Regional location value will be
            supported in the future.
        query (str):
            Optional. User query in natural language.
        direct_lookups (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.DirectLookup]):
            Optional. A list of direct lookup parameters.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )
    direct_lookups: MutableSequence["DirectLookup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="DirectLookup",
    )


class RetrieveBigQueryTableContextsResponse(proto.Message):
    r"""Response for retrieving BigQuery table contextual data via
    direct lookup.

    Attributes:
        table_candidates (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.TableCandidate]):
            List of retrieved candidates with their
            bundled metadata.
    """

    table_candidates: MutableSequence["TableCandidate"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TableCandidate",
    )


class RetrieveBigQueryTableContextsFromRecentTablesRequest(proto.Message):
    r"""Request for retrieving BigQuery table contextual data from
    recently accessed tables. Response is sorted by semantic
    similarity to the query.

    Attributes:
        parent (str):
            Required. Parent value for
            RetrieveBigQueryTableContextsFromRecentTablesRequest.
            Pattern: ``projects/{project}/locations/{location}`` For
            location, use "global" for now. Regional location value will
            be supported in the future.
        query (str):
            Optional. User query in natural language.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RetrieveBigQueryTableContextsFromRecentTablesResponse(proto.Message):
    r"""Response for retrieving BigQuery table contextual data from
    recently accessed tables. Response is sorted by semantic
    similarity to the query.

    Attributes:
        table_candidates (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.TableCandidate]):
            List of retrieved candidates with their
            bundled metadata.
    """

    table_candidates: MutableSequence["TableCandidate"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TableCandidate",
    )


class RetrieveBigQueryTableSuggestedDescriptionsRequest(proto.Message):
    r"""Request for retrieving BigQuery table schema with suggested
    table and column descriptions. Columns are sorted by default
    BigQuery table schema order.

    Attributes:
        parent (str):
            Required. Parent value for
            RetrieveBigQueryTableSuggestedDescriptionsRequest. Pattern:
            ``projects/{project}/locations/{location}`` For location,
            use "global" for now. Regional location value will be
            supported in the future.
        direct_lookup (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.DirectLookup]):
            Optional. A list of direct lookup parameters.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    direct_lookup: MutableSequence["DirectLookup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="DirectLookup",
    )


class RetrieveBigQueryTableSuggestedDescriptionsResponse(proto.Message):
    r"""Response for retrieving BigQuery table schema with suggested
    table and column descriptions. Columns are sorted by default
    BigQuery table schema order.

    Attributes:
        table_candidates (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.TableCandidate]):
            List of retrieved candidates with their
            bundled metadata.
    """

    table_candidates: MutableSequence["TableCandidate"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TableCandidate",
    )


class RetrieveBigQueryTableSuggestedExamplesRequest(proto.Message):
    r"""Request for retrieving BigQuery table schema with suggested
    NL-SQL examples.

    Attributes:
        parent (str):
            Required. Parent value for
            RetrieveBigQueryTableSuggestedExamplesRequest. Pattern:
            ``projects/{project}/locations/{location}`` For location,
            use "global" for now. Regional location value will be
            supported in the future.
        direct_lookup (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.DirectLookup]):
            Optional. A list of direct lookup parameters.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    direct_lookup: MutableSequence["DirectLookup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="DirectLookup",
    )


class RetrieveBigQueryTableSuggestedExamplesResponse(proto.Message):
    r"""Request for retrieving BigQuery table schema with suggested
    NL-SQL examples.

    Attributes:
        example_suggestions (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.RetrieveBigQueryTableSuggestedExamplesResponse.ExampleSuggestion]):
            List of suggested examples.
    """

    class ExampleSuggestion(proto.Message):
        r"""A suggested BigQuery NL-SQL example for the given table.

        Attributes:
            nl_query (str):
                The natural language query.
            sql (str):
                The SQL answer to the query.
            linked_bigquery_tables (MutableSequence[str]):
                The linked table resources for the suggested
                example.
        """

        nl_query: str = proto.Field(
            proto.STRING,
            number=1,
        )
        sql: str = proto.Field(
            proto.STRING,
            number=2,
        )
        linked_bigquery_tables: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    example_suggestions: MutableSequence[ExampleSuggestion] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=ExampleSuggestion,
    )


class RetrieveBigQueryRecentRelevantTablesRequest(proto.Message):
    r"""Request for retrieving BigQuery table references from
    recently accessed tables. Response is sorted by semantic
    similarity to the query.

    Attributes:
        parent (str):
            Required. Parent value for
            RetrieveBigQueryRecentTablesRequest. Pattern:
            ``projects/{project}/locations/{location}`` For location,
            use "global" for now. Regional location value will be
            supported in the future.
        query (str):
            Optional. User query in natural language.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RetrieveBigQueryRecentRelevantTablesResponse(proto.Message):
    r"""Response for retrieving BigQuery table references from
    recently accessed tables. Response is sorted by semantic
    similarity to the query.

    Attributes:
        table_ids (MutableSequence[str]):
            List of retrieved table ids. The unique identifier for the
            table. Names are case-sensitive. Example for BigQuery Table:
            ``{project}.{dataset}.{table}``.
    """

    table_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class DirectLookup(proto.Message):
    r"""Direct lookup parameters.

    Attributes:
        big_query_table_reference (google.cloud.geminidataanalytics_v1alpha.types.BigQueryTableReference):
            Optional. Table reference that server invokes
            a direct lookup of table metadata upon. The
            returned candidate will be TableMetadataResult.
    """

    big_query_table_reference: datasource.BigQueryTableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=datasource.BigQueryTableReference,
    )


class TableCandidate(proto.Message):
    r"""A retrieved BigQuery table candidate.

    Attributes:
        linked_resource (str):
            The fully qualified resource name of the candidate in its
            source system, if applicable. E.g. for BigQuery tables, the
            format is:
            ``bigquery.googleapis.com/projects/{project_id}/datasets/{dataset_id}/tables/{table_id}``.
        icl_string (str):
            In-context-learning string. For example,
            could be in DDL format.
        field_suggestions (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.TableCandidate.FieldSuggestion]):
            Suggested field descriptions for this
            candidate, if requested.
    """

    class FieldSuggestion(proto.Message):
        r"""A suggested description for a field.

        Attributes:
            field (str):
                The field name.
            suggested_description (str):
                The suggested description, if descriptions
                were requested.
            nested (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.TableCandidate.FieldSuggestion]):
                Suggestions for nested fields.
        """

        field: str = proto.Field(
            proto.STRING,
            number=1,
        )
        suggested_description: str = proto.Field(
            proto.STRING,
            number=2,
        )
        nested: MutableSequence["TableCandidate.FieldSuggestion"] = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="TableCandidate.FieldSuggestion",
        )

    linked_resource: str = proto.Field(
        proto.STRING,
        number=1,
    )
    icl_string: str = proto.Field(
        proto.STRING,
        number=2,
    )
    field_suggestions: MutableSequence[FieldSuggestion] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=FieldSuggestion,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
