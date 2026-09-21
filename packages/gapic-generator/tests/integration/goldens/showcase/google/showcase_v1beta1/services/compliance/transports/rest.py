# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
import logging
import json  # type: ignore

from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import gapic_v1
from google.showcase_v1beta1._compat import transcode_request
import google.protobuf

from google.protobuf import json_format
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.cloud.location import locations_pb2 # type: ignore

from requests import __version__ as requests_version
import dataclasses
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings


from google.showcase_v1beta1.types import compliance
from google.longrunning import operations_pb2  # type: ignore


from .rest_base import _BaseComplianceRestTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

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

DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class ComplianceRestInterceptor:
    """Interceptor for Compliance.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ComplianceRestTransport.

    .. code-block:: python
        class MyCustomComplianceInterceptor(ComplianceRestInterceptor):
            def pre_get_enum(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_enum(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_body(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_body(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_body_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_body_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_body_patch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_body_patch(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_body_put(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_body_put(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_path_resource(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_path_resource(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_path_trailing_resource(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_path_trailing_resource(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_query(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repeat_data_simple_path(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repeat_data_simple_path(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_verify_enum(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_verify_enum(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ComplianceRestTransport(interceptor=MyCustomComplianceInterceptor())
        client = ComplianceClient(transport=transport)


    """
    def pre_get_enum(self, request: compliance.EnumRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.EnumRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_enum

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_get_enum(self, response: compliance.EnumResponse) -> compliance.EnumResponse:
        """Post-rpc interceptor for get_enum

        DEPRECATED. Please use the `post_get_enum_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_get_enum` interceptor runs
        before the `post_get_enum_with_metadata` interceptor.
        """
        return response

    def post_get_enum_with_metadata(self, response: compliance.EnumResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.EnumResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_enum

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_get_enum_with_metadata`
        interceptor in new development instead of the `post_get_enum` interceptor.
        When both interceptors are used, this `post_get_enum_with_metadata` interceptor runs after the
        `post_get_enum` interceptor. The (possibly modified) response returned by
        `post_get_enum` will be passed to
        `post_get_enum_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_body(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_body

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_body(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_body

        DEPRECATED. Please use the `post_repeat_data_body_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_body` interceptor runs
        before the `post_repeat_data_body_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_body_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_body

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_body_with_metadata`
        interceptor in new development instead of the `post_repeat_data_body` interceptor.
        When both interceptors are used, this `post_repeat_data_body_with_metadata` interceptor runs after the
        `post_repeat_data_body` interceptor. The (possibly modified) response returned by
        `post_repeat_data_body` will be passed to
        `post_repeat_data_body_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_body_info(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_body_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_body_info(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_body_info

        DEPRECATED. Please use the `post_repeat_data_body_info_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_body_info` interceptor runs
        before the `post_repeat_data_body_info_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_body_info_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_body_info

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_body_info_with_metadata`
        interceptor in new development instead of the `post_repeat_data_body_info` interceptor.
        When both interceptors are used, this `post_repeat_data_body_info_with_metadata` interceptor runs after the
        `post_repeat_data_body_info` interceptor. The (possibly modified) response returned by
        `post_repeat_data_body_info` will be passed to
        `post_repeat_data_body_info_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_body_patch(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_body_patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_body_patch(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_body_patch

        DEPRECATED. Please use the `post_repeat_data_body_patch_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_body_patch` interceptor runs
        before the `post_repeat_data_body_patch_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_body_patch_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_body_patch

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_body_patch_with_metadata`
        interceptor in new development instead of the `post_repeat_data_body_patch` interceptor.
        When both interceptors are used, this `post_repeat_data_body_patch_with_metadata` interceptor runs after the
        `post_repeat_data_body_patch` interceptor. The (possibly modified) response returned by
        `post_repeat_data_body_patch` will be passed to
        `post_repeat_data_body_patch_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_body_put(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_body_put

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_body_put(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_body_put

        DEPRECATED. Please use the `post_repeat_data_body_put_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_body_put` interceptor runs
        before the `post_repeat_data_body_put_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_body_put_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_body_put

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_body_put_with_metadata`
        interceptor in new development instead of the `post_repeat_data_body_put` interceptor.
        When both interceptors are used, this `post_repeat_data_body_put_with_metadata` interceptor runs after the
        `post_repeat_data_body_put` interceptor. The (possibly modified) response returned by
        `post_repeat_data_body_put` will be passed to
        `post_repeat_data_body_put_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_path_resource(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_path_resource

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_path_resource(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_path_resource

        DEPRECATED. Please use the `post_repeat_data_path_resource_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_path_resource` interceptor runs
        before the `post_repeat_data_path_resource_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_path_resource_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_path_resource

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_path_resource_with_metadata`
        interceptor in new development instead of the `post_repeat_data_path_resource` interceptor.
        When both interceptors are used, this `post_repeat_data_path_resource_with_metadata` interceptor runs after the
        `post_repeat_data_path_resource` interceptor. The (possibly modified) response returned by
        `post_repeat_data_path_resource` will be passed to
        `post_repeat_data_path_resource_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_path_trailing_resource(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_path_trailing_resource

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_path_trailing_resource(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_path_trailing_resource

        DEPRECATED. Please use the `post_repeat_data_path_trailing_resource_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_path_trailing_resource` interceptor runs
        before the `post_repeat_data_path_trailing_resource_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_path_trailing_resource_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_path_trailing_resource

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_path_trailing_resource_with_metadata`
        interceptor in new development instead of the `post_repeat_data_path_trailing_resource` interceptor.
        When both interceptors are used, this `post_repeat_data_path_trailing_resource_with_metadata` interceptor runs after the
        `post_repeat_data_path_trailing_resource` interceptor. The (possibly modified) response returned by
        `post_repeat_data_path_trailing_resource` will be passed to
        `post_repeat_data_path_trailing_resource_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_query(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_query(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_query

        DEPRECATED. Please use the `post_repeat_data_query_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_query` interceptor runs
        before the `post_repeat_data_query_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_query_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_query

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_query_with_metadata`
        interceptor in new development instead of the `post_repeat_data_query` interceptor.
        When both interceptors are used, this `post_repeat_data_query_with_metadata` interceptor runs after the
        `post_repeat_data_query` interceptor. The (possibly modified) response returned by
        `post_repeat_data_query` will be passed to
        `post_repeat_data_query_with_metadata`.
        """
        return response, metadata

    def pre_repeat_data_simple_path(self, request: compliance.RepeatRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for repeat_data_simple_path

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_repeat_data_simple_path(self, response: compliance.RepeatResponse) -> compliance.RepeatResponse:
        """Post-rpc interceptor for repeat_data_simple_path

        DEPRECATED. Please use the `post_repeat_data_simple_path_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_repeat_data_simple_path` interceptor runs
        before the `post_repeat_data_simple_path_with_metadata` interceptor.
        """
        return response

    def post_repeat_data_simple_path_with_metadata(self, response: compliance.RepeatResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.RepeatResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for repeat_data_simple_path

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_repeat_data_simple_path_with_metadata`
        interceptor in new development instead of the `post_repeat_data_simple_path` interceptor.
        When both interceptors are used, this `post_repeat_data_simple_path_with_metadata` interceptor runs after the
        `post_repeat_data_simple_path` interceptor. The (possibly modified) response returned by
        `post_repeat_data_simple_path` will be passed to
        `post_repeat_data_simple_path_with_metadata`.
        """
        return response, metadata

    def pre_verify_enum(self, request: compliance.EnumResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.EnumResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for verify_enum

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_verify_enum(self, response: compliance.EnumResponse) -> compliance.EnumResponse:
        """Post-rpc interceptor for verify_enum

        DEPRECATED. Please use the `post_verify_enum_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code. This `post_verify_enum` interceptor runs
        before the `post_verify_enum_with_metadata` interceptor.
        """
        return response

    def post_verify_enum_with_metadata(self, response: compliance.EnumResponse, metadata: Sequence[Tuple[str, Union[str, bytes]]]) -> Tuple[compliance.EnumResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for verify_enum

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Compliance server but before it is returned to user code.

        We recommend only using this `post_verify_enum_with_metadata`
        interceptor in new development instead of the `post_verify_enum` interceptor.
        When both interceptors are used, this `post_verify_enum_with_metadata` interceptor runs after the
        `post_verify_enum` interceptor. The (possibly modified) response returned by
        `post_verify_enum` will be passed to
        `post_verify_enum_with_metadata`.
        """
        return response, metadata

    def pre_list_locations(
        self, request: locations_pb2.ListLocationsRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self, request: locations_pb2.GetLocationRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self, request: iam_policy_pb2.SetIamPolicyRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_set_iam_policy(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self, request: iam_policy_pb2.GetIamPolicyRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_get_iam_policy(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self, request: iam_policy_pb2.TestIamPermissionsRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self, request: operations_pb2.ListOperationsRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self, request: operations_pb2.GetOperationRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self, request: operations_pb2.DeleteOperationRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_delete_operation(
        self, response: None
    ) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self, request: operations_pb2.CancelOperationRequest, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Compliance server.
        """
        return request, metadata

    def post_cancel_operation(
        self, response: None
    ) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Compliance server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ComplianceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ComplianceRestInterceptor


class ComplianceRestTransport(_BaseComplianceRestTransport):
    """REST backend synchronous transport for Compliance.

    This service is used to test that GAPICs implement various
    REST-related features correctly. This mostly means transcoding
    proto3 requests to REST format correctly for various types of
    HTTP annotations, but it also includes verifying that unknown
    (numeric) enums received by clients can be round-tripped
    correctly.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(self, *,
            host: str = 'localhost:7469',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[ComplianceRestInterceptor] = None,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

       NOTE: This REST transport functionality is currently in a beta
       state (preview). We welcome your feedback via a GitHub issue in
       this library's repository. Thank you!

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'localhost:7469').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
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
            interceptor (Optional[ComplianceRestInterceptor]): Interceptor used
                to manipulate requests, request metadata, and responses.
            api_audience (Optional[str]): The intended audience for the API calls
                to the service that will be set when using certain 3rd party
                authentication flows. Audience is typically a resource identifier.
                If not set, the host value will be used as a default.
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
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ComplianceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetEnum(_BaseComplianceRestTransport._BaseGetEnum, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.GetEnum")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.EnumRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.EnumResponse:
            r"""Call the get enum method over HTTP.

            Args:
                request (~.compliance.EnumRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.EnumResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseGetEnum._get_http_options()
            request, metadata = self._interceptor.pre_get_enum(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseGetEnum,
                    "_BaseGetEnum__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.GetEnum",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetEnum",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._GetEnum._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.EnumResponse()
            pb_resp = compliance.EnumResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_enum(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_enum_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.EnumResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.get_enum",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetEnum",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataBody(_BaseComplianceRestTransport._BaseRepeatDataBody, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataBody")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data body method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataBody._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_body(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataBody,
                    "_BaseRepeatDataBody__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataBody",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBody",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataBody._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_body(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_body_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_body",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBody",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataBodyInfo(_BaseComplianceRestTransport._BaseRepeatDataBodyInfo, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataBodyInfo")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data body info method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataBodyInfo._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_body_info(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataBodyInfo,
                    "_BaseRepeatDataBodyInfo__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataBodyInfo",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyInfo",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataBodyInfo._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_body_info(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_body_info_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_body_info",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyInfo",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataBodyPatch(_BaseComplianceRestTransport._BaseRepeatDataBodyPatch, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataBodyPatch")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data body patch method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataBodyPatch._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_body_patch(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataBodyPatch,
                    "_BaseRepeatDataBodyPatch__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataBodyPatch",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyPatch",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataBodyPatch._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_body_patch(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_body_patch_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_body_patch",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyPatch",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataBodyPut(_BaseComplianceRestTransport._BaseRepeatDataBodyPut, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataBodyPut")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data body put method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataBodyPut._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_body_put(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataBodyPut,
                    "_BaseRepeatDataBodyPut__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataBodyPut",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyPut",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataBodyPut._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_body_put(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_body_put_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_body_put",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataBodyPut",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataPathResource(_BaseComplianceRestTransport._BaseRepeatDataPathResource, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataPathResource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data path resource method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataPathResource._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_path_resource(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataPathResource,
                    "_BaseRepeatDataPathResource__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataPathResource",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataPathResource",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataPathResource._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_path_resource(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_path_resource_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_path_resource",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataPathResource",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataPathTrailingResource(_BaseComplianceRestTransport._BaseRepeatDataPathTrailingResource, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataPathTrailingResource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data path trailing
        resource method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataPathTrailingResource._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_path_trailing_resource(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataPathTrailingResource,
                    "_BaseRepeatDataPathTrailingResource__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataPathTrailingResource",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataPathTrailingResource",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataPathTrailingResource._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_path_trailing_resource(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_path_trailing_resource_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_path_trailing_resource",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataPathTrailingResource",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataQuery(_BaseComplianceRestTransport._BaseRepeatDataQuery, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataQuery")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data query method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataQuery._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_query(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataQuery,
                    "_BaseRepeatDataQuery__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataQuery",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataQuery",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataQuery._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_query(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_query_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_query",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataQuery",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RepeatDataSimplePath(_BaseComplianceRestTransport._BaseRepeatDataSimplePath, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.RepeatDataSimplePath")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.RepeatRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.RepeatResponse:
            r"""Call the repeat data simple path method over HTTP.

            Args:
                request (~.compliance.RepeatRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.RepeatResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseRepeatDataSimplePath._get_http_options()
            request, metadata = self._interceptor.pre_repeat_data_simple_path(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseRepeatDataSimplePath,
                    "_BaseRepeatDataSimplePath__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.RepeatDataSimplePath",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataSimplePath",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._RepeatDataSimplePath._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.RepeatResponse()
            pb_resp = compliance.RepeatResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_repeat_data_simple_path(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_repeat_data_simple_path_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.RepeatResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.repeat_data_simple_path",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "RepeatDataSimplePath",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _VerifyEnum(_BaseComplianceRestTransport._BaseVerifyEnum, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.VerifyEnum")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
                request: compliance.EnumResponse, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
                ) -> compliance.EnumResponse:
            r"""Call the verify enum method over HTTP.

            Args:
                request (~.compliance.EnumResponse):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compliance.EnumResponse:

            """

            http_options = _BaseComplianceRestTransport._BaseVerifyEnum._get_http_options()
            request, metadata = self._interceptor.pre_verify_enum(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseVerifyEnum,
                    "_BaseVerifyEnum__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.VerifyEnum",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "VerifyEnum",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._VerifyEnum._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compliance.EnumResponse()
            pb_resp = compliance.EnumResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_verify_enum(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_verify_enum_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = compliance.EnumResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                "payload": response_payload,
                "headers":  dict(response.headers),
                "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceClient.verify_enum",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "VerifyEnum",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get_enum(self) -> Callable[
            [compliance.EnumRequest],
            compliance.EnumResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEnum(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_body(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataBody(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_body_info(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataBodyInfo(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_body_patch(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataBodyPatch(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_body_put(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataBodyPut(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_path_resource(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataPathResource(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_path_trailing_resource(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataPathTrailingResource(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_query(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataQuery(self._session, self._host, self._interceptor) # type: ignore

    @property
    def repeat_data_simple_path(self) -> Callable[
            [compliance.RepeatRequest],
            compliance.RepeatResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepeatDataSimplePath(self._session, self._host, self._interceptor) # type: ignore

    @property
    def verify_enum(self) -> Callable[
            [compliance.EnumResponse],
            compliance.EnumResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._VerifyEnum(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor) # type: ignore

    class _ListLocations(_BaseComplianceRestTransport._BaseListLocations, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: locations_pb2.ListLocationsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> locations_pb2.ListLocationsResponse:

            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = _BaseComplianceRestTransport._BaseListLocations._get_http_options()
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseListLocations,
                    "_BaseListLocations__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.ListLocations",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._ListLocations._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.ListLocations",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor) # type: ignore

    class _GetLocation(_BaseComplianceRestTransport._BaseGetLocation, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: locations_pb2.GetLocationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> locations_pb2.Location:

            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = _BaseComplianceRestTransport._BaseGetLocation._get_http_options()
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseGetLocation,
                    "_BaseGetLocation__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.GetLocation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._GetLocation._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.GetLocation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor) # type: ignore

    class _SetIamPolicy(_BaseComplianceRestTransport._BaseSetIamPolicy, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.SetIamPolicy")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
            request: iam_policy_pb2.SetIamPolicyRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> policy_pb2.Policy:

            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = _BaseComplianceRestTransport._BaseSetIamPolicy._get_http_options()
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseSetIamPolicy,
                    "_BaseSetIamPolicy__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.SetIamPolicy",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._SetIamPolicy._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.SetIamPolicy",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "SetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor) # type: ignore

    class _GetIamPolicy(_BaseComplianceRestTransport._BaseGetIamPolicy, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.GetIamPolicy")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: iam_policy_pb2.GetIamPolicyRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> policy_pb2.Policy:

            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = _BaseComplianceRestTransport._BaseGetIamPolicy._get_http_options()
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseGetIamPolicy,
                    "_BaseGetIamPolicy__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.GetIamPolicy",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._GetIamPolicy._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.GetIamPolicy",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor) # type: ignore

    class _TestIamPermissions(_BaseComplianceRestTransport._BaseTestIamPermissions, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.TestIamPermissions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )
            return response

        def __call__(self,
            request: iam_policy_pb2.TestIamPermissionsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> iam_policy_pb2.TestIamPermissionsResponse:

            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = _BaseComplianceRestTransport._BaseTestIamPermissions._get_http_options()
            request, metadata = self._interceptor.pre_test_iam_permissions(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseTestIamPermissions,
                    "_BaseTestIamPermissions__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.TestIamPermissions",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._TestIamPermissions._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request, body)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.TestIamPermissions",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "TestIamPermissions",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor) # type: ignore

    class _ListOperations(_BaseComplianceRestTransport._BaseListOperations, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: operations_pb2.ListOperationsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
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

            http_options = _BaseComplianceRestTransport._BaseListOperations._get_http_options()
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseListOperations,
                    "_BaseListOperations__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.ListOperations",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._ListOperations._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.ListOperations",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor) # type: ignore

    class _GetOperation(_BaseComplianceRestTransport._BaseGetOperation, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: operations_pb2.GetOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
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

            http_options = _BaseComplianceRestTransport._BaseGetOperation._get_http_options()
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseGetOperation,
                    "_BaseGetOperation__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.GetOperation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._GetOperation._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers":  dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.showcase_v1beta1.ComplianceAsyncClient.GetOperation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor) # type: ignore

    class _DeleteOperation(_BaseComplianceRestTransport._BaseDeleteOperation, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: operations_pb2.DeleteOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> None:

            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = _BaseComplianceRestTransport._BaseDeleteOperation._get_http_options()
            request, metadata = self._interceptor.pre_delete_operation(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseDeleteOperation,
                    "_BaseDeleteOperation__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.DeleteOperation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._DeleteOperation._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor) # type: ignore

    class _CancelOperation(_BaseComplianceRestTransport._BaseCancelOperation, ComplianceRestStub):
        def __hash__(self):
            return hash("ComplianceRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None):

            uri = transcoded_request['uri']
            method = transcoded_request['method']
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )
            return response

        def __call__(self,
            request: operations_pb2.CancelOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]]=(),
            ) -> None:

            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = _BaseComplianceRestTransport._BaseCancelOperation._get_http_options()
            request, metadata = self._interceptor.pre_cancel_operation(request, metadata)
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseComplianceRestTransport._BaseCancelOperation,
                    "_BaseCancelOperation__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(logging.DEBUG):  # pragma: NO COVER
                request_url = "{host}{uri}".format(host=self._host, uri=transcoded_request['uri'])
                method = transcoded_request['method']
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
                    f"Sending request for google.showcase_v1beta1.ComplianceClient.CancelOperation",
                    extra = {
                        "serviceName": "google.showcase.v1beta1.Compliance",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ComplianceRestTransport._CancelOperation._get_response(self._host, metadata, query_params, self._session, timeout, transcoded_request)

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'ComplianceRestTransport',
)
