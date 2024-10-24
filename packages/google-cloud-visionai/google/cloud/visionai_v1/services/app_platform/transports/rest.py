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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.visionai_v1.types import platform

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAppPlatformRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class AppPlatformRestInterceptor:
    """Interceptor for AppPlatform.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AppPlatformRestTransport.

    .. code-block:: python
        class MyCustomAppPlatformInterceptor(AppPlatformRestInterceptor):
            def pre_add_application_stream_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_application_stream_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_application_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_application_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_draft(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_draft(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_application_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_application_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_draft(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_draft(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_deploy_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_draft(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_draft(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_applications(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_applications(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_drafts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_drafts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_prebuilt_processors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_prebuilt_processors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_application_stream_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_application_stream_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undeploy_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undeploy_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_application_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_application_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_application_stream_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_application_stream_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_draft(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_draft(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AppPlatformRestTransport(interceptor=MyCustomAppPlatformInterceptor())
        client = AppPlatformClient(transport=transport)


    """

    def pre_add_application_stream_input(
        self,
        request: platform.AddApplicationStreamInputRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.AddApplicationStreamInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_application_stream_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_add_application_stream_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_application_stream_input

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_create_application(
        self,
        request: platform.CreateApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.CreateApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_create_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_create_application_instances(
        self,
        request: platform.CreateApplicationInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.CreateApplicationInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_application_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_create_application_instances(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_application_instances

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_create_draft(
        self, request: platform.CreateDraftRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.CreateDraftRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_draft

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_create_draft(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_draft

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_create_processor(
        self,
        request: platform.CreateProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.CreateProcessorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_create_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_processor

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_delete_application(
        self,
        request: platform.DeleteApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.DeleteApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_delete_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_delete_application_instances(
        self,
        request: platform.DeleteApplicationInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.DeleteApplicationInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_application_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_delete_application_instances(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_application_instances

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_delete_draft(
        self, request: platform.DeleteDraftRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.DeleteDraftRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_draft

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_delete_draft(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_draft

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_delete_processor(
        self,
        request: platform.DeleteProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.DeleteProcessorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_delete_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_processor

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_deploy_application(
        self,
        request: platform.DeployApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.DeployApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for deploy_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_deploy_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_get_application(
        self,
        request: platform.GetApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.GetApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_get_application(
        self, response: platform.Application
    ) -> platform.Application:
        """Post-rpc interceptor for get_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_get_draft(
        self, request: platform.GetDraftRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.GetDraftRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_draft

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_get_draft(self, response: platform.Draft) -> platform.Draft:
        """Post-rpc interceptor for get_draft

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self, request: platform.GetInstanceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_get_instance(self, response: platform.Instance) -> platform.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_get_processor(
        self, request: platform.GetProcessorRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.GetProcessorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_get_processor(self, response: platform.Processor) -> platform.Processor:
        """Post-rpc interceptor for get_processor

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_list_applications(
        self,
        request: platform.ListApplicationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.ListApplicationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_applications

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_applications(
        self, response: platform.ListApplicationsResponse
    ) -> platform.ListApplicationsResponse:
        """Post-rpc interceptor for list_applications

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_list_drafts(
        self, request: platform.ListDraftsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.ListDraftsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_drafts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_drafts(
        self, response: platform.ListDraftsResponse
    ) -> platform.ListDraftsResponse:
        """Post-rpc interceptor for list_drafts

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: platform.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_instances(
        self, response: platform.ListInstancesResponse
    ) -> platform.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_list_prebuilt_processors(
        self,
        request: platform.ListPrebuiltProcessorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.ListPrebuiltProcessorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_prebuilt_processors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_prebuilt_processors(
        self, response: platform.ListPrebuiltProcessorsResponse
    ) -> platform.ListPrebuiltProcessorsResponse:
        """Post-rpc interceptor for list_prebuilt_processors

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_list_processors(
        self,
        request: platform.ListProcessorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.ListProcessorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_processors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_processors(
        self, response: platform.ListProcessorsResponse
    ) -> platform.ListProcessorsResponse:
        """Post-rpc interceptor for list_processors

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_remove_application_stream_input(
        self,
        request: platform.RemoveApplicationStreamInputRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.RemoveApplicationStreamInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_application_stream_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_remove_application_stream_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_application_stream_input

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_undeploy_application(
        self,
        request: platform.UndeployApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.UndeployApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undeploy_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_undeploy_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undeploy_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_update_application(
        self,
        request: platform.UpdateApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.UpdateApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_update_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_application

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_update_application_instances(
        self,
        request: platform.UpdateApplicationInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.UpdateApplicationInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_application_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_update_application_instances(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_application_instances

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_update_application_stream_input(
        self,
        request: platform.UpdateApplicationStreamInputRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.UpdateApplicationStreamInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_application_stream_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_update_application_stream_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_application_stream_input

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_update_draft(
        self, request: platform.UpdateDraftRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[platform.UpdateDraftRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_draft

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_update_draft(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_draft

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response

    def pre_update_processor(
        self,
        request: platform.UpdateProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[platform.UpdateProcessorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_update_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_processor

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
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
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
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
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
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
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
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
        before they are sent to the AppPlatform server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AppPlatform server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AppPlatformRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AppPlatformRestInterceptor


class AppPlatformRestTransport(_BaseAppPlatformRestTransport):
    """REST backend synchronous transport for AppPlatform.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "visionai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AppPlatformRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'visionai.googleapis.com').
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
        self._interceptor = interceptor or AppPlatformRestInterceptor()
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
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/warehouseOperations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/imageIndexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/indexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
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

    class _AddApplicationStreamInput(
        _BaseAppPlatformRestTransport._BaseAddApplicationStreamInput,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.AddApplicationStreamInput")

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
            request: platform.AddApplicationStreamInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add application stream
            input method over HTTP.

                Args:
                    request (~.platform.AddApplicationStreamInputRequest):
                        The request object. Message for adding stream input to an
                    Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseAddApplicationStreamInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_application_stream_input(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseAddApplicationStreamInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseAddApplicationStreamInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseAddApplicationStreamInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._AddApplicationStreamInput._get_response(
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
            resp = self._interceptor.post_add_application_stream_input(resp)
            return resp

    class _CreateApplication(
        _BaseAppPlatformRestTransport._BaseCreateApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.CreateApplication")

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
            request: platform.CreateApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create application method over HTTP.

            Args:
                request (~.platform.CreateApplicationRequest):
                    The request object. Message for creating a Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseCreateApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_application(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseCreateApplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseCreateApplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseCreateApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._CreateApplication._get_response(
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
            resp = self._interceptor.post_create_application(resp)
            return resp

    class _CreateApplicationInstances(
        _BaseAppPlatformRestTransport._BaseCreateApplicationInstances,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.CreateApplicationInstances")

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
            request: platform.CreateApplicationInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create application
            instances method over HTTP.

                Args:
                    request (~.platform.CreateApplicationInstancesRequest):
                        The request object. Message for adding stream input to an
                    Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseCreateApplicationInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_application_instances(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseCreateApplicationInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseCreateApplicationInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseCreateApplicationInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._CreateApplicationInstances._get_response(
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
            resp = self._interceptor.post_create_application_instances(resp)
            return resp

    class _CreateDraft(
        _BaseAppPlatformRestTransport._BaseCreateDraft, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.CreateDraft")

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
            request: platform.CreateDraftRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create draft method over HTTP.

            Args:
                request (~.platform.CreateDraftRequest):
                    The request object. Message for creating a Draft.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseCreateDraft._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_draft(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseCreateDraft._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseAppPlatformRestTransport._BaseCreateDraft._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseCreateDraft._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._CreateDraft._get_response(
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
            resp = self._interceptor.post_create_draft(resp)
            return resp

    class _CreateProcessor(
        _BaseAppPlatformRestTransport._BaseCreateProcessor, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.CreateProcessor")

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
            request: platform.CreateProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create processor method over HTTP.

            Args:
                request (~.platform.CreateProcessorRequest):
                    The request object. Message for creating a Processor.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseCreateProcessor._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_processor(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseCreateProcessor._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseCreateProcessor._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseCreateProcessor._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._CreateProcessor._get_response(
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
            resp = self._interceptor.post_create_processor(resp)
            return resp

    class _DeleteApplication(
        _BaseAppPlatformRestTransport._BaseDeleteApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeleteApplication")

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
            request: platform.DeleteApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete application method over HTTP.

            Args:
                request (~.platform.DeleteApplicationRequest):
                    The request object. Message for deleting an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeleteApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_application(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseDeleteApplication._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseDeleteApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._DeleteApplication._get_response(
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
            resp = self._interceptor.post_delete_application(resp)
            return resp

    class _DeleteApplicationInstances(
        _BaseAppPlatformRestTransport._BaseDeleteApplicationInstances,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeleteApplicationInstances")

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
            request: platform.DeleteApplicationInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete application
            instances method over HTTP.

                Args:
                    request (~.platform.DeleteApplicationInstancesRequest):
                        The request object. Message for removing stream input
                    from an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeleteApplicationInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_application_instances(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseDeleteApplicationInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseDeleteApplicationInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseDeleteApplicationInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._DeleteApplicationInstances._get_response(
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
            resp = self._interceptor.post_delete_application_instances(resp)
            return resp

    class _DeleteDraft(
        _BaseAppPlatformRestTransport._BaseDeleteDraft, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeleteDraft")

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
            request: platform.DeleteDraftRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete draft method over HTTP.

            Args:
                request (~.platform.DeleteDraftRequest):
                    The request object. Message for deleting a Draft.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeleteDraft._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_draft(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseDeleteDraft._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseDeleteDraft._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._DeleteDraft._get_response(
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
            resp = self._interceptor.post_delete_draft(resp)
            return resp

    class _DeleteProcessor(
        _BaseAppPlatformRestTransport._BaseDeleteProcessor, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeleteProcessor")

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
            request: platform.DeleteProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete processor method over HTTP.

            Args:
                request (~.platform.DeleteProcessorRequest):
                    The request object. Message for deleting a Processor.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeleteProcessor._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_processor(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseDeleteProcessor._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseDeleteProcessor._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._DeleteProcessor._get_response(
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
            resp = self._interceptor.post_delete_processor(resp)
            return resp

    class _DeployApplication(
        _BaseAppPlatformRestTransport._BaseDeployApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeployApplication")

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
            request: platform.DeployApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy application method over HTTP.

            Args:
                request (~.platform.DeployApplicationRequest):
                    The request object. Message for deploying an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeployApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_deploy_application(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseDeployApplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseDeployApplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseDeployApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._DeployApplication._get_response(
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
            resp = self._interceptor.post_deploy_application(resp)
            return resp

    class _GetApplication(
        _BaseAppPlatformRestTransport._BaseGetApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.GetApplication")

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
            request: platform.GetApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.Application:
            r"""Call the get application method over HTTP.

            Args:
                request (~.platform.GetApplicationRequest):
                    The request object. Message for getting a Application.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.Application:
                    Message describing Application object
            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseGetApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_application(request, metadata)
            transcoded_request = _BaseAppPlatformRestTransport._BaseGetApplication._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseGetApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._GetApplication._get_response(
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
            resp = platform.Application()
            pb_resp = platform.Application.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_application(resp)
            return resp

    class _GetDraft(_BaseAppPlatformRestTransport._BaseGetDraft, AppPlatformRestStub):
        def __hash__(self):
            return hash("AppPlatformRestTransport.GetDraft")

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
            request: platform.GetDraftRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.Draft:
            r"""Call the get draft method over HTTP.

            Args:
                request (~.platform.GetDraftRequest):
                    The request object. Message for getting a Draft.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.Draft:
                    Message describing Draft object
            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseGetDraft._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_draft(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseGetDraft._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseGetDraft._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._GetDraft._get_response(
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
            resp = platform.Draft()
            pb_resp = platform.Draft.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_draft(resp)
            return resp

    class _GetInstance(
        _BaseAppPlatformRestTransport._BaseGetInstance, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.GetInstance")

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
            request: platform.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.platform.GetInstanceRequest):
                    The request object. Message for getting a Instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.Instance:
                    Message describing Instance object
                Next ID: 12

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseGetInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseGetInstance._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseGetInstance._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._GetInstance._get_response(
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
            resp = platform.Instance()
            pb_resp = platform.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _GetProcessor(
        _BaseAppPlatformRestTransport._BaseGetProcessor, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.GetProcessor")

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
            request: platform.GetProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.Processor:
            r"""Call the get processor method over HTTP.

            Args:
                request (~.platform.GetProcessorRequest):
                    The request object. Message for getting a Processor.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.Processor:
                    Message describing Processor object.
                Next ID: 19

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseGetProcessor._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_processor(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseGetProcessor._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseGetProcessor._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._GetProcessor._get_response(
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
            resp = platform.Processor()
            pb_resp = platform.Processor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_processor(resp)
            return resp

    class _ListApplications(
        _BaseAppPlatformRestTransport._BaseListApplications, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListApplications")

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
            request: platform.ListApplicationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.ListApplicationsResponse:
            r"""Call the list applications method over HTTP.

            Args:
                request (~.platform.ListApplicationsRequest):
                    The request object. Message for requesting list of
                Applications.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.ListApplicationsResponse:
                    Message for response to listing
                Applications.

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseListApplications._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_applications(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseListApplications._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseListApplications._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._ListApplications._get_response(
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
            resp = platform.ListApplicationsResponse()
            pb_resp = platform.ListApplicationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_applications(resp)
            return resp

    class _ListDrafts(
        _BaseAppPlatformRestTransport._BaseListDrafts, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListDrafts")

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
            request: platform.ListDraftsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.ListDraftsResponse:
            r"""Call the list drafts method over HTTP.

            Args:
                request (~.platform.ListDraftsRequest):
                    The request object. Message for requesting list of
                Drafts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.ListDraftsResponse:
                    Message for response to listing
                Drafts.

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseListDrafts._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_drafts(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseListDrafts._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseListDrafts._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._ListDrafts._get_response(
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
            resp = platform.ListDraftsResponse()
            pb_resp = platform.ListDraftsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_drafts(resp)
            return resp

    class _ListInstances(
        _BaseAppPlatformRestTransport._BaseListInstances, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListInstances")

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
            request: platform.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.platform.ListInstancesRequest):
                    The request object. Message for requesting list of
                Instances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.ListInstancesResponse:
                    Message for response to listing
                Instances.

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseListInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            transcoded_request = _BaseAppPlatformRestTransport._BaseListInstances._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseListInstances._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._ListInstances._get_response(
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
            resp = platform.ListInstancesResponse()
            pb_resp = platform.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _ListPrebuiltProcessors(
        _BaseAppPlatformRestTransport._BaseListPrebuiltProcessors, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListPrebuiltProcessors")

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
            request: platform.ListPrebuiltProcessorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.ListPrebuiltProcessorsResponse:
            r"""Call the list prebuilt processors method over HTTP.

            Args:
                request (~.platform.ListPrebuiltProcessorsRequest):
                    The request object. Request Message for listing Prebuilt
                Processors.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.ListPrebuiltProcessorsResponse:
                    Response Message for listing Prebuilt
                Processors.

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseListPrebuiltProcessors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_prebuilt_processors(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseListPrebuiltProcessors._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseListPrebuiltProcessors._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseListPrebuiltProcessors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._ListPrebuiltProcessors._get_response(
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
            resp = platform.ListPrebuiltProcessorsResponse()
            pb_resp = platform.ListPrebuiltProcessorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_prebuilt_processors(resp)
            return resp

    class _ListProcessors(
        _BaseAppPlatformRestTransport._BaseListProcessors, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListProcessors")

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
            request: platform.ListProcessorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> platform.ListProcessorsResponse:
            r"""Call the list processors method over HTTP.

            Args:
                request (~.platform.ListProcessorsRequest):
                    The request object. Message for requesting list of
                Processors.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.platform.ListProcessorsResponse:
                    Message for response to listing
                Processors.

            """

            http_options = (
                _BaseAppPlatformRestTransport._BaseListProcessors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_processors(request, metadata)
            transcoded_request = _BaseAppPlatformRestTransport._BaseListProcessors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseListProcessors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._ListProcessors._get_response(
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
            resp = platform.ListProcessorsResponse()
            pb_resp = platform.ListProcessorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processors(resp)
            return resp

    class _RemoveApplicationStreamInput(
        _BaseAppPlatformRestTransport._BaseRemoveApplicationStreamInput,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.RemoveApplicationStreamInput")

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
            request: platform.RemoveApplicationStreamInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove application stream
            input method over HTTP.

                Args:
                    request (~.platform.RemoveApplicationStreamInputRequest):
                        The request object. Message for removing stream input
                    from an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseRemoveApplicationStreamInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_application_stream_input(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseRemoveApplicationStreamInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseRemoveApplicationStreamInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseRemoveApplicationStreamInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._RemoveApplicationStreamInput._get_response(
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
            resp = self._interceptor.post_remove_application_stream_input(resp)
            return resp

    class _UndeployApplication(
        _BaseAppPlatformRestTransport._BaseUndeployApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UndeployApplication")

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
            request: platform.UndeployApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undeploy application method over HTTP.

            Args:
                request (~.platform.UndeployApplicationRequest):
                    The request object. Message for undeploying an
                Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUndeployApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_undeploy_application(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseUndeployApplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseUndeployApplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseUndeployApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._UndeployApplication._get_response(
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
            resp = self._interceptor.post_undeploy_application(resp)
            return resp

    class _UpdateApplication(
        _BaseAppPlatformRestTransport._BaseUpdateApplication, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UpdateApplication")

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
            request: platform.UpdateApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update application method over HTTP.

            Args:
                request (~.platform.UpdateApplicationRequest):
                    The request object. Message for updating an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUpdateApplication._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_application(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseUpdateApplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseUpdateApplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseUpdateApplication._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._UpdateApplication._get_response(
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
            resp = self._interceptor.post_update_application(resp)
            return resp

    class _UpdateApplicationInstances(
        _BaseAppPlatformRestTransport._BaseUpdateApplicationInstances,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UpdateApplicationInstances")

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
            request: platform.UpdateApplicationInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update application
            instances method over HTTP.

                Args:
                    request (~.platform.UpdateApplicationInstancesRequest):
                        The request object. Message for updating an
                    ApplicationInstance.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUpdateApplicationInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_application_instances(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseUpdateApplicationInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseUpdateApplicationInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseUpdateApplicationInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._UpdateApplicationInstances._get_response(
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
            resp = self._interceptor.post_update_application_instances(resp)
            return resp

    class _UpdateApplicationStreamInput(
        _BaseAppPlatformRestTransport._BaseUpdateApplicationStreamInput,
        AppPlatformRestStub,
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UpdateApplicationStreamInput")

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
            request: platform.UpdateApplicationStreamInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update application stream
            input method over HTTP.

                Args:
                    request (~.platform.UpdateApplicationStreamInputRequest):
                        The request object. Message for updating stream input to
                    an Application.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUpdateApplicationStreamInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_application_stream_input(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseUpdateApplicationStreamInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseUpdateApplicationStreamInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseUpdateApplicationStreamInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AppPlatformRestTransport._UpdateApplicationStreamInput._get_response(
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
            resp = self._interceptor.post_update_application_stream_input(resp)
            return resp

    class _UpdateDraft(
        _BaseAppPlatformRestTransport._BaseUpdateDraft, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UpdateDraft")

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
            request: platform.UpdateDraftRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update draft method over HTTP.

            Args:
                request (~.platform.UpdateDraftRequest):
                    The request object. Message for updating a Draft.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUpdateDraft._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_draft(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseUpdateDraft._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseAppPlatformRestTransport._BaseUpdateDraft._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseUpdateDraft._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._UpdateDraft._get_response(
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
            resp = self._interceptor.post_update_draft(resp)
            return resp

    class _UpdateProcessor(
        _BaseAppPlatformRestTransport._BaseUpdateProcessor, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.UpdateProcessor")

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
            request: platform.UpdateProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update processor method over HTTP.

            Args:
                request (~.platform.UpdateProcessorRequest):
                    The request object. Message for updating a Processor.
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

            http_options = (
                _BaseAppPlatformRestTransport._BaseUpdateProcessor._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_processor(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseUpdateProcessor._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseUpdateProcessor._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseUpdateProcessor._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._UpdateProcessor._get_response(
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
            resp = self._interceptor.post_update_processor(resp)
            return resp

    @property
    def add_application_stream_input(
        self,
    ) -> Callable[
        [platform.AddApplicationStreamInputRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddApplicationStreamInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_application(
        self,
    ) -> Callable[[platform.CreateApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_application_instances(
        self,
    ) -> Callable[
        [platform.CreateApplicationInstancesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApplicationInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_draft(
        self,
    ) -> Callable[[platform.CreateDraftRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDraft(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_processor(
        self,
    ) -> Callable[[platform.CreateProcessorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_application(
        self,
    ) -> Callable[[platform.DeleteApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_application_instances(
        self,
    ) -> Callable[
        [platform.DeleteApplicationInstancesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApplicationInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_draft(
        self,
    ) -> Callable[[platform.DeleteDraftRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDraft(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_processor(
        self,
    ) -> Callable[[platform.DeleteProcessorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_application(
        self,
    ) -> Callable[[platform.DeployApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_application(
        self,
    ) -> Callable[[platform.GetApplicationRequest], platform.Application]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_draft(self) -> Callable[[platform.GetDraftRequest], platform.Draft]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDraft(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[[platform.GetInstanceRequest], platform.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_processor(
        self,
    ) -> Callable[[platform.GetProcessorRequest], platform.Processor]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_applications(
        self,
    ) -> Callable[
        [platform.ListApplicationsRequest], platform.ListApplicationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApplications(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_drafts(
        self,
    ) -> Callable[[platform.ListDraftsRequest], platform.ListDraftsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDrafts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[[platform.ListInstancesRequest], platform.ListInstancesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_prebuilt_processors(
        self,
    ) -> Callable[
        [platform.ListPrebuiltProcessorsRequest],
        platform.ListPrebuiltProcessorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPrebuiltProcessors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processors(
        self,
    ) -> Callable[[platform.ListProcessorsRequest], platform.ListProcessorsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcessors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_application_stream_input(
        self,
    ) -> Callable[
        [platform.RemoveApplicationStreamInputRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveApplicationStreamInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undeploy_application(
        self,
    ) -> Callable[[platform.UndeployApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeployApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_application(
        self,
    ) -> Callable[[platform.UpdateApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_application_instances(
        self,
    ) -> Callable[
        [platform.UpdateApplicationInstancesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApplicationInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_application_stream_input(
        self,
    ) -> Callable[
        [platform.UpdateApplicationStreamInputRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApplicationStreamInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_draft(
        self,
    ) -> Callable[[platform.UpdateDraftRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDraft(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_processor(
        self,
    ) -> Callable[[platform.UpdateProcessorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseAppPlatformRestTransport._BaseCancelOperation, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.CancelOperation")

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

            http_options = (
                _BaseAppPlatformRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseAppPlatformRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseAppPlatformRestTransport._BaseDeleteOperation, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.DeleteOperation")

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

            http_options = (
                _BaseAppPlatformRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseAppPlatformRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseAppPlatformRestTransport._BaseGetOperation, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.GetOperation")

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

            http_options = (
                _BaseAppPlatformRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseAppPlatformRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseAppPlatformRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AppPlatformRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseAppPlatformRestTransport._BaseListOperations, AppPlatformRestStub
    ):
        def __hash__(self):
            return hash("AppPlatformRestTransport.ListOperations")

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

            http_options = (
                _BaseAppPlatformRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseAppPlatformRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAppPlatformRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AppPlatformRestTransport._ListOperations._get_response(
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
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AppPlatformRestTransport",)
