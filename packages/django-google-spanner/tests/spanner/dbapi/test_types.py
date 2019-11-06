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

from spanner.dbapi.types import (
    Date, DateFromTicks, Time, TimeFromTicks, Timestamp, TimestampFromTicks,
)


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
        want = datetime.date(2019, 11, 3)
        self.assertEqual(got, want, 'mismatch between conversion')

    def test_TimeFromTicks(self):
        epochTicks = 1572851662.9782631  # Sun Nov 03 23:14:22 2019
        got = TimeFromTicks(epochTicks)
        want = datetime.time(23, 14, 22)
        self.assertEqual(got, want, 'mismatch between conversion')

    def test_TimestampFromTicks(self):
        epochTicks = 1572851662.9782631  # Sun Nov 03 23:14:22 2019
        got = TimestampFromTicks(epochTicks)
        want = datetime.datetime(2019, 11, 3, 23, 14, 22)
        self.assertEqual(got, want, 'mismatch between conversion')
