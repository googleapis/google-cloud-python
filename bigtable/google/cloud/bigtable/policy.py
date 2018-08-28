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

from google.cloud.iam import Policy as IamPolicy
from google.cloud._helpers import _to_bytes

"""IAM roles supported by Bigtable Instance resource"""
BIGTABLE_ADMIN_ROLE = 'roles/bigtable.admin'
"""Administers all instances within a project, including the data stored
within tables. Can create new instances. Intended for project administrators.
"""
BIGTABLE_USER_ROLE = 'roles/bigtable.user'
"""Provides read-write access to the data stored within tables. Intended for
application developers or service accounts.
"""
BIGTABLE_READER_ROLE = 'roles/bigtable.reader'
"""Provides read-only access to the data stored within tables. Intended for
data scientists, dashboard generators, and other data-analysis scenarios.
"""
BIGTABLE_VIEWER_ROLE = 'roles/bigtable.viewer'
"""Provides no data access. Intended as a minimal set of permissions to access
the GCP Console for Cloud Bigtable.
"""
"""For detailed information
See
https://cloud.google.com/bigtable/docs/access-control#roles
"""


class Policy(IamPolicy):
    """IAM Policy

    See
    https://cloud.google.com/bigtable/docs/reference/admin/rpc/google.iam.v1#policy

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
        IamPolicy.__init__(self,
                           etag=etag if etag is None else _to_bytes(etag),
                           version=version)

    @property
    def bigtable_admins(self):
        """Access to bigtable.admin role memebers"""
        result = set()
        for member in self._bindings.get(BIGTABLE_ADMIN_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_readers(self):
        """Access to bigtable.reader role memebers"""
        result = set()
        for member in self._bindings.get(BIGTABLE_READER_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_users(self):
        """Access to bigtable.user role memebers"""
        result = set()
        for member in self._bindings.get(BIGTABLE_USER_ROLE, ()):
            result.add(member)
        return frozenset(result)

    @property
    def bigtable_viewers(self):
        """Access to bigtable.viewer role memebers"""
        result = set()
        for member in self._bindings.get(BIGTABLE_VIEWER_ROLE, ()):
            result.add(member)
        return frozenset(result)
