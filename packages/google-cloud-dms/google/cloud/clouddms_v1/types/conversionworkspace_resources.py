# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.clouddms_v1.types import clouddms_resources

__protobuf__ = proto.module(
    package="google.cloud.clouddms.v1",
    manifest={
        "DatabaseEntityType",
        "BackgroundJobType",
        "ImportRulesFileFormat",
        "DatabaseEngineInfo",
        "ConversionWorkspace",
        "BackgroundJobLogEntry",
        "DatabaseEntity",
        "SchemaEntity",
        "TableEntity",
        "ColumnEntity",
        "ConstraintEntity",
        "IndexEntity",
        "TriggerEntity",
        "ViewEntity",
        "SequenceEntity",
        "StoredProcedureEntity",
        "FunctionEntity",
        "SynonymEntity",
        "PackageEntity",
        "EntityMapping",
        "EntityMappingLogEntry",
    },
)


class DatabaseEntityType(proto.Enum):
    r"""The type of database entities supported,

    Values:
        DATABASE_ENTITY_TYPE_UNSPECIFIED (0):
            Unspecified database entity type.
        DATABASE_ENTITY_TYPE_SCHEMA (1):
            Schema.
        DATABASE_ENTITY_TYPE_TABLE (2):
            Table.
        DATABASE_ENTITY_TYPE_COLUMN (3):
            Column.
        DATABASE_ENTITY_TYPE_CONSTRAINT (4):
            Constraint.
        DATABASE_ENTITY_TYPE_INDEX (5):
            Index.
        DATABASE_ENTITY_TYPE_TRIGGER (6):
            Trigger.
        DATABASE_ENTITY_TYPE_VIEW (7):
            View.
        DATABASE_ENTITY_TYPE_SEQUENCE (8):
            Sequence.
        DATABASE_ENTITY_TYPE_STORED_PROCEDURE (9):
            Stored Procedure.
        DATABASE_ENTITY_TYPE_FUNCTION (10):
            Function.
        DATABASE_ENTITY_TYPE_SYNONYM (11):
            Synonym.
        DATABASE_ENTITY_TYPE_DATABASE_PACKAGE (12):
            Package.
        DATABASE_ENTITY_TYPE_UDT (13):
            UDT.
        DATABASE_ENTITY_TYPE_MATERIALIZED_VIEW (14):
            Materialized View.
        DATABASE_ENTITY_TYPE_DATABASE (15):
            Database.
    """
    DATABASE_ENTITY_TYPE_UNSPECIFIED = 0
    DATABASE_ENTITY_TYPE_SCHEMA = 1
    DATABASE_ENTITY_TYPE_TABLE = 2
    DATABASE_ENTITY_TYPE_COLUMN = 3
    DATABASE_ENTITY_TYPE_CONSTRAINT = 4
    DATABASE_ENTITY_TYPE_INDEX = 5
    DATABASE_ENTITY_TYPE_TRIGGER = 6
    DATABASE_ENTITY_TYPE_VIEW = 7
    DATABASE_ENTITY_TYPE_SEQUENCE = 8
    DATABASE_ENTITY_TYPE_STORED_PROCEDURE = 9
    DATABASE_ENTITY_TYPE_FUNCTION = 10
    DATABASE_ENTITY_TYPE_SYNONYM = 11
    DATABASE_ENTITY_TYPE_DATABASE_PACKAGE = 12
    DATABASE_ENTITY_TYPE_UDT = 13
    DATABASE_ENTITY_TYPE_MATERIALIZED_VIEW = 14
    DATABASE_ENTITY_TYPE_DATABASE = 15


class BackgroundJobType(proto.Enum):
    r"""The types of jobs that can be executed in the background.

    Values:
        BACKGROUND_JOB_TYPE_UNSPECIFIED (0):
            Unspecified background job type.
        BACKGROUND_JOB_TYPE_SOURCE_SEED (1):
            Job to seed from the source database.
        BACKGROUND_JOB_TYPE_CONVERT (2):
            Job to convert the source database into a
            draft of the destination database.
        BACKGROUND_JOB_TYPE_APPLY_DESTINATION (3):
            Job to apply the draft tree onto the
            destination.
        BACKGROUND_JOB_TYPE_IMPORT_RULES_FILE (5):
            Job to import and convert mapping rules from
            an external source such as an ora2pg config
            file.
    """
    BACKGROUND_JOB_TYPE_UNSPECIFIED = 0
    BACKGROUND_JOB_TYPE_SOURCE_SEED = 1
    BACKGROUND_JOB_TYPE_CONVERT = 2
    BACKGROUND_JOB_TYPE_APPLY_DESTINATION = 3
    BACKGROUND_JOB_TYPE_IMPORT_RULES_FILE = 5


class ImportRulesFileFormat(proto.Enum):
    r"""The format for the import rules file.

    Values:
        IMPORT_RULES_FILE_FORMAT_UNSPECIFIED (0):
            Unspecified rules format.
        IMPORT_RULES_FILE_FORMAT_HARBOUR_BRIDGE_SESSION_FILE (1):
            HarbourBridge session file.
        IMPORT_RULES_FILE_FORMAT_ORATOPG_CONFIG_FILE (2):
            Ora2Pg configuration file.
    """
    IMPORT_RULES_FILE_FORMAT_UNSPECIFIED = 0
    IMPORT_RULES_FILE_FORMAT_HARBOUR_BRIDGE_SESSION_FILE = 1
    IMPORT_RULES_FILE_FORMAT_ORATOPG_CONFIG_FILE = 2


class DatabaseEngineInfo(proto.Message):
    r"""The type and version of a source or destination database.

    Attributes:
        engine (google.cloud.clouddms_v1.types.DatabaseEngine):
            Required. Engine type.
        version (str):
            Required. Engine named version, for example
            12.c.1.
    """

    engine: clouddms_resources.DatabaseEngine = proto.Field(
        proto.ENUM,
        number=1,
        enum=clouddms_resources.DatabaseEngine,
    )
    version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ConversionWorkspace(proto.Message):
    r"""The main conversion workspace resource entity.

    Attributes:
        name (str):
            Full name of the workspace resource, in the form of:
            projects/{project}/locations/{location}/conversionWorkspaces/{conversion_workspace}.
        source (google.cloud.clouddms_v1.types.DatabaseEngineInfo):
            Required. The source engine details.
        destination (google.cloud.clouddms_v1.types.DatabaseEngineInfo):
            Required. The destination engine details.
        global_settings (MutableMapping[str, str]):
            A generic list of settings for the workspace. The settings
            are database pair dependant and can indicate default
            behavior for the mapping rules engine or turn on or off
            specific features. Such examples can be:
            convert_foreign_key_to_interleave=true, skip_triggers=false,
            ignore_non_table_synonyms=true
        has_uncommitted_changes (bool):
            Output only. Whether the workspace has
            uncommitted changes (changes which were made
            after the workspace was committed).
        latest_commit_id (str):
            Output only. The latest commit ID.
        latest_commit_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the workspace
            was committed.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the workspace
            resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the workspace
            resource was last updated.
        display_name (str):
            The display name for the workspace.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    source: "DatabaseEngineInfo" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DatabaseEngineInfo",
    )
    destination: "DatabaseEngineInfo" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DatabaseEngineInfo",
    )
    global_settings: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    has_uncommitted_changes: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    latest_commit_id: str = proto.Field(
        proto.STRING,
        number=6,
    )
    latest_commit_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=11,
    )


class BackgroundJobLogEntry(proto.Message):
    r"""Execution log of a background job.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        id (str):
            The background job log entry ID.
        job_type (google.cloud.clouddms_v1.types.BackgroundJobType):
            The type of job that was executed.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when the background job was
            started.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when the background job was
            finished.
        completion_state (google.cloud.clouddms_v1.types.BackgroundJobLogEntry.JobCompletionState):
            Job completion state, i.e. the final state
            after the job completed.
        completion_comment (str):
            Job completion comment, such as how many
            entities were seeded, how many warnings were
            found during conversion, and similar
            information.
        request_autocommit (bool):
            Whether the client requested the conversion
            workspace to be committed after a successful
            completion of the job.
        seed_job_details (google.cloud.clouddms_v1.types.BackgroundJobLogEntry.SeedJobDetails):
            Seed job details.

            This field is a member of `oneof`_ ``job_details``.
        import_rules_job_details (google.cloud.clouddms_v1.types.BackgroundJobLogEntry.ImportRulesJobDetails):
            Import rules job details.

            This field is a member of `oneof`_ ``job_details``.
        convert_job_details (google.cloud.clouddms_v1.types.BackgroundJobLogEntry.ConvertJobDetails):
            Convert job details.

            This field is a member of `oneof`_ ``job_details``.
        apply_job_details (google.cloud.clouddms_v1.types.BackgroundJobLogEntry.ApplyJobDetails):
            Apply job details.

            This field is a member of `oneof`_ ``job_details``.
    """

    class JobCompletionState(proto.Enum):
        r"""Final state after a job completes.

        Values:
            JOB_COMPLETION_STATE_UNSPECIFIED (0):
                The status is not specified. This state is
                used when job is not yet finished.
            SUCCEEDED (1):
                Success.
            FAILED (2):
                Error.
        """
        JOB_COMPLETION_STATE_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2

    class SeedJobDetails(proto.Message):
        r"""Details regarding a Seed background job.

        Attributes:
            connection_profile (str):
                The connection profile which was used for the
                seed job.
        """

        connection_profile: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class ImportRulesJobDetails(proto.Message):
        r"""Details regarding an Import Rules background job.

        Attributes:
            files (MutableSequence[str]):
                File names used for the import rules job.
            file_format (google.cloud.clouddms_v1.types.ImportRulesFileFormat):
                The requested file format.
        """

        files: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        file_format: "ImportRulesFileFormat" = proto.Field(
            proto.ENUM,
            number=2,
            enum="ImportRulesFileFormat",
        )

    class ConvertJobDetails(proto.Message):
        r"""Details regarding a Convert background job.

        Attributes:
            filter (str):
                AIP-160 based filter used to specify the
                entities to convert
        """

        filter: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class ApplyJobDetails(proto.Message):
        r"""Details regarding an Apply background job.

        Attributes:
            connection_profile (str):
                The connection profile which was used for the
                apply job.
            filter (str):
                AIP-160 based filter used to specify the
                entities to apply
        """

        connection_profile: str = proto.Field(
            proto.STRING,
            number=1,
        )
        filter: str = proto.Field(
            proto.STRING,
            number=2,
        )

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_type: "BackgroundJobType" = proto.Field(
        proto.ENUM,
        number=2,
        enum="BackgroundJobType",
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    finish_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    completion_state: JobCompletionState = proto.Field(
        proto.ENUM,
        number=5,
        enum=JobCompletionState,
    )
    completion_comment: str = proto.Field(
        proto.STRING,
        number=6,
    )
    request_autocommit: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    seed_job_details: SeedJobDetails = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="job_details",
        message=SeedJobDetails,
    )
    import_rules_job_details: ImportRulesJobDetails = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="job_details",
        message=ImportRulesJobDetails,
    )
    convert_job_details: ConvertJobDetails = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="job_details",
        message=ConvertJobDetails,
    )
    apply_job_details: ApplyJobDetails = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="job_details",
        message=ApplyJobDetails,
    )


class DatabaseEntity(proto.Message):
    r"""The base entity type for all the database related entities.
    The message contains the entity name, the name of its parent,
    the entity type, and the specific details per entity type.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        short_name (str):
            The short name (e.g. table name) of the
            entity.
        parent_entity (str):
            The full name of the parent entity (e.g.
            schema name).
        tree (google.cloud.clouddms_v1.types.DatabaseEntity.TreeType):
            The type of tree the entity belongs to.
        entity_type (google.cloud.clouddms_v1.types.DatabaseEntityType):
            The type of the database entity (table, view,
            index, ...).
        mappings (MutableSequence[google.cloud.clouddms_v1.types.EntityMapping]):
            Details about entity mappings.
            For source tree entities, this holds the draft
            entities which were generated by the mapping
            rules.
            For draft tree entities, this holds the source
            entities which were converted to form the draft
            entity.
            Destination entities will have no mapping
            details.
        schema (google.cloud.clouddms_v1.types.SchemaEntity):
            Schema.

            This field is a member of `oneof`_ ``entity_body``.
        table (google.cloud.clouddms_v1.types.TableEntity):
            Table.

            This field is a member of `oneof`_ ``entity_body``.
        view (google.cloud.clouddms_v1.types.ViewEntity):
            View.

            This field is a member of `oneof`_ ``entity_body``.
        sequence (google.cloud.clouddms_v1.types.SequenceEntity):
            Sequence.

            This field is a member of `oneof`_ ``entity_body``.
        stored_procedure (google.cloud.clouddms_v1.types.StoredProcedureEntity):
            Stored procedure.

            This field is a member of `oneof`_ ``entity_body``.
        database_function (google.cloud.clouddms_v1.types.FunctionEntity):
            Function.

            This field is a member of `oneof`_ ``entity_body``.
        synonym (google.cloud.clouddms_v1.types.SynonymEntity):
            Synonym.

            This field is a member of `oneof`_ ``entity_body``.
        database_package (google.cloud.clouddms_v1.types.PackageEntity):
            Package.

            This field is a member of `oneof`_ ``entity_body``.
    """

    class TreeType(proto.Enum):
        r"""The type of database entities tree.

        Values:
            TREE_TYPE_UNSPECIFIED (0):
                Tree type unspecified.
            SOURCE (1):
                Tree of entities loaded from a source
                database.
            DRAFT (2):
                Tree of entities converted from the source
                tree using the mapping rules.
            DESTINATION (3):
                Tree of entities observed on the destination
                database.
        """
        TREE_TYPE_UNSPECIFIED = 0
        SOURCE = 1
        DRAFT = 2
        DESTINATION = 3

    short_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parent_entity: str = proto.Field(
        proto.STRING,
        number=2,
    )
    tree: TreeType = proto.Field(
        proto.ENUM,
        number=3,
        enum=TreeType,
    )
    entity_type: "DatabaseEntityType" = proto.Field(
        proto.ENUM,
        number=4,
        enum="DatabaseEntityType",
    )
    mappings: MutableSequence["EntityMapping"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="EntityMapping",
    )
    schema: "SchemaEntity" = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="entity_body",
        message="SchemaEntity",
    )
    table: "TableEntity" = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="entity_body",
        message="TableEntity",
    )
    view: "ViewEntity" = proto.Field(
        proto.MESSAGE,
        number=104,
        oneof="entity_body",
        message="ViewEntity",
    )
    sequence: "SequenceEntity" = proto.Field(
        proto.MESSAGE,
        number=105,
        oneof="entity_body",
        message="SequenceEntity",
    )
    stored_procedure: "StoredProcedureEntity" = proto.Field(
        proto.MESSAGE,
        number=106,
        oneof="entity_body",
        message="StoredProcedureEntity",
    )
    database_function: "FunctionEntity" = proto.Field(
        proto.MESSAGE,
        number=107,
        oneof="entity_body",
        message="FunctionEntity",
    )
    synonym: "SynonymEntity" = proto.Field(
        proto.MESSAGE,
        number=108,
        oneof="entity_body",
        message="SynonymEntity",
    )
    database_package: "PackageEntity" = proto.Field(
        proto.MESSAGE,
        number=109,
        oneof="entity_body",
        message="PackageEntity",
    )


class SchemaEntity(proto.Message):
    r"""Schema typically has no parent entity, but can have a parent
    entity DatabaseInstance (for database engines which support it).
    For some database engines, the terms  schema and user can be
    used interchangeably when they refer to a namespace or a
    collection of other database entities. Can store additional
    information which is schema specific.

    Attributes:
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=1,
        message=struct_pb2.Struct,
    )


class TableEntity(proto.Message):
    r"""Table's parent is a schema.

    Attributes:
        columns (MutableSequence[google.cloud.clouddms_v1.types.ColumnEntity]):
            Table columns.
        constraints (MutableSequence[google.cloud.clouddms_v1.types.ConstraintEntity]):
            Table constraints.
        indices (MutableSequence[google.cloud.clouddms_v1.types.IndexEntity]):
            Table indices.
        triggers (MutableSequence[google.cloud.clouddms_v1.types.TriggerEntity]):
            Table triggers.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
        comment (str):
            Comment associated with the table.
    """

    columns: MutableSequence["ColumnEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ColumnEntity",
    )
    constraints: MutableSequence["ConstraintEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ConstraintEntity",
    )
    indices: MutableSequence["IndexEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="IndexEntity",
    )
    triggers: MutableSequence["TriggerEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="TriggerEntity",
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )
    comment: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ColumnEntity(proto.Message):
    r"""Column is not used as an independent entity, it is retrieved
    as part of a Table entity.

    Attributes:
        name (str):
            Column name.
        data_type (str):
            Column data type.
        charset (str):
            Charset override - instead of table level
            charset.
        collation (str):
            Collation override - instead of table level
            collation.
        length (int):
            Column length - e.g. varchar (50).
        precision (int):
            Column precision - when relevant.
        scale (int):
            Column scale - when relevant.
        fractional_seconds_precision (int):
            Column fractional second precision - used for
            timestamp based datatypes.
        array (bool):
            Is the column of array type.
        array_length (int):
            If the column is array, of which length.
        nullable (bool):
            Is the column nullable.
        auto_generated (bool):
            Is the column auto-generated/identity.
        udt (bool):
            Is the column a UDT.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
        set_values (MutableSequence[str]):
            Specifies the list of values allowed in the
            column. Only used for set data type.
        comment (str):
            Comment associated with the column.
        ordinal_position (int):
            Column order in the table.
        default_value (str):
            Default value of the column.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    charset: str = proto.Field(
        proto.STRING,
        number=3,
    )
    collation: str = proto.Field(
        proto.STRING,
        number=4,
    )
    length: int = proto.Field(
        proto.INT64,
        number=5,
    )
    precision: int = proto.Field(
        proto.INT32,
        number=6,
    )
    scale: int = proto.Field(
        proto.INT32,
        number=7,
    )
    fractional_seconds_precision: int = proto.Field(
        proto.INT32,
        number=8,
    )
    array: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    array_length: int = proto.Field(
        proto.INT32,
        number=10,
    )
    nullable: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    auto_generated: bool = proto.Field(
        proto.BOOL,
        number=12,
    )
    udt: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=14,
        message=struct_pb2.Struct,
    )
    set_values: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=15,
    )
    comment: str = proto.Field(
        proto.STRING,
        number=16,
    )
    ordinal_position: int = proto.Field(
        proto.INT32,
        number=17,
    )
    default_value: str = proto.Field(
        proto.STRING,
        number=18,
    )


class ConstraintEntity(proto.Message):
    r"""Constraint is not used as an independent entity, it is
    retrieved as part of another entity such as Table or View.

    Attributes:
        name (str):
            The name of the table constraint.
        type_ (str):
            Type of constraint, for example unique,
            primary key, foreign key (currently only primary
            key is supported).
        table_columns (MutableSequence[str]):
            Table columns used as part of the Constraint,
            for example primary key constraint should list
            the columns which constitutes the key.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
        reference_columns (MutableSequence[str]):
            Reference columns which may be associated with the
            constraint. For example, if the constraint is a FOREIGN_KEY,
            this represents the list of full names of referenced columns
            by the foreign key.
        reference_table (str):
            Reference table which may be associated with the constraint.
            For example, if the constraint is a FOREIGN_KEY, this
            represents the list of full name of the referenced table by
            the foreign key.
        table_name (str):
            Table which is associated with the constraint. In case the
            constraint is defined on a table, this field is left empty
            as this information is stored in parent_name. However, if
            constraint is defined on a view, this field stores the table
            name on which the view is defined.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )
    reference_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    reference_table: str = proto.Field(
        proto.STRING,
        number=6,
    )
    table_name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class IndexEntity(proto.Message):
    r"""Index is not used as an independent entity, it is retrieved
    as part of a Table entity.

    Attributes:
        name (str):
            The name of the index.
        type_ (str):
            Type of index, for example B-TREE.
        table_columns (MutableSequence[str]):
            Table columns used as part of the Index, for
            example B-TREE index should list the columns
            which constitutes the index.
        unique (bool):
            Boolean value indicating whether the index is
            unique.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    unique: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )


class TriggerEntity(proto.Message):
    r"""Trigger is not used as an independent entity, it is retrieved
    as part of a Table entity.

    Attributes:
        name (str):
            The name of the trigger.
        triggering_events (MutableSequence[str]):
            The DML, DDL, or database events that fire
            the trigger, for example INSERT, UPDATE.
        trigger_type (str):
            Indicates when the trigger fires, for example
            BEFORE STATEMENT, AFTER EACH ROW.
        sql_code (str):
            The SQL code which creates the trigger.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    triggering_events: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    trigger_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    sql_code: str = proto.Field(
        proto.STRING,
        number=4,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )


class ViewEntity(proto.Message):
    r"""View's parent is a schema.

    Attributes:
        sql_code (str):
            The SQL code which creates the view.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
        constraints (MutableSequence[google.cloud.clouddms_v1.types.ConstraintEntity]):
            View constraints.
    """

    sql_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )
    constraints: MutableSequence["ConstraintEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ConstraintEntity",
    )


class SequenceEntity(proto.Message):
    r"""Sequence's parent is a schema.

    Attributes:
        increment (int):
            Increment value for the sequence.
        start_value (bytes):
            Start number for the sequence represented as
            bytes to accommodate large. numbers
        max_value (bytes):
            Maximum number for the sequence represented
            as bytes to accommodate large. numbers
        min_value (bytes):
            Minimum number for the sequence represented
            as bytes to accommodate large. numbers
        cycle (bool):
            Indicates whether the sequence value should
            cycle through.
        cache (int):
            Indicates number of entries to cache /
            precreate.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    increment: int = proto.Field(
        proto.INT64,
        number=1,
    )
    start_value: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    max_value: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )
    min_value: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )
    cycle: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    cache: int = proto.Field(
        proto.INT64,
        number=6,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=7,
        message=struct_pb2.Struct,
    )


class StoredProcedureEntity(proto.Message):
    r"""Stored procedure's parent is a schema.

    Attributes:
        sql_code (str):
            The SQL code which creates the stored
            procedure.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    sql_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )


class FunctionEntity(proto.Message):
    r"""Function's parent is a schema.

    Attributes:
        sql_code (str):
            The SQL code which creates the function.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    sql_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )


class SynonymEntity(proto.Message):
    r"""Synonym's parent is a schema.

    Attributes:
        source_entity (str):
            The name of the entity for which the synonym
            is being created (the source).
        source_type (google.cloud.clouddms_v1.types.DatabaseEntityType):
            The type of the entity for which the synonym
            is being created (usually a table or a
            sequence).
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    source_entity: str = proto.Field(
        proto.STRING,
        number=1,
    )
    source_type: "DatabaseEntityType" = proto.Field(
        proto.ENUM,
        number=2,
        enum="DatabaseEntityType",
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )


class PackageEntity(proto.Message):
    r"""Package's parent is a schema.

    Attributes:
        package_sql_code (str):
            The SQL code which creates the package.
        package_body (str):
            The SQL code which creates the package body.
            If the package specification has cursors or
            subprograms, then the package body is mandatory.
        custom_features (google.protobuf.struct_pb2.Struct):
            Custom engine specific features.
    """

    package_sql_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    package_body: str = proto.Field(
        proto.STRING,
        number=2,
    )
    custom_features: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )


class EntityMapping(proto.Message):
    r"""Details of the mappings of a database entity.

    Attributes:
        source_entity (str):
            Source entity full name.
            The source entity can also be a column, index or
            constraint using the same naming notation
            schema.table.column.
        draft_entity (str):
            Target entity full name.
            The draft entity can also include a column,
            index or constraint using the same naming
            notation schema.table.column.
        source_type (google.cloud.clouddms_v1.types.DatabaseEntityType):
            Type of source entity.
        draft_type (google.cloud.clouddms_v1.types.DatabaseEntityType):
            Type of draft entity.
        mapping_log (MutableSequence[google.cloud.clouddms_v1.types.EntityMappingLogEntry]):
            Entity mapping log entries.
            Multiple rules can be effective and contribute
            changes to a converted entity, such as a rule
            can handle the entity name, another rule can
            handle an entity type. In addition, rules which
            did not change the entity are also logged along
            with the reason preventing them to do so.
    """

    source_entity: str = proto.Field(
        proto.STRING,
        number=1,
    )
    draft_entity: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_type: "DatabaseEntityType" = proto.Field(
        proto.ENUM,
        number=4,
        enum="DatabaseEntityType",
    )
    draft_type: "DatabaseEntityType" = proto.Field(
        proto.ENUM,
        number=5,
        enum="DatabaseEntityType",
    )
    mapping_log: MutableSequence["EntityMappingLogEntry"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="EntityMappingLogEntry",
    )


class EntityMappingLogEntry(proto.Message):
    r"""A single record of a rule which was used for a mapping.

    Attributes:
        rule_id (str):
            Which rule caused this log entry.
        rule_revision_id (str):
            Rule revision ID.
        mapping_comment (str):
            Comment.
    """

    rule_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rule_revision_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    mapping_comment: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
