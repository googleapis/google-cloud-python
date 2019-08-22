# Copyright 2019 Google LLC
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
"""Non-API-specific IAM policy v3 definitions

For allowed roles / permissions, see:
https://cloud.google.com/iam/docs/understanding-roles

Example usage:

.. code-block:: python

   # ``get_iam_policy_v2`` returns a :class:'~google.api_core.iam.PolicyV2`.
   policy = resource.get_iam_policy_v2()

   phred = policy.user("phred@example.com")
   admin_group = policy.group("admins@groups.example.com")
   account = policy.service_account("account-1234@accounts.example.com")
   policy.bindings.append(
       "role": "roles/owner",
       "members": [phred, admin_group, account]
   })

   resource.set_iam_policy_v2(policy)
"""

class PolicyV2():
    """IAM Policy v2
    The PolicyV2 class supports all version values of Policy, where the legacy
    Policy class only supports a Policy version of 1.

    See <insert versioning doc>

    See
    https://cloud.google.com/iam/reference/rest/v1/Policy

    Args:
        version (Optional[int]): The version of the policy
        etag (Optional[str]): ETag used to identify a unique of the policy
        bindings (Optional[list of dict]): The list of bindings
    """

    def __init__(self, version=None, etag=None, bindings=[]):
        self.version = version
        self.etag = etag
        self.bindings = bindings

    @staticmethod
    def user(email):
        """Factory method for a user member.

        Args:
            email (str): E-mail for this particular user.

        Returns:
            str: A member string corresponding to the given user.
        """
        return "user:%s" % (email,)

    @staticmethod
    def service_account(email):
        """Factory method for a service account member.

        Args:
            email (str): E-mail for this particular service account.

        Returns:
            str: A member string corresponding to the given service account.
        """
        return "serviceAccount:%s" % (email,)

    @staticmethod
    def group(email):
        """Factory method for a group member.

        Args:
            email (str): An id or e-mail for this particular group.

        Returns:
            str: A member string corresponding to the given group.
        """
        return "group:%s" % (email,)

    @staticmethod
    def domain(domain):
        """Factory method for a domain member.

        Args:
            domain (str): The domain for this member.

        Returns:
            str: A member string corresponding to the given domain.
        """
        return "domain:%s" % (domain,)

    @staticmethod
    def all_users():
        """Factory method for a member representing all users.

        Returns:
            str: A member string representing all users.
        """
        return "allUsers"

    @staticmethod
    def authenticated_users():
        """Factory method for a member representing all authenticated users.

        Returns:
            str: A member string representing all authenticated users.
        """
        return "allAuthenticatedUsers"

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: create a policy from a JSON resource.

        Args:
            resource (dict): policy resource returned by ``getIamPolicy`` API.

        Returns:
            :class:`Policy`: the parsed policy
        """
        version = resource.get("version")
        etag = resource.get("etag")
        bindings = resource.get("bindings")
        return policy

    def to_api_repr(self):
        """Render a JSON policy resource.

        Returns:
            dict: a resource to be passed to the ``setIamPolicy`` API.
        """
        resource = {}

        if self.etag is not None:
            resource["etag"] = self.etag

        if self.version is not None:
            resource["version"] = self.version

        if self.bindings is not None:
            resource["bindings"] = self.bindings

        return resource
