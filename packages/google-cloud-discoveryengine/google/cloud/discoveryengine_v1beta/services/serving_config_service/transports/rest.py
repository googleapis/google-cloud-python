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

from google.cloud.discoveryengine_v1beta.types import (
    serving_config as gcd_serving_config,
)
from google.cloud.discoveryengine_v1beta.types import serving_config
from google.cloud.discoveryengine_v1beta.types import serving_config_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseServingConfigServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ServingConfigServiceRestInterceptor:
    """Interceptor for ServingConfigService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ServingConfigServiceRestTransport.

    .. code-block:: python
        class MyCustomServingConfigServiceInterceptor(ServingConfigServiceRestInterceptor):
            def pre_get_serving_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_serving_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_serving_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_serving_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_serving_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_serving_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ServingConfigServiceRestTransport(interceptor=MyCustomServingConfigServiceInterceptor())
        client = ServingConfigServiceClient(transport=transport)


    """

    def pre_get_serving_config(
        self,
        request: serving_config_service.GetServingConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        serving_config_service.GetServingConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_serving_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_get_serving_config(
        self, response: serving_config.ServingConfig
    ) -> serving_config.ServingConfig:
        """Post-rpc interceptor for get_serving_config

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_list_serving_configs(
        self,
        request: serving_config_service.ListServingConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        serving_config_service.ListServingConfigsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_serving_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_list_serving_configs(
        self, response: serving_config_service.ListServingConfigsResponse
    ) -> serving_config_service.ListServingConfigsResponse:
        """Post-rpc interceptor for list_serving_configs

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_update_serving_config(
        self,
        request: serving_config_service.UpdateServingConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        serving_config_service.UpdateServingConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_serving_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_update_serving_config(
        self, response: gcd_serving_config.ServingConfig
    ) -> gcd_serving_config.ServingConfig:
        """Post-rpc interceptor for update_serving_config

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
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
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
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
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
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
        before they are sent to the ServingConfigService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ServingConfigService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ServingConfigServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ServingConfigServiceRestInterceptor


class ServingConfigServiceRestTransport(_BaseServingConfigServiceRestTransport):
    """REST backend synchronous transport for ServingConfigService.

    Service for operations related to
    [ServingConfig][google.cloud.discoveryengine.v1beta.ServingConfig].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ServingConfigServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
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
        self._interceptor = interceptor or ServingConfigServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetServingConfig(
        _BaseServingConfigServiceRestTransport._BaseGetServingConfig,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.GetServingConfig")

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
            request: serving_config_service.GetServingConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> serving_config.ServingConfig:
            r"""Call the get serving config method over HTTP.

            Args:
                request (~.serving_config_service.GetServingConfigRequest):
                    The request object. Request for GetServingConfig method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.serving_config.ServingConfig:
                    Configures metadata that is used to
                generate serving time results (e.g.
                search results or recommendation
                predictions). The ServingConfig is
                passed in the search and predict request
                and generates results.

            """

            http_options = (
                _BaseServingConfigServiceRestTransport._BaseGetServingConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_serving_config(
                request, metadata
            )
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseGetServingConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseGetServingConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ServingConfigServiceRestTransport._GetServingConfig._get_response(
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
            resp = serving_config.ServingConfig()
            pb_resp = serving_config.ServingConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_serving_config(resp)
            return resp

    class _ListServingConfigs(
        _BaseServingConfigServiceRestTransport._BaseListServingConfigs,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.ListServingConfigs")

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
            request: serving_config_service.ListServingConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> serving_config_service.ListServingConfigsResponse:
            r"""Call the list serving configs method over HTTP.

            Args:
                request (~.serving_config_service.ListServingConfigsRequest):
                    The request object. Request for ListServingConfigs
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.serving_config_service.ListServingConfigsResponse:
                    Response for ListServingConfigs
                method.

            """

            http_options = (
                _BaseServingConfigServiceRestTransport._BaseListServingConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_serving_configs(
                request, metadata
            )
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseListServingConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseListServingConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ServingConfigServiceRestTransport._ListServingConfigs._get_response(
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
            resp = serving_config_service.ListServingConfigsResponse()
            pb_resp = serving_config_service.ListServingConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_serving_configs(resp)
            return resp

    class _UpdateServingConfig(
        _BaseServingConfigServiceRestTransport._BaseUpdateServingConfig,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.UpdateServingConfig")

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
            request: serving_config_service.UpdateServingConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_serving_config.ServingConfig:
            r"""Call the update serving config method over HTTP.

            Args:
                request (~.serving_config_service.UpdateServingConfigRequest):
                    The request object. Request for UpdateServingConfig
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_serving_config.ServingConfig:
                    Configures metadata that is used to
                generate serving time results (e.g.
                search results or recommendation
                predictions). The ServingConfig is
                passed in the search and predict request
                and generates results.

            """

            http_options = (
                _BaseServingConfigServiceRestTransport._BaseUpdateServingConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_serving_config(
                request, metadata
            )
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseUpdateServingConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseServingConfigServiceRestTransport._BaseUpdateServingConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseUpdateServingConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ServingConfigServiceRestTransport._UpdateServingConfig._get_response(
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
            resp = gcd_serving_config.ServingConfig()
            pb_resp = gcd_serving_config.ServingConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_serving_config(resp)
            return resp

    @property
    def get_serving_config(
        self,
    ) -> Callable[
        [serving_config_service.GetServingConfigRequest], serving_config.ServingConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServingConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_serving_configs(
        self,
    ) -> Callable[
        [serving_config_service.ListServingConfigsRequest],
        serving_config_service.ListServingConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServingConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_serving_config(
        self,
    ) -> Callable[
        [serving_config_service.UpdateServingConfigRequest],
        gcd_serving_config.ServingConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateServingConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseServingConfigServiceRestTransport._BaseCancelOperation,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.CancelOperation")

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
                _BaseServingConfigServiceRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseServingConfigServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServingConfigServiceRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseServingConfigServiceRestTransport._BaseGetOperation,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.GetOperation")

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
                _BaseServingConfigServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServingConfigServiceRestTransport._GetOperation._get_response(
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
        _BaseServingConfigServiceRestTransport._BaseListOperations,
        ServingConfigServiceRestStub,
    ):
        def __hash__(self):
            return hash("ServingConfigServiceRestTransport.ListOperations")

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
                _BaseServingConfigServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseServingConfigServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseServingConfigServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ServingConfigServiceRestTransport._ListOperations._get_response(
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


__all__ = ("ServingConfigServiceRestTransport",)
