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
        "Trigger",
        "DataSource",
        "ScannedData",
    },
)


class Trigger(proto.Message):
    r"""DataScan scheduling and trigger settings.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        on_demand (google.cloud.dataplex_v1.types.Trigger.OnDemand):
            The scan runs once via ``RunDataScan`` API.

            This field is a member of `oneof`_ ``mode``.
        schedule (google.cloud.dataplex_v1.types.Trigger.Schedule):
            The scan is scheduled to run periodically.

            This field is a member of `oneof`_ ``mode``.
    """

    class OnDemand(proto.Message):
        r"""The scan runs once via ``RunDataScan`` API."""

    class Schedule(proto.Message):
        r"""The scan is scheduled to run periodically.

        Attributes:
            cron (str):
                Required. `Cron <https://en.wikipedia.org/wiki/Cron>`__
                schedule for running scans periodically.

                To explicitly set a timezone in the cron tab, apply a prefix
                in the cron tab: **"CRON_TZ=${IANA_TIME_ZONE}"** or
                **"TZ=${IANA_TIME_ZONE}"**. The **${IANA_TIME_ZONE}** may
                only be a valid string from IANA time zone database
                (`wikipedia <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`__).
                For example, ``CRON_TZ=America/New_York 1 * * * *``, or
                ``TZ=America/New_York 1 * * * *``.

                This field is required for Schedule scans.
        """

        cron: str = proto.Field(
            proto.STRING,
            number=1,
        )

    on_demand: OnDemand = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="mode",
        message=OnDemand,
    )
    schedule: Schedule = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="mode",
        message=Schedule,
    )


class DataSource(proto.Message):
    r"""The data source for DataScan.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        entity (str):
            Immutable. The Dataplex entity that represents the data
            source (e.g. BigQuery table) for DataScan, of the form:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.

            This field is a member of `oneof`_ ``source``.
        resource (str):
            Immutable. The service-qualified full resource name of the
            cloud resource for a DataScan job to scan against. The field
            could be: BigQuery table of type "TABLE" for
            DataProfileScan/DataQualityScan Format:
            //bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID

            This field is a member of `oneof`_ ``source``.
    """

    entity: str = proto.Field(
        proto.STRING,
        number=100,
        oneof="source",
    )
    resource: str = proto.Field(
        proto.STRING,
        number=101,
        oneof="source",
    )


class ScannedData(proto.Message):
    r"""The data scanned during processing (e.g. in incremental
    DataScan)


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        incremental_field (google.cloud.dataplex_v1.types.ScannedData.IncrementalField):
            The range denoted by values of an incremental
            field

            This field is a member of `oneof`_ ``data_range``.
    """

    class IncrementalField(proto.Message):
        r"""A data range denoted by a pair of start/end values of a
        field.

        Attributes:
            field (str):
                The field that contains values which
                monotonically increases over time (e.g. a
                timestamp column).
            start (str):
                Value that marks the start of the range.
            end (str):
                Value that marks the end of the range.
        """

        field: str = proto.Field(
            proto.STRING,
            number=1,
        )
        start: str = proto.Field(
            proto.STRING,
            number=2,
        )
        end: str = proto.Field(
            proto.STRING,
            number=3,
        )

    incremental_field: IncrementalField = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="data_range",
        message=IncrementalField,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
