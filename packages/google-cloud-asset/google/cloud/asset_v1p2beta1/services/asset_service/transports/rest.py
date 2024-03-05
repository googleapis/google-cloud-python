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


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.asset_v1p2beta1.types import asset_service

from .base import AssetServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AssetServiceRestInterceptor:
    """Interceptor for AssetService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AssetServiceRestTransport.

    .. code-block:: python
        class MyCustomAssetServiceInterceptor(AssetServiceRestInterceptor):
            def pre_create_feed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_feed(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_feed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_feed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_feed(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_feeds(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_feeds(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_feed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_feed(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AssetServiceRestTransport(interceptor=MyCustomAssetServiceInterceptor())
        client = AssetServiceClient(transport=transport)


    """

    def pre_create_feed(
        self,
        request: asset_service.CreateFeedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[asset_service.CreateFeedRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_feed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AssetService server.
        """
        return request, metadata

    def post_create_feed(self, response: asset_service.Feed) -> asset_service.Feed:
        """Post-rpc interceptor for create_feed

        Override in a subclass to manipulate the response
        after it is returned by the AssetService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_feed(
        self,
        request: asset_service.DeleteFeedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[asset_service.DeleteFeedRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_feed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AssetService server.
        """
        return request, metadata

    def pre_get_feed(
        self, request: asset_service.GetFeedRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[asset_service.GetFeedRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_feed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AssetService server.
        """
        return request, metadata

    def post_get_feed(self, response: asset_service.Feed) -> asset_service.Feed:
        """Post-rpc interceptor for get_feed

        Override in a subclass to manipulate the response
        after it is returned by the AssetService server but before
        it is returned to user code.
        """
        return response

    def pre_list_feeds(
        self,
        request: asset_service.ListFeedsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[asset_service.ListFeedsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_feeds

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AssetService server.
        """
        return request, metadata

    def post_list_feeds(
        self, response: asset_service.ListFeedsResponse
    ) -> asset_service.ListFeedsResponse:
        """Post-rpc interceptor for list_feeds

        Override in a subclass to manipulate the response
        after it is returned by the AssetService server but before
        it is returned to user code.
        """
        return response

    def pre_update_feed(
        self,
        request: asset_service.UpdateFeedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[asset_service.UpdateFeedRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_feed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AssetService server.
        """
        return request, metadata

    def post_update_feed(self, response: asset_service.Feed) -> asset_service.Feed:
        """Post-rpc interceptor for update_feed

        Override in a subclass to manipulate the response
        after it is returned by the AssetService server but before
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
        before they are sent to the AssetService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AssetService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AssetServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AssetServiceRestInterceptor


class AssetServiceRestTransport(AssetServiceTransport):
    """REST backend transport for AssetService.

    Asset service definition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudasset.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AssetServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudasset.googleapis.com').
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
        self._interceptor = interceptor or AssetServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateFeed(AssetServiceRestStub):
        def __hash__(self):
            return hash("CreateFeed")

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
            request: asset_service.CreateFeedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> asset_service.Feed:
            r"""Call the create feed method over HTTP.

            Args:
                request (~.asset_service.CreateFeedRequest):
                    The request object. Create asset feed request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.asset_service.Feed:
                    An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:

                Cloud Pub/Sub topics.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p2beta1/{parent=*/*}/feeds",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_feed(request, metadata)
            pb_request = asset_service.CreateFeedRequest.pb(request)
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
            resp = asset_service.Feed()
            pb_resp = asset_service.Feed.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_feed(resp)
            return resp

    class _DeleteFeed(AssetServiceRestStub):
        def __hash__(self):
            return hash("DeleteFeed")

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
            request: asset_service.DeleteFeedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete feed method over HTTP.

            Args:
                request (~.asset_service.DeleteFeedRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1p2beta1/{name=*/*/feeds/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_feed(request, metadata)
            pb_request = asset_service.DeleteFeedRequest.pb(request)
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

    class _GetFeed(AssetServiceRestStub):
        def __hash__(self):
            return hash("GetFeed")

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
            request: asset_service.GetFeedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> asset_service.Feed:
            r"""Call the get feed method over HTTP.

            Args:
                request (~.asset_service.GetFeedRequest):
                    The request object. Get asset feed request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.asset_service.Feed:
                    An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:

                Cloud Pub/Sub topics.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p2beta1/{name=*/*/feeds/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_feed(request, metadata)
            pb_request = asset_service.GetFeedRequest.pb(request)
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
            resp = asset_service.Feed()
            pb_resp = asset_service.Feed.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_feed(resp)
            return resp

    class _ListFeeds(AssetServiceRestStub):
        def __hash__(self):
            return hash("ListFeeds")

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
            request: asset_service.ListFeedsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> asset_service.ListFeedsResponse:
            r"""Call the list feeds method over HTTP.

            Args:
                request (~.asset_service.ListFeedsRequest):
                    The request object. List asset feeds request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.asset_service.ListFeedsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p2beta1/{parent=*/*}/feeds",
                },
            ]
            request, metadata = self._interceptor.pre_list_feeds(request, metadata)
            pb_request = asset_service.ListFeedsRequest.pb(request)
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
            resp = asset_service.ListFeedsResponse()
            pb_resp = asset_service.ListFeedsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_feeds(resp)
            return resp

    class _UpdateFeed(AssetServiceRestStub):
        def __hash__(self):
            return hash("UpdateFeed")

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
            request: asset_service.UpdateFeedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> asset_service.Feed:
            r"""Call the update feed method over HTTP.

            Args:
                request (~.asset_service.UpdateFeedRequest):
                    The request object. Update asset feed request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.asset_service.Feed:
                    An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:

                Cloud Pub/Sub topics.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1p2beta1/{feed.name=*/*/feeds/*}",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_feed(request, metadata)
            pb_request = asset_service.UpdateFeedRequest.pb(request)
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
            resp = asset_service.Feed()
            pb_resp = asset_service.Feed.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_feed(resp)
            return resp

    @property
    def create_feed(
        self,
    ) -> Callable[[asset_service.CreateFeedRequest], asset_service.Feed]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFeed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_feed(
        self,
    ) -> Callable[[asset_service.DeleteFeedRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFeed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_feed(self) -> Callable[[asset_service.GetFeedRequest], asset_service.Feed]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFeed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_feeds(
        self,
    ) -> Callable[[asset_service.ListFeedsRequest], asset_service.ListFeedsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFeeds(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_feed(
        self,
    ) -> Callable[[asset_service.UpdateFeedRequest], asset_service.Feed]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFeed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(AssetServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p2beta1/{name=*/*/operations/*/**}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AssetServiceRestTransport",)
