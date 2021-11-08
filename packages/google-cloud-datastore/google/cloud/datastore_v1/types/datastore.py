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

from google.cloud.datastore_v1.types import entity
from google.cloud.datastore_v1.types import query as gd_query


__protobuf__ = proto.module(
    package="google.datastore.v1",
    manifest={
        "LookupRequest",
        "LookupResponse",
        "RunQueryRequest",
        "RunQueryResponse",
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
        read_options (google.cloud.datastore_v1.types.ReadOptions):
            The options for this lookup request.
        keys (Sequence[google.cloud.datastore_v1.types.Key]):
            Required. Keys of entities to look up.
    """

    project_id = proto.Field(proto.STRING, number=8,)
    read_options = proto.Field(proto.MESSAGE, number=1, message="ReadOptions",)
    keys = proto.RepeatedField(proto.MESSAGE, number=3, message=entity.Key,)


class LookupResponse(proto.Message):
    r"""The response for
    [Datastore.Lookup][google.datastore.v1.Datastore.Lookup].

    Attributes:
        found (Sequence[google.cloud.datastore_v1.types.EntityResult]):
            Entities found as ``ResultType.FULL`` entities. The order of
            results in this field is undefined and has no relation to
            the order of the keys in the input.
        missing (Sequence[google.cloud.datastore_v1.types.EntityResult]):
            Entities not found as ``ResultType.KEY_ONLY`` entities. The
            order of results in this field is undefined and has no
            relation to the order of the keys in the input.
        deferred (Sequence[google.cloud.datastore_v1.types.Key]):
            A list of keys that were not looked up due to
            resource constraints. The order of results in
            this field is undefined and has no relation to
            the order of the keys in the input.
    """

    found = proto.RepeatedField(proto.MESSAGE, number=1, message=gd_query.EntityResult,)
    missing = proto.RepeatedField(
        proto.MESSAGE, number=2, message=gd_query.EntityResult,
    )
    deferred = proto.RepeatedField(proto.MESSAGE, number=3, message=entity.Key,)


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
            The GQL query to run.
            This field is a member of `oneof`_ ``query_type``.
    """

    project_id = proto.Field(proto.STRING, number=8,)
    partition_id = proto.Field(proto.MESSAGE, number=2, message=entity.PartitionId,)
    read_options = proto.Field(proto.MESSAGE, number=1, message="ReadOptions",)
    query = proto.Field(
        proto.MESSAGE, number=3, oneof="query_type", message=gd_query.Query,
    )
    gql_query = proto.Field(
        proto.MESSAGE, number=7, oneof="query_type", message=gd_query.GqlQuery,
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
    """

    batch = proto.Field(proto.MESSAGE, number=1, message=gd_query.QueryResultBatch,)
    query = proto.Field(proto.MESSAGE, number=2, message=gd_query.Query,)


class BeginTransactionRequest(proto.Message):
    r"""The request for
    [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        transaction_options (google.cloud.datastore_v1.types.TransactionOptions):
            Options for a new transaction.
    """

    project_id = proto.Field(proto.STRING, number=8,)
    transaction_options = proto.Field(
        proto.MESSAGE, number=10, message="TransactionOptions",
    )


class BeginTransactionResponse(proto.Message):
    r"""The response for
    [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

    Attributes:
        transaction (bytes):
            The transaction identifier (always present).
    """

    transaction = proto.Field(proto.BYTES, number=1,)


class RollbackRequest(proto.Message):
    r"""The request for
    [Datastore.Rollback][google.datastore.v1.Datastore.Rollback].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        transaction (bytes):
            Required. The transaction identifier, returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].
    """

    project_id = proto.Field(proto.STRING, number=8,)
    transaction = proto.Field(proto.BYTES, number=1,)


class RollbackResponse(proto.Message):
    r"""The response for
    [Datastore.Rollback][google.datastore.v1.Datastore.Rollback]. (an
    empty message).

    """


class CommitRequest(proto.Message):
    r"""The request for
    [Datastore.Commit][google.datastore.v1.Datastore.Commit].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        mode (google.cloud.datastore_v1.types.CommitRequest.Mode):
            The type of commit to perform. Defaults to
            ``TRANSACTIONAL``.
        transaction (bytes):
            The identifier of the transaction associated with the
            commit. A transaction identifier is returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].
            This field is a member of `oneof`_ ``transaction_selector``.
        mutations (Sequence[google.cloud.datastore_v1.types.Mutation]):
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
        r"""The modes available for commits."""
        MODE_UNSPECIFIED = 0
        TRANSACTIONAL = 1
        NON_TRANSACTIONAL = 2

    project_id = proto.Field(proto.STRING, number=8,)
    mode = proto.Field(proto.ENUM, number=5, enum=Mode,)
    transaction = proto.Field(proto.BYTES, number=1, oneof="transaction_selector",)
    mutations = proto.RepeatedField(proto.MESSAGE, number=6, message="Mutation",)


class CommitResponse(proto.Message):
    r"""The response for
    [Datastore.Commit][google.datastore.v1.Datastore.Commit].

    Attributes:
        mutation_results (Sequence[google.cloud.datastore_v1.types.MutationResult]):
            The result of performing the mutations.
            The i-th mutation result corresponds to the i-th
            mutation in the request.
        index_updates (int):
            The number of index entries updated during
            the commit, or zero if none were updated.
    """

    mutation_results = proto.RepeatedField(
        proto.MESSAGE, number=3, message="MutationResult",
    )
    index_updates = proto.Field(proto.INT32, number=4,)


class AllocateIdsRequest(proto.Message):
    r"""The request for
    [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        keys (Sequence[google.cloud.datastore_v1.types.Key]):
            Required. A list of keys with incomplete key
            paths for which to allocate IDs. No key may be
            reserved/read-only.
    """

    project_id = proto.Field(proto.STRING, number=8,)
    keys = proto.RepeatedField(proto.MESSAGE, number=1, message=entity.Key,)


class AllocateIdsResponse(proto.Message):
    r"""The response for
    [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].

    Attributes:
        keys (Sequence[google.cloud.datastore_v1.types.Key]):
            The keys specified in the request (in the
            same order), each with its key path completed
            with a newly allocated ID.
    """

    keys = proto.RepeatedField(proto.MESSAGE, number=1, message=entity.Key,)


class ReserveIdsRequest(proto.Message):
    r"""The request for
    [Datastore.ReserveIds][google.datastore.v1.Datastore.ReserveIds].

    Attributes:
        project_id (str):
            Required. The ID of the project against which
            to make the request.
        database_id (str):
            If not empty, the ID of the database against
            which to make the request.
        keys (Sequence[google.cloud.datastore_v1.types.Key]):
            Required. A list of keys with complete key
            paths whose numeric IDs should not be auto-
            allocated.
    """

    project_id = proto.Field(proto.STRING, number=8,)
    database_id = proto.Field(proto.STRING, number=9,)
    keys = proto.RepeatedField(proto.MESSAGE, number=1, message=entity.Key,)


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
            complete key path and must not be reserved/read-
            only.
            This field is a member of `oneof`_ ``operation``.
        base_version (int):
            The version of the entity that this mutation
            is being applied to. If this does not match the
            current version on the server, the mutation
            conflicts.
            This field is a member of `oneof`_ ``conflict_detection_strategy``.
    """

    insert = proto.Field(
        proto.MESSAGE, number=4, oneof="operation", message=entity.Entity,
    )
    update = proto.Field(
        proto.MESSAGE, number=5, oneof="operation", message=entity.Entity,
    )
    upsert = proto.Field(
        proto.MESSAGE, number=6, oneof="operation", message=entity.Entity,
    )
    delete = proto.Field(
        proto.MESSAGE, number=7, oneof="operation", message=entity.Key,
    )
    base_version = proto.Field(
        proto.INT64, number=8, oneof="conflict_detection_strategy",
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
        conflict_detected (bool):
            Whether a conflict was detected for this
            mutation. Always false when a conflict detection
            strategy field is not set in the mutation.
    """

    key = proto.Field(proto.MESSAGE, number=3, message=entity.Key,)
    version = proto.Field(proto.INT64, number=4,)
    conflict_detected = proto.Field(proto.BOOL, number=5,)


class ReadOptions(proto.Message):
    r"""The options shared by read requests.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        read_consistency (google.cloud.datastore_v1.types.ReadOptions.ReadConsistency):
            The non-transactional read consistency to use. Cannot be set
            to ``STRONG`` for global queries.
            This field is a member of `oneof`_ ``consistency_type``.
        transaction (bytes):
            The identifier of the transaction in which to read. A
            transaction identifier is returned by a call to
            [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].
            This field is a member of `oneof`_ ``consistency_type``.
    """

    class ReadConsistency(proto.Enum):
        r"""The possible values for read consistencies."""
        READ_CONSISTENCY_UNSPECIFIED = 0
        STRONG = 1
        EVENTUAL = 2

    read_consistency = proto.Field(
        proto.ENUM, number=1, oneof="consistency_type", enum=ReadConsistency,
    )
    transaction = proto.Field(proto.BYTES, number=2, oneof="consistency_type",)


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

        previous_transaction = proto.Field(proto.BYTES, number=1,)

    class ReadOnly(proto.Message):
        r"""Options specific to read-only transactions.
        """

    read_write = proto.Field(proto.MESSAGE, number=1, oneof="mode", message=ReadWrite,)
    read_only = proto.Field(proto.MESSAGE, number=2, oneof="mode", message=ReadOnly,)


__all__ = tuple(sorted(__protobuf__.manifest))
