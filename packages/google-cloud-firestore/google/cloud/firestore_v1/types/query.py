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


from google.cloud.firestore_v1.types import document
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.v1", manifest={"StructuredQuery", "Cursor",},
)


class StructuredQuery(proto.Message):
    r"""A Firestore query.

    Attributes:
        select (~.query.StructuredQuery.Projection):
            The projection to return.
        from_ (Sequence[~.query.StructuredQuery.CollectionSelector]):
            The collections to query.
        where (~.query.StructuredQuery.Filter):
            The filter to apply.
        order_by (Sequence[~.query.StructuredQuery.Order]):
            The order to apply to the query results.

            Firestore guarantees a stable ordering through the following
            rules:

            -  Any field required to appear in ``order_by``, that is not
               already specified in ``order_by``, is appended to the
               order in field name order by default.
            -  If an order on ``__name__`` is not specified, it is
               appended by default.

            Fields are appended with the same sort direction as the last
            order specified, or 'ASCENDING' if no order was specified.
            For example:

            -  ``SELECT * FROM Foo ORDER BY A`` becomes
               ``SELECT * FROM Foo ORDER BY A, __name__``
            -  ``SELECT * FROM Foo ORDER BY A DESC`` becomes
               ``SELECT * FROM Foo ORDER BY A DESC, __name__ DESC``
            -  ``SELECT * FROM Foo WHERE A > 1`` becomes
               ``SELECT * FROM Foo WHERE A > 1 ORDER BY A, __name__``
        start_at (~.query.Cursor):
            A starting point for the query results.
        end_at (~.query.Cursor):
            A end point for the query results.
        offset (int):
            The number of results to skip.
            Applies before limit, but after all other
            constraints. Must be >= 0 if specified.
        limit (~.wrappers.Int32Value):
            The maximum number of results to return.
            Applies after all other constraints.
            Must be >= 0 if specified.
    """

    class Direction(proto.Enum):
        r"""A sort direction."""
        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

    class CollectionSelector(proto.Message):
        r"""A selection of a collection, such as ``messages as m1``.

        Attributes:
            collection_id (str):
                The collection ID.
                When set, selects only collections with this ID.
            all_descendants (bool):
                When false, selects only collections that are immediate
                children of the ``parent`` specified in the containing
                ``RunQueryRequest``. When true, selects all descendant
                collections.
        """

        collection_id = proto.Field(proto.STRING, number=2)

        all_descendants = proto.Field(proto.BOOL, number=3)

    class Filter(proto.Message):
        r"""A filter.

        Attributes:
            composite_filter (~.query.StructuredQuery.CompositeFilter):
                A composite filter.
            field_filter (~.query.StructuredQuery.FieldFilter):
                A filter on a document field.
            unary_filter (~.query.StructuredQuery.UnaryFilter):
                A filter that takes exactly one argument.
        """

        composite_filter = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="filter_type",
            message="StructuredQuery.CompositeFilter",
        )

        field_filter = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="filter_type",
            message="StructuredQuery.FieldFilter",
        )

        unary_filter = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="filter_type",
            message="StructuredQuery.UnaryFilter",
        )

    class CompositeFilter(proto.Message):
        r"""A filter that merges multiple other filters using the given
        operator.

        Attributes:
            op (~.query.StructuredQuery.CompositeFilter.Operator):
                The operator for combining multiple filters.
            filters (Sequence[~.query.StructuredQuery.Filter]):
                The list of filters to combine.
                Must contain at least one filter.
        """

        class Operator(proto.Enum):
            r"""A composite filter operator."""
            OPERATOR_UNSPECIFIED = 0
            AND = 1

        op = proto.Field(
            proto.ENUM, number=1, enum="StructuredQuery.CompositeFilter.Operator",
        )

        filters = proto.RepeatedField(
            proto.MESSAGE, number=2, message="StructuredQuery.Filter",
        )

    class FieldFilter(proto.Message):
        r"""A filter on a specific field.

        Attributes:
            field (~.query.StructuredQuery.FieldReference):
                The field to filter by.
            op (~.query.StructuredQuery.FieldFilter.Operator):
                The operator to filter by.
            value (~.document.Value):
                The value to compare to.
        """

        class Operator(proto.Enum):
            r"""A field filter operator."""
            OPERATOR_UNSPECIFIED = 0
            LESS_THAN = 1
            LESS_THAN_OR_EQUAL = 2
            GREATER_THAN = 3
            GREATER_THAN_OR_EQUAL = 4
            EQUAL = 5
            NOT_EQUAL = 6
            ARRAY_CONTAINS = 7
            IN = 8
            ARRAY_CONTAINS_ANY = 9
            NOT_IN = 10

        field = proto.Field(
            proto.MESSAGE, number=1, message="StructuredQuery.FieldReference",
        )

        op = proto.Field(
            proto.ENUM, number=2, enum="StructuredQuery.FieldFilter.Operator",
        )

        value = proto.Field(proto.MESSAGE, number=3, message=document.Value,)

    class UnaryFilter(proto.Message):
        r"""A filter with a single operand.

        Attributes:
            op (~.query.StructuredQuery.UnaryFilter.Operator):
                The unary operator to apply.
            field (~.query.StructuredQuery.FieldReference):
                The field to which to apply the operator.
        """

        class Operator(proto.Enum):
            r"""A unary operator."""
            OPERATOR_UNSPECIFIED = 0
            IS_NAN = 2
            IS_NULL = 3
            IS_NOT_NAN = 4
            IS_NOT_NULL = 5

        op = proto.Field(
            proto.ENUM, number=1, enum="StructuredQuery.UnaryFilter.Operator",
        )

        field = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="operand_type",
            message="StructuredQuery.FieldReference",
        )

    class Order(proto.Message):
        r"""An order on a field.

        Attributes:
            field (~.query.StructuredQuery.FieldReference):
                The field to order by.
            direction (~.query.StructuredQuery.Direction):
                The direction to order by. Defaults to ``ASCENDING``.
        """

        field = proto.Field(
            proto.MESSAGE, number=1, message="StructuredQuery.FieldReference",
        )

        direction = proto.Field(proto.ENUM, number=2, enum="StructuredQuery.Direction",)

    class FieldReference(proto.Message):
        r"""A reference to a field, such as ``max(messages.time) as max_time``.

        Attributes:
            field_path (str):

        """

        field_path = proto.Field(proto.STRING, number=2)

    class Projection(proto.Message):
        r"""The projection of document's fields to return.

        Attributes:
            fields (Sequence[~.query.StructuredQuery.FieldReference]):
                The fields to return.

                If empty, all fields are returned. To only return the name
                of the document, use ``['__name__']``.
        """

        fields = proto.RepeatedField(
            proto.MESSAGE, number=2, message="StructuredQuery.FieldReference",
        )

    select = proto.Field(proto.MESSAGE, number=1, message=Projection,)

    from_ = proto.RepeatedField(proto.MESSAGE, number=2, message=CollectionSelector,)

    where = proto.Field(proto.MESSAGE, number=3, message=Filter,)

    order_by = proto.RepeatedField(proto.MESSAGE, number=4, message=Order,)

    start_at = proto.Field(proto.MESSAGE, number=7, message="Cursor",)

    end_at = proto.Field(proto.MESSAGE, number=8, message="Cursor",)

    offset = proto.Field(proto.INT32, number=6)

    limit = proto.Field(proto.MESSAGE, number=5, message=wrappers.Int32Value,)


class Cursor(proto.Message):
    r"""A position in a query result set.

    Attributes:
        values (Sequence[~.document.Value]):
            The values that represent a position, in the
            order they appear in the order by clause of a
            query.
            Can contain fewer values than specified in the
            order by clause.
        before (bool):
            If the position is just before or just after
            the given values, relative to the sort order
            defined by the query.
    """

    values = proto.RepeatedField(proto.MESSAGE, number=1, message=document.Value,)

    before = proto.Field(proto.BOOL, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
