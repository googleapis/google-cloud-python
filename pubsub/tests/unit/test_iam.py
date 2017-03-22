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


class TestPolicy(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.iam import Policy

        return Policy

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        policy = self._make_one()
        self.assertIsNone(policy.etag)
        self.assertIsNone(policy.version)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(list(policy.publishers), [])
        self.assertEqual(list(policy.subscribers), [])

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = 'ETAG'
        policy = self._make_one(ETAG, VERSION)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(list(policy.publishers), [])
        self.assertEqual(list(policy.subscribers), [])

    def test__bind_custom_role_publisher(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_PUBLISHER_ROLE,
        )
        PUBLISHER = 'user:phred@example.com'
        policy = self._make_one()
        policy._bind_custom_role(PUBSUB_PUBLISHER_ROLE, set([PUBLISHER]))

        self.assertEqual(sorted(policy.publishers), [PUBLISHER])

    def test__bind_custom_role_subscriber(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_SUBSCRIBER_ROLE,
        )
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        policy = self._make_one()
        policy._bind_custom_role(PUBSUB_SUBSCRIBER_ROLE, set([SUBSCRIBER]))

        self.assertEqual(sorted(policy.subscribers), [SUBSCRIBER])

    def test__bind_custom_role_unknown(self):
        policy = self._make_one()
        USER = 'user:phred@example.com'
        with self.assertRaises(ValueError):
            policy._bind_custom_role('nonesuch', set([USER]))

    def test__role_bindings(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_ADMIN_ROLE,
            PUBSUB_EDITOR_ROLE,
            PUBSUB_VIEWER_ROLE,
            PUBSUB_PUBLISHER_ROLE,
            PUBSUB_SUBSCRIBER_ROLE,
        )

        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        PUBLISHER = 'user:phred@example.com'
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        EXPECTED = [
            {'role': PUBSUB_ADMIN_ROLE, 'members': [OWNER1, OWNER2]},
            {'role': PUBSUB_EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
            {'role': PUBSUB_VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            {'role': PUBSUB_PUBLISHER_ROLE, 'members': [PUBLISHER]},
            {'role': PUBSUB_SUBSCRIBER_ROLE, 'members': [SUBSCRIBER]},
        ]
        policy = self._make_one('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)
        policy.publishers.add(PUBLISHER)
        policy.subscribers.add(SUBSCRIBER)
        self.assertEqual(policy._role_bindings(), EXPECTED)
