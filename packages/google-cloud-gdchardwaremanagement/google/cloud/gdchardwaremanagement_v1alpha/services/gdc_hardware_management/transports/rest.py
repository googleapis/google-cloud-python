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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.gdchardwaremanagement_v1alpha.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseGDCHardwareManagementRestTransport

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

            def pre_delete_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_site(self, response):
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

            def pre_record_action_on_comment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_record_action_on_comment(self, response):
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
        self,
        request: service.CreateCommentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateCommentRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateHardwareRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.CreateHardwareGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.CreateOrderRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateOrderRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.CreateSiteRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateSiteRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.CreateZoneRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.CreateZoneRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteHardwareRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.DeleteHardwareGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.DeleteOrderRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteOrderRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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

    def pre_delete_site(
        self,
        request: service.DeleteSiteRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteSiteRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_delete_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_site

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_zone(
        self,
        request: service.DeleteZoneRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.DeleteZoneRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GetChangeLogEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.GetCommentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetCommentRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.GetHardwareRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetHardwareRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.GetHardwareGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.GetOrderRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetOrderRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.GetSiteRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetSiteRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.GetSkuRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetSkuRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.GetZoneRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetZoneRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListChangeLogEntriesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.ListCommentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListCommentsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.ListHardwareRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListHardwareRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListHardwareGroupsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.ListOrdersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListOrdersRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.ListSitesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListSitesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.ListSkusRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListSkusRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.ListZonesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.ListZonesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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

    def pre_record_action_on_comment(
        self,
        request: service.RecordActionOnCommentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.RecordActionOnCommentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for record_action_on_comment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GDCHardwareManagement server.
        """
        return request, metadata

    def post_record_action_on_comment(
        self, response: resources.Comment
    ) -> resources.Comment:
        """Post-rpc interceptor for record_action_on_comment

        Override in a subclass to manipulate the response
        after it is returned by the GDCHardwareManagement server but before
        it is returned to user code.
        """
        return response

    def pre_signal_zone_state(
        self,
        request: service.SignalZoneStateRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.SignalZoneStateRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.SubmitOrderRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.SubmitOrderRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateHardwareRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.UpdateHardwareGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        self,
        request: service.UpdateOrderRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateOrderRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.UpdateSiteRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateSiteRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        self,
        request: service.UpdateZoneRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateZoneRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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


class GDCHardwareManagementRestTransport(_BaseGDCHardwareManagementRestTransport):
    """REST backend synchronous transport for GDCHardwareManagement.

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

    class _CreateComment(
        _BaseGDCHardwareManagementRestTransport._BaseCreateComment,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateComment")

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
            request: service.CreateCommentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create comment method over HTTP.

            Args:
                request (~.service.CreateCommentRequest):
                    The request object. A request to create a comment.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateComment._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_comment(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateComment._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateComment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateComment._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateComment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateComment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._CreateComment._get_response(
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

            resp = self._interceptor.post_create_comment(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_comment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateComment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateHardware(
        _BaseGDCHardwareManagementRestTransport._BaseCreateHardware,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateHardware")

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
            request: service.CreateHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create hardware method over HTTP.

            Args:
                request (~.service.CreateHardwareRequest):
                    The request object. A request to create hardware.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateHardware._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_hardware(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateHardware._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateHardware._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateHardware._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateHardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateHardware",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._CreateHardware._get_response(
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

            resp = self._interceptor.post_create_hardware(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_hardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateHardware",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateHardwareGroup(
        _BaseGDCHardwareManagementRestTransport._BaseCreateHardwareGroup,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateHardwareGroup")

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
            request: service.CreateHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create hardware group method over HTTP.

            Args:
                request (~.service.CreateHardwareGroupRequest):
                    The request object. A request to create a hardware group.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateHardwareGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_hardware_group(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateHardwareGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateHardwareGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateHardwareGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateHardwareGroup",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateHardwareGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._CreateHardwareGroup._get_response(
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

            resp = self._interceptor.post_create_hardware_group(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_hardware_group",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateHardwareGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateOrder(
        _BaseGDCHardwareManagementRestTransport._BaseCreateOrder,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateOrder")

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
            request: service.CreateOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create order method over HTTP.

            Args:
                request (~.service.CreateOrderRequest):
                    The request object. A request to create an order.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateOrder._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_order(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateOrder._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateOrder._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateOrder._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateOrder",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateOrder",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._CreateOrder._get_response(
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

            resp = self._interceptor.post_create_order(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_order",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateOrder",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateSite(
        _BaseGDCHardwareManagementRestTransport._BaseCreateSite,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateSite")

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
            request: service.CreateSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create site method over HTTP.

            Args:
                request (~.service.CreateSiteRequest):
                    The request object. A request to create a site.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateSite._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_site(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateSite._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateSite._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateSite._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateSite",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateSite",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._CreateSite._get_response(
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

            resp = self._interceptor.post_create_site(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_site",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateSite",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateZone(
        _BaseGDCHardwareManagementRestTransport._BaseCreateZone,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CreateZone")

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
            request: service.CreateZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create zone method over HTTP.

            Args:
                request (~.service.CreateZoneRequest):
                    The request object. A request to create a zone.
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
                _BaseGDCHardwareManagementRestTransport._BaseCreateZone._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_zone(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCreateZone._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCreateZone._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCreateZone._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CreateZone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateZone",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._CreateZone._get_response(
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

            resp = self._interceptor.post_create_zone(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.create_zone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CreateZone",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteHardware(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteHardware,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteHardware")

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
            request: service.DeleteHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete hardware method over HTTP.

            Args:
                request (~.service.DeleteHardwareRequest):
                    The request object. A request to delete hardware.
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
                _BaseGDCHardwareManagementRestTransport._BaseDeleteHardware._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_hardware(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteHardware._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteHardware._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteHardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteHardware",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._DeleteHardware._get_response(
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

            resp = self._interceptor.post_delete_hardware(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.delete_hardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteHardware",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteHardwareGroup(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteHardwareGroup,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteHardwareGroup")

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
            request: service.DeleteHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete hardware group method over HTTP.

            Args:
                request (~.service.DeleteHardwareGroupRequest):
                    The request object. A request to delete a hardware group.
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
                _BaseGDCHardwareManagementRestTransport._BaseDeleteHardwareGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_hardware_group(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteHardwareGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteHardwareGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteHardwareGroup",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteHardwareGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._DeleteHardwareGroup._get_response(
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

            resp = self._interceptor.post_delete_hardware_group(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.delete_hardware_group",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteHardwareGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteOrder(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteOrder,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteOrder")

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
            request: service.DeleteOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete order method over HTTP.

            Args:
                request (~.service.DeleteOrderRequest):
                    The request object. A request to delete an order.
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
                _BaseGDCHardwareManagementRestTransport._BaseDeleteOrder._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_order(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteOrder._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteOrder._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteOrder",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteOrder",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._DeleteOrder._get_response(
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

            resp = self._interceptor.post_delete_order(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.delete_order",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteOrder",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteSite(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteSite,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteSite")

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
            request: service.DeleteSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete site method over HTTP.

            Args:
                request (~.service.DeleteSiteRequest):
                    The request object. A request to delete a site.
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
                _BaseGDCHardwareManagementRestTransport._BaseDeleteSite._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_site(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteSite._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteSite._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteSite",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteSite",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._DeleteSite._get_response(
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

            resp = self._interceptor.post_delete_site(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.delete_site",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteSite",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteZone(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteZone,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteZone")

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
            request: service.DeleteZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete zone method over HTTP.

            Args:
                request (~.service.DeleteZoneRequest):
                    The request object. A request to delete a zone.
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
                _BaseGDCHardwareManagementRestTransport._BaseDeleteZone._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_zone(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteZone._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteZone._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteZone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteZone",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._DeleteZone._get_response(
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

            resp = self._interceptor.post_delete_zone(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.delete_zone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteZone",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetChangeLogEntry(
        _BaseGDCHardwareManagementRestTransport._BaseGetChangeLogEntry,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetChangeLogEntry")

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
            request: service.GetChangeLogEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.ChangeLogEntry:
            r"""Call the get change log entry method over HTTP.

            Args:
                request (~.service.GetChangeLogEntryRequest):
                    The request object. A request to get a change log entry.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.ChangeLogEntry:
                    A log entry of a change made to an
                order.

            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetChangeLogEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_change_log_entry(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetChangeLogEntry._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetChangeLogEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetChangeLogEntry",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetChangeLogEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._GetChangeLogEntry._get_response(
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
            resp = resources.ChangeLogEntry()
            pb_resp = resources.ChangeLogEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_change_log_entry(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.ChangeLogEntry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_change_log_entry",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetChangeLogEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetComment(
        _BaseGDCHardwareManagementRestTransport._BaseGetComment,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetComment")

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
            request: service.GetCommentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Comment:
            r"""Call the get comment method over HTTP.

            Args:
                request (~.service.GetCommentRequest):
                    The request object. A request to get a comment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Comment:
                    A comment on an order.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetComment._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_comment(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetComment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetComment._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetComment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetComment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetComment._get_response(
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
            resp = resources.Comment()
            pb_resp = resources.Comment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_comment(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Comment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_comment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetComment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetHardware(
        _BaseGDCHardwareManagementRestTransport._BaseGetHardware,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetHardware")

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
            request: service.GetHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Hardware:
            r"""Call the get hardware method over HTTP.

            Args:
                request (~.service.GetHardwareRequest):
                    The request object. A request to get hardware.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Hardware:
                    An instance of hardware installed at
                a site.

            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetHardware._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_hardware(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetHardware._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetHardware._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetHardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetHardware",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetHardware._get_response(
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
            resp = resources.Hardware()
            pb_resp = resources.Hardware.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_hardware(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Hardware.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_hardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetHardware",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetHardwareGroup(
        _BaseGDCHardwareManagementRestTransport._BaseGetHardwareGroup,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetHardwareGroup")

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
            request: service.GetHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.HardwareGroup:
            r"""Call the get hardware group method over HTTP.

            Args:
                request (~.service.GetHardwareGroupRequest):
                    The request object. A request to get a hardware group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.HardwareGroup:
                    A group of hardware that is part of
                the same order, has the same SKU, and is
                delivered to the same site.

            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetHardwareGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_hardware_group(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetHardwareGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetHardwareGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetHardwareGroup",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetHardwareGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._GetHardwareGroup._get_response(
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
            resp = resources.HardwareGroup()
            pb_resp = resources.HardwareGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_hardware_group(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.HardwareGroup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_hardware_group",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetHardwareGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetOrder(
        _BaseGDCHardwareManagementRestTransport._BaseGetOrder,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetOrder")

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
            request: service.GetOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Order:
            r"""Call the get order method over HTTP.

            Args:
                request (~.service.GetOrderRequest):
                    The request object. A request to get an order.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Order:
                    An order for GDC hardware.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetOrder._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_order(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetOrder._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetOrder._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetOrder",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetOrder",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetOrder._get_response(
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
            resp = resources.Order()
            pb_resp = resources.Order.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_order(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Order.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_order",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetOrder",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSite(
        _BaseGDCHardwareManagementRestTransport._BaseGetSite,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetSite")

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
            request: service.GetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Site:
            r"""Call the get site method over HTTP.

            Args:
                request (~.service.GetSiteRequest):
                    The request object. A request to get a site.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Site:
                    A physical site where hardware will
                be installed.

            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetSite._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_site(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetSite._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetSite._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetSite",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetSite",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetSite._get_response(
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
            resp = resources.Site()
            pb_resp = resources.Site.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_site(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Site.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_site",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetSite",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSku(
        _BaseGDCHardwareManagementRestTransport._BaseGetSku,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetSku")

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
            request: service.GetSkuRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Sku:
            r"""Call the get sku method over HTTP.

            Args:
                request (~.service.GetSkuRequest):
                    The request object. A request to get an SKU.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Sku:
                    A stock keeping unit (SKU) of GDC
                hardware.

            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetSku._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_sku(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetSku._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetSku._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetSku",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetSku",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetSku._get_response(
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
            resp = resources.Sku()
            pb_resp = resources.Sku.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_sku(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Sku.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_sku",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetSku",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetZone(
        _BaseGDCHardwareManagementRestTransport._BaseGetZone,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetZone")

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
            request: service.GetZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Zone:
            r"""Call the get zone method over HTTP.

            Args:
                request (~.service.GetZoneRequest):
                    The request object. A request to get a zone.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Zone:
                    A zone holding a set of hardware.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetZone._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_zone(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetZone._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetZone._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetZone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetZone",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetZone._get_response(
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
            resp = resources.Zone()
            pb_resp = resources.Zone.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_zone(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Zone.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.get_zone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetZone",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListChangeLogEntries(
        _BaseGDCHardwareManagementRestTransport._BaseListChangeLogEntries,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListChangeLogEntries")

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
            request: service.ListChangeLogEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListChangeLogEntriesResponse:
            r"""Call the list change log entries method over HTTP.

            Args:
                request (~.service.ListChangeLogEntriesRequest):
                    The request object. A request to list change log entries.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListChangeLogEntriesResponse:
                    A list of change log entries.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListChangeLogEntries._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_change_log_entries(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListChangeLogEntries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListChangeLogEntries._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListChangeLogEntries",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListChangeLogEntries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._ListChangeLogEntries._get_response(
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
            resp = service.ListChangeLogEntriesResponse()
            pb_resp = service.ListChangeLogEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_change_log_entries(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListChangeLogEntriesResponse.to_json(
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_change_log_entries",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListChangeLogEntries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListComments(
        _BaseGDCHardwareManagementRestTransport._BaseListComments,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListComments")

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
            request: service.ListCommentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListCommentsResponse:
            r"""Call the list comments method over HTTP.

            Args:
                request (~.service.ListCommentsRequest):
                    The request object. A request to list comments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListCommentsResponse:
                    A request to list comments.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListComments._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_comments(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListComments._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListComments._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListComments",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListComments",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListComments._get_response(
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
            resp = service.ListCommentsResponse()
            pb_resp = service.ListCommentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_comments(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListCommentsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_comments",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListComments",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListHardware(
        _BaseGDCHardwareManagementRestTransport._BaseListHardware,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListHardware")

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
            request: service.ListHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListHardwareResponse:
            r"""Call the list hardware method over HTTP.

            Args:
                request (~.service.ListHardwareRequest):
                    The request object. A request to list hardware.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListHardwareResponse:
                    A list of hardware.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListHardware._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_hardware(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListHardware._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListHardware._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListHardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListHardware",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListHardware._get_response(
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
            resp = service.ListHardwareResponse()
            pb_resp = service.ListHardwareResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_hardware(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListHardwareResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_hardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListHardware",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListHardwareGroups(
        _BaseGDCHardwareManagementRestTransport._BaseListHardwareGroups,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListHardwareGroups")

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
            request: service.ListHardwareGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListHardwareGroupsResponse:
            r"""Call the list hardware groups method over HTTP.

            Args:
                request (~.service.ListHardwareGroupsRequest):
                    The request object. A request to list hardware groups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListHardwareGroupsResponse:
                    A list of hardware groups.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListHardwareGroups._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_hardware_groups(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListHardwareGroups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListHardwareGroups._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListHardwareGroups",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListHardwareGroups",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._ListHardwareGroups._get_response(
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
            resp = service.ListHardwareGroupsResponse()
            pb_resp = service.ListHardwareGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_hardware_groups(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListHardwareGroupsResponse.to_json(
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_hardware_groups",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListHardwareGroups",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListOrders(
        _BaseGDCHardwareManagementRestTransport._BaseListOrders,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListOrders")

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
            request: service.ListOrdersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListOrdersResponse:
            r"""Call the list orders method over HTTP.

            Args:
                request (~.service.ListOrdersRequest):
                    The request object. A request to list orders.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListOrdersResponse:
                    A list of orders.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListOrders._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_orders(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListOrders._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListOrders._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListOrders",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListOrders",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListOrders._get_response(
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
            resp = service.ListOrdersResponse()
            pb_resp = service.ListOrdersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_orders(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListOrdersResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_orders",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListOrders",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListSites(
        _BaseGDCHardwareManagementRestTransport._BaseListSites,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListSites")

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
            request: service.ListSitesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListSitesResponse:
            r"""Call the list sites method over HTTP.

            Args:
                request (~.service.ListSitesRequest):
                    The request object. A request to list sites.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListSitesResponse:
                    A list of sites.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListSites._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_sites(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListSites._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListSites._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListSites",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListSites",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListSites._get_response(
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
            resp = service.ListSitesResponse()
            pb_resp = service.ListSitesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_sites(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListSitesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_sites",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListSites",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListSkus(
        _BaseGDCHardwareManagementRestTransport._BaseListSkus,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListSkus")

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
            request: service.ListSkusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListSkusResponse:
            r"""Call the list skus method over HTTP.

            Args:
                request (~.service.ListSkusRequest):
                    The request object. A request to list SKUs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListSkusResponse:
                    A list of SKUs.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListSkus._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_skus(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListSkus._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListSkus._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListSkus",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListSkus",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListSkus._get_response(
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
            resp = service.ListSkusResponse()
            pb_resp = service.ListSkusResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_skus(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListSkusResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_skus",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListSkus",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListZones(
        _BaseGDCHardwareManagementRestTransport._BaseListZones,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListZones")

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
            request: service.ListZonesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListZonesResponse:
            r"""Call the list zones method over HTTP.

            Args:
                request (~.service.ListZonesRequest):
                    The request object. A request to list zones.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListZonesResponse:
                    A list of zones.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListZones._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_zones(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListZones._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListZones._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListZones",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListZones",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListZones._get_response(
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
            resp = service.ListZonesResponse()
            pb_resp = service.ListZonesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_zones(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListZonesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.list_zones",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListZones",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RecordActionOnComment(
        _BaseGDCHardwareManagementRestTransport._BaseRecordActionOnComment,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.RecordActionOnComment")

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
            request: service.RecordActionOnCommentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Comment:
            r"""Call the record action on comment method over HTTP.

            Args:
                request (~.service.RecordActionOnCommentRequest):
                    The request object. A request to record an action on a
                comment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Comment:
                    A comment on an order.
            """

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseRecordActionOnComment._get_http_options()
            )

            request, metadata = self._interceptor.pre_record_action_on_comment(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseRecordActionOnComment._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseRecordActionOnComment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseRecordActionOnComment._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.RecordActionOnComment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "RecordActionOnComment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._RecordActionOnComment._get_response(
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
            resp = resources.Comment()
            pb_resp = resources.Comment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_record_action_on_comment(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Comment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.record_action_on_comment",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "RecordActionOnComment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SignalZoneState(
        _BaseGDCHardwareManagementRestTransport._BaseSignalZoneState,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.SignalZoneState")

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
            request: service.SignalZoneStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the signal zone state method over HTTP.

            Args:
                request (~.service.SignalZoneStateRequest):
                    The request object. A request to signal the state of a
                zone.
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
                _BaseGDCHardwareManagementRestTransport._BaseSignalZoneState._get_http_options()
            )

            request, metadata = self._interceptor.pre_signal_zone_state(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseSignalZoneState._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseSignalZoneState._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseSignalZoneState._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.SignalZoneState",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "SignalZoneState",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._SignalZoneState._get_response(
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

            resp = self._interceptor.post_signal_zone_state(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.signal_zone_state",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "SignalZoneState",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SubmitOrder(
        _BaseGDCHardwareManagementRestTransport._BaseSubmitOrder,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.SubmitOrder")

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
            request: service.SubmitOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the submit order method over HTTP.

            Args:
                request (~.service.SubmitOrderRequest):
                    The request object. A request to submit an order.
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
                _BaseGDCHardwareManagementRestTransport._BaseSubmitOrder._get_http_options()
            )

            request, metadata = self._interceptor.pre_submit_order(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseSubmitOrder._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseSubmitOrder._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseSubmitOrder._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.SubmitOrder",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "SubmitOrder",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._SubmitOrder._get_response(
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

            resp = self._interceptor.post_submit_order(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.submit_order",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "SubmitOrder",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateHardware(
        _BaseGDCHardwareManagementRestTransport._BaseUpdateHardware,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.UpdateHardware")

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
            request: service.UpdateHardwareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update hardware method over HTTP.

            Args:
                request (~.service.UpdateHardwareRequest):
                    The request object. A request to update hardware.
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
                _BaseGDCHardwareManagementRestTransport._BaseUpdateHardware._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_hardware(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardware._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardware._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardware._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.UpdateHardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateHardware",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._UpdateHardware._get_response(
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

            resp = self._interceptor.post_update_hardware(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.update_hardware",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateHardware",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateHardwareGroup(
        _BaseGDCHardwareManagementRestTransport._BaseUpdateHardwareGroup,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.UpdateHardwareGroup")

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
            request: service.UpdateHardwareGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update hardware group method over HTTP.

            Args:
                request (~.service.UpdateHardwareGroupRequest):
                    The request object. A request to update a hardware group.
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
                _BaseGDCHardwareManagementRestTransport._BaseUpdateHardwareGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_hardware_group(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardwareGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardwareGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseUpdateHardwareGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.UpdateHardwareGroup",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateHardwareGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._UpdateHardwareGroup._get_response(
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

            resp = self._interceptor.post_update_hardware_group(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.update_hardware_group",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateHardwareGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateOrder(
        _BaseGDCHardwareManagementRestTransport._BaseUpdateOrder,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.UpdateOrder")

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
            request: service.UpdateOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update order method over HTTP.

            Args:
                request (~.service.UpdateOrderRequest):
                    The request object. A request to update an order.
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
                _BaseGDCHardwareManagementRestTransport._BaseUpdateOrder._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_order(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseUpdateOrder._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseUpdateOrder._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseUpdateOrder._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.UpdateOrder",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateOrder",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._UpdateOrder._get_response(
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

            resp = self._interceptor.post_update_order(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.update_order",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateOrder",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSite(
        _BaseGDCHardwareManagementRestTransport._BaseUpdateSite,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.UpdateSite")

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
            request: service.UpdateSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update site method over HTTP.

            Args:
                request (~.service.UpdateSiteRequest):
                    The request object. A request to update a site.
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
                _BaseGDCHardwareManagementRestTransport._BaseUpdateSite._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_site(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseUpdateSite._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseUpdateSite._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseUpdateSite._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.UpdateSite",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateSite",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._UpdateSite._get_response(
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

            resp = self._interceptor.post_update_site(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.update_site",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateSite",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateZone(
        _BaseGDCHardwareManagementRestTransport._BaseUpdateZone,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.UpdateZone")

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
            request: service.UpdateZoneRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update zone method over HTTP.

            Args:
                request (~.service.UpdateZoneRequest):
                    The request object. A request to update a zone.
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
                _BaseGDCHardwareManagementRestTransport._BaseUpdateZone._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_zone(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseUpdateZone._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseUpdateZone._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseUpdateZone._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.UpdateZone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateZone",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._UpdateZone._get_response(
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

            resp = self._interceptor.post_update_zone(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.update_zone",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "UpdateZone",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
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
    def delete_site(
        self,
    ) -> Callable[[service.DeleteSiteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSite(self._session, self._host, self._interceptor)  # type: ignore

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
    def record_action_on_comment(
        self,
    ) -> Callable[[service.RecordActionOnCommentRequest], resources.Comment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RecordActionOnComment(self._session, self._host, self._interceptor)  # type: ignore

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

    class _GetLocation(
        _BaseGDCHardwareManagementRestTransport._BaseGetLocation,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetLocation._get_response(
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
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseGDCHardwareManagementRestTransport._BaseListLocations,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListLocations._get_response(
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
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseGDCHardwareManagementRestTransport._BaseCancelOperation,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.CancelOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseGDCHardwareManagementRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseCancelOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseGDCHardwareManagementRestTransport._BaseDeleteOperation,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.DeleteOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseDeleteOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                GDCHardwareManagementRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseGDCHardwareManagementRestTransport._BaseGetOperation,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.GetOperation")

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
                _BaseGDCHardwareManagementRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseGDCHardwareManagementRestTransport._BaseListOperations,
        GDCHardwareManagementRestStub,
    ):
        def __hash__(self):
            return hash("GDCHardwareManagementRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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

            http_options = (
                _BaseGDCHardwareManagementRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseGDCHardwareManagementRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGDCHardwareManagementRestTransport._BaseListOperations._get_query_params_json(
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
                    f"Sending request for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GDCHardwareManagementRestTransport._ListOperations._get_response(
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
                    "Received response for google.cloud.gdchardwaremanagement_v1alpha.GDCHardwareManagementAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.gdchardwaremanagement.v1alpha.GDCHardwareManagement",
                        "rpcName": "ListOperations",
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


__all__ = ("GDCHardwareManagementRestTransport",)
