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


class TestPolicy(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.iam import Policy
        return Policy

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        policy = self._makeOne()
        self.assertEqual(policy.etag, None)
        self.assertEqual(policy.version, None)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(list(policy.publishers), [])
        self.assertEqual(list(policy.subscribers), [])

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = 'ETAG'
        policy = self._makeOne(ETAG, VERSION)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(list(policy.publishers), [])
        self.assertEqual(list(policy.subscribers), [])

    def test_user(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'user:%s' % (EMAIL,)
        policy = self._makeOne()
        self.assertEqual(policy.user(EMAIL), MEMBER)

    def test_service_account(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'serviceAccount:%s' % (EMAIL,)
        policy = self._makeOne()
        self.assertEqual(policy.service_account(EMAIL), MEMBER)

    def test_group(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'group:%s' % (EMAIL,)
        policy = self._makeOne()
        self.assertEqual(policy.group(EMAIL), MEMBER)

    def test_domain(self):
        DOMAIN = 'example.com'
        MEMBER = 'domain:%s' % (DOMAIN,)
        policy = self._makeOne()
        self.assertEqual(policy.domain(DOMAIN), MEMBER)

    def test_all_users(self):
        policy = self._makeOne()
        self.assertEqual(policy.all_users(), 'allUsers')

    def test_authenticated_users(self):
        policy = self._makeOne()
        self.assertEqual(policy.authenticated_users(), 'allAuthenticatedUsers')

    def test_from_api_repr_only_etag(self):
        RESOURCE = {
            'etag': 'ACAB',
        }
        klass = self._getTargetClass()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'ACAB')
        self.assertEqual(policy.version, None)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])

    def test_from_api_repr_complete(self):
        from gcloud.pubsub.iam import (
            OWNER_ROLE,
            EDITOR_ROLE,
            VIEWER_ROLE,
            PUBSUB_PUBLISHER_ROLE,
            PUBSUB_SUBSCRIBER_ROLE,
        )
        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        PUBLISHER = 'user:phred@example.com'
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        RESOURCE = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
                {'role': PUBSUB_PUBLISHER_ROLE, 'members': [PUBLISHER]},
                {'role': PUBSUB_SUBSCRIBER_ROLE, 'members': [SUBSCRIBER]},
            ],
        }
        klass = self._getTargetClass()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(sorted(policy.publishers), [PUBLISHER])
        self.assertEqual(sorted(policy.subscribers), [SUBSCRIBER])

    def test_from_api_repr_bad_role(self):
        BOGUS1 = 'user:phred@example.com'
        BOGUS2 = 'group:cloud-logs@google.com'
        RESOURCE = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': 'nonesuch', 'members': [BOGUS1, BOGUS2]},
            ],
        }
        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_api_repr(RESOURCE)

    def test_to_api_repr_defaults(self):
        policy = self._makeOne()
        self.assertEqual(policy.to_api_repr(), {})

    def test_to_api_repr_only_etag(self):
        policy = self._makeOne('DEADBEEF')
        self.assertEqual(policy.to_api_repr(), {'etag': 'DEADBEEF'})

    def test_to_api_repr_full(self):
        from gcloud.pubsub.iam import (
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
        EXPECTED = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': PUBSUB_ADMIN_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': PUBSUB_EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': PUBSUB_VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
                {'role': PUBSUB_PUBLISHER_ROLE, 'members': [PUBLISHER]},
                {'role': PUBSUB_SUBSCRIBER_ROLE, 'members': [SUBSCRIBER]},
            ],
        }
        policy = self._makeOne('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)
        policy.publishers.add(PUBLISHER)
        policy.subscribers.add(SUBSCRIBER)
        self.assertEqual(policy.to_api_repr(), EXPECTED)
