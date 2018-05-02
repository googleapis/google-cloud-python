# -*- coding: utf8 -*-
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
"""Accesses the google.cloud.dialogflow.v2beta1 Intents API."""

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

from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic import intents_client_config
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import entity_type_pb2
from dialogflow_v2beta1.proto import intent_pb2
from dialogflow_v2beta1.proto import intent_pb2_grpc

from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow',
                                                        ).version


class IntentsClient(object):
    """
    An intent represents a mapping between input from a user and an action to
    be taken by your application. When you pass user input to the
    ``DetectIntent`` (or
    ``StreamingDetectIntent``) method, the
    Dialogflow API analyzes the input and searches
    for a matching intent. If no match is found, the Dialogflow API returns a
    fallback intent (``is_fallback`` = true).

    You can provide additional information for the Dialogflow API to use to
    match user input to an intent by adding the following to your intent.

    *   **Contexts** - provide additional context for intent analysis. For
        example, if an intent is related to an object in your application that
        plays music, you can provide a context to determine when to match the
        intent if the user input is “turn it off”.  You can include a context
        that matches the intent when there is previous user input of
        \"play music\", and not when there is previous user input of
        \"turn on the light\".
    *   **Events** - allow for matching an intent by using an event name
        instead of user input. Your application can provide an event name and
        related parameters to the Dialogflow API to match an intent. For
        example, when your application starts, you can send a welcome event
        with a user name parameter to the Dialogflow API to match an intent with
        a personalized welcome message for the user.
    *   **Training phrases** - provide examples of user input to train the
        Dialogflow API agent to better match intents.

    For more information about intents, see the
    `Dialogflow documentation <https://dialogflow.com/docs/intents>`__.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.Intents'

    @classmethod
    def project_agent_path(cls, project):
        """Return a fully-qualified project_agent string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent',
            project=project,
        )

    @classmethod
    def intent_path(cls, project, intent):
        """Return a fully-qualified intent string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/intents/{intent}',
            project=project,
            intent=intent,
        )

    @classmethod
    def agent_path(cls, project, agent):
        """Return a fully-qualified agent string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agents/{agent}',
            project=project,
            agent=agent,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=intents_client_config.config,
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
        self.intents_stub = (intent_pb2_grpc.IntentsStub(channel))

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
        self._list_intents = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.ListIntents,
            default_retry=method_configs['ListIntents'].retry,
            default_timeout=method_configs['ListIntents'].timeout,
            client_info=client_info,
        )
        self._get_intent = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.GetIntent,
            default_retry=method_configs['GetIntent'].retry,
            default_timeout=method_configs['GetIntent'].timeout,
            client_info=client_info,
        )
        self._create_intent = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.CreateIntent,
            default_retry=method_configs['CreateIntent'].retry,
            default_timeout=method_configs['CreateIntent'].timeout,
            client_info=client_info,
        )
        self._update_intent = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.UpdateIntent,
            default_retry=method_configs['UpdateIntent'].retry,
            default_timeout=method_configs['UpdateIntent'].timeout,
            client_info=client_info,
        )
        self._delete_intent = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.DeleteIntent,
            default_retry=method_configs['DeleteIntent'].retry,
            default_timeout=method_configs['DeleteIntent'].timeout,
            client_info=client_info,
        )
        self._batch_update_intents = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.BatchUpdateIntents,
            default_retry=method_configs['BatchUpdateIntents'].retry,
            default_timeout=method_configs['BatchUpdateIntents'].timeout,
            client_info=client_info,
        )
        self._batch_delete_intents = google.api_core.gapic_v1.method.wrap_method(
            self.intents_stub.BatchDeleteIntents,
            default_retry=method_configs['BatchDeleteIntents'].retry,
            default_timeout=method_configs['BatchDeleteIntents'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_intents(self,
                     parent,
                     language_code=None,
                     intent_view=None,
                     page_size=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Returns the list of all intents in the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_intents(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_intents(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The agent to list all intents from.
                Format: ``projects/<Project ID>/agent``.
            language_code (str): Optional. The language to list training phrases, parameters and rich
                messages for. If not specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent before they can be used.
            intent_view (~dialogflow_v2beta1.types.IntentView): Optional. The resource view to apply to the returned intent.
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
            is an iterable of :class:`~dialogflow_v2beta1.types.Intent` instances.
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
        request = intent_pb2.ListIntentsRequest(
            parent=parent,
            language_code=language_code,
            intent_view=intent_view,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_intents,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='intents',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_intent(self,
                   name,
                   language_code=None,
                   intent_view=None,
                   retry=google.api_core.gapic_v1.method.DEFAULT,
                   timeout=google.api_core.gapic_v1.method.DEFAULT,
                   metadata=None):
        """
        Retrieves the specified intent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> name = client.intent_path('[PROJECT]', '[INTENT]')
            >>>
            >>> response = client.get_intent(name)

        Args:
            name (str): Required. The name of the intent.
                Format: ``projects/<Project ID>/agent/intents/<Intent ID>``.
            language_code (str): Optional. The language to retrieve training phrases, parameters and rich
                messages for. If not specified, the agent's default language is used.
                [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            intent_view (~dialogflow_v2beta1.types.IntentView): Optional. The resource view to apply to the returned intent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Intent` instance.

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
        request = intent_pb2.GetIntentRequest(
            name=name,
            language_code=language_code,
            intent_view=intent_view,
        )
        return self._get_intent(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_intent(self,
                      parent,
                      intent,
                      language_code=None,
                      intent_view=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Creates an intent in the specified agent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> parent = client.project_agent_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize ``intent``:
            >>> intent = {}
            >>>
            >>> response = client.create_intent(parent, intent)

        Args:
            parent (str): Required. The agent to create a intent for.
                Format: ``projects/<Project ID>/agent``.
            intent (Union[dict, ~dialogflow_v2beta1.types.Intent]): Required. The intent to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.Intent`
            language_code (str): Optional. The language of training phrases, parameters and rich messages
                defined in ``intent``. If not specified, the agent's default language is
                used. [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            intent_view (~dialogflow_v2beta1.types.IntentView): Optional. The resource view to apply to the returned intent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Intent` instance.

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
        request = intent_pb2.CreateIntentRequest(
            parent=parent,
            intent=intent,
            language_code=language_code,
            intent_view=intent_view,
        )
        return self._create_intent(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_intent(self,
                      intent,
                      language_code,
                      update_mask=None,
                      intent_view=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Updates the specified intent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> # TODO: Initialize ``intent``:
            >>> intent = {}
            >>>
            >>> # TODO: Initialize ``language_code``:
            >>> language_code = ''
            >>>
            >>> response = client.update_intent(intent, language_code)

        Args:
            intent (Union[dict, ~dialogflow_v2beta1.types.Intent]): Required. The intent to update.
                Format: ``projects/<Project ID>/agent/intents/<Intent ID>``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.Intent`
            language_code (str): Optional. The language of training phrases, parameters and rich messages
                defined in ``intent``. If not specified, the agent's default language is
                used. [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            update_mask (Union[dict, ~dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.FieldMask`
            intent_view (~dialogflow_v2beta1.types.IntentView): Optional. The resource view to apply to the returned intent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Intent` instance.

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
        request = intent_pb2.UpdateIntentRequest(
            intent=intent,
            language_code=language_code,
            update_mask=update_mask,
            intent_view=intent_view,
        )
        return self._update_intent(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_intent(self,
                      name,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Deletes the specified intent.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> name = client.intent_path('[PROJECT]', '[INTENT]')
            >>>
            >>> client.delete_intent(name)

        Args:
            name (str): Required. The name of the intent to delete.
                Format: ``projects/<Project ID>/agent/intents/<Intent ID>``.
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
        request = intent_pb2.DeleteIntentRequest(name=name, )
        self._delete_intent(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def batch_update_intents(self,
                             parent,
                             language_code,
                             intent_batch_uri=None,
                             intent_batch_inline=None,
                             update_mask=None,
                             intent_view=None,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Updates/Creates multiple intents in the specified agent.

        Operation <response: ``BatchUpdateIntentsResponse``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> parent = client.agent_path('[PROJECT]', '[AGENT]')
            >>>
            >>> # TODO: Initialize ``language_code``:
            >>> language_code = ''
            >>>
            >>> response = client.batch_update_intents(parent, language_code)
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
            parent (str): Required. The name of the agent to update or create intents in.
                Format: ``projects/<Project ID>/agent``.
            language_code (str): Optional. The language of training phrases, parameters and rich messages
                defined in ``intents``. If not specified, the agent's default language is
                used. [More than a dozen
                languages](https://dialogflow.com/docs/reference/language) are supported.
                Note: languages must be enabled in the agent, before they can be used.
            intent_batch_uri (str): The URI to a Google Cloud Storage file containing intents to update or
                create. The file format can either be a serialized proto (of IntentBatch
                type) or JSON object. Note: The URI must start with \"gs://\".
            intent_batch_inline (Union[dict, ~dialogflow_v2beta1.types.IntentBatch]): The collection of intents to update or create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.IntentBatch`
            update_mask (Union[dict, ~dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.FieldMask`
            intent_view (~dialogflow_v2beta1.types.IntentView): Optional. The resource view to apply to the returned intent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

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
            intent_batch_uri=intent_batch_uri,
            intent_batch_inline=intent_batch_inline,
        )

        request = intent_pb2.BatchUpdateIntentsRequest(
            parent=parent,
            language_code=language_code,
            intent_batch_uri=intent_batch_uri,
            intent_batch_inline=intent_batch_inline,
            update_mask=update_mask,
            intent_view=intent_view,
        )
        operation = self._batch_update_intents(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            intent_pb2.BatchUpdateIntentsResponse,
            metadata_type=struct_pb2.Struct,
        )

    def batch_delete_intents(self,
                             parent,
                             intents,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Deletes intents in the specified agent.

        Operation <response: ``google.protobuf.Empty``>

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.IntentsClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize ``intents``:
            >>> intents = []
            >>>
            >>> response = client.batch_delete_intents(parent, intents)
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
            intents (list[Union[dict, ~dialogflow_v2beta1.types.Intent]]): Required. The collection of intents to delete. Only intent ``name`` must be
                filled in.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.Intent`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types._OperationFuture` instance.

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
        request = intent_pb2.BatchDeleteIntentsRequest(
            parent=parent,
            intents=intents,
        )
        operation = self._batch_delete_intents(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )
