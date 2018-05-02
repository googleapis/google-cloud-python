# Copyright 2018 Google LLC
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
"""Accesses the google.cloud.dialogflow.v2 EntityTypes API."""

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

from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

from dialogflow_v2.gapic import entity_types_client_config
from dialogflow_v2.gapic import enums
from dialogflow_v2.proto import agent_pb2
from dialogflow_v2.proto import context_pb2
from dialogflow_v2.proto import entity_type_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'dialogflow',
).version


class EntityTypesClient(object):
    """
    Manages agent entity types.


    Refer to the `Dialogflow documentation <https://dialogflow.com/docs/entities>`__
    for more details about entity types.
    #
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2.EntityTypes'

    @classmethod
    def project_agent_path(cls, project):
        """Return a fully-qualified project_agent string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent',
            project=project,
        )

    @classmethod
    def entity_type_path(cls, project, entity_type):
        """Return a fully-qualified entity_type string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/entityTypes/{entity_type}',
            project=project,
            entity_type=entity_type,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=entity_types_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.entity_types_stub = (entity_type_pb2.EntityTypesStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._list_entity_types = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.ListEntityTypes,
            default_retry=method_configs['ListEntityTypes'].retry,
            default_timeout=method_configs['ListEntityTypes'].timeout,
            client_info=client_info,
        )
        self._get_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.GetEntityType,
            default_retry=method_configs['GetEntityType'].retry,
            default_timeout=method_configs['GetEntityType'].timeout,
            client_info=client_info,
        )
        self._create_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.CreateEntityType,
            default_retry=method_configs['CreateEntityType'].retry,
            default_timeout=method_configs['CreateEntityType'].timeout,
            client_info=client_info,
        )
        self._update_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.UpdateEntityType,
            default_retry=method_configs['UpdateEntityType'].retry,
            default_timeout=method_configs['UpdateEntityType'].timeout,
            client_info=client_info,
        )
        self._delete_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.DeleteEntityType,
            default_retry=method_configs['DeleteEntityType'].retry,
            default_timeout=method_configs['DeleteEntityType'].timeout,
            client_info=client_info,
        )
        self._batch_update_entity_types = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.BatchUpdateEntityTypes,
            default_retry=method_configs['BatchUpdateEntityTypes'].retry,
            default_timeout=method_configs['BatchUpdateEntityTypes'].timeout,
            client_info=client_info,
        )
        self._batch_delete_entity_types = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.BatchDeleteEntityTypes,
            default_retry=method_configs['BatchDeleteEntityTypes'].retry,
            default_timeout=method_configs['BatchDeleteEntityTypes'].timeout,
            client_info=client_info,
        )
        self._batch_create_entities = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.BatchCreateEntities,
            default_retry=method_configs['BatchCreateEntities'].retry,
            default_timeout=method_configs['BatchCreateEntities'].timeout,
            client_info=client_info,
        )
        self._batch_update_entities = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.BatchUpdateEntities,
            default_retry=method_configs['BatchUpdateEntities'].retry,
            default_timeout=method_configs['BatchUpdateEntities'].timeout,
            client_info=client_info,
        )
        self._batch_delete_entities = google.api_core.gapic_v1.method.wrap_method(
            self.entity_types_stub.BatchDeleteEntities,
            default_retry=method_configs['BatchDeleteEntities'].retry,
            default_timeout=method_configs['BatchDeleteEntities'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_entity_types(self,
                          parent,
                          language_code=None,
                          page_size=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Returns the list of all entity types in the specified agent.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_entity_types(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_entity_types(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The agent to list all entity types from.
                Format: ``projects/<Project ID>/agent``.
            language_code (str): Optional. The language to list entity synonyms for. If not specified,
                the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
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
            is an iterable of :class:`~google.cloud.dialogflow_v2.types.EntityType` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.ListEntityTypesRequest(
            parent=parent,
            language_code=language_code,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_entity_types,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='entity_types',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_entity_type(self,
                        name,
                        language_code=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Retrieves the specified entity type.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> response = client.get_entity_type(name)

        Args:
            name (str): Required. The name of the entity type.
                Format: ``projects/<Project ID>/agent/entityTypes/<EntityType ID>``.
            language_code (str): Optional. The language to retrieve entity synonyms for. If not specified,
                the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.GetEntityTypeRequest(
            name=name,
            language_code=language_code,
        )
        return self._get_entity_type(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_entity_type(self,
                           parent,
                           entity_type,
                           language_code=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Creates an entity type in the specified agent.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>> entity_type = {}
            >>>
            >>> response = client.create_entity_type(parent, entity_type)

        Args:
            parent (str): Required. The agent to create a entity type for.
                Format: ``projects/<Project ID>/agent``.
            entity_type (Union[dict, ~google.cloud.dialogflow_v2.types.EntityType]): Required. The entity type to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.EntityType`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_type``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.CreateEntityTypeRequest(
            parent=parent,
            entity_type=entity_type,
            language_code=language_code,
        )
        return self._create_entity_type(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_entity_type(self,
                           entity_type,
                           language_code=None,
                           update_mask=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Updates the specified entity type.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> entity_type = {}
            >>>
            >>> response = client.update_entity_type(entity_type)

        Args:
            entity_type (Union[dict, ~google.cloud.dialogflow_v2.types.EntityType]): Required. The entity type to update.
                Format: ``projects/<Project ID>/agent/entityTypes/<EntityType ID>``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.EntityType`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_type``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2.types.EntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.UpdateEntityTypeRequest(
            entity_type=entity_type,
            language_code=language_code,
            update_mask=update_mask,
        )
        return self._update_entity_type(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_entity_type(self,
                           name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Deletes the specified entity type.

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
            >>>
            >>> client.delete_entity_type(name)

        Args:
            name (str): Required. The name of the entity type to delete.
                Format: ``projects/<Project ID>/agent/entityTypes/<EntityType ID>``.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.DeleteEntityTypeRequest(name=name, )
        self._delete_entity_type(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def batch_update_entity_types(
            self,
            parent,
            entity_type_batch_uri=None,
            entity_type_batch_inline=None,
            language_code=None,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates/Creates multiple entity types in the specified agent.

        Operation <response: ``BatchUpdateEntityTypesResponse``,
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
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
                \"gs://\".
            entity_type_batch_inline (Union[dict, ~google.cloud.dialogflow_v2.types.EntityTypeBatch]): The collection of entity type to update or create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.EntityTypeBatch`
            language_code (str): Optional. The language of entity synonyms defined in ``entity_types``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.FieldMask`
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
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
        operation = self._batch_update_entity_types(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            entity_type_pb2.BatchUpdateEntityTypesResponse,
            metadata_type=struct_pb2.Struct,
        )

    def batch_delete_entity_types(
            self,
            parent,
            entity_type_names,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes entity types in the specified agent.

        Operation <response: ``google.protobuf.Empty``,
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
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
            parent (str): Required. The name of the agent to delete all entities types for. Format:
                ``projects/<Project ID>/agent``.
            entity_type_names (list[str]): Required. The names entity types to delete. All names must point to the
                same agent as ``parent``.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.BatchDeleteEntityTypesRequest(
            parent=parent,
            entity_type_names=entity_type_names,
        )
        operation = self._batch_delete_entity_types(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_create_entities(self,
                              parent,
                              entities,
                              language_code=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Creates multiple new entities in the specified entity type (extends the
        existing collection of entries).

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
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
            entities (list[Union[dict, ~google.cloud.dialogflow_v2.types.Entity]]): Required. The collection of entities to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.Entity`
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.BatchCreateEntitiesRequest(
            parent=parent,
            entities=entities,
            language_code=language_code,
        )
        operation = self._batch_create_entities(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_update_entities(self,
                              parent,
                              entities,
                              language_code=None,
                              update_mask=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Updates entities in the specified entity type (replaces the existing
        collection of entries).

        Operation <response: ``google.protobuf.Empty``,
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
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
            parent (str): Required. The name of the entity type to update the entities in. Format:
                ``projects/<Project ID>/agent/entityTypes/<Entity Type ID>``.
            entities (list[Union[dict, ~google.cloud.dialogflow_v2.types.Entity]]): Required. The collection of new entities to replace the existing entities.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.Entity`
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            update_mask (Union[dict, ~google.cloud.dialogflow_v2.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2.types.FieldMask`
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.BatchUpdateEntitiesRequest(
            parent=parent,
            entities=entities,
            language_code=language_code,
            update_mask=update_mask,
        )
        operation = self._batch_update_entities(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

    def batch_delete_entities(self,
                              parent,
                              entity_values,
                              language_code=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Deletes entities in the specified entity type.

        Operation <response: ``google.protobuf.Empty``,
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>

        Example:
            >>> import dialogflow_v2
            >>>
            >>> client = dialogflow_v2.EntityTypesClient()
            >>>
            >>> parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
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
            language_code (str): Optional. The language of entity synonyms defined in ``entities``. If not
                specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = entity_type_pb2.BatchDeleteEntitiesRequest(
            parent=parent,
            entity_values=entity_values,
            language_code=language_code,
        )
        operation = self._batch_delete_entities(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )
