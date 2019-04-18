# Copyright 2017 Google LLC All rights reserved.
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

"""Classes for representing queries for the Google Cloud Firestore API.

A :class:`~.firestore_v1.query.Query` can be created directly from
a :class:`~.firestore_v1.collection.Collection` and that can be
a more common way to create a query than direct usage of the constructor.
"""
import copy
import math
import warnings

from google.protobuf import wrappers_pb2
import six

from google.cloud.firestore_v1 import _helpers
from google.cloud.firestore_v1 import document
from google.cloud.firestore_v1 import field_path as field_path_module
from google.cloud.firestore_v1 import transforms
from google.cloud.firestore_v1.gapic import enums
from google.cloud.firestore_v1.proto import query_pb2
from google.cloud.firestore_v1.order import Order
from google.cloud.firestore_v1.watch import Watch

_EQ_OP = "=="
_operator_enum = enums.StructuredQuery.FieldFilter.Operator
_COMPARISON_OPERATORS = {
    "<": _operator_enum.LESS_THAN,
    "<=": _operator_enum.LESS_THAN_OR_EQUAL,
    _EQ_OP: _operator_enum.EQUAL,
    ">=": _operator_enum.GREATER_THAN_OR_EQUAL,
    ">": _operator_enum.GREATER_THAN,
    "array_contains": _operator_enum.ARRAY_CONTAINS,
}
_BAD_OP_STRING = "Operator string {!r} is invalid. Valid choices are: {}."
_BAD_OP_NAN_NULL = 'Only an equality filter ("==") can be used with None or NaN values'
_INVALID_WHERE_TRANSFORM = "Transforms cannot be used as where values."
_BAD_DIR_STRING = "Invalid direction {!r}. Must be one of {!r} or {!r}."
_INVALID_CURSOR_TRANSFORM = "Transforms cannot be used as cursor values."
_MISSING_ORDER_BY = (
    'The "order by" field path {!r} is not present in the cursor data {!r}. '
    "All fields sent to ``order_by()`` must be present in the fields "
    "if passed to one of ``start_at()`` / ``start_after()`` / "
    "``end_before()`` / ``end_at()`` to define a cursor."
)
_NO_ORDERS_FOR_CURSOR = (
    "Attempting to create a cursor with no fields to order on. "
    "When defining a cursor with one of ``start_at()`` / ``start_after()`` / "
    "``end_before()`` / ``end_at()``, all fields in the cursor must "
    "come from fields set in ``order_by()``."
)
_MISMATCH_CURSOR_W_ORDER_BY = "The cursor {!r} does not match the order fields {!r}."


class Query(object):
    """Represents a query to the Firestore API.

    Instances of this class are considered immutable: all methods that
    would modify an instance instead return a new instance.

    Args:
        parent (~.firestore_v1.collection.Collection): The collection
            that this query applies to.
        projection (Optional[google.cloud.proto.firestore.v1.\
            query_pb2.StructuredQuery.Projection]): A projection of document
            fields to limit the query results to.
        field_filters (Optional[Tuple[google.cloud.proto.firestore.v1.\
            query_pb2.StructuredQuery.FieldFilter, ...]]): The filters to be
            applied in the query.
        orders (Optional[Tuple[google.cloud.proto.firestore.v1.\
            query_pb2.StructuredQuery.Order, ...]]): The "order by" entries
            to use in the query.
        limit (Optional[int]): The maximum number of documents the
            query is allowed to return.
        offset (Optional[int]): The number of results to skip.
        start_at (Optional[Tuple[dict, bool]]): Two-tuple of

            * a mapping of fields. Any field that is present in this mapping
              must also be present in ``orders``
            * an ``after`` flag

            The fields and the flag combine to form a cursor used as
            a starting point in a query result set. If the ``after``
            flag is :data:`True`, the results will start just after any
            documents which have fields matching the cursor, otherwise
            any matching documents will be included in the result set.
            When the query is formed, the document values
            will be used in the order given by ``orders``.
        end_at (Optional[Tuple[dict, bool]]): Two-tuple of

            * a mapping of fields. Any field that is present in this mapping
              must also be present in ``orders``
            * a ``before`` flag

            The fields and the flag combine to form a cursor used as
            an ending point in a query result set. If the ``before``
            flag is :data:`True`, the results will end just before any
            documents which have fields matching the cursor, otherwise
            any matching documents will be included in the result set.
            When the query is formed, the document values
            will be used in the order given by ``orders``.
    """

    ASCENDING = "ASCENDING"
    """str: Sort query results in ascending order on a field."""
    DESCENDING = "DESCENDING"
    """str: Sort query results in descending order on a field."""

    def __init__(
        self,
        parent,
        projection=None,
        field_filters=(),
        orders=(),
        limit=None,
        offset=None,
        start_at=None,
        end_at=None,
        all_descendants=None,
    ):
        self._parent = parent
        self._projection = projection
        self._field_filters = field_filters
        self._orders = orders
        self._limit = limit
        self._offset = offset
        self._start_at = start_at
        self._end_at = end_at
        self._all_descendants=all_descendants

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._parent == other._parent
            and self._projection == other._projection
            and self._field_filters == other._field_filters
            and self._orders == other._orders
            and self._limit == other._limit
            and self._offset == other._offset
            and self._start_at == other._start_at
            and self._end_at == other._end_at
        )

    @property
    def _client(self):
        """The client of the parent collection.

        Returns:
            ~.firestore_v1.client.Client: The client that owns
            this query.
        """
        return self._parent._client

    def select(self, field_paths):
        """Project documents matching query to a limited set of fields.

        See :meth:`~.firestore_v1.client.Client.field_path` for
        more information on **field paths**.

        If the current query already has a projection set (i.e. has already
        called :meth:`~.firestore_v1.query.Query.select`), this
        will overwrite it.

        Args:
            field_paths (Iterable[str, ...]): An iterable of field paths
                (``.``-delimited list of field names) to use as a projection
                of document fields in the query results.

        Returns:
            ~.firestore_v1.query.Query: A "projected" query. Acts as
            a copy of the current query, modified with the newly added
            projection.
        Raises:
            ValueError: If any ``field_path`` is invalid.
        """
        field_paths = list(field_paths)
        for field_path in field_paths:
            field_path_module.split_field_path(field_path)  # raises

        new_projection = query_pb2.StructuredQuery.Projection(
            fields=[
                query_pb2.StructuredQuery.FieldReference(field_path=field_path)
                for field_path in field_paths
            ]
        )
        return self.__class__(
            self._parent,
            projection=new_projection,
            field_filters=self._field_filters,
            orders=self._orders,
            limit=self._limit,
            offset=self._offset,
            start_at=self._start_at,
            end_at=self._end_at,
        )

    def where(self, field_path, op_string, value):
        """Filter the query on a field.

        See :meth:`~.firestore_v1.client.Client.field_path` for
        more information on **field paths**.

        Returns a new :class:`~.firestore_v1.query.Query` that
        filters on a specific field path, according to an operation (e.g.
        ``==`` or "equals") and a particular value to be paired with that
        operation.

        Args:
            field_path (str): A field path (``.``-delimited list of
                field names) for the field to filter on.
            op_string (str): A comparison operation in the form of a string.
                Acceptable values are ``<``, ``<=``, ``==``, ``>=``
                and ``>``.
            value (Any): The value to compare the field against in the filter.
                If ``value`` is :data:`None` or a NaN, then ``==`` is the only
                allowed operation.

        Returns:
            ~.firestore_v1.query.Query: A filtered query. Acts as a
            copy of the current query, modified with the newly added filter.

        Raises:
            ValueError: If ``field_path`` is invalid.
            ValueError: If ``value`` is a NaN or :data:`None` and
                ``op_string`` is not ``==``.
        """
        field_path_module.split_field_path(field_path)  # raises

        if value is None:
            if op_string != _EQ_OP:
                raise ValueError(_BAD_OP_NAN_NULL)
            filter_pb = query_pb2.StructuredQuery.UnaryFilter(
                field=query_pb2.StructuredQuery.FieldReference(field_path=field_path),
                op=enums.StructuredQuery.UnaryFilter.Operator.IS_NULL,
            )
        elif _isnan(value):
            if op_string != _EQ_OP:
                raise ValueError(_BAD_OP_NAN_NULL)
            filter_pb = query_pb2.StructuredQuery.UnaryFilter(
                field=query_pb2.StructuredQuery.FieldReference(field_path=field_path),
                op=enums.StructuredQuery.UnaryFilter.Operator.IS_NAN,
            )
        elif isinstance(value, (transforms.Sentinel, transforms._ValueList)):
            raise ValueError(_INVALID_WHERE_TRANSFORM)
        else:
            filter_pb = query_pb2.StructuredQuery.FieldFilter(
                field=query_pb2.StructuredQuery.FieldReference(field_path=field_path),
                op=_enum_from_op_string(op_string),
                value=_helpers.encode_value(value),
            )

        new_filters = self._field_filters + (filter_pb,)
        return self.__class__(
            self._parent,
            projection=self._projection,
            field_filters=new_filters,
            orders=self._orders,
            limit=self._limit,
            offset=self._offset,
            start_at=self._start_at,
            end_at=self._end_at,
        )

    @staticmethod
    def _make_order(field_path, direction):
        """Helper for :meth:`order_by`."""
        return query_pb2.StructuredQuery.Order(
            field=query_pb2.StructuredQuery.FieldReference(field_path=field_path),
            direction=_enum_from_direction(direction),
        )

    def order_by(self, field_path, direction=ASCENDING):
        """Modify the query to add an order clause on a specific field.

        See :meth:`~.firestore_v1.client.Client.field_path` for
        more information on **field paths**.

        Successive :meth:`~.firestore_v1.query.Query.order_by` calls
        will further refine the ordering of results returned by the query
        (i.e. the new "order by" fields will be added to existing ones).

        Args:
            field_path (str): A field path (``.``-delimited list of
                field names) on which to order the query results.
            direction (Optional[str]): The direction to order by. Must be one
                of :attr:`ASCENDING` or :attr:`DESCENDING`, defaults to
                :attr:`ASCENDING`.

        Returns:
            ~.firestore_v1.query.Query: An ordered query. Acts as a
            copy of the current query, modified with the newly added
            "order by" constraint.

        Raises:
            ValueError: If ``field_path`` is invalid.
            ValueError: If ``direction`` is not one of :attr:`ASCENDING` or
                :attr:`DESCENDING`.
        """
        field_path_module.split_field_path(field_path)  # raises

        order_pb = self._make_order(field_path, direction)

        new_orders = self._orders + (order_pb,)
        return self.__class__(
            self._parent,
            projection=self._projection,
            field_filters=self._field_filters,
            orders=new_orders,
            limit=self._limit,
            offset=self._offset,
            start_at=self._start_at,
            end_at=self._end_at,
        )

    def limit(self, count):
        """Limit a query to return a fixed number of results.

        If the current query already has a limit set, this will overwrite it.

        Args:
            count (int): Maximum number of documents to return that match
                the query.

        Returns:
            ~.firestore_v1.query.Query: A limited query. Acts as a
            copy of the current query, modified with the newly added
            "limit" filter.
        """
        return self.__class__(
            self._parent,
            projection=self._projection,
            field_filters=self._field_filters,
            orders=self._orders,
            limit=count,
            offset=self._offset,
            start_at=self._start_at,
            end_at=self._end_at,
        )

    def offset(self, num_to_skip):
        """Skip to an offset in a query.

        If the current query already has specified an offset, this will
        overwrite it.

        Args:
            num_to_skip (int): The number of results to skip at the beginning
                of query results. (Must be non-negative.)

        Returns:
            ~.firestore_v1.query.Query: An offset query. Acts as a
            copy of the current query, modified with the newly added
            "offset" field.
        """
        return self.__class__(
            self._parent,
            projection=self._projection,
            field_filters=self._field_filters,
            orders=self._orders,
            limit=self._limit,
            offset=num_to_skip,
            start_at=self._start_at,
            end_at=self._end_at,
        )

    def _cursor_helper(self, document_fields, before, start):
        """Set values to be used for a ``start_at`` or ``end_at`` cursor.

        The values will later be used in a query protobuf.

        When the query is sent to the server, the ``document_fields`` will
        be used in the order given by fields set by
        :meth:`~.firestore_v1.query.Query.order_by`.

        Args:
            document_fields (Union[~.firestore_v1.\
                document.DocumentSnapshot, dict, list, tuple]): a document
                snapshot or a dictionary/list/tuple of fields representing a
                query results cursor. A cursor is a collection of values that
                represent a position in a query result set.
            before (bool): Flag indicating if the document in
                ``document_fields`` should (:data:`False`) or
                shouldn't (:data:`True`) be included in the result set.
            start (Optional[bool]): determines if the cursor is a ``start_at``
                cursor (:data:`True`) or an ``end_at`` cursor (:data:`False`).

        Returns:
            ~.firestore_v1.query.Query: A query with cursor. Acts as
            a copy of the current query, modified with the newly added
            "start at" cursor.
        """
        if isinstance(document_fields, tuple):
            document_fields = list(document_fields)
        elif isinstance(document_fields, document.DocumentSnapshot):
            if document_fields.reference._path[:-1] != self._parent._path:
                raise ValueError(
                    "Cannot use snapshot from another collection as a cursor."
                )
        else:
            # NOTE: We copy so that the caller can't modify after calling.
            document_fields = copy.deepcopy(document_fields)

        cursor_pair = document_fields, before
        query_kwargs = {
            "projection": self._projection,
            "field_filters": self._field_filters,
            "orders": self._orders,
            "limit": self._limit,
            "offset": self._offset,
        }
        if start:
            query_kwargs["start_at"] = cursor_pair
            query_kwargs["end_at"] = self._end_at
        else:
            query_kwargs["start_at"] = self._start_at
            query_kwargs["end_at"] = cursor_pair

        return self.__class__(self._parent, **query_kwargs)

    def start_at(self, document_fields):
        """Start query results at a particular document value.

        The result set will **include** the document specified by
        ``document_fields``.

        If the current query already has specified a start cursor -- either
        via this method or
        :meth:`~.firestore_v1.query.Query.start_after` -- this will
        overwrite it.

        When the query is sent to the server, the ``document_fields`` will
        be used in the order given by fields set by
        :meth:`~.firestore_v1.query.Query.order_by`.

        Args:
            document_fields (Union[~.firestore_v1.\
                document.DocumentSnapshot, dict, list, tuple]): a document
                snapshot or a dictionary/list/tuple of fields representing a
                query results cursor. A cursor is a collection of values that
                represent a position in a query result set.

        Returns:
            ~.firestore_v1.query.Query: A query with cursor. Acts as
            a copy of the current query, modified with the newly added
            "start at" cursor.
        """
        return self._cursor_helper(document_fields, before=True, start=True)

    def start_after(self, document_fields):
        """Start query results after a particular document value.

        The result set will **exclude** the document specified by
        ``document_fields``.

        If the current query already has specified a start cursor -- either
        via this method or
        :meth:`~.firestore_v1.query.Query.start_at` -- this will
        overwrite it.

        When the query is sent to the server, the ``document_fields`` will
        be used in the order given by fields set by
        :meth:`~.firestore_v1.query.Query.order_by`.

        Args:
            document_fields (Union[~.firestore_v1.\
                document.DocumentSnapshot, dict, list, tuple]): a document
                snapshot or a dictionary/list/tuple of fields representing a
                query results cursor. A cursor is a collection of values that
                represent a position in a query result set.

        Returns:
            ~.firestore_v1.query.Query: A query with cursor. Acts as
            a copy of the current query, modified with the newly added
            "start after" cursor.
        """
        return self._cursor_helper(document_fields, before=False, start=True)

    def end_before(self, document_fields):
        """End query results before a particular document value.

        The result set will **exclude** the document specified by
        ``document_fields``.

        If the current query already has specified an end cursor -- either
        via this method or
        :meth:`~.firestore_v1.query.Query.end_at` -- this will
        overwrite it.

        When the query is sent to the server, the ``document_fields`` will
        be used in the order given by fields set by
        :meth:`~.firestore_v1.query.Query.order_by`.

        Args:
            document_fields (Union[~.firestore_v1.\
                document.DocumentSnapshot, dict, list, tuple]): a document
                snapshot or a dictionary/list/tuple of fields representing a
                query results cursor. A cursor is a collection of values that
                represent a position in a query result set.

        Returns:
            ~.firestore_v1.query.Query: A query with cursor. Acts as
            a copy of the current query, modified with the newly added
            "end before" cursor.
        """
        return self._cursor_helper(document_fields, before=True, start=False)

    def end_at(self, document_fields):
        """End query results at a particular document value.

        The result set will **include** the document specified by
        ``document_fields``.

        If the current query already has specified an end cursor -- either
        via this method or
        :meth:`~.firestore_v1.query.Query.end_before` -- this will
        overwrite it.

        When the query is sent to the server, the ``document_fields`` will
        be used in the order given by fields set by
        :meth:`~.firestore_v1.query.Query.order_by`.

        Args:
            document_fields (Union[~.firestore_v1.\
                document.DocumentSnapshot, dict, list, tuple]): a document
                snapshot or a dictionary/list/tuple of fields representing a
                query results cursor. A cursor is a collection of values that
                represent a position in a query result set.

        Returns:
            ~.firestore_v1.query.Query: A query with cursor. Acts as
            a copy of the current query, modified with the newly added
            "end at" cursor.
        """
        return self._cursor_helper(document_fields, before=False, start=False)

    def _filters_pb(self):
        """Convert all the filters into a single generic Filter protobuf.

        This may be a lone field filter or unary filter, may be a composite
        filter or may be :data:`None`.

        Returns:
            google.cloud.firestore_v1.types.\
            StructuredQuery.Filter: A "generic" filter representing the
            current query's filters.
        """
        num_filters = len(self._field_filters)
        if num_filters == 0:
            return None
        elif num_filters == 1:
            return _filter_pb(self._field_filters[0])
        else:
            composite_filter = query_pb2.StructuredQuery.CompositeFilter(
                op=enums.StructuredQuery.CompositeFilter.Operator.AND,
                filters=[_filter_pb(filter_) for filter_ in self._field_filters],
            )
            return query_pb2.StructuredQuery.Filter(composite_filter=composite_filter)

    @staticmethod
    def _normalize_projection(projection):
        """Helper:  convert field paths to message."""
        if projection is not None:

            fields = list(projection.fields)

            if not fields:
                field_ref = query_pb2.StructuredQuery.FieldReference(
                    field_path="__name__"
                )
                return query_pb2.StructuredQuery.Projection(fields=[field_ref])

        return projection

    def _normalize_orders(self):
        """Helper:  adjust orders based on cursors, where clauses."""
        orders = list(self._orders)
        _has_snapshot_cursor = False

        if self._start_at:
            if isinstance(self._start_at[0], document.DocumentSnapshot):
                _has_snapshot_cursor = True

        if self._end_at:
            if isinstance(self._end_at[0], document.DocumentSnapshot):
                _has_snapshot_cursor = True

        if _has_snapshot_cursor:
            should_order = [
                _enum_from_op_string(key)
                for key in _COMPARISON_OPERATORS
                if key not in (_EQ_OP, "array_contains")
            ]
            order_keys = [order.field.field_path for order in orders]
            for filter_ in self._field_filters:
                field = filter_.field.field_path
                if filter_.op in should_order and field not in order_keys:
                    orders.append(self._make_order(field, "ASCENDING"))
            if not orders:
                orders.append(self._make_order("__name__", "ASCENDING"))
            else:
                order_keys = [order.field.field_path for order in orders]
                if "__name__" not in order_keys:
                    direction = orders[-1].direction  # enum?
                    orders.append(self._make_order("__name__", direction))

        return orders

    def _normalize_cursor(self, cursor, orders):
        """Helper: convert cursor to a list of values based on orders."""
        if cursor is None:
            return

        if not orders:
            raise ValueError(_NO_ORDERS_FOR_CURSOR)

        document_fields, before = cursor

        order_keys = [order.field.field_path for order in orders]

        if isinstance(document_fields, document.DocumentSnapshot):
            snapshot = document_fields
            document_fields = snapshot.to_dict()
            document_fields["__name__"] = snapshot.reference

        if isinstance(document_fields, dict):
            # Transform to list using orders
            values = []
            data = document_fields
            for order_key in order_keys:
                try:
                    values.append(field_path_module.get_nested_value(order_key, data))
                except KeyError:
                    msg = _MISSING_ORDER_BY.format(order_key, data)
                    raise ValueError(msg)
            document_fields = values

        if len(document_fields) != len(orders):
            msg = _MISMATCH_CURSOR_W_ORDER_BY.format(document_fields, order_keys)
            raise ValueError(msg)

        _transform_bases = (transforms.Sentinel, transforms._ValueList)

        for index, key_field in enumerate(zip(order_keys, document_fields)):
            key, field = key_field

            if isinstance(field, _transform_bases):
                msg = _INVALID_CURSOR_TRANSFORM
                raise ValueError(msg)

            if key == "__name__" and isinstance(field, six.string_types):
                document_fields[index] = self._parent.document(field)

        return document_fields, before

    def _to_protobuf(self):
        """Convert the current query into the equivalent protobuf.

        Returns:
            google.cloud.firestore_v1.types.StructuredQuery: The
            query protobuf.
        """
        projection = self._normalize_projection(self._projection)
        orders = self._normalize_orders()
        start_at = self._normalize_cursor(self._start_at, orders)
        end_at = self._normalize_cursor(self._end_at, orders)

        query_kwargs = {
            "select": projection,
            "from": [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=self._parent.id,
                    all_descendants=self._all_descendants,
                )
            ],
            "where": self._filters_pb(),
            "order_by": orders,
            "start_at": _cursor_pb(start_at),
            "end_at": _cursor_pb(end_at),
        }
        if self._offset is not None:
            query_kwargs["offset"] = self._offset
        if self._limit is not None:
            query_kwargs["limit"] = wrappers_pb2.Int32Value(value=self._limit)

        return query_pb2.StructuredQuery(**query_kwargs)

    def get(self, transaction=None):
        """Deprecated alias for :meth:`stream`."""
        warnings.warn(
            "'Query.get' is deprecated:  please use 'Query.stream' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.stream(transaction=transaction)

    def stream(self, transaction=None):
        """Read the documents in the collection that match this query.

        This sends a ``RunQuery`` RPC and then returns an iterator which
        consumes each document returned in the stream of ``RunQueryResponse``
        messages.

        .. note::

           The underlying stream of responses will time out after
           the ``max_rpc_timeout_millis`` value set in the GAPIC
           client configuration for the ``RunQuery`` API.  Snapshots
           not consumed from the iterator before that point will be lost.

        If a ``transaction`` is used and it already has write operations
        added, this method cannot be used (i.e. read-after-write is not
        allowed).

        Args:
            transaction (Optional[~.firestore_v1.transaction.\
                Transaction]): An existing transaction that this query will
                run in.

        Yields:
            ~.firestore_v1.document.DocumentSnapshot: The next
            document that fulfills the query.
        """
        parent_path, expected_prefix = self._parent._parent_info()
        response_iterator = self._client._firestore_api.run_query(
            parent_path,
            self._to_protobuf(),
            transaction=_helpers.get_transaction_id(transaction),
            metadata=self._client._rpc_metadata,
        )

        for response in response_iterator:
            if self._all_descendants:
                snapshot = _collection_group_query_response_to_snapshot(
                    response, self._parent
                )
            else:
                snapshot = _query_response_to_snapshot(
                    response, self._parent, expected_prefix
                )
            if snapshot is not None:
                yield snapshot

    def on_snapshot(self, callback):
        """Monitor the documents in this collection that match this query.

        This starts a watch on this query using a background thread. The
        provided callback is run on the snapshot of the documents.

        Args:
            callback(~.firestore.query.QuerySnapshot): a callback to run when
                a change occurs.

        Example:
            from google.cloud import firestore_v1

            db = firestore_v1.Client()
            query_ref = db.collection(u'users').where("user", "==", u'Ada')

            def on_snapshot(docs, changes, read_time):
                for doc in docs:
                    print(u'{} => {}'.format(doc.id, doc.to_dict()))

            # Watch this query
            query_watch = query_ref.on_snapshot(on_snapshot)

            # Terminate this watch
            query_watch.unsubscribe()
        """
        return Watch.for_query(
            self, callback, document.DocumentSnapshot, document.DocumentReference
        )

    def _comparator(self, doc1, doc2):
        _orders = self._orders

        # Add implicit sorting by name, using the last specified direction.
        if len(_orders) == 0:
            lastDirection = Query.ASCENDING
        else:
            if _orders[-1].direction == 1:
                lastDirection = Query.ASCENDING
            else:
                lastDirection = Query.DESCENDING

        orderBys = list(_orders)

        order_pb = query_pb2.StructuredQuery.Order(
            field=query_pb2.StructuredQuery.FieldReference(field_path="id"),
            direction=_enum_from_direction(lastDirection),
        )
        orderBys.append(order_pb)

        for orderBy in orderBys:
            if orderBy.field.field_path == "id":
                # If ordering by docuent id, compare resource paths.
                comp = Order()._compare_to(doc1.reference._path, doc2.reference._path)
            else:
                if (
                    orderBy.field.field_path not in doc1._data
                    or orderBy.field.field_path not in doc2._data
                ):
                    raise ValueError(
                        "Can only compare fields that exist in the "
                        "DocumentSnapshot. Please include the fields you are "
                        "ordering on in your select() call."
                    )
                v1 = doc1._data[orderBy.field.field_path]
                v2 = doc2._data[orderBy.field.field_path]
                encoded_v1 = _helpers.encode_value(v1)
                encoded_v2 = _helpers.encode_value(v2)
                comp = Order().compare(encoded_v1, encoded_v2)

            if comp != 0:
                # 1 == Ascending, -1 == Descending
                return orderBy.direction * comp

        return 0


def _enum_from_op_string(op_string):
    """Convert a string representation of a binary operator to an enum.

    These enums come from the protobuf message definition
    ``StructuredQuery.FieldFilter.Operator``.

    Args:
        op_string (str): A comparison operation in the form of a string.
            Acceptable values are ``<``, ``<=``, ``==``, ``>=``
            and ``>``.

    Returns:
        int: The enum corresponding to ``op_string``.

    Raises:
        ValueError: If ``op_string`` is not a valid operator.
    """
    try:
        return _COMPARISON_OPERATORS[op_string]
    except KeyError:
        choices = ", ".join(sorted(_COMPARISON_OPERATORS.keys()))
        msg = _BAD_OP_STRING.format(op_string, choices)
        raise ValueError(msg)


def _isnan(value):
    """Check if a value is NaN.

    This differs from ``math.isnan`` in that **any** input type is
    allowed.

    Args:
        value (Any): A value to check for NaN-ness.

    Returns:
        bool: Indicates if the value is the NaN float.
    """
    if isinstance(value, float):
        return math.isnan(value)
    else:
        return False


def _enum_from_direction(direction):
    """Convert a string representation of a direction to an enum.

    Args:
        direction (str): A direction to order by. Must be one of
            :attr:`~.firestore.Query.ASCENDING` or
            :attr:`~.firestore.Query.DESCENDING`.

    Returns:
        int: The enum corresponding to ``direction``.

    Raises:
        ValueError: If ``direction`` is not a valid direction.
    """
    if isinstance(direction, int):
        return direction

    if direction == Query.ASCENDING:
        return enums.StructuredQuery.Direction.ASCENDING
    elif direction == Query.DESCENDING:
        return enums.StructuredQuery.Direction.DESCENDING
    else:
        msg = _BAD_DIR_STRING.format(direction, Query.ASCENDING, Query.DESCENDING)
        raise ValueError(msg)


def _filter_pb(field_or_unary):
    """Convert a specific protobuf filter to the generic filter type.

    Args:
        field_or_unary (Union[google.cloud.proto.firestore.v1.\
            query_pb2.StructuredQuery.FieldFilter, google.cloud.proto.\
            firestore.v1.query_pb2.StructuredQuery.FieldFilter]): A
            field or unary filter to convert to a generic filter.

    Returns:
        google.cloud.firestore_v1.types.\
        StructuredQuery.Filter: A "generic" filter.

    Raises:
        ValueError: If ``field_or_unary`` is not a field or unary filter.
    """
    if isinstance(field_or_unary, query_pb2.StructuredQuery.FieldFilter):
        return query_pb2.StructuredQuery.Filter(field_filter=field_or_unary)
    elif isinstance(field_or_unary, query_pb2.StructuredQuery.UnaryFilter):
        return query_pb2.StructuredQuery.Filter(unary_filter=field_or_unary)
    else:
        raise ValueError("Unexpected filter type", type(field_or_unary), field_or_unary)


def _cursor_pb(cursor_pair):
    """Convert a cursor pair to a protobuf.

    If ``cursor_pair`` is :data:`None`, just returns :data:`None`.

    Args:
        cursor_pair (Optional[Tuple[list, bool]]): Two-tuple of

            * a list of field values.
            * a ``before`` flag

    Returns:
        Optional[google.cloud.firestore_v1.types.Cursor]: A
        protobuf cursor corresponding to the values.
    """
    if cursor_pair is not None:
        data, before = cursor_pair
        value_pbs = [_helpers.encode_value(value) for value in data]
        return query_pb2.Cursor(values=value_pbs, before=before)


def _query_response_to_snapshot(response_pb, collection, expected_prefix):
    """Parse a query response protobuf to a document snapshot.

    Args:
        response_pb (google.cloud.proto.firestore.v1.\
            firestore_pb2.RunQueryResponse): A
        collection (~.firestore_v1.collection.CollectionReference): A
            reference to the collection that initiated the query.
        expected_prefix (str): The expected prefix for fully-qualified
            document names returned in the query results. This can be computed
            directly from ``collection`` via :meth:`_parent_info`.

    Returns:
        Optional[~.firestore.document.DocumentSnapshot]: A
        snapshot of the data returned in the query. If ``response_pb.document``
        is not set, the snapshot will be :data:`None`.
    """
    if not response_pb.HasField("document"):
        return None

    document_id = _helpers.get_doc_id(response_pb.document, expected_prefix)
    reference = collection.document(document_id)
    data = _helpers.decode_dict(response_pb.document.fields, collection._client)
    snapshot = document.DocumentSnapshot(
        reference,
        data,
        exists=True,
        read_time=response_pb.read_time,
        create_time=response_pb.document.create_time,
        update_time=response_pb.document.update_time,
    )
    return snapshot


def _collection_group_query_response_to_snapshot(response_pb, collection):
    """Parse a query response protobuf to a document snapshot.

    Args:
        response_pb (google.cloud.proto.firestore.v1.\
            firestore_pb2.RunQueryResponse): A
        collection (~.firestore_v1.collection.CollectionReference): A
            reference to the collection that initiated the query.

    Returns:
        Optional[~.firestore.document.DocumentSnapshot]: A
        snapshot of the data returned in the query. If ``response_pb.document``
        is not set, the snapshot will be :data:`None`.
    """
    if not response_pb.HasField("document"):
        return None
    reference = collection._client.document(response_pb.document.name)
    data = _helpers.decode_dict(response_pb.document.fields, collection._client)
    snapshot = document.DocumentSnapshot(
        reference,
        data,
        exists=True,
        read_time=response_pb.read_time,
        create_time=response_pb.document.create_time,
        update_time=response_pb.document.update_time,
    )
    return snapshot
