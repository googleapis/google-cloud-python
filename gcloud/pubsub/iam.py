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
"""PubSub API IAM policy definitions

For allowed roles / permissions, see:
https://cloud.google.com/pubsub/access_control#permissions
"""

# Generic IAM roles

OWNER_ROLE = 'roles/owner'
"""Generic role implying all rights to an object."""

EDITOR_ROLE = 'roles/editor'
"""Generic role implying rights to modify an object."""

VIEWER_ROLE = 'roles/viewer'
"""Generic role implying rights to access an object."""

# Pubsub-specific IAM roles

PUBSUB_ADMIN_ROLE = 'roles/pubsub.admin'
"""Role implying all rights to an object."""

PUBSUB_EDITOR_ROLE = 'roles/pubsub.editor'
"""Role implying rights to modify an object."""

PUBSUB_VIEWER_ROLE = 'roles/pubsub.viewer'
"""Role implying rights to access an object."""

PUBSUB_PUBLISHER_ROLE = 'roles/pubsub.publisher'
"""Role implying rights to publish to a topic."""

PUBSUB_SUBSCRIBER_ROLE = 'roles/pubsub.subscriber'
"""Role implying rights to subscribe to a topic."""


# Pubsub-specific permissions

PUBSUB_TOPICS_CONSUME = 'pubsub.topics.consume'
"""Permission: consume events from a subscription."""

PUBSUB_TOPICS_CREATE = 'pubsub.topics.create'
"""Permission: create topics."""

PUBSUB_TOPICS_DELETE = 'pubsub.topics.delete'
"""Permission: delete topics."""

PUBSUB_TOPICS_GET = 'pubsub.topics.get'
"""Permission: retrieve topics."""

PUBSUB_TOPICS_GET_IAM_POLICY = 'pubsub.topics.getIamPolicy'
"""Permission: retrieve subscription IAM policies."""

PUBSUB_TOPICS_LIST = 'pubsub.topics.list'
"""Permission: list topics."""

PUBSUB_TOPICS_SET_IAM_POLICY = 'pubsub.topics.setIamPolicy'
"""Permission: update subscription IAM policies."""

PUBSUB_SUBSCRIPTIONS_CONSUME = 'pubsub.subscriptions.consume'
"""Permission: consume events from a subscription."""

PUBSUB_SUBSCRIPTIONS_CREATE = 'pubsub.subscriptions.create'
"""Permission: create subscriptions."""

PUBSUB_SUBSCRIPTIONS_DELETE = 'pubsub.subscriptions.delete'
"""Permission: delete subscriptions."""

PUBSUB_SUBSCRIPTIONS_GET = 'pubsub.subscriptions.get'
"""Permission: retrieve subscriptions."""

PUBSUB_SUBSCRIPTIONS_GET_IAM_POLICY = 'pubsub.subscriptions.getIamPolicy'
"""Permission: retrieve subscription IAM policies."""

PUBSUB_SUBSCRIPTIONS_LIST = 'pubsub.subscriptions.list'
"""Permission: list subscriptions."""

PUBSUB_SUBSCRIPTIONS_SET_IAM_POLICY = 'pubsub.subscriptions.setIamPolicy'
"""Permission: update subscription IAM policies."""

PUBSUB_SUBSCRIPTIONS_UPDATE = 'pubsub.subscriptions.update'
"""Permission: update subscriptions."""


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
        self.publishers = set()
        self.subscribers = set()

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
            if role in (OWNER_ROLE, PUBSUB_ADMIN_ROLE):
                policy.owners |= members
            elif role in (EDITOR_ROLE, PUBSUB_EDITOR_ROLE):
                policy.editors |= members
            elif role in (VIEWER_ROLE, PUBSUB_VIEWER_ROLE):
                policy.viewers |= members
            elif role == PUBSUB_PUBLISHER_ROLE:
                policy.publishers |= members
            elif role == PUBSUB_SUBSCRIBER_ROLE:
                policy.subscribers |= members
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
                {'role': PUBSUB_ADMIN_ROLE,
                 'members': sorted(self.owners)})

        if self.editors:
            bindings.append(
                {'role': PUBSUB_EDITOR_ROLE,
                 'members': sorted(self.editors)})

        if self.viewers:
            bindings.append(
                {'role': PUBSUB_VIEWER_ROLE,
                 'members': sorted(self.viewers)})

        if self.publishers:
            bindings.append(
                {'role': PUBSUB_PUBLISHER_ROLE,
                 'members': sorted(self.publishers)})

        if self.subscribers:
            bindings.append(
                {'role': PUBSUB_SUBSCRIBER_ROLE,
                 'members': sorted(self.subscribers)})

        if bindings:
            resource['bindings'] = bindings

        return resource
