# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.dialogflow_v2.types import conversation
from google.cloud.dialogflow_v2.types import conversation as gcd_conversation

from .base import ConversationsTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ConversationsRestInterceptor:
    """Interceptor for Conversations.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConversationsRestTransport.

    .. code-block:: python
        class MyCustomConversationsInterceptor(ConversationsRestInterceptor):
            def pre_complete_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_complete_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_stateless_summary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_stateless_summary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conversations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_messages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_messages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_knowledge(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_knowledge(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_suggest_conversation_summary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_suggest_conversation_summary(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConversationsRestTransport(interceptor=MyCustomConversationsInterceptor())
        client = ConversationsClient(transport=transport)


    """

    def pre_complete_conversation(
        self,
        request: conversation.CompleteConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.CompleteConversationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for complete_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_complete_conversation(
        self, response: conversation.Conversation
    ) -> conversation.Conversation:
        """Post-rpc interceptor for complete_conversation

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_create_conversation(
        self,
        request: gcd_conversation.CreateConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_conversation.CreateConversationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_create_conversation(
        self, response: gcd_conversation.Conversation
    ) -> gcd_conversation.Conversation:
        """Post-rpc interceptor for create_conversation

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_generate_stateless_summary(
        self,
        request: conversation.GenerateStatelessSummaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.GenerateStatelessSummaryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_stateless_summary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_generate_stateless_summary(
        self, response: conversation.GenerateStatelessSummaryResponse
    ) -> conversation.GenerateStatelessSummaryResponse:
        """Post-rpc interceptor for generate_stateless_summary

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_get_conversation(
        self,
        request: conversation.GetConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.GetConversationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_get_conversation(
        self, response: conversation.Conversation
    ) -> conversation.Conversation:
        """Post-rpc interceptor for get_conversation

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_list_conversations(
        self,
        request: conversation.ListConversationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.ListConversationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_conversations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_list_conversations(
        self, response: conversation.ListConversationsResponse
    ) -> conversation.ListConversationsResponse:
        """Post-rpc interceptor for list_conversations

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_list_messages(
        self,
        request: conversation.ListMessagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.ListMessagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_messages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_list_messages(
        self, response: conversation.ListMessagesResponse
    ) -> conversation.ListMessagesResponse:
        """Post-rpc interceptor for list_messages

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_search_knowledge(
        self,
        request: conversation.SearchKnowledgeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversation.SearchKnowledgeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_knowledge

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_search_knowledge(
        self, response: conversation.SearchKnowledgeResponse
    ) -> conversation.SearchKnowledgeResponse:
        """Post-rpc interceptor for search_knowledge

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_suggest_conversation_summary(
        self,
        request: gcd_conversation.SuggestConversationSummaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_conversation.SuggestConversationSummaryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for suggest_conversation_summary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_suggest_conversation_summary(
        self, response: gcd_conversation.SuggestConversationSummaryResponse
    ) -> gcd_conversation.SuggestConversationSummaryResponse:
        """Post-rpc interceptor for suggest_conversation_summary

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Conversations server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Conversations server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConversationsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConversationsRestInterceptor


class ConversationsRestTransport(ConversationsTransport):
    """REST backend transport for Conversations.

    Service for managing
    [Conversations][google.cloud.dialogflow.v2.Conversation].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConversationsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ConversationsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CompleteConversation(ConversationsRestStub):
        def __hash__(self):
            return hash("CompleteConversation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.CompleteConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.Conversation:
            r"""Call the complete conversation method over HTTP.

            Args:
                request (~.conversation.CompleteConversationRequest):
                    The request object. The request message for
                [Conversations.CompleteConversation][google.cloud.dialogflow.v2.Conversations.CompleteConversation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation.Conversation:
                    Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/conversations/*}:complete",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/conversations/*}:complete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_complete_conversation(
                request, metadata
            )
            pb_request = conversation.CompleteConversationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.Conversation()
            pb_resp = conversation.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_complete_conversation(resp)
            return resp

    class _CreateConversation(ConversationsRestStub):
        def __hash__(self):
            return hash("CreateConversation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation.CreateConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_conversation.Conversation:
            r"""Call the create conversation method over HTTP.

            Args:
                request (~.gcd_conversation.CreateConversationRequest):
                    The request object. The request message for
                [Conversations.CreateConversation][google.cloud.dialogflow.v2.Conversations.CreateConversation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_conversation.Conversation:
                    Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/conversations",
                    "body": "conversation",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/conversations",
                    "body": "conversation",
                },
            ]
            request, metadata = self._interceptor.pre_create_conversation(
                request, metadata
            )
            pb_request = gcd_conversation.CreateConversationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_conversation.Conversation()
            pb_resp = gcd_conversation.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_conversation(resp)
            return resp

    class _GenerateStatelessSummary(ConversationsRestStub):
        def __hash__(self):
            return hash("GenerateStatelessSummary")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.GenerateStatelessSummaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.GenerateStatelessSummaryResponse:
            r"""Call the generate stateless
            summary method over HTTP.

                Args:
                    request (~.conversation.GenerateStatelessSummaryRequest):
                        The request object. The request message for
                    [Conversations.GenerateStatelessSummary][google.cloud.dialogflow.v2.Conversations.GenerateStatelessSummary].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.conversation.GenerateStatelessSummaryResponse:
                        The response message for
                    [Conversations.GenerateStatelessSummary][google.cloud.dialogflow.v2.Conversations.GenerateStatelessSummary].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{stateless_conversation.parent=projects/*}/suggestions:generateStatelessSummary",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{stateless_conversation.parent=projects/*/locations/*}/suggestions:generateStatelessSummary",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_stateless_summary(
                request, metadata
            )
            pb_request = conversation.GenerateStatelessSummaryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.GenerateStatelessSummaryResponse()
            pb_resp = conversation.GenerateStatelessSummaryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_stateless_summary(resp)
            return resp

    class _GetConversation(ConversationsRestStub):
        def __hash__(self):
            return hash("GetConversation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.GetConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.Conversation:
            r"""Call the get conversation method over HTTP.

            Args:
                request (~.conversation.GetConversationRequest):
                    The request object. The request message for
                [Conversations.GetConversation][google.cloud.dialogflow.v2.Conversations.GetConversation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation.Conversation:
                    Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/conversations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/conversations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_conversation(
                request, metadata
            )
            pb_request = conversation.GetConversationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.Conversation()
            pb_resp = conversation.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conversation(resp)
            return resp

    class _ListConversations(ConversationsRestStub):
        def __hash__(self):
            return hash("ListConversations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.ListConversationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.ListConversationsResponse:
            r"""Call the list conversations method over HTTP.

            Args:
                request (~.conversation.ListConversationsRequest):
                    The request object. The request message for
                [Conversations.ListConversations][google.cloud.dialogflow.v2.Conversations.ListConversations].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation.ListConversationsResponse:
                    The response message for
                [Conversations.ListConversations][google.cloud.dialogflow.v2.Conversations.ListConversations].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/conversations",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/conversations",
                },
            ]
            request, metadata = self._interceptor.pre_list_conversations(
                request, metadata
            )
            pb_request = conversation.ListConversationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.ListConversationsResponse()
            pb_resp = conversation.ListConversationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conversations(resp)
            return resp

    class _ListMessages(ConversationsRestStub):
        def __hash__(self):
            return hash("ListMessages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.ListMessagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.ListMessagesResponse:
            r"""Call the list messages method over HTTP.

            Args:
                request (~.conversation.ListMessagesRequest):
                    The request object. The request message for
                [Conversations.ListMessages][google.cloud.dialogflow.v2.Conversations.ListMessages].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation.ListMessagesResponse:
                    The response message for
                [Conversations.ListMessages][google.cloud.dialogflow.v2.Conversations.ListMessages].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/conversations/*}/messages",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/conversations/*}/messages",
                },
            ]
            request, metadata = self._interceptor.pre_list_messages(request, metadata)
            pb_request = conversation.ListMessagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.ListMessagesResponse()
            pb_resp = conversation.ListMessagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_messages(resp)
            return resp

    class _SearchKnowledge(ConversationsRestStub):
        def __hash__(self):
            return hash("SearchKnowledge")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation.SearchKnowledgeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation.SearchKnowledgeResponse:
            r"""Call the search knowledge method over HTTP.

            Args:
                request (~.conversation.SearchKnowledgeRequest):
                    The request object. The request message for
                [Conversations.SearchKnowledge][google.cloud.dialogflow.v2.Conversations.SearchKnowledge].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation.SearchKnowledgeResponse:
                    The response message for
                [Conversations.SearchKnowledge][google.cloud.dialogflow.v2.Conversations.SearchKnowledge].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/suggestions:searchKnowledge",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/suggestions:searchKnowledge",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{conversation=projects/*/conversations/*}/suggestions:searchKnowledge",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{conversation=projects/*/locations/*/conversations/*}/suggestions:searchKnowledge",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_knowledge(
                request, metadata
            )
            pb_request = conversation.SearchKnowledgeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation.SearchKnowledgeResponse()
            pb_resp = conversation.SearchKnowledgeResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_knowledge(resp)
            return resp

    class _SuggestConversationSummary(ConversationsRestStub):
        def __hash__(self):
            return hash("SuggestConversationSummary")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation.SuggestConversationSummaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_conversation.SuggestConversationSummaryResponse:
            r"""Call the suggest conversation
            summary method over HTTP.

                Args:
                    request (~.gcd_conversation.SuggestConversationSummaryRequest):
                        The request object. The request message for
                    [Conversations.SuggestConversationSummary][google.cloud.dialogflow.v2.Conversations.SuggestConversationSummary].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_conversation.SuggestConversationSummaryResponse:
                        The response message for
                    [Conversations.SuggestConversationSummary][google.cloud.dialogflow.v2.Conversations.SuggestConversationSummary].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{conversation=projects/*/conversations/*}/suggestions:suggestConversationSummary",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{conversation=projects/*/locations/*/conversations/*}/suggestions:suggestConversationSummary",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_suggest_conversation_summary(
                request, metadata
            )
            pb_request = gcd_conversation.SuggestConversationSummaryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_conversation.SuggestConversationSummaryResponse()
            pb_resp = gcd_conversation.SuggestConversationSummaryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_suggest_conversation_summary(resp)
            return resp

    @property
    def complete_conversation(
        self,
    ) -> Callable[
        [conversation.CompleteConversationRequest], conversation.Conversation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompleteConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_conversation(
        self,
    ) -> Callable[
        [gcd_conversation.CreateConversationRequest], gcd_conversation.Conversation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_stateless_summary(
        self,
    ) -> Callable[
        [conversation.GenerateStatelessSummaryRequest],
        conversation.GenerateStatelessSummaryResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateStatelessSummary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_conversation(
        self,
    ) -> Callable[[conversation.GetConversationRequest], conversation.Conversation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conversations(
        self,
    ) -> Callable[
        [conversation.ListConversationsRequest], conversation.ListConversationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConversations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_messages(
        self,
    ) -> Callable[
        [conversation.ListMessagesRequest], conversation.ListMessagesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMessages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_knowledge(
        self,
    ) -> Callable[
        [conversation.SearchKnowledgeRequest], conversation.SearchKnowledgeResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchKnowledge(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def suggest_conversation_summary(
        self,
    ) -> Callable[
        [gcd_conversation.SuggestConversationSummaryRequest],
        gcd_conversation.SuggestConversationSummaryResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SuggestConversationSummary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ConversationsRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(ConversationsRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(ConversationsRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}:cancel",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ConversationsRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(ConversationsRestStub):
        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ConversationsRestTransport",)
