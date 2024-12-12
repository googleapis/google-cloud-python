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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.retail_v2alpha.types import merchant_center_account_link_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMerchantCenterAccountLinkServiceRestTransport

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


class MerchantCenterAccountLinkServiceRestInterceptor:
    """Interceptor for MerchantCenterAccountLinkService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MerchantCenterAccountLinkServiceRestTransport.

    .. code-block:: python
        class MyCustomMerchantCenterAccountLinkServiceInterceptor(MerchantCenterAccountLinkServiceRestInterceptor):
            def pre_create_merchant_center_account_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_merchant_center_account_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_merchant_center_account_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_list_merchant_center_account_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_merchant_center_account_links(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MerchantCenterAccountLinkServiceRestTransport(interceptor=MyCustomMerchantCenterAccountLinkServiceInterceptor())
        client = MerchantCenterAccountLinkServiceClient(transport=transport)


    """

    def pre_create_merchant_center_account_link(
        self,
        request: merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_merchant_center_account_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MerchantCenterAccountLinkService server.
        """
        return request, metadata

    def post_create_merchant_center_account_link(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_merchant_center_account_link

        Override in a subclass to manipulate the response
        after it is returned by the MerchantCenterAccountLinkService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_merchant_center_account_link(
        self,
        request: merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_merchant_center_account_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MerchantCenterAccountLinkService server.
        """
        return request, metadata

    def pre_list_merchant_center_account_links(
        self,
        request: merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_merchant_center_account_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MerchantCenterAccountLinkService server.
        """
        return request, metadata

    def post_list_merchant_center_account_links(
        self,
        response: merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse,
    ) -> merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse:
        """Post-rpc interceptor for list_merchant_center_account_links

        Override in a subclass to manipulate the response
        after it is returned by the MerchantCenterAccountLinkService server but before
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
        before they are sent to the MerchantCenterAccountLinkService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the MerchantCenterAccountLinkService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MerchantCenterAccountLinkService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the MerchantCenterAccountLinkService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MerchantCenterAccountLinkServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MerchantCenterAccountLinkServiceRestInterceptor


class MerchantCenterAccountLinkServiceRestTransport(
    _BaseMerchantCenterAccountLinkServiceRestTransport
):
    """REST backend synchronous transport for MerchantCenterAccountLinkService.

    Merchant Center Link service to link a Branch to a Merchant
    Center Account.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "retail.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MerchantCenterAccountLinkServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'retail.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = (
            interceptor or MerchantCenterAccountLinkServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/places/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateMerchantCenterAccountLink(
        _BaseMerchantCenterAccountLinkServiceRestTransport._BaseCreateMerchantCenterAccountLink,
        MerchantCenterAccountLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MerchantCenterAccountLinkServiceRestTransport.CreateMerchantCenterAccountLink"
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
                data=body,
            )
            return response

        def __call__(
            self,
            request: merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create merchant center
            account link method over HTTP.

                Args:
                    request (~.merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest):
                        The request object. Request for
                    [MerchantCenterAccountLinkService.CreateMerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.CreateMerchantCenterAccountLink]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseMerchantCenterAccountLinkServiceRestTransport._BaseCreateMerchantCenterAccountLink._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_create_merchant_center_account_link(
                request, metadata
            )
            transcoded_request = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseCreateMerchantCenterAccountLink._get_transcoded_request(
                http_options, request
            )

            body = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseCreateMerchantCenterAccountLink._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseCreateMerchantCenterAccountLink._get_query_params_json(
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
                    f"Sending request for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.CreateMerchantCenterAccountLink",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "CreateMerchantCenterAccountLink",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MerchantCenterAccountLinkServiceRestTransport._CreateMerchantCenterAccountLink._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_merchant_center_account_link(resp)
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
                    "Received response for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.create_merchant_center_account_link",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "CreateMerchantCenterAccountLink",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteMerchantCenterAccountLink(
        _BaseMerchantCenterAccountLinkServiceRestTransport._BaseDeleteMerchantCenterAccountLink,
        MerchantCenterAccountLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MerchantCenterAccountLinkServiceRestTransport.DeleteMerchantCenterAccountLink"
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
            request: merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete merchant center
            account link method over HTTP.

                Args:
                    request (~.merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest):
                        The request object. Request for
                    [MerchantCenterAccountLinkService.DeleteMerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.DeleteMerchantCenterAccountLink]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.
            """

            http_options = (
                _BaseMerchantCenterAccountLinkServiceRestTransport._BaseDeleteMerchantCenterAccountLink._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_merchant_center_account_link(
                request, metadata
            )
            transcoded_request = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseDeleteMerchantCenterAccountLink._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseDeleteMerchantCenterAccountLink._get_query_params_json(
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
                    f"Sending request for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.DeleteMerchantCenterAccountLink",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "DeleteMerchantCenterAccountLink",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MerchantCenterAccountLinkServiceRestTransport._DeleteMerchantCenterAccountLink._get_response(
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

    class _ListMerchantCenterAccountLinks(
        _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListMerchantCenterAccountLinks,
        MerchantCenterAccountLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MerchantCenterAccountLinkServiceRestTransport.ListMerchantCenterAccountLinks"
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
            request: merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> (
            merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse
        ):
            r"""Call the list merchant center
            account links method over HTTP.

                Args:
                    request (~.merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest):
                        The request object. Request for
                    [MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse:
                        Response for
                    [MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks]
                    method.

            """

            http_options = (
                _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListMerchantCenterAccountLinks._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_list_merchant_center_account_links(
                request, metadata
            )
            transcoded_request = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListMerchantCenterAccountLinks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListMerchantCenterAccountLinks._get_query_params_json(
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
                    f"Sending request for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.ListMerchantCenterAccountLinks",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "ListMerchantCenterAccountLinks",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MerchantCenterAccountLinkServiceRestTransport._ListMerchantCenterAccountLinks._get_response(
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
                merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse()
            )
            pb_resp = merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_merchant_center_account_links(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse.to_json(
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
                    "Received response for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.list_merchant_center_account_links",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "ListMerchantCenterAccountLinks",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_merchant_center_account_link(
        self,
    ) -> Callable[
        [merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMerchantCenterAccountLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_merchant_center_account_link(
        self,
    ) -> Callable[
        [merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest],
        empty_pb2.Empty,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMerchantCenterAccountLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_merchant_center_account_links(
        self,
    ) -> Callable[
        [merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest],
        merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMerchantCenterAccountLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseMerchantCenterAccountLinkServiceRestTransport._BaseGetOperation,
        MerchantCenterAccountLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("MerchantCenterAccountLinkServiceRestTransport.GetOperation")

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
                _BaseMerchantCenterAccountLinkServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MerchantCenterAccountLinkServiceRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListOperations,
        MerchantCenterAccountLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("MerchantCenterAccountLinkServiceRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMerchantCenterAccountLinkServiceRestTransport._BaseListOperations._get_query_params_json(
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
                    f"Sending request for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MerchantCenterAccountLinkServiceRestTransport._ListOperations._get_response(
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
                    "Received response for google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                        "rpcName": "ListOperations",
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


__all__ = ("MerchantCenterAccountLinkServiceRestTransport",)
