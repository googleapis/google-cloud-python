# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from unittest import TestCase

from spanner.dbapi import apilevel, paramstyle, threadsafety


class DBAPIGlobalsTests(TestCase):
    def test_apilevel(self):
        self.assertEqual(apilevel, '2.0', 'We implement PEP-0249 version 2.0')
        self.assertEqual(paramstyle, 'at-named', 'Cloud Spanner uses @param')
        self.assertEqual(threadsafety, 0, 'Downgraded to the least concurrency')
