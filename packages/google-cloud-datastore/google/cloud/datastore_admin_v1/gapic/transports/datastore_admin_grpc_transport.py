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
import google.api_core.operations_v1

from google.cloud.datastore_admin_v1.proto import datastore_admin_pb2_grpc


class DatastoreAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.datastore.admin.v1 DatastoreAdmin API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/datastore",
    )

    def __init__(
        self, channel=None, credentials=None, address="datastore.googleapis.com:443"
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
                "The `channel` and `credentials` arguments are mutually " "exclusive.",
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
            "datastore_admin_stub": datastore_admin_pb2_grpc.DatastoreAdminStub(
                channel
            ),
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="datastore.googleapis.com:443", credentials=None, **kwargs
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
    def export_entities(self):
        """Return the gRPC stub for :meth:`DatastoreAdminClient.export_entities`.

        Exports a copy of all or a subset of entities from Google Cloud Datastore
        to another storage system, such as Google Cloud Storage. Recent updates to
        entities may not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed via the
        Operation resource that is created. The output of an export may only be
        used once the associated operation is done. If an export operation is
        cancelled before completion it may leave partial data behind in Google
        Cloud Storage.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["datastore_admin_stub"].ExportEntities

    @property
    def import_entities(self):
        """Return the gRPC stub for :meth:`DatastoreAdminClient.import_entities`.

        Imports entities into Google Cloud Datastore. Existing entities with the
        same key are overwritten. The import occurs in the background and its
        progress can be monitored and managed via the Operation resource that is
        created. If an ImportEntities operation is cancelled, it is possible
        that a subset of the data has already been imported to Cloud Datastore.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["datastore_admin_stub"].ImportEntities

    @property
    def get_index(self):
        """Return the gRPC stub for :meth:`DatastoreAdminClient.get_index`.

        Gets an index.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["datastore_admin_stub"].GetIndex

    @property
    def list_indexes(self):
        """Return the gRPC stub for :meth:`DatastoreAdminClient.list_indexes`.

        Lists the indexes that match the specified filters.  Datastore uses an
        eventually consistent query to fetch the list of indexes and may
        occasionally return stale results.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["datastore_admin_stub"].ListIndexes
