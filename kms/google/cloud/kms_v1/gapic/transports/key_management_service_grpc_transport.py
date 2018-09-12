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

from google.cloud.kms_v1.proto import service_pb2_grpc
from google.iam.v1 import iam_policy_pb2


class KeyManagementServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.kms.v1 KeyManagementService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """
    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 address='cloudkms.googleapis.com:443'):
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
            'key_management_service_stub':
            service_pb2_grpc.KeyManagementServiceStub(channel),
            'iam_policy_stub':
            iam_policy_pb2.IAMPolicyStub(channel),
        }

    @classmethod
    def create_channel(cls,
                       address='cloudkms.googleapis.com:443',
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
    def list_key_rings(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists ``KeyRings``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].ListKeyRings

    @property
    def list_crypto_keys(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists ``CryptoKeys``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].ListCryptoKeys

    @property
    def list_crypto_key_versions(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists ``CryptoKeyVersions``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].ListCryptoKeyVersions

    @property
    def get_key_ring(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns metadata for a given ``KeyRing``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].GetKeyRing

    @property
    def get_crypto_key(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns metadata for a given ``CryptoKey``, as well as its
        ``primary`` ``CryptoKeyVersion``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].GetCryptoKey

    @property
    def get_crypto_key_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns metadata for a given ``CryptoKeyVersion``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].GetCryptoKeyVersion

    @property
    def create_key_ring(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Create a new ``KeyRing`` in a given Project and Location.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].CreateKeyRing

    @property
    def create_crypto_key(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Create a new ``CryptoKey`` within a ``KeyRing``.

        ``CryptoKey.purpose`` and
        ``CryptoKey.version_template.algorithm``
        are required.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].CreateCryptoKey

    @property
    def create_crypto_key_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Create a new ``CryptoKeyVersion`` in a ``CryptoKey``.

        The server will assign the next sequential id. If unset,
        ``state`` will be set to
        ``ENABLED``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            'key_management_service_stub'].CreateCryptoKeyVersion

    @property
    def update_crypto_key(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Update a ``CryptoKey``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].UpdateCryptoKey

    @property
    def update_crypto_key_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Update a ``CryptoKeyVersion``'s metadata.

        ``state`` may be changed between
        ``ENABLED`` and
        ``DISABLED`` using this
        method. See ``DestroyCryptoKeyVersion`` and ``RestoreCryptoKeyVersion`` to
        move between other states.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            'key_management_service_stub'].UpdateCryptoKeyVersion

    @property
    def encrypt(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Encrypts data, so that it can only be recovered by a call to ``Decrypt``.
        The ``CryptoKey.purpose`` must be
        ``ENCRYPT_DECRYPT``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].Encrypt

    @property
    def decrypt(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Decrypts data that was protected by ``Encrypt``. The ``CryptoKey.purpose``
        must be ``ENCRYPT_DECRYPT``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['key_management_service_stub'].Decrypt

    @property
    def update_crypto_key_primary_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Update the version of a ``CryptoKey`` that will be used in ``Encrypt``.

        Returns an error if called on an asymmetric key.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            'key_management_service_stub'].UpdateCryptoKeyPrimaryVersion

    @property
    def destroy_crypto_key_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Schedule a ``CryptoKeyVersion`` for destruction.

        Upon calling this method, ``CryptoKeyVersion.state`` will be set to
        ``DESTROY_SCHEDULED``
        and ``destroy_time`` will be set to a time 24
        hours in the future, at which point the ``state``
        will be changed to
        ``DESTROYED``, and the key
        material will be irrevocably destroyed.

        Before the ``destroy_time`` is reached,
        ``RestoreCryptoKeyVersion`` may be called to reverse the process.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            'key_management_service_stub'].DestroyCryptoKeyVersion

    @property
    def restore_crypto_key_version(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Restore a ``CryptoKeyVersion`` in the
        ``DESTROY_SCHEDULED``
        state.

        Upon restoration of the CryptoKeyVersion, ``state``
        will be set to ``DISABLED``,
        and ``destroy_time`` will be cleared.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            'key_management_service_stub'].RestoreCryptoKeyVersion

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
        return self._stubs['iam_policy_stub'].SetIamPolicy

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
        return self._stubs['iam_policy_stub'].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['iam_policy_stub'].TestIamPermissions
