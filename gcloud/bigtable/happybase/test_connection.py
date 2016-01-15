# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest2


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.connection import Connection
        return Connection

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        connection = self._makeOne()
        self.assertEqual(connection.timeout, None)
        self.assertTrue(connection.autoconnect)
        self.assertEqual(connection.table_prefix, None)
        self.assertEqual(connection.table_prefix_separator, '_')

    def test_constructor_explicit(self):
        timeout = 12345
        autoconnect = False
        table_prefix = 'table-prefix'
        table_prefix_separator = 'sep'

        connection = self._makeOne(
            timeout=timeout,
            autoconnect=autoconnect,
            table_prefix=table_prefix,
            table_prefix_separator=table_prefix_separator)
        self.assertEqual(connection.timeout, timeout)
        self.assertFalse(connection.autoconnect)
        self.assertEqual(connection.table_prefix, table_prefix)
        self.assertEqual(connection.table_prefix_separator,
                         table_prefix_separator)

    def test_constructor_with_host(self):
        with self.assertRaises(ValueError):
            self._makeOne(host=object())

    def test_constructor_with_port(self):
        with self.assertRaises(ValueError):
            self._makeOne(port=object())

    def test_constructor_with_compat(self):
        with self.assertRaises(ValueError):
            self._makeOne(compat=object())

    def test_constructor_with_transport(self):
        with self.assertRaises(ValueError):
            self._makeOne(transport=object())

    def test_constructor_with_protocol(self):
        with self.assertRaises(ValueError):
            self._makeOne(protocol=object())

    def test_constructor_non_string_prefix(self):
        table_prefix = object()

        with self.assertRaises(TypeError):
            self._makeOne(autoconnect=False,
                          table_prefix=table_prefix)

    def test_constructor_non_string_prefix_separator(self):
        table_prefix_separator = object()

        with self.assertRaises(TypeError):
            self._makeOne(autoconnect=False,
                          table_prefix_separator=table_prefix_separator)
