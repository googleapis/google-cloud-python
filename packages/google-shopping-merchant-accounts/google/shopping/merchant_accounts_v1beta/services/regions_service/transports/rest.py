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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.shopping.merchant_accounts_v1beta.types import regions

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RegionsServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionsServiceRestInterceptor:
    """Interceptor for RegionsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionsServiceRestTransport.

    .. code-block:: python
        class MyCustomRegionsServiceInterceptor(RegionsServiceRestInterceptor):
            def pre_create_region(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_region(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_region(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_region(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_region(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_regions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_regions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_region(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_region(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegionsServiceRestTransport(interceptor=MyCustomRegionsServiceInterceptor())
        client = RegionsServiceClient(transport=transport)


    """

    def pre_create_region(
        self, request: regions.CreateRegionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[regions.CreateRegionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_region

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionsService server.
        """
        return request, metadata

    def post_create_region(self, response: regions.Region) -> regions.Region:
        """Post-rpc interceptor for create_region

        Override in a subclass to manipulate the response
        after it is returned by the RegionsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_region(
        self, request: regions.DeleteRegionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[regions.DeleteRegionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_region

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionsService server.
        """
        return request, metadata

    def pre_get_region(
        self, request: regions.GetRegionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[regions.GetRegionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_region

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionsService server.
        """
        return request, metadata

    def post_get_region(self, response: regions.Region) -> regions.Region:
        """Post-rpc interceptor for get_region

        Override in a subclass to manipulate the response
        after it is returned by the RegionsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_regions(
        self, request: regions.ListRegionsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[regions.ListRegionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_regions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionsService server.
        """
        return request, metadata

    def post_list_regions(
        self, response: regions.ListRegionsResponse
    ) -> regions.ListRegionsResponse:
        """Post-rpc interceptor for list_regions

        Override in a subclass to manipulate the response
        after it is returned by the RegionsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_region(
        self, request: regions.UpdateRegionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[regions.UpdateRegionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_region

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionsService server.
        """
        return request, metadata

    def post_update_region(self, response: regions.Region) -> regions.Region:
        """Post-rpc interceptor for update_region

        Override in a subclass to manipulate the response
        after it is returned by the RegionsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionsServiceRestInterceptor


class RegionsServiceRestTransport(RegionsServiceTransport):
    """REST backend transport for RegionsService.

    Manages regions configuration.

    This API defines the following resource model:

    -  [Region][google.shopping.merchant.accounts.v1main.Region]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RegionsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        self._interceptor = interceptor or RegionsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateRegion(RegionsServiceRestStub):
        def __hash__(self):
            return hash("CreateRegion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "regionId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: regions.CreateRegionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> regions.Region:
            r"""Call the create region method over HTTP.

            Args:
                request (~.regions.CreateRegionRequest):
                    The request object. Request message for the ``CreateRegion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.regions.Region:
                    Represents a geographic region that you can use as a
                target with both the ``RegionalInventory`` and
                ``ShippingSettings`` services. You can define regions as
                collections of either postal codes or, in some
                countries, using predefined geotargets. For more
                information, see `Set up
                regions <https://support.google.com/merchants/answer/7410946#zippy=%2Ccreate-a-new-region>`__
                for more information.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/accounts/v1beta/{parent=accounts/*}/regions",
                    "body": "region",
                },
            ]
            request, metadata = self._interceptor.pre_create_region(request, metadata)
            pb_request = regions.CreateRegionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = regions.Region()
            pb_resp = regions.Region.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_region(resp)
            return resp

    class _DeleteRegion(RegionsServiceRestStub):
        def __hash__(self):
            return hash("DeleteRegion")

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
            request: regions.DeleteRegionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete region method over HTTP.

            Args:
                request (~.regions.DeleteRegionRequest):
                    The request object. Request message for the ``DeleteRegion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/accounts/v1beta/{name=accounts/*/regions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_region(request, metadata)
            pb_request = regions.DeleteRegionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _GetRegion(RegionsServiceRestStub):
        def __hash__(self):
            return hash("GetRegion")

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
            request: regions.GetRegionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> regions.Region:
            r"""Call the get region method over HTTP.

            Args:
                request (~.regions.GetRegionRequest):
                    The request object. Request message for the ``GetRegion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.regions.Region:
                    Represents a geographic region that you can use as a
                target with both the ``RegionalInventory`` and
                ``ShippingSettings`` services. You can define regions as
                collections of either postal codes or, in some
                countries, using predefined geotargets. For more
                information, see `Set up
                regions <https://support.google.com/merchants/answer/7410946#zippy=%2Ccreate-a-new-region>`__
                for more information.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/accounts/v1beta/{name=accounts/*/regions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_region(request, metadata)
            pb_request = regions.GetRegionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = regions.Region()
            pb_resp = regions.Region.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_region(resp)
            return resp

    class _ListRegions(RegionsServiceRestStub):
        def __hash__(self):
            return hash("ListRegions")

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
            request: regions.ListRegionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> regions.ListRegionsResponse:
            r"""Call the list regions method over HTTP.

            Args:
                request (~.regions.ListRegionsRequest):
                    The request object. Request message for the ``ListRegions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.regions.ListRegionsResponse:
                    Response message for the ``ListRegions`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/accounts/v1beta/{parent=accounts/*}/regions",
                },
            ]
            request, metadata = self._interceptor.pre_list_regions(request, metadata)
            pb_request = regions.ListRegionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = regions.ListRegionsResponse()
            pb_resp = regions.ListRegionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_regions(resp)
            return resp

    class _UpdateRegion(RegionsServiceRestStub):
        def __hash__(self):
            return hash("UpdateRegion")

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
            request: regions.UpdateRegionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> regions.Region:
            r"""Call the update region method over HTTP.

            Args:
                request (~.regions.UpdateRegionRequest):
                    The request object. Request message for the ``UpdateRegion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.regions.Region:
                    Represents a geographic region that you can use as a
                target with both the ``RegionalInventory`` and
                ``ShippingSettings`` services. You can define regions as
                collections of either postal codes or, in some
                countries, using predefined geotargets. For more
                information, see `Set up
                regions <https://support.google.com/merchants/answer/7410946#zippy=%2Ccreate-a-new-region>`__
                for more information.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/accounts/v1beta/{region.name=accounts/*/regions/*}",
                    "body": "region",
                },
            ]
            request, metadata = self._interceptor.pre_update_region(request, metadata)
            pb_request = regions.UpdateRegionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = regions.Region()
            pb_resp = regions.Region.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_region(resp)
            return resp

    @property
    def create_region(self) -> Callable[[regions.CreateRegionRequest], regions.Region]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRegion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_region(self) -> Callable[[regions.DeleteRegionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRegion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_region(self) -> Callable[[regions.GetRegionRequest], regions.Region]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRegion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_regions(
        self,
    ) -> Callable[[regions.ListRegionsRequest], regions.ListRegionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRegions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_region(self) -> Callable[[regions.UpdateRegionRequest], regions.Region]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRegion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionsServiceRestTransport",)
