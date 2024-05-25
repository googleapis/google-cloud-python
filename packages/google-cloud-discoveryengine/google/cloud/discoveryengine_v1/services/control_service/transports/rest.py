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
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.discoveryengine_v1.types import control
from google.cloud.discoveryengine_v1.types import control as gcd_control
from google.cloud.discoveryengine_v1.types import control_service

from .base import ControlServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ControlServiceRestInterceptor:
    """Interceptor for ControlService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ControlServiceRestTransport.

    .. code-block:: python
        class MyCustomControlServiceInterceptor(ControlServiceRestInterceptor):
            def pre_create_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_control(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_control(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_controls(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_controls(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_control(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ControlServiceRestTransport(interceptor=MyCustomControlServiceInterceptor())
        client = ControlServiceClient(transport=transport)


    """

    def pre_create_control(
        self,
        request: control_service.CreateControlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[control_service.CreateControlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_create_control(self, response: gcd_control.Control) -> gcd_control.Control:
        """Post-rpc interceptor for create_control

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_control(
        self,
        request: control_service.DeleteControlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[control_service.DeleteControlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ControlService server.
        """
        return request, metadata

    def pre_get_control(
        self,
        request: control_service.GetControlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[control_service.GetControlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_get_control(self, response: control.Control) -> control.Control:
        """Post-rpc interceptor for get_control

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
        it is returned to user code.
        """
        return response

    def pre_list_controls(
        self,
        request: control_service.ListControlsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[control_service.ListControlsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_controls

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_list_controls(
        self, response: control_service.ListControlsResponse
    ) -> control_service.ListControlsResponse:
        """Post-rpc interceptor for list_controls

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
        it is returned to user code.
        """
        return response

    def pre_update_control(
        self,
        request: control_service.UpdateControlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[control_service.UpdateControlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_update_control(self, response: gcd_control.Control) -> gcd_control.Control:
        """Post-rpc interceptor for update_control

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
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
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
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
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
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
        before they are sent to the ControlService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ControlService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ControlServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ControlServiceRestInterceptor


class ControlServiceRestTransport(ControlServiceTransport):
    """REST backend transport for ControlService.

    Service for performing CRUD operations on Controls.
    Controls allow for custom logic to be implemented in the serving
    path. Controls need to be attached to a Serving Config to be
    considered during a request.

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
        interceptor: Optional[ControlServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or ControlServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateControl(ControlServiceRestStub):
        def __hash__(self):
            return hash("CreateControl")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "controlId": "",
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
            request: control_service.CreateControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_control.Control:
            r"""Call the create control method over HTTP.

            Args:
                request (~.control_service.CreateControlRequest):
                    The request object. Request for CreateControl method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_control.Control:
                    Defines a conditioned behavior to employ during serving.
                Must be attached to a [ServingConfig][] to be considered
                at serving time. Permitted actions dependent on
                ``SolutionType``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/dataStores/*}/controls",
                    "body": "control",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/collections/*/dataStores/*}/controls",
                    "body": "control",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/collections/*/engines/*}/controls",
                    "body": "control",
                },
            ]
            request, metadata = self._interceptor.pre_create_control(request, metadata)
            pb_request = control_service.CreateControlRequest.pb(request)
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
            resp = gcd_control.Control()
            pb_resp = gcd_control.Control.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_control(resp)
            return resp

    class _DeleteControl(ControlServiceRestStub):
        def __hash__(self):
            return hash("DeleteControl")

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
            request: control_service.DeleteControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete control method over HTTP.

            Args:
                request (~.control_service.DeleteControlRequest):
                    The request object. Request for DeleteControl method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/controls/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/controls/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/engines/*/controls/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_control(request, metadata)
            pb_request = control_service.DeleteControlRequest.pb(request)
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

    class _GetControl(ControlServiceRestStub):
        def __hash__(self):
            return hash("GetControl")

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
            request: control_service.GetControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> control.Control:
            r"""Call the get control method over HTTP.

            Args:
                request (~.control_service.GetControlRequest):
                    The request object. Request for GetControl method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.control.Control:
                    Defines a conditioned behavior to employ during serving.
                Must be attached to a [ServingConfig][] to be considered
                at serving time. Permitted actions dependent on
                ``SolutionType``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/controls/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/controls/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/engines/*/controls/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_control(request, metadata)
            pb_request = control_service.GetControlRequest.pb(request)
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
            resp = control.Control()
            pb_resp = control.Control.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_control(resp)
            return resp

    class _ListControls(ControlServiceRestStub):
        def __hash__(self):
            return hash("ListControls")

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
            request: control_service.ListControlsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> control_service.ListControlsResponse:
            r"""Call the list controls method over HTTP.

            Args:
                request (~.control_service.ListControlsRequest):
                    The request object. Request for ListControls method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.control_service.ListControlsResponse:
                    Response for ListControls method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/dataStores/*}/controls",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/collections/*/dataStores/*}/controls",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/collections/*/engines/*}/controls",
                },
            ]
            request, metadata = self._interceptor.pre_list_controls(request, metadata)
            pb_request = control_service.ListControlsRequest.pb(request)
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
            resp = control_service.ListControlsResponse()
            pb_resp = control_service.ListControlsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_controls(resp)
            return resp

    class _UpdateControl(ControlServiceRestStub):
        def __hash__(self):
            return hash("UpdateControl")

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
            request: control_service.UpdateControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_control.Control:
            r"""Call the update control method over HTTP.

            Args:
                request (~.control_service.UpdateControlRequest):
                    The request object. Request for UpdateControl method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_control.Control:
                    Defines a conditioned behavior to employ during serving.
                Must be attached to a [ServingConfig][] to be considered
                at serving time. Permitted actions dependent on
                ``SolutionType``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{control.name=projects/*/locations/*/dataStores/*/controls/*}",
                    "body": "control",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{control.name=projects/*/locations/*/collections/*/dataStores/*/controls/*}",
                    "body": "control",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{control.name=projects/*/locations/*/collections/*/engines/*/controls/*}",
                    "body": "control",
                },
            ]
            request, metadata = self._interceptor.pre_update_control(request, metadata)
            pb_request = control_service.UpdateControlRequest.pb(request)
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
            resp = gcd_control.Control()
            pb_resp = gcd_control.Control.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_control(resp)
            return resp

    @property
    def create_control(
        self,
    ) -> Callable[[control_service.CreateControlRequest], gcd_control.Control]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_control(
        self,
    ) -> Callable[[control_service.DeleteControlRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_control(
        self,
    ) -> Callable[[control_service.GetControlRequest], control.Control]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_controls(
        self,
    ) -> Callable[
        [control_service.ListControlsRequest], control_service.ListControlsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListControls(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_control(
        self,
    ) -> Callable[[control_service.UpdateControlRequest], gcd_control.Control]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(ControlServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/operations/*}:cancel",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ControlServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/operations/*}",
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(ControlServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/collections/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
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

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ControlServiceRestTransport",)
