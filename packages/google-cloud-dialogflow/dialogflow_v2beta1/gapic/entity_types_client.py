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

"""Accesses the google.cloud.dialogflow.v2beta1 EntityTypes API."""

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

from dialogflow_v2beta1.gapic import entity_types_client_config
from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic.transports import entity_types_grpc_transport
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import agent_pb2_grpc
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import context_pb2_grpc
from dialogflow_v2beta1.proto import document_pb2
from dialogflow_v2beta1.proto import document_pb2_grpc
from dialogflow_v2beta1.proto import entity_type_pb2
from dialogflow_v2beta1.proto import entity_type_pb2_grpc
from dialogflow_v2beta1.proto import gcs_pb2
from dialogflow_v2beta1.proto import validation_result_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("dialogflow").version


class EntityTypesClient(object):
    """
    Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    When you define an entity, you can also include synonyms that all map to
    that entity. For example, "soft drink", "soda", "pop", and so on.

    There are three types of entities:

    -  **System** - entities that are defined by the Dialogflow API for
       common data types such as date, time, currency, and so on. A system
       entity is represented by the ``EntityType`` type.

    -  **Developer** - entities that are defined by you that represent
       actionable data that is meaningful to your application. For example,
       you could define a ``pizza.sauce`` entity for red or white pizza
       sauce, a ``pizza.cheese`` entity for the different types of cheese on
       a pizza, a ``pizza.topping`` entity for different toppings, and so
       on. A developer entity is represented by the ``EntityType`` type.

    -  **User** - entities that are built for an individual user such as
       favorites, preferences, playlists, and so on. A user entity is
       represented by the ``SessionEntityType`` type.

    For more information about entity types, see the `Dialogflow
    documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.
    """

    SERVICE_ADDRESS = "dialogflow.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dialogflow.v2beta1.EntityTypes"

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
            dialogflow_v2beta1.EntityTypesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def entity_type_path(cls, project, entity_type):
        """Return a fully-qualified entity_type string."""
        return google.api_core.path_template.expand(
            "projects/{project}/agent/entityTypes/{entity_type}",
            project=project,
            entity_type=entity_type,
        )

    @classmethod
    def project_agent_path(cls, project):
        """Return a fully-qualified project_agent string."""
        return google.api_core.path_template.expand(
            "projects/{project}/agent", project=project
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
            transport (Union[~.EntityTypesGrpcTransport,
                    Callable[[~.Credentials, type], ~.EntityTypesGrpcTransport]): A transport
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
            client_config = entity_types_client_config.config

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
                    default_class=entity_types_grpc_transport.EntityTypesGrpcTransport,
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
            self.transport = entity_types_grpc_transport.EntityTypesGrpcTransport(
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
    def list_entity_types(
        self,
        parent,
        language_code=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns the list of all entity types in the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_entity_types(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_entity_types(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The agent to list all entity types from. Format:
                ``projects/<Project ID>/agent``.
            language_code (str): Optional. The language to list entity synonyms for. If not specified,
                the agent's default language is used. `Many
                languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
                are supported. Note: languages must be enabled in the agent before they
                can be used.
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
            An iterable of :class:`~google.cloud.dialogflow_v2beta1.types.EntityType` instances.
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
        if "list_entity_types" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_entity_types"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_entity_types,
                default_retry=self._method_configs["ListEntityTypes"].retry,
                default_timeout=self._method_configs["ListEntityTypes"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.ListEntityTypesRequest(
            parent=parent, language_code=language_code, page_size=page_size
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
                self._inner_api_calls["list_entity_types"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="entity_types",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_entity_type(
        self,
        name,
        language_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves the specified entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> response = client.get_entity_type(name)

        Args:
            name (str): Required. The name of the entity type. Format:
                ``projects/<Project ID>/agent/entityTypes/<EntityType ID>``.
            language_code (str): Optional. The language to retrieve entity synonyms for. If not
                specified, the agent's default language is used. `Many
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
            A :class:`~google.cloud.dialogflow_v2beta1.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_entity_type" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_entity_type"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_entity_type,
                default_retry=self._method_configs["GetEntityType"].retry,
                default_timeout=self._method_configs["GetEntityType"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.GetEntityTypeRequest(
            name=name, language_code=language_code
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

        return self._inner_api_calls["get_entity_type"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_entity_type(
        self,
        parent,
        entity_type,
        language_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an entity type in the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `entity_type`:
            >>> entity_type = {}
            >>>
            >>> response = client.create_entity_type(parent, entity_type)

        Args:
            parent (str): Required. The agent to create a entity type for. Format:
                ``projects/<Project ID>/agent``.
            entity_type (Union[dict, ~google.cloud.dialogflow_v2beta1.types.EntityType]): Required. The entity type to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.EntityType`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_type``. If
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
            A :class:`~google.cloud.dialogflow_v2beta1.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_entity_type" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_entity_type"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_entity_type,
                default_retry=self._method_configs["CreateEntityType"].retry,
                default_timeout=self._method_configs["CreateEntityType"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.CreateEntityTypeRequest(
            parent=parent, entity_type=entity_type, language_code=language_code
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

        return self._inner_api_calls["create_entity_type"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_entity_type(
        self,
        entity_type,
        language_code=None,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the specified entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> # TODO: Initialize `entity_type`:
            >>> entity_type = {}
            >>>
            >>> response = client.update_entity_type(entity_type)

        Args:
            entity_type (Union[dict, ~google.cloud.dialogflow_v2beta1.types.EntityType]): Required. The entity type to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.EntityType`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_type``. If
                not specified, the agent's default language is used. `Many
                languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
                are supported. Note: languages must be enabled in the agent before they
                can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_entity_type" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_entity_type"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_entity_type,
                default_retry=self._method_configs["UpdateEntityType"].retry,
                default_timeout=self._method_configs["UpdateEntityType"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.UpdateEntityTypeRequest(
            entity_type=entity_type,
            language_code=language_code,
            update_mask=update_mask,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("entity_type.name", entity_type.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_entity_type"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_entity_type(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> client.delete_entity_type(name)

        Args:
            name (str): Required. The name of the entity type to delete. Format:
                ``projects/<Project ID>/agent/entityTypes/<EntityType ID>``.
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
        if "delete_entity_type" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_entity_type"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_entity_type,
                default_retry=self._method_configs["DeleteEntityType"].retry,
                default_timeout=self._method_configs["DeleteEntityType"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.DeleteEntityTypeRequest(name=name)
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

        self._inner_api_calls["delete_entity_type"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_update_entity_types(
        self,
        parent,
        entity_type_batch_uri=None,
        entity_type_batch_inline=None,
        language_code=None,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates/Creates multiple entity types in the specified agent.

        Operation <response: ``BatchUpdateEntityTypesResponse``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>> response = client.batch_update_entity_types(parent)
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
            parent (str): Required. The name of the agent to update or create entity types in.
                Format: ``projects/<Project ID>/agent``.
            entity_type_batch_uri (str): The URI to a Google Cloud Storage file containing entity types to update
                or create. The file format can either be a serialized proto (of
                EntityBatch type) or a JSON object. Note: The URI must start with
                "gs://".
            entity_type_batch_inline (Union[dict, ~google.cloud.dialogflow_v2beta1.types.EntityTypeBatch]): The collection of entity types to update or create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.EntityTypeBatch`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_types``.
                If not specified, the agent's default language is used. `Many
                languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
                are supported. Note: languages must be enabled in the agent before they
                can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "batch_update_entity_types" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_update_entity_types"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_update_entity_types,
                default_retry=self._method_configs["BatchUpdateEntityTypes"].retry,
                default_timeout=self._method_configs["BatchUpdateEntityTypes"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            entity_type_batch_uri=entity_type_batch_uri,
            entity_type_batch_inline=entity_type_batch_inline,
        )

        request = entity_type_pb2.BatchUpdateEntityTypesRequest(
            parent=parent,
            entity_type_batch_uri=entity_type_batch_uri,
            entity_type_batch_inline=entity_type_batch_inline,
            language_code=language_code,
            update_mask=update_mask,
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

        operation = self._inner_api_calls["batch_update_entity_types"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            entity_type_pb2.BatchUpdateEntityTypesResponse,
            metadata_type=struct_pb2.Struct,
        )

    def batch_delete_entity_types(
        self,
        parent,
        entity_type_names,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes entity types in the specified agent.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `entity_type_names`:
            >>> entity_type_names = []
            >>>
            >>> response = client.batch_delete_entity_types(parent, entity_type_names)
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
            parent (str): Required. The name of the agent to delete all entities types for.
                Format: ``projects/<Project ID>/agent``.
            entity_type_names (list[str]): Required. The names entity types to delete. All names must point to the
                same agent as ``parent``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "batch_delete_entity_types" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_delete_entity_types"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_delete_entity_types,
                default_retry=self._method_configs["BatchDeleteEntityTypes"].retry,
                default_timeout=self._method_configs["BatchDeleteEntityTypes"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.BatchDeleteEntityTypesRequest(
            parent=parent, entity_type_names=entity_type_names
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

        operation = self._inner_api_calls["batch_delete_entity_types"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_create_entities(
        self,
        parent,
        entities,
        language_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates multiple new entities in the specified entity type.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> # TODO: Initialize `entities`:
            >>> entities = []
            >>>
            >>> response = client.batch_create_entities(parent, entities)
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
            parent (str): Required. The name of the entity type to create entities in. Format:
                ``projects/<Project ID>/agent/entityTypes/<Entity Type ID>``.
            entities (list[Union[dict, ~google.cloud.dialogflow_v2beta1.types.Entity]]): Required. The entities to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.Entity`
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If
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
            A :class:`~google.cloud.dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_entities,
                default_retry=self._method_configs["BatchCreateEntities"].retry,
                default_timeout=self._method_configs["BatchCreateEntities"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.BatchCreateEntitiesRequest(
            parent=parent, entities=entities, language_code=language_code
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

        operation = self._inner_api_calls["batch_create_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_update_entities(
        self,
        parent,
        entities,
        language_code=None,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates or creates multiple entities in the specified entity type. This
        method does not affect entities in the entity type that aren't
        explicitly specified in the request.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> # TODO: Initialize `entities`:
            >>> entities = []
            >>>
            >>> response = client.batch_update_entities(parent, entities)
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
            parent (str): Required. The name of the entity type to update or create entities in.
                Format: ``projects/<Project ID>/agent/entityTypes/<Entity Type ID>``.
            entities (list[Union[dict, ~google.cloud.dialogflow_v2beta1.types.Entity]]): Required. The entities to update or create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.Entity`
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If
                not specified, the agent's default language is used. `Many
                languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
                are supported. Note: languages must be enabled in the agent before they
                can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "batch_update_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_update_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_update_entities,
                default_retry=self._method_configs["BatchUpdateEntities"].retry,
                default_timeout=self._method_configs["BatchUpdateEntities"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.BatchUpdateEntitiesRequest(
            parent=parent,
            entities=entities,
            language_code=language_code,
            update_mask=update_mask,
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

        operation = self._inner_api_calls["batch_update_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_delete_entities(
        self,
        parent,
        entity_values,
        language_code=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes entities in the specified entity type.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> # TODO: Initialize `entity_values`:
            >>> entity_values = []
            >>>
            >>> response = client.batch_delete_entities(parent, entity_values)
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
            parent (str): Required. The name of the entity type to delete entries for. Format:
                ``projects/<Project ID>/agent/entityTypes/<Entity Type ID>``.
            entity_values (list[str]): Required. The canonical ``values`` of the entities to delete. Note that
                these are not fully-qualified names, i.e. they don't start with
                ``projects/<Project ID>``.
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If
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
            A :class:`~google.cloud.dialogflow_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_delete_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_delete_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_delete_entities,
                default_retry=self._method_configs["BatchDeleteEntities"].retry,
                default_timeout=self._method_configs["BatchDeleteEntities"].timeout,
                client_info=self._client_info,
            )

        request = entity_type_pb2.BatchDeleteEntitiesRequest(
            parent=parent, entity_values=entity_values, language_code=language_code
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

        operation = self._inner_api_calls["batch_delete_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )
