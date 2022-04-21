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
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1",
    manifest={
        "UsageStats",
        "UsageSignal",
    },
)


class UsageStats(proto.Message):
    r"""Detailed statistics on the entry's usage.

    Usage statistics have the following limitations:

    -  Only BigQuery tables have them.
    -  They only include BigQuery query jobs.
    -  They might be underestimated because wildcard table references
       are not yet counted. For more information, see [Querying multiple
       tables using a wildcard table]
       (https://cloud.google.com/bigquery/docs/querying-wildcard-tables)

    Attributes:
        total_completions (float):
            The number of successful uses of the
            underlying entry.
        total_failures (float):
            The number of failed attempts to use the
            underlying entry.
        total_cancellations (float):
            The number of cancelled attempts to use the
            underlying entry.
        total_execution_time_for_completions_millis (float):
            Total time spent only on successful uses, in
            milliseconds.
    """

    total_completions = proto.Field(
        proto.FLOAT,
        number=1,
    )
    total_failures = proto.Field(
        proto.FLOAT,
        number=2,
    )
    total_cancellations = proto.Field(
        proto.FLOAT,
        number=3,
    )
    total_execution_time_for_completions_millis = proto.Field(
        proto.FLOAT,
        number=4,
    )


class UsageSignal(proto.Message):
    r"""The set of all usage signals that Data Catalog stores.
    Note: Usually, these signals are updated daily. In rare cases,
    an update may fail but will be performed again on the next day.

    Attributes:
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The end timestamp of the duration of usage
            statistics.
        usage_within_time_range (Mapping[str, google.cloud.datacatalog_v1.types.UsageStats]):
            Usage statistics over each of the predefined time ranges.

            Supported time ranges are ``{"24H", "7D", "30D"}``.
    """

    update_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    usage_within_time_range = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message="UsageStats",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
