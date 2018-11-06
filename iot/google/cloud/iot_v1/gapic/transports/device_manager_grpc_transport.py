# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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

from google.cloud.iot_v1.proto import device_manager_pb2_grpc


class DeviceManagerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.iot.v1 DeviceManager API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """
    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloudiot',
    )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 address='cloudiot.googleapis.com:443'):
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
                'The `channel` and `credentials` arguments are mutually '
                'exclusive.', )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
            )

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            'device_manager_stub':
            device_manager_pb2_grpc.DeviceManagerStub(channel),
        }

    @classmethod
    def create_channel(cls,
                       address='cloudiot.googleapis.com:443',
                       credentials=None):
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
            address,
            credentials=credentials,
            scopes=cls._OAUTH_SCOPES,
        )

    @property
    def create_device_registry(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Creates a device registry that contains devices.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].CreateDeviceRegistry

    @property
    def get_device_registry(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Gets a device registry configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].GetDeviceRegistry

    @property
    def update_device_registry(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Updates a device registry configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].UpdateDeviceRegistry

    @property
    def delete_device_registry(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Deletes a device registry configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].DeleteDeviceRegistry

    @property
    def list_device_registries(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists device registries.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].ListDeviceRegistries

    @property
    def create_device(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Creates a device in a device registry.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].CreateDevice

    @property
    def get_device(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Gets details about a device.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].GetDevice

    @property
    def update_device(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Updates a device.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].UpdateDevice

    @property
    def delete_device(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Deletes a device.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].DeleteDevice

    @property
    def list_devices(self):
        """Return the gRPC stub for {$apiMethod.name}.

        List devices in a device registry.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].ListDevices

    @property
    def modify_cloud_to_device_config(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Modifies the configuration for the device, which is eventually sent from
        the Cloud IoT Core servers. Returns the modified configuration version and
        its metadata.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].ModifyCloudToDeviceConfig

    @property
    def list_device_config_versions(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists the last few versions of the device configuration in descending
        order (i.e.: newest first).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].ListDeviceConfigVersions

    @property
    def list_device_states(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists the last few versions of the device state in descending order (i.e.:
        newest first).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].ListDeviceStates

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of permissions,
        not a NOT\_FOUND error.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['device_manager_stub'].TestIamPermissions
