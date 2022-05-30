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
    package="google.firestore.admin.v1",
    manifest={
        "Database",
    },
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
        app_engine_integration_mode (google.cloud.firestore_admin_v1.types.Database.AppEngineIntegrationMode):
            The App Engine integration mode to use for
            this database.
        key_prefix (str):
            Output only. The key_prefix for this database. This
            key_prefix is used, in combination with the project id ("~")
            to construct the application id that is returned from the
            Cloud Datastore APIs in Google App Engine first generation
            runtimes.

            This value may be empty in which case the appid to use for
            URL-encoded keys is the project_id (eg: foo instead of
            v~foo).
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

        Mode changes are only allowed if the database is empty.
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

    class AppEngineIntegrationMode(proto.Enum):
        r"""The type of App Engine integration mode."""
        APP_ENGINE_INTEGRATION_MODE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    location_id = proto.Field(
        proto.STRING,
        number=9,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=10,
        enum=DatabaseType,
    )
    concurrency_mode = proto.Field(
        proto.ENUM,
        number=15,
        enum=ConcurrencyMode,
    )
    app_engine_integration_mode = proto.Field(
        proto.ENUM,
        number=19,
        enum=AppEngineIntegrationMode,
    )
    key_prefix = proto.Field(
        proto.STRING,
        number=20,
    )
    etag = proto.Field(
        proto.STRING,
        number=99,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
