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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.storagetransfer.v1",
    manifest={
        "GoogleServiceAccount",
        "AwsAccessKey",
        "AzureCredentials",
        "ObjectConditions",
        "GcsData",
        "AwsS3Data",
        "AzureBlobStorageData",
        "HttpData",
        "TransferOptions",
        "TransferSpec",
        "Schedule",
        "TransferJob",
        "ErrorLogEntry",
        "ErrorSummary",
        "TransferCounters",
        "NotificationConfig",
        "TransferOperation",
    },
)


class GoogleServiceAccount(proto.Message):
    r"""Google service account

    Attributes:
        account_email (str):
            Email address of the service account.
        subject_id (str):
            Unique identifier for the service account.
    """

    account_email = proto.Field(proto.STRING, number=1,)
    subject_id = proto.Field(proto.STRING, number=2,)


class AwsAccessKey(proto.Message):
    r"""AWS access key (see `AWS Security
    Credentials <https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html>`__).

    For information on our data retention policy for user credentials,
    see `User
    credentials </storage-transfer/docs/data-retention#user-credentials>`__.

    Attributes:
        access_key_id (str):
            Required. AWS access key ID.
        secret_access_key (str):
            Required. AWS secret access key. This field
            is not returned in RPC responses.
    """

    access_key_id = proto.Field(proto.STRING, number=1,)
    secret_access_key = proto.Field(proto.STRING, number=2,)


class AzureCredentials(proto.Message):
    r"""Azure credentials

    For information on our data retention policy for user credentials,
    see `User
    credentials </storage-transfer/docs/data-retention#user-credentials>`__.

    Attributes:
        sas_token (str):
            Required. Azure shared access signature (SAS).

            .. raw:: html

                <aside class="note">
                <strong>Note:</strong>Copying data from Azure Data Lake
                Storage (ADLS) Gen 2 is in [Preview](/products/#product-launch-stages).
                During Preview, if you are copying data from ADLS Gen 2, you must use an
                account SAS.
                </aside>

            For more information about SAS, see `Grant limited access to
            Azure Storage resources using shared access signatures
            (SAS) <https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview>`__.
    """

    sas_token = proto.Field(proto.STRING, number=2,)


class ObjectConditions(proto.Message):
    r"""Conditions that determine which objects will be transferred. Applies
    only to Cloud Data Sources such as S3, Azure, and Cloud Storage.

    The "last modification time" refers to the time of the last change
    to the object's content or metadata — specifically, this is the
    ``updated`` property of Cloud Storage objects, the ``LastModified``
    field of S3 objects, and the ``Last-Modified`` header of Azure
    blobs.

    Attributes:
        min_time_elapsed_since_last_modification (google.protobuf.duration_pb2.Duration):
            If specified, only objects with a "last modification time"
            before ``NOW`` -
            ``min_time_elapsed_since_last_modification`` and objects
            that don't have a "last modification time" are transferred.

            For each
            [TransferOperation][google.storagetransfer.v1.TransferOperation]
            started by this
            [TransferJob][google.storagetransfer.v1.TransferJob],
            ``NOW`` refers to the [start_time]
            [google.storagetransfer.v1.TransferOperation.start_time] of
            the ``TransferOperation``.
        max_time_elapsed_since_last_modification (google.protobuf.duration_pb2.Duration):
            If specified, only objects with a "last modification time"
            on or after ``NOW`` -
            ``max_time_elapsed_since_last_modification`` and objects
            that don't have a "last modification time" are transferred.

            For each
            [TransferOperation][google.storagetransfer.v1.TransferOperation]
            started by this
            [TransferJob][google.storagetransfer.v1.TransferJob],
            ``NOW`` refers to the [start_time]
            [google.storagetransfer.v1.TransferOperation.start_time] of
            the ``TransferOperation``.
        include_prefixes (Sequence[str]):
            If you specify ``include_prefixes``, Storage Transfer
            Service uses the items in the ``include_prefixes`` array to
            determine which objects to include in a transfer. Objects
            must start with one of the matching ``include_prefixes`` for
            inclusion in the transfer. If [exclude_prefixes]
            [google.storagetransfer.v1.ObjectConditions.exclude_prefixes]
            is specified, objects must not start with any of the
            ``exclude_prefixes`` specified for inclusion in the
            transfer.

            The following are requirements of ``include_prefixes``:

            -  Each include-prefix can contain any sequence of Unicode
               characters, to a max length of 1024 bytes when
               UTF8-encoded, and must not contain Carriage Return or
               Line Feed characters. Wildcard matching and regular
               expression matching are not supported.

            -  Each include-prefix must omit the leading slash. For
               example, to include the object
               ``s3://my-aws-bucket/logs/y=2015/requests.gz``, specify
               the include-prefix as ``logs/y=2015/requests.gz``.

            -  None of the include-prefix values can be empty, if
               specified.

            -  Each include-prefix must include a distinct portion of
               the object namespace. No include-prefix may be a prefix
               of another include-prefix.

            The max size of ``include_prefixes`` is 1000.

            For more information, see `Filtering objects from
            transfers </storage-transfer/docs/filtering-objects-from-transfers>`__.
        exclude_prefixes (Sequence[str]):
            If you specify ``exclude_prefixes``, Storage Transfer
            Service uses the items in the ``exclude_prefixes`` array to
            determine which objects to exclude from a transfer. Objects
            must not start with one of the matching ``exclude_prefixes``
            for inclusion in a transfer.

            The following are requirements of ``exclude_prefixes``:

            -  Each exclude-prefix can contain any sequence of Unicode
               characters, to a max length of 1024 bytes when
               UTF8-encoded, and must not contain Carriage Return or
               Line Feed characters. Wildcard matching and regular
               expression matching are not supported.

            -  Each exclude-prefix must omit the leading slash. For
               example, to exclude the object
               ``s3://my-aws-bucket/logs/y=2015/requests.gz``, specify
               the exclude-prefix as ``logs/y=2015/requests.gz``.

            -  None of the exclude-prefix values can be empty, if
               specified.

            -  Each exclude-prefix must exclude a distinct portion of
               the object namespace. No exclude-prefix may be a prefix
               of another exclude-prefix.

            -  If [include_prefixes]
               [google.storagetransfer.v1.ObjectConditions.include_prefixes]
               is specified, then each exclude-prefix must start with
               the value of a path explicitly included by
               ``include_prefixes``.

            The max size of ``exclude_prefixes`` is 1000.

            For more information, see `Filtering objects from
            transfers </storage-transfer/docs/filtering-objects-from-transfers>`__.
        last_modified_since (google.protobuf.timestamp_pb2.Timestamp):
            If specified, only objects with a "last modification time"
            on or after this timestamp and objects that don't have a
            "last modification time" are transferred.

            The ``last_modified_since`` and ``last_modified_before``
            fields can be used together for chunked data processing. For
            example, consider a script that processes each day's worth
            of data at a time. For that you'd set each of the fields as
            follows:

            -  ``last_modified_since`` to the start of the day

            -  ``last_modified_before`` to the end of the day
        last_modified_before (google.protobuf.timestamp_pb2.Timestamp):
            If specified, only objects with a "last
            modification time" before this timestamp and
            objects that don't have a "last modification
            time" will be transferred.
    """

    min_time_elapsed_since_last_modification = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    max_time_elapsed_since_last_modification = proto.Field(
        proto.MESSAGE, number=2, message=duration_pb2.Duration,
    )
    include_prefixes = proto.RepeatedField(proto.STRING, number=3,)
    exclude_prefixes = proto.RepeatedField(proto.STRING, number=4,)
    last_modified_since = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    last_modified_before = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )


class GcsData(proto.Message):
    r"""In a GcsData resource, an object's name is the Cloud Storage
    object's name and its "last modification time" refers to the
    object's ``updated`` property of Cloud Storage objects, which
    changes when the content or the metadata of the object is updated.

    Attributes:
        bucket_name (str):
            Required. Cloud Storage bucket name. Must meet `Bucket Name
            Requirements </storage/docs/naming#requirements>`__.
        path (str):
            Root path to transfer objects.

            Must be an empty string or full path name that ends with a
            '/'. This field is treated as an object prefix. As such, it
            should generally not begin with a '/'.

            The root path value must meet `Object Name
            Requirements </storage/docs/naming#objectnames>`__.
    """

    bucket_name = proto.Field(proto.STRING, number=1,)
    path = proto.Field(proto.STRING, number=3,)


class AwsS3Data(proto.Message):
    r"""An AwsS3Data resource can be a data source, but not a data
    sink. In an AwsS3Data resource, an object's name is the S3
    object's key name.

    Attributes:
        bucket_name (str):
            Required. S3 Bucket name (see `Creating a
            bucket <https://docs.aws.amazon.com/AmazonS3/latest/dev/create-bucket-get-location-example.html>`__).
        aws_access_key (google.cloud.storage_transfer_v1.types.AwsAccessKey):
            Input only. AWS access key used to sign the API requests to
            the AWS S3 bucket. Permissions on the bucket must be granted
            to the access ID of the AWS access key. This field is
            required.

            For information on our data retention policy for user
            credentials, see `User
            credentials </storage-transfer/docs/data-retention#user-credentials>`__.
        path (str):
            Root path to transfer objects.
            Must be an empty string or full path name that
            ends with a '/'. This field is treated as an
            object prefix. As such, it should generally not
            begin with a '/'.
        role_arn (str):
            Input only. Role arn to support temporary credentials via
            AssumeRoleWithWebIdentity.

            When role arn is provided, transfer service will fetch
            temporary credentials for the session using
            AssumeRoleWithWebIdentity call for the provided role using
            the [GoogleServiceAccount] for this project.
    """

    bucket_name = proto.Field(proto.STRING, number=1,)
    aws_access_key = proto.Field(proto.MESSAGE, number=2, message="AwsAccessKey",)
    path = proto.Field(proto.STRING, number=3,)
    role_arn = proto.Field(proto.STRING, number=4,)


class AzureBlobStorageData(proto.Message):
    r"""An AzureBlobStorageData resource can be a data source, but not a
    data sink. An AzureBlobStorageData resource represents one Azure
    container. The storage account determines the `Azure
    endpoint <https://docs.microsoft.com/en-us/azure/storage/common/storage-create-storage-account#storage-account-endpoints>`__.
    In an AzureBlobStorageData resource, a blobs's name is the `Azure
    Blob Storage blob's key
    name <https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-names>`__.

    Attributes:
        storage_account (str):
            Required. The name of the Azure Storage
            account.
        azure_credentials (google.cloud.storage_transfer_v1.types.AzureCredentials):
            Required. Input only. Credentials used to authenticate API
            requests to Azure.

            For information on our data retention policy for user
            credentials, see `User
            credentials </storage-transfer/docs/data-retention#user-credentials>`__.
        container (str):
            Required. The container to transfer from the
            Azure Storage account.
        path (str):
            Root path to transfer objects.
            Must be an empty string or full path name that
            ends with a '/'. This field is treated as an
            object prefix. As such, it should generally not
            begin with a '/'.
    """

    storage_account = proto.Field(proto.STRING, number=1,)
    azure_credentials = proto.Field(
        proto.MESSAGE, number=2, message="AzureCredentials",
    )
    container = proto.Field(proto.STRING, number=4,)
    path = proto.Field(proto.STRING, number=5,)


class HttpData(proto.Message):
    r"""An HttpData resource specifies a list of objects on the web to be
    transferred over HTTP. The information of the objects to be
    transferred is contained in a file referenced by a URL. The first
    line in the file must be ``"TsvHttpData-1.0"``, which specifies the
    format of the file. Subsequent lines specify the information of the
    list of objects, one object per list entry. Each entry has the
    following tab-delimited fields:

    -  **HTTP URL** — The location of the object.

    -  **Length** — The size of the object in bytes.

    -  **MD5** — The base64-encoded MD5 hash of the object.

    For an example of a valid TSV file, see `Transferring data from
    URLs <https://cloud.google.com/storage-transfer/docs/create-url-list>`__.

    When transferring data based on a URL list, keep the following in
    mind:

    -  When an object located at ``http(s)://hostname:port/<URL-path>``
       is transferred to a data sink, the name of the object at the data
       sink is ``<hostname>/<URL-path>``.

    -  If the specified size of an object does not match the actual size
       of the object fetched, the object will not be transferred.

    -  If the specified MD5 does not match the MD5 computed from the
       transferred bytes, the object transfer will fail.

    -  Ensure that each URL you specify is publicly accessible. For
       example, in Cloud Storage you can [share an object publicly]
       (/storage/docs/cloud-console#_sharingdata) and get a link to it.

    -  Storage Transfer Service obeys ``robots.txt`` rules and requires
       the source HTTP server to support ``Range`` requests and to
       return a ``Content-Length`` header in each response.

    -  [ObjectConditions][google.storagetransfer.v1.ObjectConditions]
       have no effect when filtering objects to transfer.

    Attributes:
        list_url (str):
            Required. The URL that points to the file
            that stores the object list entries. This file
            must allow public access.  Currently, only URLs
            with HTTP and HTTPS schemes are supported.
    """

    list_url = proto.Field(proto.STRING, number=1,)


class TransferOptions(proto.Message):
    r"""TransferOptions define the actions to be performed on objects
    in a transfer.

    Attributes:
        overwrite_objects_already_existing_in_sink (bool):
            When to overwrite objects that already exist
            in the sink. The default is that only objects
            that are different from the source are
            ovewritten. If true, all objects in the sink
            whose name matches an object in the source will
            be overwritten with the source object.
        delete_objects_unique_in_sink (bool):
            Whether objects that exist only in the sink should be
            deleted.

            **Note:** This option and
            [delete_objects_from_source_after_transfer]
            [google.storagetransfer.v1.TransferOptions.delete_objects_from_source_after_transfer]
            are mutually exclusive.
        delete_objects_from_source_after_transfer (bool):
            Whether objects should be deleted from the source after they
            are transferred to the sink.

            **Note:** This option and [delete_objects_unique_in_sink]
            [google.storagetransfer.v1.TransferOptions.delete_objects_unique_in_sink]
            are mutually exclusive.
    """

    overwrite_objects_already_existing_in_sink = proto.Field(proto.BOOL, number=1,)
    delete_objects_unique_in_sink = proto.Field(proto.BOOL, number=2,)
    delete_objects_from_source_after_transfer = proto.Field(proto.BOOL, number=3,)


class TransferSpec(proto.Message):
    r"""Configuration for running a transfer.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_data_sink (google.cloud.storage_transfer_v1.types.GcsData):
            A Cloud Storage data sink.

            This field is a member of `oneof`_ ``data_sink``.
        gcs_data_source (google.cloud.storage_transfer_v1.types.GcsData):
            A Cloud Storage data source.

            This field is a member of `oneof`_ ``data_source``.
        aws_s3_data_source (google.cloud.storage_transfer_v1.types.AwsS3Data):
            An AWS S3 data source.

            This field is a member of `oneof`_ ``data_source``.
        http_data_source (google.cloud.storage_transfer_v1.types.HttpData):
            An HTTP URL data source.

            This field is a member of `oneof`_ ``data_source``.
        azure_blob_storage_data_source (google.cloud.storage_transfer_v1.types.AzureBlobStorageData):
            An Azure Blob Storage data source.

            This field is a member of `oneof`_ ``data_source``.
        object_conditions (google.cloud.storage_transfer_v1.types.ObjectConditions):
            Only objects that satisfy these object
            conditions are included in the set of data
            source and data sink objects.  Object conditions
            based on objects' "last modification time" do
            not exclude objects in a data sink.
        transfer_options (google.cloud.storage_transfer_v1.types.TransferOptions):
            If the option
            [delete_objects_unique_in_sink][google.storagetransfer.v1.TransferOptions.delete_objects_unique_in_sink]
            is ``true`` and time-based object conditions such as 'last
            modification time' are specified, the request fails with an
            [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT] error.
    """

    gcs_data_sink = proto.Field(
        proto.MESSAGE, number=4, oneof="data_sink", message="GcsData",
    )
    gcs_data_source = proto.Field(
        proto.MESSAGE, number=1, oneof="data_source", message="GcsData",
    )
    aws_s3_data_source = proto.Field(
        proto.MESSAGE, number=2, oneof="data_source", message="AwsS3Data",
    )
    http_data_source = proto.Field(
        proto.MESSAGE, number=3, oneof="data_source", message="HttpData",
    )
    azure_blob_storage_data_source = proto.Field(
        proto.MESSAGE, number=8, oneof="data_source", message="AzureBlobStorageData",
    )
    object_conditions = proto.Field(
        proto.MESSAGE, number=5, message="ObjectConditions",
    )
    transfer_options = proto.Field(proto.MESSAGE, number=6, message="TransferOptions",)


class Schedule(proto.Message):
    r"""Transfers can be scheduled to recur or to run just once.

    Attributes:
        schedule_start_date (google.type.date_pb2.Date):
            Required. The start date of a transfer. Date boundaries are
            determined relative to UTC time. If ``schedule_start_date``
            and
            [start_time_of_day][google.storagetransfer.v1.Schedule.start_time_of_day]
            are in the past relative to the job's creation time, the
            transfer starts the day after you schedule the transfer
            request.

            **Note:** When starting jobs at or near midnight UTC it is
            possible that a job will start later than expected. For
            example, if you send an outbound request on June 1 one
            millisecond prior to midnight UTC and the Storage Transfer
            Service server receives the request on June 2, then it will
            create a TransferJob with ``schedule_start_date`` set to
            June 2 and a ``start_time_of_day`` set to midnight UTC. The
            first scheduled
            [TransferOperation][google.storagetransfer.v1.TransferOperation]
            will take place on June 3 at midnight UTC.
        schedule_end_date (google.type.date_pb2.Date):
            The last day a transfer runs. Date boundaries are determined
            relative to UTC time. A job will run once per 24 hours
            within the following guidelines:

            -  If ``schedule_end_date`` and
               [schedule_start_date][google.storagetransfer.v1.Schedule.schedule_start_date]
               are the same and in the future relative to UTC, the
               transfer is executed only one time.
            -  If ``schedule_end_date`` is later than
               ``schedule_start_date`` and ``schedule_end_date`` is in
               the future relative to UTC, the job will run each day at
               [start_time_of_day][google.storagetransfer.v1.Schedule.start_time_of_day]
               through ``schedule_end_date``.
        start_time_of_day (google.type.timeofday_pb2.TimeOfDay):
            The time in UTC that a transfer job is scheduled to run.
            Transfers may start later than this time.

            If ``start_time_of_day`` is not specified:

            -  One-time transfers run immediately.
            -  Recurring transfers run immediately, and each day at
               midnight UTC, through
               [schedule_end_date][google.storagetransfer.v1.Schedule.schedule_end_date].

            If ``start_time_of_day`` is specified:

            -  One-time transfers run at the specified time.
            -  Recurring transfers run at the specified time each day,
               through ``schedule_end_date``.
        end_time_of_day (google.type.timeofday_pb2.TimeOfDay):
            The time in UTC that no further transfer operations are
            scheduled. Combined with
            [schedule_end_date][google.storagetransfer.v1.Schedule.schedule_end_date],
            ``end_time_of_day`` specifies the end date and time for
            starting new transfer operations. This field must be greater
            than or equal to the timestamp corresponding to the
            combintation of
            [schedule_start_date][google.storagetransfer.v1.Schedule.schedule_start_date]
            and
            [start_time_of_day][google.storagetransfer.v1.Schedule.start_time_of_day],
            and is subject to the following:

            -  If ``end_time_of_day`` is not set and
               ``schedule_end_date`` is set, then a default value of
               ``23:59:59`` is used for ``end_time_of_day``.

            -  If ``end_time_of_day`` is set and ``schedule_end_date``
               is not set, then
               [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT] is
               returned.
        repeat_interval (google.protobuf.duration_pb2.Duration):
            Interval between the start of each scheduled
            TransferOperation. If unspecified, the default
            value is 24 hours. This value may not be less
            than 1 hour.
    """

    schedule_start_date = proto.Field(proto.MESSAGE, number=1, message=date_pb2.Date,)
    schedule_end_date = proto.Field(proto.MESSAGE, number=2, message=date_pb2.Date,)
    start_time_of_day = proto.Field(
        proto.MESSAGE, number=3, message=timeofday_pb2.TimeOfDay,
    )
    end_time_of_day = proto.Field(
        proto.MESSAGE, number=4, message=timeofday_pb2.TimeOfDay,
    )
    repeat_interval = proto.Field(
        proto.MESSAGE, number=5, message=duration_pb2.Duration,
    )


class TransferJob(proto.Message):
    r"""This resource represents the configuration of a transfer job
    that runs periodically.

    Attributes:
        name (str):
            A unique name (within the transfer project) assigned when
            the job is created. If this field is empty in a
            CreateTransferJobRequest, Storage Transfer Service will
            assign a unique name. Otherwise, the specified name is used
            as the unique name for this job.

            If the specified name is in use by a job, the creation
            request fails with an
            [ALREADY_EXISTS][google.rpc.Code.ALREADY_EXISTS] error.

            This name must start with ``"transferJobs/"`` prefix and end
            with a letter or a number, and should be no more than 128
            characters. This name must not start with
            'transferJobs/OPI'. 'transferJobs/OPI' is a reserved prefix.
            Example:
            ``"transferJobs/^(?!OPI)[A-Za-z0-9-._~]*[A-Za-z0-9]$"``

            Invalid job names will fail with an
            [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT] error.
        description (str):
            A description provided by the user for the
            job. Its max length is 1024 bytes when
            Unicode-encoded.
        project_id (str):
            The ID of the Google Cloud Platform Project
            that owns the job.
        transfer_spec (google.cloud.storage_transfer_v1.types.TransferSpec):
            Transfer specification.
        notification_config (google.cloud.storage_transfer_v1.types.NotificationConfig):
            Notification configuration.
        schedule (google.cloud.storage_transfer_v1.types.Schedule):
            Specifies schedule for the transfer job.
            This is an optional field. When the field is not
            set, the job will never execute a transfer,
            unless you invoke RunTransferJob or update the
            job to have a non-empty schedule.
        status (google.cloud.storage_transfer_v1.types.TransferJob.Status):
            Status of the job. This value MUST be specified for
            ``CreateTransferJobRequests``.

            **Note:** The effect of the new job status takes place
            during a subsequent job run. For example, if you change the
            job status from
            [ENABLED][google.storagetransfer.v1.TransferJob.Status.ENABLED]
            to
            [DISABLED][google.storagetransfer.v1.TransferJob.Status.DISABLED],
            and an operation spawned by the transfer is running, the
            status change would not affect the current operation.
        creation_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time that the transfer job
            was created.
        last_modification_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time that the transfer job
            was last modified.
        deletion_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time that the transfer job
            was deleted.
        latest_operation_name (str):
            The name of the most recently started
            TransferOperation of this JobConfig. Present if
            a TransferOperation has been created for this
            JobConfig.
    """

    class Status(proto.Enum):
        r"""The status of the transfer job."""
        STATUS_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        DELETED = 3

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    project_id = proto.Field(proto.STRING, number=3,)
    transfer_spec = proto.Field(proto.MESSAGE, number=4, message="TransferSpec",)
    notification_config = proto.Field(
        proto.MESSAGE, number=11, message="NotificationConfig",
    )
    schedule = proto.Field(proto.MESSAGE, number=5, message="Schedule",)
    status = proto.Field(proto.ENUM, number=6, enum=Status,)
    creation_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    last_modification_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    deletion_time = proto.Field(
        proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,
    )
    latest_operation_name = proto.Field(proto.STRING, number=12,)


class ErrorLogEntry(proto.Message):
    r"""An entry describing an error that has occurred.

    Attributes:
        url (str):
            Required. A URL that refers to the target (a
            data source, a data sink, or an object) with
            which the error is associated.
        error_details (Sequence[str]):
            A list of messages that carry the error
            details.
    """

    url = proto.Field(proto.STRING, number=1,)
    error_details = proto.RepeatedField(proto.STRING, number=3,)


class ErrorSummary(proto.Message):
    r"""A summary of errors by error code, plus a count and sample
    error log entries.

    Attributes:
        error_code (google.rpc.code_pb2.Code):
            Required.
        error_count (int):
            Required. Count of this type of error.
        error_log_entries (Sequence[google.cloud.storage_transfer_v1.types.ErrorLogEntry]):
            Error samples.
            At most 5 error log entries will be recorded for
            a given error code for a single transfer
            operation.
    """

    error_code = proto.Field(proto.ENUM, number=1, enum=code_pb2.Code,)
    error_count = proto.Field(proto.INT64, number=2,)
    error_log_entries = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ErrorLogEntry",
    )


class TransferCounters(proto.Message):
    r"""A collection of counters that report the progress of a
    transfer operation.

    Attributes:
        objects_found_from_source (int):
            Objects found in the data source that are
            scheduled to be transferred, excluding any that
            are filtered based on object conditions or
            skipped due to sync.
        bytes_found_from_source (int):
            Bytes found in the data source that are
            scheduled to be transferred, excluding any that
            are filtered based on object conditions or
            skipped due to sync.
        objects_found_only_from_sink (int):
            Objects found only in the data sink that are
            scheduled to be deleted.
        bytes_found_only_from_sink (int):
            Bytes found only in the data sink that are
            scheduled to be deleted.
        objects_from_source_skipped_by_sync (int):
            Objects in the data source that are not
            transferred because they already exist in the
            data sink.
        bytes_from_source_skipped_by_sync (int):
            Bytes in the data source that are not
            transferred because they already exist in the
            data sink.
        objects_copied_to_sink (int):
            Objects that are copied to the data sink.
        bytes_copied_to_sink (int):
            Bytes that are copied to the data sink.
        objects_deleted_from_source (int):
            Objects that are deleted from the data
            source.
        bytes_deleted_from_source (int):
            Bytes that are deleted from the data source.
        objects_deleted_from_sink (int):
            Objects that are deleted from the data sink.
        bytes_deleted_from_sink (int):
            Bytes that are deleted from the data sink.
        objects_from_source_failed (int):
            Objects in the data source that failed to be
            transferred or that failed to be deleted after
            being transferred.
        bytes_from_source_failed (int):
            Bytes in the data source that failed to be
            transferred or that failed to be deleted after
            being transferred.
        objects_failed_to_delete_from_sink (int):
            Objects that failed to be deleted from the
            data sink.
        bytes_failed_to_delete_from_sink (int):
            Bytes that failed to be deleted from the data
            sink.
    """

    objects_found_from_source = proto.Field(proto.INT64, number=1,)
    bytes_found_from_source = proto.Field(proto.INT64, number=2,)
    objects_found_only_from_sink = proto.Field(proto.INT64, number=3,)
    bytes_found_only_from_sink = proto.Field(proto.INT64, number=4,)
    objects_from_source_skipped_by_sync = proto.Field(proto.INT64, number=5,)
    bytes_from_source_skipped_by_sync = proto.Field(proto.INT64, number=6,)
    objects_copied_to_sink = proto.Field(proto.INT64, number=7,)
    bytes_copied_to_sink = proto.Field(proto.INT64, number=8,)
    objects_deleted_from_source = proto.Field(proto.INT64, number=9,)
    bytes_deleted_from_source = proto.Field(proto.INT64, number=10,)
    objects_deleted_from_sink = proto.Field(proto.INT64, number=11,)
    bytes_deleted_from_sink = proto.Field(proto.INT64, number=12,)
    objects_from_source_failed = proto.Field(proto.INT64, number=13,)
    bytes_from_source_failed = proto.Field(proto.INT64, number=14,)
    objects_failed_to_delete_from_sink = proto.Field(proto.INT64, number=15,)
    bytes_failed_to_delete_from_sink = proto.Field(proto.INT64, number=16,)


class NotificationConfig(proto.Message):
    r"""Specification to configure notifications published to Cloud Pub/Sub.
    Notifications will be published to the customer-provided topic using
    the following ``PubsubMessage.attributes``:

    -  ``"eventType"``: one of the
       [EventType][google.storagetransfer.v1.NotificationConfig.EventType]
       values
    -  ``"payloadFormat"``: one of the
       [PayloadFormat][google.storagetransfer.v1.NotificationConfig.PayloadFormat]
       values
    -  ``"projectId"``: the
       [project_id][google.storagetransfer.v1.TransferOperation.project_id]
       of the ``TransferOperation``
    -  ``"transferJobName"``: the
       [transfer_job_name][google.storagetransfer.v1.TransferOperation.transfer_job_name]
       of the ``TransferOperation``
    -  ``"transferOperationName"``: the
       [name][google.storagetransfer.v1.TransferOperation.name] of the
       ``TransferOperation``

    The ``PubsubMessage.data`` will contain a
    [TransferOperation][google.storagetransfer.v1.TransferOperation]
    resource formatted according to the specified ``PayloadFormat``.

    Attributes:
        pubsub_topic (str):
            Required. The ``Topic.name`` of the Cloud Pub/Sub topic to
            which to publish notifications. Must be of the format:
            ``projects/{project}/topics/{topic}``. Not matching this
            format will result in an
            [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT] error.
        event_types (Sequence[google.cloud.storage_transfer_v1.types.NotificationConfig.EventType]):
            Event types for which a notification is
            desired. If empty, send notifications for all
            event types.
        payload_format (google.cloud.storage_transfer_v1.types.NotificationConfig.PayloadFormat):
            Required. The desired format of the
            notification message payloads.
    """

    class EventType(proto.Enum):
        r"""Enum for specifying event types for which notifications are
        to be published.

        Additional event types may be added in the future. Clients
        should either safely ignore unrecognized event types or
        explicitly specify which event types they are prepared to
        accept.
        """
        EVENT_TYPE_UNSPECIFIED = 0
        TRANSFER_OPERATION_SUCCESS = 1
        TRANSFER_OPERATION_FAILED = 2
        TRANSFER_OPERATION_ABORTED = 3

    class PayloadFormat(proto.Enum):
        r"""Enum for specifying the format of a notification message's
        payload.
        """
        PAYLOAD_FORMAT_UNSPECIFIED = 0
        NONE = 1
        JSON = 2

    pubsub_topic = proto.Field(proto.STRING, number=1,)
    event_types = proto.RepeatedField(proto.ENUM, number=2, enum=EventType,)
    payload_format = proto.Field(proto.ENUM, number=3, enum=PayloadFormat,)


class TransferOperation(proto.Message):
    r"""A description of the execution of a transfer.

    Attributes:
        name (str):
            A globally unique ID assigned by the system.
        project_id (str):
            The ID of the Google Cloud Platform Project
            that owns the operation.
        transfer_spec (google.cloud.storage_transfer_v1.types.TransferSpec):
            Transfer specification.
        notification_config (google.cloud.storage_transfer_v1.types.NotificationConfig):
            Notification configuration.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Start time of this transfer execution.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End time of this transfer execution.
        status (google.cloud.storage_transfer_v1.types.TransferOperation.Status):
            Status of the transfer operation.
        counters (google.cloud.storage_transfer_v1.types.TransferCounters):
            Information about the progress of the
            transfer operation.
        error_breakdowns (Sequence[google.cloud.storage_transfer_v1.types.ErrorSummary]):
            Summarizes errors encountered with sample
            error log entries.
        transfer_job_name (str):
            The name of the transfer job that triggers
            this transfer operation.
    """

    class Status(proto.Enum):
        r"""The status of a TransferOperation."""
        STATUS_UNSPECIFIED = 0
        IN_PROGRESS = 1
        PAUSED = 2
        SUCCESS = 3
        FAILED = 4
        ABORTED = 5
        QUEUED = 6

    name = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)
    transfer_spec = proto.Field(proto.MESSAGE, number=3, message="TransferSpec",)
    notification_config = proto.Field(
        proto.MESSAGE, number=10, message="NotificationConfig",
    )
    start_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    status = proto.Field(proto.ENUM, number=6, enum=Status,)
    counters = proto.Field(proto.MESSAGE, number=7, message="TransferCounters",)
    error_breakdowns = proto.RepeatedField(
        proto.MESSAGE, number=8, message="ErrorSummary",
    )
    transfer_job_name = proto.Field(proto.STRING, number=9,)


__all__ = tuple(sorted(__protobuf__.manifest))
