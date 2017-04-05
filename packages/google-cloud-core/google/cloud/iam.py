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
"""Non-API-specific IAM policy definitions

For allowed roles / permissions, see:
https://cloud.google.com/iam/docs/understanding-roles
"""

# Generic IAM roles

OWNER_ROLE = 'roles/owner'
"""Generic role implying all rights to an object."""

EDITOR_ROLE = 'roles/editor'
"""Generic role implying rights to modify an object."""

VIEWER_ROLE = 'roles/viewer'
"""Generic role implying rights to access an object."""


class Policy(object):
    """IAM Policy

    See:
    https://cloud.google.com/iam/reference/rest/v1/Policy

    :type etag: str
    :param etag: ETag used to identify a unique of the policy

    :type version: int
    :param version: unique version of the policy
    """
    _OWNER_ROLES = (OWNER_ROLE,)
    """Roles mapped onto our ``owners`` attribute."""

    _EDITOR_ROLES = (EDITOR_ROLE,)
    """Roles mapped onto our ``editors`` attribute."""

    _VIEWER_ROLES = (VIEWER_ROLE,)
    """Roles mapped onto our ``viewers`` attribute."""

    def __init__(self, etag=None, version=None):
        self.etag = etag
        self.version = version
        self.bindings = {}

    @property
    def owners(self):
        """Legacy access to owner role."""
        result = set()
        for role in self._OWNER_ROLES:
            for member in self.bindings.get(role, ()):
                result.add(member)
        return frozenset(result)

    @owners.setter
    def owners(self, value):
        """Update owners."""
        self.bindings[OWNER_ROLE] = list(value)

    @property
    def editors(self):
        """Legacy access to editor role."""
        result = set()
        for role in self._EDITOR_ROLES:
            for member in self.bindings.get(role, ()):
                result.add(member)
        return frozenset(result)

    @editors.setter
    def editors(self, value):
        """Update editors."""
        self.bindings[EDITOR_ROLE] = list(value)

    @property
    def viewers(self):
        """Legacy access to viewer role."""
        result = set()
        for role in self._VIEWER_ROLES:
            for member in self.bindings.get(role, ()):
                result.add(member)
        return frozenset(result)

    @viewers.setter
    def viewers(self, value):
        """Update viewers."""
        self.bindings[VIEWER_ROLE] = list(value)

    @staticmethod
    def user(email):
        """Factory method for a user member.

        :type email: str
        :param email: E-mail for this particular user.

        :rtype: str
        :returns: A member string corresponding to the given user.
        """
        return 'user:%s' % (email,)

    @staticmethod
    def service_account(email):
        """Factory method for a service account member.

        :type email: str
        :param email: E-mail for this particular service account.

        :rtype: str
        :returns: A member string corresponding to the given service account.
        """
        return 'serviceAccount:%s' % (email,)

    @staticmethod
    def group(email):
        """Factory method for a group member.

        :type email: str
        :param email: An id or e-mail for this particular group.

        :rtype: str
        :returns: A member string corresponding to the given group.
        """
        return 'group:%s' % (email,)

    @staticmethod
    def domain(domain):
        """Factory method for a domain member.

        :type domain: str
        :param domain: The domain for this member.

        :rtype: str
        :returns: A member string corresponding to the given domain.
        """
        return 'domain:%s' % (domain,)

    @staticmethod
    def all_users():
        """Factory method for a member representing all users.

        :rtype: str
        :returns: A member string representing all users.
        """
        return 'allUsers'

    @staticmethod
    def authenticated_users():
        """Factory method for a member representing all authenticated users.

        :rtype: str
        :returns: A member string representing all authenticated users.
        """
        return 'allAuthenticatedUsers'

    @classmethod
    def from_api_repr(cls, resource):
        """Create a policy from the resource returned from the API.

        :type resource: dict
        :param resource: resource returned from the ``getIamPolicy`` API.

        :rtype: :class:`Policy`
        :returns: the parsed policy
        """
        version = resource.get('version')
        etag = resource.get('etag')
        policy = cls(etag, version)
        for binding in resource.get('bindings', ()):
            role = binding['role']
            members = sorted(binding['members'])
            policy.bindings[role] = members
        return policy

    def to_api_repr(self):
        """Construct a Policy resource.

        :rtype: dict
        :returns: a resource to be passed to the ``setIamPolicy`` API.
        """
        resource = {}

        if self.etag is not None:
            resource['etag'] = self.etag

        if self.version is not None:
            resource['version'] = self.version

        if len(self.bindings) > 0:
            bindings = resource['bindings'] = []
            for role, members in sorted(self.bindings.items()):
                if len(members) > 0:
                    bindings.append(
                        {'role': role, 'members': sorted(set(members))})

            if len(bindings) == 0:
                del resource['bindings']

        return resource
