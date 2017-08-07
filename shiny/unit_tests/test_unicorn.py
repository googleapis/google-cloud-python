# Copyright 2016 Google Inc.
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

import unittest


class TestUnicorn(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.shiny.unicorn import Unicorn
        return Unicorn

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        name = 'Dandelion Delightful'
        client = object()
        unicorn = self._make_one(name, client)
        self.assertEqual(unicorn._name, name)
        self.assertIs(unicorn._client, client)

    def test_name_property(self):
        name = 'Chestnut Cheeky Hooves'
        unicorn = self._make_one(name, None)
        self.assertEqual(unicorn.name, name)

    def test_client_property(self):
        client = object()
        unicorn = self._make_one(None, client)
        self.assertIs(unicorn.client, client)

    def test_do_nothing(self):
        import mock

        client = mock.Mock()
        shiny_api = mock.Mock()
        client.shiny_api = shiny_api

        name = 'Starflower Rainbow Mane'
        unicorn = self._make_one(name, client)

        # Make the request.
        self.assertIsNone(unicorn.do_nothing())

        # Verify which request was made.
        shiny_api.do_nothing.assert_called_once_with(name)
