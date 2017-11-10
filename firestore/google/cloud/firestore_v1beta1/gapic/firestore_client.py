# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/firestore/v1beta1/firestore.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.firestore.v1beta1 Firestore API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
from google.gax.utils import oneof
import google.gax

from google.cloud.firestore_v1beta1.gapic import enums
from google.cloud.firestore_v1beta1.gapic import firestore_client_config
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.cloud.firestore_v1beta1.proto import query_pb2
from google.cloud.firestore_v1beta1.proto import write_pb2
from google.cloud.firestore_v1beta1.proto.admin import firestore_admin_pb2
from google.cloud.firestore_v1beta1.proto.admin import index_pb2
from google.protobuf import timestamp_pb2

_PageDesc = google.gax.PageDescriptor


class FirestoreClient(object):
    """
    The Cloud Firestore service.

    This service exposes several types of comparable timestamps:

    *    ``create_time`` - The time at which a document was created. Changes only
    ::

         when a document is deleted, then re-created. Increases in a strict
          monotonic fashion.
    *    ``update_time`` - The time at which a document was last updated. Changes
    ::

         every time a document is modified. Does not change when a write results
         in no modifications. Increases in a strict monotonic fashion.
    *    ``read_time`` - The time at which a particular state was observed. Used
    ::

         to denote a consistent snapshot of the database or the time at which a
         Document was observed to not exist.
    *    ``commit_time`` - The time at which the writes in a transaction were
    ::

         committed. Any read with an equal or greater `read_time` is guaranteed
         to see the effects of the transaction.
    """

    SERVICE_ADDRESS = 'firestore.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _PAGE_DESCRIPTORS = {
        'list_documents':
        _PageDesc('page_token', 'next_page_token', 'documents'),
        'list_collection_ids':
        _PageDesc('page_token', 'next_page_token', 'collection_ids')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/datastore', )

    _DATABASE_ROOT_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}')
    _DOCUMENT_ROOT_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}/documents')
    _DOCUMENT_PATH_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}/documents/{document_path=**}')
    _ANY_PATH_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}/documents/{document}/{any_path=**}'
    )

    @classmethod
    def database_root_path(cls, project, database):
        """Returns a fully-qualified database_root resource name string."""
        return cls._DATABASE_ROOT_PATH_TEMPLATE.render({
            'project': project,
            'database': database,
        })

    @classmethod
    def document_root_path(cls, project, database):
        """Returns a fully-qualified document_root resource name string."""
        return cls._DOCUMENT_ROOT_PATH_TEMPLATE.render({
            'project': project,
            'database': database,
        })

    @classmethod
    def document_path_path(cls, project, database, document_path):
        """Returns a fully-qualified document_path resource name string."""
        return cls._DOCUMENT_PATH_PATH_TEMPLATE.render({
            'project':
            project,
            'database':
            database,
            'document_path':
            document_path,
        })

    @classmethod
    def any_path_path(cls, project, database, document, any_path):
        """Returns a fully-qualified any_path resource name string."""
        return cls._ANY_PATH_PATH_TEMPLATE.render({
            'project': project,
            'database': database,
            'document': document,
            'any_path': any_path,
        })

    @classmethod
    def match_project_from_database_root_name(cls, database_root_name):
        """Parses the project from a database_root resource.

        Args:
            database_root_name (str): A fully-qualified path representing a database_root
                resource.

        Returns:
            A string representing the project.
        """
        return cls._DATABASE_ROOT_PATH_TEMPLATE.match(database_root_name).get(
            'project')

    @classmethod
    def match_database_from_database_root_name(cls, database_root_name):
        """Parses the database from a database_root resource.

        Args:
            database_root_name (str): A fully-qualified path representing a database_root
                resource.

        Returns:
            A string representing the database.
        """
        return cls._DATABASE_ROOT_PATH_TEMPLATE.match(database_root_name).get(
            'database')

    @classmethod
    def match_project_from_document_root_name(cls, document_root_name):
        """Parses the project from a document_root resource.

        Args:
            document_root_name (str): A fully-qualified path representing a document_root
                resource.

        Returns:
            A string representing the project.
        """
        return cls._DOCUMENT_ROOT_PATH_TEMPLATE.match(document_root_name).get(
            'project')

    @classmethod
    def match_database_from_document_root_name(cls, document_root_name):
        """Parses the database from a document_root resource.

        Args:
            document_root_name (str): A fully-qualified path representing a document_root
                resource.

        Returns:
            A string representing the database.
        """
        return cls._DOCUMENT_ROOT_PATH_TEMPLATE.match(document_root_name).get(
            'database')

    @classmethod
    def match_project_from_document_path_name(cls, document_path_name):
        """Parses the project from a document_path resource.

        Args:
            document_path_name (str): A fully-qualified path representing a document_path
                resource.

        Returns:
            A string representing the project.
        """
        return cls._DOCUMENT_PATH_PATH_TEMPLATE.match(document_path_name).get(
            'project')

    @classmethod
    def match_database_from_document_path_name(cls, document_path_name):
        """Parses the database from a document_path resource.

        Args:
            document_path_name (str): A fully-qualified path representing a document_path
                resource.

        Returns:
            A string representing the database.
        """
        return cls._DOCUMENT_PATH_PATH_TEMPLATE.match(document_path_name).get(
            'database')

    @classmethod
    def match_document_path_from_document_path_name(cls, document_path_name):
        """Parses the document_path from a document_path resource.

        Args:
            document_path_name (str): A fully-qualified path representing a document_path
                resource.

        Returns:
            A string representing the document_path.
        """
        return cls._DOCUMENT_PATH_PATH_TEMPLATE.match(document_path_name).get(
            'document_path')

    @classmethod
    def match_project_from_any_path_name(cls, any_path_name):
        """Parses the project from a any_path resource.

        Args:
            any_path_name (str): A fully-qualified path representing a any_path
                resource.

        Returns:
            A string representing the project.
        """
        return cls._ANY_PATH_PATH_TEMPLATE.match(any_path_name).get('project')

    @classmethod
    def match_database_from_any_path_name(cls, any_path_name):
        """Parses the database from a any_path resource.

        Args:
            any_path_name (str): A fully-qualified path representing a any_path
                resource.

        Returns:
            A string representing the database.
        """
        return cls._ANY_PATH_PATH_TEMPLATE.match(any_path_name).get('database')

    @classmethod
    def match_document_from_any_path_name(cls, any_path_name):
        """Parses the document from a any_path resource.

        Args:
            any_path_name (str): A fully-qualified path representing a any_path
                resource.

        Returns:
            A string representing the document.
        """
        return cls._ANY_PATH_PATH_TEMPLATE.match(any_path_name).get('document')

    @classmethod
    def match_any_path_from_any_path_name(cls, any_path_name):
        """Parses the any_path from a any_path resource.

        Args:
            any_path_name (str): A fully-qualified path representing a any_path
                resource.

        Returns:
            A string representing the any_path.
        """
        return cls._ANY_PATH_PATH_TEMPLATE.match(any_path_name).get('any_path')

    def __init__(self,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
            channel (~grpc.Channel): A ``Channel`` instance through
                which to make calls.
            credentials (~google.auth.credentials.Credentials): The authorization
                credentials to attach to requests. These credentials identify this
                application to the service.
            ssl_credentials (~grpc.ChannelCredentials): A
                ``ChannelCredentials`` instance for use with an SSL-enabled
                channel.
            scopes (Sequence[str]): A list of OAuth2 scopes to attach to requests.
            client_config (dict):
                A dictionary for call options for each method. See
                :func:`google.gax.construct_settings` for the structure of
                this data. Falls back to the default config if not specified
                or the specified config is missing data points.
            lib_name (str): The API library software used for calling
                the service. (Unless you are writing an API client itself,
                leave this as default.)
            lib_version (str): The API library software version used
                for calling the service. (Unless you are writing an API client
                itself, leave this as default.)
            metrics_headers (dict): A dictionary of values for tracking
                client library metrics. Ultimately serializes to a string
                (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
                considered private.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'google-cloud-firestore', ).version

        # Load the configuration defaults.
        defaults = api_callable.construct_settings(
            'google.firestore.v1beta1.Firestore',
            firestore_client_config.config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers,
            page_descriptors=self._PAGE_DESCRIPTORS, )
        self.firestore_stub = config.create_stub(
            firestore_pb2.FirestoreStub,
            channel=channel,
            service_path=self.SERVICE_ADDRESS,
            service_port=self.DEFAULT_SERVICE_PORT,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self._get_document = api_callable.create_api_call(
            self.firestore_stub.GetDocument, settings=defaults['get_document'])
        self._list_documents = api_callable.create_api_call(
            self.firestore_stub.ListDocuments,
            settings=defaults['list_documents'])
        self._create_document = api_callable.create_api_call(
            self.firestore_stub.CreateDocument,
            settings=defaults['create_document'])
        self._update_document = api_callable.create_api_call(
            self.firestore_stub.UpdateDocument,
            settings=defaults['update_document'])
        self._delete_document = api_callable.create_api_call(
            self.firestore_stub.DeleteDocument,
            settings=defaults['delete_document'])
        self._batch_get_documents = api_callable.create_api_call(
            self.firestore_stub.BatchGetDocuments,
            settings=defaults['batch_get_documents'])
        self._begin_transaction = api_callable.create_api_call(
            self.firestore_stub.BeginTransaction,
            settings=defaults['begin_transaction'])
        self._commit = api_callable.create_api_call(
            self.firestore_stub.Commit, settings=defaults['commit'])
        self._rollback = api_callable.create_api_call(
            self.firestore_stub.Rollback, settings=defaults['rollback'])
        self._run_query = api_callable.create_api_call(
            self.firestore_stub.RunQuery, settings=defaults['run_query'])
        self._write = api_callable.create_api_call(
            self.firestore_stub.Write, settings=defaults['write'])
        self._listen = api_callable.create_api_call(
            self.firestore_stub.Listen, settings=defaults['listen'])
        self._list_collection_ids = api_callable.create_api_call(
            self.firestore_stub.ListCollectionIds,
            settings=defaults['list_collection_ids'])

    # Service calls
    def get_document(self,
                     name,
                     mask=None,
                     transaction=None,
                     read_time=None,
                     options=None):
        """
        Gets a single document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> response = client.get_document(name)

        Args:
            name (str): The resource name of the Document to get. In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
            mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to return. If not set, returns all fields.

                If the document has a field that is not present in this mask, that field
                will not be returned in the response.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            transaction (bytes): Reads the document in a transaction.
            read_time (Union[dict, ~google.cloud.firestore_v1beta1.types.Timestamp]): Reads the version of the document at the given time.
                This may not be older than 60 seconds.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Timestamp`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(
            transaction=transaction,
            read_time=read_time, )

        request = firestore_pb2.GetDocumentRequest(
            name=name, mask=mask, transaction=transaction, read_time=read_time)
        return self._get_document(request, options)

    def list_documents(self,
                       parent,
                       collection_id,
                       page_size=None,
                       order_by=None,
                       mask=None,
                       transaction=None,
                       read_time=None,
                       show_missing=None,
                       options=None):
        """
        Lists documents.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>> from google.gax import CallOptions, INITIAL_PAGE
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>> collection_id = ''
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_documents(parent, collection_id):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_documents(parent, collection_id, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name. In the format:
                ``projects/{project_id}/databases/{database_id}/documents`` or
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                For example:
                ``projects/my-project/databases/my-database/documents`` or
                ``projects/my-project/databases/my-database/documents/chatrooms/my-chatroom``
            collection_id (str): The collection ID, relative to ``parent``, to list. For example: ``chatrooms``
                or ``messages``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): The order to sort results by. For example: ``priority desc, name``.
            mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to return. If not set, returns all fields.

                If a document has a field that is not present in this mask, that field
                will not be returned in the response.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            transaction (bytes): Reads documents in a transaction.
            read_time (Union[dict, ~google.cloud.firestore_v1beta1.types.Timestamp]): Reads documents as they were at the given time.
                This may not be older than 60 seconds.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Timestamp`
            show_missing (bool): If the list should show missing documents. A missing document is a
                document that does not exist but has sub-documents. These documents will
                be returned with a key but will not have fields, ``Document.create_time``,
                or ``Document.update_time`` set.

                Requests with ``show_missing`` may not specify ``where`` or
                ``order_by``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.firestore_v1beta1.types.Document` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(
            transaction=transaction,
            read_time=read_time, )

        request = firestore_pb2.ListDocumentsRequest(
            parent=parent,
            collection_id=collection_id,
            page_size=page_size,
            order_by=order_by,
            mask=mask,
            transaction=transaction,
            read_time=read_time,
            show_missing=show_missing)
        return self._list_documents(request, options)

    def create_document(self,
                        parent,
                        collection_id,
                        document_id,
                        document,
                        mask=None,
                        options=None):
        """
        Creates a new document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>> collection_id = ''
            >>> document_id = ''
            >>> document = {}
            >>>
            >>> response = client.create_document(parent, collection_id, document_id, document)

        Args:
            parent (str): The parent resource. For example:
                ``projects/{project_id}/databases/{database_id}/documents`` or
                ``projects/{project_id}/databases/{database_id}/documents/chatrooms/{chatroom_id}``
            collection_id (str): The collection ID, relative to ``parent``, to list. For example: ``chatrooms``.
            document_id (str): The client-assigned document ID to use for this document.

                Optional. If not specified, an ID will be assigned by the service.
            document (Union[dict, ~google.cloud.firestore_v1beta1.types.Document]): The document to create. ``name`` must not be set.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Document`
            mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to return. If not set, returns all fields.

                If the document has a field that is not present in this mask, that field
                will not be returned in the response.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.CreateDocumentRequest(
            parent=parent,
            collection_id=collection_id,
            document_id=document_id,
            document=document,
            mask=mask)
        return self._create_document(request, options)

    def update_document(self,
                        document,
                        update_mask,
                        mask=None,
                        current_document=None,
                        options=None):
        """
        Updates or inserts a document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> document = {}
            >>> update_mask = {}
            >>>
            >>> response = client.update_document(document, update_mask)

        Args:
            document (Union[dict, ~google.cloud.firestore_v1beta1.types.Document]): The updated document.
                Creates the document if it does not already exist.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Document`
            update_mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to update.
                None of the field paths in the mask may contain a reserved name.

                If the document exists on the server and has fields not referenced in the
                mask, they are left unchanged.
                Fields referenced in the mask, but not present in the input document, are
                deleted from the document on the server.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to return. If not set, returns all fields.

                If the document has a field that is not present in this mask, that field
                will not be returned in the response.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            current_document (Union[dict, ~google.cloud.firestore_v1beta1.types.Precondition]): An optional precondition on the document.
                The request will fail if this is set and not met by the target document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Precondition`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.UpdateDocumentRequest(
            document=document,
            update_mask=update_mask,
            mask=mask,
            current_document=current_document)
        return self._update_document(request, options)

    def delete_document(self, name, current_document=None, options=None):
        """
        Deletes a document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> client.delete_document(name)

        Args:
            name (str): The resource name of the Document to delete. In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
            current_document (Union[dict, ~google.cloud.firestore_v1beta1.types.Precondition]): An optional precondition on the document.
                The request will fail if this is set and not met by the target document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Precondition`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.DeleteDocumentRequest(
            name=name, current_document=current_document)
        self._delete_document(request, options)

    def batch_get_documents(self,
                            database,
                            documents,
                            mask=None,
                            transaction=None,
                            new_transaction=None,
                            read_time=None,
                            options=None):
        """
        Gets multiple documents.

        Documents returned by this method are not guaranteed to be returned in the
        same order that they were requested.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>> documents = []
            >>>
            >>> for element in client.batch_get_documents(database, documents):
            ...     # process element
            ...     pass

        Args:
            database (str): The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
            documents (list[str]): The names of the documents to retrieve. In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                The request will fail if any of the document is not a child resource of the
                given ``database``. Duplicate names will be elided.
            mask (Union[dict, ~google.cloud.firestore_v1beta1.types.DocumentMask]): The fields to return. If not set, returns all fields.

                If a document has a field that is not present in this mask, that field will
                not be returned in the response.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.DocumentMask`
            transaction (bytes): Reads documents in a transaction.
            new_transaction (Union[dict, ~google.cloud.firestore_v1beta1.types.TransactionOptions]): Starts a new transaction and reads the documents.
                Defaults to a read-only transaction.
                The new transaction ID will be returned as the first response in the
                stream.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.TransactionOptions`
            read_time (Union[dict, ~google.cloud.firestore_v1beta1.types.Timestamp]): Reads documents as they were at the given time.
                This may not be older than 60 seconds.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Timestamp`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.BatchGetDocumentsResponse].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time, )

        request = firestore_pb2.BatchGetDocumentsRequest(
            database=database,
            documents=documents,
            mask=mask,
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time)
        return self._batch_get_documents(request, options)

    def begin_transaction(self, database, options_=None, options=None):
        """
        Starts a new transaction.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>>
            >>> response = client.begin_transaction(database)

        Args:
            database (str): The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
            options_ (Union[dict, ~google.cloud.firestore_v1beta1.types.TransactionOptions]): The options for the transaction.
                Defaults to a read-write transaction.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.TransactionOptions`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.BeginTransactionResponse` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.BeginTransactionRequest(
            database=database, options=options_)
        return self._begin_transaction(request, options)

    def commit(self, database, writes, transaction=None, options=None):
        """
        Commits a transaction, while optionally updating documents.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>> writes = []
            >>>
            >>> response = client.commit(database, writes)

        Args:
            database (str): The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
            writes (list[Union[dict, ~google.cloud.firestore_v1beta1.types.Write]]): The writes to apply.

                Always executed atomically and in order.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Write`
            transaction (bytes): If set, applies all writes in this transaction, and commits it.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.CommitResponse` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.CommitRequest(
            database=database, writes=writes, transaction=transaction)
        return self._commit(request, options)

    def rollback(self, database, transaction, options=None):
        """
        Rolls back a transaction.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>> transaction = b''
            >>>
            >>> client.rollback(database, transaction)

        Args:
            database (str): The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
            transaction (bytes): The transaction to roll back.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.RollbackRequest(
            database=database, transaction=transaction)
        self._rollback(request, options)

    def run_query(self,
                  parent,
                  structured_query=None,
                  transaction=None,
                  new_transaction=None,
                  read_time=None,
                  options=None):
        """
        Runs a query.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> for element in client.run_query(parent):
            ...     # process element
            ...     pass

        Args:
            parent (str): The parent resource name. In the format:
                ``projects/{project_id}/databases/{database_id}/documents`` or
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                For example:
                ``projects/my-project/databases/my-database/documents`` or
                ``projects/my-project/databases/my-database/documents/chatrooms/my-chatroom``
            structured_query (Union[dict, ~google.cloud.firestore_v1beta1.types.StructuredQuery]): A structured query.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.StructuredQuery`
            transaction (bytes): Reads documents in a transaction.
            new_transaction (Union[dict, ~google.cloud.firestore_v1beta1.types.TransactionOptions]): Starts a new transaction and reads the documents.
                Defaults to a read-only transaction.
                The new transaction ID will be returned as the first response in the
                stream.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.TransactionOptions`
            read_time (Union[dict, ~google.cloud.firestore_v1beta1.types.Timestamp]): Reads documents as they were at the given time.
                This may not be older than 60 seconds.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Timestamp`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.RunQueryResponse].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(structured_query=structured_query, )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        oneof.check_oneof(
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time, )

        request = firestore_pb2.RunQueryRequest(
            parent=parent,
            structured_query=structured_query,
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time)
        return self._run_query(request, options)

    def write(self, requests, options=None):
        """
        Streams batches of document updates and deletes, in order.

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>> request = {'database': database}
            >>>
            >>> requests = [request]
            >>> for element in client.write(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.firestore_v1beta1.proto.firestore_pb2.WriteRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.firestore_v1beta1.types.WriteRequest`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.WriteResponse].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        return self._write(requests, options)

    def listen(self, requests, options=None):
        """
        Listens to changes.

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>> request = {'database': database}
            >>>
            >>> requests = [request]
            >>> for element in client.listen(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.firestore_v1beta1.proto.firestore_pb2.ListenRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.firestore_v1beta1.types.ListenRequest`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.ListenResponse].

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        return self._listen(requests, options)

    def list_collection_ids(self, parent, page_size=None, options=None):
        """
        Lists all the collection IDs underneath a document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>> from google.gax import CallOptions, INITIAL_PAGE
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_collection_ids(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_collection_ids(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent document. In the format:
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                For example:
                ``projects/my-project/databases/my-database/documents/chatrooms/my-chatroom``
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`str` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_pb2.ListCollectionIdsRequest(
            parent=parent, page_size=page_size)
        return self._list_collection_ids(request, options)
