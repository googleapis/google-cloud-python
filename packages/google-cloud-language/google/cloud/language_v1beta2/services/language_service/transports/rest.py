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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.language_v1beta2.types import language_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseLanguageServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class LanguageServiceRestInterceptor:
    """Interceptor for LanguageService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LanguageServiceRestTransport.

    .. code-block:: python
        class MyCustomLanguageServiceInterceptor(LanguageServiceRestInterceptor):
            def pre_analyze_entities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_entities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_analyze_entity_sentiment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_entity_sentiment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_analyze_sentiment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_sentiment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_analyze_syntax(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_syntax(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_annotate_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_annotate_text(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_classify_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_classify_text(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_moderate_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_moderate_text(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LanguageServiceRestTransport(interceptor=MyCustomLanguageServiceInterceptor())
        client = LanguageServiceClient(transport=transport)


    """

    def pre_analyze_entities(
        self,
        request: language_service.AnalyzeEntitiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.AnalyzeEntitiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_entities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_analyze_entities(
        self, response: language_service.AnalyzeEntitiesResponse
    ) -> language_service.AnalyzeEntitiesResponse:
        """Post-rpc interceptor for analyze_entities

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_analyze_entity_sentiment(
        self,
        request: language_service.AnalyzeEntitySentimentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        language_service.AnalyzeEntitySentimentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for analyze_entity_sentiment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_analyze_entity_sentiment(
        self, response: language_service.AnalyzeEntitySentimentResponse
    ) -> language_service.AnalyzeEntitySentimentResponse:
        """Post-rpc interceptor for analyze_entity_sentiment

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_analyze_sentiment(
        self,
        request: language_service.AnalyzeSentimentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.AnalyzeSentimentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_sentiment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_analyze_sentiment(
        self, response: language_service.AnalyzeSentimentResponse
    ) -> language_service.AnalyzeSentimentResponse:
        """Post-rpc interceptor for analyze_sentiment

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_analyze_syntax(
        self,
        request: language_service.AnalyzeSyntaxRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.AnalyzeSyntaxRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_syntax

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_analyze_syntax(
        self, response: language_service.AnalyzeSyntaxResponse
    ) -> language_service.AnalyzeSyntaxResponse:
        """Post-rpc interceptor for analyze_syntax

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_annotate_text(
        self,
        request: language_service.AnnotateTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.AnnotateTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for annotate_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_annotate_text(
        self, response: language_service.AnnotateTextResponse
    ) -> language_service.AnnotateTextResponse:
        """Post-rpc interceptor for annotate_text

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_classify_text(
        self,
        request: language_service.ClassifyTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.ClassifyTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for classify_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_classify_text(
        self, response: language_service.ClassifyTextResponse
    ) -> language_service.ClassifyTextResponse:
        """Post-rpc interceptor for classify_text

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response

    def pre_moderate_text(
        self,
        request: language_service.ModerateTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[language_service.ModerateTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for moderate_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LanguageService server.
        """
        return request, metadata

    def post_moderate_text(
        self, response: language_service.ModerateTextResponse
    ) -> language_service.ModerateTextResponse:
        """Post-rpc interceptor for moderate_text

        Override in a subclass to manipulate the response
        after it is returned by the LanguageService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LanguageServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LanguageServiceRestInterceptor


class LanguageServiceRestTransport(_BaseLanguageServiceRestTransport):
    """REST backend synchronous transport for LanguageService.

    Provides text analysis operations such as sentiment analysis
    and entity recognition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "language.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LanguageServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'language.googleapis.com').
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
        self._interceptor = interceptor or LanguageServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AnalyzeEntities(
        _BaseLanguageServiceRestTransport._BaseAnalyzeEntities, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.AnalyzeEntities")

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
            request: language_service.AnalyzeEntitiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.AnalyzeEntitiesResponse:
            r"""Call the analyze entities method over HTTP.

            Args:
                request (~.language_service.AnalyzeEntitiesRequest):
                    The request object. The entity analysis request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.AnalyzeEntitiesResponse:
                    The entity analysis response message.
            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseAnalyzeEntities._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_entities(
                request, metadata
            )
            transcoded_request = _BaseLanguageServiceRestTransport._BaseAnalyzeEntities._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseAnalyzeEntities._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseAnalyzeEntities._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._AnalyzeEntities._get_response(
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
            resp = language_service.AnalyzeEntitiesResponse()
            pb_resp = language_service.AnalyzeEntitiesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_analyze_entities(resp)
            return resp

    class _AnalyzeEntitySentiment(
        _BaseLanguageServiceRestTransport._BaseAnalyzeEntitySentiment,
        LanguageServiceRestStub,
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.AnalyzeEntitySentiment")

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
            request: language_service.AnalyzeEntitySentimentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.AnalyzeEntitySentimentResponse:
            r"""Call the analyze entity sentiment method over HTTP.

            Args:
                request (~.language_service.AnalyzeEntitySentimentRequest):
                    The request object. The entity-level sentiment analysis
                request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.AnalyzeEntitySentimentResponse:
                    The entity-level sentiment analysis
                response message.

            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseAnalyzeEntitySentiment._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_entity_sentiment(
                request, metadata
            )
            transcoded_request = _BaseLanguageServiceRestTransport._BaseAnalyzeEntitySentiment._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseAnalyzeEntitySentiment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseAnalyzeEntitySentiment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                LanguageServiceRestTransport._AnalyzeEntitySentiment._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = language_service.AnalyzeEntitySentimentResponse()
            pb_resp = language_service.AnalyzeEntitySentimentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_analyze_entity_sentiment(resp)
            return resp

    class _AnalyzeSentiment(
        _BaseLanguageServiceRestTransport._BaseAnalyzeSentiment, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.AnalyzeSentiment")

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
            request: language_service.AnalyzeSentimentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.AnalyzeSentimentResponse:
            r"""Call the analyze sentiment method over HTTP.

            Args:
                request (~.language_service.AnalyzeSentimentRequest):
                    The request object. The sentiment analysis request
                message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.AnalyzeSentimentResponse:
                    The sentiment analysis response
                message.

            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseAnalyzeSentiment._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_sentiment(
                request, metadata
            )
            transcoded_request = _BaseLanguageServiceRestTransport._BaseAnalyzeSentiment._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseAnalyzeSentiment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseAnalyzeSentiment._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._AnalyzeSentiment._get_response(
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
            resp = language_service.AnalyzeSentimentResponse()
            pb_resp = language_service.AnalyzeSentimentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_analyze_sentiment(resp)
            return resp

    class _AnalyzeSyntax(
        _BaseLanguageServiceRestTransport._BaseAnalyzeSyntax, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.AnalyzeSyntax")

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
            request: language_service.AnalyzeSyntaxRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.AnalyzeSyntaxResponse:
            r"""Call the analyze syntax method over HTTP.

            Args:
                request (~.language_service.AnalyzeSyntaxRequest):
                    The request object. The syntax analysis request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.AnalyzeSyntaxResponse:
                    The syntax analysis response message.
            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseAnalyzeSyntax._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_syntax(request, metadata)
            transcoded_request = _BaseLanguageServiceRestTransport._BaseAnalyzeSyntax._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseAnalyzeSyntax._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseAnalyzeSyntax._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._AnalyzeSyntax._get_response(
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
            resp = language_service.AnalyzeSyntaxResponse()
            pb_resp = language_service.AnalyzeSyntaxResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_analyze_syntax(resp)
            return resp

    class _AnnotateText(
        _BaseLanguageServiceRestTransport._BaseAnnotateText, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.AnnotateText")

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
            request: language_service.AnnotateTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.AnnotateTextResponse:
            r"""Call the annotate text method over HTTP.

            Args:
                request (~.language_service.AnnotateTextRequest):
                    The request object. The request message for the text
                annotation API, which can perform
                multiple analysis types (sentiment,
                entities, and syntax) in one call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.AnnotateTextResponse:
                    The text annotations response
                message.

            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseAnnotateText._get_http_options()
            )
            request, metadata = self._interceptor.pre_annotate_text(request, metadata)
            transcoded_request = _BaseLanguageServiceRestTransport._BaseAnnotateText._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseAnnotateText._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseAnnotateText._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._AnnotateText._get_response(
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
            resp = language_service.AnnotateTextResponse()
            pb_resp = language_service.AnnotateTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_annotate_text(resp)
            return resp

    class _ClassifyText(
        _BaseLanguageServiceRestTransport._BaseClassifyText, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.ClassifyText")

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
            request: language_service.ClassifyTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.ClassifyTextResponse:
            r"""Call the classify text method over HTTP.

            Args:
                request (~.language_service.ClassifyTextRequest):
                    The request object. The document classification request
                message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.ClassifyTextResponse:
                    The document classification response
                message.

            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseClassifyText._get_http_options()
            )
            request, metadata = self._interceptor.pre_classify_text(request, metadata)
            transcoded_request = _BaseLanguageServiceRestTransport._BaseClassifyText._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseClassifyText._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseClassifyText._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._ClassifyText._get_response(
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
            resp = language_service.ClassifyTextResponse()
            pb_resp = language_service.ClassifyTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_classify_text(resp)
            return resp

    class _ModerateText(
        _BaseLanguageServiceRestTransport._BaseModerateText, LanguageServiceRestStub
    ):
        def __hash__(self):
            return hash("LanguageServiceRestTransport.ModerateText")

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
            request: language_service.ModerateTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> language_service.ModerateTextResponse:
            r"""Call the moderate text method over HTTP.

            Args:
                request (~.language_service.ModerateTextRequest):
                    The request object. The document moderation request
                message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.language_service.ModerateTextResponse:
                    The document moderation response
                message.

            """

            http_options = (
                _BaseLanguageServiceRestTransport._BaseModerateText._get_http_options()
            )
            request, metadata = self._interceptor.pre_moderate_text(request, metadata)
            transcoded_request = _BaseLanguageServiceRestTransport._BaseModerateText._get_transcoded_request(
                http_options, request
            )

            body = _BaseLanguageServiceRestTransport._BaseModerateText._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLanguageServiceRestTransport._BaseModerateText._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LanguageServiceRestTransport._ModerateText._get_response(
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
            resp = language_service.ModerateTextResponse()
            pb_resp = language_service.ModerateTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_moderate_text(resp)
            return resp

    @property
    def analyze_entities(
        self,
    ) -> Callable[
        [language_service.AnalyzeEntitiesRequest],
        language_service.AnalyzeEntitiesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeEntities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def analyze_entity_sentiment(
        self,
    ) -> Callable[
        [language_service.AnalyzeEntitySentimentRequest],
        language_service.AnalyzeEntitySentimentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeEntitySentiment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def analyze_sentiment(
        self,
    ) -> Callable[
        [language_service.AnalyzeSentimentRequest],
        language_service.AnalyzeSentimentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeSentiment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def analyze_syntax(
        self,
    ) -> Callable[
        [language_service.AnalyzeSyntaxRequest], language_service.AnalyzeSyntaxResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeSyntax(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def annotate_text(
        self,
    ) -> Callable[
        [language_service.AnnotateTextRequest], language_service.AnnotateTextResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnnotateText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def classify_text(
        self,
    ) -> Callable[
        [language_service.ClassifyTextRequest], language_service.ClassifyTextResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ClassifyText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def moderate_text(
        self,
    ) -> Callable[
        [language_service.ModerateTextRequest], language_service.ModerateTextResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ModerateText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LanguageServiceRestTransport",)
