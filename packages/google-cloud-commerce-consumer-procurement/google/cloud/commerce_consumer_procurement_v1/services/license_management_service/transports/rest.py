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

from google.cloud.commerce_consumer_procurement_v1.types import (
    license_management_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseLicenseManagementServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class LicenseManagementServiceRestInterceptor:
    """Interceptor for LicenseManagementService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LicenseManagementServiceRestTransport.

    .. code-block:: python
        class MyCustomLicenseManagementServiceInterceptor(LicenseManagementServiceRestInterceptor):
            def pre_assign(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_assign(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enumerate_licensed_users(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enumerate_licensed_users(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_license_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_license_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_unassign(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_unassign(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_license_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_license_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LicenseManagementServiceRestTransport(interceptor=MyCustomLicenseManagementServiceInterceptor())
        client = LicenseManagementServiceClient(transport=transport)


    """

    def pre_assign(
        self,
        request: license_management_service.AssignRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[license_management_service.AssignRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for assign

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_assign(
        self, response: license_management_service.AssignResponse
    ) -> license_management_service.AssignResponse:
        """Post-rpc interceptor for assign

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_enumerate_licensed_users(
        self,
        request: license_management_service.EnumerateLicensedUsersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        license_management_service.EnumerateLicensedUsersRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for enumerate_licensed_users

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_enumerate_licensed_users(
        self, response: license_management_service.EnumerateLicensedUsersResponse
    ) -> license_management_service.EnumerateLicensedUsersResponse:
        """Post-rpc interceptor for enumerate_licensed_users

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_license_pool(
        self,
        request: license_management_service.GetLicensePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        license_management_service.GetLicensePoolRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_license_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_get_license_pool(
        self, response: license_management_service.LicensePool
    ) -> license_management_service.LicensePool:
        """Post-rpc interceptor for get_license_pool

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_unassign(
        self,
        request: license_management_service.UnassignRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[license_management_service.UnassignRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for unassign

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_unassign(
        self, response: license_management_service.UnassignResponse
    ) -> license_management_service.UnassignResponse:
        """Post-rpc interceptor for unassign

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_update_license_pool(
        self,
        request: license_management_service.UpdateLicensePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        license_management_service.UpdateLicensePoolRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_license_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_update_license_pool(
        self, response: license_management_service.LicensePool
    ) -> license_management_service.LicensePool:
        """Post-rpc interceptor for update_license_pool

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
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
        before they are sent to the LicenseManagementService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the LicenseManagementService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LicenseManagementServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LicenseManagementServiceRestInterceptor


class LicenseManagementServiceRestTransport(_BaseLicenseManagementServiceRestTransport):
    """REST backend synchronous transport for LicenseManagementService.

    Service for managing licenses.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudcommerceconsumerprocurement.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LicenseManagementServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudcommerceconsumerprocurement.googleapis.com').
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
        self._interceptor = interceptor or LicenseManagementServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Assign(
        _BaseLicenseManagementServiceRestTransport._BaseAssign,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.Assign")

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
            request: license_management_service.AssignRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> license_management_service.AssignResponse:
            r"""Call the assign method over HTTP.

            Args:
                request (~.license_management_service.AssignRequest):
                    The request object. Request message for
                [LicenseManagementService.Assign][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.Assign].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.license_management_service.AssignResponse:
                    Response message for
                [LicenseManagementService.Assign][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.Assign].

            """

            http_options = (
                _BaseLicenseManagementServiceRestTransport._BaseAssign._get_http_options()
            )
            request, metadata = self._interceptor.pre_assign(request, metadata)
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseAssign._get_transcoded_request(
                http_options, request
            )

            body = _BaseLicenseManagementServiceRestTransport._BaseAssign._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseAssign._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LicenseManagementServiceRestTransport._Assign._get_response(
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
            resp = license_management_service.AssignResponse()
            pb_resp = license_management_service.AssignResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_assign(resp)
            return resp

    class _EnumerateLicensedUsers(
        _BaseLicenseManagementServiceRestTransport._BaseEnumerateLicensedUsers,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.EnumerateLicensedUsers")

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
            request: license_management_service.EnumerateLicensedUsersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> license_management_service.EnumerateLicensedUsersResponse:
            r"""Call the enumerate licensed users method over HTTP.

            Args:
                request (~.license_management_service.EnumerateLicensedUsersRequest):
                    The request object. Request message for
                [LicenseManagementService.EnumerateLicensedUsers][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.EnumerateLicensedUsers].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.license_management_service.EnumerateLicensedUsersResponse:
                    Response message for
                [LicenseManagementService.EnumerateLicensedUsers][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.EnumerateLicensedUsers].

            """

            http_options = (
                _BaseLicenseManagementServiceRestTransport._BaseEnumerateLicensedUsers._get_http_options()
            )
            request, metadata = self._interceptor.pre_enumerate_licensed_users(
                request, metadata
            )
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseEnumerateLicensedUsers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseEnumerateLicensedUsers._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LicenseManagementServiceRestTransport._EnumerateLicensedUsers._get_response(
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
            resp = license_management_service.EnumerateLicensedUsersResponse()
            pb_resp = license_management_service.EnumerateLicensedUsersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enumerate_licensed_users(resp)
            return resp

    class _GetLicensePool(
        _BaseLicenseManagementServiceRestTransport._BaseGetLicensePool,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.GetLicensePool")

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
            request: license_management_service.GetLicensePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> license_management_service.LicensePool:
            r"""Call the get license pool method over HTTP.

            Args:
                request (~.license_management_service.GetLicensePoolRequest):
                    The request object. Request message for getting a license
                pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.license_management_service.LicensePool:
                    A license pool represents a pool of
                licenses that can be assigned to users.

            """

            http_options = (
                _BaseLicenseManagementServiceRestTransport._BaseGetLicensePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_license_pool(
                request, metadata
            )
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseGetLicensePool._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseGetLicensePool._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                LicenseManagementServiceRestTransport._GetLicensePool._get_response(
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
            resp = license_management_service.LicensePool()
            pb_resp = license_management_service.LicensePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_license_pool(resp)
            return resp

    class _Unassign(
        _BaseLicenseManagementServiceRestTransport._BaseUnassign,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.Unassign")

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
            request: license_management_service.UnassignRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> license_management_service.UnassignResponse:
            r"""Call the unassign method over HTTP.

            Args:
                request (~.license_management_service.UnassignRequest):
                    The request object. Request message for
                [LicenseManagementService.Unassign][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.Unassign].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.license_management_service.UnassignResponse:
                    Response message for
                [LicenseManagementService.Unassign][google.cloud.commerce.consumer.procurement.v1.LicenseManagementService.Unassign].

            """

            http_options = (
                _BaseLicenseManagementServiceRestTransport._BaseUnassign._get_http_options()
            )
            request, metadata = self._interceptor.pre_unassign(request, metadata)
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseUnassign._get_transcoded_request(
                http_options, request
            )

            body = _BaseLicenseManagementServiceRestTransport._BaseUnassign._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseUnassign._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LicenseManagementServiceRestTransport._Unassign._get_response(
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
            resp = license_management_service.UnassignResponse()
            pb_resp = license_management_service.UnassignResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_unassign(resp)
            return resp

    class _UpdateLicensePool(
        _BaseLicenseManagementServiceRestTransport._BaseUpdateLicensePool,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.UpdateLicensePool")

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
            request: license_management_service.UpdateLicensePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> license_management_service.LicensePool:
            r"""Call the update license pool method over HTTP.

            Args:
                request (~.license_management_service.UpdateLicensePoolRequest):
                    The request object. Request message for updating a
                license pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.license_management_service.LicensePool:
                    A license pool represents a pool of
                licenses that can be assigned to users.

            """

            http_options = (
                _BaseLicenseManagementServiceRestTransport._BaseUpdateLicensePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_license_pool(
                request, metadata
            )
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseUpdateLicensePool._get_transcoded_request(
                http_options, request
            )

            body = _BaseLicenseManagementServiceRestTransport._BaseUpdateLicensePool._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseUpdateLicensePool._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                LicenseManagementServiceRestTransport._UpdateLicensePool._get_response(
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
            resp = license_management_service.LicensePool()
            pb_resp = license_management_service.LicensePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_license_pool(resp)
            return resp

    @property
    def assign(
        self,
    ) -> Callable[
        [license_management_service.AssignRequest],
        license_management_service.AssignResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Assign(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enumerate_licensed_users(
        self,
    ) -> Callable[
        [license_management_service.EnumerateLicensedUsersRequest],
        license_management_service.EnumerateLicensedUsersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnumerateLicensedUsers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_license_pool(
        self,
    ) -> Callable[
        [license_management_service.GetLicensePoolRequest],
        license_management_service.LicensePool,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLicensePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def unassign(
        self,
    ) -> Callable[
        [license_management_service.UnassignRequest],
        license_management_service.UnassignResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Unassign(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_license_pool(
        self,
    ) -> Callable[
        [license_management_service.UpdateLicensePoolRequest],
        license_management_service.LicensePool,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateLicensePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseLicenseManagementServiceRestTransport._BaseGetOperation,
        LicenseManagementServiceRestStub,
    ):
        def __hash__(self):
            return hash("LicenseManagementServiceRestTransport.GetOperation")

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
                _BaseLicenseManagementServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseLicenseManagementServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLicenseManagementServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                LicenseManagementServiceRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LicenseManagementServiceRestTransport",)
