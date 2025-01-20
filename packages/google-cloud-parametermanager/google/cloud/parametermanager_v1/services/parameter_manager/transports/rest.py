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
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.parametermanager_v1.types import service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseParameterManagerRestTransport

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


class ParameterManagerRestInterceptor:
    """Interceptor for ParameterManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ParameterManagerRestTransport.

    .. code-block:: python
        class MyCustomParameterManagerInterceptor(ParameterManagerRestInterceptor):
            def pre_create_parameter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_parameter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_parameter_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_parameter_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_parameter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_parameter_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_parameter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_parameter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_parameter_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_parameter_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_parameters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_parameters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_parameter_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_parameter_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_render_parameter_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_render_parameter_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_parameter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_parameter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_parameter_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_parameter_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ParameterManagerRestTransport(interceptor=MyCustomParameterManagerInterceptor())
        client = ParameterManagerClient(transport=transport)


    """

    def pre_create_parameter(
        self,
        request: service.CreateParameterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateParameterRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_parameter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_create_parameter(self, response: service.Parameter) -> service.Parameter:
        """Post-rpc interceptor for create_parameter

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_parameter_version(
        self,
        request: service.CreateParameterVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.CreateParameterVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_parameter_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_create_parameter_version(
        self, response: service.ParameterVersion
    ) -> service.ParameterVersion:
        """Post-rpc interceptor for create_parameter_version

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_parameter(
        self,
        request: service.DeleteParameterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteParameterRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_parameter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def pre_delete_parameter_version(
        self,
        request: service.DeleteParameterVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.DeleteParameterVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_parameter_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def pre_get_parameter(
        self,
        request: service.GetParameterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetParameterRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_parameter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_get_parameter(self, response: service.Parameter) -> service.Parameter:
        """Post-rpc interceptor for get_parameter

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_parameter_version(
        self,
        request: service.GetParameterVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GetParameterVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_parameter_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_get_parameter_version(
        self, response: service.ParameterVersion
    ) -> service.ParameterVersion:
        """Post-rpc interceptor for get_parameter_version

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_parameters(
        self,
        request: service.ListParametersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListParametersRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_parameters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_list_parameters(
        self, response: service.ListParametersResponse
    ) -> service.ListParametersResponse:
        """Post-rpc interceptor for list_parameters

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_parameter_versions(
        self,
        request: service.ListParameterVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListParameterVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_parameter_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_list_parameter_versions(
        self, response: service.ListParameterVersionsResponse
    ) -> service.ListParameterVersionsResponse:
        """Post-rpc interceptor for list_parameter_versions

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_render_parameter_version(
        self,
        request: service.RenderParameterVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.RenderParameterVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for render_parameter_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_render_parameter_version(
        self, response: service.RenderParameterVersionResponse
    ) -> service.RenderParameterVersionResponse:
        """Post-rpc interceptor for render_parameter_version

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_parameter(
        self,
        request: service.UpdateParameterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateParameterRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_parameter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_update_parameter(self, response: service.Parameter) -> service.Parameter:
        """Post-rpc interceptor for update_parameter

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_parameter_version(
        self,
        request: service.UpdateParameterVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.UpdateParameterVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_parameter_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_update_parameter_version(
        self, response: service.ParameterVersion
    ) -> service.ParameterVersion:
        """Post-rpc interceptor for update_parameter_version

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ParameterManager server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ParameterManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ParameterManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ParameterManagerRestInterceptor


class ParameterManagerRestTransport(_BaseParameterManagerRestTransport):
    """REST backend synchronous transport for ParameterManager.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "parametermanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ParameterManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'parametermanager.googleapis.com').
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
        self._interceptor = interceptor or ParameterManagerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateParameter(
        _BaseParameterManagerRestTransport._BaseCreateParameter,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.CreateParameter")

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
            request: service.CreateParameterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Parameter:
            r"""Call the create parameter method over HTTP.

            Args:
                request (~.service.CreateParameterRequest):
                    The request object. Message for creating a Parameter
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Parameter:
                    Message describing Parameter resource
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseCreateParameter._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_parameter(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseCreateParameter._get_transcoded_request(
                http_options, request
            )

            body = _BaseParameterManagerRestTransport._BaseCreateParameter._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseCreateParameter._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.CreateParameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "CreateParameter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._CreateParameter._get_response(
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
            resp = service.Parameter()
            pb_resp = service.Parameter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_parameter(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Parameter.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.create_parameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "CreateParameter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateParameterVersion(
        _BaseParameterManagerRestTransport._BaseCreateParameterVersion,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.CreateParameterVersion")

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
            request: service.CreateParameterVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ParameterVersion:
            r"""Call the create parameter version method over HTTP.

            Args:
                request (~.service.CreateParameterVersionRequest):
                    The request object. Message for creating a
                ParameterVersion
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ParameterVersion:
                    Message describing ParameterVersion
                resource

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseCreateParameterVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_parameter_version(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseCreateParameterVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseParameterManagerRestTransport._BaseCreateParameterVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseCreateParameterVersion._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.CreateParameterVersion",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "CreateParameterVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ParameterManagerRestTransport._CreateParameterVersion._get_response(
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
            resp = service.ParameterVersion()
            pb_resp = service.ParameterVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_parameter_version(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ParameterVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.create_parameter_version",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "CreateParameterVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteParameter(
        _BaseParameterManagerRestTransport._BaseDeleteParameter,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.DeleteParameter")

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
            request: service.DeleteParameterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete parameter method over HTTP.

            Args:
                request (~.service.DeleteParameterRequest):
                    The request object. Message for deleting a Parameter
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseDeleteParameter._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_parameter(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseDeleteParameter._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseDeleteParameter._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.DeleteParameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "DeleteParameter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._DeleteParameter._get_response(
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

    class _DeleteParameterVersion(
        _BaseParameterManagerRestTransport._BaseDeleteParameterVersion,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.DeleteParameterVersion")

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
            request: service.DeleteParameterVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete parameter version method over HTTP.

            Args:
                request (~.service.DeleteParameterVersionRequest):
                    The request object. Message for deleting a
                ParameterVersion
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseDeleteParameterVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_parameter_version(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseDeleteParameterVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseDeleteParameterVersion._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.DeleteParameterVersion",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "DeleteParameterVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ParameterManagerRestTransport._DeleteParameterVersion._get_response(
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

    class _GetParameter(
        _BaseParameterManagerRestTransport._BaseGetParameter, ParameterManagerRestStub
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.GetParameter")

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
            request: service.GetParameterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Parameter:
            r"""Call the get parameter method over HTTP.

            Args:
                request (~.service.GetParameterRequest):
                    The request object. Message for getting a Parameter
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Parameter:
                    Message describing Parameter resource
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseGetParameter._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_parameter(request, metadata)
            transcoded_request = _BaseParameterManagerRestTransport._BaseGetParameter._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseGetParameter._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.GetParameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetParameter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._GetParameter._get_response(
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
            resp = service.Parameter()
            pb_resp = service.Parameter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_parameter(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Parameter.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.get_parameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetParameter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetParameterVersion(
        _BaseParameterManagerRestTransport._BaseGetParameterVersion,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.GetParameterVersion")

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
            request: service.GetParameterVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ParameterVersion:
            r"""Call the get parameter version method over HTTP.

            Args:
                request (~.service.GetParameterVersionRequest):
                    The request object. Message for getting a
                ParameterVersion
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ParameterVersion:
                    Message describing ParameterVersion
                resource

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseGetParameterVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_parameter_version(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseGetParameterVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseGetParameterVersion._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.GetParameterVersion",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetParameterVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._GetParameterVersion._get_response(
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
            resp = service.ParameterVersion()
            pb_resp = service.ParameterVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_parameter_version(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ParameterVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.get_parameter_version",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetParameterVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListParameters(
        _BaseParameterManagerRestTransport._BaseListParameters, ParameterManagerRestStub
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.ListParameters")

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
            request: service.ListParametersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListParametersResponse:
            r"""Call the list parameters method over HTTP.

            Args:
                request (~.service.ListParametersRequest):
                    The request object. Message for requesting list of
                Parameters
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListParametersResponse:
                    Message for response to listing
                Parameters

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseListParameters._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_parameters(request, metadata)
            transcoded_request = _BaseParameterManagerRestTransport._BaseListParameters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseListParameters._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.ListParameters",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListParameters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._ListParameters._get_response(
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
            resp = service.ListParametersResponse()
            pb_resp = service.ListParametersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_parameters(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListParametersResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.list_parameters",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListParameters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListParameterVersions(
        _BaseParameterManagerRestTransport._BaseListParameterVersions,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.ListParameterVersions")

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
            request: service.ListParameterVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListParameterVersionsResponse:
            r"""Call the list parameter versions method over HTTP.

            Args:
                request (~.service.ListParameterVersionsRequest):
                    The request object. Message for requesting list of
                ParameterVersions
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListParameterVersionsResponse:
                    Message for response to listing
                ParameterVersions

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseListParameterVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_parameter_versions(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseListParameterVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseListParameterVersions._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.ListParameterVersions",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListParameterVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ParameterManagerRestTransport._ListParameterVersions._get_response(
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
            resp = service.ListParameterVersionsResponse()
            pb_resp = service.ListParameterVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_parameter_versions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListParameterVersionsResponse.to_json(
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
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.list_parameter_versions",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListParameterVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RenderParameterVersion(
        _BaseParameterManagerRestTransport._BaseRenderParameterVersion,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.RenderParameterVersion")

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
            request: service.RenderParameterVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.RenderParameterVersionResponse:
            r"""Call the render parameter version method over HTTP.

            Args:
                request (~.service.RenderParameterVersionRequest):
                    The request object. Message for getting a
                ParameterVersionRender
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.RenderParameterVersionResponse:
                    Message describing
                RenderParameterVersionResponse resource

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseRenderParameterVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_render_parameter_version(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseRenderParameterVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseRenderParameterVersion._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.RenderParameterVersion",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "RenderParameterVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ParameterManagerRestTransport._RenderParameterVersion._get_response(
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
            resp = service.RenderParameterVersionResponse()
            pb_resp = service.RenderParameterVersionResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_render_parameter_version(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.RenderParameterVersionResponse.to_json(
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
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.render_parameter_version",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "RenderParameterVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateParameter(
        _BaseParameterManagerRestTransport._BaseUpdateParameter,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.UpdateParameter")

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
            request: service.UpdateParameterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Parameter:
            r"""Call the update parameter method over HTTP.

            Args:
                request (~.service.UpdateParameterRequest):
                    The request object. Message for updating a Parameter
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Parameter:
                    Message describing Parameter resource
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseUpdateParameter._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_parameter(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseUpdateParameter._get_transcoded_request(
                http_options, request
            )

            body = _BaseParameterManagerRestTransport._BaseUpdateParameter._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseUpdateParameter._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.UpdateParameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "UpdateParameter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._UpdateParameter._get_response(
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
            resp = service.Parameter()
            pb_resp = service.Parameter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_parameter(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Parameter.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.update_parameter",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "UpdateParameter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateParameterVersion(
        _BaseParameterManagerRestTransport._BaseUpdateParameterVersion,
        ParameterManagerRestStub,
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.UpdateParameterVersion")

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
            request: service.UpdateParameterVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ParameterVersion:
            r"""Call the update parameter version method over HTTP.

            Args:
                request (~.service.UpdateParameterVersionRequest):
                    The request object. Message for updating a
                ParameterVersion
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ParameterVersion:
                    Message describing ParameterVersion
                resource

            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseUpdateParameterVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_parameter_version(
                request, metadata
            )
            transcoded_request = _BaseParameterManagerRestTransport._BaseUpdateParameterVersion._get_transcoded_request(
                http_options, request
            )

            body = _BaseParameterManagerRestTransport._BaseUpdateParameterVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseUpdateParameterVersion._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.UpdateParameterVersion",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "UpdateParameterVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ParameterManagerRestTransport._UpdateParameterVersion._get_response(
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
            resp = service.ParameterVersion()
            pb_resp = service.ParameterVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_parameter_version(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ParameterVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerClient.update_parameter_version",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "UpdateParameterVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_parameter(
        self,
    ) -> Callable[[service.CreateParameterRequest], service.Parameter]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateParameter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_parameter_version(
        self,
    ) -> Callable[[service.CreateParameterVersionRequest], service.ParameterVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateParameterVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_parameter(
        self,
    ) -> Callable[[service.DeleteParameterRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteParameter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_parameter_version(
        self,
    ) -> Callable[[service.DeleteParameterVersionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteParameterVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_parameter(
        self,
    ) -> Callable[[service.GetParameterRequest], service.Parameter]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetParameter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_parameter_version(
        self,
    ) -> Callable[[service.GetParameterVersionRequest], service.ParameterVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetParameterVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_parameters(
        self,
    ) -> Callable[[service.ListParametersRequest], service.ListParametersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListParameters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_parameter_versions(
        self,
    ) -> Callable[
        [service.ListParameterVersionsRequest], service.ListParameterVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListParameterVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def render_parameter_version(
        self,
    ) -> Callable[
        [service.RenderParameterVersionRequest], service.RenderParameterVersionResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenderParameterVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_parameter(
        self,
    ) -> Callable[[service.UpdateParameterRequest], service.Parameter]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateParameter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_parameter_version(
        self,
    ) -> Callable[[service.UpdateParameterVersionRequest], service.ParameterVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateParameterVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseParameterManagerRestTransport._BaseGetLocation, ParameterManagerRestStub
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.GetLocation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseParameterManagerRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._GetLocation._get_response(
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
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseParameterManagerRestTransport._BaseListLocations, ParameterManagerRestStub
    ):
        def __hash__(self):
            return hash("ParameterManagerRestTransport.ListLocations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseParameterManagerRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseParameterManagerRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseParameterManagerRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.parametermanager_v1.ParameterManagerClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ParameterManagerRestTransport._ListLocations._get_response(
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
                    "Received response for google.cloud.parametermanager_v1.ParameterManagerAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.parametermanager.v1.ParameterManager",
                        "rpcName": "ListLocations",
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


__all__ = ("ParameterManagerRestTransport",)
