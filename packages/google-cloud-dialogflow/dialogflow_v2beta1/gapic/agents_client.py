# Copyright 2017, Google LLC
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
# https://github.com/google/googleapis/blob/master/google/cloud/dialogflow/v2beta1/agent.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.dialogflow.v2beta1 Agents API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers

from dialogflow_v2beta1.gapic import agents_client_config
from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.proto import agent_pb2
from google.protobuf import empty_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow').version


class AgentsClient(object):
    """
    Manages conversational agents.


    Refer to `agents documentation <https://dialogflow.com/docs/agents>`_ for
    more details about agents.

    Standard methods.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.cloud.dialogflow.v2beta1.Agents')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project, )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=agents_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.agents_stub = (agent_pb2.AgentsStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._get_agent = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.GetAgent,
            default_retry=method_configs['GetAgent'].retry,
            default_timeout=method_configs['GetAgent'].timeout,
            client_info=client_info)
        self._search_agents = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.SearchAgents,
            default_retry=method_configs['SearchAgents'].retry,
            default_timeout=method_configs['SearchAgents'].timeout,
            client_info=client_info)
        self._train_agent = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.TrainAgent,
            default_retry=method_configs['TrainAgent'].retry,
            default_timeout=method_configs['TrainAgent'].timeout,
            client_info=client_info)
        self._export_agent = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.ExportAgent,
            default_retry=method_configs['ExportAgent'].retry,
            default_timeout=method_configs['ExportAgent'].timeout,
            client_info=client_info)
        self._import_agent = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.ImportAgent,
            default_retry=method_configs['ImportAgent'].retry,
            default_timeout=method_configs['ImportAgent'].timeout,
            client_info=client_info)
        self._restore_agent = google.api_core.gapic_v1.method.wrap_method(
            self.agents_stub.RestoreAgent,
            default_retry=method_configs['RestoreAgent'].retry,
            default_timeout=method_configs['RestoreAgent'].timeout,
            client_info=client_info)

    # Service calls
    def get_agent(self,
                  parent,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Retrieves the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
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

        Returns:
            A :class:`~dialogflow_v2beta1.types.Agent` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = agent_pb2.GetAgentRequest(parent=parent)
        return self._get_agent(request, retry=retry, timeout=timeout)

    def search_agents(self,
                      parent,
                      page_size=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns the list of agents.

        Since there is at most one conversational agent per project, this method is
        useful primarily for listing all agents across projects the caller has
        access to. One can achieve that with a wildcard project collection id \"-\".
        Refer to [List
        Sub-Collections](https://cloud.google.com/apis/design/design_patterns#list_sub-collections).

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_agents(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.search_agents(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project to list agents from.
                Format: ``projects/<Project ID or '-'>``.
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

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~dialogflow_v2beta1.types.Agent` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = agent_pb2.SearchAgentsRequest(
            parent=parent, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._search_agents, retry=retry, timeout=timeout),
            request=request,
            items_field='agents',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def train_agent(self,
                    parent,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Trains the specified agent.


        Operation<response: google.protobuf.Empty,
        metadata: google.protobuf.Struct>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
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

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = agent_pb2.TrainAgentRequest(parent=parent)
        operation = self._train_agent(request, retry=retry, timeout=timeout)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct)

    def export_agent(self,
                     parent,
                     agent_uri=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Exports the specified agent to a ZIP file.


        Operation<response: ExportAgentResponse,
        metadata: google.protobuf.Struct>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
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
            agent_uri (str): Optional. The URI to export the agent to. Note: The URI must start with
                \"gs://\". If left unspecified, the serialized agent is returned inline.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = agent_pb2.ExportAgentRequest(
            parent=parent, agent_uri=agent_uri)
        operation = self._export_agent(request, retry=retry, timeout=timeout)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            agent_pb2.ExportAgentResponse,
            metadata_type=struct_pb2.Struct)

    def import_agent(self,
                     parent,
                     agent_uri=None,
                     agent_content=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the existing ones.
        Intents and entity types with the same name are replaced with the new
        versions from ImportAgentRequest.


        Operation<response: google.protobuf.Empty,
        metadata: google.protobuf.Struct>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
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
            agent_uri (str): The URI to a file containing the agent to import. Note: The URI must
                start with \"gs://\".
            agent_content (bytes): The agent to import.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri,
            agent_content=agent_content, )

        request = agent_pb2.ImportAgentRequest(
            parent=parent, agent_uri=agent_uri, agent_content=agent_content)
        operation = self._import_agent(request, retry=retry, timeout=timeout)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct)

    def restore_agent(self,
                      parent,
                      agent_uri=None,
                      agent_content=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Restores the specified agent from a ZIP file.

        Replaces the current agent version with a new one. All the intents and
        entity types in the older version are deleted.


        Operation<response: google.protobuf.Empty,
        metadata: google.protobuf.Struct>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.AgentsClient()
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
            agent_uri (str): The URI to a file containing the agent to restore. Note: The URI must
                start with \"gs://\".
            agent_content (bytes): The agent to restore.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri,
            agent_content=agent_content, )

        request = agent_pb2.RestoreAgentRequest(
            parent=parent, agent_uri=agent_uri, agent_content=agent_content)
        operation = self._restore_agent(request, retry=retry, timeout=timeout)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct)
