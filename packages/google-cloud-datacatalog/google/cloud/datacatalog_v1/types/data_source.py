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
    package="google.cloud.datacatalog.v1", manifest={"DataSource",},
)


class DataSource(proto.Message):
    r"""Physical location of an entry.

    Attributes:
        service (google.cloud.datacatalog_v1.types.DataSource.Service):
            Service that physically stores the data.
        resource (str):
            Full name of a resource as defined by the service. For
            example:

            ``//bigquery.googleapis.com/projects/{PROJECT_ID}/locations/{LOCATION}/datasets/{DATASET_ID}/tables/{TABLE_ID}``
    """

    class Service(proto.Enum):
        r"""Name of a service that stores the data."""
        SERVICE_UNSPECIFIED = 0
        CLOUD_STORAGE = 1
        BIGQUERY = 2

    service = proto.Field(proto.ENUM, number=1, enum=Service,)
    resource = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
