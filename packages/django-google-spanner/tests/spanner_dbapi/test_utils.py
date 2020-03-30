# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from unittest import TestCase

from spanner_dbapi.utils import PeekIterator


class UtilsTests(TestCase):
    def test_peekIterator_list_rows_converted_to_tuples(self):
        # Cloud Spanner returns results in lists e.g. [result].
        # PeekIterator is used by BaseCursor in its fetch* methods.
        # This test ensures that anything passed into PeekIterator
        # will be returned as a tuple.
        pit = PeekIterator([['a'], ['b'], ['c'], ['d'], ['e']])
        got = list(pit)
        want = [('a',), ('b',), ('c',), ('d',), ('e',)]
        self.assertEqual(got, want, 'Rows of type list must be returned as tuples')

        seventeen = PeekIterator([[17]])
        self.assertEqual(list(seventeen), [(17,)])

        pit = PeekIterator([['%', '%d']])
        self.assertEqual(next(pit), ('%', '%d',))

        pit = PeekIterator([('Clark', 'Kent')])
        self.assertEqual(next(pit), ('Clark', 'Kent',))

    def test_peekIterator_nonlist_rows_unconverted(self):
        pi = PeekIterator(['a', 'b', 'c', 'd', 'e'])
        got = list(pi)
        want = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(got, want, 'Values should be returned unchanged')
