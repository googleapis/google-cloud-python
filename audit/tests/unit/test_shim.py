# -*- coding: utf-8 -*-
#
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


import unittest


class Test_shim_messages(unittest.TestCase):
    def _get_module_under_test(self):
        from google.cloud import audit

        return audit

    def test_messages_have_remapped_module_name(self):
        from google.cloud.audit.proto import audit_log_pb2

        audit = self._get_module_under_test()

        for name in audit.__all__:
            found = getattr(audit, name)
            expected = getattr(audit_log_pb2, name)
            self.assertIs(found, expected)
            self.assertEqual(found.__module__, audit_log_pb2.__name__)
