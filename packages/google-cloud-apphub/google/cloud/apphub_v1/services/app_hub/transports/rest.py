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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.apphub_v1.types import (
    apphub_service,
    application,
    service,
    service_project_attachment,
    workload,
)

from .base import AppHubTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AppHubRestInterceptor:
    """Interceptor for AppHub.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AppHubRestTransport.

    .. code-block:: python
        class MyCustomAppHubInterceptor(AppHubRestInterceptor):
            def pre_create_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_detach_service_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detach_service_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_discovered_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_discovered_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_discovered_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_discovered_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_applications(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_applications(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_discovered_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_discovered_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_discovered_workloads(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_discovered_workloads(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_service_project_attachments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_service_project_attachments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workloads(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workloads(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_discovered_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_discovered_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_discovered_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_discovered_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_service_project_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_service_project_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_application(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_application(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workload(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AppHubRestTransport(interceptor=MyCustomAppHubInterceptor())
        client = AppHubClient(transport=transport)


    """

    def pre_create_application(
        self,
        request: apphub_service.CreateApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.CreateApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_create_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_application

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_service(
        self,
        request: apphub_service.CreateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.CreateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_create_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_service_project_attachment(
        self,
        request: apphub_service.CreateServiceProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.CreateServiceProjectAttachmentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_service_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_create_service_project_attachment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_create_workload(
        self,
        request: apphub_service.CreateWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.CreateWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_create_workload(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_delete_application(
        self,
        request: apphub_service.DeleteApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.DeleteApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_delete_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_application

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service(
        self,
        request: apphub_service.DeleteServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.DeleteServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_delete_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service_project_attachment(
        self,
        request: apphub_service.DeleteServiceProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.DeleteServiceProjectAttachmentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_service_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_delete_service_project_attachment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_delete_workload(
        self,
        request: apphub_service.DeleteWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.DeleteWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_delete_workload(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_detach_service_project_attachment(
        self,
        request: apphub_service.DetachServiceProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.DetachServiceProjectAttachmentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for detach_service_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_detach_service_project_attachment(
        self, response: apphub_service.DetachServiceProjectAttachmentResponse
    ) -> apphub_service.DetachServiceProjectAttachmentResponse:
        """Post-rpc interceptor for detach_service_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_application(
        self,
        request: apphub_service.GetApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.GetApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_application(
        self, response: application.Application
    ) -> application.Application:
        """Post-rpc interceptor for get_application

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_discovered_service(
        self,
        request: apphub_service.GetDiscoveredServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.GetDiscoveredServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_discovered_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_discovered_service(
        self, response: service.DiscoveredService
    ) -> service.DiscoveredService:
        """Post-rpc interceptor for get_discovered_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_discovered_workload(
        self,
        request: apphub_service.GetDiscoveredWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.GetDiscoveredWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_discovered_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_discovered_workload(
        self, response: workload.DiscoveredWorkload
    ) -> workload.DiscoveredWorkload:
        """Post-rpc interceptor for get_discovered_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_service(
        self,
        request: apphub_service.GetServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.GetServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_service(self, response: service.Service) -> service.Service:
        """Post-rpc interceptor for get_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_service_project_attachment(
        self,
        request: apphub_service.GetServiceProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.GetServiceProjectAttachmentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_service_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_service_project_attachment(
        self, response: service_project_attachment.ServiceProjectAttachment
    ) -> service_project_attachment.ServiceProjectAttachment:
        """Post-rpc interceptor for get_service_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_get_workload(
        self,
        request: apphub_service.GetWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.GetWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_workload(self, response: workload.Workload) -> workload.Workload:
        """Post-rpc interceptor for get_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_applications(
        self,
        request: apphub_service.ListApplicationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.ListApplicationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_applications

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_applications(
        self, response: apphub_service.ListApplicationsResponse
    ) -> apphub_service.ListApplicationsResponse:
        """Post-rpc interceptor for list_applications

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_discovered_services(
        self,
        request: apphub_service.ListDiscoveredServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.ListDiscoveredServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_discovered_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_discovered_services(
        self, response: apphub_service.ListDiscoveredServicesResponse
    ) -> apphub_service.ListDiscoveredServicesResponse:
        """Post-rpc interceptor for list_discovered_services

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_discovered_workloads(
        self,
        request: apphub_service.ListDiscoveredWorkloadsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.ListDiscoveredWorkloadsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_discovered_workloads

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_discovered_workloads(
        self, response: apphub_service.ListDiscoveredWorkloadsResponse
    ) -> apphub_service.ListDiscoveredWorkloadsResponse:
        """Post-rpc interceptor for list_discovered_workloads

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_service_project_attachments(
        self,
        request: apphub_service.ListServiceProjectAttachmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.ListServiceProjectAttachmentsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_service_project_attachments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_service_project_attachments(
        self, response: apphub_service.ListServiceProjectAttachmentsResponse
    ) -> apphub_service.ListServiceProjectAttachmentsResponse:
        """Post-rpc interceptor for list_service_project_attachments

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_services(
        self,
        request: apphub_service.ListServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.ListServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_services(
        self, response: apphub_service.ListServicesResponse
    ) -> apphub_service.ListServicesResponse:
        """Post-rpc interceptor for list_services

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_list_workloads(
        self,
        request: apphub_service.ListWorkloadsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.ListWorkloadsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workloads

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_workloads(
        self, response: apphub_service.ListWorkloadsResponse
    ) -> apphub_service.ListWorkloadsResponse:
        """Post-rpc interceptor for list_workloads

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_discovered_service(
        self,
        request: apphub_service.LookupDiscoveredServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.LookupDiscoveredServiceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for lookup_discovered_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_lookup_discovered_service(
        self, response: apphub_service.LookupDiscoveredServiceResponse
    ) -> apphub_service.LookupDiscoveredServiceResponse:
        """Post-rpc interceptor for lookup_discovered_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_discovered_workload(
        self,
        request: apphub_service.LookupDiscoveredWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.LookupDiscoveredWorkloadRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for lookup_discovered_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_lookup_discovered_workload(
        self, response: apphub_service.LookupDiscoveredWorkloadResponse
    ) -> apphub_service.LookupDiscoveredWorkloadResponse:
        """Post-rpc interceptor for lookup_discovered_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_lookup_service_project_attachment(
        self,
        request: apphub_service.LookupServiceProjectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        apphub_service.LookupServiceProjectAttachmentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for lookup_service_project_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_lookup_service_project_attachment(
        self, response: apphub_service.LookupServiceProjectAttachmentResponse
    ) -> apphub_service.LookupServiceProjectAttachmentResponse:
        """Post-rpc interceptor for lookup_service_project_attachment

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_application(
        self,
        request: apphub_service.UpdateApplicationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.UpdateApplicationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_application

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_update_application(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_application

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_service(
        self,
        request: apphub_service.UpdateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.UpdateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_update_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_service

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response

    def pre_update_workload(
        self,
        request: apphub_service.UpdateWorkloadRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apphub_service.UpdateWorkloadRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_workload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_update_workload(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_workload

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
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
        before they are sent to the AppHub server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AppHub server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AppHubRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AppHubRestInterceptor


class AppHubRestTransport(AppHubTransport):
    """REST backend transport for AppHub.

    The App Hub API allows you to manage App Hub resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "apphub.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AppHubRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apphub.googleapis.com').
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
        self._interceptor = interceptor or AppHubRestInterceptor()
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

    class _CreateApplication(AppHubRestStub):
        def __hash__(self):
            return hash("CreateApplication")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "applicationId": "",
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
            request: apphub_service.CreateApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create application method over HTTP.

            Args:
                request (~.apphub_service.CreateApplicationRequest):
                    The request object. Request for CreateApplication.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/applications",
                    "body": "application",
                },
            ]
            request, metadata = self._interceptor.pre_create_application(
                request, metadata
            )
            pb_request = apphub_service.CreateApplicationRequest.pb(request)
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
            resp = self._interceptor.post_create_application(resp)
            return resp

    class _CreateService(AppHubRestStub):
        def __hash__(self):
            return hash("CreateService")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "serviceId": "",
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
            request: apphub_service.CreateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service method over HTTP.

            Args:
                request (~.apphub_service.CreateServiceRequest):
                    The request object. Request for CreateService.
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
                    "uri": "/v1/{parent=projects/*/locations/*/applications/*}/services",
                    "body": "service",
                },
            ]
            request, metadata = self._interceptor.pre_create_service(request, metadata)
            pb_request = apphub_service.CreateServiceRequest.pb(request)
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
            resp = self._interceptor.post_create_service(resp)
            return resp

    class _CreateServiceProjectAttachment(AppHubRestStub):
        def __hash__(self):
            return hash("CreateServiceProjectAttachment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "serviceProjectAttachmentId": "",
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
            request: apphub_service.CreateServiceProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service project
            attachment method over HTTP.

                Args:
                    request (~.apphub_service.CreateServiceProjectAttachmentRequest):
                        The request object. Request for
                    CreateServiceProjectAttachment.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/serviceProjectAttachments",
                    "body": "service_project_attachment",
                },
            ]
            request, metadata = self._interceptor.pre_create_service_project_attachment(
                request, metadata
            )
            pb_request = apphub_service.CreateServiceProjectAttachmentRequest.pb(
                request
            )
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
            resp = self._interceptor.post_create_service_project_attachment(resp)
            return resp

    class _CreateWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("CreateWorkload")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workloadId": "",
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
            request: apphub_service.CreateWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create workload method over HTTP.

            Args:
                request (~.apphub_service.CreateWorkloadRequest):
                    The request object. Request for CreateWorkload.
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
                    "uri": "/v1/{parent=projects/*/locations/*/applications/*}/workloads",
                    "body": "workload",
                },
            ]
            request, metadata = self._interceptor.pre_create_workload(request, metadata)
            pb_request = apphub_service.CreateWorkloadRequest.pb(request)
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
            resp = self._interceptor.post_create_workload(resp)
            return resp

    class _DeleteApplication(AppHubRestStub):
        def __hash__(self):
            return hash("DeleteApplication")

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
            request: apphub_service.DeleteApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete application method over HTTP.

            Args:
                request (~.apphub_service.DeleteApplicationRequest):
                    The request object. Request for DeleteApplication.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_application(
                request, metadata
            )
            pb_request = apphub_service.DeleteApplicationRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_application(resp)
            return resp

    class _DeleteService(AppHubRestStub):
        def __hash__(self):
            return hash("DeleteService")

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
            request: apphub_service.DeleteServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service method over HTTP.

            Args:
                request (~.apphub_service.DeleteServiceRequest):
                    The request object. Request for DeleteService.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*/services/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_service(request, metadata)
            pb_request = apphub_service.DeleteServiceRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_service(resp)
            return resp

    class _DeleteServiceProjectAttachment(AppHubRestStub):
        def __hash__(self):
            return hash("DeleteServiceProjectAttachment")

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
            request: apphub_service.DeleteServiceProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service project
            attachment method over HTTP.

                Args:
                    request (~.apphub_service.DeleteServiceProjectAttachmentRequest):
                        The request object. Request for
                    DeleteServiceProjectAttachment.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/serviceProjectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_service_project_attachment(
                request, metadata
            )
            pb_request = apphub_service.DeleteServiceProjectAttachmentRequest.pb(
                request
            )
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_service_project_attachment(resp)
            return resp

    class _DeleteWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("DeleteWorkload")

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
            request: apphub_service.DeleteWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete workload method over HTTP.

            Args:
                request (~.apphub_service.DeleteWorkloadRequest):
                    The request object. Request for DeleteWorkload.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*/workloads/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workload(request, metadata)
            pb_request = apphub_service.DeleteWorkloadRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_workload(resp)
            return resp

    class _DetachServiceProjectAttachment(AppHubRestStub):
        def __hash__(self):
            return hash("DetachServiceProjectAttachment")

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
            request: apphub_service.DetachServiceProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.DetachServiceProjectAttachmentResponse:
            r"""Call the detach service project
            attachment method over HTTP.

                Args:
                    request (~.apphub_service.DetachServiceProjectAttachmentRequest):
                        The request object. Request for
                    DetachServiceProjectAttachment.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.apphub_service.DetachServiceProjectAttachmentResponse:
                        Response for
                    DetachServiceProjectAttachment.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*}:detachServiceProjectAttachment",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_detach_service_project_attachment(
                request, metadata
            )
            pb_request = apphub_service.DetachServiceProjectAttachmentRequest.pb(
                request
            )
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
            resp = apphub_service.DetachServiceProjectAttachmentResponse()
            pb_resp = apphub_service.DetachServiceProjectAttachmentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_detach_service_project_attachment(resp)
            return resp

    class _GetApplication(AppHubRestStub):
        def __hash__(self):
            return hash("GetApplication")

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
            request: apphub_service.GetApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> application.Application:
            r"""Call the get application method over HTTP.

            Args:
                request (~.apphub_service.GetApplicationRequest):
                    The request object. Request for GetApplication.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.application.Application:
                    Application defines the governance
                boundary for App Hub Entities that
                perform a logical end-to-end business
                function. App Hub supports application
                level IAM permission to align with
                governance requirements.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_application(request, metadata)
            pb_request = apphub_service.GetApplicationRequest.pb(request)
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
            resp = application.Application()
            pb_resp = application.Application.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_application(resp)
            return resp

    class _GetDiscoveredService(AppHubRestStub):
        def __hash__(self):
            return hash("GetDiscoveredService")

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
            request: apphub_service.GetDiscoveredServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.DiscoveredService:
            r"""Call the get discovered service method over HTTP.

            Args:
                request (~.apphub_service.GetDiscoveredServiceRequest):
                    The request object. Request for GetDiscoveredService.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.DiscoveredService:
                    DiscoveredService is a network/api
                interface that exposes some
                functionality to clients for consumption
                over the network. A discovered service
                can be registered to a App Hub service.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/discoveredServices/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_discovered_service(
                request, metadata
            )
            pb_request = apphub_service.GetDiscoveredServiceRequest.pb(request)
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
            resp = service.DiscoveredService()
            pb_resp = service.DiscoveredService.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_discovered_service(resp)
            return resp

    class _GetDiscoveredWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("GetDiscoveredWorkload")

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
            request: apphub_service.GetDiscoveredWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workload.DiscoveredWorkload:
            r"""Call the get discovered workload method over HTTP.

            Args:
                request (~.apphub_service.GetDiscoveredWorkloadRequest):
                    The request object. Request for GetDiscoveredWorkload.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workload.DiscoveredWorkload:
                    DiscoveredWorkload is a binary
                deployment (such as managed instance
                groups (MIGs) and GKE deployments) that
                performs the smallest logical subset of
                business functionality. A discovered
                workload can be registered to an App Hub
                Workload.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/discoveredWorkloads/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_discovered_workload(
                request, metadata
            )
            pb_request = apphub_service.GetDiscoveredWorkloadRequest.pb(request)
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
            resp = workload.DiscoveredWorkload()
            pb_resp = workload.DiscoveredWorkload.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_discovered_workload(resp)
            return resp

    class _GetService(AppHubRestStub):
        def __hash__(self):
            return hash("GetService")

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
            request: apphub_service.GetServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.Service:
            r"""Call the get service method over HTTP.

            Args:
                request (~.apphub_service.GetServiceRequest):
                    The request object. Request for GetService.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.Service:
                    Service is an App Hub data model that
                contains a discovered service, which
                represents a network/api interface that
                exposes some functionality to clients
                for consumption over the network.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*/services/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_service(request, metadata)
            pb_request = apphub_service.GetServiceRequest.pb(request)
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
            resp = service.Service()
            pb_resp = service.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service(resp)
            return resp

    class _GetServiceProjectAttachment(AppHubRestStub):
        def __hash__(self):
            return hash("GetServiceProjectAttachment")

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
            request: apphub_service.GetServiceProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service_project_attachment.ServiceProjectAttachment:
            r"""Call the get service project
            attachment method over HTTP.

                Args:
                    request (~.apphub_service.GetServiceProjectAttachmentRequest):
                        The request object. Request for
                    GetServiceProjectAttachment.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service_project_attachment.ServiceProjectAttachment:
                        ServiceProjectAttachment represents
                    an attachment from a service project to
                    a host project. Service projects contain
                    the underlying cloud infrastructure
                    resources, and expose these resources to
                    the host project through a
                    ServiceProjectAttachment. With the
                    attachments, the host project can
                    provide an aggregated view of resources
                    across all service projects.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/serviceProjectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_service_project_attachment(
                request, metadata
            )
            pb_request = apphub_service.GetServiceProjectAttachmentRequest.pb(request)
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
            resp = service_project_attachment.ServiceProjectAttachment()
            pb_resp = service_project_attachment.ServiceProjectAttachment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service_project_attachment(resp)
            return resp

    class _GetWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("GetWorkload")

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
            request: apphub_service.GetWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workload.Workload:
            r"""Call the get workload method over HTTP.

            Args:
                request (~.apphub_service.GetWorkloadRequest):
                    The request object. Request for GetWorkload.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workload.Workload:
                    Workload is an App Hub data model
                that contains a discovered workload,
                which represents a binary deployment
                (such as managed instance groups (MIGs)
                and GKE deployments) that performs the
                smallest logical subset of business
                functionality.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/applications/*/workloads/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workload(request, metadata)
            pb_request = apphub_service.GetWorkloadRequest.pb(request)
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
            resp = workload.Workload()
            pb_resp = workload.Workload.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workload(resp)
            return resp

    class _ListApplications(AppHubRestStub):
        def __hash__(self):
            return hash("ListApplications")

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
            request: apphub_service.ListApplicationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListApplicationsResponse:
            r"""Call the list applications method over HTTP.

            Args:
                request (~.apphub_service.ListApplicationsRequest):
                    The request object. Request for ListApplications.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.ListApplicationsResponse:
                    Response for ListApplications.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/applications",
                },
            ]
            request, metadata = self._interceptor.pre_list_applications(
                request, metadata
            )
            pb_request = apphub_service.ListApplicationsRequest.pb(request)
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
            resp = apphub_service.ListApplicationsResponse()
            pb_resp = apphub_service.ListApplicationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_applications(resp)
            return resp

    class _ListDiscoveredServices(AppHubRestStub):
        def __hash__(self):
            return hash("ListDiscoveredServices")

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
            request: apphub_service.ListDiscoveredServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListDiscoveredServicesResponse:
            r"""Call the list discovered services method over HTTP.

            Args:
                request (~.apphub_service.ListDiscoveredServicesRequest):
                    The request object. Request for ListDiscoveredServices.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.ListDiscoveredServicesResponse:
                    Response for ListDiscoveredServices.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/discoveredServices",
                },
            ]
            request, metadata = self._interceptor.pre_list_discovered_services(
                request, metadata
            )
            pb_request = apphub_service.ListDiscoveredServicesRequest.pb(request)
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
            resp = apphub_service.ListDiscoveredServicesResponse()
            pb_resp = apphub_service.ListDiscoveredServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_discovered_services(resp)
            return resp

    class _ListDiscoveredWorkloads(AppHubRestStub):
        def __hash__(self):
            return hash("ListDiscoveredWorkloads")

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
            request: apphub_service.ListDiscoveredWorkloadsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListDiscoveredWorkloadsResponse:
            r"""Call the list discovered workloads method over HTTP.

            Args:
                request (~.apphub_service.ListDiscoveredWorkloadsRequest):
                    The request object. Request for ListDiscoveredWorkloads.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.ListDiscoveredWorkloadsResponse:
                    Response for ListDiscoveredWorkloads.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/discoveredWorkloads",
                },
            ]
            request, metadata = self._interceptor.pre_list_discovered_workloads(
                request, metadata
            )
            pb_request = apphub_service.ListDiscoveredWorkloadsRequest.pb(request)
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
            resp = apphub_service.ListDiscoveredWorkloadsResponse()
            pb_resp = apphub_service.ListDiscoveredWorkloadsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_discovered_workloads(resp)
            return resp

    class _ListServiceProjectAttachments(AppHubRestStub):
        def __hash__(self):
            return hash("ListServiceProjectAttachments")

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
            request: apphub_service.ListServiceProjectAttachmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListServiceProjectAttachmentsResponse:
            r"""Call the list service project
            attachments method over HTTP.

                Args:
                    request (~.apphub_service.ListServiceProjectAttachmentsRequest):
                        The request object. Request for
                    ListServiceProjectAttachments.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.apphub_service.ListServiceProjectAttachmentsResponse:
                        Response for
                    ListServiceProjectAttachments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/serviceProjectAttachments",
                },
            ]
            request, metadata = self._interceptor.pre_list_service_project_attachments(
                request, metadata
            )
            pb_request = apphub_service.ListServiceProjectAttachmentsRequest.pb(request)
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
            resp = apphub_service.ListServiceProjectAttachmentsResponse()
            pb_resp = apphub_service.ListServiceProjectAttachmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_service_project_attachments(resp)
            return resp

    class _ListServices(AppHubRestStub):
        def __hash__(self):
            return hash("ListServices")

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
            request: apphub_service.ListServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListServicesResponse:
            r"""Call the list services method over HTTP.

            Args:
                request (~.apphub_service.ListServicesRequest):
                    The request object. Request for ListServices.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.ListServicesResponse:
                    Response for ListServices.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/applications/*}/services",
                },
            ]
            request, metadata = self._interceptor.pre_list_services(request, metadata)
            pb_request = apphub_service.ListServicesRequest.pb(request)
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
            resp = apphub_service.ListServicesResponse()
            pb_resp = apphub_service.ListServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_services(resp)
            return resp

    class _ListWorkloads(AppHubRestStub):
        def __hash__(self):
            return hash("ListWorkloads")

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
            request: apphub_service.ListWorkloadsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.ListWorkloadsResponse:
            r"""Call the list workloads method over HTTP.

            Args:
                request (~.apphub_service.ListWorkloadsRequest):
                    The request object. Request for ListWorkloads.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.ListWorkloadsResponse:
                    Response for ListWorkloads.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/applications/*}/workloads",
                },
            ]
            request, metadata = self._interceptor.pre_list_workloads(request, metadata)
            pb_request = apphub_service.ListWorkloadsRequest.pb(request)
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
            resp = apphub_service.ListWorkloadsResponse()
            pb_resp = apphub_service.ListWorkloadsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workloads(resp)
            return resp

    class _LookupDiscoveredService(AppHubRestStub):
        def __hash__(self):
            return hash("LookupDiscoveredService")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "uri": "",
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
            request: apphub_service.LookupDiscoveredServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.LookupDiscoveredServiceResponse:
            r"""Call the lookup discovered service method over HTTP.

            Args:
                request (~.apphub_service.LookupDiscoveredServiceRequest):
                    The request object. Request for LookupDiscoveredService.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apphub_service.LookupDiscoveredServiceResponse:
                    Response for LookupDiscoveredService.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/discoveredServices:lookup",
                },
            ]
            request, metadata = self._interceptor.pre_lookup_discovered_service(
                request, metadata
            )
            pb_request = apphub_service.LookupDiscoveredServiceRequest.pb(request)
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
            resp = apphub_service.LookupDiscoveredServiceResponse()
            pb_resp = apphub_service.LookupDiscoveredServiceResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_discovered_service(resp)
            return resp

    class _LookupDiscoveredWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("LookupDiscoveredWorkload")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "uri": "",
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
            request: apphub_service.LookupDiscoveredWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.LookupDiscoveredWorkloadResponse:
            r"""Call the lookup discovered
            workload method over HTTP.

                Args:
                    request (~.apphub_service.LookupDiscoveredWorkloadRequest):
                        The request object. Request for LookupDiscoveredWorkload.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.apphub_service.LookupDiscoveredWorkloadResponse:
                        Response for
                    LookupDiscoveredWorkload.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/discoveredWorkloads:lookup",
                },
            ]
            request, metadata = self._interceptor.pre_lookup_discovered_workload(
                request, metadata
            )
            pb_request = apphub_service.LookupDiscoveredWorkloadRequest.pb(request)
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
            resp = apphub_service.LookupDiscoveredWorkloadResponse()
            pb_resp = apphub_service.LookupDiscoveredWorkloadResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_discovered_workload(resp)
            return resp

    class _LookupServiceProjectAttachment(AppHubRestStub):
        def __hash__(self):
            return hash("LookupServiceProjectAttachment")

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
            request: apphub_service.LookupServiceProjectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apphub_service.LookupServiceProjectAttachmentResponse:
            r"""Call the lookup service project
            attachment method over HTTP.

                Args:
                    request (~.apphub_service.LookupServiceProjectAttachmentRequest):
                        The request object. Request for
                    LookupServiceProjectAttachment.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.apphub_service.LookupServiceProjectAttachmentResponse:
                        Response for
                    LookupServiceProjectAttachment.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}:lookupServiceProjectAttachment",
                },
            ]
            request, metadata = self._interceptor.pre_lookup_service_project_attachment(
                request, metadata
            )
            pb_request = apphub_service.LookupServiceProjectAttachmentRequest.pb(
                request
            )
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
            resp = apphub_service.LookupServiceProjectAttachmentResponse()
            pb_resp = apphub_service.LookupServiceProjectAttachmentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lookup_service_project_attachment(resp)
            return resp

    class _UpdateApplication(AppHubRestStub):
        def __hash__(self):
            return hash("UpdateApplication")

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
            request: apphub_service.UpdateApplicationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update application method over HTTP.

            Args:
                request (~.apphub_service.UpdateApplicationRequest):
                    The request object. Request for UpdateApplication.
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
                    "method": "patch",
                    "uri": "/v1/{application.name=projects/*/locations/*/applications/*}",
                    "body": "application",
                },
            ]
            request, metadata = self._interceptor.pre_update_application(
                request, metadata
            )
            pb_request = apphub_service.UpdateApplicationRequest.pb(request)
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
            resp = self._interceptor.post_update_application(resp)
            return resp

    class _UpdateService(AppHubRestStub):
        def __hash__(self):
            return hash("UpdateService")

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
            request: apphub_service.UpdateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update service method over HTTP.

            Args:
                request (~.apphub_service.UpdateServiceRequest):
                    The request object. Request for UpdateService.
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
                    "method": "patch",
                    "uri": "/v1/{service.name=projects/*/locations/*/applications/*/services/*}",
                    "body": "service",
                },
            ]
            request, metadata = self._interceptor.pre_update_service(request, metadata)
            pb_request = apphub_service.UpdateServiceRequest.pb(request)
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
            resp = self._interceptor.post_update_service(resp)
            return resp

    class _UpdateWorkload(AppHubRestStub):
        def __hash__(self):
            return hash("UpdateWorkload")

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
            request: apphub_service.UpdateWorkloadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update workload method over HTTP.

            Args:
                request (~.apphub_service.UpdateWorkloadRequest):
                    The request object. Request for UpdateWorkload.
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
                    "method": "patch",
                    "uri": "/v1/{workload.name=projects/*/locations/*/applications/*/workloads/*}",
                    "body": "workload",
                },
            ]
            request, metadata = self._interceptor.pre_update_workload(request, metadata)
            pb_request = apphub_service.UpdateWorkloadRequest.pb(request)
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
            resp = self._interceptor.post_update_workload(resp)
            return resp

    @property
    def create_application(
        self,
    ) -> Callable[[apphub_service.CreateApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service(
        self,
    ) -> Callable[[apphub_service.CreateServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service_project_attachment(
        self,
    ) -> Callable[
        [apphub_service.CreateServiceProjectAttachmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServiceProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workload(
        self,
    ) -> Callable[[apphub_service.CreateWorkloadRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_application(
        self,
    ) -> Callable[[apphub_service.DeleteApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service(
        self,
    ) -> Callable[[apphub_service.DeleteServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service_project_attachment(
        self,
    ) -> Callable[
        [apphub_service.DeleteServiceProjectAttachmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteServiceProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workload(
        self,
    ) -> Callable[[apphub_service.DeleteWorkloadRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def detach_service_project_attachment(
        self,
    ) -> Callable[
        [apphub_service.DetachServiceProjectAttachmentRequest],
        apphub_service.DetachServiceProjectAttachmentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DetachServiceProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_application(
        self,
    ) -> Callable[[apphub_service.GetApplicationRequest], application.Application]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_discovered_service(
        self,
    ) -> Callable[
        [apphub_service.GetDiscoveredServiceRequest], service.DiscoveredService
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDiscoveredService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_discovered_workload(
        self,
    ) -> Callable[
        [apphub_service.GetDiscoveredWorkloadRequest], workload.DiscoveredWorkload
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDiscoveredWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service(
        self,
    ) -> Callable[[apphub_service.GetServiceRequest], service.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service_project_attachment(
        self,
    ) -> Callable[
        [apphub_service.GetServiceProjectAttachmentRequest],
        service_project_attachment.ServiceProjectAttachment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServiceProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workload(
        self,
    ) -> Callable[[apphub_service.GetWorkloadRequest], workload.Workload]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_applications(
        self,
    ) -> Callable[
        [apphub_service.ListApplicationsRequest],
        apphub_service.ListApplicationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApplications(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_discovered_services(
        self,
    ) -> Callable[
        [apphub_service.ListDiscoveredServicesRequest],
        apphub_service.ListDiscoveredServicesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDiscoveredServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_discovered_workloads(
        self,
    ) -> Callable[
        [apphub_service.ListDiscoveredWorkloadsRequest],
        apphub_service.ListDiscoveredWorkloadsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDiscoveredWorkloads(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_service_project_attachments(
        self,
    ) -> Callable[
        [apphub_service.ListServiceProjectAttachmentsRequest],
        apphub_service.ListServiceProjectAttachmentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServiceProjectAttachments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_services(
        self,
    ) -> Callable[
        [apphub_service.ListServicesRequest], apphub_service.ListServicesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workloads(
        self,
    ) -> Callable[
        [apphub_service.ListWorkloadsRequest], apphub_service.ListWorkloadsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkloads(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_discovered_service(
        self,
    ) -> Callable[
        [apphub_service.LookupDiscoveredServiceRequest],
        apphub_service.LookupDiscoveredServiceResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupDiscoveredService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_discovered_workload(
        self,
    ) -> Callable[
        [apphub_service.LookupDiscoveredWorkloadRequest],
        apphub_service.LookupDiscoveredWorkloadResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupDiscoveredWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_service_project_attachment(
        self,
    ) -> Callable[
        [apphub_service.LookupServiceProjectAttachmentRequest],
        apphub_service.LookupServiceProjectAttachmentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupServiceProjectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_application(
        self,
    ) -> Callable[[apphub_service.UpdateApplicationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_service(
        self,
    ) -> Callable[[apphub_service.UpdateServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workload(
        self,
    ) -> Callable[[apphub_service.UpdateWorkloadRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(AppHubRestStub):
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

    class _ListLocations(AppHubRestStub):
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(AppHubRestStub):
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
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/applications/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(AppHubRestStub):
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
                    "uri": "/v1/{resource=projects/*/locations/*/applications/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(AppHubRestStub):
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
                    "uri": "/v1/{resource=projects/*/locations/*/applications/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
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

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(AppHubRestStub):
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

    class _DeleteOperation(AppHubRestStub):
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

    class _GetOperation(AppHubRestStub):
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

    class _ListOperations(AppHubRestStub):
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


__all__ = ("AppHubRestTransport",)
