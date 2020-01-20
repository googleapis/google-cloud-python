# Copyright (c) 2020 Google LLC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from unittest import TestCase

from spanner.dbapi import apilevel, paramstyle, threadsafety


class DBAPIGlobalsTests(TestCase):
    def test_apilevel(self):
        self.assertEqual(apilevel, '2.0', 'We implement PEP-0249 version 2.0')
        self.assertEqual(paramstyle, 'at-named', 'Cloud Spanner uses @param')
        self.assertEqual(threadsafety, 2, 'The module and connections can be shared across threads but not cursors')
