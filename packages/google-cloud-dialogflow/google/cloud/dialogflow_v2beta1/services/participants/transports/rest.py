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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflow_v2beta1.types import participant as gcd_participant
from google.cloud.dialogflow_v2beta1.types import participant

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseParticipantsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ParticipantsRestInterceptor:
    """Interceptor for Participants.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ParticipantsRestTransport.

    .. code-block:: python
        class MyCustomParticipantsInterceptor(ParticipantsRestInterceptor):
            def pre_analyze_content(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_content(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_compile_suggestion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compile_suggestion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_participant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_participant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_participant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_participant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_participants(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_participants(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_suggestions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_suggestions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_suggest_articles(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_suggest_articles(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_suggest_faq_answers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_suggest_faq_answers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_suggest_knowledge_assist(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_suggest_knowledge_assist(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_suggest_smart_replies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_suggest_smart_replies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_participant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_participant(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ParticipantsRestTransport(interceptor=MyCustomParticipantsInterceptor())
        client = ParticipantsClient(transport=transport)


    """

    def pre_analyze_content(
        self,
        request: gcd_participant.AnalyzeContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_participant.AnalyzeContentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_content

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_analyze_content(
        self, response: gcd_participant.AnalyzeContentResponse
    ) -> gcd_participant.AnalyzeContentResponse:
        """Post-rpc interceptor for analyze_content

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_compile_suggestion(
        self,
        request: participant.CompileSuggestionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.CompileSuggestionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for compile_suggestion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_compile_suggestion(
        self, response: participant.CompileSuggestionResponse
    ) -> participant.CompileSuggestionResponse:
        """Post-rpc interceptor for compile_suggestion

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_create_participant(
        self,
        request: gcd_participant.CreateParticipantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_participant.CreateParticipantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_participant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_create_participant(
        self, response: gcd_participant.Participant
    ) -> gcd_participant.Participant:
        """Post-rpc interceptor for create_participant

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_get_participant(
        self,
        request: participant.GetParticipantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.GetParticipantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_participant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_get_participant(
        self, response: participant.Participant
    ) -> participant.Participant:
        """Post-rpc interceptor for get_participant

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_list_participants(
        self,
        request: participant.ListParticipantsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.ListParticipantsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_participants

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_list_participants(
        self, response: participant.ListParticipantsResponse
    ) -> participant.ListParticipantsResponse:
        """Post-rpc interceptor for list_participants

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_list_suggestions(
        self,
        request: participant.ListSuggestionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.ListSuggestionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_suggestions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_list_suggestions(
        self, response: participant.ListSuggestionsResponse
    ) -> participant.ListSuggestionsResponse:
        """Post-rpc interceptor for list_suggestions

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_suggest_articles(
        self,
        request: participant.SuggestArticlesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.SuggestArticlesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for suggest_articles

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_suggest_articles(
        self, response: participant.SuggestArticlesResponse
    ) -> participant.SuggestArticlesResponse:
        """Post-rpc interceptor for suggest_articles

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_suggest_faq_answers(
        self,
        request: participant.SuggestFaqAnswersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.SuggestFaqAnswersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for suggest_faq_answers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_suggest_faq_answers(
        self, response: participant.SuggestFaqAnswersResponse
    ) -> participant.SuggestFaqAnswersResponse:
        """Post-rpc interceptor for suggest_faq_answers

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_suggest_knowledge_assist(
        self,
        request: participant.SuggestKnowledgeAssistRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.SuggestKnowledgeAssistRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for suggest_knowledge_assist

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_suggest_knowledge_assist(
        self, response: participant.SuggestKnowledgeAssistResponse
    ) -> participant.SuggestKnowledgeAssistResponse:
        """Post-rpc interceptor for suggest_knowledge_assist

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_suggest_smart_replies(
        self,
        request: participant.SuggestSmartRepliesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[participant.SuggestSmartRepliesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for suggest_smart_replies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_suggest_smart_replies(
        self, response: participant.SuggestSmartRepliesResponse
    ) -> participant.SuggestSmartRepliesResponse:
        """Post-rpc interceptor for suggest_smart_replies

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response

    def pre_update_participant(
        self,
        request: gcd_participant.UpdateParticipantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_participant.UpdateParticipantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_participant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_update_participant(
        self, response: gcd_participant.Participant
    ) -> gcd_participant.Participant:
        """Post-rpc interceptor for update_participant

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
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
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
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
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
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
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
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
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
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
        before they are sent to the Participants server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Participants server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ParticipantsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ParticipantsRestInterceptor


class ParticipantsRestTransport(_BaseParticipantsRestTransport):
    """REST backend synchronous transport for Participants.

    Service for managing
    [Participants][google.cloud.dialogflow.v2beta1.Participant].

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
        interceptor: Optional[ParticipantsRestInterceptor] = None,
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
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ParticipantsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AnalyzeContent(
        _BaseParticipantsRestTransport._BaseAnalyzeContent, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.AnalyzeContent")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gcd_participant.AnalyzeContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_participant.AnalyzeContentResponse:
            r"""Call the analyze content method over HTTP.

            Args:
                request (~.gcd_participant.AnalyzeContentRequest):
                    The request object. The request message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_participant.AnalyzeContentResponse:
                    The response message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseAnalyzeContent._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_content(request, metadata)
            transcoded_request = _BaseParticipantsRestTransport._BaseAnalyzeContent._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseAnalyzeContent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseAnalyzeContent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._AnalyzeContent._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_participant.AnalyzeContentResponse()
            pb_resp = gcd_participant.AnalyzeContentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_analyze_content(resp)
            return resp

    class _CompileSuggestion(
        _BaseParticipantsRestTransport._BaseCompileSuggestion, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.CompileSuggestion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: participant.CompileSuggestionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.CompileSuggestionResponse:
            r"""Call the compile suggestion method over HTTP.

            Args:
                request (~.participant.CompileSuggestionRequest):
                    The request object. The request message for
                [Participants.CompileSuggestion][google.cloud.dialogflow.v2beta1.Participants.CompileSuggestion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.CompileSuggestionResponse:
                    The response message for
                [Participants.CompileSuggestion][google.cloud.dialogflow.v2beta1.Participants.CompileSuggestion].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseCompileSuggestion._get_http_options()
            )
            request, metadata = self._interceptor.pre_compile_suggestion(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseCompileSuggestion._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseCompileSuggestion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseCompileSuggestion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._CompileSuggestion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.CompileSuggestionResponse()
            pb_resp = participant.CompileSuggestionResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_compile_suggestion(resp)
            return resp

    class _CreateParticipant(
        _BaseParticipantsRestTransport._BaseCreateParticipant, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.CreateParticipant")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gcd_participant.CreateParticipantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_participant.Participant:
            r"""Call the create participant method over HTTP.

            Args:
                request (~.gcd_participant.CreateParticipantRequest):
                    The request object. The request message for
                [Participants.CreateParticipant][google.cloud.dialogflow.v2beta1.Participants.CreateParticipant].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_participant.Participant:
                    Represents a conversation participant
                (human agent, virtual agent, end-user).

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseCreateParticipant._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_participant(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseCreateParticipant._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseCreateParticipant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseCreateParticipant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._CreateParticipant._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_participant.Participant()
            pb_resp = gcd_participant.Participant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_participant(resp)
            return resp

    class _GetParticipant(
        _BaseParticipantsRestTransport._BaseGetParticipant, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.GetParticipant")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: participant.GetParticipantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.Participant:
            r"""Call the get participant method over HTTP.

            Args:
                request (~.participant.GetParticipantRequest):
                    The request object. The request message for
                [Participants.GetParticipant][google.cloud.dialogflow.v2beta1.Participants.GetParticipant].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.Participant:
                    Represents a conversation participant
                (human agent, virtual agent, end-user).

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseGetParticipant._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_participant(request, metadata)
            transcoded_request = _BaseParticipantsRestTransport._BaseGetParticipant._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseGetParticipant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._GetParticipant._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.Participant()
            pb_resp = participant.Participant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_participant(resp)
            return resp

    class _ListParticipants(
        _BaseParticipantsRestTransport._BaseListParticipants, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.ListParticipants")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: participant.ListParticipantsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.ListParticipantsResponse:
            r"""Call the list participants method over HTTP.

            Args:
                request (~.participant.ListParticipantsRequest):
                    The request object. The request message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2beta1.Participants.ListParticipants].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.ListParticipantsResponse:
                    The response message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2beta1.Participants.ListParticipants].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseListParticipants._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_participants(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseListParticipants._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseListParticipants._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._ListParticipants._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.ListParticipantsResponse()
            pb_resp = participant.ListParticipantsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_participants(resp)
            return resp

    class _ListSuggestions(
        _BaseParticipantsRestTransport._BaseListSuggestions, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.ListSuggestions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: participant.ListSuggestionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.ListSuggestionsResponse:
            r"""Call the list suggestions method over HTTP.

            Args:
                request (~.participant.ListSuggestionsRequest):
                    The request object. The request message for
                [Participants.ListSuggestions][google.cloud.dialogflow.v2beta1.Participants.ListSuggestions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.ListSuggestionsResponse:
                    The response message for
                [Participants.ListSuggestions][google.cloud.dialogflow.v2beta1.Participants.ListSuggestions].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseListSuggestions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_suggestions(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseListSuggestions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseListSuggestions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._ListSuggestions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.ListSuggestionsResponse()
            pb_resp = participant.ListSuggestionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_suggestions(resp)
            return resp

    class _StreamingAnalyzeContent(
        _BaseParticipantsRestTransport._BaseStreamingAnalyzeContent,
        ParticipantsRestStub,
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.StreamingAnalyzeContent")

        def __call__(
            self,
            request: participant.StreamingAnalyzeContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method StreamingAnalyzeContent is not available over REST transport"
            )

    class _SuggestArticles(
        _BaseParticipantsRestTransport._BaseSuggestArticles, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.SuggestArticles")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: participant.SuggestArticlesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.SuggestArticlesResponse:
            r"""Call the suggest articles method over HTTP.

            Args:
                request (~.participant.SuggestArticlesRequest):
                    The request object. The request message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2beta1.Participants.SuggestArticles].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.SuggestArticlesResponse:
                    The response message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2beta1.Participants.SuggestArticles].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseSuggestArticles._get_http_options()
            )
            request, metadata = self._interceptor.pre_suggest_articles(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseSuggestArticles._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseSuggestArticles._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseSuggestArticles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._SuggestArticles._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.SuggestArticlesResponse()
            pb_resp = participant.SuggestArticlesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_suggest_articles(resp)
            return resp

    class _SuggestFaqAnswers(
        _BaseParticipantsRestTransport._BaseSuggestFaqAnswers, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.SuggestFaqAnswers")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: participant.SuggestFaqAnswersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.SuggestFaqAnswersResponse:
            r"""Call the suggest faq answers method over HTTP.

            Args:
                request (~.participant.SuggestFaqAnswersRequest):
                    The request object. The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2beta1.Participants.SuggestFaqAnswers].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.SuggestFaqAnswersResponse:
                    The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2beta1.Participants.SuggestFaqAnswers].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseSuggestFaqAnswers._get_http_options()
            )
            request, metadata = self._interceptor.pre_suggest_faq_answers(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseSuggestFaqAnswers._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseSuggestFaqAnswers._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseSuggestFaqAnswers._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._SuggestFaqAnswers._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.SuggestFaqAnswersResponse()
            pb_resp = participant.SuggestFaqAnswersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_suggest_faq_answers(resp)
            return resp

    class _SuggestKnowledgeAssist(
        _BaseParticipantsRestTransport._BaseSuggestKnowledgeAssist, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.SuggestKnowledgeAssist")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: participant.SuggestKnowledgeAssistRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.SuggestKnowledgeAssistResponse:
            r"""Call the suggest knowledge assist method over HTTP.

            Args:
                request (~.participant.SuggestKnowledgeAssistRequest):
                    The request object. The request message for
                [Participants.SuggestKnowledgeAssist][google.cloud.dialogflow.v2beta1.Participants.SuggestKnowledgeAssist].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.SuggestKnowledgeAssistResponse:
                    The response message for
                [Participants.SuggestKnowledgeAssist][google.cloud.dialogflow.v2beta1.Participants.SuggestKnowledgeAssist].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseSuggestKnowledgeAssist._get_http_options()
            )
            request, metadata = self._interceptor.pre_suggest_knowledge_assist(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseSuggestKnowledgeAssist._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseSuggestKnowledgeAssist._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseSuggestKnowledgeAssist._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._SuggestKnowledgeAssist._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.SuggestKnowledgeAssistResponse()
            pb_resp = participant.SuggestKnowledgeAssistResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_suggest_knowledge_assist(resp)
            return resp

    class _SuggestSmartReplies(
        _BaseParticipantsRestTransport._BaseSuggestSmartReplies, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.SuggestSmartReplies")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: participant.SuggestSmartRepliesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> participant.SuggestSmartRepliesResponse:
            r"""Call the suggest smart replies method over HTTP.

            Args:
                request (~.participant.SuggestSmartRepliesRequest):
                    The request object. The request message for
                [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2beta1.Participants.SuggestSmartReplies].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.participant.SuggestSmartRepliesResponse:
                    The response message for
                [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2beta1.Participants.SuggestSmartReplies].

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseSuggestSmartReplies._get_http_options()
            )
            request, metadata = self._interceptor.pre_suggest_smart_replies(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseSuggestSmartReplies._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseSuggestSmartReplies._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseSuggestSmartReplies._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._SuggestSmartReplies._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = participant.SuggestSmartRepliesResponse()
            pb_resp = participant.SuggestSmartRepliesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_suggest_smart_replies(resp)
            return resp

    class _UpdateParticipant(
        _BaseParticipantsRestTransport._BaseUpdateParticipant, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.UpdateParticipant")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gcd_participant.UpdateParticipantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_participant.Participant:
            r"""Call the update participant method over HTTP.

            Args:
                request (~.gcd_participant.UpdateParticipantRequest):
                    The request object. The request message for
                [Participants.UpdateParticipant][google.cloud.dialogflow.v2beta1.Participants.UpdateParticipant].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_participant.Participant:
                    Represents a conversation participant
                (human agent, virtual agent, end-user).

            """

            http_options = (
                _BaseParticipantsRestTransport._BaseUpdateParticipant._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_participant(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseUpdateParticipant._get_transcoded_request(
                http_options, request
            )

            body = _BaseParticipantsRestTransport._BaseUpdateParticipant._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseUpdateParticipant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._UpdateParticipant._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_participant.Participant()
            pb_resp = gcd_participant.Participant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_participant(resp)
            return resp

    @property
    def analyze_content(
        self,
    ) -> Callable[
        [gcd_participant.AnalyzeContentRequest], gcd_participant.AnalyzeContentResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def compile_suggestion(
        self,
    ) -> Callable[
        [participant.CompileSuggestionRequest], participant.CompileSuggestionResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompileSuggestion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_participant(
        self,
    ) -> Callable[
        [gcd_participant.CreateParticipantRequest], gcd_participant.Participant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateParticipant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_participant(
        self,
    ) -> Callable[[participant.GetParticipantRequest], participant.Participant]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetParticipant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_participants(
        self,
    ) -> Callable[
        [participant.ListParticipantsRequest], participant.ListParticipantsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListParticipants(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_suggestions(
        self,
    ) -> Callable[
        [participant.ListSuggestionsRequest], participant.ListSuggestionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSuggestions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def streaming_analyze_content(
        self,
    ) -> Callable[
        [participant.StreamingAnalyzeContentRequest],
        participant.StreamingAnalyzeContentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StreamingAnalyzeContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def suggest_articles(
        self,
    ) -> Callable[
        [participant.SuggestArticlesRequest], participant.SuggestArticlesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SuggestArticles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def suggest_faq_answers(
        self,
    ) -> Callable[
        [participant.SuggestFaqAnswersRequest], participant.SuggestFaqAnswersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SuggestFaqAnswers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def suggest_knowledge_assist(
        self,
    ) -> Callable[
        [participant.SuggestKnowledgeAssistRequest],
        participant.SuggestKnowledgeAssistResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SuggestKnowledgeAssist(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def suggest_smart_replies(
        self,
    ) -> Callable[
        [participant.SuggestSmartRepliesRequest],
        participant.SuggestSmartRepliesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SuggestSmartReplies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_participant(
        self,
    ) -> Callable[
        [gcd_participant.UpdateParticipantRequest], gcd_participant.Participant
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateParticipant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseParticipantsRestTransport._BaseGetLocation, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

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

            http_options = (
                _BaseParticipantsRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseParticipantsRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseParticipantsRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ParticipantsRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseParticipantsRestTransport._BaseListLocations, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

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

            http_options = (
                _BaseParticipantsRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseParticipantsRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseParticipantsRestTransport._BaseCancelOperation, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

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

            http_options = (
                _BaseParticipantsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseParticipantsRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseParticipantsRestTransport._BaseGetOperation, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

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

            http_options = (
                _BaseParticipantsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseParticipantsRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseParticipantsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ParticipantsRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseParticipantsRestTransport._BaseListOperations, ParticipantsRestStub
    ):
        def __hash__(self):
            return hash("ParticipantsRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

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

            http_options = (
                _BaseParticipantsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseParticipantsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParticipantsRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ParticipantsRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ParticipantsRestTransport",)
