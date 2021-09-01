# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.secretmanager_v1beta1.types import resources
from google.cloud.secretmanager_v1beta1.types import service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import SecretManagerServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import SecretManagerServiceGrpcTransport


class SecretManagerServiceGrpcAsyncIOTransport(SecretManagerServiceTransport):
    """gRPC AsyncIO backend transport for SecretManagerService.

    Secret Manager Service

    Manages secrets and operations using those secrets. Implements a
    REST model with the following objects:

    -  [Secret][google.cloud.secrets.v1beta1.Secret]
    -  [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "secretmanager.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "secretmanager.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_secrets(
        self,
    ) -> Callable[[service.ListSecretsRequest], Awaitable[service.ListSecretsResponse]]:
        r"""Return a callable for the list secrets method over gRPC.

        Lists [Secrets][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.ListSecretsRequest],
                    Awaitable[~.ListSecretsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_secrets" not in self._stubs:
            self._stubs["list_secrets"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/ListSecrets",
                request_serializer=service.ListSecretsRequest.serialize,
                response_deserializer=service.ListSecretsResponse.deserialize,
            )
        return self._stubs["list_secrets"]

    @property
    def create_secret(
        self,
    ) -> Callable[[service.CreateSecretRequest], Awaitable[resources.Secret]]:
        r"""Return a callable for the create secret method over gRPC.

        Creates a new [Secret][google.cloud.secrets.v1beta1.Secret]
        containing no
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion].

        Returns:
            Callable[[~.CreateSecretRequest],
                    Awaitable[~.Secret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_secret" not in self._stubs:
            self._stubs["create_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/CreateSecret",
                request_serializer=service.CreateSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["create_secret"]

    @property
    def add_secret_version(
        self,
    ) -> Callable[
        [service.AddSecretVersionRequest], Awaitable[resources.SecretVersion]
    ]:
        r"""Return a callable for the add secret version method over gRPC.

        Creates a new
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
        containing secret data and attaches it to an existing
        [Secret][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.AddSecretVersionRequest],
                    Awaitable[~.SecretVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_secret_version" not in self._stubs:
            self._stubs["add_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/AddSecretVersion",
                request_serializer=service.AddSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["add_secret_version"]

    @property
    def get_secret(
        self,
    ) -> Callable[[service.GetSecretRequest], Awaitable[resources.Secret]]:
        r"""Return a callable for the get secret method over gRPC.

        Gets metadata for a given
        [Secret][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.GetSecretRequest],
                    Awaitable[~.Secret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_secret" not in self._stubs:
            self._stubs["get_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/GetSecret",
                request_serializer=service.GetSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["get_secret"]

    @property
    def update_secret(
        self,
    ) -> Callable[[service.UpdateSecretRequest], Awaitable[resources.Secret]]:
        r"""Return a callable for the update secret method over gRPC.

        Updates metadata of an existing
        [Secret][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.UpdateSecretRequest],
                    Awaitable[~.Secret]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_secret" not in self._stubs:
            self._stubs["update_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/UpdateSecret",
                request_serializer=service.UpdateSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["update_secret"]

    @property
    def delete_secret(
        self,
    ) -> Callable[[service.DeleteSecretRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete secret method over gRPC.

        Deletes a [Secret][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.DeleteSecretRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_secret" not in self._stubs:
            self._stubs["delete_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/DeleteSecret",
                request_serializer=service.DeleteSecretRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_secret"]

    @property
    def list_secret_versions(
        self,
    ) -> Callable[
        [service.ListSecretVersionsRequest],
        Awaitable[service.ListSecretVersionsResponse],
    ]:
        r"""Return a callable for the list secret versions method over gRPC.

        Lists
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion].
        This call does not return secret data.

        Returns:
            Callable[[~.ListSecretVersionsRequest],
                    Awaitable[~.ListSecretVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_secret_versions" not in self._stubs:
            self._stubs["list_secret_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/ListSecretVersions",
                request_serializer=service.ListSecretVersionsRequest.serialize,
                response_deserializer=service.ListSecretVersionsResponse.deserialize,
            )
        return self._stubs["list_secret_versions"]

    @property
    def get_secret_version(
        self,
    ) -> Callable[
        [service.GetSecretVersionRequest], Awaitable[resources.SecretVersion]
    ]:
        r"""Return a callable for the get secret version method over gRPC.

        Gets metadata for a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Returns:
            Callable[[~.GetSecretVersionRequest],
                    Awaitable[~.SecretVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_secret_version" not in self._stubs:
            self._stubs["get_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/GetSecretVersion",
                request_serializer=service.GetSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["get_secret_version"]

    @property
    def access_secret_version(
        self,
    ) -> Callable[
        [service.AccessSecretVersionRequest],
        Awaitable[service.AccessSecretVersionResponse],
    ]:
        r"""Return a callable for the access secret version method over gRPC.

        Accesses a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].
        This call returns the secret data.

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Returns:
            Callable[[~.AccessSecretVersionRequest],
                    Awaitable[~.AccessSecretVersionResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "access_secret_version" not in self._stubs:
            self._stubs["access_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/AccessSecretVersion",
                request_serializer=service.AccessSecretVersionRequest.serialize,
                response_deserializer=service.AccessSecretVersionResponse.deserialize,
            )
        return self._stubs["access_secret_version"]

    @property
    def disable_secret_version(
        self,
    ) -> Callable[
        [service.DisableSecretVersionRequest], Awaitable[resources.SecretVersion]
    ]:
        r"""Return a callable for the disable secret version method over gRPC.

        Disables a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [DISABLED][google.cloud.secrets.v1beta1.SecretVersion.State.DISABLED].

        Returns:
            Callable[[~.DisableSecretVersionRequest],
                    Awaitable[~.SecretVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_secret_version" not in self._stubs:
            self._stubs["disable_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/DisableSecretVersion",
                request_serializer=service.DisableSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["disable_secret_version"]

    @property
    def enable_secret_version(
        self,
    ) -> Callable[
        [service.EnableSecretVersionRequest], Awaitable[resources.SecretVersion]
    ]:
        r"""Return a callable for the enable secret version method over gRPC.

        Enables a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [ENABLED][google.cloud.secrets.v1beta1.SecretVersion.State.ENABLED].

        Returns:
            Callable[[~.EnableSecretVersionRequest],
                    Awaitable[~.SecretVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_secret_version" not in self._stubs:
            self._stubs["enable_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/EnableSecretVersion",
                request_serializer=service.EnableSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["enable_secret_version"]

    @property
    def destroy_secret_version(
        self,
    ) -> Callable[
        [service.DestroySecretVersionRequest], Awaitable[resources.SecretVersion]
    ]:
        r"""Return a callable for the destroy secret version method over gRPC.

        Destroys a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [DESTROYED][google.cloud.secrets.v1beta1.SecretVersion.State.DESTROYED]
        and irrevocably destroys the secret data.

        Returns:
            Callable[[~.DestroySecretVersionRequest],
                    Awaitable[~.SecretVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "destroy_secret_version" not in self._stubs:
            self._stubs["destroy_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/DestroySecretVersion",
                request_serializer=service.DestroySecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["destroy_secret_version"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy.SetIamPolicyRequest], Awaitable[policy.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the access control policy on the specified secret. Replaces
        any existing policy.

        Permissions on
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion] are
        enforced according to the policy set on the associated
        [Secret][google.cloud.secrets.v1beta1.Secret].

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/SetIamPolicy",
                request_serializer=iam_policy.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy.GetIamPolicyRequest], Awaitable[policy.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the access control policy for a secret.
        Returns empty policy if the secret exists and does not
        have a policy set.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/GetIamPolicy",
                request_serializer=iam_policy.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy.TestIamPermissionsRequest],
        Awaitable[iam_policy.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns permissions that a caller has for the specified secret.
        If the secret does not exist, this call returns an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.cloud.secrets.v1beta1.SecretManagerService/TestIamPermissions",
                request_serializer=iam_policy.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("SecretManagerServiceGrpcAsyncIOTransport",)
