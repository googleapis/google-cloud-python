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
"""Accesses the google.cloud.dialogflow.v2beta1 SessionEntityTypes API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic import session_entity_types_client_config
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import entity_type_pb2
from dialogflow_v2beta1.proto import intent_pb2
from dialogflow_v2beta1.proto import session_entity_type_pb2
from dialogflow_v2beta1.proto import session_entity_type_pb2_grpc

from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow',
                                                        ).version


class SessionEntityTypesClient(object):
    """
    Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    Session entity types are referred to as **User** entity types and are
    entities that are built for an individual user such as
    favorites, preferences, playlists, and so on. You can redefine a session
    entity type at the session level.

    For more information about entity types, see the
    `Dialogflow documentation <https://dialogflow.com/docs/entities>`__.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.SessionEntityTypes'

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
    def session_entity_type_path(cls, project, session, entity_type):
        """Return a fully-qualified session_entity_type string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}',
            project=project,
            session=session,
            entity_type=entity_type,
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

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=session_entity_types_client_config.config,
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
        self.session_entity_types_stub = (
            session_entity_type_pb2_grpc.SessionEntityTypesStub(channel))

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
        self._list_session_entity_types = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.ListSessionEntityTypes,
            default_retry=method_configs['ListSessionEntityTypes'].retry,
            default_timeout=method_configs['ListSessionEntityTypes'].timeout,
            client_info=client_info,
        )
        self._get_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.GetSessionEntityType,
            default_retry=method_configs['GetSessionEntityType'].retry,
            default_timeout=method_configs['GetSessionEntityType'].timeout,
            client_info=client_info,
        )
        self._create_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.CreateSessionEntityType,
            default_retry=method_configs['CreateSessionEntityType'].retry,
            default_timeout=method_configs['CreateSessionEntityType'].timeout,
            client_info=client_info,
        )
        self._update_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.UpdateSessionEntityType,
            default_retry=method_configs['UpdateSessionEntityType'].retry,
            default_timeout=method_configs['UpdateSessionEntityType'].timeout,
            client_info=client_info,
        )
        self._delete_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.DeleteSessionEntityType,
            default_retry=method_configs['DeleteSessionEntityType'].retry,
            default_timeout=method_configs['DeleteSessionEntityType'].timeout,
            client_info=client_info,
        )

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
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_session_entity_types(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_session_entity_types(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The session to list all session entity types from.
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/
                sessions/<Session ID>``.
                Note: Environments and users are under construction and will be available
                soon. If <Environment ID> is not specified, we assume default 'draft'
                environment. If <User ID> is not specified, we assume default '-' user.
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
            is an iterable of :class:`~dialogflow_v2beta1.types.SessionEntityType` instances.
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
        request = session_entity_type_pb2.ListSessionEntityTypesRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_session_entity_types,
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
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type
                Display Name>`` or ``projects/<Project ID>/agent/environments/<Environment
                ID>/users/<User ID>/sessions/<Session ID>/
                entityTypes/<Entity Type Display Name>``.
                Note: Environments and users re under construction and will be available
                soon. If <Environment ID> is not specified, we assume default 'draft'
                environment. If <User ID> is not specified, we assume default '-' user.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

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
        request = session_entity_type_pb2.GetSessionEntityTypeRequest(
            name=name, )
        return self._get_session_entity_type(
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

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> # TODO: Initialize ``session_entity_type``:
            >>> session_entity_type = {}
            >>>
            >>> response = client.create_session_entity_type(parent, session_entity_type)

        Args:
            parent (str): Required. The session to create a session entity type for.
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/
                sessions/<Session ID>``.
                Note: Environments and users are under construction and will be available
                soon. If <Environment ID> is not specified, we assume default 'draft'
                environment. If <User ID> is not specified, we assume default '-' user.
            session_entity_type (Union[dict, ~dialogflow_v2beta1.types.SessionEntityType]): Required. The session entity type to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.SessionEntityType`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

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
        request = session_entity_type_pb2.CreateSessionEntityTypeRequest(
            parent=parent,
            session_entity_type=session_entity_type,
        )
        return self._create_session_entity_type(
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
            >>> # TODO: Initialize ``session_entity_type``:
            >>> session_entity_type = {}
            >>>
            >>> response = client.update_session_entity_type(session_entity_type)

        Args:
            session_entity_type (Union[dict, ~dialogflow_v2beta1.types.SessionEntityType]): Required. The entity type to update. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type
                Display Name>`` or ``projects/<Project ID>/agent/environments/<Environment
                ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display
                Name>``.
                Note: Environments and users are under construction and will be available
                soon. If <Environment ID> is not specified, we assume default 'draft'
                environment. If <User ID> is not specified, we assume default '-' user.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.SessionEntityType`
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
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

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
        request = session_entity_type_pb2.UpdateSessionEntityTypeRequest(
            session_entity_type=session_entity_type,
            update_mask=update_mask,
        )
        return self._update_session_entity_type(
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
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type
                Display Name>`` or ``projects/<Project ID>/agent/environments/<Environment
                ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display
                Name>``.
                Note: Environments and users are under construction and will be available
                soon. If <Environment ID> is not specified, we assume default 'draft'
                environment. If <User ID> is not specified, we assume default '-' user.
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
        request = session_entity_type_pb2.DeleteSessionEntityTypeRequest(
            name=name, )
        self._delete_session_entity_type(
            request, retry=retry, timeout=timeout, metadata=metadata)
