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
"""Accesses the google.cloud.dialogflow.v2beta1 Sessions API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template

from dialogflow_v2beta1.gapic import enums
from dialogflow_v2beta1.gapic import sessions_client_config
from dialogflow_v2beta1.proto import agent_pb2
from dialogflow_v2beta1.proto import context_pb2
from dialogflow_v2beta1.proto import entity_type_pb2
from dialogflow_v2beta1.proto import intent_pb2
from dialogflow_v2beta1.proto import session_entity_type_pb2
from dialogflow_v2beta1.proto import session_pb2
from dialogflow_v2beta1.proto import session_pb2_grpc

from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('dialogflow',
                                                        ).version


class SessionsClient(object):
    """
    A session represents an interaction with a user. You retrieve user input
    and pass it to the ``DetectIntent`` (or
    ``StreamingDetectIntent``) method to determine
    user intent and respond.
    """

    SERVICE_ADDRESS = 'dialogflow.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.dialogflow.v2beta1.Sessions'

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

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=sessions_client_config.config,
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
        self.sessions_stub = (session_pb2_grpc.SessionsStub(channel))

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
        self._detect_intent = google.api_core.gapic_v1.method.wrap_method(
            self.sessions_stub.DetectIntent,
            default_retry=method_configs['DetectIntent'].retry,
            default_timeout=method_configs['DetectIntent'].timeout,
            client_info=client_info,
        )
        self._streaming_detect_intent = google.api_core.gapic_v1.method.wrap_method(
            self.sessions_stub.StreamingDetectIntent,
            default_retry=method_configs['StreamingDetectIntent'].retry,
            default_timeout=method_configs['StreamingDetectIntent'].timeout,
            client_info=client_info,
        )

    # Service calls
    def detect_intent(self,
                      session,
                      query_input,
                      query_params=None,
                      input_audio=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Processes a natural language query and returns structured, actionable data
        as a result. This method is not idempotent, because it may cause contexts
        and session entity types to be updated, which in turn might affect
        results of future queries.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionsClient()
            >>>
            >>> session = client.session_path('[PROJECT]', '[SESSION]')
            >>>
            >>> # TODO: Initialize ``query_input``:
            >>> query_input = {}
            >>>
            >>> response = client.detect_intent(session, query_input)

        Args:
            session (str): Required. The name of the session this query is sent to. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>``, or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User
                ID>/sessions/<Session ID>``. Note: Environments and users are under
                construction and will be available soon. If <Environment ID> is not
                specified, we assume default 'draft' environment. If <User ID> is not
                specified, we are using \"-\". It’s up to the API caller to choose an
                appropriate <Session ID>. and <User Id>. They can be a random numbers or
                some type of user and session identifiers (preferably hashed). The length
                of the <Session ID> and <User ID> must not exceed 36 characters.
            query_input (Union[dict, ~dialogflow_v2beta1.types.QueryInput]): Required. The input specification. It can be set to:

                1.  an audio config
                ::

                    which instructs the speech recognizer how to process the speech audio,

                2.  a conversational query in the form of text, or

                3.  an event that specifies which intent to trigger.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.QueryInput`
            query_params (Union[dict, ~dialogflow_v2beta1.types.QueryParameters]): Optional. The parameters of this query.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~dialogflow_v2beta1.types.QueryParameters`
            input_audio (bytes): Optional. The natural language speech audio to be processed. This field
                should be populated iff ``query_input`` is set to an input audio config.
                A single request can contain up to 1 minute of speech audio data.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~dialogflow_v2beta1.types.DetectIntentResponse` instance.

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
        request = session_pb2.DetectIntentRequest(
            session=session,
            query_input=query_input,
            query_params=query_params,
            input_audio=input_audio,
        )
        return self._detect_intent(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def streaming_detect_intent(
            self,
            requests,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Processes a natural language query in audio format in a streaming fashion
        and returns structured, actionable data as a result. This method is only
        available via the gRPC API (not REST).

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> import dialogflow_v2beta1
            >>>
            >>> client = dialogflow_v2beta1.SessionsClient()
            >>>
            >>> # TODO: Initialize ``session``:
            >>> session = ''
            >>>
            >>> # TODO: Initialize ``query_input``:
            >>> query_input = {}
            >>> request = {'session': session, 'query_input': query_input}
            >>>
            >>> requests = [request]
            >>> for element in client.streaming_detect_intent(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|dialogflow_v2beta1.proto.session_pb2.StreamingDetectIntentRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~dialogflow_v2beta1.types.StreamingDetectIntentRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~dialogflow_v2beta1.types.StreamingDetectIntentResponse].

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
        return self._streaming_detect_intent(
            requests, retry=retry, timeout=timeout, metadata=metadata)
