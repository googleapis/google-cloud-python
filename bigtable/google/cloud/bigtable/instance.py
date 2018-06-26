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

"""User-friendly container for Google Cloud Bigtable Instance."""


import re

from google.cloud.bigtable.table import Table
from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

from google.protobuf import field_mask_pb2

from google.cloud.bigtable_admin_v2 import enums
from google.cloud.bigtable_admin_v2.types import instance_pb2


_EXISTING_INSTANCE_LOCATION_ID = 'see-existing-cluster'
_INSTANCE_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                               r'instances/(?P<instance_id>[a-z][-a-z0-9]*)$')
ROUTING_POLICY_TYPE_ANY = 1
ROUTING_POLICY_TYPE_SINGLE = 2
_STORAGE_TYPE_UNSPECIFIED = enums.StorageType.STORAGE_TYPE_UNSPECIFIED


class Instance(object):
    """Representation of a Google Cloud Bigtable Instance.

    We can use an :class:`Instance` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    .. note::

        For now, we leave out the ``default_storage_type`` (an enum)
        which if not sent will end up as :data:`.data_v2_pb2.STORAGE_SSD`.

    :type instance_id: str
    :param instance_id: The ID of the instance.

    :type client: :class:`Client <google.cloud.bigtable.client.Client>`
    :param client: The client that owns the instance. Provides
                   authorization and a project ID.

    :type display_name: str
    :param display_name: (Optional) The display name for the instance in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the instance ID.
    """

    def __init__(self, instance_id, client, display_name=None):
        self.instance_id = instance_id
        self.display_name = display_name or instance_id
        self._client = client

    @classmethod
    def from_pb(cls, instance_pb, client):
        """Creates an instance instance from a protobuf.

        :type instance_pb: :class:`instance_pb2.Instance`
        :param instance_pb: An instance protobuf object.

        :type client: :class:`Client <google.cloud.bigtable.client.Client>`
        :param client: The client that owns the instance.

        :rtype: :class:`Instance`
        :returns: The instance parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the instance
                 name does not match
                 ``projects/{project}/instances/{instance_id}``
                 or if the parsed project ID does not match the project ID
                 on the client.
        """
        match = _INSTANCE_NAME_RE.match(instance_pb.name)
        if match is None:
            raise ValueError('Instance protobuf name was not in the '
                             'expected format.', instance_pb.name)
        if match.group('project') != client.project:
            raise ValueError('Project ID on instance does not match the '
                             'project ID on the client')
        instance_id = match.group('instance_id')

        result = cls(instance_id, client,
                     display_name=instance_pb.display_name)
        return result

    def _update_from_pb(self, instance_pb):
        """Refresh self from the server-provided protobuf.
        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not instance_pb.display_name:  # Simple field (string)
            raise ValueError('Instance protobuf does not contain display_name')
        self.display_name = instance_pb.display_name

    @property
    def name(self):
        """Instance name used in requests.

        .. note::
          This property will not change if ``instance_id`` does not,
          but the return value is not cached.

        The instance name is of the form

            ``"projects/{project}/instances/{instance_id}"``

        :rtype: str
        :returns: Return a fully-qualified instance string.
        """
        return self._client.instance_admin_client.instance_path(
            project=self._client.project, instance=self.instance_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the display_name. Instead, it only compares
        #       identifying values instance ID and client. This is
        #       intentional, since the same instance can be in different states
        #       if not synchronized. Instances with similar instance
        #       settings but different clients can't be used in the same way.
        return (other.instance_id == self.instance_id and
                other._client == self._client)

    def __ne__(self, other):
        return not self == other

    def reload(self):
        """Reload the metadata for this instance."""
        instance_pb = self._client.instance_admin_client.get_instance(
            self.name)

        # NOTE: _update_from_pb does not check that the project and
        #       instance ID on the response match the request.
        self._update_from_pb(instance_pb)

    def create(self, location_id=_EXISTING_INSTANCE_LOCATION_ID,
               serve_nodes=DEFAULT_SERVE_NODES,
               default_storage_type=_STORAGE_TYPE_UNSPECIFIED):
        """Create this instance.

        .. note::

            Uses the ``project`` and ``instance_id`` on the current
            :class:`Instance` in addition to the ``display_name``.
            To change them before creating, reset the values via

            .. code:: python

                instance.display_name = 'New display name'
                instance.instance_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :type location_id: str
        :param location_id: ID of the location in which the instance will be
                            created.  Required for instances which do not yet
                            exist.


        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the instance's
                            cluster; used to set up the instance's cluster.

        :type default_storage_type: int
        :param default_storage_type: (Optional) The default values are
                                     STORAGE_TYPE_UNSPECIFIED = 0: The user
                                     did not specify a storage type.
                                     SSD = 1: Flash (SSD) storage should be
                                     used.
                                     HDD = 2: Magnetic drive (HDD) storage
                                     should be used.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the create
                    operation.
        """
        clusters = {}
        cluster_id = '{}-cluster'.format(self.instance_id)
        cluster_name = self._client.instance_admin_client.cluster_path(
            self._client.project, self.instance_id, cluster_id)
        location = self._client.instance_admin_client.location_path(
            self._client.project, location_id)
        cluster = instance_pb2.Cluster(
            name=cluster_name, location=location,
            serve_nodes=serve_nodes,
            default_storage_type=default_storage_type)
        instance = instance_pb2.Instance(
            display_name=self.display_name
        )
        clusters[cluster_id] = cluster
        parent = self._client.project_path

        return self._client.instance_admin_client.create_instance(
            parent=parent, instance_id=self.instance_id, instance=instance,
            clusters=clusters)

    def update(self):
        """Update this instance.

        .. note::

            Updates the ``display_name``. To change that value before
            updating, reset its values via

            .. code:: python

                instance.display_name = 'New display name'

            before calling :meth:`update`.
        """
        type = enums.Instance.Type.TYPE_UNSPECIFIED
        self._client.instance_admin_client.update_instance(
            name=self.name, display_name=self.display_name, type_=type,
            labels={})

    def delete(self):
        """Delete this instance.

        Marks an instance and all of its tables for permanent deletion
        in 7 days.

        Immediately upon completion of the request:

        * Billing will cease for all of the instance's reserved resources.
        * The instance's ``delete_time`` field will be set 7 days in
          the future.

        Soon afterward:

        * All tables within the instance will become unavailable.

        At the instance's ``delete_time``:

        * The instance and **all of its tables** will immediately and
          irrevocably disappear from the API, and their data will be
          permanently deleted.
        """
        self._client.instance_admin_client.delete_instance(name=self.name)

    def table(self, table_id):
        """Factory to create a table associated with this instance.

        :type table_id: str
        :param table_id: The ID of the table.

        :rtype: :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The table owned by this instance.
        """
        return Table(table_id, self)

    def list_tables(self):
        """List the tables in this instance.

        :rtype: list of :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The list of tables owned by the instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if one of the
                 returned tables has a name that is not of the expected format.
        """
        table_list_pb = self._client.table_admin_client.list_tables(self.name)

        result = []
        for table_pb in table_list_pb:
            table_prefix = self.name + '/tables/'
            if not table_pb.name.startswith(table_prefix):
                raise ValueError('Table name %s not of expected format' % (
                    table_pb.name,))
            table_id = table_pb.name[len(table_prefix):]
            result.append(self.table(table_id))

        return result

    def create_app_profile(self, app_profile_id, routing_policy_type,
                           description='', ignore_warnings=None,
                           cluster_id=None, allow_transactional_writes=False):
        """Creates an app profile within an instance.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the new app profile.

        :type: routing_policy_type: int
        :param: routing_policy_type: There are two routing policies
                                    ROUTING_POLICY_TYPE_ANY = 1 and
                                    ROUTING_POLICY_TYPE_SINGLE = 2.
                                    If ROUTING_POLICY_TYPE_ANY
                                    which will create a
                                    MultiClusterRoutingUseAny policy and if
                                    ROUTING_POLICY_TYPE_ANY is specified, a
                                    SingleClusterRouting policy will be created
                                    using the cluster_id and
                                    allow_transactional_writes parameters.

        :type: description: str
        :param: description: (Optional) Long form description of the use
                                case for this AppProfile.

        :type: ignore_warnings: bool
        :param: ignore_warnings: (Optional) If true, ignore safety checks when
                                    creating the app profile.

        :type: cluster_id: str
        :param: cluster_id: (Optional) Unique cluster_id which is only required
                            when routing_policy_type is
                            ROUTING_POLICY_TYPE_SINGLE.

        :type: allow_transactional_writes: bool
        :param: allow_transactional_writes: (Optional) If true, allow
                                            transactional writes for
                                            ROUTING_POLICY_TYPE_SINGLE.

        :rtype: :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
        :return: The AppProfile instance.
        :raises: :class:`ValueError <exceptions.ValueError>` If routing
                policy is not set.
        """
        if not routing_policy_type:
            raise ValueError('AppProfile required routing policy.')

        single_cluster_routing = None
        multi_cluster_routing_use_any = None
        instance_admin_client = self._client._instance_admin_client
        name = instance_admin_client.app_profile_path(
            self._client.project, self.instance_id, app_profile_id)

        if routing_policy_type == ROUTING_POLICY_TYPE_ANY:
            multi_cluster_routing_use_any = (
                instance_pb2.AppProfile.MultiClusterRoutingUseAny())

        if routing_policy_type == ROUTING_POLICY_TYPE_SINGLE:
            single_cluster_routing = (
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=cluster_id,
                    allow_transactional_writes=allow_transactional_writes
                ))

        app_profile = instance_pb2.AppProfile(
            name=name, description=description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )

        return self._client._instance_admin_client.create_app_profile(
            parent=self.name, app_profile_id=app_profile_id,
            app_profile=app_profile, ignore_warnings=ignore_warnings)

    def get_app_profile(self, app_profile_id):
        """Gets information about an app profile.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the app profile.

        :rtype: :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
        :return: The AppProfile instance.
        """
        instance_admin_client = self._client._instance_admin_client
        name = instance_admin_client.app_profile_path(
            self._client.project, self.instance_id, app_profile_id)
        return self._client._instance_admin_client.get_app_profile(name)

    def list_app_profiles(self):
        """Lists information about app profiles in an instance.

        :rtype: :list:[`~google.cloud.bigtable_admin_v2.types.AppProfile`]
        :return: A :list:[`~google.cloud.bigtable_admin_v2.types.AppProfile`].
                By default, this is a list of
                :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
                instances.
        """
        list_app_profiles = list(
            self._client._instance_admin_client.list_app_profiles(self.name))
        return list_app_profiles

    def update_app_profile(self, app_profile_id, update_mask,
                           routing_policy_type, description='',
                           ignore_warnings=None,
                           cluster_id=None, allow_transactional_writes=False):
        """Updates an app profile within an instance.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the new app profile.

        :type: update_mask: list
        :param: update_mask: Name of the parameters of AppProfiles that
                                needed to update.

        :type: routing_policy_type: int
        :param: routing_policy_type: There are two routing policies
                                    ROUTING_POLICY_TYPE_ANY = 1 and
                                    ROUTING_POLICY_TYPE_SINGLE = 2.
                                    If ROUTING_POLICY_TYPE_ANY
                                    which will create a
                                    MultiClusterRoutingUseAny policy and if
                                    ROUTING_POLICY_TYPE_ANY is specified, a
                                    SingleClusterRouting policy will be created
                                    using the cluster_id and
                                    allow_transactional_writes parameters.

        :type: description: str
        :param: description: (Optional) Optional long form description of the
                                use case for this AppProfile.

        :type: ignore_warnings: bool
        :param: ignore_warnings: (Optional) If true, ignore safety checks when
                                    creating the app profile.

        :type: cluster_id: str
        :param: cluster_id: (Optional) Unique cluster_id which is only required
                            when routing_policy_type is
                            ROUTING_POLICY_TYPE_SINGLE.

        :type: allow_transactional_writes: bool
        :param: allow_transactional_writes: (Optional) If true, allow
                                            transactional writes for
                                            ROUTING_POLICY_TYPE_SINGLE.

        :rtype: :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
        :return: The AppProfile instance.
        :raises: :class:`ValueError <exceptions.ValueError>` If routing
                policy is not set.
        """
        if not routing_policy_type:
            raise ValueError('AppProfile required routing policy.')

        single_cluster_routing = None
        multi_cluster_routing_use_any = None
        instance_admin_client = self._client._instance_admin_client
        name = instance_admin_client.app_profile_path(
            self._client.project, self.instance_id, app_profile_id)

        if routing_policy_type == ROUTING_POLICY_TYPE_ANY:
            multi_cluster_routing_use_any = (
                instance_pb2.AppProfile.MultiClusterRoutingUseAny())

        if routing_policy_type == ROUTING_POLICY_TYPE_SINGLE:
            single_cluster_routing = (
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=cluster_id,
                    allow_transactional_writes=allow_transactional_writes
                ))

        update_app_profile = instance_pb2.AppProfile(
            name=name, description=description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )
        update_mask = field_mask_pb2.FieldMask(paths=update_mask)

        return self._client._instance_admin_client.update_app_profile(
            app_profile=update_app_profile, update_mask=update_mask,
            ignore_warnings=ignore_warnings)

    def delete_app_profile(self, app_profile_id, ignore_warnings=False):
        """Deletes an app profile from an instance.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the app profile to delete.

        :raises: google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason. google.api_core.exceptions.RetryError:
                If the request failed due to a retryable error and retry
                attempts failed. ValueError: If the parameters are invalid.
        """
        instance_admin_client = self._client._instance_admin_client
        app_profile_path = instance_admin_client.app_profile_path(
            self._client.project, self.instance_id, app_profile_id)
        self._client._instance_admin_client.delete_app_profile(
            app_profile_path, ignore_warnings)
