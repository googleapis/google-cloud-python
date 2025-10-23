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

from google.ads.admanager_v1.types import content_label_messages, content_label_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseContentLabelServiceRestTransport

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


class ContentLabelServiceRestInterceptor:
    """Interceptor for ContentLabelService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ContentLabelServiceRestTransport.

    .. code-block:: python
        class MyCustomContentLabelServiceInterceptor(ContentLabelServiceRestInterceptor):
            def pre_get_content_label(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_content_label(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_content_labels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_content_labels(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ContentLabelServiceRestTransport(interceptor=MyCustomContentLabelServiceInterceptor())
        client = ContentLabelServiceClient(transport=transport)


    """

    def pre_get_content_label(
        self,
        request: content_label_service.GetContentLabelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        content_label_service.GetContentLabelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_content_label

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContentLabelService server.
        """
        return request, metadata

    def post_get_content_label(
        self, response: content_label_messages.ContentLabel
    ) -> content_label_messages.ContentLabel:
        """Post-rpc interceptor for get_content_label

        DEPRECATED. Please use the `post_get_content_label_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContentLabelService server but before
        it is returned to user code. This `post_get_content_label` interceptor runs
        before the `post_get_content_label_with_metadata` interceptor.
        """
        return response

    def post_get_content_label_with_metadata(
        self,
        response: content_label_messages.ContentLabel,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        content_label_messages.ContentLabel, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_content_label

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContentLabelService server but before it is returned to user code.

        We recommend only using this `post_get_content_label_with_metadata`
        interceptor in new development instead of the `post_get_content_label` interceptor.
        When both interceptors are used, this `post_get_content_label_with_metadata` interceptor runs after the
        `post_get_content_label` interceptor. The (possibly modified) response returned by
        `post_get_content_label` will be passed to
        `post_get_content_label_with_metadata`.
        """
        return response, metadata

    def pre_list_content_labels(
        self,
        request: content_label_service.ListContentLabelsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        content_label_service.ListContentLabelsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_content_labels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContentLabelService server.
        """
        return request, metadata

    def post_list_content_labels(
        self, response: content_label_service.ListContentLabelsResponse
    ) -> content_label_service.ListContentLabelsResponse:
        """Post-rpc interceptor for list_content_labels

        DEPRECATED. Please use the `post_list_content_labels_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContentLabelService server but before
        it is returned to user code. This `post_list_content_labels` interceptor runs
        before the `post_list_content_labels_with_metadata` interceptor.
        """
        return response

    def post_list_content_labels_with_metadata(
        self,
        response: content_label_service.ListContentLabelsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        content_label_service.ListContentLabelsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_content_labels

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContentLabelService server but before it is returned to user code.

        We recommend only using this `post_list_content_labels_with_metadata`
        interceptor in new development instead of the `post_list_content_labels` interceptor.
        When both interceptors are used, this `post_list_content_labels_with_metadata` interceptor runs after the
        `post_list_content_labels` interceptor. The (possibly modified) response returned by
        `post_list_content_labels` will be passed to
        `post_list_content_labels_with_metadata`.
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
        before they are sent to the ContentLabelService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContentLabelService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ContentLabelServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ContentLabelServiceRestInterceptor


class ContentLabelServiceRestTransport(_BaseContentLabelServiceRestTransport):
    """REST backend synchronous transport for ContentLabelService.

    Provides methods for handling ``ContentLabel`` objects.

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
        interceptor: Optional[ContentLabelServiceRestInterceptor] = None,
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

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
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
        self._interceptor = interceptor or ContentLabelServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetContentLabel(
        _BaseContentLabelServiceRestTransport._BaseGetContentLabel,
        ContentLabelServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContentLabelServiceRestTransport.GetContentLabel")

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
            request: content_label_service.GetContentLabelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> content_label_messages.ContentLabel:
            r"""Call the get content label method over HTTP.

            Args:
                request (~.content_label_service.GetContentLabelRequest):
                    The request object. Request object for ``GetContentLabel`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.content_label_messages.ContentLabel:
                    A content label.
            """

            http_options = (
                _BaseContentLabelServiceRestTransport._BaseGetContentLabel._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_content_label(
                request, metadata
            )
            transcoded_request = _BaseContentLabelServiceRestTransport._BaseGetContentLabel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContentLabelServiceRestTransport._BaseGetContentLabel._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContentLabelServiceClient.GetContentLabel",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
                        "rpcName": "GetContentLabel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContentLabelServiceRestTransport._GetContentLabel._get_response(
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
            resp = content_label_messages.ContentLabel()
            pb_resp = content_label_messages.ContentLabel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_content_label(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_content_label_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = content_label_messages.ContentLabel.to_json(
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
                    "Received response for google.ads.admanager_v1.ContentLabelServiceClient.get_content_label",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
                        "rpcName": "GetContentLabel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListContentLabels(
        _BaseContentLabelServiceRestTransport._BaseListContentLabels,
        ContentLabelServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContentLabelServiceRestTransport.ListContentLabels")

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
            request: content_label_service.ListContentLabelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> content_label_service.ListContentLabelsResponse:
            r"""Call the list content labels method over HTTP.

            Args:
                request (~.content_label_service.ListContentLabelsRequest):
                    The request object. Request object for ``ListContentLabels`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.content_label_service.ListContentLabelsResponse:
                    Response object for ``ListContentLabelsRequest``
                containing matching ``ContentLabel`` objects.

            """

            http_options = (
                _BaseContentLabelServiceRestTransport._BaseListContentLabels._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_content_labels(
                request, metadata
            )
            transcoded_request = _BaseContentLabelServiceRestTransport._BaseListContentLabels._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContentLabelServiceRestTransport._BaseListContentLabels._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContentLabelServiceClient.ListContentLabels",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
                        "rpcName": "ListContentLabels",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ContentLabelServiceRestTransport._ListContentLabels._get_response(
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
            resp = content_label_service.ListContentLabelsResponse()
            pb_resp = content_label_service.ListContentLabelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_content_labels(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_content_labels_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        content_label_service.ListContentLabelsResponse.to_json(
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
                    "Received response for google.ads.admanager_v1.ContentLabelServiceClient.list_content_labels",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
                        "rpcName": "ListContentLabels",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get_content_label(
        self,
    ) -> Callable[
        [content_label_service.GetContentLabelRequest],
        content_label_messages.ContentLabel,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetContentLabel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_content_labels(
        self,
    ) -> Callable[
        [content_label_service.ListContentLabelsRequest],
        content_label_service.ListContentLabelsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListContentLabels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseContentLabelServiceRestTransport._BaseGetOperation,
        ContentLabelServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContentLabelServiceRestTransport.GetOperation")

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
                _BaseContentLabelServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseContentLabelServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContentLabelServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContentLabelServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContentLabelServiceRestTransport._GetOperation._get_response(
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
                    "Received response for google.ads.admanager_v1.ContentLabelServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContentLabelService",
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


__all__ = ("ContentLabelServiceRestTransport",)
