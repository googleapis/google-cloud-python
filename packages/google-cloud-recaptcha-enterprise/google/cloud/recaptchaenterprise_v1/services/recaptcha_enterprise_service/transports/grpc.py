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

from typing import Callable, Dict, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import RecaptchaEnterpriseServiceTransport


class RecaptchaEnterpriseServiceGrpcTransport(RecaptchaEnterpriseServiceTransport):
    """gRPC backend transport for RecaptchaEnterpriseService.

    Service to determine the likelihood an event is legitimate.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "recaptchaenterprise.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None
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
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
          google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = grpc_helpers.create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_credentials,
                scopes=self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

    @classmethod
    def create_channel(
        cls,
        host: str = "recaptchaenterprise.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_assessment(
        self,
    ) -> Callable[
        [recaptchaenterprise.CreateAssessmentRequest], recaptchaenterprise.Assessment
    ]:
        r"""Return a callable for the create assessment method over gRPC.

        Creates an Assessment of the likelihood an event is
        legitimate.

        Returns:
            Callable[[~.CreateAssessmentRequest],
                    ~.Assessment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_assessment" not in self._stubs:
            self._stubs["create_assessment"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/CreateAssessment",
                request_serializer=recaptchaenterprise.CreateAssessmentRequest.serialize,
                response_deserializer=recaptchaenterprise.Assessment.deserialize,
            )
        return self._stubs["create_assessment"]

    @property
    def annotate_assessment(
        self,
    ) -> Callable[
        [recaptchaenterprise.AnnotateAssessmentRequest],
        recaptchaenterprise.AnnotateAssessmentResponse,
    ]:
        r"""Return a callable for the annotate assessment method over gRPC.

        Annotates a previously created Assessment to provide
        additional information on whether the event turned out
        to be authentic or fradulent.

        Returns:
            Callable[[~.AnnotateAssessmentRequest],
                    ~.AnnotateAssessmentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "annotate_assessment" not in self._stubs:
            self._stubs["annotate_assessment"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/AnnotateAssessment",
                request_serializer=recaptchaenterprise.AnnotateAssessmentRequest.serialize,
                response_deserializer=recaptchaenterprise.AnnotateAssessmentResponse.deserialize,
            )
        return self._stubs["annotate_assessment"]

    @property
    def create_key(
        self,
    ) -> Callable[[recaptchaenterprise.CreateKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the create key method over gRPC.

        Creates a new reCAPTCHA Enterprise key.

        Returns:
            Callable[[~.CreateKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_key" not in self._stubs:
            self._stubs["create_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/CreateKey",
                request_serializer=recaptchaenterprise.CreateKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["create_key"]

    @property
    def list_keys(
        self,
    ) -> Callable[
        [recaptchaenterprise.ListKeysRequest], recaptchaenterprise.ListKeysResponse
    ]:
        r"""Return a callable for the list keys method over gRPC.

        Returns the list of all keys that belong to a
        project.

        Returns:
            Callable[[~.ListKeysRequest],
                    ~.ListKeysResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_keys" not in self._stubs:
            self._stubs["list_keys"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/ListKeys",
                request_serializer=recaptchaenterprise.ListKeysRequest.serialize,
                response_deserializer=recaptchaenterprise.ListKeysResponse.deserialize,
            )
        return self._stubs["list_keys"]

    @property
    def get_key(
        self,
    ) -> Callable[[recaptchaenterprise.GetKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the get key method over gRPC.

        Returns the specified key.

        Returns:
            Callable[[~.GetKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_key" not in self._stubs:
            self._stubs["get_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/GetKey",
                request_serializer=recaptchaenterprise.GetKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["get_key"]

    @property
    def update_key(
        self,
    ) -> Callable[[recaptchaenterprise.UpdateKeyRequest], recaptchaenterprise.Key]:
        r"""Return a callable for the update key method over gRPC.

        Updates the specified key.

        Returns:
            Callable[[~.UpdateKeyRequest],
                    ~.Key]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_key" not in self._stubs:
            self._stubs["update_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/UpdateKey",
                request_serializer=recaptchaenterprise.UpdateKeyRequest.serialize,
                response_deserializer=recaptchaenterprise.Key.deserialize,
            )
        return self._stubs["update_key"]

    @property
    def delete_key(
        self,
    ) -> Callable[[recaptchaenterprise.DeleteKeyRequest], empty.Empty]:
        r"""Return a callable for the delete key method over gRPC.

        Deletes the specified key.

        Returns:
            Callable[[~.DeleteKeyRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_key" not in self._stubs:
            self._stubs["delete_key"] = self.grpc_channel.unary_unary(
                "/google.cloud.recaptchaenterprise.v1.RecaptchaEnterpriseService/DeleteKey",
                request_serializer=recaptchaenterprise.DeleteKeyRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_key"]


__all__ = ("RecaptchaEnterpriseServiceGrpcTransport",)
