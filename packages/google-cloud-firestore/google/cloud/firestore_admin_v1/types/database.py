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

        Values:
            DATABASE_TYPE_UNSPECIFIED (0):
                The default value. This value is used if the
                database type is omitted.
            FIRESTORE_NATIVE (1):
                Firestore Native Mode
            DATASTORE_MODE (2):
                Firestore in Datastore Mode.
        """
        DATABASE_TYPE_UNSPECIFIED = 0
        FIRESTORE_NATIVE = 1
        DATASTORE_MODE = 2

    class ConcurrencyMode(proto.Enum):
        r"""The type of concurrency control mode for transactions.

        Values:
            CONCURRENCY_MODE_UNSPECIFIED (0):
                Not used.
            OPTIMISTIC (1):
                Use optimistic concurrency control by
                default. This mode is available for Cloud
                Firestore databases.
            PESSIMISTIC (2):
                Use pessimistic concurrency control by
                default. This mode is available for Cloud
                Firestore databases.

                This is the default setting for Cloud Firestore.
            OPTIMISTIC_WITH_ENTITY_GROUPS (3):
                Use optimistic concurrency control with
                entity groups by default.
                This is the only available mode for Cloud
                Datastore.

                This mode is also available for Cloud Firestore
                with Datastore Mode but is not recommended.
        """
        CONCURRENCY_MODE_UNSPECIFIED = 0
        OPTIMISTIC = 1
        PESSIMISTIC = 2
        OPTIMISTIC_WITH_ENTITY_GROUPS = 3

    class AppEngineIntegrationMode(proto.Enum):
        r"""The type of App Engine integration mode.

        Values:
            APP_ENGINE_INTEGRATION_MODE_UNSPECIFIED (0):
                Not used.
            ENABLED (1):
                If an App Engine application exists in the
                same region as this database, App Engine
                configuration will impact this database. This
                includes disabling of the application &
                database, as well as disabling writes to the
                database.
            DISABLED (2):
                Appengine has no affect on the ability of
                this database to serve requests.
        """
        APP_ENGINE_INTEGRATION_MODE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    location_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    type_: DatabaseType = proto.Field(
        proto.ENUM,
        number=10,
        enum=DatabaseType,
    )
    concurrency_mode: ConcurrencyMode = proto.Field(
        proto.ENUM,
        number=15,
        enum=ConcurrencyMode,
    )
    app_engine_integration_mode: AppEngineIntegrationMode = proto.Field(
        proto.ENUM,
        number=19,
        enum=AppEngineIntegrationMode,
    )
    key_prefix: str = proto.Field(
        proto.STRING,
        number=20,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=99,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
