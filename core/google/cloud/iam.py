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
        self.owners = set()
        self.editors = set()
        self.viewers = set()

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

    def _bind_custom_role(self, role, members):  # pylint: disable=no-self-use
        """Bind an API-specific role to members.

        Helper for :meth:`from_api_repr`.

        :type role: str
        :param role: role to bind.

        :type members: set of str
        :param members: member IDs to be bound to the role.

        Subclasses may override.
        """
        raise ValueError(
            'Unknown binding: role=%s, members=%s' % (role, members))

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
            members = set(binding['members'])
            if role in cls._OWNER_ROLES:
                policy.owners |= members
            elif role in cls._EDITOR_ROLES:
                policy.editors |= members
            elif role in cls._VIEWER_ROLES:
                policy.viewers |= members
            else:
                policy._bind_custom_role(role, members)
        return policy

    def _role_bindings(self):
        """Enumerate members bound to roles for the policy.

        Helper for :meth:`to_api_repr`.

        :rtype: list of mapping
        :returns: zero or more mappings describing roles / members bound by
                  the policy.

        Subclasses may override.
        """
        bindings = []

        if self.owners:
            bindings.append(
                {'role': OWNER_ROLE,
                 'members': sorted(self.owners)})

        if self.editors:
            bindings.append(
                {'role': EDITOR_ROLE,
                 'members': sorted(self.editors)})

        if self.viewers:
            bindings.append(
                {'role': VIEWER_ROLE,
                 'members': sorted(self.viewers)})

        return bindings

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

        bindings = self._role_bindings()

        if bindings:
            resource['bindings'] = bindings

        return resource
