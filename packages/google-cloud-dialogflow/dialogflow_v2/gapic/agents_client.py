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
"""Accesses the google.cloud.dialogflow.v2 Agents API."""

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
import google.api_core.protobuf_helpers
import grpc

from dialogflow_v2.gapic import agents_client_config
from dialogflow_v2.gapic import enums
from dialogflow_v2.gapic.transports import agents_grpc_transport
from dialogflow_v2.proto import agent_pb2
from dialogflow_v2.proto import agent_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'dialogflow', ).version


class AgentsClient(object):
    """
    Agents are best described as Natural Language Understanding (NLU)
    modules that transform user requests into actionable data. You can
    include agents in your app, product, or service to determine user intent
    and respond to the user in a natural way.

    After you create an agent, you can add ``Intents``, ``Contexts``,
    ``Entity Types``, ``Webhooks``, and so on to manage the flow of a
    conversation and match user input to predefined intents and actions.

    You can create an agent using both Dialogflow Standard Edition and
    Dialogflow Enterprise Edition. For details, see `Dialogflow
    Editions <https://cloud.google.com/dialogflow-enterprise/docs/editions>`__.

    You can save your agent for backup or versioning by exporting the agent
    by using the ``ExportAgent`` method. You can import a saved agent by
    using the ``ImportAgent`` method.

    Dialogflow provides several `prebuilt
    agents <https://cloud.google.com/dialogflow-enterprise/docs/agents-prebuilt>`__
    for common conversation scenarios such as determining a date and time,
    converting currency, and so on.

    For more information about agents, see the `Dialogflow
    documentation <https://cloud.google.com/dialogflow-enterprise/docs/agents-overview>`__.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2.Agents'

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
            dialogflow_v2.AgentsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
            transport (Union[~.AgentsGrpcTransport,
                    Callable[[~.Credentials, type], ~.AgentsGrpcTransport]): A transport
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
            client_config = agents_client_config.config

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
                    default_class=agents_grpc_transport.AgentsGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = agents_grpc_transport.AgentsGrpcTransport(
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
    def get_agent(self,
                  parent,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT,
                  metadata=None):
        """
        Retrieves the specified agent.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.get_agent(parent)

        Args:
            parent (str): Required. The project that the agent to fetch is associated with.
                Format: ``projects/<Project ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types.Agent` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_agent' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_agent'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_agent,
                    default_retry=self._method_configs['GetAgent'].retry,
                    default_timeout=self._method_configs['GetAgent'].timeout,
                    client_info=self._client_info,
                )

        request = agent_pb2.GetAgentRequest(parent=parent, )
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

        return self._inner_api_calls['get_agent'](request,
                                                  retry=retry,
                                                  timeout=timeout,
                                                  metadata=metadata)

    def search_agents(self,
                      parent,
                      page_size=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Returns the list of agents.

        Since there is at most one conversational agent per project, this method
        is useful primarily for listing all agents across projects the caller
        has access to. One can achieve that with a wildcard project collection
        id "-". Refer to `List
        Sub-Collections <https://cloud.google.com/apis/design/design_patterns#list_sub-collections>`__.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_agents(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_agents(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project to list agents from. Format:
                ``projects/<Project ID or '-'>``.
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
            is an iterable of :class:`~google.cloud.dialogflow_v2.types.Agent` instances.
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
        if 'search_agents' not in self._inner_api_calls:
            self._inner_api_calls[
                'search_agents'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.search_agents,
                    default_retry=self._method_configs['SearchAgents'].retry,
                    default_timeout=self._method_configs['SearchAgents'].
                    timeout,
                    client_info=self._client_info,
                )

        request = agent_pb2.SearchAgentsRequest(
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
            method=functools.partial(self._inner_api_calls['search_agents'],
                                     retry=retry,
                                     timeout=timeout,
                                     metadata=metadata),
            request=request,
            items_field='agents',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def train_agent(self,
                    parent,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Trains the specified agent.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.train_agent(parent)
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
            parent (str): Required. The project that the agent to train is associated with.
                Format: ``projects/<Project ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'train_agent' not in self._inner_api_calls:
            self._inner_api_calls[
                'train_agent'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.train_agent,
                    default_retry=self._method_configs['TrainAgent'].retry,
                    default_timeout=self._method_configs['TrainAgent'].timeout,
                    client_info=self._client_info,
                )

        request = agent_pb2.TrainAgentRequest(parent=parent, )
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

        operation = self._inner_api_calls['train_agent'](request,
                                                         retry=retry,
                                                         timeout=timeout,
                                                         metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def export_agent(self,
                     parent,
                     agent_uri=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Exports the specified agent to a ZIP file.

        Operation <response: ``ExportAgentResponse``>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.export_agent(parent)
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
            parent (str): Required. The project that the agent to export is associated with.
                Format: ``projects/<Project ID>``.
            agent_uri (str): Optional. The `Google Cloud
                Storage <https://cloud.google.com/storage/docs/>`__ URI to export the
                agent to. The format of this URI must be
                ``gs://<bucket-name>/<object-name>``. If left unspecified, the
                serialized agent is returned inline.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'export_agent' not in self._inner_api_calls:
            self._inner_api_calls[
                'export_agent'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.export_agent,
                    default_retry=self._method_configs['ExportAgent'].retry,
                    default_timeout=self._method_configs['ExportAgent'].
                    timeout,
                    client_info=self._client_info,
                )

        request = agent_pb2.ExportAgentRequest(
            parent=parent,
            agent_uri=agent_uri,
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

        operation = self._inner_api_calls['export_agent'](request,
                                                          retry=retry,
                                                          timeout=timeout,
                                                          metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            agent_pb2.ExportAgentResponse,
            metadata_type=struct_pb2.Struct,
        )

    def import_agent(self,
                     parent,
                     agent_uri=None,
                     agent_content=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the existing ones.
        Intents and entity types with the same name are replaced with the new
        versions from ImportAgentRequest.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.import_agent(parent)
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
            parent (str): Required. The project that the agent to import is associated with.
                Format: ``projects/<Project ID>``.
            agent_uri (str): The URI to a Google Cloud Storage file containing the agent to import.
                Note: The URI must start with "gs://".
            agent_content (bytes): The agent to import.

                Example for how to import an agent via the command line:

                .. raw:: html

                    <pre>curl \
                      'https://dialogflow.googleapis.com/v2/projects/&lt;project_name&gt;/agent:import\
                       -X POST \
                       -H 'Authorization: Bearer '$(gcloud auth application-default
                       print-access-token) \
                       -H 'Accept: application/json' \
                       -H 'Content-Type: application/json' \
                       --compressed \
                       --data-binary "{
                          'agentContent': '$(cat &lt;agent zip file&gt; | base64 -w 0)'
                       }"</pre>
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'import_agent' not in self._inner_api_calls:
            self._inner_api_calls[
                'import_agent'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.import_agent,
                    default_retry=self._method_configs['ImportAgent'].retry,
                    default_timeout=self._method_configs['ImportAgent'].
                    timeout,
                    client_info=self._client_info,
                )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri,
            agent_content=agent_content,
        )

        request = agent_pb2.ImportAgentRequest(
            parent=parent,
            agent_uri=agent_uri,
            agent_content=agent_content,
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

        operation = self._inner_api_calls['import_agent'](request,
                                                          retry=retry,
                                                          timeout=timeout,
                                                          metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def restore_agent(self,
                      parent,
                      agent_uri=None,
                      agent_content=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Restores the specified agent from a ZIP file.

        Replaces the current agent version with a new one. All the intents and
        entity types in the older version are deleted.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.restore_agent(parent)
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
            parent (str): Required. The project that the agent to restore is associated with.
                Format: ``projects/<Project ID>``.
            agent_uri (str): The URI to a Google Cloud Storage file containing the agent to restore.
                Note: The URI must start with "gs://".
            agent_content (bytes): The agent to restore.

                Example for how to restore an agent via the command line:

                .. raw:: html

                    <pre>curl \
                      'https://dialogflow.googleapis.com/v2/projects/&lt;project_name&gt;/agent:restore\
                       -X POST \
                       -H 'Authorization: Bearer '$(gcloud auth application-default
                       print-access-token) \
                       -H 'Accept: application/json' \
                       -H 'Content-Type: application/json' \
                       --compressed \
                       --data-binary "{
                           'agentContent': '$(cat &lt;agent zip file&gt; | base64 -w 0)'
                       }"</pre>
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'restore_agent' not in self._inner_api_calls:
            self._inner_api_calls[
                'restore_agent'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.restore_agent,
                    default_retry=self._method_configs['RestoreAgent'].retry,
                    default_timeout=self._method_configs['RestoreAgent'].
                    timeout,
                    client_info=self._client_info,
                )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri,
            agent_content=agent_content,
        )

        request = agent_pb2.RestoreAgentRequest(
            parent=parent,
            agent_uri=agent_uri,
            agent_content=agent_content,
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

        operation = self._inner_api_calls['restore_agent'](request,
                                                           retry=retry,
                                                           timeout=timeout,
                                                           metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )
