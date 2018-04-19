# Copyright 2015 Google LLC
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

* a :class:`~google.cloud.bigtable.client.Client` owns an
  :class:`~google.cloud.bigtable.instance.Instance`
* an :class:`~google.cloud.bigtable.instance.Instance` owns a
  :class:`~google.cloud.bigtable.table.Table`
* a :class:`~google.cloud.bigtable.table.Table` owns a
  :class:`~.column_family.ColumnFamily`
* a :class:`~google.cloud.bigtable.table.Table` owns a
  :class:`~google.cloud.bigtable.row.Row` (and all the cells in the row)
"""


from google.cloud.bigtable.instance import Instance
from google.cloud.bigtable.instance import _EXISTING_INSTANCE_LOCATION_ID

from google.cloud import bigtable_v2
from google.cloud import bigtable_admin_v2


ADMIN_SCOPE = 'https://www.googleapis.com/auth/bigtable.admin'
"""Scope for interacting with the Cluster Admin and Table Admin APIs."""
DATA_SCOPE = 'https://www.googleapis.com/auth/bigtable.data'
"""Scope for reading and writing table data."""
READ_ONLY_SCOPE = 'https://www.googleapis.com/auth/bigtable.data.readonly'
"""Scope for reading table data."""


class Client(object):
    """Client for interacting with Google Cloud Bigtable API.

    .. note::

        Since the Cloud Bigtable API requires the gRPC transport, no
        ``_http`` argument is accepted by this class.

    :type project: :class:`str` or :func:`unicode <unicode>`
    :param project: (Optional) The ID of the project which owns the
                    instances, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed, falls back to the default
                        inferred from the environment.

    :type read_only: bool
    :param read_only: (Optional) Boolean indicating if the data scope should be
                      for reading only (or for writing as well). Defaults to
                      :data:`False`.

    :type admin: bool
    :param admin: (Optional) Boolean indicating if the client will be used to
                  interact with the Instance Admin or Table Admin APIs. This
                  requires the :const:`ADMIN_SCOPE`. Defaults to :data:`False`.

    :type project: :instance: grpc.Channel
    :param channel (grpc.Channel): (Optional) A ``Channel`` instance
            through which to make calls. This argument is mutually
            exclusive with ``credentials``; providing both will raise an
            exception.

    :raises: :class:`ValueError <exceptions.ValueError>` if both ``read_only``
             and ``admin`` are :data:`True`
    """

    def __init__(self, project=None, credentials=None,
                 read_only=False, admin=False, channel=None):
        if read_only and admin:
            raise ValueError('A read-only client cannot also perform'
                             'administrative actions.')

        # NOTE: We set the scopes **before** calling the parent constructor.
        #       It **may** use those scopes in ``with_scopes_if_required``.
        self.project = project
        self._read_only = bool(read_only)
        self._admin = bool(admin)
        self.channel = channel
        self._credentials = credentials
        self.SCOPE = self._get_scopes()

        # NOTE: This API has no use for the _http argument, but sending it
        #       will have no impact since the _http() @property only lazily
        #       creates a working HTTP object.
        super(Client, self).__init__()

        if self.channel is not None:
            self._credentials = None

    def _get_scopes(self):
        """Get the scopes corresponding to admin / read-only state.

        Returns:
            Tuple[str, ...]: The tuple of scopes.
        """
        if self._read_only:
            scopes = (READ_ONLY_SCOPE,)
        else:
            scopes = (DATA_SCOPE,)

        if self._admin:
            scopes += (ADMIN_SCOPE,)

        return scopes

    @property
    def project_path(self):
        """Project name to be used with Instance Admin API.

        .. note::

            This property will not change if ``project`` does not, but the
            return value is not cached.

        The project name is of the form

            ``"projects/{project}"``

        :rtype: str
        :returns: Return a fully-qualified project string.
        """
        instance_client = self._instance_admin_client
        return instance_client.project_path(self.project)

    @property
    def _table_data_client(self):
        """Getter for the gRPC stub used for the Table Admin API.

        :rtype: :class:`.bigtable_v2.BigtableClient`
        :returns: A BigtableClient object.
        """
        return bigtable_v2.BigtableClient(channel=self.channel,
                                          credentials=self._credentials)

    @property
    def _table_admin_client(self):
        """Getter for the gRPC stub used for the Table Admin API.

        :rtype: :class:`.bigtable_admin_pb2.BigtableTableAdmin`
        :returns: A BigtableTableAdmin instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        return bigtable_admin_v2.BigtableTableAdminClient(
            channel=self.channel, credentials=self._credentials)

    @property
    def _instance_admin_client(self):
        """Getter for the gRPC stub used for the Table Admin API.

        :rtype: :class:`.bigtable_admin_pb2.BigtableInstanceAdmin`
        :returns: A BigtableInstanceAdmin instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        return bigtable_admin_v2.BigtableInstanceAdminClient(
            channel=self.channel, credentials=self._credentials)

    def instance(self, instance_id, location=_EXISTING_INSTANCE_LOCATION_ID,
                 display_name=None):
        """Factory to create a instance associated with this client.

        :type instance_id: str
        :param instance_id: The ID of the instance.

        :type location: str
        :param location: location name, in form
                         ``projects/<project>/locations/<location>``; used to
                         set up the instance's cluster.

        :type display_name: str
        :param display_name: (Optional) The display name for the instance in
                             the Cloud Console UI. (Must be between 4 and 30
                             characters.) If this value is not set in the
                             constructor, will fall back to the instance ID.

        :rtype: :class:`~google.cloud.bigtable.instance.Instance`
        :returns: an instance owned by this client.
        """
        return Instance(instance_id, self, location, display_name=display_name)

    def list_instances(self):
        """List instances owned by the project.

        :rtype: :class:`~google.gax.PageIterator`
        :returns: A list of Instance.
        """
        return self._instance_admin_client.list_instances(self.project_path)
