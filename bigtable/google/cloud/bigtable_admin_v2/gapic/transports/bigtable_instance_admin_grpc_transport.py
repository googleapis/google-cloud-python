# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2_grpc


class BigtableInstanceAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.bigtable.admin.v2 BigtableInstanceAdmin API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigtable.admin",
        "https://www.googleapis.com/auth/bigtable.admin.cluster",
        "https://www.googleapis.com/auth/bigtable.admin.instance",
        "https://www.googleapis.com/auth/bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-bigtable.admin",
        "https://www.googleapis.com/auth/cloud-bigtable.admin.cluster",
        "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    def __init__(
        self, channel=None, credentials=None, address="bigtableadmin.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "bigtable_instance_admin_stub": bigtable_instance_admin_pb2_grpc.BigtableInstanceAdminStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="bigtableadmin.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_instance(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.create_instance`.

        Create an instance within a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].CreateInstance

    @property
    def get_instance(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.get_instance`.

        Gets information about an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].GetInstance

    @property
    def list_instances(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.list_instances`.

        Lists information about instances in a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].ListInstances

    @property
    def update_instance(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.update_instance`.

        Updates an instance within a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].UpdateInstance

    @property
    def partial_update_instance(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.partial_update_instance`.

        Partially updates an instance within a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].PartialUpdateInstance

    @property
    def delete_instance(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.delete_instance`.

        Delete an instance from a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].DeleteInstance

    @property
    def create_cluster(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.create_cluster`.

        Creates a cluster within an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].CreateCluster

    @property
    def get_cluster(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.get_cluster`.

        Gets information about a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].GetCluster

    @property
    def list_clusters(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.list_clusters`.

        Lists information about clusters in an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].ListClusters

    @property
    def update_cluster(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.update_cluster`.

        Updates a cluster within an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].UpdateCluster

    @property
    def delete_cluster(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.delete_cluster`.

        Deletes a cluster from an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].DeleteCluster

    @property
    def create_app_profile(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.create_app_profile`.

        Creates an app profile within an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].CreateAppProfile

    @property
    def get_app_profile(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.get_app_profile`.

        Gets information about an app profile.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].GetAppProfile

    @property
    def list_app_profiles(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.list_app_profiles`.

        Lists information about app profiles in an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].ListAppProfiles

    @property
    def update_app_profile(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.update_app_profile`.

        Updates an app profile within an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].UpdateAppProfile

    @property
    def delete_app_profile(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.delete_app_profile`.

        Deletes an app profile from an instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].DeleteAppProfile

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.get_iam_policy`.

        Gets the access control policy for an instance resource. Returns an empty
        policy if an instance exists but does not have a policy set.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].GetIamPolicy

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.set_iam_policy`.

        Sets the access control policy on an instance resource. Replaces any
        existing policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].SetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`BigtableInstanceAdminClient.test_iam_permissions`.

        Returns permissions that the caller has on the specified instance resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_instance_admin_stub"].TestIamPermissions
