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


from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.spanner.v1",
    manifest={"TransactionOptions", "Transaction", "TransactionSelector",},
)


class TransactionOptions(proto.Message):
    r"""TransactionOptions are used to specify different types of transactions.

    For more info, see: https://cloud.google.com/spanner/docs/reference/rest/v1/Transaction

    Attributes:
        read_write (~.transaction.TransactionOptions.ReadWrite):
            Transaction may write.

            Authorization to begin a read-write transaction requires
            ``spanner.databases.beginOrRollbackReadWriteTransaction``
            permission on the ``session`` resource.
        partitioned_dml (~.transaction.TransactionOptions.PartitionedDml):
            Partitioned DML transaction.

            Authorization to begin a Partitioned DML transaction
            requires
            ``spanner.databases.beginPartitionedDmlTransaction``
            permission on the ``session`` resource.
        read_only (~.transaction.TransactionOptions.ReadOnly):
            Transaction will not write.

            Authorization to begin a read-only transaction requires
            ``spanner.databases.beginReadOnlyTransaction`` permission on
            the ``session`` resource.
    """

    class ReadWrite(proto.Message):
        r"""Message type to initiate a read-write transaction. Currently
        this transaction type has no options.
        """

    class PartitionedDml(proto.Message):
        r"""Message type to initiate a Partitioned DML transaction."""

    class ReadOnly(proto.Message):
        r"""Message type to initiate a read-only transaction.

        Attributes:
            strong (bool):
                Read at a timestamp where all previously
                committed transactions are visible.
            min_read_timestamp (~.timestamp.Timestamp):
                Executes all reads at a timestamp >= ``min_read_timestamp``.

                This is useful for requesting fresher data than some
                previous read, or data that is fresh enough to observe the
                effects of some previously committed transaction whose
                timestamp is known.

                Note that this option can only be used in single-use
                transactions.

                A timestamp in RFC3339 UTC "Zulu" format, accurate to
                nanoseconds. Example: ``"2014-10-02T15:01:23.045123456Z"``.
            max_staleness (~.duration.Duration):
                Read data at a timestamp >= ``NOW - max_staleness`` seconds.
                Guarantees that all writes that have committed more than the
                specified number of seconds ago are visible. Because Cloud
                Spanner chooses the exact timestamp, this mode works even if
                the client's local clock is substantially skewed from Cloud
                Spanner commit timestamps.

                Useful for reading the freshest data available at a nearby
                replica, while bounding the possible staleness if the local
                replica has fallen behind.

                Note that this option can only be used in single-use
                transactions.
            read_timestamp (~.timestamp.Timestamp):
                Executes all reads at the given timestamp. Unlike other
                modes, reads at a specific timestamp are repeatable; the
                same read at the same timestamp always returns the same
                data. If the timestamp is in the future, the read will block
                until the specified timestamp, modulo the read's deadline.

                Useful for large scale consistent reads such as mapreduces,
                or for coordinating many reads against a consistent snapshot
                of the data.

                A timestamp in RFC3339 UTC "Zulu" format, accurate to
                nanoseconds. Example: ``"2014-10-02T15:01:23.045123456Z"``.
            exact_staleness (~.duration.Duration):
                Executes all reads at a timestamp that is
                ``exact_staleness`` old. The timestamp is chosen soon after
                the read is started.

                Guarantees that all writes that have committed more than the
                specified number of seconds ago are visible. Because Cloud
                Spanner chooses the exact timestamp, this mode works even if
                the client's local clock is substantially skewed from Cloud
                Spanner commit timestamps.

                Useful for reading at nearby replicas without the
                distributed timestamp negotiation overhead of
                ``max_staleness``.
            return_read_timestamp (bool):
                If true, the Cloud Spanner-selected read timestamp is
                included in the [Transaction][google.spanner.v1.Transaction]
                message that describes the transaction.
        """

        strong = proto.Field(proto.BOOL, number=1, oneof="timestamp_bound")

        min_read_timestamp = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="timestamp_bound",
            message=timestamp.Timestamp,
        )

        max_staleness = proto.Field(
            proto.MESSAGE, number=3, oneof="timestamp_bound", message=duration.Duration,
        )

        read_timestamp = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="timestamp_bound",
            message=timestamp.Timestamp,
        )

        exact_staleness = proto.Field(
            proto.MESSAGE, number=5, oneof="timestamp_bound", message=duration.Duration,
        )

        return_read_timestamp = proto.Field(proto.BOOL, number=6)

    read_write = proto.Field(proto.MESSAGE, number=1, oneof="mode", message=ReadWrite,)

    partitioned_dml = proto.Field(
        proto.MESSAGE, number=3, oneof="mode", message=PartitionedDml,
    )

    read_only = proto.Field(proto.MESSAGE, number=2, oneof="mode", message=ReadOnly,)


class Transaction(proto.Message):
    r"""A transaction.

    Attributes:
        id (bytes):
            ``id`` may be used to identify the transaction in subsequent
            [Read][google.spanner.v1.Spanner.Read],
            [ExecuteSql][google.spanner.v1.Spanner.ExecuteSql],
            [Commit][google.spanner.v1.Spanner.Commit], or
            [Rollback][google.spanner.v1.Spanner.Rollback] calls.

            Single-use read-only transactions do not have IDs, because
            single-use transactions do not support multiple requests.
        read_timestamp (~.timestamp.Timestamp):
            For snapshot read-only transactions, the read timestamp
            chosen for the transaction. Not returned by default: see
            [TransactionOptions.ReadOnly.return_read_timestamp][google.spanner.v1.TransactionOptions.ReadOnly.return_read_timestamp].

            A timestamp in RFC3339 UTC "Zulu" format, accurate to
            nanoseconds. Example: ``"2014-10-02T15:01:23.045123456Z"``.
    """

    id = proto.Field(proto.BYTES, number=1)

    read_timestamp = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)


class TransactionSelector(proto.Message):
    r"""This message is used to select the transaction in which a
    [Read][google.spanner.v1.Spanner.Read] or
    [ExecuteSql][google.spanner.v1.Spanner.ExecuteSql] call runs.

    See [TransactionOptions][google.spanner.v1.TransactionOptions] for
    more information about transactions.

    Attributes:
        single_use (~.transaction.TransactionOptions):
            Execute the read or SQL query in a temporary
            transaction. This is the most efficient way to
            execute a transaction that consists of a single
            SQL query.
        id (bytes):
            Execute the read or SQL query in a
            previously-started transaction.
        begin (~.transaction.TransactionOptions):
            Begin a new transaction and execute this read or SQL query
            in it. The transaction ID of the new transaction is returned
            in
            [ResultSetMetadata.transaction][google.spanner.v1.ResultSetMetadata.transaction],
            which is a [Transaction][google.spanner.v1.Transaction].
    """

    single_use = proto.Field(
        proto.MESSAGE, number=1, oneof="selector", message="TransactionOptions",
    )

    id = proto.Field(proto.BYTES, number=2, oneof="selector")

    begin = proto.Field(
        proto.MESSAGE, number=3, oneof="selector", message="TransactionOptions",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
