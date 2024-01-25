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

from google.cloud.datastore_v1.types import aggregation_result
from google.cloud.datastore_v1.types import entity
from google.cloud.datastore_v1.types import query as gd_query
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.v1",
    manifest={
        "LookupRequest",
        "LookupResponse",
        "RunQueryRequest",
        "RunQueryResponse",
        "RunAggregationQueryRequest",
        "RunAggregationQueryResponse",
        "BeginTransactionRequest",
        "BeginTransactionResponse",
        "RollbackRequest",
        "RollbackResponse",
        "CommitRequest",
        "CommitResponse",
        "AllocateIdsRequest",
        "AllocateIdsResponse",
        "ReserveIdsRequest",
        "ReserveIdsResponse",
        "Mutation",
        "MutationResult",
        "ReadOptions",
        "TransactionOptions",
    },
)


class LookupRequest(proto.Message):
    r"""The request for
    [Datastore.Lookup][google.datastore.v1.Datastore.Lookup].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        read_options (google.cloud.datastore_v1.types.ReadOptions):
            The options for this lookup request.
        keys (MutableSequence[google.cloud.datastore_v1.types.Key]):
            Required. Keys of entities to look up.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    read_options: "ReadOptions" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ReadOptions",
    )
    keys: MutableSequence[entity.Key] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=entity.Key,
    )


class LookupResponse(proto.Message):
    r"""The response for
    [Datastore.Lookup][google.datastore.v1.Datastore.Lookup].

    Attributes:
        found (MutableSequence[google.cloud.datastore_v1.types.EntityResult]):
            Entities found as ``ResultType.FULL`` entities. The order of
            results in this field is undefined and has no relation to
            the order of the keys in the input.
        missing (MutableSequence[google.cloud.datastore_v1.types.EntityResult]):
            Entities not found as ``ResultType.KEY_ONLY`` entities. The
            order of results in this field is undefined and has no
            relation to the order of the keys in the input.
        deferred (MutableSequence[google.cloud.datastore_v1.types.Key]):
            A list of keys that were not looked up due to
            resource constraints. The order of results in
            this field is undefined and has no relation to
            the order of the keys in the input.
        transaction (bytes):
            The identifier of the transaction that was started as part
            of this Lookup request.

            Set only when
            [ReadOptions.new_transaction][google.datastore.v1.ReadOptions.new_transaction]
            was set in
            [LookupRequest.read_options][google.datastore.v1.LookupRequest.read_options].
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which these entities were read or
            found missing.
    """

    found: MutableSequence[gd_query.EntityResult] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gd_query.EntityResult,
    )
    missing: MutableSequence[gd_query.EntityResult] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=gd_query.EntityResult,
    )
    deferred: MutableSequence[entity.Key] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=entity.Key,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=5,
    )
    read_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )


class RunQueryRequest(proto.Message):
    r"""The request for
    [Datastore.RunQuery][google.datastore.v1.Datastore.RunQuery].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        partition_id (google.cloud.datastore_v1.types.PartitionId):
            Entities are partitioned into subsets,
            identified by a partition ID. Queries are scoped
            to a single partition. This partition ID is
            normalized with the standard default context
            partition ID.
        read_options (google.cloud.datastore_v1.types.ReadOptions):
            The options for this query.
        query (google.cloud.datastore_v1.types.Query):
            The query to run.

            This field is a member of `oneof`_ ``query_type``.
        gql_query (google.cloud.datastore_v1.types.GqlQuery):
            The GQL query to run. This query must be a
            non-aggregation query.

            This field is a member of `oneof`_ ``query_type``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    partition_id: entity.PartitionId = proto.Field(
        proto.MESSAGE,
        number=2,
        message=entity.PartitionId,
    )
    read_options: "ReadOptions" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ReadOptions",
    )
    query: gd_query.Query = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="query_type",
        message=gd_query.Query,
    )
    gql_query: gd_query.GqlQuery = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="query_type",
        message=gd_query.GqlQuery,
    )


class RunQueryResponse(proto.Message):
    r"""The response for
    [Datastore.RunQuery][google.datastore.v1.Datastore.RunQuery].

    Attributes:
        batch (google.cloud.datastore_v1.types.QueryResultBatch):
            A batch of query results (always present).
        query (google.cloud.datastore_v1.types.Query):
            The parsed form of the ``GqlQuery`` from the request, if it
            was set.
        transaction (bytes):
            The identifier of the transaction that was started as part
            of this RunQuery request.

            Set only when
            [ReadOptions.new_transaction][google.datastore.v1.ReadOptions.new_transaction]
            was set in
            [RunQueryRequest.read_options][google.datastore.v1.RunQueryRequest.read_options].
    """

    batch: gd_query.QueryResultBatch = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gd_query.QueryResultBatch,
    )
    query: gd_query.Query = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gd_query.Query,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=5,
    )


class RunAggregationQueryRequest(proto.Message):
    r"""The request for
    [Datastore.RunAggregationQuery][google.datastore.v1.Datastore.RunAggregationQuery].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        partition_id (google.cloud.datastore_v1.types.PartitionId):
            Entities are partitioned into subsets,
            identified by a partition ID. Queries are scoped
            to a single partition. This partition ID is
            normalized with the standard default context
            partition ID.
        read_options (google.cloud.datastore_v1.types.ReadOptions):
            The options for this query.
        aggregation_query (google.cloud.datastore_v1.types.AggregationQuery):
            The query to run.

            This field is a member of `oneof`_ ``query_type``.
        gql_query (google.cloud.datastore_v1.types.GqlQuery):
            The GQL query to run. This query must be an
            aggregation query.

            This field is a member of `oneof`_ ``query_type``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    partition_id: entity.PartitionId = proto.Field(
        proto.MESSAGE,
        number=2,
        message=entity.PartitionId,
    )
    read_options: "ReadOptions" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ReadOptions",
    )
    aggregation_query: gd_query.AggregationQuery = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="query_type",
        message=gd_query.AggregationQuery,
    )
    gql_query: gd_query.GqlQuery = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="query_type",
        message=gd_query.GqlQuery,
    )


class RunAggregationQueryResponse(proto.Message):
    r"""The response for
    [Datastore.RunAggregationQuery][google.datastore.v1.Datastore.RunAggregationQuery].

    Attributes:
        batch (google.cloud.datastore_v1.types.AggregationResultBatch):
            A batch of aggregation results. Always
            present.
        query (google.cloud.datastore_v1.types.AggregationQuery):
            The parsed form of the ``GqlQuery`` from the request, if it
            was set.
        transaction (bytes):
            The identifier of the transaction that was started as part
            of this RunAggregationQuery request.

            Set only when
            [ReadOptions.new_transaction][google.datastore.v1.ReadOptions.new_transaction]
            was set in
            [RunAggregationQueryRequest.read_options][google.datastore.v1.RunAggregationQueryRequest.read_options].
    """

    batch: aggregation_result.AggregationResultBatch = proto.Field(
        proto.MESSAGE,
        number=1,
        message=aggregation_result.AggregationResultBatch,
    )
    query: gd_query.AggregationQuery = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gd_query.AggregationQuery,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=5,
    )


class BeginTransactionRequest(proto.Message):
    r"""The request for
    [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        transaction_options (google.cloud.datastore_v1.types.TransactionOptions):
            Options for a new transaction.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    transaction_options: "TransactionOptions" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="TransactionOptions",
    )


class BeginTransactionResponse(proto.Message):
    r"""The response for
    [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

    Attributes:
        transaction (bytes):
            The transaction identifier (always present).
    """

    transaction: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


class RollbackRequest(proto.Message):
    r"""The request for
    [Datastore.Rollback][google.datastore.v1.Datastore.Rollback].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        transaction (bytes):
            Required. The transaction identifier, returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


class RollbackResponse(proto.Message):
    r"""The response for
    [Datastore.Rollback][google.datastore.v1.Datastore.Rollback]. (an
    empty message).

    """


class CommitRequest(proto.Message):
    r"""The request for
    [Datastore.Commit][google.datastore.v1.Datastore.Commit].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        mode (google.cloud.datastore_v1.types.CommitRequest.Mode):
            The type of commit to perform. Defaults to
            ``TRANSACTIONAL``.
        transaction (bytes):
            The identifier of the transaction associated with the
            commit. A transaction identifier is returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

            This field is a member of `oneof`_ ``transaction_selector``.
        single_use_transaction (google.cloud.datastore_v1.types.TransactionOptions):
            Options for beginning a new transaction for this request.
            The transaction is committed when the request completes. If
            specified,
            [TransactionOptions.mode][google.datastore.v1.TransactionOptions]
            must be
            [TransactionOptions.ReadWrite][google.datastore.v1.TransactionOptions.ReadWrite].

            This field is a member of `oneof`_ ``transaction_selector``.
        mutations (MutableSequence[google.cloud.datastore_v1.types.Mutation]):
            The mutations to perform.

            When mode is ``TRANSACTIONAL``, mutations affecting a single
            entity are applied in order. The following sequences of
            mutations affecting a single entity are not permitted in a
            single ``Commit`` request:

            -  ``insert`` followed by ``insert``
            -  ``update`` followed by ``insert``
            -  ``upsert`` followed by ``insert``
            -  ``delete`` followed by ``update``

            When mode is ``NON_TRANSACTIONAL``, no two mutations may
            affect a single entity.
    """

    class Mode(proto.Enum):
        r"""The modes available for commits.

        Values:
            MODE_UNSPECIFIED (0):
                Unspecified. This value must not be used.
            TRANSACTIONAL (1):
                Transactional: The mutations are either all applied, or none
                are applied. Learn about transactions
                `here <https://cloud.google.com/datastore/docs/concepts/transactions>`__.
            NON_TRANSACTIONAL (2):
                Non-transactional: The mutations may not
                apply as all or none.
        """
        MODE_UNSPECIFIED = 0
        TRANSACTIONAL = 1
        NON_TRANSACTIONAL = 2

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    mode: Mode = proto.Field(
        proto.ENUM,
        number=5,
        enum=Mode,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=1,
        oneof="transaction_selector",
    )
    single_use_transaction: "TransactionOptions" = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="transaction_selector",
        message="TransactionOptions",
    )
    mutations: MutableSequence["Mutation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="Mutation",
    )


class CommitResponse(proto.Message):
    r"""The response for
    [Datastore.Commit][google.datastore.v1.Datastore.Commit].

    Attributes:
        mutation_results (MutableSequence[google.cloud.datastore_v1.types.MutationResult]):
            The result of performing the mutations.
            The i-th mutation result corresponds to the i-th
            mutation in the request.
        index_updates (int):
            The number of index entries updated during
            the commit, or zero if none were updated.
        commit_time (google.protobuf.timestamp_pb2.Timestamp):
            The transaction commit timestamp. Not set for
            non-transactional commits.
    """

    mutation_results: MutableSequence["MutationResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="MutationResult",
    )
    index_updates: int = proto.Field(
        proto.INT32,
        number=4,
    )
    commit_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )


class AllocateIdsRequest(proto.Message):
    r"""The request for
    [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        keys (MutableSequence[google.cloud.datastore_v1.types.Key]):
            Required. A list of keys with incomplete key
            paths for which to allocate IDs. No key may be
            reserved/read-only.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    keys: MutableSequence[entity.Key] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=entity.Key,
    )


class AllocateIdsResponse(proto.Message):
    r"""The response for
    [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].

    Attributes:
        keys (MutableSequence[google.cloud.datastore_v1.types.Key]):
            The keys specified in the request (in the
            same order), each with its key path completed
            with a newly allocated ID.
    """

    keys: MutableSequence[entity.Key] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=entity.Key,
    )


class ReserveIdsRequest(proto.Message):
    r"""The request for
    [Datastore.ReserveIds][google.datastore.v1.Datastore.ReserveIds].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            The ID of the database against which to make
            the request.
            '(default)' is not allowed; please use empty
            string '' to refer the default database.
        keys (MutableSequence[google.cloud.datastore_v1.types.Key]):
            Required. A list of keys with complete key
            paths whose numeric IDs should not be
            auto-allocated.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    keys: MutableSequence[entity.Key] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=entity.Key,
    )


class ReserveIdsResponse(proto.Message):
    r"""The response for
    [Datastore.ReserveIds][google.datastore.v1.Datastore.ReserveIds].

    """


class Mutation(proto.Message):
    r"""A mutation to apply to an entity.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        insert (google.cloud.datastore_v1.types.Entity):
            The entity to insert. The entity must not
            already exist. The entity key's final path
            element may be incomplete.

            This field is a member of `oneof`_ ``operation``.
        update (google.cloud.datastore_v1.types.Entity):
            The entity to update. The entity must already
            exist. Must have a complete key path.

            This field is a member of `oneof`_ ``operation``.
        upsert (google.cloud.datastore_v1.types.Entity):
            The entity to upsert. The entity may or may
            not already exist. The entity key's final path
            element may be incomplete.

            This field is a member of `oneof`_ ``operation``.
        delete (google.cloud.datastore_v1.types.Key):
            The key of the entity to delete. The entity
            may or may not already exist. Must have a
            complete key path and must not be
            reserved/read-only.

            This field is a member of `oneof`_ ``operation``.
        base_version (int):
            The version of the entity that this mutation
            is being applied to. If this does not match the
            current version on the server, the mutation
            conflicts.

            This field is a member of `oneof`_ ``conflict_detection_strategy``.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The update time of the entity that this
            mutation is being applied to. If this does not
            match the current update time on the server, the
            mutation conflicts.

            This field is a member of `oneof`_ ``conflict_detection_strategy``.
    """

    insert: entity.Entity = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="operation",
        message=entity.Entity,
    )
    update: entity.Entity = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="operation",
        message=entity.Entity,
    )
    upsert: entity.Entity = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="operation",
        message=entity.Entity,
    )
    delete: entity.Key = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="operation",
        message=entity.Key,
    )
    base_version: int = proto.Field(
        proto.INT64,
        number=8,
        oneof="conflict_detection_strategy",
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="conflict_detection_strategy",
        message=timestamp_pb2.Timestamp,
    )


class MutationResult(proto.Message):
    r"""The result of applying a mutation.

    Attributes:
        key (google.cloud.datastore_v1.types.Key):
            The automatically allocated key.
            Set only when the mutation allocated a key.
        version (int):
            The version of the entity on the server after
            processing the mutation. If the mutation doesn't
            change anything on the server, then the version
            will be the version of the current entity or, if
            no entity is present, a version that is strictly
            greater than the version of any previous entity
            and less than the version of any possible future
            entity.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The create time of the entity. This field
            will not be set after a 'delete'.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The update time of the entity on the server
            after processing the mutation. If the mutation
            doesn't change anything on the server, then the
            timestamp will be the update timestamp of the
            current entity. This field will not be set after
            a 'delete'.
        conflict_detected (bool):
            Whether a conflict was detected for this
            mutation. Always false when a conflict detection
            strategy field is not set in the mutation.
    """

    key: entity.Key = proto.Field(
        proto.MESSAGE,
        number=3,
        message=entity.Key,
    )
    version: int = proto.Field(
        proto.INT64,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    conflict_detected: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class ReadOptions(proto.Message):
    r"""The options shared by read requests.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        read_consistency (google.cloud.datastore_v1.types.ReadOptions.ReadConsistency):
            The non-transactional read consistency to
            use.

            This field is a member of `oneof`_ ``consistency_type``.
        transaction (bytes):
            The identifier of the transaction in which to read. A
            transaction identifier is returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

            This field is a member of `oneof`_ ``consistency_type``.
        new_transaction (google.cloud.datastore_v1.types.TransactionOptions):
            Options for beginning a new transaction for this request.

            The new transaction identifier will be returned in the
            corresponding response as either
            [LookupResponse.transaction][google.datastore.v1.LookupResponse.transaction]
            or
            [RunQueryResponse.transaction][google.datastore.v1.RunQueryResponse.transaction].

            This field is a member of `oneof`_ ``consistency_type``.
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Reads entities as they were at the given
            time. This value is only supported for Cloud
            Firestore in Datastore mode.

            This must be a microsecond precision timestamp
            within the past one hour, or if Point-in-Time
            Recovery is enabled, can additionally be a whole
            minute timestamp within the past 7 days.

            This field is a member of `oneof`_ ``consistency_type``.
    """

    class ReadConsistency(proto.Enum):
        r"""The possible values for read consistencies.

        Values:
            READ_CONSISTENCY_UNSPECIFIED (0):
                Unspecified. This value must not be used.
            STRONG (1):
                Strong consistency.
            EVENTUAL (2):
                Eventual consistency.
        """
        READ_CONSISTENCY_UNSPECIFIED = 0
        STRONG = 1
        EVENTUAL = 2

    read_consistency: ReadConsistency = proto.Field(
        proto.ENUM,
        number=1,
        oneof="consistency_type",
        enum=ReadConsistency,
    )
    transaction: bytes = proto.Field(
        proto.BYTES,
        number=2,
        oneof="consistency_type",
    )
    new_transaction: "TransactionOptions" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="consistency_type",
        message="TransactionOptions",
    )
    read_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="consistency_type",
        message=timestamp_pb2.Timestamp,
    )


class TransactionOptions(proto.Message):
    r"""Options for beginning a new transaction.

    Transactions can be created explicitly with calls to
    [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction]
    or implicitly by setting
    [ReadOptions.new_transaction][google.datastore.v1.ReadOptions.new_transaction]
    in read requests.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        read_write (google.cloud.datastore_v1.types.TransactionOptions.ReadWrite):
            The transaction should allow both reads and
            writes.

            This field is a member of `oneof`_ ``mode``.
        read_only (google.cloud.datastore_v1.types.TransactionOptions.ReadOnly):
            The transaction should only allow reads.

            This field is a member of `oneof`_ ``mode``.
    """

    class ReadWrite(proto.Message):
        r"""Options specific to read / write transactions.

        Attributes:
            previous_transaction (bytes):
                The transaction identifier of the transaction
                being retried.
        """

        previous_transaction: bytes = proto.Field(
            proto.BYTES,
            number=1,
        )

    class ReadOnly(proto.Message):
        r"""Options specific to read-only transactions.

        Attributes:
            read_time (google.protobuf.timestamp_pb2.Timestamp):
                Reads entities at the given time.

                This must be a microsecond precision timestamp
                within the past one hour, or if Point-in-Time
                Recovery is enabled, can additionally be a whole
                minute timestamp within the past 7 days.
        """

        read_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=1,
            message=timestamp_pb2.Timestamp,
        )

    read_write: ReadWrite = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="mode",
        message=ReadWrite,
    )
    read_only: ReadOnly = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="mode",
        message=ReadOnly,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
