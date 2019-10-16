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

from dialogflow_v2beta1.proto import agent_pb2_grpc


class AgentsGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.dialogflow.v2beta1 Agents API.

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
        self._stubs = {"agents_stub": agent_pb2_grpc.AgentsStub(channel)}

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
    def set_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.set_agent`.

        Creates/updates the specified agent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].SetAgent

    @property
    def delete_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.delete_agent`.

        Deletes the specified agent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].DeleteAgent

    @property
    def get_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.get_agent`.

        Retrieves the specified agent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].GetAgent

    @property
    def search_agents(self):
        """Return the gRPC stub for :meth:`AgentsClient.search_agents`.

        Returns the list of agents.

        Since there is at most one conversational agent per project, this method
        is useful primarily for listing all agents across projects the caller
        has access to. One can achieve that with a wildcard project collection
        id "-". Refer to `List
        Sub-Collections <https://cloud.google.com/apis/design/design_patterns#list_sub-collections>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].SearchAgents

    @property
    def train_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.train_agent`.

        Trains the specified agent.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].TrainAgent

    @property
    def export_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.export_agent`.

        Exports the specified agent to a ZIP file.

        Operation <response: ``ExportAgentResponse``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].ExportAgent

    @property
    def import_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.import_agent`.

        Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the existing ones.
        Intents and entity types with the same name are replaced with the new
        versions from ImportAgentRequest.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].ImportAgent

    @property
    def restore_agent(self):
        """Return the gRPC stub for :meth:`AgentsClient.restore_agent`.

        Restores the specified agent from a ZIP file.

        Replaces the current agent version with a new one. All the intents and
        entity types in the older version are deleted.

        Operation <response: ``google.protobuf.Empty``>

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].RestoreAgent

    @property
    def get_validation_result(self):
        """Return the gRPC stub for :meth:`AgentsClient.get_validation_result`.

        Gets agent validation result. Agent validation is performed during
        training time and is updated automatically when training is completed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["agents_stub"].GetValidationResult
