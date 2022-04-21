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
        "IntegratedSystem",
        "PersonalDetails",
    },
)


class IntegratedSystem(proto.Enum):
    r"""This enum lists all the systems that Data Catalog integrates
    with.
    """
    INTEGRATED_SYSTEM_UNSPECIFIED = 0
    BIGQUERY = 1
    CLOUD_PUBSUB = 2
    DATAPROC_METASTORE = 3
    DATAPLEX = 4


class PersonalDetails(proto.Message):
    r"""Entry metadata relevant only to the user and private to them.

    Attributes:
        starred (bool):
            True if the entry is starred by the user;
            false otherwise.
        star_time (google.protobuf.timestamp_pb2.Timestamp):
            Set if the entry is starred; unset otherwise.
    """

    starred = proto.Field(
        proto.BOOL,
        number=1,
    )
    star_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
