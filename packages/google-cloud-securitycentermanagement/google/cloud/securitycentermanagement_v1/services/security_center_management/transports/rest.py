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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.securitycentermanagement_v1.types import security_center_management

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSecurityCenterManagementRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SecurityCenterManagementRestInterceptor:
    """Interceptor for SecurityCenterManagement.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecurityCenterManagementRestTransport.

    .. code-block:: python
        class MyCustomSecurityCenterManagementInterceptor(SecurityCenterManagementRestInterceptor):
            def pre_create_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_event_threat_detection_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_security_health_analytics_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_effective_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_effective_event_threat_detection_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_effective_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_effective_security_health_analytics_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event_threat_detection_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_security_center_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_security_center_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_security_health_analytics_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_descendant_event_threat_detection_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_descendant_event_threat_detection_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_descendant_security_health_analytics_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_descendant_security_health_analytics_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_effective_event_threat_detection_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_effective_event_threat_detection_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_effective_security_health_analytics_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_effective_security_health_analytics_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_event_threat_detection_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_event_threat_detection_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_security_center_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_security_center_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_security_health_analytics_custom_modules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_security_health_analytics_custom_modules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_simulate_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_simulate_security_health_analytics_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_event_threat_detection_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_security_center_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_security_center_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_security_health_analytics_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_security_health_analytics_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_validate_event_threat_detection_custom_module(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_validate_event_threat_detection_custom_module(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecurityCenterManagementRestTransport(interceptor=MyCustomSecurityCenterManagementInterceptor())
        client = SecurityCenterManagementClient(transport=transport)


    """

    def pre_create_event_threat_detection_custom_module(
        self,
        request: security_center_management.CreateEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.CreateEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_create_event_threat_detection_custom_module(
        self, response: security_center_management.EventThreatDetectionCustomModule
    ) -> security_center_management.EventThreatDetectionCustomModule:
        """Post-rpc interceptor for create_event_threat_detection_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_create_security_health_analytics_custom_module(
        self,
        request: security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_create_security_health_analytics_custom_module(
        self, response: security_center_management.SecurityHealthAnalyticsCustomModule
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        """Post-rpc interceptor for create_security_health_analytics_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_delete_event_threat_detection_custom_module(
        self,
        request: security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def pre_delete_security_health_analytics_custom_module(
        self,
        request: security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def pre_get_effective_event_threat_detection_custom_module(
        self,
        request: security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_effective_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_effective_event_threat_detection_custom_module(
        self,
        response: security_center_management.EffectiveEventThreatDetectionCustomModule,
    ) -> security_center_management.EffectiveEventThreatDetectionCustomModule:
        """Post-rpc interceptor for get_effective_event_threat_detection_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_effective_security_health_analytics_custom_module(
        self,
        request: security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_effective_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_effective_security_health_analytics_custom_module(
        self,
        response: security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
    ) -> security_center_management.EffectiveSecurityHealthAnalyticsCustomModule:
        """Post-rpc interceptor for get_effective_security_health_analytics_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_event_threat_detection_custom_module(
        self,
        request: security_center_management.GetEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.GetEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_event_threat_detection_custom_module(
        self, response: security_center_management.EventThreatDetectionCustomModule
    ) -> security_center_management.EventThreatDetectionCustomModule:
        """Post-rpc interceptor for get_event_threat_detection_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_security_center_service(
        self,
        request: security_center_management.GetSecurityCenterServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.GetSecurityCenterServiceRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_security_center_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_security_center_service(
        self, response: security_center_management.SecurityCenterService
    ) -> security_center_management.SecurityCenterService:
        """Post-rpc interceptor for get_security_center_service

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_get_security_health_analytics_custom_module(
        self,
        request: security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_security_health_analytics_custom_module(
        self, response: security_center_management.SecurityHealthAnalyticsCustomModule
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        """Post-rpc interceptor for get_security_health_analytics_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_descendant_event_threat_detection_custom_modules(
        self,
        request: security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_descendant_event_threat_detection_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_descendant_event_threat_detection_custom_modules(
        self,
        response: security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse,
    ) -> (
        security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse
    ):
        """Post-rpc interceptor for list_descendant_event_threat_detection_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_descendant_security_health_analytics_custom_modules(
        self,
        request: security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_descendant_security_health_analytics_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_descendant_security_health_analytics_custom_modules(
        self,
        response: security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
    ) -> (
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse
    ):
        """Post-rpc interceptor for list_descendant_security_health_analytics_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_effective_event_threat_detection_custom_modules(
        self,
        request: security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_effective_event_threat_detection_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_effective_event_threat_detection_custom_modules(
        self,
        response: security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse,
    ) -> (
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse
    ):
        """Post-rpc interceptor for list_effective_event_threat_detection_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_effective_security_health_analytics_custom_modules(
        self,
        request: security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_effective_security_health_analytics_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_effective_security_health_analytics_custom_modules(
        self,
        response: security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
    ) -> (
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse
    ):
        """Post-rpc interceptor for list_effective_security_health_analytics_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_event_threat_detection_custom_modules(
        self,
        request: security_center_management.ListEventThreatDetectionCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListEventThreatDetectionCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_event_threat_detection_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_event_threat_detection_custom_modules(
        self,
        response: security_center_management.ListEventThreatDetectionCustomModulesResponse,
    ) -> security_center_management.ListEventThreatDetectionCustomModulesResponse:
        """Post-rpc interceptor for list_event_threat_detection_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_security_center_services(
        self,
        request: security_center_management.ListSecurityCenterServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListSecurityCenterServicesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_security_center_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_security_center_services(
        self, response: security_center_management.ListSecurityCenterServicesResponse
    ) -> security_center_management.ListSecurityCenterServicesResponse:
        """Post-rpc interceptor for list_security_center_services

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_list_security_health_analytics_custom_modules(
        self,
        request: security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_security_health_analytics_custom_modules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_security_health_analytics_custom_modules(
        self,
        response: security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse,
    ) -> security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse:
        """Post-rpc interceptor for list_security_health_analytics_custom_modules

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_simulate_security_health_analytics_custom_module(
        self,
        request: security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for simulate_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_simulate_security_health_analytics_custom_module(
        self,
        response: security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse,
    ) -> security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse:
        """Post-rpc interceptor for simulate_security_health_analytics_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_event_threat_detection_custom_module(
        self,
        request: security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_update_event_threat_detection_custom_module(
        self, response: security_center_management.EventThreatDetectionCustomModule
    ) -> security_center_management.EventThreatDetectionCustomModule:
        """Post-rpc interceptor for update_event_threat_detection_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_security_center_service(
        self,
        request: security_center_management.UpdateSecurityCenterServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.UpdateSecurityCenterServiceRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_security_center_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_update_security_center_service(
        self, response: security_center_management.SecurityCenterService
    ) -> security_center_management.SecurityCenterService:
        """Post-rpc interceptor for update_security_center_service

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_update_security_health_analytics_custom_module(
        self,
        request: security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_security_health_analytics_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_update_security_health_analytics_custom_module(
        self, response: security_center_management.SecurityHealthAnalyticsCustomModule
    ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
        """Post-rpc interceptor for update_security_health_analytics_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response

    def pre_validate_event_threat_detection_custom_module(
        self,
        request: security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for validate_event_threat_detection_custom_module

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_validate_event_threat_detection_custom_module(
        self,
        response: security_center_management.ValidateEventThreatDetectionCustomModuleResponse,
    ) -> security_center_management.ValidateEventThreatDetectionCustomModuleResponse:
        """Post-rpc interceptor for validate_event_threat_detection_custom_module

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
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
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
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
        before they are sent to the SecurityCenterManagement server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenterManagement server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecurityCenterManagementRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecurityCenterManagementRestInterceptor


class SecurityCenterManagementRestTransport(_BaseSecurityCenterManagementRestTransport):
    """REST backend synchronous transport for SecurityCenterManagement.

    Service describing handlers for resources

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "securitycentermanagement.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecurityCenterManagementRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'securitycentermanagement.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or SecurityCenterManagementRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.CreateEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.CreateEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.EventThreatDetectionCustomModule:
            r"""Call the create event threat
            detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.CreateEventThreatDetectionCustomModuleRequest):
                        The request object. Message for creating a
                    EventThreatDetectionCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.EventThreatDetectionCustomModule:
                        An event threat detection custom
                    module is a Cloud SCC resource that
                    contains the configuration and
                    enablement state of a custom module,
                    which enables ETD to write certain
                    findings to Cloud SCC.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._CreateEventThreatDetectionCustomModule._get_response(
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
            resp = security_center_management.EventThreatDetectionCustomModule()
            pb_resp = security_center_management.EventThreatDetectionCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_event_threat_detection_custom_module(
                resp
            )
            return resp

    class _CreateSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.CreateSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
            r"""Call the create security health
            analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Message for creating a
                    SecurityHealthAnalyticsCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SecurityHealthAnalyticsCustomModule:
                        Represents an instance of a Security
                    Health Analytics custom module,
                    including its full module name, display
                    name, enablement state, and last updated
                    time. You can create a custom module at
                    the organization, folder, or project
                    level. Custom modules that you create at
                    the organization or folder level are
                    inherited by the child folders and
                    projects.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._CreateSecurityHealthAnalyticsCustomModule._get_response(
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
            resp = security_center_management.SecurityHealthAnalyticsCustomModule()
            pb_resp = security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_create_security_health_analytics_custom_module(
                    resp
                )
            )
            return resp

    class _DeleteEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseDeleteEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.DeleteEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.DeleteEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete event threat
            detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.DeleteEventThreatDetectionCustomModuleRequest):
                        The request object. Message for deleting a
                    EventThreatDetectionCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseDeleteEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseDeleteEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseDeleteEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._DeleteEventThreatDetectionCustomModule._get_response(
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

    class _DeleteSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseDeleteSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.DeleteSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete security health
            analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Message for deleting a
                    SecurityHealthAnalyticsCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseDeleteSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseDeleteSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseDeleteSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._DeleteSecurityHealthAnalyticsCustomModule._get_response(
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

    class _GetEffectiveEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.GetEffectiveEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.EffectiveEventThreatDetectionCustomModule:
            r"""Call the get effective event
            threat detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest):
                        The request object. Message for getting a
                    EffectiveEventThreatDetectionCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.EffectiveEventThreatDetectionCustomModule:
                        An EffectiveEventThreatDetectionCustomModule is the
                    representation of EventThreatDetectionCustomModule at a
                    given level taking hierarchy into account and resolving
                    various fields accordingly. e.g. if the module is
                    enabled at the ancestor level, effective modules at all
                    descendant levels will have enablement_state set to
                    ENABLED. Similarly, if module.inherited is set, then
                    effective module's config will contain the ancestor's
                    config details.
                    EffectiveEventThreatDetectionCustomModule is read-only.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_effective_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetEffectiveEventThreatDetectionCustomModule._get_response(
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
            resp = (
                security_center_management.EffectiveEventThreatDetectionCustomModule()
            )
            pb_resp = (
                security_center_management.EffectiveEventThreatDetectionCustomModule.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_effective_event_threat_detection_custom_module(
                resp
            )
            return resp

    class _GetEffectiveSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.GetEffectiveSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.EffectiveSecurityHealthAnalyticsCustomModule:
            r"""Call the get effective security
            health analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Message for getting a
                    EffectiveSecurityHealthAnalyticsCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.EffectiveSecurityHealthAnalyticsCustomModule:
                        An EffectiveSecurityHealthAnalyticsCustomModule is the
                    representation of a Security Health Analytics custom
                    module at a specified level of the resource hierarchy:
                    organization, folder, or project. If a custom module is
                    inherited from a parent organization or folder, the
                    value of the ``enablementState`` property in
                    EffectiveSecurityHealthAnalyticsCustomModule is set to
                    the value that is effective in the parent, instead of
                    ``INHERITED``. For example, if the module is enabled in
                    a parent organization or folder, the effective
                    enablement_state for the module in all child folders or
                    projects is also ``enabled``.
                    EffectiveSecurityHealthAnalyticsCustomModule is
                    read-only.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_effective_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetEffectiveSecurityHealthAnalyticsCustomModule._get_response(
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
            resp = (
                security_center_management.EffectiveSecurityHealthAnalyticsCustomModule()
            )
            pb_resp = security_center_management.EffectiveSecurityHealthAnalyticsCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_effective_security_health_analytics_custom_module(
                resp
            )
            return resp

    class _GetEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseGetEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.GetEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.GetEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.EventThreatDetectionCustomModule:
            r"""Call the get event threat
            detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.GetEventThreatDetectionCustomModuleRequest):
                        The request object. Message for getting a
                    EventThreatDetectionCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.EventThreatDetectionCustomModule:
                        An event threat detection custom
                    module is a Cloud SCC resource that
                    contains the configuration and
                    enablement state of a custom module,
                    which enables ETD to write certain
                    findings to Cloud SCC.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetEventThreatDetectionCustomModule._get_response(
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
            resp = security_center_management.EventThreatDetectionCustomModule()
            pb_resp = security_center_management.EventThreatDetectionCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event_threat_detection_custom_module(resp)
            return resp

    class _GetSecurityCenterService(
        _BaseSecurityCenterManagementRestTransport._BaseGetSecurityCenterService,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.GetSecurityCenterService"
            )

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
            request: security_center_management.GetSecurityCenterServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.SecurityCenterService:
            r"""Call the get security center
            service method over HTTP.

                Args:
                    request (~.security_center_management.GetSecurityCenterServiceRequest):
                        The request object. Request message for getting a
                    Security Command Center service.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SecurityCenterService:
                        Represents a particular Security
                    Command Center service. This includes
                    settings information such as top-level
                    enablement in addition to individual
                    module settings. Service settings can be
                    configured at the organization, folder,
                    or project level. Service settings at
                    the organization or folder level are
                    inherited by those in child folders and
                    projects.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetSecurityCenterService._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_security_center_service(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetSecurityCenterService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetSecurityCenterService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetSecurityCenterService._get_response(
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
            resp = security_center_management.SecurityCenterService()
            pb_resp = security_center_management.SecurityCenterService.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_security_center_service(resp)
            return resp

    class _GetSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseGetSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.GetSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
            r"""Call the get security health
            analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Message for getting a
                    SecurityHealthAnalyticsCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SecurityHealthAnalyticsCustomModule:
                        Represents an instance of a Security
                    Health Analytics custom module,
                    including its full module name, display
                    name, enablement state, and last updated
                    time. You can create a custom module at
                    the organization, folder, or project
                    level. Custom modules that you create at
                    the organization or folder level are
                    inherited by the child folders and
                    projects.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetSecurityHealthAnalyticsCustomModule._get_response(
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
            resp = security_center_management.SecurityHealthAnalyticsCustomModule()
            pb_resp = security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_security_health_analytics_custom_module(
                resp
            )
            return resp

    class _ListDescendantEventThreatDetectionCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListDescendantEventThreatDetectionCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListDescendantEventThreatDetectionCustomModules"
            )

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
            request: security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse
        ):
            r"""Call the list descendant event
            threat detection custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest):
                        The request object. Request message for listing
                    descendant Event Threat Detection custom
                    modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse:
                        Response message for listing
                    descendant Event Threat Detection custom
                    modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListDescendantEventThreatDetectionCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_descendant_event_threat_detection_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListDescendantEventThreatDetectionCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListDescendantEventThreatDetectionCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListDescendantEventThreatDetectionCustomModules._get_response(
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
            resp = (
                security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse()
            )
            pb_resp = security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_descendant_event_threat_detection_custom_modules(
                resp
            )
            return resp

    class _ListDescendantSecurityHealthAnalyticsCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListDescendantSecurityHealthAnalyticsCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListDescendantSecurityHealthAnalyticsCustomModules"
            )

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
            request: security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse
        ):
            r"""Call the list descendant security
            health analytics custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest):
                        The request object. Request message for listing
                    descendant Security Health Analytics
                    custom modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse:
                        Response message for listing
                    descendant Security Health Analytics
                    custom modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListDescendantSecurityHealthAnalyticsCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_descendant_security_health_analytics_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListDescendantSecurityHealthAnalyticsCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListDescendantSecurityHealthAnalyticsCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListDescendantSecurityHealthAnalyticsCustomModules._get_response(
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
            resp = (
                security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse()
            )
            pb_resp = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_descendant_security_health_analytics_custom_modules(
                resp
            )
            return resp

    class _ListEffectiveEventThreatDetectionCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListEffectiveEventThreatDetectionCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListEffectiveEventThreatDetectionCustomModules"
            )

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
            request: security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse
        ):
            r"""Call the list effective event
            threat detection custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest):
                        The request object. Request message for listing effective
                    Event Threat Detection custom modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse:
                        Response message for listing
                    effective Event Threat Detection custom
                    modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListEffectiveEventThreatDetectionCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_effective_event_threat_detection_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListEffectiveEventThreatDetectionCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListEffectiveEventThreatDetectionCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListEffectiveEventThreatDetectionCustomModules._get_response(
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
            resp = (
                security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse()
            )
            pb_resp = security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_effective_event_threat_detection_custom_modules(
                resp
            )
            return resp

    class _ListEffectiveSecurityHealthAnalyticsCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListEffectiveSecurityHealthAnalyticsCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListEffectiveSecurityHealthAnalyticsCustomModules"
            )

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
            request: security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse
        ):
            r"""Call the list effective security
            health analytics custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest):
                        The request object. Request message for listing effective
                    Security Health Analytics custom
                    modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse:
                        Response message for listing
                    effective Security Health Analytics
                    custom modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListEffectiveSecurityHealthAnalyticsCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_effective_security_health_analytics_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListEffectiveSecurityHealthAnalyticsCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListEffectiveSecurityHealthAnalyticsCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListEffectiveSecurityHealthAnalyticsCustomModules._get_response(
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
            resp = (
                security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse()
            )
            pb_resp = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_effective_security_health_analytics_custom_modules(
                resp
            )
            return resp

    class _ListEventThreatDetectionCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListEventThreatDetectionCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListEventThreatDetectionCustomModules"
            )

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
            request: security_center_management.ListEventThreatDetectionCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.ListEventThreatDetectionCustomModulesResponse:
            r"""Call the list event threat
            detection custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListEventThreatDetectionCustomModulesRequest):
                        The request object. Request message for listing Event
                    Threat Detection custom modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListEventThreatDetectionCustomModulesResponse:
                        Response message for listing Event
                    Threat Detection custom modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListEventThreatDetectionCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_event_threat_detection_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListEventThreatDetectionCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListEventThreatDetectionCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListEventThreatDetectionCustomModules._get_response(
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
            resp = (
                security_center_management.ListEventThreatDetectionCustomModulesResponse()
            )
            pb_resp = security_center_management.ListEventThreatDetectionCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_event_threat_detection_custom_modules(
                resp
            )
            return resp

    class _ListSecurityCenterServices(
        _BaseSecurityCenterManagementRestTransport._BaseListSecurityCenterServices,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListSecurityCenterServices"
            )

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
            request: security_center_management.ListSecurityCenterServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.ListSecurityCenterServicesResponse:
            r"""Call the list security center
            services method over HTTP.

                Args:
                    request (~.security_center_management.ListSecurityCenterServicesRequest):
                        The request object. Request message for listing Security
                    Command Center services.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListSecurityCenterServicesResponse:
                        Response message for listing Security
                    Command Center services.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListSecurityCenterServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_security_center_services(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListSecurityCenterServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListSecurityCenterServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListSecurityCenterServices._get_response(
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
            resp = security_center_management.ListSecurityCenterServicesResponse()
            pb_resp = security_center_management.ListSecurityCenterServicesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_security_center_services(resp)
            return resp

    class _ListSecurityHealthAnalyticsCustomModules(
        _BaseSecurityCenterManagementRestTransport._BaseListSecurityHealthAnalyticsCustomModules,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ListSecurityHealthAnalyticsCustomModules"
            )

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
            request: security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse
        ):
            r"""Call the list security health
            analytics custom modules method over HTTP.

                Args:
                    request (~.security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest):
                        The request object. Request message for listing Security
                    Health Analytics custom modules.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse:
                        Response message for listing Security
                    Health Analytics custom modules.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListSecurityHealthAnalyticsCustomModules._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_security_health_analytics_custom_modules(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListSecurityHealthAnalyticsCustomModules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListSecurityHealthAnalyticsCustomModules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ListSecurityHealthAnalyticsCustomModules._get_response(
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
            resp = (
                security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse()
            )
            pb_resp = security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_security_health_analytics_custom_modules(
                resp
            )
            return resp

    class _SimulateSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.SimulateSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse
        ):
            r"""Call the simulate security health
            analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Request message to simulate a
                    CustomConfig against a given test
                    resource. Maximum size of the request is
                    4 MB by default.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse:
                        Response message for simulating a
                    ``SecurityHealthAnalyticsCustomModule`` against a given
                    resource.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_simulate_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._SimulateSecurityHealthAnalyticsCustomModule._get_response(
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
            resp = (
                security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse()
            )
            pb_resp = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_simulate_security_health_analytics_custom_module(
                    resp
                )
            )
            return resp

    class _UpdateEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.UpdateEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.UpdateEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.EventThreatDetectionCustomModule:
            r"""Call the update event threat
            detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.UpdateEventThreatDetectionCustomModuleRequest):
                        The request object. Message for updating a
                    EventThreatDetectionCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.EventThreatDetectionCustomModule:
                        An event threat detection custom
                    module is a Cloud SCC resource that
                    contains the configuration and
                    enablement state of a custom module,
                    which enables ETD to write certain
                    findings to Cloud SCC.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._UpdateEventThreatDetectionCustomModule._get_response(
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
            resp = security_center_management.EventThreatDetectionCustomModule()
            pb_resp = security_center_management.EventThreatDetectionCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_event_threat_detection_custom_module(
                resp
            )
            return resp

    class _UpdateSecurityCenterService(
        _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.UpdateSecurityCenterService"
            )

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
            request: security_center_management.UpdateSecurityCenterServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.SecurityCenterService:
            r"""Call the update security center
            service method over HTTP.

                Args:
                    request (~.security_center_management.UpdateSecurityCenterServiceRequest):
                        The request object. Request message for updating a
                    Security Command Center service.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SecurityCenterService:
                        Represents a particular Security
                    Command Center service. This includes
                    settings information such as top-level
                    enablement in addition to individual
                    module settings. Service settings can be
                    configured at the organization, folder,
                    or project level. Service settings at
                    the organization or folder level are
                    inherited by those in child folders and
                    projects.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_security_center_service(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._UpdateSecurityCenterService._get_response(
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
            resp = security_center_management.SecurityCenterService()
            pb_resp = security_center_management.SecurityCenterService.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_security_center_service(resp)
            return resp

    class _UpdateSecurityHealthAnalyticsCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.UpdateSecurityHealthAnalyticsCustomModule"
            )

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
            request: security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> security_center_management.SecurityHealthAnalyticsCustomModule:
            r"""Call the update security health
            analytics custom module method over HTTP.

                Args:
                    request (~.security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest):
                        The request object. Message for updating a
                    SecurityHealthAnalyticsCustomModule
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.SecurityHealthAnalyticsCustomModule:
                        Represents an instance of a Security
                    Health Analytics custom module,
                    including its full module name, display
                    name, enablement state, and last updated
                    time. You can create a custom module at
                    the organization, folder, or project
                    level. Custom modules that you create at
                    the organization or folder level are
                    inherited by the child folders and
                    projects.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_security_health_analytics_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._UpdateSecurityHealthAnalyticsCustomModule._get_response(
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
            resp = security_center_management.SecurityHealthAnalyticsCustomModule()
            pb_resp = security_center_management.SecurityHealthAnalyticsCustomModule.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_update_security_health_analytics_custom_module(
                    resp
                )
            )
            return resp

    class _ValidateEventThreatDetectionCustomModule(
        _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash(
                "SecurityCenterManagementRestTransport.ValidateEventThreatDetectionCustomModule"
            )

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
            request: security_center_management.ValidateEventThreatDetectionCustomModuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> (
            security_center_management.ValidateEventThreatDetectionCustomModuleResponse
        ):
            r"""Call the validate event threat
            detection custom module method over HTTP.

                Args:
                    request (~.security_center_management.ValidateEventThreatDetectionCustomModuleRequest):
                        The request object. Request to validate an Event Threat
                    Detection custom module.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.security_center_management.ValidateEventThreatDetectionCustomModuleResponse:
                        Response to validating an Event
                    Threat Detection custom module.

            """

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_validate_event_threat_detection_custom_module(
                request, metadata
            )
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._ValidateEventThreatDetectionCustomModule._get_response(
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
            resp = (
                security_center_management.ValidateEventThreatDetectionCustomModuleResponse()
            )
            pb_resp = security_center_management.ValidateEventThreatDetectionCustomModuleResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_validate_event_threat_detection_custom_module(
                resp
            )
            return resp

    @property
    def create_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [security_center_management.CreateEventThreatDetectionCustomModuleRequest],
        security_center_management.EventThreatDetectionCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest],
        security_center_management.SecurityHealthAnalyticsCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [security_center_management.DeleteEventThreatDetectionCustomModuleRequest],
        empty_pb2.Empty,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest],
        empty_pb2.Empty,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_effective_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [
            security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest
        ],
        security_center_management.EffectiveEventThreatDetectionCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEffectiveEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_effective_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [
            security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest
        ],
        security_center_management.EffectiveSecurityHealthAnalyticsCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEffectiveSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [security_center_management.GetEventThreatDetectionCustomModuleRequest],
        security_center_management.EventThreatDetectionCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_security_center_service(
        self,
    ) -> Callable[
        [security_center_management.GetSecurityCenterServiceRequest],
        security_center_management.SecurityCenterService,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSecurityCenterService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest],
        security_center_management.SecurityHealthAnalyticsCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_descendant_event_threat_detection_custom_modules(
        self,
    ) -> Callable[
        [
            security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest
        ],
        security_center_management.ListDescendantEventThreatDetectionCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDescendantEventThreatDetectionCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_descendant_security_health_analytics_custom_modules(
        self,
    ) -> Callable[
        [
            security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest
        ],
        security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDescendantSecurityHealthAnalyticsCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_effective_event_threat_detection_custom_modules(
        self,
    ) -> Callable[
        [
            security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest
        ],
        security_center_management.ListEffectiveEventThreatDetectionCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEffectiveEventThreatDetectionCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_effective_security_health_analytics_custom_modules(
        self,
    ) -> Callable[
        [
            security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest
        ],
        security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEffectiveSecurityHealthAnalyticsCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_event_threat_detection_custom_modules(
        self,
    ) -> Callable[
        [security_center_management.ListEventThreatDetectionCustomModulesRequest],
        security_center_management.ListEventThreatDetectionCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEventThreatDetectionCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_security_center_services(
        self,
    ) -> Callable[
        [security_center_management.ListSecurityCenterServicesRequest],
        security_center_management.ListSecurityCenterServicesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSecurityCenterServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_security_health_analytics_custom_modules(
        self,
    ) -> Callable[
        [security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest],
        security_center_management.ListSecurityHealthAnalyticsCustomModulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSecurityHealthAnalyticsCustomModules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def simulate_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest],
        security_center_management.SimulateSecurityHealthAnalyticsCustomModuleResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SimulateSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [security_center_management.UpdateEventThreatDetectionCustomModuleRequest],
        security_center_management.EventThreatDetectionCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_security_center_service(
        self,
    ) -> Callable[
        [security_center_management.UpdateSecurityCenterServiceRequest],
        security_center_management.SecurityCenterService,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSecurityCenterService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_security_health_analytics_custom_module(
        self,
    ) -> Callable[
        [security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest],
        security_center_management.SecurityHealthAnalyticsCustomModule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSecurityHealthAnalyticsCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def validate_event_threat_detection_custom_module(
        self,
    ) -> Callable[
        [security_center_management.ValidateEventThreatDetectionCustomModuleRequest],
        security_center_management.ValidateEventThreatDetectionCustomModuleResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ValidateEventThreatDetectionCustomModule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseSecurityCenterManagementRestTransport._BaseGetLocation,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash("SecurityCenterManagementRestTransport.GetLocation")

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

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecurityCenterManagementRestTransport._GetLocation._get_response(
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
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseSecurityCenterManagementRestTransport._BaseListLocations,
        SecurityCenterManagementRestStub,
    ):
        def __hash__(self):
            return hash("SecurityCenterManagementRestTransport.ListLocations")

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

            http_options = (
                _BaseSecurityCenterManagementRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseSecurityCenterManagementRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecurityCenterManagementRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecurityCenterManagementRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SecurityCenterManagementRestTransport",)
