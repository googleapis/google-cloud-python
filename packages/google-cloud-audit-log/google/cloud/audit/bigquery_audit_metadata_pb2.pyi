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

from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.iam.v1 import policy_pb2 as _policy_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.rpc import status_pb2 as _status_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class BigQueryAuditMetadata(_message.Message):
    __slots__ = [
        "dataset_change",
        "dataset_creation",
        "dataset_deletion",
        "first_party_app_metadata",
        "job_change",
        "job_deletion",
        "job_insertion",
        "model_creation",
        "model_data_change",
        "model_data_read",
        "model_deletion",
        "model_metadata_change",
        "routine_change",
        "routine_creation",
        "routine_deletion",
        "row_access_policy_change",
        "row_access_policy_creation",
        "row_access_policy_deletion",
        "table_change",
        "table_creation",
        "table_data_change",
        "table_data_read",
        "table_deletion",
        "unlink_dataset",
    ]
    class CreateDisposition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class JobState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class QueryStatementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class WriteDisposition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class BigQueryAcl(_message.Message):
        __slots__ = ["authorized_views", "policy"]
        AUTHORIZED_VIEWS_FIELD_NUMBER: _ClassVar[int]
        POLICY_FIELD_NUMBER: _ClassVar[int]
        authorized_views: _containers.RepeatedScalarFieldContainer[str]
        policy: _policy_pb2.Policy
        def __init__(
            self,
            policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...,
            authorized_views: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class Dataset(_message.Message):
        __slots__ = [
            "acl",
            "create_time",
            "dataset_info",
            "dataset_name",
            "default_collation",
            "default_encryption",
            "default_table_expire_duration",
            "update_time",
        ]
        ACL_FIELD_NUMBER: _ClassVar[int]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        DATASET_INFO_FIELD_NUMBER: _ClassVar[int]
        DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_COLLATION_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_TABLE_EXPIRE_DURATION_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        acl: BigQueryAuditMetadata.BigQueryAcl
        create_time: _timestamp_pb2.Timestamp
        dataset_info: BigQueryAuditMetadata.EntityInfo
        dataset_name: str
        default_collation: str
        default_encryption: BigQueryAuditMetadata.EncryptionInfo
        default_table_expire_duration: _duration_pb2.Duration
        update_time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            dataset_name: _Optional[str] = ...,
            dataset_info: _Optional[
                _Union[BigQueryAuditMetadata.EntityInfo, _Mapping]
            ] = ...,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            acl: _Optional[_Union[BigQueryAuditMetadata.BigQueryAcl, _Mapping]] = ...,
            default_table_expire_duration: _Optional[
                _Union[_duration_pb2.Duration, _Mapping]
            ] = ...,
            default_encryption: _Optional[
                _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
            ] = ...,
            default_collation: _Optional[str] = ...,
        ) -> None: ...

    class DatasetChange(_message.Message):
        __slots__ = ["dataset", "job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        DATASET_FIELD_NUMBER: _ClassVar[int]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.DatasetChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.DatasetChange.Reason
        SET_IAM_POLICY: BigQueryAuditMetadata.DatasetChange.Reason
        UPDATE: BigQueryAuditMetadata.DatasetChange.Reason
        dataset: BigQueryAuditMetadata.Dataset
        job_name: str
        reason: BigQueryAuditMetadata.DatasetChange.Reason
        def __init__(
            self,
            dataset: _Optional[_Union[BigQueryAuditMetadata.Dataset, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.DatasetChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class DatasetCreation(_message.Message):
        __slots__ = ["dataset", "job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        CREATE: BigQueryAuditMetadata.DatasetCreation.Reason
        DATASET_FIELD_NUMBER: _ClassVar[int]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.DatasetCreation.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.DatasetCreation.Reason
        dataset: BigQueryAuditMetadata.Dataset
        job_name: str
        reason: BigQueryAuditMetadata.DatasetCreation.Reason
        def __init__(
            self,
            dataset: _Optional[_Union[BigQueryAuditMetadata.Dataset, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.DatasetCreation.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class DatasetDeletion(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        DELETE: BigQueryAuditMetadata.DatasetDeletion.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.DatasetDeletion.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.DatasetDeletion.Reason
        job_name: str
        reason: BigQueryAuditMetadata.DatasetDeletion.Reason
        def __init__(
            self,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.DatasetDeletion.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class EncryptionInfo(_message.Message):
        __slots__ = ["kms_key_name"]
        KMS_KEY_NAME_FIELD_NUMBER: _ClassVar[int]
        kms_key_name: str
        def __init__(self, kms_key_name: _Optional[str] = ...) -> None: ...

    class EntityInfo(_message.Message):
        __slots__ = ["description", "friendly_name", "labels"]
        class LabelsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FRIENDLY_NAME_FIELD_NUMBER: _ClassVar[int]
        LABELS_FIELD_NUMBER: _ClassVar[int]
        description: str
        friendly_name: str
        labels: _containers.ScalarMap[str, str]
        def __init__(
            self,
            friendly_name: _Optional[str] = ...,
            description: _Optional[str] = ...,
            labels: _Optional[_Mapping[str, str]] = ...,
        ) -> None: ...

    class FirstPartyAppMetadata(_message.Message):
        __slots__ = ["sheets_metadata"]
        SHEETS_METADATA_FIELD_NUMBER: _ClassVar[int]
        sheets_metadata: BigQueryAuditMetadata.SheetsMetadata
        def __init__(
            self,
            sheets_metadata: _Optional[
                _Union[BigQueryAuditMetadata.SheetsMetadata, _Mapping]
            ] = ...,
        ) -> None: ...

    class Job(_message.Message):
        __slots__ = ["job_config", "job_name", "job_stats", "job_status"]
        JOB_CONFIG_FIELD_NUMBER: _ClassVar[int]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        JOB_STATS_FIELD_NUMBER: _ClassVar[int]
        JOB_STATUS_FIELD_NUMBER: _ClassVar[int]
        job_config: BigQueryAuditMetadata.JobConfig
        job_name: str
        job_stats: BigQueryAuditMetadata.JobStats
        job_status: BigQueryAuditMetadata.JobStatus
        def __init__(
            self,
            job_name: _Optional[str] = ...,
            job_config: _Optional[
                _Union[BigQueryAuditMetadata.JobConfig, _Mapping]
            ] = ...,
            job_status: _Optional[
                _Union[BigQueryAuditMetadata.JobStatus, _Mapping]
            ] = ...,
            job_stats: _Optional[
                _Union[BigQueryAuditMetadata.JobStats, _Mapping]
            ] = ...,
        ) -> None: ...

    class JobChange(_message.Message):
        __slots__ = ["after", "before", "job"]
        AFTER_FIELD_NUMBER: _ClassVar[int]
        BEFORE_FIELD_NUMBER: _ClassVar[int]
        JOB_FIELD_NUMBER: _ClassVar[int]
        after: BigQueryAuditMetadata.JobState
        before: BigQueryAuditMetadata.JobState
        job: BigQueryAuditMetadata.Job
        def __init__(
            self,
            before: _Optional[_Union[BigQueryAuditMetadata.JobState, str]] = ...,
            after: _Optional[_Union[BigQueryAuditMetadata.JobState, str]] = ...,
            job: _Optional[_Union[BigQueryAuditMetadata.Job, _Mapping]] = ...,
        ) -> None: ...

    class JobConfig(_message.Message):
        __slots__ = [
            "extract_config",
            "labels",
            "load_config",
            "query_config",
            "table_copy_config",
            "type",
        ]
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        class Extract(_message.Message):
            __slots__ = [
                "destination_uris",
                "destination_uris_truncated",
                "source_model",
                "source_table",
            ]
            DESTINATION_URIS_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_URIS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
            SOURCE_MODEL_FIELD_NUMBER: _ClassVar[int]
            SOURCE_TABLE_FIELD_NUMBER: _ClassVar[int]
            destination_uris: _containers.RepeatedScalarFieldContainer[str]
            destination_uris_truncated: bool
            source_model: str
            source_table: str
            def __init__(
                self,
                destination_uris: _Optional[_Iterable[str]] = ...,
                destination_uris_truncated: bool = ...,
                source_table: _Optional[str] = ...,
                source_model: _Optional[str] = ...,
            ) -> None: ...

        class LabelsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        class Load(_message.Message):
            __slots__ = [
                "create_disposition",
                "destination_table",
                "destination_table_encryption",
                "schema_json",
                "schema_json_truncated",
                "source_uris",
                "source_uris_truncated",
                "write_disposition",
            ]
            CREATE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
            SCHEMA_JSON_FIELD_NUMBER: _ClassVar[int]
            SCHEMA_JSON_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
            SOURCE_URIS_FIELD_NUMBER: _ClassVar[int]
            SOURCE_URIS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
            WRITE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            create_disposition: BigQueryAuditMetadata.CreateDisposition
            destination_table: str
            destination_table_encryption: BigQueryAuditMetadata.EncryptionInfo
            schema_json: str
            schema_json_truncated: bool
            source_uris: _containers.RepeatedScalarFieldContainer[str]
            source_uris_truncated: bool
            write_disposition: BigQueryAuditMetadata.WriteDisposition
            def __init__(
                self,
                source_uris: _Optional[_Iterable[str]] = ...,
                source_uris_truncated: bool = ...,
                schema_json: _Optional[str] = ...,
                schema_json_truncated: bool = ...,
                destination_table: _Optional[str] = ...,
                create_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.CreateDisposition, str]
                ] = ...,
                write_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.WriteDisposition, str]
                ] = ...,
                destination_table_encryption: _Optional[
                    _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
                ] = ...,
            ) -> None: ...

        class Query(_message.Message):
            __slots__ = [
                "create_disposition",
                "default_dataset",
                "destination_table",
                "destination_table_encryption",
                "priority",
                "query",
                "query_truncated",
                "statement_type",
                "table_definitions",
                "write_disposition",
            ]
            class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = []

            CREATE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            DEFAULT_DATASET_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
            PRIORITY_FIELD_NUMBER: _ClassVar[int]
            PRIORITY_UNSPECIFIED: BigQueryAuditMetadata.JobConfig.Query.Priority
            QUERY_BATCH: BigQueryAuditMetadata.JobConfig.Query.Priority
            QUERY_FIELD_NUMBER: _ClassVar[int]
            QUERY_INTERACTIVE: BigQueryAuditMetadata.JobConfig.Query.Priority
            QUERY_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
            STATEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
            TABLE_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
            WRITE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            create_disposition: BigQueryAuditMetadata.CreateDisposition
            default_dataset: str
            destination_table: str
            destination_table_encryption: BigQueryAuditMetadata.EncryptionInfo
            priority: BigQueryAuditMetadata.JobConfig.Query.Priority
            query: str
            query_truncated: bool
            statement_type: BigQueryAuditMetadata.QueryStatementType
            table_definitions: _containers.RepeatedCompositeFieldContainer[
                BigQueryAuditMetadata.TableDefinition
            ]
            write_disposition: BigQueryAuditMetadata.WriteDisposition
            def __init__(
                self,
                query: _Optional[str] = ...,
                query_truncated: bool = ...,
                destination_table: _Optional[str] = ...,
                create_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.CreateDisposition, str]
                ] = ...,
                write_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.WriteDisposition, str]
                ] = ...,
                default_dataset: _Optional[str] = ...,
                table_definitions: _Optional[
                    _Iterable[_Union[BigQueryAuditMetadata.TableDefinition, _Mapping]]
                ] = ...,
                priority: _Optional[
                    _Union[BigQueryAuditMetadata.JobConfig.Query.Priority, str]
                ] = ...,
                destination_table_encryption: _Optional[
                    _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
                ] = ...,
                statement_type: _Optional[
                    _Union[BigQueryAuditMetadata.QueryStatementType, str]
                ] = ...,
            ) -> None: ...

        class TableCopy(_message.Message):
            __slots__ = [
                "create_disposition",
                "destination_expiration_time",
                "destination_table",
                "destination_table_encryption",
                "operation_type",
                "source_tables",
                "source_tables_truncated",
                "write_disposition",
            ]
            CREATE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_EXPIRATION_TIME_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
            DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
            OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
            SOURCE_TABLES_FIELD_NUMBER: _ClassVar[int]
            SOURCE_TABLES_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
            WRITE_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
            create_disposition: BigQueryAuditMetadata.CreateDisposition
            destination_expiration_time: _timestamp_pb2.Timestamp
            destination_table: str
            destination_table_encryption: BigQueryAuditMetadata.EncryptionInfo
            operation_type: BigQueryAuditMetadata.OperationType
            source_tables: _containers.RepeatedScalarFieldContainer[str]
            source_tables_truncated: bool
            write_disposition: BigQueryAuditMetadata.WriteDisposition
            def __init__(
                self,
                source_tables: _Optional[_Iterable[str]] = ...,
                source_tables_truncated: bool = ...,
                destination_table: _Optional[str] = ...,
                create_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.CreateDisposition, str]
                ] = ...,
                write_disposition: _Optional[
                    _Union[BigQueryAuditMetadata.WriteDisposition, str]
                ] = ...,
                destination_table_encryption: _Optional[
                    _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
                ] = ...,
                operation_type: _Optional[
                    _Union[BigQueryAuditMetadata.OperationType, str]
                ] = ...,
                destination_expiration_time: _Optional[
                    _Union[_timestamp_pb2.Timestamp, _Mapping]
                ] = ...,
            ) -> None: ...

        COPY: BigQueryAuditMetadata.JobConfig.Type
        EXPORT: BigQueryAuditMetadata.JobConfig.Type
        EXTRACT_CONFIG_FIELD_NUMBER: _ClassVar[int]
        IMPORT: BigQueryAuditMetadata.JobConfig.Type
        LABELS_FIELD_NUMBER: _ClassVar[int]
        LOAD_CONFIG_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.JobConfig.Type
        QUERY_CONFIG_FIELD_NUMBER: _ClassVar[int]
        TABLE_COPY_CONFIG_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TYPE_UNSPECIFIED: BigQueryAuditMetadata.JobConfig.Type
        extract_config: BigQueryAuditMetadata.JobConfig.Extract
        labels: _containers.ScalarMap[str, str]
        load_config: BigQueryAuditMetadata.JobConfig.Load
        query_config: BigQueryAuditMetadata.JobConfig.Query
        table_copy_config: BigQueryAuditMetadata.JobConfig.TableCopy
        type: BigQueryAuditMetadata.JobConfig.Type
        def __init__(
            self,
            type: _Optional[_Union[BigQueryAuditMetadata.JobConfig.Type, str]] = ...,
            query_config: _Optional[
                _Union[BigQueryAuditMetadata.JobConfig.Query, _Mapping]
            ] = ...,
            load_config: _Optional[
                _Union[BigQueryAuditMetadata.JobConfig.Load, _Mapping]
            ] = ...,
            extract_config: _Optional[
                _Union[BigQueryAuditMetadata.JobConfig.Extract, _Mapping]
            ] = ...,
            table_copy_config: _Optional[
                _Union[BigQueryAuditMetadata.JobConfig.TableCopy, _Mapping]
            ] = ...,
            labels: _Optional[_Mapping[str, str]] = ...,
        ) -> None: ...

    class JobDeletion(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_DELETE_REQUEST: BigQueryAuditMetadata.JobDeletion.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.JobDeletion.Reason
        job_name: str
        reason: BigQueryAuditMetadata.JobDeletion.Reason
        def __init__(
            self,
            job_name: _Optional[str] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.JobDeletion.Reason, str]
            ] = ...,
        ) -> None: ...

    class JobInsertion(_message.Message):
        __slots__ = ["job", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_FIELD_NUMBER: _ClassVar[int]
        JOB_INSERT_REQUEST: BigQueryAuditMetadata.JobInsertion.Reason
        QUERY_REQUEST: BigQueryAuditMetadata.JobInsertion.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.JobInsertion.Reason
        job: BigQueryAuditMetadata.Job
        reason: BigQueryAuditMetadata.JobInsertion.Reason
        def __init__(
            self,
            job: _Optional[_Union[BigQueryAuditMetadata.Job, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.JobInsertion.Reason, str]
            ] = ...,
        ) -> None: ...

    class JobStats(_message.Message):
        __slots__ = [
            "create_time",
            "end_time",
            "extract_stats",
            "load_stats",
            "parent_job_name",
            "query_stats",
            "reservation",
            "reservation_usage",
            "start_time",
            "total_slot_ms",
        ]
        class Extract(_message.Message):
            __slots__ = ["total_input_bytes"]
            TOTAL_INPUT_BYTES_FIELD_NUMBER: _ClassVar[int]
            total_input_bytes: int
            def __init__(self, total_input_bytes: _Optional[int] = ...) -> None: ...

        class Load(_message.Message):
            __slots__ = ["total_output_bytes"]
            TOTAL_OUTPUT_BYTES_FIELD_NUMBER: _ClassVar[int]
            total_output_bytes: int
            def __init__(self, total_output_bytes: _Optional[int] = ...) -> None: ...

        class Query(_message.Message):
            __slots__ = [
                "billing_tier",
                "cache_hit",
                "output_row_count",
                "referenced_routines",
                "referenced_tables",
                "referenced_views",
                "total_billed_bytes",
                "total_processed_bytes",
            ]
            BILLING_TIER_FIELD_NUMBER: _ClassVar[int]
            CACHE_HIT_FIELD_NUMBER: _ClassVar[int]
            OUTPUT_ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
            REFERENCED_ROUTINES_FIELD_NUMBER: _ClassVar[int]
            REFERENCED_TABLES_FIELD_NUMBER: _ClassVar[int]
            REFERENCED_VIEWS_FIELD_NUMBER: _ClassVar[int]
            TOTAL_BILLED_BYTES_FIELD_NUMBER: _ClassVar[int]
            TOTAL_PROCESSED_BYTES_FIELD_NUMBER: _ClassVar[int]
            billing_tier: int
            cache_hit: bool
            output_row_count: int
            referenced_routines: _containers.RepeatedScalarFieldContainer[str]
            referenced_tables: _containers.RepeatedScalarFieldContainer[str]
            referenced_views: _containers.RepeatedScalarFieldContainer[str]
            total_billed_bytes: int
            total_processed_bytes: int
            def __init__(
                self,
                total_processed_bytes: _Optional[int] = ...,
                total_billed_bytes: _Optional[int] = ...,
                billing_tier: _Optional[int] = ...,
                referenced_tables: _Optional[_Iterable[str]] = ...,
                referenced_views: _Optional[_Iterable[str]] = ...,
                referenced_routines: _Optional[_Iterable[str]] = ...,
                output_row_count: _Optional[int] = ...,
                cache_hit: bool = ...,
            ) -> None: ...

        class ReservationResourceUsage(_message.Message):
            __slots__ = ["name", "slot_ms"]
            NAME_FIELD_NUMBER: _ClassVar[int]
            SLOT_MS_FIELD_NUMBER: _ClassVar[int]
            name: str
            slot_ms: int
            def __init__(
                self, name: _Optional[str] = ..., slot_ms: _Optional[int] = ...
            ) -> None: ...

        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        EXTRACT_STATS_FIELD_NUMBER: _ClassVar[int]
        LOAD_STATS_FIELD_NUMBER: _ClassVar[int]
        PARENT_JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY_STATS_FIELD_NUMBER: _ClassVar[int]
        RESERVATION_FIELD_NUMBER: _ClassVar[int]
        RESERVATION_USAGE_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        TOTAL_SLOT_MS_FIELD_NUMBER: _ClassVar[int]
        create_time: _timestamp_pb2.Timestamp
        end_time: _timestamp_pb2.Timestamp
        extract_stats: BigQueryAuditMetadata.JobStats.Extract
        load_stats: BigQueryAuditMetadata.JobStats.Load
        parent_job_name: str
        query_stats: BigQueryAuditMetadata.JobStats.Query
        reservation: str
        reservation_usage: _containers.RepeatedCompositeFieldContainer[
            BigQueryAuditMetadata.JobStats.ReservationResourceUsage
        ]
        start_time: _timestamp_pb2.Timestamp
        total_slot_ms: int
        def __init__(
            self,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            query_stats: _Optional[
                _Union[BigQueryAuditMetadata.JobStats.Query, _Mapping]
            ] = ...,
            load_stats: _Optional[
                _Union[BigQueryAuditMetadata.JobStats.Load, _Mapping]
            ] = ...,
            extract_stats: _Optional[
                _Union[BigQueryAuditMetadata.JobStats.Extract, _Mapping]
            ] = ...,
            total_slot_ms: _Optional[int] = ...,
            reservation_usage: _Optional[
                _Iterable[
                    _Union[
                        BigQueryAuditMetadata.JobStats.ReservationResourceUsage,
                        _Mapping,
                    ]
                ]
            ] = ...,
            reservation: _Optional[str] = ...,
            parent_job_name: _Optional[str] = ...,
        ) -> None: ...

    class JobStatus(_message.Message):
        __slots__ = ["error_result", "errors", "job_state"]
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        ERROR_RESULT_FIELD_NUMBER: _ClassVar[int]
        JOB_STATE_FIELD_NUMBER: _ClassVar[int]
        error_result: _status_pb2.Status
        errors: _containers.RepeatedCompositeFieldContainer[_status_pb2.Status]
        job_state: BigQueryAuditMetadata.JobState
        def __init__(
            self,
            job_state: _Optional[_Union[BigQueryAuditMetadata.JobState, str]] = ...,
            error_result: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...,
            errors: _Optional[_Iterable[_Union[_status_pb2.Status, _Mapping]]] = ...,
        ) -> None: ...

    class Model(_message.Message):
        __slots__ = [
            "create_time",
            "encryption",
            "expire_time",
            "model_info",
            "model_name",
            "update_time",
        ]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
        EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
        MODEL_INFO_FIELD_NUMBER: _ClassVar[int]
        MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        create_time: _timestamp_pb2.Timestamp
        encryption: BigQueryAuditMetadata.EncryptionInfo
        expire_time: _timestamp_pb2.Timestamp
        model_info: BigQueryAuditMetadata.EntityInfo
        model_name: str
        update_time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            model_name: _Optional[str] = ...,
            model_info: _Optional[
                _Union[BigQueryAuditMetadata.EntityInfo, _Mapping]
            ] = ...,
            expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            encryption: _Optional[
                _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
            ] = ...,
        ) -> None: ...

    class ModelCreation(_message.Message):
        __slots__ = ["job_name", "model", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        MODEL_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.ModelCreation.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.ModelCreation.Reason
        job_name: str
        model: BigQueryAuditMetadata.Model
        reason: BigQueryAuditMetadata.ModelCreation.Reason
        def __init__(
            self,
            model: _Optional[_Union[BigQueryAuditMetadata.Model, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.ModelCreation.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class ModelDataChange(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.ModelDataChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.ModelDataChange.Reason
        job_name: str
        reason: BigQueryAuditMetadata.ModelDataChange.Reason
        def __init__(
            self,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.ModelDataChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class ModelDataRead(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB: BigQueryAuditMetadata.ModelDataRead.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.ModelDataRead.Reason
        job_name: str
        reason: BigQueryAuditMetadata.ModelDataRead.Reason
        def __init__(
            self,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.ModelDataRead.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class ModelDeletion(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        EXPIRED: BigQueryAuditMetadata.ModelDeletion.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        MODEL_DELETE_REQUEST: BigQueryAuditMetadata.ModelDeletion.Reason
        QUERY: BigQueryAuditMetadata.ModelDeletion.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.ModelDeletion.Reason
        job_name: str
        reason: BigQueryAuditMetadata.ModelDeletion.Reason
        def __init__(
            self,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.ModelDeletion.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class ModelMetadataChange(_message.Message):
        __slots__ = ["job_name", "model", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        MODEL_FIELD_NUMBER: _ClassVar[int]
        MODEL_PATCH_REQUEST: BigQueryAuditMetadata.ModelMetadataChange.Reason
        QUERY: BigQueryAuditMetadata.ModelMetadataChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.ModelMetadataChange.Reason
        job_name: str
        model: BigQueryAuditMetadata.Model
        reason: BigQueryAuditMetadata.ModelMetadataChange.Reason
        def __init__(
            self,
            model: _Optional[_Union[BigQueryAuditMetadata.Model, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.ModelMetadataChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class Routine(_message.Message):
        __slots__ = ["create_time", "routine_name", "update_time"]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        ROUTINE_NAME_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        create_time: _timestamp_pb2.Timestamp
        routine_name: str
        update_time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            routine_name: _Optional[str] = ...,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ) -> None: ...

    class RoutineChange(_message.Message):
        __slots__ = ["job_name", "reason", "routine"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.RoutineChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.RoutineChange.Reason
        ROUTINE_FIELD_NUMBER: _ClassVar[int]
        ROUTINE_UPDATE_REQUEST: BigQueryAuditMetadata.RoutineChange.Reason
        job_name: str
        reason: BigQueryAuditMetadata.RoutineChange.Reason
        routine: BigQueryAuditMetadata.Routine
        def __init__(
            self,
            routine: _Optional[_Union[BigQueryAuditMetadata.Routine, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.RoutineChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class RoutineCreation(_message.Message):
        __slots__ = ["job_name", "reason", "routine"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.RoutineCreation.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.RoutineCreation.Reason
        ROUTINE_FIELD_NUMBER: _ClassVar[int]
        ROUTINE_INSERT_REQUEST: BigQueryAuditMetadata.RoutineCreation.Reason
        job_name: str
        reason: BigQueryAuditMetadata.RoutineCreation.Reason
        routine: BigQueryAuditMetadata.Routine
        def __init__(
            self,
            routine: _Optional[_Union[BigQueryAuditMetadata.Routine, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.RoutineCreation.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class RoutineDeletion(_message.Message):
        __slots__ = ["job_name", "reason", "routine"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.RoutineDeletion.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.RoutineDeletion.Reason
        ROUTINE_DELETE_REQUEST: BigQueryAuditMetadata.RoutineDeletion.Reason
        ROUTINE_FIELD_NUMBER: _ClassVar[int]
        job_name: str
        reason: BigQueryAuditMetadata.RoutineDeletion.Reason
        routine: BigQueryAuditMetadata.Routine
        def __init__(
            self,
            routine: _Optional[_Union[BigQueryAuditMetadata.Routine, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.RoutineDeletion.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class RowAccessPolicy(_message.Message):
        __slots__ = ["row_access_policy_name"]
        ROW_ACCESS_POLICY_NAME_FIELD_NUMBER: _ClassVar[int]
        row_access_policy_name: str
        def __init__(self, row_access_policy_name: _Optional[str] = ...) -> None: ...

    class RowAccessPolicyChange(_message.Message):
        __slots__ = ["job_name", "row_access_policy"]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        ROW_ACCESS_POLICY_FIELD_NUMBER: _ClassVar[int]
        job_name: str
        row_access_policy: BigQueryAuditMetadata.RowAccessPolicy
        def __init__(
            self,
            row_access_policy: _Optional[
                _Union[BigQueryAuditMetadata.RowAccessPolicy, _Mapping]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class RowAccessPolicyCreation(_message.Message):
        __slots__ = ["job_name", "row_access_policy"]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        ROW_ACCESS_POLICY_FIELD_NUMBER: _ClassVar[int]
        job_name: str
        row_access_policy: BigQueryAuditMetadata.RowAccessPolicy
        def __init__(
            self,
            row_access_policy: _Optional[
                _Union[BigQueryAuditMetadata.RowAccessPolicy, _Mapping]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class RowAccessPolicyDeletion(_message.Message):
        __slots__ = [
            "all_row_access_policies_dropped",
            "job_name",
            "row_access_policies",
        ]
        ALL_ROW_ACCESS_POLICIES_DROPPED_FIELD_NUMBER: _ClassVar[int]
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        ROW_ACCESS_POLICIES_FIELD_NUMBER: _ClassVar[int]
        all_row_access_policies_dropped: bool
        job_name: str
        row_access_policies: _containers.RepeatedCompositeFieldContainer[
            BigQueryAuditMetadata.RowAccessPolicy
        ]
        def __init__(
            self,
            row_access_policies: _Optional[
                _Iterable[_Union[BigQueryAuditMetadata.RowAccessPolicy, _Mapping]]
            ] = ...,
            job_name: _Optional[str] = ...,
            all_row_access_policies_dropped: bool = ...,
        ) -> None: ...

    class SheetsMetadata(_message.Message):
        __slots__ = ["doc_id"]
        DOC_ID_FIELD_NUMBER: _ClassVar[int]
        doc_id: str
        def __init__(self, doc_id: _Optional[str] = ...) -> None: ...

    class Table(_message.Message):
        __slots__ = [
            "create_time",
            "encryption",
            "expire_time",
            "schema_json",
            "schema_json_truncated",
            "table_info",
            "table_name",
            "truncate_time",
            "update_time",
            "view",
        ]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
        EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_JSON_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_JSON_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        TABLE_INFO_FIELD_NUMBER: _ClassVar[int]
        TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
        TRUNCATE_TIME_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        VIEW_FIELD_NUMBER: _ClassVar[int]
        create_time: _timestamp_pb2.Timestamp
        encryption: BigQueryAuditMetadata.EncryptionInfo
        expire_time: _timestamp_pb2.Timestamp
        schema_json: str
        schema_json_truncated: bool
        table_info: BigQueryAuditMetadata.EntityInfo
        table_name: str
        truncate_time: _timestamp_pb2.Timestamp
        update_time: _timestamp_pb2.Timestamp
        view: BigQueryAuditMetadata.TableViewDefinition
        def __init__(
            self,
            table_name: _Optional[str] = ...,
            table_info: _Optional[
                _Union[BigQueryAuditMetadata.EntityInfo, _Mapping]
            ] = ...,
            schema_json: _Optional[str] = ...,
            schema_json_truncated: bool = ...,
            view: _Optional[
                _Union[BigQueryAuditMetadata.TableViewDefinition, _Mapping]
            ] = ...,
            expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            truncate_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            encryption: _Optional[
                _Union[BigQueryAuditMetadata.EncryptionInfo, _Mapping]
            ] = ...,
        ) -> None: ...

    class TableChange(_message.Message):
        __slots__ = ["job_name", "reason", "table", "truncated"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB: BigQueryAuditMetadata.TableChange.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.TableChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.TableChange.Reason
        TABLE_FIELD_NUMBER: _ClassVar[int]
        TABLE_UPDATE_REQUEST: BigQueryAuditMetadata.TableChange.Reason
        TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        job_name: str
        reason: BigQueryAuditMetadata.TableChange.Reason
        table: BigQueryAuditMetadata.Table
        truncated: bool
        def __init__(
            self,
            table: _Optional[_Union[BigQueryAuditMetadata.Table, _Mapping]] = ...,
            truncated: bool = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.TableChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class TableCreation(_message.Message):
        __slots__ = ["job_name", "reason", "table"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        JOB: BigQueryAuditMetadata.TableCreation.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.TableCreation.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.TableCreation.Reason
        TABLE_FIELD_NUMBER: _ClassVar[int]
        TABLE_INSERT_REQUEST: BigQueryAuditMetadata.TableCreation.Reason
        job_name: str
        reason: BigQueryAuditMetadata.TableCreation.Reason
        table: BigQueryAuditMetadata.Table
        def __init__(
            self,
            table: _Optional[_Union[BigQueryAuditMetadata.Table, _Mapping]] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.TableCreation.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class TableDataChange(_message.Message):
        __slots__ = [
            "deleted_rows_count",
            "inserted_rows_count",
            "job_name",
            "reason",
            "stream_name",
            "truncated",
        ]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        DELETED_ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
        INSERTED_ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
        JOB: BigQueryAuditMetadata.TableDataChange.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        MATERIALIZED_VIEW_REFRESH: BigQueryAuditMetadata.TableDataChange.Reason
        QUERY: BigQueryAuditMetadata.TableDataChange.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.TableDataChange.Reason
        STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        WRITE_API: BigQueryAuditMetadata.TableDataChange.Reason
        deleted_rows_count: int
        inserted_rows_count: int
        job_name: str
        reason: BigQueryAuditMetadata.TableDataChange.Reason
        stream_name: str
        truncated: bool
        def __init__(
            self,
            deleted_rows_count: _Optional[int] = ...,
            inserted_rows_count: _Optional[int] = ...,
            truncated: bool = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.TableDataChange.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
            stream_name: _Optional[str] = ...,
        ) -> None: ...

    class TableDataRead(_message.Message):
        __slots__ = [
            "fields",
            "fields_truncated",
            "job_name",
            "policy_tags",
            "policy_tags_truncated",
            "reason",
            "session_name",
        ]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        CREATE_READ_SESSION: BigQueryAuditMetadata.TableDataRead.Reason
        FIELDS_FIELD_NUMBER: _ClassVar[int]
        FIELDS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        GET_QUERY_RESULTS_REQUEST: BigQueryAuditMetadata.TableDataRead.Reason
        JOB: BigQueryAuditMetadata.TableDataRead.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        MATERIALIZED_VIEW_REFRESH: BigQueryAuditMetadata.TableDataRead.Reason
        POLICY_TAGS_FIELD_NUMBER: _ClassVar[int]
        POLICY_TAGS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        QUERY_REQUEST: BigQueryAuditMetadata.TableDataRead.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.TableDataRead.Reason
        SESSION_NAME_FIELD_NUMBER: _ClassVar[int]
        TABLEDATA_LIST_REQUEST: BigQueryAuditMetadata.TableDataRead.Reason
        fields: _containers.RepeatedScalarFieldContainer[str]
        fields_truncated: bool
        job_name: str
        policy_tags: _containers.RepeatedScalarFieldContainer[str]
        policy_tags_truncated: bool
        reason: BigQueryAuditMetadata.TableDataRead.Reason
        session_name: str
        def __init__(
            self,
            fields: _Optional[_Iterable[str]] = ...,
            fields_truncated: bool = ...,
            policy_tags: _Optional[_Iterable[str]] = ...,
            policy_tags_truncated: bool = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.TableDataRead.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
            session_name: _Optional[str] = ...,
        ) -> None: ...

    class TableDefinition(_message.Message):
        __slots__ = ["name", "source_uris"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SOURCE_URIS_FIELD_NUMBER: _ClassVar[int]
        name: str
        source_uris: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            name: _Optional[str] = ...,
            source_uris: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class TableDeletion(_message.Message):
        __slots__ = ["job_name", "reason"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        EXPIRED: BigQueryAuditMetadata.TableDeletion.Reason
        JOB_NAME_FIELD_NUMBER: _ClassVar[int]
        QUERY: BigQueryAuditMetadata.TableDeletion.Reason
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.TableDeletion.Reason
        TABLE_DELETE_REQUEST: BigQueryAuditMetadata.TableDeletion.Reason
        job_name: str
        reason: BigQueryAuditMetadata.TableDeletion.Reason
        def __init__(
            self,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.TableDeletion.Reason, str]
            ] = ...,
            job_name: _Optional[str] = ...,
        ) -> None: ...

    class TableViewDefinition(_message.Message):
        __slots__ = ["query", "query_truncated"]
        QUERY_FIELD_NUMBER: _ClassVar[int]
        QUERY_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
        query: str
        query_truncated: bool
        def __init__(
            self, query: _Optional[str] = ..., query_truncated: bool = ...
        ) -> None: ...

    class UnlinkDataset(_message.Message):
        __slots__ = ["linked_dataset", "reason", "source_dataset"]
        class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        LINKED_DATASET_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        REASON_UNSPECIFIED: BigQueryAuditMetadata.UnlinkDataset.Reason
        SOURCE_DATASET_FIELD_NUMBER: _ClassVar[int]
        UNLINK_API: BigQueryAuditMetadata.UnlinkDataset.Reason
        linked_dataset: str
        reason: BigQueryAuditMetadata.UnlinkDataset.Reason
        source_dataset: str
        def __init__(
            self,
            linked_dataset: _Optional[str] = ...,
            source_dataset: _Optional[str] = ...,
            reason: _Optional[
                _Union[BigQueryAuditMetadata.UnlinkDataset.Reason, str]
            ] = ...,
        ) -> None: ...

    ALTER_MATERIALIZED_VIEW: BigQueryAuditMetadata.QueryStatementType
    ALTER_SCHEMA: BigQueryAuditMetadata.QueryStatementType
    ALTER_TABLE: BigQueryAuditMetadata.QueryStatementType
    ALTER_VIEW: BigQueryAuditMetadata.QueryStatementType
    ASSERT: BigQueryAuditMetadata.QueryStatementType
    CALL: BigQueryAuditMetadata.QueryStatementType
    COPY: BigQueryAuditMetadata.OperationType
    CREATE_DISPOSITION_UNSPECIFIED: BigQueryAuditMetadata.CreateDisposition
    CREATE_EXTERNAL_TABLE: BigQueryAuditMetadata.QueryStatementType
    CREATE_FUNCTION: BigQueryAuditMetadata.QueryStatementType
    CREATE_IF_NEEDED: BigQueryAuditMetadata.CreateDisposition
    CREATE_MATERIALIZED_VIEW: BigQueryAuditMetadata.QueryStatementType
    CREATE_MODEL: BigQueryAuditMetadata.QueryStatementType
    CREATE_NEVER: BigQueryAuditMetadata.CreateDisposition
    CREATE_PROCEDURE: BigQueryAuditMetadata.QueryStatementType
    CREATE_ROW_ACCESS_POLICY: BigQueryAuditMetadata.QueryStatementType
    CREATE_SCHEMA: BigQueryAuditMetadata.QueryStatementType
    CREATE_SNAPSHOT_TABLE: BigQueryAuditMetadata.QueryStatementType
    CREATE_TABLE: BigQueryAuditMetadata.QueryStatementType
    CREATE_TABLE_AS_SELECT: BigQueryAuditMetadata.QueryStatementType
    CREATE_TABLE_FUNCTION: BigQueryAuditMetadata.QueryStatementType
    CREATE_VIEW: BigQueryAuditMetadata.QueryStatementType
    DATASET_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DATASET_CREATION_FIELD_NUMBER: _ClassVar[int]
    DATASET_DELETION_FIELD_NUMBER: _ClassVar[int]
    DELETE: BigQueryAuditMetadata.QueryStatementType
    DONE: BigQueryAuditMetadata.JobState
    DROP_EXTERNAL_TABLE: BigQueryAuditMetadata.QueryStatementType
    DROP_FUNCTION: BigQueryAuditMetadata.QueryStatementType
    DROP_MATERIALIZED_VIEW: BigQueryAuditMetadata.QueryStatementType
    DROP_MODEL: BigQueryAuditMetadata.QueryStatementType
    DROP_PROCEDURE: BigQueryAuditMetadata.QueryStatementType
    DROP_ROW_ACCESS_POLICY: BigQueryAuditMetadata.QueryStatementType
    DROP_SCHEMA: BigQueryAuditMetadata.QueryStatementType
    DROP_SNAPSHOT_TABLE: BigQueryAuditMetadata.QueryStatementType
    DROP_TABLE: BigQueryAuditMetadata.QueryStatementType
    DROP_VIEW: BigQueryAuditMetadata.QueryStatementType
    EXPORT_DATA: BigQueryAuditMetadata.QueryStatementType
    FIRST_PARTY_APP_METADATA_FIELD_NUMBER: _ClassVar[int]
    INSERT: BigQueryAuditMetadata.QueryStatementType
    JOB_CHANGE_FIELD_NUMBER: _ClassVar[int]
    JOB_DELETION_FIELD_NUMBER: _ClassVar[int]
    JOB_INSERTION_FIELD_NUMBER: _ClassVar[int]
    JOB_STATE_UNSPECIFIED: BigQueryAuditMetadata.JobState
    MERGE: BigQueryAuditMetadata.QueryStatementType
    MODEL_CREATION_FIELD_NUMBER: _ClassVar[int]
    MODEL_DATA_CHANGE_FIELD_NUMBER: _ClassVar[int]
    MODEL_DATA_READ_FIELD_NUMBER: _ClassVar[int]
    MODEL_DELETION_FIELD_NUMBER: _ClassVar[int]
    MODEL_METADATA_CHANGE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPE_UNSPECIFIED: BigQueryAuditMetadata.OperationType
    PENDING: BigQueryAuditMetadata.JobState
    QUERY_STATEMENT_TYPE_UNSPECIFIED: BigQueryAuditMetadata.QueryStatementType
    RESTORE: BigQueryAuditMetadata.OperationType
    ROUTINE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ROUTINE_CREATION_FIELD_NUMBER: _ClassVar[int]
    ROUTINE_DELETION_FIELD_NUMBER: _ClassVar[int]
    ROW_ACCESS_POLICY_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ROW_ACCESS_POLICY_CREATION_FIELD_NUMBER: _ClassVar[int]
    ROW_ACCESS_POLICY_DELETION_FIELD_NUMBER: _ClassVar[int]
    RUNNING: BigQueryAuditMetadata.JobState
    SCRIPT: BigQueryAuditMetadata.QueryStatementType
    SELECT: BigQueryAuditMetadata.QueryStatementType
    SNAPSHOT: BigQueryAuditMetadata.OperationType
    TABLE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    TABLE_CREATION_FIELD_NUMBER: _ClassVar[int]
    TABLE_DATA_CHANGE_FIELD_NUMBER: _ClassVar[int]
    TABLE_DATA_READ_FIELD_NUMBER: _ClassVar[int]
    TABLE_DELETION_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_TABLE: BigQueryAuditMetadata.QueryStatementType
    UNLINK_DATASET_FIELD_NUMBER: _ClassVar[int]
    UPDATE: BigQueryAuditMetadata.QueryStatementType
    WRITE_APPEND: BigQueryAuditMetadata.WriteDisposition
    WRITE_DISPOSITION_UNSPECIFIED: BigQueryAuditMetadata.WriteDisposition
    WRITE_EMPTY: BigQueryAuditMetadata.WriteDisposition
    WRITE_TRUNCATE: BigQueryAuditMetadata.WriteDisposition
    dataset_change: BigQueryAuditMetadata.DatasetChange
    dataset_creation: BigQueryAuditMetadata.DatasetCreation
    dataset_deletion: BigQueryAuditMetadata.DatasetDeletion
    first_party_app_metadata: BigQueryAuditMetadata.FirstPartyAppMetadata
    job_change: BigQueryAuditMetadata.JobChange
    job_deletion: BigQueryAuditMetadata.JobDeletion
    job_insertion: BigQueryAuditMetadata.JobInsertion
    model_creation: BigQueryAuditMetadata.ModelCreation
    model_data_change: BigQueryAuditMetadata.ModelDataChange
    model_data_read: BigQueryAuditMetadata.ModelDataRead
    model_deletion: BigQueryAuditMetadata.ModelDeletion
    model_metadata_change: BigQueryAuditMetadata.ModelMetadataChange
    routine_change: BigQueryAuditMetadata.RoutineChange
    routine_creation: BigQueryAuditMetadata.RoutineCreation
    routine_deletion: BigQueryAuditMetadata.RoutineDeletion
    row_access_policy_change: BigQueryAuditMetadata.RowAccessPolicyChange
    row_access_policy_creation: BigQueryAuditMetadata.RowAccessPolicyCreation
    row_access_policy_deletion: BigQueryAuditMetadata.RowAccessPolicyDeletion
    table_change: BigQueryAuditMetadata.TableChange
    table_creation: BigQueryAuditMetadata.TableCreation
    table_data_change: BigQueryAuditMetadata.TableDataChange
    table_data_read: BigQueryAuditMetadata.TableDataRead
    table_deletion: BigQueryAuditMetadata.TableDeletion
    unlink_dataset: BigQueryAuditMetadata.UnlinkDataset
    def __init__(
        self,
        job_insertion: _Optional[
            _Union[BigQueryAuditMetadata.JobInsertion, _Mapping]
        ] = ...,
        job_change: _Optional[_Union[BigQueryAuditMetadata.JobChange, _Mapping]] = ...,
        job_deletion: _Optional[
            _Union[BigQueryAuditMetadata.JobDeletion, _Mapping]
        ] = ...,
        dataset_creation: _Optional[
            _Union[BigQueryAuditMetadata.DatasetCreation, _Mapping]
        ] = ...,
        dataset_change: _Optional[
            _Union[BigQueryAuditMetadata.DatasetChange, _Mapping]
        ] = ...,
        dataset_deletion: _Optional[
            _Union[BigQueryAuditMetadata.DatasetDeletion, _Mapping]
        ] = ...,
        table_creation: _Optional[
            _Union[BigQueryAuditMetadata.TableCreation, _Mapping]
        ] = ...,
        table_change: _Optional[
            _Union[BigQueryAuditMetadata.TableChange, _Mapping]
        ] = ...,
        table_deletion: _Optional[
            _Union[BigQueryAuditMetadata.TableDeletion, _Mapping]
        ] = ...,
        table_data_read: _Optional[
            _Union[BigQueryAuditMetadata.TableDataRead, _Mapping]
        ] = ...,
        table_data_change: _Optional[
            _Union[BigQueryAuditMetadata.TableDataChange, _Mapping]
        ] = ...,
        model_deletion: _Optional[
            _Union[BigQueryAuditMetadata.ModelDeletion, _Mapping]
        ] = ...,
        model_creation: _Optional[
            _Union[BigQueryAuditMetadata.ModelCreation, _Mapping]
        ] = ...,
        model_metadata_change: _Optional[
            _Union[BigQueryAuditMetadata.ModelMetadataChange, _Mapping]
        ] = ...,
        model_data_change: _Optional[
            _Union[BigQueryAuditMetadata.ModelDataChange, _Mapping]
        ] = ...,
        model_data_read: _Optional[
            _Union[BigQueryAuditMetadata.ModelDataRead, _Mapping]
        ] = ...,
        routine_creation: _Optional[
            _Union[BigQueryAuditMetadata.RoutineCreation, _Mapping]
        ] = ...,
        routine_change: _Optional[
            _Union[BigQueryAuditMetadata.RoutineChange, _Mapping]
        ] = ...,
        routine_deletion: _Optional[
            _Union[BigQueryAuditMetadata.RoutineDeletion, _Mapping]
        ] = ...,
        row_access_policy_creation: _Optional[
            _Union[BigQueryAuditMetadata.RowAccessPolicyCreation, _Mapping]
        ] = ...,
        row_access_policy_change: _Optional[
            _Union[BigQueryAuditMetadata.RowAccessPolicyChange, _Mapping]
        ] = ...,
        row_access_policy_deletion: _Optional[
            _Union[BigQueryAuditMetadata.RowAccessPolicyDeletion, _Mapping]
        ] = ...,
        unlink_dataset: _Optional[
            _Union[BigQueryAuditMetadata.UnlinkDataset, _Mapping]
        ] = ...,
        first_party_app_metadata: _Optional[
            _Union[BigQueryAuditMetadata.FirstPartyAppMetadata, _Mapping]
        ] = ...,
    ) -> None: ...
