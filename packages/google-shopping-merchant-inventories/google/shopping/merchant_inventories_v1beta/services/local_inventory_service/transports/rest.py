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

from google.shopping.merchant_inventories_v1beta.types import localinventory

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import LocalInventoryServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class LocalInventoryServiceRestInterceptor:
    """Interceptor for LocalInventoryService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LocalInventoryServiceRestTransport.

    .. code-block:: python
        class MyCustomLocalInventoryServiceInterceptor(LocalInventoryServiceRestInterceptor):
            def pre_delete_local_inventory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_insert_local_inventory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_local_inventory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_local_inventories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_local_inventories(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LocalInventoryServiceRestTransport(interceptor=MyCustomLocalInventoryServiceInterceptor())
        client = LocalInventoryServiceClient(transport=transport)


    """

    def pre_delete_local_inventory(
        self,
        request: localinventory.DeleteLocalInventoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[localinventory.DeleteLocalInventoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_local_inventory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LocalInventoryService server.
        """
        return request, metadata

    def pre_insert_local_inventory(
        self,
        request: localinventory.InsertLocalInventoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[localinventory.InsertLocalInventoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert_local_inventory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LocalInventoryService server.
        """
        return request, metadata

    def post_insert_local_inventory(
        self, response: localinventory.LocalInventory
    ) -> localinventory.LocalInventory:
        """Post-rpc interceptor for insert_local_inventory

        Override in a subclass to manipulate the response
        after it is returned by the LocalInventoryService server but before
        it is returned to user code.
        """
        return response

    def pre_list_local_inventories(
        self,
        request: localinventory.ListLocalInventoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[localinventory.ListLocalInventoriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_local_inventories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LocalInventoryService server.
        """
        return request, metadata

    def post_list_local_inventories(
        self, response: localinventory.ListLocalInventoriesResponse
    ) -> localinventory.ListLocalInventoriesResponse:
        """Post-rpc interceptor for list_local_inventories

        Override in a subclass to manipulate the response
        after it is returned by the LocalInventoryService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LocalInventoryServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LocalInventoryServiceRestInterceptor


class LocalInventoryServiceRestTransport(LocalInventoryServiceTransport):
    """REST backend transport for LocalInventoryService.

    Service to manage local inventory for products

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
        interceptor: Optional[LocalInventoryServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or LocalInventoryServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteLocalInventory(LocalInventoryServiceRestStub):
        def __hash__(self):
            return hash("DeleteLocalInventory")

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
            request: localinventory.DeleteLocalInventoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete local inventory method over HTTP.

            Args:
                request (~.localinventory.DeleteLocalInventoryRequest):
                    The request object. Request message for the ``DeleteLocalInventory`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/inventories/v1beta/{name=accounts/*/products/*/localInventories/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_local_inventory(
                request, metadata
            )
            pb_request = localinventory.DeleteLocalInventoryRequest.pb(request)
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

    class _InsertLocalInventory(LocalInventoryServiceRestStub):
        def __hash__(self):
            return hash("InsertLocalInventory")

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
            request: localinventory.InsertLocalInventoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> localinventory.LocalInventory:
            r"""Call the insert local inventory method over HTTP.

            Args:
                request (~.localinventory.InsertLocalInventoryRequest):
                    The request object. Request message for the ``InsertLocalInventory`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.localinventory.LocalInventory:
                    Local inventory information for the product. Represents
                in-store information for a specific product at the store
                specified by
                [``storeCode``][google.shopping.merchant.inventories.v1beta.LocalInventory.store_code].
                For a list of all accepted attribute values, see the
                `local product inventory data
                specification <https://support.google.com/merchants/answer/3061342>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/inventories/v1beta/{parent=accounts/*/products/*}/localInventories:insert",
                    "body": "local_inventory",
                },
            ]
            request, metadata = self._interceptor.pre_insert_local_inventory(
                request, metadata
            )
            pb_request = localinventory.InsertLocalInventoryRequest.pb(request)
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
            resp = localinventory.LocalInventory()
            pb_resp = localinventory.LocalInventory.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert_local_inventory(resp)
            return resp

    class _ListLocalInventories(LocalInventoryServiceRestStub):
        def __hash__(self):
            return hash("ListLocalInventories")

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
            request: localinventory.ListLocalInventoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> localinventory.ListLocalInventoriesResponse:
            r"""Call the list local inventories method over HTTP.

            Args:
                request (~.localinventory.ListLocalInventoriesRequest):
                    The request object. Request message for the ``ListLocalInventories`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.localinventory.ListLocalInventoriesResponse:
                    Response message for the ``ListLocalInventories``
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/inventories/v1beta/{parent=accounts/*/products/*}/localInventories",
                },
            ]
            request, metadata = self._interceptor.pre_list_local_inventories(
                request, metadata
            )
            pb_request = localinventory.ListLocalInventoriesRequest.pb(request)
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
            resp = localinventory.ListLocalInventoriesResponse()
            pb_resp = localinventory.ListLocalInventoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_local_inventories(resp)
            return resp

    @property
    def delete_local_inventory(
        self,
    ) -> Callable[[localinventory.DeleteLocalInventoryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteLocalInventory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_local_inventory(
        self,
    ) -> Callable[
        [localinventory.InsertLocalInventoryRequest], localinventory.LocalInventory
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertLocalInventory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_local_inventories(
        self,
    ) -> Callable[
        [localinventory.ListLocalInventoriesRequest],
        localinventory.ListLocalInventoriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLocalInventories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LocalInventoryServiceRestTransport",)
