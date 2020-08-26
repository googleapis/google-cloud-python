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

"""Accesses the google.cloud.dialogflow.v2 Agents API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
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
from dialogflow_v2.proto import validation_result_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("dialogflow").version


class AgentsClient(object):
    """Service for managing ``Agents``."""

    SERVICE_ADDRESS = "dialogflow.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dialogflow.v2.Agents"

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
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = agents_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=agents_grpc_transport.AgentsGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = agents_grpc_transport.AgentsGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
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
    def get_agent(
        self,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "get_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_agent,
                default_retry=self._method_configs["GetAgent"].retry,
                default_timeout=self._method_configs["GetAgent"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.GetAgentRequest(parent=parent)
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

        return self._inner_api_calls["get_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_agent(
        self,
        agent,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates/updates the specified agent.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> # TODO: Initialize `agent`:
            >>> agent = {}
            >>>
            >>> response = client.set_agent(agent)

        Args:
            agent (Union[dict, ~google.cloud.dialogflow_v2.types.Agent]): Required. The agent to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.Agent`
            update_mask (Union[dict, ~google.cloud.dialogflow_v2.types.FieldMask]): Optional. The mask to control which fields get updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "set_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_agent,
                default_retry=self._method_configs["SetAgent"].retry,
                default_timeout=self._method_configs["SetAgent"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.SetAgentRequest(agent=agent, update_mask=update_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("agent.parent", agent.parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_agent(
        self,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified agent.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> client.delete_agent(parent)

        Args:
            parent (str): Required. The project that the agent to delete is associated with.
                Format: ``projects/<Project ID>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "delete_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_agent,
                default_retry=self._method_configs["DeleteAgent"].retry,
                default_timeout=self._method_configs["DeleteAgent"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.DeleteAgentRequest(parent=parent)
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

        self._inner_api_calls["delete_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_agents(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.dialogflow_v2.types.Agent` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_agents" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_agents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_agents,
                default_retry=self._method_configs["SearchAgents"].retry,
                default_timeout=self._method_configs["SearchAgents"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.SearchAgentsRequest(parent=parent, page_size=page_size)
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
                self._inner_api_calls["search_agents"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="agents",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def train_agent(
        self,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "train_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "train_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.train_agent,
                default_retry=self._method_configs["TrainAgent"].retry,
                default_timeout=self._method_configs["TrainAgent"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.TrainAgentRequest(parent=parent)
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

        operation = self._inner_api_calls["train_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def export_agent(
        self,
        parent,
        agent_uri=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>> # TODO: Initialize `agent_uri`:
            >>> agent_uri = ''
            >>>
            >>> response = client.export_agent(parent, agent_uri)
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
            agent_uri (str): Required. The `Google Cloud
                Storage <https://cloud.google.com/storage/docs/>`__ URI to export the
                agent to. The format of this URI must be
                ``gs://<bucket-name>/<object-name>``. If left unspecified, the
                serialized agent is returned inline.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "export_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_agent,
                default_retry=self._method_configs["ExportAgent"].retry,
                default_timeout=self._method_configs["ExportAgent"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.ExportAgentRequest(parent=parent, agent_uri=agent_uri)
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

        operation = self._inner_api_calls["export_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            agent_pb2.ExportAgentResponse,
            metadata_type=struct_pb2.Struct,
        )

    def import_agent(
        self,
        parent,
        agent_uri=None,
        agent_content=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the existing ones.
        Intents and entity types with the same name are replaced with the new
        versions from ``ImportAgentRequest``. After the import, the imported
        draft agent will be trained automatically (unless disabled in agent
        settings). However, once the import is done, training may not be
        completed yet. Please call ``TrainAgent`` and wait for the operation it
        returns in order to train explicitly.

        Operation <response: ``google.protobuf.Empty``> An operation which
        tracks when importing is complete. It only tracks when the draft agent
        is updated not when it is done training.

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
            agent_content (bytes): Zip compressed raw byte content for agent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "import_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_agent,
                default_retry=self._method_configs["ImportAgent"].retry,
                default_timeout=self._method_configs["ImportAgent"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri, agent_content=agent_content
        )

        request = agent_pb2.ImportAgentRequest(
            parent=parent, agent_uri=agent_uri, agent_content=agent_content
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

        operation = self._inner_api_calls["import_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def restore_agent(
        self,
        parent,
        agent_uri=None,
        agent_content=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Restores the specified agent from a ZIP file.

        Replaces the current agent version with a new one. All the intents and
        entity types in the older version are deleted. After the restore, the
        restored draft agent will be trained automatically (unless disabled in
        agent settings). However, once the restore is done, training may not be
        completed yet. Please call ``TrainAgent`` and wait for the operation it
        returns in order to train explicitly.

        Operation <response: ``google.protobuf.Empty``> An operation which
        tracks when restoring is complete. It only tracks when the draft agent
        is updated not when it is done training.

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
            agent_content (bytes): Zip compressed raw byte content for agent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "restore_agent" not in self._inner_api_calls:
            self._inner_api_calls[
                "restore_agent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.restore_agent,
                default_retry=self._method_configs["RestoreAgent"].retry,
                default_timeout=self._method_configs["RestoreAgent"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            agent_uri=agent_uri, agent_content=agent_content
        )

        request = agent_pb2.RestoreAgentRequest(
            parent=parent, agent_uri=agent_uri, agent_content=agent_content
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

        operation = self._inner_api_calls["restore_agent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def get_validation_result(
        self,
        parent=None,
        language_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets agent validation result. Agent validation is performed during
        training time and is updated automatically when training is completed.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.AgentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.get_validation_result(parent)

        Args:
            parent (str): Required. The project that the agent is associated with. Format:
                ``projects/<Project ID>``.
            language_code (str): Optional. The language for which you want a validation result. If
                not specified, the agent's default language is used. `Many
                languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
                are supported. Note: languages must be enabled in the agent before they
                can be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types.ValidationResult` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_validation_result" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_validation_result"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_validation_result,
                default_retry=self._method_configs["GetValidationResult"].retry,
                default_timeout=self._method_configs["GetValidationResult"].timeout,
                client_info=self._client_info,
            )

        request = agent_pb2.GetValidationResultRequest(
            parent=parent, language_code=language_code
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

        return self._inner_api_calls["get_validation_result"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
