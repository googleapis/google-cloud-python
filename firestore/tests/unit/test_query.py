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
import types
import unittest

import mock


class TestQuery(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.query import Query

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

    def _make_one_all_fields(self, limit=9876, offset=12, skip_fields=()):
        kwargs = {
            'projection': mock.sentinel.projection,
            'field_filters': mock.sentinel.filters,
            'orders': mock.sentinel.orders,
            'limit': limit,
            'offset': offset,
            'start_at': mock.sentinel.start_at,
            'end_at': mock.sentinel.end_at,
        }
        for field in skip_fields:
            kwargs.pop(field)
        return self._make_one(mock.sentinel.parent, **kwargs)

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

    def test__client_property(self):
        parent = mock.Mock(_client=mock.sentinel.client, spec=['_client'])
        query = self._make_one(parent)
        self.assertIs(query._client, mock.sentinel.client)

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
        from google.cloud.firestore_v1beta1.proto import query_pb2

        return query_pb2.StructuredQuery.Projection(
            fields=[
                query_pb2.StructuredQuery.FieldReference(field_path=field_path)
                for field_path in field_paths
            ],
        )

    def test_select(self):
        query1 = self._make_one_all_fields()

        field_paths2 = ['foo', 'bar']
        query2 = query1.select(field_paths2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(
            query2._projection,
            self._make_projection_for_select(field_paths2))
        self._compare_queries(query1, query2, '_projection')

        # Make sure it overrides.
        field_paths3 = ['foo.baz']
        query3 = query2.select(field_paths3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(
            query3._projection,
            self._make_projection_for_select(field_paths3))
        self._compare_queries(query2, query3, '_projection')

    def test_where(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        query = self._make_one_all_fields(skip_fields=('field_filters',))
        new_query = query.where('power.level', '>', 9000)

        self.assertIsNot(query, new_query)
        self.assertIsInstance(new_query, self._get_target_class())
        self.assertEqual(len(new_query._field_filters), 1)

        field_pb = new_query._field_filters[0]
        expected_pb = query_pb2.StructuredQuery.FieldFilter(
            field=query_pb2.StructuredQuery.FieldReference(
                field_path='power.level',
            ),
            op=enums.StructuredQuery.FieldFilter.Operator.GREATER_THAN,
            value=document_pb2.Value(integer_value=9000),
        )
        self.assertEqual(field_pb, expected_pb)
        self._compare_queries(query, new_query, '_field_filters')

    def _where_unary_helper(self, value, op_enum, op_string='=='):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import query_pb2

        query = self._make_one_all_fields(skip_fields=('field_filters',))
        field_path = 'feeeld'
        new_query = query.where(field_path, op_string, value)

        self.assertIsNot(query, new_query)
        self.assertIsInstance(new_query, self._get_target_class())
        self.assertEqual(len(new_query._field_filters), 1)

        field_pb = new_query._field_filters[0]
        expected_pb = query_pb2.StructuredQuery.UnaryFilter(
            field=query_pb2.StructuredQuery.FieldReference(
                field_path=field_path,
            ),
            op=op_enum,
        )
        self.assertEqual(field_pb, expected_pb)
        self._compare_queries(query, new_query, '_field_filters')

    def test_where_eq_null(self):
        from google.cloud.firestore_v1beta1.gapic import enums

        op_enum = enums.StructuredQuery.UnaryFilter.Operator.IS_NULL
        self._where_unary_helper(None, op_enum)

    def test_where_gt_null(self):
        with self.assertRaises(ValueError):
            self._where_unary_helper(None, 0, op_string='>')

    def test_where_eq_nan(self):
        from google.cloud.firestore_v1beta1.gapic import enums

        op_enum = enums.StructuredQuery.UnaryFilter.Operator.IS_NAN
        self._where_unary_helper(float('nan'), op_enum)

    def test_where_le_nan(self):
        with self.assertRaises(ValueError):
            self._where_unary_helper(float('nan'), 0, op_string='<=')

    def test_order_by(self):
        from google.cloud.firestore_v1beta1.gapic import enums

        klass = self._get_target_class()
        query1 = self._make_one_all_fields(skip_fields=('orders',))

        field_path2 = 'a'
        query2 = query1.order_by(field_path2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, klass)
        order_pb2 = _make_order_pb(
            field_path2, enums.StructuredQuery.Direction.ASCENDING)
        self.assertEqual(query2._orders, (order_pb2,))
        self._compare_queries(query1, query2, '_orders')

        # Make sure it appends to the orders.
        field_path3 = 'b'
        query3 = query2.order_by(field_path3, direction=klass.DESCENDING)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, klass)
        order_pb3 = _make_order_pb(
            field_path3, enums.StructuredQuery.Direction.DESCENDING)
        self.assertEqual(query3._orders, (order_pb2, order_pb3))
        self._compare_queries(query2, query3, '_orders')

    def test_limit(self):
        query1 = self._make_one_all_fields()

        limit2 = 100
        query2 = query1.limit(limit2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(query2._limit, limit2)
        self._compare_queries(query1, query2, '_limit')

        # Make sure it overrides.
        limit3 = 10
        query3 = query2.limit(limit3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._limit, limit3)
        self._compare_queries(query2, query3, '_limit')

    def test_offset(self):
        query1 = self._make_one_all_fields()

        offset2 = 23
        query2 = query1.offset(offset2)
        self.assertIsNot(query2, query1)
        self.assertIsInstance(query2, self._get_target_class())
        self.assertEqual(query2._offset, offset2)
        self._compare_queries(query1, query2, '_offset')

        # Make sure it overrides.
        offset3 = 35
        query3 = query2.offset(offset3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._offset, offset3)
        self._compare_queries(query2, query3, '_offset')

    def test_start_at(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        query1 = self._make_one_all_fields(skip_fields=('orders',))
        query2 = query1.order_by('hi')

        document_fields3 = {'hi': 'mom'}
        query3 = query2.start_at(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._start_at, (document_fields3, True))
        self._compare_queries(query2, query3, '_start_at')

        # Make sure it overrides.
        query4 = query3.order_by('bye')
        values5 = {'hi': 'zap', 'bye': 88}
        document_fields5 = DocumentSnapshot(
            None, values5, True, None, None, None)
        query5 = query4.start_at(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._start_at, (values5, True))
        self._compare_queries(query4, query5, '_start_at')

    def test_start_after(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        query1 = self._make_one_all_fields(skip_fields=('orders',))
        query2 = query1.order_by('down')

        document_fields3 = {'down': 99.75}
        query3 = query2.start_after(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._start_at, (document_fields3, False))
        self._compare_queries(query2, query3, '_start_at')

        # Make sure it overrides.
        query4 = query3.order_by('out')
        values5 = {'down': 100.25, 'out': b'\x00\x01'}
        document_fields5 = DocumentSnapshot(
            None, values5, True, None, None, None)
        query5 = query4.start_after(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._start_at, (values5, False))
        self._compare_queries(query4, query5, '_start_at')

    def test_end_before(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        query1 = self._make_one_all_fields(skip_fields=('orders',))
        query2 = query1.order_by('down')

        document_fields3 = {'down': 99.75}
        query3 = query2.end_before(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._end_at, (document_fields3, True))
        self._compare_queries(query2, query3, '_end_at')

        # Make sure it overrides.
        query4 = query3.order_by('out')
        values5 = {'down': 100.25, 'out': b'\x00\x01'}
        document_fields5 = DocumentSnapshot(
            None, values5, True, None, None, None)
        query5 = query4.end_before(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._end_at, (values5, True))
        self._compare_queries(query4, query5, '_end_at')

    def test_end_at(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        query1 = self._make_one_all_fields(skip_fields=('orders',))
        query2 = query1.order_by('hi')

        document_fields3 = {'hi': 'mom'}
        query3 = query2.end_at(document_fields3)
        self.assertIsNot(query3, query2)
        self.assertIsInstance(query3, self._get_target_class())
        self.assertEqual(query3._end_at, (document_fields3, False))
        self._compare_queries(query2, query3, '_end_at')

        # Make sure it overrides.
        query4 = query3.order_by('bye')
        values5 = {'hi': 'zap', 'bye': 88}
        document_fields5 = DocumentSnapshot(
            None, values5, True, None, None, None)
        query5 = query4.end_at(document_fields5)
        self.assertIsNot(query5, query4)
        self.assertIsInstance(query5, self._get_target_class())
        self.assertEqual(query5._end_at, (values5, False))
        self._compare_queries(query4, query5, '_end_at')

    def test__filters_pb_empty(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertEqual(len(query._field_filters), 0)
        self.assertIsNone(query._filters_pb())

    def test__filters_pb_single(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1.where('x.y', '>', 50.5)
        filter_pb = query2._filters_pb()
        expected_pb = query_pb2.StructuredQuery.Filter(
            field_filter=query_pb2.StructuredQuery.FieldFilter(
                field=query_pb2.StructuredQuery.FieldReference(
                    field_path='x.y',
                ),
                op=enums.StructuredQuery.FieldFilter.Operator.GREATER_THAN,
                value=document_pb2.Value(double_value=50.5),
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test__filters_pb_multi(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        query1 = self._make_one(mock.sentinel.parent)
        query2 = query1.where('x.y', '>', 50.5)
        query3 = query2.where('ABC', '==', 123)

        filter_pb = query3._filters_pb()
        op_class = enums.StructuredQuery.FieldFilter.Operator
        expected_pb = query_pb2.StructuredQuery.Filter(
            composite_filter=query_pb2.StructuredQuery.CompositeFilter(
                op=enums.StructuredQuery.CompositeFilter.Operator.AND,
                filters=[
                    query_pb2.StructuredQuery.Filter(
                        field_filter=query_pb2.StructuredQuery.FieldFilter(
                            field=query_pb2.StructuredQuery.FieldReference(
                                field_path='x.y',
                            ),
                            op=op_class.GREATER_THAN,
                            value=document_pb2.Value(double_value=50.5),
                        ),
                    ),
                    query_pb2.StructuredQuery.Filter(
                        field_filter=query_pb2.StructuredQuery.FieldFilter(
                            field=query_pb2.StructuredQuery.FieldReference(
                                field_path='ABC',
                            ),
                            op=op_class.EQUAL,
                            value=document_pb2.Value(integer_value=123),
                        ),
                    ),
                ],
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test__to_protobuf_all_fields(self):
        from google.protobuf import wrappers_pb2
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='cat', spec=['id'])
        query1 = self._make_one(parent)
        query2 = query1.select(['X', 'Y', 'Z'])
        query3 = query2.where('Y', '>', 2.5)
        query4 = query3.order_by('X')
        query5 = query4.limit(17)
        query6 = query5.offset(3)
        query7 = query6.start_at({'X': 10})
        query8 = query7.end_at({'X': 25})

        structured_query_pb = query8._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'select': query_pb2.StructuredQuery.Projection(
                fields=[
                    query_pb2.StructuredQuery.FieldReference(
                        field_path=field_path
                    )
                    for field_path in ['X', 'Y', 'Z']
                ],
            ),
            'where': query_pb2.StructuredQuery.Filter(
                field_filter=query_pb2.StructuredQuery.FieldFilter(
                    field=query_pb2.StructuredQuery.FieldReference(
                        field_path='Y',
                    ),
                    op=enums.StructuredQuery.FieldFilter.Operator.GREATER_THAN,
                    value=document_pb2.Value(double_value=2.5),
                ),
            ),
            'order_by': [
                _make_order_pb(
                    'X',
                    enums.StructuredQuery.Direction.ASCENDING,
                ),
            ],
            'start_at': query_pb2.Cursor(
                values=[
                    document_pb2.Value(integer_value=10),
                ],
                before=True,
            ),
            'end_at': query_pb2.Cursor(
                values=[
                    document_pb2.Value(integer_value=25),
                ],
            ),
            'offset': 3,
            'limit': wrappers_pb2.Int32Value(value=17),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_select_only(self):
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='cat', spec=['id'])
        query1 = self._make_one(parent)
        field_paths = ['a.b', 'a.c', 'd']
        query2 = query1.select(field_paths)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'select': query_pb2.StructuredQuery.Projection(
                fields=[
                    query_pb2.StructuredQuery.FieldReference(
                        field_path=field_path
                    )
                    for field_path in field_paths
                ],
            ),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_where_only(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='dog', spec=['id'])
        query1 = self._make_one(parent)
        query2 = query1.where('a', '==', u'b')

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'where': query_pb2.StructuredQuery.Filter(
                field_filter=query_pb2.StructuredQuery.FieldFilter(
                    field=query_pb2.StructuredQuery.FieldReference(
                        field_path='a',
                    ),
                    op=enums.StructuredQuery.FieldFilter.Operator.EQUAL,
                    value=document_pb2.Value(string_value=u'b'),
                ),
            ),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_order_by_only(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='fish', spec=['id'])
        query1 = self._make_one(parent)
        query2 = query1.order_by('abc')

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'order_by': [
                _make_order_pb(
                    'abc',
                    enums.StructuredQuery.Direction.ASCENDING,
                ),
            ],
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_start_at_only(self):
        # NOTE: "only" is wrong since we must have ``order_by`` as well.
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='phish', spec=['id'])
        query1 = self._make_one(parent)
        query2 = query1.start_after({'X': {'Y': u'Z'}})
        query3 = query2.order_by('X.Y')

        structured_query_pb = query3._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'order_by': [
                _make_order_pb(
                    'X.Y',
                    enums.StructuredQuery.Direction.ASCENDING,
                ),
            ],
            'start_at': query_pb2.Cursor(
                values=[
                    document_pb2.Value(string_value=u'Z'),
                ],
            ),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_end_at_only(self):
        # NOTE: "only" is wrong since we must have ``order_by`` as well.
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='ghoti', spec=['id'])
        query1 = self._make_one(parent)
        query2 = query1.end_at({'a': 88})
        query3 = query2.order_by('a')

        structured_query_pb = query3._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'order_by': [
                _make_order_pb(
                    'a',
                    enums.StructuredQuery.Direction.ASCENDING,
                ),
            ],
            'end_at': query_pb2.Cursor(
                values=[
                    document_pb2.Value(integer_value=88),
                ],
            ),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_offset_only(self):
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='cartt', spec=['id'])
        query1 = self._make_one(parent)
        offset = 14
        query2 = query1.offset(offset)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'offset': offset,
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)
        self.assertEqual(structured_query_pb, expected_pb)

    def test__to_protobuf_limit_only(self):
        from google.protobuf import wrappers_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        parent = mock.Mock(id='donut', spec=['id'])
        query1 = self._make_one(parent)
        limit = 31
        query2 = query1.limit(limit)

        structured_query_pb = query2._to_protobuf()
        query_kwargs = {
            'from': [
                query_pb2.StructuredQuery.CollectionSelector(
                    collection_id=parent.id,
                ),
            ],
            'limit': wrappers_pb2.Int32Value(value=limit),
        }
        expected_pb = query_pb2.StructuredQuery(**query_kwargs)

    def test_get_simple(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=['run_query'])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection('dee')

        # Add a dummy response to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = '{}/sleep'.format(expected_prefix)
        data = {'snooze': 10}
        response_pb = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.get()
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ('dee', 'sleep'))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=None,
            options=client._call_options)

    def test_get_with_transaction(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=['run_query'])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Create a real-ish transaction for this client.
        transaction = client.transaction()
        txn_id = b'\x00\x00\x01-work-\xf2'
        transaction._id = txn_id

        # Make a **real** collection reference as parent.
        parent = client.collection('declaration')

        # Add a dummy response to the minimal fake GAPIC.
        parent_path, expected_prefix = parent._parent_info()
        name = '{}/burger'.format(expected_prefix)
        data = {'lettuce': b'\xee\x87'}
        response_pb = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.get(transaction=transaction)
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ('declaration', 'burger'))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=txn_id,
            options=client._call_options)

    def test_get_no_results(self):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['run_query'])
        empty_response = _make_query_response()
        run_query_response = iter([empty_response])
        firestore_api.run_query.return_value = run_query_response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection('dah', 'dah', 'dum')
        query = self._make_one(parent)

        get_response = query.get()
        self.assertIsInstance(get_response, types.GeneratorType)
        self.assertEqual(list(get_response), [])

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=None,
            options=client._call_options)

    def test_get_second_response_in_empty_stream(self):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['run_query'])
        empty_response1 = _make_query_response()
        empty_response2 = _make_query_response()
        run_query_response = iter([empty_response1, empty_response2])
        firestore_api.run_query.return_value = run_query_response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection('dah', 'dah', 'dum')
        query = self._make_one(parent)

        get_response = query.get()
        self.assertIsInstance(get_response, types.GeneratorType)
        with self.assertRaises(ValueError) as exc_info:
            list(get_response)

        exc_args = exc_info.exception.args
        self.assertEqual(len(exc_args), 3)
        self.assertIs(exc_args[2], empty_response2)
        self.assertIsNot(empty_response1, empty_response2)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=None,
            options=client._call_options)

    def test_get_with_skipped_results(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=['run_query'])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection('talk', 'and', 'chew-gum')

        # Add two dummy responses to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        response_pb1 = _make_query_response(skipped_results=1)
        name = '{}/clock'.format(expected_prefix)
        data = {'noon': 12, 'nested': {'bird': 10.5}}
        response_pb2 = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter(
            [response_pb1, response_pb2])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.get()
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(
            snapshot.reference._path, ('talk', 'and', 'chew-gum', 'clock'))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=None,
            options=client._call_options)

    def test_get_empty_after_first_response(self):
        from google.cloud.firestore_v1beta1.query import _EMPTY_DOC_TEMPLATE

        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=['run_query'])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection('charles')

        # Add two dummy responses to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = '{}/bark'.format(expected_prefix)
        data = {'lee': 'hoop'}
        response_pb1 = _make_query_response(name=name, data=data)
        response_pb2 = _make_query_response()
        firestore_api.run_query.return_value = iter(
            [response_pb1, response_pb2])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.get()
        self.assertIsInstance(get_response, types.GeneratorType)
        with self.assertRaises(ValueError) as exc_info:
            list(get_response)

        exc_args = exc_info.exception.args
        self.assertEqual(len(exc_args), 1)
        msg = _EMPTY_DOC_TEMPLATE.format(1, response_pb2)
        self.assertEqual(exc_args[0], msg)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            parent_path, query._to_protobuf(), transaction=None,
            options=client._call_options)


class Test__enum_from_op_string(unittest.TestCase):

    @staticmethod
    def _call_fut(op_string):
        from google.cloud.firestore_v1beta1.query import _enum_from_op_string

        return _enum_from_op_string(op_string)

    def test_success(self):
        from google.cloud.firestore_v1beta1.gapic import enums

        op_class = enums.StructuredQuery.FieldFilter.Operator
        self.assertEqual(self._call_fut('<'), op_class.LESS_THAN)
        self.assertEqual(self._call_fut('<='), op_class.LESS_THAN_OR_EQUAL)
        self.assertEqual(self._call_fut('=='), op_class.EQUAL)
        self.assertEqual(self._call_fut('>='), op_class.GREATER_THAN_OR_EQUAL)
        self.assertEqual(self._call_fut('>'), op_class.GREATER_THAN)

    def test_failure(self):
        with self.assertRaises(ValueError):
            self._call_fut('?')


class Test__isnan(unittest.TestCase):

    @staticmethod
    def _call_fut(value):
        from google.cloud.firestore_v1beta1.query import _isnan

        return _isnan(value)

    def test_valid(self):
        self.assertTrue(self._call_fut(float('nan')))

    def test_invalid(self):
        self.assertFalse(self._call_fut(51.5))
        self.assertFalse(self._call_fut(None))
        self.assertFalse(self._call_fut('str'))
        self.assertFalse(self._call_fut(int))
        self.assertFalse(self._call_fut(1.0 + 1.0j))


class Test__enum_from_direction(unittest.TestCase):

    @staticmethod
    def _call_fut(direction):
        from google.cloud.firestore_v1beta1.query import _enum_from_direction

        return _enum_from_direction(direction)

    def test_success(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.query import Query

        dir_class = enums.StructuredQuery.Direction
        self.assertEqual(
            self._call_fut(Query.ASCENDING), dir_class.ASCENDING)
        self.assertEqual(
            self._call_fut(Query.DESCENDING), dir_class.DESCENDING)

    def test_failure(self):
        with self.assertRaises(ValueError):
            self._call_fut('neither-ASCENDING-nor-DESCENDING')


class Test__filter_pb(unittest.TestCase):

    @staticmethod
    def _call_fut(field_or_unary):
        from google.cloud.firestore_v1beta1.query import _filter_pb

        return _filter_pb(field_or_unary)

    def test_unary(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import query_pb2

        unary_pb = query_pb2.StructuredQuery.UnaryFilter(
            field=query_pb2.StructuredQuery.FieldReference(
                field_path='a.b.c',
            ),
            op=enums.StructuredQuery.UnaryFilter.Operator.IS_NULL,
        )
        filter_pb = self._call_fut(unary_pb)
        expected_pb = query_pb2.StructuredQuery.Filter(
            unary_filter=unary_pb)
        self.assertEqual(filter_pb, expected_pb)

    def test_field(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import query_pb2

        field_filter_pb = query_pb2.StructuredQuery.FieldFilter(
            field=query_pb2.StructuredQuery.FieldReference(
                field_path='XYZ',
            ),
            op=enums.StructuredQuery.FieldFilter.Operator.GREATER_THAN,
            value=document_pb2.Value(double_value=90.75),
        )
        filter_pb = self._call_fut(field_filter_pb)
        expected_pb = query_pb2.StructuredQuery.Filter(
            field_filter=field_filter_pb)
        self.assertEqual(filter_pb, expected_pb)

    def test_bad_type(self):
        with self.assertRaises(ValueError):
            self._call_fut(None)


class Test__cursor_pb(unittest.TestCase):

    @staticmethod
    def _call_fut(cursor_pair, orders):
        from google.cloud.firestore_v1beta1.query import _cursor_pb

        return _cursor_pb(cursor_pair, orders)

    def test_no_pair(self):
        ret_val = self._call_fut(None, ())
        self.assertIsNone(ret_val)

    def test_no_orders(self):
        from google.cloud.firestore_v1beta1.query import _NO_ORDERS_FOR_CURSOR

        cursor_pair = {'a': 'b'}, True
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(cursor_pair, ())

        self.assertEqual(exc_info.exception.args, (_NO_ORDERS_FOR_CURSOR,))

    def test_missing_data(self):
        from google.cloud.firestore_v1beta1.gapic import enums

        order_pb = _make_order_pb(
            'a.b', enums.StructuredQuery.Direction.ASCENDING)
        orders = (order_pb,)
        data = {}
        cursor_pair = data, False

        with self.assertRaises(ValueError):
            self._call_fut(cursor_pair, orders)

    def test_success(self):
        from google.cloud.firestore_v1beta1.gapic import enums
        from google.cloud.firestore_v1beta1.proto import query_pb2
        from google.cloud.firestore_v1beta1 import _helpers

        field_path1 = 'a'
        field_path2 = 'a.b'
        field_path3 = 'x'
        direction1 = enums.StructuredQuery.Direction.DESCENDING
        direction2 = enums.StructuredQuery.Direction.ASCENDING
        direction3 = enums.StructuredQuery.Direction.ASCENDING
        orders = (
            _make_order_pb(field_path1, direction1),
            _make_order_pb(field_path2, direction2),
            _make_order_pb(field_path3, direction3),
        )
        data = {
            'a': {
                'b': 10,
                'c': 1.5,
            },
            'x': True,
        }
        cursor_pair = data, True

        cursor_pb = self._call_fut(cursor_pair, orders)
        expected_pb = query_pb2.Cursor(
            values=[
                _helpers.encode_value(data['a']),
                _helpers.encode_value(data['a']['b']),
                _helpers.encode_value(data['x']),
            ],
            before=True,
        )
        self.assertEqual(cursor_pb, expected_pb)


class Test__query_response_to_snapshot(unittest.TestCase):

    @staticmethod
    def _call_fut(response_pb, collection, expected_prefix):
        from google.cloud.firestore_v1beta1.query import _query_response_to_snapshot

        return _query_response_to_snapshot(
            response_pb, collection, expected_prefix)

    def test_empty(self):
        response_pb = _make_query_response()
        snapshot, skipped_results = self._call_fut(response_pb, None, None)
        self.assertIsNone(snapshot)
        self.assertEqual(skipped_results, 0)

    def test_after_offset(self):
        skipped_results = 410
        response_pb = _make_query_response(skipped_results=skipped_results)
        snapshot, skipped_results = self._call_fut(response_pb, None, None)
        self.assertIsNone(snapshot)
        self.assertEqual(skipped_results, skipped_results)

    def test_response(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        client = _make_client()
        collection = client.collection('a', 'b', 'c')
        _, expected_prefix = collection._parent_info()

        # Create name for the protobuf.
        doc_id = 'gigantic'
        name = '{}/{}'.format(expected_prefix, doc_id)
        data = {'a': 901, 'b': True}
        response_pb = _make_query_response(name=name, data=data)

        snapshot, skipped_results = self._call_fut(
            response_pb, collection, expected_prefix)
        self.assertEqual(skipped_results, 0)
        self.assertIsInstance(snapshot, DocumentSnapshot)
        expected_path = collection._path + (doc_id,)
        self.assertEqual(snapshot.reference._path, expected_path)
        self.assertEqual(snapshot.to_dict(), data)
        self.assertTrue(snapshot.exists)
        self.assertEqual(snapshot.read_time, response_pb.read_time)
        self.assertEqual(
            snapshot.create_time, response_pb.document.create_time)
        self.assertEqual(
            snapshot.update_time, response_pb.document.update_time)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project='project-project'):
    from google.cloud.firestore_v1beta1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)


def _make_order_pb(field_path, direction):
    from google.cloud.firestore_v1beta1.proto import query_pb2

    return query_pb2.StructuredQuery.Order(
        field=query_pb2.StructuredQuery.FieldReference(
            field_path=field_path,
        ),
        direction=direction,
    )


def _make_query_response(**kwargs):
    # kwargs supported are ``skipped_results``, ``name`` and ``data``
    from google.cloud.firestore_v1beta1.proto import document_pb2
    from google.cloud.firestore_v1beta1.proto import firestore_pb2
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.firestore_v1beta1 import _helpers

    now = datetime.datetime.utcnow()
    read_time = _datetime_to_pb_timestamp(now)
    kwargs['read_time'] = read_time

    name = kwargs.pop('name', None)
    data = kwargs.pop('data', None)
    if name is not None and data is not None:
        document_pb = document_pb2.Document(
            name=name,
            fields=_helpers.encode_dict(data),
        )
        delta = datetime.timedelta(seconds=100)
        update_time = _datetime_to_pb_timestamp(now - delta)
        create_time = _datetime_to_pb_timestamp(now - 2 * delta)
        document_pb.update_time.CopyFrom(update_time)
        document_pb.create_time.CopyFrom(create_time)

        kwargs['document'] = document_pb

    return firestore_pb2.RunQueryResponse(**kwargs)
