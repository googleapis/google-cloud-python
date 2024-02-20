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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.admin.v1",
    manifest={
        "Database",
    },
)


class Database(proto.Message):
    r"""A Cloud Firestore Database.

    Attributes:
        name (str):
            The resource name of the Database. Format:
            ``projects/{project}/databases/{database}``
        uid (str):
            Output only. The system-generated UUID4 for
            this Database.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp at which this database was
            created. Databases created before 2016 do not populate
            create_time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp at which this
            database was most recently updated. Note this
            only includes updates to the database resource
            and not data contained by the database.
        location_id (str):
            The location of the database. Available
            locations are listed at
            https://cloud.google.com/firestore/docs/locations.
        type_ (google.cloud.firestore_admin_v1.types.Database.DatabaseType):
            The type of the database.
            See
            https://cloud.google.com/datastore/docs/firestore-or-datastore
            for information about how to choose.
        concurrency_mode (google.cloud.firestore_admin_v1.types.Database.ConcurrencyMode):
            The concurrency control mode to use for this
            database.
        version_retention_period (google.protobuf.duration_pb2.Duration):
            Output only. The period during which past versions of data
            are retained in the database.

            Any [read][google.firestore.v1.GetDocumentRequest.read_time]
            or
            [query][google.firestore.v1.ListDocumentsRequest.read_time]
            can specify a ``read_time`` within this window, and will
            read the state of the database at that time.

            If the PITR feature is enabled, the retention period is 7
            days. Otherwise, the retention period is 1 hour.
        earliest_version_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The earliest timestamp at which older versions
            of the data can be read from the database. See
            [version_retention_period] above; this field is populated
            with ``now - version_retention_period``.

            This value is continuously updated, and becomes stale the
            moment it is queried. If you are using this value to recover
            data, make sure to account for the time from the moment when
            the value is queried to the moment when you initiate the
            recovery.
        point_in_time_recovery_enablement (google.cloud.firestore_admin_v1.types.Database.PointInTimeRecoveryEnablement):
            Whether to enable the PITR feature on this
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
        delete_protection_state (google.cloud.firestore_admin_v1.types.Database.DeleteProtectionState):
            State of delete protection for the database.
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

    class PointInTimeRecoveryEnablement(proto.Enum):
        r"""Point In Time Recovery feature enablement.

        Values:
            POINT_IN_TIME_RECOVERY_ENABLEMENT_UNSPECIFIED (0):
                Not used.
            POINT_IN_TIME_RECOVERY_ENABLED (1):
                Reads are supported on selected versions of the data from
                within the past 7 days:

                -  Reads against any timestamp within the past hour
                -  Reads against 1-minute snapshots beyond 1 hour and within
                   7 days

                ``version_retention_period`` and ``earliest_version_time``
                can be used to determine the supported versions.
            POINT_IN_TIME_RECOVERY_DISABLED (2):
                Reads are supported on any version of the
                data from within the past 1 hour.
        """
        POINT_IN_TIME_RECOVERY_ENABLEMENT_UNSPECIFIED = 0
        POINT_IN_TIME_RECOVERY_ENABLED = 1
        POINT_IN_TIME_RECOVERY_DISABLED = 2

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
                App Engine has no effect on the ability of
                this database to serve requests.

                This is the default setting for databases
                created with the Firestore API.
        """
        APP_ENGINE_INTEGRATION_MODE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    class DeleteProtectionState(proto.Enum):
        r"""The delete protection state of the database.

        Values:
            DELETE_PROTECTION_STATE_UNSPECIFIED (0):
                The default value. Delete protection type is
                not specified
            DELETE_PROTECTION_DISABLED (1):
                Delete protection is disabled
            DELETE_PROTECTION_ENABLED (2):
                Delete protection is enabled
        """
        DELETE_PROTECTION_STATE_UNSPECIFIED = 0
        DELETE_PROTECTION_DISABLED = 1
        DELETE_PROTECTION_ENABLED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
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
    version_retention_period: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=17,
        message=duration_pb2.Duration,
    )
    earliest_version_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=18,
        message=timestamp_pb2.Timestamp,
    )
    point_in_time_recovery_enablement: PointInTimeRecoveryEnablement = proto.Field(
        proto.ENUM,
        number=21,
        enum=PointInTimeRecoveryEnablement,
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
    delete_protection_state: DeleteProtectionState = proto.Field(
        proto.ENUM,
        number=22,
        enum=DeleteProtectionState,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=99,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
