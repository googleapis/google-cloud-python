# Copyright 2017 Google Inc.
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
        from google.cloud.iam import Policy

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
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = 'ETAG'
        policy = self._make_one(ETAG, VERSION)
        self.assertEqual(policy.etag, ETAG)
        self.assertEqual(policy.version, VERSION)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test___getitem___miss(self):
        policy = self._make_one()
        with self.assertRaises(KeyError):
            policy['nonesuch']

    def test___setitem__(self):
        USER = 'user:phred@example.com'
        policy = self._make_one()
        policy['rolename'] = [USER]
        self.assertEqual(policy['rolename'], [USER])
        self.assertEqual(len(policy), 1)
        self.assertEqual(dict(policy), {'rolename': [USER]})

    def test___delitem___hit(self):
        policy = self._make_one()
        policy._bindings['rolename'] = ['phred@example.com']
        del policy['rolename']
        self.assertEqual(len(policy), 0)
        self.assertEqual(dict(policy), {})

    def test___delitem___miss(self):
        policy = self._make_one()
        with self.assertRaises(KeyError):
            del policy['nonesuch']

    def test_owners_getter(self):
        from google.cloud.iam import OWNER_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        policy[OWNER_ROLE] = [MEMBER]
        self.assertIsInstance(policy.owners, frozenset)
        self.assertEqual(list(policy.owners), [MEMBER])

    def test_owners_setter(self):
        import warnings
        from google.cloud.iam import OWNER_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        with warnings.catch_warnings():
            policy.owners = [MEMBER]
        self.assertEqual(list(policy[OWNER_ROLE]), [MEMBER])

    def test_editors_getter(self):
        from google.cloud.iam import EDITOR_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        policy[EDITOR_ROLE] = [MEMBER]
        self.assertIsInstance(policy.editors, frozenset)
        self.assertEqual(list(policy.editors), [MEMBER])

    def test_editors_setter(self):
        import warnings
        from google.cloud.iam import EDITOR_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        with warnings.catch_warnings():
            policy.editors = [MEMBER]
        self.assertEqual(list(policy[EDITOR_ROLE]), [MEMBER])

    def test_viewers_getter(self):
        from google.cloud.iam import VIEWER_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        policy[VIEWER_ROLE] = [MEMBER]
        self.assertIsInstance(policy.viewers, frozenset)
        self.assertEqual(list(policy.viewers), [MEMBER])

    def test_viewers_setter(self):
        import warnings
        from google.cloud.iam import VIEWER_ROLE
        MEMBER = 'user:phred@example.com'
        policy = self._make_one()
        with warnings.catch_warnings():
            warnings.simplefilter('always')
            policy.viewers = [MEMBER]
        self.assertEqual(list(policy[VIEWER_ROLE]), [MEMBER])

    def test_user(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'user:%s' % (EMAIL,)
        policy = self._make_one()
        self.assertEqual(policy.user(EMAIL), MEMBER)

    def test_service_account(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'serviceAccount:%s' % (EMAIL,)
        policy = self._make_one()
        self.assertEqual(policy.service_account(EMAIL), MEMBER)

    def test_group(self):
        EMAIL = 'phred@example.com'
        MEMBER = 'group:%s' % (EMAIL,)
        policy = self._make_one()
        self.assertEqual(policy.group(EMAIL), MEMBER)

    def test_domain(self):
        DOMAIN = 'example.com'
        MEMBER = 'domain:%s' % (DOMAIN,)
        policy = self._make_one()
        self.assertEqual(policy.domain(DOMAIN), MEMBER)

    def test_all_users(self):
        policy = self._make_one()
        self.assertEqual(policy.all_users(), 'allUsers')

    def test_authenticated_users(self):
        policy = self._make_one()
        self.assertEqual(policy.authenticated_users(), 'allAuthenticatedUsers')

    def test_from_api_repr_only_etag(self):
        RESOURCE = {
            'etag': 'ACAB',
        }
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'ACAB')
        self.assertIsNone(policy.version)
        self.assertEqual(list(policy.owners), [])
        self.assertEqual(list(policy.editors), [])
        self.assertEqual(list(policy.viewers), [])
        self.assertEqual(dict(policy), {})

    def test_from_api_repr_complete(self):
        from google.cloud.iam import (
            OWNER_ROLE,
            EDITOR_ROLE,
            VIEWER_ROLE,
        )

        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        RESOURCE = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER1, OWNER2])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(
            dict(policy), {
                OWNER_ROLE: [OWNER1, OWNER2],
                EDITOR_ROLE: [EDITOR1, EDITOR2],
                VIEWER_ROLE: [VIEWER1, VIEWER2],
            })

    def test_from_api_repr_unknown_role(self):
        USER = 'user:phred@example.com'
        GROUP = 'group:cloud-logs@google.com'
        RESOURCE = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': 'unknown', 'members': [USER, GROUP]},
            ],
        }
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(dict(policy), {'unknown': [GROUP, USER]})

    def test_to_api_repr_defaults(self):
        policy = self._make_one()
        self.assertEqual(policy.to_api_repr(), {})

    def test_to_api_repr_only_etag(self):
        policy = self._make_one('DEADBEEF')
        self.assertEqual(policy.to_api_repr(), {'etag': 'DEADBEEF'})

    def test_to_api_repr_binding_wo_members(self):
        policy = self._make_one()
        policy['empty'] = []
        self.assertEqual(policy.to_api_repr(), {})

    def test_to_api_repr_binding_w_duplicates(self):
        from google.cloud.iam import OWNER_ROLE

        OWNER = 'group:cloud-logs@google.com'
        policy = self._make_one()
        policy.owners = [OWNER, OWNER]
        self.assertEqual(
            policy.to_api_repr(), {
                'bindings': [{'role': OWNER_ROLE, 'members': [OWNER]}],
            })

    def test_to_api_repr_full(self):
        import operator
        from google.cloud.iam import (
            OWNER_ROLE,
            EDITOR_ROLE,
            VIEWER_ROLE,
        )

        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        BINDINGS = [
            {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
            {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
            {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
        ]
        policy = self._make_one('DEADBEEF', 17)
        policy.owners = [OWNER1, OWNER2]
        policy.editors = [EDITOR1, EDITOR2]
        policy.viewers = [VIEWER1, VIEWER2]
        resource = policy.to_api_repr()
        self.assertEqual(resource['etag'], 'DEADBEEF')
        self.assertEqual(resource['version'], 17)
        key = operator.itemgetter('role')
        self.assertEqual(
            sorted(resource['bindings'], key=key), sorted(BINDINGS, key=key))
