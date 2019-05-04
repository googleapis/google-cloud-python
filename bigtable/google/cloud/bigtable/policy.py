# Copyright 2018 Google LLC
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

import base64

from google.api_core.iam import Policy as BasePolicy
from google.cloud._helpers import _to_bytes
from google.iam.v1 import policy_pb2

"""IAM roles supported by Bigtable Instance resource"""
BIGTABLE_ADMIN_ROLE = "roles/bigtable.admin"
"""Administers all instances within a project, including the data stored
within tables. Can create new instances. Intended for project administrators.
"""
BIGTABLE_USER_ROLE = "roles/bigtable.user"
"""Provides read-write access to the data stored within tables. Intended for
application developers or service accounts.
"""
BIGTABLE_READER_ROLE = "roles/bigtable.reader"
"""Provides read-only access to the data stored within tables. Intended for
data scientists, dashboard generators, and other data-analysis scenarios.
"""
BIGTABLE_VIEWER_ROLE = "roles/bigtable.viewer"
"""Provides no data access. Intended as a minimal set of permissions to access
the GCP Console for Cloud Bigtable.
"""
"""For detailed information
See
https://cloud.google.com/bigtable/docs/access-control#roles
"""


class Policy(BasePolicy):
    """IAM Policy

    See
    https://cloud.google.com/bigtable/docs/reference/admin/rpc/google.iam.v1#policy

    A Policy consists of a list of bindings. A binding binds a list of
    members to a role, where the members can be user accounts, Google
    groups, Google domains, and service accounts. A role is a named list
    of permissions defined by IAM.
    For more information about predefined roles currently supoprted
    by Bigtable Instance please see
    `Predefined roles
    <https://cloud.google.com/bigtable/docs/access-control#roles>`_.
    For more information about custom roles please see
    `Custom roles
    <https://cloud.google.com/bigtable/docs/access-control#custom-roles>`_.

    :type etag: str
    :param etag: etag is used for optimistic concurrency control as a way to
                 help prevent simultaneous updates of a policy from overwriting
                 each other. It is strongly suggested that systems make use
                 of the etag in the read-modify-write cycle to perform policy
                 updates in order to avoid race conditions:
                 An etag is returned in the response to getIamPolicy, and
                 systems are expected to put that etag in the request to
                 setIamPolicy to ensure that their change will be applied to
                 the same version of the policy.

                 If no etag is provided in the call to setIamPolicy, then the
                 existing policy is overwritten blindly.
    """

    def __init__(self, etag=None, version=None):
        BasePolicy.__init__(
            self, etag=etag if etag is None else _to_bytes(etag), version=version
        )

    @property
    def bigtable_admins(self):
        """Access to bigtable.admin role memebers

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_admins_policy]
            :end-before: [END bigtable_admins_policy]
        """
        result = set()
        for member in self._bindings.get(BIGTABLE_ADMIN_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_readers(self):
        """Access to bigtable.reader role memebers

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_readers_policy]
            :end-before: [END bigtable_readers_policy]
        """
        result = set()
        for member in self._bindings.get(BIGTABLE_READER_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_users(self):
        """Access to bigtable.user role memebers

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_users_policy]
            :end-before: [END bigtable_users_policy]
        """
        result = set()
        for member in self._bindings.get(BIGTABLE_USER_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_viewers(self):
        """Access to bigtable.viewer role memebers

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_viewers_policy]
            :end-before: [END bigtable_viewers_policy]
        """
        result = set()
        for member in self._bindings.get(BIGTABLE_VIEWER_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @classmethod
    def from_pb(cls, policy_pb):
        """Factory: create a policy from a protobuf message.

        Args:
            policy_pb (google.iam.policy_pb2.Policy): message returned by
            ``get_iam_policy`` gRPC API.

        Returns:
            :class:`Policy`: the parsed policy
        """
        policy = cls(policy_pb.etag, policy_pb.version)

        for binding in policy_pb.bindings:
            policy[binding.role] = sorted(binding.members)

        return policy

    def to_pb(self):
        """Render a protobuf message.

        Returns:
            google.iam.policy_pb2.Policy: a message to be passed to the
            ``set_iam_policy`` gRPC API.
        """

        return policy_pb2.Policy(
            etag=self.etag,
            version=self.version or 0,
            bindings=[
                policy_pb2.Binding(role=role, members=sorted(self[role]))
                for role in self
            ],
        )

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: create a policy from a JSON resource.

        Overrides the base class version to store :attr:`etag` as bytes.

        Args:
            resource (dict): JSON policy resource returned by the
            ``getIamPolicy`` REST API.

        Returns:
            :class:`Policy`: the parsed policy
        """
        etag = resource.get("etag")

        if etag is not None:
            resource = resource.copy()
            resource["etag"] = base64.b64decode(etag.encode("ascii"))

        return super(Policy, cls).from_api_repr(resource)

    def to_api_repr(self):
        """Render a JSON policy resource.

        Overrides the base class version to convert :attr:`etag` from bytes
        to JSON-compatible base64-encoded text.

        Returns:
            dict: a JSON resource to be passed to the
            ``setIamPolicy`` REST API.
        """
        resource = super(Policy, self).to_api_repr()

        if self.etag is not None:
            resource["etag"] = base64.b64encode(self.etag).decode("ascii")

        return resource
