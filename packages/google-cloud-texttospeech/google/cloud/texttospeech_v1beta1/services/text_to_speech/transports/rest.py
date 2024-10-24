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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.texttospeech_v1beta1.types import cloud_tts

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseTextToSpeechRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class TextToSpeechRestInterceptor:
    """Interceptor for TextToSpeech.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TextToSpeechRestTransport.

    .. code-block:: python
        class MyCustomTextToSpeechInterceptor(TextToSpeechRestInterceptor):
            def pre_list_voices(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_voices(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_synthesize_speech(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_synthesize_speech(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TextToSpeechRestTransport(interceptor=MyCustomTextToSpeechInterceptor())
        client = TextToSpeechClient(transport=transport)


    """

    def pre_list_voices(
        self, request: cloud_tts.ListVoicesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloud_tts.ListVoicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_voices

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TextToSpeech server.
        """
        return request, metadata

    def post_list_voices(
        self, response: cloud_tts.ListVoicesResponse
    ) -> cloud_tts.ListVoicesResponse:
        """Post-rpc interceptor for list_voices

        Override in a subclass to manipulate the response
        after it is returned by the TextToSpeech server but before
        it is returned to user code.
        """
        return response

    def pre_synthesize_speech(
        self,
        request: cloud_tts.SynthesizeSpeechRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_tts.SynthesizeSpeechRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for synthesize_speech

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TextToSpeech server.
        """
        return request, metadata

    def post_synthesize_speech(
        self, response: cloud_tts.SynthesizeSpeechResponse
    ) -> cloud_tts.SynthesizeSpeechResponse:
        """Post-rpc interceptor for synthesize_speech

        Override in a subclass to manipulate the response
        after it is returned by the TextToSpeech server but before
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
        before they are sent to the TextToSpeech server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the TextToSpeech server but before
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
        before they are sent to the TextToSpeech server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the TextToSpeech server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class TextToSpeechRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TextToSpeechRestInterceptor


class TextToSpeechRestTransport(_BaseTextToSpeechRestTransport):
    """REST backend synchronous transport for TextToSpeech.

    Service that implements Google Cloud Text-to-Speech API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "texttospeech.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[TextToSpeechRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'texttospeech.googleapis.com').
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
        self._interceptor = interceptor or TextToSpeechRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _ListVoices(
        _BaseTextToSpeechRestTransport._BaseListVoices, TextToSpeechRestStub
    ):
        def __hash__(self):
            return hash("TextToSpeechRestTransport.ListVoices")

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
            request: cloud_tts.ListVoicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_tts.ListVoicesResponse:
            r"""Call the list voices method over HTTP.

            Args:
                request (~.cloud_tts.ListVoicesRequest):
                    The request object. The top-level message sent by the client for the
                ``ListVoices`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_tts.ListVoicesResponse:
                    The message returned to the client by the ``ListVoices``
                method.

            """

            http_options = (
                _BaseTextToSpeechRestTransport._BaseListVoices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_voices(request, metadata)
            transcoded_request = (
                _BaseTextToSpeechRestTransport._BaseListVoices._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTextToSpeechRestTransport._BaseListVoices._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TextToSpeechRestTransport._ListVoices._get_response(
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
            resp = cloud_tts.ListVoicesResponse()
            pb_resp = cloud_tts.ListVoicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_voices(resp)
            return resp

    class _StreamingSynthesize(
        _BaseTextToSpeechRestTransport._BaseStreamingSynthesize, TextToSpeechRestStub
    ):
        def __hash__(self):
            return hash("TextToSpeechRestTransport.StreamingSynthesize")

        def __call__(
            self,
            request: cloud_tts.StreamingSynthesizeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method StreamingSynthesize is not available over REST transport"
            )

    class _SynthesizeSpeech(
        _BaseTextToSpeechRestTransport._BaseSynthesizeSpeech, TextToSpeechRestStub
    ):
        def __hash__(self):
            return hash("TextToSpeechRestTransport.SynthesizeSpeech")

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
            request: cloud_tts.SynthesizeSpeechRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_tts.SynthesizeSpeechResponse:
            r"""Call the synthesize speech method over HTTP.

            Args:
                request (~.cloud_tts.SynthesizeSpeechRequest):
                    The request object. The top-level message sent by the client for the
                ``SynthesizeSpeech`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_tts.SynthesizeSpeechResponse:
                    The message returned to the client by the
                ``SynthesizeSpeech`` method.

            """

            http_options = (
                _BaseTextToSpeechRestTransport._BaseSynthesizeSpeech._get_http_options()
            )
            request, metadata = self._interceptor.pre_synthesize_speech(
                request, metadata
            )
            transcoded_request = _BaseTextToSpeechRestTransport._BaseSynthesizeSpeech._get_transcoded_request(
                http_options, request
            )

            body = _BaseTextToSpeechRestTransport._BaseSynthesizeSpeech._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTextToSpeechRestTransport._BaseSynthesizeSpeech._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TextToSpeechRestTransport._SynthesizeSpeech._get_response(
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
            resp = cloud_tts.SynthesizeSpeechResponse()
            pb_resp = cloud_tts.SynthesizeSpeechResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_synthesize_speech(resp)
            return resp

    @property
    def list_voices(
        self,
    ) -> Callable[[cloud_tts.ListVoicesRequest], cloud_tts.ListVoicesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVoices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def streaming_synthesize(
        self,
    ) -> Callable[
        [cloud_tts.StreamingSynthesizeRequest], cloud_tts.StreamingSynthesizeResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StreamingSynthesize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def synthesize_speech(
        self,
    ) -> Callable[
        [cloud_tts.SynthesizeSpeechRequest], cloud_tts.SynthesizeSpeechResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SynthesizeSpeech(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseTextToSpeechRestTransport._BaseGetOperation, TextToSpeechRestStub
    ):
        def __hash__(self):
            return hash("TextToSpeechRestTransport.GetOperation")

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
                _BaseTextToSpeechRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseTextToSpeechRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseTextToSpeechRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TextToSpeechRestTransport._GetOperation._get_response(
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
        _BaseTextToSpeechRestTransport._BaseListOperations, TextToSpeechRestStub
    ):
        def __hash__(self):
            return hash("TextToSpeechRestTransport.ListOperations")

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
                _BaseTextToSpeechRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseTextToSpeechRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseTextToSpeechRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TextToSpeechRestTransport._ListOperations._get_response(
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


__all__ = ("TextToSpeechRestTransport",)
