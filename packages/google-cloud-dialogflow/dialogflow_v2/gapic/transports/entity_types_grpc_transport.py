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

from dialogflow_v2.proto import entity_type_pb2_grpc


class EntityTypesGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.dialogflow.v2 EntityTypes API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/dialogflow",
    )

    def __init__(
        self, channel=None, credentials=None, address="dialogflow.googleapis.com:443"
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
            "entity_types_stub": entity_type_pb2_grpc.EntityTypesStub(channel)
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="dialogflow.googleapis.com:443", credentials=None, **kwargs
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
    def list_entity_types(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.list_entity_types`.

        Returns the list of all entity types in the specified agent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].ListEntityTypes

    @property
    def get_entity_type(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.get_entity_type`.

        Retrieves the specified entity type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].GetEntityType

    @property
    def create_entity_type(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.create_entity_type`.

        Creates an entity type in the specified agent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].CreateEntityType

    @property
    def update_entity_type(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.update_entity_type`.

        Updates the specified entity type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].UpdateEntityType

    @property
    def delete_entity_type(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.delete_entity_type`.

        Deletes the specified entity type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].DeleteEntityType

    @property
    def batch_update_entity_types(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.batch_update_entity_types`.

        Updates/Creates multiple entity types in the specified agent.

        Operation <response: ``BatchUpdateEntityTypesResponse``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].BatchUpdateEntityTypes

    @property
    def batch_delete_entity_types(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.batch_delete_entity_types`.

        Deletes entity types in the specified agent.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].BatchDeleteEntityTypes

    @property
    def batch_create_entities(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.batch_create_entities`.

        Creates multiple new entities in the specified entity type.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].BatchCreateEntities

    @property
    def batch_update_entities(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.batch_update_entities`.

        Updates or creates multiple entities in the specified entity type. This
        method does not affect entities in the entity type that aren't
        explicitly specified in the request.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].BatchUpdateEntities

    @property
    def batch_delete_entities(self):
        """Return the gRPC stub for :meth:`EntityTypesClient.batch_delete_entities`.

        Deletes entities in the specified entity type.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["entity_types_stub"].BatchDeleteEntities
