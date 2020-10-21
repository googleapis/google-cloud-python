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

import datetime
import unittest

import mock


class TestBaseQuery(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.query import Query

        return Query

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor_defaults(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertIs(query._parent, mock.sentinel.parent)
        self.assertIsNone(query._projection)
        self.assertEqual(query._field_filters, ())
        self.assertEqual(query._orders, ())
        self.assertIsNone(query._limit)
        self.assertIsNone(query._offset)
        self.assertIsNone(query._start_at)
        self.assertIsNone(query._end_at)
        self.assertFalse(query._all_descendants)

    def _make_one_all_fields(
        self, limit=9876, offset=12, skip_fields=(), parent=None, all_descendants=True
    ):
        kwargs = {
            "projection": mock.sentinel.projection,
            "field_filters": mock.sentinel.filters,
            "orders": mock.sentinel.orders,
            "limit": limit,
            "offset": offset,
            "start_at": mock.sentinel.start_at,
            "end_at": mock.sentinel.end_at,
            "all_descendants": all_descendants,
        }
        for field in skip_fields:
            kwargs.pop(field)
        if parent is None:
            parent = mock.sentinel.parent
        return self._make_one(parent, **kwargs)

    def test_constructor_explicit(self):
        limit = 234
        offset = 56
        query = self._make_one_all_fields(limit=limit, offset=offset)
        self.assertIs(query._parent, mock.sentinel.parent)
        self.assertIs(query._projection, mock.sentinel.projection)
        self.assertIs(query._field_filters, mock.sentinel.filters)
        self.assertEqual(query._orders, mock.sentinel.orders)
        self.assertEqual(query._limit, limit)
        self.assertEqual(query._offset, offset)
        self.assertIs(query._start_at, mock.sentinel.start_at)
        self.assertIs(query._end_at, mock.sentinel.end_at)
        self.assertTrue(query._all_descendants)

    def test__client_property(self):
        parent = mock.Mock(_client=mock.sentinel.client, spec=["_client"])
        query = self._make_one(parent)
        self.assertIs(query._client, mock.sentinel.client)

    def test___eq___other_type(self):
        query = self._make_one_all_fields()
        other = object()
        self.assertFalse(query == other)

    def test___eq___different_parent(self):
        parent = mock.sentinel.parent
        other_parent = mock.sentinel.other_parent
        query = self._make_one_all_fields(parent=parent)
        other = self._make_one_all_fields(parent=other_parent)
        self.assertFalse(query == other)

    def test___eq___different_projection(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, skip_fields=("projection",))
        query._projection = mock.sentinel.projection
        other = self._make_one_all_fields(parent=parent, skip_fields=("projection",))
        other._projection = mock.sentinel.other_projection
        self.assertFalse(query == other)

    def test___eq___different_field_filters(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, skip_fields=("field_filters",))
        query._field_filters = mock.sentinel.field_filters
        other = self._make_one_all_fields(parent=parent, skip_fields=("field_filters",))
        other._field_filters = mock.sentinel.other_field_filters
        self.assertFalse(query == other)

    def test___eq___different_orders(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, skip_fields=("orders",))
        query._orders = mock.sentinel.orders
        other = self._make_one_all_fields(parent=parent, skip_fields=("orders",))
        other._orders = mock.sentinel.other_orders
        self.assertFalse(query == other)

    def test___eq___different_limit(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, limit=10)
        other = self._make_one_all_fields(parent=parent, limit=20)
        self.assertFalse(query == other)

    def test___eq___different_offset(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, offset=10)
        other = self._make_one_all_fields(parent=parent, offset=20)
        self.assertFalse(query == other)

    def test___eq___different_start_at(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, skip_fields=("start_at",))
        query._start_at = mock.sentinel.start_at
        other = self._make_one_all_fields(parent=parent, skip_fields=("start_at",))
        other._start_at = mock.sentinel.other_start_at
        self.assertFalse(query == other)

    def test___eq___different_end_at(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, skip_fields=("end_at",))
        query._end_at = mock.sentinel.end_at
        other = self._make_one_all_fields(parent=parent, skip_fields=("end_at",))
        other._end_at = mock.sentinel.other_end_at
        self.assertFalse(query == other)

    def test___eq___different_all_descendants(self):
        parent = mock.sentinel.parent
        query = self._make_one_all_fields(parent=parent, all_descendants=True)
        other = self._make_one_all_fields(parent=parent, all_descendants=False)
        self.assertFalse(query == other)

    def test___eq___hit(self):
        query = self._make_one_all_fields()
        other = self._make_one_all_fields()
        self.assertTrue(query == other)

    def _compare_queries(self, query1, query2, attr_name):
        attrs1 = query1.__dict__.copy()
        attrs2 = query2.__dict__.copy()

        attrs1.pop(attr_name)
        attrs2.pop(attr_name)

        # The only different should be in ``attr_name``.
        self.assertEqual(len(attrs1), len(attrs2))
        for key, value in attrs1.items():
            self.assertIs(value, attrs2[key])

    @staticmethod
    def _make_projection_for_select(field_paths):
        from google.cloud.firestore_v1.types import query

        return query.StructuredQuery.Projection(
            fields=[
                query.StructuredQuery.FieldReference(field_path=field_path)
                for field_path in field_paths
            ]
        )

    def test_select_invalid_path(self):
        query = self._make_one(mock.sentinel.parent)

        with self.assertRaises(ValueError):
            query.select(["*"])

    def test_select(self):
        query1 = self._make_one_all_fields(all_descendants=True)

        field_paths2 = ["foo", "bar"]
        query2 = query1.select(field_paths2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(
            query2._projection, self._make_projection_for_select(field_paths2)
        )
        self._compare_queries(query1, query2, "_projection")

        # Make sure it overrides.
        field_paths3 = ["foo.baz"]
        query3 = query2.select(field_paths3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(
            query3._projection, self._make_projection_for_select(field_paths3)
        )
        self._compare_queries(query2, query3, "_projection")

    def test_where_invalid_path(self):
        query = self._make_one(mock.sentinel.parent)

        with self.assertRaises(ValueError):
            query.where("*", "==", 1)

    def test_where(self):
        from google.cloud.firestore_v1.types import StructuredQuery
        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        query_inst = self._make_one_all_fields(
            skip_fields=("field_filters",), all_descendants=True
        )
        new_query = query_inst.where("power.level", ">", 9000)

        self.assertIsNot(query_inst, new_query)
        self.assertIsInstance(new_query, self._get_target_class())
        self.assertEqual(len(new_query._field_filters), 1)

        field_pb = new_query._field_filters[0]
        expected_pb = query.StructuredQuery.FieldFilter(
            field=query.StructuredQuery.FieldReference(field_path="power.level"),
            op=StructuredQuery.FieldFilter.Operator.GREATER_THAN,
            value=document.Value(integer_value=9000),
        )
        self.assertEqual(field_pb, expected_pb)
        self._compare_queries(query_inst, new_query, "_field_filters")

    def _where_unary_helper(self, value, op_enum, op_string="=="):
        from google.cloud.firestore_v1.types import StructuredQuery

        query_inst = self._make_one_all_fields(skip_fields=("field_filters",))
        field_path = "feeeld"
        new_query = query_inst.where(field_path, op_string, value)

        self.assertIsNot(query_inst, new_query)
        self.assertIsInstance(new_query, self._get_target_class())
        self.assertEqual(len(new_query._field_filters), 1)

        field_pb = new_query._field_filters[0]
        expected_pb = StructuredQuery.UnaryFilter(
            field=StructuredQuery.FieldReference(field_path=field_path), op=op_enum
        )
        self.assertEqual(field_pb, expected_pb)
        self._compare_queries(query_inst, new_query, "_field_filters")

    def test_where_eq_null(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        op_enum = StructuredQuery.UnaryFilter.Operator.IS_NULL
        self._where_unary_helper(None, op_enum)

    def test_where_gt_null(self):
        with self.assertRaises(ValueError):
            self._where_unary_helper(None, 0, op_string=">")

    def test_where_eq_nan(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        op_enum = StructuredQuery.UnaryFilter.Operator.IS_NAN
        self._where_unary_helper(float("nan"), op_enum)

    def test_where_le_nan(self):
        with self.assertRaises(ValueError):
            self._where_unary_helper(float("nan"), 0, op_string="<=")

    def test_where_w_delete(self):
        from google.cloud.firestore_v1 import DELETE_FIELD

        with self.assertRaises(ValueError):
            self._where_unary_helper(DELETE_FIELD, 0)

    def test_where_w_server_timestamp(self):
        from google.cloud.firestore_v1 import SERVER_TIMESTAMP

        with self.assertRaises(ValueError):
            self._where_unary_helper(SERVER_TIMESTAMP, 0)

    def test_where_w_array_remove(self):
        from google.cloud.firestore_v1 import ArrayRemove

        with self.assertRaises(ValueError):
            self._where_unary_helper(ArrayRemove([1, 3, 5]), 0)

    def test_where_w_array_union(self):
        from google.cloud.firestore_v1 import ArrayUnion

        with self.assertRaises(ValueError):
            self._where_unary_helper(ArrayUnion([2, 4, 8]), 0)

    def test_order_by_invalid_path(self):
        query = self._make_one(mock.sentinel.parent)

        with self.assertRaises(ValueError):
            query.order_by("*")

    def test_order_by(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        klass = self._get_target_class()
        query1 = self._make_one_all_fields(
            skip_fields=("orders",), all_descendants=True
        )

        field_path2 = "a"
        query2 = query1.order_by(field_path2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, klass)
        order = _make_order_pb(field_path2, StructuredQuery.Direction.ASCENDING)
        self.assertEqual(query2._orders, (order,))
        self._compare_queries(query1, query2, "_orders")

        # Make sure it appends to the orders.
        field_path3 = "b"
        query3 = query2.order_by(field_path3, direction=klass.DESCENDING)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, klass)
        order_pb3 = _make_order_pb(field_path3, StructuredQuery.Direction.DESCENDING)
        self.assertEqual(query3._orders, (order, order_pb3))
        self._compare_queries(query2, query3, "_orders")

    def test_limit(self):
        query1 = self._make_one_all_fields(all_descendants=True)

        limit2 = 100
        query2 = query1.limit(limit2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(query2._limit, limit2)
        self._compare_queries(query1, query2, "_limit")

        # Make sure it overrides.
        limit3 = 10
        query3 = query2.limit(limit3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._limit, limit3)
        self._compare_queries(query2, query3, "_limit")

    def test_offset(self):
        query1 = self._make_one_all_fields(all_descendants=True)

        offset2 = 23
        query2 = query1.offset(offset2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(query2._offset, offset2)
        self._compare_queries(query1, query2, "_offset")

        # Make sure it overrides.
        offset3 = 35
        query3 = query2.offset(offset3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._offset, offset3)
        self._compare_queries(query2, query3, "_offset")

    @staticmethod
    def _make_collection(*path, **kw):
        from google.cloud.firestore_v1 import collection

        return collection.CollectionReference(*path, **kw)

    @staticmethod
    def _make_docref(*path, **kw):
        from google.cloud.firestore_v1 import document

        return document.DocumentReference(*path, **kw)

    @staticmethod
    def _make_snapshot(docref, values):
        from google.cloud.firestore_v1 import document

        return document.DocumentSnapshot(docref, values, True, None, None, None)

    def test__cursor_helper_w_dict(self):
        values = {"a": 7, "b": "foo"}
        query1 = self._make_one(mock.sentinel.parent)
        query1._all_descendants = True
        query2 = query1._cursor_helper(values, True, True)

        self.assertIs(query2._parent, mock.sentinel.parent)
        self.assertIsNone(query2._projection)
        self.assertEqual(query2._field_filters, ())
        self.assertEqual(query2._orders, query1._orders)
        self.assertIsNone(query2._limit)
        self.assertIsNone(query2._offset)
        self.assertIsNone(query2._end_at)
        self.assertTrue(query2._all_descendants)

        cursor, before = query2._start_at

        self.assertEqual(cursor, values)
        self.assertTrue(before)

    def test__cursor_helper_w_tuple(self):
        values = (7, "foo")
        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1._cursor_helper(values, False, True)

        self.assertIs(query2._parent, mock.sentinel.parent)
        self.assertIsNone(query2._projection)
        self.assertEqual(query2._field_filters, ())
        self.assertEqual(query2._orders, query1._orders)
        self.assertIsNone(query2._limit)
        self.assertIsNone(query2._offset)
        self.assertIsNone(query2._end_at)

        cursor, before = query2._start_at

        self.assertEqual(cursor, list(values))
        self.assertFalse(before)

    def test__cursor_helper_w_list(self):
        values = [7, "foo"]
        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1._cursor_helper(values, True, False)

        self.assertIs(query2._parent, mock.sentinel.parent)
        self.assertIsNone(query2._projection)
        self.assertEqual(query2._field_filters, ())
        self.assertEqual(query2._orders, query1._orders)
        self.assertIsNone(query2._limit)
        self.assertIsNone(query2._offset)
        self.assertIsNone(query2._start_at)

        cursor, before = query2._end_at

        self.assertEqual(cursor, values)
        self.assertIsNot(cursor, values)
        self.assertTrue(before)

    def test__cursor_helper_w_snapshot_wrong_collection(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("there", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query = self._make_one(collection)

        with self.assertRaises(ValueError):
            query._cursor_helper(snapshot, False, False)

    def test__cursor_helper_w_snapshot_other_collection_all_descendants(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("there", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query1 = self._make_one(collection, all_descendants=True)

        query2 = query1._cursor_helper(snapshot, False, False)

        self.assertIs(query2._parent, collection)
        self.assertIsNone(query2._projection)
        self.assertEqual(query2._field_filters, ())
        self.assertEqual(query2._orders, ())
        self.assertIsNone(query2._limit)
        self.assertIsNone(query2._offset)
        self.assertIsNone(query2._start_at)

        cursor, before = query2._end_at

        self.assertIs(cursor, snapshot)
        self.assertFalse(before)

    def test__cursor_helper_w_snapshot(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query1 = self._make_one(collection)

        query2 = query1._cursor_helper(snapshot, False, False)

        self.assertIs(query2._parent, collection)
        self.assertIsNone(query2._projection)
        self.assertEqual(query2._field_filters, ())
        self.assertEqual(query2._orders, ())
        self.assertIsNone(query2._limit)
        self.assertIsNone(query2._offset)
        self.assertIsNone(query2._start_at)

        cursor, before = query2._end_at

        self.assertIs(cursor, snapshot)
        self.assertFalse(before)

    def test_start_at(self):
        collection = self._make_collection("here")
        query1 = self._make_one_all_fields(
            parent=collection, skip_fields=("orders",), all_descendants=True
        )
        query2 = query1.order_by("hi")

        document_fields3 = {"hi": "mom"}
        query3 = query2.start_at(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._start_at, (document_fields3, True))
        self._compare_queries(query2, query3, "_start_at")

        # Make sure it overrides.
        query4 = query3.order_by("bye")
        values5 = {"hi": "zap", "bye": 88}
        docref = self._make_docref("here", "doc_id")
        document_fields5 = self._make_snapshot(docref, values5)
        query5 = query4.start_at(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._start_at, (document_fields5, True))
        self._compare_queries(query4, query5, "_start_at")

    def test_start_after(self):
        collection = self._make_collection("here")
        query1 = self._make_one_all_fields(parent=collection, skip_fields=("orders",))
        query2 = query1.order_by("down")

        document_fields3 = {"down": 99.75}
        query3 = query2.start_after(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._start_at, (document_fields3, False))
        self._compare_queries(query2, query3, "_start_at")

        # Make sure it overrides.
        query4 = query3.order_by("out")
        values5 = {"down": 100.25, "out": b"\x00\x01"}
        docref = self._make_docref("here", "doc_id")
        document_fields5 = self._make_snapshot(docref, values5)
        query5 = query4.start_after(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._start_at, (document_fields5, False))
        self._compare_queries(query4, query5, "_start_at")

    def test_end_before(self):
        collection = self._make_collection("here")
        query1 = self._make_one_all_fields(parent=collection, skip_fields=("orders",))
        query2 = query1.order_by("down")

        document_fields3 = {"down": 99.75}
        query3 = query2.end_before(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._end_at, (document_fields3, True))
        self._compare_queries(query2, query3, "_end_at")

        # Make sure it overrides.
        query4 = query3.order_by("out")
        values5 = {"down": 100.25, "out": b"\x00\x01"}
        docref = self._make_docref("here", "doc_id")
        document_fields5 = self._make_snapshot(docref, values5)
        query5 = query4.end_before(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._end_at, (document_fields5, True))
        self._compare_queries(query4, query5, "_end_at")
        self._compare_queries(query4, query5, "_end_at")

    def test_end_at(self):
        collection = self._make_collection("here")
        query1 = self._make_one_all_fields(parent=collection, skip_fields=("orders",))
        query2 = query1.order_by("hi")

        document_fields3 = {"hi": "mom"}
        query3 = query2.end_at(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._end_at, (document_fields3, False))
        self._compare_queries(query2, query3, "_end_at")

        # Make sure it overrides.
        query4 = query3.order_by("bye")
        values5 = {"hi": "zap", "bye": 88}
        docref = self._make_docref("here", "doc_id")
        document_fields5 = self._make_snapshot(docref, values5)
        query5 = query4.end_at(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._end_at, (document_fields5, False))
        self._compare_queries(query4, query5, "_end_at")

    def test__filters_pb_empty(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertEqual(len(query._field_filters), 0)
        self.assertIsNone(query._filters_pb())

    def test__filters_pb_single(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1.where("x.y", ">", 50.5)
        filter_pb = query2._filters_pb()
        expected_pb = query.StructuredQuery.Filter(
            field_filter=query.StructuredQuery.FieldFilter(
                field=query.StructuredQuery.FieldReference(field_path="x.y"),
                op=StructuredQuery.FieldFilter.Operator.GREATER_THAN,
                value=document.Value(double_value=50.5),
            )
        )
        self.assertEqual(filter_pb, expected_pb)

    def test__filters_pb_multi(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1.where("x.y", ">", 50.5)
        query3 = query2.where("ABC", "==", 123)

        filter_pb = query3._filters_pb()
        op_class = StructuredQuery.FieldFilter.Operator
        expected_pb = query.StructuredQuery.Filter(
            composite_filter=query.StructuredQuery.CompositeFilter(
                op=StructuredQuery.CompositeFilter.Operator.AND,
                filters=[
                    query.StructuredQuery.Filter(
                        field_filter=query.StructuredQuery.FieldFilter(
                            field=query.StructuredQuery.FieldReference(
                                field_path="x.y"
                            ),
                            op=op_class.GREATER_THAN,
                            value=document.Value(double_value=50.5),
                        )
                    ),
                    query.StructuredQuery.Filter(
                        field_filter=query.StructuredQuery.FieldFilter(
                            field=query.StructuredQuery.FieldReference(
                                field_path="ABC"
                            ),
                            op=op_class.EQUAL,
                            value=document.Value(integer_value=123),
                        )
                    ),
                ],
            )
        )
        self.assertEqual(filter_pb, expected_pb)

    def test__normalize_projection_none(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertIsNone(query._normalize_projection(None))

    def test__normalize_projection_empty(self):
        projection = self._make_projection_for_select([])
        query = self._make_one(mock.sentinel.parent)
        normalized = query._normalize_projection(projection)
        field_paths = [field_ref.field_path for field_ref in normalized.fields]
        self.assertEqual(field_paths, ["__name__"])

    def test__normalize_projection_non_empty(self):
        projection = self._make_projection_for_select(["a", "b"])
        query = self._make_one(mock.sentinel.parent)
        self.assertIs(query._normalize_projection(projection), projection)

    def test__normalize_orders_wo_orders_wo_cursors(self):
        query = self._make_one(mock.sentinel.parent)
        expected = []
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_orders_w_orders_wo_cursors(self):
        query = self._make_one(mock.sentinel.parent).order_by("a")
        expected = [query._make_order("a", "ASCENDING")]
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_orders_wo_orders_w_snapshot_cursor(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query = self._make_one(collection).start_at(snapshot)
        expected = [query._make_order("__name__", "ASCENDING")]
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_orders_w_name_orders_w_snapshot_cursor(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query = (
            self._make_one(collection)
            .order_by("__name__", "DESCENDING")
            .start_at(snapshot)
        )
        expected = [query._make_order("__name__", "DESCENDING")]
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_orders_wo_orders_w_snapshot_cursor_w_neq_exists(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query = (
            self._make_one(collection)
            .where("c", "<=", 20)
            .order_by("c", "DESCENDING")
            .start_at(snapshot)
        )
        expected = [
            query._make_order("c", "DESCENDING"),
            query._make_order("__name__", "DESCENDING"),
        ]
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_orders_wo_orders_w_snapshot_cursor_w_neq_where(self):
        values = {"a": 7, "b": "foo"}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        collection = self._make_collection("here")
        query = self._make_one(collection).where("c", "<=", 20).end_at(snapshot)
        expected = [
            query._make_order("c", "ASCENDING"),
            query._make_order("__name__", "ASCENDING"),
        ]
        self.assertEqual(query._normalize_orders(), expected)

    def test__normalize_cursor_none(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertIsNone(query._normalize_cursor(None, query._orders))

    def test__normalize_cursor_no_order(self):
        cursor = ([1], True)
        query = self._make_one(mock.sentinel.parent)

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_as_list_mismatched_order(self):
        cursor = ([1, 2], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_as_dict_mismatched_order(self):
        cursor = ({"a": 1}, True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_w_delete(self):
        from google.cloud.firestore_v1 import DELETE_FIELD

        cursor = ([DELETE_FIELD], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_w_server_timestamp(self):
        from google.cloud.firestore_v1 import SERVER_TIMESTAMP

        cursor = ([SERVER_TIMESTAMP], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_w_array_remove(self):
        from google.cloud.firestore_v1 import ArrayRemove

        cursor = ([ArrayRemove([1, 3, 5])], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_w_array_union(self):
        from google.cloud.firestore_v1 import ArrayUnion

        cursor = ([ArrayUnion([2, 4, 8])], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        with self.assertRaises(ValueError):
            query._normalize_cursor(cursor, query._orders)

    def test__normalize_cursor_as_list_hit(self):
        cursor = ([1], True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        self.assertEqual(query._normalize_cursor(cursor, query._orders), ([1], True))

    def test__normalize_cursor_as_dict_hit(self):
        cursor = ({"b": 1}, True)
        query = self._make_one(mock.sentinel.parent).order_by("b", "ASCENDING")

        self.assertEqual(query._normalize_cursor(cursor, query._orders), ([1], True))

    def test__normalize_cursor_as_dict_with_dot_key_hit(self):
        cursor = ({"b.a": 1}, True)
        query = self._make_one(mock.sentinel.parent).order_by("b.a", "ASCENDING")
        self.assertEqual(query._normalize_cursor(cursor, query._orders), ([1], True))

    def test__normalize_cursor_as_dict_with_inner_data_hit(self):
        cursor = ({"b": {"a": 1}}, True)
        query = self._make_one(mock.sentinel.parent).order_by("b.a", "ASCENDING")
        self.assertEqual(query._normalize_cursor(cursor, query._orders), ([1], True))

    def test__normalize_cursor_as_snapshot_hit(self):
        values = {"b": 1}
        docref = self._make_docref("here", "doc_id")
        snapshot = self._make_snapshot(docref, values)
        cursor = (snapshot, True)
        collection = self._make_collection("here")
        query = self._make_one(collection).order_by("b", "ASCENDING")

        self.assertEqual(query._normalize_cursor(cursor, query._orders), ([1], True))

    def test__normalize_cursor_w___name___w_reference(self):
        db_string = "projects/my-project/database/(default)"
        client = mock.Mock(spec=["_database_string"])
        client._database_string = db_string
        parent = mock.Mock(spec=["_path", "_client"])
        parent._client = client
        parent._path = ["C"]
        query = self._make_one(parent).order_by("__name__", "ASCENDING")
        docref = self._make_docref("here", "doc_id")
        values = {"a": 7}
        snapshot = self._make_snapshot(docref, values)
        expected = docref
        cursor = (snapshot, True)

        self.assertEqual(
            query._normalize_cursor(cursor, query._orders), ([expected], True)
        )

    def test__normalize_cursor_w___name___wo_slash(self):
        db_string = "projects/my-project/database/(default)"
        client = mock.Mock(spec=["_database_string"])
        client._database_string = db_string
        parent = mock.Mock(spec=["_path", "_client", "document"])
        parent._client = client
        parent._path = ["C"]
        document = parent.document.return_value = mock.Mock(spec=[])
        query = self._make_one(parent).order_by("__name__", "ASCENDING")
        cursor = (["b"], True)
        expected = document

        self.assertEqual(
            query._normalize_cursor(cursor, query._orders), ([expected], True)
        )
        parent.document.assert_called_once_with("b")

    def test__to_protobuf_all_fields(self):
        from google.protobuf import wrappers_pb2
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="cat", spec=["id"])
        query1 = self._make_one(parent)
        query2 = query1.select(["X", "Y", "Z"])
        query3 = query2.where("Y", ">", 2.5)
        query4 = query3.order_by("X")
        query5 = query4.limit(17)
        query6 = query5.offset(3)
        query7 = query6.start_at({"X": 10})
        query8 = query7.end_at({"X": 25})

        structured_query_pb = query8._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "select": query.StructuredQuery.Projection(
                fields=[
                    query.StructuredQuery.FieldReference(field_path=field_path)
                    for field_path in ["X", "Y", "Z"]
                ]
            ),
            "where": query.StructuredQuery.Filter(
                field_filter=query.StructuredQuery.FieldFilter(
                    field=query.StructuredQuery.FieldReference(field_path="Y"),
                    op=StructuredQuery.FieldFilter.Operator.GREATER_THAN,
                    value=document.Value(double_value=2.5),
                )
            ),
            "order_by": [_make_order_pb("X", StructuredQuery.Direction.ASCENDING)],
            "start_at": query.Cursor(
                values=[document.Value(integer_value=10)], before=True
            ),
            "end_at": query.Cursor(values=[document.Value(integer_value=25)]),
            "offset": 3,
            "limit": wrappers_pb2.Int32Value(value=17),
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_select_only(self):
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="cat", spec=["id"])
        query1 = self._make_one(parent)
        field_paths = ["a.b", "a.c", "d"]
        query2 = query1.select(field_paths)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "select": query.StructuredQuery.Projection(
                fields=[
                    query.StructuredQuery.FieldReference(field_path=field_path)
                    for field_path in field_paths
                ]
            ),
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_where_only(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="dog", spec=["id"])
        query1 = self._make_one(parent)
        query2 = query1.where("a", "==", u"b")

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "where": query.StructuredQuery.Filter(
                field_filter=query.StructuredQuery.FieldFilter(
                    field=query.StructuredQuery.FieldReference(field_path="a"),
                    op=StructuredQuery.FieldFilter.Operator.EQUAL,
                    value=document.Value(string_value=u"b"),
                )
            ),
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_order_by_only(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="fish", spec=["id"])
        query1 = self._make_one(parent)
        query2 = query1.order_by("abc")

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "order_by": [_make_order_pb("abc", StructuredQuery.Direction.ASCENDING)],
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_start_at_only(self):
        # NOTE: "only" is wrong since we must have ``order_by`` as well.
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="phish", spec=["id"])
        query_inst = (
            self._make_one(parent).order_by("X.Y").start_after({"X": {"Y": u"Z"}})
        )

        structured_query_pb = query_inst._to_protobuf()
        query_kwargs = {
            "from_": [StructuredQuery.CollectionSelector(collection_id=parent.id)],
            "order_by": [_make_order_pb("X.Y", StructuredQuery.Direction.ASCENDING)],
            "start_at": query.Cursor(values=[document.Value(string_value=u"Z")]),
        }
        expected_pb = StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_end_at_only(self):
        # NOTE: "only" is wrong since we must have ``order_by`` as well.
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="ghoti", spec=["id"])
        query_inst = self._make_one(parent).order_by("a").end_at({"a": 88})

        structured_query_pb = query_inst._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "order_by": [_make_order_pb("a", StructuredQuery.Direction.ASCENDING)],
            "end_at": query.Cursor(values=[document.Value(integer_value=88)]),
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_offset_only(self):
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="cartt", spec=["id"])
        query1 = self._make_one(parent)
        offset = 14
        query2 = query1.offset(offset)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "offset": offset,
        }
        expected_pb = query.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_limit_only(self):
        from google.protobuf import wrappers_pb2
        from google.cloud.firestore_v1.types import query

        parent = mock.Mock(id="donut", spec=["id"])
        query1 = self._make_one(parent)
        limit = 31
        query2 = query1.limit(limit)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            "from_": [
                query.StructuredQuery.CollectionSelector(collection_id=parent.id)
            ],
            "limit": wrappers_pb2.Int32Value(value=limit),
        }
        expected_pb = query.StructuredQuery(**query_kwargs)

        self.assertEqual(structured_query_pb, expected_pb)

    def test_comparator_no_ordering(self):
        query = self._make_one(mock.sentinel.parent)
        query._orders = []
        doc1 = mock.Mock()
        doc1.reference._path = ("col", "adocument1")

        doc2 = mock.Mock()
        doc2.reference._path = ("col", "adocument2")

        sort = query._comparator(doc1, doc2)
        self.assertEqual(sort, -1)

    def test_comparator_no_ordering_same_id(self):
        query = self._make_one(mock.sentinel.parent)
        query._orders = []
        doc1 = mock.Mock()
        doc1.reference._path = ("col", "adocument1")

        doc2 = mock.Mock()
        doc2.reference._path = ("col", "adocument1")

        sort = query._comparator(doc1, doc2)
        self.assertEqual(sort, 0)

    def test_comparator_ordering(self):
        query = self._make_one(mock.sentinel.parent)
        orderByMock = mock.Mock()
        orderByMock.field.field_path = "last"
        orderByMock.direction = 1  # ascending
        query._orders = [orderByMock]

        doc1 = mock.Mock()
        doc1.reference._path = ("col", "adocument1")
        doc1._data = {
            "first": {"stringValue": "Ada"},
            "last": {"stringValue": "secondlovelace"},
        }
        doc2 = mock.Mock()
        doc2.reference._path = ("col", "adocument2")
        doc2._data = {
            "first": {"stringValue": "Ada"},
            "last": {"stringValue": "lovelace"},
        }

        sort = query._comparator(doc1, doc2)
        self.assertEqual(sort, 1)

    def test_comparator_ordering_descending(self):
        query = self._make_one(mock.sentinel.parent)
        orderByMock = mock.Mock()
        orderByMock.field.field_path = "last"
        orderByMock.direction = -1  # descending
        query._orders = [orderByMock]

        doc1 = mock.Mock()
        doc1.reference._path = ("col", "adocument1")
        doc1._data = {
            "first": {"stringValue": "Ada"},
            "last": {"stringValue": "secondlovelace"},
        }
        doc2 = mock.Mock()
        doc2.reference._path = ("col", "adocument2")
        doc2._data = {
            "first": {"stringValue": "Ada"},
            "last": {"stringValue": "lovelace"},
        }

        sort = query._comparator(doc1, doc2)
        self.assertEqual(sort, -1)

    def test_comparator_missing_order_by_field_in_data_raises(self):
        query = self._make_one(mock.sentinel.parent)
        orderByMock = mock.Mock()
        orderByMock.field.field_path = "last"
        orderByMock.direction = 1  # ascending
        query._orders = [orderByMock]

        doc1 = mock.Mock()
        doc1.reference._path = ("col", "adocument1")
        doc1._data = {}
        doc2 = mock.Mock()
        doc2.reference._path = ("col", "adocument2")
        doc2._data = {
            "first": {"stringValue": "Ada"},
            "last": {"stringValue": "lovelace"},
        }

        with self.assertRaisesRegex(ValueError, "Can only compare fields "):
            query._comparator(doc1, doc2)


class Test__enum_from_op_string(unittest.TestCase):
    @staticmethod
    def _call_fut(op_string):
        from google.cloud.firestore_v1.base_query import _enum_from_op_string

        return _enum_from_op_string(op_string)

    @staticmethod
    def _get_op_class():
        from google.cloud.firestore_v1.types import StructuredQuery

        return StructuredQuery.FieldFilter.Operator

    def test_lt(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("<"), op_class.LESS_THAN)

    def test_le(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("<="), op_class.LESS_THAN_OR_EQUAL)

    def test_eq(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("=="), op_class.EQUAL)

    def test_ge(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut(">="), op_class.GREATER_THAN_OR_EQUAL)

    def test_gt(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut(">"), op_class.GREATER_THAN)

    def test_array_contains(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("array_contains"), op_class.ARRAY_CONTAINS)

    def test_in(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("in"), op_class.IN)

    def test_array_contains_any(self):
        op_class = self._get_op_class()
        self.assertEqual(
            self._call_fut("array_contains_any"), op_class.ARRAY_CONTAINS_ANY
        )

    def test_not_in(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("not-in"), op_class.NOT_IN)

    def test_not_eq(self):
        op_class = self._get_op_class()
        self.assertEqual(self._call_fut("!="), op_class.NOT_EQUAL)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            self._call_fut("?")


class Test__isnan(unittest.TestCase):
    @staticmethod
    def _call_fut(value):
        from google.cloud.firestore_v1.base_query import _isnan

        return _isnan(value)

    def test_valid(self):
        self.assertTrue(self._call_fut(float("nan")))

    def test_invalid(self):
        self.assertFalse(self._call_fut(51.5))
        self.assertFalse(self._call_fut(None))
        self.assertFalse(self._call_fut("str"))
        self.assertFalse(self._call_fut(int))
        self.assertFalse(self._call_fut(1.0 + 1.0j))


class Test__enum_from_direction(unittest.TestCase):
    @staticmethod
    def _call_fut(direction):
        from google.cloud.firestore_v1.base_query import _enum_from_direction

        return _enum_from_direction(direction)

    def test_success(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.query import Query

        dir_class = StructuredQuery.Direction
        self.assertEqual(self._call_fut(Query.ASCENDING), dir_class.ASCENDING)
        self.assertEqual(self._call_fut(Query.DESCENDING), dir_class.DESCENDING)

        # Ints pass through
        self.assertEqual(self._call_fut(dir_class.ASCENDING), dir_class.ASCENDING)
        self.assertEqual(self._call_fut(dir_class.DESCENDING), dir_class.DESCENDING)

    def test_failure(self):
        with self.assertRaises(ValueError):
            self._call_fut("neither-ASCENDING-nor-DESCENDING")


class Test__filter_pb(unittest.TestCase):
    @staticmethod
    def _call_fut(field_or_unary):
        from google.cloud.firestore_v1.base_query import _filter_pb

        return _filter_pb(field_or_unary)

    def test_unary(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import query

        unary_pb = query.StructuredQuery.UnaryFilter(
            field=query.StructuredQuery.FieldReference(field_path="a.b.c"),
            op=StructuredQuery.UnaryFilter.Operator.IS_NULL,
        )
        filter_pb = self._call_fut(unary_pb)
        expected_pb = query.StructuredQuery.Filter(unary_filter=unary_pb)
        self.assertEqual(filter_pb, expected_pb)

    def test_field(self):
        from google.cloud.firestore_v1.types import StructuredQuery

        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import query

        field_filter_pb = query.StructuredQuery.FieldFilter(
            field=query.StructuredQuery.FieldReference(field_path="XYZ"),
            op=StructuredQuery.FieldFilter.Operator.GREATER_THAN,
            value=document.Value(double_value=90.75),
        )
        filter_pb = self._call_fut(field_filter_pb)
        expected_pb = query.StructuredQuery.Filter(field_filter=field_filter_pb)
        self.assertEqual(filter_pb, expected_pb)

    def test_bad_type(self):
        with self.assertRaises(ValueError):
            self._call_fut(None)


class Test__cursor_pb(unittest.TestCase):
    @staticmethod
    def _call_fut(cursor_pair):
        from google.cloud.firestore_v1.base_query import _cursor_pb

        return _cursor_pb(cursor_pair)

    def test_no_pair(self):
        self.assertIsNone(self._call_fut(None))

    def test_success(self):
        from google.cloud.firestore_v1.types import query
        from google.cloud.firestore_v1 import _helpers

        data = [1.5, 10, True]
        cursor_pair = data, True

        cursor_pb = self._call_fut(cursor_pair)

        expected_pb = query.Cursor(
            values=[_helpers.encode_value(value) for value in data], before=True
        )
        self.assertEqual(cursor_pb, expected_pb)


class Test__query_response_to_snapshot(unittest.TestCase):
    @staticmethod
    def _call_fut(response_pb, collection, expected_prefix):
        from google.cloud.firestore_v1.base_query import _query_response_to_snapshot

        return _query_response_to_snapshot(response_pb, collection, expected_prefix)

    def test_empty(self):
        response_pb = _make_query_response()
        snapshot = self._call_fut(response_pb, None, None)
        self.assertIsNone(snapshot)

    def test_after_offset(self):
        skipped_results = 410
        response_pb = _make_query_response(skipped_results=skipped_results)
        snapshot = self._call_fut(response_pb, None, None)
        self.assertIsNone(snapshot)

    def test_response(self):
        from google.cloud.firestore_v1.document import DocumentSnapshot

        client = _make_client()
        collection = client.collection("a", "b", "c")
        _, expected_prefix = collection._parent_info()

        # Create name for the protobuf.
        doc_id = "gigantic"
        name = "{}/{}".format(expected_prefix, doc_id)
        data = {"a": 901, "b": True}
        response_pb = _make_query_response(name=name, data=data)

        snapshot = self._call_fut(response_pb, collection, expected_prefix)
        self.assertIsInstance(snapshot, DocumentSnapshot)
        expected_path = collection._path + (doc_id,)
        self.assertEqual(snapshot.reference._path, expected_path)
        self.assertEqual(snapshot.to_dict(), data)
        self.assertTrue(snapshot.exists)
        self.assertEqual(snapshot.read_time, response_pb.read_time)
        self.assertEqual(snapshot.create_time, response_pb.document.create_time)
        self.assertEqual(snapshot.update_time, response_pb.document.update_time)


class Test__collection_group_query_response_to_snapshot(unittest.TestCase):
    @staticmethod
    def _call_fut(response_pb, collection):
        from google.cloud.firestore_v1.base_query import (
            _collection_group_query_response_to_snapshot,
        )

        return _collection_group_query_response_to_snapshot(response_pb, collection)

    def test_empty(self):
        response_pb = _make_query_response()
        snapshot = self._call_fut(response_pb, None)
        self.assertIsNone(snapshot)

    def test_after_offset(self):
        skipped_results = 410
        response_pb = _make_query_response(skipped_results=skipped_results)
        snapshot = self._call_fut(response_pb, None)
        self.assertIsNone(snapshot)

    def test_response(self):
        from google.cloud.firestore_v1.document import DocumentSnapshot

        client = _make_client()
        collection = client.collection("a", "b", "c")
        other_collection = client.collection("a", "b", "d")
        to_match = other_collection.document("gigantic")
        data = {"a": 901, "b": True}
        response_pb = _make_query_response(name=to_match._document_path, data=data)

        snapshot = self._call_fut(response_pb, collection)
        self.assertIsInstance(snapshot, DocumentSnapshot)
        self.assertEqual(snapshot.reference._document_path, to_match._document_path)
        self.assertEqual(snapshot.to_dict(), data)
        self.assertTrue(snapshot.exists)
        self.assertEqual(snapshot.read_time, response_pb._pb.read_time)
        self.assertEqual(snapshot.create_time, response_pb._pb.document.create_time)
        self.assertEqual(snapshot.update_time, response_pb._pb.document.update_time)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="project-project"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)


def _make_order_pb(field_path, direction):
    from google.cloud.firestore_v1.types import query

    return query.StructuredQuery.Order(
        field=query.StructuredQuery.FieldReference(field_path=field_path),
        direction=direction,
    )


def _make_query_response(**kwargs):
    # kwargs supported are ``skipped_results``, ``name`` and ``data``
    from google.cloud.firestore_v1.types import document
    from google.cloud.firestore_v1.types import firestore
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.firestore_v1 import _helpers

    now = datetime.datetime.utcnow()
    read_time = _datetime_to_pb_timestamp(now)
    kwargs["read_time"] = read_time

    name = kwargs.pop("name", None)
    data = kwargs.pop("data", None)
    if name is not None and data is not None:
        document_pb = document.Document(name=name, fields=_helpers.encode_dict(data))
        delta = datetime.timedelta(seconds=100)
        update_time = _datetime_to_pb_timestamp(now - delta)
        create_time = _datetime_to_pb_timestamp(now - 2 * delta)
        document_pb._pb.update_time.CopyFrom(update_time)
        document_pb._pb.create_time.CopyFrom(create_time)

        kwargs["document"] = document_pb

    return firestore.RunQueryResponse(**kwargs)


def _make_cursor_pb(pair):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.types import query

    values, before = pair
    value_pbs = [_helpers.encode_value(value) for value in values]
    return query.Cursor(values=value_pbs, before=before)


class TestQueryPartition(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.base_query import QueryPartition

        return QueryPartition

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        partition = self._make_one(mock.sentinel.query, "start", "end")
        assert partition._query is mock.sentinel.query
        assert partition.start_at == "start"
        assert partition.end_at == "end"

    def test_query_begin(self):
        partition = self._make_one(DummyQuery("PARENT"), None, "end")
        query = partition.query()
        assert query._parent == "PARENT"
        assert query.all_descendants == "YUP"
        assert query.orders == "ORDER"
        assert query.start_at is None
        assert query.end_at == (["end"], True)

    def test_query_middle(self):
        partition = self._make_one(DummyQuery("PARENT"), "start", "end")
        query = partition.query()
        assert query._parent == "PARENT"
        assert query.all_descendants == "YUP"
        assert query.orders == "ORDER"
        assert query.start_at == (["start"], True)
        assert query.end_at == (["end"], True)

    def test_query_end(self):
        partition = self._make_one(DummyQuery("PARENT"), "start", None)
        query = partition.query()
        assert query._parent == "PARENT"
        assert query.all_descendants == "YUP"
        assert query.orders == "ORDER"
        assert query.start_at == (["start"], True)
        assert query.end_at is None


class DummyQuery:
    _all_descendants = "YUP"
    _PARTITION_QUERY_ORDER = "ORDER"

    def __init__(
        self, parent, *, all_descendants=None, orders=None, start_at=None, end_at=None
    ):
        self._parent = parent
        self.all_descendants = all_descendants
        self.orders = orders
        self.start_at = start_at
        self.end_at = end_at
