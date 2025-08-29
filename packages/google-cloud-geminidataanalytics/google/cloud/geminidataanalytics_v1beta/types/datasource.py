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

from google.cloud.geminidataanalytics_v1beta.types import credentials as gcg_credentials

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1beta",
    manifest={
        "DataFilterType",
        "DatasourceReferences",
        "BigQueryTableReferences",
        "BigQueryTableReference",
        "StudioDatasourceReferences",
        "StudioDatasourceReference",
        "LookerExploreReferences",
        "LookerExploreReference",
        "PrivateLookerInstanceInfo",
        "Datasource",
        "Schema",
        "Field",
        "DataFilter",
    },
)


class DataFilterType(proto.Enum):
    r"""The type of filter present on a datasource, such as ALWAYS_FILTER.

    Values:
        DATA_FILTER_TYPE_UNSPECIFIED (0):
            The filter type was not specified.
        ALWAYS_FILTER (1):
            A filter that the user configures, and any
            queries to the Explore will always apply this
            filter by default. Currently only used for
            Looker data sources.
    """
    DATA_FILTER_TYPE_UNSPECIFIED = 0
    ALWAYS_FILTER = 1


class DatasourceReferences(proto.Message):
    r"""A collection of references to datasources.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bq (google.cloud.geminidataanalytics_v1beta.types.BigQueryTableReferences):
            References to BigQuery tables.

            This field is a member of `oneof`_ ``references``.
        studio (google.cloud.geminidataanalytics_v1beta.types.StudioDatasourceReferences):
            References to Looker Studio datasources.

            This field is a member of `oneof`_ ``references``.
        looker (google.cloud.geminidataanalytics_v1beta.types.LookerExploreReferences):
            References to Looker Explores.

            This field is a member of `oneof`_ ``references``.
    """

    bq: "BigQueryTableReferences" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="references",
        message="BigQueryTableReferences",
    )
    studio: "StudioDatasourceReferences" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="references",
        message="StudioDatasourceReferences",
    )
    looker: "LookerExploreReferences" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="references",
        message="LookerExploreReferences",
    )


class BigQueryTableReferences(proto.Message):
    r"""Message representing references to BigQuery tables.

    Attributes:
        table_references (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.BigQueryTableReference]):
            Required. References to BigQuery tables.
    """

    table_references: MutableSequence["BigQueryTableReference"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BigQueryTableReference",
    )


class BigQueryTableReference(proto.Message):
    r"""Message representing a reference to a single BigQuery table.

    Attributes:
        project_id (str):
            Required. The project that the table belongs
            to.
        dataset_id (str):
            Required. The dataset that the table belongs
            to.
        table_id (str):
            Required. The table id.
        schema (google.cloud.geminidataanalytics_v1beta.types.Schema):
            Optional. The schema of the datasource.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    schema: "Schema" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Schema",
    )


class StudioDatasourceReferences(proto.Message):
    r"""Message representing references to Looker Studio datasources.

    Attributes:
        studio_references (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.StudioDatasourceReference]):
            The references to the studio datasources.
    """

    studio_references: MutableSequence[
        "StudioDatasourceReference"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="StudioDatasourceReference",
    )


class StudioDatasourceReference(proto.Message):
    r"""Message representing a reference to a single Looker Studio
    datasource.

    Attributes:
        datasource_id (str):
            Required. The id of the datasource.
    """

    datasource_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class LookerExploreReferences(proto.Message):
    r"""Message representing references to Looker explores.

    Attributes:
        explore_references (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.LookerExploreReference]):
            Required. References to Looker explores.
        credentials (google.cloud.geminidataanalytics_v1beta.types.Credentials):
            Optional. The credentials to use when calling the Looker
            API.

            Currently supports both OAuth token and API key-based
            credentials, as described in `Authentication with an
            SDK <https://cloud.google.com/looker/docs/api-auth#authentication_with_an_sdk>`__.
    """

    explore_references: MutableSequence["LookerExploreReference"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LookerExploreReference",
    )
    credentials: gcg_credentials.Credentials = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcg_credentials.Credentials,
    )


class LookerExploreReference(proto.Message):
    r"""Message representing a reference to a single Looker explore.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        looker_instance_uri (str):
            Required. The base url of the Looker
            instance.

            This field is a member of `oneof`_ ``instance``.
        private_looker_instance_info (google.cloud.geminidataanalytics_v1beta.types.PrivateLookerInstanceInfo):
            Private Looker instance info.

            This field is a member of `oneof`_ ``instance``.
        lookml_model (str):
            Required. Looker model, as outlined in `Major LookML
            structures <https://cloud.google.com/looker/docs/lookml-terms-and-concepts#major_lookml_structures>`__.
            Name of the LookML model.
        explore (str):
            Required. Looker Explore, as outlined in `Major LookML
            structures <https://cloud.google.com/looker/docs/lookml-terms-and-concepts#major_lookml_structures>`__.
            Name of the LookML Explore.
        schema (google.cloud.geminidataanalytics_v1beta.types.Schema):
            Optional. The schema of the datasource.
    """

    looker_instance_uri: str = proto.Field(
        proto.STRING,
        number=9,
        oneof="instance",
    )
    private_looker_instance_info: "PrivateLookerInstanceInfo" = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="instance",
        message="PrivateLookerInstanceInfo",
    )
    lookml_model: str = proto.Field(
        proto.STRING,
        number=4,
    )
    explore: str = proto.Field(
        proto.STRING,
        number=5,
    )
    schema: "Schema" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="Schema",
    )


class PrivateLookerInstanceInfo(proto.Message):
    r"""Message representing a private Looker instance info required
    if the Looker instance is behind a private network.

    Attributes:
        looker_instance_id (str):
            The Looker instance id.
        service_directory_name (str):
            The service directory name of the Looker
            instance.
    """

    looker_instance_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_directory_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Datasource(proto.Message):
    r"""A datasource that can be used to answer questions.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bigquery_table_reference (google.cloud.geminidataanalytics_v1beta.types.BigQueryTableReference):
            A reference to a BigQuery table.

            This field is a member of `oneof`_ ``reference``.
        studio_datasource_id (str):
            A reference to a Looker Studio datasource.

            This field is a member of `oneof`_ ``reference``.
        looker_explore_reference (google.cloud.geminidataanalytics_v1beta.types.LookerExploreReference):
            A reference to a Looker explore.

            This field is a member of `oneof`_ ``reference``.
        schema (google.cloud.geminidataanalytics_v1beta.types.Schema):
            Optional. The schema of the datasource.
    """

    bigquery_table_reference: "BigQueryTableReference" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="reference",
        message="BigQueryTableReference",
    )
    studio_datasource_id: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="reference",
    )
    looker_explore_reference: "LookerExploreReference" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="reference",
        message="LookerExploreReference",
    )
    schema: "Schema" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="Schema",
    )


class Schema(proto.Message):
    r"""The schema of a Datasource or QueryResult instance.

    Attributes:
        fields (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.Field]):
            Optional. The fields in the schema.
        description (str):
            Optional. A textual description of the
            table's content and purpose. For example:
            "Contains information about customer orders in
            our e-commerce store.".
        synonyms (MutableSequence[str]):
            Optional. A list of alternative names or synonyms that can
            be used to refer to the table. For example: ["sales",
            "orders", "purchases"]
        tags (MutableSequence[str]):
            Optional. A list of tags or keywords associated with the
            table, used for categorization. For example: ["transaction",
            "revenue", "customer_data"]
        display_name (str):
            Optional. Table display_name (same as label in
            cloud/data_analytics/anarres/data/looker/proto/model_explore.proto),
            not required, currently only Looker has this field.
        filters (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.DataFilter]):
            Optional. The filters on the datasource's
            underlying data. Currently only used for Looker
            data sources.
    """

    fields: MutableSequence["Field"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Field",
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    synonyms: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    filters: MutableSequence["DataFilter"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="DataFilter",
    )


class Field(proto.Message):
    r"""A field in a schema.

    Attributes:
        name (str):
            Optional. The name of the field.
        type_ (str):
            Optional. The type of the field.
        description (str):
            Optional. A brief description of the field.
        mode (str):
            Optional. The mode of the field (e.g.,
            NULLABLE, REPEATED).
        synonyms (MutableSequence[str]):
            Optional. A list of alternative names or synonyms that can
            be used to refer to this field. For example: ["id",
            "customerid", "cust_id"]
        tags (MutableSequence[str]):
            Optional. A list of tags or keywords associated with the
            field, used for categorization. For example: ["identifier",
            "customer", "pii"]
        display_name (str):
            Optional. Field display_name (same as label in
        subfields (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.Field]):
            Optional. Recursive property for nested
            schema structures.
        category (str):
            Optional. Field category, not required,
            currently only useful for Looker. We are using a
            string to avoid depending on an external package
            and keep this package self-contained.
        value_format (str):
            Optional. Looker only. Value format of the
            field. Ref:

            https://cloud.google.com/looker/docs/reference/param-field-value-format
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    mode: str = proto.Field(
        proto.STRING,
        number=4,
    )
    synonyms: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    subfields: MutableSequence["Field"] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="Field",
    )
    category: str = proto.Field(
        proto.STRING,
        number=10,
    )
    value_format: str = proto.Field(
        proto.STRING,
        number=11,
    )


class DataFilter(proto.Message):
    r"""A filter on a datasource's underlying data. Filter syntax
    documentation:
    https://cloud.google.com/looker/docs/filter-expressions

    Attributes:
        field (str):
            Optional. The field to filter on. For example:
            ["event_date", "customer_id", "product_category"]
        value (str):
            Optional. The default value used for this filter if the
            filter is not overridden in a query. For example: ["after
            2024-01-01", "123", "-fashion"]
        type_ (google.cloud.geminidataanalytics_v1beta.types.DataFilterType):
            Optional. The type of filter present on a datasource, such
            as ALWAYS_FILTER.
    """

    field: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    type_: "DataFilterType" = proto.Field(
        proto.ENUM,
        number=3,
        enum="DataFilterType",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
