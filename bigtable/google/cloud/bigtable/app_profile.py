# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""User firendly container for Google Cloud Bigtable App Profile."""


import re

from google.cloud.bigtable.enums import RoutingPolicyType
from google.cloud.bigtable_admin_v2.types import instance_pb2
from google.protobuf import field_mask_pb2
from google.api_core.exceptions import NotFound

_APP_PROFILE_NAME_RE = re.compile(
    r'^projects/(?P<project>[^/]+)/'
    r'instances/(?P<instance>[^/]+)/appProfiles/'
    r'(?P<app_profile_id>[_a-zA-Z0-9][-_.a-zA-Z0-9]*)$')


class AppProfile(object):
    """Representation of a Google Cloud Bigtable App Profile.

    We can use a :class:`AppProfile` to:

    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    :type app_profile_id: str
    :param app_profile_id: The ID of the app profile. Must be of the form
                          ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

    :type: routing_policy_type: int
        :param: routing_policy_type: The type of the routing policy.
                                     Possible values are represented
                                     by the following constants:
                                     :data:`google.cloud.bigtable.enums.RoutingPolicyType.ANY`
                                     :data:`google.cloud.bigtable.enums.RoutingPolicyType.SINGLE`

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
    """

    def __init__(self, app_profile_id, instance,
                 routing_policy_type=None,
                 description=None, cluster_id=None,
                 allow_transactional_writes=None):
        self.app_profile_id = app_profile_id
        self._instance = instance
        self.routing_policy_type = routing_policy_type
        self.description = description
        self.cluster_id = cluster_id
        self.allow_transactional_writes = allow_transactional_writes

    @property
    def name(self):
        """App Profile name used in requests.

        .. note::

          This property will not change if ``app_profile_id`` does not, but
          the return value is not cached.

        The app profile name is of the form
            ``"projects/../instances/../app_profile/{app_profile_id}"``

        :rtype: str
        :returns: The app profile name.
        """
        return self._instance._client.instance_admin_client.app_profile_path(
            self._instance._client.project, self._instance.instance_id,
            self.app_profile_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the routing_policy_type. Instead, it only compares
        #       identifying values instance, app profile ID and client. This is
        #       intentional, since the same app profile can be in different
        #       states if not synchronized.
        return (other.app_profile_id == self.app_profile_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_pb(cls, app_profile_pb, instance):
        """Creates an instance app_profile from a protobuf.

        :type app_profile_pb: :class:`instance_pb2.app_profile_pb`
        :param app_profile_pb: An instance protobuf object.

        :type instance: :class:`google.cloud.bigtable.instance.Instance`
        :param instance: The instance that owns the cluster.

        :rtype: :class:`AppProfile`
        :returns: The AppProfile parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the AppProfile
                 name does not match
                 ``projects/{project}/instances/{instance_id}/appProfiles/{app_profile_id}``
                 or if the parsed instance ID does not match the istance ID
                 on the client.
                 or if the parsed project ID does not match the project ID
                 on the client.
        """
        match_app_profile_name = (
            _APP_PROFILE_NAME_RE.match(app_profile_pb.name))
        if match_app_profile_name is None:
            raise ValueError('AppProfile protobuf name was not in the '
                             'expected format.', app_profile_pb.name)
        if match_app_profile_name.group('instance') != instance.instance_id:
            raise ValueError('Instance ID on app_profile does not match the '
                             'instance ID on the client')
        if match_app_profile_name.group('project') != instance._client.project:
            raise ValueError('Project ID on app_profile does not match the '
                             'project ID on the client')
        app_profile_id = match_app_profile_name.group('app_profile_id')

        result = cls(app_profile_id, instance)
        result._update_from_pb(app_profile_pb)
        return result

    def _update_from_pb(self, app_profile_pb):
        """Refresh self from the server-provided protobuf.
        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        self.routing_policy_type = None
        self.allow_transactional_writes = None
        self.cluster_id = None

        self.description = app_profile_pb.description

        routing_policy_type = None
        if app_profile_pb.HasField('multi_cluster_routing_use_any'):
            routing_policy_type = RoutingPolicyType.ANY
            self.allow_transactional_writes = False
        else:
            routing_policy_type = RoutingPolicyType.SINGLE
            self.cluster_id = app_profile_pb.single_cluster_routing.cluster_id
            self.allow_transactional_writes = (
                app_profile_pb.single_cluster_routing
                .allow_transactional_writes)
        self.routing_policy_type = routing_policy_type

    def reload(self):
        """Reload the metadata for this cluster"""

        app_profile_pb = (
            self._instance._client.instance_admin_client.get_app_profile(
                self.name))

        # NOTE: _update_from_pb does not check that the project and
        #       app_profile ID on the response match the request.
        self._update_from_pb(app_profile_pb)

    def exists(self):
        """Check whether the app profile already exists.

        :rtype: bool
        :returns: True if the app profile exists, else False.
        """
        client = self._instance._client
        try:
            client.instance_admin_client.get_app_profile(self.name)
            return True
        # NOTE: There could be other exceptions that are returned to the user.
        except NotFound:
            return False

    def create(self, ignore_warnings=None):
        """Create this app profile.

        .. note::

            Uses the ``project``, ``instance`` and ``app_profile_id`` on the
            current :class:`AppProfile` in addition to the ``serve_nodes``.
            To change them before creating, reset the values via

            .. code:: python

                cluster.serve_nodes = 8
                cluster.cluster_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :type: ignore_warnings: bool
        :param: ignore_warnings: (Optional) If true, ignore safety checks when
                                 creating the app profile.
        """
        if not self.routing_policy_type:
            raise ValueError('AppProfile required routing policy.')

        single_cluster_routing = None
        multi_cluster_routing_use_any = None

        if self.routing_policy_type == RoutingPolicyType.ANY:
            multi_cluster_routing_use_any = (
                instance_pb2.AppProfile.MultiClusterRoutingUseAny())

        if self.routing_policy_type == RoutingPolicyType.SINGLE:
            single_cluster_routing = (
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=self.cluster_id,
                    allow_transactional_writes=self.allow_transactional_writes)
            )

        client = self._instance._client
        app_profile_pb = instance_pb2.AppProfile(
            name=self.name, description=self.description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )
        return self.from_pb(client._instance_admin_client.create_app_profile(
            parent=self._instance.name, app_profile_id=self.app_profile_id,
            app_profile=app_profile_pb, ignore_warnings=ignore_warnings),
            self._instance)

    def update(self, ignore_warnings=None):
        """Update this app_profile.

        .. note::

            Update any or all fo the following values:
            ``description``
            TODO: put full detail of properties that could be updated
        """
        print('update\n')
        if not self.routing_policy_type:
            raise ValueError('AppProfile required routing policy.')

        update_mask_pb = field_mask_pb2.FieldMask()
        single_cluster_routing = None
        multi_cluster_routing_use_any = None

        if self.description is not None:
            update_mask_pb.paths.append('description')

        print('self policy', self.routing_policy_type)
        if self.routing_policy_type == RoutingPolicyType.ANY:
            multi_cluster_routing_use_any = (
                instance_pb2.AppProfile.MultiClusterRoutingUseAny())
            update_mask_pb.paths.append('multi_cluster_routing_use_any')

        if self.routing_policy_type == RoutingPolicyType.SINGLE:
            print('self.cluster', self.cluster_id)
            print('self.writes', self.allow_transactional_writes)
            single_cluster_routing = (
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=self.cluster_id,
                    allow_transactional_writes=self.allow_transactional_writes
                ))
            update_mask_pb.paths.append('single_cluster_routing')

        client = self._instance._client
        update_app_profile_pb = instance_pb2.AppProfile(
            name=self.name, description=self.description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            single_cluster_routing=single_cluster_routing
        )
        print('profile to update with', update_app_profile_pb)
        print('update_mask', update_mask_pb)
        return client._instance_admin_client.update_app_profile(
            app_profile=update_app_profile_pb, update_mask=update_mask_pb,
            ignore_warnings=ignore_warnings)

    def delete(self, ignore_warnings=None):
        """Delete this app profile.

        :type: ignore_warnings: bool
        :param: ignore_warnings: If true, ignore safety checks when deleting
                the app profile.

        :raises: google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason. google.api_core.exceptions.RetryError:
                If the request failed due to a retryable error and retry
                attempts failed. ValueError: If the parameters are invalid.
        """
        print('deleting', self.name)
        client = self._instance._client
        client.instance_admin_client.delete_app_profile(
            self.name, ignore_warnings)
