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


from google.cloud.spanner_admin_database_v1.types import common
from google.longrunning import operations_pb2 as gl_operations  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.spanner.admin.database.v1",
    manifest={
        "Backup",
        "CreateBackupRequest",
        "CreateBackupMetadata",
        "UpdateBackupRequest",
        "GetBackupRequest",
        "DeleteBackupRequest",
        "ListBackupsRequest",
        "ListBackupsResponse",
        "ListBackupOperationsRequest",
        "ListBackupOperationsResponse",
        "BackupInfo",
    },
)


class Backup(proto.Message):
    r"""A backup of a Cloud Spanner database.

    Attributes:
        database (str):
            Required for the
            [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup]
            operation. Name of the database from which this backup was
            created. This needs to be in the same instance as the
            backup. Values are of the form
            ``projects/<project>/instances/<instance>/databases/<database>``.
        expire_time (~.timestamp.Timestamp):
            Required for the
            [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup]
            operation. The expiration time of the backup, with
            microseconds granularity that must be at least 6 hours and
            at most 366 days from the time the CreateBackup request is
            processed. Once the ``expire_time`` has passed, the backup
            is eligible to be automatically deleted by Cloud Spanner to
            free the resources used by the backup.
        name (str):
            Output only for the
            [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup]
            operation. Required for the
            [UpdateBackup][google.spanner.admin.database.v1.DatabaseAdmin.UpdateBackup]
            operation.

            A globally unique identifier for the backup which cannot be
            changed. Values are of the form
            ``projects/<project>/instances/<instance>/backups/[a-z][a-z0-9_\-]*[a-z0-9]``
            The final segment of the name must be between 2 and 60
            characters in length.

            The backup is stored in the location(s) specified in the
            instance configuration of the instance containing the
            backup, identified by the prefix of the backup name of the
            form ``projects/<project>/instances/<instance>``.
        create_time (~.timestamp.Timestamp):
            Output only. The backup will contain an externally
            consistent copy of the database at the timestamp specified
            by ``create_time``. ``create_time`` is approximately the
            time the
            [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup]
            request is received.
        size_bytes (int):
            Output only. Size of the backup in bytes.
        state (~.gsad_backup.Backup.State):
            Output only. The current state of the backup.
        referencing_databases (Sequence[str]):
            Output only. The names of the restored databases that
            reference the backup. The database names are of the form
            ``projects/<project>/instances/<instance>/databases/<database>``.
            Referencing databases may exist in different instances. The
            existence of any referencing database prevents the backup
            from being deleted. When a restored database from the backup
            enters the ``READY`` state, the reference to the backup is
            removed.
    """

    class State(proto.Enum):
        r"""Indicates the current state of the backup."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2

    database = proto.Field(proto.STRING, number=2)

    expire_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    name = proto.Field(proto.STRING, number=1)

    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    size_bytes = proto.Field(proto.INT64, number=5)

    state = proto.Field(proto.ENUM, number=6, enum=State,)

    referencing_databases = proto.RepeatedField(proto.STRING, number=7)


class CreateBackupRequest(proto.Message):
    r"""The request for
    [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup].

    Attributes:
        parent (str):
            Required. The name of the instance in which the backup will
            be created. This must be the same instance that contains the
            database the backup will be created from. The backup will be
            stored in the location(s) specified in the instance
            configuration of this instance. Values are of the form
            ``projects/<project>/instances/<instance>``.
        backup_id (str):
            Required. The id of the backup to be created. The
            ``backup_id`` appended to ``parent`` forms the full backup
            name of the form
            ``projects/<project>/instances/<instance>/backups/<backup_id>``.
        backup (~.gsad_backup.Backup):
            Required. The backup to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    backup_id = proto.Field(proto.STRING, number=2)

    backup = proto.Field(proto.MESSAGE, number=3, message="Backup",)


class CreateBackupMetadata(proto.Message):
    r"""Metadata type for the operation returned by
    [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup].

    Attributes:
        name (str):
            The name of the backup being created.
        database (str):
            The name of the database the backup is
            created from.
        progress (~.common.OperationProgress):
            The progress of the
            [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup]
            operation.
        cancel_time (~.timestamp.Timestamp):
            The time at which cancellation of this operation was
            received.
            [Operations.CancelOperation][google.longrunning.Operations.CancelOperation]
            starts asynchronous cancellation on a long-running
            operation. The server makes a best effort to cancel the
            operation, but success is not guaranteed. Clients can use
            [Operations.GetOperation][google.longrunning.Operations.GetOperation]
            or other methods to check whether the cancellation succeeded
            or whether the operation completed despite cancellation. On
            successful cancellation, the operation is not deleted;
            instead, it becomes an operation with an [Operation.error][]
            value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
    """

    name = proto.Field(proto.STRING, number=1)

    database = proto.Field(proto.STRING, number=2)

    progress = proto.Field(proto.MESSAGE, number=3, message=common.OperationProgress,)

    cancel_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)


class UpdateBackupRequest(proto.Message):
    r"""The request for
    [UpdateBackup][google.spanner.admin.database.v1.DatabaseAdmin.UpdateBackup].

    Attributes:
        backup (~.gsad_backup.Backup):
            Required. The backup to update. ``backup.name``, and the
            fields to be updated as specified by ``update_mask`` are
            required. Other fields are ignored. Update is only supported
            for the following fields:

            -  ``backup.expire_time``.
        update_mask (~.field_mask.FieldMask):
            Required. A mask specifying which fields (e.g.
            ``expire_time``) in the Backup resource should be updated.
            This mask is relative to the Backup resource, not to the
            request message. The field mask must always be specified;
            this prevents any future fields from being erased
            accidentally by clients that do not know about them.
    """

    backup = proto.Field(proto.MESSAGE, number=1, message="Backup",)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class GetBackupRequest(proto.Message):
    r"""The request for
    [GetBackup][google.spanner.admin.database.v1.DatabaseAdmin.GetBackup].

    Attributes:
        name (str):
            Required. Name of the backup. Values are of the form
            ``projects/<project>/instances/<instance>/backups/<backup>``.
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteBackupRequest(proto.Message):
    r"""The request for
    [DeleteBackup][google.spanner.admin.database.v1.DatabaseAdmin.DeleteBackup].

    Attributes:
        name (str):
            Required. Name of the backup to delete. Values are of the
            form
            ``projects/<project>/instances/<instance>/backups/<backup>``.
    """

    name = proto.Field(proto.STRING, number=1)


class ListBackupsRequest(proto.Message):
    r"""The request for
    [ListBackups][google.spanner.admin.database.v1.DatabaseAdmin.ListBackups].

    Attributes:
        parent (str):
            Required. The instance to list backups from. Values are of
            the form ``projects/<project>/instances/<instance>``.
        filter (str):
            An expression that filters the list of returned backups.

            A filter expression consists of a field name, a comparison
            operator, and a value for filtering. The value must be a
            string, a number, or a boolean. The comparison operator must
            be one of: ``<``, ``>``, ``<=``, ``>=``, ``!=``, ``=``, or
            ``:``. Colon ``:`` is the contains operator. Filter rules
            are not case sensitive.

            The following fields in the
            [Backup][google.spanner.admin.database.v1.Backup] are
            eligible for filtering:

            -  ``name``
            -  ``database``
            -  ``state``
            -  ``create_time`` (and values are of the format
               YYYY-MM-DDTHH:MM:SSZ)
            -  ``expire_time`` (and values are of the format
               YYYY-MM-DDTHH:MM:SSZ)
            -  ``size_bytes``

            You can combine multiple expressions by enclosing each
            expression in parentheses. By default, expressions are
            combined with AND logic, but you can specify AND, OR, and
            NOT logic explicitly.

            Here are a few examples:

            -  ``name:Howl`` - The backup's name contains the string
               "howl".
            -  ``database:prod`` - The database's name contains the
               string "prod".
            -  ``state:CREATING`` - The backup is pending creation.
            -  ``state:READY`` - The backup is fully created and ready
               for use.
            -  ``(name:howl) AND (create_time < \"2018-03-28T14:50:00Z\")``
               - The backup name contains the string "howl" and
               ``create_time`` of the backup is before
               2018-03-28T14:50:00Z.
            -  ``expire_time < \"2018-03-28T14:50:00Z\"`` - The backup
               ``expire_time`` is before 2018-03-28T14:50:00Z.
            -  ``size_bytes > 10000000000`` - The backup's size is
               greater than 10GB
        page_size (int):
            Number of backups to be returned in the
            response. If 0 or less, defaults to the server's
            maximum allowed page size.
        page_token (str):
            If non-empty, ``page_token`` should contain a
            [next_page_token][google.spanner.admin.database.v1.ListBackupsResponse.next_page_token]
            from a previous
            [ListBackupsResponse][google.spanner.admin.database.v1.ListBackupsResponse]
            to the same ``parent`` and with the same ``filter``.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListBackupsResponse(proto.Message):
    r"""The response for
    [ListBackups][google.spanner.admin.database.v1.DatabaseAdmin.ListBackups].

    Attributes:
        backups (Sequence[~.gsad_backup.Backup]):
            The list of matching backups. Backups returned are ordered
            by ``create_time`` in descending order, starting from the
            most recent ``create_time``.
        next_page_token (str):
            ``next_page_token`` can be sent in a subsequent
            [ListBackups][google.spanner.admin.database.v1.DatabaseAdmin.ListBackups]
            call to fetch more of the matching backups.
    """

    @property
    def raw_page(self):
        return self

    backups = proto.RepeatedField(proto.MESSAGE, number=1, message="Backup",)

    next_page_token = proto.Field(proto.STRING, number=2)


class ListBackupOperationsRequest(proto.Message):
    r"""The request for
    [ListBackupOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListBackupOperations].

    Attributes:
        parent (str):
            Required. The instance of the backup operations. Values are
            of the form ``projects/<project>/instances/<instance>``.
        filter (str):
            An expression that filters the list of returned backup
            operations.

            A filter expression consists of a field name, a comparison
            operator, and a value for filtering. The value must be a
            string, a number, or a boolean. The comparison operator must
            be one of: ``<``, ``>``, ``<=``, ``>=``, ``!=``, ``=``, or
            ``:``. Colon ``:`` is the contains operator. Filter rules
            are not case sensitive.

            The following fields in the
            [operation][google.longrunning.Operation] are eligible for
            filtering:

            -  ``name`` - The name of the long-running operation
            -  ``done`` - False if the operation is in progress, else
               true.
            -  ``metadata.@type`` - the type of metadata. For example,
               the type string for
               [CreateBackupMetadata][google.spanner.admin.database.v1.CreateBackupMetadata]
               is
               ``type.googleapis.com/google.spanner.admin.database.v1.CreateBackupMetadata``.
            -  ``metadata.<field_name>`` - any field in metadata.value.
            -  ``error`` - Error associated with the long-running
               operation.
            -  ``response.@type`` - the type of response.
            -  ``response.<field_name>`` - any field in response.value.

            You can combine multiple expressions by enclosing each
            expression in parentheses. By default, expressions are
            combined with AND logic, but you can specify AND, OR, and
            NOT logic explicitly.

            Here are a few examples:

            -  ``done:true`` - The operation is complete.
            -  ``metadata.database:prod`` - The database the backup was
               taken from has a name containing the string "prod".
            -  ``(metadata.@type=type.googleapis.com/google.spanner.admin.database.v1.CreateBackupMetadata) AND``
               ``(metadata.name:howl) AND``
               ``(metadata.progress.start_time < \"2018-03-28T14:50:00Z\") AND``
               ``(error:*)`` - Returns operations where:

               -  The operation's metadata type is
                  [CreateBackupMetadata][google.spanner.admin.database.v1.CreateBackupMetadata].
               -  The backup name contains the string "howl".
               -  The operation started before 2018-03-28T14:50:00Z.
               -  The operation resulted in an error.
        page_size (int):
            Number of operations to be returned in the
            response. If 0 or less, defaults to the server's
            maximum allowed page size.
        page_token (str):
            If non-empty, ``page_token`` should contain a
            [next_page_token][google.spanner.admin.database.v1.ListBackupOperationsResponse.next_page_token]
            from a previous
            [ListBackupOperationsResponse][google.spanner.admin.database.v1.ListBackupOperationsResponse]
            to the same ``parent`` and with the same ``filter``.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListBackupOperationsResponse(proto.Message):
    r"""The response for
    [ListBackupOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListBackupOperations].

    Attributes:
        operations (Sequence[~.gl_operations.Operation]):
            The list of matching backup [long-running
            operations][google.longrunning.Operation]. Each operation's
            name will be prefixed by the backup's name and the
            operation's
            [metadata][google.longrunning.Operation.metadata] will be of
            type
            [CreateBackupMetadata][google.spanner.admin.database.v1.CreateBackupMetadata].
            Operations returned include those that are pending or have
            completed/failed/canceled within the last 7 days. Operations
            returned are ordered by
            ``operation.metadata.value.progress.start_time`` in
            descending order starting from the most recently started
            operation.
        next_page_token (str):
            ``next_page_token`` can be sent in a subsequent
            [ListBackupOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListBackupOperations]
            call to fetch more of the matching metadata.
    """

    @property
    def raw_page(self):
        return self

    operations = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gl_operations.Operation,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class BackupInfo(proto.Message):
    r"""Information about a backup.

    Attributes:
        backup (str):
            Name of the backup.
        create_time (~.timestamp.Timestamp):
            The backup contains an externally consistent copy of
            ``source_database`` at the timestamp specified by
            ``create_time``.
        source_database (str):
            Name of the database the backup was created
            from.
    """

    backup = proto.Field(proto.STRING, number=1)

    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    source_database = proto.Field(proto.STRING, number=3)


__all__ = tuple(sorted(__protobuf__.manifest))
