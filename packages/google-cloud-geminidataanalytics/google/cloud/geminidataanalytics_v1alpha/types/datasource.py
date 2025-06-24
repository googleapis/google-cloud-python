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

from google.cloud.geminidataanalytics_v1alpha.types import (
    credentials as gcg_credentials,
)

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1alpha",
    manifest={
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
    },
)


class DatasourceReferences(proto.Message):
    r"""A collection of references to datasources.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bq (google.cloud.geminidataanalytics_v1alpha.types.BigQueryTableReferences):
            References to BigQuery tables.

            This field is a member of `oneof`_ ``references``.
        studio (google.cloud.geminidataanalytics_v1alpha.types.StudioDatasourceReferences):
            References to LookerStudio datasources.

            This field is a member of `oneof`_ ``references``.
        looker (google.cloud.geminidataanalytics_v1alpha.types.LookerExploreReferences):
            References to Looker explores.

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
        table_references (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.BigQueryTableReference]):
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
            Required. The project the table belongs to.
        dataset_id (str):
            Required. The dataset the table belongs to.
        table_id (str):
            Required. The table id.
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


class StudioDatasourceReferences(proto.Message):
    r"""Message representing references to LookerStudio datasources.

    Attributes:
        studio_references (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.StudioDatasourceReference]):
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
    r"""Message representing a reference to a single LookerStudio
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
        explore_references (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.LookerExploreReference]):
            Required. References to Looker explores.
        credentials (google.cloud.geminidataanalytics_v1alpha.types.Credentials):
            Optional. The credentials to use when calling the Looker
            API.

            Currently supports both oauth token and api keys based
            credentials, as described in
            https://cloud.google.com/looker/docs/api-auth#authentication_with_an_sdk
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
        private_looker_instance_info (google.cloud.geminidataanalytics_v1alpha.types.PrivateLookerInstanceInfo):
            Private Looker instance info.

            This field is a member of `oneof`_ ``instance``.
        lookml_model (str):
            Required. Looker Model as outlined in
            https://cloud.google.com/looker/docs/lookml-terms-and-concepts#major_lookml_structures
            Name of LookML model.
        explore (str):
            Required. Looker Explore as outlined in
            https://cloud.google.com/looker/docs/lookml-terms-and-concepts#major_lookml_structures
            Name of LookML explore.
        schema (google.cloud.geminidataanalytics_v1alpha.types.Schema):
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
        bigquery_table_reference (google.cloud.geminidataanalytics_v1alpha.types.BigQueryTableReference):
            A reference to a BigQuery table.

            This field is a member of `oneof`_ ``reference``.
        studio_datasource_id (str):
            A reference to a LookerStudio datasource.

            This field is a member of `oneof`_ ``reference``.
        looker_explore_reference (google.cloud.geminidataanalytics_v1alpha.types.LookerExploreReference):
            A reference to a Looker explore.

            This field is a member of `oneof`_ ``reference``.
        schema (google.cloud.geminidataanalytics_v1alpha.types.Schema):
            Output only. The schema of the datasource.
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
        fields (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Field]):
            Output only. The fields in the schema.
        display_name (str):
            Optional. Table display_name (same as label in
            cloud/data_analytics/anarres/data/looker/proto/model_explore.proto),
            not required, currently only Looker has this field.
    """

    fields: MutableSequence["Field"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Field",
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Field(proto.Message):
    r"""A field in a schema.

    Attributes:
        name (str):
            Output only. The name of the field.
        type_ (str):
            Output only. The type of the field.
        description (str):
            Output only. A brief description of the
            field.
        mode (str):
            Output only. The mode of the field (e.g.,
            NULLABLE, REPEATED).
        display_name (str):
            Optional. Field display_name (same as label in
        subfields (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Field]):
            Optional. Recursive property for nested
            schema structures.
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
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    subfields: MutableSequence["Field"] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="Field",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
