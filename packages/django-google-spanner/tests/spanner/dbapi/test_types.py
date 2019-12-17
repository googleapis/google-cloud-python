# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from unittest import TestCase

from spanner.dbapi.cursor import PeekIterator
from spanner.dbapi.types import (
    Date, DateFromTicks, Time, TimeFromTicks, Timestamp, TimestampFromTicks,
)

tzUTC = 0  # 0 hours offset from UTC


class TypesTests(TestCase):
    def test_Date(self):
        got = Date(2019, 11, 3)
        want = datetime.date(2019, 11, 3)
        self.assertEqual(got, want, 'mismatch between conversion')

    def test_Time(self):
        got = Time(23, 8, 19)
        want = datetime.time(23, 8, 19)
        self.assertEqual(got, want, 'mismatch between conversion')

    def test_Timestamp(self):
        got = Timestamp(2019, 11, 3, 23, 8, 19)
        want = datetime.datetime(2019, 11, 3, 23, 8, 19)
        self.assertEqual(got, want, 'mismatch between conversion')

    def test_DateFromTicks(self):
        epochTicks = 1572851662.9782631  # Sun Nov 03 23:14:22 2019
        got = DateFromTicks(epochTicks)
        # Since continuous integration infrastructure such as Travis CI
        # uses clocks on UTC, it is useful to be able to compare against
        # either of UTC or the known standard time.
        want = (
            datetime.date(2019, 11, 3),
            datetime.datetime(2019, 11, 4, tzUTC).date(),
        )
        matches = got in want
        self.assertTrue(matches, '`%s` not present in any of\n`%s`' % (got, want))

    def test_TimeFromTicks(self):
        epochTicks = 1572851662.9782631  # Sun Nov 03 23:14:22 2019
        got = TimeFromTicks(epochTicks)
        # Since continuous integration infrastructure such as Travis CI
        # uses clocks on UTC, it is useful to be able to compare against
        # either of UTC or the known standard time.
        want = (
            datetime.time(23, 14, 22),
            datetime.datetime(2019, 11, 4, 7, 14, 22, tzUTC).time(),
        )
        matches = got in want
        self.assertTrue(matches, '`%s` not present in any of\n`%s`' % (got, want))

    def test_TimestampFromTicks(self):
        epochTicks = 1572851662.9782631  # Sun Nov 03 23:14:22 2019
        got = TimestampFromTicks(epochTicks)
        # Since continuous integration infrastructure such as Travis CI
        # uses clocks on UTC, it is useful to be able to compare against
        # either of UTC or the known standard time.
        want = (
            datetime.datetime(2019, 11, 3, 23, 14, 22),
            datetime.datetime(2019, 11, 4, 7, 14, 22, tzUTC),
        )
        matches = got in want
        self.assertTrue(matches, '`%s` not present in any of\n`%s`' % (got, want))

    def test_PeekIterator(self):
        cases = [
            ('list', [1, 2, 3, 4, 6, 7], [1, 2, 3, 4, 6, 7]),
            ('iter_from_list', iter([1, 2, 3, 4, 6, 7]), [1, 2, 3, 4, 6, 7]),
            ('tuple', ('a', 12, 0xff,), ['a', 12, 0xff]),
            ('iter_from_tuple', iter(('a', 12, 0xff,)), ['a', 12, 0xff]),
            ('no_args', (), []),
        ]

        for name, data_in, want in cases:
            with self.subTest(name=name):
                pitr = PeekIterator(data_in)
                got = list(pitr)
                self.assertEqual(got, want)
