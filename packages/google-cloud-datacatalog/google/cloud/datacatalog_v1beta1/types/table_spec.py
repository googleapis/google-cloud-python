# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
    package="google.cloud.datacatalog.v1beta1",
    manifest={
        "TableSourceType",
        "BigQueryTableSpec",
        "ViewSpec",
        "TableSpec",
        "BigQueryDateShardedSpec",
    },
)


class TableSourceType(proto.Enum):
    r"""Table source type."""
    TABLE_SOURCE_TYPE_UNSPECIFIED = 0
    BIGQUERY_VIEW = 2
    BIGQUERY_TABLE = 5


class BigQueryTableSpec(proto.Message):
    r"""Describes a BigQuery table.
    Attributes:
        table_source_type (google.cloud.datacatalog_v1beta1.types.TableSourceType):
            Output only. The table source type.
        view_spec (google.cloud.datacatalog_v1beta1.types.ViewSpec):
            Table view specification. This field should only be
            populated if ``table_source_type`` is ``BIGQUERY_VIEW``.
        table_spec (google.cloud.datacatalog_v1beta1.types.TableSpec):
            Spec of a BigQuery table. This field should only be
            populated if ``table_source_type`` is ``BIGQUERY_TABLE``.
    """

    table_source_type = proto.Field(proto.ENUM, number=1, enum="TableSourceType",)
    view_spec = proto.Field(
        proto.MESSAGE, number=2, oneof="type_spec", message="ViewSpec",
    )
    table_spec = proto.Field(
        proto.MESSAGE, number=3, oneof="type_spec", message="TableSpec",
    )


class ViewSpec(proto.Message):
    r"""Table view specification.
    Attributes:
        view_query (str):
            Output only. The query that defines the table
            view.
    """

    view_query = proto.Field(proto.STRING, number=1,)


class TableSpec(proto.Message):
    r"""Normal BigQuery table spec.
    Attributes:
        grouped_entry (str):
            Output only. If the table is a dated shard, i.e., with name
            pattern ``[prefix]YYYYMMDD``, ``grouped_entry`` is the Data
            Catalog resource name of the date sharded grouped entry, for
            example,
            ``projects/{project_id}/locations/{location}/entrygroups/{entry_group_id}/entries/{entry_id}``.
            Otherwise, ``grouped_entry`` is empty.
    """

    grouped_entry = proto.Field(proto.STRING, number=1,)


class BigQueryDateShardedSpec(proto.Message):
    r"""Spec for a group of BigQuery tables with name pattern
    ``[prefix]YYYYMMDD``. Context:
    https://cloud.google.com/bigquery/docs/partitioned-tables#partitioning_versus_sharding

    Attributes:
        dataset (str):
            Output only. The Data Catalog resource name of the dataset
            entry the current table belongs to, for example,
            ``projects/{project_id}/locations/{location}/entrygroups/{entry_group_id}/entries/{entry_id}``.
        table_prefix (str):
            Output only. The table name prefix of the shards. The name
            of any given shard is ``[table_prefix]YYYYMMDD``, for
            example, for shard ``MyTable20180101``, the ``table_prefix``
            is ``MyTable``.
        shard_count (int):
            Output only. Total number of shards.
    """

    dataset = proto.Field(proto.STRING, number=1,)
    table_prefix = proto.Field(proto.STRING, number=2,)
    shard_count = proto.Field(proto.INT64, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
