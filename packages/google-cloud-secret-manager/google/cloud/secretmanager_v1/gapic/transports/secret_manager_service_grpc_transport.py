# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.secretmanager_v1.proto import service_pb2_grpc


class SecretManagerServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.secretmanager.v1 SecretManagerService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="secretmanager.googleapis.com:443"
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
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "secret_manager_service_stub": service_pb2_grpc.SecretManagerServiceStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="secretmanager.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_secrets(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.list_secrets`.

        Lists ``Secrets``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].ListSecrets

    @property
    def create_secret(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.create_secret`.

        Creates a new ``Secret`` containing no ``SecretVersions``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].CreateSecret

    @property
    def add_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.add_secret_version`.

        Creates a new ``SecretVersion`` containing secret data and attaches
        it to an existing ``Secret``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].AddSecretVersion

    @property
    def get_secret(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.get_secret`.

        Gets metadata for a given ``Secret``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].GetSecret

    @property
    def update_secret(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.update_secret`.

        Updates metadata of an existing ``Secret``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].UpdateSecret

    @property
    def delete_secret(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.delete_secret`.

        Deletes a ``Secret``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].DeleteSecret

    @property
    def list_secret_versions(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.list_secret_versions`.

        Lists ``SecretVersions``. This call does not return secret data.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].ListSecretVersions

    @property
    def get_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.get_secret_version`.

        Gets metadata for a ``SecretVersion``.

        ``projects/*/secrets/*/versions/latest`` is an alias to the ``latest``
        ``SecretVersion``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].GetSecretVersion

    @property
    def access_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.access_secret_version`.

        Accesses a ``SecretVersion``. This call returns the secret data.

        ``projects/*/secrets/*/versions/latest`` is an alias to the ``latest``
        ``SecretVersion``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].AccessSecretVersion

    @property
    def disable_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.disable_secret_version`.

        Disables a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``DISABLED``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].DisableSecretVersion

    @property
    def enable_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.enable_secret_version`.

        Enables a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``ENABLED``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].EnableSecretVersion

    @property
    def destroy_secret_version(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.destroy_secret_version`.

        Destroys a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``DESTROYED`` and
        irrevocably destroys the secret data.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].DestroySecretVersion

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.set_iam_policy`.

        Sets the access control policy on the specified secret. Replaces any
        existing policy.

        Permissions on ``SecretVersions`` are enforced according to the policy
        set on the associated ``Secret``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.get_iam_policy`.

        Gets the access control policy for a secret.
        Returns empty policy if the secret exists and does not have a policy set.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`SecretManagerServiceClient.test_iam_permissions`.

        Returns permissions that a caller has for the specified secret. If
        the secret does not exist, this call returns an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["secret_manager_service_stub"].TestIamPermissions
