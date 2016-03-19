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
        self.assertEqual(list(policy.writers), [])
        self.assertEqual(list(policy.readers), [])

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = 'ETAG'
        policy = self._makeOne(ETAG, VERSION)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.writers), [])
        self.assertEqual(list(policy.readers), [])

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
        self.assertEqual(list(policy.writers), [])
        self.assertEqual(list(policy.readers), [])

    def test_from_api_repr_complete(self):
        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        WRITER1 = 'domain:google.com'
        WRITER2 = 'user:phred@example.com'
        READER1 = 'serviceAccount:1234-abcdef@service.example.com'
        READER2 = 'user:phred@example.com'
        RESOURCE = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': 'roles/owner', 'members': [OWNER1, OWNER2]},
                {'role': 'roles/writer', 'members': [WRITER1, WRITER2]},
                {'role': 'roles/reader', 'members': [READER1, READER2]},
            ],
        }
        klass = self._getTargetClass()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.writers), [WRITER1, WRITER2])
        self.assertEqual(sorted(policy.readers), [READER1, READER2])

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
        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        WRITER1 = 'domain:google.com'
        WRITER2 = 'user:phred@example.com'
        READER1 = 'serviceAccount:1234-abcdef@service.example.com'
        READER2 = 'user:phred@example.com'
        EXPECTED = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': 'roles/owner', 'members': [OWNER1, OWNER2]},
                {'role': 'roles/writer', 'members': [WRITER1, WRITER2]},
                {'role': 'roles/reader', 'members': [READER1, READER2]},
            ],
        }
        policy = self._makeOne('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.writers.add(WRITER1)
        policy.writers.add(WRITER2)
        policy.readers.add(READER1)
        policy.readers.add(READER2)
        self.assertEqual(policy.to_api_repr(), EXPECTED)
