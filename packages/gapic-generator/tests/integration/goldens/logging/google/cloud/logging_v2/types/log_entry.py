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

from google.api import monitored_resource_pb2  # type: ignore
from google.logging.type import http_request_pb2  # type: ignore
from google.logging.type import log_severity_pb2  # type: ignore
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.logging.v2',
    manifest={
        'LogEntry',
        'LogEntryOperation',
        'LogEntrySourceLocation',
    },
)


class LogEntry(proto.Message):
    r"""An individual entry in a log.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        log_name (str):
            Required. The resource name of the log to which this log
            entry belongs:

            ::

                "projects/[PROJECT_ID]/logs/[LOG_ID]"
                "organizations/[ORGANIZATION_ID]/logs/[LOG_ID]"
                "billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]"
                "folders/[FOLDER_ID]/logs/[LOG_ID]"

            A project number may be used in place of PROJECT_ID. The
            project number is translated to its corresponding PROJECT_ID
            internally and the ``log_name`` field will contain
            PROJECT_ID in queries and exports.

            ``[LOG_ID]`` must be URL-encoded within ``log_name``.
            Example:
            ``"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity"``.
            ``[LOG_ID]`` must be less than 512 characters long and can
            only include the following characters: upper and lower case
            alphanumeric characters, forward-slash, underscore, hyphen,
            and period.

            For backward compatibility, if ``log_name`` begins with a
            forward-slash, such as ``/projects/...``, then the log entry
            is ingested as usual but the forward-slash is removed.
            Listing the log entry will not show the leading slash and
            filtering for a log name with a leading slash will never
            return any results.
        resource (google.api.monitored_resource_pb2.MonitoredResource):
            Required. The monitored resource that
            produced this log entry.
            Example: a log entry that reports a database
            error would be associated with the monitored
            resource designating the particular database
            that reported the error.
        proto_payload (google.protobuf.any_pb2.Any):
            The log entry payload, represented as a
            protocol buffer. Some Google Cloud Platform
            services use this field for their log entry
            payloads.
            The following protocol buffer types are
            supported; user-defined types are not supported:

            "type.googleapis.com/google.cloud.audit.AuditLog"
            "type.googleapis.com/google.appengine.logging.v1.RequestLog".

            This field is a member of `oneof`_ ``payload``.
        text_payload (str):
            The log entry payload, represented as a
            Unicode string (UTF-8).

            This field is a member of `oneof`_ ``payload``.
        json_payload (google.protobuf.struct_pb2.Struct):
            The log entry payload, represented as a
            structure that is expressed as a JSON object.

            This field is a member of `oneof`_ ``payload``.
        timestamp (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The time the event described by the log entry
            occurred. This time is used to compute the log entry's age
            and to enforce the logs retention period. If this field is
            omitted in a new log entry, then Logging assigns it the
            current time. Timestamps have nanosecond accuracy, but
            trailing zeros in the fractional seconds might be omitted
            when the timestamp is displayed.

            Incoming log entries must have timestamps that don't exceed
            the `logs retention
            period <https://cloud.google.com/logging/quotas#logs_retention_periods>`__
            in the past, and that don't exceed 24 hours in the future.
            Log entries outside those time boundaries aren't ingested by
            Logging.
        receive_timestamp (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the log entry was
            received by Logging.
        severity (google.logging.type.log_severity_pb2.LogSeverity):
            Optional. The severity of the log entry. The default value
            is ``LogSeverity.DEFAULT``.
        insert_id (str):
            Optional. A unique identifier for the log entry. If you
            provide a value, then Logging considers other log entries in
            the same project, with the same ``timestamp``, and with the
            same ``insert_id`` to be duplicates which are removed in a
            single query result. However, there are no guarantees of
            de-duplication in the export of logs.

            If the ``insert_id`` is omitted when writing a log entry,
            the Logging API assigns its own unique identifier in this
            field.

            In queries, the ``insert_id`` is also used to order log
            entries that have the same ``log_name`` and ``timestamp``
            values.
        http_request (google.logging.type.http_request_pb2.HttpRequest):
            Optional. Information about the HTTP request
            associated with this log entry, if applicable.
        labels (Mapping[str, str]):
            Optional. A set of user-defined (key, value)
            data that provides additional information about
            the log entry.
        operation (google.cloud.logging_v2.types.LogEntryOperation):
            Optional. Information about an operation
            associated with the log entry, if applicable.
        trace (str):
            Optional. Resource name of the trace associated with the log
            entry, if any. If it contains a relative resource name, the
            name is assumed to be relative to
            ``//tracing.googleapis.com``. Example:
            ``projects/my-projectid/traces/06796866738c859f2f19b7cfb3214824``
        span_id (str):
            Optional. The span ID within the trace associated with the
            log entry.

            For Trace spans, this is the same format that the Trace API
            v2 uses: a 16-character hexadecimal encoding of an 8-byte
            array, such as ``000000000000004a``.
        trace_sampled (bool):
            Optional. The sampling decision of the trace associated with
            the log entry.

            True means that the trace resource name in the ``trace``
            field was sampled for storage in a trace backend. False
            means that the trace was not sampled for storage when this
            log entry was written, or the sampling decision was unknown
            at the time. A non-sampled ``trace`` value is still useful
            as a request correlation identifier. The default is False.
        source_location (google.cloud.logging_v2.types.LogEntrySourceLocation):
            Optional. Source code location information
            associated with the log entry, if any.
    """

    log_name = proto.Field(
        proto.STRING,
        number=12,
    )
    resource = proto.Field(
        proto.MESSAGE,
        number=8,
        message=monitored_resource_pb2.MonitoredResource,
    )
    proto_payload = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof='payload',
        message=any_pb2.Any,
    )
    text_payload = proto.Field(
        proto.STRING,
        number=3,
        oneof='payload',
    )
    json_payload = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof='payload',
        message=struct_pb2.Struct,
    )
    timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    receive_timestamp = proto.Field(
        proto.MESSAGE,
        number=24,
        message=timestamp_pb2.Timestamp,
    )
    severity = proto.Field(
        proto.ENUM,
        number=10,
        enum=log_severity_pb2.LogSeverity,
    )
    insert_id = proto.Field(
        proto.STRING,
        number=4,
    )
    http_request = proto.Field(
        proto.MESSAGE,
        number=7,
        message=http_request_pb2.HttpRequest,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=11,
    )
    operation = proto.Field(
        proto.MESSAGE,
        number=15,
        message='LogEntryOperation',
    )
    trace = proto.Field(
        proto.STRING,
        number=22,
    )
    span_id = proto.Field(
        proto.STRING,
        number=27,
    )
    trace_sampled = proto.Field(
        proto.BOOL,
        number=30,
    )
    source_location = proto.Field(
        proto.MESSAGE,
        number=23,
        message='LogEntrySourceLocation',
    )


class LogEntryOperation(proto.Message):
    r"""Additional information about a potentially long-running
    operation with which a log entry is associated.

    Attributes:
        id (str):
            Optional. An arbitrary operation identifier.
            Log entries with the same identifier are assumed
            to be part of the same operation.
        producer (str):
            Optional. An arbitrary producer identifier. The combination
            of ``id`` and ``producer`` must be globally unique. Examples
            for ``producer``: ``"MyDivision.MyBigCompany.com"``,
            ``"github.com/MyProject/MyApplication"``.
        first (bool):
            Optional. Set this to True if this is the
            first log entry in the operation.
        last (bool):
            Optional. Set this to True if this is the
            last log entry in the operation.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    producer = proto.Field(
        proto.STRING,
        number=2,
    )
    first = proto.Field(
        proto.BOOL,
        number=3,
    )
    last = proto.Field(
        proto.BOOL,
        number=4,
    )


class LogEntrySourceLocation(proto.Message):
    r"""Additional information about the source code location that
    produced the log entry.

    Attributes:
        file (str):
            Optional. Source file name. Depending on the
            runtime environment, this might be a simple name
            or a fully-qualified name.
        line (int):
            Optional. Line within the source file.
            1-based; 0 indicates no line number available.
        function (str):
            Optional. Human-readable name of the function or method
            being invoked, with optional context such as the class or
            package name. This information may be used in contexts such
            as the logs viewer, where a file and line number are less
            meaningful. The format can vary by language. For example:
            ``qual.if.ied.Class.method`` (Java), ``dir/package.func``
            (Go), ``function`` (Python).
    """

    file = proto.Field(
        proto.STRING,
        number=1,
    )
    line = proto.Field(
        proto.INT64,
        number=2,
    )
    function = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
