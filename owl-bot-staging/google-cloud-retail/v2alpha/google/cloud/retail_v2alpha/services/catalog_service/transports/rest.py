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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.cloud.location import locations_pb2 # type: ignore
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.retail_v2alpha.types import catalog
from google.cloud.retail_v2alpha.types import catalog as gcr_catalog
from google.cloud.retail_v2alpha.types import catalog_service
from google.protobuf import empty_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from .base import CatalogServiceTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CatalogServiceRestInterceptor:
    """Interceptor for CatalogService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CatalogServiceRestTransport.

    .. code-block:: python
        class MyCustomCatalogServiceInterceptor(CatalogServiceRestInterceptor):
            def pre_add_catalog_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_catalog_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_remove_catalog_attributes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_remove_catalog_attributes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attributes_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attributes_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_completion_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_completion_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_default_branch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_default_branch(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_catalogs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_catalogs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_catalog_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_catalog_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_replace_catalog_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_replace_catalog_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_default_branch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_attributes_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_attributes_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_catalog(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_catalog(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_completion_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_completion_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CatalogServiceRestTransport(interceptor=MyCustomCatalogServiceInterceptor())
        client = CatalogServiceClient(transport=transport)


    """
    def pre_add_catalog_attribute(self, request: catalog_service.AddCatalogAttributeRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.AddCatalogAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_catalog_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_add_catalog_attribute(self, response: catalog.AttributesConfig) -> catalog.AttributesConfig:
        """Post-rpc interceptor for add_catalog_attribute

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_batch_remove_catalog_attributes(self, request: catalog_service.BatchRemoveCatalogAttributesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.BatchRemoveCatalogAttributesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_remove_catalog_attributes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_batch_remove_catalog_attributes(self, response: catalog_service.BatchRemoveCatalogAttributesResponse) -> catalog_service.BatchRemoveCatalogAttributesResponse:
        """Post-rpc interceptor for batch_remove_catalog_attributes

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_get_attributes_config(self, request: catalog_service.GetAttributesConfigRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.GetAttributesConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_attributes_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_attributes_config(self, response: catalog.AttributesConfig) -> catalog.AttributesConfig:
        """Post-rpc interceptor for get_attributes_config

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_get_completion_config(self, request: catalog_service.GetCompletionConfigRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.GetCompletionConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_completion_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_completion_config(self, response: catalog.CompletionConfig) -> catalog.CompletionConfig:
        """Post-rpc interceptor for get_completion_config

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_get_default_branch(self, request: catalog_service.GetDefaultBranchRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.GetDefaultBranchRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_default_branch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_default_branch(self, response: catalog_service.GetDefaultBranchResponse) -> catalog_service.GetDefaultBranchResponse:
        """Post-rpc interceptor for get_default_branch

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_list_catalogs(self, request: catalog_service.ListCatalogsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.ListCatalogsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_catalogs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_catalogs(self, response: catalog_service.ListCatalogsResponse) -> catalog_service.ListCatalogsResponse:
        """Post-rpc interceptor for list_catalogs

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_remove_catalog_attribute(self, request: catalog_service.RemoveCatalogAttributeRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.RemoveCatalogAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_catalog_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_remove_catalog_attribute(self, response: catalog.AttributesConfig) -> catalog.AttributesConfig:
        """Post-rpc interceptor for remove_catalog_attribute

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_replace_catalog_attribute(self, request: catalog_service.ReplaceCatalogAttributeRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.ReplaceCatalogAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for replace_catalog_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_replace_catalog_attribute(self, response: catalog.AttributesConfig) -> catalog.AttributesConfig:
        """Post-rpc interceptor for replace_catalog_attribute

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_set_default_branch(self, request: catalog_service.SetDefaultBranchRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.SetDefaultBranchRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_default_branch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def pre_update_attributes_config(self, request: catalog_service.UpdateAttributesConfigRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.UpdateAttributesConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_attributes_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_attributes_config(self, response: catalog.AttributesConfig) -> catalog.AttributesConfig:
        """Post-rpc interceptor for update_attributes_config

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_update_catalog(self, request: catalog_service.UpdateCatalogRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.UpdateCatalogRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_catalog

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_catalog(self, response: gcr_catalog.Catalog) -> gcr_catalog.Catalog:
        """Post-rpc interceptor for update_catalog

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_update_completion_config(self, request: catalog_service.UpdateCompletionConfigRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[catalog_service.UpdateCompletionConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_completion_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_completion_config(self, response: catalog.CompletionConfig) -> catalog.CompletionConfig:
        """Post-rpc interceptor for update_completion_config

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self, request: operations_pb2.GetOperationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response
    def pre_list_operations(
        self, request: operations_pb2.ListOperationsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CatalogServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CatalogServiceRestInterceptor


class CatalogServiceRestTransport(CatalogServiceTransport):
    """REST backend transport for CatalogService.

    Service for managing catalog configuration.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(self, *,
            host: str = 'retail.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[CatalogServiceRestInterceptor] = None,
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CatalogServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AddCatalogAttribute(CatalogServiceRestStub):
        def __hash__(self):
            return hash("AddCatalogAttribute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.AddCatalogAttributeRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.AttributesConfig:
            r"""Call the add catalog attribute method over HTTP.

            Args:
                request (~.catalog_service.AddCatalogAttributeRequest):
                    The request object. Request for
                [CatalogService.AddCatalogAttribute][google.cloud.retail.v2alpha.CatalogService.AddCatalogAttribute]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.AttributesConfig:
                    Catalog level attribute config.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2alpha/{attributes_config=projects/*/locations/*/catalogs/*/attributesConfig}:addCatalogAttribute',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_add_catalog_attribute(request, metadata)
            pb_request = catalog_service.AddCatalogAttributeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.AttributesConfig()
            pb_resp = catalog.AttributesConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_catalog_attribute(resp)
            return resp

    class _BatchRemoveCatalogAttributes(CatalogServiceRestStub):
        def __hash__(self):
            return hash("BatchRemoveCatalogAttributes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.BatchRemoveCatalogAttributesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog_service.BatchRemoveCatalogAttributesResponse:
            r"""Call the batch remove catalog
        attributes method over HTTP.

            Args:
                request (~.catalog_service.BatchRemoveCatalogAttributesRequest):
                    The request object. Request for
                [CatalogService.BatchRemoveCatalogAttributes][google.cloud.retail.v2alpha.CatalogService.BatchRemoveCatalogAttributes]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog_service.BatchRemoveCatalogAttributesResponse:
                    Response of the
                [CatalogService.BatchRemoveCatalogAttributes][google.cloud.retail.v2alpha.CatalogService.BatchRemoveCatalogAttributes].

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2alpha/{attributes_config=projects/*/locations/*/catalogs/*/attributesConfig}:batchRemoveCatalogAttributes',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_remove_catalog_attributes(request, metadata)
            pb_request = catalog_service.BatchRemoveCatalogAttributesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog_service.BatchRemoveCatalogAttributesResponse()
            pb_resp = catalog_service.BatchRemoveCatalogAttributesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_remove_catalog_attributes(resp)
            return resp

    class _GetAttributesConfig(CatalogServiceRestStub):
        def __hash__(self):
            return hash("GetAttributesConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.GetAttributesConfigRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.AttributesConfig:
            r"""Call the get attributes config method over HTTP.

            Args:
                request (~.catalog_service.GetAttributesConfigRequest):
                    The request object. Request for
                [CatalogService.GetAttributesConfig][google.cloud.retail.v2alpha.CatalogService.GetAttributesConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.AttributesConfig:
                    Catalog level attribute config.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*/attributesConfig}',
            },
            ]
            request, metadata = self._interceptor.pre_get_attributes_config(request, metadata)
            pb_request = catalog_service.GetAttributesConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.AttributesConfig()
            pb_resp = catalog.AttributesConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attributes_config(resp)
            return resp

    class _GetCompletionConfig(CatalogServiceRestStub):
        def __hash__(self):
            return hash("GetCompletionConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.GetCompletionConfigRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.CompletionConfig:
            r"""Call the get completion config method over HTTP.

            Args:
                request (~.catalog_service.GetCompletionConfigRequest):
                    The request object. Request for
                [CatalogService.GetCompletionConfig][google.cloud.retail.v2alpha.CatalogService.GetCompletionConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.CompletionConfig:
                    Catalog level autocomplete config for
                customers to customize autocomplete
                feature's settings.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*/completionConfig}',
            },
            ]
            request, metadata = self._interceptor.pre_get_completion_config(request, metadata)
            pb_request = catalog_service.GetCompletionConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.CompletionConfig()
            pb_resp = catalog.CompletionConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_completion_config(resp)
            return resp

    class _GetDefaultBranch(CatalogServiceRestStub):
        def __hash__(self):
            return hash("GetDefaultBranch")

        def __call__(self,
                request: catalog_service.GetDefaultBranchRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog_service.GetDefaultBranchResponse:
            r"""Call the get default branch method over HTTP.

            Args:
                request (~.catalog_service.GetDefaultBranchRequest):
                    The request object. Request message to show which branch
                is currently the default branch.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog_service.GetDefaultBranchResponse:
                    Response message of
                [CatalogService.GetDefaultBranch][google.cloud.retail.v2alpha.CatalogService.GetDefaultBranch].

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{catalog=projects/*/locations/*/catalogs/*}:getDefaultBranch',
            },
            ]
            request, metadata = self._interceptor.pre_get_default_branch(request, metadata)
            pb_request = catalog_service.GetDefaultBranchRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog_service.GetDefaultBranchResponse()
            pb_resp = catalog_service.GetDefaultBranchResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_default_branch(resp)
            return resp

    class _ListCatalogs(CatalogServiceRestStub):
        def __hash__(self):
            return hash("ListCatalogs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.ListCatalogsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog_service.ListCatalogsResponse:
            r"""Call the list catalogs method over HTTP.

            Args:
                request (~.catalog_service.ListCatalogsRequest):
                    The request object. Request for
                [CatalogService.ListCatalogs][google.cloud.retail.v2alpha.CatalogService.ListCatalogs]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog_service.ListCatalogsResponse:
                    Response for
                [CatalogService.ListCatalogs][google.cloud.retail.v2alpha.CatalogService.ListCatalogs]
                method.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{parent=projects/*/locations/*}/catalogs',
            },
            ]
            request, metadata = self._interceptor.pre_list_catalogs(request, metadata)
            pb_request = catalog_service.ListCatalogsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog_service.ListCatalogsResponse()
            pb_resp = catalog_service.ListCatalogsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_catalogs(resp)
            return resp

    class _RemoveCatalogAttribute(CatalogServiceRestStub):
        def __hash__(self):
            return hash("RemoveCatalogAttribute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.RemoveCatalogAttributeRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.AttributesConfig:
            r"""Call the remove catalog attribute method over HTTP.

            Args:
                request (~.catalog_service.RemoveCatalogAttributeRequest):
                    The request object. Request for
                [CatalogService.RemoveCatalogAttribute][google.cloud.retail.v2alpha.CatalogService.RemoveCatalogAttribute]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.AttributesConfig:
                    Catalog level attribute config.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2alpha/{attributes_config=projects/*/locations/*/catalogs/*/attributesConfig}:removeCatalogAttribute',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_remove_catalog_attribute(request, metadata)
            pb_request = catalog_service.RemoveCatalogAttributeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.AttributesConfig()
            pb_resp = catalog.AttributesConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_remove_catalog_attribute(resp)
            return resp

    class _ReplaceCatalogAttribute(CatalogServiceRestStub):
        def __hash__(self):
            return hash("ReplaceCatalogAttribute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.ReplaceCatalogAttributeRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.AttributesConfig:
            r"""Call the replace catalog attribute method over HTTP.

            Args:
                request (~.catalog_service.ReplaceCatalogAttributeRequest):
                    The request object. Request for
                [CatalogService.ReplaceCatalogAttribute][google.cloud.retail.v2alpha.CatalogService.ReplaceCatalogAttribute]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.AttributesConfig:
                    Catalog level attribute config.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2alpha/{attributes_config=projects/*/locations/*/catalogs/*/attributesConfig}:replaceCatalogAttribute',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_replace_catalog_attribute(request, metadata)
            pb_request = catalog_service.ReplaceCatalogAttributeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.AttributesConfig()
            pb_resp = catalog.AttributesConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_replace_catalog_attribute(resp)
            return resp

    class _SetDefaultBranch(CatalogServiceRestStub):
        def __hash__(self):
            return hash("SetDefaultBranch")

        def __call__(self,
                request: catalog_service.SetDefaultBranchRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the set default branch method over HTTP.

            Args:
                request (~.catalog_service.SetDefaultBranchRequest):
                    The request object. Request message to set a specified branch as new
                default_branch.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2alpha/{catalog=projects/*/locations/*/catalogs/*}:setDefaultBranch',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_set_default_branch(request, metadata)
            pb_request = catalog_service.SetDefaultBranchRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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

    class _UpdateAttributesConfig(CatalogServiceRestStub):
        def __hash__(self):
            return hash("UpdateAttributesConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.UpdateAttributesConfigRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.AttributesConfig:
            r"""Call the update attributes config method over HTTP.

            Args:
                request (~.catalog_service.UpdateAttributesConfigRequest):
                    The request object. Request for
                [CatalogService.UpdateAttributesConfig][google.cloud.retail.v2alpha.CatalogService.UpdateAttributesConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.AttributesConfig:
                    Catalog level attribute config.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2alpha/{attributes_config.name=projects/*/locations/*/catalogs/*/attributesConfig}',
                'body': 'attributes_config',
            },
            ]
            request, metadata = self._interceptor.pre_update_attributes_config(request, metadata)
            pb_request = catalog_service.UpdateAttributesConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.AttributesConfig()
            pb_resp = catalog.AttributesConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_attributes_config(resp)
            return resp

    class _UpdateCatalog(CatalogServiceRestStub):
        def __hash__(self):
            return hash("UpdateCatalog")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.UpdateCatalogRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> gcr_catalog.Catalog:
            r"""Call the update catalog method over HTTP.

            Args:
                request (~.catalog_service.UpdateCatalogRequest):
                    The request object. Request for
                [CatalogService.UpdateCatalog][google.cloud.retail.v2alpha.CatalogService.UpdateCatalog]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcr_catalog.Catalog:
                    The catalog configuration.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2alpha/{catalog.name=projects/*/locations/*/catalogs/*}',
                'body': 'catalog',
            },
            ]
            request, metadata = self._interceptor.pre_update_catalog(request, metadata)
            pb_request = catalog_service.UpdateCatalogRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = gcr_catalog.Catalog()
            pb_resp = gcr_catalog.Catalog.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_catalog(resp)
            return resp

    class _UpdateCompletionConfig(CatalogServiceRestStub):
        def __hash__(self):
            return hash("UpdateCompletionConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: catalog_service.UpdateCompletionConfigRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> catalog.CompletionConfig:
            r"""Call the update completion config method over HTTP.

            Args:
                request (~.catalog_service.UpdateCompletionConfigRequest):
                    The request object. Request for
                [CatalogService.UpdateCompletionConfig][google.cloud.retail.v2alpha.CatalogService.UpdateCompletionConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.catalog.CompletionConfig:
                    Catalog level autocomplete config for
                customers to customize autocomplete
                feature's settings.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2alpha/{completion_config.name=projects/*/locations/*/catalogs/*/completionConfig}',
                'body': 'completion_config',
            },
            ]
            request, metadata = self._interceptor.pre_update_completion_config(request, metadata)
            pb_request = catalog_service.UpdateCompletionConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            resp = catalog.CompletionConfig()
            pb_resp = catalog.CompletionConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_completion_config(resp)
            return resp

    @property
    def add_catalog_attribute(self) -> Callable[
            [catalog_service.AddCatalogAttributeRequest],
            catalog.AttributesConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddCatalogAttribute(self._session, self._host, self._interceptor) # type: ignore

    @property
    def batch_remove_catalog_attributes(self) -> Callable[
            [catalog_service.BatchRemoveCatalogAttributesRequest],
            catalog_service.BatchRemoveCatalogAttributesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchRemoveCatalogAttributes(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_attributes_config(self) -> Callable[
            [catalog_service.GetAttributesConfigRequest],
            catalog.AttributesConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttributesConfig(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_completion_config(self) -> Callable[
            [catalog_service.GetCompletionConfigRequest],
            catalog.CompletionConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCompletionConfig(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_default_branch(self) -> Callable[
            [catalog_service.GetDefaultBranchRequest],
            catalog_service.GetDefaultBranchResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDefaultBranch(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_catalogs(self) -> Callable[
            [catalog_service.ListCatalogsRequest],
            catalog_service.ListCatalogsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCatalogs(self._session, self._host, self._interceptor) # type: ignore

    @property
    def remove_catalog_attribute(self) -> Callable[
            [catalog_service.RemoveCatalogAttributeRequest],
            catalog.AttributesConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveCatalogAttribute(self._session, self._host, self._interceptor) # type: ignore

    @property
    def replace_catalog_attribute(self) -> Callable[
            [catalog_service.ReplaceCatalogAttributeRequest],
            catalog.AttributesConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReplaceCatalogAttribute(self._session, self._host, self._interceptor) # type: ignore

    @property
    def set_default_branch(self) -> Callable[
            [catalog_service.SetDefaultBranchRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetDefaultBranch(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_attributes_config(self) -> Callable[
            [catalog_service.UpdateAttributesConfigRequest],
            catalog.AttributesConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAttributesConfig(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_catalog(self) -> Callable[
            [catalog_service.UpdateCatalogRequest],
            gcr_catalog.Catalog]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCatalog(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_completion_config(self) -> Callable[
            [catalog_service.UpdateCompletionConfigRequest],
            catalog.CompletionConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCompletionConfig(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor) # type: ignore

    class _GetOperation(CatalogServiceRestStub):
        def __call__(self,
            request: operations_pb2.GetOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
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

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/places/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/operations/*}',
            },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor) # type: ignore

    class _ListOperations(CatalogServiceRestStub):
        def __call__(self,
            request: operations_pb2.ListOperationsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
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

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*/catalogs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*/locations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v2alpha/{name=projects/*}/operations',
            },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'CatalogServiceRestTransport',
)
