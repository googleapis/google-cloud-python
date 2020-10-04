# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
from time import timezone
from unittest import TestCase

from google.cloud.spanner_dbapi import types


class TypesTests(TestCase):

    TICKS = 1572822862.9782631 + timezone  # Sun 03 Nov 2019 23:14:22 UTC

    def test__date_from_ticks(self):
        actual = types._date_from_ticks(self.TICKS)
        expected = datetime.date(2019, 11, 3)

        self.assertEqual(actual, expected)

    def test__time_from_ticks(self):
        actual = types._time_from_ticks(self.TICKS)
        expected = datetime.time(23, 14, 22)

        self.assertEqual(actual, expected)

    def test__timestamp_from_ticks(self):
        actual = types._timestamp_from_ticks(self.TICKS)
        expected = datetime.datetime(2019, 11, 3, 23, 14, 22)

        self.assertEqual(actual, expected)

    def test_type_equal(self):
        self.assertEqual(types.BINARY, "TYPE_CODE_UNSPECIFIED")
        self.assertEqual(types.BINARY, "BYTES")
        self.assertEqual(types.BINARY, "ARRAY")
        self.assertEqual(types.BINARY, "STRUCT")
        self.assertNotEqual(types.BINARY, "STRING")

        self.assertEqual(types.NUMBER, "BOOL")
        self.assertEqual(types.NUMBER, "INT64")
        self.assertEqual(types.NUMBER, "FLOAT64")
        self.assertEqual(types.NUMBER, "NUMERIC")
        self.assertNotEqual(types.NUMBER, "STRING")

        self.assertEqual(types.DATETIME, "TIMESTAMP")
        self.assertEqual(types.DATETIME, "DATE")
        self.assertNotEqual(types.DATETIME, "STRING")
