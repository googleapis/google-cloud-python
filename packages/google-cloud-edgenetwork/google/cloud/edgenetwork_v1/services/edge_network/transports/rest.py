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

from google.cloud.edgenetwork_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import EdgeNetworkTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class EdgeNetworkRestInterceptor:
    """Interceptor for EdgeNetwork.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EdgeNetworkRestTransport.

    .. code-block:: python
        class MyCustomEdgeNetworkInterceptor(EdgeNetworkRestInterceptor):
            def pre_create_interconnect_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_interconnect_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_router(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_router(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_interconnect_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_interconnect_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_router(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_router(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_diagnose_interconnect(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_diagnose_interconnect(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_diagnose_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_diagnose_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_diagnose_router(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_diagnose_router(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_interconnect(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_interconnect(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_interconnect_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_interconnect_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_router(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_router(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_initialize_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_initialize_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_interconnect_attachments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_interconnect_attachments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_interconnects(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_interconnects(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_networks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_networks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_routers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_routers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_subnets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_subnets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_zones(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_zones(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_router(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_router(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EdgeNetworkRestTransport(interceptor=MyCustomEdgeNetworkInterceptor())
        client = EdgeNetworkClient(transport=transport)


    """

    def pre_create_interconnect_attachment(
        self,
        request: service.CreateInterconnectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateInterconnectAttachmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_interconnect_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_create_interconnect_attachment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_interconnect_attachment

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_create_network(
        self, request: service.CreateNetworkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_create_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_network

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_create_router(
        self, request: service.CreateRouterRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateRouterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_router

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_create_router(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_router

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_create_subnet(
        self, request: service.CreateSubnetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_create_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_subnet

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_delete_interconnect_attachment(
        self,
        request: service.DeleteInterconnectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteInterconnectAttachmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_interconnect_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_delete_interconnect_attachment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_interconnect_attachment

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_delete_network(
        self, request: service.DeleteNetworkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_delete_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_network

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_delete_router(
        self, request: service.DeleteRouterRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteRouterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_router

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_delete_router(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_router

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_delete_subnet(
        self, request: service.DeleteSubnetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_delete_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_subnet

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_diagnose_interconnect(
        self,
        request: service.DiagnoseInterconnectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DiagnoseInterconnectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for diagnose_interconnect

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_diagnose_interconnect(
        self, response: service.DiagnoseInterconnectResponse
    ) -> service.DiagnoseInterconnectResponse:
        """Post-rpc interceptor for diagnose_interconnect

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_diagnose_network(
        self,
        request: service.DiagnoseNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DiagnoseNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for diagnose_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_diagnose_network(
        self, response: service.DiagnoseNetworkResponse
    ) -> service.DiagnoseNetworkResponse:
        """Post-rpc interceptor for diagnose_network

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_diagnose_router(
        self,
        request: service.DiagnoseRouterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DiagnoseRouterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for diagnose_router

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_diagnose_router(
        self, response: service.DiagnoseRouterResponse
    ) -> service.DiagnoseRouterResponse:
        """Post-rpc interceptor for diagnose_router

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_interconnect(
        self,
        request: service.GetInterconnectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetInterconnectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_interconnect

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_interconnect(
        self, response: resources.Interconnect
    ) -> resources.Interconnect:
        """Post-rpc interceptor for get_interconnect

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_interconnect_attachment(
        self,
        request: service.GetInterconnectAttachmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetInterconnectAttachmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_interconnect_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_interconnect_attachment(
        self, response: resources.InterconnectAttachment
    ) -> resources.InterconnectAttachment:
        """Post-rpc interceptor for get_interconnect_attachment

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_network(
        self, request: service.GetNetworkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_network(self, response: resources.Network) -> resources.Network:
        """Post-rpc interceptor for get_network

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_router(
        self, request: service.GetRouterRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetRouterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_router

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_router(self, response: resources.Router) -> resources.Router:
        """Post-rpc interceptor for get_router

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_subnet(
        self, request: service.GetSubnetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_subnet(self, response: resources.Subnet) -> resources.Subnet:
        """Post-rpc interceptor for get_subnet

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_get_zone(
        self, request: service.GetZoneRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_zone(self, response: resources.Zone) -> resources.Zone:
        """Post-rpc interceptor for get_zone

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_initialize_zone(
        self,
        request: service.InitializeZoneRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.InitializeZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for initialize_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_initialize_zone(
        self, response: service.InitializeZoneResponse
    ) -> service.InitializeZoneResponse:
        """Post-rpc interceptor for initialize_zone

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_interconnect_attachments(
        self,
        request: service.ListInterconnectAttachmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListInterconnectAttachmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_interconnect_attachments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_interconnect_attachments(
        self, response: service.ListInterconnectAttachmentsResponse
    ) -> service.ListInterconnectAttachmentsResponse:
        """Post-rpc interceptor for list_interconnect_attachments

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_interconnects(
        self,
        request: service.ListInterconnectsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListInterconnectsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_interconnects

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_interconnects(
        self, response: service.ListInterconnectsResponse
    ) -> service.ListInterconnectsResponse:
        """Post-rpc interceptor for list_interconnects

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_networks(
        self, request: service.ListNetworksRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListNetworksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_networks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_networks(
        self, response: service.ListNetworksResponse
    ) -> service.ListNetworksResponse:
        """Post-rpc interceptor for list_networks

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_routers(
        self, request: service.ListRoutersRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListRoutersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_routers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_routers(
        self, response: service.ListRoutersResponse
    ) -> service.ListRoutersResponse:
        """Post-rpc interceptor for list_routers

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_subnets(
        self, request: service.ListSubnetsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListSubnetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_subnets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_subnets(
        self, response: service.ListSubnetsResponse
    ) -> service.ListSubnetsResponse:
        """Post-rpc interceptor for list_subnets

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_list_zones(
        self, request: service.ListZonesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListZonesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_zones

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_zones(
        self, response: service.ListZonesResponse
    ) -> service.ListZonesResponse:
        """Post-rpc interceptor for list_zones

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_update_router(
        self, request: service.UpdateRouterRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateRouterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_router

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_update_router(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_router

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response

    def pre_update_subnet(
        self, request: service.UpdateSubnetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_update_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_subnet

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
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
        before they are sent to the EdgeNetwork server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the EdgeNetwork server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EdgeNetworkRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EdgeNetworkRestInterceptor


class EdgeNetworkRestTransport(EdgeNetworkTransport):
    """REST backend transport for EdgeNetwork.

    EdgeNetwork API provides managed, highly available cloud
    dynamic network configuration service to the GEC customer to
    enable edge application and network function solutions. This
    allows the customers to easily define and configure the network
    setup and property to meet the workload requirement.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "edgenetwork.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EdgeNetworkRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'edgenetwork.googleapis.com').
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
        self._interceptor = interceptor or EdgeNetworkRestInterceptor()
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

    class _CreateInterconnectAttachment(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("CreateInterconnectAttachment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "interconnectAttachmentId": "",
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
            request: service.CreateInterconnectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create interconnect
            attachment method over HTTP.

                Args:
                    request (~.service.CreateInterconnectAttachmentRequest):
                        The request object. Message for creating a
                    InterconnectAttachment
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
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/interconnectAttachments",
                    "body": "interconnect_attachment",
                },
            ]
            request, metadata = self._interceptor.pre_create_interconnect_attachment(
                request, metadata
            )
            pb_request = service.CreateInterconnectAttachmentRequest.pb(request)
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
            resp = self._interceptor.post_create_interconnect_attachment(resp)
            return resp

    class _CreateNetwork(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("CreateNetwork")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "networkId": "",
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
            request: service.CreateNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create network method over HTTP.

            Args:
                request (~.service.CreateNetworkRequest):
                    The request object. Message for creating a Network
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
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/networks",
                    "body": "network",
                },
            ]
            request, metadata = self._interceptor.pre_create_network(request, metadata)
            pb_request = service.CreateNetworkRequest.pb(request)
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
            resp = self._interceptor.post_create_network(resp)
            return resp

    class _CreateRouter(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("CreateRouter")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "routerId": "",
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
            request: service.CreateRouterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create router method over HTTP.

            Args:
                request (~.service.CreateRouterRequest):
                    The request object. Message for creating a Router
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
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/routers",
                    "body": "router",
                },
            ]
            request, metadata = self._interceptor.pre_create_router(request, metadata)
            pb_request = service.CreateRouterRequest.pb(request)
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
            resp = self._interceptor.post_create_router(resp)
            return resp

    class _CreateSubnet(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("CreateSubnet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "subnetId": "",
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
            request: service.CreateSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create subnet method over HTTP.

            Args:
                request (~.service.CreateSubnetRequest):
                    The request object. Message for creating a Subnet
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
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/subnets",
                    "body": "subnet",
                },
            ]
            request, metadata = self._interceptor.pre_create_subnet(request, metadata)
            pb_request = service.CreateSubnetRequest.pb(request)
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
            resp = self._interceptor.post_create_subnet(resp)
            return resp

    class _DeleteInterconnectAttachment(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DeleteInterconnectAttachment")

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
            request: service.DeleteInterconnectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete interconnect
            attachment method over HTTP.

                Args:
                    request (~.service.DeleteInterconnectAttachmentRequest):
                        The request object. Message for deleting a
                    InterconnectAttachment
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
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/interconnectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_interconnect_attachment(
                request, metadata
            )
            pb_request = service.DeleteInterconnectAttachmentRequest.pb(request)
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
            resp = self._interceptor.post_delete_interconnect_attachment(resp)
            return resp

    class _DeleteNetwork(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DeleteNetwork")

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
            request: service.DeleteNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete network method over HTTP.

            Args:
                request (~.service.DeleteNetworkRequest):
                    The request object. Message for deleting a Network
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
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/networks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_network(request, metadata)
            pb_request = service.DeleteNetworkRequest.pb(request)
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
            resp = self._interceptor.post_delete_network(resp)
            return resp

    class _DeleteRouter(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DeleteRouter")

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
            request: service.DeleteRouterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete router method over HTTP.

            Args:
                request (~.service.DeleteRouterRequest):
                    The request object. Message for deleting a Router
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
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/routers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_router(request, metadata)
            pb_request = service.DeleteRouterRequest.pb(request)
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
            resp = self._interceptor.post_delete_router(resp)
            return resp

    class _DeleteSubnet(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DeleteSubnet")

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
            request: service.DeleteSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete subnet method over HTTP.

            Args:
                request (~.service.DeleteSubnetRequest):
                    The request object. Message for deleting a Subnet
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
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/subnets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_subnet(request, metadata)
            pb_request = service.DeleteSubnetRequest.pb(request)
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
            resp = self._interceptor.post_delete_subnet(resp)
            return resp

    class _DiagnoseInterconnect(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DiagnoseInterconnect")

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
            request: service.DiagnoseInterconnectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.DiagnoseInterconnectResponse:
            r"""Call the diagnose interconnect method over HTTP.

            Args:
                request (~.service.DiagnoseInterconnectRequest):
                    The request object. Message for requesting the
                diagnostics of an interconnect within a
                specific zone.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.DiagnoseInterconnectResponse:
                    DiagnoseInterconnectResponse contains
                the current diagnostics for a specific
                interconnect.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/interconnects/*}:diagnose",
                },
            ]
            request, metadata = self._interceptor.pre_diagnose_interconnect(
                request, metadata
            )
            pb_request = service.DiagnoseInterconnectRequest.pb(request)
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
            resp = service.DiagnoseInterconnectResponse()
            pb_resp = service.DiagnoseInterconnectResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_diagnose_interconnect(resp)
            return resp

    class _DiagnoseNetwork(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DiagnoseNetwork")

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
            request: service.DiagnoseNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.DiagnoseNetworkResponse:
            r"""Call the diagnose network method over HTTP.

            Args:
                request (~.service.DiagnoseNetworkRequest):
                    The request object. Message for requesting the
                diagnostics of a network within a
                specific zone.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.DiagnoseNetworkResponse:
                    DiagnoseNetworkResponse contains the
                current status for a specific network.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/networks/*}:diagnose",
                },
            ]
            request, metadata = self._interceptor.pre_diagnose_network(
                request, metadata
            )
            pb_request = service.DiagnoseNetworkRequest.pb(request)
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
            resp = service.DiagnoseNetworkResponse()
            pb_resp = service.DiagnoseNetworkResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_diagnose_network(resp)
            return resp

    class _DiagnoseRouter(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("DiagnoseRouter")

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
            request: service.DiagnoseRouterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.DiagnoseRouterResponse:
            r"""Call the diagnose router method over HTTP.

            Args:
                request (~.service.DiagnoseRouterRequest):
                    The request object. Message for requesting diagnositcs of
                a router within a specific zone.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.DiagnoseRouterResponse:
                    DiagnoseRouterResponse contains the
                current status for a specific router.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/routers/*}:diagnose",
                },
            ]
            request, metadata = self._interceptor.pre_diagnose_router(request, metadata)
            pb_request = service.DiagnoseRouterRequest.pb(request)
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
            resp = service.DiagnoseRouterResponse()
            pb_resp = service.DiagnoseRouterResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_diagnose_router(resp)
            return resp

    class _GetInterconnect(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetInterconnect")

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
            request: service.GetInterconnectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Interconnect:
            r"""Call the get interconnect method over HTTP.

            Args:
                request (~.service.GetInterconnectRequest):
                    The request object. Message for getting a Interconnect
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Interconnect:
                    Message describing Interconnect
                object

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/interconnects/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_interconnect(
                request, metadata
            )
            pb_request = service.GetInterconnectRequest.pb(request)
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
            resp = resources.Interconnect()
            pb_resp = resources.Interconnect.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_interconnect(resp)
            return resp

    class _GetInterconnectAttachment(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetInterconnectAttachment")

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
            request: service.GetInterconnectAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.InterconnectAttachment:
            r"""Call the get interconnect
            attachment method over HTTP.

                Args:
                    request (~.service.GetInterconnectAttachmentRequest):
                        The request object. Message for getting a
                    InterconnectAttachment
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.InterconnectAttachment:
                        Message describing
                    InterconnectAttachment object

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/interconnectAttachments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_interconnect_attachment(
                request, metadata
            )
            pb_request = service.GetInterconnectAttachmentRequest.pb(request)
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
            resp = resources.InterconnectAttachment()
            pb_resp = resources.InterconnectAttachment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_interconnect_attachment(resp)
            return resp

    class _GetNetwork(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetNetwork")

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
            request: service.GetNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Network:
            r"""Call the get network method over HTTP.

            Args:
                request (~.service.GetNetworkRequest):
                    The request object. Message for getting a Network
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Network:
                    Message describing Network object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/networks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_network(request, metadata)
            pb_request = service.GetNetworkRequest.pb(request)
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
            resp = resources.Network()
            pb_resp = resources.Network.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_network(resp)
            return resp

    class _GetRouter(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetRouter")

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
            request: service.GetRouterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Router:
            r"""Call the get router method over HTTP.

            Args:
                request (~.service.GetRouterRequest):
                    The request object. Message for getting a Router
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Router:
                    Message describing Router object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/routers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_router(request, metadata)
            pb_request = service.GetRouterRequest.pb(request)
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
            resp = resources.Router()
            pb_resp = resources.Router.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_router(resp)
            return resp

    class _GetSubnet(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetSubnet")

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
            request: service.GetSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Subnet:
            r"""Call the get subnet method over HTTP.

            Args:
                request (~.service.GetSubnetRequest):
                    The request object. Message for getting a Subnet
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Subnet:
                    Message describing Subnet object
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*/subnets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_subnet(request, metadata)
            pb_request = service.GetSubnetRequest.pb(request)
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
            resp = resources.Subnet()
            pb_resp = resources.Subnet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_subnet(resp)
            return resp

    class _GetZone(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("GetZone")

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
            request: service.GetZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Zone:
            r"""Call the get zone method over HTTP.

            Args:
                request (~.service.GetZoneRequest):
                    The request object. Deprecated: not implemented.
                Message for getting a Zone
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Zone:
                    A Google Edge Cloud zone.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_zone(request, metadata)
            pb_request = service.GetZoneRequest.pb(request)
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
            resp = resources.Zone()
            pb_resp = resources.Zone.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_zone(resp)
            return resp

    class _InitializeZone(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("InitializeZone")

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
            request: service.InitializeZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.InitializeZoneResponse:
            r"""Call the initialize zone method over HTTP.

            Args:
                request (~.service.InitializeZoneRequest):
                    The request object. Message for initializing a specified
                zone
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.InitializeZoneResponse:
                    The response of initializing a zone
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/zones/*}:initialize",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_initialize_zone(request, metadata)
            pb_request = service.InitializeZoneRequest.pb(request)
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
            resp = service.InitializeZoneResponse()
            pb_resp = service.InitializeZoneResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_initialize_zone(resp)
            return resp

    class _ListInterconnectAttachments(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListInterconnectAttachments")

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
            request: service.ListInterconnectAttachmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListInterconnectAttachmentsResponse:
            r"""Call the list interconnect
            attachments method over HTTP.

                Args:
                    request (~.service.ListInterconnectAttachmentsRequest):
                        The request object. Message for requesting list of
                    InterconnectAttachments
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListInterconnectAttachmentsResponse:
                        Message for response to listing
                    InterconnectAttachments

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/interconnectAttachments",
                },
            ]
            request, metadata = self._interceptor.pre_list_interconnect_attachments(
                request, metadata
            )
            pb_request = service.ListInterconnectAttachmentsRequest.pb(request)
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
            resp = service.ListInterconnectAttachmentsResponse()
            pb_resp = service.ListInterconnectAttachmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_interconnect_attachments(resp)
            return resp

    class _ListInterconnects(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListInterconnects")

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
            request: service.ListInterconnectsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListInterconnectsResponse:
            r"""Call the list interconnects method over HTTP.

            Args:
                request (~.service.ListInterconnectsRequest):
                    The request object. Message for requesting list of
                Interconnects
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListInterconnectsResponse:
                    Message for response to listing
                Interconnects

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/interconnects",
                },
            ]
            request, metadata = self._interceptor.pre_list_interconnects(
                request, metadata
            )
            pb_request = service.ListInterconnectsRequest.pb(request)
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
            resp = service.ListInterconnectsResponse()
            pb_resp = service.ListInterconnectsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_interconnects(resp)
            return resp

    class _ListNetworks(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListNetworks")

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
            request: service.ListNetworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListNetworksResponse:
            r"""Call the list networks method over HTTP.

            Args:
                request (~.service.ListNetworksRequest):
                    The request object. Message for requesting list of
                Networks
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListNetworksResponse:
                    Message for response to listing
                Networks

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/networks",
                },
            ]
            request, metadata = self._interceptor.pre_list_networks(request, metadata)
            pb_request = service.ListNetworksRequest.pb(request)
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
            resp = service.ListNetworksResponse()
            pb_resp = service.ListNetworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_networks(resp)
            return resp

    class _ListRouters(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListRouters")

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
            request: service.ListRoutersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListRoutersResponse:
            r"""Call the list routers method over HTTP.

            Args:
                request (~.service.ListRoutersRequest):
                    The request object. Message for requesting list of
                Routers
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListRoutersResponse:
                    Message for response to listing
                Routers

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/routers",
                },
            ]
            request, metadata = self._interceptor.pre_list_routers(request, metadata)
            pb_request = service.ListRoutersRequest.pb(request)
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
            resp = service.ListRoutersResponse()
            pb_resp = service.ListRoutersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_routers(resp)
            return resp

    class _ListSubnets(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListSubnets")

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
            request: service.ListSubnetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListSubnetsResponse:
            r"""Call the list subnets method over HTTP.

            Args:
                request (~.service.ListSubnetsRequest):
                    The request object. Message for requesting list of
                Subnets
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListSubnetsResponse:
                    Message for response to listing
                Subnets

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/zones/*}/subnets",
                },
            ]
            request, metadata = self._interceptor.pre_list_subnets(request, metadata)
            pb_request = service.ListSubnetsRequest.pb(request)
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
            resp = service.ListSubnetsResponse()
            pb_resp = service.ListSubnetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_subnets(resp)
            return resp

    class _ListZones(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("ListZones")

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
            request: service.ListZonesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListZonesResponse:
            r"""Call the list zones method over HTTP.

            Args:
                request (~.service.ListZonesRequest):
                    The request object. Deprecated: not implemented.
                Message for requesting list of Zones
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListZonesResponse:
                    Deprecated: not implemented.
                Message for response to listing Zones

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/zones",
                },
            ]
            request, metadata = self._interceptor.pre_list_zones(request, metadata)
            pb_request = service.ListZonesRequest.pb(request)
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
            resp = service.ListZonesResponse()
            pb_resp = service.ListZonesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_zones(resp)
            return resp

    class _UpdateRouter(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("UpdateRouter")

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
            request: service.UpdateRouterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update router method over HTTP.

            Args:
                request (~.service.UpdateRouterRequest):
                    The request object. Message for updating a Router
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
                    "uri": "/v1/{router.name=projects/*/locations/*/zones/*/routers/*}",
                    "body": "router",
                },
            ]
            request, metadata = self._interceptor.pre_update_router(request, metadata)
            pb_request = service.UpdateRouterRequest.pb(request)
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
            resp = self._interceptor.post_update_router(resp)
            return resp

    class _UpdateSubnet(EdgeNetworkRestStub):
        def __hash__(self):
            return hash("UpdateSubnet")

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
            request: service.UpdateSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update subnet method over HTTP.

            Args:
                request (~.service.UpdateSubnetRequest):
                    The request object. Message for updating a Subnet
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
                    "uri": "/v1/{subnet.name=projects/*/locations/*/zones/*/subnets/*}",
                    "body": "subnet",
                },
            ]
            request, metadata = self._interceptor.pre_update_subnet(request, metadata)
            pb_request = service.UpdateSubnetRequest.pb(request)
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
            resp = self._interceptor.post_update_subnet(resp)
            return resp

    @property
    def create_interconnect_attachment(
        self,
    ) -> Callable[
        [service.CreateInterconnectAttachmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInterconnectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_network(
        self,
    ) -> Callable[[service.CreateNetworkRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_router(
        self,
    ) -> Callable[[service.CreateRouterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRouter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_subnet(
        self,
    ) -> Callable[[service.CreateSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_interconnect_attachment(
        self,
    ) -> Callable[
        [service.DeleteInterconnectAttachmentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInterconnectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_network(
        self,
    ) -> Callable[[service.DeleteNetworkRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_router(
        self,
    ) -> Callable[[service.DeleteRouterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRouter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_subnet(
        self,
    ) -> Callable[[service.DeleteSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def diagnose_interconnect(
        self,
    ) -> Callable[
        [service.DiagnoseInterconnectRequest], service.DiagnoseInterconnectResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DiagnoseInterconnect(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def diagnose_network(
        self,
    ) -> Callable[[service.DiagnoseNetworkRequest], service.DiagnoseNetworkResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DiagnoseNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def diagnose_router(
        self,
    ) -> Callable[[service.DiagnoseRouterRequest], service.DiagnoseRouterResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DiagnoseRouter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_interconnect(
        self,
    ) -> Callable[[service.GetInterconnectRequest], resources.Interconnect]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInterconnect(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_interconnect_attachment(
        self,
    ) -> Callable[
        [service.GetInterconnectAttachmentRequest], resources.InterconnectAttachment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInterconnectAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_network(self) -> Callable[[service.GetNetworkRequest], resources.Network]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_router(self) -> Callable[[service.GetRouterRequest], resources.Router]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRouter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_subnet(self) -> Callable[[service.GetSubnetRequest], resources.Subnet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_zone(self) -> Callable[[service.GetZoneRequest], resources.Zone]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def initialize_zone(
        self,
    ) -> Callable[[service.InitializeZoneRequest], service.InitializeZoneResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InitializeZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_interconnect_attachments(
        self,
    ) -> Callable[
        [service.ListInterconnectAttachmentsRequest],
        service.ListInterconnectAttachmentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInterconnectAttachments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_interconnects(
        self,
    ) -> Callable[
        [service.ListInterconnectsRequest], service.ListInterconnectsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInterconnects(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_networks(
        self,
    ) -> Callable[[service.ListNetworksRequest], service.ListNetworksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_routers(
        self,
    ) -> Callable[[service.ListRoutersRequest], service.ListRoutersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRouters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_subnets(
        self,
    ) -> Callable[[service.ListSubnetsRequest], service.ListSubnetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSubnets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_zones(
        self,
    ) -> Callable[[service.ListZonesRequest], service.ListZonesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListZones(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_router(
        self,
    ) -> Callable[[service.UpdateRouterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRouter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_subnet(
        self,
    ) -> Callable[[service.UpdateSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(EdgeNetworkRestStub):
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

    class _ListLocations(EdgeNetworkRestStub):
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

    class _CancelOperation(EdgeNetworkRestStub):
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

    class _DeleteOperation(EdgeNetworkRestStub):
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

    class _GetOperation(EdgeNetworkRestStub):
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

    class _ListOperations(EdgeNetworkRestStub):
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


__all__ = ("EdgeNetworkRestTransport",)
