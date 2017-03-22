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
"""PubSub API IAM policy definitions

For allowed roles / permissions, see:
https://cloud.google.com/pubsub/access_control#permissions
"""

from google.cloud.iam import OWNER_ROLE
from google.cloud.iam import EDITOR_ROLE
from google.cloud.iam import VIEWER_ROLE
from google.cloud.iam import Policy as _BasePolicy

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


class Policy(_BasePolicy):
    """IAM Policy / Bindings.

    See:
    https://cloud.google.com/pubsub/docs/reference/rest/Shared.Types/Policy
    https://cloud.google.com/pubsub/docs/reference/rest/Shared.Types/Binding

    :type etag: str
    :param etag: ETag used to identify a unique of the policy

    :type version: int
    :param version: unique version of the policy
    """
    _OWNER_ROLES = (OWNER_ROLE, PUBSUB_ADMIN_ROLE)
    _EDITOR_ROLES = (EDITOR_ROLE, PUBSUB_EDITOR_ROLE)
    _VIEWER_ROLES = (VIEWER_ROLE, PUBSUB_VIEWER_ROLE)

    def __init__(self, etag=None, version=None):
        super(Policy, self).__init__(etag, version)
        self.publishers = set()
        self.subscribers = set()

    def _bind_custom_role(self, role, members):
        """Bind an API-specific role to members.

        Helper for :meth:`from_api_repr`.

        :type role: str
        :param role: role to bind.

        :type members: set of str
        :param members: member IDs to be bound to the role.

        Subclasses may override.
        """
        if role == PUBSUB_PUBLISHER_ROLE:
            self.publishers |= members
        elif role == PUBSUB_SUBSCRIBER_ROLE:
            self.subscribers |= members
        else:
            super(Policy, self)._bind_custom_role(role, members)

    def _role_bindings(self):
        """Enumerate members bound to roles for the policy.

        Helper for :meth:`to_api_repr`.

        :rtype: list of mapping
        :returns: zero or more mappings describing roles / members bound by
                  the policy.
        """
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

        return bindings
