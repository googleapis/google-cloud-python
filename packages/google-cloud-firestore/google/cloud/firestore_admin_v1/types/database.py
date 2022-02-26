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
    package="google.firestore.admin.v1", manifest={"Database",},
)


class Database(proto.Message):
    r"""A Cloud Firestore Database. Currently only one database is allowed
    per cloud project; this database must have a ``database_id`` of
    '(default)'.

    Attributes:
        name (str):
            The resource name of the Database. Format:
            ``projects/{project}/databases/{database}``
        location_id (str):
            The location of the database. Available
            databases are listed at
            https://cloud.google.com/firestore/docs/locations.
        type_ (google.cloud.firestore_admin_v1.types.Database.DatabaseType):
            The type of the database.
            See
            https://cloud.google.com/datastore/docs/firestore-or-datastore
            for information about how to choose.
        concurrency_mode (google.cloud.firestore_admin_v1.types.Database.ConcurrencyMode):
            The concurrency control mode to use for this
            database.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
    """

    class DatabaseType(proto.Enum):
        r"""The type of the database.
        See
        https://cloud.google.com/datastore/docs/firestore-or-datastore
        for information about how to choose.
        """
        DATABASE_TYPE_UNSPECIFIED = 0
        FIRESTORE_NATIVE = 1
        DATASTORE_MODE = 2

    class ConcurrencyMode(proto.Enum):
        r"""The type of concurrency control mode for transactions."""
        CONCURRENCY_MODE_UNSPECIFIED = 0
        OPTIMISTIC = 1
        PESSIMISTIC = 2
        OPTIMISTIC_WITH_ENTITY_GROUPS = 3

    name = proto.Field(proto.STRING, number=1,)
    location_id = proto.Field(proto.STRING, number=9,)
    type_ = proto.Field(proto.ENUM, number=10, enum=DatabaseType,)
    concurrency_mode = proto.Field(proto.ENUM, number=15, enum=ConcurrencyMode,)
    etag = proto.Field(proto.STRING, number=99,)


__all__ = tuple(sorted(__protobuf__.manifest))
