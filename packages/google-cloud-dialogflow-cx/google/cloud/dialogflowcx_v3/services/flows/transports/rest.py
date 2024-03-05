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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
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

from google.cloud.dialogflowcx_v3.types import flow
from google.cloud.dialogflowcx_v3.types import flow as gcdc_flow

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import FlowsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class FlowsRestInterceptor:
    """Interceptor for Flows.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the FlowsRestTransport.

    .. code-block:: python
        class MyCustomFlowsInterceptor(FlowsRestInterceptor):
            def pre_create_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_export_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_flow_validation_result(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_flow_validation_result(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_flows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_flows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_train_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_train_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_validate_flow(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_validate_flow(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = FlowsRestTransport(interceptor=MyCustomFlowsInterceptor())
        client = FlowsClient(transport=transport)


    """

    def pre_create_flow(
        self, request: gcdc_flow.CreateFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gcdc_flow.CreateFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_create_flow(self, response: gcdc_flow.Flow) -> gcdc_flow.Flow:
        """Post-rpc interceptor for create_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_delete_flow(
        self, request: flow.DeleteFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.DeleteFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def pre_export_flow(
        self, request: flow.ExportFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.ExportFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_export_flow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_get_flow(
        self, request: flow.GetFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.GetFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_get_flow(self, response: flow.Flow) -> flow.Flow:
        """Post-rpc interceptor for get_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_get_flow_validation_result(
        self,
        request: flow.GetFlowValidationResultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[flow.GetFlowValidationResultRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_flow_validation_result

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_get_flow_validation_result(
        self, response: flow.FlowValidationResult
    ) -> flow.FlowValidationResult:
        """Post-rpc interceptor for get_flow_validation_result

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_import_flow(
        self, request: flow.ImportFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.ImportFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_import_flow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_list_flows(
        self, request: flow.ListFlowsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.ListFlowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_flows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_list_flows(
        self, response: flow.ListFlowsResponse
    ) -> flow.ListFlowsResponse:
        """Post-rpc interceptor for list_flows

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_train_flow(
        self, request: flow.TrainFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.TrainFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for train_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_train_flow(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for train_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_update_flow(
        self, request: gcdc_flow.UpdateFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gcdc_flow.UpdateFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_update_flow(self, response: gcdc_flow.Flow) -> gcdc_flow.Flow:
        """Post-rpc interceptor for update_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_validate_flow(
        self, request: flow.ValidateFlowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[flow.ValidateFlowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for validate_flow

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_validate_flow(
        self, response: flow.FlowValidationResult
    ) -> flow.FlowValidationResult:
        """Post-rpc interceptor for validate_flow

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
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
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
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
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
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
        before they are sent to the Flows server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Flows server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class FlowsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: FlowsRestInterceptor


class FlowsRestTransport(FlowsTransport):
    """REST backend transport for Flows.

    Service for managing [Flows][google.cloud.dialogflow.cx.v3.Flow].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[FlowsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or FlowsRestInterceptor()
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
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v3/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v3",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateFlow(FlowsRestStub):
        def __hash__(self):
            return hash("CreateFlow")

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
            request: gcdc_flow.CreateFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_flow.Flow:
            r"""Call the create flow method over HTTP.

            Args:
                request (~.gcdc_flow.CreateFlowRequest):
                    The request object. The request message for
                [Flows.CreateFlow][google.cloud.dialogflow.cx.v3.Flows.CreateFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_flow.Flow:
                    Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*/agents/*}/flows",
                    "body": "flow",
                },
            ]
            request, metadata = self._interceptor.pre_create_flow(request, metadata)
            pb_request = gcdc_flow.CreateFlowRequest.pb(request)
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
            resp = gcdc_flow.Flow()
            pb_resp = gcdc_flow.Flow.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_flow(resp)
            return resp

    class _DeleteFlow(FlowsRestStub):
        def __hash__(self):
            return hash("DeleteFlow")

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
            request: flow.DeleteFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete flow method over HTTP.

            Args:
                request (~.flow.DeleteFlowRequest):
                    The request object. The request message for
                [Flows.DeleteFlow][google.cloud.dialogflow.cx.v3.Flows.DeleteFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_flow(request, metadata)
            pb_request = flow.DeleteFlowRequest.pb(request)
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

    class _ExportFlow(FlowsRestStub):
        def __hash__(self):
            return hash("ExportFlow")

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
            request: flow.ExportFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export flow method over HTTP.

            Args:
                request (~.flow.ExportFlowRequest):
                    The request object. The request message for
                [Flows.ExportFlow][google.cloud.dialogflow.cx.v3.Flows.ExportFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*}:export",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_export_flow(request, metadata)
            pb_request = flow.ExportFlowRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_flow(resp)
            return resp

    class _GetFlow(FlowsRestStub):
        def __hash__(self):
            return hash("GetFlow")

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
            request: flow.GetFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> flow.Flow:
            r"""Call the get flow method over HTTP.

            Args:
                request (~.flow.GetFlowRequest):
                    The request object. The response message for
                [Flows.GetFlow][google.cloud.dialogflow.cx.v3.Flows.GetFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.flow.Flow:
                    Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_flow(request, metadata)
            pb_request = flow.GetFlowRequest.pb(request)
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
            resp = flow.Flow()
            pb_resp = flow.Flow.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_flow(resp)
            return resp

    class _GetFlowValidationResult(FlowsRestStub):
        def __hash__(self):
            return hash("GetFlowValidationResult")

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
            request: flow.GetFlowValidationResultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> flow.FlowValidationResult:
            r"""Call the get flow validation
            result method over HTTP.

                Args:
                    request (~.flow.GetFlowValidationResultRequest):
                        The request object. The request message for
                    [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3.Flows.GetFlowValidationResult].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.flow.FlowValidationResult:
                        The response message for
                    [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3.Flows.GetFlowValidationResult].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*/validationResult}",
                },
            ]
            request, metadata = self._interceptor.pre_get_flow_validation_result(
                request, metadata
            )
            pb_request = flow.GetFlowValidationResultRequest.pb(request)
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
            resp = flow.FlowValidationResult()
            pb_resp = flow.FlowValidationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_flow_validation_result(resp)
            return resp

    class _ImportFlow(FlowsRestStub):
        def __hash__(self):
            return hash("ImportFlow")

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
            request: flow.ImportFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import flow method over HTTP.

            Args:
                request (~.flow.ImportFlowRequest):
                    The request object. The request message for
                [Flows.ImportFlow][google.cloud.dialogflow.cx.v3.Flows.ImportFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*/agents/*}/flows:import",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_flow(request, metadata)
            pb_request = flow.ImportFlowRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_flow(resp)
            return resp

    class _ListFlows(FlowsRestStub):
        def __hash__(self):
            return hash("ListFlows")

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
            request: flow.ListFlowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> flow.ListFlowsResponse:
            r"""Call the list flows method over HTTP.

            Args:
                request (~.flow.ListFlowsRequest):
                    The request object. The request message for
                [Flows.ListFlows][google.cloud.dialogflow.cx.v3.Flows.ListFlows].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.flow.ListFlowsResponse:
                    The response message for
                [Flows.ListFlows][google.cloud.dialogflow.cx.v3.Flows.ListFlows].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/agents/*}/flows",
                },
            ]
            request, metadata = self._interceptor.pre_list_flows(request, metadata)
            pb_request = flow.ListFlowsRequest.pb(request)
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
            resp = flow.ListFlowsResponse()
            pb_resp = flow.ListFlowsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_flows(resp)
            return resp

    class _TrainFlow(FlowsRestStub):
        def __hash__(self):
            return hash("TrainFlow")

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
            request: flow.TrainFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the train flow method over HTTP.

            Args:
                request (~.flow.TrainFlowRequest):
                    The request object. The request message for
                [Flows.TrainFlow][google.cloud.dialogflow.cx.v3.Flows.TrainFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*}:train",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_train_flow(request, metadata)
            pb_request = flow.TrainFlowRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_train_flow(resp)
            return resp

    class _UpdateFlow(FlowsRestStub):
        def __hash__(self):
            return hash("UpdateFlow")

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
            request: gcdc_flow.UpdateFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_flow.Flow:
            r"""Call the update flow method over HTTP.

            Args:
                request (~.gcdc_flow.UpdateFlowRequest):
                    The request object. The request message for
                [Flows.UpdateFlow][google.cloud.dialogflow.cx.v3.Flows.UpdateFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_flow.Flow:
                    Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v3/{flow.name=projects/*/locations/*/agents/*/flows/*}",
                    "body": "flow",
                },
            ]
            request, metadata = self._interceptor.pre_update_flow(request, metadata)
            pb_request = gcdc_flow.UpdateFlowRequest.pb(request)
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
            resp = gcdc_flow.Flow()
            pb_resp = gcdc_flow.Flow.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_flow(resp)
            return resp

    class _ValidateFlow(FlowsRestStub):
        def __hash__(self):
            return hash("ValidateFlow")

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
            request: flow.ValidateFlowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> flow.FlowValidationResult:
            r"""Call the validate flow method over HTTP.

            Args:
                request (~.flow.ValidateFlowRequest):
                    The request object. The request message for
                [Flows.ValidateFlow][google.cloud.dialogflow.cx.v3.Flows.ValidateFlow].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.flow.FlowValidationResult:
                    The response message for
                [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3.Flows.GetFlowValidationResult].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/agents/*/flows/*}:validate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_validate_flow(request, metadata)
            pb_request = flow.ValidateFlowRequest.pb(request)
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
            resp = flow.FlowValidationResult()
            pb_resp = flow.FlowValidationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_validate_flow(resp)
            return resp

    @property
    def create_flow(self) -> Callable[[gcdc_flow.CreateFlowRequest], gcdc_flow.Flow]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_flow(self) -> Callable[[flow.DeleteFlowRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_flow(
        self,
    ) -> Callable[[flow.ExportFlowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_flow(self) -> Callable[[flow.GetFlowRequest], flow.Flow]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_flow_validation_result(
        self,
    ) -> Callable[[flow.GetFlowValidationResultRequest], flow.FlowValidationResult]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFlowValidationResult(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_flow(
        self,
    ) -> Callable[[flow.ImportFlowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_flows(self) -> Callable[[flow.ListFlowsRequest], flow.ListFlowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFlows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def train_flow(self) -> Callable[[flow.TrainFlowRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TrainFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_flow(self) -> Callable[[gcdc_flow.UpdateFlowRequest], gcdc_flow.Flow]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def validate_flow(
        self,
    ) -> Callable[[flow.ValidateFlowRequest], flow.FlowValidationResult]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ValidateFlow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(FlowsRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
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

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(FlowsRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
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

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(FlowsRestStub):
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
                    "uri": "/v3/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}:cancel",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(FlowsRestStub):
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
                    "uri": "/v3/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(FlowsRestStub):
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
                    "uri": "/v3/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*}/operations",
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


__all__ = ("FlowsRestTransport",)
