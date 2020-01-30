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

from google.cloud.firestore_admin_v1.proto import firestore_admin_pb2_grpc


class FirestoreAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.firestore.admin.v1 FirestoreAdmin API.

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
        self._stubs = {
            "firestore_admin_stub": firestore_admin_pb2_grpc.FirestoreAdminStub(channel)
        }

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
    def create_index(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.create_index`.

        Creates a composite index. This returns a
        ``google.longrunning.Operation`` which may be used to track the status
        of the creation. The metadata for the operation will be the type
        ``IndexOperationMetadata``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].CreateIndex

    @property
    def list_indexes(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.list_indexes`.

        Lists composite indexes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].ListIndexes

    @property
    def get_index(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.get_index`.

        Gets a composite index.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].GetIndex

    @property
    def delete_index(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.delete_index`.

        Deletes a composite index.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].DeleteIndex

    @property
    def import_documents(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.import_documents`.

        Imports documents into Google Cloud Firestore. Existing documents with the
        same name are overwritten. The import occurs in the background and its
        progress can be monitored and managed via the Operation resource that is
        created. If an ImportDocuments operation is cancelled, it is possible
        that a subset of the data has already been imported to Cloud Firestore.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].ImportDocuments

    @property
    def export_documents(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.export_documents`.

        Exports a copy of all or a subset of documents from Google Cloud Firestore
        to another storage system, such as Google Cloud Storage. Recent updates to
        documents may not be reflected in the export. The export occurs in the
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
        return self._stubs["firestore_admin_stub"].ExportDocuments

    @property
    def get_field(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.get_field`.

        Gets the metadata and configuration for a Field.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].GetField

    @property
    def list_fields(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.list_fields`.

        Lists the field configuration and metadata for this database.

        Currently, ``FirestoreAdmin.ListFields`` only supports listing fields
        that have been explicitly overridden. To issue this query, call
        ``FirestoreAdmin.ListFields`` with the filter set to
        ``indexConfig.usesAncestorConfig:false``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].ListFields

    @property
    def update_field(self):
        """Return the gRPC stub for :meth:`FirestoreAdminClient.update_field`.

        Updates a field configuration. Currently, field updates apply only to
        single field index configuration. However, calls to
        ``FirestoreAdmin.UpdateField`` should provide a field mask to avoid
        changing any configuration that the caller isn't aware of. The field
        mask should be specified as: ``{ paths: "index_config" }``.

        This call returns a ``google.longrunning.Operation`` which may be used
        to track the status of the field update. The metadata for the operation
        will be the type ``FieldOperationMetadata``.

        To configure the default field settings for the database, use the
        special ``Field`` with resource name:
        ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["firestore_admin_stub"].UpdateField
