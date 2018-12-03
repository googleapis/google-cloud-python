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
from google.cloud.bigtable.cluster import Cluster
from google.cloud.bigtable.app_profile import AppProfile

from google.protobuf import field_mask_pb2

from google.cloud.bigtable_admin_v2.types import instance_pb2

from google.api_core.exceptions import NotFound

from google.cloud.bigtable.policy import Policy


_EXISTING_INSTANCE_LOCATION_ID = "see-existing-cluster"
_INSTANCE_NAME_RE = re.compile(
    r"^projects/(?P<project>[^/]+)/" r"instances/(?P<instance_id>[a-z][-a-z0-9]*)$"
)


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

    :type instance_type: int
    :param instance_type: (Optional) The type of the instance.
                          Possible values are represented
                          by the following constants:
                          :data:`google.cloud.bigtable.enums.InstanceType.PRODUCTION`.
                          :data:`google.cloud.bigtable.enums.InstanceType.DEVELOPMENT`,
                          Defaults to
                          :data:`google.cloud.bigtable.enums.InstanceType.UNSPECIFIED`.

    :type labels: dict
    :param labels: (Optional) Labels are a flexible and lightweight
                   mechanism for organizing cloud resources into groups
                   that reflect a customer's organizational needs and
                   deployment strategies. They can be used to filter
                   resources and aggregate metrics. Label keys must be
                   between 1 and 63 characters long. Maximum 64 labels can
                   be associated with a given resource. Label values must
                   be between 0 and 63 characters long. Keys and values
                   must both be under 128 bytes.

    :type _state: int
    :param _state: (`OutputOnly`)
                   The current state of the instance.
                   Possible values are represented by the following constants:
                   :data:`google.cloud.bigtable.enums.Instance.State.STATE_NOT_KNOWN`.
                   :data:`google.cloud.bigtable.enums.Instance.State.READY`.
                   :data:`google.cloud.bigtable.enums.Instance.State.CREATING`.
    """

    def __init__(
        self,
        instance_id,
        client,
        display_name=None,
        instance_type=None,
        labels=None,
        _state=None,
    ):
        self.instance_id = instance_id
        self._client = client
        self.display_name = display_name or instance_id
        self.type_ = instance_type
        self.labels = labels
        self._state = _state

    def _update_from_pb(self, instance_pb):
        """Refresh self from the server-provided protobuf.
        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not instance_pb.display_name:  # Simple field (string)
            raise ValueError("Instance protobuf does not contain display_name")
        self.display_name = instance_pb.display_name
        self.type_ = instance_pb.type
        self.labels = dict(instance_pb.labels)
        self._state = instance_pb.state

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
            raise ValueError(
                "Instance protobuf name was not in the " "expected format.",
                instance_pb.name,
            )
        if match.group("project") != client.project:
            raise ValueError(
                "Project ID on instance does not match the " "project ID on the client"
            )
        instance_id = match.group("instance_id")

        result = cls(instance_id, client)
        result._update_from_pb(instance_pb)
        return result

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
            project=self._client.project, instance=self.instance_id
        )

    @property
    def state(self):
        """google.cloud.bigtable.enums.Instance.State: state of Instance."""
        return self._state

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the display_name. Instead, it only compares
        #       identifying values instance ID and client. This is
        #       intentional, since the same instance can be in different states
        #       if not synchronized. Instances with similar instance
        #       settings but different clients can't be used in the same way.
        return other.instance_id == self.instance_id and other._client == self._client

    def __ne__(self, other):
        return not self == other

    def create(
        self,
        location_id=None,
        serve_nodes=None,
        default_storage_type=None,
        clusters=None,
    ):
        """Create this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_create_prod_instance]
            :end-before: [END bigtable_create_prod_instance]

        .. note::

            Uses the ``project`` and ``instance_id`` on the current
            :class:`Instance` in addition to the ``display_name``.
            To change them before creating, reset the values via

            .. code:: python

                instance.display_name = 'New display name'
                instance.instance_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :type location_id: str
        :param location_id: (Creation Only) The location where nodes and
                            storage of the cluster owned by this instance
                            reside. For best performance, clients should be
                            located as close as possible to cluster's location.
                            For list of supported locations refer to
                            https://cloud.google.com/bigtable/docs/locations


        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the instance's
                            cluster; used to set up the instance's cluster.

        :type default_storage_type: int
        :param default_storage_type: (Optional) The storage media type for
                                      persisting Bigtable data.
                                      Possible values are represented
                                      by the following constants:
                                      :data:`google.cloud.bigtable.enums.StorageType.SSD`.
                                      :data:`google.cloud.bigtable.enums.StorageType.SHD`,
                                      Defaults to
                                      :data:`google.cloud.bigtable.enums.StorageType.UNSPECIFIED`.

        :type clusters: class:`~[~google.cloud.bigtable.cluster.Cluster]`
        :param clusters: List of clusters to be created.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the create
                    operation.

        :raises: :class:`ValueError <exceptions.ValueError>` if both
                 ``clusters`` and one of ``location_id``, ``serve_nodes``
                 and ``default_storage_type`` are set.
        """

        if clusters is None:
            cluster_id = "{}-cluster".format(self.instance_id)

            clusters = [
                self.cluster(
                    cluster_id,
                    location_id=location_id,
                    serve_nodes=serve_nodes,
                    default_storage_type=default_storage_type,
                )
            ]
        elif (
            location_id is not None
            or serve_nodes is not None
            or default_storage_type is not None
        ):
            raise ValueError(
                "clusters and one of location_id, serve_nodes, \
                             default_storage_type can not be set \
                             simultaneously."
            )

        instance_pb = instance_pb2.Instance(
            display_name=self.display_name, type=self.type_, labels=self.labels
        )

        parent = self._client.project_path

        return self._client.instance_admin_client.create_instance(
            parent=parent,
            instance_id=self.instance_id,
            instance=instance_pb,
            clusters={c.cluster_id: c._to_pb() for c in clusters},
        )

    def exists(self):
        """Check whether the instance already exists.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_check_instance_exists]
            :end-before: [END bigtable_check_instance_exists]

        :rtype: bool
        :returns: True if the table exists, else False.
        """
        try:
            self._client.instance_admin_client.get_instance(name=self.name)
            return True
        # NOTE: There could be other exceptions that are returned to the user.
        except NotFound:
            return False

    def reload(self):
        """Reload the metadata for this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_reload_instance]
            :end-before: [END bigtable_reload_instance]
        """
        instance_pb = self._client.instance_admin_client.get_instance(self.name)

        # NOTE: _update_from_pb does not check that the project and
        #       instance ID on the response match the request.
        self._update_from_pb(instance_pb)

    def update(self):
        """Updates an instance within a project.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_update_instance]
            :end-before: [END bigtable_update_instance]

        .. note::

            Updates any or all of the following values:
            ``display_name``
            ``type``
            ``labels``
            To change a value before
            updating, assign that values via

            .. code:: python

                instance.display_name = 'New display name'

            before calling :meth:`update`.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the update
                    operation.
        """
        update_mask_pb = field_mask_pb2.FieldMask()
        if self.display_name is not None:
            update_mask_pb.paths.append("display_name")
        if self.type_ is not None:
            update_mask_pb.paths.append("type")
        if self.labels is not None:
            update_mask_pb.paths.append("labels")
        instance_pb = instance_pb2.Instance(
            name=self.name,
            display_name=self.display_name,
            type=self.type_,
            labels=self.labels,
        )

        return self._client.instance_admin_client.partial_update_instance(
            instance=instance_pb, update_mask=update_mask_pb
        )

    def delete(self):
        """Delete this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_delete_instance]
            :end-before: [END bigtable_delete_instance]

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

    def get_iam_policy(self):
        """Gets the access control policy for an instance resource.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_get_iam_policy]
            :end-before: [END bigtable_get_iam_policy]

        :rtype: :class:`google.cloud.bigtable.policy.Policy`
        :returns: The current IAM policy of this instance
        """
        instance_admin_client = self._client.instance_admin_client
        resp = instance_admin_client.get_iam_policy(resource=self.name)
        return Policy.from_api_repr(self._to_dict_from_policy_pb(resp))

    def set_iam_policy(self, policy):
        """Sets the access control policy on an instance resource. Replaces any
        existing policy.

        For more information about policy, please see documentation of
        class `google.cloud.bigtable.policy.Policy`

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_set_iam_policy]
            :end-before: [END bigtable_set_iam_policy]

        :type policy: :class:`google.cloud.bigtable.policy.Policy`
        :param policy: A new IAM policy to replace the current IAM policy
                       of this instance

        :rtype: :class:`google.cloud.bigtable.policy.Policy`
        :returns: The current IAM policy of this instance.
        """
        instance_admin_client = self._client.instance_admin_client
        resp = instance_admin_client.set_iam_policy(
            resource=self.name, policy=policy.to_api_repr()
        )
        return Policy.from_api_repr(self._to_dict_from_policy_pb(resp))

    def test_iam_permissions(self, permissions):
        """Returns permissions that the caller has on the specified instance
        resource.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_test_iam_permissions]
            :end-before: [END bigtable_test_iam_permissions]

        :type permissions: list
        :param permissions: The set of permissions to check for
               the ``resource``. Permissions with wildcards (such as '*'
               or 'storage.*') are not allowed. For more information see
               `IAM Overview
               <https://cloud.google.com/iam/docs/overview#permissions>`_.
               `Bigtable Permissions
               <https://cloud.google.com/bigtable/docs/access-control>`_.

        :rtype: list
        :returns: A List(string) of permissions allowed on the instance
        """
        instance_admin_client = self._client.instance_admin_client
        resp = instance_admin_client.test_iam_permissions(
            resource=self.name, permissions=permissions
        )
        return list(resp.permissions)

    def _to_dict_from_policy_pb(self, policy):
        """Returns a dictionary representation of resource returned from
        the getIamPolicy API to use as parameter for
        :meth: google.api_core.iam.Policy.from_api_repr
        """
        pb_dict = {}
        bindings = [
            {"role": binding.role, "members": binding.members}
            for binding in policy.bindings
        ]
        pb_dict["etag"] = policy.etag
        pb_dict["version"] = policy.version
        pb_dict["bindings"] = bindings
        return pb_dict

    def cluster(
        self, cluster_id, location_id=None, serve_nodes=None, default_storage_type=None
    ):
        """Factory to create a cluster associated with this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_create_cluster]
            :end-before: [END bigtable_create_cluster]

        :type cluster_id: str
        :param cluster_id: The ID of the cluster.

        :type instance: :class:`~google.cloud.bigtable.instance.Instance`
        :param instance: The instance where the cluster resides.

        :type location_id: str
        :param location_id: (Creation Only) The location where this cluster's
                            nodes and storage reside. For best performance,
                            clients should be located as close as possible to
                            this cluster.
                            For list of supported locations refer to
                            https://cloud.google.com/bigtable/docs/locations

        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the cluster.

        :type default_storage_type: int
        :param default_storage_type: (Optional) The type of storage
                                     Possible values are represented by the
                                     following constants:
                                     :data:`google.cloud.bigtable.enums.StorageType.SSD`.
                                     :data:`google.cloud.bigtable.enums.StorageType.SHD`,
                                     Defaults to
                                     :data:`google.cloud.bigtable.enums.StorageType.UNSPECIFIED`.

        :rtype: :class:`~google.cloud.bigtable.instance.Cluster`
        :returns: a cluster owned by this instance.
        """
        return Cluster(
            cluster_id,
            self,
            location_id=location_id,
            serve_nodes=serve_nodes,
            default_storage_type=default_storage_type,
        )

    def list_clusters(self):
        """List the clusters in this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_list_clusters_on_instance]
            :end-before: [END bigtable_list_clusters_on_instance]

        :rtype: tuple
        :returns:
            (clusters, failed_locations), where 'clusters' is list of
            :class:`google.cloud.bigtable.instance.Cluster`, and
            'failed_locations' is a list of locations which could not
            be resolved.
        """
        resp = self._client.instance_admin_client.list_clusters(self.name)
        clusters = [Cluster.from_pb(cluster, self) for cluster in resp.clusters]
        return clusters, resp.failed_locations

    def table(self, table_id, app_profile_id=None):
        """Factory to create a table associated with this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_create_table]
            :end-before: [END bigtable_create_table]

        :type table_id: str
        :param table_id: The ID of the table.

        :type app_profile_id: str
        :param app_profile_id: (Optional) The unique name of the AppProfile.

        :rtype: :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The table owned by this instance.
        """
        return Table(table_id, self, app_profile_id=app_profile_id)

    def list_tables(self):
        """List the tables in this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_list_tables]
            :end-before: [END bigtable_list_tables]

        :rtype: list of :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The list of tables owned by the instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if one of the
                 returned tables has a name that is not of the expected format.
        """
        table_list_pb = self._client.table_admin_client.list_tables(self.name)

        result = []
        for table_pb in table_list_pb:
            table_prefix = self.name + "/tables/"
            if not table_pb.name.startswith(table_prefix):
                raise ValueError(
                    "Table name {} not of expected format".format(table_pb.name)
                )
            table_id = table_pb.name[len(table_prefix) :]
            result.append(self.table(table_id))

        return result

    def app_profile(
        self,
        app_profile_id,
        routing_policy_type=None,
        description=None,
        cluster_id=None,
        allow_transactional_writes=None,
    ):
        """Factory to create AppProfile associated with this instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_create_app_profile]
            :end-before: [END bigtable_create_app_profile]

        :type app_profile_id: str
        :param app_profile_id: The ID of the AppProfile. Must be of the form
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

        :type: cluster_id: str
        :param: cluster_id: (Optional) Unique cluster_id which is only required
                            when routing_policy_type is
                            ROUTING_POLICY_TYPE_SINGLE.

        :type: allow_transactional_writes: bool
        :param: allow_transactional_writes: (Optional) If true, allow
                                            transactional writes for
                                            ROUTING_POLICY_TYPE_SINGLE.

        :rtype: :class:`~google.cloud.bigtable.app_profile.AppProfile>`
        :returns: AppProfile for this instance.
        """
        return AppProfile(
            app_profile_id,
            self,
            routing_policy_type=routing_policy_type,
            description=description,
            cluster_id=cluster_id,
            allow_transactional_writes=allow_transactional_writes,
        )

    def list_app_profiles(self):
        """Lists information about AppProfiles in an instance.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_list_app_profiles]
            :end-before: [END bigtable_list_app_profiles]

        :rtype: :list:[`~google.cloud.bigtable.app_profile.AppProfile`]
        :returns: A :list:[`~google.cloud.bigtable.app_profile.AppProfile`].
                  By default, this is a list of
                  :class:`~google.cloud.bigtable.app_profile.AppProfile`
                  instances.
        """
        resp = self._client.instance_admin_client.list_app_profiles(self.name)
        return [AppProfile.from_pb(app_profile, self) for app_profile in resp]
