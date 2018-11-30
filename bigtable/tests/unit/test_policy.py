# Copyright 2018 Google LLC
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


class TestPolicy(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.policy import Policy

        return Policy

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        empty = frozenset()
        policy = self._make_one()
        self.assertIsNone(policy.etag)
        self.assertIsNone(policy.version)
        self.assertEqual(policy.bigtable_admins, empty)
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = b"ETAG"
        empty = frozenset()
        policy = self._make_one(ETAG, VERSION)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(policy.bigtable_admins, empty)
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_bigtable_admins_getter(self):
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[BIGTABLE_ADMIN_ROLE] = [MEMBER]
        self.assertEqual(policy.bigtable_admins, expected)

    def test_bigtable_readers_getter(self):
        from google.cloud.bigtable.policy import BIGTABLE_READER_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[BIGTABLE_READER_ROLE] = [MEMBER]
        self.assertEqual(policy.bigtable_readers, expected)

    def test_bigtable_users_getter(self):
        from google.cloud.bigtable.policy import BIGTABLE_USER_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[BIGTABLE_USER_ROLE] = [MEMBER]
        self.assertEqual(policy.bigtable_users, expected)

    def test_bigtable_viewers_getter(self):
        from google.cloud.bigtable.policy import BIGTABLE_VIEWER_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[BIGTABLE_VIEWER_ROLE] = [MEMBER]
        self.assertEqual(policy.bigtable_viewers, expected)
