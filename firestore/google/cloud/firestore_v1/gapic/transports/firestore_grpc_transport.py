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

from google.cloud.firestore_v1.proto import firestore_pb2_grpc


class FirestoreGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.firestore.v1 Firestore API.

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
        self, channel=None, credentials=None, address="firestore.googleapis.com:443"
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
        self._stubs = {"firestore_stub": firestore_pb2_grpc.FirestoreStub(channel)}

    @classmethod
    def create_channel(
        cls, address="firestore.googleapis.com:443", credentials=None, **kwargs
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
    def get_document(self):
        """Return the gRPC stub for :meth:`FirestoreClient.get_document`.

        Gets a single document.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].GetDocument

    @property
    def list_documents(self):
        """Return the gRPC stub for :meth:`FirestoreClient.list_documents`.

        Lists documents.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].ListDocuments

    @property
    def create_document(self):
        """Return the gRPC stub for :meth:`FirestoreClient.create_document`.

        Creates a new document.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].CreateDocument

    @property
    def update_document(self):
        """Return the gRPC stub for :meth:`FirestoreClient.update_document`.

        Updates or inserts a document.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].UpdateDocument

    @property
    def delete_document(self):
        """Return the gRPC stub for :meth:`FirestoreClient.delete_document`.

        Deletes a document.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].DeleteDocument

    @property
    def batch_get_documents(self):
        """Return the gRPC stub for :meth:`FirestoreClient.batch_get_documents`.

        Gets multiple documents.

        Documents returned by this method are not guaranteed to be returned in the
        same order that they were requested.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].BatchGetDocuments

    @property
    def begin_transaction(self):
        """Return the gRPC stub for :meth:`FirestoreClient.begin_transaction`.

        Starts a new transaction.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].BeginTransaction

    @property
    def commit(self):
        """Return the gRPC stub for :meth:`FirestoreClient.commit`.

        Commits a transaction, while optionally updating documents.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].Commit

    @property
    def rollback(self):
        """Return the gRPC stub for :meth:`FirestoreClient.rollback`.

        Rolls back a transaction.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].Rollback

    @property
    def run_query(self):
        """Return the gRPC stub for :meth:`FirestoreClient.run_query`.

        Runs a query.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].RunQuery

    @property
    def write(self):
        """Return the gRPC stub for :meth:`FirestoreClient.write`.

        Streams batches of document updates and deletes, in order.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].Write

    @property
    def listen(self):
        """Return the gRPC stub for :meth:`FirestoreClient.listen`.

        Listens to changes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].Listen

    @property
    def list_collection_ids(self):
        """Return the gRPC stub for :meth:`FirestoreClient.list_collection_ids`.

        Lists all the collection IDs underneath a document.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_stub"].ListCollectionIds
