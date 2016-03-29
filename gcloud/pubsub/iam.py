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
"""PubSub API IAM policy definitions"""

OWNER_ROLE = 'roles/owner'
"""IAM permission implying all rights to an object."""

EDITOR_ROLE = 'roles/editor'
"""IAM permission implying rights to modify an object."""

VIEWER_ROLE = 'roles/viewer'
"""IAM permission implying rights to access an object without modifying it."""


class Policy(object):
    """Combined IAM Policy / Bindings.

    See:
    https://cloud.google.com/pubsub/reference/rest/Shared.Types/Policy
    https://cloud.google.com/pubsub/reference/rest/Shared.Types/Binding

    :type etag: string
    :param etag: ETag used to identify a unique of the policy

    :type version: int
    :param version: unique version of the policy
    """
    def __init__(self, etag=None, version=None):
        self.etag = etag
        self.version = version
        self.owners = set()
        self.editors = set()
        self.viewers = set()

    @staticmethod
    def user(email):
        """Factory method for a user member.

        :type email: string
        :param email: E-mail for this particular user.

        :rtype: string
        :returns: A member string corresponding to the given user.
        """
        return 'user:%s' % (email,)

    @staticmethod
    def service_account(email):
        """Factory method for a service account member.

        :type email: string
        :param email: E-mail for this particular service account.

        :rtype: string
        :returns: A member string corresponding to the given service account.
        """
        return 'serviceAccount:%s' % (email,)

    @staticmethod
    def group(email):
        """Factory method for a group member.

        :type email: string
        :param email: An id or e-mail for this particular group.

        :rtype: string
        :returns: A member string corresponding to the given group.
        """
        return 'group:%s' % (email,)

    @staticmethod
    def domain(domain):
        """Factory method for a domain member.

        :type domain: string
        :param domain: The domain for this member.

        :rtype: string
        :returns: A member string corresponding to the given domain.
        """
        return 'domain:%s' % (domain,)

    @staticmethod
    def all_users():
        """Factory method for a member representing all users.

        :rtype: string
        :returns: A member string representing all users.
        """
        return 'allUsers'

    @staticmethod
    def authenticated_users():
        """Factory method for a member representing all authenticated users.

        :rtype: string
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
            members = set(binding['members'])
            if role == OWNER_ROLE:
                policy.owners = members
            elif role == EDITOR_ROLE:
                policy.editors = members
            elif role == VIEWER_ROLE:
                policy.viewers = members
            else:
                raise ValueError('Unknown role: %s' % (role,))
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

        bindings = []

        if self.owners:
            bindings.append(
                {'role': OWNER_ROLE, 'members': sorted(self.owners)})

        if self.editors:
            bindings.append(
                {'role': EDITOR_ROLE, 'members': sorted(self.editors)})

        if self.viewers:
            bindings.append(
                {'role': VIEWER_ROLE, 'members': sorted(self.viewers)})

        if bindings:
            resource['bindings'] = bindings

        return resource
