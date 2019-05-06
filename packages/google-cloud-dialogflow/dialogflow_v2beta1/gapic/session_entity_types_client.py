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
"""Accesses the google.cloud.dialogflow.v2beta1 SessionEntityTypes API."""

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
from dialogflow_v2beta1.gapic import session_entity_types_client_config
from dialogflow_v2beta1.gapic.transports import session_entity_types_grpc_transport
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
from dialogflow_v2beta1.proto import session_entity_type_pb2
from dialogflow_v2beta1.proto import session_entity_type_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'dialogflow', ).version


class SessionEntityTypesClient(object):
    """
    Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    Session entity types are referred to as **User** entity types and are
    entities that are built for an individual user such as favorites,
    preferences, playlists, and so on. You can redefine a session entity
    type at the session level.

    For more information about entity types, see the `Dialogflow
    documentation <https://cloud.google.com/dialogflow-enterprise/docs/entities-overview>`__.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.SessionEntityTypes'

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
            dialogflow_v2beta1.SessionEntityTypesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
    def environment_session_entity_type_path(cls, project, environment, user,
                                             session, entity_type):
        """Return a fully-qualified environment_session_entity_type string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/environments/{environment}/users/{user}/sessions/{session}/entityTypes/{entity_type}',
            project=project,
            environment=environment,
            user=user,
            session=session,
            entity_type=entity_type,
        )

    @classmethod
    def session_path(cls, project, session):
        """Return a fully-qualified session string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}',
            project=project,
            session=session,
        )

    @classmethod
    def session_entity_type_path(cls, project, session, entity_type):
        """Return a fully-qualified session_entity_type string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}',
            project=project,
            session=session,
            entity_type=entity_type,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=None,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.SessionEntityTypesGrpcTransport,
                    Callable[[~.Credentials, type], ~.SessionEntityTypesGrpcTransport]): A transport
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
            client_config = session_entity_types_client_config.config

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
                    default_class=session_entity_types_grpc_transport.
                    SessionEntityTypesGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = session_entity_types_grpc_transport.SessionEntityTypesGrpcTransport(
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
    def list_session_entity_types(
            self,
            parent,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the list of all session entity types in the specified session.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_session_entity_types(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_session_entity_types(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The session to list all session entity types from. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/ sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. If ``User ID`` is not specified, we assume default '-'
                user.
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
            is an iterable of :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType` instances.
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
        if 'list_session_entity_types' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_session_entity_types'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_session_entity_types,
                    default_retry=self.
                    _method_configs['ListSessionEntityTypes'].retry,
                    default_timeout=self.
                    _method_configs['ListSessionEntityTypes'].timeout,
                    client_info=self._client_info,
                )

        request = session_entity_type_pb2.ListSessionEntityTypesRequest(
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
                self._inner_api_calls['list_session_entity_types'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='session_entity_types',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_session_entity_type(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Retrieves the specified session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> name = client.session_entity_type_path('[PROJECT]', '[SESSION]', '[ENTITY_TYPE]')
            >>>
            >>> response = client.get_session_entity_type(name)

        Args:
            name (str): Required. The name of the session entity type. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. If ``User ID`` is not specified, we assume default '-'
                user.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_session_entity_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_session_entity_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_session_entity_type,
                    default_retry=self._method_configs['GetSessionEntityType'].
                    retry,
                    default_timeout=self.
                    _method_configs['GetSessionEntityType'].timeout,
                    client_info=self._client_info,
                )

        request = session_entity_type_pb2.GetSessionEntityTypeRequest(
            name=name, )
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

        return self._inner_api_calls['get_session_entity_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_session_entity_type(
            self,
            parent,
            session_entity_type,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates a session entity type.

        If the specified session entity type already exists, overrides the
        session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> # TODO: Initialize `session_entity_type`:
            >>> session_entity_type = {}
            >>>
            >>> response = client.create_session_entity_type(parent, session_entity_type)

        Args:
            parent (str): Required. The session to create a session entity type for. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/ sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. If ``User ID`` is not specified, we assume default '-'
                user.
            session_entity_type (Union[dict, ~google.cloud.dialogflow_v2beta1.types.SessionEntityType]): Required. The session entity type to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_session_entity_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_session_entity_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_session_entity_type,
                    default_retry=self.
                    _method_configs['CreateSessionEntityType'].retry,
                    default_timeout=self.
                    _method_configs['CreateSessionEntityType'].timeout,
                    client_info=self._client_info,
                )

        request = session_entity_type_pb2.CreateSessionEntityTypeRequest(
            parent=parent,
            session_entity_type=session_entity_type,
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

        return self._inner_api_calls['create_session_entity_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_session_entity_type(
            self,
            session_entity_type,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates the specified session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> # TODO: Initialize `session_entity_type`:
            >>> session_entity_type = {}
            >>>
            >>> response = client.update_session_entity_type(session_entity_type)

        Args:
            session_entity_type (Union[dict, ~google.cloud.dialogflow_v2beta1.types.SessionEntityType]): Required. The entity type to update. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. If ``User ID`` is not specified, we assume default '-'
                user.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType`
            update_mask (Union[dict, ~google.cloud.dialogflow_v2beta1.types.FieldMask]): Optional. The mask to control which fields get updated.

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
            A :class:`~google.cloud.dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_session_entity_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_session_entity_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_session_entity_type,
                    default_retry=self.
                    _method_configs['UpdateSessionEntityType'].retry,
                    default_timeout=self.
                    _method_configs['UpdateSessionEntityType'].timeout,
                    client_info=self._client_info,
                )

        request = session_entity_type_pb2.UpdateSessionEntityTypeRequest(
            session_entity_type=session_entity_type,
            update_mask=update_mask,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('session_entity_type.name',
                               session_entity_type.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['update_session_entity_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_session_entity_type(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes the specified session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> name = client.session_entity_type_path('[PROJECT]', '[SESSION]', '[ENTITY_TYPE]')
            >>>
            >>> client.delete_session_entity_type(name)

        Args:
            name (str): Required. The name of the entity type to delete. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. If ``User ID`` is not specified, we assume default '-'
                user.
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
        if 'delete_session_entity_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_session_entity_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_session_entity_type,
                    default_retry=self.
                    _method_configs['DeleteSessionEntityType'].retry,
                    default_timeout=self.
                    _method_configs['DeleteSessionEntityType'].timeout,
                    client_info=self._client_info,
                )

        request = session_entity_type_pb2.DeleteSessionEntityTypeRequest(
            name=name, )
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

        self._inner_api_calls['delete_session_entity_type'](request,
                                                            retry=retry,
                                                            timeout=timeout,
                                                            metadata=metadata)
