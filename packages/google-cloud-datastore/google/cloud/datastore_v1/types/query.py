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

from google.cloud.datastore_v1.types import entity as gd_entity
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.v1",
    manifest={
        "EntityResult",
        "Query",
        "KindExpression",
        "PropertyReference",
        "Projection",
        "PropertyOrder",
        "Filter",
        "CompositeFilter",
        "PropertyFilter",
        "GqlQuery",
        "GqlQueryParameter",
        "QueryResultBatch",
    },
)


class EntityResult(proto.Message):
    r"""The result of fetching an entity from Datastore.

    Attributes:
        entity (google.cloud.datastore_v1.types.Entity):
            The resulting entity.
        version (int):
            The version of the entity, a strictly positive number that
            monotonically increases with changes to the entity.

            This field is set for
            [``FULL``][google.datastore.v1.EntityResult.ResultType.FULL]
            entity results.

            For [missing][google.datastore.v1.LookupResponse.missing]
            entities in ``LookupResponse``, this is the version of the
            snapshot that was used to look up the entity, and it is
            always set except for eventually consistent reads.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the entity was last changed. This field is
            set for
            [``FULL``][google.datastore.v1.EntityResult.ResultType.FULL]
            entity results. If this entity is missing, this field will
            not be set.
        cursor (bytes):
            A cursor that points to the position after the result
            entity. Set only when the ``EntityResult`` is part of a
            ``QueryResultBatch`` message.
    """

    class ResultType(proto.Enum):
        r"""Specifies what data the 'entity' field contains. A ``ResultType`` is
        either implied (for example, in ``LookupResponse.missing`` from
        ``datastore.proto``, it is always ``KEY_ONLY``) or specified by
        context (for example, in message ``QueryResultBatch``, field
        ``entity_result_type`` specifies a ``ResultType`` for all the values
        in field ``entity_results``).
        """
        RESULT_TYPE_UNSPECIFIED = 0
        FULL = 1
        PROJECTION = 2
        KEY_ONLY = 3

    entity = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gd_entity.Entity,
    )
    version = proto.Field(
        proto.INT64,
        number=4,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    cursor = proto.Field(
        proto.BYTES,
        number=3,
    )


class Query(proto.Message):
    r"""A query for entities.

    Attributes:
        projection (Sequence[google.cloud.datastore_v1.types.Projection]):
            The projection to return. Defaults to
            returning all properties.
        kind (Sequence[google.cloud.datastore_v1.types.KindExpression]):
            The kinds to query (if empty, returns
            entities of all kinds). Currently at most 1 kind
            may be specified.
        filter (google.cloud.datastore_v1.types.Filter):
            The filter to apply.
        order (Sequence[google.cloud.datastore_v1.types.PropertyOrder]):
            The order to apply to the query results (if
            empty, order is unspecified).
        distinct_on (Sequence[google.cloud.datastore_v1.types.PropertyReference]):
            The properties to make distinct. The query
            results will contain the first result for each
            distinct combination of values for the given
            properties (if empty, all results are returned).
        start_cursor (bytes):
            A starting point for the query results. Query cursors are
            returned in query result batches and `can only be used to
            continue the same
            query <https://cloud.google.com/datastore/docs/concepts/queries#cursors_limits_and_offsets>`__.
        end_cursor (bytes):
            An ending point for the query results. Query cursors are
            returned in query result batches and `can only be used to
            limit the same
            query <https://cloud.google.com/datastore/docs/concepts/queries#cursors_limits_and_offsets>`__.
        offset (int):
            The number of results to skip. Applies before
            limit, but after all other constraints.
            Optional. Must be >= 0 if specified.
        limit (google.protobuf.wrappers_pb2.Int32Value):
            The maximum number of results to return.
            Applies after all other constraints. Optional.
            Unspecified is interpreted as no limit.
            Must be >= 0 if specified.
    """

    projection = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Projection",
    )
    kind = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="KindExpression",
    )
    filter = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Filter",
    )
    order = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="PropertyOrder",
    )
    distinct_on = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="PropertyReference",
    )
    start_cursor = proto.Field(
        proto.BYTES,
        number=7,
    )
    end_cursor = proto.Field(
        proto.BYTES,
        number=8,
    )
    offset = proto.Field(
        proto.INT32,
        number=10,
    )
    limit = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.Int32Value,
    )


class KindExpression(proto.Message):
    r"""A representation of a kind.

    Attributes:
        name (str):
            The name of the kind.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class PropertyReference(proto.Message):
    r"""A reference to a property relative to the kind expressions.

    Attributes:
        name (str):
            The name of the property.
            If name includes "."s, it may be interpreted as
            a property name path.
    """

    name = proto.Field(
        proto.STRING,
        number=2,
    )


class Projection(proto.Message):
    r"""A representation of a property in a projection.

    Attributes:
        property (google.cloud.datastore_v1.types.PropertyReference):
            The property to project.
    """

    property = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PropertyReference",
    )


class PropertyOrder(proto.Message):
    r"""The desired order for a specific property.

    Attributes:
        property (google.cloud.datastore_v1.types.PropertyReference):
            The property to order by.
        direction (google.cloud.datastore_v1.types.PropertyOrder.Direction):
            The direction to order by. Defaults to ``ASCENDING``.
    """

    class Direction(proto.Enum):
        r"""The sort direction."""
        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

    property = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PropertyReference",
    )
    direction = proto.Field(
        proto.ENUM,
        number=2,
        enum=Direction,
    )


class Filter(proto.Message):
    r"""A holder for any type of filter.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        composite_filter (google.cloud.datastore_v1.types.CompositeFilter):
            A composite filter.

            This field is a member of `oneof`_ ``filter_type``.
        property_filter (google.cloud.datastore_v1.types.PropertyFilter):
            A filter on a property.

            This field is a member of `oneof`_ ``filter_type``.
    """

    composite_filter = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="filter_type",
        message="CompositeFilter",
    )
    property_filter = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="filter_type",
        message="PropertyFilter",
    )


class CompositeFilter(proto.Message):
    r"""A filter that merges multiple other filters using the given
    operator.

    Attributes:
        op (google.cloud.datastore_v1.types.CompositeFilter.Operator):
            The operator for combining multiple filters.
        filters (Sequence[google.cloud.datastore_v1.types.Filter]):
            The list of filters to combine.
            Must contain at least one filter.
    """

    class Operator(proto.Enum):
        r"""A composite filter operator."""
        OPERATOR_UNSPECIFIED = 0
        AND = 1

    op = proto.Field(
        proto.ENUM,
        number=1,
        enum=Operator,
    )
    filters = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Filter",
    )


class PropertyFilter(proto.Message):
    r"""A filter on a specific property.

    Attributes:
        property (google.cloud.datastore_v1.types.PropertyReference):
            The property to filter by.
        op (google.cloud.datastore_v1.types.PropertyFilter.Operator):
            The operator to filter by.
        value (google.cloud.datastore_v1.types.Value):
            The value to compare the property to.
    """

    class Operator(proto.Enum):
        r"""A property filter operator."""
        OPERATOR_UNSPECIFIED = 0
        LESS_THAN = 1
        LESS_THAN_OR_EQUAL = 2
        GREATER_THAN = 3
        GREATER_THAN_OR_EQUAL = 4
        EQUAL = 5
        IN = 6
        NOT_EQUAL = 9
        HAS_ANCESTOR = 11
        NOT_IN = 13

    property = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PropertyReference",
    )
    op = proto.Field(
        proto.ENUM,
        number=2,
        enum=Operator,
    )
    value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gd_entity.Value,
    )


class GqlQuery(proto.Message):
    r"""A `GQL
    query <https://cloud.google.com/datastore/docs/apis/gql/gql_reference>`__.

    Attributes:
        query_string (str):
            A string of the format described
            `here <https://cloud.google.com/datastore/docs/apis/gql/gql_reference>`__.
        allow_literals (bool):
            When false, the query string must not contain any literals
            and instead must bind all values. For example,
            ``SELECT * FROM Kind WHERE a = 'string literal'`` is not
            allowed, while ``SELECT * FROM Kind WHERE a = @value`` is.
        named_bindings (Mapping[str, google.cloud.datastore_v1.types.GqlQueryParameter]):
            For each non-reserved named binding site in the query
            string, there must be a named parameter with that name, but
            not necessarily the inverse.

            Key must match regex ``[A-Za-z_$][A-Za-z_$0-9]*``, must not
            match regex ``__.*__``, and must not be ``""``.
        positional_bindings (Sequence[google.cloud.datastore_v1.types.GqlQueryParameter]):
            Numbered binding site @1 references the first numbered
            parameter, effectively using 1-based indexing, rather than
            the usual 0.

            For each binding site numbered i in ``query_string``, there
            must be an i-th numbered parameter. The inverse must also be
            true.
    """

    query_string = proto.Field(
        proto.STRING,
        number=1,
    )
    allow_literals = proto.Field(
        proto.BOOL,
        number=2,
    )
    named_bindings = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=5,
        message="GqlQueryParameter",
    )
    positional_bindings = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="GqlQueryParameter",
    )


class GqlQueryParameter(proto.Message):
    r"""A binding parameter for a GQL query.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        value (google.cloud.datastore_v1.types.Value):
            A value parameter.

            This field is a member of `oneof`_ ``parameter_type``.
        cursor (bytes):
            A query cursor. Query cursors are returned in
            query result batches.

            This field is a member of `oneof`_ ``parameter_type``.
    """

    value = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="parameter_type",
        message=gd_entity.Value,
    )
    cursor = proto.Field(
        proto.BYTES,
        number=3,
        oneof="parameter_type",
    )


class QueryResultBatch(proto.Message):
    r"""A batch of results produced by a query.

    Attributes:
        skipped_results (int):
            The number of results skipped, typically
            because of an offset.
        skipped_cursor (bytes):
            A cursor that points to the position after the last skipped
            result. Will be set when ``skipped_results`` != 0.
        entity_result_type (google.cloud.datastore_v1.types.EntityResult.ResultType):
            The result type for every entity in ``entity_results``.
        entity_results (Sequence[google.cloud.datastore_v1.types.EntityResult]):
            The results for this batch.
        end_cursor (bytes):
            A cursor that points to the position after
            the last result in the batch.
        more_results (google.cloud.datastore_v1.types.QueryResultBatch.MoreResultsType):
            The state of the query after the current
            batch.
        snapshot_version (int):
            The version number of the snapshot this batch was returned
            from. This applies to the range of results from the query's
            ``start_cursor`` (or the beginning of the query if no cursor
            was given) to this batch's ``end_cursor`` (not the query's
            ``end_cursor``).

            In a single transaction, subsequent query result batches for
            the same query can have a greater snapshot version number.
            Each batch's snapshot version is valid for all preceding
            batches. The value will be zero for eventually consistent
            queries.
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            Read timestamp this batch was returned from. This applies to
            the range of results from the query's ``start_cursor`` (or
            the beginning of the query if no cursor was given) to this
            batch's ``end_cursor`` (not the query's ``end_cursor``).

            In a single transaction, subsequent query result batches for
            the same query can have a greater timestamp. Each batch's
            read timestamp is valid for all preceding batches. This
            value will not be set for eventually consistent queries in
            Cloud Datastore.
    """

    class MoreResultsType(proto.Enum):
        r"""The possible values for the ``more_results`` field."""
        MORE_RESULTS_TYPE_UNSPECIFIED = 0
        NOT_FINISHED = 1
        MORE_RESULTS_AFTER_LIMIT = 2
        MORE_RESULTS_AFTER_CURSOR = 4
        NO_MORE_RESULTS = 3

    skipped_results = proto.Field(
        proto.INT32,
        number=6,
    )
    skipped_cursor = proto.Field(
        proto.BYTES,
        number=3,
    )
    entity_result_type = proto.Field(
        proto.ENUM,
        number=1,
        enum="EntityResult.ResultType",
    )
    entity_results = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="EntityResult",
    )
    end_cursor = proto.Field(
        proto.BYTES,
        number=4,
    )
    more_results = proto.Field(
        proto.ENUM,
        number=5,
        enum=MoreResultsType,
    )
    snapshot_version = proto.Field(
        proto.INT64,
        number=7,
    )
    read_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
