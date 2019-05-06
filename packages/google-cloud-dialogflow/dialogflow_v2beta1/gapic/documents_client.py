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
"""Accesses the google.cloud.dialogflow.v2beta1 Documents API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from dialogflow_v2beta1.gapic import documents_client_config
from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic.transports import documents_grpc_transport
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import agent_pb2_grpc
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import context_pb2_grpc
from dialogflow_v2beta1.proto import document_pb2
from dialogflow_v2beta1.proto import document_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'dialogflow', ).version


class DocumentsClient(object):
    """Manages documents of a knowledge base."""

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.Documents'

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
            dialogflow_v2beta1.DocumentsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def document_path(cls, project, knowledge_base, document):
        """Return a fully-qualified document string."""
        return google.api_core.path_template.expand(
            'projects/{project}/knowledgeBases/{knowledge_base}/documents/{document}',
            project=project,
            knowledge_base=knowledge_base,
            document=document,
        )

    @classmethod
    def knowledge_base_path(cls, project, knowledge_base):
        """Return a fully-qualified knowledge_base string."""
        return google.api_core.path_template.expand(
            'projects/{project}/knowledgeBases/{knowledge_base}',
            project=project,
            knowledge_base=knowledge_base,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=None,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.DocumentsGrpcTransport,
                    Callable[[~.Credentials, type], ~.DocumentsGrpcTransport]): A transport
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
            warnings.warn('The `client_config` argument is deprecated.',
                          PendingDeprecationWarning,
                          stacklevel=2)
        else:
            client_config = documents_client_config.config

        if channel:
            warnings.warn(
                'The `channel` argument is deprecated; use '
                '`transport` instead.',
                PendingDeprecationWarning,
                stacklevel=2)

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=documents_grpc_transport.
                    DocumentsGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = documents_grpc_transport.DocumentsGrpcTransport(
                address=self.SERVICE_ADDRESS,
                channel=channel,
                credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION, )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_documents(self,
                       parent,
                       page_size=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Returns the list of all documents of the knowledge base.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> parent = client.knowledge_base_path('[PROJECT]', '[KNOWLEDGE_BASE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_documents(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_documents(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The knowledge base to list all documents for. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>``.
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
            is an iterable of :class:`~google.cloud.dialogflow_v2beta1.types.Document` instances.
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
        if 'list_documents' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_documents'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_documents,
                    default_retry=self._method_configs['ListDocuments'].retry,
                    default_timeout=self._method_configs['ListDocuments'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.ListDocumentsRequest(
            parent=parent,
            page_size=page_size,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('parent', parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(self._inner_api_calls['list_documents'],
                                     retry=retry,
                                     timeout=timeout,
                                     metadata=metadata),
            request=request,
            items_field='documents',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_document(self,
                     name,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Retrieves the specified document.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> name = client.document_path('[PROJECT]', '[KNOWLEDGE_BASE]', '[DOCUMENT]')
            >>>
            >>> response = client.get_document(name)

        Args:
            name (str): Required. The name of the document to retrieve. Format
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.Document` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_document' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_document'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_document,
                    default_retry=self._method_configs['GetDocument'].retry,
                    default_timeout=self._method_configs['GetDocument'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.GetDocumentRequest(name=name, )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('name', name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['get_document'](request,
                                                     retry=retry,
                                                     timeout=timeout,
                                                     metadata=metadata)

    def create_document(self,
                        parent,
                        document,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Creates a new document.

        Operation <response: ``Document``, metadata:
        ``KnowledgeOperationMetadata``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> parent = client.knowledge_base_path('[PROJECT]', '[KNOWLEDGE_BASE]')
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.create_document(parent, document)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The knoweldge base to create a document for. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>``.
            document (Union[dict, ~google.cloud.dialogflow_v2beta1.types.Document]): Required. The document to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.Document`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_document' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_document'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_document,
                    default_retry=self._method_configs['CreateDocument'].retry,
                    default_timeout=self._method_configs['CreateDocument'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.CreateDocumentRequest(
            parent=parent,
            document=document,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('parent', parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        operation = self._inner_api_calls['create_document'](request,
                                                             retry=retry,
                                                             timeout=timeout,
                                                             metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            document_pb2.Document,
            metadata_type=document_pb2.KnowledgeOperationMetadata,
        )

    def delete_document(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Deletes the specified document.

        Operation <response: ``google.protobuf.Empty``, metadata:
        ``KnowledgeOperationMetadata``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> name = client.document_path('[PROJECT]', '[KNOWLEDGE_BASE]', '[DOCUMENT]')
            >>>
            >>> response = client.delete_document(name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): The name of the document to delete. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'delete_document' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_document'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_document,
                    default_retry=self._method_configs['DeleteDocument'].retry,
                    default_timeout=self._method_configs['DeleteDocument'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.DeleteDocumentRequest(name=name, )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('name', name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        operation = self._inner_api_calls['delete_document'](request,
                                                             retry=retry,
                                                             timeout=timeout,
                                                             metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=document_pb2.KnowledgeOperationMetadata,
        )

    def update_document(self,
                        document=None,
                        update_mask=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Updates the specified document. Operation <response: ``Document``,
        metadata: ``KnowledgeOperationMetadata``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> response = client.update_document()

        Args:
            document (Union[dict, ~google.cloud.dialogflow_v2beta1.types.Document]): Required. The document to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.Document`
            update_mask (Union[dict, ~google.cloud.dialogflow_v2beta1.types.FieldMask]): Optional. Not specified means ``update all``. Currently, only
                ``display_name`` can be updated, an InvalidArgument will be returned for
                attempting to update other fields.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_document' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_document'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_document,
                    default_retry=self._method_configs['UpdateDocument'].retry,
                    default_timeout=self._method_configs['UpdateDocument'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.UpdateDocumentRequest(
            document=document,
            update_mask=update_mask,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('document.name', document.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['update_document'](request,
                                                        retry=retry,
                                                        timeout=timeout,
                                                        metadata=metadata)

    def reload_document(self,
                        name=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Reloads the specified document from its specified source, content\_uri
        or content. The previously loaded content of the document will be
        deleted. Note: Even when the content of the document has not changed,
        there still may be side effects because of internal implementation
        changes. Operation <response: ``Document``, metadata:
        ``KnowledgeOperationMetadata``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.DocumentsClient()
            >>>
            >>> response = client.reload_document()

        Args:
            name (str): The name of the document to reload. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'reload_document' not in self._inner_api_calls:
            self._inner_api_calls[
                'reload_document'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.reload_document,
                    default_retry=self._method_configs['ReloadDocument'].retry,
                    default_timeout=self._method_configs['ReloadDocument'].
                    timeout,
                    client_info=self._client_info,
                )

        request = document_pb2.ReloadDocumentRequest(name=name, )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('name', name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['reload_document'](request,
                                                        retry=retry,
                                                        timeout=timeout,
                                                        metadata=metadata)
