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
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ads.admanager_v1.types import (
    operating_system_version_messages,
    operating_system_version_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseOperatingSystemVersionServiceRestTransport

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

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class OperatingSystemVersionServiceRestInterceptor:
    """Interceptor for OperatingSystemVersionService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the OperatingSystemVersionServiceRestTransport.

    .. code-block:: python
        class MyCustomOperatingSystemVersionServiceInterceptor(OperatingSystemVersionServiceRestInterceptor):
            def pre_get_operating_system_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_operating_system_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_operating_system_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_operating_system_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OperatingSystemVersionServiceRestTransport(interceptor=MyCustomOperatingSystemVersionServiceInterceptor())
        client = OperatingSystemVersionServiceClient(transport=transport)


    """

    def pre_get_operating_system_version(
        self,
        request: operating_system_version_service.GetOperatingSystemVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operating_system_version_service.GetOperatingSystemVersionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_operating_system_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OperatingSystemVersionService server.
        """
        return request, metadata

    def post_get_operating_system_version(
        self, response: operating_system_version_messages.OperatingSystemVersion
    ) -> operating_system_version_messages.OperatingSystemVersion:
        """Post-rpc interceptor for get_operating_system_version

        DEPRECATED. Please use the `post_get_operating_system_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OperatingSystemVersionService server but before
        it is returned to user code. This `post_get_operating_system_version` interceptor runs
        before the `post_get_operating_system_version_with_metadata` interceptor.
        """
        return response

    def post_get_operating_system_version_with_metadata(
        self,
        response: operating_system_version_messages.OperatingSystemVersion,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operating_system_version_messages.OperatingSystemVersion,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for get_operating_system_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OperatingSystemVersionService server but before it is returned to user code.

        We recommend only using this `post_get_operating_system_version_with_metadata`
        interceptor in new development instead of the `post_get_operating_system_version` interceptor.
        When both interceptors are used, this `post_get_operating_system_version_with_metadata` interceptor runs after the
        `post_get_operating_system_version` interceptor. The (possibly modified) response returned by
        `post_get_operating_system_version` will be passed to
        `post_get_operating_system_version_with_metadata`.
        """
        return response, metadata

    def pre_list_operating_system_versions(
        self,
        request: operating_system_version_service.ListOperatingSystemVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operating_system_version_service.ListOperatingSystemVersionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_operating_system_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OperatingSystemVersionService server.
        """
        return request, metadata

    def post_list_operating_system_versions(
        self,
        response: operating_system_version_service.ListOperatingSystemVersionsResponse,
    ) -> operating_system_version_service.ListOperatingSystemVersionsResponse:
        """Post-rpc interceptor for list_operating_system_versions

        DEPRECATED. Please use the `post_list_operating_system_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the OperatingSystemVersionService server but before
        it is returned to user code. This `post_list_operating_system_versions` interceptor runs
        before the `post_list_operating_system_versions_with_metadata` interceptor.
        """
        return response

    def post_list_operating_system_versions_with_metadata(
        self,
        response: operating_system_version_service.ListOperatingSystemVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operating_system_version_service.ListOperatingSystemVersionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_operating_system_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the OperatingSystemVersionService server but before it is returned to user code.

        We recommend only using this `post_list_operating_system_versions_with_metadata`
        interceptor in new development instead of the `post_list_operating_system_versions` interceptor.
        When both interceptors are used, this `post_list_operating_system_versions_with_metadata` interceptor runs after the
        `post_list_operating_system_versions` interceptor. The (possibly modified) response returned by
        `post_list_operating_system_versions` will be passed to
        `post_list_operating_system_versions_with_metadata`.
        """
        return response, metadata

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OperatingSystemVersionService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the OperatingSystemVersionService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class OperatingSystemVersionServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: OperatingSystemVersionServiceRestInterceptor


class OperatingSystemVersionServiceRestTransport(
    _BaseOperatingSystemVersionServiceRestTransport
):
    """REST backend synchronous transport for OperatingSystemVersionService.

    Provides methods for handling ``OperatingSystemVersion`` objects.

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
        interceptor: Optional[OperatingSystemVersionServiceRestInterceptor] = None,
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
        self._interceptor = (
            interceptor or OperatingSystemVersionServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _GetOperatingSystemVersion(
        _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperatingSystemVersion,
        OperatingSystemVersionServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "OperatingSystemVersionServiceRestTransport.GetOperatingSystemVersion"
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
            request: operating_system_version_service.GetOperatingSystemVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operating_system_version_messages.OperatingSystemVersion:
            r"""Call the get operating system
            version method over HTTP.

                Args:
                    request (~.operating_system_version_service.GetOperatingSystemVersionRequest):
                        The request object. Request object for ``GetOperatingSystemVersion`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operating_system_version_messages.OperatingSystemVersion:
                        Represents a specific version of an
                    operating system.

            """

            http_options = (
                _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperatingSystemVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operating_system_version(
                request, metadata
            )
            transcoded_request = _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperatingSystemVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperatingSystemVersion._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.OperatingSystemVersionServiceClient.GetOperatingSystemVersion",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
                        "rpcName": "GetOperatingSystemVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OperatingSystemVersionServiceRestTransport._GetOperatingSystemVersion._get_response(
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
            resp = operating_system_version_messages.OperatingSystemVersion()
            pb_resp = operating_system_version_messages.OperatingSystemVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_operating_system_version(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_operating_system_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = operating_system_version_messages.OperatingSystemVersion.to_json(
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
                    "Received response for google.ads.admanager_v1.OperatingSystemVersionServiceClient.get_operating_system_version",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
                        "rpcName": "GetOperatingSystemVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListOperatingSystemVersions(
        _BaseOperatingSystemVersionServiceRestTransport._BaseListOperatingSystemVersions,
        OperatingSystemVersionServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "OperatingSystemVersionServiceRestTransport.ListOperatingSystemVersions"
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
            request: operating_system_version_service.ListOperatingSystemVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operating_system_version_service.ListOperatingSystemVersionsResponse:
            r"""Call the list operating system
            versions method over HTTP.

                Args:
                    request (~.operating_system_version_service.ListOperatingSystemVersionsRequest):
                        The request object. Request object for ``ListOperatingSystemVersions``
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operating_system_version_service.ListOperatingSystemVersionsResponse:
                        Response object for
                    ``ListOperatingSystemVersionsRequest`` containing
                    matching ``OperatingSystemVersion`` objects.

            """

            http_options = (
                _BaseOperatingSystemVersionServiceRestTransport._BaseListOperatingSystemVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operating_system_versions(
                request, metadata
            )
            transcoded_request = _BaseOperatingSystemVersionServiceRestTransport._BaseListOperatingSystemVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOperatingSystemVersionServiceRestTransport._BaseListOperatingSystemVersions._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.OperatingSystemVersionServiceClient.ListOperatingSystemVersions",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
                        "rpcName": "ListOperatingSystemVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = OperatingSystemVersionServiceRestTransport._ListOperatingSystemVersions._get_response(
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
            resp = (
                operating_system_version_service.ListOperatingSystemVersionsResponse()
            )
            pb_resp = (
                operating_system_version_service.ListOperatingSystemVersionsResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_operating_system_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_list_operating_system_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = operating_system_version_service.ListOperatingSystemVersionsResponse.to_json(
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
                    "Received response for google.ads.admanager_v1.OperatingSystemVersionServiceClient.list_operating_system_versions",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
                        "rpcName": "ListOperatingSystemVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get_operating_system_version(
        self,
    ) -> Callable[
        [operating_system_version_service.GetOperatingSystemVersionRequest],
        operating_system_version_messages.OperatingSystemVersion,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOperatingSystemVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_operating_system_versions(
        self,
    ) -> Callable[
        [operating_system_version_service.ListOperatingSystemVersionsRequest],
        operating_system_version_service.ListOperatingSystemVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOperatingSystemVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperation,
        OperatingSystemVersionServiceRestStub,
    ):
        def __hash__(self):
            return hash("OperatingSystemVersionServiceRestTransport.GetOperation")

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
                _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseOperatingSystemVersionServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.OperatingSystemVersionServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                OperatingSystemVersionServiceRestTransport._GetOperation._get_response(
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
                    "Received response for google.ads.admanager_v1.OperatingSystemVersionServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.OperatingSystemVersionService",
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


__all__ = ("OperatingSystemVersionServiceRestTransport",)
