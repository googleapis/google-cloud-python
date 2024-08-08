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

from google.cloud.apihub_v1.types import apihub_service, common_fields

from .base import ApiHubTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ApiHubRestInterceptor:
    """Interceptor for ApiHub.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ApiHubRestTransport.

    .. code-block:: python
        class MyCustomApiHubInterceptor(ApiHubRestInterceptor):
            def pre_create_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_external_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_external_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_external_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_operation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_operation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_definition(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_definition(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_external_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_external_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_spec_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_spec_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_operations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_operations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_apis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_apis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_attributes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_attributes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_external_apis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_external_apis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_specs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_specs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_resources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_resources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_attribute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_attribute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_external_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_external_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ApiHubRestTransport(interceptor=MyCustomApiHubInterceptor())
        client = ApiHubClient(transport=transport)


    """

    def pre_create_api(
        self,
        request: apihub_service.CreateApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_api(self, response: common_fields.Api) -> common_fields.Api:
        """Post-rpc interceptor for create_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_attribute(
        self,
        request: apihub_service.CreateAttributeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_attribute(
        self, response: common_fields.Attribute
    ) -> common_fields.Attribute:
        """Post-rpc interceptor for create_attribute

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_deployment(
        self,
        request: apihub_service.CreateDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_deployment(
        self, response: common_fields.Deployment
    ) -> common_fields.Deployment:
        """Post-rpc interceptor for create_deployment

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_external_api(
        self,
        request: apihub_service.CreateExternalApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateExternalApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_external_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_external_api(
        self, response: common_fields.ExternalApi
    ) -> common_fields.ExternalApi:
        """Post-rpc interceptor for create_external_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_spec(
        self,
        request: apihub_service.CreateSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_spec(self, response: common_fields.Spec) -> common_fields.Spec:
        """Post-rpc interceptor for create_spec

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_version(
        self,
        request: apihub_service.CreateVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.CreateVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_create_version(
        self, response: common_fields.Version
    ) -> common_fields.Version:
        """Post-rpc interceptor for create_version

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api(
        self,
        request: apihub_service.DeleteApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_delete_attribute(
        self,
        request: apihub_service.DeleteAttributeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_delete_deployment(
        self,
        request: apihub_service.DeleteDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_delete_external_api(
        self,
        request: apihub_service.DeleteExternalApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteExternalApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_external_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_delete_spec(
        self,
        request: apihub_service.DeleteSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_delete_version(
        self,
        request: apihub_service.DeleteVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.DeleteVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def pre_get_api(
        self, request: apihub_service.GetApiRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apihub_service.GetApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_api(self, response: common_fields.Api) -> common_fields.Api:
        """Post-rpc interceptor for get_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_operation(
        self,
        request: apihub_service.GetApiOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetApiOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_api_operation(
        self, response: common_fields.ApiOperation
    ) -> common_fields.ApiOperation:
        """Post-rpc interceptor for get_api_operation

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_attribute(
        self,
        request: apihub_service.GetAttributeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_attribute(
        self, response: common_fields.Attribute
    ) -> common_fields.Attribute:
        """Post-rpc interceptor for get_attribute

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_definition(
        self,
        request: apihub_service.GetDefinitionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetDefinitionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_definition

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_definition(
        self, response: common_fields.Definition
    ) -> common_fields.Definition:
        """Post-rpc interceptor for get_definition

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_deployment(
        self,
        request: apihub_service.GetDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_deployment(
        self, response: common_fields.Deployment
    ) -> common_fields.Deployment:
        """Post-rpc interceptor for get_deployment

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_external_api(
        self,
        request: apihub_service.GetExternalApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetExternalApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_external_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_external_api(
        self, response: common_fields.ExternalApi
    ) -> common_fields.ExternalApi:
        """Post-rpc interceptor for get_external_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_spec(
        self,
        request: apihub_service.GetSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_spec(self, response: common_fields.Spec) -> common_fields.Spec:
        """Post-rpc interceptor for get_spec

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_spec_contents(
        self,
        request: apihub_service.GetSpecContentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetSpecContentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_spec_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_spec_contents(
        self, response: common_fields.SpecContents
    ) -> common_fields.SpecContents:
        """Post-rpc interceptor for get_spec_contents

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_version(
        self,
        request: apihub_service.GetVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.GetVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_version(
        self, response: common_fields.Version
    ) -> common_fields.Version:
        """Post-rpc interceptor for get_version

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_operations(
        self,
        request: apihub_service.ListApiOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListApiOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_api_operations(
        self, response: apihub_service.ListApiOperationsResponse
    ) -> apihub_service.ListApiOperationsResponse:
        """Post-rpc interceptor for list_api_operations

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_apis(
        self,
        request: apihub_service.ListApisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListApisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_apis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_apis(
        self, response: apihub_service.ListApisResponse
    ) -> apihub_service.ListApisResponse:
        """Post-rpc interceptor for list_apis

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_attributes(
        self,
        request: apihub_service.ListAttributesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListAttributesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_attributes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_attributes(
        self, response: apihub_service.ListAttributesResponse
    ) -> apihub_service.ListAttributesResponse:
        """Post-rpc interceptor for list_attributes

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_deployments(
        self,
        request: apihub_service.ListDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListDeploymentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_deployments(
        self, response: apihub_service.ListDeploymentsResponse
    ) -> apihub_service.ListDeploymentsResponse:
        """Post-rpc interceptor for list_deployments

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_external_apis(
        self,
        request: apihub_service.ListExternalApisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListExternalApisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_external_apis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_external_apis(
        self, response: apihub_service.ListExternalApisResponse
    ) -> apihub_service.ListExternalApisResponse:
        """Post-rpc interceptor for list_external_apis

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_specs(
        self,
        request: apihub_service.ListSpecsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListSpecsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_specs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_specs(
        self, response: apihub_service.ListSpecsResponse
    ) -> apihub_service.ListSpecsResponse:
        """Post-rpc interceptor for list_specs

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_versions(
        self,
        request: apihub_service.ListVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.ListVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_versions(
        self, response: apihub_service.ListVersionsResponse
    ) -> apihub_service.ListVersionsResponse:
        """Post-rpc interceptor for list_versions

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_search_resources(
        self,
        request: apihub_service.SearchResourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.SearchResourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_resources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_search_resources(
        self, response: apihub_service.SearchResourcesResponse
    ) -> apihub_service.SearchResourcesResponse:
        """Post-rpc interceptor for search_resources

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_api(
        self,
        request: apihub_service.UpdateApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_api(self, response: common_fields.Api) -> common_fields.Api:
        """Post-rpc interceptor for update_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_attribute(
        self,
        request: apihub_service.UpdateAttributeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateAttributeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_attribute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_attribute(
        self, response: common_fields.Attribute
    ) -> common_fields.Attribute:
        """Post-rpc interceptor for update_attribute

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_deployment(
        self,
        request: apihub_service.UpdateDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_deployment(
        self, response: common_fields.Deployment
    ) -> common_fields.Deployment:
        """Post-rpc interceptor for update_deployment

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_external_api(
        self,
        request: apihub_service.UpdateExternalApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateExternalApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_external_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_external_api(
        self, response: common_fields.ExternalApi
    ) -> common_fields.ExternalApi:
        """Post-rpc interceptor for update_external_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_spec(
        self,
        request: apihub_service.UpdateSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_spec(self, response: common_fields.Spec) -> common_fields.Spec:
        """Post-rpc interceptor for update_spec

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_version(
        self,
        request: apihub_service.UpdateVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apihub_service.UpdateVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_update_version(
        self, response: common_fields.Version
    ) -> common_fields.Version:
        """Post-rpc interceptor for update_version

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
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
        before they are sent to the ApiHub server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ApiHub server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ApiHubRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ApiHubRestInterceptor


class ApiHubRestTransport(ApiHubTransport):
    """REST backend transport for ApiHub.

    This service provides all methods related to the API hub.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "apihub.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ApiHubRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apihub.googleapis.com').
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
        self._interceptor = interceptor or ApiHubRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateApi(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateApi")

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
            request: apihub_service.CreateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Api:
            r"""Call the create api method over HTTP.

            Args:
                request (~.apihub_service.CreateApiRequest):
                    The request object. The [CreateApi][google.cloud.apihub.v1.ApiHub.CreateApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Api:
                    An API resource in the API Hub.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/apis",
                    "body": "api",
                },
            ]
            request, metadata = self._interceptor.pre_create_api(request, metadata)
            pb_request = apihub_service.CreateApiRequest.pb(request)
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
            resp = common_fields.Api()
            pb_resp = common_fields.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_api(resp)
            return resp

    class _CreateAttribute(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateAttribute")

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
            request: apihub_service.CreateAttributeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Attribute:
            r"""Call the create attribute method over HTTP.

            Args:
                request (~.apihub_service.CreateAttributeRequest):
                    The request object. The
                [CreateAttribute][google.cloud.apihub.v1.ApiHub.CreateAttribute]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Attribute:
                    An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/attributes",
                    "body": "attribute",
                },
            ]
            request, metadata = self._interceptor.pre_create_attribute(
                request, metadata
            )
            pb_request = apihub_service.CreateAttributeRequest.pb(request)
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
            resp = common_fields.Attribute()
            pb_resp = common_fields.Attribute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_attribute(resp)
            return resp

    class _CreateDeployment(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateDeployment")

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
            request: apihub_service.CreateDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Deployment:
            r"""Call the create deployment method over HTTP.

            Args:
                request (~.apihub_service.CreateDeploymentRequest):
                    The request object. The
                [CreateDeployment][google.cloud.apihub.v1.ApiHub.CreateDeployment]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Deployment:
                    Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/deployments",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_create_deployment(
                request, metadata
            )
            pb_request = apihub_service.CreateDeploymentRequest.pb(request)
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
            resp = common_fields.Deployment()
            pb_resp = common_fields.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_deployment(resp)
            return resp

    class _CreateExternalApi(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateExternalApi")

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
            request: apihub_service.CreateExternalApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.ExternalApi:
            r"""Call the create external api method over HTTP.

            Args:
                request (~.apihub_service.CreateExternalApiRequest):
                    The request object. The
                [CreateExternalApi][google.cloud.apihub.v1.ApiHub.CreateExternalApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.ExternalApi:
                    An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/externalApis",
                    "body": "external_api",
                },
            ]
            request, metadata = self._interceptor.pre_create_external_api(
                request, metadata
            )
            pb_request = apihub_service.CreateExternalApiRequest.pb(request)
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
            resp = common_fields.ExternalApi()
            pb_resp = common_fields.ExternalApi.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_external_api(resp)
            return resp

    class _CreateSpec(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateSpec")

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
            request: apihub_service.CreateSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Spec:
            r"""Call the create spec method over HTTP.

            Args:
                request (~.apihub_service.CreateSpecRequest):
                    The request object. The
                [CreateSpec][google.cloud.apihub.v1.ApiHub.CreateSpec]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Spec:
                    Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs",
                    "body": "spec",
                },
            ]
            request, metadata = self._interceptor.pre_create_spec(request, metadata)
            pb_request = apihub_service.CreateSpecRequest.pb(request)
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
            resp = common_fields.Spec()
            pb_resp = common_fields.Spec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_spec(resp)
            return resp

    class _CreateVersion(ApiHubRestStub):
        def __hash__(self):
            return hash("CreateVersion")

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
            request: apihub_service.CreateVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Version:
            r"""Call the create version method over HTTP.

            Args:
                request (~.apihub_service.CreateVersionRequest):
                    The request object. The
                [CreateVersion][google.cloud.apihub.v1.ApiHub.CreateVersion]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Version:
                    Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/versions",
                    "body": "version",
                },
            ]
            request, metadata = self._interceptor.pre_create_version(request, metadata)
            pb_request = apihub_service.CreateVersionRequest.pb(request)
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
            resp = common_fields.Version()
            pb_resp = common_fields.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_version(resp)
            return resp

    class _DeleteApi(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteApi")

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
            request: apihub_service.DeleteApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete api method over HTTP.

            Args:
                request (~.apihub_service.DeleteApiRequest):
                    The request object. The [DeleteApi][google.cloud.apihub.v1.ApiHub.DeleteApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api(request, metadata)
            pb_request = apihub_service.DeleteApiRequest.pb(request)
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

    class _DeleteAttribute(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteAttribute")

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
            request: apihub_service.DeleteAttributeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete attribute method over HTTP.

            Args:
                request (~.apihub_service.DeleteAttributeRequest):
                    The request object. The
                [DeleteAttribute][google.cloud.apihub.v1.ApiHub.DeleteAttribute]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/attributes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_attribute(
                request, metadata
            )
            pb_request = apihub_service.DeleteAttributeRequest.pb(request)
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

    class _DeleteDeployment(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteDeployment")

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
            request: apihub_service.DeleteDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete deployment method over HTTP.

            Args:
                request (~.apihub_service.DeleteDeploymentRequest):
                    The request object. The
                [DeleteDeployment][google.cloud.apihub.v1.ApiHub.DeleteDeployment]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_deployment(
                request, metadata
            )
            pb_request = apihub_service.DeleteDeploymentRequest.pb(request)
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

    class _DeleteExternalApi(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteExternalApi")

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
            request: apihub_service.DeleteExternalApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete external api method over HTTP.

            Args:
                request (~.apihub_service.DeleteExternalApiRequest):
                    The request object. The
                [DeleteExternalApi][google.cloud.apihub.v1.ApiHub.DeleteExternalApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/externalApis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_external_api(
                request, metadata
            )
            pb_request = apihub_service.DeleteExternalApiRequest.pb(request)
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

    class _DeleteSpec(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteSpec")

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
            request: apihub_service.DeleteSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete spec method over HTTP.

            Args:
                request (~.apihub_service.DeleteSpecRequest):
                    The request object. The
                [DeleteSpec][google.cloud.apihub.v1.ApiHub.DeleteSpec]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_spec(request, metadata)
            pb_request = apihub_service.DeleteSpecRequest.pb(request)
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

    class _DeleteVersion(ApiHubRestStub):
        def __hash__(self):
            return hash("DeleteVersion")

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
            request: apihub_service.DeleteVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete version method over HTTP.

            Args:
                request (~.apihub_service.DeleteVersionRequest):
                    The request object. The
                [DeleteVersion][google.cloud.apihub.v1.ApiHub.DeleteVersion]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_version(request, metadata)
            pb_request = apihub_service.DeleteVersionRequest.pb(request)
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

    class _GetApi(ApiHubRestStub):
        def __hash__(self):
            return hash("GetApi")

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
            request: apihub_service.GetApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Api:
            r"""Call the get api method over HTTP.

            Args:
                request (~.apihub_service.GetApiRequest):
                    The request object. The [GetApi][google.cloud.apihub.v1.ApiHub.GetApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Api:
                    An API resource in the API Hub.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api(request, metadata)
            pb_request = apihub_service.GetApiRequest.pb(request)
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
            resp = common_fields.Api()
            pb_resp = common_fields.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api(resp)
            return resp

    class _GetApiOperation(ApiHubRestStub):
        def __hash__(self):
            return hash("GetApiOperation")

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
            request: apihub_service.GetApiOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.ApiOperation:
            r"""Call the get api operation method over HTTP.

            Args:
                request (~.apihub_service.GetApiOperationRequest):
                    The request object. The
                [GetApiOperation][google.cloud.apihub.v1.ApiHub.GetApiOperation]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.ApiOperation:
                    Represents an operation contained in
                an API version in the API Hub. An
                operation is added/updated/deleted in an
                API version when a new spec is added or
                an existing spec is updated/deleted in a
                version. Currently, an operation will be
                created only corresponding to OpenAPI
                spec as parsing is supported for OpenAPI
                spec.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/operations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api_operation(
                request, metadata
            )
            pb_request = apihub_service.GetApiOperationRequest.pb(request)
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
            resp = common_fields.ApiOperation()
            pb_resp = common_fields.ApiOperation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_operation(resp)
            return resp

    class _GetAttribute(ApiHubRestStub):
        def __hash__(self):
            return hash("GetAttribute")

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
            request: apihub_service.GetAttributeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Attribute:
            r"""Call the get attribute method over HTTP.

            Args:
                request (~.apihub_service.GetAttributeRequest):
                    The request object. The
                [GetAttribute][google.cloud.apihub.v1.ApiHub.GetAttribute]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Attribute:
                    An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/attributes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_attribute(request, metadata)
            pb_request = apihub_service.GetAttributeRequest.pb(request)
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
            resp = common_fields.Attribute()
            pb_resp = common_fields.Attribute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attribute(resp)
            return resp

    class _GetDefinition(ApiHubRestStub):
        def __hash__(self):
            return hash("GetDefinition")

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
            request: apihub_service.GetDefinitionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Definition:
            r"""Call the get definition method over HTTP.

            Args:
                request (~.apihub_service.GetDefinitionRequest):
                    The request object. The
                [GetDefinition][google.cloud.apihub.v1.ApiHub.GetDefinition]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Definition:
                    Represents a definition for example schema, request,
                response definitions contained in an API version. A
                definition is added/updated/deleted in an API version
                when a new spec is added or an existing spec is
                updated/deleted in a version. Currently, definition will
                be created only corresponding to OpenAPI spec as parsing
                is supported for OpenAPI spec. Also, within OpenAPI
                spec, only ``schema`` object is supported.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/definitions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_definition(request, metadata)
            pb_request = apihub_service.GetDefinitionRequest.pb(request)
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
            resp = common_fields.Definition()
            pb_resp = common_fields.Definition.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_definition(resp)
            return resp

    class _GetDeployment(ApiHubRestStub):
        def __hash__(self):
            return hash("GetDeployment")

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
            request: apihub_service.GetDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Deployment:
            r"""Call the get deployment method over HTTP.

            Args:
                request (~.apihub_service.GetDeploymentRequest):
                    The request object. The
                [GetDeployment][google.cloud.apihub.v1.ApiHub.GetDeployment]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Deployment:
                    Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_deployment(request, metadata)
            pb_request = apihub_service.GetDeploymentRequest.pb(request)
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
            resp = common_fields.Deployment()
            pb_resp = common_fields.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_deployment(resp)
            return resp

    class _GetExternalApi(ApiHubRestStub):
        def __hash__(self):
            return hash("GetExternalApi")

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
            request: apihub_service.GetExternalApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.ExternalApi:
            r"""Call the get external api method over HTTP.

            Args:
                request (~.apihub_service.GetExternalApiRequest):
                    The request object. The
                [GetExternalApi][google.cloud.apihub.v1.ApiHub.GetExternalApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.ExternalApi:
                    An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/externalApis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_external_api(
                request, metadata
            )
            pb_request = apihub_service.GetExternalApiRequest.pb(request)
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
            resp = common_fields.ExternalApi()
            pb_resp = common_fields.ExternalApi.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_external_api(resp)
            return resp

    class _GetSpec(ApiHubRestStub):
        def __hash__(self):
            return hash("GetSpec")

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
            request: apihub_service.GetSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Spec:
            r"""Call the get spec method over HTTP.

            Args:
                request (~.apihub_service.GetSpecRequest):
                    The request object. The [GetSpec][google.cloud.apihub.v1.ApiHub.GetSpec]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Spec:
                    Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_spec(request, metadata)
            pb_request = apihub_service.GetSpecRequest.pb(request)
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
            resp = common_fields.Spec()
            pb_resp = common_fields.Spec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_spec(resp)
            return resp

    class _GetSpecContents(ApiHubRestStub):
        def __hash__(self):
            return hash("GetSpecContents")

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
            request: apihub_service.GetSpecContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.SpecContents:
            r"""Call the get spec contents method over HTTP.

            Args:
                request (~.apihub_service.GetSpecContentsRequest):
                    The request object. The
                [GetSpecContents][google.cloud.apihub.v1.ApiHub.GetSpecContents]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.SpecContents:
                    The spec contents.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:contents",
                },
            ]
            request, metadata = self._interceptor.pre_get_spec_contents(
                request, metadata
            )
            pb_request = apihub_service.GetSpecContentsRequest.pb(request)
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
            resp = common_fields.SpecContents()
            pb_resp = common_fields.SpecContents.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_spec_contents(resp)
            return resp

    class _GetVersion(ApiHubRestStub):
        def __hash__(self):
            return hash("GetVersion")

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
            request: apihub_service.GetVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Version:
            r"""Call the get version method over HTTP.

            Args:
                request (~.apihub_service.GetVersionRequest):
                    The request object. The
                [GetVersion][google.cloud.apihub.v1.ApiHub.GetVersion]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Version:
                    Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_version(request, metadata)
            pb_request = apihub_service.GetVersionRequest.pb(request)
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
            resp = common_fields.Version()
            pb_resp = common_fields.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_version(resp)
            return resp

    class _ListApiOperations(ApiHubRestStub):
        def __hash__(self):
            return hash("ListApiOperations")

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
            request: apihub_service.ListApiOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListApiOperationsResponse:
            r"""Call the list api operations method over HTTP.

            Args:
                request (~.apihub_service.ListApiOperationsRequest):
                    The request object. The
                [ListApiOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListApiOperationsResponse:
                    The
                [ListApiOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/operations",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_operations(
                request, metadata
            )
            pb_request = apihub_service.ListApiOperationsRequest.pb(request)
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
            resp = apihub_service.ListApiOperationsResponse()
            pb_resp = apihub_service.ListApiOperationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_operations(resp)
            return resp

    class _ListApis(ApiHubRestStub):
        def __hash__(self):
            return hash("ListApis")

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
            request: apihub_service.ListApisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListApisResponse:
            r"""Call the list apis method over HTTP.

            Args:
                request (~.apihub_service.ListApisRequest):
                    The request object. The [ListApis][google.cloud.apihub.v1.ApiHub.ListApis]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListApisResponse:
                    The [ListApis][google.cloud.apihub.v1.ApiHub.ListApis]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/apis",
                },
            ]
            request, metadata = self._interceptor.pre_list_apis(request, metadata)
            pb_request = apihub_service.ListApisRequest.pb(request)
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
            resp = apihub_service.ListApisResponse()
            pb_resp = apihub_service.ListApisResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_apis(resp)
            return resp

    class _ListAttributes(ApiHubRestStub):
        def __hash__(self):
            return hash("ListAttributes")

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
            request: apihub_service.ListAttributesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListAttributesResponse:
            r"""Call the list attributes method over HTTP.

            Args:
                request (~.apihub_service.ListAttributesRequest):
                    The request object. The
                [ListAttributes][google.cloud.apihub.v1.ApiHub.ListAttributes]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListAttributesResponse:
                    The
                [ListAttributes][google.cloud.apihub.v1.ApiHub.ListAttributes]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/attributes",
                },
            ]
            request, metadata = self._interceptor.pre_list_attributes(request, metadata)
            pb_request = apihub_service.ListAttributesRequest.pb(request)
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
            resp = apihub_service.ListAttributesResponse()
            pb_resp = apihub_service.ListAttributesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_attributes(resp)
            return resp

    class _ListDeployments(ApiHubRestStub):
        def __hash__(self):
            return hash("ListDeployments")

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
            request: apihub_service.ListDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListDeploymentsResponse:
            r"""Call the list deployments method over HTTP.

            Args:
                request (~.apihub_service.ListDeploymentsRequest):
                    The request object. The
                [ListDeployments][google.cloud.apihub.v1.ApiHub.ListDeployments]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListDeploymentsResponse:
                    The
                [ListDeployments][google.cloud.apihub.v1.ApiHub.ListDeployments]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/deployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_deployments(
                request, metadata
            )
            pb_request = apihub_service.ListDeploymentsRequest.pb(request)
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
            resp = apihub_service.ListDeploymentsResponse()
            pb_resp = apihub_service.ListDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_deployments(resp)
            return resp

    class _ListExternalApis(ApiHubRestStub):
        def __hash__(self):
            return hash("ListExternalApis")

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
            request: apihub_service.ListExternalApisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListExternalApisResponse:
            r"""Call the list external apis method over HTTP.

            Args:
                request (~.apihub_service.ListExternalApisRequest):
                    The request object. The
                [ListExternalApis][google.cloud.apihub.v1.ApiHub.ListExternalApis]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListExternalApisResponse:
                    The
                [ListExternalApis][google.cloud.apihub.v1.ApiHub.ListExternalApis]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/externalApis",
                },
            ]
            request, metadata = self._interceptor.pre_list_external_apis(
                request, metadata
            )
            pb_request = apihub_service.ListExternalApisRequest.pb(request)
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
            resp = apihub_service.ListExternalApisResponse()
            pb_resp = apihub_service.ListExternalApisResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_external_apis(resp)
            return resp

    class _ListSpecs(ApiHubRestStub):
        def __hash__(self):
            return hash("ListSpecs")

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
            request: apihub_service.ListSpecsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListSpecsResponse:
            r"""Call the list specs method over HTTP.

            Args:
                request (~.apihub_service.ListSpecsRequest):
                    The request object. The [ListSpecs][ListSpecs] method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListSpecsResponse:
                    The [ListSpecs][google.cloud.apihub.v1.ApiHub.ListSpecs]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs",
                },
            ]
            request, metadata = self._interceptor.pre_list_specs(request, metadata)
            pb_request = apihub_service.ListSpecsRequest.pb(request)
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
            resp = apihub_service.ListSpecsResponse()
            pb_resp = apihub_service.ListSpecsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_specs(resp)
            return resp

    class _ListVersions(ApiHubRestStub):
        def __hash__(self):
            return hash("ListVersions")

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
            request: apihub_service.ListVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.ListVersionsResponse:
            r"""Call the list versions method over HTTP.

            Args:
                request (~.apihub_service.ListVersionsRequest):
                    The request object. The
                [ListVersions][google.cloud.apihub.v1.ApiHub.ListVersions]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.ListVersionsResponse:
                    The
                [ListVersions][google.cloud.apihub.v1.ApiHub.ListVersions]
                method's response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/versions",
                },
            ]
            request, metadata = self._interceptor.pre_list_versions(request, metadata)
            pb_request = apihub_service.ListVersionsRequest.pb(request)
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
            resp = apihub_service.ListVersionsResponse()
            pb_resp = apihub_service.ListVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_versions(resp)
            return resp

    class _SearchResources(ApiHubRestStub):
        def __hash__(self):
            return hash("SearchResources")

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
            request: apihub_service.SearchResourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apihub_service.SearchResourcesResponse:
            r"""Call the search resources method over HTTP.

            Args:
                request (~.apihub_service.SearchResourcesRequest):
                    The request object. The
                [SearchResources][google.cloud.apihub.v1.ApiHub.SearchResources]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apihub_service.SearchResourcesResponse:
                    Response for the
                [SearchResources][google.cloud.apihub.v1.ApiHub.SearchResources]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{location=projects/*/locations/*}:searchResources",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_resources(
                request, metadata
            )
            pb_request = apihub_service.SearchResourcesRequest.pb(request)
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
            resp = apihub_service.SearchResourcesResponse()
            pb_resp = apihub_service.SearchResourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_resources(resp)
            return resp

    class _UpdateApi(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateApi")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Api:
            r"""Call the update api method over HTTP.

            Args:
                request (~.apihub_service.UpdateApiRequest):
                    The request object. The [UpdateApi][google.cloud.apihub.v1.ApiHub.UpdateApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Api:
                    An API resource in the API Hub.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{api.name=projects/*/locations/*/apis/*}",
                    "body": "api",
                },
            ]
            request, metadata = self._interceptor.pre_update_api(request, metadata)
            pb_request = apihub_service.UpdateApiRequest.pb(request)
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
            resp = common_fields.Api()
            pb_resp = common_fields.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_api(resp)
            return resp

    class _UpdateAttribute(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateAttribute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateAttributeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Attribute:
            r"""Call the update attribute method over HTTP.

            Args:
                request (~.apihub_service.UpdateAttributeRequest):
                    The request object. The
                [UpdateAttribute][google.cloud.apihub.v1.ApiHub.UpdateAttribute]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Attribute:
                    An attribute in the API Hub.
                An attribute is a name value pair which
                can be attached to different resources
                in the API hub based on the scope of the
                attribute. Attributes can either be
                pre-defined by the API Hub or created by
                users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{attribute.name=projects/*/locations/*/attributes/*}",
                    "body": "attribute",
                },
            ]
            request, metadata = self._interceptor.pre_update_attribute(
                request, metadata
            )
            pb_request = apihub_service.UpdateAttributeRequest.pb(request)
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
            resp = common_fields.Attribute()
            pb_resp = common_fields.Attribute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_attribute(resp)
            return resp

    class _UpdateDeployment(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Deployment:
            r"""Call the update deployment method over HTTP.

            Args:
                request (~.apihub_service.UpdateDeploymentRequest):
                    The request object. The
                [UpdateDeployment][google.cloud.apihub.v1.ApiHub.UpdateDeployment]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Deployment:
                    Details of the deployment where APIs
                are hosted. A deployment could represent
                an Apigee proxy, API gateway, other
                Google Cloud services or non-Google
                Cloud services as well. A deployment
                entity is a root level entity in the API
                hub and exists independent of any API.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{deployment.name=projects/*/locations/*/deployments/*}",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_update_deployment(
                request, metadata
            )
            pb_request = apihub_service.UpdateDeploymentRequest.pb(request)
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
            resp = common_fields.Deployment()
            pb_resp = common_fields.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_deployment(resp)
            return resp

    class _UpdateExternalApi(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateExternalApi")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateExternalApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.ExternalApi:
            r"""Call the update external api method over HTTP.

            Args:
                request (~.apihub_service.UpdateExternalApiRequest):
                    The request object. The
                [UpdateExternalApi][google.cloud.apihub.v1.ApiHub.UpdateExternalApi]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.ExternalApi:
                    An external API represents an API
                being provided by external sources. This
                can be used to model third-party APIs
                and can be used to define dependencies.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{external_api.name=projects/*/locations/*/externalApis/*}",
                    "body": "external_api",
                },
            ]
            request, metadata = self._interceptor.pre_update_external_api(
                request, metadata
            )
            pb_request = apihub_service.UpdateExternalApiRequest.pb(request)
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
            resp = common_fields.ExternalApi()
            pb_resp = common_fields.ExternalApi.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_external_api(resp)
            return resp

    class _UpdateSpec(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateSpec")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Spec:
            r"""Call the update spec method over HTTP.

            Args:
                request (~.apihub_service.UpdateSpecRequest):
                    The request object. The
                [UpdateSpec][google.cloud.apihub.v1.ApiHub.UpdateSpec]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Spec:
                    Represents a spec associated with an
                API version in the API Hub. Note that
                specs of various types can be uploaded,
                however parsing of details is supported
                for OpenAPI spec currently.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{spec.name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                    "body": "spec",
                },
            ]
            request, metadata = self._interceptor.pre_update_spec(request, metadata)
            pb_request = apihub_service.UpdateSpecRequest.pb(request)
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
            resp = common_fields.Spec()
            pb_resp = common_fields.Spec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_spec(resp)
            return resp

    class _UpdateVersion(ApiHubRestStub):
        def __hash__(self):
            return hash("UpdateVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: apihub_service.UpdateVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common_fields.Version:
            r"""Call the update version method over HTTP.

            Args:
                request (~.apihub_service.UpdateVersionRequest):
                    The request object. The
                [UpdateVersion][google.cloud.apihub.v1.ApiHub.UpdateVersion]
                method's request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common_fields.Version:
                    Represents a version of the API
                resource in API hub. This is also
                referred to as the API version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{version.name=projects/*/locations/*/apis/*/versions/*}",
                    "body": "version",
                },
            ]
            request, metadata = self._interceptor.pre_update_version(request, metadata)
            pb_request = apihub_service.UpdateVersionRequest.pb(request)
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
            resp = common_fields.Version()
            pb_resp = common_fields.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_version(resp)
            return resp

    @property
    def create_api(
        self,
    ) -> Callable[[apihub_service.CreateApiRequest], common_fields.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_attribute(
        self,
    ) -> Callable[[apihub_service.CreateAttributeRequest], common_fields.Attribute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAttribute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_deployment(
        self,
    ) -> Callable[[apihub_service.CreateDeploymentRequest], common_fields.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_external_api(
        self,
    ) -> Callable[[apihub_service.CreateExternalApiRequest], common_fields.ExternalApi]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExternalApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_spec(
        self,
    ) -> Callable[[apihub_service.CreateSpecRequest], common_fields.Spec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_version(
        self,
    ) -> Callable[[apihub_service.CreateVersionRequest], common_fields.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api(
        self,
    ) -> Callable[[apihub_service.DeleteApiRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_attribute(
        self,
    ) -> Callable[[apihub_service.DeleteAttributeRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAttribute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_deployment(
        self,
    ) -> Callable[[apihub_service.DeleteDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_external_api(
        self,
    ) -> Callable[[apihub_service.DeleteExternalApiRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExternalApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_spec(
        self,
    ) -> Callable[[apihub_service.DeleteSpecRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_version(
        self,
    ) -> Callable[[apihub_service.DeleteVersionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api(self) -> Callable[[apihub_service.GetApiRequest], common_fields.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_operation(
        self,
    ) -> Callable[[apihub_service.GetApiOperationRequest], common_fields.ApiOperation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiOperation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attribute(
        self,
    ) -> Callable[[apihub_service.GetAttributeRequest], common_fields.Attribute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttribute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_definition(
        self,
    ) -> Callable[[apihub_service.GetDefinitionRequest], common_fields.Definition]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDefinition(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_deployment(
        self,
    ) -> Callable[[apihub_service.GetDeploymentRequest], common_fields.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_external_api(
        self,
    ) -> Callable[[apihub_service.GetExternalApiRequest], common_fields.ExternalApi]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExternalApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_spec(self) -> Callable[[apihub_service.GetSpecRequest], common_fields.Spec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_spec_contents(
        self,
    ) -> Callable[[apihub_service.GetSpecContentsRequest], common_fields.SpecContents]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpecContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_version(
        self,
    ) -> Callable[[apihub_service.GetVersionRequest], common_fields.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_operations(
        self,
    ) -> Callable[
        [apihub_service.ListApiOperationsRequest],
        apihub_service.ListApiOperationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiOperations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_apis(
        self,
    ) -> Callable[[apihub_service.ListApisRequest], apihub_service.ListApisResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_attributes(
        self,
    ) -> Callable[
        [apihub_service.ListAttributesRequest], apihub_service.ListAttributesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAttributes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_deployments(
        self,
    ) -> Callable[
        [apihub_service.ListDeploymentsRequest], apihub_service.ListDeploymentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_external_apis(
        self,
    ) -> Callable[
        [apihub_service.ListExternalApisRequest],
        apihub_service.ListExternalApisResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExternalApis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_specs(
        self,
    ) -> Callable[[apihub_service.ListSpecsRequest], apihub_service.ListSpecsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSpecs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_versions(
        self,
    ) -> Callable[
        [apihub_service.ListVersionsRequest], apihub_service.ListVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_resources(
        self,
    ) -> Callable[
        [apihub_service.SearchResourcesRequest], apihub_service.SearchResourcesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchResources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api(
        self,
    ) -> Callable[[apihub_service.UpdateApiRequest], common_fields.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_attribute(
        self,
    ) -> Callable[[apihub_service.UpdateAttributeRequest], common_fields.Attribute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAttribute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_deployment(
        self,
    ) -> Callable[[apihub_service.UpdateDeploymentRequest], common_fields.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_external_api(
        self,
    ) -> Callable[[apihub_service.UpdateExternalApiRequest], common_fields.ExternalApi]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExternalApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_spec(
        self,
    ) -> Callable[[apihub_service.UpdateSpecRequest], common_fields.Spec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_version(
        self,
    ) -> Callable[[apihub_service.UpdateVersionRequest], common_fields.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ApiHubRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}",
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

    class _ListLocations(ApiHubRestStub):
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
                    "uri": "/v1/{name=projects/*}/locations",
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

    class _CancelOperation(ApiHubRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
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
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(ApiHubRestStub):
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

    class _GetOperation(ApiHubRestStub):
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

    class _ListOperations(ApiHubRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
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


__all__ = ("ApiHubRestTransport",)
