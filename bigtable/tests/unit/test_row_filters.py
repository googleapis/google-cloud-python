# Copyright 2016 Google Inc.
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


class Test_BoolFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import _BoolFilter

        return _BoolFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        flag = object()
        row_filter = self._make_one(flag)
        self.assertIs(row_filter.flag, flag)

    def test___eq__type_differ(self):
        flag = object()
        row_filter1 = self._make_one(flag)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        flag = object()
        row_filter1 = self._make_one(flag)
        row_filter2 = self._make_one(flag)
        self.assertEqual(row_filter1, row_filter2)

    def test___ne__same_value(self):
        flag = object()
        row_filter1 = self._make_one(flag)
        row_filter2 = self._make_one(flag)
        comparison_val = (row_filter1 != row_filter2)
        self.assertFalse(comparison_val)


class TestSinkFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import SinkFilter

        return SinkFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        flag = True
        row_filter = self._make_one(flag)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(sink=flag)
        self.assertEqual(pb_val, expected_pb)


class TestPassAllFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import PassAllFilter

        return PassAllFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        flag = True
        row_filter = self._make_one(flag)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(pass_all_filter=flag)
        self.assertEqual(pb_val, expected_pb)


class TestBlockAllFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import BlockAllFilter

        return BlockAllFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        flag = True
        row_filter = self._make_one(flag)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(block_all_filter=flag)
        self.assertEqual(pb_val, expected_pb)


class Test_RegexFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import _RegexFilter

        return _RegexFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        regex = b'abc'
        row_filter = self._make_one(regex)
        self.assertIs(row_filter.regex, regex)

    def test_constructor_non_bytes(self):
        regex = u'abc'
        row_filter = self._make_one(regex)
        self.assertEqual(row_filter.regex, b'abc')

    def test___eq__type_differ(self):
        regex = b'def-rgx'
        row_filter1 = self._make_one(regex)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        regex = b'trex-regex'
        row_filter1 = self._make_one(regex)
        row_filter2 = self._make_one(regex)
        self.assertEqual(row_filter1, row_filter2)

    def test___ne__same_value(self):
        regex = b'abc'
        row_filter1 = self._make_one(regex)
        row_filter2 = self._make_one(regex)
        comparison_val = (row_filter1 != row_filter2)
        self.assertFalse(comparison_val)


class TestRowKeyRegexFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import RowKeyRegexFilter

        return RowKeyRegexFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        regex = b'row-key-regex'
        row_filter = self._make_one(regex)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(row_key_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)


class TestRowSampleFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import RowSampleFilter

        return RowSampleFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        sample = object()
        row_filter = self._make_one(sample)
        self.assertIs(row_filter.sample, sample)

    def test___eq__type_differ(self):
        sample = object()
        row_filter1 = self._make_one(sample)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        sample = object()
        row_filter1 = self._make_one(sample)
        row_filter2 = self._make_one(sample)
        self.assertEqual(row_filter1, row_filter2)

    def test_to_pb(self):
        sample = 0.25
        row_filter = self._make_one(sample)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(row_sample_filter=sample)
        self.assertEqual(pb_val, expected_pb)


class TestFamilyNameRegexFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import FamilyNameRegexFilter

        return FamilyNameRegexFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        regex = u'family-regex'
        row_filter = self._make_one(regex)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(family_name_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)


class TestColumnQualifierRegexFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import (
            ColumnQualifierRegexFilter)

        return ColumnQualifierRegexFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        regex = b'column-regex'
        row_filter = self._make_one(regex)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(
            column_qualifier_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)


class TestTimestampRange(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import TimestampRange

        return TimestampRange

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        start = object()
        end = object()
        time_range = self._make_one(start=start, end=end)
        self.assertIs(time_range.start, start)
        self.assertIs(time_range.end, end)

    def test___eq__(self):
        start = object()
        end = object()
        time_range1 = self._make_one(start=start, end=end)
        time_range2 = self._make_one(start=start, end=end)
        self.assertEqual(time_range1, time_range2)

    def test___eq__type_differ(self):
        start = object()
        end = object()
        time_range1 = self._make_one(start=start, end=end)
        time_range2 = object()
        self.assertNotEqual(time_range1, time_range2)

    def test___ne__same_value(self):
        start = object()
        end = object()
        time_range1 = self._make_one(start=start, end=end)
        time_range2 = self._make_one(start=start, end=end)
        comparison_val = (time_range1 != time_range2)
        self.assertFalse(comparison_val)

    def _to_pb_helper(self, start_micros=None, end_micros=None):
        import datetime
        from google.cloud._helpers import _EPOCH

        pb_kwargs = {}

        start = None
        if start_micros is not None:
            start = _EPOCH + datetime.timedelta(microseconds=start_micros)
            pb_kwargs['start_timestamp_micros'] = start_micros
        end = None
        if end_micros is not None:
            end = _EPOCH + datetime.timedelta(microseconds=end_micros)
            pb_kwargs['end_timestamp_micros'] = end_micros
        time_range = self._make_one(start=start, end=end)

        expected_pb = _TimestampRangePB(**pb_kwargs)
        self.assertEqual(time_range.to_pb(), expected_pb)

    def test_to_pb(self):
        # Makes sure already milliseconds granularity
        start_micros = 30871000
        end_micros = 12939371000
        self._to_pb_helper(start_micros=start_micros,
                           end_micros=end_micros)

    def test_to_pb_start_only(self):
        # Makes sure already milliseconds granularity
        start_micros = 30871000
        self._to_pb_helper(start_micros=start_micros)

    def test_to_pb_end_only(self):
        # Makes sure already milliseconds granularity
        end_micros = 12939371000
        self._to_pb_helper(end_micros=end_micros)


class TestTimestampRangeFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import TimestampRangeFilter

        return TimestampRangeFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        range_ = object()
        row_filter = self._make_one(range_)
        self.assertIs(row_filter.range_, range_)

    def test___eq__type_differ(self):
        range_ = object()
        row_filter1 = self._make_one(range_)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        range_ = object()
        row_filter1 = self._make_one(range_)
        row_filter2 = self._make_one(range_)
        self.assertEqual(row_filter1, row_filter2)

    def test_to_pb(self):
        from google.cloud.bigtable.row_filters import TimestampRange

        range_ = TimestampRange()
        row_filter = self._make_one(range_)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(
            timestamp_range_filter=_TimestampRangePB())
        self.assertEqual(pb_val, expected_pb)


class TestColumnRangeFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import ColumnRangeFilter

        return ColumnRangeFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        column_family_id = object()
        row_filter = self._make_one(column_family_id)
        self.assertIs(row_filter.column_family_id, column_family_id)
        self.assertIsNone(row_filter.start_column)
        self.assertIsNone(row_filter.end_column)
        self.assertTrue(row_filter.inclusive_start)
        self.assertTrue(row_filter.inclusive_end)

    def test_constructor_explicit(self):
        column_family_id = object()
        start_column = object()
        end_column = object()
        inclusive_start = object()
        inclusive_end = object()
        row_filter = self._make_one(
            column_family_id,
            start_column=start_column,
            end_column=end_column,
            inclusive_start=inclusive_start,
            inclusive_end=inclusive_end)
        self.assertIs(row_filter.column_family_id, column_family_id)
        self.assertIs(row_filter.start_column, start_column)
        self.assertIs(row_filter.end_column, end_column)
        self.assertIs(row_filter.inclusive_start, inclusive_start)
        self.assertIs(row_filter.inclusive_end, inclusive_end)

    def test_constructor_bad_start(self):
        column_family_id = object()
        self.assertRaises(ValueError, self._make_one,
                          column_family_id, inclusive_start=True)

    def test_constructor_bad_end(self):
        column_family_id = object()
        self.assertRaises(ValueError, self._make_one,
                          column_family_id, inclusive_end=True)

    def test___eq__(self):
        column_family_id = object()
        start_column = object()
        end_column = object()
        inclusive_start = object()
        inclusive_end = object()
        row_filter1 = self._make_one(column_family_id,
                                     start_column=start_column,
                                     end_column=end_column,
                                     inclusive_start=inclusive_start,
                                     inclusive_end=inclusive_end)
        row_filter2 = self._make_one(column_family_id,
                                     start_column=start_column,
                                     end_column=end_column,
                                     inclusive_start=inclusive_start,
                                     inclusive_end=inclusive_end)
        self.assertEqual(row_filter1, row_filter2)

    def test___eq__type_differ(self):
        column_family_id = object()
        row_filter1 = self._make_one(column_family_id)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test_to_pb(self):
        column_family_id = u'column-family-id'
        row_filter = self._make_one(column_family_id)
        col_range_pb = _ColumnRangePB(family_name=column_family_id)
        expected_pb = _RowFilterPB(column_range_filter=col_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_inclusive_start(self):
        column_family_id = u'column-family-id'
        column = b'column'
        row_filter = self._make_one(column_family_id, start_column=column)
        col_range_pb = _ColumnRangePB(
            family_name=column_family_id,
            start_qualifier_closed=column,
        )
        expected_pb = _RowFilterPB(column_range_filter=col_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_exclusive_start(self):
        column_family_id = u'column-family-id'
        column = b'column'
        row_filter = self._make_one(column_family_id, start_column=column,
                                    inclusive_start=False)
        col_range_pb = _ColumnRangePB(
            family_name=column_family_id,
            start_qualifier_open=column,
        )
        expected_pb = _RowFilterPB(column_range_filter=col_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_inclusive_end(self):
        column_family_id = u'column-family-id'
        column = b'column'
        row_filter = self._make_one(column_family_id, end_column=column)
        col_range_pb = _ColumnRangePB(
            family_name=column_family_id,
            end_qualifier_closed=column,
        )
        expected_pb = _RowFilterPB(column_range_filter=col_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_exclusive_end(self):
        column_family_id = u'column-family-id'
        column = b'column'
        row_filter = self._make_one(column_family_id, end_column=column,
                                    inclusive_end=False)
        col_range_pb = _ColumnRangePB(
            family_name=column_family_id,
            end_qualifier_open=column,
        )
        expected_pb = _RowFilterPB(column_range_filter=col_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)


class TestValueRegexFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import ValueRegexFilter

        return ValueRegexFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        regex = b'value-regex'
        row_filter = self._make_one(regex)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(value_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)


class TestValueRangeFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import ValueRangeFilter

        return ValueRangeFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        row_filter = self._make_one()
        self.assertIsNone(row_filter.start_value)
        self.assertIsNone(row_filter.end_value)
        self.assertTrue(row_filter.inclusive_start)
        self.assertTrue(row_filter.inclusive_end)

    def test_constructor_explicit(self):
        start_value = object()
        end_value = object()
        inclusive_start = object()
        inclusive_end = object()
        row_filter = self._make_one(start_value=start_value,
                                    end_value=end_value,
                                    inclusive_start=inclusive_start,
                                    inclusive_end=inclusive_end)
        self.assertIs(row_filter.start_value, start_value)
        self.assertIs(row_filter.end_value, end_value)
        self.assertIs(row_filter.inclusive_start, inclusive_start)
        self.assertIs(row_filter.inclusive_end, inclusive_end)

    def test_constructor_bad_start(self):
        self.assertRaises(ValueError, self._make_one, inclusive_start=True)

    def test_constructor_bad_end(self):
        self.assertRaises(ValueError, self._make_one, inclusive_end=True)

    def test___eq__(self):
        start_value = object()
        end_value = object()
        inclusive_start = object()
        inclusive_end = object()
        row_filter1 = self._make_one(start_value=start_value,
                                     end_value=end_value,
                                     inclusive_start=inclusive_start,
                                     inclusive_end=inclusive_end)
        row_filter2 = self._make_one(start_value=start_value,
                                     end_value=end_value,
                                     inclusive_start=inclusive_start,
                                     inclusive_end=inclusive_end)
        self.assertEqual(row_filter1, row_filter2)

    def test___eq__type_differ(self):
        row_filter1 = self._make_one()
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test_to_pb(self):
        row_filter = self._make_one()
        expected_pb = _RowFilterPB(
            value_range_filter=_ValueRangePB())
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_inclusive_start(self):
        value = b'some-value'
        row_filter = self._make_one(start_value=value)
        val_range_pb = _ValueRangePB(start_value_closed=value)
        expected_pb = _RowFilterPB(value_range_filter=val_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_exclusive_start(self):
        value = b'some-value'
        row_filter = self._make_one(start_value=value, inclusive_start=False)
        val_range_pb = _ValueRangePB(start_value_open=value)
        expected_pb = _RowFilterPB(value_range_filter=val_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_inclusive_end(self):
        value = b'some-value'
        row_filter = self._make_one(end_value=value)
        val_range_pb = _ValueRangePB(end_value_closed=value)
        expected_pb = _RowFilterPB(value_range_filter=val_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)

    def test_to_pb_exclusive_end(self):
        value = b'some-value'
        row_filter = self._make_one(end_value=value, inclusive_end=False)
        val_range_pb = _ValueRangePB(end_value_open=value)
        expected_pb = _RowFilterPB(value_range_filter=val_range_pb)
        self.assertEqual(row_filter.to_pb(), expected_pb)


class Test_CellCountFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import _CellCountFilter

        return _CellCountFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        num_cells = object()
        row_filter = self._make_one(num_cells)
        self.assertIs(row_filter.num_cells, num_cells)

    def test___eq__type_differ(self):
        num_cells = object()
        row_filter1 = self._make_one(num_cells)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        num_cells = object()
        row_filter1 = self._make_one(num_cells)
        row_filter2 = self._make_one(num_cells)
        self.assertEqual(row_filter1, row_filter2)

    def test___ne__same_value(self):
        num_cells = object()
        row_filter1 = self._make_one(num_cells)
        row_filter2 = self._make_one(num_cells)
        comparison_val = (row_filter1 != row_filter2)
        self.assertFalse(comparison_val)


class TestCellsRowOffsetFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import CellsRowOffsetFilter

        return CellsRowOffsetFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        num_cells = 76
        row_filter = self._make_one(num_cells)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(
            cells_per_row_offset_filter=num_cells)
        self.assertEqual(pb_val, expected_pb)


class TestCellsRowLimitFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import CellsRowLimitFilter

        return CellsRowLimitFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        num_cells = 189
        row_filter = self._make_one(num_cells)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(
            cells_per_row_limit_filter=num_cells)
        self.assertEqual(pb_val, expected_pb)


class TestCellsColumnLimitFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import CellsColumnLimitFilter

        return CellsColumnLimitFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        num_cells = 10
        row_filter = self._make_one(num_cells)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(
            cells_per_column_limit_filter=num_cells)
        self.assertEqual(pb_val, expected_pb)


class TestStripValueTransformerFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        return StripValueTransformerFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        flag = True
        row_filter = self._make_one(flag)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(strip_value_transformer=flag)
        self.assertEqual(pb_val, expected_pb)


class TestApplyLabelFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import ApplyLabelFilter

        return ApplyLabelFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        label = object()
        row_filter = self._make_one(label)
        self.assertIs(row_filter.label, label)

    def test___eq__type_differ(self):
        label = object()
        row_filter1 = self._make_one(label)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        label = object()
        row_filter1 = self._make_one(label)
        row_filter2 = self._make_one(label)
        self.assertEqual(row_filter1, row_filter2)

    def test_to_pb(self):
        label = u'label'
        row_filter = self._make_one(label)
        pb_val = row_filter.to_pb()
        expected_pb = _RowFilterPB(apply_label_transformer=label)
        self.assertEqual(pb_val, expected_pb)


class Test_FilterCombination(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import _FilterCombination

        return _FilterCombination

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        row_filter = self._make_one()
        self.assertEqual(row_filter.filters, [])

    def test_constructor_explicit(self):
        filters = object()
        row_filter = self._make_one(filters=filters)
        self.assertIs(row_filter.filters, filters)

    def test___eq__(self):
        filters = object()
        row_filter1 = self._make_one(filters=filters)
        row_filter2 = self._make_one(filters=filters)
        self.assertEqual(row_filter1, row_filter2)

    def test___eq__type_differ(self):
        filters = object()
        row_filter1 = self._make_one(filters=filters)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)


class TestRowFilterChain(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import RowFilterChain

        return RowFilterChain

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter1_pb = row_filter1.to_pb()

        row_filter2 = RowSampleFilter(0.25)
        row_filter2_pb = row_filter2.to_pb()

        row_filter3 = self._make_one(filters=[row_filter1, row_filter2])
        filter_pb = row_filter3.to_pb()

        expected_pb = _RowFilterPB(
            chain=_RowFilterChainPB(
                filters=[row_filter1_pb, row_filter2_pb],
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test_to_pb_nested(self):
        from google.cloud.bigtable.row_filters import CellsRowLimitFilter
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter2 = RowSampleFilter(0.25)

        row_filter3 = self._make_one(filters=[row_filter1, row_filter2])
        row_filter3_pb = row_filter3.to_pb()

        row_filter4 = CellsRowLimitFilter(11)
        row_filter4_pb = row_filter4.to_pb()

        row_filter5 = self._make_one(filters=[row_filter3, row_filter4])
        filter_pb = row_filter5.to_pb()

        expected_pb = _RowFilterPB(
            chain=_RowFilterChainPB(
                filters=[row_filter3_pb, row_filter4_pb],
            ),
        )
        self.assertEqual(filter_pb, expected_pb)


class TestRowFilterUnion(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import RowFilterUnion

        return RowFilterUnion

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_to_pb(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter1_pb = row_filter1.to_pb()

        row_filter2 = RowSampleFilter(0.25)
        row_filter2_pb = row_filter2.to_pb()

        row_filter3 = self._make_one(filters=[row_filter1, row_filter2])
        filter_pb = row_filter3.to_pb()

        expected_pb = _RowFilterPB(
            interleave=_RowFilterInterleavePB(
                filters=[row_filter1_pb, row_filter2_pb],
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test_to_pb_nested(self):
        from google.cloud.bigtable.row_filters import CellsRowLimitFilter
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter2 = RowSampleFilter(0.25)

        row_filter3 = self._make_one(filters=[row_filter1, row_filter2])
        row_filter3_pb = row_filter3.to_pb()

        row_filter4 = CellsRowLimitFilter(11)
        row_filter4_pb = row_filter4.to_pb()

        row_filter5 = self._make_one(filters=[row_filter3, row_filter4])
        filter_pb = row_filter5.to_pb()

        expected_pb = _RowFilterPB(
            interleave=_RowFilterInterleavePB(
                filters=[row_filter3_pb, row_filter4_pb],
            ),
        )
        self.assertEqual(filter_pb, expected_pb)


class TestConditionalRowFilter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_filters import ConditionalRowFilter

        return ConditionalRowFilter

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        base_filter = object()
        true_filter = object()
        false_filter = object()
        cond_filter = self._make_one(base_filter,
                                     true_filter=true_filter,
                                     false_filter=false_filter)
        self.assertIs(cond_filter.base_filter, base_filter)
        self.assertIs(cond_filter.true_filter, true_filter)
        self.assertIs(cond_filter.false_filter, false_filter)

    def test___eq__(self):
        base_filter = object()
        true_filter = object()
        false_filter = object()
        cond_filter1 = self._make_one(base_filter,
                                      true_filter=true_filter,
                                      false_filter=false_filter)
        cond_filter2 = self._make_one(base_filter,
                                      true_filter=true_filter,
                                      false_filter=false_filter)
        self.assertEqual(cond_filter1, cond_filter2)

    def test___eq__type_differ(self):
        base_filter = object()
        true_filter = object()
        false_filter = object()
        cond_filter1 = self._make_one(base_filter,
                                      true_filter=true_filter,
                                      false_filter=false_filter)
        cond_filter2 = object()
        self.assertNotEqual(cond_filter1, cond_filter2)

    def test_to_pb(self):
        from google.cloud.bigtable.row_filters import CellsRowOffsetFilter
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter1_pb = row_filter1.to_pb()

        row_filter2 = RowSampleFilter(0.25)
        row_filter2_pb = row_filter2.to_pb()

        row_filter3 = CellsRowOffsetFilter(11)
        row_filter3_pb = row_filter3.to_pb()

        row_filter4 = self._make_one(row_filter1, true_filter=row_filter2,
                                     false_filter=row_filter3)
        filter_pb = row_filter4.to_pb()

        expected_pb = _RowFilterPB(
            condition=_RowFilterConditionPB(
                predicate_filter=row_filter1_pb,
                true_filter=row_filter2_pb,
                false_filter=row_filter3_pb,
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test_to_pb_true_only(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter1_pb = row_filter1.to_pb()

        row_filter2 = RowSampleFilter(0.25)
        row_filter2_pb = row_filter2.to_pb()

        row_filter3 = self._make_one(row_filter1, true_filter=row_filter2)
        filter_pb = row_filter3.to_pb()

        expected_pb = _RowFilterPB(
            condition=_RowFilterConditionPB(
                predicate_filter=row_filter1_pb,
                true_filter=row_filter2_pb,
            ),
        )
        self.assertEqual(filter_pb, expected_pb)

    def test_to_pb_false_only(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable.row_filters import (
            StripValueTransformerFilter)

        row_filter1 = StripValueTransformerFilter(True)
        row_filter1_pb = row_filter1.to_pb()

        row_filter2 = RowSampleFilter(0.25)
        row_filter2_pb = row_filter2.to_pb()

        row_filter3 = self._make_one(row_filter1, false_filter=row_filter2)
        filter_pb = row_filter3.to_pb()

        expected_pb = _RowFilterPB(
            condition=_RowFilterConditionPB(
                predicate_filter=row_filter1_pb,
                false_filter=row_filter2_pb,
            ),
        )
        self.assertEqual(filter_pb, expected_pb)


def _ColumnRangePB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.ColumnRange(*args, **kw)


def _RowFilterPB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.RowFilter(*args, **kw)


def _RowFilterChainPB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.RowFilter.Chain(*args, **kw)


def _RowFilterConditionPB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.RowFilter.Condition(*args, **kw)


def _RowFilterInterleavePB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.RowFilter.Interleave(*args, **kw)


def _TimestampRangePB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.TimestampRange(*args, **kw)


def _ValueRangePB(*args, **kw):
    from google.cloud.bigtable._generated import (
        data_pb2 as data_v2_pb2)

    return data_v2_pb2.ValueRange(*args, **kw)
