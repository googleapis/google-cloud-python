# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import unittest


class TestUtils(unittest.TestCase):
    def test_PeekIterator(self):
        from google.cloud.spanner_dbapi.utils import PeekIterator

        cases = [
            ("list", [1, 2, 3, 4, 6, 7], [1, 2, 3, 4, 6, 7]),
            ("iter_from_list", iter([1, 2, 3, 4, 6, 7]), [1, 2, 3, 4, 6, 7]),
            ("tuple", ("a", 12, 0xFF), ["a", 12, 0xFF]),
            ("iter_from_tuple", iter(("a", 12, 0xFF)), ["a", 12, 0xFF]),
            ("no_args", (), []),
        ]

        for name, data_in, expected in cases:
            with self.subTest(name=name):
                pitr = PeekIterator(data_in)
                actual = list(pitr)
                self.assertEqual(actual, expected)

    def test_peekIterator_list_rows_converted_to_tuples(self):
        from google.cloud.spanner_dbapi.utils import PeekIterator

        # Cloud Spanner returns results in lists e.g. [result].
        # PeekIterator is used by BaseCursor in its fetch* methods.
        # This test ensures that anything passed into PeekIterator
        # will be returned as a tuple.
        pit = PeekIterator([["a"], ["b"], ["c"], ["d"], ["e"]])
        got = list(pit)
        want = [("a",), ("b",), ("c",), ("d",), ("e",)]
        self.assertEqual(
            got, want, "Rows of type list must be returned as tuples"
        )

        seventeen = PeekIterator([[17]])
        self.assertEqual(list(seventeen), [(17,)])

        pit = PeekIterator([["%", "%d"]])
        self.assertEqual(next(pit), ("%", "%d"))

        pit = PeekIterator([("Clark", "Kent")])
        self.assertEqual(next(pit), ("Clark", "Kent"))

    def test_peekIterator_nonlist_rows_unconverted(self):
        from google.cloud.spanner_dbapi.utils import PeekIterator

        pi = PeekIterator(["a", "b", "c", "d", "e"])
        got = list(pi)
        want = ["a", "b", "c", "d", "e"]
        self.assertEqual(got, want, "Values should be returned unchanged")

    def test_backtick_unicode(self):
        from google.cloud.spanner_dbapi.utils import backtick_unicode

        cases = [
            ("SELECT (1) as foo WHERE 1=1", "SELECT (1) as foo WHERE 1=1"),
            ("SELECT (1) as föö", "SELECT (1) as `föö`"),
            ("SELECT (1) as `föö`", "SELECT (1) as `föö`"),
            ("SELECT (1) as `föö` `umläut", "SELECT (1) as `föö` `umläut"),
            ("SELECT (1) as `föö", "SELECT (1) as `föö"),
        ]
        for sql, want in cases:
            with self.subTest(sql=sql):
                got = backtick_unicode(sql)
                self.assertEqual(got, want)
