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
    package="google.cloud.dataplex.v1",
    manifest={
        "DataDiscoverySpec",
        "DataDiscoveryResult",
    },
)


class DataDiscoverySpec(proto.Message):
    r"""Spec for a data discovery scan.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bigquery_publishing_config (google.cloud.dataplex_v1.types.DataDiscoverySpec.BigQueryPublishingConfig):
            Optional. Configuration for metadata
            publishing.
        storage_config (google.cloud.dataplex_v1.types.DataDiscoverySpec.StorageConfig):
            Cloud Storage related configurations.

            This field is a member of `oneof`_ ``resource_config``.
    """

    class BigQueryPublishingConfig(proto.Message):
        r"""Describes BigQuery publishing configurations.

        Attributes:
            table_type (google.cloud.dataplex_v1.types.DataDiscoverySpec.BigQueryPublishingConfig.TableType):
                Optional. Determines whether to  publish
                discovered tables as BigLake external tables or
                non-BigLake external tables.
            connection (str):
                Optional. The BigQuery connection used to create BigLake
                tables. Must be in the form
                ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``
        """

        class TableType(proto.Enum):
            r"""Determines how discovered tables are published.

            Values:
                TABLE_TYPE_UNSPECIFIED (0):
                    Table type unspecified.
                EXTERNAL (1):
                    Default. Discovered tables are published as
                    BigQuery external tables whose data is accessed
                    using the credentials of the user querying the
                    table.
                BIGLAKE (2):
                    Discovered tables are published as BigLake
                    external tables whose data is accessed using the
                    credentials of the associated BigQuery
                    connection.
            """
            TABLE_TYPE_UNSPECIFIED = 0
            EXTERNAL = 1
            BIGLAKE = 2

        table_type: "DataDiscoverySpec.BigQueryPublishingConfig.TableType" = (
            proto.Field(
                proto.ENUM,
                number=2,
                enum="DataDiscoverySpec.BigQueryPublishingConfig.TableType",
            )
        )
        connection: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class StorageConfig(proto.Message):
        r"""Configurations related to Cloud Storage as the data source.

        Attributes:
            include_patterns (MutableSequence[str]):
                Optional. Defines the data to include during
                discovery when only a subset of the data should
                be considered. Provide a list of patterns that
                identify the data to include. For Cloud Storage
                bucket assets, these patterns are interpreted as
                glob patterns used to match object names. For
                BigQuery dataset assets, these patterns are
                interpreted as patterns to match table names.
            exclude_patterns (MutableSequence[str]):
                Optional. Defines the data to exclude during
                discovery. Provide a list of patterns that
                identify the data to exclude. For Cloud Storage
                bucket assets, these patterns are interpreted as
                glob patterns used to match object names. For
                BigQuery dataset assets, these patterns are
                interpreted as patterns to match table names.
            csv_options (google.cloud.dataplex_v1.types.DataDiscoverySpec.StorageConfig.CsvOptions):
                Optional. Configuration for CSV data.
            json_options (google.cloud.dataplex_v1.types.DataDiscoverySpec.StorageConfig.JsonOptions):
                Optional. Configuration for JSON data.
        """

        class CsvOptions(proto.Message):
            r"""Describes CSV and similar semi-structured data formats.

            Attributes:
                header_rows (int):
                    Optional. The number of rows to interpret as
                    header rows that should be skipped when reading
                    data rows.
                delimiter (str):
                    Optional. The delimiter that is used to separate values. The
                    default is ``,`` (comma).
                encoding (str):
                    Optional. The character encoding of the data.
                    The default is UTF-8.
                type_inference_disabled (bool):
                    Optional. Whether to disable the inference of
                    data types for CSV data. If true, all columns
                    are registered as strings.
                quote (str):
                    Optional. The character used to quote column values. Accepts
                    ``"`` (double quotation mark) or ``'`` (single quotation
                    mark). If unspecified, defaults to ``"`` (double quotation
                    mark).
            """

            header_rows: int = proto.Field(
                proto.INT32,
                number=1,
            )
            delimiter: str = proto.Field(
                proto.STRING,
                number=2,
            )
            encoding: str = proto.Field(
                proto.STRING,
                number=3,
            )
            type_inference_disabled: bool = proto.Field(
                proto.BOOL,
                number=4,
            )
            quote: str = proto.Field(
                proto.STRING,
                number=5,
            )

        class JsonOptions(proto.Message):
            r"""Describes JSON data format.

            Attributes:
                encoding (str):
                    Optional. The character encoding of the data.
                    The default is UTF-8.
                type_inference_disabled (bool):
                    Optional. Whether to disable the inference of
                    data types for JSON data. If true, all columns
                    are registered as their primitive types
                    (strings, number, or boolean).
            """

            encoding: str = proto.Field(
                proto.STRING,
                number=1,
            )
            type_inference_disabled: bool = proto.Field(
                proto.BOOL,
                number=2,
            )

        include_patterns: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        exclude_patterns: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        csv_options: "DataDiscoverySpec.StorageConfig.CsvOptions" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="DataDiscoverySpec.StorageConfig.CsvOptions",
        )
        json_options: "DataDiscoverySpec.StorageConfig.JsonOptions" = proto.Field(
            proto.MESSAGE,
            number=4,
            message="DataDiscoverySpec.StorageConfig.JsonOptions",
        )

    bigquery_publishing_config: BigQueryPublishingConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=BigQueryPublishingConfig,
    )
    storage_config: StorageConfig = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="resource_config",
        message=StorageConfig,
    )


class DataDiscoveryResult(proto.Message):
    r"""The output of a data discovery scan.

    Attributes:
        bigquery_publishing (google.cloud.dataplex_v1.types.DataDiscoveryResult.BigQueryPublishing):
            Output only. Configuration for metadata
            publishing.
    """

    class BigQueryPublishing(proto.Message):
        r"""Describes BigQuery publishing configurations.

        Attributes:
            dataset (str):
                Output only. The BigQuery dataset to publish to. It takes
                the form ``projects/{project_id}/datasets/{dataset_id}``. If
                not set, the service creates a default publishing dataset.
        """

        dataset: str = proto.Field(
            proto.STRING,
            number=1,
        )

    bigquery_publishing: BigQueryPublishing = proto.Field(
        proto.MESSAGE,
        number=1,
        message=BigQueryPublishing,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
