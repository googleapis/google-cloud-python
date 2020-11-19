# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC All rights reserved.
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


class TestLoggingShim(unittest.TestCase):
    def test_shim_matches_logging_v2(self):
        from google.cloud import logging
        from google.cloud import logging_v2

        self.assertEqual(logging.__all__, logging_v2.__all__)

        for name in logging.__all__:
            found = getattr(logging, name)
            expected = getattr(logging_v2, name)
            self.assertIs(found, expected)
