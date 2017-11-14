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
# https://github.com/google/googleapis/blob/master/google/cloud/dialogflow/v2beta1/session_entity_type.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
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
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow').version


class SessionEntityTypesClient(object):
    """
    Manages session entity types.

    Session entity types can be redefined on a session level, allowing for
    specific concepts, like a user's playlists.


    Standard methods.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.cloud.dialogflow.v2beta1.SessionEntityTypes')

    @classmethod
    def session_path(cls, project, session):
        """Returns a fully-qualified session resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}',
            project=project,
            session=session, )

    @classmethod
    def session_entity_type_path(cls, project, session, entity_type):
        """Returns a fully-qualified session_entity_type resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}',
            project=project,
            session=session,
            entity_type=entity_type, )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=session_entity_types_client_config.config,
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

        self.session_entity_types_stub = (
            session_entity_type_pb2.SessionEntityTypesStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._list_session_entity_types = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.ListSessionEntityTypes,
            default_retry=method_configs['ListSessionEntityTypes'].retry,
            default_timeout=method_configs['ListSessionEntityTypes'].timeout,
            client_info=client_info)
        self._get_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.GetSessionEntityType,
            default_retry=method_configs['GetSessionEntityType'].retry,
            default_timeout=method_configs['GetSessionEntityType'].timeout,
            client_info=client_info)
        self._create_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.CreateSessionEntityType,
            default_retry=method_configs['CreateSessionEntityType'].retry,
            default_timeout=method_configs['CreateSessionEntityType'].timeout,
            client_info=client_info)
        self._update_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.UpdateSessionEntityType,
            default_retry=method_configs['UpdateSessionEntityType'].retry,
            default_timeout=method_configs['UpdateSessionEntityType'].timeout,
            client_info=client_info)
        self._delete_session_entity_type = google.api_core.gapic_v1.method.wrap_method(
            self.session_entity_types_stub.DeleteSessionEntityType,
            default_retry=method_configs['DeleteSessionEntityType'].retry,
            default_timeout=method_configs['DeleteSessionEntityType'].timeout,
            client_info=client_info)

    # Service calls
    def list_session_entity_types(
            self,
            parent,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
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
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>``.
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
        request = session_entity_type_pb2.ListSessionEntityTypesRequest(
            parent=parent, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_session_entity_types, retry=retry, timeout=timeout),
            request=request,
            items_field='session_entity_types',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def get_session_entity_type(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
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
                Display Name>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = session_entity_type_pb2.GetSessionEntityTypeRequest(
            name=name)
        return self._get_session_entity_type(
            request, retry=retry, timeout=timeout)

    def create_session_entity_type(
            self,
            parent,
            session_entity_type,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> parent = client.session_path('[PROJECT]', '[SESSION]')
            >>> session_entity_type = {}
            >>>
            >>> response = client.create_session_entity_type(parent, session_entity_type)

        Args:
            parent (str): Required. The session to create a session entity type for.
                Format: ``projects/<Project ID>/agent/sessions/<Session ID>``.
            session_entity_type (Union[dict, ~dialogflow_v2beta1.types.SessionEntityType]): Required. The session entity type to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.SessionEntityType`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = session_entity_type_pb2.CreateSessionEntityTypeRequest(
            parent=parent, session_entity_type=session_entity_type)
        return self._create_session_entity_type(
            request, retry=retry, timeout=timeout)

    def update_session_entity_type(
            self,
            session_entity_type,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates the specified session entity type.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionEntityTypesClient()
            >>>
            >>> session_entity_type = {}
            >>>
            >>> response = client.update_session_entity_type(session_entity_type)

        Args:
            session_entity_type (Union[dict, ~dialogflow_v2beta1.types.SessionEntityType]): Required. The entity type to update. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type
                Display Name>``.
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

        Returns:
            A :class:`~dialogflow_v2beta1.types.SessionEntityType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = session_entity_type_pb2.UpdateSessionEntityTypeRequest(
            session_entity_type=session_entity_type, update_mask=update_mask)
        return self._update_session_entity_type(
            request, retry=retry, timeout=timeout)

    def delete_session_entity_type(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
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
                Display Name>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = session_entity_type_pb2.DeleteSessionEntityTypeRequest(
            name=name)
        self._delete_session_entity_type(request, retry=retry, timeout=timeout)
