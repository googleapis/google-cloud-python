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
"""Accesses the google.cloud.dialogflow.v2beta1 Contexts API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from dialogflow_v2beta1.gapic import contexts_client_config
from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import context_pb2_grpc

from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow',
                                                        ).version


class ContextsClient(object):
    """
    A context represents additional information included with user input or with
    an intent returned by the Dialogflow API. Contexts are helpful for
    differentiating user input which may be vague or have a different meaning
    depending on additional details from your application such as user setting
    and preferences, previous user input, where the user is in your application,
    geographic location, and so on.

    You can include contexts as input parameters of a
    ``DetectIntent`` (or
    ``StreamingDetectIntent``) request,
    or as output contexts included in the returned intent.
    Contexts expire when an intent is matched, after the number of ``DetectIntent``
    requests specified by the ``lifespan_count`` parameter, or after 10 minutes
    if no intents are matched for a ``DetectIntent`` request.

    For more information about contexts, see the
    `Dialogflow documentation <https://dialogflow.com/docs/contexts>`__.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.Contexts'

    @classmethod
    def session_path(cls, project, session):
        """Return a fully-qualified session string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}',
            project=project,
            session=session,
        )

    @classmethod
    def environment_session_path(cls, project, environment, user, session):
        """Return a fully-qualified environment_session string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/environments/{environment}/users/{user}/sessions/{session}',
            project=project,
            environment=environment,
            user=user,
            session=session,
        )

    @classmethod
    def context_path(cls, project, session, context):
        """Return a fully-qualified context string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}/contexts/{context}',
            project=project,
            session=session,
            context=context,
        )

    @classmethod
    def environment_context_path(cls, project, environment, user, session,
                                 context):
        """Return a fully-qualified environment_context string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/environments/{environment}/users/{user}/sessions/{session}/contexts/{context}',
            project=project,
            environment=environment,
            user=user,
            session=session,
            context=context,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=contexts_client_config.config,
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
        self.contexts_stub = (context_pb2_grpc.ContextsStub(channel))

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
        self._list_contexts = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.ListContexts,
            default_retry=method_configs['ListContexts'].retry,
            default_timeout=method_configs['ListContexts'].timeout,
            client_info=client_info,
        )
        self._get_context = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.GetContext,
            default_retry=method_configs['GetContext'].retry,
            default_timeout=method_configs['GetContext'].timeout,
            client_info=client_info,
        )
        self._create_context = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.CreateContext,
            default_retry=method_configs['CreateContext'].retry,
            default_timeout=method_configs['CreateContext'].timeout,
            client_info=client_info,
        )
        self._update_context = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.UpdateContext,
            default_retry=method_configs['UpdateContext'].retry,
            default_timeout=method_configs['UpdateContext'].timeout,
            client_info=client_info,
        )
        self._delete_context = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.DeleteContext,
            default_retry=method_configs['DeleteContext'].retry,
            default_timeout=method_configs['DeleteContext'].timeout,
            client_info=client_info,
        )
        self._delete_all_contexts = google.api_core.gapic_v1.method.wrap_method(
            self.contexts_stub.DeleteAllContexts,
            default_retry=method_configs['DeleteAllContexts'].retry,
            default_timeout=method_configs['DeleteAllContexts'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_contexts(self,
                      parent,
                      page_size=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Returns the list of all contexts in the specified session.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_contexts(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_contexts(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The session to list all contexts from.
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User
                ID>/sessions/<Session ID>``. Note: Environments and users are under
                construction and will be available soon. If <Environment ID> is not
                specified, we assume default 'draft' environment. If <User ID> is not
                specified, we assume default '-' user.
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
            is an iterable of :class:`~dialogflow_v2beta1.types.Context` instances.
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
        request = context_pb2.ListContextsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_contexts,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='contexts',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_context(self,
                    name,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Retrieves the specified context.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')
            >>>
            >>> response = client.get_context(name)

        Args:
            name (str): Required. The name of the context. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/contexts/<Context ID>``
                or ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User
                ID>/sessions/<Session ID>/contexts/<Context ID>``. Note: Environments and
                users are under construction and will be available soon. If <Environment
                ID> is not specified, we assume default 'draft' environment. If <User ID>
                is not specified, we assume default '-' user.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Context` instance.

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
        request = context_pb2.GetContextRequest(name=name, )
        return self._get_context(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_context(self,
                       parent,
                       context,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Creates a context.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> # TODO: Initialize ``context``:
            >>> context = {}
            >>>
            >>> response = client.create_context(parent, context)

        Args:
            parent (str): Required. The session to create a context for.
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User
                ID>/sessions/<Session ID>``. Note: Environments and users are under
                construction and will be available soon. If <Environment ID> is not
                specified, we assume default 'draft' environment. If <User ID> is not
                specified, we assume default '-' user.
            context (Union[dict, ~dialogflow_v2beta1.types.Context]): Required. The context to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.Context`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Context` instance.

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
        request = context_pb2.CreateContextRequest(
            parent=parent,
            context=context,
        )
        return self._create_context(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_context(self,
                       context,
                       update_mask=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Updates the specified context.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> # TODO: Initialize ``context``:
            >>> context = {}
            >>>
            >>> response = client.update_context(context)

        Args:
            context (Union[dict, ~dialogflow_v2beta1.types.Context]): Required. The context to update.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.Context`
            update_mask (Union[dict, ~dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.Context` instance.

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
        request = context_pb2.UpdateContextRequest(
            context=context,
            update_mask=update_mask,
        )
        return self._update_context(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_context(self,
                       name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Deletes the specified context.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')
            >>>
            >>> client.delete_context(name)

        Args:
            name (str): Required. The name of the context to delete. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/contexts/<Context ID>``
                or ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User
                ID>/sessions/<Session ID>/contexts/<Context ID>``. Note: Environments and
                users are under construction and will be available soon. If <Environment
                ID> is not specified, we assume default 'draft' environment. If <User ID>
                is not specified, we assume default
                '-' user.
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
        request = context_pb2.DeleteContextRequest(name=name, )
        self._delete_context(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_all_contexts(self,
                            parent,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT,
                            metadata=None):
        """
        Deletes all active contexts in the specified session.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.ContextsClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> client.delete_all_contexts(parent)

        Args:
            parent (str): Required. The name of the session to delete all contexts from. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>`` or ``projects/<Project
                ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session
                ID>``. Note: Environments and users are under construction and will be
                available soon. If <Environment ID> is not specified we assume default
                'draft' environment. If <User ID> is not specified, we assume default
                '-' user.
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
        request = context_pb2.DeleteAllContextsRequest(parent=parent, )
        self._delete_all_contexts(
            request, retry=retry, timeout=timeout, metadata=metadata)
