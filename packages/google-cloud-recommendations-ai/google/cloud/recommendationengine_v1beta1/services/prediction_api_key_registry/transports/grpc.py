# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.recommendationengine_v1beta1.types import (
    prediction_apikey_registry_service,
)
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import PredictionApiKeyRegistryTransport


class PredictionApiKeyRegistryGrpcTransport(PredictionApiKeyRegistryTransport):
    """gRPC backend transport for PredictionApiKeyRegistry.

    Service for registering API keys for use with the ``predict``
    method. If you use an API key to request predictions, you must first
    register the API key. Otherwise, your prediction request is
    rejected. If you use OAuth to authenticate your ``predict`` method
    call, you do not need to register an API key. You can register up to
    20 API keys per project.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "recommendationengine.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
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
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @classmethod
    def create_channel(
        cls,
        host: str = "recommendationengine.googleapis.com",
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
    def create_prediction_api_key_registration(
        self
    ) -> Callable[
        [prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest],
        prediction_apikey_registry_service.PredictionApiKeyRegistration,
    ]:
        r"""Return a callable for the create prediction api key
        registration method over gRPC.

        Register an API key for use with predict method.

        Returns:
            Callable[[~.CreatePredictionApiKeyRegistrationRequest],
                    ~.PredictionApiKeyRegistration]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_prediction_api_key_registration" not in self._stubs:
            self._stubs[
                "create_prediction_api_key_registration"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.PredictionApiKeyRegistry/CreatePredictionApiKeyRegistration",
                request_serializer=prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest.serialize,
                response_deserializer=prediction_apikey_registry_service.PredictionApiKeyRegistration.deserialize,
            )
        return self._stubs["create_prediction_api_key_registration"]

    @property
    def list_prediction_api_key_registrations(
        self
    ) -> Callable[
        [prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest],
        prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse,
    ]:
        r"""Return a callable for the list prediction api key
        registrations method over gRPC.

        List the registered apiKeys for use with predict
        method.

        Returns:
            Callable[[~.ListPredictionApiKeyRegistrationsRequest],
                    ~.ListPredictionApiKeyRegistrationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_prediction_api_key_registrations" not in self._stubs:
            self._stubs[
                "list_prediction_api_key_registrations"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.PredictionApiKeyRegistry/ListPredictionApiKeyRegistrations",
                request_serializer=prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest.serialize,
                response_deserializer=prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse.deserialize,
            )
        return self._stubs["list_prediction_api_key_registrations"]

    @property
    def delete_prediction_api_key_registration(
        self
    ) -> Callable[
        [prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest],
        empty.Empty,
    ]:
        r"""Return a callable for the delete prediction api key
        registration method over gRPC.

        Unregister an apiKey from using for predict method.

        Returns:
            Callable[[~.DeletePredictionApiKeyRegistrationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_prediction_api_key_registration" not in self._stubs:
            self._stubs[
                "delete_prediction_api_key_registration"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.PredictionApiKeyRegistry/DeletePredictionApiKeyRegistration",
                request_serializer=prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_prediction_api_key_registration"]


__all__ = ("PredictionApiKeyRegistryGrpcTransport",)
