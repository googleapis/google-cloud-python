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

from google.cloud.gdchardwaremanagement_v1alpha.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import GDCHardwareManagementTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class GDCHardwareManagementRestInterceptor:
    """Interceptor for GDCHardwareManagement.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GDCHardwareManagementRestTransport.

    .. code-block:: python
        class MyCustomGDCHardwareManagementInterceptor(GDCHardwareManagementRestInterceptor):
            def pre_create_comment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_comment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_hardware(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_hardware(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_hardware_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_hardware_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_hardware(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_hardware(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_hardware_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_hardware_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_change_log_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_change_log_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_comment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_comment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_hardware(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_hardware(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_hardware_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_hardware_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_sku(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_sku(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_change_log_entries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_change_log_entries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_comments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_comments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_hardware(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_hardware(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_hardware_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_hardware_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_orders(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_orders(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sites(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sites(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_skus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_skus(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_zones(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_zones(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_signal_zone_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_signal_zone_state(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_submit_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_submit_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_hardware(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_hardware(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_hardware_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_hardware_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_zone(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_zone(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = GDCHardwareManagementRestTransport(interceptor=MyCustomGDCHardwareManagementInterceptor())
        client = GDCHardwareManagementClient(transport=transport)


    """

    def pre_create_comment(
        self, request: service.CreateCommentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateCommentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_comment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_comment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_comment

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_hardware(
        self,
        request: service.CreateHardwareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateHardwareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_hardware

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_hardware(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_hardware

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_hardware_group(
        self,
        request: service.CreateHardwareGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateHardwareGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_hardware_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_hardware_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_hardware_group

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_order(
        self, request: service.CreateOrderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_order(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_order

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_site(
        self, request: service.CreateSiteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateSiteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_site

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_zone(
        self, request: service.CreateZoneRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_create_zone(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_zone

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_hardware(
        self,
        request: service.DeleteHardwareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteHardwareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_hardware

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_hardware(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_hardware

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_hardware_group(
        self,
        request: service.DeleteHardwareGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteHardwareGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_hardware_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_hardware_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_hardware_group

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_order(
        self, request: service.DeleteOrderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_order(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_order

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_zone(
        self, request: service.DeleteZoneRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_zone(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_zone

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_change_log_entry(
        self,
        request: service.GetChangeLogEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetChangeLogEntryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_change_log_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_change_log_entry(
        self, response: resources.ChangeLogEntry
    ) -> resources.ChangeLogEntry:
        """Post-rpc interceptor for get_change_log_entry

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_comment(
        self, request: service.GetCommentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetCommentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_comment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_comment(self, response: resources.Comment) -> resources.Comment:
        """Post-rpc interceptor for get_comment

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_hardware(
        self, request: service.GetHardwareRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetHardwareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_hardware

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_hardware(self, response: resources.Hardware) -> resources.Hardware:
        """Post-rpc interceptor for get_hardware

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_hardware_group(
        self,
        request: service.GetHardwareGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetHardwareGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_hardware_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_hardware_group(
        self, response: resources.HardwareGroup
    ) -> resources.HardwareGroup:
        """Post-rpc interceptor for get_hardware_group

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_order(
        self, request: service.GetOrderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_order(self, response: resources.Order) -> resources.Order:
        """Post-rpc interceptor for get_order

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_site(
        self, request: service.GetSiteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetSiteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_site(self, response: resources.Site) -> resources.Site:
        """Post-rpc interceptor for get_site

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_sku(
        self, request: service.GetSkuRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetSkuRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_sku

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_sku(self, response: resources.Sku) -> resources.Sku:
        """Post-rpc interceptor for get_sku

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_zone(
        self, request: service.GetZoneRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_zone(self, response: resources.Zone) -> resources.Zone:
        """Post-rpc interceptor for get_zone

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_change_log_entries(
        self,
        request: service.ListChangeLogEntriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListChangeLogEntriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_change_log_entries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_change_log_entries(
        self, response: service.ListChangeLogEntriesResponse
    ) -> service.ListChangeLogEntriesResponse:
        """Post-rpc interceptor for list_change_log_entries

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_comments(
        self, request: service.ListCommentsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListCommentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_comments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_comments(
        self, response: service.ListCommentsResponse
    ) -> service.ListCommentsResponse:
        """Post-rpc interceptor for list_comments

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_hardware(
        self, request: service.ListHardwareRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListHardwareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_hardware

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_hardware(
        self, response: service.ListHardwareResponse
    ) -> service.ListHardwareResponse:
        """Post-rpc interceptor for list_hardware

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_hardware_groups(
        self,
        request: service.ListHardwareGroupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListHardwareGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_hardware_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_hardware_groups(
        self, response: service.ListHardwareGroupsResponse
    ) -> service.ListHardwareGroupsResponse:
        """Post-rpc interceptor for list_hardware_groups

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_orders(
        self, request: service.ListOrdersRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListOrdersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_orders

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_orders(
        self, response: service.ListOrdersResponse
    ) -> service.ListOrdersResponse:
        """Post-rpc interceptor for list_orders

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_sites(
        self, request: service.ListSitesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListSitesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sites

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_sites(
        self, response: service.ListSitesResponse
    ) -> service.ListSitesResponse:
        """Post-rpc interceptor for list_sites

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_skus(
        self, request: service.ListSkusRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListSkusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_skus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_skus(
        self, response: service.ListSkusResponse
    ) -> service.ListSkusResponse:
        """Post-rpc interceptor for list_skus

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_zones(
        self, request: service.ListZonesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListZonesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_zones

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_zones(
        self, response: service.ListZonesResponse
    ) -> service.ListZonesResponse:
        """Post-rpc interceptor for list_zones

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_signal_zone_state(
        self,
        request: service.SignalZoneStateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.SignalZoneStateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for signal_zone_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_signal_zone_state(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for signal_zone_state

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_submit_order(
        self, request: service.SubmitOrderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.SubmitOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for submit_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_submit_order(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for submit_order

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_hardware(
        self,
        request: service.UpdateHardwareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateHardwareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_hardware

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_update_hardware(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_hardware

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_hardware_group(
        self,
        request: service.UpdateHardwareGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateHardwareGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_hardware_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_update_hardware_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_hardware_group

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_order(
        self, request: service.UpdateOrderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_update_order(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_order

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_site(
        self, request: service.UpdateSiteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateSiteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_update_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_site

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_zone(
        self, request: service.UpdateZoneRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateZoneRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_zone

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_update_zone(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_zone

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
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
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class GDCHardwareManagementRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GDCHardwareManagementRestInterceptor


class GDCHardwareManagementRestTransport(GDCHardwareManagementTransport):
    """REST backend transport for GDCHardwareManagement.

    The GDC Hardware Management service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "gdchardwaremanagement.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GDCHardwareManagementRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'gdchardwaremanagement.googleapis.com').
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
        self._interceptor = interceptor or GDCHardwareManagementRestInterceptor()
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
                        "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateComment(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateComment")

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
            request: service.CreateCommentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create comment method over HTTP.

            Args:
                request (~.service.CreateCommentRequest):
                    The request object. A request to create a comment.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*/orders/*}/comments",
                    "body": "comment",
                },
            ]
            request, metadata = self._interceptor.pre_create_comment(request, metadata)
            pb_request = service.CreateCommentRequest.pb(request)
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
            resp = self._interceptor.post_create_comment(resp)
            return resp

    class _CreateHardware(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateHardware")

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
            request: service.CreateHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create hardware method over HTTP.

            Args:
                request (~.service.CreateHardwareRequest):
                    The request object. A request to create hardware.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/hardware",
                    "body": "hardware",
                },
            ]
            request, metadata = self._interceptor.pre_create_hardware(request, metadata)
            pb_request = service.CreateHardwareRequest.pb(request)
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
            resp = self._interceptor.post_create_hardware(resp)
            return resp

    class _CreateHardwareGroup(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateHardwareGroup")

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
            request: service.CreateHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create hardware group method over HTTP.

            Args:
                request (~.service.CreateHardwareGroupRequest):
                    The request object. A request to create a hardware group.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*/orders/*}/hardwareGroups",
                    "body": "hardware_group",
                },
            ]
            request, metadata = self._interceptor.pre_create_hardware_group(
                request, metadata
            )
            pb_request = service.CreateHardwareGroupRequest.pb(request)
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
            resp = self._interceptor.post_create_hardware_group(resp)
            return resp

    class _CreateOrder(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateOrder")

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
            request: service.CreateOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create order method over HTTP.

            Args:
                request (~.service.CreateOrderRequest):
                    The request object. A request to create an order.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/orders",
                    "body": "order",
                },
            ]
            request, metadata = self._interceptor.pre_create_order(request, metadata)
            pb_request = service.CreateOrderRequest.pb(request)
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
            resp = self._interceptor.post_create_order(resp)
            return resp

    class _CreateSite(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateSite")

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
            request: service.CreateSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create site method over HTTP.

            Args:
                request (~.service.CreateSiteRequest):
                    The request object. A request to create a site.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/sites",
                    "body": "site",
                },
            ]
            request, metadata = self._interceptor.pre_create_site(request, metadata)
            pb_request = service.CreateSiteRequest.pb(request)
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
            resp = self._interceptor.post_create_site(resp)
            return resp

    class _CreateZone(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("CreateZone")

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
            request: service.CreateZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create zone method over HTTP.

            Args:
                request (~.service.CreateZoneRequest):
                    The request object. A request to create a zone.
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
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/zones",
                    "body": "zone",
                },
            ]
            request, metadata = self._interceptor.pre_create_zone(request, metadata)
            pb_request = service.CreateZoneRequest.pb(request)
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
            resp = self._interceptor.post_create_zone(resp)
            return resp

    class _DeleteHardware(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("DeleteHardware")

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
            request: service.DeleteHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete hardware method over HTTP.

            Args:
                request (~.service.DeleteHardwareRequest):
                    The request object. A request to delete hardware.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/hardware/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_hardware(request, metadata)
            pb_request = service.DeleteHardwareRequest.pb(request)
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
            resp = self._interceptor.post_delete_hardware(resp)
            return resp

    class _DeleteHardwareGroup(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("DeleteHardwareGroup")

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
            request: service.DeleteHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete hardware group method over HTTP.

            Args:
                request (~.service.DeleteHardwareGroupRequest):
                    The request object. A request to delete a hardware group.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*/hardwareGroups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_hardware_group(
                request, metadata
            )
            pb_request = service.DeleteHardwareGroupRequest.pb(request)
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
            resp = self._interceptor.post_delete_hardware_group(resp)
            return resp

    class _DeleteOrder(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("DeleteOrder")

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
            request: service.DeleteOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete order method over HTTP.

            Args:
                request (~.service.DeleteOrderRequest):
                    The request object. A request to delete an order.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_order(request, metadata)
            pb_request = service.DeleteOrderRequest.pb(request)
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
            resp = self._interceptor.post_delete_order(resp)
            return resp

    class _DeleteZone(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("DeleteZone")

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
            request: service.DeleteZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete zone method over HTTP.

            Args:
                request (~.service.DeleteZoneRequest):
                    The request object. A request to delete a zone.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/zones/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_zone(request, metadata)
            pb_request = service.DeleteZoneRequest.pb(request)
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
            resp = self._interceptor.post_delete_zone(resp)
            return resp

    class _GetChangeLogEntry(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetChangeLogEntry")

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
            request: service.GetChangeLogEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ChangeLogEntry:
            r"""Call the get change log entry method over HTTP.

            Args:
                request (~.service.GetChangeLogEntryRequest):
                    The request object. A request to get a change log entry.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ChangeLogEntry:
                    A log entry of a change made to an
                order.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*/changeLogEntries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_change_log_entry(
                request, metadata
            )
            pb_request = service.GetChangeLogEntryRequest.pb(request)
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
            resp = resources.ChangeLogEntry()
            pb_resp = resources.ChangeLogEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_change_log_entry(resp)
            return resp

    class _GetComment(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetComment")

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
            request: service.GetCommentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Comment:
            r"""Call the get comment method over HTTP.

            Args:
                request (~.service.GetCommentRequest):
                    The request object. A request to get a comment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Comment:
                    A comment on an order.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*/comments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_comment(request, metadata)
            pb_request = service.GetCommentRequest.pb(request)
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
            resp = resources.Comment()
            pb_resp = resources.Comment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_comment(resp)
            return resp

    class _GetHardware(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetHardware")

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
            request: service.GetHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Hardware:
            r"""Call the get hardware method over HTTP.

            Args:
                request (~.service.GetHardwareRequest):
                    The request object. A request to get hardware.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Hardware:
                    An instance of hardware installed at
                a site.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/hardware/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_hardware(request, metadata)
            pb_request = service.GetHardwareRequest.pb(request)
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
            resp = resources.Hardware()
            pb_resp = resources.Hardware.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_hardware(resp)
            return resp

    class _GetHardwareGroup(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetHardwareGroup")

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
            request: service.GetHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.HardwareGroup:
            r"""Call the get hardware group method over HTTP.

            Args:
                request (~.service.GetHardwareGroupRequest):
                    The request object. A request to get a hardware group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.HardwareGroup:
                    A group of hardware that is part of
                the same order, has the same SKU, and is
                delivered to the same site.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*/hardwareGroups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_hardware_group(
                request, metadata
            )
            pb_request = service.GetHardwareGroupRequest.pb(request)
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
            resp = resources.HardwareGroup()
            pb_resp = resources.HardwareGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_hardware_group(resp)
            return resp

    class _GetOrder(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetOrder")

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
            request: service.GetOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Order:
            r"""Call the get order method over HTTP.

            Args:
                request (~.service.GetOrderRequest):
                    The request object. A request to get an order.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Order:
                    An order for GDC hardware.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_order(request, metadata)
            pb_request = service.GetOrderRequest.pb(request)
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
            resp = resources.Order()
            pb_resp = resources.Order.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_order(resp)
            return resp

    class _GetSite(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetSite")

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
            request: service.GetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Site:
            r"""Call the get site method over HTTP.

            Args:
                request (~.service.GetSiteRequest):
                    The request object. A request to get a site.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Site:
                    A physical site where hardware will
                be installed.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/sites/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_site(request, metadata)
            pb_request = service.GetSiteRequest.pb(request)
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
            resp = resources.Site()
            pb_resp = resources.Site.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_site(resp)
            return resp

    class _GetSku(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("GetSku")

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
            request: service.GetSkuRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Sku:
            r"""Call the get sku method over HTTP.

            Args:
                request (~.service.GetSkuRequest):
                    The request object. A request to get an SKU.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Sku:
                    A stock keeping unit (SKU) of GDC
                hardware.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/skus/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_sku(request, metadata)
            pb_request = service.GetSkuRequest.pb(request)
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
            resp = resources.Sku()
            pb_resp = resources.Sku.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_sku(resp)
            return resp

    class _GetZone(GDCHardwareManagementRestStub):
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
                    The request object. A request to get a zone.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Zone:
                    A zone holding a set of hardware.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/zones/*}",
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

    class _ListChangeLogEntries(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListChangeLogEntries")

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
            request: service.ListChangeLogEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListChangeLogEntriesResponse:
            r"""Call the list change log entries method over HTTP.

            Args:
                request (~.service.ListChangeLogEntriesRequest):
                    The request object. A request to list change log entries.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListChangeLogEntriesResponse:
                    A list of change log entries.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/orders/*}/changeLogEntries",
                },
            ]
            request, metadata = self._interceptor.pre_list_change_log_entries(
                request, metadata
            )
            pb_request = service.ListChangeLogEntriesRequest.pb(request)
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
            resp = service.ListChangeLogEntriesResponse()
            pb_resp = service.ListChangeLogEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_change_log_entries(resp)
            return resp

    class _ListComments(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListComments")

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
            request: service.ListCommentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCommentsResponse:
            r"""Call the list comments method over HTTP.

            Args:
                request (~.service.ListCommentsRequest):
                    The request object. A request to list comments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCommentsResponse:
                    A request to list comments.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/orders/*}/comments",
                },
            ]
            request, metadata = self._interceptor.pre_list_comments(request, metadata)
            pb_request = service.ListCommentsRequest.pb(request)
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
            resp = service.ListCommentsResponse()
            pb_resp = service.ListCommentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_comments(resp)
            return resp

    class _ListHardware(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListHardware")

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
            request: service.ListHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListHardwareResponse:
            r"""Call the list hardware method over HTTP.

            Args:
                request (~.service.ListHardwareRequest):
                    The request object. A request to list hardware.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListHardwareResponse:
                    A list of hardware.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/hardware",
                },
            ]
            request, metadata = self._interceptor.pre_list_hardware(request, metadata)
            pb_request = service.ListHardwareRequest.pb(request)
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
            resp = service.ListHardwareResponse()
            pb_resp = service.ListHardwareResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_hardware(resp)
            return resp

    class _ListHardwareGroups(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListHardwareGroups")

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
            request: service.ListHardwareGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListHardwareGroupsResponse:
            r"""Call the list hardware groups method over HTTP.

            Args:
                request (~.service.ListHardwareGroupsRequest):
                    The request object. A request to list hardware groups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListHardwareGroupsResponse:
                    A list of hardware groups.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/orders/*}/hardwareGroups",
                },
            ]
            request, metadata = self._interceptor.pre_list_hardware_groups(
                request, metadata
            )
            pb_request = service.ListHardwareGroupsRequest.pb(request)
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
            resp = service.ListHardwareGroupsResponse()
            pb_resp = service.ListHardwareGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_hardware_groups(resp)
            return resp

    class _ListOrders(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListOrders")

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
            request: service.ListOrdersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListOrdersResponse:
            r"""Call the list orders method over HTTP.

            Args:
                request (~.service.ListOrdersRequest):
                    The request object. A request to list orders.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListOrdersResponse:
                    A list of orders.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/orders",
                },
            ]
            request, metadata = self._interceptor.pre_list_orders(request, metadata)
            pb_request = service.ListOrdersRequest.pb(request)
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
            resp = service.ListOrdersResponse()
            pb_resp = service.ListOrdersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_orders(resp)
            return resp

    class _ListSites(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListSites")

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
            request: service.ListSitesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListSitesResponse:
            r"""Call the list sites method over HTTP.

            Args:
                request (~.service.ListSitesRequest):
                    The request object. A request to list sites.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListSitesResponse:
                    A list of sites.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/sites",
                },
            ]
            request, metadata = self._interceptor.pre_list_sites(request, metadata)
            pb_request = service.ListSitesRequest.pb(request)
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
            resp = service.ListSitesResponse()
            pb_resp = service.ListSitesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sites(resp)
            return resp

    class _ListSkus(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("ListSkus")

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
            request: service.ListSkusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListSkusResponse:
            r"""Call the list skus method over HTTP.

            Args:
                request (~.service.ListSkusRequest):
                    The request object. A request to list SKUs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListSkusResponse:
                    A list of SKUs.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/skus",
                },
            ]
            request, metadata = self._interceptor.pre_list_skus(request, metadata)
            pb_request = service.ListSkusRequest.pb(request)
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
            resp = service.ListSkusResponse()
            pb_resp = service.ListSkusResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_skus(resp)
            return resp

    class _ListZones(GDCHardwareManagementRestStub):
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
                    The request object. A request to list zones.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListZonesResponse:
                    A list of zones.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/zones",
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

    class _SignalZoneState(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("SignalZoneState")

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
            request: service.SignalZoneStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the signal zone state method over HTTP.

            Args:
                request (~.service.SignalZoneStateRequest):
                    The request object. A request to signal the state of a
                zone.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/zones/*}:signal",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_signal_zone_state(
                request, metadata
            )
            pb_request = service.SignalZoneStateRequest.pb(request)
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
            resp = self._interceptor.post_signal_zone_state(resp)
            return resp

    class _SubmitOrder(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("SubmitOrder")

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
            request: service.SubmitOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the submit order method over HTTP.

            Args:
                request (~.service.SubmitOrderRequest):
                    The request object. A request to submit an order.
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/orders/*}:submit",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_submit_order(request, metadata)
            pb_request = service.SubmitOrderRequest.pb(request)
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
            resp = self._interceptor.post_submit_order(resp)
            return resp

    class _UpdateHardware(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("UpdateHardware")

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
            request: service.UpdateHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update hardware method over HTTP.

            Args:
                request (~.service.UpdateHardwareRequest):
                    The request object. A request to update hardware.
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
                    "uri": "/v1alpha/{hardware.name=projects/*/locations/*/hardware/*}",
                    "body": "hardware",
                },
            ]
            request, metadata = self._interceptor.pre_update_hardware(request, metadata)
            pb_request = service.UpdateHardwareRequest.pb(request)
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
            resp = self._interceptor.post_update_hardware(resp)
            return resp

    class _UpdateHardwareGroup(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("UpdateHardwareGroup")

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
            request: service.UpdateHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update hardware group method over HTTP.

            Args:
                request (~.service.UpdateHardwareGroupRequest):
                    The request object. A request to update a hardware group.
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
                    "uri": "/v1alpha/{hardware_group.name=projects/*/locations/*/orders/*/hardwareGroups/*}",
                    "body": "hardware_group",
                },
            ]
            request, metadata = self._interceptor.pre_update_hardware_group(
                request, metadata
            )
            pb_request = service.UpdateHardwareGroupRequest.pb(request)
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
            resp = self._interceptor.post_update_hardware_group(resp)
            return resp

    class _UpdateOrder(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("UpdateOrder")

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
            request: service.UpdateOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update order method over HTTP.

            Args:
                request (~.service.UpdateOrderRequest):
                    The request object. A request to update an order.
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
                    "uri": "/v1alpha/{order.name=projects/*/locations/*/orders/*}",
                    "body": "order",
                },
            ]
            request, metadata = self._interceptor.pre_update_order(request, metadata)
            pb_request = service.UpdateOrderRequest.pb(request)
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
            resp = self._interceptor.post_update_order(resp)
            return resp

    class _UpdateSite(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("UpdateSite")

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
            request: service.UpdateSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update site method over HTTP.

            Args:
                request (~.service.UpdateSiteRequest):
                    The request object. A request to update a site.
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
                    "uri": "/v1alpha/{site.name=projects/*/locations/*/sites/*}",
                    "body": "site",
                },
            ]
            request, metadata = self._interceptor.pre_update_site(request, metadata)
            pb_request = service.UpdateSiteRequest.pb(request)
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
            resp = self._interceptor.post_update_site(resp)
            return resp

    class _UpdateZone(GDCHardwareManagementRestStub):
        def __hash__(self):
            return hash("UpdateZone")

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
            request: service.UpdateZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update zone method over HTTP.

            Args:
                request (~.service.UpdateZoneRequest):
                    The request object. A request to update a zone.
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
                    "uri": "/v1alpha/{zone.name=projects/*/locations/*/zones/*}",
                    "body": "zone",
                },
            ]
            request, metadata = self._interceptor.pre_update_zone(request, metadata)
            pb_request = service.UpdateZoneRequest.pb(request)
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
            resp = self._interceptor.post_update_zone(resp)
            return resp

    @property
    def create_comment(
        self,
    ) -> Callable[[service.CreateCommentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateComment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_hardware(
        self,
    ) -> Callable[[service.CreateHardwareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateHardware(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_hardware_group(
        self,
    ) -> Callable[[service.CreateHardwareGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateHardwareGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_order(
        self,
    ) -> Callable[[service.CreateOrderRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_site(
        self,
    ) -> Callable[[service.CreateSiteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_zone(
        self,
    ) -> Callable[[service.CreateZoneRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_hardware(
        self,
    ) -> Callable[[service.DeleteHardwareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteHardware(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_hardware_group(
        self,
    ) -> Callable[[service.DeleteHardwareGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteHardwareGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_order(
        self,
    ) -> Callable[[service.DeleteOrderRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_zone(
        self,
    ) -> Callable[[service.DeleteZoneRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_change_log_entry(
        self,
    ) -> Callable[[service.GetChangeLogEntryRequest], resources.ChangeLogEntry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChangeLogEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_comment(self) -> Callable[[service.GetCommentRequest], resources.Comment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetComment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_hardware(
        self,
    ) -> Callable[[service.GetHardwareRequest], resources.Hardware]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHardware(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_hardware_group(
        self,
    ) -> Callable[[service.GetHardwareGroupRequest], resources.HardwareGroup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHardwareGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_order(self) -> Callable[[service.GetOrderRequest], resources.Order]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_site(self) -> Callable[[service.GetSiteRequest], resources.Site]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_sku(self) -> Callable[[service.GetSkuRequest], resources.Sku]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSku(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_zone(self) -> Callable[[service.GetZoneRequest], resources.Zone]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_change_log_entries(
        self,
    ) -> Callable[
        [service.ListChangeLogEntriesRequest], service.ListChangeLogEntriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChangeLogEntries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_comments(
        self,
    ) -> Callable[[service.ListCommentsRequest], service.ListCommentsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListComments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_hardware(
        self,
    ) -> Callable[[service.ListHardwareRequest], service.ListHardwareResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHardware(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_hardware_groups(
        self,
    ) -> Callable[
        [service.ListHardwareGroupsRequest], service.ListHardwareGroupsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHardwareGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_orders(
        self,
    ) -> Callable[[service.ListOrdersRequest], service.ListOrdersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOrders(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sites(
        self,
    ) -> Callable[[service.ListSitesRequest], service.ListSitesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSites(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_skus(
        self,
    ) -> Callable[[service.ListSkusRequest], service.ListSkusResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSkus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_zones(
        self,
    ) -> Callable[[service.ListZonesRequest], service.ListZonesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListZones(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def signal_zone_state(
        self,
    ) -> Callable[[service.SignalZoneStateRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SignalZoneState(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def submit_order(
        self,
    ) -> Callable[[service.SubmitOrderRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SubmitOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_hardware(
        self,
    ) -> Callable[[service.UpdateHardwareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateHardware(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_hardware_group(
        self,
    ) -> Callable[[service.UpdateHardwareGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateHardwareGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_order(
        self,
    ) -> Callable[[service.UpdateOrderRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_site(
        self,
    ) -> Callable[[service.UpdateSiteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_zone(
        self,
    ) -> Callable[[service.UpdateZoneRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateZone(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*}",
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

    class _ListLocations(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*}/locations",
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

    class _CancelOperation(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}:cancel",
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

    class _DeleteOperation(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
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

    class _GetOperation(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(GDCHardwareManagementRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
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


__all__ = ("GDCHardwareManagementRestTransport",)
