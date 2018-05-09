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

from google.protobuf import field_mask_pb2

from google.cloud.bigtable_admin_v2 import enums
from google.cloud.bigtable_admin_v2.proto import instance_pb2


_EXISTING_INSTANCE_LOCATION_ID = 'see-existing-cluster'
_INSTANCE_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                               r'instances/(?P<instance_id>[a-z][-a-z0-9]*)$')
ROUTING_POLICY_TYPE_ANY = 1
ROUTING_POLICY_TYPE_SINGLE = 2


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

    :type location_id: str
    :param location_id: ID of the location in which the instance will be
                        created.  Required for instances which do not yet
                        exist.

    :type display_name: str
    :param display_name: (Optional) The display name for the instance in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the instance ID.
    """

    def __init__(self, instance_id, client,
                 location_id=_EXISTING_INSTANCE_LOCATION_ID,
                 display_name=None):
        self.instance_id = instance_id
        self.display_name = display_name or instance_id
        self._cluster_location_id = location_id
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

        result = cls(instance_id, client, _EXISTING_INSTANCE_LOCATION_ID)
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
        return self._client._instance_admin_client.instance_path(
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

    def create(self):
        """Create this instance.

        .. note::

            Uses the ``project`` and ``instance_id`` on the current
            :class:`Instance` in addition to the ``display_name``.
            To change them before creating, reset the values via

            .. code:: python

                instance.display_name = 'New display name'
                instance.instance_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the create
                    operation.
        """
        parent = self._client.project_path
        return self._client._instance_admin_client.create_instance(
            parent=parent, instance_id=self.instance_id, instance={},
            clusters={})

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
        self._client._instance_admin_client.update_instance(
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
        self._client._instance_admin_client.delete_instance(name=self.name)

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
        table_list_pb = self._client._table_admin_client.list_tables(self.name)

        result = []
        for table_pb in table_list_pb:
            table_prefix = self.name + '/tables/'
            if not table_pb.name.startswith(table_prefix):
                raise ValueError('Table name %s not of expected format' % (
                    table_pb.name,))
            table_id = table_pb.name[len(table_prefix):]
            result.append(self.table(table_id))

        return result

    def create_app_profile(self, app_profile_id, etag='', description='',
                           ignore_warnings=None, metadata=None,
                           routing_policy_type=ROUTING_POLICY_TYPE_ANY,
                           cluster_id=None,
                           allow_transactional_writes=False):
        """Creates an app profile within an instance.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the new app profile.

        :type: etag: str
        :param: etag: (Optional) Strongly validated etag for optimistic
                        concurrency control. Preserve the value returned
                        from ``GetAppProfile`` when calling
                        ``UpdateAppProfile`` to fail the request if there
                        has been a modification in the mean time. The
                        ``update_mask`` of the request need not include
                        ``etag`` for this protection to apply.

        :type: description: str
        :param: description: (Optional) Long form description of the use
                                case for this AppProfile.

        :type: ignore_warnings: bool
        :param: ignore_warnings: (Optional) If true, ignore safety checks when
                                    creating the app profile.

        :type: metadata: [Sequence[Tuple[str, str]]]
        :param: metadata: (Optional) Additional metadata that is provided to
                            the method.

        :type: routing_policy_type: int
        :parm: routing_policy_type: (Optional) There are two routing policies
                                    1. ROUTING_POLICY_TYPE_ANY = 1 and
                                    2. ROUTING_POLICY_TYPE_SINGLE = 2.
                                    By default it is ROUTING_POLICY_TYPE_ANY
                                    which is MultiClusterRoutingUseAny policy
                                    and for SingleClusterRouting user need to
                                    assign 2 and that will need cluster_id
                                    and allow_transactional_writes
                                    for single cluster routing policy proto.

        :type: cluster_id: str
        :param: cluster_id: (Optional) Unique cluster_id  to create AppProfile
                            on selected cluster route. It is only required
                            when routing_policy_type is
                            ROUTING_POLICY_TYPE_SINGLE.

        :type: allow_transactional_writes: bool
        :param: allow_transactional_writes: (Optional) If true, allow
                                            transactional writes to single
                                            cluster routing, if cluster_id is
                                            given.

        :rtype: :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
        :return: The AppProfile instance.
        """
        single_cluster_routing = None
        multi_cluster_routing_use_any = None
        instance_admin_client = self._client._instance_admin_client
        name = instance_admin_client.app_profile_path(
            self._client.project, self.name, app_profile_id)

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
            name=name, etag=etag, description=description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )

        return self._client._instance_admin_client.create_app_profile(
            parent=self.name, app_profile_id=app_profile_id,
            app_profile=app_profile, ignore_warnings=ignore_warnings,
            metadata=metadata)

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

    def update_app_profile(self, app_profile_id, update_mask, etag='',
                           description='', ignore_warnings=None, metadata=None,
                           routing_policy_type=ROUTING_POLICY_TYPE_ANY,
                           cluster_id=None, allow_transactional_writes=False):
        """Updates an app profile within an instance.

        :type: app_profile_id: str
        :param app_profile_id: The unique name for the new app profile.

        :type: update_mask: list
        :param: update_mask: Name of the parameters of AppProfiles that
                                needed to update.

        :type: etag: str
        :param: etag: (Optional) Strongly validated etag for optimistic
                        concurrency control. Preserve the value returned
                        from ``GetAppProfile`` when calling
                        ``UpdateAppProfile`` to fail the request if there has
                        been a modification in the mean time. The
                        ``update_mask`` of the request need not include
                        ``etag`` for this protection to apply.

        :type: description: str
        :param: description: (Optional) Optional long form description of the
                                use case for this AppProfile.

        :type: ignore_warnings: bool
        :param: ignore_warnings: (Optional) If true, ignore safety checks when
                                    creating the app profile.

        :type: metadata: [Sequence[Tuple[str, str]]]
        :param: metadata: (Optional) Additional metadata that is provided to
                            the method.

        :type: routing_policy_type: int
        :parm: routing_policy_type: (Optional) There are two routing policies
                                    1. ROUTING_POLICY_TYPE_ANY = 1 and
                                    2. ROUTING_POLICY_TYPE_SINGLE = 2.
                                    By default it is ROUTING_POLICY_TYPE_ANY
                                    which is MultiClusterRoutingUseAny policy
                                    and for SingleClusterRouting user need to
                                    assign 2 and that will need cluster_id
                                    and allow_transactional_writes
                                    for single cluster routing policy proto.

        :type: cluster_id: str
        :param: cluster_id: (Optional) Unique cluster_id  to create AppProfile
                            on selected cluster route. It is only required
                            when routing_policy_type is
                            ROUTING_POLICY_TYPE_SINGLE.

        :type: allow_transactional_writes: bool
        :param: allow_transactional_writes: (Optional) If true, allow
                                            transactional writes to single
                                            cluster routing, if cluster_id is
                                            given.

        :rtype: :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
        :return: The AppProfile instance.
        """
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
            name=name, etag=etag, description=description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )
        update_mask = field_mask_pb2.FieldMask(paths=update_mask)

        return self._client._instance_admin_client.update_app_profile(
            app_profile=update_app_profile, update_mask=update_mask,
            ignore_warnings=ignore_warnings, metadata=metadata
        )

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
