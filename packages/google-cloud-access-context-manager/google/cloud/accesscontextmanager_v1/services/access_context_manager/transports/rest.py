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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.accesscontextmanager_v1.types import (
    access_context_manager,
    access_level,
    access_policy,
    gcp_user_access_binding,
    service_perimeter,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAccessContextManagerRestTransport

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


class AccessContextManagerRestInterceptor:
    """Interceptor for AccessContextManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AccessContextManagerRestTransport.

    .. code-block:: python
        class MyCustomAccessContextManagerInterceptor(AccessContextManagerRestInterceptor):
            def pre_commit_service_perimeters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_commit_service_perimeters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_access_level(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_access_level(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_gcp_user_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_gcp_user_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service_perimeter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service_perimeter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_access_level(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_access_level(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_gcp_user_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_gcp_user_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service_perimeter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service_perimeter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_access_level(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_access_level(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_gcp_user_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_gcp_user_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service_perimeter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service_perimeter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_access_levels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_access_levels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_access_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_access_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_gcp_user_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_gcp_user_access_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_service_perimeters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_service_perimeters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_replace_access_levels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_replace_access_levels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_replace_service_perimeters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_replace_service_perimeters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_access_level(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_access_level(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_gcp_user_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_gcp_user_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_service_perimeter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_service_perimeter(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AccessContextManagerRestTransport(interceptor=MyCustomAccessContextManagerInterceptor())
        client = AccessContextManagerClient(transport=transport)


    """

    def pre_commit_service_perimeters(
        self,
        request: access_context_manager.CommitServicePerimetersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.CommitServicePerimetersRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for commit_service_perimeters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_commit_service_perimeters(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for commit_service_perimeters

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_access_level(
        self,
        request: access_context_manager.CreateAccessLevelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.CreateAccessLevelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_access_level

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_create_access_level(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_access_level

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_access_policy(
        self,
        request: access_policy.AccessPolicy,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[access_policy.AccessPolicy, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_create_access_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_access_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_gcp_user_access_binding(
        self,
        request: access_context_manager.CreateGcpUserAccessBindingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.CreateGcpUserAccessBindingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_gcp_user_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_create_gcp_user_access_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_gcp_user_access_binding

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_service_perimeter(
        self,
        request: access_context_manager.CreateServicePerimeterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.CreateServicePerimeterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_service_perimeter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_create_service_perimeter(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service_perimeter

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_access_level(
        self,
        request: access_context_manager.DeleteAccessLevelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.DeleteAccessLevelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_access_level

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_delete_access_level(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_access_level

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_access_policy(
        self,
        request: access_context_manager.DeleteAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.DeleteAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_delete_access_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_access_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_gcp_user_access_binding(
        self,
        request: access_context_manager.DeleteGcpUserAccessBindingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.DeleteGcpUserAccessBindingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_gcp_user_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_delete_gcp_user_access_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_gcp_user_access_binding

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service_perimeter(
        self,
        request: access_context_manager.DeleteServicePerimeterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.DeleteServicePerimeterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_service_perimeter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_delete_service_perimeter(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service_perimeter

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_access_level(
        self,
        request: access_context_manager.GetAccessLevelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.GetAccessLevelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_access_level

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_access_level(
        self, response: access_level.AccessLevel
    ) -> access_level.AccessLevel:
        """Post-rpc interceptor for get_access_level

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_access_policy(
        self,
        request: access_context_manager.GetAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.GetAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_access_policy(
        self, response: access_policy.AccessPolicy
    ) -> access_policy.AccessPolicy:
        """Post-rpc interceptor for get_access_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_gcp_user_access_binding(
        self,
        request: access_context_manager.GetGcpUserAccessBindingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.GetGcpUserAccessBindingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_gcp_user_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_gcp_user_access_binding(
        self, response: gcp_user_access_binding.GcpUserAccessBinding
    ) -> gcp_user_access_binding.GcpUserAccessBinding:
        """Post-rpc interceptor for get_gcp_user_access_binding

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_service_perimeter(
        self,
        request: access_context_manager.GetServicePerimeterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.GetServicePerimeterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_service_perimeter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_service_perimeter(
        self, response: service_perimeter.ServicePerimeter
    ) -> service_perimeter.ServicePerimeter:
        """Post-rpc interceptor for get_service_perimeter

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_access_levels(
        self,
        request: access_context_manager.ListAccessLevelsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ListAccessLevelsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_access_levels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_list_access_levels(
        self, response: access_context_manager.ListAccessLevelsResponse
    ) -> access_context_manager.ListAccessLevelsResponse:
        """Post-rpc interceptor for list_access_levels

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_access_policies(
        self,
        request: access_context_manager.ListAccessPoliciesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ListAccessPoliciesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_access_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_list_access_policies(
        self, response: access_context_manager.ListAccessPoliciesResponse
    ) -> access_context_manager.ListAccessPoliciesResponse:
        """Post-rpc interceptor for list_access_policies

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_gcp_user_access_bindings(
        self,
        request: access_context_manager.ListGcpUserAccessBindingsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ListGcpUserAccessBindingsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_gcp_user_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_list_gcp_user_access_bindings(
        self, response: access_context_manager.ListGcpUserAccessBindingsResponse
    ) -> access_context_manager.ListGcpUserAccessBindingsResponse:
        """Post-rpc interceptor for list_gcp_user_access_bindings

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_service_perimeters(
        self,
        request: access_context_manager.ListServicePerimetersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ListServicePerimetersRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_service_perimeters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_list_service_perimeters(
        self, response: access_context_manager.ListServicePerimetersResponse
    ) -> access_context_manager.ListServicePerimetersResponse:
        """Post-rpc interceptor for list_service_perimeters

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_replace_access_levels(
        self,
        request: access_context_manager.ReplaceAccessLevelsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ReplaceAccessLevelsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for replace_access_levels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_replace_access_levels(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for replace_access_levels

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_replace_service_perimeters(
        self,
        request: access_context_manager.ReplaceServicePerimetersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.ReplaceServicePerimetersRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for replace_service_perimeters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_replace_service_perimeters(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for replace_service_perimeters

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.TestIamPermissionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_access_level(
        self,
        request: access_context_manager.UpdateAccessLevelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.UpdateAccessLevelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_access_level

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_update_access_level(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_access_level

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_access_policy(
        self,
        request: access_context_manager.UpdateAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.UpdateAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_update_access_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_access_policy

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_gcp_user_access_binding(
        self,
        request: access_context_manager.UpdateGcpUserAccessBindingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.UpdateGcpUserAccessBindingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_gcp_user_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_update_gcp_user_access_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_gcp_user_access_binding

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_service_perimeter(
        self,
        request: access_context_manager.UpdateServicePerimeterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        access_context_manager.UpdateServicePerimeterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_service_perimeter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_update_service_perimeter(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_service_perimeter

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
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
        before they are sent to the AccessContextManager server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AccessContextManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AccessContextManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AccessContextManagerRestInterceptor


class AccessContextManagerRestTransport(_BaseAccessContextManagerRestTransport):
    """REST backend synchronous transport for AccessContextManager.

    API for setting [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter] for
    Google Cloud projects. Each organization has one [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] that contains
    the [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter]. This
    [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] is applicable
    to all resources in the organization. AccessPolicies

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "accesscontextmanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AccessContextManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'accesscontextmanager.googleapis.com').
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
        self._interceptor = interceptor or AccessContextManagerRestInterceptor()
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
                        "uri": "/v1/{name=operations/**}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CommitServicePerimeters(
        _BaseAccessContextManagerRestTransport._BaseCommitServicePerimeters,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.CommitServicePerimeters")

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
            request: access_context_manager.CommitServicePerimetersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the commit service perimeters method over HTTP.

            Args:
                request (~.access_context_manager.CommitServicePerimetersRequest):
                    The request object. A request to commit dry-run specs in all [Service
                Perimeters]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                belonging to an [Access
                Policy][google.identity.accesscontextmanager.v1.AccessPolicy].
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
                _BaseAccessContextManagerRestTransport._BaseCommitServicePerimeters._get_http_options()
            )

            request, metadata = self._interceptor.pre_commit_service_perimeters(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseCommitServicePerimeters._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseCommitServicePerimeters._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseCommitServicePerimeters._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.CommitServicePerimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CommitServicePerimeters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._CommitServicePerimeters._get_response(
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

            resp = self._interceptor.post_commit_service_perimeters(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.commit_service_perimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CommitServicePerimeters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateAccessLevel(
        _BaseAccessContextManagerRestTransport._BaseCreateAccessLevel,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.CreateAccessLevel")

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
            request: access_context_manager.CreateAccessLevelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create access level method over HTTP.

            Args:
                request (~.access_context_manager.CreateAccessLevelRequest):
                    The request object. A request to create an ``AccessLevel``.
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
                _BaseAccessContextManagerRestTransport._BaseCreateAccessLevel._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_access_level(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseCreateAccessLevel._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseCreateAccessLevel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseCreateAccessLevel._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.CreateAccessLevel",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateAccessLevel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._CreateAccessLevel._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_access_level(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.create_access_level",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateAccessLevel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateAccessPolicy(
        _BaseAccessContextManagerRestTransport._BaseCreateAccessPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.CreateAccessPolicy")

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
            request: access_policy.AccessPolicy,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create access policy method over HTTP.

            Args:
                request (~.access_policy.AccessPolicy):
                    The request object. ``AccessPolicy`` is a container for ``AccessLevels``
                (which define the necessary attributes to use Google
                Cloud services) and ``ServicePerimeters`` (which define
                regions of services able to freely pass data within a
                perimeter). An access policy is globally visible within
                an organization, and the restrictions it specifies apply
                to all projects within an organization.
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
                _BaseAccessContextManagerRestTransport._BaseCreateAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_access_policy(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseCreateAccessPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseCreateAccessPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseCreateAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.CreateAccessPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._CreateAccessPolicy._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_access_policy(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.create_access_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateGcpUserAccessBinding(
        _BaseAccessContextManagerRestTransport._BaseCreateGcpUserAccessBinding,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.CreateGcpUserAccessBinding")

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
            request: access_context_manager.CreateGcpUserAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create gcp user access
            binding method over HTTP.

                Args:
                    request (~.access_context_manager.CreateGcpUserAccessBindingRequest):
                        The request object. Request of [CreateGcpUserAccessBinding]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.CreateGcpUserAccessBinding].
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
                _BaseAccessContextManagerRestTransport._BaseCreateGcpUserAccessBinding._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_gcp_user_access_binding(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseCreateGcpUserAccessBinding._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseCreateGcpUserAccessBinding._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseCreateGcpUserAccessBinding._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.CreateGcpUserAccessBinding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateGcpUserAccessBinding",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._CreateGcpUserAccessBinding._get_response(
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

            resp = self._interceptor.post_create_gcp_user_access_binding(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.create_gcp_user_access_binding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateGcpUserAccessBinding",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateServicePerimeter(
        _BaseAccessContextManagerRestTransport._BaseCreateServicePerimeter,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.CreateServicePerimeter")

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
            request: access_context_manager.CreateServicePerimeterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service perimeter method over HTTP.

            Args:
                request (~.access_context_manager.CreateServicePerimeterRequest):
                    The request object. A request to create a ``ServicePerimeter``.
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
                _BaseAccessContextManagerRestTransport._BaseCreateServicePerimeter._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_service_perimeter(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseCreateServicePerimeter._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseCreateServicePerimeter._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseCreateServicePerimeter._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.CreateServicePerimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateServicePerimeter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._CreateServicePerimeter._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_service_perimeter(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.create_service_perimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "CreateServicePerimeter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteAccessLevel(
        _BaseAccessContextManagerRestTransport._BaseDeleteAccessLevel,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.DeleteAccessLevel")

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
            request: access_context_manager.DeleteAccessLevelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete access level method over HTTP.

            Args:
                request (~.access_context_manager.DeleteAccessLevelRequest):
                    The request object. A request to delete an ``AccessLevel``.
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
                _BaseAccessContextManagerRestTransport._BaseDeleteAccessLevel._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_access_level(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseDeleteAccessLevel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseDeleteAccessLevel._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.DeleteAccessLevel",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteAccessLevel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._DeleteAccessLevel._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_access_level(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.delete_access_level",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteAccessLevel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteAccessPolicy(
        _BaseAccessContextManagerRestTransport._BaseDeleteAccessPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.DeleteAccessPolicy")

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
            request: access_context_manager.DeleteAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete access policy method over HTTP.

            Args:
                request (~.access_context_manager.DeleteAccessPolicyRequest):
                    The request object. A request to delete an ``AccessPolicy``.
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
                _BaseAccessContextManagerRestTransport._BaseDeleteAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_access_policy(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseDeleteAccessPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseDeleteAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.DeleteAccessPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._DeleteAccessPolicy._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_access_policy(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.delete_access_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteGcpUserAccessBinding(
        _BaseAccessContextManagerRestTransport._BaseDeleteGcpUserAccessBinding,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.DeleteGcpUserAccessBinding")

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
            request: access_context_manager.DeleteGcpUserAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete gcp user access
            binding method over HTTP.

                Args:
                    request (~.access_context_manager.DeleteGcpUserAccessBindingRequest):
                        The request object. Request of [DeleteGcpUserAccessBinding]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.DeleteGcpUserAccessBinding].
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
                _BaseAccessContextManagerRestTransport._BaseDeleteGcpUserAccessBinding._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_gcp_user_access_binding(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseDeleteGcpUserAccessBinding._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseDeleteGcpUserAccessBinding._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.DeleteGcpUserAccessBinding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteGcpUserAccessBinding",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._DeleteGcpUserAccessBinding._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_gcp_user_access_binding(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.delete_gcp_user_access_binding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteGcpUserAccessBinding",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteServicePerimeter(
        _BaseAccessContextManagerRestTransport._BaseDeleteServicePerimeter,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.DeleteServicePerimeter")

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
            request: access_context_manager.DeleteServicePerimeterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service perimeter method over HTTP.

            Args:
                request (~.access_context_manager.DeleteServicePerimeterRequest):
                    The request object. A request to delete a ``ServicePerimeter``.
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
                _BaseAccessContextManagerRestTransport._BaseDeleteServicePerimeter._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_service_perimeter(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseDeleteServicePerimeter._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseDeleteServicePerimeter._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.DeleteServicePerimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteServicePerimeter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._DeleteServicePerimeter._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_service_perimeter(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.delete_service_perimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "DeleteServicePerimeter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetAccessLevel(
        _BaseAccessContextManagerRestTransport._BaseGetAccessLevel,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetAccessLevel")

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
            request: access_context_manager.GetAccessLevelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_level.AccessLevel:
            r"""Call the get access level method over HTTP.

            Args:
                request (~.access_context_manager.GetAccessLevelRequest):
                    The request object. A request to get a particular ``AccessLevel``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.access_level.AccessLevel:
                    An ``AccessLevel`` is a label that can be applied to
                requests to Google Cloud services, along with a list of
                requirements necessary for the label to be applied.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseGetAccessLevel._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_access_level(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetAccessLevel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetAccessLevel._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetAccessLevel",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetAccessLevel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._GetAccessLevel._get_response(
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
            resp = access_level.AccessLevel()
            pb_resp = access_level.AccessLevel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_access_level(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = access_level.AccessLevel.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.get_access_level",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetAccessLevel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetAccessPolicy(
        _BaseAccessContextManagerRestTransport._BaseGetAccessPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetAccessPolicy")

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
            request: access_context_manager.GetAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_policy.AccessPolicy:
            r"""Call the get access policy method over HTTP.

            Args:
                request (~.access_context_manager.GetAccessPolicyRequest):
                    The request object. A request to get a particular ``AccessPolicy``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.access_policy.AccessPolicy:
                    ``AccessPolicy`` is a container for ``AccessLevels``
                (which define the necessary attributes to use Google
                Cloud services) and ``ServicePerimeters`` (which define
                regions of services able to freely pass data within a
                perimeter). An access policy is globally visible within
                an organization, and the restrictions it specifies apply
                to all projects within an organization.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseGetAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_access_policy(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetAccessPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetAccessPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._GetAccessPolicy._get_response(
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
            resp = access_policy.AccessPolicy()
            pb_resp = access_policy.AccessPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_access_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = access_policy.AccessPolicy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.get_access_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetGcpUserAccessBinding(
        _BaseAccessContextManagerRestTransport._BaseGetGcpUserAccessBinding,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetGcpUserAccessBinding")

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
            request: access_context_manager.GetGcpUserAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gcp_user_access_binding.GcpUserAccessBinding:
            r"""Call the get gcp user access
            binding method over HTTP.

                Args:
                    request (~.access_context_manager.GetGcpUserAccessBindingRequest):
                        The request object. Request of [GetGcpUserAccessBinding]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.GetGcpUserAccessBinding].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.gcp_user_access_binding.GcpUserAccessBinding:
                        Restricts access to Cloud Console and
                    Google Cloud APIs for a set of users
                    using Context-Aware Access.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseGetGcpUserAccessBinding._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_gcp_user_access_binding(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetGcpUserAccessBinding._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetGcpUserAccessBinding._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetGcpUserAccessBinding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetGcpUserAccessBinding",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._GetGcpUserAccessBinding._get_response(
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
            resp = gcp_user_access_binding.GcpUserAccessBinding()
            pb_resp = gcp_user_access_binding.GcpUserAccessBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_gcp_user_access_binding(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        gcp_user_access_binding.GcpUserAccessBinding.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.get_gcp_user_access_binding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetGcpUserAccessBinding",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetIamPolicy(
        _BaseAccessContextManagerRestTransport._BaseGetIamPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_iam_policy(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.get_iam_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetServicePerimeter(
        _BaseAccessContextManagerRestTransport._BaseGetServicePerimeter,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetServicePerimeter")

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
            request: access_context_manager.GetServicePerimeterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service_perimeter.ServicePerimeter:
            r"""Call the get service perimeter method over HTTP.

            Args:
                request (~.access_context_manager.GetServicePerimeterRequest):
                    The request object. A request to get a particular ``ServicePerimeter``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service_perimeter.ServicePerimeter:
                    ``ServicePerimeter`` describes a set of Google Cloud
                resources which can freely import and export data
                amongst themselves, but not export outside of the
                ``ServicePerimeter``. If a request with a source within
                this ``ServicePerimeter`` has a target outside of the
                ``ServicePerimeter``, the request will be blocked.
                Otherwise the request is allowed. There are two types of
                Service Perimeter - Regular and Bridge. Regular Service
                Perimeters cannot overlap, a single Google Cloud project
                can only belong to a single regular Service Perimeter.
                Service Perimeter Bridges can contain only Google Cloud
                projects as members, a single Google Cloud project may
                belong to multiple Service Perimeter Bridges.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseGetServicePerimeter._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_service_perimeter(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetServicePerimeter._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetServicePerimeter._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetServicePerimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetServicePerimeter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._GetServicePerimeter._get_response(
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
            resp = service_perimeter.ServicePerimeter()
            pb_resp = service_perimeter.ServicePerimeter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_service_perimeter(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service_perimeter.ServicePerimeter.to_json(
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.get_service_perimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetServicePerimeter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAccessLevels(
        _BaseAccessContextManagerRestTransport._BaseListAccessLevels,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ListAccessLevels")

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
            request: access_context_manager.ListAccessLevelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_context_manager.ListAccessLevelsResponse:
            r"""Call the list access levels method over HTTP.

            Args:
                request (~.access_context_manager.ListAccessLevelsRequest):
                    The request object. A request to list all ``AccessLevels`` in an
                ``AccessPolicy``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.access_context_manager.ListAccessLevelsResponse:
                    A response to ``ListAccessLevelsRequest``.
            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseListAccessLevels._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_access_levels(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseListAccessLevels._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseListAccessLevels._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ListAccessLevels",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListAccessLevels",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._ListAccessLevels._get_response(
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
            resp = access_context_manager.ListAccessLevelsResponse()
            pb_resp = access_context_manager.ListAccessLevelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_access_levels(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        access_context_manager.ListAccessLevelsResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.list_access_levels",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListAccessLevels",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAccessPolicies(
        _BaseAccessContextManagerRestTransport._BaseListAccessPolicies,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ListAccessPolicies")

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
            request: access_context_manager.ListAccessPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_context_manager.ListAccessPoliciesResponse:
            r"""Call the list access policies method over HTTP.

            Args:
                request (~.access_context_manager.ListAccessPoliciesRequest):
                    The request object. A request to list all ``AccessPolicies`` for a
                container.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.access_context_manager.ListAccessPoliciesResponse:
                    A response to ``ListAccessPoliciesRequest``.
            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseListAccessPolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_access_policies(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseListAccessPolicies._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseListAccessPolicies._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ListAccessPolicies",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListAccessPolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._ListAccessPolicies._get_response(
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
            resp = access_context_manager.ListAccessPoliciesResponse()
            pb_resp = access_context_manager.ListAccessPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_access_policies(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        access_context_manager.ListAccessPoliciesResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.list_access_policies",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListAccessPolicies",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListGcpUserAccessBindings(
        _BaseAccessContextManagerRestTransport._BaseListGcpUserAccessBindings,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ListGcpUserAccessBindings")

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
            request: access_context_manager.ListGcpUserAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_context_manager.ListGcpUserAccessBindingsResponse:
            r"""Call the list gcp user access
            bindings method over HTTP.

                Args:
                    request (~.access_context_manager.ListGcpUserAccessBindingsRequest):
                        The request object. Request of [ListGcpUserAccessBindings]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.access_context_manager.ListGcpUserAccessBindingsResponse:
                        Response of [ListGcpUserAccessBindings]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseListGcpUserAccessBindings._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_gcp_user_access_bindings(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseListGcpUserAccessBindings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseListGcpUserAccessBindings._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ListGcpUserAccessBindings",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListGcpUserAccessBindings",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._ListGcpUserAccessBindings._get_response(
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
            resp = access_context_manager.ListGcpUserAccessBindingsResponse()
            pb_resp = access_context_manager.ListGcpUserAccessBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_gcp_user_access_bindings(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = access_context_manager.ListGcpUserAccessBindingsResponse.to_json(
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.list_gcp_user_access_bindings",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListGcpUserAccessBindings",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListServicePerimeters(
        _BaseAccessContextManagerRestTransport._BaseListServicePerimeters,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ListServicePerimeters")

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
            request: access_context_manager.ListServicePerimetersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> access_context_manager.ListServicePerimetersResponse:
            r"""Call the list service perimeters method over HTTP.

            Args:
                request (~.access_context_manager.ListServicePerimetersRequest):
                    The request object. A request to list all ``ServicePerimeters`` in an
                ``AccessPolicy``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.access_context_manager.ListServicePerimetersResponse:
                    A response to ``ListServicePerimetersRequest``.
            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseListServicePerimeters._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_service_perimeters(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseListServicePerimeters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseListServicePerimeters._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ListServicePerimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListServicePerimeters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._ListServicePerimeters._get_response(
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
            resp = access_context_manager.ListServicePerimetersResponse()
            pb_resp = access_context_manager.ListServicePerimetersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_service_perimeters(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        access_context_manager.ListServicePerimetersResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.list_service_perimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ListServicePerimeters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ReplaceAccessLevels(
        _BaseAccessContextManagerRestTransport._BaseReplaceAccessLevels,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ReplaceAccessLevels")

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
            request: access_context_manager.ReplaceAccessLevelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the replace access levels method over HTTP.

            Args:
                request (~.access_context_manager.ReplaceAccessLevelsRequest):
                    The request object. A request to replace all existing
                Access Levels in an Access Policy with
                the Access Levels provided. This is done
                atomically.
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
                _BaseAccessContextManagerRestTransport._BaseReplaceAccessLevels._get_http_options()
            )

            request, metadata = self._interceptor.pre_replace_access_levels(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseReplaceAccessLevels._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseReplaceAccessLevels._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseReplaceAccessLevels._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ReplaceAccessLevels",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ReplaceAccessLevels",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._ReplaceAccessLevels._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_replace_access_levels(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.replace_access_levels",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ReplaceAccessLevels",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ReplaceServicePerimeters(
        _BaseAccessContextManagerRestTransport._BaseReplaceServicePerimeters,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.ReplaceServicePerimeters")

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
            request: access_context_manager.ReplaceServicePerimetersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the replace service
            perimeters method over HTTP.

                Args:
                    request (~.access_context_manager.ReplaceServicePerimetersRequest):
                        The request object. A request to replace all existing
                    Service Perimeters in an Access Policy
                    with the Service Perimeters provided.
                    This is done atomically.
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
                _BaseAccessContextManagerRestTransport._BaseReplaceServicePerimeters._get_http_options()
            )

            request, metadata = self._interceptor.pre_replace_service_perimeters(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseReplaceServicePerimeters._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseReplaceServicePerimeters._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseReplaceServicePerimeters._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.ReplaceServicePerimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ReplaceServicePerimeters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._ReplaceServicePerimeters._get_response(
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

            resp = self._interceptor.post_replace_service_perimeters(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.replace_service_perimeters",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "ReplaceServicePerimeters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetIamPolicy(
        _BaseAccessContextManagerRestTransport._BaseSetIamPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseSetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._SetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_set_iam_policy(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.set_iam_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "SetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TestIamPermissions(
        _BaseAccessContextManagerRestTransport._BaseTestIamPermissions,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options = (
                _BaseAccessContextManagerRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseTestIamPermissions._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_test_iam_permissions(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.test_iam_permissions",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "TestIamPermissions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateAccessLevel(
        _BaseAccessContextManagerRestTransport._BaseUpdateAccessLevel,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.UpdateAccessLevel")

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
            request: access_context_manager.UpdateAccessLevelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update access level method over HTTP.

            Args:
                request (~.access_context_manager.UpdateAccessLevelRequest):
                    The request object. A request to update an ``AccessLevel``.
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
                _BaseAccessContextManagerRestTransport._BaseUpdateAccessLevel._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_access_level(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseUpdateAccessLevel._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseUpdateAccessLevel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseUpdateAccessLevel._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.UpdateAccessLevel",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateAccessLevel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._UpdateAccessLevel._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_access_level(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.update_access_level",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateAccessLevel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateAccessPolicy(
        _BaseAccessContextManagerRestTransport._BaseUpdateAccessPolicy,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.UpdateAccessPolicy")

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
            request: access_context_manager.UpdateAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update access policy method over HTTP.

            Args:
                request (~.access_context_manager.UpdateAccessPolicyRequest):
                    The request object. A request to update an ``AccessPolicy``.
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
                _BaseAccessContextManagerRestTransport._BaseUpdateAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_access_policy(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseUpdateAccessPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseUpdateAccessPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseUpdateAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.UpdateAccessPolicy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._UpdateAccessPolicy._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_access_policy(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.update_access_policy",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateGcpUserAccessBinding(
        _BaseAccessContextManagerRestTransport._BaseUpdateGcpUserAccessBinding,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.UpdateGcpUserAccessBinding")

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
            request: access_context_manager.UpdateGcpUserAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update gcp user access
            binding method over HTTP.

                Args:
                    request (~.access_context_manager.UpdateGcpUserAccessBindingRequest):
                        The request object. Request of [UpdateGcpUserAccessBinding]
                    [google.identity.accesscontextmanager.v1.AccessContextManager.UpdateGcpUserAccessBinding].
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
                _BaseAccessContextManagerRestTransport._BaseUpdateGcpUserAccessBinding._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_gcp_user_access_binding(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseUpdateGcpUserAccessBinding._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseUpdateGcpUserAccessBinding._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseUpdateGcpUserAccessBinding._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.UpdateGcpUserAccessBinding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateGcpUserAccessBinding",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._UpdateGcpUserAccessBinding._get_response(
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

            resp = self._interceptor.post_update_gcp_user_access_binding(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.update_gcp_user_access_binding",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateGcpUserAccessBinding",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateServicePerimeter(
        _BaseAccessContextManagerRestTransport._BaseUpdateServicePerimeter,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.UpdateServicePerimeter")

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
            request: access_context_manager.UpdateServicePerimeterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update service perimeter method over HTTP.

            Args:
                request (~.access_context_manager.UpdateServicePerimeterRequest):
                    The request object. A request to update a ``ServicePerimeter``.
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
                _BaseAccessContextManagerRestTransport._BaseUpdateServicePerimeter._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_service_perimeter(
                request, metadata
            )
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseUpdateServicePerimeter._get_transcoded_request(
                http_options, request
            )

            body = _BaseAccessContextManagerRestTransport._BaseUpdateServicePerimeter._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseUpdateServicePerimeter._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.UpdateServicePerimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateServicePerimeter",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AccessContextManagerRestTransport._UpdateServicePerimeter._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_service_perimeter(resp)
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerClient.update_service_perimeter",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "UpdateServicePerimeter",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def commit_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.CommitServicePerimetersRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CommitServicePerimeters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_access_level(
        self,
    ) -> Callable[
        [access_context_manager.CreateAccessLevelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAccessLevel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_access_policy(
        self,
    ) -> Callable[[access_policy.AccessPolicy], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.CreateGcpUserAccessBindingRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGcpUserAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.CreateServicePerimeterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServicePerimeter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_access_level(
        self,
    ) -> Callable[
        [access_context_manager.DeleteAccessLevelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccessLevel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.DeleteAccessPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.DeleteGcpUserAccessBindingRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGcpUserAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.DeleteServicePerimeterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteServicePerimeter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_access_level(
        self,
    ) -> Callable[
        [access_context_manager.GetAccessLevelRequest], access_level.AccessLevel
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccessLevel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.GetAccessPolicyRequest], access_policy.AccessPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.GetGcpUserAccessBindingRequest],
        gcp_user_access_binding.GcpUserAccessBinding,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGcpUserAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.GetServicePerimeterRequest],
        service_perimeter.ServicePerimeter,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServicePerimeter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_access_levels(
        self,
    ) -> Callable[
        [access_context_manager.ListAccessLevelsRequest],
        access_context_manager.ListAccessLevelsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccessLevels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_access_policies(
        self,
    ) -> Callable[
        [access_context_manager.ListAccessPoliciesRequest],
        access_context_manager.ListAccessPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccessPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_gcp_user_access_bindings(
        self,
    ) -> Callable[
        [access_context_manager.ListGcpUserAccessBindingsRequest],
        access_context_manager.ListGcpUserAccessBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGcpUserAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.ListServicePerimetersRequest],
        access_context_manager.ListServicePerimetersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServicePerimeters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def replace_access_levels(
        self,
    ) -> Callable[
        [access_context_manager.ReplaceAccessLevelsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReplaceAccessLevels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def replace_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.ReplaceServicePerimetersRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReplaceServicePerimeters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_access_level(
        self,
    ) -> Callable[
        [access_context_manager.UpdateAccessLevelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccessLevel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.UpdateAccessPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.UpdateGcpUserAccessBindingRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGcpUserAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.UpdateServicePerimeterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateServicePerimeter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseAccessContextManagerRestTransport._BaseGetOperation,
        AccessContextManagerRestStub,
    ):
        def __hash__(self):
            return hash("AccessContextManagerRestTransport.GetOperation")

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
                _BaseAccessContextManagerRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseAccessContextManagerRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAccessContextManagerRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.identity.accesscontextmanager_v1.AccessContextManagerClient.GetOperation",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AccessContextManagerRestTransport._GetOperation._get_response(
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
                    "Received response for google.identity.accesscontextmanager_v1.AccessContextManagerAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                        "rpcName": "GetOperation",
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


__all__ = ("AccessContextManagerRestTransport",)
