# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.iap_v1.types import service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import IdentityAwareProxyOAuthServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class IdentityAwareProxyOAuthServiceRestInterceptor:
    """Interceptor for IdentityAwareProxyOAuthService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the IdentityAwareProxyOAuthServiceRestTransport.

    .. code-block:: python
        class MyCustomIdentityAwareProxyOAuthServiceInterceptor(IdentityAwareProxyOAuthServiceRestInterceptor):
            def pre_create_brand(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_brand(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_identity_aware_proxy_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_identity_aware_proxy_client(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_identity_aware_proxy_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_brand(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_brand(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_identity_aware_proxy_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_identity_aware_proxy_client(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_brands(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_brands(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_identity_aware_proxy_clients(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_identity_aware_proxy_clients(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reset_identity_aware_proxy_client_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reset_identity_aware_proxy_client_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = IdentityAwareProxyOAuthServiceRestTransport(interceptor=MyCustomIdentityAwareProxyOAuthServiceInterceptor())
        client = IdentityAwareProxyOAuthServiceClient(transport=transport)


    """

    def pre_create_brand(
        self, request: service.CreateBrandRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateBrandRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_brand

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_create_brand(self, response: service.Brand) -> service.Brand:
        """Post-rpc interceptor for create_brand

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_create_identity_aware_proxy_client(
        self,
        request: service.CreateIdentityAwareProxyClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.CreateIdentityAwareProxyClientRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_identity_aware_proxy_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_create_identity_aware_proxy_client(
        self, response: service.IdentityAwareProxyClient
    ) -> service.IdentityAwareProxyClient:
        """Post-rpc interceptor for create_identity_aware_proxy_client

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_identity_aware_proxy_client(
        self,
        request: service.DeleteIdentityAwareProxyClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.DeleteIdentityAwareProxyClientRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_identity_aware_proxy_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def pre_get_brand(
        self, request: service.GetBrandRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetBrandRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_brand

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_get_brand(self, response: service.Brand) -> service.Brand:
        """Post-rpc interceptor for get_brand

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_get_identity_aware_proxy_client(
        self,
        request: service.GetIdentityAwareProxyClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetIdentityAwareProxyClientRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_identity_aware_proxy_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_get_identity_aware_proxy_client(
        self, response: service.IdentityAwareProxyClient
    ) -> service.IdentityAwareProxyClient:
        """Post-rpc interceptor for get_identity_aware_proxy_client

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_list_brands(
        self, request: service.ListBrandsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListBrandsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_brands

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_list_brands(
        self, response: service.ListBrandsResponse
    ) -> service.ListBrandsResponse:
        """Post-rpc interceptor for list_brands

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_list_identity_aware_proxy_clients(
        self,
        request: service.ListIdentityAwareProxyClientsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListIdentityAwareProxyClientsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_identity_aware_proxy_clients

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_list_identity_aware_proxy_clients(
        self, response: service.ListIdentityAwareProxyClientsResponse
    ) -> service.ListIdentityAwareProxyClientsResponse:
        """Post-rpc interceptor for list_identity_aware_proxy_clients

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response

    def pre_reset_identity_aware_proxy_client_secret(
        self,
        request: service.ResetIdentityAwareProxyClientSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.ResetIdentityAwareProxyClientSecretRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for reset_identity_aware_proxy_client_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IdentityAwareProxyOAuthService server.
        """
        return request, metadata

    def post_reset_identity_aware_proxy_client_secret(
        self, response: service.IdentityAwareProxyClient
    ) -> service.IdentityAwareProxyClient:
        """Post-rpc interceptor for reset_identity_aware_proxy_client_secret

        Override in a subclass to manipulate the response
        after it is returned by the IdentityAwareProxyOAuthService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class IdentityAwareProxyOAuthServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: IdentityAwareProxyOAuthServiceRestInterceptor


class IdentityAwareProxyOAuthServiceRestTransport(
    IdentityAwareProxyOAuthServiceTransport
):
    """REST backend transport for IdentityAwareProxyOAuthService.

    API to programmatically create, list and retrieve Identity
    Aware Proxy (IAP) OAuth brands; and create, retrieve, delete and
    reset-secret of IAP OAuth clients.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "iap.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[IdentityAwareProxyOAuthServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = (
            interceptor or IdentityAwareProxyOAuthServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _CreateBrand(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("CreateBrand")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.CreateBrandRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.Brand:
            r"""Call the create brand method over HTTP.

            Args:
                request (~.service.CreateBrandRequest):
                    The request object. The request sent to CreateBrand.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.Brand:
                    OAuth brand data.
                NOTE: Only contains a portion of the
                data that describes a brand.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/brands",
                    "body": "brand",
                },
            ]
            request, metadata = self._interceptor.pre_create_brand(request, metadata)
            pb_request = service.CreateBrandRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.Brand()
            pb_resp = service.Brand.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_brand(resp)
            return resp

    class _CreateIdentityAwareProxyClient(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("CreateIdentityAwareProxyClient")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.CreateIdentityAwareProxyClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.IdentityAwareProxyClient:
            r"""Call the create identity aware
            proxy client method over HTTP.

                Args:
                    request (~.service.CreateIdentityAwareProxyClientRequest):
                        The request object. The request sent to
                    CreateIdentityAwareProxyClient.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.IdentityAwareProxyClient:
                        Contains the data that describes an
                    Identity Aware Proxy owned client.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/brands/*}/identityAwareProxyClients",
                    "body": "identity_aware_proxy_client",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_identity_aware_proxy_client(
                request, metadata
            )
            pb_request = service.CreateIdentityAwareProxyClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.IdentityAwareProxyClient()
            pb_resp = service.IdentityAwareProxyClient.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_identity_aware_proxy_client(resp)
            return resp

    class _DeleteIdentityAwareProxyClient(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("DeleteIdentityAwareProxyClient")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.DeleteIdentityAwareProxyClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete identity aware
            proxy client method over HTTP.

                Args:
                    request (~.service.DeleteIdentityAwareProxyClientRequest):
                        The request object. The request sent to
                    DeleteIdentityAwareProxyClient.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/brands/*/identityAwareProxyClients/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_identity_aware_proxy_client(
                request, metadata
            )
            pb_request = service.DeleteIdentityAwareProxyClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetBrand(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("GetBrand")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetBrandRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.Brand:
            r"""Call the get brand method over HTTP.

            Args:
                request (~.service.GetBrandRequest):
                    The request object. The request sent to GetBrand.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.Brand:
                    OAuth brand data.
                NOTE: Only contains a portion of the
                data that describes a brand.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/brands/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_brand(request, metadata)
            pb_request = service.GetBrandRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.Brand()
            pb_resp = service.Brand.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_brand(resp)
            return resp

    class _GetIdentityAwareProxyClient(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("GetIdentityAwareProxyClient")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetIdentityAwareProxyClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.IdentityAwareProxyClient:
            r"""Call the get identity aware proxy
            client method over HTTP.

                Args:
                    request (~.service.GetIdentityAwareProxyClientRequest):
                        The request object. The request sent to
                    GetIdentityAwareProxyClient.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.IdentityAwareProxyClient:
                        Contains the data that describes an
                    Identity Aware Proxy owned client.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/brands/*/identityAwareProxyClients/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_identity_aware_proxy_client(
                request, metadata
            )
            pb_request = service.GetIdentityAwareProxyClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.IdentityAwareProxyClient()
            pb_resp = service.IdentityAwareProxyClient.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_identity_aware_proxy_client(resp)
            return resp

    class _ListBrands(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("ListBrands")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ListBrandsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListBrandsResponse:
            r"""Call the list brands method over HTTP.

            Args:
                request (~.service.ListBrandsRequest):
                    The request object. The request sent to ListBrands.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListBrandsResponse:
                    Response message for ListBrands.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/brands",
                },
            ]
            request, metadata = self._interceptor.pre_list_brands(request, metadata)
            pb_request = service.ListBrandsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListBrandsResponse()
            pb_resp = service.ListBrandsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_brands(resp)
            return resp

    class _ListIdentityAwareProxyClients(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("ListIdentityAwareProxyClients")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ListIdentityAwareProxyClientsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListIdentityAwareProxyClientsResponse:
            r"""Call the list identity aware proxy
            clients method over HTTP.

                Args:
                    request (~.service.ListIdentityAwareProxyClientsRequest):
                        The request object. The request sent to
                    ListIdentityAwareProxyClients.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListIdentityAwareProxyClientsResponse:
                        Response message for
                    ListIdentityAwareProxyClients.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/brands/*}/identityAwareProxyClients",
                },
            ]
            request, metadata = self._interceptor.pre_list_identity_aware_proxy_clients(
                request, metadata
            )
            pb_request = service.ListIdentityAwareProxyClientsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListIdentityAwareProxyClientsResponse()
            pb_resp = service.ListIdentityAwareProxyClientsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_identity_aware_proxy_clients(resp)
            return resp

    class _ResetIdentityAwareProxyClientSecret(IdentityAwareProxyOAuthServiceRestStub):
        def __hash__(self):
            return hash("ResetIdentityAwareProxyClientSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ResetIdentityAwareProxyClientSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.IdentityAwareProxyClient:
            r"""Call the reset identity aware
            proxy client secret method over HTTP.

                Args:
                    request (~.service.ResetIdentityAwareProxyClientSecretRequest):
                        The request object. The request sent to
                    ResetIdentityAwareProxyClientSecret.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.IdentityAwareProxyClient:
                        Contains the data that describes an
                    Identity Aware Proxy owned client.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/brands/*/identityAwareProxyClients/*}:resetSecret",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_reset_identity_aware_proxy_client_secret(
                request, metadata
            )
            pb_request = service.ResetIdentityAwareProxyClientSecretRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.IdentityAwareProxyClient()
            pb_resp = service.IdentityAwareProxyClient.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_reset_identity_aware_proxy_client_secret(resp)
            return resp

    @property
    def create_brand(self) -> Callable[[service.CreateBrandRequest], service.Brand]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBrand(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_identity_aware_proxy_client(
        self,
    ) -> Callable[
        [service.CreateIdentityAwareProxyClientRequest],
        service.IdentityAwareProxyClient,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIdentityAwareProxyClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_identity_aware_proxy_client(
        self,
    ) -> Callable[[service.DeleteIdentityAwareProxyClientRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIdentityAwareProxyClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_brand(self) -> Callable[[service.GetBrandRequest], service.Brand]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBrand(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_identity_aware_proxy_client(
        self,
    ) -> Callable[
        [service.GetIdentityAwareProxyClientRequest], service.IdentityAwareProxyClient
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIdentityAwareProxyClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_brands(
        self,
    ) -> Callable[[service.ListBrandsRequest], service.ListBrandsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBrands(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_identity_aware_proxy_clients(
        self,
    ) -> Callable[
        [service.ListIdentityAwareProxyClientsRequest],
        service.ListIdentityAwareProxyClientsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIdentityAwareProxyClients(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_identity_aware_proxy_client_secret(
        self,
    ) -> Callable[
        [service.ResetIdentityAwareProxyClientSecretRequest],
        service.IdentityAwareProxyClient,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetIdentityAwareProxyClientSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("IdentityAwareProxyOAuthServiceRestTransport",)
