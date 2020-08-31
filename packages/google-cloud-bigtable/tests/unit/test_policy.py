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
        VERSION = 1
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

    def test_from_pb_empty(self):
        from google.iam.v1 import policy_pb2

        empty = frozenset()
        message = policy_pb2.Policy()
        klass = self._get_target_class()
        policy = klass.from_pb(message)
        self.assertEqual(policy.etag, b"")
        self.assertEqual(policy.version, 0)
        self.assertEqual(policy.bigtable_admins, empty)
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_from_pb_non_empty(self):
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        ETAG = b"ETAG"
        VERSION = 1
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        empty = frozenset()
        message = policy_pb2.Policy(
            etag=ETAG,
            version=VERSION,
            bindings=[{"role": BIGTABLE_ADMIN_ROLE, "members": members}],
        )
        klass = self._get_target_class()
        policy = klass.from_pb(message)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(policy.bigtable_admins, set(members))
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 1)
        self.assertEqual(dict(policy), {BIGTABLE_ADMIN_ROLE: set(members)})

    def test_from_pb_with_condition(self):
        import pytest
        from google.iam.v1 import policy_pb2
        from google.api_core.iam import InvalidOperationException, _DICT_ACCESS_MSG
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        ETAG = b"ETAG"
        VERSION = 3
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        BINDINGS = [
            {
                "role": BIGTABLE_ADMIN_ROLE,
                "members": members,
                "condition": {
                    "title": "request_time",
                    "description": "Requests made before 2021-01-01T00:00:00Z",
                    "expression": 'request.time < timestamp("2021-01-01T00:00:00Z")',
                },
            }
        ]
        message = policy_pb2.Policy(
            etag=ETAG,
            version=VERSION,
            bindings=BINDINGS,
        )
        klass = self._get_target_class()
        policy = klass.from_pb(message)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(policy.bindings[0]["role"], BIGTABLE_ADMIN_ROLE)
        self.assertEqual(policy.bindings[0]["members"], set(members))
        self.assertEqual(policy.bindings[0]["condition"], BINDINGS[0]["condition"])
        with pytest.raises(InvalidOperationException, match=_DICT_ACCESS_MSG):
            policy.bigtable_admins
        with pytest.raises(InvalidOperationException, match=_DICT_ACCESS_MSG):
            policy.bigtable_readers
        with pytest.raises(InvalidOperationException, match=_DICT_ACCESS_MSG):
            policy.bigtable_users
        with pytest.raises(InvalidOperationException, match=_DICT_ACCESS_MSG):
            policy.bigtable_viewers
        with pytest.raises(InvalidOperationException, match=_DICT_ACCESS_MSG):
            len(policy)

    def test_to_pb_empty(self):
        from google.iam.v1 import policy_pb2

        policy = self._make_one()
        expected = policy_pb2.Policy()

        self.assertEqual(policy.to_pb(), expected)

    def test_to_pb_explicit(self):
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        VERSION = 1
        ETAG = b"ETAG"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        policy = self._make_one(ETAG, VERSION)
        policy[BIGTABLE_ADMIN_ROLE] = members
        expected = policy_pb2.Policy(
            etag=ETAG,
            version=VERSION,
            bindings=[
                policy_pb2.Binding(role=BIGTABLE_ADMIN_ROLE, members=sorted(members))
            ],
        )

        self.assertEqual(policy.to_pb(), expected)

    def test_to_pb_with_condition(self):
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        VERSION = 3
        ETAG = b"ETAG"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        condition = {
            "title": "request_time",
            "description": "Requests made before 2021-01-01T00:00:00Z",
            "expression": 'request.time < timestamp("2021-01-01T00:00:00Z")',
        }
        policy = self._make_one(ETAG, VERSION)
        policy.bindings = [
            {
                "role": BIGTABLE_ADMIN_ROLE,
                "members": set(members),
                "condition": condition,
            }
        ]
        expected = policy_pb2.Policy(
            etag=ETAG,
            version=VERSION,
            bindings=[
                policy_pb2.Binding(
                    role=BIGTABLE_ADMIN_ROLE,
                    members=sorted(members),
                    condition=condition,
                )
            ],
        )

        self.assertEqual(policy.to_pb(), expected)

    def test_from_api_repr_wo_etag(self):
        VERSION = 1
        empty = frozenset()
        resource = {"version": VERSION}
        klass = self._get_target_class()
        policy = klass.from_api_repr(resource)
        self.assertIsNone(policy.etag)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(policy.bigtable_admins, empty)
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_from_api_repr_w_etag(self):
        import base64

        ETAG = b"ETAG"
        empty = frozenset()
        resource = {"etag": base64.b64encode(ETAG).decode("ascii")}
        klass = self._get_target_class()
        policy = klass.from_api_repr(resource)
        self.assertEqual(policy.etag, ETAG)
        self.assertIsNone(policy.version)
        self.assertEqual(policy.bigtable_admins, empty)
        self.assertEqual(policy.bigtable_readers, empty)
        self.assertEqual(policy.bigtable_users, empty)
        self.assertEqual(policy.bigtable_viewers, empty)
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_to_api_repr_wo_etag(self):
        VERSION = 1
        resource = {"version": VERSION}
        policy = self._make_one(version=VERSION)
        self.assertEqual(policy.to_api_repr(), resource)

    def test_to_api_repr_w_etag(self):
        import base64

        ETAG = b"ETAG"
        policy = self._make_one(etag=ETAG)
        resource = {"etag": base64.b64encode(ETAG).decode("ascii")}
        self.assertEqual(policy.to_api_repr(), resource)
