# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.dataproc_v1.types import autoscaling_policies
from google.protobuf import empty_pb2  # type: ignore

from .base import (
    AutoscalingPolicyServiceTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AutoscalingPolicyServiceRestInterceptor:
    """Interceptor for AutoscalingPolicyService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AutoscalingPolicyServiceRestTransport.

    .. code-block:: python
        class MyCustomAutoscalingPolicyServiceInterceptor(AutoscalingPolicyServiceRestInterceptor):
            def pre_create_autoscaling_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_autoscaling_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_autoscaling_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_autoscaling_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_autoscaling_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_autoscaling_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_autoscaling_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_autoscaling_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_autoscaling_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AutoscalingPolicyServiceRestTransport(interceptor=MyCustomAutoscalingPolicyServiceInterceptor())
        client = AutoscalingPolicyServiceClient(transport=transport)


    """

    def pre_create_autoscaling_policy(
        self,
        request: autoscaling_policies.CreateAutoscalingPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        autoscaling_policies.CreateAutoscalingPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_autoscaling_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_create_autoscaling_policy(
        self, response: autoscaling_policies.AutoscalingPolicy
    ) -> autoscaling_policies.AutoscalingPolicy:
        """Post-rpc interceptor for create_autoscaling_policy

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_autoscaling_policy(
        self,
        request: autoscaling_policies.DeleteAutoscalingPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        autoscaling_policies.DeleteAutoscalingPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_autoscaling_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def pre_get_autoscaling_policy(
        self,
        request: autoscaling_policies.GetAutoscalingPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        autoscaling_policies.GetAutoscalingPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_autoscaling_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_get_autoscaling_policy(
        self, response: autoscaling_policies.AutoscalingPolicy
    ) -> autoscaling_policies.AutoscalingPolicy:
        """Post-rpc interceptor for get_autoscaling_policy

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_list_autoscaling_policies(
        self,
        request: autoscaling_policies.ListAutoscalingPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        autoscaling_policies.ListAutoscalingPoliciesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_autoscaling_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_list_autoscaling_policies(
        self, response: autoscaling_policies.ListAutoscalingPoliciesResponse
    ) -> autoscaling_policies.ListAutoscalingPoliciesResponse:
        """Post-rpc interceptor for list_autoscaling_policies

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_update_autoscaling_policy(
        self,
        request: autoscaling_policies.UpdateAutoscalingPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        autoscaling_policies.UpdateAutoscalingPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_autoscaling_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_update_autoscaling_policy(
        self, response: autoscaling_policies.AutoscalingPolicy
    ) -> autoscaling_policies.AutoscalingPolicy:
        """Post-rpc interceptor for update_autoscaling_policy

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
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
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
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
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
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
        before they are sent to the AutoscalingPolicyService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AutoscalingPolicyService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AutoscalingPolicyServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AutoscalingPolicyServiceRestInterceptor


class AutoscalingPolicyServiceRestTransport(AutoscalingPolicyServiceTransport):
    """REST backend transport for AutoscalingPolicyService.

    The API interface for managing autoscaling policies in the
    Dataproc API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dataproc.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AutoscalingPolicyServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or AutoscalingPolicyServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateAutoscalingPolicy(AutoscalingPolicyServiceRestStub):
        def __hash__(self):
            return hash("CreateAutoscalingPolicy")

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
            request: autoscaling_policies.CreateAutoscalingPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> autoscaling_policies.AutoscalingPolicy:
            r"""Call the create autoscaling policy method over HTTP.

            Args:
                request (~.autoscaling_policies.CreateAutoscalingPolicyRequest):
                    The request object. A request to create an autoscaling
                policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.autoscaling_policies.AutoscalingPolicy:
                    Describes an autoscaling policy for
                Dataproc cluster autoscaler.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/autoscalingPolicies",
                    "body": "policy",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/regions/*}/autoscalingPolicies",
                    "body": "policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_autoscaling_policy(
                request, metadata
            )
            pb_request = autoscaling_policies.CreateAutoscalingPolicyRequest.pb(request)
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
            resp = autoscaling_policies.AutoscalingPolicy()
            pb_resp = autoscaling_policies.AutoscalingPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_autoscaling_policy(resp)
            return resp

    class _DeleteAutoscalingPolicy(AutoscalingPolicyServiceRestStub):
        def __hash__(self):
            return hash("DeleteAutoscalingPolicy")

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
            request: autoscaling_policies.DeleteAutoscalingPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete autoscaling policy method over HTTP.

            Args:
                request (~.autoscaling_policies.DeleteAutoscalingPolicyRequest):
                    The request object. A request to delete an autoscaling
                policy.
                Autoscaling policies in use by one or
                more clusters will not be deleted.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/autoscalingPolicies/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/regions/*/autoscalingPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_autoscaling_policy(
                request, metadata
            )
            pb_request = autoscaling_policies.DeleteAutoscalingPolicyRequest.pb(request)
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

    class _GetAutoscalingPolicy(AutoscalingPolicyServiceRestStub):
        def __hash__(self):
            return hash("GetAutoscalingPolicy")

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
            request: autoscaling_policies.GetAutoscalingPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> autoscaling_policies.AutoscalingPolicy:
            r"""Call the get autoscaling policy method over HTTP.

            Args:
                request (~.autoscaling_policies.GetAutoscalingPolicyRequest):
                    The request object. A request to fetch an autoscaling
                policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.autoscaling_policies.AutoscalingPolicy:
                    Describes an autoscaling policy for
                Dataproc cluster autoscaler.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/autoscalingPolicies/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/regions/*/autoscalingPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_autoscaling_policy(
                request, metadata
            )
            pb_request = autoscaling_policies.GetAutoscalingPolicyRequest.pb(request)
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
            resp = autoscaling_policies.AutoscalingPolicy()
            pb_resp = autoscaling_policies.AutoscalingPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_autoscaling_policy(resp)
            return resp

    class _ListAutoscalingPolicies(AutoscalingPolicyServiceRestStub):
        def __hash__(self):
            return hash("ListAutoscalingPolicies")

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
            request: autoscaling_policies.ListAutoscalingPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> autoscaling_policies.ListAutoscalingPoliciesResponse:
            r"""Call the list autoscaling policies method over HTTP.

            Args:
                request (~.autoscaling_policies.ListAutoscalingPoliciesRequest):
                    The request object. A request to list autoscaling
                policies in a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.autoscaling_policies.ListAutoscalingPoliciesResponse:
                    A response to a request to list
                autoscaling policies in a project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/autoscalingPolicies",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/regions/*}/autoscalingPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_autoscaling_policies(
                request, metadata
            )
            pb_request = autoscaling_policies.ListAutoscalingPoliciesRequest.pb(request)
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
            resp = autoscaling_policies.ListAutoscalingPoliciesResponse()
            pb_resp = autoscaling_policies.ListAutoscalingPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_autoscaling_policies(resp)
            return resp

    class _UpdateAutoscalingPolicy(AutoscalingPolicyServiceRestStub):
        def __hash__(self):
            return hash("UpdateAutoscalingPolicy")

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
            request: autoscaling_policies.UpdateAutoscalingPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> autoscaling_policies.AutoscalingPolicy:
            r"""Call the update autoscaling policy method over HTTP.

            Args:
                request (~.autoscaling_policies.UpdateAutoscalingPolicyRequest):
                    The request object. A request to update an autoscaling
                policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.autoscaling_policies.AutoscalingPolicy:
                    Describes an autoscaling policy for
                Dataproc cluster autoscaler.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{policy.name=projects/*/locations/*/autoscalingPolicies/*}",
                    "body": "policy",
                },
                {
                    "method": "put",
                    "uri": "/v1/{policy.name=projects/*/regions/*/autoscalingPolicies/*}",
                    "body": "policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_autoscaling_policy(
                request, metadata
            )
            pb_request = autoscaling_policies.UpdateAutoscalingPolicyRequest.pb(request)
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
            resp = autoscaling_policies.AutoscalingPolicy()
            pb_resp = autoscaling_policies.AutoscalingPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_autoscaling_policy(resp)
            return resp

    @property
    def create_autoscaling_policy(
        self,
    ) -> Callable[
        [autoscaling_policies.CreateAutoscalingPolicyRequest],
        autoscaling_policies.AutoscalingPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAutoscalingPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_autoscaling_policy(
        self,
    ) -> Callable[
        [autoscaling_policies.DeleteAutoscalingPolicyRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAutoscalingPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_autoscaling_policy(
        self,
    ) -> Callable[
        [autoscaling_policies.GetAutoscalingPolicyRequest],
        autoscaling_policies.AutoscalingPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAutoscalingPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_autoscaling_policies(
        self,
    ) -> Callable[
        [autoscaling_policies.ListAutoscalingPoliciesRequest],
        autoscaling_policies.ListAutoscalingPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutoscalingPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_autoscaling_policy(
        self,
    ) -> Callable[
        [autoscaling_policies.UpdateAutoscalingPolicyRequest],
        autoscaling_policies.AutoscalingPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAutoscalingPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(AutoscalingPolicyServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:

            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/clusters/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/jobs/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/operations/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/workflowTemplates/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/workflowTemplates/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/autoscalingPolicies/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/autoscalingPolicies/*}:getIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.loads(json.dumps(transcoded_request["body"]))
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(AutoscalingPolicyServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:

            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/clusters/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/jobs/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/operations/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/workflowTemplates/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/workflowTemplates/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/autoscalingPolicies/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/autoscalingPolicies/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.loads(json.dumps(transcoded_request["body"]))
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(AutoscalingPolicyServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:

            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/clusters/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/jobs/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/operations/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/workflowTemplates/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/workflowTemplates/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/regions/*/autoscalingPolicies/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/autoscalingPolicies/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.loads(json.dumps(transcoded_request["body"]))
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

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(AutoscalingPolicyServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/regions/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
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
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(AutoscalingPolicyServiceRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:

            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/regions/*/operations/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(AutoscalingPolicyServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/regions/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(AutoscalingPolicyServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/regions/*/operations}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations}",
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


__all__ = ("AutoscalingPolicyServiceRestTransport",)
