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
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.bigquery.migration.v2",
    manifest={
        "TranslationConfigDetails",
        "Dialect",
        "BigQueryDialect",
        "HiveQLDialect",
        "RedshiftDialect",
        "TeradataDialect",
        "OracleDialect",
        "SparkSQLDialect",
        "SnowflakeDialect",
        "NetezzaDialect",
        "AzureSynapseDialect",
        "VerticaDialect",
        "SQLServerDialect",
        "ObjectNameMappingList",
        "ObjectNameMapping",
        "NameMappingKey",
        "NameMappingValue",
        "SourceEnv",
    },
)


class TranslationConfigDetails(proto.Message):
    r"""The translation config to capture necessary settings for a
    translation task and subtask.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source_path (str):
            The Cloud Storage path for a directory of
            files to translate in a task.

            This field is a member of `oneof`_ ``source_location``.
        gcs_target_path (str):
            The Cloud Storage path to write back the
            corresponding input files to.

            This field is a member of `oneof`_ ``target_location``.
        source_dialect (google.cloud.bigquery_migration_v2.types.Dialect):
            The dialect of the input files.
        target_dialect (google.cloud.bigquery_migration_v2.types.Dialect):
            The target dialect for the engine to
            translate the input to.
        name_mapping_list (google.cloud.bigquery_migration_v2.types.ObjectNameMappingList):
            The mapping of objects to their desired
            output names in list form.

            This field is a member of `oneof`_ ``output_name_mapping``.
        source_env (google.cloud.bigquery_migration_v2.types.SourceEnv):
            The default source environment values for the
            translation.
    """

    gcs_source_path = proto.Field(
        proto.STRING,
        number=1,
        oneof="source_location",
    )
    gcs_target_path = proto.Field(
        proto.STRING,
        number=2,
        oneof="target_location",
    )
    source_dialect = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Dialect",
    )
    target_dialect = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Dialect",
    )
    name_mapping_list = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="output_name_mapping",
        message="ObjectNameMappingList",
    )
    source_env = proto.Field(
        proto.MESSAGE,
        number=6,
        message="SourceEnv",
    )


class Dialect(proto.Message):
    r"""The possible dialect options for translation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bigquery_dialect (google.cloud.bigquery_migration_v2.types.BigQueryDialect):
            The BigQuery dialect

            This field is a member of `oneof`_ ``dialect_value``.
        hiveql_dialect (google.cloud.bigquery_migration_v2.types.HiveQLDialect):
            The HiveQL dialect

            This field is a member of `oneof`_ ``dialect_value``.
        redshift_dialect (google.cloud.bigquery_migration_v2.types.RedshiftDialect):
            The Redshift dialect

            This field is a member of `oneof`_ ``dialect_value``.
        teradata_dialect (google.cloud.bigquery_migration_v2.types.TeradataDialect):
            The Teradata dialect

            This field is a member of `oneof`_ ``dialect_value``.
        oracle_dialect (google.cloud.bigquery_migration_v2.types.OracleDialect):
            The Oracle dialect

            This field is a member of `oneof`_ ``dialect_value``.
        sparksql_dialect (google.cloud.bigquery_migration_v2.types.SparkSQLDialect):
            The SparkSQL dialect

            This field is a member of `oneof`_ ``dialect_value``.
        snowflake_dialect (google.cloud.bigquery_migration_v2.types.SnowflakeDialect):
            The Snowflake dialect

            This field is a member of `oneof`_ ``dialect_value``.
        netezza_dialect (google.cloud.bigquery_migration_v2.types.NetezzaDialect):
            The Netezza dialect

            This field is a member of `oneof`_ ``dialect_value``.
        azure_synapse_dialect (google.cloud.bigquery_migration_v2.types.AzureSynapseDialect):
            The Azure Synapse dialect

            This field is a member of `oneof`_ ``dialect_value``.
        vertica_dialect (google.cloud.bigquery_migration_v2.types.VerticaDialect):
            The Vertica dialect

            This field is a member of `oneof`_ ``dialect_value``.
        sql_server_dialect (google.cloud.bigquery_migration_v2.types.SQLServerDialect):
            The SQL Server dialect

            This field is a member of `oneof`_ ``dialect_value``.
    """

    bigquery_dialect = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="dialect_value",
        message="BigQueryDialect",
    )
    hiveql_dialect = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="dialect_value",
        message="HiveQLDialect",
    )
    redshift_dialect = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="dialect_value",
        message="RedshiftDialect",
    )
    teradata_dialect = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="dialect_value",
        message="TeradataDialect",
    )
    oracle_dialect = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="dialect_value",
        message="OracleDialect",
    )
    sparksql_dialect = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="dialect_value",
        message="SparkSQLDialect",
    )
    snowflake_dialect = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="dialect_value",
        message="SnowflakeDialect",
    )
    netezza_dialect = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="dialect_value",
        message="NetezzaDialect",
    )
    azure_synapse_dialect = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="dialect_value",
        message="AzureSynapseDialect",
    )
    vertica_dialect = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="dialect_value",
        message="VerticaDialect",
    )
    sql_server_dialect = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="dialect_value",
        message="SQLServerDialect",
    )


class BigQueryDialect(proto.Message):
    r"""The dialect definition for BigQuery."""


class HiveQLDialect(proto.Message):
    r"""The dialect definition for HiveQL."""


class RedshiftDialect(proto.Message):
    r"""The dialect definition for Redshift."""


class TeradataDialect(proto.Message):
    r"""The dialect definition for Teradata.

    Attributes:
        mode (google.cloud.bigquery_migration_v2.types.TeradataDialect.Mode):
            Which Teradata sub-dialect mode the user
            specifies.
    """

    class Mode(proto.Enum):
        r"""The sub-dialect options for Teradata."""
        MODE_UNSPECIFIED = 0
        SQL = 1
        BTEQ = 2

    mode = proto.Field(
        proto.ENUM,
        number=1,
        enum=Mode,
    )


class OracleDialect(proto.Message):
    r"""The dialect definition for Oracle."""


class SparkSQLDialect(proto.Message):
    r"""The dialect definition for SparkSQL."""


class SnowflakeDialect(proto.Message):
    r"""The dialect definition for Snowflake."""


class NetezzaDialect(proto.Message):
    r"""The dialect definition for Netezza."""


class AzureSynapseDialect(proto.Message):
    r"""The dialect definition for Azure Synapse."""


class VerticaDialect(proto.Message):
    r"""The dialect definition for Vertica."""


class SQLServerDialect(proto.Message):
    r"""The dialect definition for SQL Server."""


class ObjectNameMappingList(proto.Message):
    r"""Represents a map of name mappings using a list of key:value
    proto messages of existing name to desired output name.

    Attributes:
        name_map (Sequence[google.cloud.bigquery_migration_v2.types.ObjectNameMapping]):
            The elements of the object name map.
    """

    name_map = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ObjectNameMapping",
    )


class ObjectNameMapping(proto.Message):
    r"""Represents a key-value pair of NameMappingKey to
    NameMappingValue to represent the mapping of SQL names from the
    input value to desired output.

    Attributes:
        source (google.cloud.bigquery_migration_v2.types.NameMappingKey):
            The name of the object in source that is
            being mapped.
        target (google.cloud.bigquery_migration_v2.types.NameMappingValue):
            The desired target name of the object that is
            being mapped.
    """

    source = proto.Field(
        proto.MESSAGE,
        number=1,
        message="NameMappingKey",
    )
    target = proto.Field(
        proto.MESSAGE,
        number=2,
        message="NameMappingValue",
    )


class NameMappingKey(proto.Message):
    r"""The potential components of a full name mapping that will be
    mapped during translation in the source data warehouse.

    Attributes:
        type_ (google.cloud.bigquery_migration_v2.types.NameMappingKey.Type):
            The type of object that is being mapped.
        database (str):
            The database name (BigQuery project ID
            equivalent in the source data warehouse).
        schema (str):
            The schema name (BigQuery dataset equivalent
            in the source data warehouse).
        relation (str):
            The relation name (BigQuery table or view
            equivalent in the source data warehouse).
        attribute (str):
            The attribute name (BigQuery column
            equivalent in the source data warehouse).
    """

    class Type(proto.Enum):
        r"""The type of the object that is being mapped."""
        TYPE_UNSPECIFIED = 0
        DATABASE = 1
        SCHEMA = 2
        RELATION = 3
        ATTRIBUTE = 4
        RELATION_ALIAS = 5
        ATTRIBUTE_ALIAS = 6
        FUNCTION = 7

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=Type,
    )
    database = proto.Field(
        proto.STRING,
        number=2,
    )
    schema = proto.Field(
        proto.STRING,
        number=3,
    )
    relation = proto.Field(
        proto.STRING,
        number=4,
    )
    attribute = proto.Field(
        proto.STRING,
        number=5,
    )


class NameMappingValue(proto.Message):
    r"""The potential components of a full name mapping that will be
    mapped during translation in the target data warehouse.

    Attributes:
        database (str):
            The database name (BigQuery project ID
            equivalent in the target data warehouse).
        schema (str):
            The schema name (BigQuery dataset equivalent
            in the target data warehouse).
        relation (str):
            The relation name (BigQuery table or view
            equivalent in the target data warehouse).
        attribute (str):
            The attribute name (BigQuery column
            equivalent in the target data warehouse).
    """

    database = proto.Field(
        proto.STRING,
        number=1,
    )
    schema = proto.Field(
        proto.STRING,
        number=2,
    )
    relation = proto.Field(
        proto.STRING,
        number=3,
    )
    attribute = proto.Field(
        proto.STRING,
        number=4,
    )


class SourceEnv(proto.Message):
    r"""Represents the default source environment values for the
    translation.

    Attributes:
        default_database (str):
            The default database name to fully qualify
            SQL objects when their database name is missing.
        schema_search_path (Sequence[str]):
            The schema search path. When SQL objects are
            missing schema name, translation engine will
            search through this list to find the value.
    """

    default_database = proto.Field(
        proto.STRING,
        number=1,
    )
    schema_search_path = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
