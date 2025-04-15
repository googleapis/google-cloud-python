# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.devicestreaming_v1.types import adb_service, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDirectAccessServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DirectAccessServiceRestInterceptor:
    """Interceptor for DirectAccessService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DirectAccessServiceRestTransport.

    .. code-block:: python
        class MyCustomDirectAccessServiceInterceptor(DirectAccessServiceRestInterceptor):
            def pre_cancel_device_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_device_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_device_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_device_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_device_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_device_sessions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_device_sessions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_device_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_device_session(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DirectAccessServiceRestTransport(interceptor=MyCustomDirectAccessServiceInterceptor())
        client = DirectAccessServiceClient(transport=transport)


    """

    def pre_cancel_device_session(
        self,
        request: service.CancelDeviceSessionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.CancelDeviceSessionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_device_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DirectAccessService server.
        """
        return request, metadata

    def pre_create_device_session(
        self,
        request: service.CreateDeviceSessionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.CreateDeviceSessionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_device_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DirectAccessService server.
        """
        return request, metadata

    def post_create_device_session(
        self, response: service.DeviceSession
    ) -> service.DeviceSession:
        """Post-rpc interceptor for create_device_session

        DEPRECATED. Please use the `post_create_device_session_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DirectAccessService server but before
        it is returned to user code. This `post_create_device_session` interceptor runs
        before the `post_create_device_session_with_metadata` interceptor.
        """
        return response

    def post_create_device_session_with_metadata(
        self,
        response: service.DeviceSession,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeviceSession, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_device_session

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DirectAccessService server but before it is returned to user code.

        We recommend only using this `post_create_device_session_with_metadata`
        interceptor in new development instead of the `post_create_device_session` interceptor.
        When both interceptors are used, this `post_create_device_session_with_metadata` interceptor runs after the
        `post_create_device_session` interceptor. The (possibly modified) response returned by
        `post_create_device_session` will be passed to
        `post_create_device_session_with_metadata`.
        """
        return response, metadata

    def pre_get_device_session(
        self,
        request: service.GetDeviceSessionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GetDeviceSessionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_device_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DirectAccessService server.
        """
        return request, metadata

    def post_get_device_session(
        self, response: service.DeviceSession
    ) -> service.DeviceSession:
        """Post-rpc interceptor for get_device_session

        DEPRECATED. Please use the `post_get_device_session_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DirectAccessService server but before
        it is returned to user code. This `post_get_device_session` interceptor runs
        before the `post_get_device_session_with_metadata` interceptor.
        """
        return response

    def post_get_device_session_with_metadata(
        self,
        response: service.DeviceSession,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeviceSession, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_device_session

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DirectAccessService server but before it is returned to user code.

        We recommend only using this `post_get_device_session_with_metadata`
        interceptor in new development instead of the `post_get_device_session` interceptor.
        When both interceptors are used, this `post_get_device_session_with_metadata` interceptor runs after the
        `post_get_device_session` interceptor. The (possibly modified) response returned by
        `post_get_device_session` will be passed to
        `post_get_device_session_with_metadata`.
        """
        return response, metadata

    def pre_list_device_sessions(
        self,
        request: service.ListDeviceSessionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListDeviceSessionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_device_sessions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DirectAccessService server.
        """
        return request, metadata

    def post_list_device_sessions(
        self, response: service.ListDeviceSessionsResponse
    ) -> service.ListDeviceSessionsResponse:
        """Post-rpc interceptor for list_device_sessions

        DEPRECATED. Please use the `post_list_device_sessions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DirectAccessService server but before
        it is returned to user code. This `post_list_device_sessions` interceptor runs
        before the `post_list_device_sessions_with_metadata` interceptor.
        """
        return response

    def post_list_device_sessions_with_metadata(
        self,
        response: service.ListDeviceSessionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListDeviceSessionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_device_sessions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DirectAccessService server but before it is returned to user code.

        We recommend only using this `post_list_device_sessions_with_metadata`
        interceptor in new development instead of the `post_list_device_sessions` interceptor.
        When both interceptors are used, this `post_list_device_sessions_with_metadata` interceptor runs after the
        `post_list_device_sessions` interceptor. The (possibly modified) response returned by
        `post_list_device_sessions` will be passed to
        `post_list_device_sessions_with_metadata`.
        """
        return response, metadata

    def pre_update_device_session(
        self,
        request: service.UpdateDeviceSessionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.UpdateDeviceSessionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_device_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DirectAccessService server.
        """
        return request, metadata

    def post_update_device_session(
        self, response: service.DeviceSession
    ) -> service.DeviceSession:
        """Post-rpc interceptor for update_device_session

        DEPRECATED. Please use the `post_update_device_session_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DirectAccessService server but before
        it is returned to user code. This `post_update_device_session` interceptor runs
        before the `post_update_device_session_with_metadata` interceptor.
        """
        return response

    def post_update_device_session_with_metadata(
        self,
        response: service.DeviceSession,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeviceSession, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_device_session

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DirectAccessService server but before it is returned to user code.

        We recommend only using this `post_update_device_session_with_metadata`
        interceptor in new development instead of the `post_update_device_session` interceptor.
        When both interceptors are used, this `post_update_device_session_with_metadata` interceptor runs after the
        `post_update_device_session` interceptor. The (possibly modified) response returned by
        `post_update_device_session` will be passed to
        `post_update_device_session_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class DirectAccessServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DirectAccessServiceRestInterceptor


class DirectAccessServiceRestTransport(_BaseDirectAccessServiceRestTransport):
    """REST backend synchronous transport for DirectAccessService.

    A service for allocating Android devices and interacting with
    the live-allocated devices.

    Each Session will wait for available capacity, at a higher
    priority over Test Execution. When allocated, the session will
    be exposed through a stream for integration.

    DirectAccessService is currently available as a preview to
    select developers. You can register today on behalf of you and
    your team at
    https://developer.android.com/studio/preview/android-device-streaming

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "devicestreaming.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DirectAccessServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'devicestreaming.googleapis.com').
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
        self._interceptor = interceptor or DirectAccessServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AdbConnect(
        _BaseDirectAccessServiceRestTransport._BaseAdbConnect,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.AdbConnect")

        def __call__(
            self,
            request: adb_service.AdbMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method AdbConnect is not available over REST transport"
            )

    class _CancelDeviceSession(
        _BaseDirectAccessServiceRestTransport._BaseCancelDeviceSession,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.CancelDeviceSession")

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
            request: service.CancelDeviceSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the cancel device session method over HTTP.

            Args:
                request (~.service.CancelDeviceSessionRequest):
                    The request object. Request message for
                DirectAccessService.CancelDeviceSession.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDirectAccessServiceRestTransport._BaseCancelDeviceSession._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_device_session(
                request, metadata
            )
            transcoded_request = _BaseDirectAccessServiceRestTransport._BaseCancelDeviceSession._get_transcoded_request(
                http_options, request
            )

            body = _BaseDirectAccessServiceRestTransport._BaseCancelDeviceSession._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDirectAccessServiceRestTransport._BaseCancelDeviceSession._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.devicestreaming_v1.DirectAccessServiceClient.CancelDeviceSession",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "CancelDeviceSession",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DirectAccessServiceRestTransport._CancelDeviceSession._get_response(
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

    class _CreateDeviceSession(
        _BaseDirectAccessServiceRestTransport._BaseCreateDeviceSession,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.CreateDeviceSession")

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
            request: service.CreateDeviceSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.DeviceSession:
            r"""Call the create device session method over HTTP.

            Args:
                request (~.service.CreateDeviceSessionRequest):
                    The request object. Request message for
                DirectAccessService.CreateDeviceSession.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.DeviceSession:
                    Protobuf message describing the
                device message, used from several RPCs.

            """

            http_options = (
                _BaseDirectAccessServiceRestTransport._BaseCreateDeviceSession._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_device_session(
                request, metadata
            )
            transcoded_request = _BaseDirectAccessServiceRestTransport._BaseCreateDeviceSession._get_transcoded_request(
                http_options, request
            )

            body = _BaseDirectAccessServiceRestTransport._BaseCreateDeviceSession._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDirectAccessServiceRestTransport._BaseCreateDeviceSession._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.devicestreaming_v1.DirectAccessServiceClient.CreateDeviceSession",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "CreateDeviceSession",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DirectAccessServiceRestTransport._CreateDeviceSession._get_response(
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
            resp = service.DeviceSession()
            pb_resp = service.DeviceSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_device_session(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_device_session_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.DeviceSession.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.devicestreaming_v1.DirectAccessServiceClient.create_device_session",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "CreateDeviceSession",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetDeviceSession(
        _BaseDirectAccessServiceRestTransport._BaseGetDeviceSession,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.GetDeviceSession")

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
            request: service.GetDeviceSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.DeviceSession:
            r"""Call the get device session method over HTTP.

            Args:
                request (~.service.GetDeviceSessionRequest):
                    The request object. Request message for
                DirectAccessService.GetDeviceSession.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.DeviceSession:
                    Protobuf message describing the
                device message, used from several RPCs.

            """

            http_options = (
                _BaseDirectAccessServiceRestTransport._BaseGetDeviceSession._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_device_session(
                request, metadata
            )
            transcoded_request = _BaseDirectAccessServiceRestTransport._BaseGetDeviceSession._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDirectAccessServiceRestTransport._BaseGetDeviceSession._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.devicestreaming_v1.DirectAccessServiceClient.GetDeviceSession",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "GetDeviceSession",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DirectAccessServiceRestTransport._GetDeviceSession._get_response(
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
            resp = service.DeviceSession()
            pb_resp = service.DeviceSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_device_session(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_device_session_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.DeviceSession.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.devicestreaming_v1.DirectAccessServiceClient.get_device_session",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "GetDeviceSession",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDeviceSessions(
        _BaseDirectAccessServiceRestTransport._BaseListDeviceSessions,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.ListDeviceSessions")

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
            request: service.ListDeviceSessionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListDeviceSessionsResponse:
            r"""Call the list device sessions method over HTTP.

            Args:
                request (~.service.ListDeviceSessionsRequest):
                    The request object. Request message for
                DirectAccessService.ListDeviceSessions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListDeviceSessionsResponse:
                    Response message for
                DirectAccessService.ListDeviceSessions.

            """

            http_options = (
                _BaseDirectAccessServiceRestTransport._BaseListDeviceSessions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_device_sessions(
                request, metadata
            )
            transcoded_request = _BaseDirectAccessServiceRestTransport._BaseListDeviceSessions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDirectAccessServiceRestTransport._BaseListDeviceSessions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.devicestreaming_v1.DirectAccessServiceClient.ListDeviceSessions",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "ListDeviceSessions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DirectAccessServiceRestTransport._ListDeviceSessions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListDeviceSessionsResponse()
            pb_resp = service.ListDeviceSessionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_device_sessions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_device_sessions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListDeviceSessionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.devicestreaming_v1.DirectAccessServiceClient.list_device_sessions",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "ListDeviceSessions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateDeviceSession(
        _BaseDirectAccessServiceRestTransport._BaseUpdateDeviceSession,
        DirectAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("DirectAccessServiceRestTransport.UpdateDeviceSession")

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
            request: service.UpdateDeviceSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.DeviceSession:
            r"""Call the update device session method over HTTP.

            Args:
                request (~.service.UpdateDeviceSessionRequest):
                    The request object. Request message for
                DirectAccessService.UpdateDeviceSession.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.DeviceSession:
                    Protobuf message describing the
                device message, used from several RPCs.

            """

            http_options = (
                _BaseDirectAccessServiceRestTransport._BaseUpdateDeviceSession._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_device_session(
                request, metadata
            )
            transcoded_request = _BaseDirectAccessServiceRestTransport._BaseUpdateDeviceSession._get_transcoded_request(
                http_options, request
            )

            body = _BaseDirectAccessServiceRestTransport._BaseUpdateDeviceSession._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDirectAccessServiceRestTransport._BaseUpdateDeviceSession._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.devicestreaming_v1.DirectAccessServiceClient.UpdateDeviceSession",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "UpdateDeviceSession",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DirectAccessServiceRestTransport._UpdateDeviceSession._get_response(
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
            resp = service.DeviceSession()
            pb_resp = service.DeviceSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_device_session(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_device_session_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.DeviceSession.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.devicestreaming_v1.DirectAccessServiceClient.update_device_session",
                    extra={
                        "serviceName": "google.cloud.devicestreaming.v1.DirectAccessService",
                        "rpcName": "UpdateDeviceSession",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def adb_connect(
        self,
    ) -> Callable[[adb_service.AdbMessage], adb_service.DeviceMessage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AdbConnect(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_device_session(
        self,
    ) -> Callable[[service.CancelDeviceSessionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelDeviceSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_device_session(
        self,
    ) -> Callable[[service.CreateDeviceSessionRequest], service.DeviceSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeviceSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_device_session(
        self,
    ) -> Callable[[service.GetDeviceSessionRequest], service.DeviceSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeviceSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_device_sessions(
        self,
    ) -> Callable[
        [service.ListDeviceSessionsRequest], service.ListDeviceSessionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeviceSessions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_device_session(
        self,
    ) -> Callable[[service.UpdateDeviceSessionRequest], service.DeviceSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeviceSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DirectAccessServiceRestTransport",)
