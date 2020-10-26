# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import unittest


class TestDBAPIGlobals(unittest.TestCase):
    def test_apilevel(self):
        from google.cloud.spanner_dbapi import apilevel
        from google.cloud.spanner_dbapi import paramstyle
        from google.cloud.spanner_dbapi import threadsafety

        self.assertEqual(apilevel, "2.0", "We implement PEP-0249 version 2.0")
        self.assertEqual(paramstyle, "format", "Cloud Spanner uses @param")
        self.assertEqual(
            threadsafety, 1, "Threads may share module but not connections"
        )
