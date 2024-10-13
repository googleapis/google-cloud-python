# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.kms_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO, KeyManagementServiceTransport
from .grpc import KeyManagementServiceGrpcTransport


class KeyManagementServiceGrpcAsyncIOTransport(KeyManagementServiceTransport):
    """gRPC AsyncIO backend transport for KeyManagementService.

    Google Cloud Key Management Service

    Manages cryptographic keys and operations using those keys.
    Implements a REST model with the following objects:

    -  [KeyRing][google.cloud.kms.v1.KeyRing]
    -  [CryptoKey][google.cloud.kms.v1.CryptoKey]
    -  [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
    -  [ImportJob][google.cloud.kms.v1.ImportJob]

    If you are using manual gRPC libraries, see `Using gRPC with Cloud
    KMS <https://cloud.google.com/kms/docs/grpc>`__.

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
        host: str = "cloudkms.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "cloudkms.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudkms.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

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

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def list_key_rings(
        self,
    ) -> Callable[
        [service.ListKeyRingsRequest], Awaitable[service.ListKeyRingsResponse]
    ]:
        r"""Return a callable for the list key rings method over gRPC.

        Lists [KeyRings][google.cloud.kms.v1.KeyRing].

        Returns:
            Callable[[~.ListKeyRingsRequest],
                    Awaitable[~.ListKeyRingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_key_rings" not in self._stubs:
            self._stubs["list_key_rings"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/ListKeyRings",
                request_serializer=service.ListKeyRingsRequest.serialize,
                response_deserializer=service.ListKeyRingsResponse.deserialize,
            )
        return self._stubs["list_key_rings"]

    @property
    def list_crypto_keys(
        self,
    ) -> Callable[
        [service.ListCryptoKeysRequest], Awaitable[service.ListCryptoKeysResponse]
    ]:
        r"""Return a callable for the list crypto keys method over gRPC.

        Lists [CryptoKeys][google.cloud.kms.v1.CryptoKey].

        Returns:
            Callable[[~.ListCryptoKeysRequest],
                    Awaitable[~.ListCryptoKeysResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_crypto_keys" not in self._stubs:
            self._stubs["list_crypto_keys"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/ListCryptoKeys",
                request_serializer=service.ListCryptoKeysRequest.serialize,
                response_deserializer=service.ListCryptoKeysResponse.deserialize,
            )
        return self._stubs["list_crypto_keys"]

    @property
    def list_crypto_key_versions(
        self,
    ) -> Callable[
        [service.ListCryptoKeyVersionsRequest],
        Awaitable[service.ListCryptoKeyVersionsResponse],
    ]:
        r"""Return a callable for the list crypto key versions method over gRPC.

        Lists [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion].

        Returns:
            Callable[[~.ListCryptoKeyVersionsRequest],
                    Awaitable[~.ListCryptoKeyVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_crypto_key_versions" not in self._stubs:
            self._stubs["list_crypto_key_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/ListCryptoKeyVersions",
                request_serializer=service.ListCryptoKeyVersionsRequest.serialize,
                response_deserializer=service.ListCryptoKeyVersionsResponse.deserialize,
            )
        return self._stubs["list_crypto_key_versions"]

    @property
    def list_import_jobs(
        self,
    ) -> Callable[
        [service.ListImportJobsRequest], Awaitable[service.ListImportJobsResponse]
    ]:
        r"""Return a callable for the list import jobs method over gRPC.

        Lists [ImportJobs][google.cloud.kms.v1.ImportJob].

        Returns:
            Callable[[~.ListImportJobsRequest],
                    Awaitable[~.ListImportJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_import_jobs" not in self._stubs:
            self._stubs["list_import_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/ListImportJobs",
                request_serializer=service.ListImportJobsRequest.serialize,
                response_deserializer=service.ListImportJobsResponse.deserialize,
            )
        return self._stubs["list_import_jobs"]

    @property
    def get_key_ring(
        self,
    ) -> Callable[[service.GetKeyRingRequest], Awaitable[resources.KeyRing]]:
        r"""Return a callable for the get key ring method over gRPC.

        Returns metadata for a given
        [KeyRing][google.cloud.kms.v1.KeyRing].

        Returns:
            Callable[[~.GetKeyRingRequest],
                    Awaitable[~.KeyRing]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_key_ring" not in self._stubs:
            self._stubs["get_key_ring"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GetKeyRing",
                request_serializer=service.GetKeyRingRequest.serialize,
                response_deserializer=resources.KeyRing.deserialize,
            )
        return self._stubs["get_key_ring"]

    @property
    def get_crypto_key(
        self,
    ) -> Callable[[service.GetCryptoKeyRequest], Awaitable[resources.CryptoKey]]:
        r"""Return a callable for the get crypto key method over gRPC.

        Returns metadata for a given
        [CryptoKey][google.cloud.kms.v1.CryptoKey], as well as its
        [primary][google.cloud.kms.v1.CryptoKey.primary]
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].

        Returns:
            Callable[[~.GetCryptoKeyRequest],
                    Awaitable[~.CryptoKey]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_crypto_key" not in self._stubs:
            self._stubs["get_crypto_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GetCryptoKey",
                request_serializer=service.GetCryptoKeyRequest.serialize,
                response_deserializer=resources.CryptoKey.deserialize,
            )
        return self._stubs["get_crypto_key"]

    @property
    def get_crypto_key_version(
        self,
    ) -> Callable[
        [service.GetCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the get crypto key version method over gRPC.

        Returns metadata for a given
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].

        Returns:
            Callable[[~.GetCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_crypto_key_version" not in self._stubs:
            self._stubs["get_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GetCryptoKeyVersion",
                request_serializer=service.GetCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["get_crypto_key_version"]

    @property
    def get_public_key(
        self,
    ) -> Callable[[service.GetPublicKeyRequest], Awaitable[resources.PublicKey]]:
        r"""Return a callable for the get public key method over gRPC.

        Returns the public key for the given
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]. The
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] must
        be
        [ASYMMETRIC_SIGN][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN]
        or
        [ASYMMETRIC_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT].

        Returns:
            Callable[[~.GetPublicKeyRequest],
                    Awaitable[~.PublicKey]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_public_key" not in self._stubs:
            self._stubs["get_public_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GetPublicKey",
                request_serializer=service.GetPublicKeyRequest.serialize,
                response_deserializer=resources.PublicKey.deserialize,
            )
        return self._stubs["get_public_key"]

    @property
    def get_import_job(
        self,
    ) -> Callable[[service.GetImportJobRequest], Awaitable[resources.ImportJob]]:
        r"""Return a callable for the get import job method over gRPC.

        Returns metadata for a given
        [ImportJob][google.cloud.kms.v1.ImportJob].

        Returns:
            Callable[[~.GetImportJobRequest],
                    Awaitable[~.ImportJob]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_import_job" not in self._stubs:
            self._stubs["get_import_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GetImportJob",
                request_serializer=service.GetImportJobRequest.serialize,
                response_deserializer=resources.ImportJob.deserialize,
            )
        return self._stubs["get_import_job"]

    @property
    def create_key_ring(
        self,
    ) -> Callable[[service.CreateKeyRingRequest], Awaitable[resources.KeyRing]]:
        r"""Return a callable for the create key ring method over gRPC.

        Create a new [KeyRing][google.cloud.kms.v1.KeyRing] in a given
        Project and Location.

        Returns:
            Callable[[~.CreateKeyRingRequest],
                    Awaitable[~.KeyRing]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_key_ring" not in self._stubs:
            self._stubs["create_key_ring"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/CreateKeyRing",
                request_serializer=service.CreateKeyRingRequest.serialize,
                response_deserializer=resources.KeyRing.deserialize,
            )
        return self._stubs["create_key_ring"]

    @property
    def create_crypto_key(
        self,
    ) -> Callable[[service.CreateCryptoKeyRequest], Awaitable[resources.CryptoKey]]:
        r"""Return a callable for the create crypto key method over gRPC.

        Create a new [CryptoKey][google.cloud.kms.v1.CryptoKey] within a
        [KeyRing][google.cloud.kms.v1.KeyRing].

        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] and
        [CryptoKey.version_template.algorithm][google.cloud.kms.v1.CryptoKeyVersionTemplate.algorithm]
        are required.

        Returns:
            Callable[[~.CreateCryptoKeyRequest],
                    Awaitable[~.CryptoKey]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_crypto_key" not in self._stubs:
            self._stubs["create_crypto_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/CreateCryptoKey",
                request_serializer=service.CreateCryptoKeyRequest.serialize,
                response_deserializer=resources.CryptoKey.deserialize,
            )
        return self._stubs["create_crypto_key"]

    @property
    def create_crypto_key_version(
        self,
    ) -> Callable[
        [service.CreateCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the create crypto key version method over gRPC.

        Create a new
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] in a
        [CryptoKey][google.cloud.kms.v1.CryptoKey].

        The server will assign the next sequential id. If unset,
        [state][google.cloud.kms.v1.CryptoKeyVersion.state] will be set
        to
        [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED].

        Returns:
            Callable[[~.CreateCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_crypto_key_version" not in self._stubs:
            self._stubs["create_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/CreateCryptoKeyVersion",
                request_serializer=service.CreateCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["create_crypto_key_version"]

    @property
    def import_crypto_key_version(
        self,
    ) -> Callable[
        [service.ImportCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the import crypto key version method over gRPC.

        Import wrapped key material into a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].

        All requests must specify a
        [CryptoKey][google.cloud.kms.v1.CryptoKey]. If a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] is
        additionally specified in the request, key material will be
        reimported into that version. Otherwise, a new version will be
        created, and will be assigned the next sequential id within the
        [CryptoKey][google.cloud.kms.v1.CryptoKey].

        Returns:
            Callable[[~.ImportCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_crypto_key_version" not in self._stubs:
            self._stubs["import_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/ImportCryptoKeyVersion",
                request_serializer=service.ImportCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["import_crypto_key_version"]

    @property
    def create_import_job(
        self,
    ) -> Callable[[service.CreateImportJobRequest], Awaitable[resources.ImportJob]]:
        r"""Return a callable for the create import job method over gRPC.

        Create a new [ImportJob][google.cloud.kms.v1.ImportJob] within a
        [KeyRing][google.cloud.kms.v1.KeyRing].

        [ImportJob.import_method][google.cloud.kms.v1.ImportJob.import_method]
        is required.

        Returns:
            Callable[[~.CreateImportJobRequest],
                    Awaitable[~.ImportJob]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_import_job" not in self._stubs:
            self._stubs["create_import_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/CreateImportJob",
                request_serializer=service.CreateImportJobRequest.serialize,
                response_deserializer=resources.ImportJob.deserialize,
            )
        return self._stubs["create_import_job"]

    @property
    def update_crypto_key(
        self,
    ) -> Callable[[service.UpdateCryptoKeyRequest], Awaitable[resources.CryptoKey]]:
        r"""Return a callable for the update crypto key method over gRPC.

        Update a [CryptoKey][google.cloud.kms.v1.CryptoKey].

        Returns:
            Callable[[~.UpdateCryptoKeyRequest],
                    Awaitable[~.CryptoKey]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_crypto_key" not in self._stubs:
            self._stubs["update_crypto_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/UpdateCryptoKey",
                request_serializer=service.UpdateCryptoKeyRequest.serialize,
                response_deserializer=resources.CryptoKey.deserialize,
            )
        return self._stubs["update_crypto_key"]

    @property
    def update_crypto_key_version(
        self,
    ) -> Callable[
        [service.UpdateCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the update crypto key version method over gRPC.

        Update a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
        metadata.

        [state][google.cloud.kms.v1.CryptoKeyVersion.state] may be
        changed between
        [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
        and
        [DISABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DISABLED]
        using this method. See
        [DestroyCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.DestroyCryptoKeyVersion]
        and
        [RestoreCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.RestoreCryptoKeyVersion]
        to move between other states.

        Returns:
            Callable[[~.UpdateCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_crypto_key_version" not in self._stubs:
            self._stubs["update_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/UpdateCryptoKeyVersion",
                request_serializer=service.UpdateCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["update_crypto_key_version"]

    @property
    def update_crypto_key_primary_version(
        self,
    ) -> Callable[
        [service.UpdateCryptoKeyPrimaryVersionRequest], Awaitable[resources.CryptoKey]
    ]:
        r"""Return a callable for the update crypto key primary
        version method over gRPC.

        Update the version of a
        [CryptoKey][google.cloud.kms.v1.CryptoKey] that will be used in
        [Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt].

        Returns an error if called on a key whose purpose is not
        [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT].

        Returns:
            Callable[[~.UpdateCryptoKeyPrimaryVersionRequest],
                    Awaitable[~.CryptoKey]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_crypto_key_primary_version" not in self._stubs:
            self._stubs[
                "update_crypto_key_primary_version"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/UpdateCryptoKeyPrimaryVersion",
                request_serializer=service.UpdateCryptoKeyPrimaryVersionRequest.serialize,
                response_deserializer=resources.CryptoKey.deserialize,
            )
        return self._stubs["update_crypto_key_primary_version"]

    @property
    def destroy_crypto_key_version(
        self,
    ) -> Callable[
        [service.DestroyCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the destroy crypto key version method over gRPC.

        Schedule a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] for
        destruction.

        Upon calling this method,
        [CryptoKeyVersion.state][google.cloud.kms.v1.CryptoKeyVersion.state]
        will be set to
        [DESTROY_SCHEDULED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROY_SCHEDULED],
        and
        [destroy_time][google.cloud.kms.v1.CryptoKeyVersion.destroy_time]
        will be set to the time
        [destroy_scheduled_duration][google.cloud.kms.v1.CryptoKey.destroy_scheduled_duration]
        in the future. At that time, the
        [state][google.cloud.kms.v1.CryptoKeyVersion.state] will
        automatically change to
        [DESTROYED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROYED],
        and the key material will be irrevocably destroyed.

        Before the
        [destroy_time][google.cloud.kms.v1.CryptoKeyVersion.destroy_time]
        is reached,
        [RestoreCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.RestoreCryptoKeyVersion]
        may be called to reverse the process.

        Returns:
            Callable[[~.DestroyCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "destroy_crypto_key_version" not in self._stubs:
            self._stubs["destroy_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/DestroyCryptoKeyVersion",
                request_serializer=service.DestroyCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["destroy_crypto_key_version"]

    @property
    def restore_crypto_key_version(
        self,
    ) -> Callable[
        [service.RestoreCryptoKeyVersionRequest], Awaitable[resources.CryptoKeyVersion]
    ]:
        r"""Return a callable for the restore crypto key version method over gRPC.

        Restore a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] in the
        [DESTROY_SCHEDULED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROY_SCHEDULED]
        state.

        Upon restoration of the CryptoKeyVersion,
        [state][google.cloud.kms.v1.CryptoKeyVersion.state] will be set
        to
        [DISABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DISABLED],
        and
        [destroy_time][google.cloud.kms.v1.CryptoKeyVersion.destroy_time]
        will be cleared.

        Returns:
            Callable[[~.RestoreCryptoKeyVersionRequest],
                    Awaitable[~.CryptoKeyVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_crypto_key_version" not in self._stubs:
            self._stubs["restore_crypto_key_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/RestoreCryptoKeyVersion",
                request_serializer=service.RestoreCryptoKeyVersionRequest.serialize,
                response_deserializer=resources.CryptoKeyVersion.deserialize,
            )
        return self._stubs["restore_crypto_key_version"]

    @property
    def encrypt(
        self,
    ) -> Callable[[service.EncryptRequest], Awaitable[service.EncryptResponse]]:
        r"""Return a callable for the encrypt method over gRPC.

        Encrypts data, so that it can only be recovered by a call to
        [Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt]. The
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] must
        be
        [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT].

        Returns:
            Callable[[~.EncryptRequest],
                    Awaitable[~.EncryptResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "encrypt" not in self._stubs:
            self._stubs["encrypt"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/Encrypt",
                request_serializer=service.EncryptRequest.serialize,
                response_deserializer=service.EncryptResponse.deserialize,
            )
        return self._stubs["encrypt"]

    @property
    def decrypt(
        self,
    ) -> Callable[[service.DecryptRequest], Awaitable[service.DecryptResponse]]:
        r"""Return a callable for the decrypt method over gRPC.

        Decrypts data that was protected by
        [Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt]. The
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] must
        be
        [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT].

        Returns:
            Callable[[~.DecryptRequest],
                    Awaitable[~.DecryptResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "decrypt" not in self._stubs:
            self._stubs["decrypt"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/Decrypt",
                request_serializer=service.DecryptRequest.serialize,
                response_deserializer=service.DecryptResponse.deserialize,
            )
        return self._stubs["decrypt"]

    @property
    def raw_encrypt(
        self,
    ) -> Callable[[service.RawEncryptRequest], Awaitable[service.RawEncryptResponse]]:
        r"""Return a callable for the raw encrypt method over gRPC.

        Encrypts data using portable cryptographic primitives. Most
        users should choose
        [Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt] and
        [Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt]
        rather than their raw counterparts. The
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] must
        be
        [RAW_ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.RAW_ENCRYPT_DECRYPT].

        Returns:
            Callable[[~.RawEncryptRequest],
                    Awaitable[~.RawEncryptResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "raw_encrypt" not in self._stubs:
            self._stubs["raw_encrypt"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/RawEncrypt",
                request_serializer=service.RawEncryptRequest.serialize,
                response_deserializer=service.RawEncryptResponse.deserialize,
            )
        return self._stubs["raw_encrypt"]

    @property
    def raw_decrypt(
        self,
    ) -> Callable[[service.RawDecryptRequest], Awaitable[service.RawDecryptResponse]]:
        r"""Return a callable for the raw decrypt method over gRPC.

        Decrypts data that was originally encrypted using a raw
        cryptographic mechanism. The
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] must
        be
        [RAW_ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.RAW_ENCRYPT_DECRYPT].

        Returns:
            Callable[[~.RawDecryptRequest],
                    Awaitable[~.RawDecryptResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "raw_decrypt" not in self._stubs:
            self._stubs["raw_decrypt"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/RawDecrypt",
                request_serializer=service.RawDecryptRequest.serialize,
                response_deserializer=service.RawDecryptResponse.deserialize,
            )
        return self._stubs["raw_decrypt"]

    @property
    def asymmetric_sign(
        self,
    ) -> Callable[
        [service.AsymmetricSignRequest], Awaitable[service.AsymmetricSignResponse]
    ]:
        r"""Return a callable for the asymmetric sign method over gRPC.

        Signs data using a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        ASYMMETRIC_SIGN, producing a signature that can be verified with
        the public key retrieved from
        [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].

        Returns:
            Callable[[~.AsymmetricSignRequest],
                    Awaitable[~.AsymmetricSignResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "asymmetric_sign" not in self._stubs:
            self._stubs["asymmetric_sign"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/AsymmetricSign",
                request_serializer=service.AsymmetricSignRequest.serialize,
                response_deserializer=service.AsymmetricSignResponse.deserialize,
            )
        return self._stubs["asymmetric_sign"]

    @property
    def asymmetric_decrypt(
        self,
    ) -> Callable[
        [service.AsymmetricDecryptRequest], Awaitable[service.AsymmetricDecryptResponse]
    ]:
        r"""Return a callable for the asymmetric decrypt method over gRPC.

        Decrypts data that was encrypted with a public key retrieved
        from
        [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey]
        corresponding to a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        ASYMMETRIC_DECRYPT.

        Returns:
            Callable[[~.AsymmetricDecryptRequest],
                    Awaitable[~.AsymmetricDecryptResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "asymmetric_decrypt" not in self._stubs:
            self._stubs["asymmetric_decrypt"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/AsymmetricDecrypt",
                request_serializer=service.AsymmetricDecryptRequest.serialize,
                response_deserializer=service.AsymmetricDecryptResponse.deserialize,
            )
        return self._stubs["asymmetric_decrypt"]

    @property
    def mac_sign(
        self,
    ) -> Callable[[service.MacSignRequest], Awaitable[service.MacSignResponse]]:
        r"""Return a callable for the mac sign method over gRPC.

        Signs data using a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] MAC,
        producing a tag that can be verified by another source with the
        same key.

        Returns:
            Callable[[~.MacSignRequest],
                    Awaitable[~.MacSignResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mac_sign" not in self._stubs:
            self._stubs["mac_sign"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/MacSign",
                request_serializer=service.MacSignRequest.serialize,
                response_deserializer=service.MacSignResponse.deserialize,
            )
        return self._stubs["mac_sign"]

    @property
    def mac_verify(
        self,
    ) -> Callable[[service.MacVerifyRequest], Awaitable[service.MacVerifyResponse]]:
        r"""Return a callable for the mac verify method over gRPC.

        Verifies MAC tag using a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose] MAC,
        and returns a response that indicates whether or not the
        verification was successful.

        Returns:
            Callable[[~.MacVerifyRequest],
                    Awaitable[~.MacVerifyResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mac_verify" not in self._stubs:
            self._stubs["mac_verify"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/MacVerify",
                request_serializer=service.MacVerifyRequest.serialize,
                response_deserializer=service.MacVerifyResponse.deserialize,
            )
        return self._stubs["mac_verify"]

    @property
    def generate_random_bytes(
        self,
    ) -> Callable[
        [service.GenerateRandomBytesRequest],
        Awaitable[service.GenerateRandomBytesResponse],
    ]:
        r"""Return a callable for the generate random bytes method over gRPC.

        Generate random bytes using the Cloud KMS randomness
        source in the provided location.

        Returns:
            Callable[[~.GenerateRandomBytesRequest],
                    Awaitable[~.GenerateRandomBytesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_random_bytes" not in self._stubs:
            self._stubs["generate_random_bytes"] = self.grpc_channel.unary_unary(
                "/google.cloud.kms.v1.KeyManagementService/GenerateRandomBytes",
                request_serializer=service.GenerateRandomBytesRequest.serialize,
                response_deserializer=service.GenerateRandomBytesResponse.deserialize,
            )
        return self._stubs["generate_random_bytes"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
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
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
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
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
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
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_key_rings: self._wrap_method(
                self.list_key_rings,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_crypto_keys: self._wrap_method(
                self.list_crypto_keys,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_crypto_key_versions: self._wrap_method(
                self.list_crypto_key_versions,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_import_jobs: self._wrap_method(
                self.list_import_jobs,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_key_ring: self._wrap_method(
                self.get_key_ring,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_crypto_key: self._wrap_method(
                self.get_crypto_key,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_crypto_key_version: self._wrap_method(
                self.get_crypto_key_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_public_key: self._wrap_method(
                self.get_public_key,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_import_job: self._wrap_method(
                self.get_import_job,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_key_ring: self._wrap_method(
                self.create_key_ring,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_crypto_key: self._wrap_method(
                self.create_crypto_key,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_crypto_key_version: self._wrap_method(
                self.create_crypto_key_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.import_crypto_key_version: self._wrap_method(
                self.import_crypto_key_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_import_job: self._wrap_method(
                self.create_import_job,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key: self._wrap_method(
                self.update_crypto_key,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key_version: self._wrap_method(
                self.update_crypto_key_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key_primary_version: self._wrap_method(
                self.update_crypto_key_primary_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.destroy_crypto_key_version: self._wrap_method(
                self.destroy_crypto_key_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.restore_crypto_key_version: self._wrap_method(
                self.restore_crypto_key_version,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.encrypt: self._wrap_method(
                self.encrypt,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.decrypt: self._wrap_method(
                self.decrypt,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.raw_encrypt: self._wrap_method(
                self.raw_encrypt,
                default_timeout=None,
                client_info=client_info,
            ),
            self.raw_decrypt: self._wrap_method(
                self.raw_decrypt,
                default_timeout=None,
                client_info=client_info,
            ),
            self.asymmetric_sign: self._wrap_method(
                self.asymmetric_sign,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.asymmetric_decrypt: self._wrap_method(
                self.asymmetric_decrypt,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.mac_sign: self._wrap_method(
                self.mac_sign,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.mac_verify: self._wrap_method(
                self.mac_verify,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.generate_random_bytes: self._wrap_method(
                self.generate_random_bytes,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("KeyManagementServiceGrpcAsyncIOTransport",)
