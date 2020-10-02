# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
import time
from unittest import TestCase

from google.cloud.spanner_dbapi.types import (
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)
from google.cloud.spanner_dbapi.utils import PeekIterator


utcOffset = time.timezone  # offset for current timezone


class TypesTests(TestCase):
    def test_Date(self):
        actual = Date(2019, 11, 3)
        expected = datetime.date(2019, 11, 3)
        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_Time(self):
        actual = Time(23, 8, 19)
        expected = datetime.time(23, 8, 19)
        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_Timestamp(self):
        actual = Timestamp(2019, 11, 3, 23, 8, 19)
        expected = datetime.datetime(2019, 11, 3, 23, 8, 19)
        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_DateFromTicks(self):
        epochTicks = 1572822862  # Sun Nov 03 23:14:22 2019 GMT

        actual = DateFromTicks(epochTicks + utcOffset)
        expected = datetime.date(2019, 11, 3)

        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_TimeFromTicks(self):
        epochTicks = 1572822862  # Sun Nov 03 23:14:22 2019 GMT

        actual = TimeFromTicks(epochTicks + utcOffset)
        expected = datetime.time(23, 14, 22)

        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_TimestampFromTicks(self):
        epochTicks = 1572822862  # Sun Nov 03 23:14:22 2019 GMT

        actual = TimestampFromTicks(epochTicks + utcOffset)
        expected = datetime.datetime(2019, 11, 3, 23, 14, 22)

        self.assertEqual(actual, expected, "mismatch between conversion")

    def test_PeekIterator(self):
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
