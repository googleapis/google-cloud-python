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

from google.cloud.spanner_admin_instance_v1.proto import spanner_instance_admin_pb2_grpc


class InstanceAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.spanner.admin.instance.v1 InstanceAdmin API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spanner.admin",
    )

    def __init__(
        self, channel=None, credentials=None, address="spanner.googleapis.com:443"
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
            "instance_admin_stub": spanner_instance_admin_pb2_grpc.InstanceAdminStub(
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
    def create_channel(cls, address="spanner.googleapis.com:443", credentials=None):
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
    def list_instance_configs(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.list_instance_configs`.

        Lists the supported instance configurations for a given project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].ListInstanceConfigs

    @property
    def get_instance_config(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.get_instance_config`.

        Gets information about a particular instance configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].GetInstanceConfig

    @property
    def list_instances(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.list_instances`.

        Lists all instances in the given project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].ListInstances

    @property
    def get_instance(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.get_instance`.

        Gets information about a particular instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].GetInstance

    @property
    def create_instance(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.create_instance`.

        Creates an instance and begins preparing it to begin serving. The
        returned ``long-running operation`` can be used to track the progress of
        preparing the new instance. The instance name is assigned by the caller.
        If the named instance already exists, ``CreateInstance`` returns
        ``ALREADY_EXISTS``.

        Immediately upon completion of this request:

        -  The instance is readable via the API, with all requested attributes
           but no allocated resources. Its state is ``CREATING``.

        Until completion of the returned operation:

        -  Cancelling the operation renders the instance immediately unreadable
           via the API.
        -  The instance can be deleted.
        -  All other attempts to modify the instance are rejected.

        Upon completion of the returned operation:

        -  Billing for all successfully-allocated resources begins (some types
           may have lower than the requested levels).
        -  Databases can be created in the instance.
        -  The instance's allocated resource levels are readable via the API.
        -  The instance's state becomes ``READY``.

        The returned ``long-running operation`` will have a name of the format
        ``<instance_name>/operations/<operation_id>`` and can be used to track
        creation of the instance. The ``metadata`` field type is
        ``CreateInstanceMetadata``. The ``response`` field type is ``Instance``,
        if successful.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].CreateInstance

    @property
    def update_instance(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.update_instance`.

        Updates an instance, and begins allocating or releasing resources as
        requested. The returned ``long-running  operation`` can be used to track
        the progress of updating the instance. If the named instance does not
        exist, returns ``NOT_FOUND``.

        Immediately upon completion of this request:

        -  For resource types for which a decrease in the instance's allocation
           has been requested, billing is based on the newly-requested level.

        Until completion of the returned operation:

        -  Cancelling the operation sets its metadata's ``cancel_time``, and
           begins restoring resources to their pre-request values. The operation
           is guaranteed to succeed at undoing all resource changes, after which
           point it terminates with a ``CANCELLED`` status.
        -  All other attempts to modify the instance are rejected.
        -  Reading the instance via the API continues to give the pre-request
           resource levels.

        Upon completion of the returned operation:

        -  Billing begins for all successfully-allocated resources (some types
           may have lower than the requested levels).
        -  All newly-reserved resources are available for serving the instance's
           tables.
        -  The instance's new resource levels are readable via the API.

        The returned ``long-running operation`` will have a name of the format
        ``<instance_name>/operations/<operation_id>`` and can be used to track
        the instance modification. The ``metadata`` field type is
        ``UpdateInstanceMetadata``. The ``response`` field type is ``Instance``,
        if successful.

        Authorization requires ``spanner.instances.update`` permission on
        resource ``name``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].UpdateInstance

    @property
    def delete_instance(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.delete_instance`.

        Deletes an instance.

        Immediately upon completion of the request:

        -  Billing ceases for all of the instance's reserved resources.

        Soon afterward:

        -  The instance and *all of its databases* immediately and irrevocably
           disappear from the API. All data in the databases is permanently
           deleted.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].DeleteInstance

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.set_iam_policy`.

        Sets the access control policy on an instance resource. Replaces any
        existing policy.

        Authorization requires ``spanner.instances.setIamPolicy`` on
        ``resource``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.get_iam_policy`.

        Gets the access control policy for an instance resource. Returns an
        empty policy if an instance exists but does not have a policy set.

        Authorization requires ``spanner.instances.getIamPolicy`` on
        ``resource``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`InstanceAdminClient.test_iam_permissions`.

        Returns permissions that the caller has on the specified instance
        resource.

        Attempting this RPC on a non-existent Cloud Spanner instance resource
        will result in a NOT\_FOUND error if the user has
        ``spanner.instances.list`` permission on the containing Google Cloud
        Project. Otherwise returns an empty set of permissions.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["instance_admin_stub"].TestIamPermissions
