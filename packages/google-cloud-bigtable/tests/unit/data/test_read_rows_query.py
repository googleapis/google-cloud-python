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

from unittest import mock

import pytest

TEST_ROWS = [
    "row_key_1",
    b"row_key_2",
]


class TestRowRange:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.data.read_rows_query import RowRange

        return RowRange

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor_start_end(self):
        row_range = self._make_one("test_row", "test_row2")
        assert row_range.start_key == "test_row".encode()
        assert row_range.end_key == "test_row2".encode()
        assert row_range.start_is_inclusive is True
        assert row_range.end_is_inclusive is False

    def test_ctor_start_only(self):
        row_range = self._make_one("test_row3")
        assert row_range.start_key == "test_row3".encode()
        assert row_range.start_is_inclusive is True
        assert row_range.end_key is None
        assert row_range.end_is_inclusive is True

    def test_ctor_end_only(self):
        row_range = self._make_one(end_key="test_row4")
        assert row_range.end_key == "test_row4".encode()
        assert row_range.end_is_inclusive is False
        assert row_range.start_key is None
        assert row_range.start_is_inclusive is True

    def test_ctor_empty_strings(self):
        """
        empty strings should be treated as None
        """
        row_range = self._make_one("", "")
        assert row_range.start_key is None
        assert row_range.end_key is None
        assert row_range.start_is_inclusive is True
        assert row_range.end_is_inclusive is True

    def test_ctor_inclusive_flags(self):
        row_range = self._make_one("test_row5", "test_row6", False, True)
        assert row_range.start_key == "test_row5".encode()
        assert row_range.end_key == "test_row6".encode()
        assert row_range.start_is_inclusive is False
        assert row_range.end_is_inclusive is True

    def test_ctor_defaults(self):
        row_range = self._make_one()
        assert row_range.start_key is None
        assert row_range.end_key is None

    def test_ctor_invalid_keys(self):
        # test with invalid keys
        with pytest.raises(ValueError) as exc:
            self._make_one(1, "2")
        assert str(exc.value) == "start_key must be a string or bytes"
        with pytest.raises(ValueError) as exc:
            self._make_one("1", 2)
        assert str(exc.value) == "end_key must be a string or bytes"
        with pytest.raises(ValueError) as exc:
            self._make_one("2", "1")
        assert str(exc.value) == "start_key must be less than or equal to end_key"

    @pytest.mark.parametrize(
        "dict_repr,expected",
        [
            ({"start_key_closed": "test_row", "end_key_open": "test_row2"}, True),
            ({"start_key_closed": b"test_row", "end_key_open": b"test_row2"}, True),
            ({"start_key_open": "test_row", "end_key_closed": "test_row2"}, True),
            ({"start_key_open": b"a"}, True),
            ({"end_key_closed": b"b"}, True),
            ({"start_key_closed": "a"}, True),
            ({"end_key_open": b"b"}, True),
            ({}, False),
        ],
    )
    def test___bool__(self, dict_repr, expected):
        """
        Only row range with both points empty should be falsy
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        row_range = RowRange._from_dict(dict_repr)
        assert bool(row_range) is expected

    def test__eq__(self):
        """
        test that row ranges can be compared for equality
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        range1 = RowRange("1", "2")
        range1_dup = RowRange("1", "2")
        range2 = RowRange("1", "3")
        range_w_empty = RowRange(None, "2")
        assert range1 == range1_dup
        assert range1 != range2
        assert range1 != range_w_empty
        range_1_w_inclusive_start = RowRange("1", "2", start_is_inclusive=True)
        range_1_w_exclusive_start = RowRange("1", "2", start_is_inclusive=False)
        range_1_w_inclusive_end = RowRange("1", "2", end_is_inclusive=True)
        range_1_w_exclusive_end = RowRange("1", "2", end_is_inclusive=False)
        assert range1 == range_1_w_inclusive_start
        assert range1 == range_1_w_exclusive_end
        assert range1 != range_1_w_exclusive_start
        assert range1 != range_1_w_inclusive_end

    @pytest.mark.parametrize(
        "dict_repr,expected",
        [
            (
                {"start_key_closed": "test_row", "end_key_open": "test_row2"},
                "[b'test_row', b'test_row2')",
            ),
            (
                {"start_key_open": "test_row", "end_key_closed": "test_row2"},
                "(b'test_row', b'test_row2']",
            ),
            ({"start_key_open": b"a"}, "(b'a', +inf]"),
            ({"end_key_closed": b"b"}, "[-inf, b'b']"),
            ({"end_key_open": b"b"}, "[-inf, b'b')"),
            ({}, "[-inf, +inf]"),
        ],
    )
    def test___str__(self, dict_repr, expected):
        """
        test string representations of row ranges
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        row_range = RowRange._from_dict(dict_repr)
        assert str(row_range) == expected

    @pytest.mark.parametrize(
        "dict_repr,expected",
        [
            (
                {"start_key_closed": "test_row", "end_key_open": "test_row2"},
                "RowRange(start_key=b'test_row', end_key=b'test_row2')",
            ),
            (
                {"start_key_open": "test_row", "end_key_closed": "test_row2"},
                "RowRange(start_key=b'test_row', end_key=b'test_row2', start_is_inclusive=False, end_is_inclusive=True)",
            ),
            (
                {"start_key_open": b"a"},
                "RowRange(start_key=b'a', end_key=None, start_is_inclusive=False)",
            ),
            (
                {"end_key_closed": b"b"},
                "RowRange(start_key=None, end_key=b'b', end_is_inclusive=True)",
            ),
            ({"end_key_open": b"b"}, "RowRange(start_key=None, end_key=b'b')"),
            ({}, "RowRange(start_key=None, end_key=None)"),
        ],
    )
    def test___repr__(self, dict_repr, expected):
        """
        test repr representations of row ranges
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        row_range = RowRange._from_dict(dict_repr)
        assert repr(row_range) == expected


class TestReadRowsQuery:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        return ReadRowsQuery

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor_defaults(self):
        query = self._make_one()
        assert query.row_keys == list()
        assert query.row_ranges == list()
        assert query.filter is None
        assert query.limit is None

    def test_ctor_explicit(self):
        from google.cloud.bigtable.data.read_rows_query import RowRange
        from google.cloud.bigtable.data.row_filters import RowFilterChain

        filter_ = RowFilterChain()
        query = self._make_one(
            ["row_key_1", "row_key_2"],
            row_ranges=[RowRange("row_key_3", "row_key_4")],
            limit=10,
            row_filter=filter_,
        )
        assert len(query.row_keys) == 2
        assert "row_key_1".encode() in query.row_keys
        assert "row_key_2".encode() in query.row_keys
        assert len(query.row_ranges) == 1
        assert RowRange("row_key_3", "row_key_4") in query.row_ranges
        assert query.filter == filter_
        assert query.limit == 10

    def test_ctor_invalid_limit(self):
        with pytest.raises(ValueError) as exc:
            self._make_one(limit=-1)
        assert str(exc.value) == "limit must be >= 0"

    def test_set_filter(self):
        from google.cloud.bigtable.data.row_filters import RowFilterChain

        filter1 = RowFilterChain()
        query = self._make_one()
        assert query.filter is None
        query.filter = filter1
        assert query.filter == filter1
        filter2 = RowFilterChain()
        query.filter = filter2
        assert query.filter == filter2
        query.filter = None
        assert query.filter is None
        query.filter = RowFilterChain()
        assert query.filter == RowFilterChain()

    def test_set_limit(self):
        query = self._make_one()
        assert query.limit is None
        query.limit = 10
        assert query.limit == 10
        query.limit = 9
        assert query.limit == 9
        query.limit = 0
        assert query.limit is None
        with pytest.raises(ValueError) as exc:
            query.limit = -1
        assert str(exc.value) == "limit must be >= 0"
        with pytest.raises(ValueError) as exc:
            query.limit = -100
        assert str(exc.value) == "limit must be >= 0"

    def test_add_key_str(self):
        query = self._make_one()
        assert query.row_keys == list()
        input_str = "test_row"
        query.add_key(input_str)
        assert len(query.row_keys) == 1
        assert input_str.encode() in query.row_keys
        input_str2 = "test_row2"
        query.add_key(input_str2)
        assert len(query.row_keys) == 2
        assert input_str.encode() in query.row_keys
        assert input_str2.encode() in query.row_keys

    def test_add_key_bytes(self):
        query = self._make_one()
        assert query.row_keys == list()
        input_bytes = b"test_row"
        query.add_key(input_bytes)
        assert len(query.row_keys) == 1
        assert input_bytes in query.row_keys
        input_bytes2 = b"test_row2"
        query.add_key(input_bytes2)
        assert len(query.row_keys) == 2
        assert input_bytes in query.row_keys
        assert input_bytes2 in query.row_keys

    def test_add_rows_batch(self):
        query = self._make_one()
        assert query.row_keys == list()
        input_batch = ["test_row", b"test_row2", "test_row3"]
        for k in input_batch:
            query.add_key(k)
        assert len(query.row_keys) == 3
        assert b"test_row" in query.row_keys
        assert b"test_row2" in query.row_keys
        assert b"test_row3" in query.row_keys
        # test adding another batch
        for k in ["test_row4", b"test_row5"]:
            query.add_key(k)
        assert len(query.row_keys) == 5
        assert input_batch[0].encode() in query.row_keys
        assert input_batch[1] in query.row_keys
        assert input_batch[2].encode() in query.row_keys
        assert b"test_row4" in query.row_keys
        assert b"test_row5" in query.row_keys

    def test_add_key_invalid(self):
        query = self._make_one()
        with pytest.raises(ValueError) as exc:
            query.add_key(1)
        assert str(exc.value) == "row_key must be string or bytes"
        with pytest.raises(ValueError) as exc:
            query.add_key(["s"])
        assert str(exc.value) == "row_key must be string or bytes"

    def test_add_range(self):
        from google.cloud.bigtable.data.read_rows_query import RowRange

        query = self._make_one()
        assert query.row_ranges == list()
        input_range = RowRange(start_key=b"test_row")
        query.add_range(input_range)
        assert len(query.row_ranges) == 1
        assert input_range in query.row_ranges
        input_range2 = RowRange(start_key=b"test_row2")
        query.add_range(input_range2)
        assert len(query.row_ranges) == 2
        assert input_range in query.row_ranges
        assert input_range2 in query.row_ranges

    def _parse_query_string(self, query_string):
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery, RowRange

        query = ReadRowsQuery()
        segments = query_string.split(",")
        for segment in segments:
            if "-" in segment:
                start, end = segment.split("-")
                s_open, e_open = True, True
                if start == "":
                    start = None
                    s_open = None
                else:
                    if start[0] == "(":
                        s_open = False
                    start = start[1:]
                if end == "":
                    end = None
                    e_open = None
                else:
                    if end[-1] == ")":
                        e_open = False
                    end = end[:-1]
                query.add_range(RowRange(start, end, s_open, e_open))
            else:
                query.add_key(segment)
        return query

    @pytest.mark.parametrize(
        "query_string,shard_points",
        [
            ("a,[p-q)", []),
            ("0_key,[1_range_start-2_range_end)", ["3_split"]),
            ("0_key,[1_range_start-2_range_end)", ["2_range_end"]),
            ("0_key,[1_range_start-2_range_end]", ["2_range_end"]),
            ("-1_range_end)", ["5_split"]),
            ("8_key,(1_range_start-2_range_end]", ["1_range_start"]),
            ("9_row_key,(5_range_start-7_range_end)", ["3_split"]),
            ("3_row_key,(5_range_start-7_range_end)", ["2_row_key"]),
            ("4_split,4_split,(3_split-5_split]", ["3_split", "5_split"]),
            ("(3_split-", ["3_split"]),
        ],
    )
    def test_shard_no_split(self, query_string, shard_points):
        """
        Test sharding with a set of queries that should not result in any splits.
        """
        initial_query = self._parse_query_string(query_string)
        row_samples = [(point.encode(), None) for point in shard_points]
        sharded_queries = initial_query.shard(row_samples)
        assert len(sharded_queries) == 1
        assert initial_query == sharded_queries[0]

    def test_shard_full_table_scan_empty_split(self):
        """
        Sharding a full table scan with no split should return another full table scan.
        """
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        full_scan_query = ReadRowsQuery()
        split_points = []
        sharded_queries = full_scan_query.shard(split_points)
        assert len(sharded_queries) == 1
        result_query = sharded_queries[0]
        assert result_query == full_scan_query

    def test_shard_full_table_scan_with_split(self):
        """
        Test splitting a full table scan into two queries
        """
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        full_scan_query = ReadRowsQuery()
        split_points = [(b"a", None)]
        sharded_queries = full_scan_query.shard(split_points)
        assert len(sharded_queries) == 2
        assert sharded_queries[0] == self._parse_query_string("-a]")
        assert sharded_queries[1] == self._parse_query_string("(a-")

    def test_shard_full_table_scan_with_multiple_split(self):
        """
        Test splitting a full table scan into three queries
        """
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        full_scan_query = ReadRowsQuery()
        split_points = [(b"a", None), (b"z", None)]
        sharded_queries = full_scan_query.shard(split_points)
        assert len(sharded_queries) == 3
        assert sharded_queries[0] == self._parse_query_string("-a]")
        assert sharded_queries[1] == self._parse_query_string("(a-z]")
        assert sharded_queries[2] == self._parse_query_string("(z-")

    def test_shard_multiple_keys(self):
        """
        Test splitting multiple individual keys into separate queries
        """
        initial_query = self._parse_query_string("1_beforeSplit,2_onSplit,3_afterSplit")
        split_points = [(b"2_onSplit", None)]
        sharded_queries = initial_query.shard(split_points)
        assert len(sharded_queries) == 2
        assert sharded_queries[0] == self._parse_query_string("1_beforeSplit,2_onSplit")
        assert sharded_queries[1] == self._parse_query_string("3_afterSplit")

    def test_shard_keys_empty_left(self):
        """
        Test with the left-most split point empty
        """
        initial_query = self._parse_query_string("5_test,8_test")
        split_points = [(b"0_split", None), (b"6_split", None)]
        sharded_queries = initial_query.shard(split_points)
        assert len(sharded_queries) == 2
        assert sharded_queries[0] == self._parse_query_string("5_test")
        assert sharded_queries[1] == self._parse_query_string("8_test")

    def test_shard_keys_empty_right(self):
        """
        Test with the right-most split point empty
        """
        initial_query = self._parse_query_string("0_test,2_test")
        split_points = [(b"1_split", None), (b"5_split", None)]
        sharded_queries = initial_query.shard(split_points)
        assert len(sharded_queries) == 2
        assert sharded_queries[0] == self._parse_query_string("0_test")
        assert sharded_queries[1] == self._parse_query_string("2_test")

    def test_shard_mixed_split(self):
        """
        Test splitting a complex query with multiple split points
        """
        initial_query = self._parse_query_string("0,a,c,-a],-b],(c-e],(d-f],(m-")
        split_points = [(s.encode(), None) for s in ["a", "d", "j", "o"]]
        sharded_queries = initial_query.shard(split_points)
        assert len(sharded_queries) == 5
        assert sharded_queries[0] == self._parse_query_string("0,a,-a]")
        assert sharded_queries[1] == self._parse_query_string("c,(a-b],(c-d]")
        assert sharded_queries[2] == self._parse_query_string("(d-e],(d-f]")
        assert sharded_queries[3] == self._parse_query_string("(m-o]")
        assert sharded_queries[4] == self._parse_query_string("(o-")

    def test_shard_unsorted_request(self):
        """
        Test with a query that contains rows and queries in a random order
        """
        initial_query = self._parse_query_string(
            "7_row_key_1,2_row_key_2,[8_range_1_start-9_range_1_end),[3_range_2_start-4_range_2_end)"
        )
        split_points = [(b"5-split", None)]
        sharded_queries = initial_query.shard(split_points)
        assert len(sharded_queries) == 2
        assert sharded_queries[0] == self._parse_query_string(
            "2_row_key_2,[3_range_2_start-4_range_2_end)"
        )
        assert sharded_queries[1] == self._parse_query_string(
            "7_row_key_1,[8_range_1_start-9_range_1_end)"
        )

    @pytest.mark.parametrize(
        "query_string,shard_points",
        [
            ("a,[p-q)", []),
            ("0_key,[1_range_start-2_range_end)", ["3_split"]),
            ("-1_range_end)", ["5_split"]),
            ("0_key,[1_range_start-2_range_end)", ["2_range_end"]),
            ("9_row_key,(5_range_start-7_range_end)", ["3_split"]),
            ("(5_range_start-", ["3_split"]),
            ("3_split,[3_split-5_split)", ["3_split", "5_split"]),
            ("[3_split-", ["3_split"]),
            ("", []),
            ("", ["3_split"]),
            ("", ["3_split", "5_split"]),
            ("1,2,3,4,5,6,7,8,9", ["3_split"]),
        ],
    )
    def test_shard_keeps_filter(self, query_string, shard_points):
        """
        sharded queries should keep the filter from the original query
        """
        initial_query = self._parse_query_string(query_string)
        expected_filter = {"test": "filter"}
        initial_query.filter = expected_filter
        row_samples = [(point.encode(), None) for point in shard_points]
        sharded_queries = initial_query.shard(row_samples)
        assert len(sharded_queries) > 0
        for query in sharded_queries:
            assert query.filter == expected_filter

    def test_shard_limit_exception(self):
        """
        queries with a limit should raise an exception when a shard is attempted
        """
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        query = ReadRowsQuery(limit=10)
        with pytest.raises(AttributeError) as e:
            query.shard([])
        assert "Cannot shard query with a limit" in str(e.value)

    @pytest.mark.parametrize(
        "first_args,second_args,expected",
        [
            ((), (), True),
            ((), ("a",), False),
            (("a",), (), False),
            (("a",), ("a",), True),
            ((["a"],), (["a", "b"],), False),
            ((["a", "b"],), (["a", "b"],), True),
            ((["a", b"b"],), ([b"a", "b"],), True),
            (("a",), (b"a",), True),
            (("a",), ("b",), False),
            (("a",), ("a", ["b"]), False),
            (("a", "b"), ("a", ["b"]), True),
            (("a", ["b"]), ("a", ["b", "c"]), False),
            (("a", ["b", "c"]), ("a", [b"b", "c"]), True),
            (("a", ["b", "c"], 1), ("a", ["b", b"c"], 1), True),
            (("a", ["b"], 1), ("a", ["b"], 2), False),
            (("a", ["b"], 1, {"a": "b"}), ("a", ["b"], 1, {"a": "b"}), True),
            (("a", ["b"], 1, {"a": "b"}), ("a", ["b"], 1), False),
            (
                (),
                (None, [None], None, None),
                True,
            ),  # empty query is equal to empty row range
            ((), (None, [None], 1, None), False),
            ((), (None, [None], None, {"a": "b"}), False),
        ],
    )
    def test___eq__(self, first_args, second_args, expected):
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery, RowRange

        # replace row_range placeholders with a RowRange object
        if len(first_args) > 1:
            first_args = list(first_args)
            first_args[1] = [RowRange(c) for c in first_args[1]]
        if len(second_args) > 1:
            second_args = list(second_args)
            second_args[1] = [RowRange(c) for c in second_args[1]]
        first = ReadRowsQuery(*first_args)
        second = ReadRowsQuery(*second_args)
        assert (first == second) == expected

    def test___repr__(self):
        from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

        instance = self._make_one(row_keys=["a", "b"], row_filter={}, limit=10)
        # should be able to recreate the instance from the repr
        repr_str = repr(instance)
        recreated = eval(repr_str)
        assert isinstance(recreated, ReadRowsQuery)
        assert recreated == instance

    def test_empty_row_set(self):
        """Empty strings should be treated as keys inputs"""
        query = self._make_one(row_keys="")
        assert query.row_keys == [b""]

    def test_add_range_does_not_materialize_row_ranges(self):
        """
        Ensures add_range scales in O(1) time and does not trigger O(N) scans.

        The legacy implementation called the `row_ranges` property helper during
        membership checks, which dynamically re-allocated and materialized brand
        new Python RowRange wrapper objects for every element in the array on
        each insertion. This led to an accidental O(N^2) memory and CPU leak.

        This test mocks out the `row_ranges` property on the class and asserts
        that it is never accessed during batch additions, proving we bypass the
        quadratic evaluation path entirely.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        query = self._make_one()

        # Intercept the `row_ranges` class property with a mock to track accesses
        with mock.patch.object(
            type(query), "row_ranges", new_callable=mock.PropertyMock
        ) as row_ranges:
            for i in range(100):
                # Add unique sequential ranges. Utilizing our fast O(1) set signature lookup
                # should never touch the slow wrapper-materialization properties.
                query.add_range(RowRange(f"k{i:03d}", f"k{i + 1:03d}"))

            # ASSERT: The slow, O(N) wrapper-building property was never accessed
            row_ranges.assert_not_called()

        # Verify that all ranges were successfully committed to the underlying protobuf
        assert len(query._row_set.row_ranges) == 100

    def test_add_key_deduplicates_via_set_without_scanning_row_set(self):
        """
        Verify that ReadRowsQuery deduplicates row_keys in __init__ and add_key
        using its internal O(1) key set without linearly scanning _row_set.row_keys.
        """
        # Duplicate keys passed to __init__ (even in mixed str/bytes forms)
        # must be deduplicated on construction.
        query = self._make_one(row_keys=["k0", b"k0"])
        assert query.row_keys == [b"k0"]

        # When adding keys that are already present in the query, add_key must
        # short-circuit via _key_set without accessing _row_set.row_keys.
        with mock.patch.object(query, "_row_set", wraps=query._row_set) as mock_row_set:
            query.add_key(b"k0")
            query.add_key("k0")
            assert not mock_row_set.row_keys.called

        assert query.row_keys == [b"k0"]

    def test_query_equality_does_not_materialize_row_keys_or_ranges(self):
        """
        Verify that ReadRowsQuery.__eq__ compares keys and ranges in order-independent
        O(N) time using internal sets without materializing row_keys or row_ranges lists.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        # Create two equivalent queries with identical keys and ranges inserted
        # in opposite orders.
        q1 = self._make_one(
            row_keys=[f"k{i}" for i in range(50)],
            row_ranges=[RowRange(f"a{i}", f"b{i}") for i in range(50)],
        )
        q2 = self._make_one(
            row_keys=[f"k{i}" for i in reversed(range(50))],
            row_ranges=[RowRange(f"a{i}", f"b{i}") for i in reversed(range(50))],
        )

        # Intercept the row_keys and row_ranges properties to verify that equality
        # comparisons operate on internal sets without constructing wrapper lists.
        with (
            mock.patch.object(
                type(q1), "row_keys", new_callable=mock.PropertyMock
            ) as mock_keys,
            mock.patch.object(
                type(q1), "row_ranges", new_callable=mock.PropertyMock
            ) as mock_ranges,
        ):
            assert q1 == q2
            mock_keys.assert_not_called()
            mock_ranges.assert_not_called()

    def test_add_range_deduplication_behavior(self):
        """Assert that identical ranges are deduplicated, but distinct ranges are kept."""
        from google.cloud.bigtable.data.read_rows_query import RowRange

        query = self._make_one()

        # Create two identical ranges
        r1 = RowRange(start_key="a", end_key="b")
        r2 = RowRange(start_key="a", end_key="b")

        # Create a distinct range
        r3 = RowRange(start_key="c", end_key="d")

        # Add all three ranges
        query.add_range(r1)
        query.add_range(r2)  # Duplicate, should be ignored
        query.add_range(r3)  # Distinct, should be kept

        # Assert that only r1 and r3 are in the final query
        assert len(query.row_ranges) == 2
        assert query.row_ranges[0] == r1
        assert query.row_ranges[1] == r3

    def test_row_range_hash_matches_legacy(self):
        """
        Verify that base RowRange and legacy row_set.RowRange instances representing
        the same range compare equal, produce identical hashes, and deduplicate
        properly when combined in a ReadRowsQuery.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange
        from google.cloud.bigtable.row_set import RowRange as LegacyRowRange

        # Instantiate equivalent ranges using both the data API and legacy classes.
        base_range = RowRange(b"a", b"b")
        legacy_range = LegacyRowRange(b"a", b"b")

        # Equal RowRange objects must produce identical hashes so set membership
        # operates consistently across base and legacy types.
        assert base_range == legacy_range
        assert hash(base_range) == hash(legacy_range)

        # Adding an equivalent legacy range to a query initialized with a base range
        # should be recognized as a duplicate and ignored.
        query = self._make_one(row_ranges=[base_range])
        query.add_range(legacy_range)
        assert len(query.row_ranges) == 1

    def test_add_range_immune_to_caller_mutating_row_range_after_insert(self):
        """
        Verify that mutating a RowRange's underlying protobuf after adding it to
        a query does not corrupt the query's internal deduplication set.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        query = self._make_one()
        r1 = RowRange(start_key=b"a", end_key=b"b")
        query.add_range(r1)

        # Mutate the caller's RowRange wrapper reference after insertion.
        r1._pb = RowRange(start_key=b"x", end_key=b"y")._pb

        # Adding a new RowRange with the original ("a", "b") bounds must still be
        # detected as a duplicate of the previously added range.
        query.add_range(RowRange(start_key=b"a", end_key=b"b"))

        assert len(query.row_ranges) == 1
        assert query.row_ranges[0] == RowRange(start_key=b"a", end_key=b"b")

    def test_row_range_from_dict_does_not_call_init(self):
        """
        Verify that RowRange._from_dict constructs the wrapper instance directly
        without invoking __init__ and allocating an unused intermediate protobuf.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        # Spy on RowRange.__init__ to ensure dictionary deserialization bypasses
        # default constructor initialization and dummy protobuf creation.
        with mock.patch.object(
            RowRange, "__init__", wraps=RowRange.__init__
        ) as mock_init:
            row_range = RowRange._from_dict(
                {"start_key_closed": b"a", "end_key_open": b"b"}
            )
            mock_init.assert_not_called()

        # Verify the resulting RowRange exposes the expected boundaries and inclusivity.
        assert row_range.start_key == b"a"
        assert row_range.start_is_inclusive is True
        assert row_range.end_key == b"b"
        assert row_range.end_is_inclusive is False

    def test_read_rows_query_enforces_slots(self):
        """
        Verify that ReadRowsQuery enforces __slots__ so instances do not allocate
        a dynamic __dict__ or permit undeclared attributes.
        """
        from google.cloud.bigtable.data.read_rows_query import RowRange

        # Initialize a query with both keys and ranges so all internal attributes
        # are populated on the instance.
        query = self._make_one(
            row_keys=[b"k1"],
            row_ranges=[RowRange(start_key=b"a", end_key=b"b")],
        )

        # Enforcing __slots__ prevents creation of a per-instance __dict__.
        assert not hasattr(query, "__dict__")

        # Assigning an attribute not declared in __slots__ must raise AttributeError.
        with pytest.raises(AttributeError):
            query._undeclared_attribute = "invalid"

    def test_copy_query_preserves_deduplication_isolation(self):
        """
        Verify that shallow-copying a ReadRowsQuery produces independent
        deduplication tracking sets so mutations on the copy do not affect the
        original query, and existing items remain deduplicated on the copy.
        """
        import copy

        from google.cloud.bigtable.data.read_rows_query import RowRange

        r1 = RowRange(start_key="a", end_key="b")
        r2 = RowRange(start_key="c", end_key="d")

        original = self._make_one(row_keys=[b"k1"], row_ranges=[r1])
        copied = copy.copy(original)

        # Re-adding existing items to the copy must be ignored as duplicates.
        copied.add_key(b"k1")
        copied.add_range(r1)
        assert copied.row_keys == [b"k1"]
        assert copied.row_ranges == [r1]

        # Mutate only the copied query by adding a new key and range.
        copied.add_key(b"k2")
        copied.add_range(r2)

        # Confirm the original query was not modified by operations on the copy.
        assert original.row_keys == [b"k1"]
        assert original.row_ranges == [r1]

        # Adding the same new key and range to the original query must succeed
        # because its internal deduplication sets are independent from the copy.
        original.add_key(b"k2")
        original.add_range(r2)

        assert original.row_keys == [b"k1", b"k2"]
        assert original.row_ranges == [r1, r2]
