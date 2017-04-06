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
        self.assertIsInstance(policy.owners, frozenset)
        self.assertEqual(list(policy.owners), [])
        self.assertIsInstance(policy.editors, frozenset)
        self.assertEqual(list(policy.editors), [])
        self.assertIsInstance(policy.viewers, frozenset)
        self.assertEqual(list(policy.viewers), [])
        self.assertIsInstance(policy.publishers, frozenset)
        self.assertEqual(list(policy.publishers), [])
        self.assertIsInstance(policy.subscribers, frozenset)
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

    def test_publishers_setter(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_PUBLISHER_ROLE,
        )
        PUBLISHER = 'user:phred@example.com'
        policy = self._make_one()
        policy.publishers = [PUBLISHER]

        self.assertEqual(sorted(policy.publishers), [PUBLISHER])
        self.assertEqual(
            dict(policy), {PUBSUB_PUBLISHER_ROLE: [PUBLISHER]})

    def test_subscribers_setter(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_SUBSCRIBER_ROLE,
        )
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        policy = self._make_one()
        policy.subscribers = [SUBSCRIBER]

        self.assertEqual(sorted(policy.subscribers), [SUBSCRIBER])
        self.assertEqual(
            dict(policy), {PUBSUB_SUBSCRIBER_ROLE: [SUBSCRIBER]})
