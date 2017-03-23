# Copyright 2016 Google Inc. All rights reserved.
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


import unittest


class TestStreamedResultSet(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.spanner.streamed import StreamedResultSet

        return StreamedResultSet

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        self.assertIs(streamed._response_iterator, iterator)
        self.assertEqual(streamed.rows, [])
        self.assertIsNone(streamed.metadata)
        self.assertIsNone(streamed.stats)
        self.assertIsNone(streamed.resume_token)

    def test_fields_unset(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        with self.assertRaises(AttributeError):
            _ = streamed.fields

    @staticmethod
    def _makeScalarField(name, type_):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType
        from google.cloud.proto.spanner.v1.type_pb2 import Type

        return StructType.Field(name=name, type=Type(code=type_))

    @staticmethod
    def _makeArrayField(name, element_type_code=None, element_type=None):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType
        from google.cloud.proto.spanner.v1.type_pb2 import Type

        if element_type is None:
            element_type = Type(code=element_type_code)
        array_type = Type(
            code='ARRAY', array_element_type=element_type)
        return StructType.Field(name=name, type=array_type)

    @staticmethod
    def _makeStructType(struct_type_fields):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType
        from google.cloud.proto.spanner.v1.type_pb2 import Type

        fields = [
            StructType.Field(name=key, type=Type(code=value))
            for key, value in struct_type_fields
        ]
        struct_type = StructType(fields=fields)
        return Type(code='STRUCT', struct_type=struct_type)

    @staticmethod
    def _makeValue(value):
        from google.cloud.spanner._helpers import _make_value_pb

        return _make_value_pb(value)

    @staticmethod
    def _makeListValue(values=(), value_pbs=None):
        from google.protobuf.struct_pb2 import ListValue
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner._helpers import _make_list_value_pb

        if value_pbs is not None:
            return Value(list_value=ListValue(values=value_pbs))
        return Value(list_value=_make_list_value_pb(values))

    def test_properties_set(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
        ]
        metadata = streamed._metadata = _ResultSetMetadataPB(FIELDS)
        stats = streamed._stats = _ResultSetStatsPB()
        self.assertEqual(list(streamed.fields), FIELDS)
        self.assertIs(streamed.metadata, metadata)
        self.assertIs(streamed.stats, stats)

    def test__merge_chunk_bool(self):
        from google.cloud.spanner.streamed import Unmergeable

        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('registered_voter', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(True)
        chunk = self._makeValue(False)

        with self.assertRaises(Unmergeable):
            streamed._merge_chunk(chunk)

    def test__merge_chunk_int64(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('age', 'INT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(42)
        chunk = self._makeValue(13)

        merged = streamed._merge_chunk(chunk)
        self.assertEqual(merged.string_value, '4213')
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_float64_nan_string(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('weight', 'FLOAT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(u'Na')
        chunk = self._makeValue(u'N')

        merged = streamed._merge_chunk(chunk)
        self.assertEqual(merged.string_value, u'NaN')

    def test__merge_chunk_float64_w_empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('weight', 'FLOAT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(3.14159)
        chunk = self._makeValue('')

        merged = streamed._merge_chunk(chunk)
        self.assertEqual(merged.number_value, 3.14159)

    def test__merge_chunk_float64_w_float64(self):
        from google.cloud.spanner.streamed import Unmergeable

        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('weight', 'FLOAT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(3.14159)
        chunk = self._makeValue(2.71828)

        with self.assertRaises(Unmergeable):
            streamed._merge_chunk(chunk)

    def test__merge_chunk_string(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('name', 'STRING'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(u'phred')
        chunk = self._makeValue(u'wylma')

        merged = streamed._merge_chunk(chunk)

        self.assertEqual(merged.string_value, u'phredwylma')
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_bool(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeArrayField('name', element_type_code='BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue([True, True])
        chunk = self._makeListValue([False, False, False])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue([True, True, False, False, False])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_int(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeArrayField('name', element_type_code='INT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue([0, 1, 2])
        chunk = self._makeListValue([3, 4, 5])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue([0, 1, 23, 4, 5])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_float(self):
        import math

        PI = math.pi
        EULER = math.e
        SQRT_2 = math.sqrt(2.0)
        LOG_10 = math.log(10)
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeArrayField('name', element_type_code='FLOAT64'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue([PI, SQRT_2])
        chunk = self._makeListValue(['', EULER, LOG_10])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue([PI, SQRT_2, EULER, LOG_10])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_string(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeArrayField('name', element_type_code='STRING'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue([u'A', u'B', u'C'])
        chunk = self._makeListValue([None, u'D', u'E'])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue([u'A', u'B', u'C', None, u'D', u'E'])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_string_with_null(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeArrayField('name', element_type_code='STRING'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue([u'A', u'B', u'C'])
        chunk = self._makeListValue([u'D', u'E'])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue([u'A', u'B', u'CD', u'E'])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_array_of_int(self):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType
        from google.cloud.proto.spanner.v1.type_pb2 import Type

        subarray_type = Type(
            code='ARRAY', array_element_type=Type(code='INT64'))
        array_type = Type(code='ARRAY', array_element_type=subarray_type)
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            StructType.Field(name='loloi', type=array_type)
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue(value_pbs=[
            self._makeListValue([0, 1]),
            self._makeListValue([2]),
        ])
        chunk = self._makeListValue(value_pbs=[
            self._makeListValue([3]),
            self._makeListValue([4, 5]),
        ])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue(value_pbs=[
            self._makeListValue([0, 1]),
            self._makeListValue([23]),
            self._makeListValue([4, 5]),
        ])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_array_of_string(self):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType
        from google.cloud.proto.spanner.v1.type_pb2 import Type

        subarray_type = Type(
            code='ARRAY', array_element_type=Type(code='STRING'))
        array_type = Type(code='ARRAY', array_element_type=subarray_type)
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            StructType.Field(name='lolos', type=array_type)
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeListValue(value_pbs=[
            self._makeListValue([u'A', u'B']),
            self._makeListValue([u'C']),
        ])
        chunk = self._makeListValue(value_pbs=[
            self._makeListValue([u'D']),
            self._makeListValue([u'E', u'F']),
        ])

        merged = streamed._merge_chunk(chunk)

        expected = self._makeListValue(value_pbs=[
            self._makeListValue([u'A', u'B']),
            self._makeListValue([u'CD']),
            self._makeListValue([u'E', u'F']),
        ])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_struct(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        struct_type = self._makeStructType([
            ('name', 'STRING'),
            ('age', 'INT64'),
        ])
        FIELDS = [
            self._makeArrayField('test', element_type=struct_type),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        partial = self._makeListValue([u'Phred '])
        streamed._pending_chunk = self._makeListValue(value_pbs=[partial])
        rest = self._makeListValue([u'Phlyntstone', 31])
        chunk = self._makeListValue(value_pbs=[rest])

        merged = streamed._merge_chunk(chunk)

        struct = self._makeListValue([u'Phred Phlyntstone', 31])
        expected = self._makeListValue(value_pbs=[struct])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test__merge_chunk_array_of_struct_unmergeable(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        struct_type = self._makeStructType([
            ('name', 'STRING'),
            ('registered', 'BOOL'),
            ('voted', 'BOOL'),
        ])
        FIELDS = [
            self._makeArrayField('test', element_type=struct_type),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        partial = self._makeListValue([u'Phred Phlyntstone', True])
        streamed._pending_chunk = self._makeListValue(value_pbs=[partial])
        rest = self._makeListValue([True])
        chunk = self._makeListValue(value_pbs=[rest])

        merged = streamed._merge_chunk(chunk)

        struct = self._makeListValue([u'Phred Phlyntstone', True, True])
        expected = self._makeListValue(value_pbs=[struct])
        self.assertEqual(merged, expected)
        self.assertIsNone(streamed._pending_chunk)

    def test_merge_values_empty_and_empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._current_row = []
        streamed._merge_values([])
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, [])

    def test_merge_values_empty_and_partial(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [u'Phred Phlyntstone', 42]
        VALUES = [self._makeValue(bare) for bare in BARE]
        streamed._current_row = []
        streamed._merge_values(VALUES)
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BARE)

    def test_merge_values_empty_and_filled(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [u'Phred Phlyntstone', 42, True]
        VALUES = [self._makeValue(bare) for bare in BARE]
        streamed._current_row = []
        streamed._merge_values(VALUES)
        self.assertEqual(streamed.rows, [BARE])
        self.assertEqual(streamed._current_row, [])

    def test_merge_values_empty_and_filled_plus(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [
            u'Phred Phlyntstone', 42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone',
        ]
        VALUES = [self._makeValue(bare) for bare in BARE]
        streamed._current_row = []
        streamed._merge_values(VALUES)
        self.assertEqual(streamed.rows, [BARE[0:3], BARE[3:6]])
        self.assertEqual(streamed._current_row, BARE[6:])

    def test_merge_values_partial_and_empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BEFORE = [
            u'Phred Phlyntstone'
        ]
        streamed._current_row[:] = BEFORE
        streamed._merge_values([])
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BEFORE)

    def test_merge_values_partial_and_partial(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BEFORE = [u'Phred Phlyntstone']
        streamed._current_row[:] = BEFORE
        MERGED = [42]
        TO_MERGE = [self._makeValue(item) for item in MERGED]
        streamed._merge_values(TO_MERGE)
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BEFORE + MERGED)

    def test_merge_values_partial_and_filled(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BEFORE = [
            u'Phred Phlyntstone'
        ]
        streamed._current_row[:] = BEFORE
        MERGED = [42, True]
        TO_MERGE = [self._makeValue(item) for item in MERGED]
        streamed._merge_values(TO_MERGE)
        self.assertEqual(streamed.rows, [BEFORE + MERGED])
        self.assertEqual(streamed._current_row, [])

    def test_merge_values_partial_and_filled_plus(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        BEFORE = [
            self._makeValue(u'Phred Phlyntstone')
        ]
        streamed._current_row[:] = BEFORE
        MERGED = [
            42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone',
        ]
        TO_MERGE = [self._makeValue(item) for item in MERGED]
        VALUES = BEFORE + MERGED
        streamed._merge_values(TO_MERGE)
        self.assertEqual(streamed.rows, [VALUES[0:3], VALUES[3:6]])
        self.assertEqual(streamed._current_row, VALUES[6:])

    def test_consume_next_empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        with self.assertRaises(StopIteration):
            streamed.consume_next()

    def test_consume_next_first_set_partial(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [u'Phred Phlyntstone', 42]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set = _PartialResultSetPB(VALUES, metadata=metadata)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        streamed.consume_next()
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BARE)
        self.assertTrue(streamed.metadata is metadata)
        self.assertEqual(streamed.resume_token, result_set.resume_token)

    def test_consume_next_w_partial_result(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        VALUES = [
            self._makeValue(u'Phred '),
        ]
        result_set = _PartialResultSetPB(VALUES, chunked_value=True)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed.consume_next()
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, [])
        self.assertEqual(streamed._pending_chunk, VALUES[0])
        self.assertEqual(streamed.resume_token, result_set.resume_token)

    def test_consume_next_w_pending_chunk(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        BARE = [
            u'Phlyntstone', 42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone',
        ]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set = _PartialResultSetPB(VALUES)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        streamed._metadata = _ResultSetMetadataPB(FIELDS)
        streamed._pending_chunk = self._makeValue(u'Phred ')
        streamed.consume_next()
        self.assertEqual(streamed.rows, [
            [u'Phred Phlyntstone', BARE[1], BARE[2]],
            [BARE[3], BARE[4], BARE[5]],
        ])
        self.assertEqual(streamed._current_row, [BARE[6]])
        self.assertIsNone(streamed._pending_chunk)
        self.assertEqual(streamed.resume_token, result_set.resume_token)

    def test_consume_next_last_set(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        stats = _ResultSetStatsPB(
            rows_returned="1",
            elapsed_time="1.23 secs",
            cpu_tme="0.98 secs",
        )
        BARE = [u'Phred Phlyntstone', 42, True]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set = _PartialResultSetPB(VALUES, stats=stats)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        streamed._metadata = metadata
        streamed.consume_next()
        self.assertEqual(streamed.rows, [BARE])
        self.assertEqual(streamed._current_row, [])
        self.assertTrue(streamed._stats is stats)
        self.assertEqual(streamed.resume_token, result_set.resume_token)

    def test_consume_all_empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        streamed.consume_all()

    def test_consume_all_one_result_set_partial(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [u'Phred Phlyntstone', 42]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set = _PartialResultSetPB(VALUES, metadata=metadata)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        streamed.consume_all()
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BARE)
        self.assertTrue(streamed.metadata is metadata)

    def test_consume_all_multiple_result_sets_filled(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [
            u'Phred Phlyntstone', 42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone', 41, True,
        ]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set1 = _PartialResultSetPB(VALUES[:4], metadata=metadata)
        result_set2 = _PartialResultSetPB(VALUES[4:])
        iterator = _MockCancellableIterator(result_set1, result_set2)
        streamed = self._make_one(iterator)
        streamed.consume_all()
        self.assertEqual(streamed.rows, [
            [BARE[0], BARE[1], BARE[2]],
            [BARE[3], BARE[4], BARE[5]],
            [BARE[6], BARE[7], BARE[8]],
        ])
        self.assertEqual(streamed._current_row, [])
        self.assertIsNone(streamed._pending_chunk)

    def test___iter___empty(self):
        iterator = _MockCancellableIterator()
        streamed = self._make_one(iterator)
        found = list(streamed)
        self.assertEqual(found, [])

    def test___iter___one_result_set_partial(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [u'Phred Phlyntstone', 42]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set = _PartialResultSetPB(VALUES, metadata=metadata)
        iterator = _MockCancellableIterator(result_set)
        streamed = self._make_one(iterator)
        found = list(streamed)
        self.assertEqual(found, [])
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, BARE)
        self.assertTrue(streamed.metadata is metadata)

    def test___iter___multiple_result_sets_filled(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        BARE = [
            u'Phred Phlyntstone', 42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone', 41, True,
        ]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set1 = _PartialResultSetPB(VALUES[:4], metadata=metadata)
        result_set2 = _PartialResultSetPB(VALUES[4:])
        iterator = _MockCancellableIterator(result_set1, result_set2)
        streamed = self._make_one(iterator)
        found = list(streamed)
        self.assertEqual(found, [
            [BARE[0], BARE[1], BARE[2]],
            [BARE[3], BARE[4], BARE[5]],
            [BARE[6], BARE[7], BARE[8]],
        ])
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, [])
        self.assertIsNone(streamed._pending_chunk)

    def test___iter___w_existing_rows_read(self):
        FIELDS = [
            self._makeScalarField('full_name', 'STRING'),
            self._makeScalarField('age', 'INT64'),
            self._makeScalarField('married', 'BOOL'),
        ]
        metadata = _ResultSetMetadataPB(FIELDS)
        ALREADY = [
            [u'Pebbylz Phlyntstone', 4, False],
            [u'Dino Rhubble', 4, False],
        ]
        BARE = [
            u'Phred Phlyntstone', 42, True,
            u'Bharney Rhubble', 39, True,
            u'Wylma Phlyntstone', 41, True,
        ]
        VALUES = [self._makeValue(bare) for bare in BARE]
        result_set1 = _PartialResultSetPB(VALUES[:4], metadata=metadata)
        result_set2 = _PartialResultSetPB(VALUES[4:])
        iterator = _MockCancellableIterator(result_set1, result_set2)
        streamed = self._make_one(iterator)
        streamed._rows[:] = ALREADY
        found = list(streamed)
        self.assertEqual(found, ALREADY + [
            [BARE[0], BARE[1], BARE[2]],
            [BARE[3], BARE[4], BARE[5]],
            [BARE[6], BARE[7], BARE[8]],
        ])
        self.assertEqual(streamed.rows, [])
        self.assertEqual(streamed._current_row, [])
        self.assertIsNone(streamed._pending_chunk)


class _MockCancellableIterator(object):

    cancel_calls = 0

    def __init__(self, *values):
        self.iter_values = iter(values)

    def next(self):
        return next(self.iter_values)

    def __next__(self):  # pragma: NO COVER Py3k
        return self.next()


class _ResultSetMetadataPB(object):

    def __init__(self, fields):
        from google.cloud.proto.spanner.v1.type_pb2 import StructType

        self.row_type = StructType(fields=fields)


class _ResultSetStatsPB(object):

    def __init__(self, query_plan=None, **query_stats):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner._helpers import _make_value_pb

        self.query_plan = query_plan
        self.query_stats = Struct(fields={
            key: _make_value_pb(value) for key, value in query_stats.items()})


class _PartialResultSetPB(object):

    resume_token = b'DEADBEEF'

    def __init__(self, values, metadata=None, stats=None, chunked_value=False):
        self.values = values
        self.metadata = metadata
        self.stats = stats
        self.chunked_value = chunked_value

    def HasField(self, name):
        assert name == 'stats'
        return self.stats is not None


class TestStreamedResultSet_JSON_acceptance_tests(unittest.TestCase):

    _json_tests = None

    def _getTargetClass(self):
        from google.cloud.spanner.streamed import StreamedResultSet

        return StreamedResultSet

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _load_json_test(self, test_name):
        import os

        if self.__class__._json_tests is None:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(
                dirname, 'streaming-read-acceptance-test.json')
            raw = _parse_streaming_read_acceptance_tests(filename)
            tests = self.__class__._json_tests = {}
            for (name, partial_result_sets, results) in raw:
                tests[name] = partial_result_sets, results
        return self.__class__._json_tests[test_name]

    # Non-error cases

    def _match_results(self, testcase_name, assert_equality=None):
        partial_result_sets, expected = self._load_json_test(testcase_name)
        iterator = _MockCancellableIterator(*partial_result_sets)
        partial = self._make_one(iterator)
        partial.consume_all()
        if assert_equality is not None:
            assert_equality(partial.rows, expected)
        else:
            self.assertEqual(partial.rows, expected)

    def test_basic(self):
        self._match_results('Basic Test')

    def test_string_chunking(self):
        self._match_results('String Chunking Test')

    def test_string_array_chunking(self):
        self._match_results('String Array Chunking Test')

    def test_string_array_chunking_with_nulls(self):
        self._match_results('String Array Chunking Test With Nulls')

    def test_string_array_chunking_with_empty_strings(self):
        self._match_results('String Array Chunking Test With Empty Strings')

    def test_string_array_chunking_with_one_large_string(self):
        self._match_results('String Array Chunking Test With One Large String')

    def test_int64_array_chunking(self):
        self._match_results('INT64 Array Chunking Test')

    def test_float64_array_chunking(self):
        import math

        def assert_float_equality(lhs, rhs):
            # NaN, +Inf, and -Inf can't be tested for equality
            if lhs is None:
                self.assertIsNone(rhs)
            elif math.isnan(lhs):
                self.assertTrue(math.isnan(rhs))
            elif math.isinf(lhs):
                self.assertTrue(math.isinf(rhs))
                # but +Inf and -Inf can be tested for magnitude
                self.assertTrue((lhs > 0) == (rhs > 0))
            else:
                self.assertEqual(lhs, rhs)

        def assert_rows_equality(lhs, rhs):
            self.assertEqual(len(lhs), len(rhs))
            for l_rows, r_rows in zip(lhs, rhs):
                self.assertEqual(len(l_rows), len(r_rows))
                for l_row, r_row in zip(l_rows, r_rows):
                    self.assertEqual(len(l_row), len(r_row))
                    for l_cell, r_cell in zip(l_row, r_row):
                        assert_float_equality(l_cell, r_cell)

        self._match_results(
            'FLOAT64 Array Chunking Test', assert_rows_equality)

    def test_struct_array_chunking(self):
        self._match_results('Struct Array Chunking Test')

    def test_nested_struct_array(self):
        self._match_results('Nested Struct Array Test')

    def test_nested_struct_array_chunking(self):
        self._match_results('Nested Struct Array Chunking Test')

    def test_struct_array_and_string_chunking(self):
        self._match_results('Struct Array And String Chunking Test')

    def test_multiple_row_single_chunk(self):
        self._match_results('Multiple Row Single Chunk')

    def test_multiple_row_multiple_chunks(self):
        self._match_results('Multiple Row Multiple Chunks')

    def test_multiple_row_chunks_non_chunks_interleaved(self):
        self._match_results('Multiple Row Chunks/Non Chunks Interleaved')


def _generate_partial_result_sets(prs_text_pbs):
    from google.protobuf.json_format import Parse
    from google.cloud.proto.spanner.v1.result_set_pb2 import PartialResultSet

    partial_result_sets = []

    for prs_text_pb in prs_text_pbs:
        prs = PartialResultSet()
        partial_result_sets.append(Parse(prs_text_pb, prs))

    return partial_result_sets


def _normalize_int_array(cell):
    normalized = []
    for subcell in cell:
        if subcell is not None:
            subcell = int(subcell)
        normalized.append(subcell)
    return normalized


def _normalize_float(cell):
    if cell == u'Infinity':
        return float('inf')
    if cell == u'-Infinity':
        return float('-inf')
    if cell == u'NaN':
        return float('nan')
    if cell is not None:
        return float(cell)


def _normalize_results(rows_data, fields):
    """Helper for _parse_streaming_read_acceptance_tests"""
    from google.cloud.proto.spanner.v1 import type_pb2

    normalized = []
    for row_data in rows_data:
        row = []
        assert len(row_data) == len(fields)
        for cell, field in zip(row_data, fields):
            if field.type.code == type_pb2.INT64:
                cell = int(cell)
            if field.type.code == type_pb2.FLOAT64:
                cell = _normalize_float(cell)
            elif field.type.code == type_pb2.BYTES:
                cell = cell.encode('utf8')
            elif field.type.code == type_pb2.ARRAY:
                if field.type.array_element_type.code == type_pb2.INT64:
                    cell = _normalize_int_array(cell)
                elif field.type.array_element_type.code == type_pb2.FLOAT64:
                    cell = [_normalize_float(subcell) for subcell in cell]
            row.append(cell)
        normalized.append(row)
    return normalized


def _parse_streaming_read_acceptance_tests(filename):
    """Parse acceptance tests from JSON

    See: streaming-read-acceptance-test.json
    """
    import json

    with open(filename) as json_file:
        test_json = json.load(json_file)

    for test in test_json['tests']:
        name = test['name']
        partial_result_sets = _generate_partial_result_sets(test['chunks'])
        fields = partial_result_sets[0].metadata.row_type.fields
        result = _normalize_results(test['result']['value'], fields)
        yield name, partial_result_sets, result
