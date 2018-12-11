# Copyright 2017 Google LLC
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

import pytest


class TestPolicy:
    @staticmethod
    def _get_target_class():
        from google.api_core.iam import Policy

        return Policy

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        empty = frozenset()
        policy = self._make_one()
        assert policy.etag is None
        assert policy.version is None
        assert policy.owners == empty
        assert policy.editors == empty
        assert policy.viewers == empty
        assert len(policy) == 0
        assert dict(policy) == {}

    def test_ctor_explicit(self):
        VERSION = 17
        ETAG = "ETAG"
        empty = frozenset()
        policy = self._make_one(ETAG, VERSION)
        assert policy.etag == ETAG
        assert policy.version == VERSION
        assert policy.owners == empty
        assert policy.editors == empty
        assert policy.viewers == empty
        assert len(policy) == 0
        assert dict(policy) == {}

    def test___getitem___miss(self):
        policy = self._make_one()
        assert policy["nonesuch"] == set()

    def test___setitem__(self):
        USER = "user:phred@example.com"
        PRINCIPALS = set([USER])
        policy = self._make_one()
        policy["rolename"] = [USER]
        assert policy["rolename"] == PRINCIPALS
        assert len(policy) == 1
        assert dict(policy) == {"rolename": PRINCIPALS}

    def test___delitem___hit(self):
        policy = self._make_one()
        policy._bindings["rolename"] = ["phred@example.com"]
        del policy["rolename"]
        assert len(policy) == 0
        assert dict(policy) == {}

    def test___delitem___miss(self):
        policy = self._make_one()
        with pytest.raises(KeyError):
            del policy["nonesuch"]

    def test_owners_getter(self):
        from google.api_core.iam import OWNER_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[OWNER_ROLE] = [MEMBER]
        assert policy.owners == expected

    def test_owners_setter(self):
        import warnings
        from google.api_core.iam import OWNER_ROLE

        MEMBER = "user:phred@example.com"
        expected = set([MEMBER])
        policy = self._make_one()

        with warnings.catch_warnings(record=True) as warned:
            policy.owners = [MEMBER]

        warning, = warned
        assert warning.category is DeprecationWarning
        assert policy[OWNER_ROLE] == expected

    def test_editors_getter(self):
        from google.api_core.iam import EDITOR_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[EDITOR_ROLE] = [MEMBER]
        assert policy.editors == expected

    def test_editors_setter(self):
        import warnings
        from google.api_core.iam import EDITOR_ROLE

        MEMBER = "user:phred@example.com"
        expected = set([MEMBER])
        policy = self._make_one()

        with warnings.catch_warnings(record=True) as warned:
            policy.editors = [MEMBER]

        warning, = warned
        assert warning.category is DeprecationWarning
        assert policy[EDITOR_ROLE] == expected

    def test_viewers_getter(self):
        from google.api_core.iam import VIEWER_ROLE

        MEMBER = "user:phred@example.com"
        expected = frozenset([MEMBER])
        policy = self._make_one()
        policy[VIEWER_ROLE] = [MEMBER]
        assert policy.viewers == expected

    def test_viewers_setter(self):
        import warnings
        from google.api_core.iam import VIEWER_ROLE

        MEMBER = "user:phred@example.com"
        expected = set([MEMBER])
        policy = self._make_one()

        with warnings.catch_warnings(record=True) as warned:
            policy.viewers = [MEMBER]

        warning, = warned
        assert warning.category is DeprecationWarning
        assert policy[VIEWER_ROLE] == expected

    def test_user(self):
        EMAIL = "phred@example.com"
        MEMBER = "user:%s" % (EMAIL,)
        policy = self._make_one()
        assert policy.user(EMAIL) == MEMBER

    def test_service_account(self):
        EMAIL = "phred@example.com"
        MEMBER = "serviceAccount:%s" % (EMAIL,)
        policy = self._make_one()
        assert policy.service_account(EMAIL) == MEMBER

    def test_group(self):
        EMAIL = "phred@example.com"
        MEMBER = "group:%s" % (EMAIL,)
        policy = self._make_one()
        assert policy.group(EMAIL) == MEMBER

    def test_domain(self):
        DOMAIN = "example.com"
        MEMBER = "domain:%s" % (DOMAIN,)
        policy = self._make_one()
        assert policy.domain(DOMAIN) == MEMBER

    def test_all_users(self):
        policy = self._make_one()
        assert policy.all_users() == "allUsers"

    def test_authenticated_users(self):
        policy = self._make_one()
        assert policy.authenticated_users() == "allAuthenticatedUsers"

    def test_from_api_repr_only_etag(self):
        empty = frozenset()
        RESOURCE = {"etag": "ACAB"}
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        assert policy.etag == "ACAB"
        assert policy.version is None
        assert policy.owners == empty
        assert policy.editors == empty
        assert policy.viewers == empty
        assert dict(policy) == {}

    def test_from_api_repr_complete(self):
        from google.api_core.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE

        OWNER1 = "group:cloud-logs@google.com"
        OWNER2 = "user:phred@example.com"
        EDITOR1 = "domain:google.com"
        EDITOR2 = "user:phred@example.com"
        VIEWER1 = "serviceAccount:1234-abcdef@service.example.com"
        VIEWER2 = "user:phred@example.com"
        RESOURCE = {
            "etag": "DEADBEEF",
            "version": 17,
            "bindings": [
                {"role": OWNER_ROLE, "members": [OWNER1, OWNER2]},
                {"role": EDITOR_ROLE, "members": [EDITOR1, EDITOR2]},
                {"role": VIEWER_ROLE, "members": [VIEWER1, VIEWER2]},
            ],
        }
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        assert policy.etag == "DEADBEEF"
        assert policy.version == 17
        assert policy.owners, frozenset([OWNER1 == OWNER2])
        assert policy.editors, frozenset([EDITOR1 == EDITOR2])
        assert policy.viewers, frozenset([VIEWER1 == VIEWER2])
        assert dict(policy) == {
            OWNER_ROLE: set([OWNER1, OWNER2]),
            EDITOR_ROLE: set([EDITOR1, EDITOR2]),
            VIEWER_ROLE: set([VIEWER1, VIEWER2]),
        }

    def test_from_api_repr_unknown_role(self):
        USER = "user:phred@example.com"
        GROUP = "group:cloud-logs@google.com"
        RESOURCE = {
            "etag": "DEADBEEF",
            "version": 17,
            "bindings": [{"role": "unknown", "members": [USER, GROUP]}],
        }
        klass = self._get_target_class()
        policy = klass.from_api_repr(RESOURCE)
        assert policy.etag == "DEADBEEF"
        assert policy.version == 17
        assert dict(policy), {"unknown": set([GROUP == USER])}

    def test_to_api_repr_defaults(self):
        policy = self._make_one()
        assert policy.to_api_repr() == {}

    def test_to_api_repr_only_etag(self):
        policy = self._make_one("DEADBEEF")
        assert policy.to_api_repr() == {"etag": "DEADBEEF"}

    def test_to_api_repr_binding_wo_members(self):
        policy = self._make_one()
        policy["empty"] = []
        assert policy.to_api_repr() == {}

    def test_to_api_repr_binding_w_duplicates(self):
        import warnings
        from google.api_core.iam import OWNER_ROLE

        OWNER = "group:cloud-logs@google.com"
        policy = self._make_one()
        with warnings.catch_warnings(record=True):
            policy.owners = [OWNER, OWNER]
        assert policy.to_api_repr() == {
            "bindings": [{"role": OWNER_ROLE, "members": [OWNER]}]
        }

    def test_to_api_repr_full(self):
        import operator
        import warnings
        from google.api_core.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE

        OWNER1 = "group:cloud-logs@google.com"
        OWNER2 = "user:phred@example.com"
        EDITOR1 = "domain:google.com"
        EDITOR2 = "user:phred@example.com"
        VIEWER1 = "serviceAccount:1234-abcdef@service.example.com"
        VIEWER2 = "user:phred@example.com"
        BINDINGS = [
            {"role": OWNER_ROLE, "members": [OWNER1, OWNER2]},
            {"role": EDITOR_ROLE, "members": [EDITOR1, EDITOR2]},
            {"role": VIEWER_ROLE, "members": [VIEWER1, VIEWER2]},
        ]
        policy = self._make_one("DEADBEEF", 17)
        with warnings.catch_warnings(record=True):
            policy.owners = [OWNER1, OWNER2]
            policy.editors = [EDITOR1, EDITOR2]
            policy.viewers = [VIEWER1, VIEWER2]
        resource = policy.to_api_repr()
        assert resource["etag"] == "DEADBEEF"
        assert resource["version"] == 17
        key = operator.itemgetter("role")
        assert sorted(resource["bindings"], key=key) == sorted(BINDINGS, key=key)
