# Copyright 2015 Google Inc. All rights reserved.
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

"""Parent client for calling the Google Cloud Bigtable API.

This is the base from which all interactions with the API occur.

In the hierarchy of API concepts

* a :class:`Client` owns a :class:`.Cluster`
* a :class:`.Cluster` owns a :class:`Table <gcloud_bigtable.table.Table>`
* a :class:`Table <gcloud_bigtable.table.Table>` owns a
  :class:`ColumnFamily <.column_family.ColumnFamily>`
* a :class:`Table <gcloud_bigtable.table.Table>` owns a :class:`Row <.row.Row>`
  (and all the cells in the row)
"""


from gcloud.client import _ClientFactoryMixin
from gcloud.client import _ClientProjectMixin
from gcloud.credentials import get_credentials


TABLE_ADMIN_HOST = 'bigtabletableadmin.googleapis.com'
"""Table Admin API request host."""
TABLE_ADMIN_PORT = 443
"""Table Admin API request port."""

CLUSTER_ADMIN_HOST = 'bigtableclusteradmin.googleapis.com'
"""Cluster Admin API request host."""
CLUSTER_ADMIN_PORT = 443
"""Cluster Admin API request port."""

DATA_API_HOST = 'bigtable.googleapis.com'
"""Data API request host."""
DATA_API_PORT = 443
"""Data API request port."""

ADMIN_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
"""Scope for interacting with the Cluster Admin and Table Admin APIs."""
DATA_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.data'
"""Scope for reading and writing table data."""
READ_ONLY_SCOPE = ('https://www.googleapis.com/auth/'
                   'cloud-bigtable.data.readonly')
"""Scope for reading table data."""

DEFAULT_TIMEOUT_SECONDS = 10
"""The default timeout to use for API requests."""

DEFAULT_USER_AGENT = 'gcloud-bigtable-python'
"""The default user agent for API requests."""


class Client(_ClientFactoryMixin, _ClientProjectMixin):
    """Client for interacting with Google Cloud Bigtable API.

    .. note::

        Since the Cloud Bigtable API requires the gRPC transport, no
        ``http`` argument is accepted by this class.

    :type project: :class:`str` or :func:`unicode <unicode>`
    :param project: (Optional) The ID of the project which owns the
                    clusters, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials:
        :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>` or
        :data:`NoneType <types.NoneType>`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        cluster. If not provided, defaulst to the Google
                        Application Default Credentials.

    :type read_only: bool
    :param read_only: (Optional) Boolean indicating if the data scope should be
                      for reading only (or for writing as well). Defaults to
                      :data:`False`.

    :type admin: bool
    :param admin: (Optional) Boolean indicating if the client will be used to
                  interact with the Cluster Admin or Table Admin APIs. This
                  requires the :const:`ADMIN_SCOPE`. Defaults to :data:`False`.

    :type user_agent: str
    :param user_agent: (Optional) The user agent to be used with API request.
                       Defaults to :const:`DEFAULT_USER_AGENT`.

    :type timeout_seconds: int
    :param timeout_seconds: Number of seconds for request time-out. If not
                            passed, defaults to
                            :const:`DEFAULT_TIMEOUT_SECONDS`.

    :raises: :class:`ValueError <exceptions.ValueError>` if both ``read_only``
             and ``admin`` are :data:`True`
    """

    def __init__(self, project=None, credentials=None,
                 read_only=False, admin=False, user_agent=DEFAULT_USER_AGENT,
                 timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
        _ClientProjectMixin.__init__(self, project=project)
        if credentials is None:
            credentials = get_credentials()

        if read_only and admin:
            raise ValueError('A read-only client cannot also perform'
                             'administrative actions.')

        scopes = []
        if read_only:
            scopes.append(READ_ONLY_SCOPE)
        else:
            scopes.append(DATA_SCOPE)

        if admin:
            scopes.append(ADMIN_SCOPE)

        self._admin = bool(admin)
        self._credentials = credentials.create_scoped(scopes)
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds

    @property
    def credentials(self):
        """Getter for client's credentials.

        :rtype:
            :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>`
        :returns: The credentials stored on the client.
        """
        return self._credentials
