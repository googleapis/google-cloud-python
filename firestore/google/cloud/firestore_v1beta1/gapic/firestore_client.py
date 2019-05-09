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
"""Accesses the google.firestore.v1beta1 Firestore API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.firestore_v1beta1.gapic import enums
from google.cloud.firestore_v1beta1.gapic import firestore_client_config
from google.cloud.firestore_v1beta1.gapic.transports import firestore_grpc_transport
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.cloud.firestore_v1beta1.proto import firestore_pb2_grpc
from google.cloud.firestore_v1beta1.proto import query_pb2
from google.cloud.firestore_v1beta1.proto import write_pb2
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-firestore"
).version


class FirestoreClient(object):
    """
    The Cloud Firestore service.

    This service exposes several types of comparable timestamps:

    -  ``create_time`` - The time at which a document was created. Changes
       only when a document is deleted, then re-created. Increases in a
       strict monotonic fashion.
    -  ``update_time`` - The time at which a document was last updated.
       Changes every time a document is modified. Does not change when a
       write results in no modifications. Increases in a strict monotonic
       fashion.
    -  ``read_time`` - The time at which a particular state was observed.
       Used to denote a consistent snapshot of the database or the time at
       which a Document was observed to not exist.
    -  ``commit_time`` - The time at which the writes in a transaction were
       committed. Any read with an equal or greater ``read_time`` is
       guaranteed to see the effects of the transaction.
    """

    SERVICE_ADDRESS = "firestore.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.firestore.v1beta1.Firestore"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FirestoreClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def database_root_path(cls, project, database):
        """Return a fully-qualified database_root string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}",
            project=project,
            database=database,
        )

    @classmethod
    def document_root_path(cls, project, database):
        """Return a fully-qualified document_root string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/documents",
            project=project,
            database=database,
        )

    @classmethod
    def document_path_path(cls, project, database, document_path):
        """Return a fully-qualified document_path string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/documents/{document_path=**}",
            project=project,
            database=database,
            document_path=document_path,
        )

    @classmethod
    def any_path_path(cls, project, database, document, any_path):
        """Return a fully-qualified any_path string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/documents/{document}/{any_path=**}",
            project=project,
            database=database,
            document=document,
            any_path=any_path,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.FirestoreGrpcTransport,
                    Callable[[~.Credentials, type], ~.FirestoreGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = firestore_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=firestore_grpc_transport.FirestoreGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = firestore_grpc_transport.FirestoreGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_document(
        self,
        name,
        mask=None,
        transaction=None,
        read_time=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_document" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_document"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_document,
                default_retry=self._method_configs["GetDocument"].retry,
                default_timeout=self._method_configs["GetDocument"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            transaction=transaction, read_time=read_time
        )

        request = firestore_pb2.GetDocumentRequest(
            name=name, mask=mask, transaction=transaction, read_time=read_time
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_document"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_documents(
        self,
        parent,
        collection_id,
        page_size=None,
        order_by=None,
        mask=None,
        transaction=None,
        read_time=None,
        show_missing=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists documents.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> # TODO: Initialize `collection_id`:
            >>> collection_id = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_documents(parent, collection_id):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_documents(parent, collection_id).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name. In the format:
                ``projects/{project_id}/databases/{database_id}/documents`` or
                ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
                For example: ``projects/my-project/databases/my-database/documents`` or
                ``projects/my-project/databases/my-database/documents/chatrooms/my-chatroom``
            collection_id (str): The collection ID, relative to ``parent``, to list. For example:
                ``chatrooms`` or ``messages``.
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
                be returned with a key but will not have fields,
                ``Document.create_time``, or ``Document.update_time`` set.

                Requests with ``show_missing`` may not specify ``where`` or
                ``order_by``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.firestore_v1beta1.types.Document` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_documents" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_documents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_documents,
                default_retry=self._method_configs["ListDocuments"].retry,
                default_timeout=self._method_configs["ListDocuments"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            transaction=transaction, read_time=read_time
        )

        request = firestore_pb2.ListDocumentsRequest(
            parent=parent,
            collection_id=collection_id,
            page_size=page_size,
            order_by=order_by,
            mask=mask,
            transaction=transaction,
            read_time=read_time,
            show_missing=show_missing,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_documents"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="documents",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_document(
        self,
        parent,
        collection_id,
        document_id,
        document,
        mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> # TODO: Initialize `collection_id`:
            >>> collection_id = ''
            >>>
            >>> # TODO: Initialize `document_id`:
            >>> document_id = ''
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.create_document(parent, collection_id, document_id, document)

        Args:
            parent (str): The parent resource. For example:
                ``projects/{project_id}/databases/{database_id}/documents`` or
                ``projects/{project_id}/databases/{database_id}/documents/chatrooms/{chatroom_id}``
            collection_id (str): The collection ID, relative to ``parent``, to list. For example:
                ``chatrooms``.
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_document" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_document"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_document,
                default_retry=self._method_configs["CreateDocument"].retry,
                default_timeout=self._method_configs["CreateDocument"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.CreateDocumentRequest(
            parent=parent,
            collection_id=collection_id,
            document_id=document_id,
            document=document,
            mask=mask,
        )
        return self._inner_api_calls["create_document"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_document(
        self,
        document,
        update_mask,
        mask=None,
        current_document=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates or inserts a document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Document` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_document" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_document"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_document,
                default_retry=self._method_configs["UpdateDocument"].retry,
                default_timeout=self._method_configs["UpdateDocument"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.UpdateDocumentRequest(
            document=document,
            update_mask=update_mask,
            mask=mask,
            current_document=current_document,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("document.name", document.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_document"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_document(
        self,
        name,
        current_document=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_document" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_document"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_document,
                default_retry=self._method_configs["DeleteDocument"].retry,
                default_timeout=self._method_configs["DeleteDocument"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.DeleteDocumentRequest(
            name=name, current_document=current_document
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_document"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_get_documents(
        self,
        database,
        documents,
        mask=None,
        transaction=None,
        new_transaction=None,
        read_time=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>>
            >>> # TODO: Initialize `documents`:
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
                The request will fail if any of the document is not a child resource of
                the given ``database``. Duplicate names will be elided.
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.BatchGetDocumentsResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_get_documents" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_get_documents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_get_documents,
                default_retry=self._method_configs["BatchGetDocuments"].retry,
                default_timeout=self._method_configs["BatchGetDocuments"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time,
        )

        request = firestore_pb2.BatchGetDocumentsRequest(
            database=database,
            documents=documents,
            mask=mask,
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["batch_get_documents"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def begin_transaction(
        self,
        database,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.BeginTransactionResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "begin_transaction" not in self._inner_api_calls:
            self._inner_api_calls[
                "begin_transaction"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.begin_transaction,
                default_retry=self._method_configs["BeginTransaction"].retry,
                default_timeout=self._method_configs["BeginTransaction"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.BeginTransactionRequest(
            database=database, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["begin_transaction"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def commit(
        self,
        database,
        writes,
        transaction=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Commits a transaction, while optionally updating documents.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>>
            >>> # TODO: Initialize `writes`:
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.CommitResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "commit" not in self._inner_api_calls:
            self._inner_api_calls[
                "commit"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.commit,
                default_retry=self._method_configs["Commit"].retry,
                default_timeout=self._method_configs["Commit"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.CommitRequest(
            database=database, writes=writes, transaction=transaction
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["commit"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def rollback(
        self,
        database,
        transaction,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Rolls back a transaction.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> database = client.database_root_path('[PROJECT]', '[DATABASE]')
            >>>
            >>> # TODO: Initialize `transaction`:
            >>> transaction = b''
            >>>
            >>> client.rollback(database, transaction)

        Args:
            database (str): The database name. In the format:
                ``projects/{project_id}/databases/{database_id}``.
            transaction (bytes): The transaction to roll back.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "rollback" not in self._inner_api_calls:
            self._inner_api_calls[
                "rollback"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.rollback,
                default_retry=self._method_configs["Rollback"].retry,
                default_timeout=self._method_configs["Rollback"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.RollbackRequest(
            database=database, transaction=transaction
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("database", database)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["rollback"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def run_query(
        self,
        parent,
        structured_query=None,
        transaction=None,
        new_transaction=None,
        read_time=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
                For example: ``projects/my-project/databases/my-database/documents`` or
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.RunQueryResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "run_query" not in self._inner_api_calls:
            self._inner_api_calls[
                "run_query"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.run_query,
                default_retry=self._method_configs["RunQuery"].retry,
                default_timeout=self._method_configs["RunQuery"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(structured_query=structured_query)

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time,
        )

        request = firestore_pb2.RunQueryRequest(
            parent=parent,
            structured_query=structured_query,
            transaction=transaction,
            new_transaction=new_transaction,
            read_time=read_time,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["run_query"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def write(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.WriteResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "write" not in self._inner_api_calls:
            self._inner_api_calls[
                "write"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.write,
                default_retry=self._method_configs["Write"].retry,
                default_timeout=self._method_configs["Write"].timeout,
                client_info=self._client_info,
            )

        return self._inner_api_calls["write"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )

    def listen(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.firestore_v1beta1.types.ListenResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "listen" not in self._inner_api_calls:
            self._inner_api_calls[
                "listen"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.listen,
                default_retry=self._method_configs["Listen"].retry,
                default_timeout=self._method_configs["Listen"].timeout,
                client_info=self._client_info,
            )

        return self._inner_api_calls["listen"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_collection_ids(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all the collection IDs underneath a document.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreClient()
            >>>
            >>> parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]', '[ANY_PATH]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_collection_ids(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_collection_ids(parent).pages:
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`str` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_collection_ids" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_collection_ids"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_collection_ids,
                default_retry=self._method_configs["ListCollectionIds"].retry,
                default_timeout=self._method_configs["ListCollectionIds"].timeout,
                client_info=self._client_info,
            )

        request = firestore_pb2.ListCollectionIdsRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_collection_ids"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="collection_ids",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
