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
"""Accesses the google.cloud.dialogflow.v2beta1 KnowledgeBases API."""

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
import grpc

from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic import knowledge_bases_client_config
from dialogflow_v2beta1.gapic.transports import knowledge_bases_grpc_transport
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import agent_pb2_grpc
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import context_pb2_grpc
from dialogflow_v2beta1.proto import document_pb2
from dialogflow_v2beta1.proto import document_pb2_grpc
from dialogflow_v2beta1.proto import entity_type_pb2
from dialogflow_v2beta1.proto import entity_type_pb2_grpc
from dialogflow_v2beta1.proto import intent_pb2
from dialogflow_v2beta1.proto import intent_pb2_grpc
from dialogflow_v2beta1.proto import knowledge_base_pb2
from dialogflow_v2beta1.proto import knowledge_base_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'dialogflow', ).version


class KnowledgeBasesClient(object):
    """
    Manages knowledge bases.

    Allows users to setup and maintain knowledge bases with their knowledge data.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.KnowledgeBases'

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
            dialogflow_v2beta1.KnowledgeBasesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def knowledge_base_path(cls, project, knowledge_base):
        """Return a fully-qualified knowledge_base string."""
        return google.api_core.path_template.expand(
            'projects/{project}/knowledgeBases/{knowledge_base}',
            project=project,
            knowledge_base=knowledge_base,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=None,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.KnowledgeBasesGrpcTransport,
                    Callable[[~.Credentials, type], ~.KnowledgeBasesGrpcTransport]): A transport
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
            client_config = knowledge_bases_client_config.config

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
                    default_class=knowledge_bases_grpc_transport.
                    KnowledgeBasesGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = knowledge_bases_grpc_transport.KnowledgeBasesGrpcTransport(
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
    def list_knowledge_bases(self,
                             parent,
                             page_size=None,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Returns the list of all knowledge bases of the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.KnowledgeBasesClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_knowledge_bases(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_knowledge_bases(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project to list of knowledge bases for. Format:
                ``projects/<Project ID>``.
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
            is an iterable of :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase` instances.
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
        if 'list_knowledge_bases' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_knowledge_bases'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_knowledge_bases,
                    default_retry=self._method_configs['ListKnowledgeBases'].
                    retry,
                    default_timeout=self._method_configs['ListKnowledgeBases'].
                    timeout,
                    client_info=self._client_info,
                )

        request = knowledge_base_pb2.ListKnowledgeBasesRequest(
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
            method=functools.partial(
                self._inner_api_calls['list_knowledge_bases'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='knowledge_bases',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_knowledge_base(self,
                           name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Retrieves the specified knowledge base.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.KnowledgeBasesClient()
            >>>
            >>> name = client.knowledge_base_path('[PROJECT]', '[KNOWLEDGE_BASE]')
            >>>
            >>> response = client.get_knowledge_base(name)

        Args:
            name (str): Required. The name of the knowledge base to retrieve. Format
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_knowledge_base' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_knowledge_base'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_knowledge_base,
                    default_retry=self._method_configs['GetKnowledgeBase'].
                    retry,
                    default_timeout=self._method_configs['GetKnowledgeBase'].
                    timeout,
                    client_info=self._client_info,
                )

        request = knowledge_base_pb2.GetKnowledgeBaseRequest(name=name, )
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

        return self._inner_api_calls['get_knowledge_base'](request,
                                                           retry=retry,
                                                           timeout=timeout,
                                                           metadata=metadata)

    def create_knowledge_base(self,
                              parent,
                              knowledge_base,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Creates a knowledge base.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.KnowledgeBasesClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `knowledge_base`:
            >>> knowledge_base = {}
            >>>
            >>> response = client.create_knowledge_base(parent, knowledge_base)

        Args:
            parent (str): Required. The project to create a knowledge base for. Format:
                ``projects/<Project ID>``.
            knowledge_base (Union[dict, ~google.cloud.dialogflow_v2beta1.types.KnowledgeBase]): Required. The knowledge base to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_knowledge_base' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_knowledge_base'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_knowledge_base,
                    default_retry=self._method_configs['CreateKnowledgeBase'].
                    retry,
                    default_timeout=self.
                    _method_configs['CreateKnowledgeBase'].timeout,
                    client_info=self._client_info,
                )

        request = knowledge_base_pb2.CreateKnowledgeBaseRequest(
            parent=parent,
            knowledge_base=knowledge_base,
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

        return self._inner_api_calls['create_knowledge_base'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_knowledge_base(self,
                              name,
                              force=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Deletes the specified knowledge base.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.KnowledgeBasesClient()
            >>>
            >>> name = client.knowledge_base_path('[PROJECT]', '[KNOWLEDGE_BASE]')
            >>>
            >>> client.delete_knowledge_base(name)

        Args:
            name (str): Required. The name of the knowledge base to delete. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>``.
            force (bool): Optional. Force deletes the knowledge base. When set to true, any documents
                in the knowledge base are also deleted.
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
        if 'delete_knowledge_base' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_knowledge_base'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_knowledge_base,
                    default_retry=self._method_configs['DeleteKnowledgeBase'].
                    retry,
                    default_timeout=self.
                    _method_configs['DeleteKnowledgeBase'].timeout,
                    client_info=self._client_info,
                )

        request = knowledge_base_pb2.DeleteKnowledgeBaseRequest(
            name=name,
            force=force,
        )
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

        self._inner_api_calls['delete_knowledge_base'](request,
                                                       retry=retry,
                                                       timeout=timeout,
                                                       metadata=metadata)

    def update_knowledge_base(self,
                              knowledge_base=None,
                              update_mask=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Updates the specified knowledge base.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.KnowledgeBasesClient()
            >>>
            >>> response = client.update_knowledge_base()

        Args:
            knowledge_base (Union[dict, ~google.cloud.dialogflow_v2beta1.types.KnowledgeBase]): Required. The knowledge base to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase`
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
            A :class:`~google.cloud.dialogflow_v2beta1.types.KnowledgeBase` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_knowledge_base' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_knowledge_base'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_knowledge_base,
                    default_retry=self._method_configs['UpdateKnowledgeBase'].
                    retry,
                    default_timeout=self.
                    _method_configs['UpdateKnowledgeBase'].timeout,
                    client_info=self._client_info,
                )

        request = knowledge_base_pb2.UpdateKnowledgeBaseRequest(
            knowledge_base=knowledge_base,
            update_mask=update_mask,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('knowledge_base.name', knowledge_base.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['update_knowledge_base'](
            request, retry=retry, timeout=timeout, metadata=metadata)
