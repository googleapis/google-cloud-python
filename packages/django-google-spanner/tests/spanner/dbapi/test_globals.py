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

from unittest import TestCase

from spanner.dbapi import (
        apilevel,
        paramstyle,
        threadsafety
)


class DBAPIGlobalsTests(TestCase):
    def test_apilevel(self):
        self.assertEqual(apilevel, '2.0', 'We implement PEP-0249 version 2.0')
        self.assertEqual(paramstyle, 'at-named', 'Cloud Spanner uses @param')
        self.assertEqual(threadsafety, 2, 'The module and connections can be shared across threads but not cursors')
