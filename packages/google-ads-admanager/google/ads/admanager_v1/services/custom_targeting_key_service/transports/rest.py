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
import logging
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

from google.ads.admanager_v1.types import (
    custom_targeting_key_messages,
    custom_targeting_key_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCustomTargetingKeyServiceRestTransport

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


class CustomTargetingKeyServiceRestInterceptor:
    """Interceptor for CustomTargetingKeyService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CustomTargetingKeyServiceRestTransport.

    .. code-block:: python
        class MyCustomCustomTargetingKeyServiceInterceptor(CustomTargetingKeyServiceRestInterceptor):
            def pre_get_custom_targeting_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_targeting_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_targeting_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_targeting_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CustomTargetingKeyServiceRestTransport(interceptor=MyCustomCustomTargetingKeyServiceInterceptor())
        client = CustomTargetingKeyServiceClient(transport=transport)


    """

    def pre_get_custom_targeting_key(
        self,
        request: custom_targeting_key_service.GetCustomTargetingKeyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        custom_targeting_key_service.GetCustomTargetingKeyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_custom_targeting_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CustomTargetingKeyService server.
        """
        return request, metadata

    def post_get_custom_targeting_key(
        self, response: custom_targeting_key_messages.CustomTargetingKey
    ) -> custom_targeting_key_messages.CustomTargetingKey:
        """Post-rpc interceptor for get_custom_targeting_key

        Override in a subclass to manipulate the response
        after it is returned by the CustomTargetingKeyService server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_targeting_keys(
        self,
        request: custom_targeting_key_service.ListCustomTargetingKeysRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        custom_targeting_key_service.ListCustomTargetingKeysRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_custom_targeting_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CustomTargetingKeyService server.
        """
        return request, metadata

    def post_list_custom_targeting_keys(
        self, response: custom_targeting_key_service.ListCustomTargetingKeysResponse
    ) -> custom_targeting_key_service.ListCustomTargetingKeysResponse:
        """Post-rpc interceptor for list_custom_targeting_keys

        Override in a subclass to manipulate the response
        after it is returned by the CustomTargetingKeyService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CustomTargetingKeyService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CustomTargetingKeyService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CustomTargetingKeyServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CustomTargetingKeyServiceRestInterceptor


class CustomTargetingKeyServiceRestTransport(
    _BaseCustomTargetingKeyServiceRestTransport
):
    """REST backend synchronous transport for CustomTargetingKeyService.

    Provides methods for handling ``CustomTargetingKey`` objects.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "admanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CustomTargetingKeyServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'admanager.googleapis.com').
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
        self._interceptor = interceptor or CustomTargetingKeyServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetCustomTargetingKey(
        _BaseCustomTargetingKeyServiceRestTransport._BaseGetCustomTargetingKey,
        CustomTargetingKeyServiceRestStub,
    ):
        def __hash__(self):
            return hash("CustomTargetingKeyServiceRestTransport.GetCustomTargetingKey")

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
            request: custom_targeting_key_service.GetCustomTargetingKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> custom_targeting_key_messages.CustomTargetingKey:
            r"""Call the get custom targeting key method over HTTP.

            Args:
                request (~.custom_targeting_key_service.GetCustomTargetingKeyRequest):
                    The request object. Request object for ``GetCustomTargetingKey`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.custom_targeting_key_messages.CustomTargetingKey:
                    The ``CustomTargetingKey`` resource.
            """

            http_options = (
                _BaseCustomTargetingKeyServiceRestTransport._BaseGetCustomTargetingKey._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_custom_targeting_key(
                request, metadata
            )
            transcoded_request = _BaseCustomTargetingKeyServiceRestTransport._BaseGetCustomTargetingKey._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCustomTargetingKeyServiceRestTransport._BaseGetCustomTargetingKey._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.CustomTargetingKeyServiceClient.GetCustomTargetingKey",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "GetCustomTargetingKey",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CustomTargetingKeyServiceRestTransport._GetCustomTargetingKey._get_response(
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
            resp = custom_targeting_key_messages.CustomTargetingKey()
            pb_resp = custom_targeting_key_messages.CustomTargetingKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_custom_targeting_key(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        custom_targeting_key_messages.CustomTargetingKey.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.CustomTargetingKeyServiceClient.get_custom_targeting_key",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "GetCustomTargetingKey",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCustomTargetingKeys(
        _BaseCustomTargetingKeyServiceRestTransport._BaseListCustomTargetingKeys,
        CustomTargetingKeyServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "CustomTargetingKeyServiceRestTransport.ListCustomTargetingKeys"
            )

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
            request: custom_targeting_key_service.ListCustomTargetingKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> custom_targeting_key_service.ListCustomTargetingKeysResponse:
            r"""Call the list custom targeting
            keys method over HTTP.

                Args:
                    request (~.custom_targeting_key_service.ListCustomTargetingKeysRequest):
                        The request object. Request object for ``ListCustomTargetingKeys`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.custom_targeting_key_service.ListCustomTargetingKeysResponse:
                        Response object for ``ListCustomTargetingKeysRequest``
                    containing matching ``CustomTargetingKey`` objects.

            """

            http_options = (
                _BaseCustomTargetingKeyServiceRestTransport._BaseListCustomTargetingKeys._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_custom_targeting_keys(
                request, metadata
            )
            transcoded_request = _BaseCustomTargetingKeyServiceRestTransport._BaseListCustomTargetingKeys._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCustomTargetingKeyServiceRestTransport._BaseListCustomTargetingKeys._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.CustomTargetingKeyServiceClient.ListCustomTargetingKeys",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "ListCustomTargetingKeys",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CustomTargetingKeyServiceRestTransport._ListCustomTargetingKeys._get_response(
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
            resp = custom_targeting_key_service.ListCustomTargetingKeysResponse()
            pb_resp = custom_targeting_key_service.ListCustomTargetingKeysResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_custom_targeting_keys(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = custom_targeting_key_service.ListCustomTargetingKeysResponse.to_json(
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
                    "Received response for google.ads.admanager_v1.CustomTargetingKeyServiceClient.list_custom_targeting_keys",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "ListCustomTargetingKeys",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get_custom_targeting_key(
        self,
    ) -> Callable[
        [custom_targeting_key_service.GetCustomTargetingKeyRequest],
        custom_targeting_key_messages.CustomTargetingKey,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomTargetingKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_targeting_keys(
        self,
    ) -> Callable[
        [custom_targeting_key_service.ListCustomTargetingKeysRequest],
        custom_targeting_key_service.ListCustomTargetingKeysResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomTargetingKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseCustomTargetingKeyServiceRestTransport._BaseGetOperation,
        CustomTargetingKeyServiceRestStub,
    ):
        def __hash__(self):
            return hash("CustomTargetingKeyServiceRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseCustomTargetingKeyServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseCustomTargetingKeyServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCustomTargetingKeyServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.CustomTargetingKeyServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                CustomTargetingKeyServiceRestTransport._GetOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.CustomTargetingKeyServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.CustomTargetingKeyService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CustomTargetingKeyServiceRestTransport",)
